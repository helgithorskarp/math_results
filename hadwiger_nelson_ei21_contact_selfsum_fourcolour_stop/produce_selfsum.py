#!/usr/bin/env python3
"""Build the conservative self-sum graph and its four-colour certificate.

This optional producer uses python-sat.  ``verify.py`` independently rebuilds
the graph with exact rational arithmetic and checks the emitted word.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement
from pathlib import Path

from pysat.solvers import Cadical195


HERE = Path(__file__).resolve().parent
GEOMETRY = HERE / "geometry_certificate.json"


def components(n, edges):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for a, b in edges:
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a
    out = {}
    for v in range(n):
        out.setdefault(find(v), []).append(v)
    return sorted(out.values(), key=lambda c: c[0])


def squared_error(dx, dy, error):
    return 2*error*(abs(dx)+abs(dy))+2*error*error


def graph():
    geometry = json.loads(GEOMETRY.read_text())
    h = geometry["midpoint_denominator"]
    points = [tuple(Q(x, h) for x in p) for p in geometry["midpoint_numerators"]]
    radius = Q(1, geometry["radius_denominator"])
    addresses = list(combinations_with_replacement(range(21), 2))
    mids = [(points[i][0]+points[j][0], points[i][1]+points[j][1])
            for i, j in addresses]
    address_error = 2*radius
    possible_equal = [(a, b) for a, b in combinations(range(231), 2)
                      if all(abs(mids[a][d]-mids[b][d]) <= 2*address_error
                             for d in range(2))]
    clusters = components(231, possible_equal)
    cluster_of = {a: c for c, members in enumerate(clusters) for a in members}
    pair_error = 2*address_error
    possible_edges = set()
    for a, b in combinations(range(231), 2):
        dx = mids[a][0]-mids[b][0]; dy = mids[a][1]-mids[b][1]
        distance2 = dx*dx+dy*dy
        error = squared_error(dx, dy, pair_error)
        if cluster_of[a] == cluster_of[b]:
            if distance2+error >= 1:
                raise ValueError("possible internal unit edge")
        else:
            if distance2 <= error:
                raise ValueError("possible equality crosses clusters")
            if abs(distance2-1) <= error:
                possible_edges.add(tuple(sorted((cluster_of[a], cluster_of[b]))))
    return clusters, sorted(possible_edges)


def colour(n, edges):
    def var(v, c): return 4*v+c+1
    clauses = []
    for v in range(n):
        clauses.append([var(v, c) for c in range(4)])
        clauses.extend([-var(v, a), -var(v, b)]
                       for a, b in combinations(range(4), 2))
    for a, b in edges:
        clauses.extend([[-var(a, c), -var(b, c)] for c in range(4)])
    with Cadical195(bootstrap_with=clauses) as solver:
        if not solver.solve():
            raise ValueError("conservative graph is not four-colourable")
        model = {x for x in solver.get_model() if x > 0}
    word = "".join(str(next(c for c in range(4) if var(v, c) in model))
                   for v in range(n))
    if not all(word[a] != word[b] for a, b in edges):
        raise ValueError("improper word")
    return word


def build(output):
    if output.exists():
        raise FileExistsError(output)
    clusters, edges = graph()
    stream = json.dumps({"clusters": clusters, "edges": edges},
                        separators=(",", ":"))+"\n"
    certificate = {
        "schema": "ei21-contact-commutative-selfsum-fourcolour-stop-v1",
        "geometry_sha256": hashlib.sha256(GEOMETRY.read_bytes()).hexdigest(),
        "formal_address_count": 231,
        "possible_equality_cluster_count": len(clusters),
        "possible_unit_cluster_edge_count": len(edges),
        "conservative_graph_sha256": hashlib.sha256(stream.encode()).hexdigest(),
        "four_colour_word": colour(len(clusters), edges),
    }
    output.write_text(json.dumps(certificate, indent=2, sort_keys=True)+"\n")
    return {k: v for k, v in certificate.items() if k != "four_colour_word"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.output), indent=2, sort_keys=True))
