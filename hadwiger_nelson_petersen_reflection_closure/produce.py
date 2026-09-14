#!/usr/bin/env python3
"""Generate the compact positive terminal-relation certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pysat.solvers import Cadical195

import model


def colour_cnf(n, edges, k):
    clauses = []
    var = lambda v, c: v * k + c + 1
    for v in range(n):
        clauses.append([var(v, c) for c in range(k)])
        for a in range(k):
            for b in range(a + 1, k):
                clauses.append([-var(v, a), -var(v, b)])
    for u, v in edges:
        for c in range(k):
            clauses.append([-var(u, c), -var(v, c)])
    return clauses, var


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=Path("certificate.json"))
    args = ap.parse_args()

    base = model.petersen_points()
    points = sorted(set(base))
    rounds = []
    for round_index in range(3):
        nxt, edges, wedges = model.reflect_round(points)
        rounds.append(
            {
                "round": round_index,
                "vertices": len(points),
                "edges": len(edges),
                "wedges": wedges,
                "next_vertices": len(nxt),
            }
        )
        if round_index < 2:
            points = nxt
    edges = model.strict_edges(points)
    index = {p: i for i, p in enumerate(points)}
    terminals = [index[p] for p in base]
    terminal_index = {v: i for i, v in enumerate(terminals)}
    terminal_edges = sorted(
        (min(terminal_index[u], terminal_index[v]), max(terminal_index[u], terminal_index[v]))
        for u, v in edges
        if u in terminal_index and v in terminal_index
    )

    clauses, var = colour_cnf(len(points), edges, 4)
    witnesses = []
    with Cadical195(bootstrap_with=clauses) as solver:
        for pattern in model.restricted_growth_partitions(10, 4):
            if any(pattern[u] == pattern[v] for u, v in terminal_edges):
                continue
            assumptions = [var(terminals[i], pattern[i]) for i in range(10)]
            if not solver.solve(assumptions=assumptions):
                raise RuntimeError(f"unexpected forbidden terminal pattern {pattern}")
            positive = set(lit for lit in solver.get_model() if lit > 0)
            word = []
            for v in range(len(points)):
                colours = [c for c in range(4) if var(v, c) in positive]
                if len(colours) != 1:
                    raise RuntimeError("nonfunctional model")
                word.append(colours[0])
            if any(word[u] == word[v] for u, v in edges):
                raise RuntimeError("improper model")
            witnesses.append(["".join(map(str, pattern)), "".join(map(str, word))])

    certificate = {
        "schema": "hn-petersen-reflection-v1",
        "base_points": [model.point_word(p) for p in base],
        "rounds": rounds,
        "terminals": terminals,
        "terminal_edges": [list(e) for e in terminal_edges],
        "witnesses": witnesses,
        "point_hash": model.stream_hash([model.point_word(p) for p in points]),
        "edge_hash": model.stream_hash([list(e) for e in edges]),
    }
    args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "vertices": len(points),
        "edges": len(edges),
        "next_vertices": rounds[-1]["next_vertices"],
        "terminal_patterns": len(witnesses),
        "point_hash": certificate["point_hash"],
        "edge_hash": certificate["edge_hash"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
