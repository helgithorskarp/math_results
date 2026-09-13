#!/usr/bin/env python3
"""Run semantic corruptions that the independent verifier must reject."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE = json.loads((HERE / "certificate.json").read_text())


def rejected(payload):
    with tempfile.TemporaryDirectory(prefix="hn-unit-edge-controls-") as directory:
        target = Path(directory) / "bad.json"
        target.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
        run = subprocess.run(
            [sys.executable, "-B", str(HERE / "verify.py"), "--certificate", str(target)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return run.returncode != 0


def main():
    controls = []

    bad = copy.deepcopy(BASE)
    bad["schema"] = "wrong"
    controls.append(("schema", rejected(bad)))

    bad = copy.deepcopy(BASE)
    bad["distinct_parity_conflict_graphs_4"] += 1
    controls.append(("parity-count", rejected(bad)))

    bad = copy.deepcopy(BASE)
    bad["unsat_no_triple"][0]["a_mask"] ^= 1
    controls.append(("no-triple-exception", rejected(bad)))

    bad = copy.deepcopy(BASE)
    bad["allocation_count_histogram"]["4"] += 1
    controls.append(("allocation-histogram", rejected(bad)))

    bad = copy.deepcopy(BASE)
    bad["unsat_one_triple"].pop()
    controls.append(("triple-exception", rejected(bad)))

    if not all(ok for _, ok in controls):
        raise SystemExit("a corrupted certificate was accepted")
    print(json.dumps({"controls": [{"name": name, "rejected": ok} for name, ok in controls]}, sort_keys=True))


if __name__ == "__main__":
    main()
