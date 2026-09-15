#!/usr/bin/env python3
"""Generate positive colouring witnesses for the Golomb direction ball."""

from __future__ import annotations

import argparse
import json
import subprocess
from itertools import combinations
from pathlib import Path

import verify as V


def variable(vertex, colour):
    return 4 * vertex + colour + 1


def base_cnf(n, edges, triangle):
    clauses = []
    for vertex in range(n):
        clauses.append([variable(vertex, colour) for colour in range(4)])
        clauses.extend([-variable(vertex, a), -variable(vertex, b)]
                       for a, b in combinations(range(4), 2))
    for u, v in edges:
        clauses.extend([-variable(u, colour), -variable(v, colour)]
                       for colour in range(4))
    clauses.extend([[variable(vertex, colour)]
                    for vertex, colour in zip(triangle, range(3))])
    return clauses


def solve(solver, n, edges, clauses, extra=()):
    all_clauses = clauses + list(extra)
    dimacs = [f"p cnf {4*n} {len(all_clauses)}"]
    dimacs.extend(" ".join(map(str, clause)) + " 0" for clause in all_clauses)
    run = subprocess.run([str(solver), "--quiet"], input="\n".join(dimacs) + "\n",
                         text=True, capture_output=True, check=False)
    if run.returncode == 20:
        return None
    if run.returncode != 10:
        raise RuntimeError(f"solver exit {run.returncode}: {run.stdout}\n{run.stderr}")
    positives = {
        int(token) for line in run.stdout.splitlines() if line.startswith("v ")
        for token in line.split()[1:] if token != "0" and int(token) > 0
    }
    word = "".join(str(next(colour for colour in range(4)
                            if variable(vertex, colour) in positives))
                   for vertex in range(n))
    if not V.proper(word, 4, n, edges):
        raise RuntimeError("solver returned an improper word")
    return word


def equality_clauses(u, v):
    return [[-variable(u, colour), variable(v, colour)] for colour in range(4)] + [
        [-variable(v, colour), variable(u, colour)] for colour in range(4)
    ]


def inequality_clauses(u, v):
    return [[-variable(u, colour), -variable(v, colour)] for colour in range(4)]


def positive_cover(solver, n, edges, clauses, pairs, relation):
    unresolved = set(pairs)
    words = []
    condition = equality_clauses if relation == "equal" else inequality_clauses
    while unresolved:
        trigger = min(unresolved)
        word = solve(solver, n, edges, clauses, condition(*trigger))
        if word is None:
            raise RuntimeError(f"found forced relation opposite to {relation}: {trigger}")
        words.append(word)
        if relation == "equal":
            covered = {pair for pair in unresolved if word[pair[0]] == word[pair[1]]}
        else:
            covered = {pair for pair in unresolved if word[pair[0]] != word[pair[1]]}
        if trigger not in covered:
            raise RuntimeError("trigger pair not covered")
        unresolved -= covered
    return words


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    source, source_edges, _, points, edges, terminals = V.construction()
    n = len(points)
    clauses = base_cnf(n, edges, terminals[:3])
    source_extensions = []
    for pattern in V.source_patterns(source_edges):
        extra = [[variable(vertex, int(colour))]
                 for vertex, colour in zip(terminals, pattern)]
        word = solve(args.solver, n, edges, clauses, extra)
        if word is None:
            raise RuntimeError(f"Golomb pattern did not extend: {pattern}")
        source_extensions.append({"pattern": pattern, "word": word})
    edge_set = set(edges)
    nonedges = [pair for pair in combinations(range(n), 2) if pair not in edge_set]
    certificate = {
        "schema": "golomb-direction-ball-neutrality-v1",
        "source_extensions": source_extensions,
        "equal_cover_words": positive_cover(
            args.solver, n, edges, clauses, nonedges, "equal"),
        "separating_cover_words": positive_cover(
            args.solver, n, edges, clauses, nonedges, "different"),
    }
    args.output.write_text(json.dumps(certificate, sort_keys=True,
                                      separators=(",", ":")) + "\n")
    print(json.dumps(V.verify(certificate), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
