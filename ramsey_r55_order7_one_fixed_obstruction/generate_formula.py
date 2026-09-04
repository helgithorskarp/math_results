#!/usr/bin/env python3
"""Generate the Ramsey(5,5;43) CNF invariant under C7 of type 1+7^6."""

from __future__ import annotations

import argparse
import hashlib
import itertools
from pathlib import Path

N = 43
VARIABLES = 129


def image(vertex: int, power: int = 1) -> int:
    """Apply the chosen order-seven permutation ``power`` times."""
    if vertex == 0:
        return 0
    cycle, position = divmod(vertex - 1, 7)
    return 1 + 7 * cycle + (position + power) % 7


def edge_key(u: int, v: int) -> tuple[int, int]:
    """Least edge in the C7 orbit of {u,v}."""
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
    """Clause falsified by exactly the supplied Boolean assignment."""
    return tuple(-variable if value else variable for variable, value in zip(variables, values))


def cycle_profile(mapping: dict[tuple[int, int], int], cycle: int) -> list[int]:
    base = 1 + 7 * cycle
    return [mapping[(0, base)]] + [mapping[(base, base + d)] for d in (1, 2, 3)]


def add_fixed_degree(
    clauses: set[tuple[int, ...]], mapping: dict[tuple[int, int], int]
) -> None:
    # R(4,5)=25 gives 18 <= deg(0) <= 24.  Since deg(0) is a multiple
    # of seven, exactly three of these six orbit variables are true.
    variables = [mapping[(0, 1 + 7 * cycle)] for cycle in range(6)]
    for four in itertools.combinations(variables, 4):
        clauses.add(tuple(four))
        clauses.add(tuple(-variable for variable in four))


def add_sorted_profiles(
    clauses: set[tuple[int, ...]], mapping: dict[tuple[int, int], int]
) -> None:
    # The centralizer permutes the six seven-cycles.  Sort their invariant
    # four-bit profiles (fixed edge plus three internal cyclic distances).
    profiles = [cycle_profile(mapping, cycle) for cycle in range(6)]
    patterns = list(itertools.product((0, 1), repeat=4))
    for left, right in zip(profiles, profiles[1:]):
        for left_bits in patterns:
            for right_bits in patterns:
                if left_bits > right_bits:
                    clauses.add(blocking_clause(left + right, left_bits + right_bits))


def rotations(bits: tuple[int, ...]):
    for shift in range(len(bits)):
        yield bits[shift:] + bits[:shift]


def add_pair_necklaces(
    clauses: set[tuple[int, ...]], mapping: dict[tuple[int, int], int]
) -> None:
    # After choosing cycle zero as phase anchor, rotate each other cycle so
    # its seven cross-edge bits with cycle zero are lexicographically least.
    for cycle in range(1, 6):
        base = 1 + 7 * cycle
        variables = [mapping[(1, base + offset)] for offset in range(7)]
        for bits in itertools.product((0, 1), repeat=7):
            if bits != min(rotations(bits)):
                clauses.add(blocking_clause(variables, bits))


def formula() -> list[tuple[int, ...]]:
    mapping = edge_variables()
    clauses = ramsey_clauses(mapping)
    add_fixed_degree(clauses, mapping)
    add_sorted_profiles(clauses, mapping)
    add_pair_necklaces(clauses, mapping)
    return sorted(clauses, key=lambda clause: (len(clause), clause))


def write_dimacs(path: Path) -> tuple[int, str]:
    clauses = formula()
    with path.open("w", encoding="ascii", newline="\n") as output:
        output.write(f"p cnf {VARIABLES} {len(clauses)}\n")
        for clause in clauses:
            output.write(" ".join(map(str, clause)) + " 0\n")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return len(clauses), digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    count, digest = write_dimacs(args.output)
    print(f"variables={VARIABLES} clauses={count} sha256={digest}")


if __name__ == "__main__":
    main()
