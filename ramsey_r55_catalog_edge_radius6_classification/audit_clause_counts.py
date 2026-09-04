#!/usr/bin/env python3
"""Independently audit radius-six formula counts on selected parents."""

import argparse
from itertools import combinations
from math import comb


def decode_graph6(record: str) -> list[int]:
    if not record:
        raise ValueError("empty graph6 record")
    order = ord(record[0]) - 63
    if order != 42:
        raise ValueError(f"expected order 42, got {order}")
    bits = []
    for char in record[1:]:
        value = ord(char) - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 byte")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    if len(bits) < order * (order - 1) // 2:
        raise ValueError("truncated graph6 record")
    adjacency = [0] * order
    at = 0
    for high in range(1, order):
        for low in range(high):
            if bits[at]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            at += 1
    return adjacency


def edge_histogram(adjacency: list[int]) -> list[int]:
    histogram = [0] * 11
    for vertices in combinations(range(42), 5):
        edges = sum(
            bool(adjacency[vertices[i]] & (1 << vertices[j]))
            for i in range(5)
            for j in range(i + 1, 5)
        )
        histogram[edges] += 1
    return histogram


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog")
    parser.add_argument("parent_counts")
    parser.add_argument("parents", nargs="*", type=int, default=[0, 15])
    args = parser.parse_args()

    with open(args.catalog, encoding="ascii") as source:
        catalog = source.read().splitlines()
    if len(catalog) != 328:
        raise RuntimeError("expected 328 catalog records")

    logged = {}
    with open(args.parent_counts, encoding="ascii") as source:
        for line in source:
            fields = dict(field.split("=", 1) for field in line.split())
            logged[int(fields["parent"])] = fields
    if sorted(logged) != list(range(328)):
        raise RuntimeError("parent counts do not cover 0,...,327 exactly")

    parents = args.parents or [0, 15]
    if len(set(parents)) != len(parents):
        raise RuntimeError("duplicate parent index")
    for parent in parents:
        if not 0 <= parent < 328:
            raise RuntimeError(f"bad parent index: {parent}")
        histogram = edge_histogram(decode_graph6(catalog[parent]))
        if sum(histogram) != comb(42, 5):
            raise RuntimeError(f"five-set count mismatch at parent {parent}")
        if histogram[0] or histogram[10]:
            raise RuntimeError(f"catalog parent {parent} has a homogeneous 5-set")
        ramsey_clauses = sum(
            count * ((edges >= 4) + (edges <= 6))
            for edges, count in enumerate(histogram)
        )
        fields = logged[parent]
        if int(fields["ramsey_clauses"]) != ramsey_clauses:
            raise RuntimeError(f"Ramsey-clause mismatch at parent {parent}")
        if int(fields["clauses"]) != ramsey_clauses + 12042:
            raise RuntimeError(f"total-clause mismatch at parent {parent}")
        if int(fields["variables"]) != 6888:
            raise RuntimeError(f"variable-count mismatch at parent {parent}")

    print(
        f"clause_count_audit={len(parents)}/{len(parents)} "
        f"parents={','.join(map(str, parents))}"
    )


if __name__ == "__main__":
    main()
