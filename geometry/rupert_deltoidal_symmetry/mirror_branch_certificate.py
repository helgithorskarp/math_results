#!/usr/bin/env python3
"""Exact endpoint/stress certificate closing the mirror-normal branch at E.

Q(sqrt(5))[epsilon,delta,z], delta=t-Tstar. Standard library only.
The proof and geometric quantifiers are in mirror_branch_proof.md.
"""
from fractions import Fraction as F
import json
from stress_limit_certificate import (
    Q5, S, ZERO, PHI, vec, vertices, add, sub, mul, dot,
    E, RAYS, T_STAR, TRIPLES, MONOMIAL_ZERO,
    const, psum, pscale, times, pdot, pcross, pvec,
    divide_monomial, quaternion_rows, digest,
    check as prior_stress_check,
)

BOX = F(1, 10**6)
CORE = BOX/10
ETA = F(1, 1000)
DELTA = {(0, 1, 0): Q5(1)}
AXIAL = {(0, 0, 1): Q5(1)}
ENDPOINTS = ((58, 45, 45), (45, 34, 45))


def origin(P):
    return P.get(MONOMIAL_ZERO, ZERO)


def norm(c):
    """Rational upper bound for |a+b*sqrt(5)|, using sqrt(5)<3."""
    return abs(c.a) + 3*abs(c.b)


def coefficient_norm(P, omit_origin=False):
    return sum((norm(c) for e, c in P.items()
                if not (omit_origin and e == MONOMIAL_ZERO)), F(0))


def split_ideal(P):
    """Replay P=delta*A+z*B; reject any term outside (delta,z)."""
    A, B = {}, {}
    for (i, j, k), c in P.items():
        assert j > 0 or k > 0
        if j > 0:
            A[(i, j-1, k)] = c
        else:
            B[(i, j, k-1)] = c
    assert psum(times(DELTA, A), times(AXIAL, B)) == P
    return A, B


def receiver_error_bound(P):
    """Error at u=E+(X,Y,0), all five variables bounded by BOX.

    For the vector polynomial P, bound |u.P-E.P(0)|. Every nonconstant
    monomial is at most BOX in absolute value, since BOX<=1.
    """
    PE = pdot(pvec(E), P)
    return BOX*(coefficient_norm(PE, omit_origin=True)
                + coefficient_norm(P[0]) + coefficient_norm(P[1]))


