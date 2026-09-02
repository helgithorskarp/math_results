#!/usr/bin/env python3
"""Independent count-vector audit of orbit_representatives.json."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


PERMUTATIONS = tuple(itertools.permutations(range(3)))


def compositions(total: int, parts: int = 8):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            yield (first,) + tail


def degrees(counts: tuple[int, ...]) -> tuple[int, int, int]:
    return tuple(
        sum(counts[mask] for mask in range(8) if (mask >> j) & 1)
        for j in range(3)
    )


def permute_counts(
    counts: tuple[int, ...], permutation: tuple[int, ...]
) -> tuple[int, ...]:
    result = [0] * 8
    for mask, count in enumerate(counts):
        new_mask = sum(
            ((mask >> j) & 1) << permutation[j] for j in range(3)
        )
        result[new_mask] = count
    return tuple(result)


def distinct_edges(counts: tuple[int, ...]) -> bool:
    for first in range(3):
        for second in range(first + 1, 3):
            symmetric_difference = sum(
                counts[mask]
                for mask in range(8)
                if ((mask >> first) ^ (mask >> second)) & 1
            )
            if symmetric_difference == 0:
                return False
    return True


def signatures(a: int) -> set[tuple[int, ...]]:
    high_points, low_points = 3 - a, 7 + a
    high_by_degree: dict[tuple[int, int, int], list[tuple[int, ...]]] = {}
    for counts in compositions(high_points):
        high_by_degree.setdefault(degrees(counts), []).append(counts)

    result = set()
    for low in compositions(low_points):
        needed = tuple(3 - value for value in degrees(low))
        if min(needed) < 0:
            continue
        for high in high_by_degree.get(needed, ()):
            combined = tuple(high[mask] + low[mask] for mask in range(8))
            if not distinct_edges(combined):
                continue
            result.add(min(
                permute_counts(high, permutation) + permute_counts(low, permutation)
                for permutation in PERMUTATIONS
            ))
    return result


def signature_from_blocks(a: int, blocks: list[list[int]]) -> tuple[int, ...]:
    triple = set(tuple(range(a)) + tuple(range(3, 3 + 3 - a)))
    remaining = tuple(range(a, 3)) + tuple(range(6 - a, 13))
    remaining_index = {point: i for i, point in enumerate(remaining)}
    edges = []
    for block in blocks:
        assert len(block) == 6 and len(set(block)) == 6
        assert triple.issubset(block)
        edge = {remaining_index[point] for point in set(block) - triple}
        assert len(edge) == 3
        edges.append(edge)
    assert len(edges) == 3 and len({tuple(sorted(edge)) for edge in edges}) == 3
    high = [0] * 8
    low = [0] * 8
    for point in range(10):
        mask = sum((1 << j) for j, edge in enumerate(edges) if point in edge)
        (high if point < 3 - a else low)[mask] += 1
    return min(
        permute_counts(tuple(high), permutation) + permute_counts(tuple(low), permutation)
        for permutation in PERMUTATIONS
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path, nargs="?", default=Path("orbit_representatives.json"))
    args = parser.parse_args()
    payload = json.loads(args.certificate.read_text())
    all_signatures = []
    counts = []
    for a in range(4):
        computed = signatures(a)
        records = payload["orbits_by_a"][str(a)]
        recorded = set()
        for record in records:
            signature = signature_from_blocks(a, record["blocks"])
            assert signature == tuple(record["signature"])
            recorded.add(signature)
        assert len(recorded) == len(records)
        assert recorded == computed
        counts.append(len(computed))
        all_signatures.extend((a,) + signature for signature in sorted(computed))
    assert counts == [177, 103, 44, 12]
    assert payload["counts_by_a"] == counts and payload["total_orbits"] == 336
    digest = hashlib.sha256(
        json.dumps(all_signatures, separators=(",", ":")).encode()
    ).hexdigest()
    print(json.dumps({"counts_by_a": counts, "total_orbits": sum(counts),
                      "signature_sha256": digest}, sort_keys=True))


if __name__ == "__main__":
    main()
