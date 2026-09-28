#!/usr/bin/env python3
"""Verify a universal-mass separator certificate, using only the stdlib.

No search code, Dijkstra implementation, SMT solver, or path-mask reduction
is imported. Floyd-Warshall and direct set traversal check the certificate.
"""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import sys


def graph():
    """The explicit planar triangulation and its small integer edge metric."""
    n = 50
    edges = set()

    def edge(a, b):
        edges.add(tuple(sorted((a, b))))

    for i in range(7):
        for j in range(7):
            v = 1 + 7 * i + j
            if i < 6:
                edge(v, v + 7)
            if j < 6:
                edge(v, v + 1)
            if i < 6 and j < 6:
                edge(v, v + 8)
            if i in (0, 6) or j in (0, 6):
                edge(0, v)
    adj = [set() for _ in range(n)]
    lengths = {}
    for a, b in sorted(edges):
        digest = sha256(f"1:{a}:{b}".encode("ascii")).digest()
        length = 1 + int.from_bytes(digest[:4], "big") % 19
        lengths[a, b] = lengths[b, a] = length
        adj[a].add(b)
        adj[b].add(a)
    return adj, lengths


def distances(adj, lengths):
    """Exact Floyd-Warshall, without using a chosen shortest-path tree."""
    n = len(adj)
    infinity = 1 + sum(lengths.values())
    dist = [[0 if i == j else infinity for j in range(n)] for i in range(n)]
    for (a, b), length in lengths.items():
        dist[a][b] = length
    for k in range(n):
        for i in range(n):
            for j in range(n):
                through = dist[i][k] + dist[k][j]
                if through < dist[i][j]:
                    dist[i][j] = through
    if any(value == infinity for row in dist for value in row):
        raise ValueError("graph is disconnected")
    return dist


def check_path(path, adj, lengths, dist):
    if not path or any(type(v) is not int or not 0 <= v < len(adj) for v in path):
        raise ValueError("empty path or invalid vertex")
    if len(set(path)) != len(path):
        raise ValueError("path repeats a vertex")
    cost = 0
    for a, b in zip(path, path[1:]):
        if b not in adj[a]:
            raise ValueError("path contains a nonedge")
        cost += lengths[a, b]
    if cost != dist[path[0]][path[-1]]:
        raise ValueError("path is not an ambient geodesic")


def components(adj, removed):
    remaining = set(range(len(adj))) - removed
    parts = []
    while remaining:
        first = min(remaining)
        remaining.remove(first)
        todo = [first]
        component = {first}
        while todo:
            v = todo.pop()
            for w in sorted(adj[v]):
                if w in remaining:
                    remaining.remove(w)
                    component.add(w)
                    todo.append(w)
        parts.append(frozenset(component))
    return parts


def check_certificate(certificate, adj, lengths, dist):
    if certificate.get("schema") != "heavy-component-chain-v1":
        raise ValueError("unrecognized certificate schema")
    if certificate.get("graph") != "boundary-apex-triangulated-7-by-7-grid":
        raise ValueError("wrong graph")
    if certificate.get("metric_seed") != 1:
        raise ValueError("wrong edge metric")
    cuts = certificate["cuts"]
    if not cuts:
        raise ValueError("empty certificate")
    forced = []
    trace = []
    distinct_paths = set()
    for index, cut in enumerate(cuts):
        paths = cut["paths"]
        if not 1 <= len(paths) <= 2:
            raise ValueError("a cut must use one or two paths")
        removed = set()
        for path in paths:
            check_path(path, adj, lengths, dist)
            distinct_paths.add(min(tuple(path), tuple(reversed(path))))
            removed.update(path)
        parts = components(adj, removed)
        possible = [c for c in parts if all(c & f for f in forced)]
        trace.append({"cut": index, "component_orders": sorted(map(len, parts)),
                      "surviving_options": len(possible),
                      "forced_order": len(possible[0]) if len(possible) == 1 else None})
        if len(possible) == 0:
            if index != len(cuts) - 1:
                raise ValueError("unused certificate suffix")
            return trace, len(distinct_paths)
        if len(possible) != 1:
            raise ValueError("step does not force a unique heavy component")
        if possible[0] in forced:
            raise ValueError("redundant forcing step")
        forced.append(possible[0])
    raise ValueError("certificate does not reach a contradiction")


