#!/usr/bin/env python3
"""Verify the D>=23 full-family theorem for five Q7 LD29 branches."""

from __future__ import annotations

import functools
import hashlib
import itertools
import pathlib
import sys


SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1]
LADDER_PATH = SOURCE_ROOT / "q7_ld29_branches0_62_bounds" / "verify_lower_frontier_bounds.py"
EXPECTED_LADDER_SHA256 = "acde98fb29c8673d57ceddc47b36e5b46a62a0cfa13ed542886e96fbaf0c4852"
assert hashlib.sha256(LADDER_PATH.read_bytes()).hexdigest() == EXPECTED_LADDER_SHA256
sys.path.insert(0, str(LADDER_PATH.parent))

import verify_lower_frontier_bounds as ladder  # noqa: E402


BRANCHES = (44, 47, 50, 52, 57)
EXPECTED = {
    44: {
        "mask": 703,
        "data": ((1, 2, 2, 3, 3, 5), 3, 10, 38, 20, 3),
        "centers": (63, 85, 95, 105, 111, 113, 119, 123, 125, 126, 127),
    },
    47: {
        "mask": 766,
        "data": ((1, 2, 3, 3, 3, 4), 2, 10, 36, 18, 3),
        "centers": (63, 95, 105, 111, 113, 119, 123, 125, 126, 127),
    },
    50: {
        "mask": 957,
        "data": ((2, 2, 2, 2, 4, 4), 2, 10, 38, 20, 3),
        "centers": (63, 95, 105, 111, 113, 119, 123, 125, 126, 127),
    },
    52: {
        "mask": 1751,
        "data": ((1, 2, 3, 3, 3, 4), 2, 10, 36, 18, 3),
        "centers": (63, 77, 95, 111, 113, 119, 123, 125, 126, 127),
    },
    57: {
        "mask": 1916,
        "data": ((2, 2, 3, 3, 3, 3), 1, 10, 36, 18, 3),
        "centers": (63, 95, 111, 113, 119, 123, 125, 126, 127),
    },
}
EXPECTED_D22_STATE = ((6, (1, 1, 5, 5), 0, 0),)
COORDINATES = tuple(range(6))
EDGES = tuple(itertools.combinations(COORDINATES, 2))


def selected_edges(mask: int) -> frozenset[tuple[int, int]]:
    return frozenset(edge for index, edge in enumerate(EDGES) if mask >> index & 1)


def local_data(mask: int):
    edges = selected_edges(mask)
    degrees = tuple(sum(vertex in edge for edge in edges) for vertex in COORDINATES)
    triangles = tuple(
        triple
        for triple in itertools.combinations(COORDINATES, 3)
        if all(edge in edges for edge in itertools.combinations(triple, 2))
    )
    fathers = {vertex for vertex, degree in enumerate(degrees) if degree >= 2}
    local_defect = sum(degrees[vertex] - 1 for vertex in fathers)
    local_capacity = sum(
        ladder.FAMILY_CAPACITY[degrees[vertex] - 1] for vertex in fathers
    )
    father_edges = sum(first in fathers and second in fathers for first, second in edges)
    forced_deficit = 2 * father_edges + 2 * len(triangles)
    independence = max(
        len(vertices)
        for size in range(7)
        for vertices in itertools.combinations(COORDINATES, size)
        if all(edge not in edges for edge in itertools.combinations(vertices, 2))
    )
    return (
        tuple(sorted(degrees)),
        len(triangles),
        local_defect,
        local_capacity,
        forced_deficit,
        independence,
    )


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


