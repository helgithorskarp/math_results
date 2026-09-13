#!/usr/bin/env python3
"""Strip timing/search metadata from a completed L-deletion search."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PARENT = REPO / "hadwiger_nelson_parts509_pool_obstruction574"
GEOMETRY = (REPO /
    "hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("search_result", type=Path)
    parser.add_argument("output", type=Path, nargs="?",
                        default=HERE / "certificate.json")
    args = parser.parse_args()
    source = json.loads(args.search_result.read_text())
    if source["status"] != "all_L_single_deletions_four_colourable":
        raise ValueError("search did not complete every L deletion")
    rows = [{"removed": row["removed"],
             "colouring_2bit": row["colouring_2bit"]}
            for row in source["colourings"]]
    if [row["removed"] for row in rows] != list(range(374)):
        raise ValueError("L deletion rows are incomplete or unordered")
    result = {
        "schema": "parts574-L-indispensability-v1",
        "parent_graph": {
            "vertices": 574,
            "edges": 2707,
            "fixed_L_vertices": 374,
            "selected_pool_vertices": 200,
        },
        "source_pins": {
            "parent_certificate.json": digest(PARENT / "certificate.json"),
            "parent_expected.json": digest(PARENT / "expected.json"),
            "parent_proof_manifest.json": digest(PARENT / "proof_manifest.json"),
            "exact_geometry_reader.py": digest(GEOMETRY),
        },
        "L_deletion_colourings": rows,
        "discovery_search": {
            "solver": "CaDiCaL 1.9.5 through python-sat",
            "queries": len(rows),
            "native_solver_seconds": source["native_solver_seconds"],
            "wall_seconds": source["elapsed_seconds"],
            "trust_boundary": "search is untrusted; verifier checks every word",
        },
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
