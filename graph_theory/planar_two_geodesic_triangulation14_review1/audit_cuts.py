#!/usr/bin/env python3
"""Independent ASCII-stream census of diameter-two triangulation cuts."""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations
import json
import subprocess


def parse_ascii(record: bytes, order: int) -> list[set[int]]:
    label, body = record.decode("ascii").strip().split(" ", 1)
    assert int(label) == order
    listed = [[ord(c) - ord("a") for c in item] for item in body.split(",")]
    assert all(len(row) == len(set(row)) for row in listed)
    assert all(0 <= v < order for row in listed for v in row)
    rows = [set(row) for row in listed]
    assert len(rows) == order
    assert all(u in rows[v] for u, row in enumerate(rows) for v in row)
    assert sum(map(len, rows)) == 2 * (3 * order - 6)
    return rows


def diameter_two(adj: list[set[int]]) -> bool:
    return all(
        v in adj[u] or bool(adj[u] & adj[v])
        for v in range(len(adj))
        for u in range(v)
    )


def balanced_cut(adj: list[set[int]], size: int) -> bool:
    n = len(adj)
    edges = [(u, v) for u, row in enumerate(adj) for v in row if u < v]
    cutoff = n // 2
    for vertices in combinations(range(n), size):
        removed = set(vertices)
        parent = list(range(n))

        def root(v: int) -> int:
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v

        for u, v in edges:
            if u not in removed and v not in removed:
                parent[root(u)] = root(v)
        sizes: dict[int, int] = {}
        for v in range(n):
            if v not in removed:
                r = root(v)
                sizes[r] = sizes.get(r, 0) + 1
        if max(sizes.values(), default=0) <= cutoff:
            return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plantri", help="path to plantri 5.8 binary")
    parser.add_argument("--order", type=int, choices=(13, 14), required=True)
    args = parser.parse_args()
    process = subprocess.Popen(
        [args.plantri, "-a", str(args.order)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdout is not None
    counts = {
        "order": args.order,
        "records": 0,
        "diameter_two": 0,
        "three_cut": 0,
        "four_cut_only": 0,
        "no_four_cut": 0,
    }
    digest = sha256()
    for record in process.stdout:
        digest.update(record)
        adj = parse_ascii(record, args.order)
        counts["records"] += 1
        if not diameter_two(adj):
            continue
        counts["diameter_two"] += 1
        if balanced_cut(adj, 3):
            counts["three_cut"] += 1
        elif balanced_cut(adj, 4):
            counts["four_cut_only"] += 1
        else:
            counts["no_four_cut"] += 1
    assert process.wait() == 0
    assert process.stderr is not None
    assert b"triangulations written" in process.stderr.read()
    counts["ascii_stream_sha256"] = digest.hexdigest()
    print(json.dumps(counts, sort_keys=True))


if __name__ == "__main__":
    main()
