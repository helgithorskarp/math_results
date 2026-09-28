#!/usr/bin/env python3
"""Exact finite boundary certificates and constructive family checks; stdlib."""
from collections import deque
from copy import deepcopy
from hashlib import sha256
from heapq import heappop, heappush
import json
from pathlib import Path
import sys


def vertex(m, h, i, j):
    return 2 + h * (i % m) + j


def graph(m, h):
    if m not in (6, 8) or h < 2:
        raise ValueError("the proved family has m in {6,8} and h>=2")
    edges = set()
    vertical = set()

    def add(a, b):
        edges.add(tuple(sorted((a, b))))

    for i in range(m):
        add(0, vertex(m, h, i, 0))
        add(1, vertex(m, h, i, h - 1))
        for j in range(h):
            add(vertex(m, h, i, j), vertex(m, h, i + 1, j))
        for j in range(h - 1):
            e = (vertex(m, h, i, j), vertex(m, h, i, j + 1))
            add(*e)
            vertical.add(e)
            if (i + j) % 2 == 0:
                add(vertex(m, h, i, j), vertex(m, h, i + 1, j + 1))
            else:
                add(vertex(m, h, i + 1, j), vertex(m, h, i, j + 1))
    return edges, vertical


def adjacency(n, lengths):
    adj = [[] for _ in range(n)]
    for (a, b), cost in lengths.items():
        if type(cost) is not int or cost <= 0:
            raise ValueError("fixtures use positive integer lengths")
        adj[a].append((b, cost))
        adj[b].append((a, cost))
    return adj


