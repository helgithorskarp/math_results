#!/usr/bin/env python3
"""Independently reconstruct and check every radius-five map entry."""

import argparse
from collections import Counter


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


def contains_clique(adjacency: list[int], wanted: int = 5) -> bool:
    def search(candidates: int, remaining: int) -> bool:
        if candidates.bit_count() < remaining:
            return False
        if remaining == 1:
            return bool(candidates)
        while candidates.bit_count() >= remaining:
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length() - 1
            if search(candidates & adjacency[vertex], remaining - 1):
                return True
        return False

    return search((1 << len(adjacency)) - 1, wanted)


def complement(adjacency: list[int]) -> list[int]:
    mask = (1 << len(adjacency)) - 1
    return [mask ^ (1 << vertex) ^ row for vertex, row in enumerate(adjacency)]


def parse_edge(text: str) -> tuple[int, int]:
    fields = text.split(",")
    if len(fields) != 2:
        raise ValueError(f"bad edge: {text}")
    low, high = map(int, fields)
    if not 0 <= low < high < 42:
        raise ValueError(f"bad edge: {text}")
    return low, high


def edge_index(edge: tuple[int, int]) -> int:
    low, high = edge
    return high * (high - 1) // 2 + low


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog")
    parser.add_argument("map")
    args = parser.parse_args()

    with open(args.catalog, encoding="ascii") as source:
        catalog = [
            decode_graph6(line.rstrip("\n"))
            for line in source
            if line.rstrip("\n")
        ]
    if len(catalog) != 328:
        raise RuntimeError("expected 328 catalog records")

    per_parent = Counter()
    seen = set()
    target_kinds = Counter()
    targets = set()
    checked = 0
    summary = None
    with open(args.map, encoding="ascii") as source:
        header = source.readline().rstrip("\n")
        expected_header = (
            "parent\tedge_1\tedge_2\tedge_3\tedge_4\tedge_5\t"
            "target_kind\ttarget_index"
        )
        if header != expected_header:
            raise RuntimeError("unexpected map header")
        for line in source:
            if line.startswith("# SUMMARY "):
                summary = dict(
                    field.split("=", 1) for field in line.split()[2:]
                )
                break
            fields = line.rstrip("\n").split("\t")
            if len(fields) != 8:
                raise RuntimeError("bad map row")
            parent = int(fields[0])
            if not 0 <= parent < len(catalog):
                raise RuntimeError("bad parent index")
            edges = [parse_edge(text) for text in fields[1:6]]
            if len(set(edges)) != 5 or edges != sorted(edges, key=edge_index):
                raise RuntimeError(f"bad edge quintuple at row {checked + 2}")
            key = (parent, tuple(edges))
            if key in seen:
                raise RuntimeError(f"duplicate flip set at row {checked + 2}")
            seen.add(key)
            if fields[6] not in {"base", "complement"}:
                raise RuntimeError("bad target kind")
            if not 0 <= int(fields[7]) < 328:
                raise RuntimeError("bad target index")
            target = (fields[6], int(fields[7]))

            graph = catalog[parent].copy()
            for low, high in edges:
                graph[low] ^= 1 << high
                graph[high] ^= 1 << low
            if contains_clique(graph) or contains_clique(complement(graph)):
                raise RuntimeError(f"homogeneous 5-set at row {checked + 2}")
            per_parent[parent] += 1
            target_kinds[target[0]] += 1
            targets.add(target)
            checked += 1

    if summary is None:
        raise RuntimeError("missing map summary")
    if int(summary["transitions"]) != checked:
        raise RuntimeError("map summary transition count mismatch")
    if int(summary["base_transitions"]) != target_kinds["base"]:
        raise RuntimeError("map summary base-transition count mismatch")
    if int(summary["complement_transitions"]) != target_kinds["complement"]:
        raise RuntimeError("map summary complement-transition count mismatch")
    if int(summary["distinct_targets"]) != len(targets):
        raise RuntimeError("map summary distinct-target count mismatch")
    target_class_kinds = Counter(kind for kind, _ in targets)
    if int(summary["base_targets"]) != target_class_kinds["base"]:
        raise RuntimeError("map summary base-target count mismatch")
    if int(summary["complement_targets"]) != target_class_kinds["complement"]:
        raise RuntimeError("map summary complement-target count mismatch")
    print(
        f"direct_graphs={checked} homogeneous5_failures=0 "
        f"nonempty_parents={len(per_parent)} distinct_targets={len(targets)}"
    )


if __name__ == "__main__":
    main()
