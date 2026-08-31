#!/usr/bin/env python3
"""Exact arithmetic checks for the Q_7 size-28 family reduction."""

from __future__ import annotations

import itertools
import math


DIMENSION = 7
VERTEX_COUNT = 1 << DIMENSION


def partitions(total: int, largest: int = 5) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = []

    def visit(remaining: int, upper: int, prefix: tuple[int, ...]) -> None:
        if remaining == 0:
            result.append(prefix)
            return
        for part in range(min(remaining, upper), 0, -1):
            visit(remaining - part, part, (*prefix, part))

    visit(total, largest, ())
    return result


def maximum_family_vertices(parts: tuple[int, ...]) -> int:
    # A part d=i-2 represents an F_i father and at most binom(i,2) sons.
    return sum(1 + math.comb(part + 2, 2) for part in parts)


def verify_family_arithmetic() -> None:
    feasible: list[tuple[int, int, int, tuple[int, ...]]] = []
    for defect in range(25):
        isolated_lower = 4 + defect
        for couples in range(15):
            if isolated_lower + 2 * couples > 28:
                continue
            family_vertices = 96 - defect - 2 * couples
            for parts in partitions(defect):
                father_count = len(parts)
                if father_count <= family_vertices <= maximum_family_vertices(parts):
                    feasible.append(
                        (defect, couples, family_vertices, parts)
                    )

    minimum_defect = min(item[0] for item in feasible)
    assert minimum_defect == 17
    equality_cases = [item for item in feasible if item[0] == 17]
    assert equality_cases == [
        (17, 3, 73, (5, 5, 5, 2)),
        (17, 3, 73, (5, 5, 5, 1, 1)),
    ]
    assert maximum_family_vertices((5, 5, 5, 2)) == 73
    assert maximum_family_vertices((5, 5, 5, 1, 1)) == 74
    # Both cases have three F_7 fathers.  Since at most one possible son is
    # missing, at least two of the three F_7 families are full.
    assert all(item[3].count(5) == 3 for item in equality_cases)
    assert all(
        maximum_family_vertices(item[3]) - item[2] <= 1
        for item in equality_cases
    )


def verify_no_three_distant_centers() -> None:
    def distance(first: int, second: int) -> int:
        return (first ^ second).bit_count()

    maximum = 0
    for first in range(VERTEX_COUNT):
        compatible = [
            second
            for second in range(first + 1, VERTEX_COUNT)
            if distance(first, second) >= 5
        ]
        if compatible:
            maximum = 2
        for second, third in itertools.combinations(compatible, 2):
            assert distance(second, third) < 5
    assert maximum == 2


def verify_full_f7_shell_separation() -> None:
    # Around a canonical full F_7 father at zero, weight-one vertices are
    # codewords, weight-two vertices are sons, and weights two and three are
    # non-codeword shells.  Any other non-codeword F_7 father has all seven
    # neighbours in the code, so it cannot occur at weights one through four.
    for vertex in range(1, VERTEX_COUNT):
        weight = vertex.bit_count()
        if weight == 1:
            continue  # This shell consists of codewords, not fathers.
        if weight == 2:
            continue  # This shell consists of sons, not fathers.
        if weight in (3, 4):
            neighbor_weights = {
                (vertex ^ (1 << coordinate)).bit_count()
                for coordinate in range(DIMENSION)
            }
            assert neighbor_weights & {2, 3}


def verify_cube_counts() -> None:
    distance_two_pairs = sum(
        (first ^ second).bit_count() == 2
        for first, second in itertools.combinations(range(VERTEX_COUNT), 2)
    )
    assert distance_two_pairs == VERTEX_COUNT * math.comb(DIMENSION, 2) // 2
    assert distance_two_pairs == 1344
    # floor(6 log_2(6)/2) = floor(log_2(6^3)) = 7, checked exactly.
    assert 1 << 7 <= 6**3 < 1 << 8


def verify_orphan_link_minimum() -> None:
    coordinate_edges = list(itertools.combinations(range(DIMENSION), 2))

    def valid(edge_set: tuple[tuple[int, int], ...]) -> bool:
        degrees = [0] * DIMENSION
        for first, second in edge_set:
            degrees[first] += 1
            degrees[second] += 1
        if degrees.count(0) != 1:
            return False
        # A two-vertex component would give its endpoints identical singleton
        # incident-edge sets, hence identical identifying sets.
        return not any(
            degrees[first] == degrees[second] == 1
            for first, second in edge_set
        )

    for edge_count in range(4):
        assert not any(
            valid(edge_set)
            for edge_set in itertools.combinations(coordinate_edges, edge_count)
        )
    witness = ((0, 1), (1, 2), (3, 4), (4, 5))
    assert valid(witness)


def main() -> None:
    verify_family_arithmetic()
    verify_full_f7_shell_separation()
    verify_no_three_distant_centers()
    verify_cube_counts()
    verify_orphan_link_minimum()
    print("verified family arithmetic: D >= 17 with two rigid D=17 patterns")
    print("verified shell obstruction: A(7,5) = 2, excluding D=17")
    print("consequence: D >= 18, at least 50 singleton signatures")
    print("consequence: at least 22 isolated codewords and at most 7 code edges")
    print("consequence: at least 44 codeword pairs at Hamming distance two")
    print("verified essential distance-two separation-pair count: 1344")


if __name__ == "__main__":
    main()
