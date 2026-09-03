#!/usr/bin/env python3
"""Lazy-SAT search for triangle-free circulant graphs with alpha < k.

Exploratory only.  All graph properties of any output must be checked by an
independent verifier before the result is used.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver


def dist(n: int, a: int, b: int) -> int:
    d = (a - b) % n
    return min(d, n - d)


def triangle_clauses(n: int) -> list[list[int]]:
    """All blue-triangle exclusions, with vertex 0 fixed by translation."""
    clauses: set[tuple[int, ...]] = set()
    for a in range(1, n):
        for b in range(a + 1, n):
            ds = {dist(n, 0, a), dist(n, 0, b), dist(n, a, b)}
            clauses.add(tuple(sorted((-d for d in ds))))
    return [list(c) for c in sorted(clauses)]


def red_adjacency(n: int, selected: set[int]) -> list[int]:
    adj = [0] * n
    for u in range(n):
        mask = 0
        for v in range(n):
            if u != v and dist(n, u, v) not in selected:
                mask |= 1 << v
        adj[u] = mask
    return adj


class SearchLimit(Exception):
    pass


def find_clique(adj: list[int], target: int,
                max_seconds: float | None = None) -> list[int] | None:
    """Find a target clique anchored at 0 in a vertex-transitive graph."""
    n = len(adj)
    answer: list[int] | None = None
    deadline = (time.monotonic() + max_seconds
                if max_seconds is not None else None)
    nodes = 0

    def color_sort(p: int) -> tuple[list[int], list[int]]:
        order: list[int] = []
        bounds: list[int] = []
        color = 0
        remaining = p
        while remaining:
            color += 1
            available = remaining
            while available:
                bit = available & -available
                v = bit.bit_length() - 1
                order.append(v)
                bounds.append(color)
                remaining ^= bit
                available ^= bit
                available &= ~adj[v]
        return order, bounds

    def expand(p: int, chosen: list[int]) -> bool:
        nonlocal answer, nodes
        nodes += 1
        if deadline is not None and not (nodes & 1023) and time.monotonic() > deadline:
            raise SearchLimit
        order, bounds = color_sort(p)
        for i in range(len(order) - 1, -1, -1):
            if len(chosen) + bounds[i] < target:
                return False
            v = order[i]
            bit = 1 << v
            if not (p & bit):
                continue
            chosen.append(v)
            if len(chosen) == target:
                answer = chosen.copy()
                return True
            if expand(p & adj[v], chosen):
                return True
            chosen.pop()
            p ^= bit
        return False

    if target <= 1:
        return [0]
    expand(adj[0], [0])
    return answer


def clique_cut(n: int, clique: list[int]) -> list[int]:
    return sorted({dist(n, clique[i], clique[j])
                   for i in range(len(clique))
                   for j in range(i + 1, len(clique))})


def cut_orbit(n: int, cut: list[int]) -> list[list[int]]:
    """Images of a valid clique cut under units of Z/nZ, modulo sign."""
    images = set()
    for multiplier in range(1, n):
        if math.gcd(multiplier, n) == 1:
            image = tuple(sorted({min((multiplier * d) % n,
                                      n - (multiplier * d) % n)
                                  for d in cut}))
            images.add(image)
    return [list(image) for image in sorted(images)]


def maximality_clauses(n: int, top_id: int) -> tuple[list[list[int]], int]:
    """Require every missing distance to have a blue common neighbor.

    The caller is responsible for proving that maximal triangle-freeness is a
    necessary condition for the search branch in question.
    """
    clauses: list[list[int]] = []
    for d in range(1, n // 2 + 1):
        pairs = {tuple(sorted((dist(n, 0, z), dist(n, d, z))))
                 for z in range(1, n) if z != d}
        witnesses = []
        for e, f in sorted(pairs):
            top_id += 1
            y = top_id
            witnesses.append(y)
            clauses.append([-y, e])
            clauses.append([-y, f])
        clauses.append([d] + witnesses)
    return clauses, top_id


def search(n: int, k: int, size: int | None, output: Path,
           checkpoint: Path | None, max_models: int | None,
           clique_seconds: float | None, seed: set[int],
           required: set[int], forbidden: set[int], maximal: bool) -> int:
    variables = n // 2
    clauses = triangle_clauses(n)
    clauses.extend([[d] for d in sorted(required)])
    clauses.extend([[-d] for d in sorted(forbidden)])
    top_id = variables
    if size is not None:
        card = CardEnc.equals(
            lits=list(range(1, variables + 1)), bound=size,
            top_id=top_id, encoding=EncType.seqcounter)
        clauses.extend(card.clauses)
        top_id = card.nv
    if maximal:
        extra, top_id = maximality_clauses(n, top_id)
        clauses.extend(extra)

    cuts: list[list[int]] = []
    cut_keys: set[tuple[int, ...]] = set()
    if checkpoint and checkpoint.exists():
        data = json.loads(checkpoint.read_text())
        if data.get("n") != n or data.get("k") != k or data.get("size") != size:
            raise ValueError("checkpoint parameters do not match")
        stored_cuts = data["cuts"]
        already_closed = data.get("orbit_closed", False) or len(stored_cuts) > 100_000
        for cut in stored_cuts:
            images = [cut] if already_closed else cut_orbit(n, cut)
            for image in images:
                key = tuple(image)
                if key not in cut_keys:
                    cut_keys.add(key)
                    cuts.append(image)
        clauses.extend(cuts)

    started = time.monotonic()
    with Solver(name="cadical195", bootstrap_with=clauses) as solver:
        solver.set_phases([d if d in seed else -d
                           for d in range(1, variables + 1)])
        iteration = len(cuts)
        while solver.solve():
            iteration += 1
            selected = {lit for lit in solver.get_model()
                        if 1 <= lit <= variables}
            try:
                clique = find_clique(red_adjacency(n, selected), k,
                                     clique_seconds)
            except SearchLimit:
                result = {
                    "status": "candidate_needs_exact_check",
                    "n": n, "k": k, "selected_distances": sorted(selected),
                    "iterations": iteration,
                    "elapsed_seconds": time.monotonic() - started,
                }
                output.write_text(json.dumps(result, indent=2) + "\n")
                if checkpoint:
                    checkpoint.write_text(json.dumps({
                        "n": n, "k": k, "size": size, "orbit_closed": True,
                        "cuts": cuts
                    }))
                print(json.dumps(result))
                return 3
            if clique is None:
                result = {
                    "n": n, "k": k, "selected_distances": sorted(selected),
                    "iterations": iteration,
                    "elapsed_seconds": time.monotonic() - started,
                }
                output.write_text(json.dumps(result, indent=2) + "\n")
                print(json.dumps(result))
                return 0
            cut = clique_cut(n, clique)
            for image in cut_orbit(n, cut):
                key = tuple(image)
                if key not in cut_keys:
                    solver.add_clause(image)
                    cut_keys.add(key)
                    cuts.append(image)
            if iteration % 100 == 0:
                elapsed = time.monotonic() - started
                print(f"iteration={iteration} elapsed={elapsed:.1f}s "
                      f"selected={sorted(selected)} cut={len(cut)}", flush=True)
            if checkpoint and iteration % 1000 == 0:
                checkpoint.write_text(json.dumps({
                    "n": n, "k": k, "size": size, "orbit_closed": True,
                    "cuts": cuts
                }))
            if max_models is not None and iteration >= max_models:
                print(f"stopped after {iteration} models")
                return 2
        if checkpoint:
            checkpoint.write_text(json.dumps({
                "n": n, "k": k, "size": size, "orbit_closed": True,
                "cuts": cuts
            }))
        print(f"UNSAT under requested cardinality after {iteration} iterations")
        return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--independence", type=int, default=21,
                        help="forbid an independent set of this size")
    parser.add_argument("--size", type=int,
                        help="require exactly this many selected distances")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--max-models", type=int)
    parser.add_argument("--clique-seconds", type=float, default=0.5,
                        help="emit a candidate if clique search exceeds this")
    parser.add_argument("--seed-distances", type=int, nargs="*", default=[])
    parser.add_argument("--require-distances", type=int, nargs="*", default=[])
    parser.add_argument("--forbid-distances", type=int, nargs="*", default=[])
    parser.add_argument("--maximal-triangle-free", action="store_true")
    args = parser.parse_args()
    return search(args.order, args.independence, args.size, args.output,
                  args.checkpoint, args.max_models, args.clique_seconds,
                  set(args.seed_distances), set(args.require_distances),
                  set(args.forbid_distances),
                  args.maximal_triangle_free)


if __name__ == "__main__":
    raise SystemExit(main())
