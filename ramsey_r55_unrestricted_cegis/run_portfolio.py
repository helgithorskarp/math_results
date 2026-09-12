#!/usr/bin/env python3
"""Run the four complete root-degree normalizations as independent processes."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess

import verify


def parse_result(output: str) -> dict:
    lines = [line for line in output.splitlines() if line.startswith("RESULT ")]
    if len(lines) != 1:
        raise RuntimeError("producer did not emit exactly one RESULT line")
    fields = {}
    for token in lines[0].split()[1:]:
        key, value = token.split("=", 1)
        fields[key] = value
    for key in ("n", "root_degree", "rounds", "clauses_added", "red_edges",
                "best", "best_red", "best_blue", "best_edges"):
        if key in fields:
            fields[key] = int(fields[key])
    return fields


def run_one(executable: Path, work: Path, degree: int, seed: int, rounds: int,
            initial_fives: int, max_new: int) -> dict:
    checkpoint = work / f"degree-{degree}.checkpoint"
    command = [
        str(executable), "43", str(seed), str(rounds), str(initial_fives),
        str(max_new), str(degree), "18", "24", str(checkpoint),
    ]
    completed = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, check=False)
    log = completed.stdout + completed.stderr
    (work / f"degree-{degree}.log").write_text(log, encoding="utf-8")
    if completed.returncode != 0:
        raise RuntimeError(f"degree {degree} producer failed with {completed.returncode}")
    result = parse_result(completed.stdout)
    if result.get("n") != 43 or result.get("root_degree") != degree:
        raise RuntimeError("producer result identity mismatch")
    if result["status"] == "UNSAT_SUBFORMULA":
        result.update({
            "seed": seed,
            "command": command[:-1] + ["<checkpoint>"],
            "physical_status": "NOT_APPLICABLE",
            "checkpoint_sha256": hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
        })
        return result
    graph_hex = result.get("red_bits_hex") or result.get("best_hex")
    if graph_hex is None:
        raise RuntimeError("producer result omitted its physical graph")
    physical = verify.audit(43, verify.decode_hex(43, graph_hex))
    expected_status = "GOOD_GRAPH" if physical["status"] == "GOOD_GRAPH" else "INCOMPLETE"
    if result["status"] != expected_status:
        raise RuntimeError("producer and independent physical status disagree")
    if result["status"] == "GOOD_GRAPH" and physical["status"] != "GOOD_GRAPH":
        raise RuntimeError("claimed target rejected")
    result.update({
        "seed": seed,
        "command": command[:-1] + ["<checkpoint>"],
        "physical_status": physical["status"],
        "physical_red_K5": physical["red_K5"],
        "physical_blue_K5": physical["blue_K5"],
        "physical_five_subsets_checked": physical["five_subsets_checked"],
        "graph_sha256": hashlib.sha256(graph_hex.encode("ascii")).hexdigest(),
        "checkpoint_sha256": hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
    })
    result.pop("red_bits_hex", None)
    result.pop("best_hex", None)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("executable", type=Path)
    parser.add_argument("work", type=Path)
    parser.add_argument("--rounds", type=int, default=120)
    parser.add_argument("--base-seed", type=int, default=36000)
    parser.add_argument("--initial-fives", type=int, default=2000)
    parser.add_argument("--max-new", type=int, default=10000)
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    if args.work.exists():
        raise SystemExit("refusing to overwrite work directory")
    args.work.mkdir(parents=True)
    executable = args.executable.resolve()
    if not executable.is_file():
        raise SystemExit("producer executable not found")

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {
            pool.submit(run_one, executable, args.work, degree,
                        args.base_seed + degree, args.rounds,
                        args.initial_fives, args.max_new): degree
            for degree in range(18, 22)
        }
        branches = [future.result() for future in concurrent.futures.as_completed(futures)]
    branches.sort(key=lambda item: item["root_degree"])
    targets = sum(branch["physical_status"] == "GOOD_GRAPH" for branch in branches)
    report = {
        "status": "GOOD_GRAPH_FOUND" if targets else "INCOMPLETE_PORTFOLIO",
        "scope": "all four complete root-degree normalizations launched",
        "root_degrees": [18, 19, 20, 21],
        "targets": targets,
        "branches": branches,
    }
    output = json.dumps(report, indent=2, sort_keys=True) + "\n"
    (args.work / "summary.json").write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
