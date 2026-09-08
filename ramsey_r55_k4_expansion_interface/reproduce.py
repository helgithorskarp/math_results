#!/usr/bin/env python3
"""Manifest, normal/-O replay, and optional full-formula audit."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import locked

HERE = Path(__file__).resolve().parent


def manifest():
    lines = (HERE / "SHA256SUMS").read_text().splitlines()
    for line in lines:
        digest, name = line.split("  ", 1)
        if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != digest:
            raise ValueError("manifest mismatch " + name)
    return len(lines)


def run_check(optimized=False):
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command += ["-B", str(HERE / "check.py")]
    return json.loads(subprocess.check_output(command, text=True))


def full_formula(cache, path, generate):
    task = "bo1-q7-r7-c000000"
    path = Path(path)
    if generate:
        command = [sys.executable, "-B", str(HERE / "augment.py"), str(cache),
                   "--task", task, "--triangles", "--cnf", str(path)]
        producer = json.loads(subprocess.check_output(command, text=True))
    else:
        producer = None
    command = [sys.executable, "-B", str(HERE / "audit.py"), "--cache", str(cache),
               "--task", task, "--triangles", "--cnf", str(path)]
    normal = json.loads(subprocess.check_output(command, text=True))
    command.insert(1, "-O")
    optimized = json.loads(subprocess.check_output(command, text=True))
    if normal != optimized:
        raise ValueError("normal/-O full audit mismatch")
    if producer is not None:
        for key in ("variables", "clauses", "bytes", "max_width", "sha256",
                    "ordered_variables", "ordered_clauses", "expansion_variables",
                    "expansion_clauses"):
            if producer[key] != normal[key]:
                raise ValueError("full producer/auditor mismatch " + key)
    expected = json.loads((HERE / "FORMULA_AUDIT.json").read_text())
    if normal != expected:
        raise ValueError("frozen full formula audit changed")
    return normal


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache")
    parser.add_argument("--cnf")
    parser.add_argument("--generate", action="store_true")
    args = parser.parse_args()
    if bool(args.cache) != bool(args.cnf):
        parser.error("--cache and --cnf are required together")
    locked.load()
    normal = run_check(False)
    optimized = run_check(True)
    if normal != optimized:
        raise ValueError("normal/-O compact replay mismatch")
    expected = json.loads((HERE / "VALIDATION.json").read_text())
    if normal != expected:
        raise ValueError("frozen compact result changed")
    result = {"status": "REPRODUCED_K4_EXPANSION_INTERFACE",
              "manifest_entries": manifest(), "compact": normal}
    if args.cache:
        result["full_formula"] = full_formula(args.cache, args.cnf, args.generate)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
