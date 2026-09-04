#!/usr/bin/env python3
"""Generate any of the six surviving cyclic order-15 formulas."""

from __future__ import annotations

import argparse
import hashlib
import itertools
from pathlib import Path


ORDER = 43
CASES = (
    (1, 4, 2, 2),
    (2, 1, 0, 8),
    (2, 1, 1, 5),
    (2, 1, 2, 2),
    (2, 2, 0, 3),
    (2, 2, 1, 0),
)


def case_label(case: tuple[int, int, int, int]) -> str:
    return "a" + "_".join(map(str, case))


def vertex_cycles(case: tuple[int, int, int, int]) -> list[list[int]]:
    counts = dict(zip((15, 5, 3, 1), case, strict=True))
    cycles = []
    top = 0
    for length in (15, 5, 3, 1):
        for _ in range(counts[length]):
            cycles.append(list(range(top, top + length)))
            top += length
    if top != ORDER:
        raise AssertionError((case, top))
    return cycles


def edge_mapping(case: tuple[int, int, int, int]) -> tuple[dict[tuple[int, int], int], dict[int, int]]:
    successor = list(range(ORDER))
    for cycle in vertex_cycles(case):
        for position, vertex in enumerate(cycle):
            successor[vertex] = cycle[(position + 1) % len(cycle)]

    def key(left: int, right: int) -> tuple[int, int]:
        images = []
        for _ in range(15):
            images.append(tuple(sorted((left, right))))
            left, right = successor[left], successor[right]
        return min(images)

    representatives = sorted(
        {key(left, right) for left in range(ORDER) for right in range(left + 1, ORDER)}
    )
    index = {edge: position + 1 for position, edge in enumerate(representatives)}
    mapping = {
        (left, right): index[key(left, right)]
        for left in range(ORDER)
        for right in range(left + 1, ORDER)
    }
    orbit_sizes = {variable: 0 for variable in index.values()}
    for variable in mapping.values():
        orbit_sizes[variable] += 1
    distribution: dict[int, int] = {}
    for size in orbit_sizes.values():
        distribution[size] = distribution.get(size, 0) + 1
    return mapping, distribution


def build(case: tuple[int, int, int, int]) -> tuple[int, list[tuple[int, ...]], dict[int, int]]:
    if case not in CASES:
        raise ValueError("case is not in the power-filtered list")
    mapping, distribution = edge_mapping(case)
    clauses: set[tuple[int, ...]] = set()
    for vertices in itertools.combinations(range(ORDER), 5):
        variables = sorted(
            {mapping[pair] for pair in itertools.combinations(vertices, 2)}
        )
        clauses.add(tuple(variables))
        clauses.add(tuple(-variable for variable in reversed(variables)))
    return max(mapping.values()), sorted(clauses, key=lambda c: (len(c), c)), distribution


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=int, choices=range(len(CASES)), required=True)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    case = CASES[args.case]
    variables, clauses, distribution = build(case)
    with args.output.open("w", encoding="ascii", newline="\n") as stream:
        stream.write(f"p cnf {variables} {len(clauses)}\n")
        for clause in clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    print(
        f"case={case} variables={variables} clauses={len(clauses)} "
        f"edge_orbit_sizes={distribution} sha256={digest}"
    )


if __name__ == "__main__":
    main()
