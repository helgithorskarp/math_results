#!/usr/bin/env python3
"""Verify branch-specific family-defect bounds for Q7 LD29 branches 0--62."""

from __future__ import annotations

import functools
import itertools


COORDINATES = tuple(range(6))
EDGES = tuple(itertools.combinations(COORDINATES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
FAMILY_CAPACITY = {1: 4, 2: 7, 3: 11, 4: 16, 5: 22, 6: 29}

# The canonical order is increasing (number of edges, bit mask).  Each row is
# (canonical mask, proved lower bound on total family defect D).
EXPECTED_ROWS = (
    (120, 18),
    (31, 18),
    (61, 18),
    (121, 18),
    (122, 18),
    (632, 19),
    (659, 18),
    (692, 19),
    (63, 19),
    (123, 20),
    (126, 19),
    (246, 20),
    (633, 20),
    (663, 20),
    (691, 20),
    (693, 20),
    (694, 20),
    (700, 20),
    (760, 20),
    (922, 20),
    (1880, 20),
    (5905, 21),
    (127, 21),
    (247, 21),
    (254, 20),
    (635, 21),
    (671, 21),
    (695, 21),
    (701, 21),
    (758, 22),
    (761, 22),
    (762, 21),
    (923, 22),
    (926, 21),
    (954, 21),
    (956, 21),
    (1749, 21),
    (1780, 22),
    (1881, 22),
    (1884, 21),
    (5907, 22),
    (255, 22),
    (510, 22),
    (639, 23),
    (703, 22),
    (759, 23),
    (763, 23),
    (766, 22),
    (927, 23),
    (955, 23),
    (957, 22),
    (958, 22),
    (1751, 22),
    (1781, 23),
    (1788, 23),
    (1883, 23),
    (1885, 23),
    (1916, 22),
    (2012, 22),
    (5873, 24),
    (5911, 23),
    (5941, 23),
    (5948, 23),
)


def transform(mask: int, permutation: tuple[int, ...]) -> int:
    result = 0
    for source, (first, second) in enumerate(EDGES):
        if (mask >> source) & 1:
            image = tuple(sorted((permutation[first], permutation[second])))
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


def local_data(mask: int) -> tuple[tuple[int, ...], int, int, int, int]:
    adjacency = [[False] * 6 for _ in COORDINATES]
    degrees = [0] * 6
    graph_edges: list[tuple[int, int]] = []
    for index, (first, second) in enumerate(EDGES):
        if (mask >> index) & 1:
            adjacency[first][second] = adjacency[second][first] = True
            degrees[first] += 1
            degrees[second] += 1
            graph_edges.append((first, second))

    fathers = {vertex for vertex, degree in enumerate(degrees) if degree >= 2}
    triangles = sum(
        adjacency[first][second]
        and adjacency[first][third]
        and adjacency[second][third]
        for first, second, third in itertools.combinations(COORDINATES, 3)
    )
    local_defect = sum(degrees[vertex] - 1 for vertex in fathers)
    local_capacity = sum(FAMILY_CAPACITY[degrees[vertex] - 1] for vertex in fathers)
    father_edges = sum(first in fathers and second in fathers for first, second in graph_edges)
    forced_deficit = 2 * father_edges + 2 * triangles
    return (
        tuple(sorted(degrees)),
        triangles,
        local_defect,
        local_capacity,
        forced_deficit,
    )


@functools.cache
def defect_partitions(total: int, minimum_part: int = 1) -> tuple[tuple[int, ...], ...]:
    if total == 0:
        return ((),)
    return tuple(
        (part,) + remainder
        for part in range(minimum_part, 7)
        if part <= total
        for remainder in defect_partitions(total - part, part)
    )


def arithmetic_state_survives(
    total_defect: int,
    couples: int,
    extra_defects: tuple[int, ...],
    local_defect: int,
    local_capacity: int,
    forced_deficit: int,
) -> bool:
    """Return whether capacity plus near-full F8/F7 tests leave this state open."""

    assert sum(extra_defects) == total_defect - local_defect
    family_vertices = 104 - total_defect - 2 * couples
    total_capacity = local_capacity + sum(FAMILY_CAPACITY[d] for d in extra_defects)
    total_deficit = total_capacity - family_vertices
    if total_deficit < forced_deficit:
        return False

    # Local forced slots and slots in the other families are disjoint.  Thus
    # at most this many missing slots remain available to all F8/F7 families.
    free_missing_slots = total_deficit - forced_deficit
    defect_six_fathers = extra_defects.count(6)
    defect_five_fathers = extra_defects.count(5)

    # Isolated codewords and the 2q codewords in couples lie outside all
    # families.  Since a >= D-5, at most 34-D-2q codewords lie in families.
    family_codeword_capacity = 34 - total_defect - 2 * couples

    # We do not know which F7 fathers are codewords or how the remaining
    # missing slots are distributed.  Exhaust every possibility in the
    # direction favorable to existence.  Codeword F8/F7 families force
    # nonisolated family codewords.  A noncodeword F7 family missing t slots
    # forces at least 7-2t isolated codewords.  Guaranteed isolated sets from
    # different noncodeword F7 fathers are disjoint after a shared pair is
    # charged to a missing slot in both families.
    for codeword_f7 in range(defect_five_fathers + 1):
        noncodeword_f7 = defect_five_fathers - codeword_f7
        for missing_f8 in range(free_missing_slots + 1):
            for missing_codeword_f7 in range(free_missing_slots - missing_f8 + 1):
                missing_noncodeword_f7 = (
                    free_missing_slots - missing_f8 - missing_codeword_f7
                )
                forced_family_codewords = max(
                    0, 8 * defect_six_fathers - missing_f8
                ) + max(0, 7 * codeword_f7 - missing_codeword_f7)
                forced_isolated_codewords = max(
                    0, 7 * noncodeword_f7 - 2 * missing_noncodeword_f7
                )
                if (
                    forced_family_codewords <= family_codeword_capacity
                    and forced_family_codewords + forced_isolated_codewords
                    <= 29 - 2 * couples
                ):
                    return True
    return False


def method_bound(mask: int) -> int:
    _, _, local_defect, local_capacity, forced_deficit = local_data(mask)
    # D >= 18 is the predecessor's universal exact-cardinality-29 theorem.
    for total_defect in range(max(18, local_defect), 35):
        maximum_couples = (34 - total_defect) // 2
        for couples in range(maximum_couples + 1):
            for extra_defects in defect_partitions(total_defect - local_defect):
                if arithmetic_state_survives(
                    total_defect,
                    couples,
                    extra_defects,
                    local_defect,
                    local_capacity,
                    forced_deficit,
                ):
                    return total_defect
    raise AssertionError("no surviving arithmetic state")


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
    assert len(EXPECTED_ROWS) == 63
    assert all(reps[index] == mask for index, (mask, _) in enumerate(EXPECTED_ROWS))
    assert [mask.bit_count() for mask, _ in EXPECTED_ROWS] == (
        [4] + [5] * 7 + [6] * 14 + [7] * 19 + [8] * 22
    )

    groups: dict[int, list[int]] = {}
    for index, (mask, expected_bound) in enumerate(EXPECTED_ROWS):
        degrees, triangles, local_defect, capacity, forced = local_data(mask)
        assert local_defect == 2 * mask.bit_count() - 6
        bound = method_bound(mask)
        assert bound == expected_bound
        groups.setdefault(bound, []).append(index)
        print(
            f"PASS branch={index:02d} edges={mask.bit_count()} mask={mask} "
            f"degrees={degrees} triangles={triangles} local_defect={local_defect} "
            f"capacity={capacity} forced_deficit={forced} D>={bound}"
        )

    assert groups == {
        18: [0, 1, 2, 3, 4, 6],
        19: [5, 7, 8, 10],
        20: [9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 24],
        21: [21, 22, 23, 25, 26, 27, 28, 31, 33, 34, 35, 36, 39],
        22: [29, 30, 32, 37, 38, 40, 41, 42, 44, 47, 50, 51, 52, 57, 58],
        23: [43, 45, 46, 48, 49, 53, 54, 55, 56, 60, 61, 62],
        24: [59],
    }

    edge_table = edge_isoperimetric_table(7)
    assert {bound: edge_table[34 - bound] for bound in range(18, 25)} == {
        18: 32,
        19: 28,
        20: 25,
        21: 22,
        22: 20,
        23: 17,
        24: 15,
    }
    print("PASS all 115 canonical admissible local graphs reconstructed")
    print("PASS 57 of branches 0--62 improve on the universal D>=18 bound")
    print("PASS consequence table p>=24+D, a>=D-5, b<=34-D, edges<=E_7(b)")


if __name__ == "__main__":
    main()
