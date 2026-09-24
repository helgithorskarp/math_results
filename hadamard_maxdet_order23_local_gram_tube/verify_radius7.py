#!/usr/bin/env python3
"""Independent exact checker for the radius-seven quotient certificates."""

from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from candidate_obstructions import (
    candidate_gram,
    enumerate_normalized_columns,
    scaled_inverse,
    vector_from_mask,
)
from symmetry import (
    action_types,
    burnside_counts,
    factor_groups,
    full_pair_action_types,
)
from verify import PRIMES, bareiss_determinant, gram_matrix, read_record


ORDER = 23
RECORD_DETERMINANT = 2_779_447_296_000_000
EXPECTED_ORBITS = 1_503_560_419
EXPECTED_SURVIVOR_HASH = (
    "33d26b9cad04217d60bd68206b850232347c8be676fbf07b2a47eab53a291b74"
)
EXPECTED_WITNESS_COUNTS = [
    751774770, 375890912, 187963672, 93960756, 46981671, 23489403,
    11748639, 5871903, 2937879, 1469917, 734639, 367068, 183012,
    91885, 45804, 22809, 11510, 5503, 2913, 1363, 748, 368, 162, 92,
    40, 13, 20, 2, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0,
]
EXPECTED_STORED_PARTITIONS = [
    ("5+2", 885_913_256, 80_430_640),
    ("5+1+1", 1_915_911_633, 169_413_271),
    ("4+3", 666_669_474, 60_513_048),
    ("4+2+1", 2_094_287_928, 184_570_637),
    ("4+1+1+1", 1_457_459_102, 126_354_465),
    ("3+3+1", 882_510_528, 77_822_243),
    ("3+2+2", 646_565_925, 56_962_972),
    ("3+2+1+1", 2_652_210_720, 229_165_803),
    ("3+1+1+1+1", 887_788_952, 76_026_179),
    ("2+2+2+1", 642_233_464, 55_421_853),
    ("2+2+1+1+1", 1_266_347_745, 108_037_470),
    ("2+1+1+1+1+1", 486_787_396, 41_366_078),
    ("1+1+1+1+1+1+1", 43_197_799, 3_682_573),
]


def survivor_hash(survivors: list[list[int]]) -> str:
    encoded = "".join(
        ",".join(map(str, item)) + "\n" for item in survivors
    ).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def mask_hash(masks: list[int]) -> str:
    encoded = "".join(f"{mask}\n" for mask in masks).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def independent_burnside_count() -> int:
    first, second, _, _ = factor_groups()
    pair_types = full_pair_action_types(action_types(first), action_types(second))
    return burnside_counts(pair_types, 7)[7]


def exact_survivor_summary(survivors: list[list[int]]) -> tuple[dict, list]:
    base = gram_matrix(read_record())
    roots: list[int] = []
    beating: list[tuple[tuple[int, ...], int]] = []
    for indices in survivors:
        assert len(indices) == 7
        assert indices == sorted(indices) and len(set(indices)) == 7
        assert all(0 <= index < 253 for index in indices)
        matrix = candidate_gram(base, tuple(indices))
        determinant = bareiss_determinant(matrix)
        assert determinant > 0
        root = math.isqrt(determinant)
        assert root * root == determinant
        roots.append(root)
        if root > RECORD_DETERMINANT:
            beating.append((tuple(indices), root))
    beating.sort(key=lambda item: (-item[1], item[0]))
    return (
        {
            "square_orbits": len(roots),
            "distinct_square_roots": len(set(roots)),
            "largest_square_root": max(roots),
            "largest_below_record": max(
                root for root in roots if root < RECORD_DETERMINANT
            ),
            "record_equal_orbits": sum(
                root == RECORD_DETERMINANT for root in roots
            ),
            "record_beating_orbits": len(beating),
        },
        beating,
    )


