#!/usr/bin/env python3
"""Certificate kernel: dense GF(2) rank, literal pair and witness checks.

Imports neither extractor, finite-field generator nor expected results.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def dense_rank(matrix):
    a = [list(row) for row in matrix]
    r = 0
    for j in range(len(a)):
        pivot = next((i for i in range(r, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        for i in range(r+1, len(a)):
            if a[i][j]:
                a[i] = [x ^ y for x, y in zip(a[i], a[r])]
        r += 1
    return r


def form(x, y):
    return sum(((x >> j & 1)*(y >> (j+3) & 1) + (y >> j & 1)*(x >> (j+3) & 1))
               for j in range(3)) % 2


def verify_spread(data):
    classes = data["classes"]
    require(type(data["zero_color"]) is int and data["zero_color"] == 0, "Zero color")
    require(isinstance(classes, list) and len(classes) == 9, "Nine spread classes")
    require(all(isinstance(c, list) and len(c) == 7 for c in classes), "Seven vectors per class")
    flat = [v for c in classes for v in c]
    require(all(type(v) is int for v in flat) and sorted(flat) == list(range(1, 64)), "Spread partition")
    for c in classes:
        require(all(form(x, y) == 0 for x, y in combinations(c, 2)), "Not isotropic")
    return 9*21


def verify(graph, certificate, spread):
    require(isinstance(graph, dict) and set(graph) == {"n", "edges"}, "Graph fields")
    n = graph["n"]
    require(type(n) is int and n >= 1 and isinstance(graph["edges"], list), "Graph order")
    matrix, previous = [[0]*n for _ in range(n)], (-1, -1)
    for e in graph["edges"]:
        require(isinstance(e, list) and len(e) == 2 and all(type(x) is int for x in e), "Pair types")
        u, v = e
        require(0 <= u < v < n and (u, v) > previous, "Sorted simple graph")
        matrix[u][v] = matrix[v][u] = 1
        previous = u, v
    c = certificate
    require(c["n"] == n and c["adjacency_color"] in ("red", "blue"), "Graph/color scope")
    if c["adjacency_color"] == "blue":
        matrix = [[0 if i == j else 1-matrix[i][j] for j in range(n)] for i in range(n)]
    rank = dense_rank(matrix)
    require(type(c["binary_rank"]) is int and c["binary_rank"] == rank and rank % 2 == 0, "Binary rank")
    pairs = c["factor_pairs"]
    require(isinstance(pairs, list) and len(pairs)*2 == rank, "Factor count")
    require(all(isinstance(p, list) and len(p) == 2 and all(type(x) is int and 0 <= x < 1 << n for x in p)
                for p in pairs), "Factor word range")
    for i in range(n):
        for j in range(n):
            value = sum((u >> i & 1)*(v >> j & 1)+(v >> i & 1)*(u >> j & 1) for u, v in pairs) % 2
            require(value == matrix[i][j], "Factorization does not reproduce adjacency")
    if rank > 6:
        require(c["status"] == "OUTSIDE_RANK_SIX", "Out-of-family verdict")
        require(not any(k in c for k in ("independent_five", "coloring", "coordinates")), "Overclaimed high rank")
        return rank
    require(c["status"] == "LOW_BINARY_RANK_CERTIFICATE", "Low-rank verdict")
    verify_spread(spread)
    coordinates, coloring = c["coordinates"], c["coloring"]
    require(len(coordinates) == len(coloring) == n, "Coordinate lengths")
    require(all(type(x) is int and 0 <= x < 64 for x in coordinates), "Coordinate range")
    require(all(type(x) is int and 0 <= x < 9 for x in coloring), "Color range")
    for i, x in enumerate(coordinates):
        expected = 0
        for k, (u, v) in enumerate(pairs):
            expected |= (u >> i & 1) << k
            expected |= (v >> i & 1) << (k+3)
        require(x == expected, "Factor/coordinate transport")
        require((x == 0 and coloring[i] == spread["zero_color"]) or x in spread["classes"][coloring[i]], "Spread color transport")
    for i, j in combinations(range(n), 2):
        require(form(coordinates[i], coordinates[j]) == matrix[i][j], "Physical form mismatch")
        require(coloring[i] != coloring[j] or matrix[i][j] == 0, "Improper coloring")
    classes = [[i for i in range(n) if coloring[i] == color] for color in range(9)]
    largest = min(classes, key=lambda part: (-len(part), part))
    require(c["largest_class"] == largest and len(largest)*9 >= n, "Pigeonhole class")
    witness = c["independent_five"]
    require(witness == (largest[:5] if len(largest) >= 5 else []), "Witness extraction")
    if witness:
        require(all(matrix[u][v] == 0 for u, v in combinations(witness, 2)), "Physical witness not independent")
        require(c["witness_color_in_input"] == ("blue" if c["adjacency_color"] == "red" else "red"), "Witness color")
    else:
        require(n <= 36 and c["witness_color_in_input"] is None, "Missing guaranteed witness")
    return rank


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    graph, certificate = json.loads(args.graph.read_text()), json.loads(args.certificate.read_text())
    spread = json.loads(Path(__file__).with_name("spread.json").read_text())
    rank = verify(graph, certificate, spread)
    print(json.dumps({"status": "VERIFIED", "binary_rank": rank, "certificate_status": certificate["status"]}, indent=2))
