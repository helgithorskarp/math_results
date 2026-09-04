#!/usr/bin/env python3
"""Independent exact checks for the dominant-factor Hamming theorem."""

from __future__ import annotations

import itertools
import math
from collections.abc import Sequence


Vertex = tuple[int, ...]


def graph(sides: Sequence[int]) -> tuple[list[Vertex], list[int]]:
    vertices = list(itertools.product(*(range(side) for side in sides)))
    index = {vertex: i for i, vertex in enumerate(vertices)}
    adjacency = [0] * len(vertices)
    for i, vertex in enumerate(vertices):
        for direction, side in enumerate(sides):
            for value in range(side):
                if value == vertex[direction]:
                    continue
                neighbour = list(vertex)
                neighbour[direction] = value
                adjacency[i] |= 1 << index[tuple(neighbour)]
    return vertices, adjacency


def direct_class_census(sides: Sequence[int]) -> tuple[int, int, int, int]:
    vertices, adjacency = graph(sides)
    degree = sum(side - 1 for side in sides)
    h = (degree + 1) // 2
    n1 = sides[0]
    checked = 0
    feasible_masks: set[int] = set()
    smaller_locally_feasible = 0
    for size in range(1, n1 + 1):
        for subset in itertools.combinations(range(len(vertices)), size):
            checked += 1
            if size <= h:
                continue
            mask = sum(1 << vertex for vertex in subset)
            if all((adjacency[vertex] & mask).bit_count() >= h for vertex in subset):
                if size == n1:
                    feasible_masks.add(mask)
                else:
                    smaller_locally_feasible += 1

    full_fibres = set()
    for minor in itertools.product(*(range(side) for side in sides[1:])):
        full_fibres.add(
            sum(1 << i for i, vertex in enumerate(vertices) if vertex[1:] == minor)
        )
    assert feasible_masks == full_fibres
    return checked, len(feasible_masks), smaller_locally_feasible, h


def doubled_g(t: int, h: int) -> int:
    return 2 * t + t * (h - t)


def endpoint_audit(limit: int = 500) -> tuple[int, int]:
    pairs = 0
    minimum_strict_gap = 10**9
    for n1_deficit in range(1, limit + 1):
        for minor_sum in range(1, n1_deficit - 1):
            degree = n1_deficit + minor_sum
            h = (degree + 1) // 2
            ell = degree - h
            assert h < n1_deficit
            endpoints = (
                (h - minor_sum, minor_sum),
                (ell - 1, h - ell + 1),
                (ell - 1, minor_sum),
            )
            for a, b in endpoints:
                doubled_bound = 2 + doubled_g(a, h) + doubled_g(b, h)
                gap = doubled_bound - 2 * (n1_deficit + 1)
                assert gap >= 0
                if minor_sum >= 2:
                    assert gap >= 2
                    minimum_strict_gap = min(minimum_strict_gap, gap)
            pairs += 1
    return pairs, minimum_strict_gap


def boundary_extension_audit(limit: int = 500) -> int:
    checked = 0
    for n1_deficit in range(2, limit + 1):
        for minor_sum in (n1_deficit - 1, n1_deficit):
            h = (n1_deficit + minor_sum + 1) // 2
            assert h == n1_deficit
            assert h + 1 == n1_deficit + 1
            checked += 1
    return checked


def dimension_two_nonunique_witness() -> int:
    sides = (4, 2)
    vertices, adjacency = graph(sides)
    index = {vertex: i for i, vertex in enumerate(vertices)}
    classes = []
    for pair in ((0, 1), (2, 3)):
        classes.append(tuple(index[(first, second)] for first in pair for second in range(2)))
    h = 2
    seen = set()
    for colour_class in classes:
        mask = sum(1 << vertex for vertex in colour_class)
        assert all((adjacency[vertex] & mask).bit_count() >= h for vertex in colour_class)
        seen.update(colour_class)
    assert seen == set(range(math.prod(sides)))
    return len(classes)


def main() -> None:
    endpoint_pairs, strict_gap = endpoint_audit()
    boundary_pairs = boundary_extension_audit()
    census_instances = ((3, 2, 2), (4, 2, 2), (5, 2, 2), (6, 3, 2))
    census = [direct_class_census(sides) for sides in census_instances]
    print(f"dominant endpoint pairs checked: {endpoint_pairs}")
    print(f"minimum doubled strict gap: {strict_gap}")
    print(f"h=N1 boundary pairs checked: {boundary_pairs}")
    print(f"direct candidate subsets checked: {sum(item[0] for item in census)}")
    print(f"locally feasible size-n1 classes: {tuple(item[1] for item in census)}")
    print(f"smaller locally feasible subsets: {tuple(item[2] for item in census)}")
    print(f"thresholds in direct censuses: {tuple(item[3] for item in census)}")
    print(f"non-fibre extremal colours in K4xK2 witness: {dimension_two_nonunique_witness()}")
    print("all independent checks passed")


if __name__ == "__main__":
    main()
