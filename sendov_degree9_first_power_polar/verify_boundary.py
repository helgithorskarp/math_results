#!/usr/bin/env python3
"""Exact controls for the analytic boundary-saturation classification."""
from fractions import Fraction as F
from math import comb


def need(ok, message):
    if not ok:
        raise ValueError(message)


def roots_polynomial(roots):
    coeff = [F(1)]
    for root in roots:
        out = [F(0)] * (len(coeff) + 1)
        for k, value in enumerate(coeff):
            out[k] -= root * value
            out[k + 1] += value
        coeff = out
    return coeff


def shift(coeff, h):
    out = [F(0)] * len(coeff)
    for j, value in enumerate(coeff):
        for k in range(j + 1):
            out[k] += value * comb(j, k) * h**(j-k)
    return out


def derivative(coeff):
    return [k * coeff[k] for k in range(1, len(coeff))]


def check_family(n, q, expected_variance):
    m = n - 1
    need(sum(q) == m and min(q) >= F(1, 2), 'Reciprocal data failed')
    Q = roots_polynomial(q)
    # Recover U from e_k(q)=(k+1)*e_k(u).
    U = [value / (m + 1 - j) for j, value in enumerate(Q)]
    T = shift(U, F(1, 2))
    need(all(T[j] == 0 for j in range(m) if (m-j) % 2), 'Parity failed')
    # Check the characteristic-polynomial differential identity directly.
    deriv = derivative(U)
    relation = [(m + 1) * value for value in U]
    for k, value in enumerate(deriv):
        relation[k + 1] -= value
    need(relation == Q, 'Characteristic identity failed')
    translated = shift(Q, F(1, 2))
    e1, e2, e3 = -translated[m-1], translated[m-2], -translated[m-3]
    need(e1 == F(m, 2), 'First coefficient failed')
    need(e3 == F(m-2, 6)*e2, 'Saturation coefficient failed')
    variance = sum((r-1)**2 for r in q) / m
    need(variance == expected_variance, 'Variance failed')


def main():
    for n in range(4, 16):
        m = n - 1
        check_family(n, [F(1)] * m, F(0))
        check_family(n, [F(1, 2)] * (m-1) + [F(n, 2)], F(n-2, 4))

    # p=(z-1)*(z^2+8z/5+1), p'=3z^2+6z/5-3/5.
    # Its nonreal zeros lie on the unit circle since the real quadratic
    # has constant one and discriminant negative. Its two real critical
    # points lie in (-1,1), witnessed by signs and the vertex location.
    p = [F(-1), F(-3, 5), F(3, 5), F(1)]
    dp = derivative(p)
    need(dp == [F(-3, 5), F(6, 5), F(3)], 'Cubic derivative failed')
    discriminant = dp[1]**2 - 4*dp[2]*dp[0]
    need(discriminant == F(216, 25), 'Cubic discriminant failed')
    eval_dp = lambda x: dp[0] + dp[1]*x + dp[2]*x*x
    need(eval_dp(-1) > 0 and eval_dp(0) < 0 and eval_dp(1) > 0,
         'Cubic critical-root location failed')
    # Sum q=p''(1)/p'(1)=2; both q are positive.
    need(sum(derivative(dp)) / sum(dp) == 2, 'Cubic first-power sum failed')
    need(F(8, 5)**2 - 4 < 0, 'Cubic unit-circle factor failed')
    need(p != [F(-1), F(0), F(0), F(1)] and
         p != [F(-1), F(-1), F(1), F(1)], 'Cubic exception failed')
    print('PASS: 24 boundary equality family controls, degrees 4--15')
    print('PASS: coefficient parity, saturation identities, and variance')
    print('PASS: degree-three exception; degree-nine exceptional variance 7/4')


if __name__ == '__main__':
    main()
