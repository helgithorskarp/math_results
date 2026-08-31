#!/usr/bin/env python3
"""Independent checker for exact-degree-six four-involution candidates."""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
from functools import cached_property, lru_cache
from itertools import combinations
from math import comb, prod
from pathlib import Path

RADIUS = 7
MAXIMUM_ORDER = 192


def invariant_factor_types(limit: int):
    """A differently structured recursive enumeration of d1 | ... | dr."""
    def extend(prefix: tuple[int, ...], product: int):
        lower = 2 if not prefix else prefix[-1]
        for final in range(lower, limit // product + 1):
            if prefix and final % prefix[-1] != 0:
                continue
            factors = prefix + (final,)
            yield factors
            yield from extend(factors, product * final)

    yield from extend((), 1)


def expected_raw_description_count() -> int:
    total = 0
    for factors in invariant_factor_types(MAXIMUM_ORDER):
        order = prod(factors)
        if (order % 4 and order % 6) or len(factors) > 5:
            continue
        involution_count = 2 ** sum(factor % 2 == 0 for factor in factors) - 1
        pair_count = (order - 1 - involution_count) // 2
        total += pair_count * comb(involution_count, 4)
    return total


@dataclass(frozen=True)
class ProductGroup:
    factors: tuple[int, ...]

    @property
    def order(self) -> int:
        return prod(self.factors)

    def _decode(self, element: int) -> tuple[int, ...]:
        result = [0] * len(self.factors)
        for index in range(len(self.factors) - 1, -1, -1):
            result[index] = element % self.factors[index]
            element //= self.factors[index]
        return tuple(result)

    @cached_property
    def coordinates(self) -> tuple[tuple[int, ...], ...]:
        return tuple(self._decode(element) for element in range(self.order))

    def encode(self, coordinates: tuple[int, ...]) -> int:
        element = 0
        for coordinate, factor in zip(coordinates, self.factors):
            element = element * factor + coordinate
        return element

    @cached_property
    def addition_table(self) -> tuple[tuple[int, ...], ...]:
        return tuple(
            tuple(
                self.encode(tuple(
                    (a + b) % factor
                    for a, b, factor in zip(
                        self.coordinates[left], self.coordinates[right], self.factors
                    )
                ))
                for right in range(self.order)
            )
            for left in range(self.order)
        )

    @cached_property
    def inverses(self) -> tuple[int, ...]:
        return tuple(
            self.encode(tuple(
                (-coordinate) % factor
                for coordinate, factor in zip(
                    self.coordinates[element], self.factors
                )
            ))
            for element in range(self.order)
        )

    def add(self, left: int, right: int, sign: int = 1) -> int:
        if sign == -1:
            right = self.inverses[right]
        return self.addition_table[left][right]

    def inverse(self, element: int) -> int:
        return self.inverses[element]

    def distances(self, steps: tuple[int, ...]) -> list[int]:
        distance = [-1] * self.order
        distance[0] = 0
        queue = deque([0])
        while queue:
            element = queue.popleft()
            for step in steps:
                neighbour = self.add(element, step)
                if distance[neighbour] == -1:
                    distance[neighbour] = distance[element] + 1
                    queue.append(neighbour)
        return distance


def has_translate_tiling(
    group: ProductGroup, sphere: tuple[int, ...], center_count: int
) -> bool:
    full = (1 << group.order) - 1
    translate_cache: dict[int, int] = {}

    def translate(shift: int) -> int:
        if shift not in translate_cache:
            mask = 0
            for element in sphere:
                mask |= 1 << group.add(element, shift)
            translate_cache[shift] = mask
        return translate_cache[shift]

    initial = translate(0)

    @lru_cache(maxsize=None)
    def search(covered: int, remaining: int) -> bool:
        if remaining == 0:
            return covered == full
        uncovered = full ^ covered
        if not uncovered:
            return False
        first = (uncovered & -uncovered).bit_length() - 1
        tried: set[int] = set()
        for sphere_element in sphere:
            shift = group.add(first, sphere_element, -1)
            if shift in tried:
                continue
            tried.add(shift)
            candidate = translate(shift)
            if covered & candidate == 0 and search(
                covered | candidate, remaining - 1
            ):
                return True
        return False

    return search(initial, center_count - 1)


def parse_candidate(line: str):
    values = [int(value) for value in line.split()]
    center_count = values[0]
    rank = values[1]
    factors = tuple(values[2 : 2 + rank])
    cursor = 2 + rank
    generator_count = values[cursor]
    cursor += 1
    generators = tuple(values[cursor : cursor + generator_count])
    cursor += generator_count
    sphere_size = values[cursor]
    if cursor + 1 != len(values):
        raise ValueError("trailing candidate fields")
    return center_count, factors, generators, sphere_size


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate_file", type=Path)
    args = parser.parse_args()

    types = tuple(invariant_factor_types(MAXIMUM_ORDER))
    assert len(types) == 371
    assert expected_raw_description_count() == 10_237_220

    lines = args.candidate_file.read_text(encoding="utf-8").splitlines()
    if len(lines) != len(set(lines)):
        raise RuntimeError("candidate file contains duplicate descriptors")

    four_candidates = 0
    six_candidates = 0
    four_tilings = 0
    six_tilings = 0

    group_cache: dict[tuple[int, ...], ProductGroup] = {}
    for line_number, line in enumerate(lines, 1):
        center_count, factors, generators, claimed_size = parse_candidate(line)
        group = group_cache.setdefault(factors, ProductGroup(factors))
        if factors not in types or group.order > MAXIMUM_ORDER:
            raise RuntimeError(f"line {line_number}: invalid group type")
        if len(generators) != 5:
            raise RuntimeError(f"line {line_number}: expected five generators")
        generator, *involutions = generators
        if not generator < group.inverse(generator):
            raise RuntimeError(f"line {line_number}: bad inverse-pair representative")
        if len(set(involutions)) != 4 or any(
            value == 0 or group.inverse(value) != value for value in involutions
        ):
            raise RuntimeError(f"line {line_number}: bad involution set")
        steps = tuple(sorted({generator, group.inverse(generator), *involutions}))
        if len(steps) != 6:
            raise RuntimeError(f"line {line_number}: connection-set size is not six")

        distance = group.distances(steps)
        if -1 in distance:
            raise RuntimeError(f"line {line_number}: graph is disconnected")
        sphere = tuple(
            element for element, value in enumerate(distance) if value == RADIUS
        )
        if len(sphere) != claimed_size:
            raise RuntimeError(f"line {line_number}: sphere-size mismatch")
        if center_count * len(sphere) != group.order:
            raise RuntimeError(f"line {line_number}: counting identity fails")

        tiles = has_translate_tiling(group, sphere, center_count)
        if center_count == 4:
            four_candidates += 1
            four_tilings += int(tiles)
        elif center_count == 6:
            six_candidates += 1
            six_tilings += int(tiles)
        else:
            raise RuntimeError(f"line {line_number}: unexpected center count")

    print(f"invariant_factor_types={len(types)}")
    print(f"raw_connection_set_descriptions={expected_raw_description_count()}")
    print(f"candidate_descriptors={len(lines)}")
    print(f"four_center_candidates_checked={four_candidates}")
    print(f"six_center_candidates_checked={six_candidates}")
    print(f"four_center_tilings={four_tilings}")
    print(f"six_center_tilings={six_tilings}")

    if (
        four_candidates != 0
        or six_candidates != 8_960
        or four_tilings != 0
        or six_tilings != 0
    ):
        raise RuntimeError("unexpected independent-check result")


if __name__ == "__main__":
    main()
