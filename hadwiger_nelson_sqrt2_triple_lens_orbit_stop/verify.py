#!/usr/bin/env python3
"""Exact standard-library checker for one sqrt(2) triple-lens orbit closure."""

import argparse
from collections import deque
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ZERO = (F(0),) * 4


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dump(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n"


# (a,b,c,d) represents (a sqrt2+b sqrt6)+i(c sqrt2+d sqrt6).
def add(p, q, scale=F(1)):
    return tuple(x + scale*y for x, y in zip(p, q))


def half(p):
    return tuple(x/2 for x in p)


def times_i(p):
    a, b, c, d = p
    return (-c, -d, a, b)


def rotate60(p):
    a, b, c, d = p
    return ((a-3*d)/2, (b-c)/2, (3*b+c)/2, (a+d)/2)


def squared_distance(p, q):
    a, b, c, d = add(p, q, -1)
    return (2*a*a+6*b*b+2*c*c+6*d*d, 4*a*b+4*c*d)


def unit(p, q):
    return squared_distance(p, q) == (1, 0)


def point_rows(points):
    return [[[x.numerator, x.denominator] for x in p] for p in points]


def k_core(adj, k):
    degree = list(map(len, adj))
    removed = [False] * len(adj)
    queue = deque(i for i, d in enumerate(degree) if d < k)
    while queue:
        a = queue.popleft()
        if removed[a]:
            continue
        removed[a] = True
        for b in adj[a]:
            if not removed[b]:
                degree[b] -= 1
                if degree[b] < k:
                    queue.append(b)
    return [i for i in range(len(adj)) if not removed[i]]


def cuts_and_bridges(adj):
    clock = 0
    seen, low, parent = [-1]*len(adj), [0]*len(adj), [-1]*len(adj)
    cuts, bridges = set(), []

    def visit(a):
        nonlocal clock
        seen[a] = low[a] = clock
        clock += 1
        children = 0
        for b in sorted(adj[a]):
            if seen[b] < 0:
                parent[b] = a
                children += 1
                visit(b)
                low[a] = min(low[a], low[b])
                if parent[a] < 0 and children > 1:
                    cuts.add(a)
                if parent[a] >= 0 and low[b] >= seen[a]:
                    cuts.add(a)
                if low[b] > seen[a]:
                    bridges.append([min(a, b), max(a, b)])
            elif b != parent[a]:
                low[a] = min(low[a], seen[b])

    for a in range(len(adj)):
        if seen[a] < 0:
            visit(a)
    return sorted(cuts), sorted(bridges)


def check_word(word, colours, edges, pins=None):
    pins = pins or {}
    require(isinstance(word, str) and len(word) == 33,
            "colour-word length")
    require(set(word) <= set(map(str, range(colours))), "colour-word alphabet")
    require(all(word[a] != word[b] for a, b in edges), "proper colour word")
    require(all(int(word[v]) == c for v, c in pins.items()), "centre pins")


def reconstruct():
    centres = [ZERO, (F(1), F(0), F(0), F(0)),
               (F(1, 2), F(0), F(0), F(1, 2))]
    require(all(squared_distance(centres[i], centres[j]) == (2, 0)
                for i in range(3) for j in range(i+1, 3)),
            "equilateral sqrt(2) centres")
    formal = [(c, ["centre", i]) for i, c in enumerate(centres)]
    lens_count = 0
    for i in range(3):
        for j in range(i+1, 3):
            delta = add(centres[j], centres[i], -1)
            midpoint = half(add(centres[i], centres[j]))
            perpendicular = half(times_i(delta))
            for sign in (-1, 1):
                lens = add(midpoint, perpendicular, sign)
                require(unit(lens, centres[i]) and unit(lens, centres[j]),
                        "complete circle intersection")
                lens_count += 1
                for owner in (i, j):
                    direction = add(lens, centres[owner], -1)
                    for step in range(6):
                        formal.append((add(centres[owner], direction),
                                       ["orbit", i, j, sign, owner, step]))
                        direction = rotate60(direction)
                    require(direction == add(lens, centres[owner], -1),
                            "sixfold orbit closes")
    require(lens_count == 6 and len(formal) == 75, "raw architecture")

    points, index, provenance = [], {}, []
    for point, source in formal:
        if point not in index:
            index[point] = len(points)
            points.append(point)
            provenance.append([])
        provenance[index[point]].append(source)
    require(len(points) == 33, "collision-merged order")
    centre_ids = [index[c] for c in centres]
    require(centre_ids == [0, 1, 2], "centre ordering")

    edges = [[a, b] for a in range(len(points))
             for b in range(a+1, len(points)) if unit(points[a], points[b])]
    require(len(edges) == 78, "complete unit-edge count")
    adj = [set() for _ in points]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return points, provenance, centre_ids, edges, adj


def verify(certificate, expected):
    points, provenance, centre_ids, edges, adj = reconstruct()
    rows = point_rows(points)
    point_sha = hashlib.sha256((json.dumps(rows, separators=(",", ":"))+"\n").encode()).hexdigest()
    edge_sha = hashlib.sha256((json.dumps(edges, separators=(",", ":"))+"\n").encode()).hexdigest()

    # Direct formula: four times the imaginary sqrt(2) coefficient modulo 3.
    three_word = "".join(str(int(4*p[2]) % 3) for p in points)
    check_word(three_word, 3, edges)
    triangle = certificate["triangle"]
    edge_set = {tuple(e) for e in edges}
    require(len(triangle) == 3 and len(set(triangle)) == 3, "triangle shape")
    require(all(tuple(sorted((triangle[i], triangle[(i+1) % 3]))) in edge_set
                for i in range(3)), "triangle edges")

    patterns = ["000", "001", "010", "011", "012"]
    require(sorted(certificate["centre_relation"]) == patterns,
            "canonical centre patterns")
    for pattern in patterns:
        pins = {v: int(c) for v, c in zip(centre_ids, pattern)}
        check_word(certificate["centre_relation"][pattern], 4, edges, pins)

    # Graph invariants are reconstructed from the complete physical graph.
    seen, component_orders = set(), []
    for root in range(len(points)):
        if root in seen:
            continue
        stack, size = [root], 0
        seen.add(root)
        while stack:
            a = stack.pop()
            size += 1
            for b in adj[a]:
                if b not in seen:
                    seen.add(b)
                    stack.append(b)
        component_orders.append(size)
    cuts, bridges = cuts_and_bridges(adj)
    triangles = sum(len(adj[a] & adj[b]) for a, b in edges) // 3
    histogram = {}
    for sources in provenance:
        histogram[str(len(sources))] = histogram.get(str(len(sources)), 0)+1
    report = {
        "verified": True,
        "record_improvement": False,
        "scope": "equilateral-sqrt(2) independent triple, complete first lens-orbit closure",
        "raw_formal_points": 75,
        "physical_points": len(points),
        "complete_unit_edges": len(edges),
        "pair_checks": len(points)*(len(points)-1)//2,
        "collision_histogram": histogram,
        "centre_ids": centre_ids,
        "centre_relation_patterns": patterns,
        "centre_relation_neutral": True,
        "component_orders": sorted(component_orders, reverse=True),
        "articulation_vertices": cuts,
        "bridges": bridges,
        "minimum_degree": min(map(len, adj)),
        "maximum_degree": max(map(len, adj)),
        "triangles": triangles,
        "three_core_vertices": len(k_core(adj, 3)),
        "four_core_vertices": len(k_core(adj, 4)),
        "five_core_vertices": len(k_core(adj, 5)),
        "chromatic_number": 3,
        "point_sha256": point_sha,
        "edge_sha256": edge_sha,
    }
    require(report == expected, "expected report")
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE/"certificate.json")
    parser.add_argument("--expected", type=Path, default=HERE/"expected.json")
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    expected = json.loads(args.expected.read_text())
    print(dump(verify(certificate, expected)), end="")


if __name__ == "__main__":
    main()
