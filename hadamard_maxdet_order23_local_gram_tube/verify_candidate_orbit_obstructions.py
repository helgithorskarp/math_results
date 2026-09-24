#!/usr/bin/env python3
"""Independent checker for the symmetry-compressed column certificate."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from candidate_obstructions import (
    CANDIDATES,
    ORDER,
    candidate_gram,
    enumerate_normalized_columns,
    gram_matrix,
    read_record,
    scaled_inverse,
)


EXPECTED_CENSUS_HASHES = (
    "f1adaf219c10cf1cc3e6ea40dc9ab858bffb0a91347902b0d583ca6f80290ad5",
    "2d83ad3b68aed06f5844335c66c1ae5c62f80b1f8b4b1c0847d7c3c42020f94a",
    "71491d5644dc929ea9759dbaeab1a9aafb7d7d818d5f0e00f51699353c528d3c",
)


def explicit_generators(
    pairs: list[list[int]], blocks: list[list[int]]
) -> list[tuple[int, ...]]:
    generators = []

    def transposition(left: int, right: int) -> tuple[int, ...]:
        answer = list(range(ORDER))
        answer[left], answer[right] = answer[right], answer[left]
        return tuple(answer)

    for left, right in pairs:
        generators.append(transposition(left, right))
    for block in blocks:
        generators.append(transposition(block[0], block[1]))
        cycle = list(range(ORDER))
        for index, source in enumerate(block):
            cycle[source] = block[(index + 1) % 4]
        generators.append(tuple(cycle))
    swap = list(range(ORDER))
    for left, right in zip(blocks[0], blocks[1]):
        swap[left], swap[right] = right, left
    generators.append(tuple(swap))
    return generators


def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    # The subgroup fixes vertex zero, so normalization v_0=1 is preserved.
    return sum(
        ((mask >> permutation[vertex]) & 1) << vertex
        for vertex in range(1, ORDER)
    )


def generator_orbit(mask: int, generators: list[tuple[int, ...]]) -> set[int]:
    orbit = {mask}
    frontier = [mask]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            image = permute_mask(current, generator)
            if image not in orbit:
                orbit.add(image)
                frontier.append(image)
    return orbit


def check_combinatorial_cover(candidate: dict, forced_singletons: int) -> None:
    fixed = len(candidate["fixed_vertices"]) - forced_singletons
    pair_count = len(candidate["interchangeable_pairs"])
    expected_representatives = (2**fixed) * (3**pair_count) * 15
    labeled = (2**fixed) * (4**pair_count) * 256
    section = (
        candidate["forbidden_v0v1_minus_one"]
        if forced_singletons
        else candidate["all_normalized_columns"]
    )
    assert section["canonical_representatives"] == expected_representatives
    assert section["represented_labeled_vectors"] == labeled


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: python3 verify_candidate_orbit_obstructions.py CERTIFICATE.json"
        )
    certificate = json.loads(Path(sys.argv[1]).read_text())
    assert certificate["order"] == ORDER
    assert certificate["normalization"] == "v_0=1"
    first, second = certificate["candidate_data"]
    assert first["candidate_index"] == 1
    assert second["candidate_index"] == 2
    assert first["edges"] == list(CANDIDATES[0]["edges"])
    assert second["edges"] == list(CANDIDATES[1]["edges"])
    assert first["inverse_scale"] == CANDIDATES[0]["inverse_scale"]
    assert second["inverse_scale"] == CANDIDATES[1]["inverse_scale"]
    assert first["fixed_vertices"] == [1, 2, 5, 6, 7, 8, 11, 12, 13, 14]
    assert second["fixed_vertices"] == [1, 2, 5, 6, 9, 10, 13, 14]
    assert first["interchangeable_pairs"] == [[3, 4], [9, 10]]
    assert second["interchangeable_pairs"] == [[3, 4], [7, 8], [11, 12]]
    assert first["interchangeable_four_blocks"] == second[
        "interchangeable_four_blocks"
    ] == [[15, 16, 17, 18], [19, 20, 21, 22]]
    assert first["symmetry_subgroup_order"] == 4608
    assert second["symmetry_subgroup_order"] == 9216
    check_combinatorial_cover(first, 0)
    check_combinatorial_cover(second, 0)
    check_combinatorial_cover(second, 1)
    assert first["all_normalized_columns"]["census_sha256"] == EXPECTED_CENSUS_HASHES[0]
    assert second["all_normalized_columns"]["census_sha256"] == EXPECTED_CENSUS_HASHES[1]
    assert second["forbidden_v0v1_minus_one"]["census_sha256"] == EXPECTED_CENSUS_HASHES[2]
    assert first["all_normalized_columns"]["solution_representatives"] == 0
    assert first["all_normalized_columns"]["solution_labeled_vectors"] == 0
    assert second["all_normalized_columns"]["solution_representatives"] == 2
    assert second["all_normalized_columns"]["solution_labeled_vectors"] == 48
    assert second["forbidden_v0v1_minus_one"]["solution_representatives"] == 0
    assert second["forbidden_v0v1_minus_one"]["solution_labeled_vectors"] == 0

    base = gram_matrix(read_record())
    brute_solution_masks: list[set[int]] = []
    for candidate in CANDIDATES:
        matrix = candidate_gram(base, candidate["edges"])
        scale, numerator = scaled_inverse(matrix)
        masks = enumerate_normalized_columns(scale, numerator)
        # The original enumeration numbers bits from x_1; the orbit certificate
        # uses actual vertex indices and therefore shifts every mask once.
        brute_solution_masks.append({mask << 1 for mask in masks})

    assert brute_solution_masks[0] == set()
    assert len(brute_solution_masks[1]) == 48
    assert all(mask & (1 << 1) == 0 for mask in brute_solution_masks[1])

    records = second["all_normalized_columns"]["solution_records"]
    generators = explicit_generators(
        second["interchangeable_pairs"], second["interchangeable_four_blocks"]
    )
    expanded: set[int] = set()
    for record in records:
        orbit = generator_orbit(record["mask"], generators)
        assert len(orbit) == record["orbit_size"]
        assert not (expanded & orbit)
        expanded.update(orbit)
    assert expanded == brute_solution_masks[1]
    assert sum(record["orbit_size"] for record in records) == 48
    assert first["all_normalized_columns"]["solution_labeled_vectors"] == 0
    assert second["forbidden_v0v1_minus_one"]["solution_labeled_vectors"] == 0

    print("candidate 1: 138,240 symmetry classes contain no admissible column")
    print("candidate 2: 51,840 forbidden-product classes contain no admissible column")
    print("two admissible candidate-2 orbits expand to exactly 48 columns")
    print("symmetry-compressed sign-column certificate verified")


if __name__ == "__main__":
    main()
