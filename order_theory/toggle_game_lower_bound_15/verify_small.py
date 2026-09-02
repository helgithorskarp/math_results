#!/usr/bin/env python3
"""Definition-level verifier for finite-lattice toggle-game catalogues.

This intentionally uses Python sets and frozensets, unlike the production
C++ bit-matrix/bit-state implementation.
"""

from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path


def parse_cover_list(line: str) -> tuple[list[tuple[int, int]], int]:
    import ast

    pairs = ast.literal_eval(line)
    edges = [(int(lower), int(upper)) for lower, upper in pairs]
    vertices = 1 + max(x for edge in edges for x in edge)
    return edges, vertices


def parse_cats(line: str, order: int) -> list[tuple[int, int]]:
    line = line.strip()
    assert len(line) == order * (order - 1) // 2
    edges = []
    for b in range(2, order + 1):
        for a in range(1, b):
            pos = (b - 1) * (b - 2) // 2 + a - 1
            assert line[pos] in ".1"
            if line[pos] == "1":
                edges.append((b - 1, a - 1))
    return edges


def transitive_order(order: int, covers: list[tuple[int, int]]) -> set[tuple[int, int]]:
    leq = {(x, x) for x in range(order)} | set(covers)
    changed = True
    while changed:
        changed = False
        additions = {
            (x, z)
            for x, y in leq
            for y2, z in leq
            if y == y2 and (x, z) not in leq
        }
        if additions:
            leq |= additions
            changed = True
    return leq


def mobius_to_top(order: int, leq: set[tuple[int, int]], top: int) -> dict[int, int]:
    mu: dict[int, int] = {top: 1}

    def value(x: int) -> int:
        if x not in mu:
            mu[x] = -sum(value(y) for y in range(order) if x != y and (x, y) in leq)
        return mu[x]

    for x in range(order):
        value(x)
    return mu


def winning_sequence(order: int, covers: list[tuple[int, int]], top: int):
    leq = transitive_order(order, covers)
    assert all((x, top) in leq for x in range(order))
    mu = mobius_to_top(order, leq, top)
    ideals = {
        move: frozenset(x for x in range(order) if (x, move) in leq)
        for move in range(order)
        if move != top and mu[move] != 0
    }
    start = frozenset()
    goal = frozenset(set(range(order)) - {top})
    parent: dict[frozenset[int], tuple[frozenset[int], int] | None] = {start: None}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        if state == goal:
            sequence = []
            while parent[state] is not None:
                old, move = parent[state]
                sequence.append(move)
                state = old
            return list(reversed(sequence))
        for move, ideal in ideals.items():
            if state.isdisjoint(ideal) or ideal <= state:
                nxt = state ^ ideal
                if nxt not in parent:
                    parent[nxt] = (state, move)
                    queue.append(nxt)
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("order", type=int)
    ap.add_argument("catalogue", type=Path)
    ap.add_argument("format", choices=("covers", "cats"))
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()
    checked = 0
    for line in args.catalogue.read_text().splitlines():
        if not line:
            continue
        if args.format == "covers":
            covers, parsed_order = parse_cover_list(line)
            assert parsed_order == args.order
            top = 1
        else:
            covers = parse_cats(line, args.order)
            top = 0
        sequence = winning_sequence(args.order, covers, top)
        if sequence is None:
            raise SystemExit(f"FAIL unwinnable index={checked + 1}")
        checked += 1
        if args.limit is not None and checked >= args.limit:
            break
    print(f"PASS independent order={args.order} checked={checked}")


if __name__ == "__main__":
    main()
