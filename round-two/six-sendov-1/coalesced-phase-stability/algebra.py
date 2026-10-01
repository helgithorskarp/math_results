"""Exact algebra for the coalesced7+1 local theorem (Python3.11, stdlib).

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


S = [-28, 28, 56, 70, 56, 28, 8, 1]
T = [-196, -392, -154, 280, 476, 328, 113, 16]
K = [7056, 65856, 286608, 751968, 1247652, 1105056, -399960,
     -3236816, -6293588, -8098272, -7933000, -6229360, -4018767,
     -2154056, -960824, -354200, -106260, -25300, -4600, -600, -50, -2]


def formula_checks(p):
    # Full rational identities after x=a/(1+a), not pointwise checks.
    require(to_a(p['2ell_c']) == scale(S, Q(4, 7)), 'complete slack polynomial')
    require(to_a(p['2ell_transverse']) == [0] + list(scale(T, Q(1, 56))),
            'complete transverse polynomial')
    determinant = add(mul(p['B_heavy'], add(p['B_diagonal'], scale(p['B_off'], 6))),
                      scale(power(p['B_cross'], 2), -7))
    # The determinant polynomial has a high power of ell. Compare directly
    # in the a representation, retaining the full degree for denominator30.
    expected = scale(mul([0, 0, 1], K), -Q(729, 448))
    require(to_a(determinant) == expected, 'complete modulus determinant polynomial')
    return determinant


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


def bound_checks(p):
    ell, mu = [Q(1), Q(-1)], Q(1, 1000)
    denominator = scale(power(ell, 8), 18)
    bh = add(p['B_heavy'], scale(denominator, -mu))
    bc = add(p['B_diagonal'], scale(p['B_off'], 6), scale(denominator, -mu))
    bounds = {
        'c_ge_half': add(p['2ell_c'], scale(ell, -1)),
        'H_le_one': add(ell, scale(p['ell_H'], -1)),
        'transverse_ge_1_1000': add(p['2ell_transverse'], scale(ell, -2*mu)),
        'heavy_ge_1_1000': bh,
        'shifted_collective_determinant': add(mul(bh, bc), scale(power(p['B_cross'], 2), -7)),
    }
    record = {}
    for name, poly in bounds.items():
        coefficients = bernstein(poly, Q(7, 15), Q(1, 2))
        require(all(c > 0 for c in coefficients), 'every complete Bernstein coefficient positive')
        record[name] = {'degree': len(poly)-1, 'power': list(map(str, poly)),
                        'bernstein': list(map(str, coefficients)),
                        'minimum': str(min(coefficients))}
    require(sum(len(r['bernstein']) for r in record.values()) == 72,
            '72 coefficient coverage')
    return record


def root_checks(lo, hi):
    require(Q(2, 3) < lo < hi < Q(7, 8), 'threshold ordered inside physical interval')
    require(value(T, lo) < 0 < value(T, hi), 'two exact threshold signs')
    # The written monotonicity proofs require these exact sign patterns.
    require(all(c < 0 for c in T[:3]) and all(c > 0 for c in T[3:]),
            'T/a^2 strictly increasing')
    require(all(c > 0 for c in K[:6]) and all(c < 0 for c in K[6:]),
            'K/a^5 strictly decreasing')
    require(all(c > 0 for c in S[1:]) and S[0] < 0, 'S strictly increasing')
    require(value(S, Q(1, 2)) > 0 and value(K, Q(2, 3)) < 0,
            'slack and collective positivity entry')
    return {'lo': str(lo), 'hi': str(hi), 'T_lo': str(value(T, lo)),
            'T_hi': str(value(T, hi)), 'S_half': str(value(S, Q(1, 2))),
            'K_two_thirds': str(value(K, Q(2, 3)))}


def reject(operation, message):
    try:
        operation()
    except ValueError:
        return message
    raise ValueError('negative control was accepted: '+message)


def regenerate():
    p = formulas()
    determinant = formula_checks(p)
    controls = polarization_checks(p)
    bounds = bound_checks(p)
    root = root_checks(Q(861212748918, 10**12), Q(861212748919, 10**12))
    # Separate damage controls hit actual mathematics rather than a digest.
    damages = []
    bad = dict(p); bad['2ell_c'] = add(p['2ell_c'], [1])
    damages.append(reject(lambda: formula_checks(bad), 'slack coefficient damage'))
    bad2 = dict(p); bad2['B_cross'] = add(p['B_cross'], [0, 1])
    damages.append(reject(lambda: polarization_checks(bad2), 'mixed-phase coefficient damage'))
    bad3 = dict(p); bad3['B_heavy'] = scale(p['B_heavy'], -1)
    damages.append(reject(lambda: bound_checks(bad3), 'matrix sign damage'))
    damages.append(reject(lambda: root_checks(Q(4, 5), Q(81, 100)), 'wrong threshold bracket'))
    b = bounds['shifted_collective_determinant']['bernstein']
    altered = list(map(Q, b)); altered[0] *= -1
    damages.append(reject(lambda: require(all(c > 0 for c in altered), 'damaged full coefficient sign'),
                          'Bernstein sign damage'))
    return {'status': 'PASS; exact algebra, ordinary written analytic proof',
            'polynomials': {k: list(map(str, v)) for k, v in p.items()},
            'modulus_determinant': list(map(str, determinant)),
            'a_polynomials': {'S': S, 'T': T, 'K': K}, 'threshold': root,
            'directional_identity_count': len(controls),
            'directional_identity_sha256': digest(controls),
            'bounds': bounds, 'bernstein_count': 72,
            'mathematical_damage_rejections': damages,
            'trust_boundary': 'No sampling proof, solver or external data. Neighborhood existence, applicability, equality and relaxed obstruction are the ordinary arguments in PROOF.md; no formal proof kernel or independent peer verdict.'}


def canonical(record):
    return json.dumps(record, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(record):
    return hashlib.sha256(canonical(record)).hexdigest()
