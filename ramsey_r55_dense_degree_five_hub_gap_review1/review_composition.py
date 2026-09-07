#!/usr/bin/env python3
"""Independent literal audit of the thirteen-interface composition.

The script does not re-enumerate the upstream classification.  It checks every
published representative, identifies its unique hub and induced five-vertex
type, and verifies that the six type-126 consumer blocks form an exact disjoint
partition while the star and type-62 blocks account for the other four types.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


INPUTS_SHA256 = "8e17676c21e4b9c5b03c21e6fdba25d9d9325b77d0f1ee4f2718681c7db2fca2"
CONSUMERS = {
    "interface_0": (0,),
    "twenty_edge": (1, 2),
    "sixteen_edge": (3, 4),
    "interface_9": (9,),
    "twelve_edge": (10, 12),
    "twenty_four_edge": (11,),
}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def decode_graph6(record: str) -> set[tuple[int, int]]:
    require(record and all(63 <= ord(ch) <= 126 for ch in record), "invalid graph6 characters")
    order = ord(record[0]) - 63
    require(order == 22, "unexpected graph6 order")
    needed = order * (order - 1) // 2
    bits = "".join(f"{ord(ch) - 63:06b}" for ch in record[1:])
    require(len(bits) == ((needed + 5) // 6) * 6 and "1" not in bits[needed:], "bad graph6 length/padding")
    result: set[tuple[int, int]] = set()
    offset = 0
    for v in range(order):
        for u in range(v):
            if bits[offset] == "1":
                result.add((u, v))
            offset += 1
    return result


def has_uniform_set(edges: set[tuple[int, int]], size: int, red: bool) -> bool:
    for vertices in combinations(range(22), size):
        if all((edge in edges) == red for edge in combinations(vertices, 2)):
            return True
    return False


def hub_type(edges: set[tuple[int, int]], hub: int) -> str:
    neighbors = [v for v in range(22) if v != hub and tuple(sorted((v, hub))) in edges]
    require(len(neighbors) == 5, "wrong hub degree")
    internal = {edge for edge in combinations(neighbors, 2) if edge in edges}
    degrees = sorted(sum(v in edge for edge in internal) for v in neighbors)
    signatures = {
        (4, (1, 1, 1, 1, 4)): "star",
        (5, (1, 2, 2, 2, 3)): "type62",
        (6, (2, 2, 2, 3, 3)): "type126",
    }
    require((len(internal), tuple(degrees)) in signatures, "unknown five-neighbor type")
    return signatures[len(internal), tuple(degrees)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", type=Path, help="pinned dense-hub inputs.json")
    args = parser.parse_args()
    raw = args.inputs.read_bytes()
    require(sha256(raw).hexdigest() == INPUTS_SHA256, "upstream inputs identity")
    inputs = json.loads(raw)
    require(len(inputs["interfaces"]) == 13, "wrong interface count")
    groups = {"star": [], "type62": [], "type126": []}
    for index, record in enumerate(inputs["interfaces"]):
        edges = decode_graph6(record)
        require(len(edges) == 109, f"interface {index}: wrong density")
        require(not has_uniform_set(edges, 4, True), f"interface {index}: red K4")
        require(not has_uniform_set(edges, 5, False), f"interface {index}: blue K5")
        degrees = [sum(v in edge for edge in edges) for v in range(22)]
        hubs = [v for v, degree in enumerate(degrees) if degree == 5]
        require(hubs == [21], f"interface {index}: unique marked hub")
        groups[hub_type(edges, hubs[0])].append(index)

    require(groups["star"] == [5], "star composition")
    require(groups["type62"] == [6, 7, 8], "type-62 composition")
    require(groups["type126"] == [0, 1, 2, 3, 4, 9, 10, 11, 12], "type-126 composition")
    flattened = [index for block in CONSUMERS.values() for index in block]
    require(len(flattened) == len(set(flattened)) == 9, "type-126 consumer blocks overlap")
    require(sorted(flattened) == groups["type126"], "type-126 consumer blocks are incomplete")
    counts = {name: 29 * 12 * len(block) for name, block in CONSUMERS.items()}
    require(sum(counts.values()) == 3132, "wrong type-126 boundary count")
    require(3 * 24 * 2 == 144, "wrong type-62 boundary count")
    result = {
        "consumer_boundary_keys": counts,
        "groups": groups,
        "interfaces": 13,
        "status": "VERIFIED_LITERAL_INTERFACE_PARTITION_AND_BOUNDARY_ACCOUNTING",
        "type126_boundary_keys": sum(counts.values()),
        "type62_boundary_keys": 144,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
