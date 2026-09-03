#!/usr/bin/env python3
"""Definition-level verifier for the H(3,n) majority C-coloring formula."""

from __future__ import annotations

import argparse
import itertools


Cell = tuple[int, int]


def parameters(n: int) -> tuple[int, int, int]:
    if n < 2:
        raise ValueError("n must be at least 2")
    r = (n - 1 + 1) // 2
    s = r + 1
    optimum = n * n // s
    return r, s, optimum


def cyclic_interval(start: int, length: int, n: int) -> frozenset[int]:
    return frozenset((start + offset) % n for offset in range(length))


def active_rows(n: int) -> frozenset[int]:
    if n % 2 == 1:
        m = (n - 1) // 2
        return frozenset(set(range(n)) - {0, m + 1})
    if n == 2:
        return frozenset()
    if n == 4:
        return frozenset({0})
    if n == 6:
        return frozenset({0, 2, 4})
    m = n // 2
    return frozenset(set(range(n)) - {0, 1, m, m + 1})


def grid_partition(n: int) -> list[frozenset[Cell]]:
    _, s, _ = parameters(n)
    rows = active_rows(n)
    row_classes = [
        frozenset((i, j) for j in cyclic_interval(i, s, n))
        for i in sorted(rows)
    ]
    used = frozenset().union(*row_classes) if row_classes else frozenset()
    column_classes = [
        frozenset((i, j) for i in range(n) if (i, j) not in used)
        for j in range(n)
    ]
    return row_classes + column_classes


def verify_construction(n: int, direct_vertices: bool = True) -> int:
    r, s, optimum = parameters(n)
    groups = grid_partition(n)
    universe = frozenset(itertools.product(range(n), repeat=2))

    assert len(groups) == optimum
    assert all(groups)
    assert frozenset().union(*groups) == universe
    assert sum(map(len, groups)) == n * n
    for left, right in itertools.combinations(groups, 2):
        assert left.isdisjoint(right)

    for group in groups:
        assert len(group) >= s
        row_coordinates = {i for i, _ in group}
        column_coordinates = {j for _, j in group}
        assert len(row_coordinates) == 1 or len(column_coordinates) == 1

    if direct_vertices:
        color_of: dict[tuple[int, int, int], int] = {}
        for color, group in enumerate(groups):
            for x in range(n):
                for y, z in group:
                    vertex = (x, y, z)
                    assert vertex not in color_of
                    color_of[vertex] = color
        assert len(color_of) == n**3

        threshold = (3 * (n - 1) + 1) // 2
        for vertex, color in color_of.items():
            same = 0
            for coordinate in range(3):
                for replacement in range(n):
                    if replacement == vertex[coordinate]:
                        continue
                    neighbor = list(vertex)
                    neighbor[coordinate] = replacement
                    same += color_of[tuple(neighbor)] == color
            assert same >= threshold
            assert same >= (n - 1) + r
    return n**3


def verify_shell_bound(n: int) -> int:
    n_minus_one = n - 1
    r, s, _ = parameters(n)
    threshold = n_minus_one + r
    target_twice = 2 * n * s
    checked = 0
    for triple in itertools.product(range(n), repeat=3):
        total = sum(triple)
        if total < threshold:
            continue
        checked += 1
        lower_twice = 2 * (1 + total) + sum(
            a * (threshold - a) for a in triple
        )
        assert lower_twice >= target_twice, (n, triple, lower_twice, target_twice)
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=60)
    parser.add_argument(
        "--direct-through",
        type=int,
        default=20,
        help="perform the full vertex-neighborhood check through this n",
    )
    args = parser.parse_args()
    if args.max_n < 2:
        raise SystemExit("--max-n must be at least 2")

    triples = 0
    max_vertices = 0
    for n in range(2, args.max_n + 1):
        max_vertices = max(
            max_vertices,
            verify_construction(n, direct_vertices=n <= args.direct_through),
        )
        triples += verify_shell_bound(n)

    print(
        f"VERIFIED n=2..{args.max_n}; constructions={args.max_n - 1}; "
        f"shell_triples={triples}; max_vertices={max_vertices}"
    )


if __name__ == "__main__":
    main()
