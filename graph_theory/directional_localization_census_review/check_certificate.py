#!/usr/bin/env python3
"""Independent semantic check of the retained directional-localization witnesses.

This checker intentionally imports no code from the contribution under review.
It uses adjacency matrices, Floyd--Warshall distances, and tuple/set response
partitions rather than the submitted mask/BFS implementations.
"""

from __future__ import annotations

import argparse
import json
from functools import lru_cache
from itertools import combinations
from pathlib import Path


def decode_graph6(record: str) -> list[list[bool]]:
    data = record.encode("ascii")
    if not data or not 63 <= data[0] <= 125:
        raise ValueError("only nonempty, one-byte-order graph6 records are supported")
    order = data[0] - 63
    bits: list[int] = []
    for byte in data[1:]:
        if not 63 <= byte <= 126:
            raise ValueError("invalid graph6 byte")
        value = byte - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = order * (order - 1) // 2
    if len(bits) < needed:
        raise ValueError("truncated graph6 record")
    adjacency = [[False] * order for _ in range(order)]
    position = 0
    for column in range(1, order):
        for row in range(column):
            adjacency[row][column] = adjacency[column][row] = bool(bits[position])
            position += 1
    return adjacency


class Game:
    def __init__(self, adjacency: list[list[bool]]) -> None:
        self.adjacency = adjacency
        self.order = len(adjacency)
        infinity = self.order + 1
        self.distance = [
            [0 if u == v else 1 if adjacency[u][v] else infinity for v in range(self.order)]
            for u in range(self.order)
        ]
        for middle in range(self.order):
            for source in range(self.order):
                through = self.distance[source][middle]
                for target in range(self.order):
                    self.distance[source][target] = min(
                        self.distance[source][target], through + self.distance[middle][target]
                    )
        if any(value == infinity for row in self.distance for value in row):
            raise ValueError("graph is disconnected")

        self.responses = [
            [self._response(probe, robber) for robber in range(self.order)]
            for probe in range(self.order)
        ]
        self.actions = list(combinations(range(self.order), 2))
        self.signatures = [
            [tuple(self.responses[probe][robber] for probe in action) for robber in range(self.order)]
            for action in self.actions
        ]
        self.partitions = [self._partition(signatures) for signatures in self.signatures]

    def _response(self, probe: int, robber: int) -> tuple[int, ...]:
        if probe == robber:
            return (probe,)
        response = tuple(
            neighbor
            for neighbor in range(self.order)
            if self.adjacency[probe][neighbor]
            and self.distance[neighbor][robber] + 1 == self.distance[probe][robber]
        )
        if not response:
            raise AssertionError("full-feedback response is empty")
        return response

    @staticmethod
    def _partition(signatures: list[tuple[tuple[int, ...], ...]]) -> tuple[frozenset[int], ...]:
        cells: dict[tuple[tuple[int, ...], ...], set[int]] = {}
        for robber, signature in enumerate(signatures):
            cells.setdefault(signature, set()).add(robber)
        return tuple(frozenset(cell) for cell in cells.values())

    @lru_cache(maxsize=None)
    def closure(self, cell: frozenset[int]) -> frozenset[int]:
        return frozenset(
            vertex
            for robber in cell
            for vertex in range(self.order)
            if vertex == robber or self.adjacency[robber][vertex]
        )

    @lru_cache(maxsize=None)
    def has_resolving_action(self, belief: frozenset[int]) -> bool:
        return any(
            len({signatures[robber] for robber in belief}) == len(belief)
            for signatures in self.signatures
        )

    @lru_cache(maxsize=None)
    def wins_within(self, belief: frozenset[int], phases: int) -> bool:
        if len(belief) <= 1:
            return True
        if phases == 0:
            return False
        if phases == 1:
            return self.has_resolving_action(belief)
        for partition in self.partitions:
            for cell in partition:
                possible = belief & cell
                if len(possible) > 1 and not self.wins_within(self.closure(possible), phases - 1):
                    break
            else:
                return True
        return False

    def capture_rank(self, maximum: int) -> int | None:
        initial = frozenset(range(self.order))
        for phases in range(maximum + 1):
            if self.wins_within(initial, phases):
                return phases
        return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path, help="submitted expected_results.json")
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text(encoding="utf-8"))

    checked_rows = 0
    checked_graphs = 0
    witnesses: list[tuple[int, str]] = []
    for family, rows in certificate["families"].items():
        for row in rows:
            total = int(row["graphs"])
            rank_total = sum(int(count) for count in row["rank_counts"].values())
            if rank_total != total:
                raise AssertionError(f"{family} order {row['order']}: rank counts do not sum")
            records = row.get("rank_3_graph6", [])
            if len(records) != int(row["rank_counts"].get("3", 0)):
                raise AssertionError(f"{family} order {row['order']}: witness count mismatch")
            witnesses.extend((int(row["order"]), record) for record in records)
            checked_rows += 1
            checked_graphs += total

    records = [record for _, record in witnesses]
    if len(records) != 71 or len(set(records)) != 71:
        raise AssertionError("expected 71 distinct retained rank-three records")

    ranks_by_order: dict[int, int] = {}
    for order, record in witnesses:
        adjacency = decode_graph6(record)
        if len(adjacency) != order:
            raise AssertionError("graph6 order disagrees with certificate")
        if any(sum(row) != 3 for row in adjacency):
            raise AssertionError("retained witness is not cubic")
        rank = Game(adjacency).capture_rank(3)
        if rank != 3:
            raise AssertionError(f"{record}: expected exact rank 3, found {rank}")
        ranks_by_order[order] = ranks_by_order.get(order, 0) + 1

    print(
        json.dumps(
            {
                "certificate_rows": checked_rows,
                "advertised_graphs": checked_graphs,
                "verified_exact_rank_3": len(witnesses),
                "witnesses_by_order": ranks_by_order,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
