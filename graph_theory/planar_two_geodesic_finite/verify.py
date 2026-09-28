#!/usr/bin/env python3
"""Definition-level cross-check of the optimized geodesic-mask checker."""

from __future__ import annotations

import argparse
import json
import sys

from check import decode_graph6, distances, find_separator, largest_component


def direct_geodesics(adj: list[int]) -> set[int]:
    d = distances(adj)
    n = len(adj)
    paths: set[int] = set()
    for start in range(n):
        stack = [(start, 1 << start, 0)]
        while stack:
            u, mask, length = stack.pop()
            if d[start][u] == length:
                paths.add(mask)
            for v in range(n):
                if adj[u] & (1 << v) and not mask & (1 << v):
                    if length + 1 <= d[start][v]:
                        stack.append((v, mask | (1 << v), length + 1))
    return paths


def direct_separator(adj: list[int]) -> bool:
    masks = sorted(direct_geodesics(adj))
    n = len(adj)
    for p in masks:
        for q in masks:
            if 2 * largest_component(adj, p | q) <= n:
                return True
    return False


def complete_minus_edge(n: int) -> list[int]:
    adj = [((1 << n) - 1) & ~(1 << v) for v in range(n)]
    adj[0] &= ~(1 << 1)
    adj[1] &= ~(1 << 0)
    return adj


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--diameter-at-most", type=int)
    args = parser.parse_args()
    count = 0
    selected = 0
    for raw in sys.stdin.buffer:
        adj = decode_graph6(raw)
        if len(adj) != args.order:
            raise ValueError("unexpected graph order")
        if args.diameter_at_most is not None:
            d = distances(adj)
            if any(x < 0 or x > args.diameter_at_most for row in d for x in row):
                count += 1
                continue
        selected += 1
        expected = direct_separator(adj)
        observed = find_separator(adj) is not None
        if expected != observed:
            raise AssertionError(f"checker disagreement on {raw!r}")
        if not expected:
            raise AssertionError(f"unbalanced graph on {raw!r}")
        count += 1
    if count == 0:
        raise ValueError("empty input")
    assert direct_separator(complete_minus_edge(10))
    assert not direct_separator(complete_minus_edge(11))
    assert find_separator(complete_minus_edge(10)) is not None
    assert find_separator(complete_minus_edge(11)) is None
    print(json.dumps({"order": args.order, "independent_records": count, "selected_records": selected, "controls": "K10-e yes; K11-e no"}, sort_keys=True))


if __name__ == "__main__":
    main()
