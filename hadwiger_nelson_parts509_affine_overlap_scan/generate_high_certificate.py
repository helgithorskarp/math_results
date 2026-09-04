#!/usr/bin/env python3
"""Build positive four-colouring certificates for the maximum-overlap placements."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
from pathlib import Path

from pysat.solvers import Solver


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


def parse_field(text: str) -> tuple[int, ...]:
    result = tuple(map(int, text.split(",")))
    if len(result) != 8:
        raise ValueError("expected eight field coefficients")
    return result


def parse_scan(path: Path):
    histogram = {}
    transformations = []
    counts = {}
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("overlap_multiplicity_"):
            key, value = line.split("=")
            histogram[key.rsplit("_", 1)[1]] = int(value)
        elif line.startswith("high_overlap="):
            row = dict(item.split("=", 1) for item in line.split(";"))
            transformations.append(
                {
                    "overlaps": int(row["high_overlap"]),
                    "reflected": bool(int(row["reflected"])),
                    "denominator": int(row["denominator"]),
                    "c": parse_field(row["c"]),
                    "s": parse_field(row["s"]),
                    "translation_x": parse_field(row["tx"]),
                    "translation_y": parse_field(row["ty"]),
                }
            )
        elif "=" in line:
            key, value = line.split("=", 1)
            if value.isdigit():
                counts[key] = int(value)
    transformations.sort(
        key=lambda row: (
            row["reflected"],
            row["denominator"],
            row["c"],
            row["s"],
            row["translation_x"],
            row["translation_y"],
        )
    )
    return histogram, transformations, counts


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


def placed_points(L, S, row):
    denominator = row["denominator"]
    result = [(scale_field(x, denominator), scale_field(y, denominator)) for x, y in L]
    for point in S:
        x, y = transform_numerator(point, row["c"], row["s"], row["reflected"])
        result.append(
            (
                geometry.field_add(x, row["translation_x"]),
                geometry.field_add(y, row["translation_y"]),
            )
        )
    return result


def strict_graph(labelled_points, denominator):
    points = list(dict.fromkeys(labelled_points))
    unit = ((96 * denominator) ** 2,) + (0,) * 7
    edges = [
        (u, v)
        for u in range(len(points))
        for v in range(u + 1, len(points))
        if geometry.squared_distance(points[u], points[v]) == unit
    ]
    return points, edges


def coloring_clauses(n, edges):
    clauses = [[4 * vertex + color + 1 for color in range(4)] for vertex in range(n)]
    clauses.extend(
        [-4 * u - color - 1, -4 * v - color - 1]
        for u, v in edges
        for color in range(4)
    )
    return clauses


def solve_coloring(n, edges):
    with Solver(name="cadical195", bootstrap_with=coloring_clauses(n, edges)) as solver:
        if not solver.solve():
            raise RuntimeError("a high-overlap placement is unexpectedly non-four-colourable")
        positive = {literal for literal in solver.get_model() if literal > 0}
    colors = [
        next(color for color in range(4) if 4 * vertex + color + 1 in positive)
        for vertex in range(n)
    ]
    if any(colors[u] == colors[v] for u, v in edges):
        raise RuntimeError("decoded colouring is improper")
    return colors


def pack_coloring(colors):
    raw = bytearray((len(colors) + 3) // 4)
    for index, color in enumerate(colors):
        raw[index // 4] |= color << (2 * (index % 4))
    return base64.b64encode(raw).decode("ascii")


def generate(scan: Path, output: Path) -> None:
    histogram, transformations, scan_counts = parse_scan(scan)
    if scan_counts.get("affine_placements_with_at_least_two_overlaps") != 2_992_078:
        raise ValueError("scan has an unexpected placement count")
    if scan_counts.get("recovered_pair_certificates") != 17_658_256:
        raise ValueError("scan has an unexpected pair checksum")
    if len(transformations) != 12:
        raise ValueError("expected twelve transformations with at least 84 overlaps")

    source_points = geometry.read_points(POINTS)
    L = source_points[:374]
    S = [source_points[0]] + source_points[374:]
    entries = []
    for row in transformations:
        labelled = placed_points(L, S, row)
        points, edges = strict_graph(labelled, row["denominator"])
        overlaps = 510 - len(points)
        if overlaps != row["overlaps"]:
            raise RuntimeError("reported and reconstructed overlap counts disagree")
        colors = solve_coloring(len(points), edges)
        entries.append(
            {
                **row,
                "union_order": len(points),
                "strict_edges": len(edges),
                "coloring": pack_coloring(colors),
            }
        )

    certificate = {
        "format": FORMAT,
        "source_sha256": {
            "points.tsv": sha256(POINTS),
            "parts509.vtx": sha256(POINTS_VTX),
            "enumerate_overlaps.cpp": sha256(ENUMERATOR),
        },
        "counts": {
            "overlap_induced_orientations": 2840,
            "affine_placements_with_at_least_two_overlaps": 2_992_078,
            "pair_certificate_checksum": 17_658_256,
            "maximum_overlap": 85,
            "maximum_overlap_placements": 6,
            "second_overlap": 84,
            "second_overlap_placements": 6,
            "placements_with_64_through_83_overlaps": 0,
            "certified_four_colorable_high_placements": len(entries),
        },
        "overlap_multiplicity_histogram": histogram,
        "placements": entries,
    }
    output.write_text(json.dumps(certificate, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps(certificate["counts"], indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scan", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    generate(args.scan, args.output)


if __name__ == "__main__":
    main()
