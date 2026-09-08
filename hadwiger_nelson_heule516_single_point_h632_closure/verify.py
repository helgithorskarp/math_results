#!/usr/bin/env python3
"""Exact witness checker for the H516 one-outside-point closure."""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
CERTIFICATE_SHA256 = "2afa90a5e96af79d0c2855db41a7d17fb8e34fee2c30bb81e3dfd9cc26da6335"
INPUT_SHA256 = {
    "hadwiger_nelson_heule632_pair_pilot/independent.py": "091b762038fae447dad5679cd6cc25009291869d641af75a7b26b5cfc0551d60",
    "hadwiger_nelson_heule632_minimize/boundary.json": "8732adbdfe9792d6b6496bfec89da64b0127c388c2bb79f892b1d35a9c396f5e",
    "hadwiger_nelson_heule632_minimize/certificate.json": "3a22660e40329c0aef34e108b91747f529adb046cf687df5b05b3531ca17e35b",
    "hadwiger_nelson_heule560_global_decision/certificate.json": "1d24fdbed29a3d17c89764fa62c599049a819a24dd9982d83b116c37df572271",
}


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_geometry():
    source = REPO / "hadwiger_nelson_heule632_pair_pilot" / "independent.py"
    specification = importlib.util.spec_from_file_location("onepoint_h632_geometry", source)
    module = importlib.util.module_from_spec(specification)
    need(specification.loader is not None, "geometry loader")
    specification.loader.exec_module(module)
    return module.geometry()


def source_supports():
    boundary = json.loads((REPO / "hadwiger_nelson_heule632_minimize" / "boundary.json").read_text())
    global_certificate = json.loads(
        (REPO / "hadwiger_nelson_heule560_global_decision" / "certificate.json").read_text()
    )
    h560_certificate = json.loads(
        (REPO / "hadwiger_nelson_heule632_minimize" / "certificate.json").read_text()
    )
    mandatory = set(boundary["mandatory_vertices"])
    optional_order = global_certificate["optional_order"]
    core_index = global_certificate["minimality_evidence_core_index"]
    core = global_certificate["negative_cores"][core_index]
    chosen = {
        vertex
        for index, vertex in enumerate(optional_order)
        if (core["mask"] >> index) & 1
    }
    base = mandatory | chosen
    h560 = set(h560_certificate["retained"])
    outside = set(range(632)) - h560
    need(len(mandatory) == 492 and len(chosen) == 24 and len(base) == 516, "H516 source support")
    need(len(h560) == 560 and base <= h560 and len(outside) == 72, "H560 and outside partition")
    return base, h560, outside


