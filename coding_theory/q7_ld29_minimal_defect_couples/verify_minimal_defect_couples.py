#!/usr/bin/env python3
"""Verify couple-count rigidity at the minimal defect of all open Q7 LD29 branches."""

from __future__ import annotations

import collections
import functools
import itertools


COORDINATES = tuple(range(6))
EDGES = tuple(itertools.combinations(COORDINATES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
FAMILY_CAPACITY = {1: 4, 2: 7, 3: 11, 4: 16, 5: 22, 6: 29}

# branch: (minimal currently proved defect, number of surviving arithmetic
# states at equality, exact distribution {number of couples: state count}).
EXPECTED = {
    0: (18, 130, {3: 1, 4: 6, 5: 8, 6: 17, 7: 35, 8: 63}),
    1: (18, 89, {4: 3, 5: 5, 6: 11, 7: 24, 8: 46}),
    2: (18, 16, {7: 4, 8: 12}),
    3: (18, 9, {7: 2, 8: 7}),
    4: (18, 2, {8: 2}),
    5: (19, 5, {7: 5}),
    6: (18, 2, {8: 2}),
    7: (19, 21, {5: 1, 6: 5, 7: 15}),
    8: (19, 3, {7: 3}),
    9: (20, 31, {5: 2, 6: 8, 7: 21}),
    10: (19, 1, {7: 1}),
    11: (20, 31, {5: 2, 6: 8, 7: 21}),
    12: (20, 10, {6: 2, 7: 8}),
    13: (20, 16, {6: 4, 7: 12}),
    14: (20, 16, {6: 4, 7: 12}),
    15: (20, 31, {5: 2, 6: 8, 7: 21}),
    16: (20, 10, {6: 2, 7: 8}),
    17: (20, 16, {6: 4, 7: 12}),
    18: (20, 4, {7: 4}),
    19: (20, 16, {6: 4, 7: 12}),
    20: (20, 10, {6: 2, 7: 8}),
    21: (21, 6, {5: 1, 6: 5}),
    22: (21, 7, {5: 1, 6: 6}),
    23: (21, 3, {6: 3}),
    24: (20, 1, {7: 1}),
    25: (21, 1, {6: 1}),
    26: (21, 3, {6: 3}),
    27: (21, 1, {6: 1}),
    28: (21, 3, {6: 3}),
    29: (22, 31, {4: 2, 5: 8, 6: 21}),
    30: (22, 31, {4: 2, 5: 8, 6: 21}),
    31: (21, 1, {6: 1}),
    32: (22, 31, {4: 2, 5: 8, 6: 21}),
    33: (21, 1, {6: 1}),
    34: (21, 7, {5: 1, 6: 6}),
    35: (21, 3, {6: 3}),
    36: (21, 1, {6: 1}),
    37: (22, 16, {5: 4, 6: 12}),
    38: (22, 31, {4: 2, 5: 8, 6: 21}),
    39: (21, 3, {6: 3}),
    40: (22, 10, {5: 2, 6: 8}),
    41: (22, 2, {6: 2}),
    42: (22, 20, {4: 1, 5: 4, 6: 15}),
    43: (23, 7, {4: 1, 5: 6}),
    46: (23, 7, {4: 1, 5: 6}),
    48: (23, 7, {4: 1, 5: 6}),
    49: (23, 7, {4: 1, 5: 6}),
    51: (22, 2, {6: 2}),
    54: (23, 7, {4: 1, 5: 6}),
    55: (23, 7, {4: 1, 5: 6}),
    56: (23, 7, {4: 1, 5: 6}),
}

EXPECTED_BY_MINIMUM = {
    3: (0,),
    4: (1, 29, 30, 32, 38, 42, 43, 46, 48, 49, 54, 55, 56),
    5: (7, 9, 11, 15, 21, 22, 34, 37, 40),
    6: (12, 13, 14, 16, 17, 19, 20, 23, 25, 26, 27, 28, 31, 33, 35, 36, 39, 41, 51),
    7: (2, 3, 5, 8, 10, 18, 24),
    8: (4, 6),
}


def transform(mask: int, permutation: tuple[int, ...]) -> int:
    result = 0
    for source, (first, second) in enumerate(EDGES):
        if mask >> source & 1:
            image = tuple(sorted((permutation[first], permutation[second])))
            result |= 1 << EDGE_INDEX[image]
    return result


def admissible(mask: int) -> bool:
    adjacency = [set() for _ in COORDINATES]
    for index, (first, second) in enumerate(EDGES):
        if mask >> index & 1:
            adjacency[first].add(second)
            adjacency[second].add(first)
    if any(not neighbors for neighbors in adjacency):
        return False
    return all(
        len(neighbors) != 1 or adjacency[next(iter(neighbors))] != {vertex}
        for vertex, neighbors in enumerate(adjacency)
    )


def representatives() -> tuple[int, ...]:
    permutations = tuple(itertools.permutations(COORDINATES))
    seen: set[int] = set()
    result = []
    for mask in range(1 << len(EDGES)):
        if mask in seen or not admissible(mask):
            continue
        orbit = {transform(mask, permutation) for permutation in permutations}
        seen.update(orbit)
        result.append(min(orbit))
    return tuple(sorted(result, key=lambda mask: (mask.bit_count(), mask)))


def local_data(mask: int) -> tuple[int, int, int]:
    adjacency = [[False] * 6 for _ in COORDINATES]
    degrees = [0] * 6
    graph_edges = []
    for index, (first, second) in enumerate(EDGES):
        if mask >> index & 1:
            adjacency[first][second] = adjacency[second][first] = True
            degrees[first] += 1
            degrees[second] += 1
            graph_edges.append((first, second))
    fathers = {vertex for vertex, degree in enumerate(degrees) if degree >= 2}
    triangles = sum(
        adjacency[a][b] and adjacency[a][c] and adjacency[b][c]
        for a, b, c in itertools.combinations(COORDINATES, 3)
    )
    local_defect = sum(degrees[vertex] - 1 for vertex in fathers)
    local_capacity = sum(FAMILY_CAPACITY[degrees[vertex] - 1] for vertex in fathers)
    father_edges = sum(a in fathers and b in fathers for a, b in graph_edges)
    forced_deficit = 2 * father_edges + 2 * triangles
    return local_defect, local_capacity, forced_deficit


@functools.cache
def defect_partitions(total: int, minimum: int = 1) -> tuple[tuple[int, ...], ...]:
    if total == 0:
        return ((),)
    return tuple(
        (part,) + tail
        for part in range(minimum, 7)
        if part <= total
        for tail in defect_partitions(total - part, part)
    )


def survives(
    defect: int,
    couples: int,
    extra: tuple[int, ...],
    local_defect: int,
    local_capacity: int,
    forced_deficit: int,
) -> bool:
    family_vertices = 104 - defect - 2 * couples
    total_capacity = local_capacity + sum(FAMILY_CAPACITY[value] for value in extra)
    free_missing = total_capacity - family_vertices - forced_deficit
    if free_missing < 0:
        return False
    f8 = extra.count(6)
    f7 = extra.count(5)
    family_codeword_capacity = 34 - defect - 2 * couples
    for codeword_f7 in range(f7 + 1):
        noncodeword_f7 = f7 - codeword_f7
        for missing_f8 in range(free_missing + 1):
            for missing_codeword_f7 in range(free_missing - missing_f8 + 1):
                missing_noncodeword_f7 = free_missing - missing_f8 - missing_codeword_f7
                forced_family = max(0, 8 * f8 - missing_f8) + max(
                    0, 7 * codeword_f7 - missing_codeword_f7
                )
                forced_isolated = max(
                    0, 7 * noncodeword_f7 - 2 * missing_noncodeword_f7
                )
                if (
                    forced_family <= family_codeword_capacity
                    and forced_family + forced_isolated <= 29 - 2 * couples
                ):
                    return True
    return False


def states(mask: int, defect: int) -> tuple[tuple[int, tuple[int, ...]], ...]:
    local_defect, local_capacity, forced_deficit = local_data(mask)
    result = []
    for couples in range((34 - defect) // 2 + 1):
        for extra in defect_partitions(defect - local_defect):
            if survives(
                defect,
                couples,
                extra,
                local_defect,
                local_capacity,
                forced_deficit,
            ):
                result.append((couples, extra))
    return tuple(result)


def method_bound(mask: int) -> int:
    local_defect, _, _ = local_data(mask)
    for defect in range(max(18, local_defect), 35):
        if states(mask, defect):
            return defect
    raise AssertionError("no surviving arithmetic state")


def main() -> None:
    reps = representatives()
    assert len(reps) == 115
    assert len(EXPECTED) == 51
    assert tuple(EXPECTED) == (*range(44), 46, 48, 49, 51, 54, 55, 56)
    grouped: dict[int, list[int]] = collections.defaultdict(list)
    for branch, (defect, expected_count, expected_distribution) in EXPECTED.items():
        mask = reps[branch]
        assert method_bound(mask) == defect
        surviving = states(mask, defect)
        distribution = dict(sorted(collections.Counter(q for q, _ in surviving).items()))
        assert len(surviving) == expected_count
        assert distribution == expected_distribution
        minimum = min(distribution)
        grouped[minimum].append(branch)
        print(
            f"PASS branch={branch:02d} mask={mask} D={defect} "
            f"states={len(surviving)} couple_distribution={distribution} q>={minimum}"
        )
    observed_groups = {minimum: tuple(branches) for minimum, branches in grouped.items()}
    assert observed_groups == EXPECTED_BY_MINIMUM
    print("PASS all 51 unresolved branches reconstructed")
    print("PASS at exact branchwise minimal defect every branch has at least three couples")
    for minimum, branches in EXPECTED_BY_MINIMUM.items():
        print(f"PASS q>={minimum}: branches={branches}")


if __name__ == "__main__":
    main()
