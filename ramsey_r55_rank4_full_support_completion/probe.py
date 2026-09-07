#!/usr/bin/env python3
"""Search for physical Ramsey(5,5) completions of retained rank-four cuts.

The fixed cut is represented by full-support factor multisets in F_2^4:
five of the 15 nonzero row labels are doubled and eight nonzero column labels
are doubled.  Affine-hyperplane column doubles are excluded by the published
affine-family theorem.  Every other such pair passes the published rank-four
class and contact filters.  For a fixed cut, the 443 within-side edges are SAT
variables and every monochromatic five-set contributes its literal clause.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import random
import subprocess
import tempfile
import time


N = 43
LEFT = 20
PAIRS = list(combinations(range(N), 2))
INTERNAL = [(u, v) for u, v in PAIRS if (u < LEFT) == (v < LEFT)]
INTERNAL_VAR = {edge: i + 1 for i, edge in enumerate(INTERNAL)}


def dot(x: int, y: int) -> int:
    return (x & y).bit_count() & 1


def affine_hyperplane(values: set[int]) -> bool:
    return any(values == {y for y in range(1, 16) if dot(w, y)}
               for w in range(1, 16))


def factor_lists(row_doubles: tuple[int, ...],
                 column_doubles: tuple[int, ...]) -> tuple[list[int], list[int]]:
    if len(row_doubles) != 5 or len(set(row_doubles)) != 5:
        raise ValueError("row_doubles must contain five distinct labels")
    if len(column_doubles) != 8 or len(set(column_doubles)) != 8:
        raise ValueError("column_doubles must contain eight distinct labels")
    if any(x not in range(1, 16) for x in row_doubles + column_doubles):
        raise ValueError("factor labels must lie in 1..15")
    if affine_hyperplane(set(column_doubles)):
        raise ValueError("affine-hyperplane column doubles are already excluded")
    rows = list(range(1, 16)) + list(row_doubles)
    columns = list(range(1, 16)) + list(column_doubles)
    return rows, columns


def fixed_cross(rows: list[int], columns: list[int]) -> dict[tuple[int, int], int]:
    return {(i, LEFT + j): dot(x, y)
            for i, x in enumerate(rows) for j, y in enumerate(columns)}


def clauses_for_cut_reference(rows: list[int], columns: list[int]) -> list[list[int]]:
    cross = fixed_cross(rows, columns)
    clauses: list[list[int]] = []
    for vertices in combinations(range(N), 5):
        internal_literals: list[int] = []
        red_possible = True
        blue_possible = True
        for u, v in combinations(vertices, 2):
            if (u < LEFT) != (v < LEFT):
                color = cross[(u, v)]
                red_possible &= color == 1
                blue_possible &= color == 0
            else:
                internal_literals.append(INTERNAL_VAR[(u, v)])
        if red_possible:
            clauses.append([-v for v in internal_literals])
        if blue_possible:
            clauses.append(internal_literals)
    return clauses


def clauses_for_cut(rows: list[int], columns: list[int]) -> list[list[int]]:
    """Generate the same clauses by common-contact sets instead of all five-sets."""
    clauses: list[list[int]] = []

    def internal_pairs(vertices):
        return [INTERNAL_VAR[edge] for edge in combinations(vertices, 2)]

    # Five-sets lying in one side are independent of the fixed cut.
    for vertices in combinations(range(LEFT), 5):
        variables = internal_pairs(vertices)
        clauses.append([-v for v in variables])
        clauses.append(variables)
    for vertices in combinations(range(LEFT, N), 5):
        variables = internal_pairs(vertices)
        clauses.append([-v for v in variables])
        clauses.append(variables)

    red_contacts = [tuple(LEFT + j for j, y in enumerate(columns) if dot(x, y))
                    for x in rows]
    blue_contacts = [tuple(LEFT + j for j, y in enumerate(columns) if not dot(x, y))
                     for x in rows]

    # One left and four right vertices.
    for i in range(LEFT):
        for contacts, sign in ((red_contacts[i], -1), (blue_contacts[i], 1)):
            for right in combinations(contacts, 4):
                variables = internal_pairs(right)
                clauses.append([sign * v for v in variables])

    # Two left and three right vertices.
    for left in combinations(range(LEFT), 2):
        left_variable = INTERNAL_VAR[left]
        for color, sign in ((1, -1), (0, 1)):
            contacts = [LEFT + j for j, y in enumerate(columns)
                        if all(dot(rows[i], y) == color for i in left)]
            for right in combinations(contacts, 3):
                variables = [left_variable] + internal_pairs(right)
                clauses.append([sign * v for v in variables])

    # Three left and two right vertices.
    for left in combinations(range(LEFT), 3):
        left_variables = internal_pairs(left)
        for color, sign in ((1, -1), (0, 1)):
            contacts = [LEFT + j for j, y in enumerate(columns)
                        if all(dot(rows[i], y) == color for i in left)]
            for right in combinations(contacts, 2):
                variables = left_variables + internal_pairs(right)
                clauses.append([sign * v for v in variables])

    # Four left and one right vertex.
    for j, y in enumerate(columns):
        for color, sign in ((1, -1), (0, 1)):
            contacts = [i for i, x in enumerate(rows) if dot(x, y) == color]
            for left in combinations(contacts, 4):
                variables = internal_pairs(left)
                clauses.append([sign * v for v in variables])
    return clauses


def dimacs(clauses: list[list[int]]) -> bytes:
    lines = [f"p cnf {len(INTERNAL)} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode("ascii")


def read_assignment(path: Path) -> list[bool]:
    text = path.read_text(encoding="ascii")
    if "s SATISFIABLE" not in text:
        raise ValueError("missing SAT status in solver witness")
    values: dict[int, bool] = {}
    for line in text.splitlines():
        if not line.startswith("v"):
            continue
        for literal in map(int, line.split()[1:]):
            if literal:
                values[abs(literal)] = literal > 0
    if set(values) != set(range(1, len(INTERNAL) + 1)):
        raise ValueError("solver witness does not assign all internal edges")
    return [values[i] for i in range(1, len(INTERNAL) + 1)]


def red_bits(rows: list[int], columns: list[int], assignment: list[bool]) -> int:
    cross = fixed_cross(rows, columns)
    bits = 0
    internal_index = {edge: i for i, edge in enumerate(INTERNAL)}
    for k, edge in enumerate(PAIRS):
        if (edge[0] < LEFT) != (edge[1] < LEFT):
            red = cross[edge]
        else:
            red = assignment[internal_index[edge]]
        bits |= int(red) << k
    return bits


def bad_fives(bits: int) -> tuple[list[int] | None, list[int] | None]:
    red_bad = None
    blue_bad = None
    pair_index = {edge: i for i, edge in enumerate(PAIRS)}
    for vertices in combinations(range(N), 5):
        colors = [bool((bits >> pair_index[edge]) & 1)
                  for edge in combinations(vertices, 2)]
        if red_bad is None and all(colors):
            red_bad = list(vertices)
        if blue_bad is None and not any(colors):
            blue_bad = list(vertices)
        if red_bad is not None and blue_bad is not None:
            break
    return red_bad, blue_bad


def solve_one(solver: str, seconds: int, row_doubles: tuple[int, ...],
              column_doubles: tuple[int, ...], scratch: Path) -> dict:
    rows, columns = factor_lists(row_doubles, column_doubles)
    clauses = clauses_for_cut(rows, columns)
    raw = dimacs(clauses)
    stem = sha256(bytes(row_doubles + column_doubles)).hexdigest()[:16]
    cnf = scratch / f"{stem}.cnf"
    witness = scratch / f"{stem}.sol"
    cnf.write_bytes(raw)
    started = time.monotonic()
    run = subprocess.run(
        [solver, "-q", "--sat", "-t", str(seconds), "-w", str(witness), str(cnf)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
        timeout=seconds + 10,
    )
    elapsed = time.monotonic() - started
    result = {
        "row_doubles": list(row_doubles),
        "column_doubles": list(column_doubles),
        "variables": len(INTERNAL),
        "clauses": len(clauses),
        "cnf_sha256": sha256(raw).hexdigest(),
        "solver_exit": run.returncode,
        "seconds": elapsed,
    }
    if run.returncode == 10:
        assignment = read_assignment(witness)
        bits = red_bits(rows, columns, assignment)
        red_bad, blue_bad = bad_fives(bits)
        if red_bad is not None or blue_bad is not None:
            raise RuntimeError(f"invalid solver model: red={red_bad}, blue={blue_bad}")
        result.update({
            "status": "SAT_GOOD43",
            "rows": rows,
            "columns": columns,
            "internal_hex": format(sum(int(x) << i for i, x in enumerate(assignment)), "0111x"),
            "red_hex": format(bits, "0226x"),
        })
    elif run.returncode == 20:
        result["status"] = "UNSAT"
    else:
        result["status"] = "UNKNOWN"
        result["solver_output_tail"] = run.stdout[-1000:]
    cnf.unlink()
    if witness.exists():
        witness.unlink()
    return result


def sampled_pairs(seed: int, count: int):
    rng = random.Random(seed)
    seen = set()
    while len(seen) < count:
        row = tuple(sorted(rng.sample(range(1, 16), 5)))
        column = tuple(sorted(rng.sample(range(1, 16), 8)))
        if affine_hyperplane(set(column)) or (row, column) in seen:
            continue
        seen.add((row, column))
        yield row, column


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", required=True)
    parser.add_argument("--seconds", type=int, default=10)
    parser.add_argument("--samples", type=int, default=16)
    parser.add_argument("--seed", type=int, default=550043)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--scratch", type=Path)
    args = parser.parse_args()
    if args.samples < 1 or args.seconds < 1:
        raise ValueError("positive sample count and time limit required")
    scratch_parent = args.scratch
    with tempfile.TemporaryDirectory(dir=scratch_parent) as tmp:
        results = []
        for row, column in sampled_pairs(args.seed, args.samples):
            result = solve_one(args.solver, args.seconds, row, column, Path(tmp))
            results.append(result)
            print(json.dumps(result, sort_keys=True), flush=True)
            if result["status"] == "SAT_GOOD43":
                break
    payload = {
        "schema": "rank4-physical-completion-probe-v1",
        "seed": args.seed,
        "requested_samples": args.samples,
        "seconds_per_instance": args.seconds,
        "solver": subprocess.run([args.solver, "--version"], capture_output=True,
                                 text=True, check=True).stdout.strip(),
        "results": results,
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")


if __name__ == "__main__":
    main()
