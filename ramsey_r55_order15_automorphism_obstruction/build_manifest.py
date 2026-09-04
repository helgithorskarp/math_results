#!/usr/bin/env python3
"""Build the compact manifest for all six order-15 cases."""

from __future__ import annotations

import argparse
import hashlib
import json
import lzma
from collections import Counter
from pathlib import Path

from generate_formula import CASES, build, case_label
from verify_cycle_types import build_result as build_type_result


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
    parser.add_argument("--result", type=Path, default=here / "result.json")
    args = parser.parse_args()

    records = []
    for case in CASES:
        label = case_label(case)
        variables, clauses, distribution = build(case)
        proof_path = here / f"proof_{label}.drat.xz"
        compressed = proof_path.read_bytes()
        proof = lzma.decompress(compressed)
        if not proof.endswith(b"\n") or b"\n\n" in proof:
            raise AssertionError((case, "malformed proof"))
        lines = proof.decode("ascii").splitlines()
        additions = sum(not line.startswith("d ") for line in lines)
        records.append(
            {
                "clause_lengths": dict(sorted(Counter(map(len, clauses)).items())),
                "clauses": len(clauses),
                "cnf_sha256": formula_sha256(variables, clauses),
                "cycle_counts_15_5_3_1": list(case),
                "edge_orbit_size_distribution": distribution,
                "edge_orbit_variables": variables,
                "proof_additions": additions,
                "proof_bytes": len(proof),
                "proof_compressed_bytes": len(compressed),
                "proof_compressed_sha256": hashlib.sha256(compressed).hexdigest(),
                "proof_deletions": len(lines) - additions,
                "proof_file": proof_path.name,
                "proof_lines": len(lines),
                "proof_sha256": hashlib.sha256(proof).hexdigest(),
            }
        )

    document = {
        "cases": records,
        "format": "r55-order15-automorphism-obstruction-v1",
        "order": 43,
        "power_filter": build_type_result(),
        "proof_generator": "Kissat 4.0.4",
        "proof_generator_sha256": KISSAT_SHA256,
        "proof_kind": "DRAT",
        "proof_total_bytes": sum(record["proof_bytes"] for record in records),
        "proof_total_compressed_bytes": sum(
            record["proof_compressed_bytes"] for record in records
        ),
        "proof_trimmer": "drat-trim 2.2",
        "proof_trimmer_sha256": DRAT_TRIM_SHA256,
    }
    args.result.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
    print(
        f"PASS cases={len(records)} proof_bytes={document['proof_total_bytes']} "
        f"compressed_bytes={document['proof_total_compressed_bytes']}"
    )


if __name__ == "__main__":
    main()
