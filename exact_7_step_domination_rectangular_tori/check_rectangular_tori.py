#!/usr/bin/env python3
"""Independent checker for rectangular three-torus exact-7 candidates."""

from __future__ import annotations

import collections
import hashlib
import sys
from pathlib import Path

RADIUS = 7
MAXIMUM_ORDER = 6 * 198


def cycle_polynomial(modulus: int) -> list[int]:
    counts = [0] * (modulus // 2 + 1)
    for value in range(modulus):
        counts[min(value, modulus - value)] += 1
    return counts


def convolve(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def product_sphere_size(dimensions: tuple[int, int, int]) -> int:
    polynomial = [1]
    for modulus in dimensions:
        polynomial = convolve(polynomial, cycle_polynomial(modulus))
    return polynomial[RADIUS] if RADIUS < len(polynomial) else 0


def encode(point: tuple[int, int, int], dimensions: tuple[int, int, int]) -> int:
    x, y, z = point
    _, second, third = dimensions
    return (x * second + y) * third + z


def decode(value: int, dimensions: tuple[int, int, int]) -> tuple[int, int, int]:
    _, second, third = dimensions
    z = value % third
    value //= third
    y = value % second
    return value // second, y, z


def add(left: int, right: int, dimensions: tuple[int, int, int]) -> int:
    a = decode(left, dimensions)
    b = decode(right, dimensions)
    return encode(tuple((a[i] + b[i]) % dimensions[i] for i in range(3)), dimensions)


def subtract(left: int, right: int, dimensions: tuple[int, int, int]) -> int:
    a = decode(left, dimensions)
    b = decode(right, dimensions)
    return encode(tuple((a[i] - b[i]) % dimensions[i] for i in range(3)), dimensions)


def bfs_sphere(dimensions: tuple[int, int, int]) -> list[int]:
    order = dimensions[0] * dimensions[1] * dimensions[2]
    steps = []
    for coordinate in range(3):
        for sign in (-1, 1):
            point = [0, 0, 0]
            point[coordinate] = sign % dimensions[coordinate]
            steps.append(encode(tuple(point), dimensions))
    distances = [-1] * order
    distances[0] = 0
    queue = collections.deque([0])
    while queue:
        value = queue.popleft()
        for step in steps:
            neighbour = add(value, step, dimensions)
            if distances[neighbour] == -1:
                distances[neighbour] = distances[value] + 1
                queue.append(neighbour)
    if any(distance == -1 for distance in distances):
        raise AssertionError("standard generators unexpectedly disconnected")
    return [value for value, distance in enumerate(distances) if distance == RADIUS]


def projection_profile(dimensions: tuple[int, int, int],
                       sphere: list[int]) -> list[int]:
    result = [0] * dimensions[0]
    for value in sphere:
        result[decode(value, dimensions)[0]] += 1
    return result


def full_nontrivial_fourier_support(profile: list[int]) -> bool:
    """Check exact cyclotomic remainders for the candidate moduli 7 and 8."""
    if len(profile) == 7:
        # Every nontrivial seventh root has minimal polynomial
        # Phi_7 = 1+x+...+x^6.  A degree-at-most-six polynomial vanishes
        # there exactly when all seven coefficients are equal.
        return len(set(profile)) != 1
    if len(profile) == 8:
        # The nontrivial eighth roots have orders 2, 4, or 8.  Test the
        # remainders modulo Phi_2=x+1, Phi_4=x^2+1, and Phi_8=x^4+1.
        at_minus_one = sum((-1) ** index * value
                           for index, value in enumerate(profile))
        modulo_phi4 = [
            profile[0] - profile[2] + profile[4] - profile[6],
            profile[1] - profile[3] + profile[5] - profile[7],
        ]
        modulo_phi8 = [profile[index] - profile[index + 4]
                       for index in range(4)]
        return (at_minus_one != 0 and any(modulo_phi4)
                and any(modulo_phi8))
    raise AssertionError("unexpected projection modulus")


def shifted_mask(sphere: list[int], shift: int,
                 dimensions: tuple[int, int, int]) -> int:
    result = 0
    for value in sphere:
        result |= 1 << add(value, shift, dimensions)
    return result


def has_exact_cover(dimensions: tuple[int, int, int], sphere: list[int],
                    center_count: int) -> bool:
    order = dimensions[0] * dimensions[1] * dimensions[2]
    if center_count * len(sphere) != order:
        return False
    masks = [shifted_mask(sphere, shift, dimensions) for shift in range(order)]
    full = (1 << order) - 1

    def search(covered: int, remaining: int) -> bool:
        if remaining == 0:
            return covered == full
        uncovered = ((~covered) & full & -((~covered) & full)).bit_length() - 1
        tried: set[int] = set()
        for element in sphere:
            shift = subtract(uncovered, element, dimensions)
            if shift in tried:
                continue
            tried.add(shift)
            mask = masks[shift]
            if covered & mask == 0 and search(covered | mask, remaining - 1):
                return True
        return False

    return search(masks[0], center_count - 1)


def enumerate_candidates() -> tuple[int, int, set[tuple[int, ...]]]:
    dimension_triples = 0
    eligible_triples = 0
    candidates: set[tuple[int, ...]] = set()
    first = 3
    while first**3 <= MAXIMUM_ORDER:
        second = first
        while first * second**2 <= MAXIMUM_ORDER:
            third = second
            while first * second * third <= MAXIMUM_ORDER:
                dimension_triples += 1
                dimensions = (first, second, third)
                order = first * second * third
                if order % 4 == 0 or order % 6 == 0:
                    eligible_triples += 1
                    size = product_sphere_size(dimensions)
                    for center_count in (4, 6):
                        if center_count * size == order:
                            candidates.add((*dimensions, center_count, size))
                third += 1
            second += 1
        first += 1
    return dimension_triples, eligible_triples, candidates


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: checker /scratch/candidates.txt")
    candidate_path = Path(sys.argv[1])
    raw = candidate_path.read_bytes()
    emitted: dict[tuple[int, ...], int] = {}
    for line_number, line in enumerate(raw.decode().splitlines(), 1):
        fields = [int(field) for field in line.split()]
        if len(fields) != 6:
            raise AssertionError(f"malformed line {line_number}")
        center_count, first, second, third, size, claimed_tiling = fields
        key = (first, second, third, center_count, size)
        if key in emitted:
            raise AssertionError(f"duplicate line {line_number}")
        emitted[key] = claimed_tiling

    dimension_triples, eligible_triples, expected = enumerate_candidates()
    if dimension_triples != 1369 or eligible_triples != 1089:
        raise AssertionError("unexpected dimension-triple counts")
    if set(emitted) != expected:
        raise AssertionError("emitted candidates differ from independent scan")

    four_candidates = 0
    six_candidates = 0
    four_tilings = 0
    six_tilings = 0
    profiles: list[tuple[tuple[int, int, int], list[int]]] = []
    for first, second, third, center_count, size in sorted(expected):
        dimensions = (first, second, third)
        sphere = bfs_sphere(dimensions)
        if len(sphere) != size:
            raise AssertionError(f"BFS sphere mismatch for {dimensions}")
        profile = projection_profile(dimensions, sphere)
        if not full_nontrivial_fourier_support(profile):
            raise AssertionError(f"projection certificate failed for {dimensions}")
        if center_count % first == 0:
            raise AssertionError("projection divisibility obstruction unavailable")
        profiles.append((dimensions, profile))
        tiling = has_exact_cover(dimensions, sphere, center_count)
        if emitted[(first, second, third, center_count, size)] != int(tiling):
            raise AssertionError(f"tiling mismatch for {dimensions}")
        if center_count == 4:
            four_candidates += 1
            four_tilings += int(tiling)
        else:
            six_candidates += 1
            six_tilings += int(tiling)

    if four_candidates != 0 or six_candidates != 3:
        raise AssertionError("unexpected candidate counts")
    if four_tilings != 0 or six_tilings != 0:
        raise AssertionError("unexpected tiling")

    print(f"radius={RADIUS}")
    print(f"maximum_group_order={MAXIMUM_ORDER}")
    print(f"dimension_triples={dimension_triples}")
    print(f"eligible_dimension_triples={eligible_triples}")
    print(f"candidate_sha256={hashlib.sha256(raw).hexdigest()}")
    for dimensions, profile in profiles:
        label = "x".join(str(value) for value in dimensions)
        print(f"projection_profile_{label}="
              + ",".join(str(value) for value in profile))
    print(f"four_center_candidates_checked={four_candidates}")
    print(f"six_center_candidates_checked={six_candidates}")
    print(f"four_center_tilings={four_tilings}")
    print(f"six_center_tilings={six_tilings}")


if __name__ == "__main__":
    main()
