#!/usr/bin/env python3
"""Exact two-geodesic half-separator test for graph6 streams (n <= 62)."""

from __future__ import annotations

import argparse
import json
import sys


def decode_graph6(line: bytes) -> list[int]:
    line = line.strip()
    if line.startswith(b">>graph6<<"):
        line = line[len(b">>graph6<<") :]
    if not line or line[0] < 63 or line[0] > 125:
        raise ValueError("invalid graph6 record")
    n = line[0] - 63
    if n > 62:
        raise ValueError("only one-byte graph6 orders are supported")
    m = n * (n - 1) // 2
    if len(line) != 1 + (m + 5) // 6:
        raise ValueError("wrong graph6 record length")
    bits = []
    for c in line[1:]:
        if c < 63 or c > 126:
            raise ValueError("invalid graph6 byte")
        bits.extend((c - 63 >> k) & 1 for k in range(5, -1, -1))
    if any(bits[m:]):
        raise ValueError("nonzero graph6 padding")
    adj = [0] * n
    idx = 0
    # graph6 reads the upper triangle column by column.
    for v in range(1, n):
        for u in range(v):
            if bits[idx]:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
            idx += 1
    return adj


def distances(adj: list[int]) -> list[list[int]]:
    n = len(adj)
    answer = []
    for source in range(n):
        d = [-1] * n
        d[source] = 0
        queue = [source]
        for u in queue:
            nb = adj[u]
            while nb:
                bit = nb & -nb
                nb -= bit
                v = bit.bit_length() - 1
                if d[v] < 0:
                    d[v] = d[u] + 1
                    queue.append(v)
        answer.append(d)
    return answer


def geodesic_masks(adj: list[int], d: list[list[int]]) -> set[int]:
    n = len(adj)
    masks = {1 << v for v in range(n)}
    for s in range(n):
        for t in range(s + 1, n):
            if d[s][t] < 0:
                continue

            def visit(u: int, mask: int) -> None:
                if u == t:
                    masks.add(mask)
                    return
                nb = adj[u]
                while nb:
                    bit = nb & -nb
                    nb -= bit
                    v = bit.bit_length() - 1
                    if d[s][v] == d[s][u] + 1 and d[s][v] + d[v][t] == d[s][t]:
                        visit(v, mask | bit)

            visit(s, 1 << s)
    return masks


def largest_component(adj: list[int], deleted: int) -> int:
    unseen = ((1 << len(adj)) - 1) & ~deleted
    largest = 0
    while unseen:
        bit = unseen & -unseen
        unseen -= bit
        frontier = bit
        size = 0
        while frontier:
            b = frontier & -frontier
            frontier -= b
            size += 1
            u = b.bit_length() - 1
            fresh = adj[u] & unseen
            frontier |= fresh
            unseen &= ~fresh
        largest = max(largest, size)
    return largest


def two_disjoint_three_vertex_geodesics(adj: list[int]) -> tuple[int, int] | None:
    # If n <= 12, two disjoint length-two paths delete six vertices and
    # immediately meet the half threshold. Their endpoints are nonadjacent.
    n = len(adj)
    if n > 12:
        return None
    paths: list[int] = []
    for u in range(n):
        for v in range(u + 1, n):
            if adj[u] & (1 << v):
                continue
            common = adj[u] & adj[v]
            while common:
                bit = common & -common
                common -= bit
                mask = (1 << u) | (1 << v) | bit
                for earlier in paths:
                    if earlier & mask == 0:
                        return earlier, mask
                paths.append(mask)
    return None


def find_separator(adj: list[int], d: list[list[int]] | None = None) -> tuple[int, int] | None:
    n = len(adj)
    if n == 0:
        return (0, 0)
    quick = two_disjoint_three_vertex_geodesics(adj)
    if quick is not None:
        return quick
    if d is None:
        d = distances(adj)
    masks = geodesic_masks(adj, d)
    # If P is contained in another geodesic Q, Q dominates P for vertex
    # deletion. Keep only inclusion-maximal masks, with no loss of pairs.
    maximal: list[int] = []
    for mask in sorted(masks, key=lambda x: (-x.bit_count(), x)):
        if not any(mask & other == mask for other in maximal):
            maximal.append(mask)
    cache: dict[int, bool] = {}
    for i, p in enumerate(maximal):
        for q in maximal[i:]:
            union = p | q
            good = cache.get(union)
            if good is None:
                good = 2 * largest_component(adj, union) <= n
                cache[union] = good
            if good:
                return (p, q)
    return None


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
        d = distances(adj)
        if args.diameter_at_most is not None:
            if any(x < 0 or x > args.diameter_at_most for row in d for x in row):
                count += 1
                continue
        selected += 1
        if find_separator(adj, d) is None:
            result = {"order": args.order, "records_before_failure": count, "graph6": raw.decode().strip()}
            print(json.dumps(result, sort_keys=True))
            raise SystemExit(1)
        count += 1
    if not count:
        raise ValueError("empty input")
    print(json.dumps({"order": args.order, "plane_graph_records_checked": count, "selected_records": selected, "failures": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
