#!/usr/bin/env python3
"""Independent finite audit of the m=6,8 boundary kernels and quotient maps."""

from __future__ import annotations

from collections import deque
import hashlib
import json
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1] / "planar_annular_stretch_family"


def vertex(h: int, i: int, j: int) -> int:
    return 2 + h * i + j


def edges_of(m: int, h: int) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    edges: set[tuple[int, int]] = set()
    vertical: set[tuple[int, int]] = set()

    def add(a: int, b: int) -> tuple[int, int]:
        e = min(a, b), max(a, b)
        edges.add(e)
        return e

    for i in range(m):
        nxt = (i + 1) % m
        add(0, vertex(h, i, 0))
        add(1, vertex(h, i, h - 1))
        for j in range(h):
            add(vertex(h, i, j), vertex(h, nxt, j))
        for j in range(h - 1):
            vertical.add(add(vertex(h, i, j), vertex(h, i, j + 1)))
            if (i + j) % 2 == 0:
                add(vertex(h, i, j), vertex(h, nxt, j + 1))
            else:
                add(vertex(h, nxt, j), vertex(h, i, j + 1))
    return edges, vertical


def adjacency(n: int, edges: set[tuple[int, int]]) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def bfs(adj: list[set[int]], source: int) -> list[int]:
    dist = [-1] * len(adj)
    dist[source] = 0
    queue = deque([source])
    while queue:
        v = queue.popleft()
        for w in adj[v]:
            if dist[w] < 0:
                dist[w] = dist[v] + 1
                queue.append(w)
    return dist


def components(adj: list[set[int]], removed: set[int]) -> list[frozenset[int]]:
    unseen = set(range(len(adj))) - removed
    parts = []
    while unseen:
        root = next(iter(unseen))
        seen = {root}
        queue = [root]
        unseen.remove(root)
        for v in queue:
            for w in adj[v] & unseen:
                unseen.remove(w)
                seen.add(w)
                queue.append(w)
        parts.append(frozenset(seen))
    return parts


def reflect(m: int, h: int, v: int) -> int:
    if v < 2:
        return 1 - v
    i, j = divmod(v - 2, h)
    shift = 1 if h % 2 == 0 else 0
    return vertex(h, (i + shift) % m, h - 1 - j)


def quotient(m: int, h: int, v: int, bottom: bool) -> int:
    if bottom:
        v = reflect(m, h, v)
    if v < 2:
        return v
    i, j = divmod(v - 2, h)
    return vertex(2, i, j) if j < 2 else 1


def main() -> None:
    raw = (SOURCE / "certificate.json").read_bytes()
    certificate = json.loads(raw)
    assert hashlib.sha256(raw).hexdigest() == (
        "51d142c536bb8b630d1eaed595c1ec020697b527927355474954c94ea0a96e7e"
    )
    result = {}
    for m in (6, 8):
        n = 2 * m + 2
        edges, vertical = edges_of(m, 2)
        adj = adjacency(n, edges)
        distances = [bfs(adj, v) for v in range(n)]
        anchor = frozenset({0} | {vertex(2, i, 0) for i in range(m)})
        states: list[tuple[frozenset[int], ...]] = [(anchor,)]
        prefixes = []
        component_orders = []
        paths = set()
        pairs = certificate["kernels"][str(m)]["pairs"]
        assert len(pairs) == 3
        for pair in pairs:
            assert 1 <= len(pair) <= 2
            removed: set[int] = set()
            for path in pair:
                assert path and len(path) == len(set(path))
                assert all(type(v) is int and 0 <= v < n and v != 1 for v in path)
                used = {(min(a, b), max(a, b)) for a, b in zip(path, path[1:])}
                assert len(used) == len(path) - 1
                assert used <= edges and not (used & vertical)
                assert len(path) - 1 == distances[path[0]][path[-1]]
                p = tuple(path)
                paths.add(min(p, p[::-1]))
                removed.update(path)
            parts = components(adj, removed)
            component_orders.append(sorted(map(len, parts)))
            states = [state + (part,) for state in states for part in parts
                      if all(part & earlier for earlier in state)]
            prefixes.append(len(states))
        assert prefixes == [1, 1, 0]
        assert len(paths) == 5

        # The lower-end reflection is a graph automorphism; either quotient
        # sends each original edge to an edge of K_m or collapses it.
        quotient_checks = 0
        for h in range(2, 34):
            original, _ = edges_of(m, h)
            assert {(min(reflect(m, h, a), reflect(m, h, b)),
                     max(reflect(m, h, a), reflect(m, h, b)))
                    for a, b in original} == original
            for bottom in (False, True):
                fibres: dict[int, set[int]] = {}
                for v in range(m * h + 2):
                    fibres.setdefault(quotient(m, h, v, bottom), set()).add(v)
                for pair in pairs:
                    removed = set().union(*map(set, pair))
                    assert all(len(fibres[v]) == 1 for v in removed)
                for a, b in original:
                    x, y = quotient(m, h, a, bottom), quotient(m, h, b, bottom)
                    assert x == y or (min(x, y), max(x, y)) in edges
                    quotient_checks += 1
        result[str(m)] = {
            "vertices": n,
            "edges": len(edges),
            "distinct_paths": len(paths),
            "anchored_compatible_prefix_counts": prefixes,
            "component_orders": component_orders,
            "quotient_edge_checks_heights_2_through_33": quotient_checks,
        }
    print(json.dumps({"certificate_sha256": hashlib.sha256(raw).hexdigest(),
                      "kernels": result}, sort_keys=True))


if __name__ == "__main__":
    main()
