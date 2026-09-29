#!/usr/bin/env python3
"""Exact contact-cone coverage of every fixed projection orientation.

Python 3.11+, standard library only, no external data or solver.
The sixteen small contact tetrahedra were discovered heuristically. This
checker reconstructs their complete coverage and all inequalities exactly.
The quantified theorem and the analytic bridges are in orientation_proof.md.
"""

from itertools import product
import json
import argparse
from copy import deepcopy

from verify import (Q5, PHI, ZERO, vec, vertices, cyclic_signed, dot, cross,
                    sub, add, mul, shadow, self_check)
from local_certificate import BASES, solve_independent_columns


# (cell, fan triangle, cofactor sign, four contacts)
# A contact (a,b,v) uses the outward normal (V[b]-V[a]) cross u,
# supported at V[v]. Vertex order is the exact sorted order in verify.py.
CERTIFICATES = [
    (0, 0, -1, [(61, 58, 58), (34, 17, 34), (17, 4, 4), (4, 0, 4)]),
    (1, 0, 1, [(57, 61, 57), (58, 45, 45), (36, 20, 36), (17, 4, 4)]),
    (1, 1, -1, [(45, 42, 45), (20, 17, 20), (17, 4, 4), (17, 4, 17)]),
    (2, 0, 1, [(61, 58, 58), (45, 34, 34), (45, 34, 45), (36, 20, 20)]),
    (3, 0, 1, [(57, 61, 57), (59, 55, 55), (42, 36, 42), (17, 4, 4)]),
    (4, 0, -1, [(59, 55, 55), (36, 20, 36), (17, 4, 4), (17, 4, 17)]),
    (4, 1, 1, [(57, 61, 57), (57, 61, 61), (59, 55, 55), (58, 45, 58)]),
    (5, 0, -1, [(43, 57, 43), (57, 61, 57), (61, 58, 58), (58, 45, 45)]),
    (6, 0, -1, [(43, 57, 43), (57, 61, 57), (57, 61, 61), (59, 55, 55)]),
    (6, 1, -1, [(43, 57, 43), (57, 61, 57), (57, 61, 61), (59, 55, 55)]),
    (7, 0, -1, [(43, 57, 43), (57, 61, 57), (57, 61, 61), (45, 34, 34)]),
    (8, 0, 1, [(43, 57, 57), (57, 53, 53), (55, 58, 55), (58, 45, 58)]),
    (8, 1, 1, [(41, 43, 43), (43, 57, 57), (57, 53, 57), (53, 59, 53)]),
    (9, 0, -1, [(59, 55, 55), (58, 45, 58), (45, 34, 34), (45, 34, 45)]),
    (10, 0, 1, [(43, 57, 57), (57, 53, 53), (55, 51, 55), (42, 36, 42)]),
    (11, 0, 1, [(43, 49, 43), (43, 49, 49), (53, 59, 59), (55, 51, 51)]),
]


EXPONENTS = sorted(set(tuple(t.count(j) for j in range(3))
                       for t in product(range(3), repeat=3)))
MONOMIALS = {e: [t for t in product(range(3), repeat=3)
                 if tuple(t.count(j) for j in range(3)) == e]
             for e in EXPONENTS}
CORNER = vec((0, 0, 1))
CHAMBER = [CORNER, vec((1 / PHI, 0, 1)), vec((0, 1 / PHI**2, 1))]


def area_twice(poly):
    return sum((poly[i][0] * poly[(i + 1) % len(poly)][1]
                - poly[i][1] * poly[(i + 1) % len(poly)][0]
                for i in range(len(poly))), ZERO)


def clip(poly, n, side):
    """Exact half-plane clipping of a counterclockwise convex polygon."""
    out = []
    for i, a in enumerate(poly):
        b = poly[(i + 1) % len(poly)]
        fa, fb = side * dot(n, a), side * dot(n, b)
        if fa.sign() >= 0:
            out.append(a)
        if fa.sign() * fb.sign() < 0:
            out.append(add(a, mul(fa / (fa - fb), sub(b, a))))
    compact = []
    for a in out:
        if not compact or a != compact[-1]:
            compact.append(a)
    if len(compact) > 1 and compact[0] == compact[-1]:
        compact.pop()
    assert len(compact) >= 3 and area_twice(compact).sign() > 0
    assert all(side * dot(n, v) >= ZERO for v in compact)
    return compact


