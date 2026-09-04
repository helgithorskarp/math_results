#!/usr/bin/env python3
"""Generate explicit 4-colourings of U-v for every colourable deletion."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from pysat.solvers import Solver

from verify import build_union, edge_digest


K = 4


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--solver", default="cadical195")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    points_path = here.parent / "hadwiger_nelson_parts509_completion_census_degree9" / "points.tsv"
    points, edges, placements, _ = build_union(points_path)
    n = len(points)

    def color_var(vertex: int, color: int) -> int:
        return K * vertex + color + 1

    def active_var(vertex: int) -> int:
        return K * n + vertex + 1

    clauses = [[-active_var(v), *[color_var(v, c) for c in range(K)]] for v in range(n)]
    for u, v in edges:
        for color in range(K):
            clauses.append([-active_var(u), -active_var(v), -color_var(u, color), -color_var(v, color)])
    anchors = (0, 149, 152)
    edge_set = set(edges)
    if not all(tuple(sorted(edge)) in edge_set for edge in ((0, 149), (0, 152), (149, 152))):
        raise AssertionError("colour-symmetry anchor is not a triangle")
    for color, vertex in enumerate(anchors):
        clauses.append([color_var(vertex, color)])

    results: dict[int, dict] = {}
    if args.output.exists():
        previous = json.loads(args.output.read_text(encoding="utf-8"))
        if previous.get("union_edge_sha256") != edge_digest(edges):
            raise ValueError("checkpoint is for a different graph")
        results = {int(key): value for key, value in previous["results"].items()}

    # A vertex exclusive to one placement can be deleted while leaving the
    # other certified 509-vertex placement intact, so U-v is non-4-colourable.
    placement_sets = [set(labels) for labels in placements.values()]
    for deleted in range(n):
        if deleted not in results and any(deleted not in placement for placement in placement_sets):
            results[deleted] = {"status": "UNSAT", "seconds": 0.0, "witness": None, "inferred": True}

    def save() -> None:
        forced = sorted(v for v, row in results.items() if row["status"] == "SAT")
        unforced = sorted(v for v, row in results.items() if row["status"] == "UNSAT")
        payload = {
            "format": "parts509-exceptional-rotation-triple-forced-v1",
            "union_edge_sha256": edge_digest(edges),
            "events": [108, 109, 789],
            "vertices": n,
            "forced": forced,
            "unforced": unforced,
            "results": {str(v): row for v, row in sorted(results.items())},
        }
        temporary = args.output.with_suffix(args.output.suffix + ".tmp")
        temporary.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
        temporary.replace(args.output)

    todo = [v for v in range(n) if v not in results]
    started = time.monotonic()
    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        for done, deleted in enumerate(todo, 1):
            assumptions = [active_var(v) if v != deleted else -active_var(v) for v in range(n)]
            task_started = time.monotonic()
            satisfiable = solver.solve(assumptions=assumptions)
            elapsed = time.monotonic() - task_started
            witness = None
            if satisfiable:
                model = {literal for literal in solver.get_model() if literal > 0}
                colors = {
                    v: next(color for color in range(K) if color_var(v, color) in model)
                    for v in range(n) if v != deleted
                }
                if any(colors[u] == colors[v] for u, v in edges if deleted not in (u, v)):
                    raise AssertionError("solver returned an invalid colouring")
                witness = "".join(str(colors[v]) for v in range(n) if v != deleted)
            results[deleted] = {
                "status": "SAT" if satisfiable else "UNSAT",
                "seconds": elapsed,
                "witness": witness,
                "inferred": False,
            }
            print(
                f"done={done}/{len(todo)} vertex={deleted} status={results[deleted]['status']} "
                f"task_seconds={elapsed:.3f} wall_seconds={time.monotonic()-started:.1f}",
                flush=True,
            )
            if done % 10 == 0:
                save()
    save()
    print(f"forced={len([r for r in results.values() if r['status'] == 'SAT'])} "
          f"unforced={len([r for r in results.values() if r['status'] == 'UNSAT'])}")


if __name__ == "__main__":
    main()
