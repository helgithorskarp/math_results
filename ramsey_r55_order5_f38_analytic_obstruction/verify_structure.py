#!/usr/bin/env python3
"""Audit the finite orbit structure and arithmetic in the f=38 proof."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


def pair_orbits() -> list[list[tuple[int, int]]]:
    pairs = {tuple(pair) for pair in itertools.combinations(range(5), 2)}
    orbits = []
    while pairs:
        seed = min(pairs)
        orbit = {
            tuple(sorted(((seed[0] + shift) % 5, (seed[1] + shift) % 5)))
            for shift in range(5)
        }
        pairs -= orbit
        orbits.append(sorted(orbit))
    return sorted(orbits)


def color_degrees(
    orbits: list[list[tuple[int, int]]], assignment: tuple[int, ...], color: int
) -> list[int]:
    result = [0] * 5
    for orbit, orbit_color in zip(orbits, assignment, strict=True):
        if orbit_color != color:
            continue
        for left, right in orbit:
            result[left] += 1
            result[right] += 1
    return result


def build_result() -> dict[str, object]:
    orbits = pair_orbits()
    if [len(orbit) for orbit in orbits] != [5, 5]:
        raise AssertionError("unexpected pair-orbit structure")

    valid = []
    for assignment in itertools.product((0, 1), repeat=len(orbits)):
        if len(set(assignment)) == 1:
            continue
        degrees = [color_degrees(orbits, assignment, color) for color in (0, 1)]
        if degrees != [[2] * 5, [2] * 5]:
            raise AssertionError((assignment, degrees))
        valid.append({"orbit_colors": list(assignment), "degrees": degrees})

    degree_lower = 42 - (25 - 1)
    fixed_neighbor_lower = degree_lower - 2
    fixed_neighbor_upper = 14 - 1
    if not fixed_neighbor_lower > fixed_neighbor_upper:
        raise AssertionError("expected strict contradiction")

    return {
        "automorphism_order": 5,
        "contradiction_gap": fixed_neighbor_lower - fixed_neighbor_upper,
        "degree_lower_bound": degree_lower,
        "fixed_neighbor_lower_bound": fixed_neighbor_lower,
        "fixed_neighbor_upper_bound": fixed_neighbor_upper,
        "fixed_points": 38,
        "format": "r55-order5-f38-analytic-obstruction-v1",
        "moving_edge_orbit_sizes": [len(orbit) for orbit in orbits],
        "moving_edge_orbits": [
            [[left, right] for left, right in orbit] for orbit in orbits
        ],
        "moving_vertices": 5,
        "nonmonochromatic_orbit_assignments": valid,
        "ramsey_inputs": {"R(3,5)": 14, "R(4,5)": 25},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    result = build_result()
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        "PASS orbit_sizes=5,5 valid_assignments=2 "
        "fixed_neighbor_bounds=16,13 contradiction_gap=3"
    )


if __name__ == "__main__":
    main()
