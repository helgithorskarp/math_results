#!/usr/bin/env python3
"""Solver-free exact verification of the G14/G15 embeddings around Parts-509.

The small distance graphs are reconstructed in Q(sqrt(3)).  Their chromatic
numbers are computed by exhaustive dynamic programming over independent-set
covers.  The embeddings are then checked by comparing every squared distance
with its image in Q(sqrt(3),sqrt(5),sqrt(11)).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from functools import lru_cache
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = ROOT / "hadwiger_nelson_parts509_criticality"
SWAP = ROOT / "hadwiger_nelson_parts509_swap_closure"
sys.path.insert(0, str(SWAP))
import kfield


def load_parts():
    spec = importlib.util.spec_from_file_location("parts509_embedding_base", BASE / "parts509.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def q(value):
    return Fraction(value)


def small_point(row):
    return tuple(q(x) for x in row)


def small_d2(p, r):
    # Elements of Q(sqrt(3)) are pairs (a,b), representing a+b*sqrt(3).
    xa, xb, ya, yb = p
    za, zb, wa, wb = r
    dx = (xa - za, xb - zb)
    dy = (ya - wa, yb - wb)
    return (
        dx[0] * dx[0] + 3 * dx[1] * dx[1] + dy[0] * dy[0] + 3 * dy[1] * dy[1],
        2 * dx[0] * dx[1] + 2 * dy[0] * dy[1],
    )


def graph_from_points(points):
    labels = {(q(1), q(0)): "1", (q(1) / 3, q(0)): "1/3", (q(4), q(0)): "4"}
    edges = []
    counts = {name: 0 for name in labels.values()}
    distances = {}
    for u in range(len(points)):
        for v in range(u + 1, len(points)):
            d2 = small_d2(points[u], points[v])
            distances[(u, v)] = d2
            if d2 in labels:
                name = labels[d2]
                edges.append((u, v))
                counts[name] += 1
    return edges, counts, distances


def exact_graph_invariants(n, edges):
    edge_masks = [0] * n
    for u, v in edges:
        edge_masks[u] |= 1 << v
        edge_masks[v] |= 1 << u
    independent = [True] * (1 << n)
    for mask in range(1, 1 << n):
        bit = mask & -mask
        v = bit.bit_length() - 1
        independent[mask] = independent[mask ^ bit] and not (edge_masks[v] & (mask ^ bit))
    alpha = max(mask.bit_count() for mask, ok in enumerate(independent) if ok)

    @lru_cache(maxsize=None)
    def chromatic(mask):
        if not mask:
            return 0
        first = mask & -mask
        best = mask.bit_count()
        subset = mask
        while subset:
            if subset & first and independent[subset]:
                best = min(best, 1 + chromatic(mask ^ subset))
            subset = (subset - 1) & mask
        return best

    chi = chromatic((1 << n) - 1)
    return chi, alpha


def as_big(point):
    xa, xb, ya, yb = point
    zero = (q(0),) * 8
    x = list(zero); y = list(zero)
    x[0], x[1] = xa, xb
    y[0], y[1] = ya, yb
    return tuple(x), tuple(y)


def resolve_image(record, vpoints, qpoints):
    kind, index = record
    return vpoints[index] if kind == "V" else qpoints[index]


def verify_distance_matrix(parts, canonical, images):
    if len(set(images)) != len(images):
        raise ValueError("embedding repeats an image point")
    for u in range(len(canonical)):
        for v in range(u + 1, len(canonical)):
            d2 = small_d2(canonical[u], canonical[v])
            expected = (d2[0], d2[1]) + (q(0),) * 6
            if parts.squared_distance(images[u], images[v]) != expected:
                raise ValueError(f"distance mismatch for mapped pair {(u, v)}")


def main():
    parts = load_parts()
    cert = json.loads((HERE / "embedding_certificate.json").read_text())
    if cert["format"] != "parts509-g14-g15-embedding-v1":
        raise ValueError("unexpected certificate format")
    if sha256(BASE / "parts509.vtx") != cert["parts_coordinate_sha256"]:
        raise ValueError("Parts coordinate hash mismatch")
    if sha256(SWAP / "completion_points.json") != cert["completion_points_sha256"]:
        raise ValueError("completion-point hash mismatch")

    vpoints = parts.parse_points(BASE / "parts509.vtx")
    completion = json.loads((SWAP / "completion_points.json").read_text())
    qpoints = [(kfield.from_strings(r["x"]), kfield.from_strings(r["y"])) for r in completion["points"]]
    if set(vpoints) & set(qpoints):
        raise ValueError("completion-point list intersects the Parts vertices")

    summaries = {}
    canonical = {}
    for name in ("g14", "g15"):
        obj = cert[name]
        points = [small_point(row) for row in obj["coordinates"]]
        if len(set(points)) != len(points):
            raise ValueError(f"{name} repeats a canonical point")
        edges, counts, _ = graph_from_points(points)
        chi, alpha = exact_graph_invariants(len(points), edges)
        if counts != obj["expected_distance_edge_counts"]:
            raise ValueError(f"{name} edge-count mismatch")
        if chi != obj["expected_chromatic_number"] or alpha != obj["expected_independence_number"]:
            raise ValueError(f"{name} invariant mismatch")
        summaries[name] = {"vertices": len(points), "edges": len(edges), "edge_counts": counts,
                           "chromatic_number": chi, "independence_number": alpha}
        canonical[name] = points

    g15_embeddings = cert["g15"]["parts_embeddings"]
    for mapping in g15_embeddings:
        verify_distance_matrix(parts, canonical["g15"], [vpoints[i] for i in mapping])
    if len(g15_embeddings) != 2 or set(g15_embeddings[0]) != set(g15_embeddings[1]):
        raise ValueError("expected two G15 isometries onto one Parts vertex set")

    used_q = set()
    embedding_summaries = []
    for records in cert["g14"]["embeddings"]:
        images = [resolve_image(r, vpoints, qpoints) for r in records]
        verify_distance_matrix(parts, canonical["g14"], images)
        qids = [index for kind, index in records if kind == "Q3"]
        vids = [index for kind, index in records if kind == "V"]
        if len(qids) != 4 or len(vids) != 10:
            raise ValueError("G14 embedding is not a 10+4 split")
        used_q.update(qids)
        embedding_summaries.append({"parts_vertices": vids, "completion_points": qids})

    # Rescan all eight cited completion points against every Parts vertex.
    neighbor_summary = {}
    for qi in sorted(used_q):
        fresh = [v for v, point in enumerate(vpoints) if parts.squared_distance(qpoints[qi], point) == parts.ONE]
        listed = completion["points"][qi]["neighbors"]
        if fresh != listed or len(fresh) < 3:
            raise ValueError(f"completion-point neighborhood mismatch at Q3 index {qi}")
        neighbor_summary[str(qi)] = fresh

    # Check that each G14 map really extends its corresponding G15 isometry on
    # every canonical point shared by the two carriers.
    g15_lookup = {point: i for i, point in enumerate(canonical["g15"])}
    for emb_index, records in enumerate(cert["g14"]["embeddings"]):
        for point, record in zip(canonical["g14"], records):
            if point in g15_lookup:
                expected = ["V", g15_embeddings[emb_index][g15_lookup[point]]]
                if record != expected:
                    raise ValueError("G14 map does not extend the corresponding G15 isometry")

    print(json.dumps({
        "all_checks": True,
        "small_graphs": summaries,
        "g15_parts_vertices": g15_embeddings[0],
        "g15_forcing": "every proper 5-coloring of the Parts unit graph has a monochromatic pair at distance 1/sqrt(3) or 2 among these 15 vertices",
        "g14_embeddings": embedding_summaries,
        "completion_neighborhoods": neighbor_summary,
        "exact_field": "Q(sqrt(3),sqrt(5),sqrt(11)); rational coefficient comparisons only after parsing"
    }, indent=2))


if __name__ == "__main__":
    main()
