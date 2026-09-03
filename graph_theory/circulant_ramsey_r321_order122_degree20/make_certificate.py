#!/usr/bin/env python3
"""Create a red-graph DIMACS certificate from blue circulant distances."""

from __future__ import annotations

import argparse
from pathlib import Path


def circular_distance(n: int, u: int, v: int) -> int:
    delta = abs(u - v)
    return min(delta, n - delta)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--blue-distances", type=int, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    n = args.order
    blue = set(args.blue_distances)
    if len(blue) != len(args.blue_distances):
        raise ValueError("duplicate distance")
    if not blue or min(blue) < 1 or max(blue) > n // 2:
        raise ValueError("distance outside canonical range")

    edges = [(u + 1, v + 1) for u in range(n) for v in range(u + 1, n)
             if circular_distance(n, u, v) not in blue]
    with args.output.open("w") as handle:
        handle.write(f"c Blue circulant distances: {sorted(blue)}\n")
        handle.write(f"p edge {n} {len(edges)}\n")
        for u, v in edges:
            handle.write(f"e {u} {v}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
