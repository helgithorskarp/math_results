#!/usr/bin/env python3
"""Exact, small controls for the extremal-map reduction. Standard library only."""
import argparse
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rank(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    if not a:
        return 0
    require(all(len(row) == len(a[0]) for row in a), "ragged matrix")
    r = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        p = a[r][col]
        a[r] = [v / p for v in a[r]]
        for i in range(r + 1, len(a)):
            factor = a[i][col]
            if factor:
                a[i] = [u - factor * v for u, v in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def distance2(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


def connected(n, edges):
    adjacency = [set() for _ in range(n)]
    for i, j in edges:
        adjacency[i].add(j)
        adjacency[j].add(i)
    seen = {0}
    todo = [0]
    while todo:
        for j in adjacency[todo.pop()] - seen:
            seen.add(j)
            todo.append(j)
    return len(seen) == n


def rigidity_rank(points, edges):
    rows = []
    for i, j in edges:
        row = [0] * (3 * len(points))
        for c in range(3):
            row[3 * i + c] = points[i][c] - points[j][c]
            row[3 * j + c] = -row[3 * i + c]
        rows.append(row)
    return rank(rows)


def audit(x, y):
    n = len(x)
    require(n == len(y) and n >= 4, "invalid configuration sizes")
    require(all(len(p) == 3 for p in x + y), "expected 3D sites")
    require(len(set(x)) == n, "input sites must be distinct")
    edges = []
    deficits = []
    for i, j in combinations(range(n), 2):
        deficit = distance2(x[i], x[j]) - distance2(y[i], y[j])
        require(deficit >= 0, "expansive pair")
        if deficit == 0:
            edges.append((i, j))
        else:
            deficits.append(deficit)
    paired = [tuple(p) + tuple(q) for p, q in zip(x, y)]
    paired_rank = rank([[u - v for u, v in zip(p, paired[0])]
                        for p in paired[1:]])
    return {
        "input_sites": n,
        "distinct_output_sites": len(set(y)),
        "pairs": n * (n - 1) // 2,
        "tight_pairs": len(edges),
        "strict_pairs": len(deficits),
        "tight_graph_connected": connected(n, edges),
        "input_rigidity_rank": rigidity_rank(x, edges),
        "output_rigidity_rank": rigidity_rank(y, edges),
        "paired_affine_rank": paired_rank,
        "positive_squared_deficits": sorted(set(deficits)),
    }


def flap_control():
    # Preserve the ordering used in the published Team fixture.
    v = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    x, y = list(v), list(v)
    for i in range(4):
        for j in range(4):
            if i != j:
                x.append(tuple(v[j][c] - v[i][c] for c in range(3)))
                y.append(tuple(v[j][c] + v[i][c] for c in range(3)))
    result = audit(x, y)
    require(result["input_rigidity_rank"] == 42, "source flap rigidity")
    require(result["output_rigidity_rank"] == 42, "image flap rigidity")
    require(result["paired_affine_rank"] == 6, "flap paired rank")
    # Optional comparison is reported separately by the reproduction commands;
    # this verifier has no dependency on the neighboring package.
    return result


def mesh_control():
    # Four tetrahedra partition the unit octahedron around its vertical edge.
    x = [(0, 0, -1), (0, 0, 1),
         (1, 0, 0), (0, 1, 0), (-1, 0, 0), (0, -1, 0)]
    cells = [(0, 1, 2 + i, 2 + ((i + 1) % 4)) for i in range(4)]
    mesh_edges = sorted({tuple(sorted(e)) for c in cells
                         for e in combinations(c, 2)})
    require(rigidity_rank(x, mesh_edges) == 12, "mesh source rigidity")
    accepted = []
    rejected = []
    # Along the dual path 0--1--2--3 the common face planes are x=0,y=0,x=0.
    for choices in product((0, 1), repeat=3):
        diagonal = (1, 1, 1)
        cell_maps = [diagonal]
        for bit, axis in zip(choices, (0, 1, 0)):
            d = list(diagonal)
            if bit:
                d[axis] *= -1
            diagonal = tuple(d)
            cell_maps.append(diagonal)
        images = {}
        consistent = True
        for cell, diagonal in zip(cells, cell_maps):
            for i in cell:
                image = tuple(d * t for d, t in zip(diagonal, x[i]))
                if i in images and images[i] != image:
                    consistent = False
                images[i] = image
        key = "".join(map(str, choices))
        if not consistent:
            rejected.append(key)
            continue
        y = [images[i] for i in range(len(x))]
        result = audit(x, y)
        require(all(distance2(x[i], x[j]) == distance2(y[i], y[j])
                    for i, j in mesh_edges), "mesh edge not tight")
        require(rigidity_rank(y, mesh_edges) == 12, "mesh image rigidity")
        accepted.append({"tree_choices": key, "audit": result})
    require(len(accepted) == len(rejected) == 4, "cycle consistency count")
    return {"tetrahedra": len(cells), "mesh_edges": len(mesh_edges),
            "tree_choices": 8, "accepted": accepted, "rejected": rejected}


def run():
    require(rank([[1, 2], [2, 4]]) == 1, "rank positive control")
    require(rank([[0, 0], [0, 0]]) == 0, "rank zero control")
    x = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
    try:
        audit(x, [tuple(2 * t for t in p) for p in x])
    except ValueError as exc:
        require(str(exc) == "expansive pair", "wrong rejection reason")
    else:
        raise ValueError("expansive control accepted")
    return {"arithmetic": "integer and fractions.Fraction",
            "expansive_control_rejected": True,
            "flap": flap_control(), "mesh": mesh_control()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = run()
    if args.check:
        expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
        require(result == expected, "expected record mismatch")
        print("PASS: rigid flap and all eight mesh fold choices")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