def verify_candidate(entry: dict) -> bool:
    base = gram_matrix(read_record())
    edges = tuple(entry["edge_indices"])
    matrix = candidate_gram(base, edges)
    root = entry["determinant_root"]
    assert bareiss_determinant(matrix) == root**2
    assert root > RECORD_DETERMINANT
    assert all(
        bareiss_determinant([row[:size] for row in matrix[:size]]) > 0
        for size in range(1, ORDER + 1)
    )
    assert entry["positive_definite_by_sylvester"] is True

    scale, numerator = scaled_inverse(matrix)
    assert scale == entry["inverse_scale"]
    masks = enumerate_normalized_columns(scale, numerator)
    assert len(masks) == entry["normalized_column_count"]
    assert mask_hash(masks) == entry["normalized_columns_sha256"]
    vectors = [vector_from_mask(mask) for mask in masks]
    obstruction = entry["obstruction"]
    kind = obstruction["type"]
    if kind == "no_admissible_column":
        assert not vectors
    elif kind == "forced_pair_product":
        right, left = obstruction["rows_zero_based"]
        forced = obstruction["forced_product_per_column"]
        assert vectors
        assert all(vector[left] * vector[right] == forced for vector in vectors)
        assert obstruction["forced_sum_over_23_columns"] == ORDER * forced
        assert obstruction["target_gram_entry"] == matrix[left][right]
        assert ORDER * forced != matrix[left][right]
    elif kind == "forced_three_row_expression":
        first, second, third = obstruction["rows_zero_based"]
        forced = obstruction["forced_value_per_column"]
        assert vectors
        assert all(
            1
            + vector[first] * vector[second]
            + vector[first] * vector[third]
            + vector[second] * vector[third]
            == forced
            for vector in vectors
        )
        target = (
            ORDER
            + matrix[first][second]
            + matrix[first][third]
            + matrix[second][third]
        )
        assert obstruction["forced_sum_over_23_columns"] == ORDER * forced
        assert obstruction["target_gram_sum"] == target
        assert ORDER * forced != target
    else:
        raise AssertionError(f"unknown obstruction type: {kind}")
    return True


def main() -> None:
    if len(sys.argv) not in (3, 4):
        raise SystemExit(
            "usage: python3 verify_radius7.py RADIUS7.json "
            "OBSTRUCTIONS.json [WORKERS]"
        )
    workers = int(sys.argv[3]) if len(sys.argv) == 4 else min(8, os.cpu_count() or 1)
    assert workers >= 1
    result = json.loads(Path(sys.argv[1]).read_text())
    obstruction_result = json.loads(Path(sys.argv[2]).read_text())

    assert result["schema"] == "radius7-certificate-v1"
    assert result["order"] == ORDER and result["radius"] == 7
    assert tuple(result["witness_primes"]) == PRIMES
    assert result["stored_connected_shapes_through_five"] == 22
    assert result["stored_colored_connected_variants_through_five"] == 2_593_788
    assert result["connected_six_edge_shapes"] == 30
    assert result["connected_seven_edge_shapes"] == 79
    assert result["radius_six_connected_regression"] == 4_361_518
    assert result["connected"] == {
        "canonical_count_vectors": 65_064,
        "assignment_leaves": 321_458_435,
        "symmetry_classes": 75_778_019,
    }
    assert result["six_plus_one"] == {
        "canonical_count_vectors": 37_616,
        "assignment_leaves": 1_225_628_975,
        "symmetry_classes": 158_015_168,
    }
    assert [
        (
            item["partition"],
            item["internally_colored_graphs"],
            item["symmetry_classes"],
        )
        for item in result["stored_partitions"]
    ] == EXPECTED_STORED_PARTITIONS
    assert result["stored_partition_internally_colored_graphs"] == 14_527_883_922
    assert result["stored_partition_symmetry_classes"] == 1_269_767_232
    assert result["symmetry_classes"] == independent_burnside_count()
    assert result["symmetry_classes"] == EXPECTED_ORBITS
    assert result["witness_counts"] == EXPECTED_WITNESS_COUNTS
    assert result["survives_48_nonsquare_tests"] == 2_943
    assert sum(result["witness_counts"]) + 2_943 == EXPECTED_ORBITS
    survivors = result["survivor_edge_indices"]
    assert survivor_hash(survivors) == EXPECTED_SURVIVOR_HASH

    summary, beating = exact_survivor_summary(survivors)
    assert summary == {
        "square_orbits": 2_943,
        "distinct_square_roots": 2_436,
        "largest_square_root": 2_838_233_088_000_000,
        "largest_below_record": 2_777_874_432_000_000,
        "record_equal_orbits": 0,
        "record_beating_orbits": 26,
    }

    assert obstruction_result["schema"] == "radius7-candidate-obstructions-v1"
    assert obstruction_result["order"] == ORDER
    assert obstruction_result["radius"] == 7
    assert obstruction_result["record_determinant_root"] == RECORD_DETERMINANT
    assert obstruction_result["record_beating_candidate_count"] == 26
    entries = obstruction_result["candidates"]
    assert [
        (tuple(entry["edge_indices"]), entry["determinant_root"])
        for entry in entries
    ] == beating
    if workers == 1:
        checks = [verify_candidate(entry) for entry in entries]
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            checks = list(pool.map(verify_candidate, entries))
    assert all(checks)

    kinds = [entry["obstruction"]["type"] for entry in entries]
    assert kinds.count("no_admissible_column") == 11
    assert kinds.count("forced_pair_product") == 14
    assert kinds.count("forced_three_row_expression") == 1
    print(
        "radius seven: 1,503,560,419 symmetry classes and 2,943 exact "
        "square Gram orbits"
    )
    print("all 26 record-beating square Gram orbits are indecomposable")
    print("exact radius-seven symmetry-quotient certificate verified")


if __name__ == "__main__":
    main()
