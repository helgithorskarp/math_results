"""Exact coefficient certificates for the written unbounded inequalities."""
from fractions import Fraction as F
from math import comb
from variance import require


def add(*terms):
    out = {}
    for term in terms:
        for power, value in term.items():
            out[power] = out.get(power, F(0))+value
    return {p: v for p, v in out.items() if v}


def scale(a, value):
    return {p: v*value for p, v in a.items() if v*value}


def mul(a, b):
    out = {}
    for (i, j), x in a.items():
        for (r, s), y in b.items():
            power = (i+r, j+s)
            out[power] = out.get(power, F(0))+x*y
    return {p: v for p, v in out.items() if v}


ONE, Q, K = {(0, 0): F(1)}, {(1, 0): F(1)}, {(0, 1): F(1)}


def constant(v):
    return scale(ONE, F(v))


def twice_e(q=Q, k=K):
    return add(mul(q, q), mul(add(constant(13), scale(k, -6)), q),
               scale(mul(k, k), 2), scale(k, -10), constant(14))


def shift(coefficients, at):
    out = [F(0)]*len(coefficients)
    for j, value in enumerate(coefficients):
        for i in range(j+1):
            out[i] += value*comb(j, i)*at**(j-i)
    return out


def positive_shift(coefficients, at, expected):
    got = shift(coefficients, at)
    require(got == list(map(F, expected)) and all(x > 0 for x in got),
            'exact strictly positive translated polynomial certificate')
    return [str(x) for x in got]


def run():
    B = add(mul(Q, Q), mul(add(constant(7), scale(K, -6)), Q),
            scale(mul(K, K), 2), scale(K, -12), constant(8))
    root = add(twice_e(add(Q, constant(-5))),
               scale(add(scale(K, 16), constant(-17), scale(Q, -2)), -2))
    require(root == B, '2e(R-5)-2(16k-17-2R)=2B0(R) coefficient identity')
    DB = add(scale(mul(K, K), 28), scale(K, -36), constant(17))
    lower = add(DB, scale(mul(add(scale(K, 5), constant(-2)),
                             add(scale(K, 5), constant(-2))), -1))
    require(lower == mul(add(scale(K, 3), constant(-13)), add(K, constant(-1))),
            'strict lower square-root comparison identity')
    upper = add(scale(mul(add(scale(K, 16), constant(-10)),
                         add(scale(K, 16), constant(-10))), F(1, 9)), scale(DB, -1))
    require(upper == scale(add(scale(mul(K, K), 4), scale(K, 4), constant(-53)), F(1, 9)),
            'strict upper square-root comparison identity')
    large = positive_shift([-480, -4224, -18655, 1600], 19,
                           [4159209, 1019686, 72545, 1600])
    require(twice_e(scale(K, 6)) == add(scale(mul(K, K), 2), scale(K, 68), constant(14)),
            'e(6k)=k^2+34k+7, all-q tail base')
    require(F(23, 20)-F(352, 625)-F(8, 625) == F(287, 500) > 0,
            'uniform k>=5,q>=6k tail residual')
    # Polynomial variables now represent u,p in the credited Pell family.
    u, p = Q, K
    qstar = add(scale(u, 3), p, constant(-5))
    kp = add(u, ONE)
    norm = add(mul(p, p), scale(mul(u, u), -7), constant(-1))
    require(add(twice_e(qstar, kp), scale(add(scale(u, 15), scale(p, -3), constant(-3)), -1)) == norm,
            'exact Pell e identity')
    nextp, nextu = add(scale(p, 8), scale(u, 21)), add(scale(p, 3), scale(u, 8))
    require(add(mul(nextp, nextp), scale(mul(nextu, nextu), -7), constant(-1)) == norm,
            'exact Pell recurrence preserves norm')
    pell = positive_shift([-3200, -30336, -126125, 2750], 49,
                          [19218961, 7417664, 278125, 2750])
    require(F(21, 8)**2 < 7 and F(8, 3)**2 > 7+F(1, 48**2),
            'Pell rational slope brackets for all u>=48')
    return {'root_shift_coefficients': [[list(p), str(v)] for p, v in sorted(root.items())],
            'all_k19_shifted_positive_cubic': large,
            'tail_residual': '287/500',
            'Pell_shifted_positive_cubic': pell,
            'Pell_e_and_recurrence_identities': True,
            'coverage': 'Exact sparse coefficient equalities; ordinary inequality bridges in PROOF.md'}
