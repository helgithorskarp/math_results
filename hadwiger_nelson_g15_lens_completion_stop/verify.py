#!/usr/bin/env python3
"""Primary exact verifier for the G15 full-lens four-colour stop."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import model

HERE = Path(__file__).resolve().parent


def edge_masks(n, edges):
    masks = [0] * n
    for u, v in edges:
        if not (0 <= u < v < n):
            raise ValueError("invalid edge")
        masks[u] |= 1 << v
        masks[v] |= 1 << u
    return masks


def small_graph_invariants(n, edges):
    masks = edge_masks(n, edges)
    independent = [True] * (1 << n)
    for subset in range(1, 1 << n):
        bit = subset & -subset
        v = bit.bit_length() - 1
        independent[subset] = independent[subset ^ bit] and not (masks[v] & (subset ^ bit))
    alpha = max(s.bit_count() for s, ok in enumerate(independent) if ok)

    @lru_cache(maxsize=None)
    def chi(subset):
        if subset == 0:
            return 0
        first = subset & -subset
        best = subset.bit_count()
        part = subset
        while part:
            if part & first and independent[part]:
                best = min(best, 1 + chi(subset ^ part))
            part = (part - 1) & subset
        return best

    return chi((1 << n) - 1), alpha


def decide_k_colour(n, edges, k):
    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    colours = [-1] * n
    nodes = 0

    def search(done):
        nonlocal nodes
        nodes += 1
        if done == n:
            return True
        vertex = max(
            (v for v in range(n) if colours[v] < 0),
            key=lambda v: (len({colours[w] for w in adjacency[v] if colours[w] >= 0}),
                           len(adjacency[v]), -v),
        )
        forbidden = {colours[w] for w in adjacency[vertex] if colours[w] >= 0}
        for colour in range(k):
            if colour in forbidden:
                continue
            colours[vertex] = colour
            if search(done + 1):
                return True
            colours[vertex] = -1
        return False

    feasible = search(0)
    return feasible, colours[:] if feasible else None, nodes


def verify_word(word, n, edges):
    if not isinstance(word, str) or len(word) != n or any(c not in "0123" for c in word):
        raise ValueError("invalid four-colour word")
    values = [int(c) for c in word]
    for u, v in edges:
        if values[u] == values[v]:
            raise ValueError(f"monochromatic edge {(u, v)}")


def verify_certificate(cert):
    if cert.get("format") != "g15-full-lens-fourcolour-v1":
        raise ValueError("unexpected certificate format")
    points, owners, source_unit, source_third, source_four = model.physical_support()
    edges = model.complete_edges(points)
    if len(points) != cert["physical_vertices"] or len(edges) != cert["strict_unit_edges"]:
        raise ValueError("physical graph count mismatch")
    if [len(source_unit), len(source_third), len(source_four)] != cert["source_distance_counts"]:
        raise ValueError("G15 distance count mismatch")
    if sum(len(group) for group in owners) != cert["formal_addresses"]:
        raise ValueError("formal-address count mismatch")
    collisions = [group for group in owners if len(group) > 1]
    if collisions != cert["collision_classes"]:
        raise ValueError("collision-class mismatch")
    if model.sha256(model.point_stream(points)) != cert["point_stream_sha256"]:
        raise ValueError("point hash mismatch")
    if model.sha256(model.edge_stream(edges)) != cert["edge_stream_sha256"]:
        raise ValueError("edge hash mismatch")

    # Every declared lens is checked against its two source owners.  The
    # all-pairs scan above independently supplies every additional unit edge.
    label_to_index = {label: i for i, group in enumerate(owners) for label in group}
    for i, j in source_third:
        for sign in ("+", "-"):
            x = label_to_index[f"L13:{i}:{j}:{sign}"]
            if model.squared_distance(points[x], points[i]) != model.ONE or model.squared_distance(points[x], points[j]) != model.ONE:
                raise ValueError("bad two-root lens incidence")
    for i, j in source_four:
        x = label_to_index[f"L4:{i}:{j}"]
        if model.squared_distance(points[x], points[i]) != model.ONE or model.squared_distance(points[x], points[j]) != model.ONE:
            raise ValueError("bad tangent lens incidence")

    d_edges = sorted(source_unit + source_third + source_four)
    source_chi, source_alpha = small_graph_invariants(15, d_edges)
    if [source_chi, source_alpha] != cert["source_D_graph_chi_alpha"]:
        raise ValueError("source D-graph invariant mismatch")

    verify_word(cert["four_colouring"], len(points), edges)
    three_feasible, _, three_nodes = decide_k_colour(len(points), edges, 3)
    if three_feasible or three_nodes != cert["three_colour_search_nodes"]:
        raise ValueError("three-colour decision mismatch")
    return {
        "status": "EXACT G15 FULL-LENS FOUR-COLOUR STOP VERIFIED",
        "source": {"vertices": 15, "D_edges": len(d_edges), "distance_counts": cert["source_distance_counts"], "chi": source_chi, "alpha": source_alpha},
        "support": {"formal_addresses": cert["formal_addresses"], "physical_vertices": len(points), "strict_unit_edges": len(edges), "collision_classes": len(collisions), "chi": 4},
        "three_colour_search_nodes": three_nodes,
        "point_stream_sha256": cert["point_stream_sha256"],
        "edge_stream_sha256": cert["edge_stream_sha256"],
    }


def main():
    cert = json.loads((HERE / "certificate.json").read_text())
    result = verify_certificate(cert)
    expected = json.loads((HERE / "expected.json").read_text())
    if result != expected:
        raise ValueError("expected-output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
