#!/usr/bin/env python3
"""Independent exact checker for the odd21 straight-chain stop."""

import argparse
import hashlib
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE = ((0, 0), (8, 0), (3, 0), (0, 3), (5, 3), (5, 0),
        (0, 5), (3, 5), (2, 3), (3, 3), (3, 2))


def plus(x, y):
    return tuple(a + b for a, b in zip(x, y, strict=True))


def minus(x, y):
    return tuple(a - b for a, b in zip(x, y, strict=True))


def scalar(r, x):
    return tuple(r*a for a in x)


def norm(x):
    # x-coordinate a+b sqrt(85); y-coordinate c sqrt(3)+d sqrt(255).
    a, b, c, d = x
    return (a*a + 85*b*b + 3*c*c + 255*d*d,
            2*a*b + 6*c*d)


def reconstruct():
    Q = Fraction
    left = [(Q(2*n + m, 2), Q(0), Q(m, 2), Q(0)) for n, m in BASE]
    right = [(Q(127, 128)*a, -Q(3, 128)*c,
              Q(127, 128)*c, Q(1, 128)*a) for a, _, c, _ in left[1:]]
    source = left + right
    assert len(source) == len(set(source)) == 21

    constraints = []
    for u, v in combinations(range(21), 2):
        value = norm(minus(source[u], source[v]))
        for length in (1, 3, 5, 7):
            if value == (Q(length*length), Q(0)):
                constraints.append((u, v, length))
                break

    occurrences = list(source)
    for u, v, length in constraints:
        delta = minus(source[v], source[u])
        occurrences.extend(plus(source[u], scalar(Q(k, length), delta))
                           for k in range(1, length))
    points = sorted(set(occurrences))
    where = {p: i for i, p in enumerate(points)}
    source_indices = [where[p] for p in source]

    edges = [(u, v) for u, v in combinations(range(len(points)), 2)
             if norm(minus(points[u], points[v])) == (Q(1), Q(0))]
    segments = set()
    for u, v, length in constraints:
        delta = minus(source[v], source[u])
        chain = [where[plus(source[u], scalar(Q(k, length), delta))]
                 for k in range(length + 1)]
        segments.update(tuple(sorted(pair)) for pair in zip(chain, chain[1:]))
    return source, constraints, points, source_indices, edges, sorted(segments)


def serial_point(point):
    return [[x.numerator, x.denominator] for x in point]


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def check_word(word, vertex_count, edges, colours):
    if not isinstance(word, str) or len(word) != vertex_count:
        raise ValueError("bad colouring length")
    if any(c not in "0123456789" or int(c) >= colours for c in word):
        raise ValueError("bad colour")
    if any(word[u] == word[v] for u, v in edges):
        raise ValueError("monochromatic unit edge")


def bipartite(vertex_count, edges):
    adjacency = [[] for _ in range(vertex_count)]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    colour = [-1] * vertex_count
    for root in range(vertex_count):
        if colour[root] >= 0:
            continue
        colour[root] = 0
        stack = [root]
        while stack:
            u = stack.pop()
            for v in adjacency[u]:
                if colour[v] < 0:
                    colour[v] = 1 - colour[u]
                    stack.append(v)
                elif colour[v] == colour[u]:
                    return False
    return True


def verify(certificate):
    source, constraints, points, source_indices, edges, segments = reconstruct()
    edge_set = set(edges)
    segment_set = set(segments)
    histogram = {str(d): sum(length == d for _, _, length in constraints)
                 for d in (1, 3, 5, 7)}
    fixed = {
        "architecture": "straight_geodesic_odd_unit_chains",
        "raw_budget_equation": "21+26*(3-1)+14*(5-1)+8*(7-1)=177",
        "raw_point_occurrences": 177,
        "physical_points": 115,
        "collision_savings": 62,
        "complete_unit_edges": 219,
        "intended_distinct_unit_segments": 141,
        "incidental_unit_edges": 78,
        "source_constraints": 55,
        "source_length_histogram": {"1": 7, "3": 26, "5": 14, "7": 8},
        "supported_unit_constraints": 7,
        "unsupported_long_constraints": 48,
        "chromatic_number": 3,
        "source_indices": source_indices,
        "points_sha256": digest([serial_point(p) for p in points]),
        "edges_sha256": digest(edges),
        "segments_sha256": digest(segments),
        "record_candidate": False,
        "stop_reason": "all_48_nonunit_source_constraints_are_unsupported",
    }
    for key, value in fixed.items():
        if certificate.get(key) != value:
            raise ValueError(f"mismatch in {key}")
    if histogram != fixed["source_length_histogram"]:
        raise AssertionError("source histogram reconstruction failed")
    if len(points) != 115 or len(edges) != 219 or len(segments) != 141:
        raise AssertionError("geometric count mismatch")
    if not segment_set <= edge_set or len(edge_set - segment_set) != 78:
        raise AssertionError("complete-edge accounting failed")
    # The three source vertices I1,I2,I3 form a physical unit triangle.
    triangle = [source_indices[i] for i in (8, 9, 10)]
    if any(tuple(sorted(pair)) not in edge_set for pair in combinations(triangle, 2)):
        raise AssertionError("lower-bound triangle missing")
    if bipartite(len(points), edges):
        raise AssertionError("claimed triangle graph is bipartite")
    check_word(certificate.get("three_colouring"), len(points), edges, 3)

    long_constraints = {(u, v, d) for u, v, d in constraints if d != 1}
    records = certificate.get("equality_witnesses")
    if not isinstance(records, list) or len(records) != 48:
        raise ValueError("wrong equality-witness count")
    seen = set()
    for record in records:
        triple = tuple(record.get("source_edge", ()))
        if triple not in long_constraints or triple in seen:
            raise ValueError("bad or repeated source constraint")
        seen.add(triple)
        word = record.get("colouring")
        check_word(word, len(points), edges, 3)
        u, v, _ = triple
        if word[source_indices[u]] != word[source_indices[v]]:
            raise ValueError("witness does not refute endpoint inequality")
    if seen != long_constraints:
        raise ValueError("not every long source constraint is refuted")

    searches = certificate.get("search_nodes")
    if not isinstance(searches, dict) or set(searches) != {
            "two_colour_unsat", "three_colour_sat", "all_equality_witnesses"}:
        raise ValueError("bad search metadata")
    if any(type(value) is not int or value <= 0 for value in searches.values()):
        raise ValueError("bad search count")
    return {
        "physical_points": len(points),
        "complete_unit_edges": len(edges),
        "chromatic_number": 3,
        "incidental_unit_edges": len(edge_set - segment_set),
        "long_source_constraints_with_equal_endpoint_witness": len(seen),
        "record_candidate": False,
        "verified": True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path, nargs="?",
                        default=HERE / "certificate.json")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = verify(json.loads(args.certificate.read_text()))
    if args.check_expected:
        expected = json.loads((HERE / "expected.json").read_text())
        if result != expected:
            raise ValueError("expected-result mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
