#!/usr/bin/env python3
"""Exact thirty-gon and contact audit; Python 3.11+ standard library.

This checks the finite premises of PROOF.md. The compactness and
linearization arguments are written mathematics, not a numeric radius.
The preceding minimum-diameter theorem is a stated proof dependency.
"""
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'pentagonal_minimum_diameter'
BASE_HASH = '12c94ea3ab9d7bc42e2086dbb5fbb9154306d6fd7095a8be4b25bb44fefd5339'
if hashlib.sha256((BASE / 'verify.py').read_bytes()).hexdigest() != BASE_HASH:
    raise ValueError('minimum-diameter arithmetic/model dependency changed')
sys.path.insert(0, str(BASE))
from verify import (Z, ONE, PHI, H, N, BOX, G, TY,
                    require, qi, dot, mv, mm, group, vertices,
                    lf, ladd, lscale, lmv, ldot, linterval,
                    poly_square, poly_add, poly_interval)


def sub(a, b):
    return tuple(ladd(x, lscale(-ONE, y)) for x, y in zip(a, b))


def linear_cross(a, b):
    """Cross a linear-form vector with a constant Q(phi) vector."""
    return (ladd(lscale(b[2], a[1]), lscale(-b[1], a[2])),
            ladd(lscale(b[0], a[2]), lscale(-b[2], a[0])),
            ladd(lscale(b[1], a[0]), lscale(-b[0], a[1])))


def multiply(a, b):
    """Product of two linear forms, retaining exact cancellations."""
    out = {}
    for i, c in enumerate(a):
        for j, d in enumerate(b):
            e = tuple(sorted((i, j)))
            out[e] = out.get(e, Z)+c*d
    return {e: c for e, c in out.items() if c != Z}


def quadratic_dot(a, b):
    out = {}
    for x, y in zip(a, b):
        out = poly_add(out, multiply(x, y))
    return out


def projected_length_squared(d):
    out = {}
    for x in d:
        out = poly_add(out, poly_square(x))
    return poly_add(out, poly_square(ldot(N, d)), -ONE/H)


def audit_polygon(vs, data):
    require(set(data) == {'axis', 'counterclockwise_vertex_indices',
                          'base_short_edge'}, 'unexpected polygon fields')
    require(data['axis'] == ['1', '0', 'phi'], 'wrong receiving axis')
    ix = data['counterclockwise_vertex_indices']
    require(isinstance(ix, list) and len(ix) == 30
            and all(type(i) is int and 0 <= i < len(vs) for i in ix)
            and len(set(ix)) == 30, 'bad polygon indices')
    require(data['base_short_edge'] == [33, 27], 'wrong base short edge')
    v = (lf(2, -ONE), lf(0, -ONE), lf(1, -ONE))
    w = (lf(2), lf(0, -ONE), lf(1))
    require(vs[33] == v and vs[27] == w, 'short-edge coordinates changed')
    shortest = projected_length_squared(sub(w, v))
    alpha = ladd(lscale(PHI, lf(2)), lf(1, -ONE))
    require(shortest == {e: 4*c/H for e, c in poly_square(alpha).items()},
            'short-edge length formula')
    require(linterval(alpha, BOX).lo > 0, 'short edge has collapsed')
    supports, gap, length_gap, turns, short = 0, [], [], [], []
    for k, i in enumerate(ix):
        j = ix[(k+1) % len(ix)]
        e = sub(vs[j], vs[i])
        normal = linear_cross(e, N)
        require(ldot(N, normal) == lf(0, Z), 'normal not in shadow plane')
        bound = quadratic_dot(normal, vs[i])
        require(poly_interval(bound, BOX).lo > 0,
                'supporting line does not bound the origin')
        for z, p in enumerate(vs):
            distance = quadratic_dot(normal, sub(vs[i], p))
            if z in (i, j):
                require(not distance, 'edge endpoint not exactly supported')
            else:
                b = poly_interval(distance, BOX)
                require(b.lo > 0, f'edge {i},{j} misses vertex {z}')
                gap.append(b.lo)
            supports += 1
        # (previous edge cross current edge) dot N > 0 is equivalent
        # to current edge dot (previous edge cross N) < 0.
        prev = sub(vs[i], vs[ix[(k-1) % len(ix)]])
        turn = {exponent: -c for exponent, c in
                quadratic_dot(e, linear_cross(prev, N)).items()}
        b = poly_interval(turn, BOX)
        require(b.lo > 0, 'polygon is not strictly counterclockwise convex')
        turns.append(b.lo)
        difference = poly_add(projected_length_squared(e), shortest, -ONE)
        if not difference:
            short.append((i, j))
        else:
            b = poly_interval(difference, BOX)
            require(b.lo > 0, 'base edge is not uniquely shortest by orbit')
            length_gap.append(b.lo)
    require(len(short) == 5 and len(length_gap) == 25,
            'wrong number of shortest edges')
    expected = set()
    m = (Z, -ONE, Z)
    normal_sum = (Z, Z, Z)
    for _ in range(5):
        i, j = vs.index(v), vs.index(w)
        expected.add((i, j))
        e = sub(w, v)
        normal = linear_cross(e, N)
        require(normal == tuple(lscale(2*c, alpha) for c in m),
                'short-edge normal formula')
        require(ldot(m, v) == lf(0) and ldot(m, w) == lf(0),
                'short-edge support is not exactly one')
        normal_sum = tuple(x+y for x, y in zip(normal_sum, m))
        v, w, m = lmv(G, v), lmv(G, w), mv(G, m)
    require(set(short) == expected, 'short edges not one fivefold orbit')
    require(normal_sum == (Z, Z, Z), 'contact normals do not cancel')
    return {'shadow_vertices': 30, 'support_tests': supports,
            'exact_endpoint_tests': 60, 'strict_support_tests': len(gap),
            'shortest_edges': 5, 'longer_edges': 25,
            'strict_convex_turns': 30,
            'strict_support_gap_lower_bound': str(min(gap)),
            'longer_squared_edge_gap_lower_bound': str(min(length_gap)),
            'turn_lower_bound': str(min(turns))}


