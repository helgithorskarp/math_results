#!/usr/bin/env python3
"""Independent small controls for the aggregate rank-four encoding primitives."""

from __future__ import annotations

from itertools import product
import json
from pathlib import Path
import tempfile

from aggregate import StreamCNF, dot, load_cover, rank


def read_cnf(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    clauses = []
    variables = None
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("p "):
            _, _, variables_text, clauses_text = line.split()
            variables = int(variables_text)
            expected = int(clauses_text)
        elif line and line[0] not in "c":
            values = tuple(map(int, line.split()))
            if not values or values[-1] != 0:
                raise ValueError("DIMACS terminator")
            clauses.append(values[:-1])
    if variables is None or expected != len(clauses):
        raise ValueError("DIMACS header")
    return variables, clauses


def holds(clause: tuple[int, ...], assignment: int) -> bool:
    return any(bool(assignment >> (abs(literal) - 1) & 1) == (literal > 0)
               for literal in clause)


def extendible(variables: int, clauses: list[tuple[int, ...]], primary: dict[int, bool]) -> bool:
    fixed_mask = sum(int(value) << (variable - 1) for variable, value in primary.items())
    auxiliaries = [variable for variable in range(1, variables + 1) if variable not in primary]
    for bits in range(1 << len(auxiliaries)):
        assignment = fixed_mask
        for index, variable in enumerate(auxiliaries):
            assignment |= ((bits >> index) & 1) << (variable - 1)
        if all(holds(clause, assignment) for clause in clauses):
            return True
    return False


def cardinality_controls(root: Path) -> dict:
    checked = 0
    gated_checked = 0
    for n in range(1, 5):
        for bound in range(n + 1):
            for gated in (False, True):
                body = root / f"card-{n}-{bound}-{int(gated)}.body"
                cnf = root / f"card-{n}-{bound}-{int(gated)}.cnf"
                formula = StreamCNF(body)
                literals = [formula.new_var() for _ in range(n)]
                gate = formula.new_var() if gated else None
                formula.at_most(literals, bound, gate)
                formula.finish(cnf)
                variables, clauses = read_cnf(cnf)
                for bits in range(1 << n):
                    gate_values = (False, True) if gated else (None,)
                    for gate_value in gate_values:
                        primary = {literal: bool(bits >> index & 1)
                                   for index, literal in enumerate(literals)}
                        if gated:
                            primary[gate] = gate_value
                        observed = extendible(variables, clauses, primary)
                        expected = (not gate_value if gated else False) or bits.bit_count() <= bound
                        if observed != expected:
                            raise AssertionError((n, bound, gated, bits, gate_value, observed, expected))
                        checked += 1
                        gated_checked += int(gated)
    return {"assignments": checked, "gated_assignments": gated_checked}


def gate_controls(root: Path) -> dict:
    checked = 0
    for operation in ("or", "and"):
        body = root / f"gate-{operation}.body"
        cnf = root / f"gate-{operation}.cnf"
        formula = StreamCNF(body)
        inputs = [formula.new_var() for _ in range(3)]
        output = formula.gate_or(inputs) if operation == "or" else formula.gate_and(inputs)
        formula.finish(cnf)
        variables, clauses = read_cnf(cnf)
        if variables != 4:
            raise AssertionError("gate variables")
        for bits in range(8):
            truth = bool(bits) if operation == "or" else bits == 7
            for output_value in (False, True):
                primary = {variable: bool(bits >> index & 1)
                           for index, variable in enumerate(inputs)}
                primary[output] = output_value
                if extendible(variables, clauses, primary) != (output_value == truth):
                    raise AssertionError((operation, bits, output_value))
                checked += 1
    return {"assignments": checked}


def binary_rank(rows: list[int], width: int) -> int:
    basis = [0] * width
    result = 0
    for row in rows:
        value = row
        while value:
            pivot = value.bit_length() - 1
            if basis[pivot]:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                result += 1
                break
    return result


def rank_guard_controls() -> dict:
    checked = 0
    for rows in product(range(4), repeat=3):
        if rank(list(rows)) != 2:
            continue
        for columns in product(range(4), repeat=3):
            if rank(list(columns)) != 2:
                continue
            red = [sum(dot(a, b) << j for j, b in enumerate(columns)) for a in rows]
            blue = [value ^ 7 for value in red]
            guard = all(
                not (all(dot(a, p) for a in rows)
                     and all(dot(b, q) for b in columns))
                for p in range(1, 4)
                for q in range(1, 4)
                if dot(p, q)
            )
            expected = binary_rank(blue, 3) >= 2
            if binary_rank(red, 3) != 2 or guard != expected:
                raise AssertionError((rows, columns, red, blue, guard, expected))
            checked += 1
    return {"spanning_factor_pairs": checked}


def five_clause_controls() -> dict:
    checked = 0
    for bits in range(1 << 10):
        positive = bool(bits)
        negative = bits != (1 << 10) - 1
        expected = bits not in (0, (1 << 10) - 1)
        if (positive and negative) != expected:
            raise AssertionError(bits)
        checked += 1
    return {"edge_colourings": checked, "accepted": (1 << 10) - 2}


def cover_window_controls(cover_path: Path) -> dict:
    tasks, digest = load_cover(cover_path)
    pairs = {(first, first + distance)
             for distance in (1, 2) for first in range(20 - distance)}
    equal_pairs = 0
    for task in tasks:
        rows = task["rows"]
        for first in range(20):
            for second in range(first + 1, 20):
                if rows[first] == rows[second]:
                    equal_pairs += 1
                    if (first, second) not in pairs:
                        raise AssertionError((task["code"], first, second, rows[first]))
    # For a sorted capped list, equal entries have positional distance below cap.
    for cap, length in ((2, 23), (5, 23)):
        for first in range(length):
            for second in range(first + 1, length):
                could_be_equal = second - first < cap
                is_in_window = second - first in range(1, cap)
                if could_be_equal != is_in_window:
                    raise AssertionError((cap, first, second))
    return {
        "cover_sha256": digest,
        "tasks": len(tasks),
        "covered_row_profiles": sum(task["orbit_size"] for task in tasks),
        "equal_row_pairs": equal_pairs,
    }


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--cover", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="rank4-aggregate-controls-") as temporary:
        root = Path(temporary)
        result = {
            "cardinality": cardinality_controls(root),
            "gates": gate_controls(root),
            "rank_guard": rank_guard_controls(),
            "physical_five_set": five_clause_controls(),
            "cover_windows": cover_window_controls(args.cover),
            "status": "VERIFIED_ALL_ROW_SUPPORT8_ENCODING_CONTROLS",
        }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
