#!/usr/bin/env python3
"""Generate the unique forced C5-square invariant Ramsey formula."""

from __future__ import annotations

import argparse
import hashlib
import itertools
from pathlib import Path


ORDER = 43


def translate(vertex: int, first: int, second: int) -> int:
    """Apply (first,second) in C5^2 to the canonical forced H-set."""
    if vertex < 3:
        return vertex
    if vertex < 8:  # H / <(0,1)>, quotient coordinate first
        return 3 + ((vertex - 3 + first) % 5)
    if vertex < 13:  # H / <(1,0)>, quotient coordinate second
        return 8 + ((vertex - 8 + second) % 5)
    if vertex < 18:  # H / <(1,1)>, quotient coordinate second-first
        return 13 + ((vertex - 13 + second - first) % 5)
    x_coordinate, y_coordinate = divmod(vertex - 18, 5)
    return (
        18
        + 5 * ((x_coordinate + first) % 5)
        + ((y_coordinate + second) % 5)
    )


def edge_key(left: int, right: int) -> tuple[int, int]:
    return min(
        tuple(sorted((translate(left, first, second),
                      translate(right, first, second))))
        for first in range(5)
        for second in range(5)
    )


def edge_mapping() -> tuple[dict[tuple[int, int], int], dict[int, int]]:
    representatives = sorted(
        {
            edge_key(left, right)
            for left in range(ORDER)
            for right in range(left + 1, ORDER)
        }
    )
    index = {edge: position + 1 for position, edge in enumerate(representatives)}
    mapping = {
        (left, right): index[edge_key(left, right)]
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


def build() -> tuple[int, list[tuple[int, ...]], dict[int, int]]:
    mapping, distribution = edge_mapping()
    clauses: set[tuple[int, ...]] = set()
    for vertices in itertools.combinations(range(ORDER), 5):
        variables = sorted(
            {
                mapping[(left, right)]
                for left, right in itertools.combinations(vertices, 2)
            }
        )
        clauses.add(tuple(variables))
        clauses.add(tuple(-variable for variable in reversed(variables)))
    return max(mapping.values()), sorted(clauses, key=lambda c: (len(c), c)), distribution


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    variables, clauses, distribution = build()
    if variables != 51 or distribution != {1: 3, 5: 15, 25: 33}:
        raise AssertionError((variables, distribution))
    with args.output.open("w", encoding="ascii", newline="\n") as stream:
        stream.write(f"p cnf {variables} {len(clauses)}\n")
        for clause in clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    print(
        f"variables={variables} clauses={len(clauses)} "
        f"edge_orbit_sizes={distribution} sha256={digest}"
    )


if __name__ == "__main__":
    main()
