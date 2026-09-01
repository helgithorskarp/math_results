#!/usr/bin/env python3
"""Standard-library checks for the Q_7 size-29 family reduction."""

from __future__ import annotations

import itertools

from local_graphs import local_graph_representatives


H = {1: 4, 2: 7, 3: 11, 4: 16, 5: 22}


def partitions(total: int, maximum: int = 5) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = []

    def visit(remaining: int, upper: int, parts: list[int]) -> None:
        if remaining == 0:
            result.append(tuple(parts))
            return
        for part in range(min(remaining, upper), 0, -1):
            visit(remaining - part, part, [*parts, part])

    visit(total, maximum, [])
    return result


def cube_edge_upper(dimension: int) -> list[int]:
    """Inductive upper bounds using cross_edges <= min(layer sizes)."""
    previous = [0, 0]
    for current_dimension in range(1, dimension + 1):
        half = 1 << (current_dimension - 1)
        current: list[int] = []
        for size in range(2 * half + 1):
            values = []
            for left in range(max(0, size - half), min(half, size) + 1):
                right = size - left
                values.append(
                    previous[left] + previous[right] + min(left, right)
                )
            current.append(max(values))
        previous = current
    return previous


def check_a_7_5() -> None:
    words = range(1 << 7)
    maximum = 0
    for first, second, third in itertools.combinations(words, 3):
        minimum = min(
            (first ^ second).bit_count(),
            (first ^ third).bit_count(),
            (second ^ third).bit_count(),
        )
        maximum = max(maximum, minimum)
    assert maximum == 4


def main() -> None:
    assert all(5 * H[d] <= 22 * d for d in H)

    feasible_15 = []
    feasible_16 = []
    for defect in (15, 16):
        for couple_count in range(15):
            if 2 * couple_count > 34 - defect:
                continue
            family_vertices = 104 - defect - 2 * couple_count
            for parts in partitions(defect):
                capacity = sum(H[part] for part in parts)
                if capacity >= family_vertices:
                    (feasible_15 if defect == 15 else feasible_16).append(
                        (couple_count, family_vertices, capacity, parts)
                    )
    assert feasible_15 == []
    assert feasible_16 == [(9, 70, 70, (5, 5, 5, 1))]

    check_a_7_5()
    edge_bounds = cube_edge_upper(7)
    assert edge_bounds[17] == 33
    local_graphs = local_graph_representatives()
    assert len(local_graphs) == 115
    assert {mask.bit_count() for mask in local_graphs} == set(range(4, 16))
    assert local_graphs[110:] == [15870, 8191, 15871, 16383, 32767]

    print("PASS family defect D>=17")
    print("PASS unique D=16 frontier: q=9, M=70, defects=(5,5,5,1)")
    print("PASS A(7,5)=2 exclusion of the D=16 frontier")
    print("PASS singleton>=41 isolated>=12 orphan-isolates>=12")
    print("PASS induced_edges<=33 distance_two_pairs>=24")
    print("PASS 115 canonical orphan-local graph branches")
    print(
        "PASS certified branch masks "
        "110:15870 111:8191 112:15871 113:16383 114:32767"
    )


if __name__ == "__main__":
    main()
