#!/usr/bin/env python3
"""Solver-free verifier for S+ single-cross-edge flexibility."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PRIOR = ROOT / "hadwiger_nelson_parts509_two_overlap_reduction"
POINTS = ROOT / "hadwiger_nelson_parts509_completion_census_degree9" / "points.tsv"
POINTS_VTX = ROOT / "hadwiger_nelson_parts509_criticality" / "parts509.vtx"
FORMAT = "parts509-splus-single-cross-flexibility-v1"

sys.path.insert(0, str(PRIOR))
import verify as geometry  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unpack(text: str):
    raw = base64.b64decode(text, validate=True)
    # There are exactly 136 vertices, so the final byte has no padding.
    if len(raw) != 34:
        raise ValueError("bad packed colouring length")
    return tuple((raw[index // 4] >> (2 * (index % 4))) & 3 for index in range(136))


def missing_requirements(witnesses, edge_set):
    missing = []
    relation_cases = 0
    requirements = 0
    for q1 in range(136):
        for q2 in range(q1 + 1, 136):
            relations = (False,) if (q1, q2) in edge_set else (True, False)
            for equal in relations:
                relation_cases += 1
                subset = [colors for colors in witnesses if (colors[q1] == colors[q2]) == equal]
                if not subset:
                    raise ValueError(f"missing pair relation for {(q1, q2, equal)}")
                for q3 in range(136):
                    if q3 in (q1, q2):
                        continue
                    for endpoint in (q1, q2):
                        requirements += 1
                        if all(colors[q3] == colors[endpoint] for colors in subset):
                            missing.append((q1, q2, equal, q3, endpoint))
    return relation_cases, requirements, missing


def verify(path: Path) -> None:
    certificate = json.loads(path.read_text(encoding="utf-8"))
    if certificate.get("format") != FORMAT:
        raise ValueError("certificate format mismatch")
    sources = {
        "points.tsv": POINTS,
        "parts509.vtx": POINTS_VTX,
        "pair_flexibility_certificate.json": PRIOR / "certificate.json",
        "pair_flexibility_verify.py": PRIOR / "verify.py",
    }
    for name, source in sources.items():
        if certificate["source_sha256"].get(name) != sha256(source):
            raise ValueError(f"source hash mismatch: {name}")

    prior_certificate = json.loads((PRIOR / "certificate.json").read_text(encoding="utf-8"))
    packed = certificate["s_colorings"]
    if packed[:31] != prior_certificate["s_colorings"]:
        raise ValueError("inherited pair-flexibility witnesses changed")
    witnesses = [unpack(text) for text in packed]
    if len(witnesses) != 194 or len(set(witnesses)) != 194:
        raise ValueError("witness count or uniqueness mismatch")

    points = geometry.read_points(POINTS)
    small = [points[0]] + points[374:]
    edges = geometry.build_edges(small)
    if len(edges) != 564:
        raise ValueError("S+ strict-edge count mismatch")
    for index, colors in enumerate(witnesses):
        if (colors[0], colors[24], colors[26]) != (0, 1, 2):
            raise ValueError(f"colour-symmetry normalization mismatch at witness {index}")
        if any(colors[u] == colors[v] for u, v in edges):
            raise ValueError(f"improper colouring at witness {index}")

    edge_set = set(edges)
    initial_relation_cases, initial_requirements, initial_missing = missing_requirements(
        witnesses[:31], edge_set
    )
    relation_cases, requirements, missing = missing_requirements(witnesses, edge_set)
    if initial_relation_cases != 17_796 or relation_cases != 17_796:
        raise ValueError("pair-relation case count mismatch")
    if initial_requirements != 4_769_328 or requirements != 4_769_328:
        raise ValueError("triple requirement count mismatch")
    if len(initial_missing) != 30_174 or missing:
        raise ValueError("triple-flexibility coverage mismatch")

    expected_counts = {
        "vertices": 136,
        "strict_edges": 564,
        "inherited_pair_flexibility_witnesses": 31,
        "initial_uncovered_requirements": 30174,
        "added_witnesses": 163,
        "total_witnesses": 194,
        "pair_relation_cases": 17796,
        "triple_flexibility_requirements": 4769328,
    }
    if certificate.get("counts") != expected_counts:
        raise ValueError("certificate count summary mismatch")

    print("Splus_vertices=136 strict_edges=564")
    print("pair_relation_cases=17796")
    print("triple_flexibility_requirements=4769328")
    print("inherited_witnesses=31 initial_misses=30174")
    print("added_witnesses=163 total_witnesses=194")
    print("single_cross_edge_absorption_property=true")
    print("solver_free_certificate_checks=true")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path, default=Path("certificate.json"))
    args = parser.parse_args()
    verify(args.certificate)


if __name__ == "__main__":
    main()
