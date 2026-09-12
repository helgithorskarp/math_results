#!/usr/bin/env python3
"""Full deterministic reconstruction of every finite catalogue layer."""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run(command):
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise ValueError("command failed:\n" + result.stdout + result.stderr)


def without_timing(value):
    if isinstance(value, dict):
        return {key: without_timing(item) for key, item in value.items()
                if key != "elapsed_seconds"}
    if isinstance(value, list):
        return [without_timing(item) for item in value]
    return value


def compare(actual, expected):
    left = without_timing(json.loads(actual.read_text()))
    right = without_timing(json.loads((ROOT / expected).read_text()))
    if left != right:
        raise ValueError(f"reproduction mismatch: {expected}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--drat-trim", required=True)
    args = parser.parse_args()
    python = sys.executable
    with tempfile.TemporaryDirectory(prefix="r55-edge-window-reproduce-") as raw_tmp:
        tmp = Path(raw_tmp)
        coarse = tmp / "COARSE.json"
        physical = tmp / "PHYSICAL.json"
        closure = tmp / "CLOSURE.json"
        ct = tmp / "CT.json"
        run([python, str(ROOT / "scan_t5_127.py"), str(args.catalog),
             str(coarse)])
        compare(coarse, "COARSE.json")
        run([python, str(ROOT / "physical_t5_127.py"),
             "--catalog", str(args.catalog), "--coarse", str(coarse),
             "--output", str(physical)])
        compare(physical, "PHYSICAL.json")
        run([python, str(ROOT / "closure_t5_127.py"),
             "--catalog", str(args.catalog), "--physical", str(physical),
             "--output", str(closure)])
        compare(closure, "CLOSURE.json")
        run([python, str(ROOT / "ct_t5_open.py"),
             "--catalog", str(args.catalog), "--physical", str(physical),
             "--closure", str(closure), "--output", str(ct)])
        compare(ct, "CT.json")
    run([python, str(ROOT / "verify.py"), "--catalog", str(args.catalog),
         "--drat-trim", args.drat_trim])
    print(json.dumps({"status": "FULL_REPRODUCTION_AND_PROOF_CHECK_PASSED"},
                     sort_keys=True))


if __name__ == "__main__":
    main()
