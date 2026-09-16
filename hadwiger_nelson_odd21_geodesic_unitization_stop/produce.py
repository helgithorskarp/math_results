#!/usr/bin/env python3
"""Produce the exact straight-chain unitization certificate for odd21."""

import argparse
import hashlib
import json
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path


BASE_NM = (
    (0, 0), (8, 0), (3, 0), (0, 3), (5, 3), (5, 0),
    (0, 5), (3, 5), (2, 3), (3, 3), (3, 2),
)
LENGTHS = (1, 3, 5, 7)


def add(p, q):
    return tuple(a + b for a, b in zip(p, q, strict=True))


def sub(p, q):
    return tuple(a - b for a, b in zip(p, q, strict=True))


def scale(p, r):
    return tuple(r * a for a in p)


def squared_norm(p):
    """For p=(a+b sqrt(85)) + i(c sqrt(3)+d sqrt(255))."""
    a, b, c, d = p
    return a*a + 85*b*b + 3*c*c + 255*d*d, 2*a*b + 6*c*d


def source_points():
    base = tuple((Q(2*n + m, 2), Q(0), Q(m, 2), Q(0)) for n, m in BASE_NM)

    def rotate(p):
        a, b, c, d = p
        assert b == d == 0
        return (Q(127, 128)*a, -Q(3, 128)*c,
                Q(127, 128)*c, Q(1, 128)*a)

    return base + tuple(rotate(p) for p in base[1:])


def source_edges(points):
    result = []
    for u, v in combinations(range(len(points)), 2):
        n = squared_norm(sub(points[u], points[v]))
        for length in LENGTHS:
            if n == (Q(length*length), Q(0)):
                result.append((u, v, length))
                break
    return result


def support():
    source = source_points()
    constraints = source_edges(source)
    raw = list(source)
    for u, v, length in constraints:
        for step in range(1, length):
            raw.append(add(source[u], scale(sub(source[v], source[u]), Q(step, length))))
    points = sorted(set(raw))
    index = {p: i for i, p in enumerate(points)}
    source_index = [index[p] for p in source]
    edges = []
    for u, v in combinations(range(len(points)), 2):
        if squared_norm(sub(points[u], points[v])) == (Q(1), Q(0)):
            edges.append((u, v))
    segments = set()
    for u, v, length in constraints:
        for step in range(length):
            p = add(source[u], scale(sub(source[v], source[u]), Q(step, length)))
            q = add(source[u], scale(sub(source[v], source[u]), Q(step + 1, length)))
            segments.add(tuple(sorted((index[p], index[q]))))
    return points, constraints, source_index, edges, sorted(segments)


def colouring(vertex_count, edges, colours, equal_pair=None):
    """Canonical DSATUR search, optionally identifying one vertex pair."""
    parent = list(range(vertex_count))

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    if equal_pair is not None:
        a, b = equal_pair
        parent[find(b)] = find(a)
    roots = sorted({find(v) for v in range(vertex_count)})
    root_id = {r: i for i, r in enumerate(roots)}
    component = [root_id[find(v)] for v in range(vertex_count)]
    adjacency = [set() for _ in roots]
    for u, v in edges:
        a, b = component[u], component[v]
        if a == b:
            return None, 0
        adjacency[a].add(b)
        adjacency[b].add(a)
    word = [-1] * len(roots)
    nodes = 0

    def visit(done):
        nonlocal nodes
        nodes += 1
        if done == len(word):
            return True
        remaining = (v for v in range(len(word)) if word[v] < 0)
        vertex = max(remaining, key=lambda v: (
            len({word[w] for w in adjacency[v] if word[w] >= 0}),
            len(adjacency[v]), -v))
        used = {word[w] for w in adjacency[vertex] if word[w] >= 0}
        # Colour names are interchangeable: try at most one new name.
        limit = min(colours, max(word, default=-1) + 2)
        for colour in range(limit):
            if colour in used:
                continue
            word[vertex] = colour
            if visit(done + 1):
                return True
            word[vertex] = -1
        return False

    if not visit(0):
        return None, nodes
    return [word[component[v]] for v in range(vertex_count)], nodes


def encoded_point(point):
    return [[x.numerator, x.denominator] for x in point]


def digest(value):
    raw = json.dumps(value, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()


def produce():
    points, constraints, source_index, edges, segments = support()
    three_word, three_nodes = colouring(len(points), edges, 3)
    two_word, two_nodes = colouring(len(points), edges, 2)
    assert three_word is not None and two_word is None

    equality_witnesses = []
    equality_nodes = 0
    for u, v, length in constraints:
        if length == 1:
            continue
        word, nodes = colouring(len(points), edges, 3,
                                (source_index[u], source_index[v]))
        equality_nodes += nodes
        if word is None:
            # The design is meant to test every long source constraint.  A
            # missing witness would be positive forcing evidence, not a stop.
            raise RuntimeError(f"constraint {(u, v, length)} unexpectedly supported")
        equality_witnesses.append({
            "source_edge": [u, v, length],
            "colouring": "".join(map(str, word)),
        })

    histogram = {str(length): 0 for length in LENGTHS}
    for _, _, length in constraints:
        histogram[str(length)] += 1
    return {
        "architecture": "straight_geodesic_odd_unit_chains",
        "raw_budget_equation": "21+26*(3-1)+14*(5-1)+8*(7-1)=177",
        "raw_point_occurrences": 177,
        "physical_points": len(points),
        "collision_savings": 177 - len(points),
        "complete_unit_edges": len(edges),
        "intended_distinct_unit_segments": len(segments),
        "incidental_unit_edges": len(set(edges) - set(segments)),
        "source_constraints": len(constraints),
        "source_length_histogram": histogram,
        "supported_unit_constraints": histogram["1"],
        "unsupported_long_constraints": len(equality_witnesses),
        "chromatic_number": 3,
        "source_indices": source_index,
        "points_sha256": digest([encoded_point(p) for p in points]),
        "edges_sha256": digest(edges),
        "segments_sha256": digest(segments),
        "three_colouring": "".join(map(str, three_word)),
        "equality_witnesses": equality_witnesses,
        "search_nodes": {
            "two_colour_unsat": two_nodes,
            "three_colour_sat": three_nodes,
            "all_equality_witnesses": equality_nodes,
        },
        "record_candidate": False,
        "stop_reason": "all_48_nonunit_source_constraints_are_unsupported",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = produce()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
