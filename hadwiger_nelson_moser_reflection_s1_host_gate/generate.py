#!/usr/bin/env python3
"""Generate the compact positive relation witnesses with a DIMACS solver."""
from argparse import ArgumentParser
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess

from verify import COMMON, SOURCE, TARGET, build, embeddings, proper


def solve(solver, n, graph_edges, pins):
    clauses = []
    for v in range(n):
        variables = [4*v+c+1 for c in range(4)]
        clauses.append(variables)
        clauses.extend([-variables[a], -variables[b]] for a, b in combinations(range(4), 2))
    clauses.extend([-4*a-c-1, -4*b-c-1] for a, b in graph_edges for c in range(4))
    clauses.extend([4*v+int(c)+1] for v, c in zip(pins, COMMON))
    text = f"p cnf {4*n} {len(clauses)}\n"
    text += "".join(" ".join(map(str, row)) + " 0\n" for row in clauses)
    run = subprocess.run([str(solver)], input=text, text=True, capture_output=True)
    if run.returncode != 10 or "s SATISFIABLE" not in run.stdout:
        raise RuntimeError("solver did not return SAT: " + run.stderr[-1000:])
    positive = {int(x) for line in run.stdout.splitlines() if line.startswith("v ")
                for x in line[2:].split() if int(x) > 0}
    colours = tuple(next(c for c in range(4) if 4*v+c+1 in positive) for v in range(n))
    if not proper(colours, graph_edges):
        raise ValueError("decoded word is not proper")
    return "".join(map(str, colours))


def main():
    parser = ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw, s0, s1, _, e1 = build()
    found = embeddings(s0, TARGET, s1)
    result = {
        "schema": "hn-moser-reflection-s1-host-gate-v1",
        "source_sha256": sha256(raw).hexdigest(),
        "target_terminals": list(TARGET),
        "excluded_pattern": "00112",
        "common_pattern": COMMON,
        "blocker_word": solve(args.solver, len(s1), e1, TARGET),
        "host_witnesses": [
            {"embedding": list(ids), "word": solve(args.solver, len(s1), e1, ids)}
            for ids in found
        ],
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
