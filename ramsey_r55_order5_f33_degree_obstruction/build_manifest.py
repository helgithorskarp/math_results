#!/usr/bin/env python3
"""Rebuild the compact manifest for the order-five f=33 obstruction."""

from __future__ import annotations

import argparse
import hashlib
import json
import lzma
from pathlib import Path

from generate_formula import build


KISSAT_SHA256 = "2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45"
DRAT_TRIM_SHA256 = "9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a"


def formula_sha256(variables: int, clauses: list[tuple[int, ...]]) -> str:
    digest = hashlib.sha256()
    digest.update(f"p cnf {variables} {len(clauses)}\n".encode("ascii"))
    for clause in clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode("ascii"))
    return digest.hexdigest()


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--proof", type=Path, default=here / "proof.drat.xz")
    parser.add_argument("--result", type=Path, default=here / "result.json")
    args = parser.parse_args()

    variables, clauses, base_clauses = build()
    compressed = args.proof.read_bytes()
    payload = lzma.decompress(compressed)
    if not payload.endswith(b"\n") or b"\n\n" in payload:
        raise AssertionError("malformed proof payload")
    lines = payload.decode("ascii").splitlines()
    additions = sum(not line.startswith("d ") for line in lines)
    document = {
        "format": "r55-order5-f33-degree-obstruction-v1",
        "order": 43,
        "automorphism_order": 5,
        "fixed_points": 33,
        "prime_cycles": 2,
        "edge_orbit_variables": 603,
        "variables": variables,
        "base_clauses": base_clauses,
        "degree_networks": 35,
        "comparators_per_network": 861,
        "degree_clauses": len(clauses) - base_clauses,
        "clauses": len(clauses),
        "cnf_sha256": formula_sha256(variables, clauses),
        "proof_kind": "DRAT",
        "proof_file": args.proof.name,
        "proof_compression": "xz",
        "proof_compressed_bytes": len(compressed),
        "proof_compressed_sha256": hashlib.sha256(compressed).hexdigest(),
        "proof_bytes": len(payload),
        "proof_sha256": hashlib.sha256(payload).hexdigest(),
        "proof_lines": len(lines),
        "proof_additions": additions,
        "proof_deletions": len(lines) - additions,
        "proof_generator": "Kissat 4.0.4",
        "proof_generator_sha256": KISSAT_SHA256,
        "proof_trimmer": "drat-trim 2.2",
        "proof_trimmer_sha256": DRAT_TRIM_SHA256,
    }
    args.result.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
    print(
        f"PASS variables={variables} clauses={len(clauses)} "
        f"additions={additions} proof_bytes={len(payload)}",
        flush=True,
    )


if __name__ == "__main__":
    main()
