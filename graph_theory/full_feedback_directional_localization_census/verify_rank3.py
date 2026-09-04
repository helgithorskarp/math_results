#!/usr/bin/env python3
"""Independently verify all stored cubic rank-three witnesses.

This implementation uses arbitrary-precision Python integers and a recursive
bounded-game search.  It shares the mathematical recurrence, but no search
code, with ``dirloc_solver.cpp``.
"""

from __future__ import annotations

import argparse
import json
from collections import deque
from itertools import combinations
from pathlib import Path

from reference_solver import decode_graph6


class BoundedDirectionalGame:
    def __init__(self, adjacency: list[int]) -> None:
        self.adjacency = adjacency
        self.n = len(adjacency)
        if self.n < 2:
            raise ValueError("bounded two-cop solver expects at least two vertices")
        self.full = (1 << self.n) - 1
        self.closed = [adjacency[v] | (1 << v) for v in range(self.n)]
        self.distances = self._distances()
        self.responses = self._responses()
        self.actions = list(combinations(range(self.n), 2))
        self.partitions = self._partitions()
        self.pair_bits = [[0] * self.n for _ in range(self.n)]
        for index, (u, v) in enumerate(combinations(range(self.n), 2)):
            self.pair_bits[u][v] = self.pair_bits[v][u] = 1 << index
        self.collisions = self._collisions()
        # Trying the finest global partitions first is only an ordering heuristic.
        order = sorted(range(len(self.actions)), key=lambda i: len(self.partitions[i]), reverse=True)
        self.actions = [self.actions[i] for i in order]
        self.partitions = [self.partitions[i] for i in order]
        self.collisions = [self.collisions[i] for i in order]
        self.pair_cache: dict[int, int] = {}
        self.closure_cache: dict[int, int] = {}
        self.resolver_cache: dict[int, int | None] = {}
        self.memo: dict[tuple[int, int], bool] = {}
        self.strategy: dict[tuple[int, int], int] = {}

    def _distances(self) -> list[list[int]]:
        result = []
        for source in range(self.n):
            distance = [-1] * self.n
            distance[source] = 0
            queue = deque([source])
            while queue:
                v = queue.popleft()
                remaining = self.adjacency[v]
                while remaining:
                    bit = remaining & -remaining
                    remaining ^= bit
                    w = bit.bit_length() - 1
                    if distance[w] < 0:
                        distance[w] = distance[v] + 1
                        queue.append(w)
            if any(value < 0 for value in distance):
                raise ValueError("graph must be connected")
            result.append(distance)
        return result

    def _responses(self) -> list[list[int]]:
        result = [[0] * self.n for _ in range(self.n)]
        for probe in range(self.n):
            for robber in range(self.n):
                if probe == robber:
                    result[probe][robber] = 1 << probe
                    continue
                target = self.distances[probe][robber] - 1
                neighbors = self.adjacency[probe]
                response = 0
                while neighbors:
                    bit = neighbors & -neighbors
                    neighbors ^= bit
                    if self.distances[bit.bit_length() - 1][robber] == target:
                        response |= bit
                if response == 0:
                    raise AssertionError("empty directional response")
                result[probe][robber] = response
        return result

    def _partitions(self) -> list[list[int]]:
        result = []
        for p, q in self.actions:
            classes: dict[tuple[int, int], int] = {}
            for robber in range(self.n):
                signature = (self.responses[p][robber], self.responses[q][robber])
                classes[signature] = classes.get(signature, 0) | (1 << robber)
            result.append(list(classes.values()))
        return result

    def _collisions(self) -> list[int]:
        result = []
        for classes in self.partitions:
            collision = 0
            for class_mask in classes:
                members = []
                remaining = class_mask
                while remaining:
                    bit = remaining & -remaining
                    remaining ^= bit
                    members.append(bit.bit_length() - 1)
                for u, v in combinations(members, 2):
                    collision |= self.pair_bits[u][v]
            result.append(collision)
        return result

    def induced_pairs(self, belief: int) -> int:
        if belief not in self.pair_cache:
            members = []
            remaining = belief
            while remaining:
                bit = remaining & -remaining
                remaining ^= bit
                members.append(bit.bit_length() - 1)
            pairs = 0
            for u, v in combinations(members, 2):
                pairs |= self.pair_bits[u][v]
            self.pair_cache[belief] = pairs
        return self.pair_cache[belief]

    def resolver(self, belief: int) -> int | None:
        if belief not in self.resolver_cache:
            pairs = self.induced_pairs(belief)
            self.resolver_cache[belief] = next(
                (index for index, collision in enumerate(self.collisions) if not (pairs & collision)),
                None,
            )
        return self.resolver_cache[belief]

    def closure(self, cell: int) -> int:
        if cell not in self.closure_cache:
            result = 0
            remaining = cell
            while remaining:
                bit = remaining & -remaining
                remaining ^= bit
                result |= self.closed[bit.bit_length() - 1]
            self.closure_cache[cell] = result
        return self.closure_cache[cell]

    def wins_within(self, belief: int, rounds: int) -> bool:
        if belief.bit_count() <= 1:
            return True
        if rounds <= 0:
            return False
        key = (belief, rounds)
        if key in self.memo:
            return self.memo[key]
        if rounds == 1:
            action = self.resolver(belief)
            answer = action is not None
            if answer:
                self.strategy[key] = action
            self.memo[key] = answer
            return answer
        for action, classes in enumerate(self.partitions):
            succeeds = True
            for class_mask in classes:
                cell = belief & class_mask
                if cell.bit_count() > 1 and not self.wins_within(self.closure(cell), rounds - 1):
                    succeeds = False
                    break
            if succeeds:
                self.strategy[key] = action
                self.memo[key] = True
                return True
        self.memo[key] = False
        return False

    def capture_rank(self, maximum: int) -> int | None:
        for rounds in range(maximum + 1):
            if self.wins_within(self.full, rounds):
                return rounds
        return None


