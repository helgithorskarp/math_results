#!/usr/bin/env python3
"""Exact finite corroboration of PROOF.md; Python 3.11+, standard library.

Fractions only. No sampling is used to establish the continuum theorem.
Every check survives python -O. Output is deterministic.
"""
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools
import json
from math import comb


COUNTS = Counter()
RECORDS = []


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def record(kind, value):
    COUNTS[kind] += 1
    RECORDS.append([kind, value])


def trim(a):
    a = list(map(F, a))
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a or [F(0)]


def add(a, b):
    return trim([(a[i] if i < len(a) else 0)
                 + (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def scale(a, c):
    return trim([c*x for x in a])


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    out = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return trim(out)


def power(a, k):
    out = [F(1)]
    while k:
        if k % 2:
            out = mul(out, a)
        a = mul(a, a)
        k //= 2
    return out


def deriv(a):
    return trim([i*a[i] for i in range(1, len(a))])


def integ(a):
    return [F(0)]+[x/F(i+1) for i, x in enumerate(a)]


def at(a, x):
    out = F(0)
    for c in reversed(a):
        out = out*x+c
    return out


def dilate(a, r):
    return trim([c*r**i for i, c in enumerate(a)])


def sphere_mean(a, d):
    """E z^(2m)=(1/2)_m/(d/2)_m, for a uniform unit normal."""
    moment = F(1)
    out = F(0)
    for m in range((len(a)+1)//2):
        if m:
            moment *= F(2*m-1, d+2*m-2)
        out += a[2*m]*moment
    return out


def jet(a, x):
    return (at(a, x), at(deriv(a), x), at(deriv(deriv(a)), x))


def jadd(a, b):
    return tuple(x+y for x, y in zip(a, b))


def jscale(a, c):
    return tuple(c*x for x in a)


def jmul(a, b):
    return (a[0]*b[0], a[1]*b[0]+a[0]*b[1],
            a[2]*b[0]+2*a[1]*b[1]+a[0]*b[2])


def jpower(a, k):
    out = (F(1), F(0), F(0))
    while k:
        if k % 2:
            out = jmul(out, a)
        a = jmul(a, a)
        k //= 2
    return out


def root_log_derivatives(g, p):
    """H'/H, H''/H for H=g^(1/p); no root evaluation required."""
    alpha = F(1, p)
    return (alpha*g[1]/g[0],
            alpha*g[2]/g[0]+alpha*(alpha-1)*(g[1]/g[0])**2)


def det(a):
    a = [list(map(F, row)) for row in a]
    out = F(1)
    for i in range(len(a)):
        pivot = next((j for j in range(i, len(a)) if a[j][i]), None)
        if pivot is None:
            return F(0)
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            out = -out
        v = a[i][i]
        out *= v
        for j in range(i+1, len(a)):
            ratio = a[j][i]/v
            for k in range(i+1, len(a)):
                a[j][k] -= ratio*a[i][k]
    return out


def cofactor_quadratic(a, v):
    n = len(a)
    out = F(0)
    for i in range(n):
        for j in range(n):
            minor = [[a[r][c] for c in range(n) if c != j]
                     for r in range(n) if r != i]
            out += (-1)**(i+j)*det(minor)*v[i]*v[j]
    return out


def check_rank_one():
    for n in range(1, 7):
        for seed in range(1, 5):
            m = [[F(((i+2)*(j+seed)) % 7-3, 5)
                  for j in range(n)] for i in range(n)]
            q = [[sum(m[k][i]*m[k][j] for k in range(n))+(i == j)
                  for j in range(n)] for i in range(n)]
            v = [F(i-seed, 3) for i in range(n)]
            a, b = F(seed+1, 3), F(seed, 7)
            matrix = [[a*q[i][j]+b*v[i]*v[j] for j in range(n)]
                      for i in range(n)]
            rhs = a**n*det(q)+a**(n-1)*b*cofactor_quadratic(q, v)
            require(det(matrix) == rhs, 'rank-one determinant')
            record('rank_one_matrices', [n, seed, str(rhs)])


Z = [F(0), F(1)]
ONE_MINUS_Z2 = [F(1), F(0), F(-1)]
SUPPORTS = [[F(1)], [F(1), 0, F(1, 12)],
            [F(1), 0, F(-1, 16), 0, F(1, 100)]]


def check_cofactor_divergence():
    for d in range(2, 13):
        for h in SUPPORTS:
            b = sub(h, mul(Z, deriv(h)))
            c = add(b, mul(ONE_MINUS_Z2, deriv(deriv(h))))
            w = power(b, d-1)  # h^2 U_meridian t', with l=z
            lhs = sub(mul(ONE_MINUS_Z2, deriv(w)), scale(mul(Z, w), d-1))
            rhs = scale(mul(Z, mul(power(b, d-2), c)), -(d-1))
            require(lhs == rhs, 'cofactor divergence sign/dimension')
            record('cofactor_divergence', [d, list(map(str, h))])


def check_actual_firey_curvature():
    for p in range(2, 10):
        for h_poly in SUPPORTS:
            for z in (F(-3, 4), F(-1, 3), F(0), F(2, 3)):
                for r in (F(1, 5), F(1, 2)):
                    h = jet(h_poly, z)
                    l = (r*z, r, F(0))
                    g = jadd(jpower(jadd(h, l), p),
                             jpower(jadd(h, jscale(l, -1)), p))
                    H1, H2 = root_log_derivatives(g, p)
                    t = l[0]/h[0]
                    t1 = (r*h[0]-l[0]*h[1])/h[0]**2
                    s = jadd(jpower((1+t, F(1), F(0)), p),
                             jpower((1-t, F(-1), F(0)), p))
                    f1, f2 = root_log_derivatives(s, p)
                    require(f2 == 4*(p-1)*(1-t*t)**(p-2)/s[0]**2,
                            'Firey second derivative')
                    a_over_f = 1-t*f1
                    qpar = h[0]-z*h[1]
                    qmer = qpar+(1-z*z)*h[2]
                    require(h[0] > 0 and qpar > 0 and qmer > 0,
                            'positive-curvature sample')
                    actual_par = 1-z*H1
                    actual_mer = actual_par+(1-z*z)*H2
                    predicted_par = a_over_f*qpar/h[0]
                    predicted_mer = a_over_f*qmer/h[0]+f2*(1-z*z)*t1*t1
                    require(actual_par == predicted_par and
                            actual_mer == predicted_mer, 'Firey curvature')
                    record('actual_firey_curvature',
                           [p, str(z), str(r), str(actual_mer), str(actual_par)])


def kernel(f, d):
    a = sub(f, mul(Z, deriv(f)))
    R = integ(mul(mul(f, power(a, d-2)), deriv(deriv(f))))
    psi = add(mul(f, power(a, d-1)), scale(mul(Z, R), d-1))
    return a, R, psi


def check_integrated_volume():
    fs = [[F(1), 0, F(1)],
          [F(3, 2), 0, F(1, 3), 0, F(1, 7)]]
    for d in range(2, 11):
        for f in fs:
            a, R, psi = kernel(f, d)
            require(deriv(deriv(psi)) ==
                    scale(mul(deriv(deriv(f)), power(a, d-1)), d),
                    'kernel second derivative')
            record('kernel_polynomial_identity', [d, list(map(str, f))])
            for r in (F(1, 3), F(1, 2), F(3, 4)):
                H = dilate(f, r)
                qpar = sub(H, mul(Z, deriv(H)))
                qmer = add(qpar, mul(ONE_MINUS_Z2, deriv(deriv(H))))
                direct = sphere_mean(mul(H, mul(qmer, power(qpar, d-2))), d)
                transformed = sphere_mean(dilate(psi, r), d)
                require(direct == transformed, 'direct integrated volume')
                record('exact_spherical_volumes', [d, str(r), str(direct)])

    d, r, f = 5, F(1, 2), fs[0]
    a, R, psi = kernel(f, d)
    good = sphere_mean(dilate(psi, r), d)
    wrong_sign = sub(mul(f, power(a, d-1)), scale(mul(Z, R), d-1))
    wrong_dim = add(mul(f, power(a, d-1)), scale(mul(Z, R), d))
    wrong_power = add(mul(f, power(a, d-2)), scale(mul(Z, R), d-1))
    for name, wrong in [('divergence_sign', wrong_sign),
                        ('tangent_dimension', wrong_dim),
                        ('determinant_power', wrong_power)]:
        require(sphere_mean(dilate(wrong, r), d) != good,
                'corruption was not rejected: '+name)
        record('rejected_corruptions', name)
    require(good*d != good, 'missing volume divisor')
    record('rejected_corruptions', 'volume_normalization')


def gamma_half(n):
    """Gamma(1+n/2)=coefficient * sqrt(pi)^parity."""
    if n % 2 == 0:
        out = F(1)
        for k in range(1, n//2+1):
            out *= k
        return out, 0
    out = F(1)
    for k in range(n//2+1):
        out *= F(2*k+1, 2)
    return out, 1


def add_pi(a, b):
    return tuple(x+y for x, y in zip(a, b))


def scale_pi(a, c):
    return tuple(c*x for x in a)


def check_constants():
    r_values = {2: (F(0), F(1, 2)), 3: (F(2), F(0))}
    displayed = {}
    for d in range(2, 41):
        if d >= 4:
            r_values[d] = add_pi((F(2, d-2), F(0)),
                                scale_pi(r_values[d-2], F(2*(d-3), d-2)))
        kernel_constant = add_pi((F(2), F(0)), scale_pi(r_values[d], d-1))
        gamma_constant = (F(0), F(0))
        gd, ed = gamma_half(d)
        for i in range(d+1):
            gi, ei = gamma_half(i)
            gj, ej = gamma_half(d-i)
            exponent = ei+ej-ed
            require(exponent in (0, 2), 'half-gamma exponent')
            term = comb(d, i)*gi*gj/gd
            gamma_constant = add_pi(gamma_constant,
                                    (term, F(0)) if exponent == 0 else (F(0), term))
        require(gamma_constant == kernel_constant, 'p=2 constant')
        record('exact_p2_constants', [d, list(map(str, kernel_constant))])
        if d <= 6:
            displayed[str(d)] = {'rational': str(kernel_constant[0]),
                                 'pi_coefficient': str(kernel_constant[1])}
        for i in range(1, d):
            for q in (F(1), F(5, 4), F(3, 2), F(2), F(3), F(17, 3), F(100)):
                beta_prefactor = F(d-1)/q*comb(d-2, i-1)
                gamma_prefactor = comb(d, i)*(F(i)/q)*(F(d-i)/q)/(F(d)/q)
                require(beta_prefactor == gamma_prefactor, 'beta-gamma normalization')
                record('beta_gamma_coefficients', [d, i, str(q), str(beta_prefactor)])
    require(displayed['2'] == {'rational': '2', 'pi_coefficient': '1/2'}, 'planar check')
    require(displayed['3'] == {'rational': '6', 'pi_coefficient': '0'}, '3D check')
    require(displayed['4'] == {'rational': '5', 'pi_coefficient': '3/2'}, '4D check')
    # The endpoint constant 2 must not be dropped in the beta evaluation.
    require(add_pi(scale_pi(r_values[4], 3), (F(0), F(0))) != (F(5), F(3, 2)),
            'missing endpoint terms')
    record('rejected_corruptions', 'missing_two_endpoint_terms')
    return displayed


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def check_equality_geometry():
    for d in range(2, 9):
        cube_polar = [tuple(F(sign if i == j else 0) for i in range(d))
                      for j in range(d) for sign in (-1, 1)]
        cross_polar = list(itertools.product((F(-1), F(1)), repeat=d))
        for name, polar, x in (
                ('cube_vertex', cube_polar, (F(1),)*d),
                ('crosspolytope_vertex', cross_polar, (F(1),)+(F(0),)*(d-1))):
            require(all(abs(dot(x, u)) == 1 for u in polar), 'equality facet criterion')
            record('equality_fixtures', [d, name, len(polar)])
            interior = tuple(v/2 for v in x)
            require(all(abs(dot(interior, u)) < 1 for u in polar), 'strict interior')
            record('strict_fixtures', [d, name+'_interior'])
        edge = (F(0),)+(F(1),)*(d-1)
        contacts = [abs(dot(edge, u)) for u in cube_polar]
        require(0 in contacts and 1 in contacts, 'boundary but not equality')
        record('strict_fixtures', [d, 'cube_edge_interior'])

    # A non-centrally-symmetric top face: the equality description cannot
    # be restricted to polars of Cartesian products or to double cones.
    F_top = [(F(2), F(0), F(1)), (F(0), F(1), F(1)),
             (F(-1), F(-2), F(1)), (F(-1), F(1), F(1))]
    polar = F_top+[tuple(-v for v in u) for u in F_top]
    require(det(F_top[:3]) != 0, 'full-dimensional polar')
    require(all(abs(u[2]) == 1 for u in polar), 'nonproduct face fixture')
    record('equality_fixtures', [3, 'nonsymmetric_top_face', len(polar)])


def main():
    check_rank_one()
    check_cofactor_divergence()
    check_actual_firey_curvature()
    check_integrated_volume()
    constants = check_constants()
    check_equality_geometry()
    encoded = json.dumps(RECORDS, ensure_ascii=True, separators=(',', ':')).encode()
    result = {'arithmetic': 'exact fractions; constants in Q+Q*pi',
              'checks': dict(sorted(COUNTS.items())),
              'p2_constants': constants,
              'record_sha256': hashlib.sha256(encoded).hexdigest(),
              'status': 'VERIFIED',
              'trust_boundary': 'Finite corroboration; analytic proof is in PROOF.md.'}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
