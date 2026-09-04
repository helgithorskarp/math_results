#!/usr/bin/env python3
"""Solver-free verification of every placement at a certified overlap threshold."""

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
FORMAT = "parts509-affine-overlap-threshold-v1"

sys.path.insert(0, str(GEOMETRY))
import verify as geometry  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scale(value, factor):
    return tuple(factor * coefficient for coefficient in value)


def transform(point, row):
    c, s = tuple(row["c"]), tuple(row["s"])
    cx = geometry.field_multiply(c, point[0])
    sy = geometry.field_multiply(s, point[1])
    sx = geometry.field_multiply(s, point[0])
    cy = geometry.field_multiply(c, point[1])
    if row["reflected"]:
        x, y = geometry.field_add(cx, sy), geometry.field_subtract(sx, cy)
    else:
        x, y = geometry.field_subtract(cx, sy), geometry.field_add(sx, cy)
    return (
        geometry.field_add(x, tuple(row["translation_x"])),
        geometry.field_add(y, tuple(row["translation_y"])),
    )


def unpack(text, order):
    raw = base64.b64decode(text, validate=True)
    if len(raw) != (order + 3) // 4:
        raise ValueError("bad packed-colouring length")
    if order % 4 and raw[-1] >> (2 * (order % 4)):
        raise ValueError("nonzero packed-colouring padding")
    return [(raw[index // 4] >> (2 * (index % 4))) & 3 for index in range(order)]


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

    minimum = certificate.get("minimum_overlap")
    if minimum != 50:
        raise ValueError("this certificate must close the overlap threshold 50")
    histogram = {int(key): value for key, value in certificate["overlap_multiplicity_histogram"].items()}
    if sum(histogram.values()) != 2_992_078:
        raise ValueError("full placement histogram mismatch")
    if sum(k * (k - 1) // 2 * value for k, value in histogram.items()) != 17_658_256:
        raise ValueError("determining-pair checksum mismatch")
    expected_placements = sum(value for k, value in histogram.items() if k >= minimum)
    rows = certificate["placements"]
    if expected_placements != 372 or certificate.get("placement_count") != 372 or len(rows) != 372:
        raise ValueError("threshold placement count mismatch")

    source_points = geometry.read_points(POINTS)
    L, S = source_points[:374], [source_points[0]] + source_points[374:]
    l_edges, s_edges = geometry.build_edges(L), geometry.build_edges(S)
    observed_overlap, observed_edges = Counter(), Counter()
    transformation_keys = set()
    for index, row in enumerate(rows):
        denominator = row["denominator"]
        if not isinstance(denominator, int) or denominator <= 0:
            raise ValueError("bad transformation denominator")
        c, s = tuple(row["c"]), tuple(row["s"])
        norm = geometry.field_add(geometry.field_multiply(c, c), geometry.field_multiply(s, s))
        if norm != (denominator * denominator,) + (0,) * 7:
            raise ValueError(f"placement {index} orientation is not orthogonal")
        key = (
            row["reflected"], denominator, c, s,
            tuple(row["translation_x"]), tuple(row["translation_y"]),
        )
        if key in transformation_keys:
            raise ValueError("duplicate threshold transformation")
        transformation_keys.add(key)

        labelled = (
            [(scale(x, denominator), scale(y, denominator)) for x, y in L]
            + [transform(point, row) for point in S]
        )
        union, edges = strict_graph(labelled, denominator, l_edges, s_edges)
        overlaps = 510 - len(union)
        if overlaps != row["overlaps"] or overlaps < minimum:
            raise ValueError(f"placement {index} overlap mismatch")
        if len(union) != row["union_order"] or len(edges) != row["strict_edges"]:
            raise ValueError(f"placement {index} graph census mismatch")
        colors = unpack(row["coloring"], len(union))
        if any(colors[u] == colors[v] for u, v in edges):
            raise ValueError(f"placement {index} colouring is improper")
        observed_overlap[overlaps] += 1
        observed_edges[len(edges)] += 1
        if (index + 1) % 50 == 0:
            print(f"verified={index + 1}/{len(rows)}")

    expected_overlap = Counter({k: value for k, value in histogram.items() if k >= minimum})
    if observed_overlap != expected_overlap:
        raise ValueError("observed threshold overlap histogram mismatch")
    expected_edges = Counter({int(key): value for key, value in certificate["strict_edge_histogram"].items()})
    if observed_edges != expected_edges:
        raise ValueError("observed strict-edge histogram mismatch")
    print("minimum_overlap=50")
    print("four_colorable_placements=372")
    print(f"union_order_range={min(510-k for k in observed_overlap)}..{max(510-k for k in observed_overlap)}")
    print(f"strict_edge_range={min(observed_edges)}..{max(observed_edges)}")
    print("solver_free_threshold_checks=true")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path, default=Path("overlap_atleast50_certificate.json"))
    args = parser.parse_args()
    verify(args.certificate)


if __name__ == "__main__":
    main()
