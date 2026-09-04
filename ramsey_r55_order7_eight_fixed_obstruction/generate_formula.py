#!/usr/bin/env python3
"""Generate the Ramsey(5,5;43) CNF invariant under C7 of type 1^8+7^5."""

from __future__ import annotations

import argparse
import hashlib
import itertools
from pathlib import Path

N = 43
FIXED = 8
CYCLES = 5
VARIABLES = 153


def image(vertex: int, power: int = 1) -> int:
    if vertex < FIXED:
        return vertex
    cycle, position = divmod(vertex - FIXED, 7)
    return FIXED + 7 * cycle + (position + power) % 7


def edge_key(u: int, v: int) -> tuple[int, int]:
    return min(tuple(sorted((image(u, k), image(v, k)))) for k in range(7))


def edge_variables() -> dict[tuple[int, int], int]:
    representatives = sorted(
        {edge_key(u, v) for u in range(N) for v in range(u + 1, N)}
    )
    assert len(representatives) == VARIABLES
    index = {edge: i + 1 for i, edge in enumerate(representatives)}
    mapping = {
        (u, v): index[edge_key(u, v)]
        for u in range(N)
        for v in range(u + 1, N)
    }
    assert len(mapping) == 903
    return mapping


def ramsey_clauses(mapping: dict[tuple[int, int], int]) -> set[tuple[int, ...]]:
    clauses: set[tuple[int, ...]] = set()
    for vertices in itertools.combinations(range(N), 5):
        variables = sorted(
            {mapping[(u, v)] for u, v in itertools.combinations(vertices, 2)}
        )
        clauses.add(tuple(variables))
        clauses.add(tuple(-variable for variable in reversed(variables)))
    return clauses


def blocking_clause(variables: list[int], values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(-variable if value else variable for variable, value in zip(variables, values))


def rotations(bits: tuple[int, ...]):
    for shift in range(len(bits)):
        yield bits[shift:] + bits[:shift]


def add_symmetry(
    clauses: set[tuple[int, ...]], mapping: dict[tuple[int, int], int]
) -> None:
    # First sort seven-cycles by their three phase-invariant internal colors.
    patterns3 = list(itertools.product((0, 1), repeat=3))
    cycle_profiles = []
    for cycle in range(CYCLES):
        base = FIXED + 7 * cycle
        cycle_profiles.append([mapping[(base, base + distance)] for distance in (1, 2, 3)])
    for left, right in zip(cycle_profiles, cycle_profiles[1:]):
        for left_bits in patterns3:
            for right_bits in patterns3:
                if left_bits > right_bits:
                    clauses.add(
                        blocking_clause(left + right, left_bits + right_bits)
                    )

    # Then sort fixed vertices by their incidence words to the ordered cycles.
    patterns5 = list(itertools.product((0, 1), repeat=5))
    fixed_profiles = [
        [mapping[(vertex, FIXED + 7 * cycle)] for cycle in range(CYCLES)]
        for vertex in range(FIXED)
    ]
    for left, right in zip(fixed_profiles, fixed_profiles[1:]):
        for left_bits in patterns5:
            for right_bits in patterns5:
                if left_bits > right_bits:
                    clauses.add(
                        blocking_clause(left + right, left_bits + right_bits)
                    )

    # Finally use four independent relative phase choices against cycle zero.
    anchor = FIXED
    for cycle in range(1, CYCLES):
        base = FIXED + 7 * cycle
        variables = [mapping[(anchor, base + offset)] for offset in range(7)]
        for word in itertools.product((0, 1), repeat=7):
            if word != min(rotations(word)):
                clauses.add(blocking_clause(variables, word))


def formula() -> list[tuple[int, ...]]:
    mapping = edge_variables()
    clauses = ramsey_clauses(mapping)
    add_symmetry(clauses, mapping)
    return sorted(clauses, key=lambda clause: (len(clause), clause))


def write_dimacs(path: Path) -> tuple[int, str]:
    clauses = formula()
    with path.open("w", encoding="ascii", newline="\n") as output:
        output.write(f"p cnf {VARIABLES} {len(clauses)}\n")
        for clause in clauses:
            output.write(" ".join(map(str, clause)) + " 0\n")
    return len(clauses), hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    clause_count, digest = write_dimacs(args.output)
    print(f"variables={VARIABLES} clauses={clause_count} sha256={digest}")


if __name__ == "__main__":
    main()
