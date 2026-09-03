#!/usr/bin/env python3
"""Independent definition-level check of the B_{2,m} NF periods.

This checker does not import verify.py, use orbit types, or use the closed
formula.  Complex facets are integer bit masks in the full Boolean lattice.
"""

from __future__ import annotations

import argparse
import itertools
import sys


def dumbbell_facets(m: int) -> frozenset[int]:
    if m < 2:
        raise ValueError("m must be at least 2")
    edges = {(1 << 0) | (1 << 1), (1 << 0) | (1 << 2)}
    edges.update(
        (1 << left) | (1 << right)
        for left, right in itertools.combinations(range(2, m + 2), 2)
    )
    return frozenset(edges)


def delta(facets: frozenset[int], vertex_count: int) -> frozenset[int]:
    allowed: list[int] = []
    for candidate in range(1 << vertex_count):
        if all(candidate & facet != facet for facet in facets):
            allowed.append(candidate)
    allowed_set = set(allowed)
    return frozenset(
        candidate
        for candidate in allowed
        if all(
            candidate | (1 << bit) not in allowed_set
            for bit in range(vertex_count)
            if candidate & (1 << bit) == 0
        )
    )


def relabel(facets: frozenset[int], permutation: tuple[int, ...]) -> frozenset[int]:
    image: set[int] = set()
    for facet in facets:
        new_facet = 0
        for old, new in enumerate(permutation):
            if facet & (1 << old):
                new_facet |= 1 << new
        image.add(new_facet)
    return frozenset(image)


def labelled_period(m: int, limit: int) -> tuple[int, list[frozenset[int]]]:
    initial = dumbbell_facets(m)
    orbit = [initial]
    current = delta(initial, m + 2)
    while current != initial:
        if len(orbit) >= limit:
            raise AssertionError(f"no return for m={m} before limit={limit}")
        if current in orbit:
            raise AssertionError(f"noninitial repetition for m={m}")
        orbit.append(current)
        current = delta(current, m + 2)
    return len(orbit), orbit


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=8)
    args = parser.parse_args()
    if not 2 <= args.max_m <= 9:
        parser.error("the full-Boolean check supports 2 <= --max-m <= 9")

    total_states = 0
    total_facets = 0
    for m in range(2, args.max_m + 1):
        period, orbit = labelled_period(m, limit=m + 5)
        expected = 2 if m == 2 else m + 4
        if period != expected:
            raise AssertionError(f"m={m}: period {period}, expected {expected}")
        total_states += len(orbit)
        total_facets += sum(map(len, orbit))

        if m == 2:
            # x_0->x_1, x_1->y_0, y_0->y_1, y_1->x_0.
            if relabel(orbit[0], (1, 2, 3, 0)) != orbit[1]:
                raise AssertionError("explicit P_4 isomorphism failed")
        else:
            if any(mask.bit_count() != 2 for mask in orbit[1]):
                raise AssertionError("the first iterate should be a graph")
            # The first iterate is bipartite across {x_0,x_1} and the K_m
            # vertices, whereas the initial graph contains a triangle.
            if not any(mask.bit_count() >= 3 for state in orbit[2:] for mask in state):
                raise AssertionError("expected a higher-dimensional intermediate facet")

    print(
        "INDEPENDENT VERIFIED "
        f"m=2..{args.max_m}; full_boolean_states={total_states}; "
        f"facets_seen_with_multiplicity={total_facets}; "
        "labelled_periods=(2,m+4)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
