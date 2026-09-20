#!/usr/bin/env python3
"""Independent state-compressed check of the total-218 profile obstruction."""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROWS = HERE.parent / "hypercube_square_saturation_q5_gap218" / "PROFILE_CLASSES.json"
EXPECTED_HASH = "9dc4c10874d87acd730ab6fb0741b23da45c13a4d01ba29149dcc11e8f4aefbb"


def capacities():
    facets = tuple(range(10))
    supports = []
    for direction in range(5):
        for vertex in range(32):
            if (vertex >> direction) & 1:
                continue
            supports.append(frozenset(
                2 * coordinate + ((vertex >> coordinate) & 1)
                for coordinate in range(5) if coordinate != direction
            ))
    return tuple(max(
        sum(support.issubset(live) for support in supports)
        for live in map(frozenset, combinations(facets, size))
    ) for size in range(1, 11))


def compressed_states(classes):
    # State = (total deficit, positive facets, edge-incidence sum, max bad-boundary count).
    states = {(0, 0, 0, -1)}
    for deficit, edges, bad, _empty_boundaries in classes:
        closure = set(states)
        frontier = list(states)
        while frontier:
            total, count, incidence, maximum_bad = frontier.pop()
            candidate = (total + deficit, count + 1, incidence + edges,
                         max(maximum_bad, bad))
            if candidate[0] <= 218 and candidate[1] <= 10 and candidate not in closure:
                closure.add(candidate)
                frontier.append(candidate)
        states = closure
    return states


def check():
    rows = json.loads(ROWS.read_text())
    digest = sha256(json.dumps(rows, separators=(",", ":")).encode("ascii")).hexdigest()
    if len(rows) != 182 or digest != EXPECTED_HASH:
        raise AssertionError("accepted profile certificate changed")
    caps = capacities()
    if caps != (0, 0, 0, 1, 5, 9, 16, 28, 48, 80):
        raise AssertionError("capacity reconstruction failed")
    states = compressed_states(sorted(tuple(row[:4]) for row in rows))
    survivors = []
    for total, positive, positive_edges, maximum_bad in states:
        if total != 218 or positive == 0:
            continue
        for equality in range(11 - positive):
            empty = 10 - positive - equality
            incidence = positive_edges + 17 * equality
            if incidence % 4:
                continue
            global_edges = incidence // 4
            live = positive + equality
            if global_edges and global_edges <= caps[live - 1] and maximum_bad <= positive + empty - 1:
                survivors.append((positive, equality, empty, global_edges, maximum_bad))
    if survivors:
        raise AssertionError("compressed checker found a subendpoint survivor")

    endpoint_pairs = [(e, s) for e in range(25) for s in range(25)
                      if 17 * s - 3 * e == 218]
    if endpoint_pairs != [(1, 13), (18, 16)]:
        raise AssertionError("endpoint arithmetic failed")
    if 6 * 1 - 7 * 0 + 2 * 0 == 13:
        raise AssertionError("one-edge endpoint was not excluded")
    endpoint_cases = []
    for equality in range(10):
        incidence = 18 + 17 * equality
        if incidence % 4 == 0:
            live = equality + 1
            endpoint_cases.append((live, incidence // 4, caps[live - 1]))
    if endpoint_cases != [(3, 13, 0), (7, 30, 16)]:
        raise AssertionError("endpoint capacity cases changed")
    if any(edges <= cap for _, edges, cap in endpoint_cases):
        raise AssertionError("endpoint capacity obstruction failed")

    return {
        "status": "PASS",
        "profile_sha256": digest,
        "compressed_state_count": len(states),
        "subendpoint_survivors": survivors,
        "endpoint_pairs": endpoint_pairs,
        "endpoint_capacity_cases": endpoint_cases,
        "conclusion": "every nonempty square-free K in Q5 has Delta_K >= 219",
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2, sort_keys=True))
