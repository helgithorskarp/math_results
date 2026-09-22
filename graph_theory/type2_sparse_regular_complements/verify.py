#!/usr/bin/env python3
"""Definition-level audit for the explicit cubic family in THEOREM.md."""

from __future__ import annotations

import hashlib
import json
from collections import deque


Graph = dict[int, set[int]]


def add_edge(graph: Graph, u: int, v: int) -> None:
    if u == v or v in graph[u]:
        raise ValueError("graph must stay simple")
    graph[u].add(v)
    graph[v].add(u)


def build_h(m: int) -> tuple[Graph, int, tuple[int, int, int]]:
    if m < 4:
        raise ValueError("m must be at least four")

    order = 6 * m + 4
    graph = {v: set() for v in range(order)}
    subdivisions = []

    for copy in range(3):
        base = copy * (2 * m + 1)

        def vertex(i: int, layer: int) -> int:
            return base + layer * m + i

        for layer in range(2):
            for i in range(m):
                add_edge(graph, vertex(i, layer), vertex((i + 1) % m, layer))

        subdivision = base + 2 * m
        subdivisions.append(subdivision)
        add_edge(graph, vertex(0, 0), subdivision)
        add_edge(graph, subdivision, vertex(0, 1))
        for i in range(1, m):
            add_edge(graph, vertex(i, 0), vertex(i, 1))

    centre = order - 1
    for subdivision in subdivisions:
        add_edge(graph, centre, subdivision)
    return graph, centre, tuple(subdivisions)


def connected(graph: Graph, forbidden_edge: tuple[int, int] | None = None) -> set[int]:
    start = next(iter(graph))
    reached = {start}
    queue = deque([start])
    blocked = None if forbidden_edge is None else frozenset(forbidden_edge)
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if blocked is not None and frozenset((u, v)) == blocked:
                continue
            if v not in reached:
                reached.add(v)
                queue.append(v)
    return reached


def component_from(graph: Graph, start: int, forbidden_edge: tuple[int, int]) -> set[int]:
    reached = {start}
    queue = deque([start])
    blocked = frozenset(forbidden_edge)
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if frozenset((u, v)) == blocked:
                continue
            if v not in reached:
                reached.add(v)
                queue.append(v)
    return reached


def triangle_free(graph: Graph) -> bool:
    return all(not (graph[u] & graph[v]) for u in graph for v in graph[u] if u < v)


def canonical_edges(graph: Graph) -> list[tuple[int, int]]:
    return [(u, v) for u in sorted(graph) for v in sorted(graph[u]) if u < v]


def audit(m: int) -> dict[str, int | bool]:
    graph, centre, subdivisions = build_h(m)
    order = len(graph)
    bridges = []
    odd_sides = []
    for subdivision in subdivisions:
        edge = (centre, subdivision)
        side = component_from(graph, subdivision, edge)
        bridges.append(centre not in side and len(side) < order)
        odd_sides.append(len(side) % 2 == 1)

    return {
        "m": m,
        "order": order,
        "edges": len(canonical_edges(graph)),
        "connected": len(connected(graph)) == order,
        "cubic": all(len(graph[v]) == 3 for v in graph),
        "triangle_free": triangle_free(graph),
        "three_central_bridges": all(bridges),
        "bridge_lobes_odd": all(odd_sides),
        "complement_degree": order - 4,
        "claimed_total_chromatic_number": order - 2,
    }


def main() -> None:
    rows = [audit(m) for m in range(4, 51)]
    required = (
        "connected",
        "cubic",
        "triangle_free",
        "three_central_bridges",
        "bridge_lobes_odd",
    )
    if not all(row[key] for row in rows for key in required):
        raise AssertionError("a structural family check failed")
    for row in rows:
        m = int(row["m"])
        if row["order"] != 6 * m + 4:
            raise AssertionError("order formula failed")
        if row["edges"] != 9 * m + 6:
            raise AssertionError("cubic size formula failed")
        if row["complement_degree"] != 6 * m:
            raise AssertionError("complement degree formula failed")
        if row["claimed_total_chromatic_number"] != 6 * m + 2:
            raise AssertionError("total-chromatic formula failed")

    digest_payload = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    summary = {
        "claim": "chi''(complement(H_m))=6m+2 for every m>=4",
        "checked_m": [4, 50],
        "checked_instances": len(rows),
        "first_order": rows[0]["order"],
        "last_order": rows[-1]["order"],
        "family_audit_sha256": hashlib.sha256(digest_payload).hexdigest(),
        "trust_boundary": "universal result rests on THEOREM.md; code audits the explicit construction",
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
