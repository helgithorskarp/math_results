#!/usr/bin/env python3
"""Exact checker for the translated pointwise-Galois I450 collision gate."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_overlapping_forcing_seed" / "certificate.json"
SOURCE_SHA256 = "3a487318d1d417e812791a1fd66d679151a7816fcf325a5bfd6a0351a0663237"
SIGNS = ((1, 1), (-1, 1), (1, -1), (-1, -1))
TRANSLATION = (0, 0, 0, -6)
PATH = (0, 10, 16, 1)
UNIT = (1296, 0)


def need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def add(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a + b for a, b in zip(p, q))


def embedding(p: tuple[int, ...], state: int) -> tuple[int, ...]:
    """Apply a real embedding after the fixed translation."""
    a, b, c, d = add(p, TRANSLATION)
    s3, s11 = SIGNS[state]
    return (s3 * a, s11 * b, c, s3 * s11 * d)


def squared_distance(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, int]:
    """Return rational and sqrt(33) coefficients of 1296*distance^2."""
    a, b, c, d = (x - y for x, y in zip(p, q))
    return (3 * a * a + 11 * b * b + c * c + 33 * d * d,
            2 * (a * b + c * d))


def reconstruct_source() -> tuple[list[tuple[int, ...]], list[int]]:
    raw = SOURCE.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "source hash mismatch")
    source = json.loads(raw)["unequal"]
    need(source["denominator"] == 1, "unexpected source denominator")
    points = [tuple(row) for row in source["points"]]
    word = source["colouring"]
    need((len(points), len(set(points))) == (450, 450), "source order/collision mismatch")
    need(points[:2] == [(0, 0, 0, 0), (0, 0, 0, 12)], "marked endpoints changed")
    need(len(word) == 450 and all(type(c) is int and 0 <= c < 4 for c in word),
         "bad source colour word")
    return points, word


def audit(translation: tuple[int, ...] = TRANSLATION,
          path: tuple[int, ...] = PATH) -> dict[str, object]:
    need(translation == TRANSLATION, "wrong translated frame")
    need(path == PATH, "wrong path")
    points, word = reconstruct_source()
    edges = [(u, v) for u, v in itertools.combinations(range(450), 2)
             if squared_distance(points[u], points[v]) == UNIT]
    need(len(edges) == 2290, "complete source edge count changed")
    need(all(word[u] != word[v] for u, v in edges), "source four-colour word failed")
    need(word[0] != word[1], "source word does not separate marked endpoints")
    edge_set = set(edges)
    path_edges = list(zip(path, path[1:]))
    need(all(tuple(sorted(e)) in edge_set for e in path_edges), "path is not a unit path")

    images = [[embedding(p, state) for state in range(4)] for p in points]
    collision_pairs = [(a, b) for a in range(4) for b in range(4)
                       if images[0][a] == images[1][b]]
    need(collision_pairs == [(0, 1), (0, 2), (1, 0), (1, 3),
                             (2, 0), (2, 3), (3, 1), (3, 2)],
         "endpoint collision classification changed")

    transitions = []
    for u, v in path_edges:
        allowed = [(a, b) for a in range(4) for b in range(4)
                   if squared_distance(images[u][a], images[v][b]) == UNIT]
        transitions.append(allowed)
    expected_outer = [(0, 0), (0, 3), (1, 1), (1, 2),
                      (2, 1), (2, 2), (3, 0), (3, 3)]
    expected_middle = [(0, 0), (1, 1), (2, 2), (3, 3)]
    need(transitions == [expected_outer, expected_middle, expected_outer],
         "path transition relation changed")

    preserving = []
    identifying = []
    for states in itertools.product(range(4), repeat=4):
        ok = all(squared_distance(images[u][a], images[v][b]) == UNIT
                 for (u, v), (a, b) in zip(path_edges, zip(states, states[1:])))
        if ok:
            preserving.append(states)
            if images[path[0]][states[0]] == images[path[-1]][states[-1]]:
                identifying.append(states)
    need(len(preserving) == 16, "edge-preserving path count changed")
    need(not identifying, "endpoint-identifying path map found")

    allowed_histogram: dict[int, int] = {}
    for u, v in edges:
        count = sum(squared_distance(images[u][a], images[v][b]) == UNIT
                    for a in range(4) for b in range(4))
        allowed_histogram[count] = allowed_histogram.get(count, 0) + 1
    need(allowed_histogram == {4: 1860, 8: 385, 16: 45},
         "full edge transition census changed")
    return {
        "status": "EXACT_I450_TRANSLATED_POINTWISE_GALOIS_COLLISION_FAILURE",
        "source_points": 450,
        "source_complete_unit_edges": len(edges),
        "complete_source_pair_checks": 450 * 449 // 2,
        "translation_row": list(TRANSLATION),
        "embedding_signs": [list(s) for s in SIGNS],
        "path": list(path),
        "path_state_assignments": 4 ** 4,
        "edge_preserving_path_assignments": len(preserving),
        "endpoint_collision_state_pairs": len(collision_pairs),
        "endpoint_identifying_path_assignments": len(identifying),
        "full_edge_allowed_state_pair_histogram": {
            str(k): v for k, v in sorted(allowed_histogram.items())
        },
        "declared_image_budget_if_realizable": 449,
        "map_exists": False,
        "new_physical_support": False,
        "record_candidate": False,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-expected", action="store_true")
    ap.add_argument("--controls", action="store_true")
    args = ap.parse_args()
    result = audit()
    if args.check_expected:
        need(result == json.loads((HERE / "EXPECTED.json").read_text()),
             "expected output mismatch")
    if args.controls:
        rejected = 0
        for translation, path in (((0, 0, 0, 0), PATH),
                                  (TRANSLATION, (0, 10, 15, 1))):
            try:
                audit(translation, path)
            except ValueError:
                rejected += 1
            else:
                raise ValueError("malformed control accepted")
        need(rejected == 2, "control count changed")
        result = dict(result)
        result["malformed_controls_rejected"] = rejected
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
