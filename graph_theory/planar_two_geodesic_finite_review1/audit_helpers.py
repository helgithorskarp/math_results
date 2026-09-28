#!/usr/bin/env python3
"""Independent small-input checks for the order-11 finite review."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path


CHECKER = Path(__file__).resolve().parents[1] / "planar_two_geodesic_finite" / "check.py"
spec = importlib.util.spec_from_file_location("author_checker", CHECKER)
assert spec is not None and spec.loader is not None
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def direct_largest_component(adj: list[int], deleted: int) -> int:
    """Count components using vertex sets, separately from the bitset routine."""
    remaining = {v for v in range(len(adj)) if not deleted & (1 << v)}
    largest = 0
    while remaining:
        start = remaining.pop()
        seen = {start}
        frontier = [start]
        while frontier:
            u = frontier.pop()
            for v in list(remaining):
                if adj[u] & (1 << v):
                    remaining.remove(v)
                    seen.add(v)
                    frontier.append(v)
        largest = max(largest, len(seen))
    return largest


def check_components() -> int:
    """Exhaust every labeled five-vertex graph and deleted vertex set."""
    pairs = [(u, v) for v in range(5) for u in range(v)]
    checks = 0
    for graph_mask in range(1 << len(pairs)):
        adj = [0] * 5
        for i, (u, v) in enumerate(pairs):
            if graph_mask & (1 << i):
                adj[u] |= 1 << v
                adj[v] |= 1 << u
        for deleted in range(1 << 5):
            assert checker.largest_component(adj, deleted) == direct_largest_component(adj, deleted)
            checks += 1
    return checks


def check_graph6_against_ascii(plantri: str) -> int:
    """Compare two plantri encodings of its full order-seven class."""
    base = [plantri, "-p", "-c1m1", "7"]
    ascii_lines = subprocess.run(
        [base[0], "-a", *base[1:]], capture_output=True, check=True
    ).stdout.splitlines()
    graph6_lines = subprocess.run(
        [base[0], "-g", *base[1:]], capture_output=True, check=True
    ).stdout.splitlines()
    assert len(ascii_lines) == len(graph6_lines) == 2014
    for ascii_line, graph6_line in zip(ascii_lines, graph6_lines):
        order, body = ascii_line.decode("ascii").split(" ", 1)
        assert order == "7"
        rows = body.split(",")
        assert len(rows) == 7
        expected = [sum(1 << (ord(c) - 97) for c in row) for row in rows]
        assert checker.decode_graph6(graph6_line) == expected
    return len(ascii_lines)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 audit_helpers.py /path/to/plantri")
    print(f"component comparisons: {check_components()}")
    print(f"ASCII/graph6 record comparisons: {check_graph6_against_ascii(sys.argv[1])}")
