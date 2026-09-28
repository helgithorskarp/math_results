#!/usr/bin/env python3
"""Exact definition-level checks of the witnesses in PROOF.md; stdlib only."""

from collections import deque
from hashlib import sha256
import json
from pathlib import Path
import sys


def mesh(m, h, cyclic, diagonal):
    if m < (3 if cyclic else 1) or h < 1:
        raise ValueError("invalid mesh dimensions")
    n = m * h + 2
    adj = [set() for _ in range(n)]

    def edge(u, v):
        if u == v:
            raise ValueError("loop")
        adj[u].add(v)
        adj[v].add(u)

    def v(i, j):
        return 2 + i * h + j - 1

    for i in range(m):
        line = [0] + [v(i, j) for j in range(1, h + 1)] + [1]
        for a, b in zip(line, line[1:]):
            edge(a, b)
    for i in range(m if cyclic else m - 1):
        q = (i + 1) % m
        for j in range(1, h + 1):
            edge(v(i, j), v(q, j))
        for j in range(1, h):
            d = diagonal(i, j)
            if d == 1:
                edge(v(i, j), v(q, j + 1))
            elif d == -1:
                edge(v(q, j), v(i, j + 1))
            elif d != 0:
                raise ValueError("invalid diagonal")
    if not cyclic:
        edge(0, 1)
    return [tuple(sorted(neighbors)) for neighbors in adj]


def witness(m, h, cyclic, weights, first=0):
    if len(weights) != m * h + 2 or any(x < 0 for x in weights):
        raise ValueError("invalid weights")
    b = [sum(weights[2 + i * h:2 + (i + 1) * h]) for i in range(m)]
    total = sum(b)

    def meridian(i):
        return [0] + list(range(2 + i * h, 2 + (i + 1) * h)) + [1]

    if cyclic:
        if not 0 <= first < m:
            raise ValueError("invalid first meridian")
        paths = [meridian(first)]
        if 2 * b[first] < total:
            accum = b[first]
            for offset in range(1, m):
                j = (first + offset) % m
                accum += b[j]
                if 2 * accum >= total:
                    paths.append(meridian(j))
                    break
        return paths
    a = 0
    if total:
        accum = 0
        for a in range(m):
            accum += b[a]
            if 2 * accum >= total:
                break
    line = meridian(a)
    cut = h // 2 + 1
    return [line[:cut], list(reversed(line[cut:]))]


def bfs_distance(adj, start, end):
    dist = {start: 0}
    todo = deque([start])
    while todo:
        v = todo.popleft()
        if v == end:
            return dist[v]
        for w in adj[v]:
            if w not in dist:
                dist[w] = dist[v] + 1
                todo.append(w)
    raise ValueError("disconnected endpoints")


def audit(adj, weights, paths):
    """Uses no levels, columns, cycle maps, or median arguments."""
    n = len(adj)
    if len(weights) != n or any(type(x) is not int or x < 0 for x in weights):
        raise ValueError("audit needs nonnegative integer weights")
    if len(paths) > 2:
        raise ValueError("more than two paths")
    for v, neighbors in enumerate(adj):
        if len(neighbors) != len(set(neighbors)) or v in neighbors:
            raise ValueError("graph is not simple")
        for w in neighbors:
            if not 0 <= w < n or v not in adj[w]:
                raise ValueError("graph is not undirected")
    removed = set()
    for path in paths:
        if not path or len(set(path)) != len(path):
            raise ValueError("empty or nonsimple path")
        if any(not 0 <= v < n for v in path):
            raise ValueError("unknown vertex")
        if any(b not in adj[a] for a, b in zip(path, path[1:])):
            raise ValueError("nonedge in path")
        if bfs_distance(adj, path[0], path[-1]) != len(path) - 1:
            raise ValueError("path is not ambient geodesic")
        removed.update(path)
    remaining = set(range(n)) - removed
    components = []
    while remaining:
        root = min(remaining)
        remaining.remove(root)
        todo = [root]
        component = []
        while todo:
            v = todo.pop()
            component.append(v)
            for w in adj[v]:
                if w in remaining:
                    remaining.remove(w)
                    todo.append(w)
        components.append(sorted(component))
    component_weights = [sum(weights[v] for v in c) for c in components]
    if 2 * max(component_weights, default=0) > sum(weights):
        raise ValueError("separator is not half balanced")
    return component_weights


