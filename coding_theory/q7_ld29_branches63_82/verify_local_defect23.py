#!/usr/bin/env python3
"""Verify leaf-aware family-collision bounds for Q7 LD29 branches 63--82."""

from __future__ import annotations

import itertools


COORDINATES = tuple(range(6))
EDGES = tuple(itertools.combinations(COORDINATES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
FAMILY_CAPACITY = {1: 4, 2: 7, 3: 11, 4: 16, 5: 22, 6: 29}
EXPECTED = {
    63: (511, (2, 2, 2, 2, 5, 5), 4, 48, 26, 24),
    64: (767, (1, 2, 3, 3, 4, 5), 5, 45, 26, 24),
    65: (959, (2, 2, 2, 3, 4, 5), 4, 46, 26, 24),
    66: (1022, (2, 2, 3, 3, 4, 4), 2, 44, 22, 24),
    67: (1759, (1, 3, 3, 3, 3, 5), 4, 44, 24, 24),
    68: (1783, (1, 2, 3, 4, 4, 4), 5, 44, 26, 24),
    69: (1789, (1, 3, 3, 3, 4, 4), 4, 43, 24, 24),
    70: (1887, (2, 2, 3, 3, 3, 5), 4, 45, 26, 24),
    71: (1915, (2, 2, 2, 4, 4, 4), 4, 45, 26, 24),
    72: (1917, (2, 2, 3, 3, 4, 4), 3, 44, 24, 24),
    73: (2013, (2, 2, 3, 3, 4, 4), 3, 44, 24, 24),
    74: (2014, (2, 3, 3, 3, 3, 4), 2, 43, 22, 24),
    75: (4060, (3, 3, 3, 3, 3, 3), 0, 42, 18, 23),
    76: (5875, (1, 3, 3, 3, 4, 4), 5, 43, 26, 24),
    77: (5919, (2, 2, 3, 3, 3, 5), 5, 45, 28, 24),
    78: (5943, (2, 2, 3, 3, 4, 4), 4, 44, 26, 24),
    79: (5949, (2, 3, 3, 3, 3, 4), 3, 43, 24, 24),
    80: (5950, (2, 2, 3, 3, 4, 4), 4, 44, 26, 24),
    81: (6010, (2, 3, 3, 3, 3, 4), 3, 43, 24, 24),
    82: (7100, (3, 3, 3, 3, 3, 3), 2, 42, 22, 24),
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


def maximum_capacity(total_defect: int, maximum_family_defect: int = 6) -> int:
    values = [0] + [-10**9] * total_defect
    for total in range(1, total_defect + 1):
        values[total] = max(
            values[total - defect] + capacity
            for defect, capacity in FAMILY_CAPACITY.items()
            if defect <= total and defect <= maximum_family_defect
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
        assert mask.bit_count() == 9
        degrees, triangles, local_defect, local_capacity, forced_deficit = graph_data(mask)
        assert degrees == expected_degrees
        assert triangles == expected_triangles
        assert local_defect == 12
        assert local_capacity == expected_capacity
        assert forced_deficit == expected_deficit

        # If D were below ``bound``, even filling all remaining family
        # capacity and maximizing the number q of couples would leave fewer
        # absent son slots than the local geometry forces.
        for total_defect in range(local_defect, bound):
            remaining = total_defect - local_defect
            extra_capacity = maximum_capacity(remaining)
            maximum_couples = (34 - total_defect) // 2
            assert maximum_couples >= 0
            for couples in range(maximum_couples + 1):
                family_vertices = 104 - total_defect - 2 * couples
                possible_deficit = local_capacity + extra_capacity - family_vertices
                if possible_deficit < forced_deficit:
                    continue

                # The only capacity case not eliminated directly occurs at
                # D=23.  Except in branch 75, capacity without a defect-six
                # family is already too small.  A defect-six father f has
                # I(f)=N[f], so f and its seven neighbors are codewords.  If
                # at most s son slots of its family are absent, the slots
                # {f,c} put at least 8-s of those codewords in the family.
                # This exceeds the global family-codeword budget.
                assert total_defect == 23
                assert index != 75
                capacity_without_six = maximum_capacity(remaining, 5)
                possible_without_six = (
                    local_capacity + capacity_without_six - family_vertices
                )
                assert possible_without_six < forced_deficit
                slack = possible_deficit - forced_deficit
                family_codeword_budget = 29 - (total_defect - 5) - 2 * couples
                assert 8 - slack > family_codeword_budget

    edge_table = edge_isoperimetric_table(7)
    assert edge_table[11] == 17
    assert edge_table[10] == 15
    print("PASS canonical admissible local graph orbits: 115")
    for index, expected in EXPECTED.items():
        mask, degrees, triangles, capacity, deficit, bound = expected
        print(
            f"PASS branch={index} mask={mask} degrees={degrees} "
            f"triangles={triangles} local_capacity={capacity} "
            f"forced_deficit={deficit} implies_D_at_least={bound}"
        )
    print("PASS branch 75: D>=23, p>=47, isolated>=18, nonisolated<=11, edges<=17")
    print("PASS other 19 branches: D>=24, p>=48, isolated>=19, nonisolated<=10, edges<=15")


if __name__ == "__main__":
    main()
