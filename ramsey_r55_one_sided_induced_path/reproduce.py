#!/usr/bin/env python3
"""Regenerate and independently audit both CNFs; verify the saved text proofs."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=True)
    for line in (root / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split("  ", 1)
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != digest:
            raise ValueError(f"Source/certificate hash mismatch: {name}")
    expected = json.loads((root / "EXPECTED.json").read_text())
    interpreter = [sys.executable] + (["-O"] if sys.flags.optimize else [])
    results = {}
    for case in ("G1", "G2"):
        cnf = args.out / f"{case}.cnf"
        commands = [
            ["build.py", case, "--out", str(args.out)],
            ["audit.py", case, str(cnf), "--out", str(args.out / f"{case}.audit.json")],
            ["check_rup.py", str(cnf), str(root / f"{case}.proof"), "--out", str(args.out / f"{case}.rup.json")],
        ]
        for command in commands:
            subprocess.run(interpreter + [str(root / command[0])] + command[1:], check=True, stdout=subprocess.DEVNULL)
        actual = {kind: json.loads((args.out / f"{case}.{kind}.json").read_text()) for kind in ("build", "audit", "rup")}
        if actual != expected[case]:
            raise ValueError(f"Expected result mismatch for {case}")
        results[case] = {"variables": actual["build"]["variables"], "clauses": actual["build"]["clauses"],
                         "rup_additions": actual["rup"]["additions"], "verified": True}
    result = {"complete_18_vertex_families": results, "all_formula_audits_and_proofs": "PASS",
              "imported_classification": "Cameron et al., arXiv:2005.03441v1, Theorem 7 (not reproduced)"}
    (args.out / "RESULT.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
