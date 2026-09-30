#!/usr/bin/env python3
"""Exact three-contact stresses restricting strict limits at E to one ray.

Domain: Q(sqrt(5))[epsilon,t,z]; w=epsilon*(a(t)+z*E).
Standard-library polynomial arithmetic independently checks CAS discovery.
No numerical, solver, or CAS result is imported as a proof input.
"""
from fractions import Fraction as F
import hashlib
import json
from verify import Q5, PHI, S, ZERO, vec, vertices, add, sub, mul, dot, cross
from orientation_certificate import build_cells
from contact_family_certificate import E, RAYS, HULL, bernstein

MONOMIAL_ZERO = (0, 0, 0)
T_STAR = Q5(F(5, 2)) - S
TRIPLES = (
    ('minus', ((61, 58, 55), (58, 45, 45), (44, 57, 57)), -1),
    ('plus', ((61, 58, 59), (45, 34, 45), (57, 61, 57)), 1),
)


def const(c):
    c = Q5.coerce(c)
    return {MONOMIAL_ZERO: c} if c != ZERO else {}


def psum(p, q):
    out = dict(p)
    for exponent, c in q.items():
        out[exponent] = out.get(exponent, ZERO) + c
        if out[exponent] == ZERO:
            del out[exponent]
    return out


def pscale(c, p):
    return {e: c*x for e, x in p.items() if c*x != ZERO}


def times(p, q):
    out = {}
    for e, a in p.items():
        for f, b in q.items():
            g = tuple(x+y for x, y in zip(e, f))
            out[g] = out.get(g, ZERO) + a*b
    return {e: c for e, c in out.items() if c != ZERO}


def pdot(a, b):
    out = {}
    for p, q in zip(a, b):
        out = psum(out, times(p, q))
    return out


def pcross(a, b):
    return (psum(times(a[1], b[2]), pscale(-1, times(a[2], b[1]))),
            psum(times(a[2], b[0]), pscale(-1, times(a[0], b[2]))),
            psum(times(a[0], b[1]), pscale(-1, times(a[1], b[0]))))


def pvec(v):
    return tuple(const(c) for c in v)


def divide_monomial(p, exponent):
    assert all(all(a >= b for a, b in zip(e, exponent)) for e in p)
    return {tuple(a-b for a, b in zip(e, exponent)): c for e, c in p.items()}


def leading_t(p):
    terms = {j: c for (i, j, k), c in p.items() if i == k == 0}
    assert terms
    return [terms.get(j, ZERO) for j in range(max(terms)+1)]


def digest(p):
    data = [[list(e), str(c.a), str(c.b)] for e, c in sorted(p.items())]
    return hashlib.sha256(json.dumps(data, separators=(',', ':')).encode()).hexdigest()


def quaternion_rows(V, W, contact):
    a, b, j = contact
    v0, v, edge = V[a], V[j], sub(V[b], V[a])
    A = pdot(W, W)
    Wxv, Wv = pcross(W, pvec(v)), pdot(W, pvec(v))
    # Numerator of (outer-Q_w v), then cross with the receiver edge.
    P = tuple(psum(psum(const(v0[i]-v[i]), pscale(v0[i]+v[i], A)),
                   psum(pscale(-2, Wxv[i]), pscale(-2, times(Wv, W[i]))))
              for i in range(3))
    return pcross(P, pvec(edge))


def check():
    V = vertices()
    assert ZERO < T_STAR < Q5(1)
    W = tuple({(1, 0, 0): RAYS[1][i],
               (1, 1, 0): RAYS[0][i]-RAYS[1][i],
               (1, 0, 1): E[i]} for i in range(3))
    reports = []
    for name, contacts, det_sign in TRIPLES:
        rows = [quaternion_rows(V, W, c) for c in contacts]
        minors = []
        leading_minors = []
        for i in range(3):
            a, b = rows[(i+1)%3], rows[(i+2)%3]
            minor = psum(times(a[0], b[1]), pscale(-1, times(a[1], b[0])))
            minors.append(minor)
            # Raw -minor is the positive weight. Division only proves its
            # sign for epsilon>0; it does not rescale the stress identity.
            quotient = divide_monomial(pscale(-1, minor), (2 if i == 0 else 1, 0, 0))
            lead = leading_t(quotient)
            B = bernstein(lead, T_STAR, Q5(1), 2)
            assert all(c.sign() >= 0 for c in B) and B[2].sign() > 0
            leading_minors.append({'epsilon_power': 2 if i == 0 else 1,
                                   'coefficients': list(map(str, lead)),
                                   'Bernstein_on_Tstar_to_1': list(map(str, B))})
        D = pdot(rows[0], pcross(rows[1], rows[2]))
        # Replay the entire polynomial cofactor identity, not only a limit.
        total = [{} for _ in range(3)]
        for c, r in zip(minors, rows):
            total = [psum(p, times(c, q)) for p, q in zip(total, r)]
        assert total == [{}, {}, D]
        quotient = divide_monomial(D, (2, 0, 1))
        lead = leading_t(quotient)
        B = bernstein([det_sign*c for c in lead], T_STAR, Q5(1), 1)
        assert all(c.sign() > 0 for c in B)
        reports.append({'name': name, 'contacts': [list(c) for c in contacts],
                        'positive_weight_limits': leading_minors,
                        'determinant_divisor': 'epsilon^2*z',
                        'determinant_quotient_limit_coefficients': list(map(str, lead)),
                        'determinant_limit_sign': det_sign,
                        'determinant_monomials': len(D),
                        'determinant_sha256': digest(D)})

    h = vec((-PHI, -PHI**2, 1))
    reflect = lambda v: sub(v, mul(2*dot(h, v)/dot(h, h), h))
    assert {reflect(v) for v in V} == set(V)
    assert reflect(E) == E
    assert {reflect(V[j]) for j in HULL} == {V[j] for j in HULL}
    c, d = 1+4*S/5, (-5+4*S)/11
    assert c.sign() > 0 and d.sign() > 0 and c*d == Q5(1)
    assert mul(-1, reflect(RAYS[0])) == mul(c, RAYS[1])
    assert mul(-1, reflect(RAYS[1])) == mul(d, RAYS[0])
    assert T_STAR == d/(1+d)
    K = d + T_STAR*(c-d)
    assert K.sign() > 0 and d*(1-T_STAR) == K*T_STAR
    astar = add(mul(T_STAR, RAYS[0]), mul(1-T_STAR, RAYS[1]))
    assert astar == vec((-1, -PHI, 1/PHI)) == mul(1/PHI, h)

    p = build_cells()[0][0]
    assert E in p
    receiver_corners = p + [reflect(u) for u in p]
    edges = sorted({contact[:2] for _, C, _ in TRIPLES for contact in C})
    comparisons = 0
    for a, b in edges:
        edge = sub(V[b], V[a])
        for u in receiver_corners:
            normal = cross(edge, u)
            assert dot(normal, V[a]).sign() > 0
            for v in V:
                assert dot(normal, sub(V[a], v)).sign() >= 0
                comparisons += 1
    return {
        'status': 'exact stress identities: strict passage limits at E have only the mirror-normal axis',
        'Tstar': str(T_STAR),
        'remaining_oriented_axis_ray': list(map(str, astar)),
        'body_mirror_normal': list(map(str, h)),
        'stress_certificates': reports,
        'axial_mirror_ray_multipliers': [str(c), str(d)],
        'receiver_support_domain': 'cell 0 union its body-mirror image',
        'receiver_support_comparisons': comparisons,
        'solver_or_floating_point_decisions': 0,
    }


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
