#!/usr/bin/env python3
"""One bounded solver invocation; check a proof or directly verify a SAT graph."""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import resource
import subprocess
import time


def require(test, message):
    if not test:
        raise ValueError(message)


def run(command, log, timeout):
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    start = time.monotonic()
    with log.open("w") as output:
        process = subprocess.Popen(command, stdout=output, stderr=subprocess.STDOUT)
        expired = False
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            expired = True
            process.terminate()
            try:
                code = process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                process.kill()
                code = process.wait()
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    return {"command": list(map(str, command)), "exit_code": code,
            "wall_timeout": expired, "wall_seconds": time.monotonic() - start,
            "user_seconds": after.ru_utime - before.ru_utime,
            "system_seconds": after.ru_stime - before.ru_stime,
            "children_max_rss_KiB": after.ru_maxrss}


def sat_graph(log):
    assignment = {}
    for line in log.read_text().splitlines():
        if line.startswith("v "):
            for literal in map(int, line.split()[1:]):
                if not literal:
                    continue
                require(1 <= abs(literal) <= 123, "Model variable out of range")
                require(abs(literal) not in assignment, "Repeated model variable")
                assignment[abs(literal)] = int(literal > 0)
    require(set(assignment) == set(range(1, 124)), "Incomplete SAT assignment")
    spin = {0: 0, **{v: assignment[v] for v in range(1, 41)}}
    red = {}
    external = 41
    for u, v in combinations(range(43), 2):
        if v < 41:
            red[u, v] = int(pow((u - v) % 41, 20, 41) == 1) ^ spin[u] ^ spin[v]
        else:
            red[u, v] = assignment[external]
            external += 1
    bad = [0, 0]
    for vertices in combinations(range(43), 5):
        colors = {red[pair] for pair in combinations(vertices, 2)}
        if len(colors) == 1:
            bad[colors.pop()] += 1
    require(bad == [0, 0], f"Decoded model has monochromatic K5s: {bad}")
    return {"vertices": 43, "red_edges": [list(pair) for pair, bit in red.items() if bit],
            "blue_K5": bad[0], "red_K5": bad[1], "assignment": assignment}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--kissat", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    args = parser.parse_args()
    folder = args.run_dir.resolve()
    require((folder / "family.cnf").exists(), "Missing generated family.cnf")
    require(not (folder / "solver.log").exists(), "Refusing to overwrite previous solver run")
    formula_hash = sha256((folder / "family.cnf").read_bytes()).hexdigest()
    checked = json.loads((folder / "verification.json").read_text())
    require(checked["status"] == "VERIFIED_EXACT_FULL_FAMILY_CNF" and
            checked["cnf_sha256"] == formula_hash, "Formula must be audited before solving")
    report = {"cnf_sha256": formula_hash, "status": "NOT_STARTED",
              "kissat_sha256": sha256(args.kissat.read_bytes()).hexdigest(),
              "drat_trim_sha256": sha256(args.drat_trim.read_bytes()).hexdigest()}
    report["solver"] = run([str(args.kissat.resolve()), "--time=300", "--no-binary",
                            str(folder / "family.cnf"), str(folder / "proof.drat")],
                           folder / "solver.log", 330)
    code = report["solver"]["exit_code"]
    if report["solver"]["wall_timeout"] or code not in (10, 20):
        report["status"] = "NO_CONCLUSION"
    elif code == 10:
        graph = sat_graph(folder / "solver.log")
        (folder / "target.json").write_text(json.dumps(graph, indent=2) + "\n")
        report["status"] = "DIRECTLY_VERIFIED_TARGET"
    else:
        require("s UNSATISFIABLE" in (folder / "solver.log").read_text(), "No UNSAT status")
        report["status"] = "UNSAT_UNCHECKED"
        (folder / "decision.json").write_text(json.dumps(report, indent=2) + "\n")
        report["proof_check"] = run(
            [str(args.drat_trim.resolve()), str(folder / "family.cnf"), str(folder / "proof.drat"),
             "-c", str(folder / "core.cnf"), "-l", str(folder / "trimmed.drat")],
            folder / "proof_check.log", 330)
        require(report["proof_check"]["exit_code"] == 0 and
                "s VERIFIED" in (folder / "proof_check.log").read_text(), "Proof not verified")
        report["status"] = "CHECKED_WHOLE_FAMILY_EXCLUSION"
    report["files"] = {p.name: {"bytes": p.stat().st_size,
                                 "sha256": sha256(p.read_bytes()).hexdigest()}
                       for p in sorted(folder.iterdir()) if p.is_file() and p.name != "decision.json"}
    (folder / "decision.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
