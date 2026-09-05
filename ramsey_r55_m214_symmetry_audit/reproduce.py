#!/usr/bin/env python3
"""Fetch pinned sources, regenerate the OPB outside Git, and audit its semantics."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import time
import urllib.request

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", required=True, type=Path, help="generated-state directory outside the repository")
    parser.add_argument("--cxx", default="g++")
    args = parser.parse_args()
    work = args.work.resolve()
    require(not work.is_relative_to(ROOT.parent), "generated state must be outside this repository")
    work.mkdir(parents=True, exist_ok=True)
    upstream = work / "upstream"
    upstream.mkdir(exist_ok=True)
    manifest = json.loads((ROOT / "upstream_manifest.json").read_text())
    base = "https://raw.githubusercontent.com/{repository}/{commit}/{directory}/".format(**manifest)
    for entry in manifest["files"]:
        path = upstream / entry["name"]
        data = path.read_bytes() if path.exists() else urllib.request.urlopen(base + entry["name"], timeout=60).read()
        require(len(data) == entry["bytes"] and hashlib.sha256(data).hexdigest() == entry["sha256"],
                f"pinned upstream file mismatch: {entry['name']}")
        if not path.exists():
            path.write_bytes(data)
    timings = []

    def run(label, command, cwd):
        start = time.monotonic()
        completed = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True, timeout=300, check=False)
        (work / (label + ".log")).write_text(completed.stdout)
        elapsed = time.monotonic() - start
        timings.append({"step": label, "seconds": round(elapsed, 3), "returncode": completed.returncode})
        require(completed.returncode == 0, f"{label} failed; see {work / (label + '.log')}")
        print(f"PASS {label} ({elapsed:.2f}s)", flush=True)
        return completed.stdout

    audit_text = run("upstream_arithmetic", [sys.executable, "audit_reduction.py"], upstream)
    formula = work / "formula.opb"
    generate_text = run("upstream_generate", [sys.executable, "generate_opb.py", "--output", str(formula)], upstream)
    binary = work / "check_upstream"
    run("upstream_compile", [args.cxx, "-std=c++20", "-O2", "-Wall", "-Wextra", "-Wpedantic", "-Werror",
                             "check_opb.cpp", "-o", str(binary)], upstream)
    check_text = run("upstream_reconstruct", [str(binary), str(formula)], upstream)
    require(audit_text + generate_text + check_text == (upstream / "EXPECTED_OUTPUT.txt").read_text(),
            "upstream expected output mismatch")
    semantic = json.loads(run("semantic_check", [sys.executable, str(ROOT / "check_semantics.py"), str(formula)], ROOT))
    lemma = json.loads(run("lemma_check", [sys.executable, str(ROOT / "verify.py")], ROOT))
    result = {"upstream_commit": manifest["commit"], "formula": semantic, "lemma": lemma}
    require(result == json.loads((ROOT / "expected.json").read_text()), "compact expected result mismatch")
    report = {"complete": True, "result": result, "timings": timings, "solver_run": False}
    (work / "reproduction.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("PASS: OPB semantics reproduced; conditional order-three range 10..12; no SAT/UNSAT verdict.")


if __name__ == "__main__":
    main()
