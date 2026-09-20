#!/usr/bin/env python3
"""Exact audit for the all-forward ordered 5-pattern at N=5m+2."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import defaultdict
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_PATH = ROOT / "EXPECTED.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def interval(start: int, length: int, modulus: int) -> frozenset[int]:
    return frozenset((start + offset) % modulus for offset in range(length))


def pair(a: int, b: int, modulus: int) -> tuple[int, int]:
    a %= modulus
    b %= modulus
    require(a != b, "pair endpoints must differ")
    return (a, b) if a < b else (b, a)


def type_graph(kind: int, start: int, m: int) -> frozenset[tuple[int, int]]:
    n = 5 * m + 2
    if kind == 0:
        vertices = interval(start, m + 1, n)
        return frozenset(itertools.combinations(sorted(vertices), 2))
    left = interval(start, m, n)
    right = interval(start + kind * m + 1, m, n)
    return frozenset(pair(a, b, n) for a in left for b in right)


def canonical_copy(m: int, omissions: tuple[int, int]):
    n = 5 * m + 2
    remaining = [vertex for vertex in range(n) if vertex not in omissions]
    require(len(remaining) == 5 * m, "wrong complement size")
    return tuple(
        tuple(remaining[block * m + rank] for block in range(5))
        for rank in range(m)
    )


def occurrence_graphs(m: int):
    n = 5 * m + 2
    occurrences: dict[tuple[int, ...], set[tuple[int, int]]] = defaultdict(set)
    for omissions in itertools.combinations(range(n), 2):
        for edge in canonical_copy(m, omissions):
            occurrences[edge].add(omissions)
    return {edge: frozenset(omitted) for edge, omitted in occurrences.items()}


def lower_blocker(m: int) -> frozenset[tuple[int, ...]]:
    n = 5 * m + 2
    return frozenset(
        edge
        for edge in itertools.combinations(range(n), 5)
        if all(edge[index + 1] - edge[index] >= m for index in range(4))
        and edge[4] <= n - m
    )


def weak_bounded(total: int, parts: int, bound: int):
    if parts == 0:
        if total == 0:
            yield ()
        return
    for first in range(min(total, bound) + 1):
        for tail in weak_bounded(total - first, parts - 1, bound):
            yield (first, *tail)


def starts_from_deficits(m: int, deficits: tuple[int, ...]) -> tuple[int, ...]:
    starts = [0]
    for deficit in deficits[:-1]:
        starts.append(starts[-1] + m - deficit)
    return tuple(starts)


def repair_intervals(m: int, deficits: tuple[int, ...]):
    n = 5 * m + 2
    starts = starts_from_deficits(m, deficits)
    repairs = []
    for index, deficit in enumerate(deficits):
        successor = starts[index + 1] if index + 1 < len(starts) else n
        repairs.append(interval(successor, deficit + 1, n))
    return tuple(repairs)


def pairwise_disjoint(sets) -> bool:
    return all(left.isdisjoint(right) for left, right in itertools.combinations(sets, 2))


def maximum_disjoint(sets) -> int:
    size = len(sets)
    return max(
        mask.bit_count()
        for mask in range(1 << size)
        if pairwise_disjoint([sets[index] for index in range(size) if mask >> index & 1])
    )


def high_masks(m: int):
    n = 5 * m + 2
    pairs = tuple(sorted({
        pair(x, x + distance, n)
        for distance in range(2 * m + 1, n // 2 + 1)
        for x in range(n)
    }))
    pair_index = {edge: index for index, edge in enumerate(pairs)}
    masks = []
    for start in range(n):
        mask = 0
        for edge in type_graph(2, start, m):
            if edge in pair_index:
                mask |= 1 << pair_index[edge]
        masks.append(mask)
    return tuple(masks), (1 << len(pairs)) - 1


def covers_high(starts: tuple[int, ...], masks, full: int) -> bool:
    covered = 0
    for start in starts:
        covered |= masks[start]
    return covered == full


def audit_occurrences(m: int):
    n = 5 * m + 2
    copies = tuple(
        canonical_copy(m, omissions)
        for omissions in itertools.combinations(range(n), 2)
    )
    occurrences = occurrence_graphs(m)
    model = tuple(
        type_graph(kind, start, m)
        for kind in range(3)
        for start in range(n)
    )
    require(len(occurrences) == 3 * n, "wrong active-edge count")
    require(len(set(model)) == len(model), "model graph duplication")
    require(set(occurrences.values()) == set(model), "Q/R/T classification failed")

    blocker = lower_blocker(m)
    require(len(blocker) == 21, "wrong blocker size")
    require(
        all(any(edge in blocker for edge in copy) for copy in copies),
        "blocker misses a canonical copy",
    )

    for kind, distance in enumerate((1, m + 1, 2 * m + 1)):
        layer = frozenset(pair(x, x + distance, n) for x in range(n))
        own = [type_graph(kind, start, m) for start in range(n)]
        other = [
            type_graph(other_kind, start, m)
            for other_kind in range(3)
            if other_kind != kind
            for start in range(n)
        ]
        require(all(len(graph & layer) == m for graph in own), "private count failed")
        require(not any(graph & layer for graph in other), "private layer leaked")

    return {
        "m": m,
        "canonical_copies": len(copies),
        "active_edges": len(occurrences),
        "blocker_edges": len(blocker),
    }


def audit_signatures(m: int):
    masks, high_full = high_masks(m)
    totals = {
        "six_signatures": 0,
        "six_high_covers": 0,
        "seven_signatures": 0,
        "seven_high_covers": 0,
        "eight_signatures": 0,
        "eight_high_covers": 0,
        "tight_placements": 0,
    }

    for count in (6, 7, 8):
        deficit_total = count * m - (5 * m + 2)
        key = ("six", "seven", "eight")[count - 6]
        for deficits in weak_bounded(deficit_total, count, m - 1):
            totals[f"{key}_signatures"] += 1
            starts = starts_from_deficits(m, deficits)
            if not covers_high(starts, masks, high_full):
                continue
            totals[f"{key}_high_covers"] += 1
            repairs = repair_intervals(m, deficits)

            if count == 6:
                raise AssertionError("six T starts cover the high band")

            if count == 7:
                require(
                    all(
                        sum(deficits[(index + offset) % 7] for offset in range(3))
                        <= m - 1
                        for index in range(7)
                    ),
                    "seven-start triple-window bound failed",
                )
                require(pairwise_disjoint(repairs), "seven-start repairs overlap")
                for offsets in itertools.product(
                    *(range(deficit + 1) for deficit in deficits)
                ):
                    totals["tight_placements"] += 1
                    propagated = tuple(
                        deficits[(index + 1) % 7]
                        - offsets[(index + 1) % 7]
                        + offsets[index]
                        for index in range(7)
                    )
                    require(all(value >= 0 for value in propagated), "negative propagated deficit")
                    require(sum(propagated) == 2 * m - 2, "propagated sum changed")
                    require(
                        all(
                            propagated[index] + propagated[(index + 1) % 7] <= m - 1
                            for index in range(7)
                        ),
                        "tight propagation overlap",
                    )

            if count == 8:
                require(maximum_disjoint(repairs) >= 7, "eight-start repair packing failed")

    return {"m": m, **totals}


def main() -> None:
    occurrence_records = [audit_occurrences(m) for m in range(2, 13)]
    signature_records = [audit_signatures(m) for m in range(2, 7)]
    records = {"occurrences": occurrence_records, "signatures": signature_records}
    record_bytes = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    occurrence_keys = ("canonical_copies", "active_edges", "blocker_edges")
    signature_keys = (
        "six_signatures",
        "six_high_covers",
        "seven_signatures",
        "seven_high_covers",
        "eight_signatures",
        "eight_high_covers",
        "tight_placements",
    )
    summary = {
        "status": "VERIFIED",
        "audit_boxes": {"occurrences_m": [2, 12], "signatures_m": [2, 6]},
        "record_sha256": hashlib.sha256(record_bytes).hexdigest(),
        "totals": {
            **{
                key: sum(record[key] for record in occurrence_records)
                for key in occurrence_keys
            },
            **{
                key: sum(record[key] for record in signature_records)
                for key in signature_keys
            },
        },
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    require(EXPECTED_PATH.exists(), "EXPECTED.json is missing")
    expected = json.loads(EXPECTED_PATH.read_text())
    require(summary == expected, "summary does not match EXPECTED.json")


if __name__ == "__main__":
    main()
