#!/usr/bin/env python3
"""Solver-free verifier for the C241 no-forced-equal-pair certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
B_PATH = HERE.parent / "hadwiger_nelson_nonmono159_214_lowden2/points214.tsv"
B_HASH = "97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f"
POINT_HASH = "70c14dfaec7875038c0f3cc1b9f84f5469143f5227fbd49377340bb46e27d908"
EDGE_HASH = "02e1fbb4c9f94cc5aca57945657706088e25560d3ca0c00217d0d17d647f55ab"
WORD_HASH = "0e88e2bf0d0c306238db2bdaee31224f89cf04c299f897f3d8b3694981fa3dd0"

GOLOMB = [
    (0, 0, 0, 0), (36, 0, 0, 0), (18, 0, 18, 0), (-18, 0, 18, 0),
    (-36, 0, 0, 0), (-18, 0, -18, 0), (18, 0, -18, 0), (6, 0, 0, 6),
    (-3, -3, 3, -3), (-3, 3, -3, -3),
]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(rows):
    return hashlib.sha256("".join(rows).encode()).hexdigest()


def unit(p, q):
    a, b, c, d = (x - y for x, y in zip(p, q))
    return a * a + 33 * b * b + 3 * c * c + 11 * d * d == 1296 and a * b + c * d == 0


def reconstruct(source_ids):
    need(hashlib.sha256(B_PATH.read_bytes()).hexdigest() == B_HASH, "B214 input hash")
    base = []
    for line in B_PATH.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        row = list(map(int, line.split()))
        need(len(row) == 16, "B214 row width")
        need(all(row[i] == 0 for i in (1, 2, 3, 4, 6, 7, 8, 10, 11, 13, 14, 15)), "B214 field support")
        base.append((3 * row[0], 3 * row[5], 3 * row[9], 3 * row[12]))
    need(len(base) == 214, "B214 order")
    left = [(a - 18, b, c, d) for a, b, c, d in base]
    right = [(-a + 18, -b, c, d) for a, b, c, d in base]
    source = []
    seen = {}
    for block in (GOLOMB, left, right):
        for p in block:
            if p not in seen:
                seen[p] = len(source)
                source.append(p)
    need(len(source) == 343, "opposed source order")
    need(source_ids == sorted(set(source_ids)), "source labels canonical and distinct")
    need(len(source_ids) == 241 and source_ids[:10] == list(range(10)), "core selection")
    points = [source[i] for i in source_ids]
    need(len(set(points)) == 241, "core collisions")
    edges = [(a, b) for a, b in combinations(range(241), 2) if unit(points[a], points[b])]
    return points, edges


def point_hash(points):
    return digest(" ".join(map(str, (a, 0, 0, b, 0, c, d, 0))) + "\n" for a, b, c, d in points)


def sign_quadratic(a, b):
    """Sign of a+b*sqrt(33), with integer a,b."""
    if b == 0:
        return (a > 0) - (a < 0)
    if a == 0:
        return (b > 0) - (b < 0)
    if a > 0 and b > 0:
        return 1
    if a < 0 and b < 0:
        return -1
    comparison = a * a - 33 * b * b
    need(comparison != 0, "unexpected rational sqrt(33)")
    magnitude = (comparison > 0) - (comparison < 0)
    return magnitude if a > 0 else -magnitude


def distance_half_class(p, q):
    a, b, c, d = (x - y for x, y in zip(p, q))
    rational = a * a + 33 * b * b + 3 * c * c + 11 * d * d - 324
    radical = 2 * (a * b + c * d)
    return sign_quadratic(rational, radical)


def check_words(words, edges):
    need(len(words) == 8 and len(set(words)) == 8, "eight distinct words")
    for word in words:
        need(isinstance(word, str) and len(word) == 241, "word length")
        need(set(word) <= set("0123"), "word alphabet")
        need(all(word[a] != word[b] for a, b in edges), "improper word")
    signatures = ["".join(word[v] for word in words) for v in range(241)]
    need(len(set(signatures)) == 241, "pair-separating signatures")
    return signatures


def golomb_three_colourable(edges):
    small = [(a, b) for a, b in edges if a < 10 and b < 10]
    need(len(small) == 18, "Golomb induced edges")
    for tail in product(range(3), repeat=7):
        word = (0, 1, 2) + tail
        if all(word[a] != word[b] for a, b in small):
            return True
    return False


def verify(certificate):
    need(certificate.get("schema") == "opposed241-equal-pair-gate-v1", "schema")
    points, edges = reconstruct(certificate["source_ids"])
    need(len(edges) == 991, "complete edge count")
    ph = point_hash(points)
    eh = digest(f"{a} {b}\n" for a, b in edges)
    wh = digest(word + "\n" for word in certificate["words"])
    need(ph == POINT_HASH and eh == EDGE_HASH and wh == WORD_HASH, "canonical stream hash")
    signatures = check_words(certificate["words"], edges)
    need(not golomb_three_colourable(edges), "embedded Golomb three-colouring")

    half = {-1: 0, 0: 0, 1: 0}
    for p, q in combinations(points, 2):
        half[distance_half_class(p, q)] += 1
    need(sum(half.values()) == 28920, "distance-half census")

    return {
        "status": "VERIFIED_NO_FORCED_EQUAL_PAIR",
        "points": len(points),
        "complete_unit_edges": len(edges),
        "all_pairs": 28920,
        "chromatic_number": 4,
        "colour_words": len(certificate["words"]),
        "distinct_vertex_signatures": len(set(signatures)),
        "pairs_distance_squared_lt_quarter": half[-1],
        "pairs_distance_squared_eq_quarter": half[0],
        "pairs_distance_squared_gt_quarter": half[1],
        "maximum_two_copy_shared_anchor_order": 481,
        "forced_equal_pairs": 0,
        "point_sha256": ph,
        "edge_sha256": eh,
        "word_stream_sha256": wh,
        "record_candidate": False,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    ap.add_argument("--check-expected", action="store_true")
    args = ap.parse_args()
    result = verify(json.loads(args.certificate.read_text()))
    if args.check_expected:
        need(result == json.loads((HERE / "EXPECTED.json").read_text()), "expected result")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
