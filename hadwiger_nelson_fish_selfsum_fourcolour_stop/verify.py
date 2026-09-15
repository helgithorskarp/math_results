#!/usr/bin/env python3
"""Verify an exact four-colour stop for the fixed fish commutative self-sum.

Only the Python standard library is required.  The verifier first replays the
source fish's rational contraction certificate.  It then constructs all 276
unordered sum addresses, derives conservative possible-equality clusters and
possible-unit edges from rational interval bounds, and checks the supplied
four-colouring on that supergraph.
"""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SOURCE = REPO / "hadwiger_nelson_fish_spindle_pair_gate"
sys.path.insert(0, str(SOURCE))

from model import fish  # type: ignore  # noqa: E402


def need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def squared_error_bound(dx: Q, dy: Q, coordinate_error: Q) -> Q:
    return 2 * coordinate_error * (abs(dx) + abs(dy)) + 2 * coordinate_error**2


def components(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    for a, b in edges:
        union(a, b)
    out: dict[int, list[int]] = {}
    for v in range(n):
        out.setdefault(find(v), []).append(v)
    return sorted(out.values(), key=lambda c: c[0])


def main() -> None:
    cert_path = HERE / "certificate.json"
    cert = json.loads(cert_path.read_text())
    need(cert["schema"] == "fish-commutative-selfsum-fourcolour-stop-v1", "schema")
    geometry_path = SOURCE / "geometry_certificate.json"
    geometry_hash = hashlib.sha256(geometry_path.read_bytes()).hexdigest()
    need(geometry_hash == cert["source_geometry_sha256"], "source geometry hash")

    points, _, radius, fish_summary = fish(geometry_path)
    addresses = list(combinations_with_replacement(range(len(points)), 2))
    need(len(addresses) == cert["address_count"] == 276, "address count")
    mids = [
        (points[i][0] + points[j][0], points[i][1] + points[j][1])
        for i, j in addresses
    ]
    sum_error = 2 * radius
    difference_error = 2 * sum_error

    possible_equal = []
    for a, b in combinations(range(len(addresses)), 2):
        if all(abs(mids[a][d] - mids[b][d]) <= 2 * sum_error for d in range(2)):
            possible_equal.append((a, b))
    clusters = components(len(addresses), possible_equal)
    need(len(clusters) == cert["cluster_count"] == 262, "cluster count")
    cluster_of = {}
    for c, members in enumerate(clusters):
        for a in members:
            cluster_of[a] = c

    possible_edges = set()
    separation_gap = None
    excluded_unit_gap = None
    within_cluster_upper = Q(0)
    physical_pair_checks = 0
    for a, b in combinations(range(len(addresses)), 2):
        dx = mids[a][0] - mids[b][0]
        dy = mids[a][1] - mids[b][1]
        d2 = dx * dx + dy * dy
        err = squared_error_bound(dx, dy, difference_error)
        physical_pair_checks += 1
        if cluster_of[a] == cluster_of[b]:
            upper = d2 + err
            need(upper < 1, "within-cluster unit contact not excluded")
            within_cluster_upper = max(within_cluster_upper, upper)
            continue

        # This proves no exact equality can cross two colour clusters.
        need(d2 > err, "possible equality crosses clusters")
        sep = d2 - err
        separation_gap = sep if separation_gap is None else min(separation_gap, sep)
        if abs(d2 - 1) <= err:
            possible_edges.add(tuple(sorted((cluster_of[a], cluster_of[b]))))
        else:
            gap = abs(d2 - 1) - err
            excluded_unit_gap = gap if excluded_unit_gap is None else min(excluded_unit_gap, gap)

    edges = sorted(possible_edges)
    need(
        len(edges) == cert["possible_unit_cluster_edge_count"] == 915,
        "possible-unit cluster edge count",
    )
    graph = {"clusters": clusters, "possible_unit_cluster_edges": edges}
    digest = hashlib.sha256(
        (json.dumps(graph, separators=(",", ":")) + "\n").encode()
    ).hexdigest()
    need(digest == cert["conservative_graph_sha256"], "conservative graph hash")

    word = cert["four_colour_word"]
    need(len(word) == len(clusters), "colour word length")
    need(set(word) <= set("0123"), "colour alphabet")
    need(all(word[a] != word[b] for a, b in edges), "improper four-colouring")

    summary = {
        "status": "EXACT FISH SELF-SUM FOUR-COLOUR STOP VERIFIED",
        "scope": "complete strict unit graph on the exact commutative self-sum",
        "source_geometry_sha256": geometry_hash,
        "source_root_radius": fish_summary["radius"],
        "address_count": len(addresses),
        "distinct_physical_point_upper_bound": len(addresses),
        "possible_equality_cluster_count": len(clusters),
        "physical_address_pair_checks": physical_pair_checks,
        "possible_unit_cluster_edges": len(edges),
        "within_cluster_squared_distance_upper": str(within_cluster_upper),
        "different_cluster_squared_separation_lower": str(separation_gap),
        "excluded_squared_unit_gap_lower": str(excluded_unit_gap),
        "conservative_graph_sha256": digest,
        "proper_four_colouring": True,
        "record_candidate": False,
    }
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    need(summary == expected, "expected summary")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
