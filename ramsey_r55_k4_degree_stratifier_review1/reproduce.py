#!/usr/bin/env python3
"""Reproduce the source and independent review checks for h3925."""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "ramsey_r55_k4_degree_stratifier"
BASELINE = ROOT / "ramsey_r55_k4_expansion_interface"
TASK = "bo1-q7-r7-c000000"
SOURCE_COMMIT = "68ce2ce13db7885be3c5f225a1108baf102cd3f4"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def command(script, *arguments, optimized=False):
    result = [sys.executable]
    if optimized:
        result.append("-O")
    result.extend(["-B", str(script), *map(str, arguments)])
    return result


def run(script, *arguments, optimized=False):
    result = subprocess.run(command(script, *arguments, optimized=optimized),
                            cwd=ROOT, capture_output=True, text=True, check=True)
    need(not result.stderr, "unexpected stderr from " + script.name)
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cache", type=Path)
    args = parser.parse_args()
    commit = subprocess.run(["git", "rev-parse", SOURCE_COMMIT + "^{commit}"],
                            cwd=ROOT, capture_output=True, text=True,
                            check=True).stdout.strip()
    need(commit == SOURCE_COMMIT, "reviewed source commit unavailable")
    unchanged = subprocess.run(
        ["git", "diff", "--quiet", SOURCE_COMMIT, "--",
         TARGET.name, BASELINE.name], cwd=ROOT
    )
    need(unchanged.returncode == 0, "reviewed source directories differ")

    base_compact = run(BASELINE / "check.py")
    need(base_compact == run(BASELINE / "check.py", optimized=True),
         "baseline compact modes")
    target_compact = run(TARGET / "check.py")
    need(target_compact == run(TARGET / "check.py", optimized=True),
         "target compact modes")

    temporary_root = os.environ.get("TMPDIR")
    with tempfile.TemporaryDirectory(prefix="r55-k4-degree-review-",
                                     dir=temporary_root) as raw:
        base_cnf = Path(raw) / "baseline.cnf"
        target_cnf = Path(raw) / "target.cnf"
        base_produced = run(BASELINE / "augment.py", args.cache, "--task", TASK,
                            "--triangles", "--cnf", base_cnf)
        base_audits = [
            run(BASELINE / "audit.py", "--cache", args.cache, "--task", TASK,
                "--triangles", "--cnf", base_cnf, optimized=optimized)
            for optimized in (False, True)
        ]
        base_expected = json.loads((BASELINE / "FORMULA_AUDIT.json").read_text())
        need(base_audits[0] == base_audits[1] == base_expected,
             "baseline literal audits")
        for field in ("variables", "clauses", "bytes", "max_width", "sha256"):
            need(base_produced[field] == base_expected[field],
                 "baseline producer field " + field)

        target_produced = run(TARGET / "stratify.py", args.cache, "--task", TASK,
                              "--triangles", "--cnf", target_cnf)
        target_audits = [
            run(TARGET / "audit.py", "--cache", args.cache, "--task", TASK,
                "--triangles", "--cnf", target_cnf, optimized=optimized)
            for optimized in (False, True)
        ]
        target_expected = json.loads((TARGET / "FORMULA_AUDIT.json").read_text())
        need(target_audits[0] == target_audits[1] == target_expected,
             "target literal audits")
        for field in ("variables", "clauses", "bytes", "max_width", "sha256"):
            need(target_produced[field] == target_expected[field],
                 "target producer field " + field)

        integration = [run(TARGET / "integration.py", args.cache,
                           optimized=optimized) for optimized in (False, True)]
        integration_expected = json.loads((TARGET / "INTEGRATION.json").read_text())
        need(integration[0] == integration[1] == integration_expected,
             "all-macro-class integration")

        independent = [
            run(HERE / "independent_check.py", ROOT, args.cache, base_cnf, target_cnf,
                optimized=optimized) for optimized in (False, True)
        ]
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        need(independent[0] == independent[1] == expected,
             "independent checker receipt")

    receipt = {
        "status": "REPRODUCED_INDEPENDENT_REVIEW_H3925",
        "reviewed_source_commit": SOURCE_COMMIT,
        "baseline_compact_modes_equal": True,
        "target_compact_modes_equal": True,
        "baseline_literal_audit_modes_equal": True,
        "target_literal_audit_modes_equal": True,
        "macro_class_integration_modes_equal": True,
        "independent_modes_equal": True,
        "formula_sha256": expected["target_formula_sha256"],
        "formula_clauses": expected["target_clauses"],
        "prefix_clauses_equal": expected["prefix_clauses_equal"],
        "independently_reconstructed_suffix_clauses":
            expected["independently_reconstructed_suffix_clauses"],
        "minimum_contact_floors": expected["minimum_contact_floors"],
        "physical_tasks": expected["physical_tasks"],
        "solver_calls": 0,
        "tasks_decided": 0,
        "good43_found": False,
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
