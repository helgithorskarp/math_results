#!/usr/bin/env python3
"""Independent structural audit of the Parts-509 pair-closure certificate.

This checker deliberately uses only the Python standard library.  It does not
verify the geometry or the colouring witnesses; the two solver-free target
checkers do that.  It independently checks the decisive declared-set layer,
the certificate payload hashes and sizes, and the descriptive classification
of the 63 pairs A with |U(A)| = 2.
"""

from __future__ import annotations

import argparse
import base64
from collections import Counter, defaultdict
import hashlib
import itertools
import json
from pathlib import Path


EXPECTED_CERT_SHA256 = (
    "bba74f49405e408238394c8c1cd8a8c8fdb0a631d9d91056ece372bcb018cf40"
)
EXPECTED_EXTRA_PAIRS = {
    (43, 60): (415, 455),
    (43, 658): (415, 499),
    (96, 139): (303, 356),
    (133, 175): (298, 347),
}
N = 509
ROW_BYTES = 127


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("completion_points", type=Path)
    parser.add_argument("swaps", type=Path)
    args = parser.parse_args()

    require(
        sha256(args.certificate) == EXPECTED_CERT_SHA256,
        "pair-certificate SHA-256 mismatch",
    )
    cert = json.loads(args.certificate.read_text())
    completion = json.loads(args.completion_points.read_text())
    swaps = json.loads(args.swaps.read_text())

    nq = cert["q3_count"]
    require(nq == 1158, "unexpected Q3 size")
    require(len(completion["points"]) == nq, "completion-point count mismatch")
    require(len(cert["declared_pairs"]) == N, "declared-pair outer length mismatch")
    require(len(cert["family_sizes"]) == N, "family-size outer length mismatch")

    family_payload = base64.b64decode(cert["family_rows_base64"], validate=True)
    triple_payload = base64.b64decode(cert["triple_rows_base64"], validate=True)
    require(
        hashlib.sha256(family_payload).hexdigest() == cert["packed_rows_sha256"],
        "family payload hash mismatch",
    )
    require(
        len(family_payload) == sum(cert["family_sizes"]) * ROW_BYTES,
        "family payload length mismatch",
    )
    require(
        hashlib.sha256(triple_payload).hexdigest()
        == cert["packed_triple_rows_sha256"],
        "triple payload hash mismatch",
    )
    require(
        len(triple_payload) == len(cert["triple_witnesses"]) * ROW_BYTES,
        "triple payload length mismatch",
    )

    U: dict[tuple[int, int], set[int]] = defaultdict(set)
    declared_instances = 0
    for u, pairs in enumerate(cert["declared_pairs"]):
        normalized = []
        for pair in pairs:
            require(len(pair) == 2, f"vertex {u}: malformed pair")
            a, b = pair
            require(0 <= a < b < nq, f"vertex {u}: invalid pair {(a, b)}")
            normalized.append((a, b))
            U[(a, b)].add(u)
        require(len(normalized) == len(set(normalized)), f"vertex {u}: duplicate pair")
        declared_instances += len(normalized)

    histogram = Counter(len(vertices) for vertices in U.values())
    require(declared_instances == 12901, "declared-instance total mismatch")
    require(len(U) == 12838, "nonempty-U pair total mismatch")
    require(histogram == Counter({1: 12775, 2: 63}), "U histogram mismatch")
    require(
        cert["U_histogram"] == {str(k): v for k, v in sorted(histogram.items())},
        "stored U histogram differs from declared pairs",
    )
    require(not any(len(vertices) >= 3 for vertices in U.values()), "found |U| >= 3")

    actual_eq2 = {
        A: tuple(sorted(vertices)) for A, vertices in U.items() if len(vertices) == 2
    }
    stored_eq2 = {
        tuple(row["A"]): tuple(row["U"]) for row in cert["pairs_with_U_eq2"]
    }
    require(stored_eq2 == actual_eq2, "stored |U|=2 list differs from declared pairs")
    require(cert["pairs_with_U_ge3"] == [], "stored |U|>=3 list is nonempty")
    require(cert["triple_witnesses"] == [], "unexpected triple witnesses")
    require(cert["candidates_508"] == [], "unexpected 508-vertex candidates")

    swap_by_q = {q: u for q, u in swaps}
    require(len(swap_by_q) == len(swaps) == 11, "expected 11 distinct swap points")
    require(len(set(swap_by_q.values())) == 11, "swap vertices are not distinct")
    swap_pairs = set(itertools.combinations(sorted(swap_by_q), 2))
    require(len(swap_pairs) == 55, "unexpected swap-pair count")
    for A in swap_pairs:
        require(
            actual_eq2.get(A) == tuple(sorted(swap_by_q[q] for q in A)),
            f"swap-pair classification mismatch for {A}",
        )

    degree10 = [
        q for q, point in enumerate(completion["points"])
        if len(point["neighbors"]) == 10
    ]
    require(degree10 == [0, 1, 2, 3], "unexpected degree-10 point indices")
    all_degree10_pairs = set(itertools.combinations(degree10, 2))
    double_degree10 = all_degree10_pairs & set(actual_eq2)
    require(
        double_degree10 == {(0, 1), (0, 3), (1, 2), (2, 3)},
        "unexpected double-critical degree-10 pairs",
    )
    require(
        all(actual_eq2[A] == (350, 353) for A in double_degree10),
        "degree-10 U set mismatch",
    )
    require(
        {(0, 2), (1, 3)}.isdisjoint(U),
        "the two noncritical degree-10 pairs unexpectedly have nonempty U",
    )

    extras = {
        A: vertices
        for A, vertices in actual_eq2.items()
        if A not in swap_pairs and A not in all_degree10_pairs
    }
    require(extras == EXPECTED_EXTRA_PAIRS, "mixed-pair classification mismatch")

    swap_by_u = {u: q for q, u in swaps}
    swap_implied = 0
    for u, pairs in enumerate(cert["declared_pairs"]):
        q = swap_by_u.get(u)
        if q is not None:
            swap_implied += sum(q in pair for pair in pairs)
    require(swap_implied == 12727, "swap-implied declared count mismatch")
    require(declared_instances - swap_implied == 174, "other declared count mismatch")

    result = {
        "all_checks": True,
        "certificate_sha256": sha256(args.certificate),
        "family_rows": sum(cert["family_sizes"]),
        "declared_instances": declared_instances,
        "swap_implied_instances": swap_implied,
        "other_declared_instances": declared_instances - swap_implied,
        "pairs_with_nonempty_U": len(U),
        "U_histogram": dict(sorted(histogram.items())),
        "swap_point_pairs_with_U2": len(swap_pairs),
        "degree10_pairs_with_U2": sorted(double_degree10),
        "degree10_pairs_with_empty_U": [(0, 2), (1, 3)],
        "mixed_pairs_with_U2": [
            {"A": list(A), "U": list(vertices)}
            for A, vertices in sorted(extras.items())
        ],
        "correct_classification": "55 swap pairs + 4 degree-10 pairs + 4 mixed pairs = 63",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
