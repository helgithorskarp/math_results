#!/usr/bin/env python3
"""Sequential reproduction of the regular twenty-pair theorem.

Actual author six-books-2, researcher. Generated full records/logs stay in
--scratch; no external data, package, solver or compiler is required.
"""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def validate(census, independent, expected):
    require(census == expected["census"], "computed census differs from fixture")
    require(independent == expected["independent"], "computed independent audit differs from fixture")
    require(census["complete"] and independent["complete"] and census["survivors"] == 0,
            "finite domain is incomplete or has survivors")
    require(census["profiles"] == independent["profiles"], "profile data differ")
    require(census["canonical_domain_obstruction_sha256"] ==
            independent["canonical_domain_obstruction_sha256"], "canonical records differ")
    require(independent["all_R_D_inside_obstruction_records_match_entrywise"],
            "entry-level comparison missing")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--expected", type=Path, default=Path(__file__).with_name("twenty_expected.json"))
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    scratch = args.scratch.resolve()
    require(directory != scratch and directory not in scratch.parents,
            "generated records must stay outside the publication directory")
    scratch.mkdir(parents=True, exist_ok=True)
    expected = json.loads(args.expected.read_text())
    env = os.environ.copy()
    for key in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]:
        env[key] = "1"
    records = scratch / "records.jsonl"
    commands = [
        [sys.executable, "-O", str(directory / "twenty_census.py"), "--emit", "--progress",
         "--records", str(records)],
        [sys.executable, "-O", str(directory / "twenty_independent.py"), "--emit", "--progress",
         "--main-records", str(records)]]
    results, runs = [], []
    started = time.monotonic()
    for name, command in zip(["census", "independent"], commands):
        print(json.dumps({"phase": name, "status": "running", "threads": 1, "local_jobs": 1}), flush=True)
        before = time.monotonic()
        try:
            child = subprocess.run(command, capture_output=True, text=True, env=env, timeout=120)
        except subprocess.TimeoutExpired as exc:
            (scratch / "incomplete.json").write_text(json.dumps({"complete": False, "phase": name,
                "reason": "child timeout; no mathematical nonexistence conclusion", "timeout_seconds": 120}) + "\n")
            raise RuntimeError("finite proof computation timed out; no completion") from exc
        (scratch / (name + ".json")).write_text(child.stdout)
        (scratch / (name + ".stderr.txt")).write_text(child.stderr)
        require(child.returncode == 0, name + " failed; inspect scratch diagnostics, no completion")
        result = json.loads(child.stdout)
        results.append(result)
        runs.append({"name": name, "command": command, "seconds": time.monotonic() - before,
                     "peak_child_rss_kib_cumulative": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
        print(json.dumps({"phase": name, "status": "finished", "seconds": runs[-1]["seconds"]}), flush=True)
    validate(results[0], results[1], expected)
    summary = {"agent": "six-books-2", "role": "researcher", "complete": True,
               "python_version": sys.version.split()[0], "threads": 1, "local_jobs": 1,
               "child_timeout_seconds": 120, "runs": runs,
               "seconds": time.monotonic() - started,
               "peak_child_rss_kib": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               "fixture_sha256": sha256(args.expected.read_bytes()).hexdigest(),
               "canonical_domain_obstruction_sha256": results[0]["canonical_domain_obstruction_sha256"],
               "all_records_match_entrywise": True, "total_D_completions": results[0]["total_D_completions"],
               "new_finite_enumeration_is_a_theorem_premise": True,
               "author_algorithmic_independence_not_peer_review": True}
    (scratch / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
