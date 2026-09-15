#!/usr/bin/env python3
"""Independent exact checker for the frozen lens-orbit support."""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent


def fail(message: str) -> None:
    raise ValueError(message)


def norm_numerator(p: tuple[int, int], q: tuple[int, int]) -> int:
    ds, dt = p[0] - q[0], p[1] - q[1]
    return 3 * ds * ds + dt * dt


def rotation_orbit(owner: tuple[int, int], point: tuple[int, int]) -> set[tuple[int, int]]:
    answer: set[tuple[int, int]] = set()
    ds, dt = point[0] - owner[0], point[1] - owner[1]
    for _ in range(6):
        answer.add((owner[0] + ds, owner[1] + dt))
        numerators = (ds - dt, 3 * ds + dt)
        if numerators[0] % 2 or numerators[1] % 2:
            fail("nonintegral orbit coordinate")
        ds, dt = numerators[0] // 2, numerators[1] // 2
    if (ds, dt) != (point[0] - owner[0], point[1] - owner[1]):
        fail("six rotations did not close")
    return answer


def sha(lines: list[str]) -> str:
    return hashlib.sha256("".join(lines).encode("ascii")).hexdigest()


def canonical_three_patterns() -> list[str]:
    patterns = []
    for a in range(4):
        for b in range(4):
            for c in range(4):
                raw = (a, b, c)
                relabel: dict[int, int] = {}
                canonical = []
                for colour in raw:
                    if colour not in relabel:
                        relabel[colour] = len(relabel)
                    canonical.append(relabel[colour])
                word = "".join(map(str, canonical))
                if word not in patterns:
                    patterns.append(word)
    return sorted(patterns)


def check_word(word: str, order: int, edges: list[tuple[int, int]], colours: int) -> None:
    if len(word) != order or any(ch not in "0123"[:colours] for ch in word):
        fail("bad colouring alphabet or length")
    if any(word[left] == word[right] for left, right in edges):
        fail("improper colouring")


def verify_certificate(data: dict[str, object]) -> dict[str, object]:
    required = {
        "format",
        "coordinate_convention",
        "centres",
        "lenses",
        "points",
        "edges",
        "centre_indices",
        "three_colouring",
        "centre_relation_witnesses",
        "unit_triangle",
        "hashes",
    }
    if set(data) != required:
        fail("unexpected certificate keys")
    if data["format"] != "hn-three-sqrt3-lens-orbit-v1":
        fail("bad format")
    if data["coordinate_convention"] != "(s,t) means (s*sqrt(3)/2,t/2)":
        fail("bad coordinate convention")

    centres = [tuple(map(int, row)) for row in data["centres"]]
    if centres != [(0, 0), (2, 0), (1, 3)]:
        fail("unexpected centre frame")
    if any(norm_numerator(a, b) != 12 for a, b in combinations(centres, 2)):
        fail("centres are not an independent equilateral sqrt(3) triangle")

    generated = set(centres)
    expected_owner_pairs = [(0, 1), (0, 2), (1, 2)]
    lenses = data["lenses"]
    if len(lenses) != 3:
        fail("wrong lens count")
    for row, expected_owners in zip(lenses, expected_owner_pairs):
        if set(row) != {"owners", "intersections"}:
            fail("bad lens row")
        owners = tuple(map(int, row["owners"]))
        if owners != expected_owners:
            fail("bad owner pair")
        intersections = [tuple(map(int, point)) for point in row["intersections"]]
        if len(set(intersections)) != 2:
            fail("lens does not list two distinct intersections")
        for point in intersections:
            if any(norm_numerator(point, centres[owner]) != 4 for owner in owners):
                fail("false unit-circle intersection")
            for owner in owners:
                generated.update(rotation_orbit(centres[owner], point))

    points = [tuple(map(int, row)) for row in data["points"]]
    if points != sorted(set(points)) or set(points) != generated:
        fail("point set is not the exact collision-merged orbit closure")
    if len(points) != 16:
        fail("unexpected physical order")
    rebuilt_edges = [
        (i, j)
        for i, j in combinations(range(len(points)), 2)
        if norm_numerator(points[i], points[j]) == 4
    ]
    edges = [tuple(map(int, edge)) for edge in data["edges"]]
    if edges != rebuilt_edges:
        fail("edge list is not the complete strict unit graph")

    hashes = data["hashes"]
    if set(hashes) != {"points", "edges"}:
        fail("bad hash keys")
    point_hash = sha([f"{s} {t}\n" for s, t in points])
    edge_hash = sha([f"{i} {j}\n" for i, j in edges])
    if hashes != {"points": point_hash, "edges": edge_hash}:
        fail("stream hash mismatch")

    centre_indices = list(map(int, data["centre_indices"]))
    if centre_indices != [points.index(point) for point in centres]:
        fail("wrong centre indices")
    if any((a, b) in edges or (b, a) in edges for a, b in combinations(centre_indices, 2)):
        fail("centres unexpectedly adjacent")

    three_word = str(data["three_colouring"])
    check_word(three_word, len(points), edges, 3)
    if three_word != "".join(str(t % 3) for _, t in points):
        fail("three-colouring is not the declared lattice residue word")

    triangle = list(map(int, data["unit_triangle"]))
    if len(set(triangle)) != 3:
        fail("bad unit triangle")
    if any(
        tuple(sorted(pair)) not in edges for pair in combinations(triangle, 2)
    ):
        fail("lower-bound triangle is not complete")

    witnesses = data["centre_relation_witnesses"]
    patterns = canonical_three_patterns()
    if sorted(witnesses) != patterns:
        fail("centre relation does not cover every canonical bare pattern")
    for pattern in patterns:
        word = str(witnesses[pattern])
        check_word(word, len(points), edges, 4)
        if "".join(word[index] for index in centre_indices) != pattern:
            fail("relation witness has wrong centre pattern")

    degrees = [0] * len(points)
    for left, right in edges:
        degrees[left] += 1
        degrees[right] += 1
    degree_histogram = {str(d): degrees.count(d) for d in sorted(set(degrees))}
    return {
        "centre_distance_squared": "3",
        "centre_relation_canonical_patterns": patterns,
        "centre_relation_neutral": True,
        "chromatic_number": 3,
        "collisions_merged": 59,
        "complete_pair_decisions": len(points) * (len(points) - 1) // 2,
        "degree_histogram": degree_histogram,
        "edges": len(edges),
        "hashes": {"edges": edge_hash, "points": point_hash},
        "lens_intersection_routes": 12,
        "ordinary_nonfour_signal": False,
        "points": len(points),
        "proper_five_word_required": False,
        "status": "EXACT_THREE_COLOUR_STOP",
        "verified": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    data = json.loads(args.certificate.read_text(encoding="utf-8"))
    result = verify_certificate(data)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check_expected:
        expected = (HERE / "expected.json").read_text(encoding="utf-8")
        if text != expected:
            raise SystemExit("verifier output differs from expected.json")
    print(text, end="")


if __name__ == "__main__":
    main()
