#!/usr/bin/env python3
"""Generate small exact Bernstein tables from the displayed polynomials.

The checker reconstructs the polynomials from these tables using a different
basis calculation and derives the adjacent-angle polynomial geometrically.
CPython >=3.11, standard library. No certificate is read by this generator.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
import json
import sys

import check as prior


def bernstein(poly, intervals):
    """Affine monomial substitution, followed by power-to-Bernstein conversion."""
    axes = list(intervals)
    degrees = [max(e[i] for e in poly.terms) for i in axes]
    mono = {}
    for e, coef in poly.terms.items():
        prior.need(not any(e[i] for i in range(prior.NV) if i not in axes),
                   'unexpected variable')
        ranges = [range(e[i] + 1) for i in axes]
        for powers in product(*ranges):
            val = coef
            for i, k in zip(axes, powers):
                lo, hi = intervals[i]
                val *= comb(e[i], k) * lo**(e[i] - k) * (hi - lo)**k
            mono[powers] = mono.get(powers, F(0)) + val
    out = {}
    for powers in product(*(range(n + 1) for n in degrees)):
        val = F(0)
        for exponents, coef in mono.items():
            if all(k <= j for k, j in zip(exponents, powers)):
                v = coef
                for k, j, n in zip(exponents, powers, degrees):
                    v *= F(comb(j, k), comb(n, k))
                val += v
        out[powers] = str(val)
    return degrees, out


def generate():
    c, z = prior.variable(0), prior.variable(4)
    H, D = 1 + 2*c, 1 + 2*c - c**2
    P = (H**2 * (1 - 4*c**2 - 2*c**3 - 3*c**4)
         + 2*(1-c)*D*H**2*z
         + H*(1 + 4*c - 14*c**3 - 9*c**4 + 2*c**5)*z**2
         + 2*c**2*(1-c)*D*H*z**3 - 2*c**4*(1+3*c)*z**4)
    J = -1-c+10*c**2+2*c**3-25*c**4+15*c**5
    degrees, table = bernstein(P, {0: (F(1, 2), F(3, 5)), 4: (F(1), F(3, 2))})
    prior.need(degrees == [6, 4], 'adjacent polynomial degrees')
    one_degree, one = bernstein(J, {0: (F(1, 2), F(3, 5))})
    prior.need(one_degree == [5], 'large-corner polynomial degree')
    result = {
        'schema': 1,
        'c_interval': ['1/2', '3/5'],
        'z_interval': ['1', '3/2'],
        'adjacent_P_degree': degrees,
        'adjacent_P_bernstein': [[table[(i, j)] for j in range(5)] for i in range(7)],
        'large_corner_J_degree': 5,
        'large_corner_J_bernstein': [one[(i,)] for i in range(6)],
    }
    prior.need(all(F(v) > 0 for row in result['adjacent_P_bernstein'] for v in row),
               'adjacent polynomial sign')
    prior.need(all(F(v) > 0 for v in result['large_corner_J_bernstein']),
               'large-corner polynomial sign')
    return result


if __name__ == '__main__':
    prior.need(not sys.argv[1:], 'usage: generate_one_five_certificate.py')
    print(json.dumps(generate(), indent=2, sort_keys=True))
