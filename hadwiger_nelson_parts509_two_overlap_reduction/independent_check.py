#!/usr/bin/env python3
"""Independent SymPy/Fraction replay of the two-overlap certificate."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CRITICALITY = ROOT / "hadwiger_nelson_parts509_criticality"
POINTS_TSV = ROOT / "hadwiger_nelson_parts509_completion_census_degree9" / "points.tsv"
POINTS_VTX = CRITICALITY / "parts509.vtx"
GRAPH_CERTIFICATE = CRITICALITY / "certificate.json"
FORMAT = "parts509-two-overlap-reduction-v1"
L_SIZE = 374
S_SIZE = 136

sys.path.insert(0, str(CRITICALITY))
import parts509 as geometry  # noqa: E402


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_scaled_tsv(path: Path):
    result = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        if len(row) != 16:
            raise ValueError("bad scaled-coordinate row")
        result.append((row[:8], row[8:]))
    return result


def scaled_coordinates(points):
    result = []
    for x, y in points:
        coordinates = []
        for coordinate in (x, y):
            scaled = tuple(value * 96 for value in coordinate)
            if any(value.denominator != 1 for value in scaled):
                raise ValueError("coordinate is not integral at scale 96")
            coordinates.append(tuple(value.numerator for value in scaled))
        result.append(tuple(coordinates))
    return result


def unpack_coloring(text: str):
    raw = base64.b64decode(text, validate=True)
    if len(raw) != 34:
        raise ValueError("bad packed S-colouring length")
    return tuple((raw[index // 4] >> (2 * (index % 4))) & 3 for index in range(S_SIZE))


def distance_histogram(points):
    return Counter(
        geometry.squared_distance(points[u], points[v])
        for u in range(len(points))
        for v in range(u + 1, len(points))
    )


def field(values):
    return tuple(Fraction(value, 64) for value in values)


ROTATIONS = (
    (field((-32, 0, 0, 0, 0, 0, 0, 0)), field((0, -32, 0, 0, 0, 0, 0, 0))),
    (field((-17, 0, -21, 0, 0, 0, 0, 0)), field((0, -17, 0, 7, 0, 0, 0, 0))),
    (field((-32, 0, 0, 0, 0, 0, 0, 0)), field((0, 32, 0, 0, 0, 0, 0, 0))),
    (field((-17, 0, 21, 0, 0, 0, 0, 0)), field((0, 17, 0, 7, 0, 0, 0, 0))),
    (field((34, 0, 0, 0, 0, 0, 0, 0)), field((0, 0, 0, -14, 0, 0, 0, 0))),
    (field((64, 0, 0, 0, 0, 0, 0, 0)), field((0, 0, 0, 0, 0, 0, 0, 0))),
)


def transform(point, c, s, reflected):
    cx = geometry.f_mul(c, point[0])
    sy = geometry.f_mul(s, point[1])
    sx = geometry.f_mul(s, point[0])
    cy = geometry.f_mul(c, point[1])
    if reflected:
        return geometry.f_add(tuple(-x for x in cx), sy), geometry.f_add(sx, cy)
    return geometry.f_sub(cx, sy), geometry.f_add(sx, cy)


def difference_counts(L, S):
    counts = []
    for c, s in ROTATIONS:
        if geometry.f_add(geometry.f_mul(c, c), geometry.f_mul(s, s)) != geometry.ONE:
            raise ValueError("listed parameter is not orthogonal")
        for reflected in (False, True):
            image = [transform(point, c, s, reflected) for point in S]
            differences = {
                (geometry.f_sub(p[0], q[0]), geometry.f_sub(p[1], q[1]))
                for p in L
                for q in image
            }
            counts.append(len(differences))
    return counts


def check(path: Path) -> None:
    certificate = json.loads(path.read_text(encoding="utf-8"))
    if certificate.get("format") != FORMAT:
        raise ValueError("certificate format mismatch")
    for name, source in (
        ("points.tsv", POINTS_TSV),
        ("parts509.vtx", POINTS_VTX),
        ("parts509_certificate.json", GRAPH_CERTIFICATE),
    ):
        if certificate["source_sha256"].get(name) != file_sha256(source):
            raise ValueError(f"source hash mismatch: {name}")

    points = geometry.parse_points(POINTS_VTX)
    if scaled_coordinates(points) != parse_scaled_tsv(POINTS_TSV):
        raise ValueError("independent coordinate sources disagree")
    graph_certificate = json.loads(GRAPH_CERTIFICATE.read_text(encoding="utf-8"))
    strict_edges = geometry.build_edges(points)
    if graph_certificate.get("coordinate_sha256") != file_sha256(POINTS_VTX):
        raise ValueError("prior certificate has a different coordinate source")
    if len(strict_edges) != graph_certificate.get("edges"):
        raise ValueError("prior strict-edge count mismatch")
    if geometry.edge_sha256(strict_edges) != graph_certificate.get("edge_sha256"):
        raise ValueError("prior strict-edge digest mismatch")

    L = points[:L_SIZE]
    S = [points[0]] + points[L_SIZE:]
    s_edges = geometry.build_edges(S)
    if len(s_edges) != 564:
        raise ValueError("independent S-edge count mismatch")
    edge_set = set(s_edges)
    nonedges = [
        (u, v)
        for u in range(S_SIZE)
        for v in range(u + 1, S_SIZE)
        if (u, v) not in edge_set
    ]
    witnesses = [unpack_coloring(text) for text in certificate["s_colorings"]]
    for index, colors in enumerate(witnesses):
        if any(colors[u] == colors[v] for u, v in s_edges):
            raise ValueError(f"independent S-colouring check failed at witness {index}")
    for u, v in nonedges:
        relations = {colors[u] == colors[v] for colors in witnesses}
        if relations != {False, True}:
            raise ValueError(f"nonedge {(u, v)} lacks both colour relations")

    l_hist = distance_histogram(L)
    s_hist = distance_histogram(S)
    common = set(l_hist) & set(s_hist)
    matching = sum(l_hist[length] * s_hist[length] for length in common)
    differences = difference_counts(L, S)
    observed = {
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
        "exceptional_orientations": len(differences),
        "cross_differences_per_exceptional_orientation": L_SIZE * S_SIZE,
    }
    for key, value in observed.items():
        if certificate["counts"].get(key) != value:
            raise ValueError(f"independent count mismatch for {key}: {value}")
    if differences != [L_SIZE * S_SIZE] * 12:
        raise ValueError("an exceptional orientation has repeated cross differences")

    print(f"independent_matching_unordered_segment_pairs={matching}")
    print(f"independent_all_overlap_pair_certificates={4 * matching}")
    print(f"independent_S_nonedges_flexible_both_relations={len(nonedges)}")
    print(f"independent_S_pair_flexibility_witnesses={len(witnesses)}")
    print(f"independent_exceptional_orientations_cross_difference_injective={len(differences)}")
    print("independent_all_checks=true")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path, default=Path("certificate.json"))
    args = parser.parse_args()
    check(args.certificate)


if __name__ == "__main__":
    main()
