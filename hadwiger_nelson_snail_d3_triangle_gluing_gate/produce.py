#!/usr/bin/env python3
"""Exact selector for a fixed Snail-D3 triangle-gluing cohort.

The fixed side is case (centre,axis)=(9,3), selected before the cohort because
its archived non-three-colour witness has the largest order (113).  Its first
embedded seed triangle is fixed.  The second side ranges over all 655 archived
four-chromatic D3 cases; its first embedded seed triangle is mapped onto the
fixed triangle by all six bijections.  Coordinates, collisions and cross unit
contacts are exact in the Snail degree-16 field.  SAT verdicts are selectors;
decoded four-colour words are checked directly.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import itertools
import json
import sys
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "hadwiger_nelson_snail_dihedral"
sys.path.insert(0, str(SRC))

import geometry as g  # type: ignore  # noqa: E402
from pysat.solvers import Cadical195  # type: ignore  # noqa: E402

F = Fraction
FIXED_CASE = (9, 3)


def div_scalar(x, q):
    return tuple(F(a) / q for a in x)


def inverse(x):
    """Inverse in the fixed degree-16 algebra by exact Gaussian elimination."""
    cols = [g.mul(x, g.basis(j)) for j in range(g.SIZE)]
    a = [[F(cols[j][i]) for j in range(g.SIZE)] + [F(i == 0)] for i in range(g.SIZE)]
    for col in range(g.SIZE):
        pivot = next((r for r in range(col, g.SIZE) if a[r][col]), None)
        if pivot is None:
            raise ZeroDivisionError("noninvertible field element")
        a[col], a[pivot] = a[pivot], a[col]
        q = a[col][col]
        a[col] = [v / q for v in a[col]]
        for r in range(g.SIZE):
            if r == col or not a[r][col]:
                continue
            q = a[r][col]
            a[r] = [u - q * v for u, v in zip(a[r], a[col])]
    y = tuple(row[-1] for row in a)
    if g.mul(x, y) != tuple(F(i == 0) for i in range(g.SIZE)):
        raise RuntimeError("bad inverse")
    return y


def normalize(points, triangle):
    p0, p1, _ = (points[i] for i in triangle)
    delta = g.sub(p1, p0)
    inv_delta = inverse(delta)
    return [g.mul(g.sub(p, p0), inv_delta) for p in points]


def canonical_triangle(graph, seed_triangle):
    ids = graph["address_ids"]
    tri = tuple(ids[i] for i in seed_triangle)  # first direct embedded seed
    if len(set(tri)) != 3:
        raise RuntimeError("canonical seed triangle collided")
    edge_set = {tuple(sorted(e)) for e in graph["edges"]}
    if any(tuple(sorted(e)) not in edge_set for e in itertools.combinations(tri, 2)):
        raise RuntimeError("canonical seed triangle lost an edge")
    return tri


def conjugate_point(z):
    return tuple(F(x) for x in g.conjugate(z))


def mod_value(z, prime=g.PRIME):
    out = 0
    for q, r in zip(z, g.RESIDUES):
        q = F(q)
        out = (out + q.numerator * pow(q.denominator, -1, prime) * r) % prime
    return out


def is_unit(z):
    return g.norm(z) == tuple(F(i == 0) for i in range(g.SIZE))


def colour(n, edges):
    clauses = [[4 * v + c + 1 for c in range(4)] for v in range(n)]
    clauses += [
        [-(4 * v + a + 1), -(4 * v + b + 1)]
        for v in range(n)
        for a in range(4)
        for b in range(a + 1, 4)
    ]
    clauses += [
        [-(4 * u + c + 1), -(4 * v + c + 1)]
        for u, v in edges
        for c in range(4)
    ]
    with Cadical195(bootstrap_with=clauses) as solver:
        if not solver.solve():
            return None, solver.accum_stats()
        pos = {x for x in solver.get_model() if x > 0}
        word = [next(c for c in range(4) if 4 * v + c + 1 in pos) for v in range(n)]
        stats = solver.accum_stats()
    if any(word[u] == word[v] for u, v in edges):
        raise RuntimeError("bad solver word")
    return word, stats


def pack(word):
    data = bytearray((len(word) + 3) // 4)
    for i, colour_value in enumerate(word):
        data[i // 4] |= colour_value << (2 * (i % 4))
    return base64.b64encode(data).decode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()
    archive = json.loads((SRC / "certificate.json").read_text())
    seed = g.seed()
    seed_triangle = tuple(archive["seed_triangle"])
    rows = {(r[0], r[1]): r for r in archive["cases"]}
    fixed_row = rows[FIXED_CASE]
    if fixed_row[3] != 4 or len(fixed_row[4]) != 113:
        raise RuntimeError("fixed source selection changed")
    base_graph = g.case(seed, *FIXED_CASE)
    base_tri = canonical_triangle(base_graph, seed_triangle)
    base_points = normalize(base_graph["points"], base_tri)
    base_ids = {p: i for i, p in enumerate(base_points)}
    if len(base_ids) != len(base_points):
        raise RuntimeError("normalized base collision")
    base_edges = {tuple(sorted(e)) for e in base_graph["edges"]}
    qbase = base_points[base_tri[2]]

    start = time.monotonic()
    cases = placements = sat_cases = 0
    max_cross = 0
    best = None
    order_hist = Counter()
    cross_hist = Counter()
    collision_hist = Counter()
    conflict_max = 0
    certificate_rows = []

    for row in archive["cases"]:
        centre, axis, _, chi, _ = row
        if chi != 4:
            continue
        graph = g.case(seed, centre, axis)
        tri0 = canonical_triangle(graph, seed_triangle)
        cases += 1
        for perm_indices in itertools.permutations(range(3)):
            perm = tuple(tri0[i] for i in perm_indices)
            normalized = normalize(graph["points"], perm)
            q = normalized[perm[2]]
            if q == qbase:
                moved = normalized
                chirality = "direct"
            elif conjugate_point(q) == qbase:
                moved = [conjugate_point(z) for z in normalized]
                chirality = "reflected"
            else:
                raise RuntimeError("equilateral triangle mismatch")

            union = list(base_points)
            point_id = dict(base_ids)
            moved_ids = []
            collisions = 0
            for z in moved:
                if z in point_id:
                    collisions += 1
                else:
                    point_id[z] = len(union)
                    union.append(z)
                moved_ids.append(point_id[z])
            if len({moved_ids[i] for i in perm}) != 3:
                raise RuntimeError("mapped triangle collision")
            if tuple(moved_ids[i] for i in perm) != base_tri:
                raise RuntimeError("triangle bijection failed")

            edges = set(base_edges)
            for u, v in graph["edges"]:
                a, b = moved_ids[u], moved_ids[v]
                if a != b:
                    edges.add(tuple(sorted((a, b))))

            # Every possible new edge has one endpoint in the base and one in
            # the moved support.  Exact coincidences were merged first.
            base_set = set(range(len(base_points)))
            moved_set = set(moved_ids)
            cross_added = 0
            residues = [mod_value(z) for z in union]
            bars = [mod_value(conjugate_point(z)) for z in union]
            for u in base_set:
                for v in moved_set:
                    if u >= v or (u, v) in edges:
                        continue
                    if (residues[u] - residues[v]) * (bars[u] - bars[v]) % g.PRIME != 1:
                        continue
                    if is_unit(g.sub(union[u], union[v])):
                        edges.add((u, v))
                        cross_added += 1

            word, stats = colour(len(union), sorted(edges))
            placements += 1
            conflict_max = max(conflict_max, stats.get("conflicts", 0))
            if word is None:
                print(
                    json.dumps(
                        {
                            "status": "NONFOUR_SIGNAL_REQUIRES_CERTIFICATE",
                            "fixed_case": list(FIXED_CASE),
                            "second_case": [centre, axis],
                            "permuted_second_triangle": list(perm),
                            "chirality": chirality,
                            "vertices": len(union),
                            "edges": len(edges),
                            "collisions": collisions,
                            "new_cross_edges": cross_added,
                            "placements_before_signal": placements,
                            "elapsed_seconds": time.monotonic() - start,
                        },
                        indent=2,
                        sort_keys=True,
                    )
                )
                return
            sat_cases += 1
            formal_word = [word[i] for i in base_graph["address_ids"]]
            formal_word += [word[moved_ids[i]] for i in graph["address_ids"]]
            certificate_rows.append(
                [centre, axis, list(perm_indices), pack(formal_word),
                 len(union), len(edges), collisions, cross_added]
            )
            order_hist[len(union)] += 1
            cross_hist[cross_added] += 1
            collision_hist[collisions] += 1
            score = (cross_added, collisions, len(edges), -len(union))
            if best is None or score > best[0]:
                best = (
                    score,
                    {
                        "second_case": [centre, axis],
                        "permuted_second_triangle": list(perm),
                        "chirality": chirality,
                        "vertices": len(union),
                        "edges": len(edges),
                        "collisions": collisions,
                        "new_cross_edges": cross_added,
                        "proper_four_colouring": word,
                    },
                )
                max_cross = cross_added

        if cases % 100 == 0:
            print(json.dumps({"cases": cases, "placements": placements, "best_cross": max_cross,
                              "elapsed": time.monotonic() - start}), file=sys.stderr, flush=True)

    result = {
        "status": "ALL_PLACEMENTS_FOUR_COLOURABLE",
        "fixed_case": list(FIXED_CASE),
        "fixed_order": len(base_points),
        "fixed_edges": len(base_edges),
        "fixed_archived_nonthree_core_order": len(fixed_row[4]),
        "second_cases": cases,
        "placements": placements,
        "sat_cases": sat_cases,
        "orders": dict(sorted(order_hist.items())),
        "collisions": dict(sorted(collision_hist.items())),
        "new_cross_edges": dict(sorted(cross_hist.items())),
        "max_solver_conflicts": conflict_max,
        "best_placement": best[1] if best else None,
        "elapsed_seconds": time.monotonic() - start,
    }
    if args.certificate is not None:
        dependency_names = ["seed.json", "certificate.json", "geometry.py"]
        dependencies = {
            name: hashlib.sha256((SRC / name).read_bytes()).hexdigest()
            for name in dependency_names
        }
        certificate_summary = dict(result)
        certificate_summary.pop("elapsed_seconds", None)
        payload = {
            "version": 1,
            "family": "fixed Snail-D3 canonical-triangle gluing",
            "fixed_case": list(FIXED_CASE),
            "second_case_order": [
                [r[0], r[1]] for r in archive["cases"] if r[3] == 4
            ],
            "permutation_order": [list(p) for p in itertools.permutations(range(3))],
            "address_order": "174 fixed formal addresses then 174 moved formal addresses",
            "dependencies": dependencies,
            "rows": certificate_rows,
            "summary": certificate_summary,
        }
        args.certificate.write_text(json.dumps(payload, separators=(",", ":"), sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
