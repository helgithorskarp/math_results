#!/usr/bin/env python3
"""Exact moving-receiver closed contact family for the deltoidal solid.

Python 3.11+, standard library only. All decisions use Q(sqrt(5)).
This certifies boundary-touching containments, not a Rupert passage.
The analytic interpretation is in contact_family_proof.md.
"""
from fractions import Fraction as F
from math import comb
import json
import sys
from verify import Q5, S, ZERO, vec, vertices, add, sub, mul, dot, cross

E = vec(((3 * S - 5) / 10, (5 - S) / 10, 1))
RAYS = (vec((-1, -(5 + S) / 2, (5 + 3 * S) / 10)),
        vec((-1, (-31 + 5 * S) / 22, (7 + S) / 22)))
HULL = (61, 58, 45, 34, 17, 4, 0, 3, 16, 27, 44, 57)
T_LO, T_HI, EPS_MAX = F(2, 5), F(4, 5), F(1, 100)


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == ZERO:
        p.pop()
    return p


def padd(p, q):
    return trim([(p[i] if i < len(p) else ZERO) +
                 (q[i] if i < len(q) else ZERO)
                 for i in range(max(len(p), len(q)))])


def pscale(c, p):
    return trim([c * x for x in p])


def pmul(p, q):
    out = [ZERO] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return trim(out)


def pvec(v):
    return tuple([x] for x in v)


def pdot(a, b):
    out = [ZERO]
    for p, q in zip(a, b):
        out = padd(out, pmul(p, q))
    return out


def pcross(a, b):
    return (padd(pmul(a[1], b[2]), pscale(-1, pmul(a[2], b[1]))),
            padd(pmul(a[2], b[0]), pscale(-1, pmul(a[0], b[2]))),
            padd(pmul(a[0], b[1]), pscale(-1, pmul(a[1], b[0]))))


def bernstein(p, lo, hi, degree=3):
    """Coefficients in the Bernstein basis on [lo,hi], exact.

    First substitute t=lo+(hi-lo)*x in the power basis, then use
    x^i=sum_{k=i}^degree C(k,i)/C(degree,i) B_{degree,k}(x).
    """
    assert hi > lo and len(p) <= degree + 1
    c = [ZERO] * (degree + 1)
    for i, a in enumerate(p):
        for j in range(i + 1):
            c[j] += a * comb(i, j) * lo**(i-j) * (hi-lo)**j
    return [sum((c[i] * F(comb(k, i), comb(degree, i))
                 for i in range(k + 1)), ZERO) for k in range(degree + 1)]


def tensor_bernstein(C, eps_max, t_lo, t_hi):
    """C[i](t) is the coefficient of epsilon^i, degrees <=3."""
    assert len(C) <= 4 and eps_max > 0
    rows = [bernstein(p, t_lo, t_hi) for p in C]
    rows += [[ZERO] * 4 for _ in range(4 - len(rows))]
    return [[sum((rows[i][k] * eps_max**i *
                  F(comb(j, i), comb(3, i)) for i in range(j + 1)), ZERO)
             for k in range(4)] for j in range(4)]


def positivity(C, eps_max, t_lo, t_hi, strict_for_positive_epsilon=False):
    B = tensor_bernstein(C, eps_max, t_lo, t_hi)
    assert all(c.sign() >= 0 for row in B for c in row)
    if strict_for_positive_epsilon:
        # B_{3,3}(epsilon/eps_max)>0 whenever epsilon>0. The four
        # Bernstein basis functions in t sum to one, including endpoints.
        assert all(c.sign() > 0 for c in B[3])
    return B


def gap_coefficients(V, a, p, edge, j, A):
    """Cayley numerator gap as epsilon power coefficients in Q5[t]."""
    first, second = edge
    e = pvec(sub(V[second], V[first]))
    outer, v, E_poly = pvec(V[first]), pvec(V[j]), pvec(E)
    n0, nd = pcross(e, E_poly), pcross(e, p)
    b0, bd = pdot(n0, outer), pdot(nd, outer)
    C0 = padd(b0, pscale(-1, pdot(n0, v)))
    C1 = padd(padd(bd, pscale(-1, pdot(nd, v))),
              pscale(-2, pdot(n0, pcross(a, v))))
    C2 = padd(pmul(A, padd(b0, pdot(n0, v))),
              pscale(-2, pmul(pdot(n0, a), pdot(a, v))))
    C2 = padd(C2, pscale(-2, pdot(nd, pcross(a, v))))
    C3 = padd(pmul(A, padd(bd, pdot(nd, v))),
              pscale(-2, pmul(pdot(nd, a), pdot(a, v))))
    return [C0, C1, C2, C3]


