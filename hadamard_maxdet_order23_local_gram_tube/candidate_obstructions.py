#!/usr/bin/env python3
"""Exact column obstructions for the two record-beating radius-six Grams.

If an invertible sign matrix R has row Gram G=R R^T, then every column v of
R satisfies v^T G^{-1} v=1 because R^T G^{-1} R=I.  Column negation lets us
normalize v[0]=1.  This program exhausts those 2^22 normalized sign vectors
using exact integer arithmetic after an exact rational inversion of G.
"""

from __future__ import annotations

import hashlib
import math
from fractions import Fraction

from verify import bareiss_determinant, gram_matrix, read_record


ORDER = 23
RECORD_DETERMINANT = 2779447296000000
CANDIDATES = (
    {
        "edges": (10, 22, 38, 47, 89, 92),
        "determinant_root": 2823605452800000,
        "inverse_scale": 51563888640,
        "normalized_column_count": 0,
        "normalized_columns_sha256": (
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        ),
    },
    {
        "edges": (2, 11, 36, 38, 46, 78),
        "determinant_root": 2783182848000000,
        "inverse_scale": 18035310240,
        "normalized_column_count": 48,
        "normalized_columns_sha256": (
            "3993d08e87f4f935d7e8e90612672609b4e6b97f806daacca64d302d510dfd47"
        ),
    },
)


def candidate_gram(base: list[list[int]], edit_indices: tuple[int, ...]) -> list[list[int]]:
    edges = tuple((left, right) for left in range(ORDER) for right in range(left))
    result = [row[:] for row in base]
    for index in edit_indices:
        left, right = edges[index]
        result[left][right] = result[right][left] = 2 - base[left][right]
    return result


def scaled_inverse(matrix: list[list[int]]) -> tuple[int, list[list[int]]]:
    """Return (Q,P) with matrix*P=Q*I, using exact Gauss--Jordan."""
    size = len(matrix)
    augmented = [
        [Fraction(value) for value in matrix[row]]
        + [Fraction(row == column) for column in range(size)]
        for row in range(size)
    ]
    for column in range(size):
        if augmented[column][column] == 0:
            pivot = next(
                row
                for row in range(column + 1, size)
                if augmented[row][column]
            )
            augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row in range(size):
            if row == column or augmented[row][column] == 0:
                continue
            multiplier = augmented[row][column]
            augmented[row] = [
                value - multiplier * pivot
                for value, pivot in zip(augmented[row], augmented[column])
            ]
    inverse = [row[size:] for row in augmented]
    scale = 1
    for row in inverse:
        for value in row:
            scale = math.lcm(scale, value.denominator)
    numerator = [[int(value * scale) for value in row] for row in inverse]
    assert numerator == [list(row) for row in zip(*numerator)]
    assert all(
        sum(matrix[i][middle] * numerator[middle][j] for middle in range(size))
        == scale * (i == j)
        for i in range(size)
        for j in range(size)
    )
    return scale, numerator


def quadratic(numerator: list[list[int]], vector: list[int]) -> int:
    return sum(
        numerator[i][j] * vector[i] * vector[j]
        for i in range(ORDER)
        for j in range(ORDER)
    )


def enumerate_normalized_columns(scale: int, numerator: list[list[int]]) -> list[int]:
    """Return Gray-code masks for all v in {+1,-1}^23 with v[0]=1 and q(v)=Q."""
    vector = [1] * ORDER
    # row_sums[i] omits the diagonal and supports an O(23) exact Gray update.
    row_sums = [
        sum(numerator[i][j] * vector[j] for j in range(ORDER) if i != j)
        for i in range(ORDER)
    ]
    value = quadratic(numerator, vector)
    masks: list[int] = []
    gray = 0
    limit = 1 << (ORDER - 1)
    for step in range(limit):
        if value == scale:
            masks.append(gray)
        if step + 1 == limit:
            break
        transition = step + 1
        bit = (transition & -transition).bit_length() - 1
        coordinate = bit + 1
        old_sign = vector[coordinate]
        value -= 4 * old_sign * row_sums[coordinate]
        for row in range(ORDER):
            if row != coordinate:
                row_sums[row] -= 2 * numerator[row][coordinate] * old_sign
        vector[coordinate] = -old_sign
        gray ^= 1 << bit

        if step in (12344, 1048575):
            assert value == quadratic(numerator, vector)
    return masks


def vector_from_mask(mask: int) -> list[int]:
    return [1] + [
        -1 if (mask >> bit) & 1 else 1 for bit in range(ORDER - 1)
    ]


def mask_hash(masks: list[int]) -> str:
    encoded = "".join(f"{mask}\n" for mask in masks).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def positive_control(record: list[list[int]], base: list[list[int]]) -> None:
    scale, numerator = scaled_inverse(base)
    for column in range(ORDER):
        vector = [record[row][column] for row in range(ORDER)]
        if vector[0] < 0:
            vector = [-value for value in vector]
        assert vector[0] == 1
        assert quadratic(numerator, vector) == scale


def main() -> None:
    record = read_record()
    base = gram_matrix(record)
    assert bareiss_determinant(base) == RECORD_DETERMINANT**2
    positive_control(record, base)

    observed: list[list[int]] = []
    for case in CANDIDATES:
        matrix = candidate_gram(base, case["edges"])
        determinant = bareiss_determinant(matrix)
        assert determinant == case["determinant_root"] ** 2
        assert case["determinant_root"] > RECORD_DETERMINANT
        # Sylvester's criterion, checked without floating point.
        assert all(
            bareiss_determinant([row[:size] for row in matrix[:size]]) > 0
            for size in range(1, ORDER + 1)
        )
        scale, numerator = scaled_inverse(matrix)
        assert scale == case["inverse_scale"]
        masks = enumerate_normalized_columns(scale, numerator)
        assert len(masks) == case["normalized_column_count"]
        assert mask_hash(masks) == case["normalized_columns_sha256"]
        for mask in masks:
            vector = vector_from_mask(mask)
            assert quadratic(numerator, vector) == scale
        observed.append(masks)

    # The first candidate has no possible sign column at all.
    assert observed[0] == []
    # For the second, every possible normalized column has v_0 v_1=1.
    # A 23-column decomposition would therefore have Gram entry 23, whereas
    # the candidate has entry 3.
    assert observed[1]
    assert all(vector_from_mask(mask)[0] * vector_from_mask(mask)[1] == 1 for mask in observed[1])
    second = candidate_gram(base, CANDIDATES[1]["edges"])
    assert second[0][1] == 3 != ORDER

    print("candidate 1: no normalized sign column satisfies v^T G^-1 v = 1")
    print("candidate 2: 48 normalized columns, all with v[0]v[1] = 1")
    print("both record-beating radius-six Gram candidates are indecomposable")


if __name__ == "__main__":
    main()
