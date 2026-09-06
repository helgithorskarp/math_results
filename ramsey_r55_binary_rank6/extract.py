#!/usr/bin/env python3
"""Decode low binary adjacency rank into a coloring and physical obstruction."""
import argparse
import json
from pathlib import Path


def graph_rows(data):
    if not isinstance(data, dict) or set(data) != {"n", "edges"}:
        raise ValueError("Graph must have precisely n and edges")
    n, edges = data["n"], data["edges"]
    if type(n) is not int or n < 1 or not isinstance(edges, list):
        raise ValueError("Invalid graph order/edges")
    rows, previous = [0]*n, (-1, -1)
    for edge in edges:
        if not isinstance(edge, list) or len(edge) != 2 or any(type(x) is not int for x in edge):
            raise ValueError("Invalid pair")
        u, v = edge
        if not 0 <= u < v < n or (u, v) <= previous:
            raise ValueError("Pairs must be increasing, sorted, unique and in range")
        rows[u] |= 1 << v
        rows[v] |= 1 << u
        previous = u, v
    return rows


def factor(rows):
    residual, pairs, n = list(rows), [], len(rows)
    while any(residual):
        p = next(i for i, row in enumerate(residual) if row)
        q = (residual[p] & -residual[p]).bit_length()-1
        u = sum(((row >> p) & 1) << i for i, row in enumerate(residual))
        v = sum(((row >> q) & 1) << i for i, row in enumerate(residual))
        pairs.append([u, v])
        for i in range(n):
            residual[i] ^= (v if u >> i & 1 else 0) ^ (u if v >> i & 1 else 0)
    return pairs


def extract(data, color="red"):
    rows = graph_rows(data)
    if color not in ("red", "blue"):
        raise ValueError("Unknown color")
    n = len(rows)
    if color == "blue":
        rows = [row ^ (((1 << n)-1) ^ (1 << i)) for i, row in enumerate(rows)]
    pairs = factor(rows)
    result = {"n": n, "adjacency_color": color, "binary_rank": 2*len(pairs), "factor_pairs": pairs}
    if len(pairs) > 3:
        return {**result, "status": "OUTSIDE_RANK_SIX"}
    spread = json.loads(Path(__file__).with_name("spread.json").read_text())
    colors = {0: spread["zero_color"]}
    for c, vectors in enumerate(spread["classes"]):
        for vector in vectors:
            colors[vector] = c
    coordinates = [sum(((u >> i) & 1) << j | ((v >> i) & 1) << (j+3)
                       for j, (u, v) in enumerate(pairs)) for i in range(n)]
    coloring = [colors[x] for x in coordinates]
    classes = [[i for i, c in enumerate(coloring) if c == j] for j in range(9)]
    largest = min(classes, key=lambda part: (-len(part), part))
    witness = largest[:5] if len(largest) >= 5 else []
    return {**result, "status": "LOW_BINARY_RANK_CERTIFICATE", "coordinates": coordinates,
            "coloring": coloring, "largest_class": largest, "independent_five": witness,
            "witness_color_in_input": ("blue" if color == "red" else "red") if witness else None}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    parser.add_argument("--color", choices=["red", "blue"], default="red")
    args = parser.parse_args()
    print(json.dumps(extract(json.loads(args.graph.read_text()), args.color), indent=2))