def longest_geodesic(adj, lengths, dist):
    """Longest path in each positive-length shortest-path DAG; ties included."""
    best = ()
    for source in range(len(adj)):
        paths = [None] * len(adj)
        paths[source] = (source,)
        for v in sorted(range(len(adj)), key=lambda x: (dist[source][x], x)):
            if paths[v] is None:
                raise ValueError("unreachable vertex in shortest-path DAG")
            for w in sorted(adj[v]):
                if dist[source][v] + lengths[v, w] == dist[source][w]:
                    candidate = paths[v] + (w,)
                    current = paths[w]
                    if current is None or len(candidate) > len(current) or (
                            len(candidate) == len(current) and candidate < current):
                        paths[w] = candidate
        for path in paths:
            if len(path) > len(best) or (len(path) == len(best) and path < best):
                best = path
    check_path(list(best), adj, lengths, dist)
    return best


def rejection_controls(certificate, adj, lengths, dist):
    count = 0

    def reject(fn):
        nonlocal count
        try:
            fn()
        except ValueError:
            count += 1
        else:
            raise AssertionError("invalid certificate control was accepted")

    short = deepcopy(certificate)
    short["cuts"].pop()
    reject(lambda: check_certificate(short, adj, lengths, dist))
    repeated = deepcopy(certificate)
    repeated["cuts"] = [{"paths": [[0], [0]]}] * 3
    reject(lambda: check_certificate(repeated, adj, lengths, dist))
    reject(lambda: check_path([0, 25], adj, lengths, dist))
    reject(lambda: check_path([0, 1, 0], adj, lengths, dist))
    nonshortest = next([a, b, c] for a in range(len(adj)) for b in sorted(adj[a])
                       for c in sorted(adj[b]) if a != c and
                       lengths[a, b] + lengths[b, c] > dist[a][c])
    reject(lambda: check_path(nonshortest, adj, lengths, dist))
    wrong_metric = deepcopy(certificate)
    wrong_metric["metric_seed"] = 2
    reject(lambda: check_certificate(wrong_metric, adj, lengths, dist))
    return count


def main():
    here = Path(__file__).resolve().parent
    raw = (here / "certificate.json").read_bytes()
    certificate = json.loads(raw)
    adj, lengths = graph()
    dist = distances(adj, lengths)
    trace, path_count = check_certificate(certificate, adj, lengths, dist)
    longest = longest_geodesic(adj, lengths, dist)
    assert 4 * len(longest) < len(adj)
    summary = {"status": "PASS", "vertices": len(adj), "edges": len(lengths) // 2,
               "edge_length_min": min(lengths.values()), "edge_length_max": max(lengths.values()),
               "certificate_cuts": len(certificate["cuts"]), "distinct_certificate_paths": path_count,
               "forcing_steps": len(trace) - 1, "longest_geodesic_vertices": len(longest),
               "longest_geodesic_witness": list(longest), "four_path_cover_capacity_bound": 4 * len(longest),
               "trace": trace, "rejected_controls": rejection_controls(certificate, adj, lengths, dist),
               "certificate_sha256": sha256(raw).hexdigest(),
               "distance_matrix_sha256": sha256(json.dumps(dist, separators=(",", ":")).encode()).hexdigest()}
    if sys.argv[1:] == ["--check"]:
        expected = json.loads((here / "expected.json").read_text())
        if summary != expected:
            raise AssertionError("result differs from expected.json")
    elif sys.argv[1:]:
        raise SystemExit("usage: verify.py [--check]")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
