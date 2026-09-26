#!/usr/bin/env python3
"""Independent exact checks for the minimal-matroid magic-index proof.

This program deliberately does not import the reviewed implementation.  It
reconstructs each Ehrhart polynomial from integer lattice-slice counts using
Newton forward differences, divides out the known binomial factor, and changes
bases by a triangular coefficient formula.  All arithmetic is exact.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction

Polynomial = list[Fraction]  # coefficients in ascending monomial order


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def trim(poly: Polynomial) -> Polynomial:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = [Fraction(0) for _ in range(max(len(left), len(right)))]
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += value
    return trim(result)


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result = [Fraction(0) for _ in range(len(left) + len(right) - 1)]
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            result[i + j] += left_value * right_value
    return trim(result)


def scale(poly: Polynomial, scalar: Fraction) -> Polynomial:
    return trim([scalar * value for value in poly])


def evaluate(poly: Polynomial, point: Fraction) -> Fraction:
    value = Fraction(0)
    for coefficient in reversed(poly):
        value = value * point + coefficient
    return value


def divide(dividend: Polynomial, divisor: Polynomial) -> tuple[Polynomial, Polynomial]:
    remainder = dividend[:]
    quotient = [Fraction(0) for _ in range(max(1, len(dividend) - len(divisor) + 1))]
    while len(remainder) >= len(divisor) and remainder != [Fraction(0)]:
        degree_gap = len(remainder) - len(divisor)
        coefficient = remainder[-1] / divisor[-1]
        quotient[degree_gap] += coefficient
        for index, value in enumerate(divisor):
            remainder[index + degree_gap] -= coefficient * value
        trim(remainder)
    return trim(quotient), trim(remainder)


def binomial_polynomial(order: int) -> Polynomial:
    result = [Fraction(1)]
    for offset in range(order):
        result = multiply(result, [Fraction(-offset), Fraction(1)])
    return scale(result, Fraction(1, math.factorial(order)))


def slice_count(dilation: int, k: int, r: int) -> int:
    return sum(
        math.comb(total + k - 1, k - 1) * math.comb(total + r - 1, r - 1)
        for total in range(dilation + 1)
    )


def interpolate_from_values(values: list[int]) -> Polynomial:
    """Newton interpolation: p(x)=sum_j Delta^j p(0) binom(x,j)."""
    row = [Fraction(value) for value in values]
    forward = []
    while row:
        forward.append(row[0])
        row = [row[index + 1] - row[index] for index in range(len(row) - 1)]
    result = [Fraction(0)]
    for order, coefficient in enumerate(forward):
        result = add(result, scale(binomial_polynomial(order), coefficient))
    return trim(result)


def binomial_factor(r: int) -> Polynomial:
    result = [Fraction(1)]
    for root_size in range(1, r + 1):
        result = multiply(result, [Fraction(root_size), Fraction(1)])
    return scale(result, Fraction(1, math.factorial(r)))


def magic_coefficients(poly: Polynomial, dilation: Fraction) -> list[Fraction]:
    """Coefficients in x^i(x+1)^(d-i), obtained triangularly."""
    degree = len(poly) - 1
    dilated = [coefficient * dilation**power for power, coefficient in enumerate(poly)]
    return [
        sum(
            (-1) ** (index - power) * math.comb(degree - power, index - power) * dilated[power]
            for power in range(index + 1)
        )
        for index in range(degree + 1)
    ]


def from_magic(coefficients: list[Fraction]) -> Polynomial:
    degree = len(coefficients) - 1
    result = [Fraction(0)]
    for index, coefficient in enumerate(coefficients):
        basis = [Fraction(0)] * index + [Fraction(1)]
        for _ in range(degree - index):
            basis = multiply(basis, [Fraction(1), Fraction(1)])
        result = add(result, scale(basis, coefficient))
    return result


def dilate(poly: Polynomial, amount: Fraction) -> Polynomial:
    return [coefficient * amount**power for power, coefficient in enumerate(poly)]


def brute_slice_count(dilation: int, k: int, r: int) -> int:
    """Enumerate both coordinate blocks, independently of stars and bars."""
    left_counts = [0] * (dilation + 1)
    right_counts = [0] * (dilation + 1)
    for vector in itertools.product(range(dilation + 1), repeat=k):
        if sum(vector) <= dilation:
            left_counts[sum(vector)] += 1
    for vector in itertools.product(range(dilation + 1), repeat=r):
        if sum(vector) <= dilation:
            right_counts[sum(vector)] += 1
    return sum(left * right for left, right in zip(left_counts, right_counts, strict=True))


def as_pair(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def main() -> None:
    max_n = 24
    cases = 0
    sign_checks = 0
    magic_vectors = 0
    previous_integer_checks = 0
    records: list[dict[str, object]] = []

    for n in range(2, max_n + 1):
        for k in range(1, n // 2 + 1):
            r = n - k
            degree = n - 1
            values = [slice_count(point, k, r) for point in range(degree + 1)]
            ehrhart = interpolate_from_values(values)
            require(len(ehrhart) - 1 == degree, f"degree mismatch for {(k, r)}")
            require(
                evaluate(ehrhart, Fraction(degree + 1)) == slice_count(degree + 1, k, r),
                f"holdout value mismatch for {(k, r)}",
            )
            require(
                ehrhart
                == interpolate_from_values(
                    [slice_count(point, r, k) for point in range(degree + 1)]
                ),
                f"duality mismatch for {(k, r)}",
            )

            residual, remainder = divide(ehrhart, binomial_factor(r))
            require(remainder == [Fraction(0)], f"division remainder for {(k, r)}")
            require(len(residual) - 1 == k - 1, f"residual degree for {(k, r)}")
            normalization = math.comb(k + r - 1, k - 1)
            signs = []
            for h in range(1, k + 1):
                actual = evaluate(residual, Fraction(-h))
                expected = Fraction((-1) ** (h - 1) * math.comb(r - 1, h - 1), normalization)
                require(actual == expected, f"residual sign identity for {(k, r, h)}")
                signs.append(as_pair(actual))
                sign_checks += 1

            boundary = magic_coefficients(ehrhart, Fraction(r))
            require(all(value > 0 for value in boundary[:-1]), f"boundary signs for {(k, r)}")
            require(boundary[-1] == 0, f"boundary top coefficient for {(k, r)}")
            require(
                from_magic(boundary) == dilate(ehrhart, Fraction(r)),
                f"boundary reconstruction for {(k, r)}",
            )

            above = magic_coefficients(ehrhart, Fraction(2 * r + 1, 2))
            require(all(value > 0 for value in above), f"above-threshold signs for {(k, r)}")
            require(
                from_magic(above) == dilate(ehrhart, Fraction(2 * r + 1, 2)),
                f"above-threshold reconstruction for {(k, r)}",
            )

            below = magic_coefficients(ehrhart, Fraction(2 * r - 1, 2))
            require(any(value < 0 for value in below), f"below-threshold sign for {(k, r)}")
            require(
                from_magic(below) == dilate(ehrhart, Fraction(2 * r - 1, 2)),
                f"below-threshold reconstruction for {(k, r)}",
            )
            magic_vectors += 3

            if r > 1:
                previous = magic_coefficients(ehrhart, Fraction(r - 1))
                require(any(value < 0 for value in previous), f"prior-integer sign for {(k, r)}")
                previous_integer_checks += 1

            records.append(
                {
                    "k": k,
                    "n": n,
                    "leftmost_binomial_root": -r,
                    "boundary_top_magic": as_pair(boundary[-1]),
                    "residual_signs": signs,
                }
            )
            cases += 1

    brute_checks = 0
    for k in range(1, 5):
        for r in range(k, 5):
            for dilation in range(4):
                require(
                    brute_slice_count(dilation, k, r) == slice_count(dilation, k, r),
                    f"brute slice mismatch for {(dilation, k, r)}",
                )
                brute_checks += 1

    canonical_records = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    result = {
        "all_checks_passed": True,
        "arithmetic": "fractions.Fraction and Python integers",
        "brute_coordinate_checks": brute_checks,
        "cases": cases,
        "magic_vectors_checked": magic_vectors,
        "max_n": max_n,
        "method": "slice values -> Newton forward differences -> exact division/basis change",
        "previous_integer_checks": previous_integer_checks,
        "record_sha256": hashlib.sha256(canonical_records).hexdigest(),
        "residual_sign_checks": sign_checks,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
