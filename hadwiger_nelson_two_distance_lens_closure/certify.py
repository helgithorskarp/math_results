#!/usr/bin/env python3
"""Generate positive colouring witnesses using a DIMACS solver."""
from argparse import ArgumentParser
import json
from pathlib import Path
import subprocess

from verify import build_graph, cnf_text, proper


def solve(solver, n, edges, units=()):
    run = subprocess.run([str(solver)], input=cnf_text(n, edges, 4, units),
                         text=True, capture_output=True)
    if run.returncode != 10 or "s SATISFIABLE" not in run.stdout:
        raise RuntimeError("solver did not return SAT: " + run.stderr[-1000:])
    literals = [int(x) for line in run.stdout.splitlines() if line.startswith("v ")
                for x in line[2:].split() if x != "0"]
    positive = {x for x in literals if x > 0}
    colours = tuple(next(c for c in range(4) if 4*v+c+1 in positive) for v in range(n))
    if not proper(colours, edges):
        raise ValueError("decoded solver word is not proper")
    return "".join(map(str, colours))


def main():
    parser = ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    points, edges, source_ids, long_edges, _ = build_graph()
    n = len(points)
    result = {"four_colouring": solve(args.solver, n, edges, (1,)),
              "long_pair_equal_four_colourings": []}
    for pair in long_edges:
        a, b = (source_ids[x] for x in pair)
        result["long_pair_equal_four_colourings"].append({
            "pair": list(pair),
            "word": solve(args.solver, n, edges, (4*a+1, 4*b+1)),
        })
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
