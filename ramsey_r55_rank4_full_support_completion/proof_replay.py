#!/usr/bin/env python3
"""Regenerate and proof-check every full-support orbit formula."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

import orbit_search
import probe


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as source:
        while chunk := source.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", required=True)
    parser.add_argument("--checker", required=True)
    parser.add_argument("--exploration", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=10)
    parser.add_argument("--progress-every", type=int, default=50)
    parser.add_argument("--shards", type=int, default=1)
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--scratch", type=Path)
    args = parser.parse_args()

    exploration = json.loads(args.exploration.read_text(encoding="utf-8"))
    expected = {row["orbit_index"]: row for row in exploration["results"]}
    reps, census = orbit_search.orbit_representatives()
    if census != exploration["census"] or set(expected) != set(range(len(reps))):
        raise RuntimeError("exploration does not cover the regenerated orbit census")
    if args.shards < 1 or not 0 <= args.shard_index < args.shards:
        raise ValueError("invalid shard specification")
    target_indices = list(range(args.shard_index, len(reps), args.shards))

    completed = {}
    if args.manifest.exists():
        for line in args.manifest.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            completed[row["orbit_index"]] = row
    started = time.monotonic()
    with tempfile.TemporaryDirectory(dir=args.scratch) as tmp:
        tmp = Path(tmp)
        with args.manifest.open("a", encoding="utf-8") as manifest:
            for index in target_indices:
                if index in completed:
                    continue
                row_doubles, column_doubles = reps[index]
                rows, columns = probe.factor_lists(row_doubles, column_doubles)
                clauses = probe.clauses_for_cut(rows, columns)
                raw = probe.dimacs(clauses)
                cnf_hash = sha256(raw).hexdigest()
                if (expected[index]["cnf_sha256"] != cnf_hash or
                        expected[index]["clauses"] != len(clauses)):
                    raise RuntimeError(f"formula identity changed at orbit {index}")
                cnf = tmp / f"{index}.cnf"
                proof = tmp / f"{index}.drat"
                cnf.write_bytes(raw)
                solver_started = time.monotonic()
                run = subprocess.run(
                    [args.solver, "-q", "--unsat", "--no-binary", "-t",
                     str(args.seconds), str(cnf), str(proof)],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                    check=False, timeout=args.seconds + 10)
                solver_seconds = time.monotonic() - solver_started
                if run.returncode != 20 or "s UNSATISFIABLE" not in run.stdout:
                    raise RuntimeError(f"solver did not refute orbit {index}: {run.stdout[-500:]}")
                if not proof.is_file() or proof.stat().st_size == 0:
                    raise RuntimeError(f"missing proof for orbit {index}")
                checker_started = time.monotonic()
                checked = subprocess.run(
                    [args.checker, str(cnf), str(proof)],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                    check=False, timeout=args.seconds + 20)
                checker_seconds = time.monotonic() - checker_started
                if checked.returncode != 0 or "s VERIFIED" not in checked.stdout:
                    raise RuntimeError(f"proof rejected at orbit {index}: {checked.stdout[-500:]}")
                row = {
                    "orbit_index": index,
                    "row_doubles": list(row_doubles),
                    "column_doubles": list(column_doubles),
                    "variables": len(probe.INTERNAL),
                    "clauses": len(clauses),
                    "cnf_bytes": len(raw),
                    "cnf_sha256": cnf_hash,
                    "proof_bytes": proof.stat().st_size,
                    "proof_sha256": file_sha256(proof),
                    "solver_seconds": solver_seconds,
                    "checker_seconds": checker_seconds,
                    "status": "UNSAT_PROOF_VERIFIED",
                }
                manifest.write(json.dumps(row, sort_keys=True) + "\n")
                manifest.flush()
                os.fsync(manifest.fileno())
                completed[index] = row
                cnf.unlink()
                proof.unlink()
                if len(completed) % args.progress_every == 0:
                    print(json.dumps({"verified": len(completed), "last": row},
                                     sort_keys=True), flush=True)

    rows = [completed[i] for i in target_indices]
    manifest_raw = args.manifest.read_bytes()
    summary = {
        "schema": "rank4-full-support-proof-replay-v1",
        "census": census,
        "shard": {"index": args.shard_index, "count": args.shards,
                  "indices": target_indices},
        "verified_cases": len(rows),
        "statuses": sorted({row["status"] for row in rows}),
        "clauses_total": sum(row["clauses"] for row in rows),
        "cnf_bytes_total": sum(row["cnf_bytes"] for row in rows),
        "proof_bytes_total": sum(row["proof_bytes"] for row in rows),
        "solver_seconds_total": sum(row["solver_seconds"] for row in rows),
        "checker_seconds_total": sum(row["checker_seconds"] for row in rows),
        "solver_seconds_max": max(row["solver_seconds"] for row in rows),
        "checker_seconds_max": max(row["checker_seconds"] for row in rows),
        "distinct_cnf_hashes": len({row["cnf_sha256"] for row in rows}),
        "distinct_proof_hashes": len({row["proof_sha256"] for row in rows}),
        "manifest_sha256": sha256(manifest_raw).hexdigest(),
        "wall_seconds_this_invocation": time.monotonic() - started,
        "solver_version": subprocess.run([args.solver, "--version"],
                                         capture_output=True, text=True,
                                         check=True).stdout.strip(),
        "checker_sha256": file_sha256(Path(args.checker)),
    }
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n",
                            encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
