#!/usr/bin/env python3
"""Enumerate the Parts136 host relation with the reviewer's binary encoding."""

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
    EXPECTED_BOUNDARY, EXPECTED_INPUT_HASHES, EXPECTED_PATTERN_HASH, H, PERMS0,
    TARGET, binary_cnf, canonical, differs_literals, read_points, reconstruct,
    require,
)


def run_worker(args):
    from pysat.solvers import Solver

    for name in ("points.tsv", "fixtures.json"):
        require(sha256((args.source / name).read_bytes()).hexdigest()
                == EXPECTED_INPUT_HASHES[name], f"frozen source hash: {name}")
    points = read_points(args.source / "points.tsv")
    _, host_edges, _, _, boundary = reconstruct(points)
    require(boundary == EXPECTED_BOUNDARY, "frozen physical boundary")
    clauses = binary_cnf(H, host_edges)
    position = {vertex: index for index, vertex in enumerate(H)}
    found = {}
    start = time.monotonic()
    status = "INCOMPLETE_PATTERN_LIMIT"
    journal = args.out / "host_relation.partial.tsv"
    require(not journal.exists(), "use a fresh output directory")
    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        with journal.open("w", buffering=1) as stream:
            while len(found) < args.max_patterns:
                if not solver.solve():
                    status = "COMPLETE_SOLVER_UNSAT"
                    break
                model = solver.get_model()
                require({abs(lit) for lit in model} >= set(range(1, 2 * len(H) + 1)),
                        "solver assigned every binary variable")
                positive = {lit for lit in model if lit > 0}
                colours = {}
                for vertex in H:
                    low = 2 * position[vertex] + 1
                    colours[vertex] = (low in positive) + 2 * ((low + 1) in positive)
                raw_pattern = tuple(colours[v] for v in boundary)
                representative = canonical(raw_pattern)
                normalizer = next(p for p in PERMS0
                                  if tuple(p[c] for c in raw_pattern) == representative)
                require(representative not in found, "no duplicate orbit")
                word = "".join(str(normalizer[colours[v]]) for v in H)
                pattern_text = "".join(map(str, representative))
                found[representative] = word
                stream.write(pattern_text + "\t" + word + "\n")
                for permutation in PERMS0:
                    clause = []
                    for vertex, colour in zip(boundary, representative):
                        if vertex == 0:
                            continue
                        clause.extend(differs_literals(position[vertex],
                                                       permutation[colour]))
                    solver.add_clause(clause)
                if len(found) % 1000 == 0:
                    print(json.dumps({"patterns": len(found),
                                      "seconds": time.monotonic() - start}), flush=True)

    rows = sorted(found.items())
    canonical_text = "".join("".join(map(str, pattern)) + "\n"
                             for pattern, _ in rows)
    pattern_hash = sha256(canonical_text.encode()).hexdigest()
    exact_match = len(rows) == 41025 and pattern_hash == EXPECTED_PATTERN_HASH
    if status == "COMPLETE_SOLVER_UNSAT":
        require(exact_match, "complete enumeration matches frozen pattern set")
        final = args.out / "host_relation.tsv"
        final.write_text("".join("".join(map(str, pattern)) + "\t" + word + "\n"
                                 for pattern, word in rows))
    result = {
        "status": status,
        "solver": args.solver,
        "python_sat_version": importlib.metadata.version("python-sat"),
        "encoding": "two_bits_per_vertex_four_edge_clauses",
        "canonical_patterns": len(rows),
        "target_pattern_hash": EXPECTED_PATTERN_HASH,
        "enumerated_sorted_patterns_sha256": pattern_hash,
        "exact_target_set_match": exact_match,
        "elapsed_seconds": time.monotonic() - start,
    }
    (args.out / "enumeration.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=here.parent / TARGET)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--solver", default="glucose4")
    parser.add_argument("--seconds", type=int, default=900)
    parser.add_argument("--max-patterns", type=int, default=100000)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    args.source = args.source.resolve()
    args.out = args.out.resolve()
    require(args.seconds > 0 and args.max_patterns > 0, "positive finite limits")
    args.out.mkdir(parents=True, exist_ok=True)
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
        (args.out / "enumeration.json").write_text(json.dumps({
            "status": "INCOMPLETE_WALL_LIMIT",
            "solver": args.solver,
            "exact_target_set_match": False,
            "note": "Partial rows are preserved; no completeness claim is made.",
        }, indent=2) + "\n")
        raise SystemExit(2)


if __name__ == "__main__":
    main()
