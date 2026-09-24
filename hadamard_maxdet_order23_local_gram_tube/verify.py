#!/usr/bin/env python3
"""Definition-level checker for the local order-23 Gram certificate."""

from __future__ import annotations

import json
import math
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRIMES = (
    1000000007, 999999937, 999999929, 999999893, 999999883, 999999797,
    999999761, 999999757, 999999751, 999999739, 999999733, 999999677,
    999999667, 999999613, 999999607, 999999599, 999999587, 999999541,
    999999527, 999999503, 999999491, 999999487, 999999433, 999999391,
    999999353, 999999337, 999999323, 999999229, 999999223, 999999197,
    999999193, 999999191, 999999181, 999999163, 999999151, 999999137,
    999999131, 999999113, 999999107, 999999103, 999999067, 999999059,
    999999043, 999999029, 999999017, 999999001, 999998981, 999998971,
)


def read_record() -> list[list[int]]:
    rows = []
    for line in (HERE / "record23.txt").read_text().splitlines():
        row = [1 if symbol == "+" else -1 for symbol in line if symbol in "+-"]
        if row:
            assert len(row) == 23
            rows.append(row)
    assert len(rows) == 23
    return rows


def gram_matrix(record: list[list[int]]) -> list[list[int]]:
    return [
        [sum(left * right for left, right in zip(row_i, row_j)) for row_j in record]
        for row_i in record
    ]


def bareiss_determinant(matrix: list[list[int]]) -> int:
    work = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for column in range(len(work) - 1):
        pivot = next(
            (row for row in range(column, len(work)) if work[row][column]), None
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign = -sign
        pivot_value = work[column][column]
        for row in range(column + 1, len(work)):
            for col in range(column + 1, len(work)):
                numerator = (
                    work[row][col] * pivot_value
                    - work[row][column] * work[column][col]
                )
                assert numerator % previous == 0
                work[row][col] = numerator // previous
        previous = pivot_value
    return sign * work[-1][-1]


def inverse_scale(matrix: list[list[int]]) -> int:
    order = len(matrix)
    augmented = [
        [Fraction(value) for value in matrix[row]]
        + [Fraction(int(row == col)) for col in range(order)]
        for row in range(order)
    ]
    for column in range(order):
        pivot = next(row for row in range(column, order) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row in range(order):
            if row == column:
                continue
            multiplier = augmented[row][column]
            if multiplier:
                augmented[row] = [
                    left - multiplier * right
                    for left, right in zip(augmented[row], augmented[column])
                ]
    scale = 1
    for row in augmented:
        for value in row[order:]:
            scale = math.lcm(scale, value.denominator)
    numerator = [
        [int(augmented[i][order + j] * scale) for j in range(order)]
        for i in range(order)
    ]
    assert all(
        sum(matrix[i][k] * numerator[k][j] for k in range(order))
        == scale * int(i == j)
        for i in range(order)
        for j in range(order)
    )
    return scale


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def validate_edit(case_name: str, edits: list[list[int]], edges: list[tuple[int, int, int]]) -> None:
    expected_lengths = {
        "arbitrary_one_edit": 1,
        "arbitrary_two_edits": 2,
        "graph_three_edits": 3,
        "delete_four_three_edges": 4,
    }
    assert len(edits) == expected_lengths[case_name]
    indices = [edit[0] for edit in edits]
    assert indices == sorted(indices) and len(indices) == len(set(indices))
    for edge_index, new_value in edits:
        assert 0 <= edge_index < len(edges)
        old_value = edges[edge_index][2]
        assert new_value in range(-21, 20, 4) and new_value != old_value
        if case_name == "graph_three_edits":
            assert new_value == (3 if old_value == -1 else -1)
        if case_name == "delete_four_three_edges":
            assert old_value == 3 and new_value == -1


def expected_groups(case: dict) -> Counter[int]:
    groups = Counter()
    for item in case["square_groups"]:
        determinant = int(item["determinant"])
        root = int(item["square_root"])
        assert root * root == determinant
        groups[determinant] = int(item["multiplicity"])
    return groups


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 verify.py RESULT.json")
    result = json.loads(Path(sys.argv[1]).read_text())
    certificate = json.loads((HERE / "certificate.json").read_text())
    record = read_record()
    gram = gram_matrix(record)
    record_determinant = int(certificate["record_determinant"])
    assert bareiss_determinant(gram) == record_determinant**2
    assert Counter(
        gram[i][j] for i in range(23) for j in range(i)
    ) == Counter({-1: 208, 3: 45})
    assert inverse_scale(gram) == certificate["inverse_scale"] == result["inverse_scale"]
    assert result["order"] == certificate["order"] == 23
    assert tuple(result["witness_primes"]) == PRIMES
    assert all(is_prime(prime) and certificate["inverse_scale"] % prime for prime in PRIMES)

    edges = [(i, j, gram[i][j]) for i in range(23) for j in range(i)]
    one_edit_squares = 0
    for i, j, old_value in edges:
        for new_value in range(-21, 20, 4):
            if new_value == old_value:
                continue
            modified = [row[:] for row in gram]
            modified[i][j] = modified[j][i] = new_value
            determinant = bareiss_determinant(modified)
            if determinant >= 0 and math.isqrt(determinant) ** 2 == determinant:
                one_edit_squares += 1
    assert one_edit_squares == 0

    for case_name, expected in certificate["cases"].items():
        observed = result["cases"][case_name]
        assert observed["total"] == expected["total"]
        assert observed["witness_counts"] == expected["witness_counts"]
        survivors = observed["survivor_edits"]
        assert observed["survives_48_nonsquare_tests"] == expected["survivors"]
        assert len(survivors) == expected["survivors"]
        assert sum(observed["witness_counts"]) + len(survivors) == observed["total"]
        canonical_survivors = {
            tuple((int(edge), int(value)) for edge, value in edits)
            for edits in survivors
        }
        assert len(canonical_survivors) == len(survivors)

        determinant_groups: Counter[int] = Counter()
        for edits in survivors:
            validate_edit(case_name, edits, edges)
            modified = [row[:] for row in gram]
            for edge_index, new_value in edits:
                i, j, _ = edges[edge_index]
                modified[i][j] = modified[j][i] = new_value
            determinant = bareiss_determinant(modified)
            assert determinant >= 0
            root = math.isqrt(determinant)
            assert root * root == determinant
            assert root < record_determinant
            determinant_groups[determinant] += 1
        assert determinant_groups == expected_groups(expected)
        print(
            f"{case_name}: {observed['total']} matrices, "
            f"{len(survivors)} exact square survivors, all below record"
        )

    print("exact local Gram exclusion certificate verified")


if __name__ == "__main__":
    main()
