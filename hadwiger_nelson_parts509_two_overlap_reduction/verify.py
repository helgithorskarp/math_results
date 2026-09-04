#!/usr/bin/env python3
"""Standard-library exact verifier for the Parts L/S two-overlap reduction."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
POINTS = ROOT / "hadwiger_nelson_parts509_completion_census_degree9" / "points.tsv"
VTX = ROOT / "hadwiger_nelson_parts509_criticality" / "parts509.vtx"
GRAPH_CERTIFICATE = ROOT / "hadwiger_nelson_parts509_criticality" / "certificate.json"
FORMAT = "parts509-two-overlap-reduction-v1"
POINTS_SHA256 = "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50"
SCALE = 96
BASIS = 8
PRIMES = (3, 5, 11)
L_SIZE = 374
S_SIZE = 136

Field = tuple[int, ...]
Point = tuple[Field, Field]
Edge = tuple[int, int]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def field_multiply(left: Field, right: Field) -> Field:
    result = [0] * BASIS
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if not b:
                continue
            factor = 1
            for bit, prime in enumerate(PRIMES):
                if (i & j) & (1 << bit):
                    factor *= prime
            result[i ^ j] += factor * a * b
    return tuple(result)


def field_add(left: Field, right: Field) -> Field:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def field_subtract(left: Field, right: Field) -> Field:
    return tuple(a - b for a, b in zip(left, right, strict=True))


def read_points(path: Path = POINTS) -> list[Point]:
    if sha256(path) != POINTS_SHA256:
        raise ValueError("unexpected points.tsv SHA-256")
    points = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        values = tuple(map(int, line.split()))
        if len(values) != 2 * BASIS:
            raise ValueError("point row does not contain 16 coefficients")
        points.append((values[:BASIS], values[BASIS:]))
    if len(points) != 509 or len(set(points)) != 509:
        raise ValueError("expected 509 distinct source points")
    return points


def squared_distance(left: Point, right: Point) -> Field:
    dx = field_subtract(left[0], right[0])
    dy = field_subtract(left[1], right[1])
    return field_add(field_multiply(dx, dx), field_multiply(dy, dy))


def build_edges(points: list[Point]) -> list[Edge]:
    unit = (SCALE * SCALE,) + (0,) * (BASIS - 1)
    return [
        (u, v)
        for u in range(len(points))
        for v in range(u + 1, len(points))
        if squared_distance(points[u], points[v]) == unit
    ]


def distance_histogram(points: list[Point]) -> Counter[Field]:
    return Counter(
        squared_distance(points[u], points[v])
        for u in range(len(points))
        for v in range(u + 1, len(points))
    )


def unpack_coloring(text: str) -> list[int]:
    raw = base64.b64decode(text, validate=True)
    if len(raw) != (S_SIZE + 3) // 4:
        raise ValueError("bad packed S-colouring length")
    if raw[-1] >> (2 * (S_SIZE % 4 or 4)):
        raise ValueError("nonzero packed padding")
    return [(raw[index // 4] >> (2 * (index % 4))) & 3 for index in range(S_SIZE)]


def pack_coloring(colors: list[int]) -> str:
    if len(colors) != S_SIZE or any(color not in range(4) for color in colors):
        raise ValueError("bad S-colouring")
    raw = bytearray((S_SIZE + 3) // 4)
    for index, color in enumerate(colors):
        raw[index // 4] |= color << (2 * (index % 4))
    return base64.b64encode(raw).decode("ascii")


# Coefficients of the six exceptional rotation parameters at denominator 64.
EXCEPTIONAL_ROTATIONS: tuple[tuple[Field, Field], ...] = (
    ((-32, 0, 0, 0, 0, 0, 0, 0), (0, -32, 0, 0, 0, 0, 0, 0)),
    ((-17, 0, -21, 0, 0, 0, 0, 0), (0, -17, 0, 7, 0, 0, 0, 0)),
    ((-32, 0, 0, 0, 0, 0, 0, 0), (0, 32, 0, 0, 0, 0, 0, 0)),
    ((-17, 0, 21, 0, 0, 0, 0, 0), (0, 17, 0, 7, 0, 0, 0, 0)),
    ((34, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, -14, 0, 0, 0, 0)),
    ((64, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0)),
)


def transform_scaled(point: Point, c: Field, s: Field, reflected: bool) -> Point:
    cx = field_multiply(c, point[0])
    sy = field_multiply(s, point[1])
    sx = field_multiply(s, point[0])
    cy = field_multiply(c, point[1])
    if reflected:  # F(-c,s), whose whole-plane J-reflection is R(c,s).
        return field_add(tuple(-x for x in cx), sy), field_add(sx, cy)
    return field_subtract(cx, sy), field_add(sx, cy)


def exceptional_difference_counts(L: list[Point], S: list[Point]) -> list[int]:
    scaled_L = [
        (tuple(64 * x for x in point[0]), tuple(64 * y for y in point[1]))
        for point in L
    ]
    counts = []
    for c, s in EXCEPTIONAL_ROTATIONS:
        for reflected in (False, True):
            transformed = [transform_scaled(point, c, s, reflected) for point in S]
            differences = {
                (field_subtract(p[0], q[0]), field_subtract(p[1], q[1]))
                for p in scaled_L
                for q in transformed
            }
            counts.append(len(differences))
    return counts


def verify(path: Path) -> None:
    certificate = json.loads(path.read_text(encoding="utf-8"))
    if certificate.get("format") != FORMAT:
        raise ValueError("certificate format mismatch")
    for name, source in (
        ("points.tsv", POINTS),
        ("parts509.vtx", VTX),
        ("parts509_certificate.json", GRAPH_CERTIFICATE),
    ):
        if certificate["source_sha256"].get(name) != sha256(source):
            raise ValueError(f"source hash mismatch: {name}")

    points = read_points()
    L = points[:L_SIZE]
    S = [points[0]] + points[L_SIZE:]
    s_edges = build_edges(S)
    edge_set = set(s_edges)
    if len(s_edges) != 564:
        raise ValueError("full S strict-edge count mismatch")

    witnesses = [unpack_coloring(text) for text in certificate["s_colorings"]]
    for index, colors in enumerate(witnesses):
        if any(colors[u] == colors[v] for u, v in s_edges):
            raise ValueError(f"S witness {index} is not proper")
    nonedges = [
        (u, v)
        for u in range(S_SIZE)
        for v in range(u + 1, S_SIZE)
        if (u, v) not in edge_set
    ]
    same_covered = sum(any(colors[u] == colors[v] for colors in witnesses) for u, v in nonedges)
    different_covered = sum(any(colors[u] != colors[v] for colors in witnesses) for u, v in nonedges)
    if same_covered != len(nonedges) or different_covered != len(nonedges):
        raise ValueError("the witness library does not realize both relations on every S nonedge")

    l_hist = distance_histogram(L)
    s_hist = distance_histogram(S)
    common = set(l_hist) & set(s_hist)
    matching = sum(l_hist[length] * s_hist[length] for length in common)
    difference_counts = exceptional_difference_counts(L, S)
    if any(count != L_SIZE * S_SIZE for count in difference_counts):
        raise ValueError("an exceptional orientation has a repeated cross difference")

    counts = {
        "L_vertices": len(L),
        "S_vertices_including_center": len(S),
        "total_labels": len(L) + len(S),
        "L_segments": sum(l_hist.values()),
        "S_segments": sum(s_hist.values()),
        "L_squared_distance_classes": len(l_hist),
        "S_squared_distance_classes": len(s_hist),
        "common_squared_distance_classes": len(common),
        "matching_unordered_segment_pairs": matching,
        "orientation_preserving_overlap_pair_certificates": 2 * matching,
        "orientation_reversing_overlap_pair_certificates": 2 * matching,
        "all_overlap_pair_certificates": 4 * matching,
        "S_edges": len(s_edges),
        "S_nonedges": len(nonedges),
        "S_pair_flexibility_witnesses": len(witnesses),
        "exceptional_orientations": len(difference_counts),
        "cross_differences_per_exceptional_orientation": L_SIZE * S_SIZE,
    }
    for key, value in counts.items():
        if certificate["counts"].get(key) != value:
            raise ValueError(f"count mismatch for {key}: {value}")

    print(f"matching_unordered_segment_pairs={matching}")
    print(f"all_overlap_pair_certificates={4 * matching}")
    print(f"S_nonedges_flexible_both_relations={len(nonedges)}")
    print(f"S_pair_flexibility_witnesses={len(witnesses)}")
    print(f"exceptional_orientations_cross_difference_injective={len(difference_counts)}")
    print("solver_free_all_checks=true")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path, default=Path("certificate.json"))
    args = parser.parse_args()
    verify(args.certificate)


if __name__ == "__main__":
    main()
