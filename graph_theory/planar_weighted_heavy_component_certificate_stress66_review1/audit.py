#!/usr/bin/env python3
"""Independent exact audit of the capped-cylinder certificate (stdlib only)."""

from __future__ import annotations

import hashlib
import heapq
import itertools
import json
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1] / "planar_weighted_heavy_component_certificate" / "stress66"
N = 66


def vertex(i: int, j: int) -> int:
    return 2 + 8 * (i % 8) + j


def graph() -> tuple[list[dict[int, int]], set[tuple[int, int]]]:
    edges: set[tuple[int, int]] = set()

    def add(a: int, b: int) -> None:
        edges.add((min(a, b), max(a, b)))

    for i in range(8):
        add(0, vertex(i, 0))
        add(1, vertex(i, 7))
        for j in range(7):
            add(vertex(i, j), vertex(i, j + 1))
            if (i + j) % 2 == 0:
                add(vertex(i, j), vertex(i + 1, j + 1))
            else:
                add(vertex(i + 1, j), vertex(i, j + 1))
        for j in range(8):
            add(vertex(i, j), vertex(i + 1, j))
    assert len(edges) == 192
    adj = [{} for _ in range(N)]
    for a, b in edges:
        digest = hashlib.sha256(f"0:{a}:{b}".encode("ascii")).digest()
        length = 1 + int.from_bytes(digest[:4], "big") % 19
        adj[a][b] = adj[b][a] = length
    return adj, edges


def distances(adj: list[dict[int, int]]) -> list[list[int]]:
    result = []
    for source in range(N):
        d = [10**9] * N
        d[source] = 0
        heap = [(0, source)]
        while heap:
            dv, v = heapq.heappop(heap)
            if dv != d[v]:
                continue
            for w, length in adj[v].items():
                if dv + length < d[w]:
                    d[w] = dv + length
                    heapq.heappush(heap, (d[w], w))
        assert max(d) < 10**9
        result.append(d)
    return result


def components(edges: set[tuple[int, int]], removed: set[int]) -> list[frozenset[int]]:
    parent = list(range(N))

    def root(v: int) -> int:
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for a, b in edges:
        if a not in removed and b not in removed:
            parent[root(a)] = root(b)
    groups: dict[int, set[int]] = {}
    for v in range(N):
        if v not in removed:
            groups.setdefault(root(v), set()).add(v)
    return [frozenset(part) for part in groups.values()]


def compatible_count(families: list[list[frozenset[int]]]) -> int:
    states: list[tuple[frozenset[int], ...]] = [()]
    for family in families:
        states = [state + (part,) for state in states for part in family
                  if all(part & earlier for earlier in state)]
    return len(states)


def is_compatible(families: list[list[frozenset[int]]]) -> bool:
    states: list[tuple[frozenset[int], ...]] = [()]
    for family in sorted(families, key=len):
        states = [state + (part,) for state in states for part in family
                  if all(part & earlier for earlier in state)]
        if not states:
            return False
    return True


def minimum_subsets(families: list[list[frozenset[int]]]) -> tuple[int, list[tuple[int, ...]]]:
    """Enumerate every smaller subset, then every minimum-size subset."""
    for size in range(1, len(families) + 1):
        solutions = [ids for ids in itertools.combinations(range(len(families)), size)
                     if not is_compatible([families[i] for i in ids])]
        if solutions:
            return size, solutions
    raise AssertionError("the listed certificate has a compatible choice")


def longest_order(adj: list[dict[int, int]], dist: list[list[int]]) -> int:
    maximum = 0
    for source in range(N):
        best = [0] * N
        best[source] = 1
        for v in sorted(range(N), key=lambda x: dist[source][x]):
            for w, length in adj[v].items():
                if dist[source][v] + length == dist[source][w]:
                    best[w] = max(best[w], best[v] + 1)
        maximum = max(maximum, max(best))
    return maximum


def main() -> None:
    raw = (SOURCE / "certificate.json").read_bytes()
    certificate = json.loads(raw)
    assert certificate["schema"] == "heavy-component-chain-v1"
    assert certificate["graph"] == "capped-cylinder-8-by-8"
    assert certificate["metric_seed"] == 0
    assert len(certificate["cuts"]) == 16
    adj, edges = graph()
    dist = distances(adj)
    distance_hash = hashlib.sha256(
        json.dumps(dist, separators=(",", ":")).encode()
    ).hexdigest()
    assert distance_hash == "04e3b59d0eb791819212fc3f2766f049521124d94fde9bd4ef4b014bbd88dc91"
    assert hashlib.sha256(raw).hexdigest() == "dadc1d75df7ea6575e40c3eaebee46715a82280818904e8a54dec9c636934a9a"

    families: list[list[frozenset[int]]] = []
    paths: set[tuple[int, ...]] = set()
    for cut in certificate["cuts"]:
        assert len(cut["paths"]) == 2
        removed: set[int] = set()
        for path in cut["paths"]:
            assert path and len(path) == len(set(path))
            assert all(type(v) is int and 0 <= v < N for v in path)
            assert all(b in adj[a] for a, b in zip(path, path[1:]))
            cost = sum(adj[a][b] for a, b in zip(path, path[1:]))
            assert cost == dist[path[0]][path[-1]]
            removed.update(path)
            p = tuple(path)
            paths.add(min(p, p[::-1]))
        families.append(components(edges, removed))

    prefix_counts = [compatible_count(families[:i]) for i in range(1, 17)]
    assert prefix_counts == [1] * 15 + [0]
    omission_counts = [compatible_count(families[:i] + families[i + 1:]) for i in range(16)]
    minimum, minimal_subsets = minimum_subsets(families)
    assert minimum == 13
    assert (1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15) in minimal_subsets
    order = longest_order(adj, dist)
    assert order == 15
    assert len(paths) == 24
    print(json.dumps({
        "vertices": N,
        "edges": len(edges),
        "cuts": len(families),
        "distinct_paths": len(paths),
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "distance_matrix_sha256": distance_hash,
        "component_orders": [sorted(map(len, f)) for f in families],
        "compatible_prefix_counts": prefix_counts,
        "one_cut_omission_compatible_counts": omission_counts,
        "minimum_cuts_within_list": minimum,
        "minimum_subsets_zero_based": minimal_subsets,
        "maximum_geodesic_order": order,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
