#!/usr/bin/env python3
"""Independent SymPy/Fraction replay of all twelve high-overlap placements."""

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
ENUMERATOR = HERE / "enumerate_overlaps.cpp"
FORMAT = "parts509-affine-high-overlap-v1"

sys.path.insert(0, str(CRITICALITY))
import parts509 as geometry  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def field(values, denominator=1):
    if len(values) != 8:
        raise ValueError("expected eight field coefficients")
    return tuple(Fraction(value, denominator) for value in values)


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
    for point in points:
        coordinates = []
        for coordinate in point:
            scaled = tuple(value * 96 for value in coordinate)
            if any(value.denominator != 1 for value in scaled):
                raise ValueError("coordinate is not integral at scale 96")
            coordinates.append(tuple(value.numerator for value in scaled))
        result.append(tuple(coordinates))
    return result


def transform(point, c, s, reflected):
    cx = geometry.f_mul(c, point[0])
    sy = geometry.f_mul(s, point[1])
    sx = geometry.f_mul(s, point[0])
    cy = geometry.f_mul(c, point[1])
    if reflected:
        return geometry.f_add(cx, sy), geometry.f_sub(sx, cy)
    return geometry.f_sub(cx, sy), geometry.f_add(sx, cy)


def unpack(text, order):
    raw = base64.b64decode(text, validate=True)
    if len(raw) != (order + 3) // 4:
        raise ValueError("bad packed-colouring length")
    if order % 4 and raw[-1] >> (2 * (order % 4)):
        raise ValueError("nonzero packed-colouring padding")
    return [(raw[index // 4] >> (2 * (index % 4))) & 3 for index in range(order)]


def check(path: Path) -> None:
    certificate = json.loads(path.read_text(encoding="utf-8"))
    if certificate.get("format") != FORMAT:
        raise ValueError("certificate format mismatch")
    for name, source in (
        ("points.tsv", POINTS_TSV),
        ("parts509.vtx", POINTS_VTX),
        ("enumerate_overlaps.cpp", ENUMERATOR),
    ):
        if certificate["source_sha256"].get(name) != sha256(source):
            raise ValueError(f"source hash mismatch: {name}")

    histogram = {int(key): value for key, value in certificate["overlap_multiplicity_histogram"].items()}
    if sum(histogram.values()) != 2_992_078:
        raise ValueError("histogram total mismatch")
    if sum(k * (k - 1) // 2 * value for k, value in histogram.items()) != 17_658_256:
        raise ValueError("pair checksum mismatch")
    if max(histogram) != 85 or histogram.get(85) != 6 or histogram.get(84) != 6:
        raise ValueError("maximum-overlap histogram mismatch")

    points = geometry.parse_points(POINTS_VTX)
    if scaled_coordinates(points) != parse_scaled_tsv(POINTS_TSV):
        raise ValueError("independent coordinate sources disagree")
    L = points[:374]
    S = [points[0]] + points[374:]
    observed = Counter()
    for index, row in enumerate(certificate["placements"]):
        denominator = row["denominator"]
        c, s = field(row["c"], denominator), field(row["s"], denominator)
        if geometry.f_add(geometry.f_mul(c, c), geometry.f_mul(s, s)) != geometry.ONE:
            raise ValueError(f"placement {index} has a nonorthogonal matrix")
        tx = field(row["translation_x"], 96 * denominator)
        ty = field(row["translation_y"], 96 * denominator)
        labelled = list(L)
        for point in S:
            x, y = transform(point, c, s, row["reflected"])
            labelled.append((geometry.f_add(x, tx), geometry.f_add(y, ty)))
        union = list(dict.fromkeys(labelled))
        overlaps = 510 - len(union)
        if overlaps != row["overlaps"] or len(union) != row["union_order"]:
            raise ValueError(f"placement {index} order mismatch")
        edges = geometry.build_edges(union)
        if len(edges) != row["strict_edges"]:
            raise ValueError(f"placement {index} edge count mismatch")
        colors = unpack(row["coloring"], len(union))
        if any(colors[u] == colors[v] for u, v in edges):
            raise ValueError(f"placement {index} colouring is improper")
        observed[(overlaps, len(union), len(edges))] += 1

    if observed != Counter({(85, 425, 2185): 6, (84, 426, 2203): 6}):
        raise ValueError("independent high-placement census mismatch")
    print("independent_maximum_overlap=85 placements=6 order=425 edges=2185 four_colorable=true")
    print("independent_second_overlap=84 placements=6 order=426 edges=2203 four_colorable=true")
    print("independent_placements_with_64_through_83_overlaps=0")
    print("independent_high_certificate_checks=true")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path, default=Path("high_overlap_certificate.json"))
    args = parser.parse_args()
    check(args.certificate)


if __name__ == "__main__":
    main()
