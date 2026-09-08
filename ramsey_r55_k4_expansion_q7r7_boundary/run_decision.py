#!/usr/bin/env python3
"""One fixed physical decision using the separator-18 K4 expansion interface."""
from itertools import combinations
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import resource
import subprocess
import sys
import time

TASK = "bo1-q7-r7-c000000"
LIMIT = 1800
FORMULA_SHA256 = "755dbcd5677bbc57a0865637dbce19fa72084c4846b3996b8697bf1485070178"
SOLVER_SHA256 = "823b3c94050654fda13dab0c8c34386d9777a1e6de31bd6bc20555979e7c5e0b"
CHECKER_SHA256 = "9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a"


def identity(path):
    path = Path(path).resolve()
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return {"bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def classify(exit_code, stdout, witness):
    stdout_status = [line for line in stdout.splitlines() if line.startswith("s ")]
    witness_status = [line for line in witness.splitlines() if line.startswith("s ")]
    combined = set(stdout_status + witness_status)
    if exit_code == 0 and not combined and witness == "c UNKNOWN\n":
        return "UNKNOWN"
    if exit_code == 10 and combined == {"s SATISFIABLE"} and witness_status == ["s SATISFIABLE"]:
        return "SATISFIABLE"
    if exit_code == 20 and combined == {"s UNSATISFIABLE"} and witness_status == ["s UNSATISFIABLE"]:
        return "UNSATISFIABLE"
    return "UNEXPECTED_SOLVER_RESULT"


def controls():
    cases = [
        (0, "", "c UNKNOWN\n", "UNKNOWN"),
        (10, "s SATISFIABLE\n", "s SATISFIABLE\nv 1 0\n", "SATISFIABLE"),
        (20, "s UNSATISFIABLE\n", "s UNSATISFIABLE\n", "UNSATISFIABLE"),
        (0, "", "", "UNEXPECTED_SOLVER_RESULT"),
        (10, "s SATISFIABLE\n", "s SATISFIABLE\ns UNSATISFIABLE\n", "UNEXPECTED_SOLVER_RESULT"),
        (20, "s UNSATISFIABLE\n", "c UNKNOWN\n", "UNEXPECTED_SOLVER_RESULT"),
    ]
    if any(classify(*row[:3]) != row[3] for row in cases):
        raise ValueError("result classification controls")
    return {"status": "VERIFIED_FAIL_CLOSED_RESULT_CLASSIFIER", "cases": len(cases)}


def run(args):
    controls()
    solver = args.solver.resolve()
    checker = args.checker.resolve()
    cnf = args.cnf.resolve()
    cache = args.cache.resolve()
    source = args.source.resolve()
    output = args.output.resolve()
    output.mkdir(exist_ok=False)
    receipt = {
        "task": TASK,
        "encoding": "h3887 ordered h3881 triangle formula plus h3899 K4 expansion interface",
        "seconds_limit": LIMIT,
        "solver": identity(solver),
        "checker": identity(checker),
        "cnf": identity(cnf),
        "source_commit": "f4f731fa29ec932099bda4ca88591220e2808f33",
        "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "target_found": False,
        "family_excluded": False,
        "solver_calls": 1,
    }
    if receipt["cnf"]["sha256"] != FORMULA_SHA256:
        raise ValueError("audited formula identity")
    if receipt["solver"]["sha256"] != SOLVER_SHA256:
        raise ValueError("solver identity")
    if receipt["checker"]["sha256"] != CHECKER_SHA256:
        raise ValueError("checker identity")
    command = [str(solver), "-t", str(LIMIT), "-w", "witness.txt", str(cnf), "trace.drat"]
    receipt["command"] = command
    (output / "FROZEN.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    start = time.monotonic()
    with (output / "stdout.txt").open("wb") as stdout, (output / "stderr.txt").open("wb") as stderr:
        result = subprocess.run(command, cwd=output, stdout=stdout, stderr=stderr)
    receipt.update(exit_code=result.returncode,
                   elapsed_seconds=time.monotonic() - start,
                   solver_max_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    for name in ("stdout.txt", "stderr.txt", "witness.txt", "trace.drat"):
        if (output / name).exists():
            receipt[name] = identity(output / name)
    stdout_text = (output / "stdout.txt").read_text()
    witness_text = (output / "witness.txt").read_text()
    outcome = classify(result.returncode, stdout_text, witness_text)
    receipt["solver_status_lines"] = [line for line in stdout_text.splitlines() if line.startswith("s ")]
    receipt["witness_status"] = witness_text.splitlines()[0] if witness_text.splitlines() else ""
    if outcome == "UNKNOWN":
        receipt.update(status="UNKNOWN", proof_status="PARTIAL_STREAM_NOT_A_CERTIFICATE")
    elif outcome == "SATISFIABLE":
        command = [sys.executable, "-B", str(source / "ramsey_r55_k4_expansion_interface" / "augment.py"),
                   str(cache), "--task", TASK, "--triangles", "--sat", str(output / "witness.txt")]
        checked = subprocess.run(command, cwd=source, text=True, capture_output=True)
        (output / "sat_check_stdout.txt").write_text(checked.stdout)
        (output / "sat_check_stderr.txt").write_text(checked.stderr)
        if checked.returncode != 0:
            receipt.update(status="SAT_MODEL_REJECTED", sat_check_exit_code=checked.returncode)
            (output / "RESULT.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
            raise ValueError("SAT model rejected by augmented physical decoder")
        certificate = json.loads(checked.stdout)
        if certificate.get("status") != "VERIFIED_GOOD43":
            raise ValueError("SAT decoder did not certify good43")
        (output / "GOOD43.json").write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
        bits = int(certificate["graph"]["red_hex"], 16)
        edges = "".join(f"{u} {v}\n" for k, (u, v) in enumerate(combinations(range(43), 2))
                        if bits >> k & 1)
        (output / "GOOD43.edges").write_text("43\n" + edges)
        receipt.update(status="VERIFIED_GOOD43", target_found=True,
                       physical_check=certificate["certificate"],
                       carrier_code=certificate["carrier_code"])
    elif outcome == "UNSATISFIABLE":
        receipt["status"] = "UNSAT_CERTIFICATE_PENDING"
        (output / "RESULT.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
        with (output / "checker.txt").open("wb") as log:
            checked = subprocess.run([str(checker), str(cnf), str(output / "trace.drat")],
                                     stdout=log, stderr=subprocess.STDOUT)
        checker_text = (output / "checker.txt").read_text()
        receipt.update(checker_exit_code=checked.returncode,
                       checker_log=identity(output / "checker.txt"),
                       combined_max_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        if checked.returncode != 0 or "s VERIFIED" not in checker_text:
            (output / "RESULT.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
            raise ValueError("DRAT verification failed")
        receipt.update(status="CERTIFIED_UNSAT", family_excluded=True,
                       proof_status="INDEPENDENTLY_VERIFIED_DRAT")
    else:
        receipt["status"] = "UNEXPECTED_SOLVER_RESULT"
        (output / "RESULT.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
        raise ValueError("unexpected solver result")
    (output / "RESULT.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    return receipt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path)
    parser.add_argument("--checker", type=Path)
    parser.add_argument("--cnf", type=Path)
    parser.add_argument("--cache", type=Path)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--controls", action="store_true")
    args = parser.parse_args()
    if args.controls:
        print(json.dumps(controls(), sort_keys=True))
        return
    if any(value is None for value in
           (args.solver, args.checker, args.cnf, args.cache, args.source, args.output)):
        parser.error("all decision paths are required")
    print(json.dumps(run(args), sort_keys=True))


if __name__ == "__main__":
    main()
