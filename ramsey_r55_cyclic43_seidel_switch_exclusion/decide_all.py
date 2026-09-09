#!/usr/bin/env python3
"""Decide every pinned Cyclic43 Seidel switching formula and check each result.

The worker formulas are independent.  An UNSAT result is accepted only after
DRAT-trim verifies the emitted proof and extracts a compact physical core and
trimmed proof.  A SAT result is accepted only after direct exhaustive K5
checking of the decoded 43-vertex graph.
"""
from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json
import os
import subprocess
import time

from generate import clauses_for_source, graph, sources, write_cnf


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return {"bytes": path.stat().st_size,
            "sha256": sha256(path.read_bytes()).hexdigest()}


def assignment_from_log(path):
    assignment = {}
    for line in path.read_text().splitlines():
        if not line.startswith("v "):
            continue
        for literal in map(int, line.split()[1:]):
            if literal == 0:
                continue
            need(1 <= abs(literal) <= 42, "model variable outside 1..42")
            need(abs(literal) not in assignment, "duplicate model variable")
            assignment[abs(literal)] = int(literal > 0)
    need(set(assignment) == set(range(1, 43)), "incomplete SAT model")
    return assignment


def verified_target(toggle_indices, assignment):
    base = graph(toggle_indices)
    spin = [0] + [assignment[v] for v in range(1, 43)]
    red = [[False] * 43 for _ in range(43)]
    red_edges = []
    for u, v in combinations(range(43), 2):
        value = bool(base[u][v] ^ spin[u] ^ spin[v])
        red[u][v] = red[v][u] = value
        if value:
            red_edges.append([u, v])
    bad = [0, 0]
    first_bad = [None, None]
    for vertices in combinations(range(43), 5):
        colors = {int(red[u][v]) for u, v in combinations(vertices, 2)}
        if len(colors) == 1:
            color = colors.pop()
            bad[color] += 1
            if first_bad[color] is None:
                first_bad[color] = list(vertices)
    need(bad == [0, 0], f"SAT model is not a good43 graph: {bad}, {first_bad}")
    return {"status": "DIRECTLY_VERIFIED_GOOD43", "vertices": 43,
            "red_edge_count": len(red_edges), "red_edges": red_edges,
            "red_K5": bad[1], "blue_K5": bad[0],
            "switch_bits_1_through_42": [assignment[v] for v in range(1, 43)]}


def run_process(command, log_path):
    start = time.monotonic()
    with log_path.open("x") as output:
        process = subprocess.run(command, stdout=output, stderr=subprocess.STDOUT,
                                 check=False)
    return process.returncode, time.monotonic() - start


def decide_one(index, toggle_indices, root, kissat, drat_trim):
    folder = root / f"source-{index:03d}"
    folder.mkdir()
    cnf = folder / "formula.cnf"
    raw_proof = folder / "proof.raw.drat"
    solver_log = folder / "solver.log"
    clauses, counts = clauses_for_source(toggle_indices)
    formula = write_cnf(cnf, clauses)
    solver_code, solver_seconds = run_process(
        [str(kissat), "--no-binary", "--no-factor", str(cnf), str(raw_proof)],
        solver_log)
    report = {"source_index": index, "toggle_indices": toggle_indices,
              "formula": formula, "formula_counts": counts,
              "solver_exit_code": solver_code,
              "solver_seconds": solver_seconds, "status": "NO_CONCLUSION"}
    solver_text = solver_log.read_text()
    if solver_code == 10:
        need("s SATISFIABLE" in solver_text, "exit 10 without SAT status")
        assignment = assignment_from_log(solver_log)
        target = verified_target(toggle_indices, assignment)
        target_path = folder / "good43.json"
        target_path.write_text(json.dumps(target, indent=2, sort_keys=True) + "\n")
        report["status"] = "DIRECTLY_VERIFIED_GOOD43"
        report["target"] = digest(target_path)
    elif solver_code == 20:
        need("s UNSATISFIABLE" in solver_text, "exit 20 without UNSAT status")
        core = folder / "core.cnf"
        trimmed = folder / "proof.trimmed.drat"
        proof_log = folder / "proof-check.log"
        proof_code, proof_seconds = run_process(
            [str(drat_trim), str(cnf), str(raw_proof),
             "-c", str(core), "-l", str(trimmed)], proof_log)
        need(proof_code == 0 and "s VERIFIED" in proof_log.read_text(),
             "DRAT-trim did not verify the UNSAT proof")
        report["status"] = "VERIFIED_UNSAT"
        report["proof_check_exit_code"] = proof_code
        report["proof_check_seconds"] = proof_seconds
        report["raw_proof"] = digest(raw_proof)
        report["core"] = digest(core)
        report["trimmed_proof"] = digest(trimmed)
    else:
        raise RuntimeError(f"source {index}: solver exit {solver_code}")
    report_path = folder / "result.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--kissat", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=min(8, os.cpu_count() or 1))
    args = parser.parse_args()
    need(args.jobs >= 1, "jobs must be positive")
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=True)
    need(not any(root.iterdir()), "output directory must be empty")
    kissat = args.kissat.resolve()
    drat_trim = args.drat_trim.resolve()
    need(kissat.is_file() and drat_trim.is_file(), "missing solver/checker binary")
    source_rows = sources()
    started = time.monotonic()
    reports = []
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(decide_one, index, row, root, kissat, drat_trim): index
                   for index, row in enumerate(source_rows)}
        for future in as_completed(futures):
            report = future.result()
            reports.append(report)
            print(json.dumps({"complete": len(reports),
                              "source_index": report["source_index"],
                              "status": report["status"],
                              "solver_seconds": report["solver_seconds"]}), flush=True)
    reports.sort(key=lambda row: row["source_index"])
    statuses = {}
    for report in reports:
        statuses[report["status"]] = statuses.get(report["status"], 0) + 1
    need(len(reports) == 238 and all(report["source_index"] == index
                                    for index, report in enumerate(reports)),
         "incomplete source census")
    need(set(statuses) <= {"VERIFIED_UNSAT", "DIRECTLY_VERIFIED_GOOD43"},
         "nonterminal result in census")
    census = {
        "status": ("DIRECTLY_VERIFIED_GOOD43" if statuses.get(
            "DIRECTLY_VERIFIED_GOOD43", 0) else
            "VERIFIED_COMPLETE_238_SOURCE_SWITCH_CLASS_EXCLUSION"),
        "source_count": len(reports), "status_counts": statuses,
        "jobs": args.jobs, "wall_seconds": time.monotonic() - started,
        "kissat": digest(kissat), "drat_trim": digest(drat_trim),
        "results": reports,
    }
    census_path = root / "census.json"
    census_path.write_text(json.dumps(census, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: census[key] for key in
                      ("status", "source_count", "status_counts", "wall_seconds")},
                     indent=2), flush=True)


if __name__ == "__main__":
    main()
