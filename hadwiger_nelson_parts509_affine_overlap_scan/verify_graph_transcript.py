#!/usr/bin/env python3
"""Verify an exact C++ graph transcript and all positive colourings in a threshold certificate."""

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
POINTS_VTX = ROOT / "hadwiger_nelson_parts509_criticality" / "parts509.vtx"
ENUMERATOR = HERE / "enumerate_overlaps.cpp"
EMITTER = HERE / "emit_graphs.cpp"
FORMAT = "parts509-affine-overlap-threshold-v1"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def field(text: str):
    result = tuple(map(int, text.split(",")))
    if len(result) != 8:
        raise ValueError("bad field encoding in overlap scan")
    return result


def transformation_key(row):
    return (
        bool(row["reflected"]),
        int(row["denominator"]),
        tuple(row["c"]),
        tuple(row["s"]),
        tuple(row["translation_x"]),
        tuple(row["translation_y"]),
    )


def read_scan(path: Path):
    transformations, histogram, scalars, flags = [], {}, {}, set()
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("high_overlap="):
            encoded = dict(item.split("=", 1) for item in line.split(";"))
            transformations.append(
                {
                    "overlaps": int(encoded["high_overlap"]),
                    "reflected": bool(int(encoded["reflected"])),
                    "denominator": int(encoded["denominator"]),
                    "c": field(encoded["c"]),
                    "s": field(encoded["s"]),
                    "translation_x": field(encoded["tx"]),
                    "translation_y": field(encoded["ty"]),
                }
            )
        elif line.startswith("overlap_multiplicity_"):
            key, value = line.split("=")
            histogram[int(key.rsplit("_", 1)[1])] = int(value)
        elif "=" in line:
            key, value = line.split("=", 1)
            if value.isdigit():
                scalars[key] = int(value)
            elif value == "true":
                flags.add(key)
    transformations.sort(key=transformation_key)
    return transformations, histogram, scalars, flags


