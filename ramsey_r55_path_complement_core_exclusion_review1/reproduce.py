#!/usr/bin/env python3
"""Reproduce the source package and independent h3931 review."""

import argparse
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_COMMIT = "e7d5932b57e804bf1f2dcb00f89360af0f76fa2e"
SOURCE_DIRECTORY = "ramsey_r55_path_complement_core_exclusion"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def run_json(command, cwd):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                            check=True)
    need(not result.stderr, "unexpected stderr: " + " ".join(map(str, command)))
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path,
                        help="root of the math_results checkout")
    args = parser.parse_args()
    root = args.root.resolve()
    source = root / SOURCE_DIRECTORY
    resolved = subprocess.run(
        ["git", "rev-parse", SOURCE_COMMIT + "^{commit}"], cwd=root,
        capture_output=True, text=True, check=True
    ).stdout.strip()
    need(resolved == SOURCE_COMMIT, "reviewed source commit unavailable")
    unchanged = subprocess.run(
        ["git", "diff", "--quiet", SOURCE_COMMIT, "--", SOURCE_DIRECTORY],
        cwd=root
    )
    need(unchanged.returncode == 0, "reviewed source directory differs")

    source_receipts = []
    for optimized in (False, True):
        command = [sys.executable]
        if optimized:
            command.append("-O")
        command.extend(["-B", str(source / "reproduce.py")])
        source_receipts.append(run_json(command, root))
    need(source_receipts[0] == source_receipts[1], "source replay modes")
    need(source_receipts[0]["status"] ==
         "REPRODUCED_COMPLETE_HEREDITARY_CORE_EXCLUSION", "source status")

    independent_receipts = []
    for optimized in (False, True):
        command = [sys.executable]
        if optimized:
            command.append("-O")
        command.extend(["-B", str(HERE / "independent_check.py"), str(source)])
        independent_receipts.append(run_json(command, root))
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    need(independent_receipts[0] == independent_receipts[1] == expected,
         "independent replay modes or expected receipt")

    print(json.dumps({
        "status": "REPRODUCED_ACCEPT_REVIEW_H3931",
        "reviewed_source_commit": SOURCE_COMMIT,
        "source_modes_equal": True,
        "independent_modes_equal": True,
        "manifest_entries": expected["manifest_entries"],
        "capacity_table": expected["capacity_table"],
        "c5_cap_rows_enumerated": expected["c5_cap_rows_enumerated"],
        "witness_five_sets_checked": expected["witness_five_sets_checked"],
        "exact_class_maximum": expected["exact_class_maximum"],
        "excluded_core_order": expected["excluded_core_order"],
        "good43_found": False,
        "solver_calls": 0,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
