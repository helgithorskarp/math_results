#!/usr/bin/env python3
"""Combine four compact proof manifests into the public result summary."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    rows = []
    shard_hashes = []
    for shard in range(4):
        path = args.directory / f"proof_manifest_shard{shard}.jsonl"
        raw = path.read_bytes()
        shard_hashes.append(sha256(raw).hexdigest())
        rows.extend(json.loads(line) for line in raw.splitlines())
    rows.sort(key=lambda row: row["orbit_index"])
    if [row["orbit_index"] for row in rows] != list(range(1348)):
        raise RuntimeError("proof manifests do not partition indices 0..1347")
    exploration = json.loads((args.directory / "orbits_complete.json").read_text())
    if len(exploration["results"]) != 1348:
        raise RuntimeError("exploratory orbit result is incomplete")
    expected_hashes = {row["orbit_index"]: row["cnf_sha256"]
                       for row in exploration["results"]}
    if any(expected_hashes[row["orbit_index"]] != row["cnf_sha256"] for row in rows):
        raise RuntimeError("proof/exploration formula identity mismatch")
    result = {
        "status": "VERIFIED_NONAFFINE_FULL_SUPPORT_RANK4_REMAINDER_EXCLUDED",
        "target43_found": False,
        "combined_with_h3757_full_support_family_excluded": True,
        "scope": {
            "row_labels": "all 15 nonzero F2^4 labels, five doubled",
            "column_labels": "all 15 nonzero F2^4 labels, eight doubled",
            "affine_column_sets_covered_by_prior_h3757": True,
            "nonaffine_pair_sets": 19279260,
            "gl4_orbits": 1348,
            "internal_edges_free": 443,
        },
        "proofs": {
            "verified_cases": len(rows),
            "statuses": sorted({row["status"] for row in rows}),
            "variables_each": sorted({row["variables"] for row in rows}),
            "clauses_min": min(row["clauses"] for row in rows),
            "clauses_max": max(row["clauses"] for row in rows),
            "clauses_total": sum(row["clauses"] for row in rows),
            "cnf_bytes_total": sum(row["cnf_bytes"] for row in rows),
            "proof_bytes_total": sum(row["proof_bytes"] for row in rows),
            "solver_seconds_total": sum(row["solver_seconds"] for row in rows),
            "checker_seconds_total": sum(row["checker_seconds"] for row in rows),
            "solver_seconds_max": max(row["solver_seconds"] for row in rows),
            "checker_seconds_max": max(row["checker_seconds"] for row in rows),
            "distinct_cnf_hashes": len({row["cnf_sha256"] for row in rows}),
            "distinct_proof_hashes": len({row["proof_sha256"] for row in rows}),
            "shard_manifest_sha256": shard_hashes,
        },
        "exploration_sha256": sha256((args.directory / "orbits_complete.json").read_bytes()).hexdigest(),
        "joint_selector_control": {
            "variables": 1098,
            "clauses": 1940044,
            "cnf_sha256": "0f82120c16744a6b57a9ba3509107c6bb485f5bdc17e693489eb0d97b0198824",
            "time_limit_seconds": 600,
            "status": "UNKNOWN_NOT_USED",
        },
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