def inflate(adj, masses):
    if len(masses) != len(adj) or any(type(a) is not int or a < 1 for a in masses):
        raise ValueError("inflation needs positive integer masses")
    enlarged = [set(neighbors) for neighbors in adj]
    for v, a in enumerate(masses):
        for _ in range(a - 1):
            w = len(enlarged)
            enlarged.append({v})
            enlarged[v].add(w)
    return [tuple(sorted(neighbors)) for neighbors in enlarged]


def weights_for(n, mode):
    if mode == 0:
        return [1] * n
    if mode == 1:
        return [0 if v != n // 2 else 101 for v in range(n)]
    if mode == 2:
        return [(v * 73 + v * v * 11 + 7) % 19 for v in range(n)]
    if mode == 3:
        return [1000 if v < 2 else v % 3 for v in range(n)]
    if mode == 4:
        return [0] * n
    if mode == 5:
        return [1 + (v * v + 3 * v) % 4 for v in range(n)]
    raise ValueError("unknown weight mode")


def main():
    diagonals = [lambda i, j: 0, lambda i, j: 1, lambda i, j: -1,
                 lambda i, j: 1 if (i + j) % 2 else -1,
                 lambda i, j: (17 * i + 31 * j + i * j) % 3 - 1]
    counts = {"cylindrical_witnesses": 0, "shortcut_witnesses": 0,
              "inflated_witnesses": 0, "rejection_controls": 0}
    digest = sha256()
    max_order = 0
    for cyclic in (True, False):
        ms = (3, 4, 7, 11) if cyclic else (1, 2, 3, 7, 11)
        for m in ms:
            for h in (1, 2, 3, 6, 9):
                for d, diagonal in enumerate(diagonals):
                    adj = mesh(m, h, cyclic, diagonal)
                    for mode in range(6):
                        weights = weights_for(len(adj), mode)
                        for first in (range(m) if cyclic else (0,)):
                            paths = witness(m, h, cyclic, weights, first)
                            component_weights = audit(adj, weights, paths)
                            key = "cylindrical_witnesses" if cyclic else "shortcut_witnesses"
                            counts[key] += 1
                            row = [cyclic, m, h, d, mode, first, paths, component_weights]
                            digest.update((json.dumps(row, separators=(",", ":")) + "\n").encode())
                            max_order = max(max_order, len(adj))
                            if mode == 5 and first == 0:
                                enlarged = inflate(adj, weights)
                                audit(enlarged, [1] * len(enlarged), paths)
                                counts["inflated_witnesses"] += 1
                                max_order = max(max_order, len(enlarged))

    def must_reject(fn):
        try:
            fn()
        except ValueError:
            counts["rejection_controls"] += 1
        else:
            raise AssertionError("malformed witness was accepted")

    # The shortcut invalidates a whole meridian, despite every edge being present.
    adj = mesh(7, 6, False, diagonals[0])
    full_meridian = [0] + list(range(2, 8)) + [1]
    must_reject(lambda: audit(adj, [1] * len(adj), [full_meridian]))
    # Both poles are singleton geodesics, but their deletion leaves a heavy grid.
    must_reject(lambda: audit(adj, [1] * len(adj), [[0], [1]]))
    must_reject(lambda: audit(adj, [1] * len(adj), [[0, 1, 0]]))
    must_reject(lambda: audit(adj, [1] * len(adj), [[0], [1], [2]]))
    must_reject(lambda: inflate(adj, [0] * len(adj)))
    must_reject(lambda: mesh(2, 1, True, diagonals[0]))

    summary = {"status": "PASS", **counts, "largest_checked_order": max_order,
               "witness_stream_sha256": digest.hexdigest(),
               "arithmetic": "Python arbitrary-precision integers",
               "scope": "finite witness checks; infinite claims proved in PROOF.md"}
    if len(sys.argv) > 1:
        if sys.argv[1:] != ["--check"]:
            raise SystemExit("usage: verify.py [--check]")
        expected = json.loads(Path(__file__).with_name("expected.json").read_text())
        if summary != expected:
            raise AssertionError("summary differs from expected.json")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