def colors(text: str, order: int):
    raw = base64.b64decode(text, validate=True)
    if len(raw) != (order + 3) // 4:
        raise ValueError("bad packed-colouring length")
    if order % 4 and raw[-1] >> (2 * (order % 4)):
        raise ValueError("nonzero packed-colouring padding")
    return [(raw[index // 4] >> (2 * (index % 4))) & 3 for index in range(order)]


def check(certificate_path: Path, scan_path: Path, graphs_path: Path) -> None:
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    if certificate.get("format") != FORMAT:
        raise ValueError("certificate format mismatch")
    for name, source in (
        ("points.tsv", POINTS),
        ("parts509.vtx", POINTS_VTX),
        ("enumerate_overlaps.cpp", ENUMERATOR),
        ("emit_graphs.cpp", EMITTER),
    ):
        if certificate["source_sha256"].get(name) != sha256(source):
            raise ValueError(f"source hash mismatch: {name}")
    if certificate.get("graph_transcript_sha256") != sha256(graphs_path):
        raise ValueError("graph transcript hash mismatch")

    scanned, histogram, scalars, flags = read_scan(scan_path)
    minimum = certificate["minimum_overlap"]
    expected_count = sum(value for overlap, value in histogram.items() if overlap >= minimum)
    if sum(histogram.values()) != 2_992_078:
        raise ValueError("full overlap histogram checksum mismatch")
    if scalars.get("affine_placements_with_at_least_two_overlaps") != 2_992_078:
        raise ValueError("full affine-placement checksum mismatch")
    if scalars.get("recovered_pair_certificates") != 17_658_256:
        raise ValueError("determining-pair checksum mismatch")
    if scalars.get("overlap_induced_rotations") != 1_420:
        raise ValueError("rotation-orientation count mismatch")
    if scalars.get("overlap_induced_reflections") != 1_420:
        raise ValueError("reflection-orientation count mismatch")
    if scalars.get("distinct_nonzero_L_vectors") != 11_650:
        raise ValueError("L-vector count mismatch")
    if scalars.get("distinct_nonzero_S_vectors") != 1_666:
        raise ValueError("S-vector count mismatch")
    if "exact_overlap_enumeration" not in flags:
        raise ValueError("exact-enumeration trailer missing")
    if expected_count != certificate["placement_count"] or len(scanned) != expected_count:
        raise ValueError("scan threshold count mismatch")
    if len({transformation_key(row) for row in scanned}) != len(scanned):
        raise ValueError("duplicate transformation in scan")
    certified_histogram = {int(key): value for key, value in certificate["overlap_multiplicity_histogram"].items()}
    if histogram != certified_histogram:
        raise ValueError("scan and certificate overlap histograms disagree")

    rows = certificate["placements"]
    if len(rows) != len(scanned):
        raise ValueError("certificate and scan lengths disagree")
    for index, (left, right) in enumerate(zip(rows, scanned, strict=True)):
        if left["overlaps"] != right["overlaps"] or transformation_key(left) != transformation_key(right):
            raise ValueError(f"transformation mismatch at row {index}")

    edge_histogram = Counter()
    graph_count = None
    next_graph = 0
    finished = False
    with graphs_path.open(encoding="ascii") as source:
        for raw_line in source:
            line = raw_line.rstrip("\n")
            if line.startswith("graphs="):
                if graph_count is not None:
                    raise ValueError("duplicate graph transcript header")
                graph_count = int(line.split("=", 1)[1])
                continue
            if line == "exact_graph_emission=true":
                if finished:
                    raise ValueError("duplicate graph transcript trailer")
                finished = True
                continue
            if not line.startswith("graph="):
                raise ValueError("unexpected graph transcript line")
            if finished or next_graph >= len(rows):
                raise ValueError("extra graph transcript row")
            if graph_count is None:
                raise ValueError("graph row precedes transcript header")
            encoded = dict(item.split("=", 1) for item in line.split(";"))
            index = int(encoded["graph"])
            if index != next_graph:
                raise ValueError("graph rows are not contiguous")
            row = rows[index]
            order = int(encoded["order"])
            declared_edges = int(encoded["edges"])
            if int(encoded["overlaps"]) != row["overlaps"] or order != row["union_order"]:
                raise ValueError(f"graph metadata mismatch at row {index}")
            if declared_edges != row["strict_edges"]:
                raise ValueError(f"strict-edge count mismatch at row {index}")
            coloring = colors(row["coloring"], order)
            seen = set()
            edge_items = encoded["edge_list"].split(",") if encoded["edge_list"] else []
            for item in edge_items:
                u, v = map(int, item.split("-"))
                if not 0 <= u < v < order or (u, v) in seen:
                    raise ValueError(f"bad strict edge at row {index}")
                seen.add((u, v))
                if coloring[u] == coloring[v]:
                    raise ValueError(f"improper colouring at row {index}")
            if len(seen) != declared_edges:
                raise ValueError(f"edge-list length mismatch at row {index}")
            edge_histogram[declared_edges] += 1
            next_graph += 1
            if next_graph % 500 == 0:
                print(f"transcript_graphs_verified={next_graph}/{len(rows)}")
    if graph_count != len(rows) or next_graph != len(rows) or not finished:
        raise ValueError("incomplete graph transcript")
    expected_edges = Counter({int(key): value for key, value in certificate["strict_edge_histogram"].items()})
    if edge_histogram != expected_edges:
        raise ValueError("strict-edge histogram mismatch")

    orders = [row["union_order"] for row in rows]
    print(f"minimum_overlap={minimum}")
    print(f"four_colorable_placements={len(rows)}")
    print(f"union_order_range={min(orders)}..{max(orders)}")
    print(f"strict_edge_range={min(edge_histogram)}..{max(edge_histogram)}")
    print("exact_graph_transcript_and_positive_witnesses=true")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("scan", type=Path)
    parser.add_argument("graphs", type=Path)
    args = parser.parse_args()
    check(args.certificate, args.scan, args.graphs)


if __name__ == "__main__":
    main()
