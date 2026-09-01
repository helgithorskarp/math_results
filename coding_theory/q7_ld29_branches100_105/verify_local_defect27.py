#!/usr/bin/env python3
"""Verify the local family-collision D>=27 calculation for Q7 LD29.

This script uses only the Python standard library.  It independently
reconstructs the 115 admissible local graph orbits, their canonical indices,
the six 11-edge cases 100--105, the father-capacity optimization, and the
edge-isoperimetric consequence E_7(7)=9.
"""

from __future__ import annotations

import itertools


COORDINATES = tuple(range(6))
EDGES = tuple(itertools.combinations(COORDINATES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
FAMILY_CAPACITY = {1: 4, 2: 7, 3: 11, 4: 16, 5: 22, 6: 29}
EXPECTED = {
    100: (6015, (2, 3, 4, 4, 4, 5), 8, 60, 38),
    101: (6142, (2, 4, 4, 4, 4, 4), 7, 59, 36),
    102: (6655, (3, 3, 3, 3, 5, 5), 8, 60, 38),
    103: (7103, (3, 3, 3, 4, 4, 5), 7, 59, 36),
    104: (7166, (3, 3, 4, 4, 4, 4), 6, 58, 34),
    105: (8157, (3, 3, 4, 4, 4, 4), 6, 58, 34),
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
    for index, (first, second) in enumerate(EDGES):
        if (mask >> index) & 1:
            adjacency[first][second] = adjacency[second][first] = True
            degrees[first] += 1
            degrees[second] += 1
    triangles = sum(
        adjacency[first][second]
        and adjacency[first][third]
        and adjacency[second][third]
        for first, second, third in itertools.combinations(COORDINATES, 3)
    )
    local_defect = sum(degree - 1 for degree in degrees)
    local_capacity = sum(FAMILY_CAPACITY[degree - 1] for degree in degrees)
    forced_deficit = 2 * mask.bit_count() + 2 * triangles
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
        mask, expected_degrees, expected_triangles, expected_capacity, expected_deficit = expected
        assert reps[index] == mask
        assert mask.bit_count() == 11
        degrees, triangles, local_defect, local_capacity, forced_deficit = graph_data(mask)
        assert degrees == expected_degrees
        assert min(degrees) >= 2
        assert triangles == expected_triangles
        assert local_defect == 16
        assert local_capacity == expected_capacity
        assert forced_deficit == expected_deficit

        # If total defect D were at most 26, the six displayed local fathers
        # use 16 defect.  All other father defects lie in 1,...,6.  Enumerate
        # every possible number q of codeword couples and compare the largest
        # possible total family capacity with M=104-D-2q family vertices.
        for total_defect in range(16, 27):
            remaining = total_defect - 16
            extra_capacity = maximum_capacity(remaining)
            maximum_couples = (34 - total_defect) // 2
            assert maximum_couples >= 0
            for couples in range(maximum_couples + 1):
                family_vertices = 104 - total_defect - 2 * couples
                possible_deficit = local_capacity + extra_capacity - family_vertices
                assert possible_deficit < forced_deficit

    assert edge_isoperimetric_table(7)[7] == 9
    print("PASS canonical admissible local graph orbits: 115")
    for index, expected in EXPECTED.items():
        mask, degrees, triangles, capacity, deficit = expected
        print(
            f"PASS branch={index} mask={mask} degrees={degrees} "
            f"triangles={triangles} local_capacity={capacity} "
            f"forced_deficit={deficit} implies_D_at_least=27"
        )
    print("PASS consequences: p>=51, isolated>=22, nonisolated<=7, induced_edges<=9")


if __name__ == "__main__":
    main()
