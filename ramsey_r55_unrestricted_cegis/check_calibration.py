#!/usr/bin/env python3
"""Reproduce the deterministic good32 calibration and verify it physically."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

import verify


def parse_result(output: str) -> dict[str, str]:
    rows = [line for line in output.splitlines() if line.startswith("RESULT ")]
    if len(rows) != 1:
        raise RuntimeError("expected exactly one RESULT line")
    return dict(token.split("=", 1) for token in rows[0].split()[1:])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("executable", type=Path)
    parser.add_argument("--expected", type=Path,
                        default=Path(__file__).with_name("calibration_good32.json"))
    args = parser.parse_args()
    expected = json.loads(args.expected.read_text(encoding="utf-8"))
    command = [str(args.executable.resolve()), "32", "32", "5000", "500", "10000"]
    completed = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, check=False)
    if completed.returncode != 0:
        raise SystemExit(completed.stdout + completed.stderr)
    result = parse_result(completed.stdout)
    actual = {
        "status": result["status"],
        "n": int(result["n"]),
        "seed": 32,
        "initial_fives": 500,
        "max_new": 10000,
        "rounds": int(result["rounds"]),
        "clauses_added": int(result["clauses_added"]),
        "red_edges": int(result["red_edges"]),
        "red_bits_hex": result["red_bits_hex"],
    }
    physical = verify.audit(32, verify.decode_hex(32, actual["red_bits_hex"]))
    actual.update({
        "independent_five_subsets_checked": physical["five_subsets_checked"],
        "red_K5": physical["red_K5"],
        "blue_K5": physical["blue_K5"],
    })
    if actual != expected:
        print(json.dumps(actual, indent=2, sort_keys=True))
        raise SystemExit("calibration differs from expected result")
    print(json.dumps({
        "status": "REPRODUCED_GOOD32",
        "rounds": actual["rounds"],
        "clauses_added": actual["clauses_added"],
        "five_subsets_checked": physical["five_subsets_checked"],
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