def unpack(encoded: str, length: int) -> list[int]:
    need(type(encoded) is str, "packed colouring type")
    try:
        raw = base64.b64decode(encoded, validate=True)
    except Exception as error:
        raise ValueError("packed colouring base64") from error
    need(len(raw) == (length + 3) // 4, "packed colouring byte length")
    need(base64.b64encode(raw).decode("ascii") == encoded, "noncanonical packed colouring")
    colours = [(raw[index // 4] >> (2 * (index % 4))) & 3 for index in range(length)]
    for index in range(length, 4 * len(raw)):
        need(((raw[index // 4] >> (2 * (index % 4))) & 3) == 0, "nonzero packed padding")
    return colours


def proper_colouring(
    order: list[int],
    encoded: str,
    edge_set: set[tuple[int, int]],
) -> tuple[dict[int, int], int]:
    colours = dict(zip(order, unpack(encoded, len(order))))
    checks = 0
    for left, right in edge_set:
        if left in colours and right in colours:
            need(colours[left] != colours[right], "monochromatic unit edge")
            checks += 1
    return colours, checks


def audit(certificate: dict, check_certificate_hash: bool = True) -> dict:
    if check_certificate_hash:
        need(sha256(HERE / "certificate.json") == CERTIFICATE_SHA256, "certificate identity")
    for relative, digest in INPUT_SHA256.items():
        need(sha256(REPO / relative) == digest, f"input identity: {relative}")

    points, edges, _ = exact_geometry()
    need(len(points) == 632 and len(edges) == 3112, "exact H632 geometry")
    edge_set = set(edges)
    need(len(edge_set) == len(edges), "edge uniqueness")
    base, h560, outside = source_supports()
    need(certificate["base_vertices"] == sorted(base), "base support identity")
    need(certificate["outside_points"] == sorted(outside), "outside-point family identity")
    need(certificate["target_order"] == 508, "target order")
    need(certificate["record_improvement"] is False, "record status")

    base_edges = sum(left in base and right in base for left, right in edges)
    deletion_rows = certificate["deletion_rows"]
    need(
        deletion_rows
        == sorted(deletion_rows, key=lambda row: (row["removed"], row["colours"])),
        "deletion-row order",
    )
    need(
        len({(row["removed"], row["colours"]) for row in deletion_rows}) == len(deletion_rows),
        "duplicate deletion row",
    )
    colourings_by_removed: dict[int, list[dict[int, int]]] = {vertex: [] for vertex in base}
    deletion_edge_checks = 0
    for row in deletion_rows:
        need(set(row) == {"removed", "colours"}, "deletion-row fields")
        removed = row["removed"]
        need(type(removed) is int and removed in base, "deleted base vertex")
        order = sorted(base - {removed})
        colours, checks = proper_colouring(order, row["colours"], edge_set)
        deletion_edge_checks += checks
        colourings_by_removed[removed].append(colours)
    need(all(colourings_by_removed.values()), "complete base-deletion coverage")

    coverage = {point: set() for point in outside}
    adjacency = [set() for _ in range(632)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    extension_checks = 0
    for point in outside:
        for removed, colourings in colourings_by_removed.items():
            for colours in colourings:
                used = {colours[vertex] for vertex in adjacency[point] & set(colours)}
                extension_checks += len(adjacency[point] & set(colours))
                if len(used) < 4:
                    coverage[point].add(removed)
                    break

    direct_rows = certificate["direct_rows"]
    need(
        direct_rows == sorted(direct_rows, key=lambda row: (row["point"], row["removed"])),
        "direct-row order",
    )
    need(
        len({(row["point"], row["removed"]) for row in direct_rows}) == len(direct_rows),
        "duplicate direct row",
    )
    direct_edge_checks = 0
    for row in direct_rows:
        need(set(row) == {"point", "removed", "colours"}, "direct-row fields")
        point, removed = row["point"], row["removed"]
        need(type(point) is int and point in outside, "direct outside point")
        need(type(removed) is int and removed in base, "direct removed vertex")
        order = sorted((base - {removed}) | {point})
        _, checks = proper_colouring(order, row["colours"], edge_set)
        direct_edge_checks += checks
        coverage[point].add(removed)

    counts = {point: len(coverage[point]) for point in sorted(outside)}
    need(min(counts.values()) >= 508, "one-point family not closed")
    degree_histogram = Counter(len(adjacency[point] & base) for point in outside)
    coverage_histogram = Counter(counts.values())
    need(max(degree_histogram) == 7, "outside degree range")

    return {
        "verified": True,
        "status": "ALL_H632_OUTSIDE_ONE_POINT_REPAIRS_CLOSED_THROUGH_508",
        "host_vertices": 632,
        "host_edges": len(edges),
        "H560_vertices": len(h560),
        "base_vertices": len(base),
        "base_edges": base_edges,
        "outside_points": len(outside),
        "outside_degree_to_base_histogram": {
            str(key): degree_histogram[key] for key in sorted(degree_histogram)
        },
        "deletion_colouring_rows": len(deletion_rows),
        "direct_augmented_colouring_rows": len(direct_rows),
        "base_vertices_with_deletion_colouring": sum(bool(rows) for rows in colourings_by_removed.values()),
        "minimum_covered_deletions_per_point": min(counts.values()),
        "maximum_covered_deletions_per_point": max(counts.values()),
        "coverage_histogram": {
            str(key): coverage_histogram[key] for key in sorted(coverage_histogram)
        },
        "deletion_edge_checks": deletion_edge_checks,
        "direct_edge_checks": direct_edge_checks,
        "extension_incidence_checks": extension_checks,
        "target_order": 508,
        "record_improvement": False,
        "certificate_sha256": CERTIFICATE_SHA256,
    }


def controls(certificate: dict) -> int:
    mutations = []
    changed = copy.deepcopy(certificate)
    changed["direct_rows"].pop(0)
    mutations.append(changed)
    changed = copy.deepcopy(certificate)
    changed["deletion_rows"][0]["colours"] = "not-base64!"
    mutations.append(changed)
    changed = copy.deepcopy(certificate)
    changed["outside_points"].pop()
    mutations.append(changed)
    changed = copy.deepcopy(certificate)
    changed["target_order"] = 509
    mutations.append(changed)
    rejected = 0
    for changed in mutations:
        try:
            audit(changed, check_certificate_hash=False)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("corrupted certificate accepted")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--controls", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    report = audit(certificate, check_certificate_hash=args.certificate == HERE / "certificate.json")
    if args.controls:
        report["mutations_rejected"] = controls(certificate)
    output = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.out is not None:
        args.out.mkdir(parents=True, exist_ok=False)
        (args.out / "result.json").write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
