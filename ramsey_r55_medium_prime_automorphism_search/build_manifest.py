#!/usr/bin/env python3
"""Build the exact manifest for the medium-prime obstruction."""

from __future__ import annotations

import argparse
import hashlib
import json
import lzma
from pathlib import Path

import pysat

from generate_formula import CASES, ORDER, build


CASE_ORDER = tuple((prime, fixed) for prime in CASES for fixed in CASES[prime])
RAT_CASE = (13, 17)
KISSAT_SHA256 = "2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45"
DRAT_TRIM_SHA256 = "9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a"


def cnf_bytes(variables: int, clauses: list[tuple[int, ...]]) -> bytes:
    lines = [f"p cnf {variables} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode("ascii")


def proof_statistics(payload: bytes) -> tuple[int, int, int]:
    if not payload.endswith(b"\n") or b"\n\n" in payload:
        raise AssertionError("malformed proof payload")
    lines = payload.decode("ascii").splitlines()
    additions = sum(not line.startswith("d ") for line in lines)
    return len(lines), additions, len(lines) - additions


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--proof-dir", type=Path, default=here / "proofs")
    parser.add_argument("--result", type=Path, default=here / "result.json")
    args = parser.parse_args()

    records = []
    for prime, fixed in CASE_ORDER:
        variables, clauses = build(prime, fixed)
        stem = f"p{prime}f{fixed}"
        if (prime, fixed) == RAT_CASE:
            path = args.proof_dir / f"{stem}.drat.xz"
            compressed = path.read_bytes()
            payload = lzma.decompress(compressed)
            lines, additions, deletions = proof_statistics(payload)
            proof_fields = {
                "proof_kind": "DRAT",
                "proof_file": str(Path("proofs") / path.name),
                "proof_compression": "xz",
                "proof_compressed_bytes": len(compressed),
                "proof_compressed_sha256": hashlib.sha256(compressed).hexdigest(),
                "proof_bytes": len(payload),
                "proof_sha256": hashlib.sha256(payload).hexdigest(),
                "proof_lines": lines,
                "proof_additions": additions,
                "proof_deletions": deletions,
                "proof_generator": "Kissat 4.0.4",
                "proof_generator_sha256": KISSAT_SHA256,
                "proof_trimmer": "drat-trim 2.2",
                "proof_trimmer_sha256": DRAT_TRIM_SHA256,
            }
        else:
            path = args.proof_dir / f"{stem}.drat"
            payload = path.read_bytes()
            lines, additions, deletions = proof_statistics(payload)
            proof_fields = {
                "proof_kind": "RUP",
                "proof_file": str(Path("proofs") / path.name),
                "proof_bytes": len(payload),
                "proof_sha256": hashlib.sha256(payload).hexdigest(),
                "proof_lines": lines,
                "proof_additions": additions,
                "proof_deletions": deletions,
                "proof_generator": "PySAT Glucose 4.2",
            }
        formula = cnf_bytes(variables, clauses)
        records.append(
            {
                "prime": prime,
                "fixed_points": fixed,
                "prime_cycles": (ORDER - fixed) // prime,
                "variables": variables,
                "clauses": len(clauses),
                "cnf_sha256": hashlib.sha256(formula).hexdigest(),
                **proof_fields,
            }
        )

    document = {
        "format": "r55-medium-prime-automorphism-obstruction-v1",
        "order": ORDER,
        "automorphism_orders": list(CASES),
        "degree_window": [18, 24],
        "single_cycle_degree_cases": [
            [prime, fixed]
            for prime, fixed in CASE_ORDER
            if (ORDER - fixed) // prime == 1
        ],
        "rup_solver": "PySAT Glucose 4.2",
        "python_sat_version": pysat.__version__,
        "rat_case": list(RAT_CASE),
        "cases": records,
    }
    args.result.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
    print(
        f"PASS wrote {len(records)} cases additions="
        f"{sum(case['proof_additions'] for case in records)} bytes="
        f"{sum(case['proof_bytes'] for case in records)}",
        flush=True,
    )


if __name__ == "__main__":
    main()
