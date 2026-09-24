#!/usr/bin/env python3
"""Definition-level checker for the fourteen explicit transpose equivalences."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ORDER = 23
DECOMPOSITION_CERTIFICATE_SHA256 = (
    "7b94f5918015a250db3619c7e1f2f37a8d31a3e2ad589afe21a99a30a445aa81"
)
EXPECTED_CLASS_MAP = [11, 12, 7, 8, 5, 6, 3, 4, 9, 10, 1, 2, 13, 14]


def vector_from_mask(mask: int) -> list[int]:
    return [1] + [-1 if (mask >> bit) & 1 else 1 for bit in range(ORDER - 1)]


def representative_matrix(masks: list[int]) -> list[list[int]]:
    assert len(masks) == ORDER and masks == sorted(masks)
    columns = [vector_from_mask(mask) for mask in masks]
    return [[columns[column][row] for column in range(ORDER)] for row in range(ORDER)]


def gram(matrix: list[list[int]]) -> list[list[int]]:
    return [
        [
            sum(matrix[left][column] * matrix[right][column] for column in range(ORDER))
            for right in range(ORDER)
        ]
        for left in range(ORDER)
    ]


def transformed_transpose(
    matrix: list[list[int]], report: dict[str, object]
) -> list[list[int]]:
    row_permutation = report["row_permutation"]
    row_signs = report["row_signs"]
    column_permutation = report["column_permutation"]
    column_signs = report["column_signs"]
    assert sorted(row_permutation) == list(range(ORDER))
    assert sorted(column_permutation) == list(range(ORDER))
    assert set(row_signs) <= {-1, 1} and len(row_signs) == ORDER
    assert set(column_signs) <= {-1, 1} and len(column_signs) == ORDER
    result = [[0] * ORDER for _ in range(ORDER)]
    for source_row in range(ORDER):
        for source_column in range(ORDER):
            result[row_permutation[source_row]][column_permutation[source_column]] = (
                row_signs[source_row]
                * column_signs[source_column]
                * matrix[source_column][source_row]
            )
    return result


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: python3 verify_transpose_duality.py "
            "DECOMPOSITIONS.json TRANSPOSE.json"
        )
    decomposition_path = Path(sys.argv[1])
    transpose_path = Path(sys.argv[2])
    assert hashlib.sha256(
        decomposition_path.read_bytes()
    ).hexdigest() == DECOMPOSITION_CERTIFICATE_SHA256
    decomposition = json.loads(decomposition_path.read_text())
    certificate = json.loads(transpose_path.read_text())

    assert certificate["order"] == decomposition["order"] == ORDER
    assert (
        certificate["decomposition_certificate_sha256"]
        == DECOMPOSITION_CERTIFICATE_SHA256
    )
    matrices = {
        report["class"]: representative_matrix(report["column_masks"])
        for report in decomposition["orbits"]
    }
    assert sorted(matrices) == list(range(1, 15))
    base = gram(matrices[14])
    assert all(gram(matrix) == base for matrix in matrices.values())

    reports = certificate["equivalences"]
    assert [report["source_class"] for report in reports] == list(range(1, 15))
    observed_map = []
    for report in reports:
        source_class = report["source_class"]
        target_class = report["target_class"]
        observed_map.append(target_class)
        transformed = transformed_transpose(matrices[source_class], report)
        assert transformed == matrices[target_class]

    assert observed_map == certificate["transpose_class_map"] == EXPECTED_CLASS_MAP
    assert all(observed_map[observed_map[index] - 1] == index + 1 for index in range(14))
    assert certificate["fixed_classes"] == [5, 6, 9, 10, 13, 14]
    assert certificate["two_cycles"] == [[1, 11], [2, 12], [3, 7], [4, 8]]

    print("fourteen explicit signed transpose equivalences verified")
    print("transpose pairs: (1,11), (2,12), (3,7), (4,8)")
    print("self-dual classes: 5, 6, 9, 10, 13, 14")
    print("every representative column Gram is signed-permutation equivalent to G0")


if __name__ == "__main__":
    main()
