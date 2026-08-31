#!/usr/bin/env python3
"""Independent checker for rectangular three-tori times K_2 at radius seven."""

from __future__ import annotations

import hashlib
import itertools
import sys
from fractions import Fraction
from pathlib import Path
from typing import Iterator


RADIUS = 7
MAXIMUM_SPHERE_SIZE = 344
MAXIMUM_ORDER = 6 * MAXIMUM_SPHERE_SIZE
MAXIMUM_THREE_TORUS_ORDER = MAXIMUM_ORDER // 2
CENTER_COUNT = 6


def cycle_polynomial(modulus: int) -> list[int]:
    result = [0] * (modulus // 2 + 1)
    for value in range(modulus):
        result[min(value, modulus - value)] += 1
    return result


def convolve(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for left_degree, left_value in enumerate(left):
        for right_degree, right_value in enumerate(right):
            result[left_degree + right_degree] += left_value * right_value
    return result


def product_sphere_size(dimensions: tuple[int, int, int]) -> int:
    polynomial = [1]
    for modulus in dimensions:
        polynomial = convolve(polynomial, cycle_polynomial(modulus))
    polynomial = convolve(polynomial, [1, 1])
    return polynomial[RADIUS] if RADIUS < len(polynomial) else 0


def direct_sphere(dimensions: tuple[int, int, int]) -> list[tuple[int, int, int, int]]:
    result = []
    for point in itertools.product(
        range(dimensions[0]), range(dimensions[1]), range(dimensions[2]), range(2)
    ):
        distance = point[3] + sum(
            min(point[index], dimensions[index] - point[index])
            for index in range(3)
        )
        if distance == RADIUS:
            result.append(point)
    return result


def projection_profile(
    dimensions: tuple[int, int, int],
    sphere: list[tuple[int, int, int, int]],
    axis: int,
) -> list[int]:
    result = [0] * dimensions[axis]
    for point in sphere:
        result[point[axis]] += 1
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


CYCLOTOMIC_FACTORS = {
    4: ((1, 1), (1, 0, 1)),
    7: ((1, 1, 1, 1, 1, 1, 1),),
    9: ((1, 1, 1), (1, 0, 0, 1, 0, 0, 1)),
}


def nontrivial_fourier_remainders(profile: list[int]) -> tuple[tuple[int, ...], ...]:
    factors = CYCLOTOMIC_FACTORS[len(profile)]
    remainders = tuple(
        polynomial_remainder(profile, list(factor)) for factor in factors
    )
    assert all(remainder for remainder in remainders)
    return remainders


def weak_compositions(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, parts - 1):
            yield (first, *tail)


def cyclic_convolution(left: tuple[int, ...], right: list[int]) -> list[int]:
    modulus = len(left)
    assert len(right) == modulus
    return [
        sum(left[index] * right[(residue - index) % modulus]
            for index in range(modulus))
        for residue in range(modulus)
    ]


def verify_no_projected_center_profile(
    profile: list[int], center_count: int, other_fiber_size: int
) -> int:
    tested = 0
    for centers in weak_compositions(center_count, len(profile)):
        tested += 1
        assert cyclic_convolution(centers, profile) != [other_fiber_size] * len(profile)
    return tested


def enumerate_candidates() -> tuple[int, int, set[tuple[int, int, int, int, int]]]:
    dimension_triples = 0
    eligible_dimension_triples = 0
    candidates: set[tuple[int, int, int, int, int]] = set()
    first = 3
    while first**3 <= MAXIMUM_THREE_TORUS_ORDER:
        second = first
        while first * second**2 <= MAXIMUM_THREE_TORUS_ORDER:
            third = second
            while first * second * third <= MAXIMUM_THREE_TORUS_ORDER:
                dimension_triples += 1
                dimensions = (first, second, third)
                order = 2 * first * second * third
                if order % 4 == 0 or order % 6 == 0:
                    eligible_dimension_triples += 1
                    size = product_sphere_size(dimensions)
                    for centers in (4, 6):
                        if centers * size == order:
                            candidates.add((centers, *dimensions, size))
                third += 1
            second += 1
        first += 1
    return dimension_triples, eligible_dimension_triples, candidates


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: checker /scratch/candidates.txt")
    candidate_path = Path(sys.argv[1])
    raw = candidate_path.read_bytes()
    emitted_lines = [
        tuple(int(field) for field in line.split())
        for line in raw.decode().splitlines()
    ]
    assert all(len(candidate) == 5 for candidate in emitted_lines)
    emitted = set(emitted_lines)
    assert len(emitted) == len(emitted_lines)

    dimension_triples, eligible_dimension_triples, expected = enumerate_candidates()
    assert dimension_triples == 1106
    assert eligible_dimension_triples == 1074
    assert emitted == expected == {
        (6, 4, 9, 9, 108),
        (6, 6, 7, 11, 154),
        (6, 6, 9, 10, 180),
        (6, 8, 9, 9, 216),
    }

    chosen_axis = {
        (4, 9, 9): 0,
        (6, 7, 11): 1,
        (6, 9, 10): 1,
        (8, 9, 9): 1,
    }
    expected_profiles = {
        (4, 9, 9): [20, 28, 32, 28],
        (6, 7, 11): [16, 22, 24, 23, 23, 24, 22],
        (6, 9, 10): [12, 19, 23, 23, 19, 19, 23, 23, 19],
        (8, 9, 9): [16, 24, 29, 27, 20, 20, 27, 29, 24],
    }
    for centers, first, second, third, size in sorted(expected):
        dimensions = (first, second, third)
        sphere = direct_sphere(dimensions)
        assert len(sphere) == size == product_sphere_size(dimensions)
        axis = chosen_axis[dimensions]
        profile = projection_profile(dimensions, sphere, axis)
        assert profile == expected_profiles[dimensions]
        remainders = nontrivial_fourier_remainders(profile)
        modulus = dimensions[axis]
        assert centers % modulus != 0
        other_fiber_size = 2 * first * second * third // modulus
        tested = verify_no_projected_center_profile(
            profile, centers, other_fiber_size
        )
        print(
            f"candidate={first}x{second}x{third}x2 sphere={size} "
            f"axis={modulus} profile={','.join(map(str, profile))} "
            f"remainders={remainders} center_profiles_tested={tested}"
        )

    print(f"radius={RADIUS}")
    print(f"maximum_group_order={MAXIMUM_ORDER}")
    print(f"dimension_triples={dimension_triples}")
    print(f"eligible_dimension_triples={eligible_dimension_triples}")
    print(f"candidate_sha256={hashlib.sha256(raw).hexdigest()}")
    print("four_center_counting_candidates=0")
    print("six_center_counting_candidates=4")
    print("four_center_tilings=0")
    print("six_center_tilings=0")


if __name__ == "__main__":
    main()
