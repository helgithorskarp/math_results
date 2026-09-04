#!/usr/bin/env python3
"""Solver-free verification of the maximum-overlap placement colourings."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GEOMETRY = ROOT / "hadwiger_nelson_parts509_two_overlap_reduction"
POINTS = ROOT / "hadwiger_nelson_parts509_completion_census_degree9" / "points.tsv"
POINTS_VTX = ROOT / "hadwiger_nelson_parts509_criticality" / "parts509.vtx"
ENUMERATOR = HERE / "enumerate_overlaps.cpp"
FORMAT = "parts509-affine-high-overlap-v1"

sys.path.insert(0, str(GEOMETRY))
import verify as geometry  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scale_field(value, factor):
    return tuple(factor * coefficient for coefficient in value)


def transform_numerator(point, c, s, reflected):
    cx = geometry.field_multiply(c, point[0])
    sy = geometry.field_multiply(s, point[1])
    sx = geometry.field_multiply(s, point[0])
    cy = geometry.field_multiply(c, point[1])
    if reflected:
        return geometry.field_add(cx, sy), geometry.field_subtract(sx, cy)
    return geometry.field_subtract(cx, sy), geometry.field_add(sx, cy)


def unpack_coloring(text, order):
    raw = base64.b64decode(text, validate=True)
    if len(raw) != (order + 3) // 4:
        raise ValueError("packed colouring length mismatch")
    if order % 4 and raw[-1] >> (2 * (order % 4)):
        raise ValueError("nonzero colouring padding")
    return [(raw[index // 4] >> (2 * (index % 4))) & 3 for index in range(order)]


def verify(path: Path) -> None:
    certificate = json.loads(path.read_text(encoding="utf-8"))
    if certificate.get("format") != FORMAT:
        raise ValueError("certificate format mismatch")
    for name, source in (
        ("points.tsv", POINTS),
        ("parts509.vtx", POINTS_VTX),
        ("enumerate_overlaps.cpp", ENUMERATOR),
    ):
        if certificate["source_sha256"].get(name) != sha256(source):
            raise ValueError(f"source hash mismatch: {name}")

    histogram = {int(key): value for key, value in certificate["overlap_multiplicity_histogram"].items()}
    if sum(histogram.values()) != 2_992_078:
        raise ValueError("affine-placement histogram total mismatch")
    if sum(k * (k - 1) // 2 * value for k, value in histogram.items()) != 17_658_256:
        raise ValueError("overlap-pair checksum mismatch")
    if max(histogram) != 85 or histogram[85] != 6 or histogram[84] != 6:
        raise ValueError("maximum-overlap histogram mismatch")
    if any(histogram.get(k, 0) for k in range(64, 84)):
        raise ValueError("unexpected placement with 64 through 83 overlaps")

    source_points = geometry.read_points(POINTS)
    L = source_points[:374]
    S = [source_points[0]] + source_points[374:]
    observed = Counter()
    transformation_keys = set()
    for index, row in enumerate(certificate["placements"]):
        denominator = row["denominator"]
        if not isinstance(denominator, int) or denominator <= 0:
            raise ValueError("bad orientation denominator")
        c, s = tuple(row["c"]), tuple(row["s"])
        norm = geometry.field_add(geometry.field_multiply(c, c), geometry.field_multiply(s, s))
        if norm != (denominator * denominator,) + (0,) * 7:
            raise ValueError("orientation parameter is not on the unit circle")
        key = (
            row["reflected"], denominator, c, s,
            tuple(row["translation_x"]), tuple(row["translation_y"]),
        )
        if key in transformation_keys:
            raise ValueError("duplicate certified transformation")
        transformation_keys.add(key)

        labelled = [(scale_field(x, denominator), scale_field(y, denominator)) for x, y in L]
        for point in S:
            x, y = transform_numerator(point, c, s, row["reflected"])
            labelled.append(
                (
                    geometry.field_add(x, tuple(row["translation_x"])),
                    geometry.field_add(y, tuple(row["translation_y"])),
                )
            )
        points = list(dict.fromkeys(labelled))
        overlaps = 510 - len(points)
        if overlaps != row["overlaps"] or len(points) != row["union_order"]:
            raise ValueError(f"placement {index} order mismatch")
        unit = ((96 * denominator) ** 2,) + (0,) * 7
        edges = [
            (u, v)
            for u in range(len(points))
            for v in range(u + 1, len(points))
            if geometry.squared_distance(points[u], points[v]) == unit
        ]
        if len(edges) != row["strict_edges"]:
            raise ValueError(f"placement {index} strict-edge count mismatch")
        colors = unpack_coloring(row["coloring"], len(points))
        if any(colors[u] == colors[v] for u, v in edges):
            raise ValueError(f"placement {index} colouring is improper")
        observed[(overlaps, len(points), len(edges))] += 1

    expected = Counter({(85, 425, 2185): 6, (84, 426, 2203): 6})
    if observed != expected:
        raise ValueError(f"high-placement census mismatch: {observed}")
    counts = certificate["counts"]
    expected_counts = {
        "overlap_induced_orientations": 2840,
        "affine_placements_with_at_least_two_overlaps": 2_992_078,
        "pair_certificate_checksum": 17_658_256,
        "maximum_overlap": 85,
        "maximum_overlap_placements": 6,
        "second_overlap": 84,
        "second_overlap_placements": 6,
        "placements_with_64_through_83_overlaps": 0,
        "certified_four_colorable_high_placements": 12,
    }
    if counts != expected_counts:
        raise ValueError("certificate count summary mismatch")

    print("affine_placements_with_at_least_two_overlaps=2992078")
    print("pair_certificate_checksum=17658256")
    print("maximum_overlap=85 placements=6 order=425 edges=2185 four_colorable=true")
    print("second_overlap=84 placements=6 order=426 edges=2203 four_colorable=true")
    print("placements_with_64_through_83_overlaps=0")
    print("solver_free_high_certificate_checks=true")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path, default=Path("high_overlap_certificate.json"))
    args = parser.parse_args()
    verify(args.certificate)


if __name__ == "__main__":
    main()
