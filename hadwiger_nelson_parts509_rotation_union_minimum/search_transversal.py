#!/usr/bin/env python3
"""Implicit hitting-set search for a <=508-vertex induced subgraph of U."""

from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path

from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
from pysat.solvers import Solver

from verify import build_union, edge_digest


K = 4


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("forced_checkpoint", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--layers", type=int, default=1)
    parser.add_argument("--improve", type=int, default=0)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--max-rounds", type=int, default=1_000_000)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    points_path = here.parent / "hadwiger_nelson_parts509_completion_census_degree9" / "points.tsv"
    points, edges, _, _ = build_union(points_path)
    n = len(points)
    graph_digest = edge_digest(edges)
    forced_data = json.loads(args.forced_checkpoint.read_text(encoding="utf-8"))
    if forced_data["union_edge_sha256"] != graph_digest:
        raise ValueError("forced checkpoint is for a different graph")
    forced = set(forced_data["forced"])
    free = sorted(set(range(n)) - forced)
    free_index = {vertex: index for index, vertex in enumerate(free)}
    target_free = 508 - len(forced)
    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    rng = random.Random(args.seed)

    def color_var(vertex: int, color: int) -> int:
        return K * vertex + color + 1

    def active_var(vertex: int) -> int:
        return K * n + vertex + 1

    clauses = [[-active_var(v), *[color_var(v, c) for c in range(K)]] for v in range(n)]
    for u, v in edges:
        for color in range(K):
            clauses.append([-active_var(u), -active_var(v), -color_var(u, color), -color_var(v, color)])
    anchors = (0, 149, 152)
    if not set(anchors) <= forced:
        raise AssertionError("colour-symmetry anchors are not forced")
    for color, vertex in enumerate(anchors):
        clauses.append([color_var(vertex, color)])

    family: list[dict] = []
    history: list[dict] = []
    seen: set[frozenset[int]] = set()
    if args.output.exists():
        previous = json.loads(args.output.read_text(encoding="utf-8"))
        if previous.get("union_edge_sha256") != graph_digest:
            raise ValueError("checkpoint is for a different graph")
        for row in previous.get("family", []):
            deleted = frozenset(row["D"])
            if deleted and deleted <= set(free) and deleted not in seen:
                seen.add(deleted)
                family.append(row)
        history = previous.get("history", [])

    sat_calls = 0
    sat_seconds = 0.0

    def save(status: str) -> None:
        payload = {
            "format": "parts509-exceptional-rotation-union-ihs-v1",
            "union_edge_sha256": graph_digest,
            "events": [108, 789],
            "forced": sorted(forced),
            "free": free,
            "target_order": 508,
            "family": family,
            "history": history,
            "records": [],
            "status": status,
            "sat_calls": sat_calls,
            "sat_seconds": sat_seconds,
            "anchors": anchors,
        }
        temporary = args.output.with_suffix(args.output.suffix + ".tmp")
        temporary.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
        temporary.replace(args.output)

    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
        def colorable(active: set[int]) -> dict[int, int] | None:
            nonlocal sat_calls, sat_seconds
            assumptions = [active_var(v) if v in active else -active_var(v) for v in range(n)]
            started = time.monotonic()
            satisfiable = solver.solve(assumptions=assumptions)
            sat_calls += 1
            sat_seconds += time.monotonic() - started
            if not satisfiable:
                return None
            model = {literal for literal in solver.get_model() if literal > 0}
            colors = {
                v: next(color for color in range(K) if color_var(v, color) in model)
                for v in active
            }
            if any(colors[u] == colors[v] for u, v in edges if u in active and v in active):
                raise AssertionError("solver returned an invalid colouring")
            return colors

        def minimum_hitting_set() -> list[int]:
            if not family:
                return []
            formula = WCNF()
            for row in family:
                formula.append([free_index[v] + 1 for v in row["D"]])
            for vertex in free:
                formula.append([-(free_index[vertex] + 1)], weight=1)
            with RC2(formula, solver="cd19", adapt=True, exhaust=False, minz=False) as optimizer:
                model = set(optimizer.compute())
            return sorted(v for v in free if free_index[v] + 1 in model)

        def add_killing_set(active: set[int], colors: dict[int, int]) -> bool:
            deleted = frozenset(set(range(n)) - active)
            if not deleted or deleted in seen:
                return False
            if not deleted <= set(free):
                raise AssertionError("a killing set contains a forced vertex")
            seen.add(deleted)
            family.append({
                "D": sorted(deleted),
                "witness": "".join(str(colors[v]) for v in range(n) if v not in deleted),
            })
            return True

        def greedy_extend(active: set[int], colors: dict[int, int]) -> tuple[set[int], dict[int, int]]:
            active = set(active)
            colors = dict(colors)
            remaining = [v for v in free if v not in active]
            rng.shuffle(remaining)
            changed = True
            while changed:
                changed = False
                for vertex in list(remaining):
                    used = {colors[neighbor] for neighbor in adjacency[vertex] if neighbor in active}
                    if len(used) < K:
                        available = [color for color in range(K) if color not in used]
                        colors[vertex] = available[rng.randrange(len(available))]
                        active.add(vertex)
                        remaining.remove(vertex)
                        changed = True
            return active, colors

        def grow(active: set[int], colors: dict[int, int]) -> tuple[set[int], dict[int, int]]:
            active, colors = greedy_extend(active, colors)
            budget = args.improve
            while budget:
                remaining = [v for v in free if v not in active]
                if not remaining:
                    break
                rng.shuffle(remaining)
                advanced = False
                for vertex in remaining:
                    if not budget:
                        break
                    budget -= 1
                    candidate = colorable(active | {vertex})
                    if candidate is not None:
                        active, colors = greedy_extend(active | {vertex}, candidate)
                        advanced = True
                        break
                if not advanced:
                    break
            return active, colors

        started = time.monotonic()
        for round_number in range(len(history) + 1, args.max_rounds + 1):
            optional = minimum_hitting_set()
            if len(optional) > target_free:
                history.append({
                    "round": round_number, "family": len(family),
                    "hitting_set": len(optional), "valid": None,
                })
                save("theorem")
                print(f"THEOREM family={len(family)} transversal={len(optional)} lower_bound={len(forced)+len(optional)}")
                return
            colors = colorable(forced | set(optional))
            history.append({
                "round": round_number, "family": len(family),
                "hitting_set": len(optional), "valid": colors is None,
            })
            print(
                f"round={round_number} family={len(family)} hit={len(optional)} "
                f"oracle={'UNSAT' if colors is None else 'SAT'} sat_calls={sat_calls} "
                f"sat_seconds={sat_seconds:.1f} wall_seconds={time.monotonic()-started:.1f}",
                flush=True,
            )
            if colors is None:
                save("record")
                print(f"RECORD order={len(forced)+len(optional)}")
                return
            forced_in = set(optional)
            base_colors = colors
            for _ in range(args.layers):
                active, full_colors = grow(forced | forced_in, base_colors)
                add_killing_set(active, full_colors)
                forced_in |= set(range(n)) - active
                base_colors = colorable(forced | forced_in)
                if base_colors is None:
                    break
            save("running")
    save("incomplete")


if __name__ == "__main__":
    main()
