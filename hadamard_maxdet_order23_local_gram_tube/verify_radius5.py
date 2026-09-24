#!/usr/bin/env python3
"""Definition-level checker for the radius-five symmetry quotient and sieve."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from symmetry import edge_image, factor_groups, lift_first, lift_second
from verify import PRIMES, bareiss_determinant, gram_matrix, read_record


HERE = Path(__file__).resolve().parent
RECORD_DETERMINANT = 2779447296000000


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


def exact_survivor_records(
    survivors: list[list[int]], gram: list[list[int]]
) -> list[dict]:
    edges = tuple((i, j) for i in range(23) for j in range(i))
    edge_index = {tuple(sorted(pair)): index for index, pair in enumerate(edges)}
    _, _, first_generators, second_generators = factor_groups()
    generators = [lift_first(item) for item in first_generators] + [
        lift_second(item) for item in second_generators
    ]
    survivor_sets = {frozenset(int(index) for index in item) for item in survivors}
    assert len(survivor_sets) == len(survivors) == 27
    records = []
    covered_survivors: set[frozenset[int]] = set()
    for indices in survivors:
        assert len(indices) == 5
        assert indices == sorted(indices) and len(set(indices)) == 5
        assert all(0 <= index < len(edges) for index in indices)
        edge_set = frozenset(indices)
        modified = [row[:] for row in gram]
        for index in indices:
            left, right = edges[index]
            modified[left][right] = modified[right][left] = 2 - gram[left][right]
        determinant = bareiss_determinant(modified)
        assert determinant >= 0
        root = math.isqrt(determinant)
        assert root * root == determinant
        assert root < RECORD_DETERMINANT
        orbit = generator_orbit(edge_set, generators, edges, edge_index)
        # The production generator emitted one representative per full orbit.
        assert len(orbit & survivor_sets) == 1
        covered_survivors.update(orbit & survivor_sets)
        records.append(
            {
                "square_root": root,
                "determinant": determinant,
                "orbit_size": len(orbit),
                "edge_indices": indices,
            }
        )
    assert covered_survivors == survivor_sets
    assert len({record["determinant"] for record in records}) == len(records)
    return sorted(
        records,
        key=lambda record: (-record["square_root"], record["edge_indices"]),
    )


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 verify_radius5.py RADIUS5_RESULT.json")
    result = json.loads(Path(sys.argv[1]).read_text())
    certificate = json.loads((HERE / "radius5_certificate.json").read_text())
    symmetry_certificate = json.loads(
        (HERE / "symmetry_certificate.json").read_text()
    )
    gram = gram_matrix(read_record())

    assert result["order"] == certificate["order"] == 23
    assert bareiss_determinant(gram) == RECORD_DETERMINANT**2
    assert tuple(result["witness_primes"]) == PRIMES
    for field in (
        "connected_unlabeled_shapes",
        "colored_connected_variants",
        "internally_colored_graph_counts",
        "canonical_orbit_counts",
    ):
        assert result[field] == certificate[field]
    expected_burnside = [
        symmetry_certificate["toggle_subset_orbits"][str(size)]
        for size in range(6)
    ]
    assert result["canonical_orbit_counts"] == expected_burnside

    observed = result["radius_five"]
    expected = certificate["radius_five"]
    assert observed["symmetry_classes"] == expected["symmetry_classes"]
    assert observed["witness_counts"] == expected["witness_counts"]
    assert observed["survives_48_nonsquare_tests"] == 27
    assert sum(observed["witness_counts"]) + 27 == observed["symmetry_classes"]

    records = exact_survivor_records(observed["survivor_edge_indices"], gram)
    assert records == expected["exact_square_orbits"]
    assert sum(record["orbit_size"] for record in records) == expected[
        "labeled_square_matrices"
    ]
    assert max(record["square_root"] for record in records) == expected[
        "largest_square_root"
    ]
    assert expected["largest_square_root"] < certificate["record_determinant"]
    print(
        "radius five: 4,132,509 symmetry classes, 27 square orbits, "
        "14,784 labeled square matrices, all strictly below the record"
    )
    print("exact radius-five symmetry-quotient certificate verified")


if __name__ == "__main__":
    main()
