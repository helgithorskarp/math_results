#!/usr/bin/env python3
"""Build the manifest for the C5-square automorphism obstruction."""

from __future__ import annotations

import argparse
import hashlib
import json
import lzma
from collections import Counter
from pathlib import Path

from generate_formula import build
from verify_group_action import build_result as build_action_result


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

    variables, clauses, edge_distribution = build()
    action = build_action_result()
    compressed = args.proof.read_bytes()
    proof = lzma.decompress(compressed)
    if not proof.endswith(b"\n") or b"\n\n" in proof:
        raise AssertionError("malformed proof payload")
    lines = proof.decode("ascii").splitlines()
    additions = sum(not line.startswith("d ") for line in lines)
    document = {
        "action_classification": action,
        "clause_lengths": dict(sorted(Counter(map(len, clauses)).items())),
        "clauses": len(clauses),
        "cnf_sha256": formula_sha256(variables, clauses),
        "edge_orbit_size_distribution": edge_distribution,
        "edge_orbit_variables": variables,
        "format": "r55-c5-square-automorphism-obstruction-v1",
        "order": 43,
        "proof_additions": additions,
        "proof_bytes": len(proof),
        "proof_compressed_bytes": len(compressed),
        "proof_compressed_sha256": hashlib.sha256(compressed).hexdigest(),
        "proof_compression": "xz",
        "proof_deletions": len(lines) - additions,
        "proof_file": args.proof.name,
        "proof_generator": "Kissat 4.0.4",
        "proof_generator_sha256": KISSAT_SHA256,
        "proof_kind": "RUP in DRAT syntax",
        "proof_lines": len(lines),
        "proof_sha256": hashlib.sha256(proof).hexdigest(),
        "proof_trimmer": "drat-trim 2.2",
        "proof_trimmer_sha256": DRAT_TRIM_SHA256,
        "vertex_orbit_sizes": [1, 1, 1, 5, 5, 5, 25],
    }
    args.result.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
    print(
        f"PASS variables={variables} clauses={len(clauses)} "
        f"proof_additions={additions} proof_bytes={len(proof)}"
    )


if __name__ == "__main__":
    main()