def bfs_all(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    rows = []
    for root in range(n):
        dist = [-1] * n
        dist[root] = 0
        todo = deque([root])
        while todo:
            v = todo.popleft()
            for u in sorted(adj[v]):
                if dist[u] < 0:
                    dist[u] = dist[v] + 1
                    todo.append(u)
        if -1 in dist:
            raise ValueError("disconnected kernel")
        rows.append(dist)
    return rows


def components(n, edges, removed):
    """Union-find, independently of the discovery program's bitset traversal."""
    parent = list(range(n))

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for a, b in edges:
        if a not in removed and b not in removed:
            parent[find(a)] = find(b)
    parts = {}
    for v in range(n):
        if v not in removed:
            parts.setdefault(find(v), set()).add(v)
    return sorted((frozenset(c) for c in parts.values()), key=lambda c: min(c))


def coordinate_bound(m, h, a, b):
    i, j = divmod(a - 2, h)
    k, ell = divmod(b - 2, h)
    delta = min((i - k) % m, (k - i) % m)
    return min(max(abs(j - ell), delta), j + ell + 2, 2 * h - j - ell)


def check_kernel(m, data):
    if data.get("height") != 2:
        raise ValueError("wrong kernel height")
    edges, vertical = graph(m, 2)
    n = 2 * m + 2
    dist = bfs_all(n, edges)
    anchor = frozenset([0] + [vertex(m, 2, i, 0) for i in range(m)])
    forced = [anchor]
    trace = []
    distinct = set()
    for index, pair in enumerate(data["pairs"]):
        if not 1 <= len(pair) <= 2:
            raise ValueError("one or two paths required")
        removed = set()
        for path in pair:
            if not path or any(type(v) is not int or not 0 <= v < n for v in path):
                raise ValueError("invalid path vertex")
            if 1 in path or len(set(path)) != len(path):
                raise ValueError("proxy cap or repeated vertex")
            used = [tuple(sorted(e)) for e in zip(path, path[1:])]
            if any(e not in edges or e in vertical for e in used):
                raise ValueError("nonedge or forbidden vertical edge")
            if len(used) != dist[path[0]][path[-1]]:
                raise ValueError("not an ambient unit geodesic")
            if path[0] < 2 or path[-1] < 2 or len(used) != coordinate_bound(m, 2, path[0], path[-1]):
                raise ValueError("coordinate lower bound does not certify this path")
            distinct.add(min(tuple(path), tuple(reversed(path))))
            removed.update(path)
        parts = components(n, edges, removed)
        possible = [c for c in parts if all(c & f for f in forced)]
        trace.append({"cut": index, "components": [sorted(c) for c in parts],
                      "compatible_components": len(possible)})
        if not possible:
            if index != len(data["pairs"]) - 1:
                raise ValueError("unused certificate suffix")
            return {"vertices": n, "pairs": len(data["pairs"]),
                    "distinct_paths": len(distinct), "anchor": sorted(anchor), "trace": trace}
        if len(possible) != 1 or possible[0] in forced:
            raise ValueError("step does not force a new component")
        forced.append(possible[0])
    raise ValueError("certificate has no contradiction")


def kernel_map(m, h, v, bottom=False):
    """Reflect if needed, keep two rows, and collapse the rest to proxy 1."""
    if v < 2:
        return 1 - v if bottom else v
    i, j = divmod(v - 2, h)
    if bottom:
        i = (i + (1 if h % 2 == 0 else 0)) % m
        j = h - 1 - j
    return vertex(m, 2, i, j) if j < 2 else 1


def lift_vertex(m, h, v, bottom=False):
    if v == 1:
        raise ValueError("cannot lift the aggregate proxy cap")
    if v == 0:
        return 1 if bottom else 0
    i, j = divmod(v - 2, 2)
    if bottom:
        i = (i - (1 if h % 2 == 0 else 0)) % m
        j = h - 1 - j
    return vertex(m, h, i, j)


def balanced(n, edges, masses, paths):
    removed = set().union(*(set(p) for p in paths)) if paths else set()
    return all(2 * sum(masses[v] for v in c) <= sum(masses)
               for c in components(n, edges, removed))


def construct(m, h, masses, certificate, short_vertical=False):
    n = m * h + 2
    if len(masses) != n or any(w < 0 for w in masses):
        raise ValueError("invalid masses")
    total = sum(masses)
    if total == 0:
        return [], "zero"
    for pole in (0, 1):
        if 2 * masses[pole] >= total:
            return [[pole]], "pole"
    if short_vertical:
        weights = [sum(masses[vertex(m, h, i, j)] for j in range(h)) for i in range(m)]
        def meridian(i):
            return [0] + [vertex(m, h, i, j) for j in range(h)] + [1]
        if 2 * weights[0] >= sum(weights):
            return [meridian(0)], "meridian"
        running = weights[0]
        for i in range(1, m):
            running += weights[i]
            if 2 * running >= sum(weights):
                return [meridian(0), meridian(i)], "meridian"
        raise AssertionError("no cyclic mass median")
    running = masses[0]
    for j in range(h):
        running += sum(masses[vertex(m, h, i, j)] for i in range(m))
        if 2 * running >= total:
            break
    if 0 < j < h - 1:
        a = [vertex(m, h, i, j) for i in range(m // 2 + 1)]
        b = [vertex(m, h, i % m, j) for i in range(m // 2, m + 1)]
        return [a, b], "row"
    bottom = (j == h - 1)
    weights = [0] * (2 * m + 2)
    for v, mass in enumerate(masses):
        weights[kernel_map(m, h, v, bottom)] += mass
    anchor = [0] + [vertex(m, 2, i, 0) for i in range(m)]
    assert 2 * sum(weights[v] for v in anchor) >= total
    kernel_edges, _ = graph(m, 2)
    for pair in certificate["kernels"][str(m)]["pairs"]:
        if balanced(len(weights), kernel_edges, weights, pair):
            return [[lift_vertex(m, h, v, bottom) for v in path] for path in pair], "bottom" if bottom else "top"
    raise AssertionError("the boundary certificate failed")


def audit_witness(m, h, lengths, masses, paths):
    n = m * h + 2
    if len(paths) > 2:
        raise ValueError("too many paths")
    adj = adjacency(n, lengths)
    for path in paths:
        if not path or len(path) != len(set(path)):
            raise ValueError("empty or nonsimple path")
        cost = sum(lengths[tuple(sorted(e))] for e in zip(path, path[1:]))
        dist = {path[0]: 0}
        todo = [(0, path[0])]
        while todo:
            d, v = heappop(todo)
            if d != dist[v]:
                continue
            for u, ell in adj[v]:
                if d + ell < dist.get(u, d + ell + 1):
                    dist[u] = d + ell
                    heappush(todo, (d + ell, u))
        if cost != dist[path[-1]]:
            raise ValueError("witness is not an ambient geodesic")
    if not balanced(n, lengths, masses, paths):
        raise ValueError("witness is not half-balanced")


def fixtures(certificate):
    count = 0
    cases = {}
    max_order = 0
    for m in (6, 8):
        for h in (2, 3, 4, 5, 8, 17, 32):
            edges, vertical = graph(m, h)
            n = m * h + 2
            max_order = max(max_order, n)
            masses = [[0] * n, [1] * n]
            for pole in (0, 1):
                w = [1] * n
                w[pole] = 10 * n
                masses.append(w)
            for j in (0, h - 1, h // 2):
                w = [0] * n
                for i in range(m):
                    w[vertex(m, h, i, j)] = i + 1
                masses.append(w)
            # Exact half mass in each boundary row forces an anchor boundary case.
            w = [0] * n
            for j in (0, h - 1):
                for i in range(m):
                    w[vertex(m, h, i, j)] = 1
            masses.append(w)
            masses.append([(19 * v * v + 7 * v + 3) % 97 for v in range(n)])
            variants = []
            for mode in range(4):
                lengths = {}
                for a, b in edges:
                    if (a, b) in vertical:
                        if mode == 3 or (mode == 2 and (a + b) % 3 == 0):
                            continue
                        lengths[a, b] = 1 if mode == 0 else 10**6 + (a + 3 * b) ** 2
                    else:
                        lengths[a, b] = 1
                variants.append((lengths, False))
                # Check the nonexpansive quotient and its reflection on every edge.
                kernel_edges, _ = graph(m, 2)
                for bottom in (False, True):
                    for (a, b), ell in lengths.items():
                        x, y = kernel_map(m, h, a, bottom), kernel_map(m, h, b, bottom)
                        if x != y:
                            assert tuple(sorted((x, y))) in kernel_edges and ell >= 1
            for p, q in ((1, 37), (1, 2), (1, 1)):
                variants.append(({e: p if e in vertical else q for e in edges}, True))
            for lengths, short in variants:
                for w in masses:
                    paths, case = construct(m, h, w, certificate, short)
                    audit_witness(m, h, lengths, w, paths)
                    cases[case] = cases.get(case, 0) + 1
                    count += 1
    return {"witnesses": count, "maximum_order": max_order, "cases": cases}


def main():
    here = Path(__file__).resolve().parent
    raw = (here / "certificate.json").read_bytes()
    certificate = json.loads(raw)
    if certificate.get("schema") != "anchored-boundary-pairs-v1":
        raise ValueError("wrong certificate schema")
    kernels = {str(m): check_kernel(m, certificate["kernels"][str(m)]) for m in (6, 8)}
    rejected = 0
    def reject(data):
        nonlocal rejected
        try:
            check_kernel(8, data)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("invalid control accepted")
    d = deepcopy(certificate["kernels"]["8"])
    d["pairs"].pop()
    reject(d)
    for path in ([1], [2, 3], [0, 1], [0, 2, 0], [0, 2, 4]):
        d = deepcopy(certificate["kernels"]["8"])
        d["pairs"][0] = [path]
        reject(d)
    result = {"status": "PASS", "kernels": kernels, "fixtures": fixtures(certificate),
              "rejected_controls": rejected, "certificate_sha256": sha256(raw).hexdigest()}
    if sys.argv[1:] == ["--check"]:
        if result != json.loads((here / "expected.json").read_text()):
            raise AssertionError("result differs from expected.json")
    elif sys.argv[1:]:
        raise SystemExit("usage: verify.py [--check]")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
