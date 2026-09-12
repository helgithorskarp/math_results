#!/usr/bin/env python3
"""Independent physical verifier for the bundled two-colour graph.

This file deliberately imports neither factorization.py nor its helpers.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path


def main() -> None:
    text = Path(__file__).with_name("calibration_good42.hex").read_text(
        encoding="ascii").strip().lower()
    n = 42
    edge_count = n * (n - 1) // 2
    if len(text) != (edge_count + 3) // 4:
        raise RuntimeError("wrong hexadecimal length")
    stream: list[int] = []
    for char in text:
        if char not in "0123456789abcdef":
            raise RuntimeError("non-hexadecimal character")
        value = int(char, 16)
        stream.extend((value >> shift) & 1 for shift in range(4))
    if any(stream[edge_count:]):
        raise RuntimeError("nonzero padding")
    del stream[edge_count:]

    adjacency = [[0] * n for _ in range(n)]
    degrees = [0] * n
    cursor = 0
    for u in range(n):
        for v in range(u + 1, n):
            color = stream[cursor]
            cursor += 1
            adjacency[u][v] = adjacency[v][u] = color
            degrees[u] += color
            degrees[v] += color

    red_bad = blue_bad = checked = 0
    for five in itertools.combinations(range(n), 5):
        red_edges = 0
        for u, v in itertools.combinations(five, 2):
            red_edges += adjacency[u][v]
        red_bad += red_edges == 10
        blue_bad += red_edges == 0
        checked += 1

    report = {
        "status": "GOOD_GRAPH" if red_bad + blue_bad == 0 else "NOT_GOOD_GRAPH",
        "n": n,
        "physical_edges": edge_count,
        "red_edges": sum(stream),
        "degree_min": min(degrees),
        "degree_max": max(degrees),
        "five_subsets_checked": checked,
        "red_K5": red_bad,
        "blue_K5": blue_bad,
    }
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    if report != {
        "status": "GOOD_GRAPH",
        "n": 42,
        "physical_edges": 861,
        "red_edges": 427,
        "degree_min": 19,
        "degree_max": 22,
        "five_subsets_checked": 850668,
        "red_K5": 0,
        "blue_K5": 0,
    }:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
