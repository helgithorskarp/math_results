#!/usr/bin/env python3
"""Regenerate, independently reconstruct, solve, and replay both formulas.

All generated files stay in --work. Reference hashes identify the observed
proofs; acceptance requires an actual successful replay of the fresh proof.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args, expected=0, log=None):
    started = time.monotonic()
    result = subprocess.run([str(arg) for arg in args], capture_output=True,
                            text=True, check=False)
    output = result.stdout + result.stderr
    if log is not None:
        log.write_text(output)
    if result.returncode != expected:
        raise RuntimeError(f"command failed ({result.returncode}): {args}\n{output[-4000:]}")
    return output, time.monotonic() - started


def reject_mutations(checker, h, cnf, work):
    lines = cnf.read_text().splitlines()
    header = lines[0].split()
    missing = work / f"h{h}.missing.cnf"
    missing.write_text(f"p cnf 148 {int(header[3])-1}\n" +
                       "\n".join(lines[2:]) + "\n")
    changed = work / f"h{h}.changed.cnf"
    tokens = lines[1].split()
    tokens[0] = str(-int(tokens[0]))
    changed.write_text(lines[0] + "\n" + " ".join(tokens) + "\n" +
                       "\n".join(lines[2:]) + "\n")
    for path in (missing, changed):
        output, _ = run([checker, h, h, path], expected=1)
        if "complete clause multiset mismatch" not in output:
            raise RuntimeError(f"mutation did not reach the comparison: {output}")
        path.unlink()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--kissat", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--cxx", default="g++")
    parser.add_argument("--seconds", type=int, default=120)
    args = parser.parse_args()
    work = args.work.resolve()
    if work == HERE or HERE in work.parents:
        parser.error("--work must be outside the contribution directory")
    if args.seconds <= 0:
        parser.error("--seconds must be positive")
    work.mkdir(parents=True, exist_ok=True)
    reference = json.loads((HERE / "result.json").read_text())
    for line in (HERE / "SHA256SUMS").read_text().splitlines():
        expected, name = line.split(maxsplit=1)
        if digest(HERE / name.strip()) != expected:
            raise RuntimeError(f"source hash mismatch: {name}")
    checker = work / "independent_formula"
    run([args.cxx, "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
         HERE / "independent_formula.cpp", "-o", checker])
    output, _ = run([sys.executable, HERE / "audit_normalization.py"])
    print(output.strip(), flush=True)
    records = []
    for case in reference["cases"]:
        h = case["h"]
        cnf, proof = work / f"h{h}.cnf", work / f"h{h}.drat"
        _, generation_seconds = run([sys.executable, HERE / "generate_formula.py",
                                     "--h", h, "--out", cnf])
        if digest(cnf) != case["cnf"]["sha256"]:
            raise RuntimeError(f"generated CNF hash mismatch for h={h}")
        output, reconstruction_seconds = run([checker, h, h, cnf])
        print(output.strip(), flush=True)
        reject_mutations(checker, h, cnf, work)
        solve_output, solve_seconds = run(
            [args.kissat.resolve(), f"--time={args.seconds}", "--quiet", cnf, proof],
            expected=20, log=work / f"h{h}.solve.log")
        if "s UNSATISFIABLE" not in solve_output:
            raise RuntimeError("missing solver UNSAT status")
        replay_output, replay_seconds = run(
            [args.drat_trim.resolve(), cnf, proof], log=work / f"h{h}.replay.log")
        if "s VERIFIED" not in replay_output:
            raise RuntimeError("missing successful DRAT replay")
        record = {"h": h, "cnf_sha256": digest(cnf), "proof_sha256": digest(proof),
                  "proof_bytes": proof.stat().st_size,
                  "proof_hash_matches_reference": digest(proof) == case["proof"]["sha256"],
                  "generation_seconds": generation_seconds,
                  "reconstruction_seconds": reconstruction_seconds,
                  "solve_seconds": solve_seconds, "replay_seconds": replay_seconds,
                  "mutation_rejections": 2, "status": "UNSAT", "replay": "VERIFIED"}
        records.append(record)
        print(f"CERTIFICATE h={h} UNSAT VERIFIED mutations_rejected=2 "
              f"reference_proof_hash={record['proof_hash_matches_reference']}", flush=True)
    report = {"cases": records, "tool_binary_sha256": {
        "kissat": digest(args.kissat.resolve()), "drat_trim": digest(args.drat_trim.resolve())}}
    (work / "reproduction.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("PASS: both residual order-five incidence patterns are certified UNSAT")


if __name__ == "__main__":
    main()
