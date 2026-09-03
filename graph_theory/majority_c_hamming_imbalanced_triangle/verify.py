#!/usr/bin/env python3
"""Exact checker for the moderately imbalanced 3D Hamming theorem."""

from __future__ import annotations

import argparse
import hashlib
from collections import deque
from dataclasses import dataclass
from itertools import product


Cell = tuple[int, int]
Piece = frozenset[Cell]


@dataclass
class Edge:
    to: int
    rev: int
    cap: int


class Dinic:
    """Small deterministic integral max-flow implementation."""

    def __init__(self, size: int) -> None:
        self.graph: list[list[Edge]] = [[] for _ in range(size)]

    def add_edge(self, source: int, target: int, capacity: int) -> Edge:
        forward = Edge(target, len(self.graph[target]), capacity)
        reverse = Edge(source, len(self.graph[source]), 0)
        self.graph[source].append(forward)
        self.graph[target].append(reverse)
        return forward

    def max_flow(self, source: int, target: int) -> int:
        total = 0
        size = len(self.graph)
        while True:
            level = [-1] * size
            level[source] = 0
            queue = deque([source])
            while queue:
                vertex = queue.popleft()
                for edge in self.graph[vertex]:
                    if edge.cap and level[edge.to] < 0:
                        level[edge.to] = level[vertex] + 1
                        queue.append(edge.to)
            if level[target] < 0:
                return total

            cursor = [0] * size

            def augment(vertex: int, amount: int) -> int:
                if vertex == target:
                    return amount
                while cursor[vertex] < len(self.graph[vertex]):
                    edge = self.graph[vertex][cursor[vertex]]
                    if edge.cap and level[edge.to] == level[vertex] + 1:
                        sent = augment(edge.to, min(amount, edge.cap))
                        if sent:
                            edge.cap -= sent
                            self.graph[edge.to][edge.rev].cap += sent
                            return sent
                    cursor[vertex] += 1
                return 0

            while (sent := augment(source, 10**30)) != 0:
                total += sent


def _ceil_div(numerator: int, denominator: int) -> int:
    return (numerator + denominator - 1) // denominator


def _bounded_composition(total: int, count: int, lower: int, upper: int) -> list[int]:
    """Return a deterministic bounded integer composition."""

    assert count * lower <= total <= count * upper
    values = [lower] * count
    remaining = total - count * lower
    for index in range(count):
        addition = min(remaining, upper - lower)
        values[index] += addition
        remaining -= addition
    assert remaining == 0
    return values


def _residual_cells(m: int, n: int, row_degree: int, degrees: list[int]) -> set[Cell]:
    """Realize the prescribed bipartite degree sequence by integral flow."""

    assert len(degrees) == n
    assert sum(degrees) == m * row_degree
    source = 0
    row_start = 1
    col_start = row_start + m
    target = col_start + n
    flow = Dinic(target + 1)
    for row in range(m):
        flow.add_edge(source, row_start + row, row_degree)
    tracked: list[tuple[int, int, Edge]] = []
    for row in range(m):
        for col in range(n):
            edge = flow.add_edge(row_start + row, col_start + col, 1)
            tracked.append((row, col, edge))
    for col, degree in enumerate(degrees):
        flow.add_edge(col_start + col, target, degree)
    value = flow.max_flow(source, target)
    if value != m * row_degree:
        raise AssertionError("Gale--Ryser degree sequence failed to realize")
    return {(row, col) for row, col, edge in tracked if edge.cap == 0}


def star_partition(m: int, n: int, s: int) -> list[Piece]:
    """Partition an m by n grid into floor(m*n/s) row/column pieces."""

    if not (m >= n >= s >= 1):
        raise ValueError("expected m >= n >= s >= 1")
    row_piece_count, row_remainder = divmod(n, s)
    if row_remainder == 0:
        return [
            frozenset((row, col) for col in range(start, start + s))
            for row in range(m)
            for start in range(0, n, s)
        ]

    column_piece_count, extra = divmod(m * row_remainder, s)
    per_column_capacity = m // s
    used_columns = max(
        row_remainder,
        _ceil_div(column_piece_count, per_column_capacity),
    )
    assert row_remainder <= used_columns <= min(n, column_piece_count)

    group_counts = _bounded_composition(
        column_piece_count,
        used_columns,
        lower=1,
        upper=per_column_capacity,
    )
    slacks = [m - s * count for count in group_counts]
    assert sum(slacks) >= extra
    additions = [0] * used_columns
    remaining = extra
    for index, slack in enumerate(slacks):
        additions[index] = min(remaining, slack)
        remaining -= additions[index]
    assert remaining == 0

    degrees = [
        s * group_counts[index] + additions[index]
        for index in range(used_columns)
    ] + [0] * (n - used_columns)
    residual = _residual_cells(m, n, row_remainder, degrees)

    pieces: list[Piece] = []
    for row in range(m):
        ordinary = [(row, col) for col in range(n) if (row, col) not in residual]
        assert len(ordinary) == row_piece_count * s
        for start in range(0, len(ordinary), s):
            pieces.append(frozenset(ordinary[start : start + s]))

    for col in range(used_columns):
        selected = sorted(cell for cell in residual if cell[1] == col)
        count = group_counts[col]
        cursor = 0
        for group in range(count):
            size = s if group + 1 < count else s + additions[col]
            pieces.append(frozenset(selected[cursor : cursor + size]))
            cursor += size
        assert cursor == len(selected)

    return pieces


