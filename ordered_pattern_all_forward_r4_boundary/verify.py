#!/usr/bin/env python3
"""Exact audit for the all-forward ordered 4-pattern at N=4m+2."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from collections import defaultdict
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
    require(a != b, "pair endpoints must be distinct")
    return (a, b) if a < b else (b, a)


def q_graph(start: int, m: int) -> frozenset[tuple[int, int]]:
    n = 4 * m + 2
    vertices = interval(start, m + 1, n)
    return frozenset(itertools.combinations(sorted(vertices), 2))


def r_graph(start: int, m: int) -> frozenset[tuple[int, int]]:
    n = 4 * m + 2
    left = interval(start, m, n)
    right = interval(start + m + 1, m, n)
    return frozenset(pair(x, y, n) for x in left for y in right)


def s_graph(start: int, m: int) -> frozenset[tuple[int, int]]:
    n = 4 * m + 2
    half = 2 * m + 1
    left = interval(start, m, n)
    right = interval(start + half, m, n)
    return frozenset(pair(x, y, n) for x in left for y in right)


def canonical_copy(m: int, omissions: tuple[int, int]):
    n = 4 * m + 2
    remaining = [x for x in range(n) if x not in omissions]
    require(len(remaining) == 4 * m, "wrong complement size")
    return tuple(
        (
            remaining[j],
            remaining[m + j],
            remaining[2 * m + j],
            remaining[3 * m + j],
        )
        for j in range(m)
    )


def occurrence_graphs(m: int):
    n = 4 * m + 2
    occurrences: dict[tuple[int, int, int, int], set[tuple[int, int]]] = (
        defaultdict(set)
    )
    for omissions in itertools.combinations(range(n), 2):
        for edge in canonical_copy(m, omissions):
            occurrences[edge].add(omissions)
    return {edge: frozenset(pairs) for edge, pairs in occurrences.items()}


def lower_blocker(m: int) -> frozenset[tuple[int, int, int, int]]:
    n = 4 * m + 2
    return frozenset(
        edge
        for edge in itertools.combinations(range(n), 4)
        if all(edge[i + 1] - edge[i] >= m for i in range(3))
        and edge[3] <= n - m
    )


def low_start_sets(x: int, distance: int, m: int):
    n = 4 * m + 2
    require(1 <= distance <= m, "not a low distance")
    q_starts = interval(x + distance - m, m - distance + 1, n)
    r_starts = interval(x - m + 1, distance - 1, n)
    return q_starts, r_starts


def high_start_sets(x: int, excess: int, m: int):
    n = 4 * m + 2
    half = 2 * m + 1
    require(1 <= excess <= m, "not a high-distance excess")
    r_starts = interval(x - m + 1 + excess, m - excess, n)
    s_starts = interval(x - m + 1, excess, half)
    return r_starts, s_starts


def weak_compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, parts - 1):
            yield (first, *tail)


def pairwise_disjoint(sets) -> bool:
    return all(left.isdisjoint(right) for left, right in itertools.combinations(sets, 2))


def audit_gap_signature(m: int, deficits: tuple[int, ...]) -> dict[str, int]:
    n = 4 * m + 2
    half = 2 * m + 1
    count = len(deficits)
    gaps = tuple(m - deficit for deficit in deficits)
    require(all(1 <= gap <= m for gap in gaps), "invalid middle-start gap")
    require(sum(gaps) == n, "gaps do not close the cycle")

    starts = [0]
    for gap in gaps[:-1]:
        starts.append(starts[-1] + gap)

    low_repairs = []
    high_repairs = []
    for i, (start, gap, deficit) in enumerate(zip(starts, gaps, deficits)):
        successor = starts[(i + 1) % count] if i + 1 < count else n
        length = deficit + 1
        low = interval(successor, length, n)
        high = interval(successor - m, length, half)
        low_repairs.append(low)
        high_repairs.append(high)

        low_pair_x = start + m
        actual_q, actual_r = low_start_sets(low_pair_x, gap, m)
        require(actual_q == low, "low repair interval identity failed")
        require(
            actual_r == interval(start + 1, gap - 1, n),
            "low empty-gap identity failed",
        )

        high_pair_x = successor - 1
        actual_r, actual_s = high_start_sets(high_pair_x, length, m)
        require(actual_s == high, "high repair interval identity failed")
        require(
            actual_r == interval(start + 1, gap - 1, n),
            "high empty-gap identity failed",
        )

    if count == 5:
        require(sum(deficits) == m - 2, "wrong five-gap deficit")
        require(pairwise_disjoint(low_repairs), "five low repairs overlap")
        require(pairwise_disjoint(high_repairs), "five high repairs overlap")
        return {"five_signatures": 1, "five_repair_pairs": 10}

    require(count == 6, "unexpected gap count")
    require(sum(deficits) == 2 * m - 2, "wrong six-gap deficit")

    overlaps = {
        tuple(sorted((i, j)))
        for i, j in itertools.combinations(range(6), 2)
        if not low_repairs[i].isdisjoint(low_repairs[j])
    }
    require(
        all((j - i) % 6 in {1, 5} for i, j in overlaps),
        "nonadjacent low repairs overlap",
    )
    require(
        not any(set(left).isdisjoint(right) for left, right in itertools.combinations(overlaps, 2)),
        "two vertex-disjoint low overlaps exist",
    )

    if not overlaps:
        require(pairwise_disjoint(low_repairs), "six low repairs not disjoint")
        return {
            "six_signatures": 1,
            "six_no_overlap": 1,
            "six_overlap": 0,
            "six_repair_pairs": 6,
        }

    overlap = min(overlaps)
    left, right = overlap
    require((right - left) % 6 == 1 or (left - right) % 6 == 1, "bad overlap")
    if (right - left) % 6 != 1:
        left, right = right, left
    remaining = [i for i in range(6) if i not in {left, right}]
    require(
        pairwise_disjoint([high_repairs[i] for i in remaining]),
        "four high repairs are not disjoint",
    )
    return {
        "six_signatures": 1,
        "six_no_overlap": 0,
        "six_overlap": 1,
        "six_repair_pairs": 10,
    }


def audit_case(m: int) -> dict[str, int]:
    n = 4 * m + 2
    half = 2 * m + 1
    universe = frozenset(itertools.combinations(range(n), 2))
    copies = tuple(
        canonical_copy(m, omissions)
        for omissions in itertools.combinations(range(n), 2)
    )

    occurrences = occurrence_graphs(m)
    q_graphs = tuple(q_graph(start, m) for start in range(n))
    r_graphs = tuple(r_graph(start, m) for start in range(n))
    s_graphs = tuple(s_graph(start, m) for start in range(half))
    model = q_graphs + r_graphs + s_graphs
    require(len(occurrences) == 10 * m + 5, "wrong active-edge count")
    require(len(set(model)) == len(model), "model occurrence graphs duplicate")
    require(
        set(occurrences.values()) == set(model),
        "Q/R/S occurrence-graph classification failed",
    )

    blocker = lower_blocker(m)
    require(len(blocker) == 15, "lower blocker has wrong size")
    require(
        all(any(edge in blocker for edge in copy) for copy in copies),
        "lower blocker misses a canonical copy",
    )

    formula_checks = 0
    for x in range(n):
        for distance in range(1, m + 1):
            omitted = pair(x, x + distance, n)
            expected_q, expected_r = low_start_sets(x, distance, m)
            actual_q = frozenset(
                start for start, graph in enumerate(q_graphs) if omitted in graph
            )
            actual_r = frozenset(
                start for start, graph in enumerate(r_graphs) if omitted in graph
            )
            require(actual_q == expected_q, "low Q-start formula failed")
            require(actual_r == expected_r, "low R-start formula failed")
            formula_checks += 2

        for excess in range(1, m + 1):
            omitted = pair(x, x + m + 1 + excess, n)
            expected_r, expected_s = high_start_sets(x, excess, m)
            actual_r = frozenset(
                start for start, graph in enumerate(r_graphs) if omitted in graph
            )
            actual_s = frozenset(
                start for start, graph in enumerate(s_graphs) if omitted in graph
            )
            require(actual_r == expected_r, "high R-start formula failed")
            require(actual_s == expected_s, "high S-start formula failed")
            formula_checks += 2

    distance_one = frozenset(
        omitted
        for omitted in universe
        if min(omitted[1] - omitted[0], n - omitted[1] + omitted[0]) == 1
    )
    middle = frozenset(
        omitted
        for omitted in universe
        if min(omitted[1] - omitted[0], n - omitted[1] + omitted[0]) == m + 1
    )
    diameter = frozenset(
        omitted
        for omitted in universe
        if min(omitted[1] - omitted[0], n - omitted[1] + omitted[0]) == half
    )
    require(all(len(graph & distance_one) == m for graph in q_graphs), "Q center count")
    require(all(len(graph & middle) == m for graph in r_graphs), "R center count")
    require(all(len(graph & diameter) == m for graph in s_graphs), "S center count")
    require(not any(graph & distance_one for graph in r_graphs + s_graphs), "distance-one type leak")
    require(not any(graph & middle for graph in q_graphs + s_graphs), "middle type leak")
    require(not any(graph & diameter for graph in q_graphs + r_graphs), "diameter type leak")

    totals = {
        "five_signatures": 0,
        "five_repair_pairs": 0,
        "six_signatures": 0,
        "six_no_overlap": 0,
        "six_overlap": 0,
        "six_repair_pairs": 0,
    }
    for deficits in weak_compositions(m - 2, 5):
        record = audit_gap_signature(m, deficits)
        for key, value in record.items():
            totals[key] += value
    for deficits in weak_compositions(2 * m - 2, 6):
        if max(deficits) >= m:
            continue
        record = audit_gap_signature(m, deficits)
        for key, value in record.items():
            totals[key] += value

    return {
        "m": m,
        "n": n,
        "canonical_copies": len(copies),
        "active_edges": len(occurrences),
        "blocker_edges": len(blocker),
        "formula_checks": formula_checks,
        **totals,
    }


def main() -> None:
    records = [audit_case(m) for m in range(2, 13)]
    record_bytes = json.dumps(
        records, sort_keys=True, separators=(",", ":")
    ).encode()
    total_keys = (
        "canonical_copies",
        "active_edges",
        "blocker_edges",
        "formula_checks",
        "five_signatures",
        "five_repair_pairs",
        "six_signatures",
        "six_no_overlap",
        "six_overlap",
        "six_repair_pairs",
    )
    summary = {
        "status": "VERIFIED",
        "audit_box": {"m": [2, 12]},
        "case_count": len(records),
        "record_sha256": hashlib.sha256(record_bytes).hexdigest(),
        "totals": {
            key: sum(record[key] for record in records) for key in total_keys
        },
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    require(EXPECTED_PATH.exists(), "EXPECTED.json is missing")
    expected = json.loads(EXPECTED_PATH.read_text())
    require(summary == expected, "summary does not match EXPECTED.json")


if __name__ == "__main__":
    main()
