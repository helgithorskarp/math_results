#!/usr/bin/env python3
"""Finite controls for the universal-vertex path-cover lemma and sharp family."""

from __future__ import annotations

import json


def distances(adj: list[int], source: int) -> list[int]:
    out = [-1] * len(adj)
    out[source] = 0
    queue = [source]
    for v in queue:
        for w in range(len(adj)):
            if adj[v] & (1 << w) and out[w] < 0:
                out[w] = out[v] + 1
                queue.append(w)
    return out


def geodesics(adj: list[int]) -> set[int]:
    paths: set[int] = set()
    for source in range(len(adj)):
        d = distances(adj, source)
        stack = [(source, 1 << source, 0)]
        while stack:
            v, mask, length = stack.pop()
            paths.add(mask)
            for w in range(len(adj)):
                if adj[v] & (1 << w) and not mask & (1 << w):
                    # Every prefix of a geodesic is itself geodesic.
                    if length + 1 == d[w]:
                        stack.append((w, mask | (1 << w), length + 1))
    return paths


def largest_component(adj: list[int], removed: int) -> int:
    unseen = ((1 << len(adj)) - 1) & ~removed
    largest = 0
    while unseen:
        bit = unseen & -unseen
        unseen ^= bit
        queue = [bit.bit_length() - 1]
        size = 0
        for v in queue:
            size += 1
            fresh = adj[v] & unseen
            while fresh:
                b = fresh & -fresh
                fresh ^= b
                unseen ^= b
                queue.append(b.bit_length() - 1)
        largest = max(largest, size)
    return largest


def local_graph(s: int, edges: int) -> list[int]:
    n = s + 1  # vertex 0 is universal
    adj = [0] * n
    for v in range(1, n):
        adj[0] |= 1 << v
        adj[v] |= 1
    idx = 0
    for v in range(2, n):
        for u in range(1, v):
            if edges & (1 << idx):
                adj[u] |= 1 << v
                adj[v] |= 1 << u
            idx += 1
    return adj


def sharp_graph(n: int) -> list[int]:
    adj = local_graph(n - 1, 0)
    # Vertex 1 is the second universal hub; 2,...,n-1 form a path.
    for v in range(2, n):
        adj[1] |= 1 << v
        adj[v] |= 1 << 1
    for v in range(2, n - 1):
        adj[v] |= 1 << (v + 1)
        adj[v + 1] |= 1 << v
    return adj


def main() -> None:
    cases = 0
    for s in range(4):
        for edges in range(1 << (s * (s - 1) // 2)):
            adj = local_graph(s, edges)
            paths = geodesics(adj)
            whole = (1 << len(adj)) - 1
            assert any(p | q == whole for p in paths for q in paths)
            cases += 1
    sharp_orders = list(range(7, 13))
    for n in sharp_orders:
        adj = sharp_graph(n)
        paths = geodesics(adj)
        assert all(2 * largest_component(adj, p) > n for p in paths)
        assert any(2 * largest_component(adj, p | q) <= n for p in paths for q in paths)
    print(json.dumps({"local_labeled_cases": cases, "local_failures": 0,
                      "one_path_sharp_orders": sharp_orders}, sort_keys=True))


if __name__ == "__main__":
    main()