def validate_star_partition(m: int, n: int, s: int, pieces: list[Piece]) -> None:
    expected = {(row, col) for row in range(m) for col in range(n)}
    seen: set[Cell] = set()
    assert len(pieces) == (m * n) // s
    for piece in pieces:
        assert len(piece) >= s
        assert not (seen & piece)
        rows = {row for row, _ in piece}
        columns = {col for _, col in piece}
        assert len(rows) == 1 or len(columns) == 1
        seen.update(piece)
    assert seen == expected


def theorem_parameters(n1: int, n2: int, n3: int) -> tuple[int, int, int]:
    if not (n1 >= n2 >= n3 >= 2):
        raise ValueError("expected n1 >= n2 >= n3 >= 2")
    degree = n1 + n2 + n3 - 3
    threshold = (degree + 1) // 2
    if threshold < n1 - 1:
        raise ValueError("the theorem requires h >= n1-1")
    r = threshold - (n1 - 1)
    return threshold, r + 1, (n2 * n3) // (r + 1)


def verify_shell_bound(n1: int, n2: int, n3: int) -> tuple[int, int]:
    """Exhaust every local line-count profile and return profile statistics."""

    threshold, s, _ = theorem_parameters(n1, n2, n3)
    caps = (n1 - 1, n2 - 1, n3 - 1)
    target_twice = 2 * n1 * s
    checked = 0
    equality = 0
    for a1 in range(caps[0] + 1):
        for a2 in range(caps[1] + 1):
            for a3 in range(caps[2] + 1):
                values = (a1, a2, a3)
                total = sum(values)
                if total < threshold:
                    continue
                checked += 1
                lower_twice = 2 * (1 + total) + sum(
                    value * (threshold - value) for value in values
                )
                assert lower_twice >= target_twice
                equality += lower_twice == target_twice
    return checked, equality


def direct_majority_check(n1: int, n2: int, n3: int, pieces: list[Piece]) -> None:
    """Lift pieces and check the colouring from the graph definition."""

    threshold, _, expected_classes = theorem_parameters(n1, n2, n3)
    classes = [
        {(x1, x2, x3) for x1 in range(n1) for x2, x3 in piece}
        for piece in pieces
    ]
    assert len(classes) == expected_classes
    vertices = set(product(range(n1), range(n2), range(n3)))
    assert set().union(*classes) == vertices
    assert sum(map(len, classes)) == len(vertices)
    for colour_class in classes:
        for vertex in colour_class:
            internal = 0
            for coordinate, bound in enumerate((n1, n2, n3)):
                for value in range(bound):
                    if value == vertex[coordinate]:
                        continue
                    neighbour = list(vertex)
                    neighbour[coordinate] = value
                    internal += tuple(neighbour) in colour_class
            assert internal >= threshold


def verify_range(max_side: int, direct_max_side: int) -> tuple[int, int, int, str]:
    records: list[str] = []
    triples = 0
    profiles = 0
    direct_triples = 0
    for n3 in range(2, max_side + 1):
        for n2 in range(n3, max_side + 1):
            for n1 in range(n2, max_side + 1):
                degree = n1 + n2 + n3 - 3
                threshold = (degree + 1) // 2
                if threshold < n1 - 1:
                    continue
                threshold, s, class_count = theorem_parameters(n1, n2, n3)
                pieces = star_partition(n2, n3, s)
                validate_star_partition(n2, n3, s, pieces)
                checked, equality = verify_shell_bound(n1, n2, n3)
                profiles += checked
                triples += 1
                if n1 <= direct_max_side:
                    direct_majority_check(n1, n2, n3, pieces)
                    direct_triples += 1
                sizes = ",".join(map(str, sorted(map(len, pieces))))
                records.append(
                    f"{n1},{n2},{n3};h={threshold};s={s};q={class_count};"
                    f"profiles={checked};equality={equality};sizes={sizes}"
                )
    digest = hashlib.sha256("\n".join(records).encode()).hexdigest()
    return triples, profiles, direct_triples, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-side", type=int, default=24)
    parser.add_argument("--direct-max-side", type=int, default=8)
    args = parser.parse_args()
    if args.max_side < 2:
        parser.error("--max-side must be at least 2")
    if not 2 <= args.direct_max_side <= args.max_side:
        parser.error("--direct-max-side must lie between 2 and --max-side")
    triples, profiles, direct, digest = verify_range(
        args.max_side,
        args.direct_max_side,
    )
    print(
        f"VERIFIED triples={triples}; shell_profiles={profiles}; "
        f"direct_triples={direct}; max_side={args.max_side}; "
        f"sha256={digest}"
    )


if __name__ == "__main__":
    main()
