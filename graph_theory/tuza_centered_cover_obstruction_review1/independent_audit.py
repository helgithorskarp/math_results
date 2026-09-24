#!/usr/bin/env python3
"""Independent exact audit of the centered-cover obstruction.

This script does not import the author's checker.  It exhausts every edge
subset and every triangle subset of the nine-vertex gadget, verifies the two
fractional certificates from definitions, and constructs AG(d,4) directly
from polynomial arithmetic for d=1,2,3,4.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json
import math


NEIGHBORHOODS = (
    (0, 1, 2),
    (0, 1, 3),
    (0, 3),
    (1, 2, 3),
    (2, 3),
)


def edge(u, v):
    return frozenset((u, v))


def triangle_edges(triangle):
    return tuple(edge(u, v) for u, v in combinations(triangle, 2))


def build_gadget():
    vertices = tuple(range(9))
    clique = set(range(4))
    edges = {edge(u, v) for u, v in combinations(clique, 2)}
    for center, neighborhood in enumerate(NEIGHBORHOODS, start=4):
        edges.update(edge(center, v) for v in neighborhood)
    triangles = tuple(
        t for t in combinations(vertices, 3)
        if all(e in edges for e in triangle_edges(t))
    )
    centered = tuple(t for t in triangles if len(set(t) - clique) == 1)
    return vertices, clique, edges, triangles, centered


def minimum_cover(edges, triangle_masks):
    ordered_edges = tuple(sorted(edges, key=lambda e: tuple(sorted(e))))
    edge_id = {e: i for i, e in enumerate(ordered_edges)}
    encoded = tuple(
        sum(1 << edge_id[e] for e in triangle_edges(t)) for t in triangle_masks
    )
    optimum = len(edges) + 1
    optimum_count = 0
    # This deliberately checks all 2^19 edge subsets, rather than sharing the
    # author's increasing-combination enumeration.
    for mask in range(1 << len(edges)):
        size = mask.bit_count()
        if size > optimum:
            continue
        if all(mask & tri for tri in encoded):
            if size < optimum:
                optimum = size
                optimum_count = 1
            else:
                optimum_count += 1
    return optimum, optimum_count


def maximum_packing(edges, triangles):
    ordered_edges = tuple(sorted(edges, key=lambda e: tuple(sorted(e))))
    edge_id = {e: i for i, e in enumerate(ordered_edges)}
    encoded = tuple(
        sum(1 << edge_id[e] for e in triangle_edges(t)) for t in triangles
    )
    optimum = -1
    optimum_count = 0
    # The gadget has only 15 triangles, so definition-level subset exhaustion
    # is clearer than an optimization package.
    for chosen in range(1 << len(encoded)):
        size = chosen.bit_count()
        if size < optimum:
            continue
        used = 0
        valid = True
        for i, tri in enumerate(encoded):
            if (chosen >> i) & 1:
                if used & tri:
                    valid = False
                    break
                used |= tri
        if valid:
            if size > optimum:
                optimum = size
                optimum_count = 1
            else:
                optimum_count += 1
    return optimum, optimum_count


def check_fractional_certificates(edges, centered):
    primal_load = Counter()
    for triangle in centered:
        for e in triangle_edges(triangle):
            primal_load[e] += Fraction(1, 2)
    assert max(primal_load.values()) <= 1
    primal_value = sum((Fraction(1, 2) for _ in centered), Fraction())

    dual = {
        edge(0, 3): Fraction(1),
        edge(2, 3): Fraction(1),
        edge(4, 0): Fraction(1, 2),
        edge(4, 1): Fraction(1, 2),
        edge(4, 2): Fraction(1, 2),
        edge(5, 1): Fraction(1),
        edge(7, 1): Fraction(1),
    }
    assert set(dual) <= edges
    dual_slacks = []
    for triangle in centered:
        weight = sum((dual.get(e, Fraction()) for e in triangle_edges(triangle)),
                     Fraction())
        assert weight >= 1
        dual_slacks.append(weight - 1)
    dual_value = sum(dual.values(), Fraction())
    assert primal_value == dual_value == Fraction(11, 2)
    return primal_value, max(primal_load.values()), max(dual_slacks)


def gf4_mul(a, b):
    """Multiply binary polynomials modulo x^2+x+1, without a table."""
    c0 = (a & 1) & (b & 1)
    c1 = ((a & 1) & ((b >> 1) & 1)) ^ (((a >> 1) & 1) & (b & 1))
    c2 = ((a >> 1) & 1) & ((b >> 1) & 1)
    # x^2 = x+1 in the quotient field.
    return (c0 ^ c2) | ((c1 ^ c2) << 1)


def point_add(x, y):
    return tuple(a ^ b for a, b in zip(x, y))


def scalar_mul(a, x):
    return tuple(gf4_mul(a, coordinate) for coordinate in x)


def affine_lines(dimension):
    points = tuple(product(range(4), repeat=dimension))
    zero = (0,) * dimension
    lines = {
        frozenset(point_add(origin, scalar_mul(a, direction)) for a in range(4))
        for origin in points
        for direction in points
        if direction != zero
    }
    assert all(len(line) == 4 for line in lines)
    return points, lines


def audit_affine_family(dimension):
    points, lines = affine_lines(dimension)
    k = len(points)
    pair_counts = Counter(
        edge(u, v) for line in lines for u, v in combinations(line, 2)
    )
    all_pairs = {edge(u, v) for u, v in combinations(points, 2)}
    assert set(pair_counts) == all_pairs
    assert set(pair_counts.values()) == {1}

    ordered_lines = sorted(tuple(sorted(line)) for line in lines)
    graph_edges = set()
    neighborhood_types = set()
    for block_id, line in enumerate(ordered_lines):
        local_edges = {edge(("p", u), ("p", v)) for u, v in combinations(line, 2)}
        for type_id, pattern in enumerate(NEIGHBORHOODS):
            center = ("c", block_id, type_id)
            neighborhood = frozenset(line[i] for i in pattern)
            assert neighborhood not in neighborhood_types
            neighborhood_types.add(neighborhood)
            local_edges.update(edge(center, ("p", line[i])) for i in pattern)
        assert graph_edges.isdisjoint(local_edges)
        graph_edges.update(local_edges)

    q = k * (k - 1) // 2
    blocks = len(lines)
    assert 6 * blocks == q
    assert len(graph_edges) == 19 * blocks
    assert len(neighborhood_types) == 5 * blocks
    spokes = sum(len(n) for n in NEIGHBORHOODS) * blocks
    assert spokes == 13 * blocks

    h = Fraction(11 * blocks, 2)
    tau = q
    phi = (Fraction(k * k, 4) - Fraction(k, 2) + h
           - h * h / (k * k) + Fraction(1, 4))
    gap = tau - phi
    expected_gap = Fraction((k - 1) ** 2, 576) + Fraction(k - 1, 24)
    assert gap == expected_gap
    if dimension >= 2:
        assert tau > math.ceil(phi)

    return {
        "dimension": dimension,
        "clique_order": k,
        "blocks": blocks,
        "pairs": len(pair_counts),
        "pair_multiplicities": sorted(set(pair_counts.values())),
        "graph_edges": len(graph_edges),
        "spokes": spokes,
        "neighborhood_types": len(neighborhood_types),
        "centered_fractional_optimum": str(h),
        "triangle_cover": tau,
        "phi": str(phi),
        "gap": str(gap),
        "ceiling_phi": math.ceil(phi),
    }


def main():
    vertices, clique, edges, triangles, centered = build_gadget()
    assert len(vertices) == 9 and len(clique) == 4 and len(edges) == 19
    assert len(triangles) == 15 and len(centered) == 11

    fractional, maximum_edge_load, maximum_dual_slack = (
        check_fractional_certificates(edges, centered)
    )
    cover, cover_count = minimum_cover(edges, triangles)
    packing, packing_count = maximum_packing(edges, triangles)
    centered_packing, centered_packing_count = maximum_packing(edges, centered)
    assert (cover, packing, centered_packing) == (6, 5, 5)

    stated_packing = (
        (4, 0, 2), (5, 0, 1), (6, 0, 3), (7, 1, 2), (8, 2, 3)
    )
    used = set()
    for triangle in stated_packing:
        assert triangle in centered or tuple(sorted(triangle)) in centered
        tri_edges = set(triangle_edges(triangle))
        assert used.isdisjoint(tri_edges)
        used.update(tri_edges)

    output = {
        "status": "independent exact audit passed",
        "gadget": {
            "vertices": len(vertices),
            "edges": len(edges),
            "triangles": len(triangles),
            "centered_triangles": len(centered),
            "fractional_optimum_certificate": str(fractional),
            "maximum_primal_edge_load": str(maximum_edge_load),
            "maximum_dual_slack": str(maximum_dual_slack),
            "minimum_full_triangle_cover": cover,
            "optimal_full_cover_count": cover_count,
            "maximum_full_triangle_packing": packing,
            "optimal_full_packing_count": packing_count,
            "maximum_centered_triangle_packing": centered_packing,
            "optimal_centered_packing_count": centered_packing_count,
        },
        "affine_families": [audit_affine_family(d) for d in range(1, 5)],
        "scope": {
            "unbounded_type_count": True,
            "fixed_type_statement_tested": False,
            "tuza_counterexample_claimed": False,
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
