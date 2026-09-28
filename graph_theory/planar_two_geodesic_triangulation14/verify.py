#!/usr/bin/env python3
"""Exact order-13/14 triangulation cut certificate, standard library only.

Input is the graph6 stream from plantri 5.8 `plantri -g ORDER`.
The script independently decodes every record and filters diameter at most two.
"""

from __future__ import annotations

import argparse
from itertools import combinations
import json
import sys


EXCEPTIONS = {
    "L|eKKE@oJ_bp?~": ((0, 1), (3, 11, 6)),
    "L|fIID@SJ_aEFx": ((0, 1), (3, 12, 6)),
}
ROTATIONS = {
    # Explicit clockwise neighbour lists, vertex labels a=0,...,m=12.
    "L|eKKE@oJ_bp?~":
        "bcdefghij,ajkc,abkd,ackle,adlf,aelg,aflmh,agmi,ahmj,aimkb,bjmldc,dkmgfe,glkjih",
    "L|fIID@SJ_aEFx":
        "bcdef,afghijkc,abkd,ackjlme,admf,aemgb,bfmh,bgmi,bhmlj,bildk,bjdc,djim,dlihgfe",
}
EXPECTED = {
    13: {"records": 49566, "diameter_two": 1532, "three_cut": 1010,
         "four_cut_only": 520, "exceptions": 2,
         "exception_edge_deletions_diameter_two": 27},
    14: {"records": 339722, "diameter_two": 3908, "three_cut": 3043,
         "four_cut_only": 865, "exceptions": 0,
         "exception_edge_deletions_diameter_two": 0},
}


