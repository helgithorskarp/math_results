#!/usr/bin/env python3
"""Produce the ten CaDiCaL proof traces and check their exact hashes."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess


EXPECTED_PATH = Path(__file__).with_name("EXPECTED.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def solve(cadical: Path, case_dir: Path, seconds: int, index: int) -> dict:
    stem = f"s4-orbit-{index:02d}"
    cnf = case_dir / f"{stem}.cnf"
    proof = case_dir / f"{stem}.drat"
    result = subprocess.run(
        [str(cadical), "-q", "-t", str(seconds), str(cnf), str(proof)],
        text=True,
        capture_output=True,
        timeout=seconds + 30,
    )
    if result.returncode != 20 or "s UNSATISFIABLE" not in result.stdout:
        raise RuntimeError(
            f"solver did not prove {stem} UNSAT (code {result.returncode}):\n"
            f"{result.stdout}{result.stderr}"
        )
    return {
        "case": stem,
        "proof_bytes": proof.stat().st_size,
        "proof_sha256": sha256(proof),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--cadical", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=300)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    expected = json.loads(EXPECTED_PATH.read_text())

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        records = list(
            executor.map(
                lambda index: solve(
                    args.cadical, args.case_dir, args.seconds, index
                ),
                range(10),
            )
        )
    expected_records = [
        {
            "case": record["case"],
            "proof_bytes": record["proof_bytes"],
            "proof_sha256": record["proof_sha256"],
        }
        for record in expected["proof_cases"]
    ]
    assert records == expected_records
    print(json.dumps({"cases": records, "status": "UNSAT"}, sort_keys=True))


if __name__ == "__main__":
    main()
