#!/usr/bin/env python3
"""Regenerate the 509 positive deletion-coloring witnesses with PySAT."""

from __future__ import annotations

import argparse
import json
import time
from fractions import Fraction
from pathlib import Path

from pysat.solvers import Solver

from verify import BASE_SIZE, BRIDGE_COORDINATES, TOTAL_SIZE, build_edges, check_coloring, edge_digest, read_points


K = 4


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--solver", default="cadical195")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    points_path = here.parent / "hadwiger_nelson_parts509_completion_census_degree9" / "points.tsv"
    points = read_points(points_path)
    points.extend(tuple(tuple(coordinate) for coordinate in point) for point in BRIDGE_COORDINATES)
    edges = build_edges(points)

    def color_var(vertex: int, color: int) -> int:
        return K * vertex + color + 1

    def active_var(vertex: int) -> int:
        return K * TOTAL_SIZE + vertex + 1

    clauses = [[-active_var(v), *[color_var(v, color) for color in range(K)]] for v in range(TOTAL_SIZE)]
    for u, v in edges:
        for color in range(K):
            clauses.append([-active_var(u), -active_var(v), -color_var(u, color), -color_var(v, color)])
    for color, vertex in enumerate((0, 149, 152)):
        clauses.append([color_var(vertex, color)])

    witnesses = []
    started = time.monotonic()
    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        for deleted in range(BASE_SIZE):
            assumptions = [active_var(vertex) if vertex != deleted else -active_var(vertex) for vertex in range(TOTAL_SIZE)]
            if not solver.solve(assumptions=assumptions):
                raise AssertionError(f"deletion {deleted} is unexpectedly non-colourable")
            model = {literal for literal in solver.get_model() if literal > 0}
            colors = {
                vertex: next(color for color in range(K) if color_var(vertex, color) in model)
                for vertex in range(TOTAL_SIZE) if vertex != deleted
            }
            check_coloring(colors, edges)
            witnesses.append("".join(str(colors[vertex]) for vertex in range(TOTAL_SIZE) if vertex != deleted))
            if (deleted + 1) % 25 == 0 or deleted + 1 == BASE_SIZE:
                print(f"done={deleted+1}/{BASE_SIZE} wall_seconds={time.monotonic()-started:.1f}", flush=True)

    bridge_rows = []
    for point in BRIDGE_COORDINATES:
        bridge_rows.append({
            "candidate": [[str(Fraction(value, 96)) for value in coordinate] for coordinate in point]
        })
    payload = {
        "format": "parts509-six-bridge-deletion-witnesses-v1",
        "vertices": TOTAL_SIZE,
        "edges": len(edges),
        "edge_sha256": edge_digest(edges),
        "base_vertices": BASE_SIZE,
        "bridge_rows": bridge_rows,
        "witnesses": witnesses,
    }
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
    temporary.replace(args.output)


if __name__ == "__main__":
    main()
