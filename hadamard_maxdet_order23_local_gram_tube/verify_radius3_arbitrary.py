#!/usr/bin/env python3
"""Independent exact checker for the arbitrary radius-three certificate."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

from symmetry import action_types, burnside_counts, factor_groups, full_pair_action_types
from verify import PRIMES, bareiss_determinant, gram_matrix, read_record


RECORD_DETERMINANT = 2779447296000000
LEGAL_VALUES = tuple(range(-21, 20, 4))
EXPECTED_WITNESS_COUNTS = [
    4438897, 2221693, 1112675, 555172, 276468, 138696,
    69501, 34412, 17433, 8578, 4252, 2177,
    1100, 557, 285, 118, 82, 40,
    22, 11, 5, 1, 0, 0,
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0,
]
EXPECTED_SURVIVOR_SHA256 = (
    "c3ef5ac259a06e9eeda3abb57fdd2c46bf0db3d2bc4e959577dd8b4d8e6d119a"
)


def survivor_hash(survivors: list[list[list[int]]]) -> str:
    encoded = "".join(
        ",".join(f"{edge}:{value}" for edge, value in edits) + "\n"
        for edits in survivors
    )
    return hashlib.sha256(encoded.encode("ascii")).hexdigest()


def independent_underlying_orbit_count() -> int:
    first, second, _, _ = factor_groups()
    pair_types = full_pair_action_types(action_types(first), action_types(second))
    return burnside_counts(pair_types, 3)[3]


def exact_survivor_summary(survivors: list[list[list[int]]]) -> dict[str, object]:
    gram = gram_matrix(read_record())
    edges = tuple((left, right) for left in range(23) for right in range(left))
    encodings: set[tuple[tuple[int, int], ...]] = set()
    roots: list[int] = []
    previous_key: tuple[tuple[int, ...], tuple[int, ...]] | None = None

    for edits in survivors:
        encoding = tuple((int(edge), int(value)) for edge, value in edits)
        indices = [edge for edge, _ in encoding]
        values = [value for _, value in encoding]
        assert len(encoding) == 3
        assert indices == sorted(indices) and len(set(indices)) == 3
        assert all(0 <= edge < len(edges) for edge in indices)
        assert all(value in LEGAL_VALUES for _, value in encoding)
        assert encoding not in encodings
        encodings.add(encoding)
        key = (tuple(indices), tuple(values))
        assert previous_key is None or previous_key < key
        previous_key = key

        modified = [row[:] for row in gram]
        for edge_index, value in encoding:
            left, right = edges[edge_index]
            assert value != gram[left][right]
            modified[left][right] = modified[right][left] = value
        determinant = bareiss_determinant(modified)
        assert determinant >= 0
        root = math.isqrt(determinant)
        assert root * root == determinant
        roots.append(root)

    counts = Counter(roots)
    return {
        "square_encodings_in_cover": len(roots),
        "distinct_square_roots": len(counts),
        "largest_square_root": max(roots),
        "largest_below_record": max(root for root in roots if root < RECORD_DETERMINANT),
        "record_equal_encodings": counts[RECORD_DETERMINANT],
        "record_beating_encodings": sum(
            multiplicity for root, multiplicity in counts.items()
            if root > RECORD_DETERMINANT
        ),
        "record_beating_roots": sorted(
            (root, multiplicity) for root, multiplicity in counts.items()
            if root > RECORD_DETERMINANT
        ),
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: python3 verify_radius3_arbitrary.py RADIUS3_RESULT.json"
        )
    result = json.loads(Path(sys.argv[1]).read_text())
    assert result["order"] == 23
    assert tuple(result["witness_primes"]) == PRIMES
    assert result["connected_shapes_through_three"] == 5
    assert result["colored_connected_variants_through_three"] == 9739
    assert result["internally_colored_underlying_graphs"] == 73707
    assert result["underlying_edit_set_orbits"] == independent_underlying_orbit_count() == 8887
    assert result["value_assignments_per_representative"] == 1000
    assert result["covered_labeled_matrices"] == math.comb(253, 3) * 1000
    assert result["normalized_cover_evaluations"] == 8887000
    assert result["witness_counts"] == EXPECTED_WITNESS_COUNTS
    survivors = result["survivor_edits"]
    assert len(survivors) == result["survives_48_nonsquare_tests"] == 4825
    assert sum(result["witness_counts"]) + len(survivors) == 8887000
    assert survivor_hash(survivors) == EXPECTED_SURVIVOR_SHA256

    summary = exact_survivor_summary(survivors)
    assert summary == {
        "square_encodings_in_cover": 4825,
        "distinct_square_roots": 880,
        "largest_square_root": 2740715520000000,
        "largest_below_record": 2740715520000000,
        "record_equal_encodings": 0,
        "record_beating_encodings": 0,
        "record_beating_roots": [],
    }
    print(json.dumps({"survivor_sha256": survivor_hash(survivors), **summary}, indent=2))
    print("exact arbitrary radius-three covering certificate verified")


if __name__ == "__main__":
    main()
