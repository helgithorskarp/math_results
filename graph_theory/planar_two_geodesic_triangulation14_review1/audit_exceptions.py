#!/usr/bin/env python3
"""Independent ASCII/graph6 and edge-deletion audit of the two exceptions."""

from __future__ import annotations

import argparse
from collections import deque
from itertools import combinations
import json
import subprocess


EXCEPTIONS = {
    "L|eKKE@oJ_bp?~": ((0, 1), (3, 11, 6)),
    "L|fIID@SJ_aEFx": ((0, 1), (3, 12, 6)),
}


def ascii_adjacency(record: bytes) -> list[list[int]]:
    order, body = record.decode("ascii").split(" ", 1)
    assert order == "13"
    rows = [[ord(c) - ord("a") for c in item] for item in body.split(",")]
    assert len(rows) == 13
    assert all(len(row) == len(set(row)) for row in rows)
    assert all(u in rows[v] for u, row in enumerate(rows) for v in row)
    return rows


def graph6_adjacency(record: str) -> list[set[int]]:
    assert record[0] == "L"
    bits = "".join(f"{ord(c) - 63:06b}" for c in record[1:])
    assert len(bits) >= 13 * 12 // 2
    assert set(bits[13 * 12 // 2 :]) <= {"0"}
    adj = [set() for _ in range(13)]
    bit = 0
    for v in range(1, 13):
        for u in range(v):
            if bits[bit] == "1":
                adj[u].add(v)
                adj[v].add(u)
            bit += 1
    return adj


def face_orders(rotation: list[list[int]]) -> list[int]:
    unseen = {(u, v) for u, row in enumerate(rotation) for v in row}
    orders = []
    while unseen:
        start = next(iter(unseen))
        dart = start
        length = 0
        while True:
            assert dart in unseen
            unseen.remove(dart)
            u, v = dart
            row = rotation[v]
            dart = (v, row[(row.index(u) - 1) % len(row)])
            length += 1
            if dart == start:
                break
        orders.append(length)
    return orders


def distance(adj: list[set[int]], source: int, target: int) -> int:
    seen = {source}
    queue = deque([(source, 0)])
    while queue:
        u, d = queue.popleft()
        if u == target:
            return d
        for v in adj[u] - seen:
            seen.add(v)
            queue.append((v, d + 1))
    return 10**6


def diameter_two(adj: list[set[int]]) -> bool:
    return all(distance(adj, u, v) <= 2 for u in range(13) for v in range(u))


def largest_component(adj: list[set[int]], removed: set[int]) -> int:
    parent = list(range(13))

    def root(v: int) -> int:
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for u in range(13):
        if u in removed:
            continue
        for v in adj[u]:
            if v not in removed:
                parent[root(u)] = root(v)
    sizes: dict[int, int] = {}
    for v in range(13):
        if v not in removed:
            r = root(v)
            sizes[r] = sizes.get(r, 0) + 1
    return max(sizes.values(), default=0)


def half_cut(adj: list[set[int]], size: int) -> bool:
    return any(
        largest_component(adj, set(vertices)) <= 6
        for vertices in combinations(range(13), size)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plantri", help="path to plantri 5.8 binary")
    args = parser.parse_args()
    g_lines = subprocess.run(
        [args.plantri, "-g", "13"], capture_output=True, check=True
    ).stdout.splitlines()
    a_lines = subprocess.run(
        [args.plantri, "-a", "13"], capture_output=True, check=True
    ).stdout.splitlines()
    assert len(g_lines) == len(a_lines) == 49566
    found = {}
    for index, (g_line, a_line) in enumerate(zip(g_lines, a_lines)):
        record = g_line.decode("ascii")
        if record not in EXCEPTIONS:
            continue
        rotation = ascii_adjacency(a_line)
        adj = [set(row) for row in rotation]
        assert adj == graph6_adjacency(record)
        edge_count = sum(len(row) for row in adj) // 2
        faces = face_orders(rotation)
        assert edge_count == 33 and len(faces) == 22
        assert all(length == 3 for length in faces)
        assert 13 - edge_count + len(faces) == 2
        assert diameter_two(adj)
        assert not half_cut(adj, 4)
        paths = EXCEPTIONS[record]
        for path in paths:
            assert all(v in adj[u] for u, v in zip(path, path[1:]))
            assert distance(adj, path[0], path[-1]) == len(path) - 1
        largest = largest_component(adj, set(paths[0]) | set(paths[1]))
        assert largest == 6
        surviving_deletions = 0
        for u in range(13):
            for v in adj[u]:
                if u >= v:
                    continue
                reduced = [set(row) for row in adj]
                reduced[u].remove(v)
                reduced[v].remove(u)
                if diameter_two(reduced):
                    surviving_deletions += 1
                    assert half_cut(reduced, 4)
        found[record] = {
            "record_index": index,
            "triangular_faces": len(faces),
            "largest_after_pair": largest,
            "diameter_two_edge_deletions_with_four_cut": surviving_deletions,
        }
    assert set(found) == set(EXCEPTIONS)
    assert [
        found[record]["diameter_two_edge_deletions_with_four_cut"]
        for record in EXCEPTIONS
    ] == [15, 12]
    print(json.dumps(found, sort_keys=True))


if __name__ == "__main__":
    main()
