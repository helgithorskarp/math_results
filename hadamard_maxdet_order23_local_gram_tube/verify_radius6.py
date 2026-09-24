#!/usr/bin/env python3
"""Independent exact checker for the radius-six quotient certificate."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

from symmetry import (
    action_types,
    burnside_counts,
    edge_image,
    factor_groups,
    full_pair_action_types,
    lift_first,
    lift_second,
)
from verify import PRIMES, bareiss_determinant, gram_matrix, read_record


RECORD_DETERMINANT = 2779447296000000
EXPECTED_WITNESS_COUNTS = [
    40543321, 20275304, 10136653, 5068257, 2534288, 1267587,
    635409, 315794, 158803, 79487, 39455, 19665,
    9999, 4998, 2558, 1159, 642, 330,
    167, 87, 51, 15, 9, 1,
    1, 2, 1, 0, 0, 0,
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0,
]
EXPECTED_ORBIT_SIZE_CENSUS = {
    1: 1, 2: 1, 8: 3, 12: 1, 16: 2, 24: 21, 48: 43, 72: 1,
    96: 80, 128: 3, 144: 1, 192: 38, 288: 2, 384: 28,
    576: 5, 768: 28, 1152: 11, 1536: 30, 1728: 2, 2304: 15,
    3072: 12, 3456: 1, 4608: 14, 6144: 1, 6912: 3, 9216: 10,
    18432: 1, 27648: 1,
}
EXPECTED_RECORD_BEATING = [
    (2823605452800000, (10, 22, 38, 47, 89, 92), 96),
    (2783182848000000, (2, 11, 36, 38, 46, 78), 48),
]


def generator_orbit(
    seed: frozenset[int],
    generators: list[tuple[int, ...]],
    edges: tuple[tuple[int, int], ...],
    edge_index: dict[tuple[int, int], int],
) -> set[frozenset[int]]:
    orbit = {seed}
    frontier = [seed]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            image = edge_image(current, generator, edges, edge_index)
            if image not in orbit:
                orbit.add(image)
                frontier.append(image)
    return orbit


def survivor_hash(survivors: list[list[int]]) -> str:
    encoded = "".join(",".join(map(str, item)) + "\n" for item in survivors)
    return hashlib.sha256(encoded.encode("ascii")).hexdigest()


def exact_survivor_summary(survivors: list[list[int]]) -> dict:
    gram = gram_matrix(read_record())
    edges = tuple((left, right) for left in range(23) for right in range(left))
    edge_index = {tuple(sorted(pair)): index for index, pair in enumerate(edges)}
    first, second, first_generators, second_generators = factor_groups()
    assert len(first) * len(second) == 442368
    generators = [lift_first(item) for item in first_generators] + [
        lift_second(item) for item in second_generators
    ]
    survivor_sets = {frozenset(item) for item in survivors}
    assert len(survivor_sets) == len(survivors) == 359

    roots: list[int] = []
    orbit_sizes: list[int] = []
    beating: list[tuple[int, tuple[int, ...], int]] = []
    covered: set[frozenset[int]] = set()
    for indices in survivors:
        assert len(indices) == 6
        assert indices == sorted(indices) and len(set(indices)) == 6
        assert all(0 <= index < len(edges) for index in indices)
        modified = [row[:] for row in gram]
        for index in indices:
            left, right = edges[index]
            modified[left][right] = modified[right][left] = 2 - gram[left][right]
        determinant = bareiss_determinant(modified)
        assert determinant > 0
        root = math.isqrt(determinant)
        assert root * root == determinant

        seed = frozenset(indices)
        orbit = generator_orbit(seed, generators, edges, edge_index)
        hits = orbit & survivor_sets
        assert hits == {seed}
        covered.update(hits)
        roots.append(root)
        orbit_sizes.append(len(orbit))
        if root > RECORD_DETERMINANT:
            beating.append((root, tuple(indices), len(orbit)))

    assert covered == survivor_sets
    return {
        "square_orbits": len(roots),
        "distinct_square_roots": len(set(roots)),
        "labeled_square_matrices": sum(orbit_sizes),
        "largest_square_root": max(roots),
        "largest_below_record": max(
            root for root in roots if root < RECORD_DETERMINANT
        ),
        "record_equal_orbits": sum(root == RECORD_DETERMINANT for root in roots),
        "orbit_size_census": dict(sorted(Counter(orbit_sizes).items())),
        "record_beating": sorted(beating, reverse=True),
    }


def independent_burnside_count() -> int:
    first, second, _, _ = factor_groups()
    pair_types = full_pair_action_types(action_types(first), action_types(second))
    return burnside_counts(pair_types, 6)[6]


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 verify_radius6.py RADIUS6_RESULT.json")
    result = json.loads(Path(sys.argv[1]).read_text())
    assert result["order"] == 23
    assert tuple(result["witness_primes"]) == PRIMES
    assert result["stored_connected_shapes_through_five"] == 22
    assert result["stored_colored_connected_variants_through_five"] == 2593788
    assert result["connected_six_edge_shapes"] == 30
    assert result["connected_six_edge_shapes_by_vertex_count"] == [
        0, 0, 0, 0, 1, 5, 13, 11
    ]

    radius = result["radius_six"]
    assert radius["internally_colored_graphs"] == 888540494
    assert radius["connected_internally_colored_graphs"] == 43702833
    assert radius["connected_symmetry_classes"] == 4361518
    assert radius["disconnected_internally_colored_graphs"] == 844837661
    assert radius["disconnected_symmetry_classes"] == 76732884
    assert radius["symmetry_classes"] == independent_burnside_count() == 81094402
    assert radius["witness_counts"] == EXPECTED_WITNESS_COUNTS
    assert radius["survives_48_nonsquare_tests"] == 359
    assert sum(radius["witness_counts"]) + 359 == radius["symmetry_classes"]
    survivors = radius["survivor_edge_indices"]
    assert survivor_hash(survivors) == (
        "9ffb0bde7035259ed3a22302816dc570dddf36c02967fc9efcaa16f872901bf7"
    )

    summary = exact_survivor_summary(survivors)
    assert summary["square_orbits"] == 359
    assert summary["distinct_square_roots"] == 298
    assert summary["labeled_square_matrices"] == 420647
    assert summary["largest_square_root"] == 2823605452800000
    assert summary["largest_below_record"] == 2771425689600000
    assert summary["record_equal_orbits"] == 0
    assert summary["orbit_size_census"] == EXPECTED_ORBIT_SIZE_CENSUS
    assert summary["record_beating"] == EXPECTED_RECORD_BEATING

    print(
        "radius six: 81,094,402 symmetry classes, 359 square orbits, "
        "420,647 labeled square matrices"
    )
    print("exactly two square Gram orbits exceed the published record")
    print("exact radius-six symmetry-quotient certificate verified")


if __name__ == "__main__":
    main()
