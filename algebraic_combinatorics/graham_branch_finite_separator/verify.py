#!/usr/bin/env python3
"""Exact audit of the one-quotient separator theorem.

The universal theorem is proved in THEOREM.md.  This checker independently
tests integer row-lattice membership by determinantal divisors and finite
quotient separation by direct subgroup generation modulo m.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from itertools import combinations, product
from math import gcd
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parent
Vector = tuple[int, ...]
Matrix = tuple[Vector, ...]


def validate_matrix(rows: Sequence[Sequence[int]], width: int | None = None) -> Matrix:
    matrix = tuple(tuple(row) for row in rows)
    if width is None:
        if not matrix:
            raise ValueError("width is required for an empty matrix")
        width = len(matrix[0])
    if type(width) is not int or width < 1:
        raise ValueError("width must be a positive integer")
    if any(len(row) != width for row in matrix):
        raise ValueError("inconsistent row width")
    if any(type(value) is not int for row in matrix for value in row):
        raise ValueError("matrix entries must be integers")
    return matrix


def determinant(square: Sequence[Sequence[int]]) -> int:
    """Bareiss determinant over the integers."""

    matrix = [list(row) for row in square]
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError("determinant needs a square matrix")
    if size == 0:
        return 1
    sign = 1
    previous = 1
    for pivot_index in range(size - 1):
        pivot_row = next(
            (row for row in range(pivot_index, size) if matrix[row][pivot_index]),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != pivot_index:
            matrix[pivot_index], matrix[pivot_row] = matrix[pivot_row], matrix[pivot_index]
            sign = -sign
        pivot = matrix[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = (
                    matrix[row][column] * pivot
                    - matrix[row][pivot_index] * matrix[pivot_index][column]
                )
                if numerator % previous:
                    raise AssertionError("Bareiss division was not exact")
                matrix[row][column] = numerator // previous
            matrix[row][pivot_index] = 0
        previous = pivot
    return sign * matrix[-1][-1]


def rational_rank(rows: Sequence[Sequence[int]], width: int | None = None) -> int:
    matrix = validate_matrix(rows, width)
    if not matrix:
        return 0
    work = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(rank, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [value / scale for value in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                work[row][entry] - scale * work[rank][entry]
                for entry in range(len(work[0]))
            ]
        rank += 1
        if rank == len(work):
            break
    return rank


def determinantal_divisor(
    rows: Sequence[Sequence[int]], order: int, width: int | None = None
) -> int:
    matrix = validate_matrix(rows, width)
    if order == 0:
        return 1
    if order < 0 or order > len(matrix) or order > width:
        return 0
    result = 0
    for row_indices in combinations(range(len(matrix)), order):
        for columns in combinations(range(width), order):
            minor = [[matrix[row][column] for column in columns] for row in row_indices]
            result = gcd(result, abs(determinant(minor)))
    return result


def in_integer_row_lattice(
    rows: Sequence[Sequence[int]], target: Sequence[int]
) -> bool:
    vector = tuple(target)
    if not vector or any(type(value) is not int for value in vector):
        raise ValueError("target must be a nonempty integer vector")
    matrix = validate_matrix(rows, len(vector))
    rank = rational_rank(matrix, len(vector))
    augmented = matrix + (vector,)
    if rational_rank(augmented, len(vector)) != rank:
        return False
    if rank == 0:
        return all(value == 0 for value in vector)
    return (
        determinantal_divisor(matrix, rank, len(vector))
        == determinantal_divisor(augmented, rank, len(vector))
    )


def forbidden_targets(width: int) -> tuple[Vector, ...]:
    if type(width) is not int or width < 1:
        raise ValueError("width must be positive")
    result = []
    for first in range(width):
        vector = [0] * width
        vector[first] = 1
        result.append(tuple(vector))
    for first in range(width):
        for second in range(first + 1, width):
            vector = [0] * width
            vector[first] = 1
            vector[second] = -1
            result.append(tuple(vector))
    return tuple(result)


def row_subgroup_mod(
    rows: Sequence[Sequence[int]], width: int, modulus: int
) -> frozenset[Vector]:
    matrix = validate_matrix(rows, width)
    if type(modulus) is not int or modulus < 2:
        raise ValueError("modulus must be at least two")
    subgroup = {(0,) * width}
    for row in matrix:
        subgroup = {
            tuple((base[column] + coefficient * row[column]) % modulus
                  for column in range(width))
            for base in subgroup
            for coefficient in range(modulus)
        }
    return frozenset(subgroup)


def quotient_separates(
    rows: Sequence[Sequence[int]], targets: Iterable[Sequence[int]], modulus: int
) -> bool:
    targets = tuple(tuple(target) for target in targets)
    if not targets:
        raise ValueError("at least one target is required")
    width = len(targets[0])
    if any(len(target) != width for target in targets):
        raise ValueError("inconsistent target width")
    subgroup = row_subgroup_mod(rows, width, modulus)
    return all(
        tuple(value % modulus for value in target) not in subgroup
        for target in targets
    )


def least_separator_modulus(
    rows: Sequence[Sequence[int]], targets: Iterable[Sequence[int]], limit: int
) -> int:
    targets = tuple(tuple(target) for target in targets)
    if type(limit) is not int or limit < 2:
        raise ValueError("limit must be at least two")
    if any(in_integer_row_lattice(rows, target) for target in targets):
        raise ValueError("a forbidden target already lies in the integer row lattice")
    for modulus in range(2, limit + 1):
        if quotient_separates(rows, targets, modulus):
            return modulus
    raise LookupError("no separator found within the requested limit")


TWO_TORSION_ROWS: Matrix = (
    (1, 1, 1, 1, 0, 0),
    (0, 1, 1, 0, 1, 0),
    (0, 0, 1, 1, 1, 1),
    (1, 0, 0, 1, 1, 0),
)

THREE_TORSION_ROWS: Matrix = (
    (0, 1, 1, 1, 1, 1),
    (0, 0, 1, 1, 1, 0),
    (1, 1, 1, 0, 0, 0),
    (1, 0, 0, 1, 0, 0),
    (1, 0, 0, 0, 1, 1),
)


def explicit_case(name: str, rows: Matrix, expected_modulus: int) -> dict[str, int | str]:
    targets = forbidden_targets(6)
    modulus = least_separator_modulus(rows, targets, 12)
    if modulus != expected_modulus:
        raise AssertionError((name, modulus, expected_modulus))
    subgroup = row_subgroup_mod(rows, 6, modulus)
    quotient_order = modulus**6 // len(subgroup)
    rank = rational_rank(rows, 6)
    divisor = determinantal_divisor(rows, rank, 6)
    return {
        "name": name,
        "row_rank": rank,
        "top_determinantal_divisor": divisor,
        "least_separator_modulus": modulus,
        "row_subgroup_order": len(subgroup),
        "quotient_order": quotient_order,
        "forbidden_targets_preserved": len(targets),
    }


def binary_matrix_audit(max_width: int, maximum_rows: int) -> dict[str, object]:
    matrices = 0
    terminal = 0
    separated = 0
    histogram: dict[int, int] = {}
    records = []
    for width in range(2, max_width + 1):
        nonzero_rows = [
            tuple(bits)
            for bits in product((0, 1), repeat=width)
            if any(bits)
        ]
        targets = forbidden_targets(width)
        for row_count in range(min(maximum_rows, len(nonzero_rows)) + 1):
            for rows in combinations(nonzero_rows, row_count):
                matrices += 1
                hits = sum(in_integer_row_lattice(rows, target) for target in targets)
                if hits:
                    terminal += 1
                    records.append(f"{width}|{rows}|terminal|{hits}")
                    continue
                modulus = least_separator_modulus(rows, targets, 24)
                if not quotient_separates(rows, targets, modulus):
                    raise AssertionError((width, rows, modulus))
                if modulus > 2 and quotient_separates(rows, targets, modulus - 1):
                    raise AssertionError("separator is not minimal")
                separated += 1
                histogram[modulus] = histogram.get(modulus, 0) + 1
                records.append(f"{width}|{rows}|separator|{modulus}")
    digest = hashlib.sha256(("\n".join(records) + "\n").encode()).hexdigest()
    return {
        "max_width": max_width,
        "maximum_rows": maximum_rows,
        "matrices": matrices,
        "terminal_matrices": terminal,
        "separated_matrices": separated,
        "separator_histogram": {str(key): histogram[key] for key in sorted(histogram)},
        "record_sha256": digest,
    }


def audit(max_width: int, maximum_rows: int) -> dict[str, object]:
    cases = [
        explicit_case("characteristic_two_branch", TWO_TORSION_ROWS, 2),
        explicit_case("characteristic_three_branch", THREE_TORSION_ROWS, 3),
    ]
    return {
        "status": "PASS",
        "arithmetic": "Python integers and Fraction",
        "explicit_cases": cases,
        "binary_matrix_audit": binary_matrix_audit(max_width, maximum_rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-width", type=int, default=5)
    parser.add_argument("--maximum-rows", type=int, default=3)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    if args.max_width < 2 or args.maximum_rows < 0:
        raise ValueError("invalid audit bounds")
    result = audit(args.max_width, args.maximum_rows)
    if args.check_expected:
        expected = json.loads((ROOT / "EXPECTED.json").read_text())
        if result != expected:
            raise AssertionError((result, expected))
    print(json.dumps(result, indent=2, sort_keys=True))
    print("ONE-QUOTIENT SEPARATOR VERIFIED")


if __name__ == "__main__":
    main()