def decode_graph6(record: bytes, order: int) -> list[int]:
    record = record.strip()
    if record.startswith(b">>graph6<<"):
        record = record[10:]
    if not record or record[0] != order + 63:
        raise ValueError("incorrect graph6 order")
    bit_count = order * (order - 1) // 2
    if len(record) != 1 + (bit_count + 5) // 6:
        raise ValueError("incorrect graph6 length")
    data = record[1:]
    if any(not 63 <= byte <= 126 for byte in data):
        raise ValueError("invalid graph6 byte")
    adj = [0] * order
    bit = 0
    for v in range(1, order):
        for u in range(v):
            if ((data[bit // 6] - 63) >> (5 - bit % 6)) & 1:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
            bit += 1
    while bit < 6 * len(data):
        if ((data[bit // 6] - 63) >> (5 - bit % 6)) & 1:
            raise ValueError("nonzero graph6 padding")
        bit += 1
    if sum(mask.bit_count() for mask in adj) != 2 * (3 * order - 6):
        raise ValueError("record does not have triangulation edge count")
    return adj


def diameter_at_most_two(adj: list[int]) -> bool:
    for v in range(len(adj)):
        for u in range(v):
            if not (adj[u] & (1 << v)) and not (adj[u] & adj[v]):
                return False
    return True


def largest_component(adj: list[int], deleted: int, cutoff: int) -> int:
    unseen = ((1 << len(adj)) - 1) & ~deleted
    largest = 0
    while unseen:
        start = unseen & -unseen
        unseen ^= start
        frontier = start
        size = 0
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            size += 1
            if size > cutoff:
                return size
            u = bit.bit_length() - 1
            fresh = adj[u] & unseen
            frontier |= fresh
            unseen &= ~fresh
        largest = max(largest, size)
    return largest


def has_half_cut(adj: list[int], size: int) -> bool:
    cutoff = len(adj) // 2
    for vertices in combinations(range(len(adj)), size):
        mask = sum(1 << v for v in vertices)
        if largest_component(adj, mask, cutoff) <= cutoff:
            return True
    return False


def distance(adj: list[int], source: int, target: int) -> int:
    seen = 1 << source
    frontier = seen
    steps = 0
    while frontier:
        if frontier & (1 << target):
            return steps
        fresh = 0
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            fresh |= adj[bit.bit_length() - 1]
        frontier = fresh & ~seen
        seen |= frontier
        steps += 1
    return -1


def check_planar_rotation(record: str, adj: list[int]) -> None:
    rotations = [[ord(ch) - ord("a") for ch in item]
                 for item in ROTATIONS[record].split(",")]
    if len(rotations) != len(adj):
        raise AssertionError("rotation order mismatch")
    for u, neighbours in enumerate(rotations):
        if len(neighbours) != len(set(neighbours)):
            raise AssertionError("duplicate neighbour in rotation")
        if set(neighbours) != {v for v in range(len(adj)) if adj[u] & (1 << v)}:
            raise AssertionError("rotation does not match graph6")
    darts = {(u, v) for u in range(len(adj)) for v in rotations[u]}
    seen: set[tuple[int, int]] = set()
    faces = 0
    while len(seen) < len(darts):
        start = min(darts - seen)
        dart = start
        length = 0
        while True:
            if dart in seen:
                raise AssertionError("rotation traversal reused dart")
            seen.add(dart)
            u, v = dart
            around = rotations[v]
            dart = (v, around[(around.index(u) - 1) % len(around)])
            length += 1
            if dart == start:
                break
        if length != 3:
            raise AssertionError("nontriangular face in rotation")
        faces += 1
    if len(adj) - len(darts) // 2 + faces != 2:
        raise AssertionError("rotation has nonplanar Euler characteristic")


def check_exception(record: str, adj: list[int]) -> int:
    check_planar_rotation(record, adj)
    paths = EXCEPTIONS[record]
    for path in paths:
        if len(path) != len(set(path)):
            raise AssertionError("repeated path vertex")
        if any(not (adj[x] & (1 << y)) for x, y in zip(path, path[1:])):
            raise AssertionError("path edge missing")
        if distance(adj, path[0], path[-1]) != len(path) - 1:
            raise AssertionError("path is not geodesic")
    deleted = 0
    for path in paths:
        for x in path:
            deleted |= 1 << x
    if largest_component(adj, deleted, len(adj) // 2) > len(adj) // 2:
        raise AssertionError("exception pair fails half balance")
    diameter_two_deletions = 0
    for u in range(len(adj)):
        for v in range(u + 1, len(adj)):
            if not adj[u] & (1 << v):
                continue
            reduced = adj.copy()
            reduced[u] &= ~(1 << v)
            reduced[v] &= ~(1 << u)
            if diameter_at_most_two(reduced):
                diameter_two_deletions += 1
                if not has_half_cut(reduced, 4):
                    raise AssertionError(f"single-edge deletion {u}-{v} lacks four-cut")
    return diameter_two_deletions


def verify(order: int) -> dict[str, int]:
    counts = {key: 0 for key in EXPECTED[order]}
    exceptions_seen: set[str] = set()
    for raw in sys.stdin.buffer:
        if not raw.strip():
            raise ValueError("empty graph6 line")
        record = raw.strip().decode("ascii")
        adj = decode_graph6(raw, order)
        counts["records"] += 1
        if not diameter_at_most_two(adj):
            continue
        counts["diameter_two"] += 1
        if has_half_cut(adj, 3):
            counts["three_cut"] += 1
        elif has_half_cut(adj, 4):
            counts["four_cut_only"] += 1
        else:
            counts["exceptions"] += 1
            if record not in EXCEPTIONS or order != 13 or record in exceptions_seen:
                raise AssertionError(f"unexpected exception: {record}")
            exceptions_seen.add(record)
            counts["exception_edge_deletions_diameter_two"] += check_exception(record, adj)
    if order == 13 and exceptions_seen != set(EXCEPTIONS):
        raise AssertionError("missing exception record")
    if counts != EXPECTED[order]:
        raise AssertionError(f"count mismatch: {counts} != {EXPECTED[order]}")
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--order", type=int, choices=(13, 14), required=True)
    args = parser.parse_args()
    result = verify(args.order)
    print(json.dumps({"order": args.order, **result}, sort_keys=True))


if __name__ == "__main__":
    main()