def audit_contacts(vs, mats):
    v = (lf(2, -ONE), lf(0, -ONE), lf(1, -ONE))
    w = (lf(2), lf(0, -ONE), lf(1))
    m = (Z, -ONE, Z)
    a = (lf(1, -ONE), lf(0, Z), lf(2))
    require(linear_cross(v, m) == a, 'first contact gradient')
    require(linear_cross(w, m) == tuple(lscale(-ONE, x) for x in a),
            'second contact gradient')
    require(lmv(TY, v) == w and mv(TY, N) == tuple(-c for c in N),
            'missing proper endpoint swap')
    alpha, beta = ldot(N, a), ldot((PHI, Z, -ONE), a)
    require(alpha == ladd(lscale(PHI, lf(2)), lf(1, -ONE)),
            'axial gradient formula')
    require(beta == ladd(lscale(-PHI, lf(1)), lf(2, -ONE)),
            'transverse gradient formula')
    ai, bi = linterval(alpha, BOX), linterval(beta, BOX)
    require(ai.lo > 0 and bi.hi < 0, 'contact orbit is rank deficient')
    normal_sum = [Z, Z, Z]
    grad_sum = [lf(0, Z)]*3
    first_normals = []
    for _ in range(5):
        require(v in vs and w in vs, 'contact point outside original model')
        require(linear_cross(v, m) == a
                and linear_cross(w, m) == tuple(lscale(-ONE, x) for x in a),
                'paired contact gradients fail to cancel')
        first_normals.append(m)
        normal_sum = [x+y for x, y in zip(normal_sum, m)]
        grad_sum = [ladd(x, y) for x, y in zip(grad_sum, a)]
        v, w, a, m = lmv(G, v), lmv(G, w), lmv(G, a), mv(G, m)
    require(tuple(normal_sum) == (Z, Z, Z), 'five normals do not average to zero')
    require(tuple(grad_sum) == tuple(lscale(5*c/H, alpha) for c in N),
            'gradient axial average')
    # The first two contact normals span N^perp. For the gradient orbit,
    # a nonzero axial average and a nonzero transverse component suffice:
    # G has angle72 degrees, strictly between0 and180 degrees.
    mn = first_normals[:2]
    normal_gram = (dot(mn[0], mn[0])*dot(mn[1], mn[1])
                   -dot(mn[0], mn[1])*dot(mn[0], mn[1]))
    require(normal_gram.sign() > 0, 'contact normals do not span plane')
    cosine = (PHI-1)/2
    require((cosine+1).sign() > 0 and (1-cosine).sign() > 0,
            'generator is a degenerate planar rotation')
    stabilizer = [M for M in mats if mv(M, N) in (N, tuple(-c for c in N))]
    require(len(stabilizer) == 10 and TY in stabilizer,
            'wrong proper axis stabilizer')
    rotations, reflected = 0, 0
    for M in stabilizer:
        # Determinant on N^perp equals the oriented-axis sign for proper M.
        if mv(M, N) == N:
            rotations += 1
        else:
            reflected += 1
    require((rotations, reflected) == (5, 5), 'wrong planar dihedral action')
    return {'contacts': 10, 'linear_cone_variables': 6,
            'linear_cone_kernel_with_nonnegative_scale': 'ZERO',
            'proper_axis_stabilizer_order': 10,
            'proper_planar_symmetries': rotations,
            'improper_planar_symmetries': reflected,
            'axial_gradient_lower_bound': str(ai.lo),
            'minus_transverse_gradient_lower_bound': str(-bi.hi),
            'contact_normal_gram': [str(normal_gram.a), str(normal_gram.b)]}


def main():
    data = json.loads((HERE / 'polygon.json').read_text())
    mats = group()
    vs = vertices(mats)
    out = {'agent': 'six-rupert-1', 'role': 'researcher',
           'claim': 'closed minimum-fit classification and qualitative uniform receiving neighborhoods',
           'full_rupert_problem': 'OPEN', 'numeric_radius': None,
           'minimum_diameter_dependency_ref': 'bafkreig6lwaauql5ebhxsquhx4zcdkprdyy4vfk3mfodeqgkoc3mznzlvi',
           'dependency_source_commit': '86ab225fb8becbe66601a5da0b5b017e872e1833',
           'arithmetic_dependency_sha256': BASE_HASH,
           'polygon_sha256': hashlib.sha256((HERE / 'polygon.json').read_bytes()).hexdigest(),
           'floating_point_proof_decisions': 0,
           'closed_minimum_fit_orientation_matrices': 60,
           'qualitative_radius_uniform_on_closed_parameter_box': True}
    out.update(audit_polygon(vs, data))
    out.update(audit_contacts(vs, mats))
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
