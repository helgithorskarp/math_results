#!/usr/bin/env python3
"""Exact checks supporting the analytic reductions; no 22-vertex enumeration."""

from collections import Counter
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path


def read_rows(path):
    rows = path.read_text().splitlines()
    n = len(rows)
    if not n or any(len(row) != n or set(row) - {"0", "1"} for row in rows):
        raise ValueError("Expected a square binary matrix")
    graph = [{j for j, bit in enumerate(row) if bit == "1"} for row in rows]
    if any(i in graph[i] for i in range(n)) or any(
        (j in graph[i]) != (i in graph[j]) for i in range(n) for j in range(n)
    ):
        raise ValueError("Expected a simple undirected graph")
    return graph


def literal_statistics(graph):
    n = len(graph)
    vertices = set(range(n))
    blue = [vertices - graph[v] - {v} for v in range(n)]
    degree = [len(neighbors) for neighbors in graph]
    red_edges = [(i, j) for i, j in combinations(range(n), 2) if j in graph[i]]
    blue_edges = [(i, j) for i, j in combinations(range(n), 2) if j in blue[i]]
    red_codes = [len(graph[i] & graph[j]) for i, j in red_edges]
    blue_codes = [len(blue[i] & blue[j]) for i, j in blue_edges]
    red_triangles = blue_triangles = 0
    for i, j, k in combinations(range(n), 3):
        red_triangles += int(j in graph[i] and k in graph[i] and k in graph[j])
        blue_triangles += int(j in blue[i] and k in blue[i] and k in blue[j])
    red_defect = 3 * len(red_edges) - sum(red_codes)
    blue_defect = 6 * len(blue_edges) - sum(blue_codes)
    assert sum(red_codes) == 3 * red_triangles
    assert sum(blue_codes) == 3 * blue_triangles
    # Twice the generic global identity, computed independently from triangles.
    assert 2 * (red_defect + blue_defect) == (
        3 * sum(d * (n - 2 - d) for d in degree) - n * (n - 1) * (n - 8)
    )
    local = []
    for v in range(n):
        direct = sum(3 - len(graph[v] & graph[u]) for u in graph[v]) + sum(
            6 - len(blue[v] & blue[u]) for u in blue[v]
        )
        imbalance = sum(degree[u] for u in graph[v]) - sum(
            degree[u] for u in blue[v]
        )
        derived = (n - 1) * (8 - n) + (2 * n - 5) * degree[v] - degree[v] ** 2 - imbalance
        assert direct == derived
        assert direct % 2 == degree[v] % 2
        local.append(direct)
    assert sum(local) == 2 * (red_defect + blue_defect)
    return {
        "vertices": n,
        "red_edges": len(red_edges),
        "degrees": dict(sorted(Counter(degree).items())),
        "red_codegrees": dict(sorted(Counter(red_codes).items())),
        "blue_codegrees": dict(sorted(Counter(blue_codes).items())),
        "red_triangles": red_triangles,
        "blue_triangles": blue_triangles,
        "red_defect": red_defect,
        "blue_defect": blue_defect,
    }


def all_small_graphs():
    checked = 0
    for n in range(1, 7):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            graph = [set() for _ in range(n)]
            for bit, (i, j) in enumerate(pairs):
                if mask >> bit & 1:
                    graph[i].add(j)
                    graph[j].add(i)
            literal_statistics(graph)
            checked += 1
    return checked


def packing_patterns():
    # Prose proof: each clique component has size <=3 and needs three
    # distinct external neighbors; different components use disjoint sets.
    result = []
    for components in range(4):
        for parts in combinations_with_replacement((1, 2, 3), components):
            z = sum(parts)
            if 3 * components <= 10 - z:
                inside_z = sum(r * (r - 1) // 2 for r in parts)
                edges_remaining = 15 - 3 * z + inside_z
                assert edges_remaining >= 5
                result.append({"component_sizes": list(parts), "remaining_edges": edges_remaining})
    # Four components already require >10 exterior vertices, and the same
    # inequality rules out every larger component count.
    assert len(result) == 8
    assert min(row["remaining_edges"] for row in result) == 5
    return result


def main():
    directory = Path(__file__).resolve().parent
    fixture = directory / "baseline21.rows"
    baseline = literal_statistics(read_rows(fixture))
    assert baseline["red_edges"] == 93
    assert baseline["degrees"] == {8: 4, 9: 16, 10: 1}
    assert max(baseline["red_codegrees"]) == 3
    assert max(baseline["blue_codegrees"]) == 6
    assert baseline["red_triangles"] == 80
    assert baseline["blue_triangles"] == 216
    for x in range(-10, 12):
        assert 3 * x * x + x % 2 >= 8 * abs(x) - 4
    result = {
        "agent": "six-books-1",
        "claim_status": "analytic necessary-condition proof; Ramsey gap remains open",
        "baseline21_sha256": sha256(fixture.read_bytes()).hexdigest(),
        "baseline21": baseline,
        "small_graph_identity_checks": all_small_graphs(),
        "cubic10_packing_patterns": packing_patterns(),
        "degree_range22": [6, 12],
        "edge_range22": [97, 123],
        "maximum_absolute_degree_deviation22": 26,
        "degree13_outside_incidence_lower": 8 * 5,
        "degree13_outside_incidence_upper": 2 * 15,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
