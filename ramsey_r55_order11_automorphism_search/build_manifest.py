#!/usr/bin/env python3
"""Build the order-eleven manifest from deterministic formulas and proofs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pysat

from generate_formula import CASES, ORDER, PRIME, build


def cnf_bytes(variables: int, clauses: list[tuple[int, ...]]) -> bytes:
    lines = [f"p cnf {variables} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode("ascii")


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--proof-dir", type=Path, default=here / "proofs")
    parser.add_argument("--result", type=Path, default=here / "result.json")
    args = parser.parse_args()

    cases = []
    for fixed in CASES:
        variables, clauses = build(fixed)
        proof_path = args.proof_dir / f"f{fixed}.drat"
        payload = proof_path.read_bytes()
        if not payload.endswith(b"\n") or b"\n\n" in payload:
            raise AssertionError(f"malformed proof file {proof_path}")
        lines = payload.decode("ascii").splitlines()
        additions = sum(not line.startswith("d ") for line in lines)
        cases.append(
            {
                "fixed_points": fixed,
                "eleven_cycles": (ORDER - fixed) // PRIME,
                "variables": variables,
                "clauses": len(clauses),
                "cnf_sha256": hashlib.sha256(cnf_bytes(variables, clauses)).hexdigest(),
                "proof_file": str(Path("proofs") / proof_path.name),
                "proof_lines": len(lines),
                "proof_additions": additions,
                "proof_deletions": len(lines) - additions,
                "proof_bytes": len(payload),
                "proof_sha256": hashlib.sha256(payload).hexdigest(),
            }
        )

    document = {
        "format": "r55-order11-automorphism-obstruction-v1",
        "order": ORDER,
        "automorphism_order": PRIME,
        "degree_window": [18, 24],
        "single_cycle_degree_case": 32,
        "solver": "PySAT Glucose 4.2",
        "python_sat_version": pysat.__version__,
        "cases": cases,
    }
    args.result.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
    print(
        f"PASS wrote {len(cases)} cases additions="
        f"{sum(case['proof_additions'] for case in cases)} bytes="
        f"{sum(case['proof_bytes'] for case in cases)}",
        flush=True,
    )


if __name__ == "__main__":
    main()
