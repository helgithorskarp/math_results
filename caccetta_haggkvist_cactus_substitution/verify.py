#!/usr/bin/env python3
"""Exact small-instance audit for the cactus-substitution theorem.

The universal result is proved in THEOREM.md.  This script exhausts labelled
quotients through order five, all their orientations, binary module weights,
and a finite quotient-arithmetic range.  It uses only exact integers.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter


def undirected_edges(n: int) -> list[tuple[int, int]]:
    return [(u, v) for u in range(n) for v in range(u + 1, n)]


def adjacency(n: int, edges: tuple[tuple[int, int], ...]) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def connected(n: int, edges: tuple[tuple[int, int], ...]) -> bool:
    if n == 0:
        return True
    adj = adjacency(n, edges)
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == n


def is_cactus(n: int, edges: tuple[tuple[int, int], ...]) -> bool:
    """Return whether every edge is in at most one simple cycle.

    An edge uv lies in two cycles iff, after deleting it, there are two
    internally vertex-disjoint u-v paths.  For these tiny graphs we instead
    enumerate all simple cycles and count edge incidences directly.
    """

    adj = adjacency(n, edges)
    counts: Counter[tuple[int, int]] = Counter()
    cycles: set[tuple[int, ...]] = set()

    def canonical(cycle: list[int]) -> tuple[int, ...]:
        seq = cycle[:]
        variants = []
        for s in (seq, list(reversed(seq))):
            for r in range(len(s)):
                variants.append(tuple(s[r:] + s[:r]))
        return min(variants)

    for start in range(n):
        def dfs(path: list[int], used: set[int]) -> None:
            u = path[-1]
            for v in adj[u]:
                if v == start and len(path) >= 3:
                    cycles.add(canonical(path))
                elif v > start and v not in used:
                    used.add(v)
                    path.append(v)
                    dfs(path, used)
                    path.pop()
                    used.remove(v)

        dfs([start], {start})

    for cycle in cycles:
        for i, u in enumerate(cycle):
            v = cycle[(i + 1) % len(cycle)]
            counts[tuple(sorted((u, v)))] += 1
    return all(value <= 1 for value in counts.values())


def orient(edges: tuple[tuple[int, int], ...], mask: int) -> tuple[tuple[int, int], ...]:
    arcs = []
    for bit, (u, v) in enumerate(edges):
        arcs.append((u, v) if (mask >> bit) & 1 else (v, u))
    return tuple(arcs)


def outsets(n: int, arcs: tuple[tuple[int, int], ...]) -> list[set[int]]:
    out = [set() for _ in range(n)]
    for u, v in arcs:
        out[u].add(v)
    return out


def directed_cycles(n: int, arcs: tuple[tuple[int, int], ...]) -> list[tuple[int, ...]]:
    out = outsets(n, arcs)
    found: set[tuple[int, ...]] = set()

    def canonical(cycle: list[int]) -> tuple[int, ...]:
        return min(tuple(cycle[r:] + cycle[:r]) for r in range(len(cycle)))

    for start in range(n):
        def dfs(path: list[int], used: set[int]) -> None:
            u = path[-1]
            for v in out[u]:
                if v == start and len(path) >= 2:
                    found.add(canonical(path))
                elif v >= start and v not in used:
                    used.add(v)
                    path.append(v)
                    dfs(path, used)
                    path.pop()
                    used.remove(v)

        dfs([start], {start})
    return sorted(found)


def is_out_packing(n: int, arcs: tuple[tuple[int, int], ...], cycle: tuple[int, ...]) -> bool:
    tails = set(cycle)
    arcset = set(arcs)
    return all(sum((u, x) in arcset for u in tails) <= 1 for x in range(n))


def is_directed_cycle_graph(n: int, arcs: tuple[tuple[int, int], ...]) -> bool:
    if len(arcs) != n:
        return False
    out = outsets(n, arcs)
    indeg = [0] * n
    for _, v in arcs:
        indeg[v] += 1
    return all(len(out[v]) == 1 and indeg[v] == 1 for v in range(n))


def audit() -> dict[str, object]:
    connected_cacti = 0
    orientations = 0
    sinkless_orientations = 0
    packing_cycles_checked = 0
    weighted_instances = 0
    equality_instances = 0
    arithmetic_instances = 0
    records: list[str] = []

    for n in range(2, 6):
        complete = undirected_edges(n)
        for graph_mask in range(1 << len(complete)):
            edges = tuple(e for bit, e in enumerate(complete) if (graph_mask >> bit) & 1)
            if not connected(n, edges) or not is_cactus(n, edges):
                continue
            connected_cacti += 1
            for orientation_mask in range(1 << len(edges)):
                arcs = orient(edges, orientation_mask)
                orientations += 1
                out = outsets(n, arcs)
                if any(not out[v] for v in range(n)):
                    continue
                sinkless_orientations += 1
                cycles = directed_cycles(n, arcs)
                if not cycles:
                    raise AssertionError("sinkless orientation has no directed cycle")
                packing = [c for c in cycles if is_out_packing(n, arcs, c)]
                if not packing:
                    raise AssertionError("cactus orientation lacks an out-packing cycle")
                packing_cycles_checked += len(packing)

                for weights in itertools.product((1, 2), repeat=n):
                    weighted_instances += 1
                    ext = [sum(weights[v] for v in out[u]) for u in range(n)]
                    delta = min(ext)
                    girth = min(map(len, cycles))
                    order = sum(weights)
                    if girth * delta > order:
                        raise AssertionError("weighted blow-up violates the sharp inequality")
                    if girth * delta == order:
                        equality_instances += 1
                        if not is_directed_cycle_graph(n, arcs) or len(set(weights)) != 1:
                            raise AssertionError("unexpected equality case")
                    records.append(f"W|{n}|{edges}|{arcs}|{weights}|{girth}|{delta}|{order}")

                # Audit the numerical heart of the fixed-k substitution proof.
                for k in range(2, 7):
                    for sizes in itertools.product((1, 2, 3), repeat=n):
                        allowed_a = [range((size - 1) // k + 1) for size in sizes]
                        for internal_minima in itertools.product(*allowed_a):
                            if any(k * a >= size for a, size in zip(internal_minima, sizes)):
                                raise AssertionError("strict internal deficit encoded incorrectly")
                            external = [sum(sizes[v] for v in out[u]) for u in range(n)]
                            global_delta = min(
                                internal_minima[u] + external[u] for u in range(n)
                            )
                            total = sum(sizes)
                            if k * global_delta >= total and min(map(len, packing)) > k:
                                raise AssertionError("substitution arithmetic failed")
                            arithmetic_instances += 1

    # A planar wheel orientation for which no directed cycle is out-packing.
    wheel_arcs = (
        (1, 0), (0, 3), (3, 2), (2, 1),
        (0, 4), (2, 4), (4, 1), (4, 3),
    )
    wheel_cycles = directed_cycles(5, wheel_arcs)
    wheel_packing = [c for c in wheel_cycles if is_out_packing(5, wheel_arcs, c)]
    if not wheel_cycles or wheel_packing:
        raise AssertionError("wheel boundary fixture is wrong")

    digest = hashlib.sha256("\n".join(records).encode()).hexdigest()
    return {
        "arithmetic_instances_checked": arithmetic_instances,
        "connected_labelled_cacti": connected_cacti,
        "equality_instances": equality_instances,
        "packing_cycles_checked": packing_cycles_checked,
        "record_sha256": digest,
        "sinkless_orientations": sinkless_orientations,
        "theorem": "cactus substitutions preserve every fixed Caccetta-Haggkvist implication",
        "weighted_instances_checked": weighted_instances,
        "wheel_boundary_cycles": len(wheel_cycles),
        "wheel_out_packing_cycles": len(wheel_packing),
        "all_orientations": orientations,
        "verified": True,
    }


def main() -> None:
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
