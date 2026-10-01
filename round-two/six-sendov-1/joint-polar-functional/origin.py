"""Standalone origin-module algebra, reused from the author's9039 source.
Seed commit ce52e8ead180f28eee7b52b248e03f3077a5837b; not an external import.
Only polynomial helpers, full origin derivatives and literal jets are retained.

Two routes: integrated derivative formulas, and literal Gaussian Taylor
factor products. These verify full polynomials, not an interpolation grid.
The analytic neighborhood/equality arguments are in PROOF.md.
"""
from fractions import Fraction as Q
from math import comb
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trim(p):
    p = list(map(Q, p))
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(*ps):
    out = [Q(0)] * max(map(len, ps))
    for p in ps:
        for k, c in enumerate(p):
            out[k] += c
    return trim(out)


def scale(p, c):
    return trim([c * x for x in p])


def mul(*ps):
    out = [Q(1)]
    for p in ps:
        nxt = [Q(0)] * (len(out) + len(p) - 1)
        for i, a in enumerate(out):
            for j, b in enumerate(p):
                nxt[i + j] += a * b
        out = trim(nxt)
    return out


def power(p, n):
    return mul(*([p] * n))


def value(p, x):
    out = Q(0)
    for c in reversed(p):
        out = out * x + c
    return out


def integral(k, n):
    return [Q((-1)**j * comb(n, j), k + j + 1) for j in range(n + 1)]


def to_a(p):
    """(1+a)^degree p(a/(1+a)), with its exact degree retained."""
    n = len(p) - 1
    return add(*(scale(mul(power([0, 1], k), power([1, 1], n-k)), c)
                 for k, c in enumerate(p)))


def compose_interval(p, lo, hi):
    n = len(p) - 1
    return trim([sum(p[j] * comb(j, k) * lo**(j-k) * (hi-lo)**k
                     for j in range(k, n+1)) for k in range(n+1)])


def bernstein(p, lo, hi):
    n = len(p) - 1
    pw = compose_interval(p, lo, hi)
    b = [sum(pw[k] * Q(comb(i, k), comb(n, k))
             for k in range(min(i+1, len(pw)))) for i in range(n+1)]
    reverse = [Q(0)] * (n+1)
    for i, c in enumerate(b):
        for j in range(n-i+1):
            reverse[i+j] += c * comb(n, i) * comb(n-i, j) * (-1)**j
    require(trim(reverse) == pw, 'complete reverse Bernstein identity')
    return b


def gaussian_mul(z, w):
    return add(mul(z[0], w[0]), scale(mul(z[1], w[1]), -1)), \
        add(mul(z[0], w[1]), mul(z[1], w[0]))


def jet_mul(p, q, ell):
    """Keys(epsilon degree,t degree). Degree2 stores ell times its value.

    A product of two linear coefficients therefore needs one extra ell.
    This avoids rational functions without changing their exact values.
    """
    out = {}
    for (e, k), z in p.items():
        for (f, l), w in q.items():
            if e+f > 2:
                continue
            result = gaussian_mul(z, w)
            if e == f == 1:
                result = tuple(mul(v, ell) for v in result)
            key = (e+f, k+l)
            old = out.get(key, ([Q(0)], [Q(0)]))
            out[key] = tuple(add(a, b) for a, b in zip(old, result))
    return out


def literal_phase(direction):
    x, ell = [Q(0), Q(1)], [Q(1), Q(-1)]
    gammas = [9] + [1]*7
    radii = [scale(ell, g) for g in gammas]
    radial2 = [scale(x, -Q(sum(v*v for v in direction[1:]), 2))]
    radial2 += [scale(x, Q(v*v, 2)) for v in direction[1:]]
    origin = {(0, 0): ([Q(1)], [Q(0)])}
    for g, r, second, v in zip(gammas, radii, radial2, direction):
        q2 = add(second, scale(r, -Q(v*v, 2)))
        factor = {(0, 0): ([Q(1)], [Q(0)]),
                  (0, 1): (scale(x, -g), [Q(0)]),
                  (1, 1): ([Q(0)], scale(x, -g*v)),
                  (2, 1): (scale(mul(x, q2), -1), [Q(0)])}
        origin = jet_mul(origin, factor, ell)
    re0 = add(*(scale(z[0], Q(9, k+1))
                for (e, k), z in origin.items() if e == 0))
    im1 = add(*(scale(z[1], Q(9, k+1))
                for (e, k), z in origin.items() if e == 1))
    re2_ell = add(*(scale(z[0], Q(9, k+1))
                    for (e, k), z in origin.items() if e == 2))
    require(re0 == mul(*radii), 'complete coalesced origin equality')
    product2 = add(*(mul(radial2[j], *(radii[k] for k in range(8) if k != j))
                     for j in range(8)))
    # 18ell^8 times the epsilon^2 coefficient of |O|-prod.
    return add(scale(mul(power(ell, 7), re2_ell), 18),
               scale(mul(power(ell, 8), product2), -18), power(im1, 2))


def formulas():
    x, ell = [Q(0), Q(1)], [Q(1), Q(-1)]
    i1, i2, i3 = integral(1, 7), integral(2, 6), integral(3, 5)
    js = add(i1, scale(mul(x, i2), -8))
    jss = add(i2, scale(mul(x, i3), -8))
    h = add(scale(mul(x, i1), 9), power(ell, 8))
    c = add(scale(mul(power(x, 2), i2), 144), scale(power(ell, 8), -16))
    heavy = scale(mul(x, ell, i1), 81)
    cross = scale(mul(power(x, 2), ell, i2), -81)
    off = scale(mul(power(x, 2), ell, jss), -9)
    diagonal = add(scale(mul(x, ell, js), 9),
                   scale(mul(power(x, 3), i2), 72),
                   scale(mul(x, power(ell, 8)), -8))
    transverse = add(diagonal, scale(off, -1))
    wh, ws = scale(mul(x, i1), -81), scale(mul(x, js), -9)
    bh = add(scale(mul(power(ell, 7), heavy), 9), power(wh, 2))
    bd = add(scale(mul(power(ell, 7), diagonal), 9), power(ws, 2))
    bx = add(scale(mul(power(ell, 7), cross), 9), mul(wh, ws))
    bo = add(scale(mul(power(ell, 7), off), 9), power(ws, 2))
    return {'ell_H': h, '2ell_c': c, '2ell_transverse': transverse,
            'B_heavy': bh, 'B_diagonal': bd, 'B_cross': bx, 'B_off': bo}



def polarization_checks(p):
    basis = [[int(i == j) for j in range(8)] for i in range(8)]
    directions = list(basis)
    for i in range(8):
        for j in range(i+1, 8):
            directions += [[basis[i][k] + sign*basis[j][k] for k in range(8)]
                           for sign in (1, -1)]
    controls = []
    for v in directions:
        expected = [Q(0)]
        for i in range(8):
            for j in range(8):
                name = 'B_heavy' if i == j == 0 else 'B_diagonal' if i == j \
                    else 'B_cross' if i == 0 or j == 0 else 'B_off'
                expected = add(expected, scale(p[name], v[i]*v[j]))
        direct = literal_phase(v)
        require(direct == expected, 'complete literal Gaussian polarization identity')
        controls.append({'direction': v, 'coefficients': list(map(str, direct))})
    require(len(controls) == 64, '64 full coordinate/pair controls')
    return controls


def canonical(record):
    return json.dumps(record, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(record):
    return hashlib.sha256(canonical(record)).hexdigest()
