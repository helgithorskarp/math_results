#!/usr/bin/env python3
"""Independent definition-level check of the B_{3,m} NF periods.

This program does not import verify.py, use orbit types, or use the closed
formula.  Facets are integer bit masks in the full Boolean lattice.
"""

from __future__ import annotations

import argparse
import itertools
import sys


def dumbbell_facets(m: int) -> frozenset[int]:
    if m < 2:
        raise ValueError("m must be at least 2")
    # x vertices are 0,1,2; y vertices are 3,...,m+2; bridge is 0--3.
    edges = {
        (1 << left) | (1 << right)
        for left, right in itertools.combinations(range(3), 2)
    }
    edges.update(
        (1 << left) | (1 << right)
        for left, right in itertools.combinations(range(3, m + 3), 2)
    )
    edges.add((1 << 0) | (1 << 3))
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


def labelled_orbit(m: int, limit: int) -> list[frozenset[int]]:
    initial = dumbbell_facets(m)
    result = [initial]
    current = delta(initial, m + 3)
    while current != initial:
        if len(result) >= limit:
            raise AssertionError(f"no return for m={m} before limit={limit}")
        if current in result:
            raise AssertionError(f"noninitial repetition for m={m}")
        result.append(current)
        current = delta(current, m + 3)
    return result


def is_bipartite_graph(facets: frozenset[int], vertex_count: int) -> bool:
    if any(edge.bit_count() != 2 for edge in facets):
        return False
    neighbors = [set() for _ in range(vertex_count)]
    for edge in facets:
        vertices = [bit for bit in range(vertex_count) if edge & (1 << bit)]
        left, right = vertices
        neighbors[left].add(right)
        neighbors[right].add(left)
    color: dict[int, int] = {}
    for root in range(vertex_count):
        if root in color:
            continue
        color[root] = 0
        stack = [root]
        while stack:
            vertex = stack.pop()
            for other in neighbors[vertex]:
                if other not in color:
                    color[other] = 1 - color[vertex]
                    stack.append(other)
                elif color[other] == color[vertex]:
                    return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=8)
    args = parser.parse_args()
    if not 2 <= args.max_m <= 10:
        parser.error("the full-Boolean check supports 2 <= --max-m <= 10")

    total_states = 0
    total_facets = 0
    for m in range(2, args.max_m + 1):
        orbit = labelled_orbit(m, limit=m + 6)
        if len(orbit) != m + 5:
            raise AssertionError(f"m={m}: period {len(orbit)}, expected {m + 5}")
        if not is_bipartite_graph(orbit[1], m + 3):
            raise AssertionError("the first iterate should be bipartite")
        if is_bipartite_graph(orbit[0], m + 3):
            raise AssertionError("B_(3,m) should contain its K_3 triangle")
        for step, state in enumerate(orbit[2:], start=2):
            if max(mask.bit_count() for mask in state) < 3:
                raise AssertionError(f"m={m}, step={step}: expected a large facet")
        total_states += len(orbit)
        total_facets += sum(map(len, orbit))

    print(
        "INDEPENDENT VERIFIED "
        f"B_(3,m), m=2..{args.max_m}; full_boolean_states={total_states}; "
        f"facets_seen_with_multiplicity={total_facets}; labelled_period=m+5; "
        "no earlier isomorphic return"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
