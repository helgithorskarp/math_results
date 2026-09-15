#!/usr/bin/env python3
"""Enumerate the host boundary relation with the reviewer's binary encoding."""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys
import time

from verify_review import (
    EXPECTED_BOUNDARY, EXPECTED_INPUT_HASHES, H, PERMS0, TARGET, binary_cnf, canonical,
    differs_literals, read_points, reconstruct, require,
)


def run_worker(args):
    from pysat.solvers import Solver

    for name in ("points.tsv", "host_relation.tsv"):
        actual = sha256((args.source / name).read_bytes()).hexdigest()
        require(actual == EXPECTED_INPUT_HASHES[name], f"frozen input hash: {name}")
    points = read_points(args.source / "points.tsv")
    _, host_edges, _, _, boundary = reconstruct(points)
    require(boundary == EXPECTED_BOUNDARY, "frozen boundary")
    clauses = binary_cnf(H, host_edges)
    position = {v: i for i, v in enumerate(H)}
    expected = {line.split("\t", 1)[0]
                for line in (args.source / "host_relation.tsv").read_text().splitlines()}
    require(len(expected) == 468, "468 frozen patterns")
    found = set()
    start = time.monotonic()
    status = "INCOMPLETE_PATTERN_LIMIT"
    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        while len(found) < args.max_patterns:
            if not solver.solve():
                status = "COMPLETE_SOLVER_UNSAT"
                break
            model = solver.get_model()
            require({abs(literal) for literal in model} >= set(range(1, 2 * len(H) + 1)),
                    "solver returned assignments for all binary variables")
            positive = {literal for literal in model if literal > 0}
            colours = {}
            for vertex in H:
                index = position[vertex]
                low_bit = 2 * index + 1
                colours[vertex] = (low_bit in positive) + 2 * ((low_bit + 1) in positive)
            pattern = tuple(colours[v] for v in boundary)
            representative = canonical(pattern)
            require(representative not in found, "no duplicate orbit")
            found.add(representative)
            for permutation in PERMS0:
                clause = []
                for vertex, colour in zip(boundary, representative):
                    if vertex == 0:
                        continue
                    clause.extend(differs_literals(position[vertex], permutation[colour]))
                solver.add_clause(clause)

    frozen = {tuple(map(int, row)) for row in expected}
    exact_match = found == frozen
    if status == "COMPLETE_SOLVER_UNSAT":
        require(exact_match, "enumerated relation equals frozen relation")
    canonical_text = "\n".join("".join(map(str, row)) for row in sorted(found)) + "\n"
    result = {
        "status": status,
        "solver": args.solver,
        "python_sat_version": importlib.metadata.version("python-sat"),
        "encoding": "two_bits_per_vertex_four_edge_clauses",
        "canonical_patterns": len(found),
        "frozen_patterns": len(frozen),
        "exact_set_match": exact_match,
        "enumerated_sorted_patterns_sha256": sha256(canonical_text.encode()).hexdigest(),
        "seconds": time.monotonic() - start,
    }
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=here.parent / TARGET)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--solver", default="glucose4")
    parser.add_argument("--seconds", type=int, default=300)
    parser.add_argument("--max-patterns", type=int, default=10000)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    args.source = args.source.resolve()
    args.out = args.out.resolve()
    require(args.seconds > 0 and args.max_patterns > 0, "positive finite limits")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.worker:
        run_worker(args)
        return
    command = [
        sys.executable, str(Path(__file__).resolve()), "--worker",
        "--source", str(args.source), "--out", str(args.out),
        "--solver", args.solver, "--max-patterns", str(args.max_patterns),
    ]
    try:
        subprocess.run(command, check=True, timeout=args.seconds)
    except subprocess.TimeoutExpired:
        args.out.write_text(json.dumps({
            "status": "INCOMPLETE_WALL_LIMIT",
            "solver": args.solver,
            "exact_set_match": False,
            "note": "No completeness claim is made for a timed-out run.",
        }, indent=2) + "\n")
        raise SystemExit(2)


if __name__ == "__main__":
    main()
