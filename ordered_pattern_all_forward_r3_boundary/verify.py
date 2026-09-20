#!/usr/bin/env python3
"""Exact audit for the all-forward ordered 3-pattern at N=3m+2."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_PATH = ROOT / "EXPECTED.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def interval(start: int, length: int, n: int) -> frozenset[int]:
    return frozenset((start + offset) % n for offset in range(length))


def pair(a: int, b: int, n: int) -> tuple[int, int]:
    a %= n
    b %= n
    require(a != b, "pair endpoints must be distinct")
    return (a, b) if a < b else (b, a)


def cyclic_distance(p: tuple[int, int], n: int) -> int:
    distance = p[1] - p[0]
    return min(distance, n - distance)


def q_graph(start: int, m: int) -> frozenset[tuple[int, int]]:
    n = 3 * m + 2
    vertices = interval(start, m + 1, n)
    return frozenset(itertools.combinations(sorted(vertices), 2))


def r_graph(start: int, m: int) -> frozenset[tuple[int, int]]:
    n = 3 * m + 2
    left = interval(start, m, n)
    right = interval(start + m + 1, m, n)
    return frozenset(pair(x, y, n) for x in left for y in right)


def canonical_copy(m: int, omissions: tuple[int, int]):
    n = 3 * m + 2
    remaining = [x for x in range(n) if x not in omissions]
    require(len(remaining) == 3 * m, "wrong complement size")
    return tuple(
        (remaining[j], remaining[m + j], remaining[2 * m + j])
        for j in range(m)
    )


def occurrence_graphs(m: int):
    n = 3 * m + 2
    occurrences: dict[tuple[int, int, int], set[tuple[int, int]]] = (
        defaultdict(set)
    )
    for omissions in itertools.combinations(range(n), 2):
        for edge in canonical_copy(m, omissions):
            occurrences[edge].add(omissions)
    return {edge: frozenset(pairs) for edge, pairs in occurrences.items()}


def lower_blocker(m: int) -> frozenset[tuple[int, int, int]]:
    n = 3 * m + 2
    return frozenset(
        edge
        for edge in itertools.combinations(range(n), 3)
        if edge[1] - edge[0] >= m
        and edge[2] - edge[1] >= m
        and edge[2] <= n - m
    )


def low_start_sets(x: int, d: int, m: int):
    n = 3 * m + 2
    require(1 <= d <= m, "not a low distance")
    q_starts = interval(x + d - m, m - d + 1, n)
    r_starts = interval(x - m + 1, d - 1, n)
    return q_starts, r_starts


def high_start_set(x: int, t: int, m: int) -> frozenset[int]:
    n = 3 * m + 2
    require(0 <= t <= m // 2, "not a canonical high-distance offset")
    return interval(x - m + 1 + t, m - t, n) | interval(
        x + m + 2, t, n
    )


def selected_union(starts, graphs):
    return frozenset().union(*(graphs[start] for start in starts))


def cyclic_gaps(starts: tuple[int, ...], n: int) -> tuple[int, ...]:
    return tuple(
        (starts[(i + 1) % len(starts)] - starts[i]) % n
        for i in range(len(starts))
    )


def audit_case(m: int) -> dict[str, int]:
    n = 3 * m + 2
    universe = frozenset(itertools.combinations(range(n), 2))
    copies = tuple(
        canonical_copy(m, omissions)
        for omissions in itertools.combinations(range(n), 2)
    )

    occurrence = occurrence_graphs(m)
    q_graphs = tuple(q_graph(start, m) for start in range(n))
    r_graphs = tuple(r_graph(start, m) for start in range(n))
    require(len(occurrence) == 2 * n, "wrong active-edge count")
    require(
        set(occurrence.values()) == set(q_graphs) | set(r_graphs),
        "occurrence-graph classification failed",
    )
    require(len(set(q_graphs)) == n, "Q rotations are not distinct")
    require(len(set(r_graphs)) == n, "R rotations are not distinct")
    require(not (set(q_graphs) & set(r_graphs)), "Q/R types overlap")

    blocker = lower_blocker(m)
    require(len(blocker) == 10, "lower blocker has wrong size")
    require(
        all(any(edge in blocker for edge in copy) for copy in copies),
        "lower blocker misses a canonical copy",
    )

    # Audit the exact permissible-start formulas against the model graphs.
    formula_checks = 0
    for x in range(n):
        for d in range(1, m + 1):
            p = pair(x, x + d, n)
            expected_q, expected_r = low_start_sets(x, d, m)
            actual_q = frozenset(s for s, graph in enumerate(q_graphs) if p in graph)
            actual_r = frozenset(s for s, graph in enumerate(r_graphs) if p in graph)
            require(actual_q == expected_q, "low Q-start formula failed")
            require(actual_r == expected_r, "low R-start formula failed")
            formula_checks += 2
        for t in range(m // 2 + 1):
            p = pair(x, x + m + 1 + t, n)
            actual_r = frozenset(s for s, graph in enumerate(r_graphs) if p in graph)
            require(
                actual_r == high_start_set(x, t, m),
                "high R-start formula failed",
            )
            formula_checks += 1

    high_pairs = frozenset(
        p for p in universe if cyclic_distance(p, n) > m
    )
    distance_one_pairs = frozenset(
        p for p in universe if cyclic_distance(p, n) == 1
    )
    require(
        all(len(graph & distance_one_pairs) == m for graph in q_graphs),
        "wrong distance-one Q count",
    )
    require(
        all(not (graph & distance_one_pairs) for graph in r_graphs),
        "R graph contains a distance-one pair",
    )

    # Exhaustive finite audit of both cyclic-gap lemmas.
    four_start_sets = 0
    four_high_covers = 0
    for starts in itertools.combinations(range(n), 4):
        four_start_sets += 1
        if high_pairs <= selected_union(starts, r_graphs):
            four_high_covers += 1
    require(four_high_covers == 0, "four R graphs cover all high pairs")

    five_start_sets = 0
    five_high_covers = 0
    repair_pairs = 0
    for starts in itertools.combinations(range(n), 5):
        five_start_sets += 1
        if not high_pairs <= selected_union(starts, r_graphs):
            continue
        five_high_covers += 1
        gaps = cyclic_gaps(starts, n)
        require(max(gaps) <= m, "center-distance gap bound failed")
        require(
            all(gaps[i] + gaps[(i + 1) % 5] >= m + 1 for i in range(5)),
            "adjacent-gap inequality failed",
        )

        repair_arcs = []
        for i, (start, d) in enumerate(zip(starts, gaps)):
            successor = starts[(i + 1) % 5]
            x = start + m
            p = pair(x, x + d, n)
            q_starts, r_starts = low_start_sets(x, d, m)
            open_gap = interval(start + 1, d - 1, n)
            repair_arc = interval(successor, m - d + 1, n)
            require(r_starts == open_gap, "repair R-gap identity failed")
            require(q_starts == repair_arc, "repair Q-arc identity failed")
            require(not (set(starts) & r_starts), "selected R hits repair pair")
            sector = interval(successor, gaps[(i + 1) % 5], n)
            require(repair_arc <= sector, "repair arc escapes its sector")
            repair_arcs.append(repair_arc)
            require(p not in selected_union(starts, r_graphs), "repair pair hit by R")
            repair_pairs += 1
        require(
            sum(len(arc) for arc in repair_arcs)
            == len(frozenset().union(*repair_arcs)),
            "repair arcs are not disjoint",
        )

    require(five_high_covers > 0, "audit found no five-R high cover")

    return {
        "m": m,
        "n": n,
        "canonical_copies": len(copies),
        "active_edges": len(occurrence),
        "blocker_edges": len(blocker),
        "formula_checks": formula_checks,
        "four_start_sets": four_start_sets,
        "four_high_covers": four_high_covers,
        "five_start_sets": five_start_sets,
        "five_high_covers": five_high_covers,
        "repair_pairs": repair_pairs,
    }


def main() -> None:
    records = [audit_case(m) for m in range(2, 13)]
    record_bytes = json.dumps(
        records, sort_keys=True, separators=(",", ":")
    ).encode()
    summary = {
        "status": "VERIFIED",
        "audit_box": {"m": [2, 12]},
        "case_count": len(records),
        "record_sha256": hashlib.sha256(record_bytes).hexdigest(),
        "totals": {
            key: sum(record[key] for record in records)
            for key in (
                "canonical_copies",
                "active_edges",
                "blocker_edges",
                "formula_checks",
                "four_start_sets",
                "four_high_covers",
                "five_start_sets",
                "five_high_covers",
                "repair_pairs",
            )
        },
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    if "--write-expected" in sys.argv:
        EXPECTED_PATH.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
        return
    require(EXPECTED_PATH.exists(), "EXPECTED.json is missing")
    expected = json.loads(EXPECTED_PATH.read_text())
    require(summary == expected, "summary does not match EXPECTED.json")


if __name__ == "__main__":
    main()
