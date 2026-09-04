#!/usr/bin/env python3
"""Generate positive colourings for every emitted overlap placement."""

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
FORMAT = "parts509-affine-overlap-threshold-v1"

sys.path.insert(0, str(GEOMETRY))
import verify as geometry  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_field(text: str):
    result = tuple(map(int, text.split(",")))
    if len(result) != 8:
        raise ValueError("expected eight field coefficients")
    return result


def parse_scan(path: Path):
    histogram, entries, scalars = {}, [], {}
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("overlap_multiplicity_"):
            key, value = line.split("=")
            histogram[key.rsplit("_", 1)[1]] = int(value)
        elif line.startswith("high_overlap="):
            row = dict(item.split("=", 1) for item in line.split(";"))
            entries.append(
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
                scalars[key] = int(value)
    entries.sort(
        key=lambda row: (
            row["reflected"], row["denominator"], row["c"], row["s"],
            row["translation_x"], row["translation_y"],
        )
    )
    return histogram, entries, scalars


def scale(value, factor):
    return tuple(factor * coefficient for coefficient in value)


def transform(point, row):
    c, s = row["c"], row["s"]
    cx = geometry.field_multiply(c, point[0])
    sy = geometry.field_multiply(s, point[1])
    sx = geometry.field_multiply(s, point[0])
    cy = geometry.field_multiply(c, point[1])
    if row["reflected"]:
        x, y = geometry.field_add(cx, sy), geometry.field_subtract(sx, cy)
    else:
        x, y = geometry.field_subtract(cx, sy), geometry.field_add(sx, cy)
    return (
        geometry.field_add(x, row["translation_x"]),
        geometry.field_add(y, row["translation_y"]),
    )


def placed_labels(L, S, row):
    denominator = row["denominator"]
    return (
        [(scale(x, denominator), scale(y, denominator)) for x, y in L]
        + [transform(point, row) for point in S]
    )


def strict_graph(labelled, denominator, l_edges, s_edges):
    unique = list(dict.fromkeys(labelled))
    point_index = {point: index for index, point in enumerate(unique)}
    label_index = [point_index[point] for point in labelled]
    edges = {
        tuple(sorted((label_index[u], label_index[v])))
        for u, v in l_edges
    }
    edges.update(
        tuple(sorted((label_index[374 + u], label_index[374 + v])))
        for u, v in s_edges
    )
    unit = ((96 * denominator) ** 2,) + (0,) * 7
    for p in range(374):
        for q in range(136):
            right = 374 + q
            if geometry.squared_distance(labelled[p], labelled[right]) == unit:
                edge = tuple(sorted((label_index[p], label_index[right])))
                if edge[0] != edge[1]:
                    edges.add(edge)
    return unique, sorted(edges)


def solve(n, edges):
    clauses = [[4 * vertex + color + 1 for color in range(4)] for vertex in range(n)]
    clauses.extend(
        [-4 * u - color - 1, -4 * v - color - 1]
        for u, v in edges
        for color in range(4)
    )
    with Solver(name="cadical195", bootstrap_with=clauses) as solver:
        if not solver.solve():
            raise RuntimeError("an emitted placement is not four-colourable")
        positive = {literal for literal in solver.get_model() if literal > 0}
    colors = [
        next(color for color in range(4) if 4 * vertex + color + 1 in positive)
        for vertex in range(n)
    ]
    if any(colors[u] == colors[v] for u, v in edges):
        raise RuntimeError("decoded colouring is improper")
    raw = bytearray((n + 3) // 4)
    for index, color in enumerate(colors):
        raw[index // 4] |= color << (2 * (index % 4))
    return base64.b64encode(raw).decode("ascii")


def generate(scan: Path, minimum: int, output: Path) -> None:
    histogram, entries, scalars = parse_scan(scan)
    expected = sum(value for key, value in histogram.items() if int(key) >= minimum)
    if len(entries) != expected:
        raise ValueError(f"scan emitted {len(entries)} placements; histogram requires {expected}")
    if any(row["overlaps"] < minimum for row in entries):
        raise ValueError("scan contains a placement below the requested threshold")
    if scalars.get("affine_placements_with_at_least_two_overlaps") != 2_992_078:
        raise ValueError("bad full-placement checksum")
    if scalars.get("recovered_pair_certificates") != 17_658_256:
        raise ValueError("bad determining-pair checksum")

    points = geometry.read_points(POINTS)
    L, S = points[:374], [points[0]] + points[374:]
    l_edges, s_edges = geometry.build_edges(L), geometry.build_edges(S)
    strict_edge_histogram = {}
    for index, row in enumerate(entries):
        labelled = placed_labels(L, S, row)
        union, edges = strict_graph(labelled, row["denominator"], l_edges, s_edges)
        if len(union) != 510 - row["overlaps"]:
            raise RuntimeError("overlap count mismatch")
        row["union_order"] = len(union)
        row["strict_edges"] = len(edges)
        row["coloring"] = solve(len(union), edges)
        strict_edge_histogram[str(len(edges))] = strict_edge_histogram.get(str(len(edges)), 0) + 1
        if (index + 1) % 25 == 0:
            print(f"colored={index + 1}/{len(entries)}", flush=True)

    certificate = {
        "format": FORMAT,
        "source_sha256": {
            "points.tsv": sha256(POINTS),
            "parts509.vtx": sha256(POINTS_VTX),
            "enumerate_overlaps.cpp": sha256(ENUMERATOR),
        },
        "minimum_overlap": minimum,
        "placement_count": len(entries),
        "overlap_multiplicity_histogram": histogram,
        "strict_edge_histogram": strict_edge_histogram,
        "placements": entries,
    }
    output.write_text(json.dumps(certificate, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"minimum_overlap={minimum}")
    print(f"four_colorable_placements={len(entries)}")
    print("strict_edge_histogram=" + json.dumps(strict_edge_histogram, sort_keys=True, separators=(",", ":")))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scan", type=Path)
    parser.add_argument("minimum", type=int)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    generate(args.scan, args.minimum, args.output)


if __name__ == "__main__":
    main()