def canonical_plane(n):
    t = next(x for x in n if x != ZERO)
    return mul(1 / t, n)


def build_cells():
    # These 60 directions are vertices of the dual rhombicosidodecahedron.
    # Their status as facet normals of K is unnecessary for coverage: every
    # listed plane merely splits the chamber into two closed half-planes.
    normals = set().union(*(cyclic_signed(vec(t)) for t in [
        (1, 1, PHI**3), (PHI, 2 * PHI, PHI**2),
        (0, PHI**2, 2 + PHI)]))
    assert len(normals) == 60
    planes = sorted(set(canonical_plane(n) for n in normals))
    assert len(planes) == 30
    polygons = [CHAMBER]
    for n in planes:
        new = []
        for p in polygons:
            signs = {dot(n, v).sign() for v in p}
            if -1 in signs and 1 in signs:
                q, r = clip(p, n, -1), clip(p, n, 1)
                assert area_twice(q) + area_twice(r) == area_twice(p)
                new.extend((q, r))
            else:
                new.append(p)
        polygons = new
    assert sum((area_twice(p) for p in polygons), ZERO) == area_twice(CHAMBER)
    assert len(polygons) == 12
    triangles = {}
    for cell, p in enumerate(polygons):
        assert area_twice(p).sign() > 0
        fans = [[p[0], p[j], p[j + 1]] for j in range(1, len(p) - 1)]
        assert all(area_twice(t).sign() > 0 for t in fans)
        assert sum((area_twice(t) for t in fans), ZERO) == area_twice(p)
        for j, t in enumerate(fans):
            triangles[cell, j] = t
    assert len(triangles) == 16
    return polygons, triangles


def check_reflections(V):
    walls = [vec((1, 0, 0)), vec((0, 1, 0)), vec((-PHI, -PHI**2, 1))]
    for n in walls:
        assert dot(n, n).sign() > 0
        reflected = {sub(v, mul(2 * dot(v, n) / dot(n, n), n)) for v in V}
        assert reflected == set(V)
    return len(walls)


def row_at(V, contact, u):
    a, b, j = contact
    assert 0 <= a < len(V) and 0 <= b < len(V) and 0 <= j < len(V)
    assert a != b
    n = cross(sub(V[b], V[a]), u)
    support = dot(n, V[j])
    assert support.sign() > 0
    assert dot(n, V[a]) == support and dot(n, V[b]) == support
    assert all((support - dot(n, w)).sign() >= 0 for w in V)
    return cross(V[j], n)


def determinant(a, b, c):
    return dot(a, cross(b, c))


def cofactor_coefficients(G, sign):
    """Ten monomial coefficients of each of four homogeneous cubic minors."""
    out = []
    for omitted in range(4):
        inds = [j for j in range(4) if j != omitted]
        row = []
        for e in EXPONENTS:
            value = sum((determinant(G[inds[0]][a], G[inds[1]][b], G[inds[2]][c])
                         for a, b, c in MONOMIALS[e]), ZERO)
            row.append(sign * (-1 if omitted % 2 else 1) * value)
        assert all(x.sign() >= 0 for x in row)
        assert any(x.sign() > 0 for x in row)
        # Every open edge of the triangle also gives four strictly positive
        # minors. Thus diagonal edges and chamber boundaries are included.
        for missing in range(3):
            assert any(x.sign() > 0 and e[missing] == 0
                       for x, e in zip(row, EXPONENTS))
        out.append(row)
    return out


