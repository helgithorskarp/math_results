#!/usr/bin/env python3
"""Explicit simple three-polytopes of odd denominator; standard library."""
from itertools import product
from functools import reduce
from math import gcd, lcm


def construct(q):
    if type(q) is not int or q < 3 or q % 2 == 0:
        raise ValueError('q must be an odd integer at least three')
    side, r = 2 * q, (q + 1) // 2
    character, offset = (1, 1, -2), (1, 0, 0)
    basis = ((1, 0, 0), (0, 1, 0), (r, r, q))
    facets_u = []
    for i in range(3):
        row = [0] * 3
        row[i] = -1
        facets_u.append((tuple(row), -offset[i]))
        row[i] = 1
        facets_u.append((tuple(row), offset[i] + side))
    cuts = []
    for bits in product((0, 1), repeat=3):
        if len(set(bits)) == 1:
            continue
        signs = tuple(1 - 2 * b for b in bits)
        steps = tuple((-pow(signs[i] * character[i], -1, q)) % q for i in range(3))
        scale = lcm(*steps)
        corner = tuple(offset[i] + side * bits[i] for i in range(3))
        row = tuple(-signs[i] * (scale // steps[i]) for i in range(3))
        rhs = sum(row[i] * corner[i] for i in range(3)) - scale
        facets_u.append((row, rhs))
        cuts.append({'bits': bits, 'signs': signs, 'steps': steps, 'corner': corner})
    facets_x = []
    for row, rhs in facets_u:
        normal = tuple(sum(row[i] * basis[i][j] for i in range(3)) for j in range(3))
        content = reduce(gcd, map(abs, normal))
        if content == 0 or rhs % content:
            raise ValueError('facet is not at integral primitive lattice height')
        facets_x.append((tuple(x // content for x in normal), rhs // content))
    return {'q': q, 'side': side, 'basis': basis, 'facets': facets_x,
            'facets_u': facets_u, 'cuts': cuts}
