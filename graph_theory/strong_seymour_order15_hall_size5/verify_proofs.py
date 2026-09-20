#!/usr/bin/env python3
"""Run drat-trim on all nine cases and check exact expected records."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import re
import subprocess


EXPECTED_PATH = Path(__file__).with_name("EXPECTED.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def numbers(pattern: str, transcript: str) -> tuple[int, ...]:
    match = re.search(pattern, transcript)
    if match is None:
        raise RuntimeError(f"missing checker field {pattern!r}")
    return tuple(int(value) for value in match.groups())


def stem(case: str) -> str:
    return "s5-tight" if case == "tight" else f"s5-strict-type-{case[-2:]}"


def verify(checker: Path, case_dir: Path, case: str) -> dict[str, object]:
    name = stem(case)
    cnf = case_dir / f"{name}.cnf"
    proof = case_dir / f"{name}.drat"
    result = subprocess.run(
        [str(checker), str(cnf), str(proof)],
        text=True,
        capture_output=True,
        timeout=300,
    )
    transcript = result.stdout + result.stderr
    if result.returncode or "s VERIFIED" not in transcript:
        raise RuntimeError(f"proof check failed for {case}:\n{transcript}")
    core_clauses, input_clauses = numbers(
        r"(\d+) of (\d+) clauses in core", transcript
    )
    core_lemmas, proof_lemmas, resolution_steps = numbers(
        r"(\d+) of (\d+) lemmas in core using (\d+) resolution steps",
        transcript,
    )
    (rat_lemmas,) = numbers(r"(\d+) RAT lemmas in core", transcript)
    return {
        "case": case,
        "cnf_bytes": cnf.stat().st_size,
        "cnf_sha256": sha256(cnf),
        "core_clauses": core_clauses,
        "core_lemmas": core_lemmas,
        "input_clauses": input_clauses,
        "proof_bytes": proof.stat().st_size,
        "proof_lemmas": proof_lemmas,
        "proof_sha256": sha256(proof),
        "rat_lemmas": rat_lemmas,
        "resolution_steps": resolution_steps,
        "status": "VERIFIED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    expected = json.loads(EXPECTED_PATH.read_text())
    cases = [record["case"] for record in expected["proof_cases"]]

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        records = list(
            executor.map(
                lambda case: verify(args.checker, args.case_dir, case), cases
            )
        )
    assert records == expected["proof_cases"]
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    manifest_sha256 = hashlib.sha256(canonical.encode()).hexdigest()
    assert manifest_sha256 == expected["proof_manifest_sha256"]
    total_proof_bytes = sum(record["proof_bytes"] for record in records)
    assert total_proof_bytes == expected["total_proof_bytes"]
    print(
        json.dumps(
            {
                "cases": len(records),
                "manifest_sha256": manifest_sha256,
                "status": "VERIFIED",
                "total_proof_bytes": total_proof_bytes,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
