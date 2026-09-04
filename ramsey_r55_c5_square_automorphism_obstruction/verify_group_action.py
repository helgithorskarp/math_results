#!/usr/bin/env python3
"""Verify the group-action classification behind the C5-square formula."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from generate_formula import ORDER, translate


Vector = tuple[int, int]


def add(left: Vector, right: Vector) -> Vector:
    return ((left[0] + right[0]) % 5, (left[1] + right[1]) % 5)


def line(vector: Vector) -> frozenset[Vector]:
    return frozenset(((scale * vector[0]) % 5, (scale * vector[1]) % 5)
                     for scale in range(5))


def projective_lines() -> list[frozenset[Vector]]:
    return sorted(
        {line(vector) for vector in itertools.product(range(5), repeat=2)
         if vector != (0, 0)},
        key=lambda item: sorted(item),
    )


def matrix_image(matrix: tuple[int, int, int, int], vector: Vector) -> Vector:
    first, second, third, fourth = matrix
    return (
        (first * vector[0] + second * vector[1]) % 5,
        (third * vector[0] + fourth * vector[1]) % 5,
    )


def group_action_orbits() -> list[list[int]]:
    unseen = set(range(ORDER))
    result = []
    while unseen:
        seed = min(unseen)
        orbit = {
            translate(seed, first, second)
            for first in range(5)
            for second in range(5)
        }
        unseen -= orbit
        result.append(sorted(orbit))
    return result


def fixed_points(element: Vector) -> int:
    return sum(translate(vertex, *element) == vertex for vertex in range(ORDER))


def build_result() -> dict[str, object]:
    elements = list(itertools.product(range(5), repeat=2))
    for element in elements:
        image = [translate(vertex, *element) for vertex in range(ORDER)]
        if sorted(image) != list(range(ORDER)):
            raise AssertionError(("non-permutation", element))
    for left in elements:
        for right in elements:
            total = add(left, right)
            for vertex in range(ORDER):
                if translate(translate(vertex, *left), *right) != translate(vertex, *total):
                    raise AssertionError(("group law", left, right, vertex))

    lines = projective_lines()
    if len(lines) != 6 or any(len(item) != 5 for item in lines):
        raise AssertionError("projective-line enumeration failed")

    admissible = []
    for global_fixed in range(ORDER + 1):
        for regular_orbits in range(2):
            possible_line_counts = [
                (fixed_count - global_fixed) // 5
                for fixed_count in (3, 8)
                if fixed_count >= global_fixed
                and (fixed_count - global_fixed) % 5 == 0
            ]
            for line_counts in itertools.product(possible_line_counts, repeat=6):
                if global_fixed + 25 * regular_orbits + 5 * sum(line_counts) != ORDER:
                    continue
                fixed_counts = [global_fixed + 5 * count for count in line_counts]
                if all(count in (3, 8) for count in fixed_counts):
                    admissible.append(
                        (global_fixed, line_counts, regular_orbits)
                    )
    expected = [
        (3, counts, 1)
        for counts in itertools.product((0, 1), repeat=6)
        if sum(counts) == 3
    ]
    if sorted(admissible) != sorted(expected):
        raise AssertionError("unexpected C5-square H-set classification")

    matrices = []
    for entries in itertools.product(range(5), repeat=4):
        first, second, third, fourth = entries
        if (first * fourth - second * third) % 5:
            matrices.append(entries)
    chosen = frozenset(range(3))
    triple_images = set()
    line_index = {item: index for index, item in enumerate(lines)}
    for matrix in matrices:
        image = frozenset(
            line_index[line(matrix_image(matrix, next(v for v in lines[index] if v != (0, 0))))]
            for index in chosen
        )
        triple_images.add(image)
    if len(matrices) != 480 or len(triple_images) != 20:
        raise AssertionError("GL(2,5) is not transitive on line triples")

    action_orbits = group_action_orbits()
    action_sizes = sorted(map(len, action_orbits))
    if action_sizes != [1, 1, 1, 5, 5, 5, 25]:
        raise AssertionError(action_sizes)
    nonzero = [element for element in itertools.product(range(5), repeat=2)
               if element != (0, 0)]
    fixed_distribution: dict[int, int] = {}
    for element in nonzero:
        count = fixed_points(element)
        fixed_distribution[count] = fixed_distribution.get(count, 0) + 1
    if fixed_distribution != {3: 12, 8: 12}:
        raise AssertionError(fixed_distribution)

    cyclic_order25 = []
    for five_cycles in range(4):
        fixed = ORDER - 25 - 5 * five_cycles
        if fixed < 0:
            continue
        cyclic_order25.append(
            {
                "cycles_25": 1,
                "cycles_5": five_cycles,
                "fixed_points": fixed,
                "fifth_power_cycles_5": 5,
            }
        )
    if any(item["fifth_power_cycles_5"] in (7, 8) for item in cyclic_order25):
        raise AssertionError("an order-25 cycle type survived")

    return {
        "C5_square": {
            "admissible_labeled_line_triples": len(admissible),
            "action_fixed_count_distribution": fixed_distribution,
            "action_orbit_sizes": action_sizes,
            "GL(2,5)_matrices": len(matrices),
            "line_triple_orbits": 1,
            "projective_lines": len(lines),
        },
        "cyclic_order25_cases": cyclic_order25,
        "format": "r55-c5-square-action-classification-v1",
        "order": ORDER,
        "surviving_order5_cycle_counts": [7, 8],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    result = build_result()
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        "PASS admissible_line_triples=20 line_triple_orbits=1 "
        "vertex_orbits=1,1,1,5,5,5,25 fixed_counts=3:12,8:12"
    )


if __name__ == "__main__":
    main()
