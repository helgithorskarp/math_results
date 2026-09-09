#!/usr/bin/env python3
"""Exhaustive small-graph and explicit regular-graph controls."""
from itertools import combinations
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


def edge_index(n):
    return list(combinations(range(n), 2))


def has_clique(mask, n, size):
    pairs = edge_index(n)
    index = {edge: i for i, edge in enumerate(pairs)}
    for vertices in combinations(range(n), size):
        if all(mask & (1 << index[edge]) for edge in combinations(vertices, 2)):
            return True
    return False


def small_exhaustive():
    n = 6
    pairs = edge_index(n)
    full = (1 << len(pairs)) - 1
    good_preserved = 0
    for graph in range(full + 1):
        complement = full ^ graph
        need((full ^ complement) == graph, "complement involution")
        need(graph.bit_count() + complement.bit_count() == len(pairs),
             "small edge partition")
        red_k5 = has_clique(graph, n, 5)
        blue_k5 = has_clique(complement, n, 5)
        complement_red_k5 = has_clique(complement, n, 5)
        complement_blue_k5 = has_clique(graph, n, 5)
        need((red_k5, blue_k5) == (complement_blue_k5, complement_red_k5),
             "K5 colors swap")
        good = not red_k5 and not blue_k5
        complement_good = not complement_red_k5 and not complement_blue_k5
        need(good == complement_good, "good property preserved")
        good_preserved += int(good)
    return {"graphs": full + 1, "good_graphs": good_preserved, "order": n}


def circulant(n, degree):
    need(degree % 2 == 0 and degree < n, "even circulant degree")
    edges = set()
    for vertex in range(n):
        for step in range(1, degree // 2 + 1):
            edges.add(tuple(sorted((vertex, (vertex + step) % n))))
            edges.add(tuple(sorted((vertex, (vertex - step) % n))))
    return edges


def regular_controls():
    all_edges = set(edge_index(43))
    report = {}
    for degree in (20, 22):
        graph = circulant(43, degree)
        complement = all_edges - graph
        graph_degrees = CounterDegree(graph, 43)
        complement_degrees = CounterDegree(complement, 43)
        need(set(graph_degrees) == {degree}, "circulant degree")
        need(set(complement_degrees) == {42 - degree}, "complement degree")
        need(len(graph) == 43 * degree // 2, "handshaking edge count")
        need(len(graph) + len(complement) == 903, "K43 edge partition")
        report[str(degree)] = {
            "complement_degree": complement_degrees[0],
            "complement_edges": len(complement),
            "red_edges": len(graph),
        }
    return report


def CounterDegree(edges, n):
    degrees = [0] * n
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1
    return degrees


if __name__ == "__main__":
    result = {
        "even_order_tie_warning": {
            "K4_edges": 6,
            "tie_edge_count": 3,
            "why_not_applicable": "K43 has 903 edges, which is odd",
        },
        "regular43": regular_controls(),
        "small_exhaustive": small_exhaustive(),
        "status": "CONTROLS_PASS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
