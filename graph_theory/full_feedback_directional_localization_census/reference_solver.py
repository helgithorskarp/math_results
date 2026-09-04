#!/usr/bin/env python3
"""Definition-level exhaustive checker for the optimized C++ solver.

The reference algorithm enumerates the entire nonempty belief lattice.  It is
intentionally slower and structurally different from the bounded-depth C++
search.  With ``--compare`` it checks every connected unlabeled graph through
the requested order, entry by entry.
"""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
from collections import Counter, deque


def decode_graph6(record: bytes) -> list[int]:
    data = record.strip()
    if data.startswith(b">>graph6<<"):
        data = data[len(b">>graph6<<") :]
    if not data:
        raise ValueError("empty graph6 record")
    order = data[0] - 63
    if not 0 <= order <= 62:
        raise ValueError("only one-byte graph6 orders are supported")
    bits: list[int] = []
    for byte in data[1:]:
        value = byte - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 byte")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    required = order * (order - 1) // 2
    if len(bits) < required:
        raise ValueError("truncated graph6 record")
    adjacency = [0] * order
    position = 0
    for column in range(1, order):
        for row in range(column):
            if bits[position]:
                adjacency[row] |= 1 << column
                adjacency[column] |= 1 << row
            position += 1
    return adjacency


def encode_graph6(adjacency: list[int]) -> bytes:
    order = len(adjacency)
    if not 0 <= order <= 62:
        raise ValueError("only one-byte graph6 orders are supported")
    bits = [
        (adjacency[row] >> column) & 1
        for column in range(1, order)
        for row in range(column)
    ]
    while len(bits) % 6:
        bits.append(0)
    payload = bytearray([order + 63])
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = 2 * value + bit
        payload.append(value + 63)
    return bytes(payload)


class ExhaustiveGame:
    """Full-feedback game solved by least fixed point on all beliefs."""

    def __init__(self, adjacency: list[int]) -> None:
        self.adjacency = adjacency
        self.order = len(adjacency)
        if self.order == 0:
            raise ValueError("graph must be nonempty")
        self.full = (1 << self.order) - 1
        self.closed = [adjacency[v] | (1 << v) for v in range(self.order)]
        self.distances = self._all_pairs_distances()
        self.responses = self._full_responses()
        self.closure = [0] * (1 << self.order)
        for mask in range(1, 1 << self.order):
            bit = mask & -mask
            self.closure[mask] = self.closure[mask ^ bit] | self.closed[bit.bit_length() - 1]

    def _all_pairs_distances(self) -> list[list[int]]:
        result = []
        for source in range(self.order):
            distance = [-1] * self.order
            distance[source] = 0
            queue = deque([source])
            while queue:
                vertex = queue.popleft()
                remaining = self.adjacency[vertex]
                while remaining:
                    bit = remaining & -remaining
                    remaining ^= bit
                    neighbor = bit.bit_length() - 1
                    if distance[neighbor] < 0:
                        distance[neighbor] = distance[vertex] + 1
                        queue.append(neighbor)
            if any(value < 0 for value in distance):
                raise ValueError("graph must be connected")
            result.append(distance)
        return result

    def _full_responses(self) -> list[list[int]]:
        responses = [[0] * self.order for _ in range(self.order)]
        for probe in range(self.order):
            for robber in range(self.order):
                if probe == robber:
                    responses[probe][robber] = 1 << probe
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
                    raise AssertionError("empty full-feedback response")
                responses[probe][robber] = response
        return responses

    def partitions(self, cops: int) -> list[list[int]]:
        partitions = []
        for size in range(1, min(cops, self.order) + 1):
            for action in itertools.combinations(range(self.order), size):
                classes: dict[tuple[int, ...], int] = {}
                for robber in range(self.order):
                    signature = tuple(self.responses[probe][robber] for probe in action)
                    classes[signature] = classes.get(signature, 0) | (1 << robber)
                partitions.append(list(classes.values()))
        return partitions

    def capture_rank(self, cops: int = 2) -> int | None:
        rank = [-1] * (1 << self.order)
        for vertex in range(self.order):
            rank[1 << vertex] = 0
        if rank[self.full] == 0:
            return 0
        partitions = self.partitions(cops)
        next_rank = 1
        while True:
            additions = []
            for belief in range(1, 1 << self.order):
                if rank[belief] >= 0:
                    continue
                for classes in partitions:
                    if all(
                        (cell := belief & class_mask).bit_count() <= 1
                        or rank[self.closure[cell]] >= 0
                        for class_mask in classes
                    ):
                        additions.append(belief)
                        break
            if not additions:
                return None
            for belief in additions:
                rank[belief] = next_rank
            if rank[self.full] >= 0:
                return rank[self.full]
            next_rank += 1


def parse_cpp_rows(output: bytes) -> dict[bytes, int]:
    rows: dict[bytes, int] = {}
    for line in output.splitlines():
        fields = line.split(b"\t")
        if len(fields) != 5 or fields[2] != b"WIN":
            raise AssertionError(f"unexpected C++ row: {line!r}")
        rows[fields[0]] = int(fields[3])
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare", required=True, help="path to compiled dirloc_solver")
    parser.add_argument("--geng", required=True, help="path to nauty geng")
    parser.add_argument("--max-order", type=int, default=8)
    args = parser.parse_args()
    if not 1 <= args.max_order <= 10:
        raise SystemExit("--max-order must lie in 1..10 (8 is the practical default)")

    summary = []
    total = 0
    for order in range(1, args.max_order + 1):
        generated = subprocess.run(
            [args.geng, "-cq", str(order)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout
        cpp = subprocess.run(
            [args.compare, "--all", "--max-rounds", "3"],
            check=True,
            input=generated,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        cpp_rows = parse_cpp_rows(cpp.stdout)
        ranks: Counter[int] = Counter()
        records = generated.splitlines()
        if len(cpp_rows) != len(records):
            raise AssertionError("C++ output did not contain one row per graph")
        for record in records:
            adjacency = decode_graph6(record)
            if encode_graph6(adjacency) != record:
                raise AssertionError(f"graph6 round trip failed for {record!r}")
            reference_rank = ExhaustiveGame(adjacency).capture_rank(2)
            if reference_rank is None or cpp_rows[record] != reference_rank:
                raise AssertionError(
                    f"rank mismatch for {record.decode()}: reference={reference_rank}, "
                    f"optimized={cpp_rows[record]}"
                )
            ranks[reference_rank] += 1
        total += len(records)
        summary.append({"order": order, "graphs": len(records), "rank_counts": dict(sorted(ranks.items()))})
    print(json.dumps({"checked_graphs": total, "orders": summary}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
