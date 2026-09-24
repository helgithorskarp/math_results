#!/usr/bin/env python3
"""Definition-level checks for the arbitrary-entry radius-four certificate."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from symmetry import action_types, burnside_counts, factor_groups, full_pair_action_types
from verify import (
    PRIMES,
    bareiss_determinant,
    expected_distance_four_relabelings,
    gram_matrix,
    read_record,
)


RECORD = 2_779_447_296_000_000
LEGAL_VALUES = tuple(range(-21, 20, 4))
EXPECTED_PARTITIONS = [
    {
        "partition": "4",
        "internally_colored_graphs": 142_566,
        "underlying_edit_set_orbits": 16_797,
    },
    {
        "partition": "3+1",
        "internally_colored_graphs": 447_294,
        "underlying_edit_set_orbits": 48_567,
    },
    {
        "partition": "2+2",
        "internally_colored_graphs": 164_757,
        "underlying_edit_set_orbits": 17_874,
    },
    {
        "partition": "2+1+1",
        "internally_colored_graphs": 806_188,
        "underlying_edit_set_orbits": 82_215,
    },
    {
        "partition": "1+1+1+1",
        "internally_colored_graphs": 325_878,
        "underlying_edit_set_orbits": 32_478,
    },
]
EXPECTED_WITNESS_COUNTS = [
    989188468, 494613332, 247269495, 123646559, 61817868, 30901254,
    15438500, 7722254, 3862664, 1923442, 964584, 486162,
    239722, 125452, 59182, 30543, 15218, 7510,
    3686, 1810, 923, 570, 186, 98,
    50, 24, 10, 19, 1, 1, 2, 1,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
]
EXPECTED_SURVIVOR_SHA256 = (
    "1bc15ff2431fb08ec0ad7faedefe8eff124e88f735a00e9a33f2e7e7cef803de"
)
EXPECTED_SQUARE_SHA256 = (
    "f65f43f0e639d55d36262c3f9e7a36ebf0cbfdcd27cfcc3fa1b34c8c40b5ab70"
)
EXPECTED_ABOVE_SHA256 = (
    "9a9c32da935a1a0d7e54e9b5bfad82eb00f0a329e17862c5b5fd2c58aa73abb4"
)


def independent_underlying_orbit_count() -> int:
    first, second, _, _ = factor_groups()
    pair_types = full_pair_action_types(action_types(first), action_types(second))
    return burnside_counts(pair_types, 4)[4]


def decode_candidate(
    item: dict, gram: list[list[int]], edges: tuple[tuple[int, int], ...]
) -> list[list[int]]:
    edits = tuple((int(edge), int(value)) for edge, value in item["edits"])
    indices = tuple(edge for edge, _ in edits)
    assert len(edits) == 4
    assert indices == tuple(sorted(indices)) and len(set(indices)) == 4
    assert all(0 <= edge < 253 for edge in indices)
    assert all(value in LEGAL_VALUES for _, value in edits)
    matrix = [row[:] for row in gram]
    for edge_index, value in edits:
        left, right = edges[edge_index]
        assert value != gram[left][right]
        matrix[left][right] = matrix[right][left] = value
    determinant = bareiss_determinant(matrix)
    root = int(item["square_root"])
    assert determinant == int(item["determinant"]) == root * root
    return matrix


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: python3 verify_radius4_arbitrary.py CERTIFICATE.json"
        )
    result = json.loads(Path(sys.argv[1]).read_text())
    gram = gram_matrix(read_record())
    edges = tuple((left, right) for left in range(23) for right in range(left))
    assert bareiss_determinant(gram) == RECORD**2

    assert result["schema"] == "radius4-arbitrary-certificate-v1"
    assert result["order"] == 23 and result["radius"] == 4
    assert result["shard_count"] == 32
    assert tuple(result["legal_values"]) == LEGAL_VALUES
    assert result["value_assignments_per_representative"] == 10_000
    assert result["covered_labeled_matrices"] == math.comb(253, 4) * 10_000
    assert result["connected_shapes_through_four"] == 10
    assert result["colored_connected_variants_through_four"] == 152_305
    assert result["partitions"] == EXPECTED_PARTITIONS
    assert result["internally_colored_underlying_graphs"] == 1_886_683
    assert (
        result["underlying_edit_set_orbits"]
        == independent_underlying_orbit_count()
        == 197_931
    )
    assert result["normalized_cover_evaluations"] == 1_979_310_000
    assert tuple(result["witness_primes"]) == PRIMES
    assert result["witness_counts"] == EXPECTED_WITNESS_COUNTS
    assert result["survives_48_nonsquare_tests"] == 990_410
    assert sum(result["witness_counts"]) + 990_410 == 1_979_310_000
    assert result["survivor_encoding_sha256"] == EXPECTED_SURVIVOR_SHA256

    assert result["exact_negative_determinants"] == 0
    assert result["exact_nonnegative_nonsquares"] == 0
    assert result["exact_squares_below_record"] == 990_408
    assert result["largest_square_root_below_record"] == 2_760_297_676_800_000
    assert result["exact_squares_equal_record"] == 1
    assert result["exact_squares_above_record"] == 1
    assert result["square_encoding_and_root_sha256"] == EXPECTED_SQUARE_SHA256
    assert result["above_record_encoding_and_root_sha256"] == EXPECTED_ABOVE_SHA256
    assert result["record_threshold"] == RECORD
    assert result["positive_definite_squares_above_record"] == 0
    assert result["positive_definite_above_record_edits"] == []

    equal = result["record_equal_square_edits"]
    assert len(equal) == 1 and int(equal[0]["square_root"]) == RECORD
    decode_candidate(equal[0], gram, edges)
    gram_edges = tuple(
        (left, right, gram[left][right])
        for left in range(23)
        for right in range(left)
    )
    equality_orbit = expected_distance_four_relabelings(gram, gram_edges)
    equal_encoding = tuple(tuple(edit) for edit in equal[0]["edits"])
    assert equal_encoding in equality_orbit

    above = result["above_record_square_edits"]
    assert len(above) == 1
    candidate = above[0]
    assert candidate["edits"] == [[23, -21], [105, 19], [110, -21], [178, -21]]
    assert candidate["square_root"] == 2_791_505_920_000_000
    assert candidate["positive_definite"] is False
    assert candidate["first_nonpositive_leading_principal_order"] == 14
    assert candidate["first_nonpositive_leading_principal_minor"] == -43_620_761_600_000
    matrix = decode_candidate(candidate, gram, edges)
    leading_minors = [
        bareiss_determinant([row[:order] for row in matrix[:order]])
        for order in range(1, 15)
    ]
    assert all(value > 0 for value in leading_minors[:13])
    assert leading_minors[13] == -43_620_761_600_000

    print(
        json.dumps(
            {
                "underlying_edit_set_orbits": 197_931,
                "normalized_cover_evaluations": 1_979_310_000,
                "exact_squares_below_record": 990_408,
                "exact_squares_equal_record": 1,
                "exact_squares_above_record": 1,
                "positive_definite_squares_above_record": 0,
                "survivor_encoding_sha256": EXPECTED_SURVIVOR_SHA256,
            },
            indent=2,
        )
    )
    print("exact arbitrary radius-four covering certificate verified")


if __name__ == "__main__":
    main()
