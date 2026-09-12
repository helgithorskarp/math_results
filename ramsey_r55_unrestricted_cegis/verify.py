#!/usr/bin/env python3
"""Definition-level verifier for physical two-colour complete graphs."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


def edge_pairs(n: int):
    return itertools.combinations(range(n), 2)


def decode_hex(n: int, text: str) -> list[int]:
    edge_count = n * (n - 1) // 2
    expected_digits = (edge_count + 3) // 4
    text = text.strip().lower()
    if len(text) != expected_digits or any(c not in "0123456789abcdef" for c in text):
        raise ValueError("invalid hexadecimal graph length or character")
    # The producer writes low nibbles first, unlike ordinary integer hex.
    bits = []
    for char in text:
        digit = int(char, 16)
        bits.extend((digit >> shift) & 1 for shift in range(4))
    if any(bits[edge_count:]):
        raise ValueError("nonzero padding bit")
    del bits[edge_count:]
    return bits


def decode_graph6(text: str) -> tuple[int, list[int]]:
    raw = text.strip().encode("ascii")
    if not raw or raw.startswith(b">>"):
        raise ValueError("only one short graph6 record is accepted")
    n = raw[0] - 63
    if not 0 <= n <= 62:
        raise ValueError("invalid short graph6 order")
    payload = raw[1:]
    required = (n * (n - 1) // 2 + 5) // 6
    if len(payload) != required or any(not 63 <= byte <= 126 for byte in payload):
        raise ValueError("invalid graph6 payload")
    stream = []
    for byte in payload:
        word = byte - 63
        stream.extend((word >> shift) & 1 for shift in range(5, -1, -1))
    matrix = [[0] * n for _ in range(n)]
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            matrix[low][high] = matrix[high][low] = stream[cursor]
            cursor += 1
    bits = [matrix[a][b] for a, b in edge_pairs(n)]
    if any(stream[cursor:]):
        raise ValueError("nonzero graph6 padding bit")
    return n, bits


def audit(n: int, bits: list[int]) -> dict:
    edge_count = n * (n - 1) // 2
    if len(bits) != edge_count or any(bit not in (0, 1) for bit in bits):
        raise ValueError("invalid physical edge vector")
    adjacency = [[0] * n for _ in range(n)]
    degrees = [0] * n
    for bit, (a, b) in zip(bits, edge_pairs(n), strict=True):
        adjacency[a][b] = adjacency[b][a] = bit
        degrees[a] += bit
        degrees[b] += bit

    red_bad = 0
    blue_bad = 0
    first_red = None
    first_blue = None
    checked = 0
    for five in itertools.combinations(range(n), 5):
        red_edges = sum(adjacency[five[i]][five[j]]
                        for i in range(5) for j in range(i + 1, 5))
        checked += 1
        if red_edges == 10:
            red_bad += 1
            if first_red is None:
                first_red = list(five)
        elif red_edges == 0:
            blue_bad += 1
            if first_blue is None:
                first_blue = list(five)
    return {
        "status": "GOOD_GRAPH" if red_bad + blue_bad == 0 else "NOT_GOOD_GRAPH",
        "n": n,
        "physical_edges": edge_count,
        "red_edges": sum(bits),
        "degrees": degrees,
        "five_subsets_checked": checked,
        "red_K5": red_bad,
        "blue_K5": blue_bad,
        "first_red_K5": first_red,
        "first_blue_K5": first_blue,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--graph6", type=Path)
    source.add_argument("--hex", dest="hex_graph")
    parser.add_argument("--n", type=int)
    parser.add_argument("--expect", choices=("good", "bad"))
    args = parser.parse_args()
    if args.graph6 is not None:
        if args.n is not None:
            parser.error("--n is incompatible with --graph6")
        records = args.graph6.read_text(encoding="ascii").splitlines()
        if len(records) != 1:
            raise SystemExit("expected exactly one graph6 record")
        n, bits = decode_graph6(records[0])
    else:
        if args.n is None:
            parser.error("--n is required with --hex")
        n, bits = args.n, decode_hex(args.n, args.hex_graph)
    report = audit(n, bits)
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    if args.expect == "good" and report["status"] != "GOOD_GRAPH":
        raise SystemExit(1)
    if args.expect == "bad" and report["status"] != "NOT_GOOD_GRAPH":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
