#!/usr/bin/env python3
"""Independently check every degree-five counting candidate and tiling."""

from __future__ import annotations

import argparse
from collections import Counter, deque
from pathlib import Path


RADIUS = 7


class AbelianGroup:
    """A direct product of cyclic groups with a precomputed addition table."""

    def __init__(self, factors: tuple[int, ...]) -> None:
        self.factors = factors
        self.order = 1
        for factor in factors:
            self.order *= factor
        self.coordinates = [self.decode(element) for element in range(self.order)]
        self.addition = [
            [self.encode_sum(left, right) for right in self.coordinates]
            for left in self.coordinates
        ]
        self.inverse = [
            self.encode(tuple((-value) % factor for value, factor in zip(row, factors)))
            for row in self.coordinates
        ]

    def decode(self, element: int) -> tuple[int, ...]:
        result = [0] * len(self.factors)
        for index in range(len(self.factors) - 1, -1, -1):
            result[index] = element % self.factors[index]
            element //= self.factors[index]
        return tuple(result)

    def encode(self, coordinates: tuple[int, ...]) -> int:
        result = 0
        for value, factor in zip(coordinates, self.factors):
            result = result * factor + value
        return result

    def encode_sum(self, left: tuple[int, ...], right: tuple[int, ...]) -> int:
        return self.encode(
            tuple(
                (first + second) % factor
                for first, second, factor in zip(left, right, self.factors)
            )
        )

    def sphere(self, generators: tuple[int, ...]) -> list[int]:
        distance = [-1] * self.order
        distance[0] = 0
        queue = deque([0])
        while queue:
            element = queue.popleft()
            for generator in generators:
                for step in (generator, self.inverse[generator]):
                    neighbour = self.addition[element][step]
                    if distance[neighbour] == -1:
                        distance[neighbour] = distance[element] + 1
                        queue.append(neighbour)
        assert all(value >= 0 for value in distance)
        return [
            element for element, value in enumerate(distance) if value == RADIUS
        ]

    def has_translate_tiling(self, sphere: list[int], center_count: int) -> bool:
        assert len(sphere) * center_count == self.order
        full = (1 << self.order) - 1
        translates = []
        for shift in range(self.order):
            mask = 0
            for element in sphere:
                mask |= 1 << self.addition[element][shift]
            translates.append(mask)
        initial = translates[0]

        def search(covered: int, remaining: int) -> bool:
            if remaining == 0:
                return covered == full
            uncovered = full ^ covered
            if uncovered == 0:
                return False
            first = (uncovered & -uncovered).bit_length() - 1
            tried = set()
            for sphere_element in sphere:
                shift = self.addition[first][self.inverse[sphere_element]]
                if shift in tried:
                    continue
                tried.add(shift)
                translated = translates[shift]
                if translated & covered == 0 and search(
                    covered | translated, remaining - 1
                ):
                    return True
            return False

        return search(initial, center_count - 1)


def parse_candidate(line: str) -> tuple[int, tuple[int, ...], tuple[int, ...], int]:
    fields = [int(value) for value in line.split()]
    center_count = fields[0]
    rank = fields[1]
    factors = tuple(fields[2 : 2 + rank])
    offset = 2 + rank
    generator_count = fields[offset]
    generators = tuple(fields[offset + 1 : offset + 1 + generator_count])
    offset += 1 + generator_count
    assert offset + 1 == len(fields)
    return center_count, factors, generators, fields[offset]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate_file", type=Path)
    args = parser.parse_args()

    counts: Counter[int] = Counter()
    tilings: Counter[int] = Counter()
    current_factors: tuple[int, ...] | None = None
    group: AbelianGroup | None = None

    with args.candidate_file.open(encoding="ascii") as input_file:
        for line_number, line in enumerate(input_file, start=1):
            center_count, factors, generators, claimed_size = parse_candidate(line)
            if factors != current_factors:
                group = AbelianGroup(factors)
                current_factors = factors
            assert group is not None
            assert center_count in (4, 6)
            assert all(0 < generator < group.order for generator in generators)
            connection_set = set(generators) | {
                group.inverse[generator] for generator in generators
            }
            assert len(connection_set) == 5
            if len(generators) == 3:
                assert all(
                    generator != group.inverse[generator]
                    for generator in generators[:2]
                )
                assert generators[2] == group.inverse[generators[2]]
            else:
                assert len(generators) == 4
                assert generators[0] != group.inverse[generators[0]]
                assert all(
                    generator == group.inverse[generator]
                    for generator in generators[1:]
                )
            sphere = group.sphere(generators)
            assert len(sphere) == claimed_size
            assert center_count * len(sphere) == group.order
            counts[center_count] += 1
            tilings[center_count] += group.has_translate_tiling(
                sphere, center_count
            )
            if line_number % 5000 == 0:
                print(f"checked_candidates={line_number}", flush=True)

    assert counts == Counter({6: 25304, 4: 702})
    assert tilings[4] == 0 and tilings[6] == 0
    print(f"four_center_candidates_checked={counts[4]}")
    print(f"six_center_candidates_checked={counts[6]}")
    print(f"four_center_tilings={tilings[4]}")
    print(f"six_center_tilings={tilings[6]}")


if __name__ == "__main__":
    main()
