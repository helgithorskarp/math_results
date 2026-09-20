#!/usr/bin/env python3
"""Run drat-trim on the ten generated cases and check exact expected data."""

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


def verify(checker: Path, case_dir: Path, index: int) -> dict[str, object]:
    stem = f"s4-orbit-{index:02d}"
    cnf = case_dir / f"{stem}.cnf"
    proof = case_dir / f"{stem}.drat"
    result = subprocess.run(
        [str(checker), str(cnf), str(proof)],
        text=True,
        capture_output=True,
        timeout=120,
    )
    transcript = result.stdout + result.stderr
    if result.returncode or "s VERIFIED" not in transcript:
        raise RuntimeError(f"proof check failed for {stem}:\n{transcript}")
    core_clauses, input_clauses = numbers(
        r"(\d+) of (\d+) clauses in core", transcript
    )
    core_lemmas, proof_lemmas, resolution_steps = numbers(
        r"(\d+) of (\d+) lemmas in core using (\d+) resolution steps",
        transcript,
    )
    (rat_lemmas,) = numbers(r"(\d+) RAT lemmas in core", transcript)
    return {
        "case": stem,
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
    args = parser.parse_args()
    expected = json.loads(EXPECTED_PATH.read_text())

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        records = list(
            executor.map(
                lambda index: verify(args.checker, args.case_dir, index),
                range(10),
            )
        )
    assert records == expected["proof_cases"]
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    manifest_sha256 = hashlib.sha256(canonical.encode()).hexdigest()
    assert manifest_sha256 == expected["proof_manifest_sha256"]
    assert sum(record["proof_bytes"] for record in records) == expected[
        "total_proof_bytes"
    ]
    print(
        json.dumps(
            {
                "cases": len(records),
                "manifest_sha256": manifest_sha256,
                "status": "VERIFIED",
                "total_proof_bytes": expected["total_proof_bytes"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
