#!/usr/bin/env python3
"""Rebuild the exact manifest for the middle order-five obstruction."""

from __future__ import annotations

import argparse
import hashlib
import json
import lzma
from pathlib import Path

from generate_formula import CASES, ORDER, build


PRIME = 5
FIXED_COUNTS = CASES[PRIME]
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

    cases = []
    for fixed in FIXED_COUNTS:
        variables, clauses = build(PRIME, fixed)
        path = args.proof_dir / f"p5f{fixed}.drat.xz"
        compressed = path.read_bytes()
        payload = lzma.decompress(compressed)
        lines, additions, deletions = proof_statistics(payload)
        formula = cnf_bytes(variables, clauses)
        cases.append(
            {
                "prime": PRIME,
                "fixed_points": fixed,
                "prime_cycles": (ORDER - fixed) // PRIME,
                "variables": variables,
                "clauses": len(clauses),
                "cnf_sha256": hashlib.sha256(formula).hexdigest(),
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
        )

    document = {
        "format": "r55-order5-middle-obstruction-v1",
        "order": ORDER,
        "automorphism_order": PRIME,
        "certified_fixed_counts": list(FIXED_COUNTS),
        "open_fixed_counts": [3, 8, 33, 38],
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
