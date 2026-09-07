#!/usr/bin/env python3
"""Combine the orbit census and checked band proof into the public result."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path


def file_hash(path):
    digest = sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def bounded_compositions(parts, total=23, cap=5):
    counts = [0] * (total + 1)
    counts[0] = 1
    for _ in range(parts):
        updated = [0] * (total + 1)
        for subtotal, count in enumerate(counts):
            for value in range(1, cap + 1):
                if subtotal + value <= total:
                    updated[subtotal + value] += count
        counts = updated
    return counts[total]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--supports", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()

    support_data = json.loads(args.supports.read_text())
    records = support_data["records"]
    targets = [record for record in records if 5 <= record["support_size"] <= 8]
    if len(targets) != 288:
        raise RuntimeError("expected 288 support-size 5--8 orbits")
    metadata = json.loads(args.metadata.read_text())
    proof = json.loads(args.proof.read_text())
    if proof["status"] != "UNSAT_PROOF_VERIFIED":
        raise RuntimeError("proof record is not verified")
    if proof["cnf_sha256"] != metadata["formula"]["sha256"]:
        raise RuntimeError("proof and formula hashes differ")
    if metadata["variable_map"]["nonzero_support_maximum"] != 8:
        raise RuntimeError("formula does not encode support at most eight")
    if not metadata["variable_map"]["support_symmetry_break"]:
        raise RuntimeError("formula does not use the corrected dual symmetry")
    masks_by_size = {
        size: sum(record["orbit_size"] for record in records
                  if record["support_size"] == size)
        for size in range(5, 9)
    }
    compositions = {size: bounded_compositions(size) for size in range(5, 9)}
    support_sets = sum(masks_by_size.values())
    factor_multiset_pairs = 105 * sum(
        masks_by_size[size] * compositions[size] for size in range(5, 9)
    )
    proofs = {
        "proof_cases": 1,
        "statuses": [proof["status"]],
        "cnf_bytes_total": proof["cnf_bytes"],
        "proof_bytes_total": proof["proof_bytes"],
        "solver_seconds_total": proof["solver_seconds"],
        "checker_seconds_total": proof["checker_seconds"],
        "solver_seconds_max": proof["solver_seconds"],
        "checker_seconds_max": proof["checker_seconds"],
        "distinct_cnf_hashes": 1,
        "distinct_proof_hashes": 1,
    }
    result = {
        "status": "VERIFIED_RANK4_ROW_TRIPLE_SUPPORT_5_8_EXCLUDED",
        "target43_found": False,
        "scope": {
            "row_labels": "one zero, all 15 nonzero labels, labels 1 and 2 tripled",
            "row_pair_orbit_size": 105,
            "column_labels": "23 nonzero labels, spanning support size 5 through 8, each multiplicity at most 5",
            "support_orbits": len(targets),
            "support_sets": support_sets,
            "row_support_set_pairs": 105 * support_sets,
            "factor_multiset_pairs": factor_multiset_pairs,
            "bounded_compositions_by_size": {str(key): value for key, value in compositions.items()},
            "internal_edges_free": 443,
        },
        "formula": metadata["formula"],
        "proofs": proofs,
        "proof_record_sha256": file_hash(args.proof),
    }
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