def check_twofold(V):
    # Recheck the exceptional corner using the previous exact certificate.
    H = shadow(V, CORNER)
    rows = []
    for n, b in H['constraints']:
        for v in V:
            if dot(n, v) == b:
                rows.append(mul(1 / b, cross(v, n)))
    for coordinate, sign, indices in BASES[2]:
        rhs = vec([sign if j == coordinate else 0 for j in range(3)])
        weights = solve_independent_columns([rows[i] for i in indices], rhs)
        assert all(w.sign() > 0 for w in weights)
        assert sum(weights, ZERO) < Q5(7)
    return len(rows)


def verify_orientation(certificates=CERTIFICATES):
    self_check()
    V = vertices()
    assert len(V) == 62 and set(V) == {mul(-1, v) for v in V}
    reflection_count = check_reflections(V)
    polygons, triangles = build_cells()
    assert [(c, j) for c, j, _, _ in certificates] == list(triangles)
    covered_vertices = {}
    coefficient_count = positive_count = comparisons = 0
    rows_summary = []
    for cell, fan, sign, contacts in certificates:
        assert sign in (-1, 1) and len(contacts) == 4
        assert len(set(contacts)) == 4
        t = triangles[cell, fan]
        G = [[row_at(V, contact, u) for u in t] for contact in contacts]
        comparisons += 4 * 3 * len(V)
        coeffs = cofactor_coefficients(G, sign)
        coefficient_count += 40
        positive = sum(x.sign() > 0 for row in coeffs for x in row)
        positive_count += positive
        good = []
        for j, u in enumerate(t):
            e = tuple(3 if k == j else 0 for k in range(3))
            ok = all(row[EXPONENTS.index(e)].sign() > 0 for row in coeffs)
            covered_vertices[u] = covered_vertices.get(u, False) or ok
            good.append(ok)
        rows_summary.append({'cell': cell, 'triangle': fan,
                             'strictly_positive_coefficients': positive,
                             'vertices_with_four_positive_minors': good})
    assert coefficient_count == 640
    assert len(covered_vertices) == 14
    assert {u for u, ok in covered_vertices.items() if not ok} == {CORNER}
    corner_contacts = check_twofold(V)
    return {
        'agent': 'six-rupert-1', 'role': 'researcher',
        'arithmetic': 'exact Q(sqrt(5)); no floating-point decisions',
        'claim': 'every fixed outer orientation excludes all sufficiently small nonzero relative rotations',
        'quantifiers': 'for every u there exists epsilon(u)>0; no uniform epsilon is asserted',
        'global_Rupert_property': 'unresolved',
        'verified_chamber_wall_reflections': reflection_count,
        'splitting_planes': 30, 'direction_cells': len(polygons),
        'cell_polygon_sizes': [len(p) for p in polygons],
        'triangles': len(triangles), 'distinct_chamber_vertices': len(covered_vertices),
        'support_comparisons_at_triangle_vertices': comparisons,
        'nonnegative_cubic_coefficients': coefficient_count,
        'strictly_positive_cubic_coefficients': positive_count,
        'twofold_corner_contact_gradients': corner_contacts,
        'certificates': rows_summary,
    }


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('verification requires assertions; do not use python -O')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    result = verify_orientation()
    if args.self_test:
        reversed_probe = deepcopy(CERTIFICATES)
        a, b, j = reversed_probe[0][3][0]
        reversed_probe[0][3][0] = (b, a, j)
        reversed_sign = deepcopy(CERTIFICATES)
        c, j, sign, probes = reversed_sign[0]
        reversed_sign[0] = (c, j, -sign, probes)
        repeated_probe = deepcopy(CERTIFICATES)
        repeated_probe[0][3][1] = repeated_probe[0][3][0]
        cases = [('missing triangle', CERTIFICATES[1:]),
                 ('reversed support normal', reversed_probe),
                 ('reversed cofactor sign', reversed_sign),
                 ('repeated contact', repeated_probe)]
        rejected = []
        for name, bad in cases:
            try:
                verify_orientation(bad)
            except AssertionError:
                rejected.append(name)
            else:
                raise RuntimeError('malformed certificate accepted: ' + name)
        result['rejected_certificate_mutations'] = rejected
    print(json.dumps(result, indent=2, sort_keys=True))
