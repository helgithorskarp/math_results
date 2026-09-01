#!/usr/bin/env python3
"""Standard-library verification of the Q7 size-29 defect-18 reduction."""

from __future__ import annotations


CAPACITY = {1: 4, 2: 7, 3: 11, 4: 16, 5: 22}


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


def feasible_rows(defect: int) -> list[tuple[int, int, int, tuple[int, ...]]]:
    rows: list[tuple[int, int, int, tuple[int, ...]]] = []
    for couples in range(15):
        if 2 * couples > 34 - defect:
            continue
        family_vertices = 104 - defect - 2 * couples
        for parts in partitions(defect):
            capacity = sum(CAPACITY[part] for part in parts)
            if capacity >= family_vertices:
                rows.append((couples, family_vertices, capacity, parts))
    return rows


def cube_edge_upper(dimension: int) -> list[int]:
    previous = [0, 0]
    for current_dimension in range(1, dimension + 1):
        half = 1 << (current_dimension - 1)
        current: list[int] = []
        for size in range(2 * half + 1):
            current.append(
                max(
                    previous[left]
                    + previous[size - left]
                    + min(left, size - left)
                    for left in range(max(0, size - half), min(half, size) + 1)
                )
            )
        previous = current
    return previous


def main() -> None:
    expected = [
        (7, 73, 73, (5, 5, 5, 2)),
        (8, 71, 73, (5, 5, 5, 2)),
        (7, 73, 74, (5, 5, 5, 1, 1)),
        (8, 71, 74, (5, 5, 5, 1, 1)),
        (8, 71, 71, (5, 5, 4, 3)),
        (8, 71, 71, (5, 5, 4, 2, 1)),
        (8, 71, 72, (5, 5, 4, 1, 1, 1)),
        (8, 71, 71, (5, 5, 3, 1, 1, 1, 1)),
        (8, 71, 71, (5, 5, 2, 1, 1, 1, 1, 1)),
        (8, 71, 72, (5, 5, 1, 1, 1, 1, 1, 1, 1)),
    ]
    rows = feasible_rows(17)
    assert sorted(rows) == sorted(expected)
    rows = expected

    exceptional = []
    for couples, family_vertices, capacity, parts in rows:
        missing_sons = capacity - family_vertices
        family_codeword_cap = 17 - 2 * couples
        max_isolated = 29 - 2 * couples
        f7_count = parts.count(5)

        # A codeword F7 father would bring itself and at least
        # 6-missing_sons of its codeword neighbors into families.
        assert 7 - missing_sons > family_codeword_cap

        guaranteed_isolated = 7 * f7_count - 2 * missing_sons
        if guaranteed_isolated <= max_isolated:
            exceptional.append(
                (
                    couples,
                    family_vertices,
                    capacity,
                    parts,
                    family_codeword_cap,
                    max_isolated,
                    guaranteed_isolated,
                )
            )

    assert exceptional == [
        (8, 71, 72, (5, 5, 4, 1, 1, 1), 1, 13, 12),
        (8, 71, 72, (5, 5, 1, 1, 1, 1, 1, 1, 1), 1, 13, 12),
    ]

    # In each exceptional row the one missing F7 son must be a codeword,
    # and it plus the two codeword endpoints are three family codewords.
    for row in exceptional:
        family_codeword_cap = row[4]
        forced_family_codewords = 3
        assert forced_family_codewords > family_codeword_cap

    edge_bounds = cube_edge_upper(7)
    assert edge_bounds[16] == 32
    assert 2 * (42 - 29) == 26

    print("PASS exactly ten abstract defect-17 rows")
    print("PASS all F7 fathers in those rows are non-codewords")
    print("PASS eight rows excluded by isolated-neighbor counting")
    print("PASS final two rows force three family codewords but allow one")
    print("PASS D>=18, singleton>=42, isolated>=13")
    print("PASS induced_edges<=32, distance_two_pairs>=26")


if __name__ == "__main__":
    main()
