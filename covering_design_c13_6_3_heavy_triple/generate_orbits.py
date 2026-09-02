#!/usr/bin/env python3
"""Generate all 336 normalized heavy-triple/three-block orbit representatives.

This implementation enumerates unordered triples of actual 3-subsets of the
ten points outside a fixed heavy triple.  It is intentionally different from
audit_orbits.py, which enumerates membership-pattern count vectors directly.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


PERMUTATIONS = tuple(itertools.permutations(range(3)))
MASK_MAPS = {
    perm: tuple(
        sum(((mask >> j) & 1) << perm[j] for j in range(3))
        for mask in range(8)
    )
    for perm in PERMUTATIONS
}


def pattern_counts(
    edges: tuple[tuple[int, ...], ...], high_count: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    high = [0] * 8
    low = [0] * 8
    edge_sets = tuple(map(set, edges))
    for point in range(10):
        mask = sum((1 << j) for j, edge in enumerate(edge_sets) if point in edge)
        (high if point < high_count else low)[mask] += 1
    return tuple(high), tuple(low)


def canonical_signature(
    high: tuple[int, ...], low: tuple[int, ...]
) -> tuple[int, ...]:
    signatures = []
    for perm in PERMUTATIONS:
        mask_map = MASK_MAPS[perm]
        perm_high = [0] * 8
        perm_low = [0] * 8
        for mask in range(8):
            perm_high[mask_map[mask]] = high[mask]
            perm_low[mask_map[mask]] = low[mask]
        signatures.append(tuple(perm_high + perm_low))
    return min(signatures)


def representatives(a: int) -> list[dict[str, object]]:
    high_count = 3 - a
    extra_sets = list(itertools.combinations(range(10), 3))
    found: dict[tuple[int, ...], tuple[tuple[int, ...], ...]] = {}
    for edges in itertools.combinations(extra_sets, 3):
        high, low = pattern_counts(edges, high_count)
        signature = canonical_signature(high, low)
        found.setdefault(signature, edges)

    triple = tuple(range(a)) + tuple(range(3, 3 + 3 - a))
    remaining = tuple(range(a, 3)) + tuple(range(6 - a, 13))
    assert len(triple) == 3 and len(remaining) == 10
    result = []
    for signature, edges in sorted(found.items()):
        blocks = [
            sorted(triple + tuple(remaining[point] for point in edge))
            for edge in edges
        ]
        assert len({tuple(block) for block in blocks}) == 3
        result.append({"signature": list(signature), "blocks": blocks})
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("orbit_representatives.json"))
    args = parser.parse_args()
    by_a = {str(a): representatives(a) for a in range(4)}
    counts = [len(by_a[str(a)]) for a in range(4)]
    assert counts == [177, 103, 44, 12]
    payload = {
        "parameters": {"v": 13, "k": 6, "t": 3, "hypothetical_blocks": 20},
        "normalization": {
            "degree_10_points": [0, 1, 2],
            "a": "number of degree-10 points in the fixed multiplicity-at-least-3 triple",
            "blocks": "three selected blocks containing the fixed triple; 0-based points"
        },
        "counts_by_a": counts,
        "total_orbits": sum(counts),
        "orbits_by_a": by_a,
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"counts_by_a": counts, "total_orbits": sum(counts)}, sort_keys=True))


if __name__ == "__main__":
    main()
