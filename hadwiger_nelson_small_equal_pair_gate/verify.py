#!/usr/bin/env python3
"""Solver-free verifier for exact small-support separating bases."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from collections import Counter
from pathlib import Path


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


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, "missing module loader")
    spec.loader.exec_module(module)
    return module


def heptagon_moser_graph(field):
    h_points, m_points, denominator = field.construction()
    points = sorted({field.add(h, m) for h in h_points for m in m_points})
    target = field.scale(field.ONE, denominator * denominator)
    edges = [
        (u, v)
        for u, v in itertools.combinations(range(len(points)), 2)
        if field.norm(field.sub(points[u], points[v])) == target
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
    require(all(u != v for u, v in edges), "unit pair collapsed")
    return len(roots), edges


def check_basis(n, edges, words):
    require(type(words) is list and words, "empty colouring basis")
    for word in words:
        require(type(word) is str and len(word) == n and set(word) <= set("0123"),
                "malformed colour word")
        require(all(word[u] != word[v] for u, v in edges), "improper colour word")
    signatures = [tuple(word[vertex] for word in words) for vertex in range(n)]
    require(len(set(signatures)) == n, "unseparated vertex pair")
    return n * (n - 1) // 2


def verify(certificate_path=HERE / "certificate.json"):
    for relative, expected in DEPENDENCIES.items():
        require(digest(ROOT / relative) == expected, f"dependency changed: {relative}")
    certificate = json.loads(certificate_path.read_text())
    require(certificate.get("schema") == "small-exact-support-separating-bases-v1",
            "wrong schema")
    require(certificate.get("dependencies") == DEPENDENCIES, "dependency table mismatch")
    field = load("verify_small_equal_pair_heptagon_field",
                 ROOT / "hadwiger_nelson_heptagon_moser_sum" / "field.py")
    golomb = load("verify_small_equal_pair_golomb",
                  ROOT / "hadwiger_nelson_golomb_rotation_sum" / "verify.py")

    h_n, h_edges = heptagon_moser_graph(field)
    h_row = certificate.get("heptagon_moser")
    require(type(h_row) is dict and h_row.get("vertices") == h_n
            and h_row.get("edges") == len(h_edges), "heptagon-Moser metadata mismatch")
    h_pairs = check_basis(h_n, h_edges, h_row.get("colourings"))

    cases, _, events, _, _, _, _ = golomb.construct_cases()
    rows = certificate.get("golomb_rotation", {}).get("cases")
    require(type(rows) is list and len(rows) == len(cases) == 205, "wrong case count")
    total_rows = 0
    total_pairs = 0
    histogram = Counter()
    for index, (case, row) in enumerate(zip(cases, rows)):
        n, edges = quotient_graph(case)
        require(type(row) is dict and row.get("case") == index
                and row.get("vertices") == n and row.get("edges") == len(edges),
                "Golomb case metadata mismatch")
        words = row.get("colourings")
        total_pairs += check_basis(n, edges, words)
        total_rows += len(words)
        histogram[(n, len(edges))] += 1
    return {
        "verified": True,
        "theorem": "every distinct physical pair is separated by a proper four-colouring",
        "heptagon_moser": {
            "vertices": h_n,
            "edges": len(h_edges),
            "colouring_rows": len(h_row["colourings"]),
            "pairs_separated": h_pairs,
        },
        "golomb_rotation": {
            "event_factors": len(events),
            "cases": len(cases),
            "colouring_rows": total_rows,
            "maximum_rows_per_case": max(len(row["colourings"]) for row in rows),
            "pairs_separated": total_pairs,
            "quotient_histogram": [
                {"vertices": n, "edges": edges, "cases": count}
                for (n, edges), count in sorted(histogram.items())
            ],
        },
        "forced_equal_pairs": 0,
        "certificate_sha256": digest(certificate_path),
    }


def main():
    print(json.dumps(verify(), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
