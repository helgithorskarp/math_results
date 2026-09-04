#!/usr/bin/env python3
"""Exhaustively audit the sparse order-two and order-three bounds."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


ORDER = 43


def rotate(vertex: int, prime: int, shift: int) -> int:
    return (vertex + shift) % prime


def edge_orbits(prime: int, two_cycles: bool) -> list[list[tuple[int, int]]]:
    vertices = range(prime * (2 if two_cycles else 1))
    if two_cycles:
        pairs = {(left, right) for left in range(prime) for right in range(prime, 2 * prime)}
    else:
        pairs = {tuple(pair) for pair in itertools.combinations(vertices, 2)}
    result = []
    while pairs:
        seed = min(pairs)
        orbit = set()
        for shift in range(prime):
            left = rotate(seed[0], prime, shift)
            right = prime + rotate(seed[1] - prime, prime, shift) if two_cycles else rotate(seed[1], prime, shift)
            orbit.add(tuple(sorted((left, right))))
        pairs -= orbit
        result.append(sorted(orbit))
    return sorted(result)


def cross_options(prime: int) -> list[dict[str, object]]:
    orbits = edge_orbits(prime, two_cycles=True)
    options = []
    for colors in itertools.product((0, 1), repeat=len(orbits)):
        degrees = [0] * prime
        for orbit, color in zip(orbits, colors, strict=True):
            if not color:
                continue
            for left, right in orbit:
                if left < prime:
                    degrees[left] += 1
                if right < prime:
                    degrees[right] += 1
        if len(set(degrees)) != 1:
            raise AssertionError((prime, colors, degrees))
        options.append(
            {
                "orbit_colors": list(colors),
                "row_degree": degrees[0],
                "common_block_vertices": prime if all(colors) else 0,
            }
        )
    return options


def maximum_degree(prime: int, cycles: int, cap: int) -> int:
    fixed = ORDER - prime * cycles
    options = cross_options(prime)
    best = -1
    for blocks in itertools.product(options, repeat=cycles - 1):
        common_from_blocks = sum(int(block["common_block_vertices"]) for block in blocks)
        if common_from_blocks > cap:
            continue
        fixed_common = min(fixed, cap - common_from_blocks)
        degree = prime - 1 + fixed_common + sum(int(block["row_degree"]) for block in blocks)
        best = max(best, degree)
    return best


def build_result() -> dict[str, object]:
    cases = {}
    for prime, last_cycle, cap in ((2, 4, 13), (3, 6, 4)):
        internal = edge_orbits(prime, two_cycles=False)
        cross = edge_orbits(prime, two_cycles=True)
        if len(internal) != 1 or len(cross) != prime:
            raise AssertionError((prime, internal, cross))
        maxima = []
        for cycles in range(1, last_cycle + 1):
            maximum = maximum_degree(prime, cycles, cap)
            formula_bound = cycles + 13 if prime == 2 else 2 * cycles + 4
            if maximum != formula_bound or maximum >= 18:
                raise AssertionError((prime, cycles, maximum, formula_bound))
            maxima.append(
                {
                    "cycles": cycles,
                    "fixed_points": ORDER - prime * cycles,
                    "maximum_internal_color_degree": maximum,
                }
            )
        threshold = last_cycle + 1
        if maximum_degree(prime, threshold, cap) != 18:
            raise AssertionError("the analytic threshold should be tight")
        cases[str(prime)] = {
            "common_neighborhood_cap": cap,
            "cross_orbit_sizes": [len(orbit) for orbit in cross],
            "first_not_excluded_cycle_count": threshold,
            "internal_orbit_sizes": [len(orbit) for orbit in internal],
            "maxima": maxima,
        }
    return {
        "cases": cases,
        "color_degree_lower_bound": 18,
        "format": "r55-sparse-order2-order3-automorphism-obstruction-v1",
        "order": ORDER,
        "ramsey_inputs": {"R(3,5)": 14, "R(4,5)": 25},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    result = build_result()
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS involution_maxima=14,15,16,17 order3_maxima=6,8,10,12,14,16")


if __name__ == "__main__":
    main()
