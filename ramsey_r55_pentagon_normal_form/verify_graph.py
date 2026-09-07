#!/usr/bin/env python3
"""Standalone full physical five-set counts by two different algorithms."""
import argparse
import itertools as it
import json
from pathlib import Path


def read(path):
    rows = [list(map(int, line.split())) for line in Path(path).read_text().splitlines()]
    if not rows or len(rows[0]) != 2:
        raise ValueError("graph header")
    n, m = rows[0]
    if not 1 <= n <= 63 or m < 0 or len(rows) != m + 1:
        raise ValueError("graph dimensions")
    edges = set()
    for row in rows[1:]:
        if len(row) != 2:
            raise ValueError("edge row")
        u, v = row
        if not 0 <= u < v < n or (u, v) in edges:
            raise ValueError("edge domain")
        edges.add((u, v))
    return n, edges


def count_cliques(adj, candidates, size):
    if size == 0:
        return 1
    total = 0
    while candidates.bit_count() >= size:
        bit = candidates & -candidates; candidates ^= bit
        total += count_cliques(adj, candidates & adj[bit.bit_length() - 1], size - 1)
    return total


def verify_graph(n, edges):
    # Literal physical sets: examine all ten unordered pairs in each five-set.
    direct = [0, 0]
    for s in it.combinations(range(n), 5):
        first = int((s[0], s[1]) in edges)
        if all(int(e in edges) == first for e in it.combinations(s, 2)):
            direct[first] += 1
    # Independent bit-intersection clique recursion in each color.
    adj = [[0] * n, [0] * n]
    for u, v in it.combinations(range(n), 2):
        c = int((u, v) in edges)
        adj[c][u] |= 1 << v; adj[c][v] |= 1 << u
    recursive = [count_cliques(a, (1 << n) - 1, 5) for a in adj]
    if direct != recursive:
        raise ValueError("physical clique count disagreement")
    return {"status": "VERIFIED_PHYSICAL_GRAPH_COUNTS", "n": n, "red_edges": len(edges),
            "blue_five_sets": direct[0], "red_five_sets": direct[1],
            "ramsey_5_5": direct == [0, 0]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify_graph(*read(args.graph)), sort_keys=True))
