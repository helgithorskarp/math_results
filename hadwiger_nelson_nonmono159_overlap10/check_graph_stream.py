#!/usr/bin/env python3
"""Solve and directly verify four-colorings for exact emitted graph rows."""

import argparse
import multiprocessing as mp
import sys
from pathlib import Path

from pysat.solvers import Cadical195


def parse_graph(line: str):
    prefix, encoded_edges = line.rstrip("\n").split(";edge_list=", 1)
    fields = dict(item.split("=", 1) for item in prefix.split(";"))
    edges = tuple(tuple(map(int, edge.split("-"))) for edge in encoded_edges.split(",") if edge)
    identifier = fields.get("graph", fields.get("triple"))
    if identifier is None:
        raise RuntimeError("missing graph/triple identifier")
    return int(identifier), int(fields["order"]), int(fields["edges"]), edges


def solve_graph(task):
    graph, order, reported_edges, edges = task
    if len(edges) != reported_edges:
        raise RuntimeError(f"graph {graph}: edge-count mismatch")

    def variable(vertex, color):
        return 4 * vertex + color + 1

    clauses = []
    for vertex in range(order):
        clauses.append([variable(vertex, color) for color in range(4)])
        for color in range(4):
            for earlier in range(color):
                clauses.append([-variable(vertex, color), -variable(vertex, earlier)])
    for u, v in edges:
        for color in range(4):
            clauses.append([-variable(u, color), -variable(v, color)])
    clauses.append([variable(0, 0)])

    with Cadical195(bootstrap_with=clauses) as solver:
        if not solver.solve():
            return graph, order, reported_edges, None
        positive = {literal for literal in solver.get_model() if literal > 0}
    coloring = tuple(
        next(color for color in range(4) if variable(vertex, color) in positive)
        for vertex in range(order)
    )
    if coloring[0] != 0 or any(coloring[u] == coloring[v] for u, v in edges):
        raise RuntimeError(f"graph {graph}: invalid SAT witness")
    return graph, order, reported_edges, coloring


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("graphs", type=Path)
    parser.add_argument("--jobs", type=int, default=1)
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    tasks = [
        parse_graph(line)
        for line in args.graphs.open()
        if line.startswith(("graph=", "triple="))
    ]
    results = []
    with mp.Pool(args.jobs) as pool:
        for count, result in enumerate(pool.imap_unordered(solve_graph, tasks, chunksize=8), 1):
            results.append(result)
            if count % 500 == 0:
                print(f"checked={count}/{len(tasks)}", file=sys.stderr, flush=True)
    results.sort()
    unsat = [graph for graph, _, _, coloring in results if coloring is None]
    print(f"graphs={len(results)}")
    print(f"unsat={len(unsat)}")
    for graph, order, edges, coloring in results:
        if coloring is None:
            print(f"graph={graph};order={order};edges={edges};status=UNSAT")
        else:
            print(
                f"graph={graph};order={order};edges={edges};status=SAT;colors="
                + "".join(map(str, coloring))
            )
    print("direct_witness_verification=true")


if __name__ == "__main__":
    main()