def raw_states(mask: int, defect: int):
    _, _, local_defect, local_capacity, forced_deficit, _ = local_data(mask)
    states = []
    for couples in range((34 - defect) // 2 + 1):
        family_vertices = 104 - defect - 2 * couples
        family_budget = 34 - defect - 2 * couples
        for extra in defect_partitions(defect - local_defect):
            capacity = local_capacity + sum(ladder.FAMILY_CAPACITY[d] for d in extra)
            free_missing = capacity - family_vertices - forced_deficit
            if free_missing >= 0:
                states.append((couples, extra, free_missing, family_budget))
    return tuple(states)


def survives_defect_six(state: tuple[int, tuple[int, ...], int, int]) -> bool:
    _, extra, free_missing, family_budget = state
    forced_family_codewords = max(0, 8 * extra.count(6) - free_missing)
    return forced_family_codewords <= family_budget


def hamming_distance(first: int, second: int) -> int:
    return (first ^ second).bit_count()


def is_zero_slack_center(center: int, mask: int) -> bool:
    """Test the complete zero-slack full-noncodeword-F7 center conditions."""

    weight = center.bit_count()
    edges = selected_edges(mask)
    selected_local_words = {
        (1 << (first + 1)) | (1 << (second + 1)) for first, second in edges
    }
    fixed_selected = {0, *selected_local_words}
    fixed_absent = {
        *(1 << coordinate for coordinate in range(7)),
        *((1 << 0) | (1 << coordinate) for coordinate in range(1, 7)),
        *(
            (1 << (first + 1)) | (1 << (second + 1))
            for first, second in EDGES
            if (first, second) not in edges
        ),
    }

    if center in fixed_selected:
        return False
    neighbors = {center ^ (1 << coordinate) for coordinate in range(7)}
    if neighbors & fixed_absent:
        return False
    if weight <= 3:
        # Any normalized full-center candidate of weight three is a local
        # triangle, which costs a third missing local slot beyond the two
        # already charged by the triangle collision bound.
        return False
    if weight == 4:
        # A selected local word at distance two contradicts isolation of the
        # two common codeword neighbors of a full noncodeword F7 center.
        return all(hamming_distance(center, word) != 2 for word in selected_local_words)
    if weight == 5:
        # Alpha(H)=3 forces a supported selected local edge, hence a selected
        # word at distance three, forbidden by a full family.
        nonorphan_support = tuple(i - 1 for i in range(1, 7) if center & (1 << i))
        assert len(nonorphan_support) >= 4
        assert any(edge in edges for edge in itertools.combinations(nonorphan_support, 2))
        return False
    return True


def verify_branch(branch: int, representatives: list[int]) -> None:
    expected = EXPECTED[branch]
    mask = representatives[branch]
    assert mask == expected["mask"]
    assert mask.bit_count() == 8
    assert local_data(mask) == expected["data"]

    assert not raw_states(mask, 21)
    d22 = tuple(filter(survives_defect_six, raw_states(mask, 22)))
    assert d22 == EXPECTED_D22_STATE

    centers = tuple(center for center in range(128) if is_zero_slack_center(center, mask))
    assert centers == expected["centers"]
    distance_distribution = {
        distance: sum(
            hamming_distance(first, second) == distance
            for first, second in itertools.combinations(centers, 2)
        )
        for distance in range(1, 8)
    }
    distance_distribution = {
        distance: count for distance, count in distance_distribution.items() if count
    }
    assert max(distance_distribution) == 4
    assert not any(
        hamming_distance(first, second) >= 5
        for first, second in itertools.combinations(centers, 2)
    )
    print(
        f"PASS branch={branch} mask={mask} local_data={local_data(mask)} "
        f"D22_state={d22[0]} centers={centers} "
        f"distance_distribution={distance_distribution} D>=23"
    )


def main() -> None:
    representatives = ladder.representatives()
    assert len(representatives) == 115
    for branch in BRANCHES:
        verify_branch(branch, representatives)
    edge_table = ladder.edge_isoperimetric_table(7)
    assert edge_table[11] == 17
    print("PASS all five branches imply p>=47, a>=18, b<=11, edges<=E_7(11)=17")


if __name__ == "__main__":
    main()
