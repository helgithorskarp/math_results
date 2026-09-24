#!/usr/bin/env python3
"""Generate exact sign-column obstructions for radius-seven candidates.

For a sign factorization ``G=R R^T``, every column ``v`` of ``R`` satisfies
``v^T G^{-1} v=1``.  This script first finds every radius-seven square Gram
whose determinant beats the record, exhausts all ``2^22`` normalized sign
vectors for each, and then searches for a compact contradiction among the
admissible columns.
"""

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
from verify import bareiss_determinant, gram_matrix, read_record


ORDER = 23
RECORD_DETERMINANT = 2_779_447_296_000_000


def mask_hash(masks: list[int]) -> str:
    encoded = "".join(f"{mask}\n" for mask in masks).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def find_obstruction(
    matrix: list[list[int]], masks: list[int]
) -> dict[str, object]:
    if not masks:
        return {"type": "no_admissible_column"}
    vectors = [vector_from_mask(mask) for mask in masks]
    for left in range(ORDER):
        for right in range(left):
            products = {vector[left] * vector[right] for vector in vectors}
            if len(products) != 1:
                continue
            forced = products.pop()
            if ORDER * forced != matrix[left][right]:
                return {
                    "type": "forced_pair_product",
                    "rows_zero_based": [right, left],
                    "forced_product_per_column": forced,
                    "forced_sum_over_23_columns": ORDER * forced,
                    "target_gram_entry": matrix[left][right],
                }

    # The expression is 4 when three signs agree and 0 otherwise.  A constant
    # value on all admissible columns yields a direct summed Gram contradiction.
    for first in range(ORDER):
        for second in range(first + 1, ORDER):
            for third in range(second + 1, ORDER):
                values = {
                    1
                    + vector[first] * vector[second]
                    + vector[first] * vector[third]
                    + vector[second] * vector[third]
                    for vector in vectors
                }
                if len(values) != 1:
                    continue
                forced = values.pop()
                target = (
                    ORDER
                    + matrix[first][second]
                    + matrix[first][third]
                    + matrix[second][third]
                )
                if ORDER * forced != target:
                    return {
                        "type": "forced_three_row_expression",
                        "rows_zero_based": [first, second, third],
                        "expression": "1+v_a*v_b+v_a*v_c+v_b*v_c",
                        "forced_value_per_column": forced,
                        "forced_sum_over_23_columns": ORDER * forced,
                        "target_gram_sum": target,
                    }
    raise AssertionError("record-beating candidate needs a stronger obstruction")


def analyze_candidate(item: tuple[tuple[int, ...], int]) -> dict[str, object]:
    edges, determinant_root = item
    base = gram_matrix(read_record())
    matrix = candidate_gram(base, edges)
    assert bareiss_determinant(matrix) == determinant_root**2
    leading_minors = [
        bareiss_determinant([row[:size] for row in matrix[:size]])
        for size in range(1, ORDER + 1)
    ]
    assert all(value > 0 for value in leading_minors)
    scale, numerator = scaled_inverse(matrix)
    masks = enumerate_normalized_columns(scale, numerator)
    return {
        "edge_indices": list(edges),
        "determinant_root": determinant_root,
        "positive_definite_by_sylvester": True,
        "inverse_scale": scale,
        "normalized_column_count": len(masks),
        "normalized_columns_sha256": mask_hash(masks),
        "obstruction": find_obstruction(matrix, masks),
    }


def main() -> None:
    if len(sys.argv) not in (3, 4):
        raise SystemExit(
            "usage: python3 radius7_candidate_obstructions.py "
            "RADIUS7_CERTIFICATE.json OUTPUT.json [WORKERS]"
        )
    radius_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    workers = int(sys.argv[3]) if len(sys.argv) == 4 else min(8, os.cpu_count() or 1)
    assert workers >= 1

    radius = json.loads(radius_path.read_text())
    assert radius["order"] == ORDER and radius["radius"] == 7
    base = gram_matrix(read_record())
    candidates: list[tuple[tuple[int, ...], int]] = []
    for edge_indices in radius["survivor_edge_indices"]:
        edges = tuple(edge_indices)
        determinant = bareiss_determinant(candidate_gram(base, edges))
        root = math.isqrt(determinant)
        assert root * root == determinant
        if root > RECORD_DETERMINANT:
            candidates.append((edges, root))
    candidates.sort(key=lambda item: (-item[1], item[0]))
    assert len(candidates) == 26

    if workers == 1:
        results = [analyze_candidate(item) for item in candidates]
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(analyze_candidate, candidates))
    result = {
        "schema": "radius7-candidate-obstructions-v1",
        "order": ORDER,
        "radius": 7,
        "record_determinant_root": RECORD_DETERMINANT,
        "record_beating_candidate_count": len(results),
        "normalization": "v_0=1; column negation leaves v*v^T unchanged",
        "necessary_column_equation": "v^T G^{-1} v = 1",
        "candidates": results,
    }
    output_path.write_text(json.dumps(result, indent=2) + "\n")
    print(
        f"{len(results)} record-beating candidates; every exact sign-column "
        "enumeration has a certified obstruction"
    )


if __name__ == "__main__":
    main()
