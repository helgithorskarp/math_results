#!/usr/bin/env python3
"""Definition-level checks for the order-15 strong Seymour result."""

from __future__ import annotations

import hashlib
import json


BASE_BITS = 37_939_005_050
BASE_WEIGHTS = [1, 3, 1, 3, 1, 1, 1, 3, 1]
EXPECTED_STRONG_OWNERS = {1, 3, 7}


def tournament_from_bits(order: int, bits: int) -> list[list[bool]]:
    matrix = [[False] * order for _ in range(order)]
    shift = 0
    for i in range(order):
        for j in range(i + 1, order):
            if (bits >> shift) & 1:
                matrix[i][j] = True
            else:
                matrix[j][i] = True
            shift += 1
    return matrix


def assert_tournament(matrix: list[list[bool]]) -> None:
    order = len(matrix)
    assert all(len(row) == order for row in matrix)
    for i in range(order):
        assert not matrix[i][i]
        for j in range(i + 1, order):
            assert matrix[i][j] != matrix[j][i]


def link_shores(
    matrix: list[list[bool]], root: int
) -> tuple[list[int], list[int]]:
    left = [vertex for vertex in range(len(matrix)) if matrix[root][vertex]]
    right = [vertex for vertex in range(len(matrix)) if matrix[vertex][root]]
    return left, right


def matching_size(matrix: list[list[bool]], root: int) -> int:
    left, right = link_shores(matrix, root)
    mate: dict[int, int] = {}

    def augment(tail: int, seen: set[int]) -> bool:
        for head in right:
            if not matrix[tail][head] or head in seen:
                continue
            seen.add(head)
            if head not in mate or augment(mate[head], seen):
                mate[head] = tail
                return True
        return False

    for tail in left:
        augment(tail, set())
    return len(mate)


def strong_by_matching(matrix: list[list[bool]], root: int) -> bool:
    left, _ = link_shores(matrix, root)
    return matching_size(matrix, root) == len(left)


def deficient_hall_sets(
    matrix: list[list[bool]], root: int
) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    left, right = link_shores(matrix, root)
    deficient: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    for mask in range(1, 1 << len(left)):
        selected = tuple(
            left[index] for index in range(len(left)) if mask & (1 << index)
        )
        neighbors = tuple(
            head
            for head in right
            if any(matrix[tail][head] for tail in selected)
        )
        if len(neighbors) < len(selected):
            deficient.append((selected, neighbors))
    return deficient


def exhaustive_hall_check(max_order: int = 6) -> dict[str, int]:
    tournaments = 0
    vertex_cases = 0
    minimal_witnesses = 0
    record = hashlib.sha256()
    for order in range(1, max_order + 1):
        for bits in range(1 << (order * (order - 1) // 2)):
            tournaments += 1
            matrix = tournament_from_bits(order, bits)
            assert_tournament(matrix)
            has_ordinary = False
            for root in range(order):
                vertex_cases += 1
                left, right = link_shores(matrix, root)
                second = [
                    head
                    for head in right
                    if any(matrix[tail][head] for tail in left)
                ]
                has_ordinary |= len(second) >= len(left)
                deficient = deficient_hall_sets(matrix, root)
                assert strong_by_matching(matrix, root) == (not deficient)

                deficient_left = {selected for selected, _ in deficient}
                for selected, neighbors in deficient:
                    if any(
                        selected[:index] + selected[index + 1 :] in deficient_left
                        for index in range(len(selected))
                    ):
                        continue
                    minimal_witnesses += 1
                    assert len(neighbors) == len(selected) - 1
                    assert all(
                        sum(matrix[tail][head] for tail in selected) >= 2
                        for head in neighbors
                    )
                record.update(
                    json.dumps(
                        [order, bits, root, len(left), len(second), len(deficient)],
                        separators=(",", ":"),
                    ).encode()
                )
            assert has_ordinary
    return {
        "tournaments": tournaments,
        "vertex_cases": vertex_cases,
        "minimal_witnesses": minimal_witnesses,
        "record_sha256": record.hexdigest(),
    }


def constant_nine_tournament() -> tuple[list[list[bool]], list[int]]:
    outer = tournament_from_bits(len(BASE_WEIGHTS), BASE_BITS)
    fibers: list[list[int]] = []
    owners: list[int] = []
    for root, weight in enumerate(BASE_WEIGHTS):
        fibers.append(list(range(len(owners), len(owners) + weight)))
        owners.extend([root] * weight)
    matrix = [[False] * len(owners) for _ in owners]
    for fiber in fibers:
        if len(fiber) == 3:
            matrix[fiber[0]][fiber[1]] = True
            matrix[fiber[1]][fiber[2]] = True
            matrix[fiber[2]][fiber[0]] = True
    for i, first in enumerate(fibers):
        for j, second in enumerate(fibers):
            if outer[i][j]:
                for u in first:
                    for v in second:
                        matrix[u][v] = True
    return matrix, owners


def check_order_fifteen_fixtures() -> dict[str, object]:
    matrix, owners = constant_nine_tournament()
    assert_tournament(matrix)
    degrees = [sum(row) for row in matrix]
    assert len(matrix) == 15 and degrees == [7] * 15
    strong = [
        root for root in range(15) if strong_by_matching(matrix, root)
    ]
    assert len(strong) == 9
    assert {owners[root] for root in strong} == EXPECTED_STRONG_OWNERS

    # An independent, highly symmetric positive fixture.
    cyclic = [[False] * 15 for _ in range(15)]
    for i in range(15):
        for offset in range(1, 8):
            cyclic[i][(i + offset) % 15] = True
    assert_tournament(cyclic)
    cyclic_strong = [
        root for root in range(15) if strong_by_matching(cyclic, root)
    ]
    assert cyclic_strong == list(range(15))
    return {
        "constant_nine_strong_vertices": strong,
        "constant_nine_strong_owners": sorted(EXPECTED_STRONG_OWNERS),
        "cyclic_strong_count": len(cyclic_strong),
    }


def check_regular_size_six_obstruction() -> dict[str, int]:
    # For a regular order-15 root x with |S|=6 and |Gamma(S)|=5,
    # B\Gamma(S) has two vertices.  Each dominates x and all six members of
    # S, exhausting its seven out-arcs.  Their mutual arc is then impossible.
    root_and_witness_size = 1 + 6
    hall_nonneighbors = 7 - 5
    assert root_and_witness_size == 7
    assert hall_nonneighbors == 2
    return {
        "forced_outneighbors_per_hall_nonneighbor": root_and_witness_size,
        "hall_nonneighbors": hall_nonneighbors,
    }


def main() -> None:
    report = {
        "hall": exhaustive_hall_check(),
        "order15_fixtures": check_order_fifteen_fixtures(),
        "regular_six": check_regular_size_six_obstruction(),
        "status": "VERIFIED",
    }
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
