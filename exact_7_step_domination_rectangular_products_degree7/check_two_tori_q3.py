#!/usr/bin/env python3
"""Independent exact checker for C_m square C_n square Q_3 at radius seven."""

from __future__ import annotations

import hashlib
import itertools
import sys
from fractions import Fraction
from pathlib import Path
from typing import Iterator


RADIUS = 7
MAXIMUM_SPHERE_SIZE = 176
MAXIMUM_ORDER = 6 * MAXIMUM_SPHERE_SIZE
MAXIMUM_TORUS_ORDER = MAXIMUM_ORDER // 8


def cycle_polynomial(modulus: int) -> list[int]:
    result = [0] * (modulus // 2 + 1)
    for value in range(modulus):
        result[min(value, modulus - value)] += 1
    return result


def convolve(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            result[i + j] += left_value * right_value
    return result


def product_sphere_size(dimensions: tuple[int, int]) -> int:
    polynomial = convolve(cycle_polynomial(dimensions[0]), cycle_polynomial(dimensions[1]))
    polynomial = convolve(polynomial, [1, 3, 3, 1])
    return polynomial[RADIUS] if RADIUS < len(polynomial) else 0


def direct_sphere(dimensions: tuple[int, int]) -> list[tuple[int, int, int]]:
    result = []
    for x, y, mask in itertools.product(
        range(dimensions[0]), range(dimensions[1]), range(8)
    ):
        distance = (
            min(x, dimensions[0] - x)
            + min(y, dimensions[1] - y)
            + mask.bit_count()
        )
        if distance == RADIUS:
            result.append((x, y, mask))
    return result


def trim(polynomial: list[Fraction]) -> None:
    while polynomial and polynomial[-1] == 0:
        polynomial.pop()


def polynomial_remainder(dividend: list[int], divisor: list[int]) -> tuple[int, ...]:
    remainder = [Fraction(value) for value in dividend]
    divisor_fraction = [Fraction(value) for value in divisor]
    trim(remainder)
    trim(divisor_fraction)
    while len(remainder) >= len(divisor_fraction):
        quotient = remainder[-1] / divisor_fraction[-1]
        offset = len(remainder) - len(divisor_fraction)
        for index, value in enumerate(divisor_fraction):
            remainder[index + offset] -= quotient * value
        trim(remainder)
    assert all(value.denominator == 1 for value in remainder)
    return tuple(int(value) for value in remainder)


def weak_compositions(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, parts - 1):
            yield (first, *tail)


def cyclic_convolution(left: tuple[int, ...], right: list[int]) -> list[int]:
    modulus = len(left)
    return [
        sum(left[index] * right[(residue - index) % modulus]
            for index in range(modulus))
        for residue in range(modulus)
    ]


def enumerate_candidates() -> tuple[int, set[tuple[int, int, int, int]]]:
    dimension_pairs = 0
    candidates: set[tuple[int, int, int, int]] = set()
    first = 3
    while first**2 <= MAXIMUM_TORUS_ORDER:
        second = first
        while first * second <= MAXIMUM_TORUS_ORDER:
            dimension_pairs += 1
            dimensions = (first, second)
            order = 8 * first * second
            size = product_sphere_size(dimensions)
            for centers in (4, 6):
                if centers * size == order:
                    candidates.add((centers, first, second, size))
            second += 1
        first += 1
    return dimension_pairs, candidates


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: checker /scratch/candidates.txt")
    raw = Path(sys.argv[1]).read_bytes()
    emitted_lines = [
        tuple(int(field) for field in line.split())
        for line in raw.decode().splitlines()
    ]
    assert all(len(candidate) == 4 for candidate in emitted_lines)
    emitted = set(emitted_lines)
    assert len(emitted) == len(emitted_lines)

    dimension_pairs, expected = enumerate_candidates()
    assert dimension_pairs == 144
    assert emitted == expected == {(6, 9, 9, 108)}

    sphere = direct_sphere((9, 9))
    assert len(sphere) == product_sphere_size((9, 9)) == 108
    profile = [0] * 9
    for x, _y, _mask in sphere:
        profile[x] += 1
    assert profile == [2, 8, 14, 16, 15, 15, 16, 14, 8]
    phi3_remainder = polynomial_remainder(profile, [1, 1, 1])
    phi9_remainder = polynomial_remainder(profile, [1, 0, 0, 1, 0, 0, 1])
    assert phi3_remainder == (-3,)
    assert phi9_remainder == (-14, -6, 6, 0, 1, 7)

    projected_profiles = 0
    target = [8 * 9] * 9
    for centers in weak_compositions(6, 9):
        projected_profiles += 1
        assert cyclic_convolution(centers, profile) != target
    assert projected_profiles == 3003

    print(f"radius={RADIUS}")
    print(f"maximum_group_order={MAXIMUM_ORDER}")
    print(f"dimension_pairs={dimension_pairs}")
    print("candidate=9x9x2x2x2 sphere=108")
    print("profile=" + ",".join(map(str, profile)))
    print(f"phi3_remainder={phi3_remainder}")
    print(f"phi9_remainder={phi9_remainder}")
    print(f"center_profiles_tested={projected_profiles}")
    print(f"candidate_sha256={hashlib.sha256(raw).hexdigest()}")
    print("four_center_counting_candidates=0")
    print("six_center_counting_candidates=1")
    print("four_center_tilings=0")
    print("six_center_tilings=0")


if __name__ == "__main__":
    main()