def verify(rays=RAYS, hull=HULL, eps_max=EPS_MAX):
    V = vertices()
    assert len(set(hull)) == 12 and len(hull) == 12
    assert T_LO < T_HI and eps_max > 0
    assert all(dot(a, E) == ZERO for a in rays)
    assert rays[0][0] == rays[1][0] == Q5(-1)
    # a(t)=t*r1+(1-t)*r2 never vanishes because its first coordinate is -1.
    a = tuple([rays[1][k], rays[0][k] - rays[1][k]] for k in range(3))
    E_poly = pvec(E)
    p = pcross(a, E_poly)
    A = pdot(a, a)
    assert pdot(a, E_poly) == [ZERO]
    # The chart stays above z=0; the viewing vector is nonzero throughout.
    positivity([[E[2]], p[2]], eps_max, T_LO, T_HI, True)

    coefficient_count = support_count = gap_count = 0
    permanent, other_contacts = [], []
    for k, first in enumerate(hull):
        second = hull[(k + 1) % len(hull)]
        edge = pvec(sub(V[second], V[first]))
        n0, nd = pcross(edge, E_poly), pcross(edge, p)
        b0, bd = pdot(n0, pvec(V[first])), pdot(nd, pvec(V[first]))
        positivity([b0, bd], eps_max, T_LO, T_HI, True)
        before = sub(V[first], V[hull[(k-1) % len(hull)]])
        turn = pvec(cross(before, sub(V[second], V[first])))
        positivity([pdot(E_poly, turn), pdot(p, turn)],
                   eps_max, T_LO, T_HI, True)
        for j, v in enumerate(V):
            outer_support = [padd(b0, pscale(-1, pdot(n0, pvec(v)))),
                             padd(bd, pscale(-1, pdot(nd, pvec(v))))]
            positivity(outer_support, eps_max, T_LO, T_HI,
                       j not in (first, second))
            support_count += 1
            C = gap_coefficients(V, a, p, (first, second), j, A)
            identically_zero = all(poly == [ZERO] for poly in C)
            B = positivity(C, eps_max, T_LO, T_HI, not identically_zero)
            coefficient_count += sum(len(row) for row in B)
            gap_count += 1
            if identically_zero:
                reflected = sub(v, mul(2 * dot(E, v) / dot(E, E), E))
                delta = sub(V[second], V[first])
                coord = next(i for i in range(3) if delta[i] != ZERO)
                lam = (reflected[coord] - V[first][coord]) / delta[coord]
                assert reflected == add(V[first], mul(lam, delta))
                assert lam.sign() >= 0 and (1-lam).sign() >= 0
                permanent.append([first, second, j, str(lam)])
            elif C[0] == [ZERO]:
                other_contacts.append([first, second, j])
    assert len(permanent) == len(other_contacts) == 16
    # This is a proper containment: the inner polygon cannot attain receiver
    # vertex 61. Attaining it would require equality on both adjacent edges,
    # whose lists of inner equality vertices are disjoint.
    first_edge = {j for a0, b0, j, _ in permanent if (a0, b0) == (61, 58)}
    last_edge = {j for a0, b0, j, _ in permanent if (a0, b0) == (57, 61)}
    assert first_edge == {55, 59} and last_edge == {57}
    assert not first_edge.intersection(last_edge)
    # The max-radius vertex pair 4,57 remains on the shadow boundary.
    R2 = (25 + 10*S) / 9
    assert dot(V[4], V[4]) == dot(V[57], V[57]) == R2
    assert all(dot(v, v) <= R2 for v in V)
    assert dot(E, V[4]) == dot(E, V[57]) == ZERO
    return {
        'status': 'exact nontrivial closed containments with boundary contact; no Rupert passage',
        'parameter_t': [str(T_LO), str(T_HI)],
        'parameter_epsilon': ['0 (excluded)', str(eps_max)],
        'receiver_hull': list(hull),
        'outer_support_comparisons': support_count,
        'Cayley_gap_polynomials': gap_count,
        'strictly_positive_gap_polynomials_for_epsilon_positive': gap_count - len(permanent),
        'nonnegative_tensor_Bernstein_coefficients': coefficient_count,
        'identically_zero_contact_gaps': permanent,
        'contacts_at_epsilon_zero_that_become_strict': other_contacts,
        'max_radius_equatorial_vertices': [4, 57],
        'proper_containment_witness_missing_outer_vertex': 61,
        'closed_optimal_uniform_scale': '1',
        'solver_or_floating_point_decisions': 0,
    }


def self_test():
    cases = [('nonperpendicular first axis',
              {'rays': (add(RAYS[0], vec((0, 0, 1))), RAYS[1])}),
             ('reversed hull orientation', {'hull': tuple(reversed(HULL))}),
             ('oversized parameter interval', {'eps_max': F(1)})]
    for name, kwargs in cases:
        try:
            verify(**kwargs)
        except AssertionError:
            continue
        raise AssertionError('accepted malformed certificate: ' + name)
    return [name for name, _ in cases]


if __name__ == '__main__':
    report = verify()
    if '--self-test' in sys.argv[1:]:
        report['rejected_mutations'] = self_test()
    print(json.dumps(report, indent=2))
