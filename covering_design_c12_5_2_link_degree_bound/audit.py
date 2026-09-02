#!/usr/bin/env python3
"""Independent finite audits for the orbit and cardinality reductions."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path

import generate_instances as producer


def valid_labeled_signatures() -> list[tuple[int, ...]]:
    result = []
    # Stars-and-bars iteration, independent of the producer's recursion.
    for bars in itertools.combinations(range(18), 7):
        stops = (-1,) + bars + (18,)
        counts = tuple(stops[i + 1] - stops[i] - 1 for i in range(8))
        rows = [
            tuple(mask for mask, count in enumerate(counts) for _ in range(count)
                  if (mask >> row) & 1)
            for row in range(3)
        ]
        if tuple(map(len, rows)) != (5, 5, 5) or len(set(rows)) != 3:
            continue
        result.append(counts)
    return result


def permute_counts(counts: tuple[int, ...], permutation: tuple[int, ...]):
    image = [0] * 8
    for mask, count in enumerate(counts):
        new_mask = sum(((mask >> row) & 1) << permutation[row] for row in range(3))
        image[new_mask] = count
    return tuple(image)


def satisfiable_with_fixed_inputs(clauses: list[list[int]], fixed: dict[int, bool]) -> bool:
    """Tiny independent DPLL used only on n <= 7 sequential counters."""
    assignment = dict(fixed)

    def search() -> bool:
        while True:
            unit = None
            for clause in clauses:
                unresolved = []
                satisfied = False
                for literal in clause:
                    value = assignment.get(abs(literal))
                    if value is None:
                        unresolved.append(literal)
                    elif value == (literal > 0):
                        satisfied = True
                        break
                if satisfied:
                    continue
                if not unresolved:
                    return False
                if len(unresolved) == 1:
                    unit = unresolved[0]
                    break
            if unit is None:
                break
            variable, value = abs(unit), unit > 0
            old = assignment.get(variable)
            if old is not None and old != value:
                return False
            assignment[variable] = value

        branch = next(
            (abs(literal) for clause in clauses for literal in clause
             if abs(literal) not in assignment),
            None,
        )
        if branch is None:
            return True
        snapshot = dict(assignment)
        for value in (False, True):
            assignment[branch] = value
            if search():
                return True
            assignment.clear()
            assignment.update(snapshot)
        return False

    return search()


def cardinality_audit() -> None:
    # Exhaustively verify equisatisfiability of the sequential counter for small n.
    for n in range(2, 8):
        for bound in range(1, n):
            variables = list(range(1, n + 1))
            clauses, largest = producer.at_most(variables, bound, n)
            for values in itertools.product((False, True), repeat=n):
                expected = sum(values) <= bound
                fixed = dict(zip(variables, values))
                extension_exists = satisfiable_with_fixed_inputs(clauses, fixed)
                assert extension_exists == expected, (n, bound, values)


def symbolic_degree_seven_audit() -> None:
    # h=1: audit the exact fractional edge-weight inequality for all class counts.
    for i in range(2):
        for x in range(5):
            for y in range(5):
                for z in range(3):
                    if i + x + y + z != 4:
                        continue
                    weight = (
                        Fraction(x * y, 4)
                        + Fraction(z * (x + y), 6)
                        + Fraction(7 * i * z, 24)
                        + Fraction(z * (z - 1), 24)
                    )
                    assert weight <= 1, (i, x, y, z, weight)

    # h=2: audit the three residual sorted Z-incidence multisets.
    survivors = []
    for counts in itertools.combinations_with_replacement(range(4), 7):
        if sum(counts) < 12:
            continue
        if sum(z * (z - 1) // 2 for z in counts) < 3:
            continue
        if sum(z * (4 - z) for z in counts) < 24:
            continue
        if sum((4 - z) ** 2 // 4 for z in counts) < 9:
            continue
        survivors.append(counts)
    assert survivors == [
        (0, 2, 2, 2, 2, 2, 2),
        (1, 1, 1, 2, 2, 2, 3),
        (1, 1, 2, 2, 2, 2, 2),
    ]


def witness_audit() -> None:
    path = Path(__file__).with_name("degree_five_witness.json")
    payload = json.loads(path.read_text())
    blocks = [tuple(block) for block in payload["blocks"]]
    assert len(blocks) == len(set(blocks)) == 9
    assert all(len(block) == len(set(block)) == 5 for block in blocks)
    assert all(
        any(set(pair) <= set(block) for block in blocks)
        for pair in itertools.combinations(range(12), 2)
    )
    degrees = [sum(point in block for block in blocks) for point in range(12)]
    assert degrees == payload["point_degrees"]
    assert max(degrees) == 5


def main() -> None:
    labeled = valid_labeled_signatures()
    assert len(labeled) == 110
    identity = (0, 1, 2)
    transposition = (1, 0, 2)
    three_cycle = (1, 2, 0)
    fixed = tuple(
        sum(permute_counts(counts, permutation) == counts for counts in labeled)
        for permutation in (identity, transposition, three_cycle)
    )
    assert fixed == (110, 28, 8)
    assert (fixed[0] + 3 * fixed[1] + 2 * fixed[2]) // 6 == 35
    assert len(producer.degree_six_representatives()) == 35
    assert [entry["intersection"] for entry in producer.degree_seven_representatives()] == list(range(5))
    cardinality_audit()
    symbolic_degree_seven_audit()
    witness_audit()
    print(json.dumps({"audit": "PASS", "labeled": len(labeled),
                      "burnside_fixed": fixed, "degree_6_orbits": 35,
                      "degree_7_orbits": 5,
                      "degree_7_symbolic_checks": "PASS",
                      "degree_five_witness": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
