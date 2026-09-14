#!/usr/bin/env python3
"""Generate separating four-colouring bases for two exact small supports."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

from pysat.solvers import Cadical195


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DEPENDENCIES = {
    "hadwiger_nelson_heptagon_moser_sum/field.py":
        "55d016633f1c18cece1a94edf90c97a6bafc7d0aec99b31dad355f1df86e1678",
    "hadwiger_nelson_heptagon_difference_lifts/geometry.py":
        "67599414c9cabc9e1e9f0100907c3c039200deea4ffd935cb6ba09d67c57ef07",
    "hadwiger_nelson_golomb_rotation_sum/verify.py":
        "b789bb72ce30e8aa69e1e2fa7c5797d1844f6aa73d535ecd223953e9cbab48a5",
}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


HFIELD = load("small_equal_pair_heptagon_field", ROOT / "hadwiger_nelson_heptagon_moser_sum" / "field.py")
GOLOMB = load("small_equal_pair_golomb", ROOT / "hadwiger_nelson_golomb_rotation_sum" / "verify.py")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def heptagon_moser_graph():
    h_points, m_points, denominator = HFIELD.construction()
    points = sorted({HFIELD.add(h, m) for h in h_points for m in m_points})
    target = HFIELD.scale(HFIELD.ONE, denominator * denominator)
    edges = [
        (u, v)
        for u, v in itertools.combinations(range(len(points)), 2)
        if HFIELD.norm(HFIELD.sub(points[u], points[v])) == target
    ]
    return len(points), edges


def quotient_graph(case):
    unit, collision = case
    parent = list(range(100))

    def find(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for u, v in collision:
        u, v = find(u), find(v)
        if u != v:
            parent[v] = u
    roots = sorted({find(vertex) for vertex in range(100)})
    index = {root: i for i, root in enumerate(roots)}
    image = [index[find(vertex)] for vertex in range(100)]
    edges = sorted({tuple(sorted((image[u], image[v]))) for u, v in unit})
    if any(u == v for u, v in edges):
        raise RuntimeError("unit pair collapsed")
    return len(roots), edges


def separating_basis(n, edges):
    edge_set = set(edges)
    var = lambda vertex, colour: 4 * vertex + colour + 1
    clauses = []
    for vertex in range(n):
        clauses.append([var(vertex, colour) for colour in range(4)])
        for c, d in itertools.combinations(range(4), 2):
            clauses.append([-var(vertex, c), -var(vertex, d)])
    for u, v in edges:
        for colour in range(4):
            clauses.append([-var(u, colour), -var(v, colour)])
    unresolved = {
        pair for pair in itertools.combinations(range(n), 2) if pair not in edge_set
    }
    words = []
    with Cadical195(bootstrap_with=clauses) as solver:
        while unresolved:
            u, v = min(unresolved)
            if not solver.solve(assumptions=[var(u, 0), var(v, 1)]):
                raise RuntimeError(f"forced-equal pair found: {(u, v)}")
            positive = {literal for literal in solver.get_model() if literal > 0}
            word = "".join(
                str(next(colour for colour in range(4)
                         if var(vertex, colour) in positive))
                for vertex in range(n)
            )
            if not all(word[u] != word[v] for u, v in edges):
                raise RuntimeError("solver model failed direct edge check")
            separated = {pair for pair in unresolved if word[pair[0]] != word[pair[1]]}
            if (u, v) not in separated:
                raise RuntimeError("trigger pair was not separated")
            words.append(word)
            unresolved -= separated
    return words


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    for relative, expected in DEPENDENCIES.items():
        if digest(ROOT / relative) != expected:
            raise RuntimeError(f"dependency changed: {relative}")
    h_n, h_edges = heptagon_moser_graph()
    h_words = separating_basis(h_n, h_edges)
    cases, _, _, _, _, _, _ = GOLOMB.construct_cases()
    rows = []
    for index, case in enumerate(cases):
        n, edges = quotient_graph(case)
        rows.append({
            "case": index,
            "vertices": n,
            "edges": len(edges),
            "colourings": separating_basis(n, edges),
        })
    certificate = {
        "schema": "small-exact-support-separating-bases-v1",
        "dependencies": DEPENDENCIES,
        "heptagon_moser": {
            "vertices": h_n,
            "edges": len(h_edges),
            "colourings": h_words,
        },
        "golomb_rotation": {"cases": rows},
    }
    args.output.write_text(json.dumps(certificate, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps({
        "heptagon_moser_vertices": h_n,
        "heptagon_moser_edges": len(h_edges),
        "heptagon_moser_rows": len(h_words),
        "golomb_cases": len(rows),
        "golomb_rows": sum(len(row["colourings"]) for row in rows),
        "maximum_golomb_rows": max(len(row["colourings"]) for row in rows),
        "certificate_sha256": digest(args.output),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
