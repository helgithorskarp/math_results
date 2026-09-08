#!/usr/bin/env python3
"""Reproduce the complete Cayley(44) puncture exclusion."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent


def run(*args):
    proc = subprocess.run([sys.executable, "-B", *map(str, args)], cwd=ROOT,
                          capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError((args, proc.returncode, proc.stdout, proc.stderr))
    return proc.stdout


def semantic_dpll(rows):
    keys = ("variables", "clauses", "satisfiable", "calls", "cached_states",
            "cache_hits", "branches", "conflicts", "units")
    return [{k: row[k] for k in keys} for row in rows]


def check_manifest():
    for line in (ROOT / "SHA256SUMS").read_text().splitlines():
        expected, rel = line.split("  ", 1)
        actual = sha256((ROOT / rel).read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError((rel, expected, actual))


def main():
    expected = json.loads((ROOT / "EXPECTED.json").read_text())
    run(ROOT / "generate.py", ROOT / "formulas")
    audit = json.loads(run(ROOT / "audit.py", ROOT))
    controls = json.loads(run(ROOT / "controls.py"))
    core_paths = [ROOT / "cores" / f"{name}.core.cnf" for name in
                  ("c11_c4", "c11_v4", "c11_sd_c4", "c11_sd_v4")]
    dpll = json.loads(run(ROOT / "dpll_check.py", *core_paths))
    if audit != expected["audit"]:
        raise AssertionError("audit mismatch")
    if controls != expected["controls"]:
        raise AssertionError("control mismatch")
    if semantic_dpll(dpll) != expected["dpll"]:
        raise AssertionError("DPLL mismatch")
    check_manifest()
    print("REPRODUCED_COMPLETE_CAYLEY44_PUNCTURE_EXCLUSION")


if __name__ == "__main__":
    main()
