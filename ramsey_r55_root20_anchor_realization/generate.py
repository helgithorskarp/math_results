#!/usr/bin/env python3
"""Optional SAT discovery of the marked 20-vertex witness; verification is solver-free."""
import argparse
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import resource
import subprocess
import time

ROOT = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def parent():
    path = ROOT.parent / "ramsey_r55_triple_graph_realization/generate.py"
    require(hashlib.sha256(path.read_bytes()).hexdigest() ==
            "0cf0264142d89472cb93358bc8f4ecf33d13b8996aba03672dd401133257e898", "parent changed")
    spec = importlib.util.spec_from_file_location("parent", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fixed_edges():
    return {(0, 1): True, **{(u, v): (u == 0 and 10 <= v < 16) or (u == 1 and 16 <= v < 20)
                            for u in (0, 1) for v in range(2, 20)}}


def add_lex(enc, left, right):
    same = True
    for a, b in zip(left, right):
        enc.add(enc.neg(same), -a, b)
        enc.variables += 1
        nxt = enc.variables
        enc.add(-nxt, same)
        enc.add(-nxt, -a, b)
        enc.add(-nxt, a, -b)
        enc.add(enc.neg(same), a, b, nxt)
        enc.add(enc.neg(same), -a, -b, nxt)
        same = nxt


def build():
    edges = tuple(combinations(range(2, 20), 2))
    index = {e: i + 1 for i, e in enumerate(edges)}
    fixed = fixed_edges()
    clauses = set()
    for red, size in ((True, 4), (False, 5)):
        for subset in combinations(range(20), size):
            if any(fixed[e] != red for e in combinations(subset, 2) if e in fixed):
                continue
            clauses.add(tuple(sorted((-1 if red else 1) * index[e] for e in combinations(subset, 2) if e in index)))
    enc = parent().CounterEncoder(153, sorted(clauses, key=lambda row: (len(row), row)))
    enc.interval(range(1, 154), 81, 81)
    for cell in (range(2, 10), range(10, 16), range(16, 20)):
        for a, b in zip(cell, list(cell)[1:]):
            other = [v for v in range(2, 20) if v not in (a, b)]
            add_lex(enc, [index[tuple(sorted((a, v)))] for v in other],
                    [index[tuple(sorted((b, v)))] for v in other])
    return edges, enc, len(clauses)


def check_graph(doc):
    require(set(doc) == {"n", "red_edges"} and doc["n"] == 20, "graph format")
    red = {tuple(e) for e in doc["red_edges"]}
    require(len(red) == 92 and len(red) == len(doc["red_edges"]), "red edge count")
    require(all(type(u) is int and type(v) is int and 0 <= u < v < 20 for u, v in red), "edge endpoints")
    require(all((e in red) == c for e, c in fixed_edges().items()), "fixed incidence pattern")
    bad = {}
    for color, size in ((True, 4), (False, 5)):
        bad[str((color, size))] = [list(s) for s in combinations(range(20), size)
                                 if all((e in red) == color for e in combinations(s, 2))]
    require(not any(bad.values()), "forbidden local clique")
    return {"status": "DIRECT_LOCAL_GRAPH_VERIFIED", "n": 20, "red_edges": len(red),
            "degrees": [sum(v in e for e in red) for v in range(20)],
            "red_k4": 0, "blue_k5": 0, "scope": "One local neighborhood only; not a 43-vertex target"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--work", type=Path, required=True)
    p.add_argument("--seconds", type=int, default=120)
    p.add_argument("--kissat", type=Path)
    p.add_argument("--emit-only", action="store_true")
    args = p.parse_args()
    require(args.seconds > 0, "positive solver bound")
    args.work.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    edges, enc, base_count = build()
    cnf = args.work / "case.cnf"
    with cnf.open("w") as out:
        out.write(f"p cnf {enc.variables} {len(enc.clauses)}\n")
        for row in enc.clauses:
            out.write(" ".join(map(str, row)) + " 0\n")
    report = {"status": "EMITTED" if args.emit_only else "RUNNING", "seconds": args.seconds, "primary_variables": len(edges),
              "variables": enc.variables, "clauses": len(enc.clauses), "primary_clauses": base_count,
              "formula_sha256": hashlib.sha256(cnf.read_bytes()).hexdigest(),
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (args.work / "result.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True), flush=True)
    if args.emit_only:
        return
    require(args.kissat is not None, "--kissat is required for discovery")
    log = args.work / "solver.log"
    kissat = args.kissat
    with log.open("w") as out:
        try:
            run = subprocess.run([str(kissat), f"--time={args.seconds}", str(cnf), str(args.work / "proof.drat")],
                                 stdout=out, stderr=subprocess.STDOUT, timeout=args.seconds + 30)
            code = run.returncode
        except subprocess.TimeoutExpired:
            code = None
    report.update(status={10: "SAT_UNCHECKED", 20: "UNSAT_UNCHECKED", 0: "UNKNOWN"}.get(code, "ERROR"),
                  solver_exit=code, elapsed_seconds=round(time.monotonic() - start, 6),
                  peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                  solver_binary_sha256=hashlib.sha256(kissat.read_bytes()).hexdigest())
    if code == 10:
        assignment = {}
        for line in log.read_text().splitlines():
            if line.startswith("v "):
                for word in line.split()[1:]:
                    lit = int(word)
                    if lit:
                        require(abs(lit) not in assignment or assignment[abs(lit)] == (lit > 0), "model inconsistency")
                        assignment[abs(lit)] = lit > 0
        require(set(range(1, enc.variables + 1)) <= assignment.keys(), "incomplete model")
        require(all(any(assignment[abs(lit)] == (lit > 0) for lit in row) for row in enc.clauses), "model failure")
        red = {e for e, color in fixed_edges().items() if color}
        red.update(e for i, e in enumerate(edges, 1) if assignment[i])
        doc = {"n": 20, "red_edges": [list(e) for e in sorted(red)]}
        report["graph_check"] = check_graph(doc)
        report["status"] = "SAT_GRAPH_VERIFIED"
        (args.work / "graph.json").write_text(json.dumps(doc, indent=2) + "\n")
    (args.work / "result.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