def check():
    prior = prior_stress_check()
    V = vertices()
    astar = add(mul(T_STAR, RAYS[0]), mul(1-T_STAR, RAYS[1]))
    direction = sub(RAYS[0], RAYS[1])
    assert astar == vec((-1, -PHI, 1/PHI))
    assert V[45] == mul(-S/2, astar)
    # Variable exponents: epsilon, delta=t-Tstar, z.
    W = tuple({(1, 0, 0): astar[i], (1, 1, 0): direction[i],
               (1, 0, 1): E[i]} for i in range(3))

    endpoint_reports = []
    c = (40-16*S)/3
    assert c > Q5(1)
    for contact, sign in zip(ENDPOINTS, (1, -1)):
        R = quaternion_rows(V, W, contact)
        # Entire row vanishes whenever delta=z=0, for every epsilon.
        R0 = tuple({e: x for e, x in P.items() if e[1] == e[2] == 0}
                   for P in R)
        assert R0 == ({}, {}, {})
        scaled = [divide_monomial(P, (1, 0, 0)) for P in R]
        splits = [split_ideal(P) for P in scaled]
        A, B = tuple(p[0] for p in splits), tuple(p[1] for p in splits)
        assert origin(pdot(pvec(E), A)) == ZERO
        assert origin(pdot(pvec(E), B)) == sign*c
        A_bound = receiver_error_bound(A)
        B_error = receiver_error_bound(B)
        assert A_bound <= ETA
        assert c-Q5(B_error) > Q5(1)
        endpoint_reports.append({
            'contact': list(contact), 'axial_slope_at_origin': str(sign*c),
            'delta_coefficient_absolute_bound': str(A_bound),
            'axial_coefficient_error_bound': str(B_error),
            'row_sha256': [digest(P) for P in R],
        })

    stress_reports = []
    for name, contacts, det_sign in TRIPLES:
        rows = [quaternion_rows(V, W, contact) for contact in contacts]
        minors = []
        weights = []
        for i in range(3):
            a, b = rows[(i+1)%3], rows[(i+2)%3]
            M = psum(times(a[0], b[1]), pscale(-1, times(a[1], b[0])))
            minors.append(M)
            weight = divide_monomial(pscale(-1, M),
                                     (2 if i == 0 else 1, 0, 0))
            if i == 1:
                error = BOX*coefficient_norm(weight, omit_origin=True)
                lower = origin(weight)-Q5(error)
                assert lower.sign() > 0
                weights.append({'index': i+1, 'origin': str(origin(weight)),
                                'box_lower_bound': str(lower)})
            else:
                P, Q = split_ideal(weight)
                error = BOX*coefficient_norm(P, omit_origin=True)
                z_coefficient_bound = coefficient_norm(Q)
                lower = origin(P)-Q5(error+ETA*z_coefficient_bound)
                assert lower.sign() > 0
                weights.append({
                    'index': i+1, 'delta_slope_at_origin': str(origin(P)),
                    'delta_coefficient_error_bound': str(error),
                    'z_coefficient_absolute_bound': str(z_coefficient_bound),
                    'weight_over_delta_lower_bound': str(lower),
                })
        D = pdot(rows[0], pcross(rows[1], rows[2]))
        total = [{} for _ in range(3)]
        for M, R in zip(minors, rows):
            total = [psum(P, times(M, Q)) for P, Q in zip(total, R)]
        assert total == [{}, {}, D]
        quotient = divide_monomial(D, (2, 0, 1))
        error = BOX*coefficient_norm(quotient, omit_origin=True)
        lower = det_sign*origin(quotient)-Q5(error)
        assert lower.sign() > 0
        stress_reports.append({
            'name': name, 'weights': weights,
            'determinant_quotient_origin': str(origin(quotient)),
            'signed_determinant_quotient_box_lower_bound': str(lower),
            'determinant_sha256': digest(D),
        })

    # Exact reflection parameter formula, including its fixed-point slope.
    c_mirror, d_mirror = 1+4*S/5, (-5+4*S)/11
    assert d_mirror+T_STAR*(c_mirror-d_mirror) == Q5(1)
    assert d_mirror*(1-T_STAR) == T_STAR
    # t'=d*(1-t)/(d+t*(c-d)); hence delta'=-delta/K,
    # epsilon'=epsilon*K and z'=-z/K. K tends to one.
    h = vec((-PHI, -PHI**2, 1))
    reflect = lambda v: sub(v, mul(2*dot(h, v)/dot(h, h), h))
    assert reflect(E) == E
    assert mul(-1, reflect(astar)) == astar
    assert mul(-1, reflect(direction)) == sub(mul(c_mirror-d_mirror, astar), direction)
    basis = [vec((1,0,0)), vec((0,1,0)), vec((0,0,1))]
    columns = [reflect(v) for v in basis]
    for i in range(3):
        for j in range(3):
            assert dot(columns[i], columns[j]) == Q5(i == j)
        assert all(Q5(-1) <= x <= Q5(1) for x in columns[i])
    assert all(Q5(-1) <= x <= Q5(1) for x in E)
    assert ZERO < c_mirror-d_mirror < Q5(3)
    assert 3*CORE < F(1,2) and 8*CORE <= BOX

    return {
        'status': 'exact endpoint rate and positive stresses exclude the remaining strict mirror-normal branch',
        'agent': 'six-rupert-1', 'role': 'researcher',
        'positive_delta_box_radius': str(BOX),
        'two_sided_critical_box_radius': str(CORE),
        'necessary_axial_to_delta_ratio_bound': str(ETA),
        'receiver_chart': 'u=E+(X,Y,0); epsilon,|delta|,|z|,|X|,|Y|<=BOX, epsilon>0',
        'mirror_bounds_on_CORE': '1/2<K<2; transformed epsilon,|delta|,|z|<=2*CORE; receiver |X|,|Y|<=8*CORE<=BOX',
        'endpoint_certificates': endpoint_reports,
        'stress_certificates': stress_reports,
        'support_domain': prior['receiver_support_domain'],
        'prior_support_comparisons': prior['receiver_support_comparisons'],
        'consequence': 'some positive receiver cap and angle bound exclude strict passages at all 30 E axes; only the 15 A axes remain as small-angle limits',
        'uniform_cap_sizes_computed': False,
        'global_Rupert_status': 'unresolved',
        'solver_or_floating_point_decisions': 0,
    }


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
