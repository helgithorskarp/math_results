#!/usr/bin/env python3
"""Verify the local family-collision bounds for Q7 LD29 branches 83--96."""

from __future__ import annotations

import itertools


COORDINATES = tuple(range(6))
EDGES = tuple(itertools.combinations(COORDINATES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
FAMILY_CAPACITY = {1: 4, 2: 7, 3: 11, 4: 16, 5: 22, 6: 29}
EXPECTED = {
    83: (1023, (2, 2, 3, 3, 5, 5), 6, 54, 32, 25),
    84: (1791, (1, 3, 3, 4, 4, 5), 7, 52, 32, 25),
    85: (1919, (2, 2, 3, 4, 4, 5), 6, 53, 32, 25),
    86: (2015, (2, 3, 3, 3, 4, 5), 5, 52, 30, 25),
    87: (2046, (2, 3, 3, 4, 4, 4), 4, 51, 28, 25),
    88: (4061, (3, 3, 3, 3, 4, 4), 3, 50, 26, 25),
    89: (5879, (1, 3, 4, 4, 4, 4), 7, 51, 32, 26),
    90: (5951, (2, 3, 3, 3, 4, 5), 6, 52, 32, 25),
    91: (6007, (2, 2, 4, 4, 4, 4), 6, 52, 32, 25),
    92: (6011, (2, 3, 3, 4, 4, 4), 5, 51, 30, 25),
    93: (6014, (2, 3, 3, 4, 4, 4), 5, 51, 30, 25),
    94: (6654, (3, 3, 3, 3, 4, 4), 4, 50, 28, 25),
    95: (7071, (3, 3, 3, 3, 3, 5), 5, 51, 30, 25),
    96: (7101, (3, 3, 3, 3, 4, 4), 4, 50, 28, 25),
}


def transform(mask: int, permutation: tuple[int, ...]) -> int:
    result = 0
    for source, (first, second) in enumerate(EDGES):
        image = tuple(sorted((permutation[first], permutation[second])))
        if (mask >> source) & 1:
            result |= 1 << EDGE_INDEX[image]
    return result


def admissible(mask: int) -> bool:
    adjacency = [set() for _ in COORDINATES]
    for index, (first, second) in enumerate(EDGES):
        if (mask >> index) & 1:
            adjacency[first].add(second)
            adjacency[second].add(first)
    if any(not neighbors for neighbors in adjacency):
        return False
    return all(
        len(neighbors) != 1 or adjacency[next(iter(neighbors))] != {vertex}
        for vertex, neighbors in enumerate(adjacency)
    )


def representatives() -> list[int]:
    permutations = tuple(itertools.permutations(COORDINATES))
    seen: set[int] = set()
    result: list[int] = []
    for mask in range(1 << len(EDGES)):
        if mask in seen or not admissible(mask):
            continue
        orbit = {transform(mask, permutation) for permutation in permutations}
        seen.update(orbit)
        result.append(min(orbit))
    return sorted(result, key=lambda mask: (mask.bit_count(), mask))


def graph_data(mask: int) -> tuple[tuple[int, ...], int, int, int, int]:
    adjacency = [[False] * 6 for _ in COORDINATES]
    degrees = [0] * 6
    graph_edges: list[tuple[int, int]] = []
    for index, (first, second) in enumerate(EDGES):
        if (mask >> index) & 1:
            adjacency[first][second] = adjacency[second][first] = True
            degrees[first] += 1
            degrees[second] += 1
            graph_edges.append((first, second))
    triangles = sum(
        adjacency[first][second]
        and adjacency[first][third]
        and adjacency[second][third]
        for first, second, third in itertools.combinations(COORDINATES, 3)
    )
    fathers = {vertex for vertex, degree in enumerate(degrees) if degree >= 2}
    local_defect = sum(degrees[vertex] - 1 for vertex in fathers)
    local_capacity = sum(FAMILY_CAPACITY[degrees[vertex] - 1] for vertex in fathers)
    father_edges = sum(first in fathers and second in fathers for first, second in graph_edges)
    forced_deficit = 2 * father_edges + 2 * triangles
    return tuple(sorted(degrees)), triangles, local_defect, local_capacity, forced_deficit


def maximum_capacity(total_defect: int) -> int:
    values = [0] + [-10**9] * total_defect
    for total in range(1, total_defect + 1):
        values[total] = max(
            values[total - defect] + capacity
            for defect, capacity in FAMILY_CAPACITY.items()
            if defect <= total
        )
    return values[total_defect]


def edge_isoperimetric_table(dimension: int) -> list[int]:
    table = [0, 0]
    for current_dimension in range(1, dimension + 1):
        half = 1 << (current_dimension - 1)
        table = [
            max(
                table[left]
                + table[size - left]
                + min(left, size - left)
                for left in range(max(0, size - half), min(half, size) + 1)
            )
            for size in range(2 * half + 1)
        ]
    return table


def main() -> None:
    reps = representatives()
    assert len(reps) == 115

    for index, expected in EXPECTED.items():
        mask, expected_degrees, expected_triangles, expected_capacity, expected_deficit, bound = expected
        assert reps[index] == mask
        assert mask.bit_count() == 10
        degrees, triangles, local_defect, local_capacity, forced_deficit = graph_data(mask)
        assert degrees == expected_degrees
        assert triangles == expected_triangles
        assert local_defect == 14
        assert local_capacity == expected_capacity
        assert forced_deficit == expected_deficit

        for total_defect in range(local_defect, bound):
            remaining = total_defect - local_defect
            extra_capacity = maximum_capacity(remaining)
            maximum_couples = (34 - total_defect) // 2
            assert maximum_couples >= 0
            for couples in range(maximum_couples + 1):
                family_vertices = 104 - total_defect - 2 * couples
                possible_deficit = local_capacity + extra_capacity - family_vertices
                assert possible_deficit < forced_deficit

    edge_table = edge_isoperimetric_table(7)
    assert edge_table[9] == 13
    assert edge_table[8] == 12
    print("PASS canonical admissible local graph orbits: 115")
    for index, expected in EXPECTED.items():
        mask, degrees, triangles, capacity, deficit, bound = expected
        print(
            f"PASS branch={index} mask={mask} degrees={degrees} "
            f"triangles={triangles} local_capacity={capacity} "
            f"forced_deficit={deficit} implies_D_at_least={bound}"
        )
    print("PASS branches except 89: p>=49, isolated>=20, nonisolated<=9, edges<=13")
    print("PASS branch 89: p>=50, isolated>=21, nonisolated<=8, edges<=12")


if __name__ == "__main__":
    main()
