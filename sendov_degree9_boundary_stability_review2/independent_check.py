#!/usr/bin/env python3
"""Exact reviewer evidence, standard library only; no target-code imports.

Ascending dense polynomials over Q; Schur recursion certifies strict disk
location for concrete instances of the target's sharpness family. A separate
real-quartic reduction certifies unit-circle location for the refinement's
family. Neither finite test substitutes for the written analytic proof.
"""
from fractions import Fraction as F
from math import comb
import hashlib
import json
import sys


def clean(p):
    p = list(map(F, p))
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def mul(p, q):
    r = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return clean(r)


def derivative(p):
    return clean([i * p[i] for i in range(1, len(p))] or [0])


def evaluate(p, x):
    r = F(0)
    for a in reversed(p):
        r = r * x + a
    return r


def divide_root_one(p):
    # Synthetic division, checked again by multiplication.
    q = [F(0)] * (len(p) - 1)
    q[-1] = p[-1]
    for i in range(len(q) - 2, -1, -1):
        q[i] = p[i + 1] + q[i + 1]
    if mul([-1, 1], q) != clean(p):
        raise ValueError('1 is not a root')
    return q


def schur_strict_disk(p):
    """Real Schur-Cohn recursion, exact; returns truth and degree trace.

    For monic h, |c0|<1 and g=(h-c0*h*)/z is the smaller problem.
    Equivalence follows in both directions by Rouche on the unit circle.
    The target's distinguished boundary root is divided out first.
    """
    p = clean(p)
    trace = []
    while len(p) > 1:
        p = [a / p[-1] for a in p]
        n = len(p) - 1
        c = p[0]
        if abs(c) >= 1:
            return False, trace
        trace.append(n)
        p = clean([p[i + 1] - c * p[n - i - 1] for i in range(n)])
    return p[0] != 0, trace


def source_family(u):
    p = [F(0)] * 10
    p[9], p[8], p[7] = F(1), -F(27, 4) * u, F(9, 7) * (u + 9 * u * u)
    p[0] = -1 - p[8] - p[7]
    return p


def certificate():
    fixtures = []
    for u in [F(1, 10**4), F(1, 10**6), F(1, 10**7)]:
        p = source_family(u)
        assert evaluate(p, 1) == 0 and evaluate(derivative(p), 1) != 0
        assert derivative(p) == mul([0] * 6 + [9], [u + 9 * u * u, -6 * u, 1])
        accepted, degrees = schur_strict_disk(divide_root_one(p))
        assert accepted and degrees == list(range(8, 0, -1))
        r2 = 1 - 5 * u + 9 * u * u
        delta = (F(6) + F(2) / r2) / 8 - 1
        energy = 2 * (u + 9 * u * u)
        assert delta == (5 * u - 9 * u * u) / (4 * r2) and r2 < 1
        if u <= F(1, 10**6):
            assert 0 < delta <= F(2, 10**5)
            assert (1 - F(1, 10**5)) ** 2 < r2
            assert energy < 9 * delta
        fixtures.append({'u': str(u), 'strict_disk_quotient_degrees': degrees,
                         'quadratic_deficit': str(delta), 'critical_energy': str(energy)})

    # Positive and rejection controls for the generic location checker.
    assert schur_strict_disk(mul([-F(1, 2), 1], [F(1, 3), 1]))[0]
    assert not schur_strict_disk([-2, 1])[0]
    assert not schur_strict_disk([-1, 1])[0]  # boundary excluded by strict test
    try:
        divide_root_one([1, 0, 1])
    except ValueError:
        pass
    else:
        raise AssertionError('non-root control accepted')
    assert evaluate(derivative(mul([-1, 1], [-1, 1])), 1) == 0

    # Unit-circle family G_t=z^9-1+t(z^5-z^4).
    # G_t/(z-1) has coefficients 1 except its middle coefficient 1+t.
    # z^-4 G_t/(z-1) = H_t(z+z^-1), H_t=x^4+x^3-3x^2-2x+1+t.
    brackets = [(F(-19, 10), F(-18, 10)), (F(-11, 10), F(-9, 10)),
                (F(3, 10), F(4, 10)), (F(15, 10), F(16, 10))]
    signs = []
    for lo, hi in brackets:
        h0lo = evaluate([1, -2, -3, 1, 1], lo)
        h0hi = evaluate([1, -2, -3, 1, 1], hi)
        # Each endpoint keeps its sign for every 0 <= t <= 1/1000.
        assert h0lo * (h0lo + F(1, 1000)) > 0
        assert h0hi * (h0hi + F(1, 1000)) > 0
        assert h0lo * h0hi < 0 and -2 < lo < hi < 2
        signs.append({'interval': [str(lo), str(hi)],
                      'H0_values': [str(h0lo), str(h0hi)]})
    for t in [F(0), F(1, 1000), F(1, 10**15)]:
        q = [F(1)] * 9
        q[4] += t
        g = [F(0)] * 10
        g[0], g[9], g[4], g[5] = -1, 1, -t, t
        assert mul([-1, 1], q) == g
        assert list(reversed(g)) == [-a for a in g]
        assert derivative(g) == mul([0, 0, 0, 1], [-4 * t, 5 * t, 0, 0, 0, 9])
        # Expand sum_{k=1}^4 (z^k+z^-k)+1+t via the Chebyshev recurrence.
        s = [[2], [0, 1]]
        for k in range(2, 5):
            xprev = [F(0)] + s[-1]
            prevprev = s[-2] + [F(0)] * (len(xprev) - len(s[-2]))
            s.append(clean([a - b for a, b in zip(xprev, prevprev)]))
        h = [F(1) + t] + [F(0)] * 4
        for sk in s[1:]:
            for i, a in enumerate(sk):
                h[i] += a
        assert h == [1 + t, -2, -3, 1, 1]

    # New explicit delta^(5/2) root matching constant.
    Tcap = F(1, 32)
    pair_sum = 126 + 84 * Tcap + 36 * Tcap**2 + 9 * Tcap**3
    assert pair_sum < 129
    coefficient_constant = F(129, 4) * 9 * 27
    root_constant = 2500
    assert F(21, 10) * coefficient_constant < 8 * root_constant
    dcap = F(2, 10**5)
    # Square both sides of rho=2500*delta^(5/2) <= 1/100.
    assert root_constant**2 * dcap**5 < F(1, 100)**2
    rho = F(1, 100)
    assert sum(F(comb(9, k)) * rho**(k - 1) for k in range(2, 10)) < 1
    assert (1 + rho)**8 + 1 < F(21, 10)
    assert F(4, 9) > 2 * rho
    return {'source_sharpness_fixtures': fixtures, 'unit_circle_quartic_brackets': signs,
            'unit_circle_family_parameter_range': '0 <= t <= 1/1000',
            'refined_coefficient_constant': str(coefficient_constant),
            'refined_root_constant': root_constant,
            'refined_deficit_cap': str(dcap), 'all_controls_passed': True}


if __name__ == '__main__':
    out = certificate()
    raw = (json.dumps(out, indent=2, sort_keys=True) + '\n').encode()
    if '--json' in sys.argv:
        sys.stdout.buffer.write(raw)
    else:
        print('PASS: 3 exact Schur disk certificates; 4 real-quartic brackets; refinement constants and rejection controls.')
        print('certificate SHA256:', hashlib.sha256(raw).hexdigest())