def validate_simple_graph(adjacency: list[int]) -> None:
    order = len(adjacency)
    allowed = (1 << order) - 1
    for vertex, neighbors in enumerate(adjacency):
        if neighbors & ~allowed:
            raise AssertionError("adjacency contains an out-of-range vertex")
        if neighbors & (1 << vertex):
            raise AssertionError("graph6 record contains a loop")
        remaining = neighbors
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            neighbor = bit.bit_length() - 1
            if not adjacency[neighbor] & (1 << vertex):
                raise AssertionError("adjacency is not symmetric")


def verify_record(record: bytes, expected_order: int) -> dict[str, object]:
    adjacency = decode_graph6(record)
    validate_simple_graph(adjacency)
    if len(adjacency) != expected_order:
        raise AssertionError(f"expected order {expected_order}, found {len(adjacency)}")
    degrees = [neighbors.bit_count() for neighbors in adjacency]
    if degrees != [3] * expected_order:
        raise AssertionError(f"expected a cubic graph, found degrees {degrees}")

    game = BoundedDirectionalGame(adjacency)
    rank = game.capture_rank(3)
    if rank != 3:
        raise AssertionError(f"expected exact capture rank 3, found {rank}")
    root_action_index = game.strategy.get((game.full, 3))
    if root_action_index is None:
        raise AssertionError("rank-three strategy has no root action")
    return {
        "graph6": record.decode("ascii"),
        "order": len(adjacency),
        "degree": 3,
        "capture_rank": rank,
        "root_probe_pair_zero_based": list(game.actions[root_action_index]),
        "memoized_states": len(game.memo),
        "closure_cache_entries": len(game.closure_cache),
        "resolver_cache_entries": len(game.resolver_cache),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--expected-results",
        type=Path,
        default=Path(__file__).with_name("expected_results.json"),
        help="census JSON containing the graph6 witnesses",
    )
    args = parser.parse_args()
    certificate = json.loads(args.expected_results.read_text(encoding="utf-8"))
    ordered_records: list[tuple[int, bytes]] = []
    for row in certificate["families"]["connected_cubic"]:
        expected_count = int(row["rank_counts"].get("3", 0))
        records = [record.encode("ascii") for record in row.get("rank_3_graph6", [])]
        if len(records) != expected_count:
            raise AssertionError(
                f"order {row['order']}: stored {len(records)} rank-three records, expected {expected_count}"
            )
        ordered_records.extend((int(row["order"]), record) for record in records)
    flat_records = [record for _, record in ordered_records]
    if len(flat_records) != 71 or len(set(flat_records)) != 71:
        raise AssertionError("the certificate must contain exactly 71 distinct rank-three records")

    smallest = {
        line.strip()
        for line in Path(__file__).with_name("rank3_cubic18.g6").read_bytes().splitlines()
        if line.strip()
    }
    if smallest != {record for order, record in ordered_records if order == 18}:
        raise AssertionError("the separate order-18 witness file disagrees with the census JSON")

    results = [verify_record(record, order) for order, record in ordered_records]
    by_order = []
    for order in sorted({int(result["order"]) for result in results}):
        group = [result for result in results if result["order"] == order]
        by_order.append(
            {
                "order": order,
                "verified_witnesses": len(group),
                "total_memoized_states": sum(int(result["memoized_states"]) for result in group),
                "maximum_memoized_states": max(int(result["memoized_states"]) for result in group),
            }
        )
    print(json.dumps({"verified_witnesses": len(results), "orders": by_order}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
