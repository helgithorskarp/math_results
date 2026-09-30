#!/usr/bin/env python3
"""Exact author certificate for the full symmetric degree-nine angular cube.

Author six-sendov-2, researcher. Standard-library rational algebra only.
Sparse polynomial/commutant methods openly adapt the author's predecessor
checkers. No campaign module, external CAS, floating input or solver.
Analytic coverage and the all-real basin bridge are written in PROOF.md.
"""
from fractions import Fraction as F
from itertools import product, combinations, combinations_with_replacement
from math import comb
from pathlib import Path
import argparse
import hashlib
import json


CHECKS = 0


def require(ok, message):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(message)


class P:
    """Sparse exact Q[x0,x1,x2]; exponent order is explicit and fixed."""
    def __init__(self, value=0):
        if isinstance(value, P):
            value = value.t
        if isinstance(value, (int, F)):
            value = {(0, 0, 0): F(value)}
        self.t = {tuple(e): F(c) for e, c in value.items() if c}
        if any(len(e) != 3 or any(k < 0 for k in e) for e in self.t):
            raise ValueError('invalid polynomial exponent')

    def __add__(self, other):
        out = dict(self.t)
        for e, c in P(other).t.items():
            out[e] = out.get(e, F(0)) + c
        return P(out)

    __radd__ = __add__

    def __neg__(self):
        return P({e: -c for e, c in self.t.items()})

    def __sub__(self, other):
        return self + -P(other)

    def __rsub__(self, other):
        return P(other) + -self

    def __mul__(self, other):
        out = {}
        for e, c in self.t.items():
            for h, b in P(other).t.items():
                k = tuple(x+y for x, y in zip(e, h))
                out[k] = out.get(k, F(0)) + c*b
        return P(out)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * (1/F(scalar))

    def __pow__(self, n):
        if n < 0:
            raise ValueError('negative polynomial power')
        out, a = P(1), self
        while n:
            if n & 1:
                out *= a
            a *= a
            n //= 2
        return out

    def __eq__(self, other):
        return self.t == P(other).t

    def dump(self):
        return [[*e, str(c)] for e, c in sorted(self.t.items())]


X, H, U = [P({tuple(int(i == j) for j in range(3)): 1}) for i in range(3)]


def subst(poly, variables):
    powers = []
    for axis, v in enumerate(variables):
        degree = max((e[axis] for e in poly.t), default=0)
        row = [P(1)]
        for _ in range(degree):
            row.append(row[-1]*P(v))
        powers.append(row)
    out = P(0)
    for e, c in poly.t.items():
        term = P(c)
        for axis, k in enumerate(e):
            term *= powers[axis][k]
        out += term
    return out


def scalar(poly, values):
    out = subst(poly, values)
    require(not any(any(e) for e in out.t), 'evaluation is scalar')
    return out.t.get((0, 0, 0), F(0))


def derivative(poly, axis):
    return P({tuple(k-1 if i == axis else k for i, k in enumerate(e)):
              e[axis]*c for e, c in poly.t.items() if e[axis]})


def remove_monomial(poly, axis, power, name):
    require(all(e[axis] >= power for e in poly.t), name+' divisibility')
    reduced = P({tuple(k-power if i == axis else k for i, k in enumerate(e)):
                 c for e, c in poly.t.items()})
    variable = (X, H, U)[axis]
    require(reduced*variable**power == poly, name+' reconstruction')
    return reduced


def cleared(squares):
    """Credited generic cubic formula, evaluated as exact polynomials."""
    es = [sum((prod(squares[i] for i in ii)
               for ii in combinations(range(4), k)), P(0))
          for k in range(1, 5)]
    a, b, c, d = es
    disc = 36*a*a*b*b-128*b**3-108*a**3*c-432*c*c+432*a*b*c
    aa = (128*b**4-480*a*b*b*c+180*a*a*c*c-64*a*a*b**3+
          204*a**3*b*c+9*a**4*b*b-27*a**5*c)
    bb = 3072*b*b-768*a*a*b-2304*a*c
    cc = (-64512*c*c-24576*b**3+70656*a*b*c+
          6912*a*a*b*b-17280*a**3*c)
    v = (c*c*aa+c*c*d*bb+d*d*cc)/8
    w = c*c*disc
    return (936*a*a-896*b)*w-5760*v, 2*a*w, v, w


def prod(values):
    out = P(1)
    for v in values:
        out *= v
    return out


def affine_power(poly, box):
    """Binomial affine substitution performed one axis at a time."""
    data = dict(poly.t)
    for axis, (a, b) in enumerate(box):
        out = {}
        for e, c in data.items():
            for k in range(e[axis]+1):
                h = tuple(k if i == axis else v for i, v in enumerate(e))
                out[h] = out.get(h, F(0)) + c*comb(e[axis], k)*a**(e[axis]-k)*(b-a)**k
        data = {e: c for e, c in out.items() if c}
    return data


def bernstein(poly, box):
    degrees = tuple(max((e[i] for e in poly.t), default=0) for i in range(3))
    normalized = affine_power(poly, box)
    data = dict(normalized)
    for axis, degree in enumerate(degrees):
        out = {}
        for e, c in data.items():
            for k in range(e[axis], degree+1):
                h = tuple(k if i == axis else v for i, v in enumerate(e))
                out[h] = out.get(h, F(0)) + c*F(comb(k, e[axis]), comb(degree, e[axis]))
        data = {e: c for e, c in out.items() if c}
    indices = list(product(*(range(n+1) for n in degrees)))
    coefficients = [data.get(e, F(0)) for e in indices]
    # Independent inverse basis identity in the normalized power coordinates.
    inverse = dict(data)
    for axis, degree in enumerate(degrees):
        out = {}
        for e, c in inverse.items():
            for k in range(e[axis], degree+1):
                h = tuple(k if i == axis else v for i, v in enumerate(e))
                out[h] = out.get(h, F(0)) + c*comb(degree, k)*comb(k, e[axis])*(-1)**(k-e[axis])
        inverse = {e: c for e, c in out.items() if c}
    require(inverse == normalized, 'complete inverse Bernstein reconstruction')
    return coefficients, degrees


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def certificate(name, poly, box, strict=False):
    require(len(box) == 3 and all(a < b for a, b in box), name+' genuine box')
    coefficients, degrees = bernstein(poly, box)
    for value in coefficients:
        require(value > 0 if strict else value >= 0, name+' Bernstein sign')
    return {'name': name, 'box': [[str(a), str(b)] for a, b in box],
            'degrees': list(degrees), 'entries': len(coefficients),
            'zero': sum(c == 0 for c in coefficients), 'minimum': str(min(coefficients)),
            'polynomial_sha256': digest(poly.dump()),
            'coefficient_sha256': digest(list(map(str, coefficients)))}


def solve(a, b):
    n = len(b)
    a = [list(r)+[v] for r, v in zip(a, b)]
    for j in range(n):
        pivots = [i for i in range(j, n) if a[i][j]]
        require(bool(pivots), 'nonzero Gaussian pivot')
        i = pivots[0]
        a[j], a[i] = a[i], a[j]
        t = a[j][j]
        a[j] = [v/t for v in a[j]]
        for i in range(j+1, n):
            t = a[i][j]
            if t:
                a[i] = [u-t*v for u, v in zip(a[i], a[j])]
    out = [F(0)]*n
    for j in range(n-1, -1, -1):
        out[j] = a[j][-1]-sum(a[j][k]*out[k] for k in range(j+1, n))
    return out


def independent_rows(rows):
    pivots, selected = {}, []
    for original in rows:
        r = list(original)
        for j, b in sorted(pivots.items()):
            t = r[j]
            if t:
                r = [u-t*v for u, v in zip(r, b)]
        if any(r):
            j = next(j for j, v in enumerate(r) if v)
            t = r[j]
            pivots[j] = [v/t for v in r]
            selected.append(original)
    return selected


def pinching(theta):
    """Rational Frobenius projection of ww* to the symmetric commutant."""
    n = 8
    require(len(theta) == n and sum(theta) == 0, 'balanced definition control')
    a = [[(theta[i] if i == j else 0)-(theta[i]+theta[j])/n
          for j in range(n)] for i in range(n)]
    pairs = list(combinations_with_replacement(range(n), 2))
    weights = [F(1 if i == j else 2) for i, j in pairs]
    w = [theta[i]*theta[j]/n for i, j in pairs]
    all_rows = []
    for i in range(n):
        for j in range(i+1, n):
            row = []
            for h, k in pairs:
                v = (a[i][h] if k == j else 0)-(a[k][j] if i == h else 0)
                if h != k:
                    v += (a[i][k] if h == j else 0)-(a[h][j] if i == k else 0)
                row.append(v)
            all_rows.append(row)
    rows = independent_rows(all_rows)
    rhs = [sum(c*v for c, v in zip(row, w)) for row in rows]
    gram = [[sum(c*d/g for c, d, g in zip(row, other, weights))
             for other in rows] for row in rows]
    lam = solve(gram, rhs)
    projected = [v-sum(row[k]*b for row, b in zip(rows, lam))/weights[k]
                 for k, v in enumerate(w)]
    for row in all_rows:
        require(sum(c*v for c, v in zip(row, projected)) == 0,
                'original commutation constraint')
    residual = [u-v for u, v in zip(w, projected)]
    require(sum(g*u*v for g, u, v in zip(weights, projected, residual)) == 0,
            'Frobenius orthogonality')
    return sum(g*v*v for g, v in zip(weights, projected)), len(rows)


def interval_add(a, b):
    return a[0]+b[0], a[1]+b[1]


def interval_mul(a, b):
    values = [x*y for x in a for y in b]
    return min(values), max(values)


def interval_poly(coefficients, box):
    out = F(0), F(0)
    for c in reversed(coefficients):
        out = interval_add(interval_mul(out, box), (F(c), F(c)))
    return out


def build():
    records = []
    # First region: X<=3/4, two complete positive-gap charts.
    for which, y, u in [(0, X+(1-X)*H, X*(1-H*U)),
                        (1, X+(1-X)*H*U, X*(1-H))]:
        n, d, _, _ = cleared([P(1), y, X, u])
        poly = remove_monomial(remove_monomial(780*d-n, 0, 2, 'low x'), 1, 2, 'low h')
        if which == 0:
            boxes = [(F(0), F(3,8), F(0), F(1,2), F(0), F(1)),
                     (F(0), F(3,8), F(1,2), F(1), F(0), F(1)),
                     (F(3,8), F(3,4), F(0), F(1,2), F(0), F(1))]
            for a, b in [(F(3,8), F(9,16)), (F(9,16), F(3,4))]:
                boxes.append((a, b, F(1,2), F(3,4), F(0), F(1)))
                for c, e in [(F(0), F(1,2)), (F(1,2), F(1))]:
                    boxes.append((a, b, F(3,4), F(1), c, e))
        else:
            boxes = [(a, b, c, e, F(0), F(1))
                     for a, b in [(F(0), F(3,8)), (F(3,8), F(3,4))]
                     for c, e in [(F(0), F(1,2)), (F(1,2), F(1))]]
        for i, box in enumerate(boxes):
            records.append(certificate(f'low{which}_{i}', poly,
                                        [(box[j], box[j+1]) for j in (0, 2, 4)]))
    # Second region: u>=1/4; common displacement scaling and corner blow-up.
    y, x, u = 1-X*H*U, 1-X*H, 1-X
    n, d, _, _ = cleared([P(1), y, x, u])
    high = remove_monomial(remove_monomial(780*d-n, 0, 6, 'high scale'), 1, 2, 'high x')
    for which, vx, vs in [(0, 1-H, 1-H*U), (1, 1-H*U, 1-H)]:
        poly = remove_monomial(subst(high, [X, vx, vs]), 1, 2, 'high corner')
        records.append(certificate(f'high{which}', poly,
                                    [(F(0), F(3,4)), (F(0), F(1)), (F(0), F(1))], True))
    # Third region: X>=3/4,u<=1/4; compare to the entire scalar curve.
    n, d, _, _ = cleared([P(1), 1-X*H, 1-X, U])
    n2 = remove_monomial(n, 0, 2, 'cap numerator')
    d2 = remove_monomial(d, 0, 2, 'cap denominator')
    jn = 2058+21912*U-15876*U**2+19224*U**3+3402*U**4
    jd = (3+U)*(1+3*U)**2
    gap = remove_monomial(jn*d2-jd*n2, 0, 1, 'cap gap')
    cap = certificate('cap', gap, [(F(0), F(1,4)), (F(0), F(1)), (F(0), F(1,4))], True)
    records.append(cap)
    require(F(cap['minimum']) == F(34642049301,1146880), 'cap minimum')
    require(subst(jn*d2-jd*n2, [0, H, U]) == 0, 'whole scalar curve recovered at cap collapse')
    require(F(34642049301,1146880) > F(405769,16), 'metric cap gap constant')
    require(2*F(13,4)*F(7,4)**2*256 == 5096, 'interlacing denominator bound')
    require(F(637,64)*5096 == F(405769,8), 'full scalar denominator bound')
    # Credited scalar optimizer checks; these are reproduction, not new priority.
    t = derivative(jn, 2)*jd-jn*derivative(jd, 2)
    tc = [26634, -231084, -907290, 376920, 971190, 224532, 30618]
    require(t == sum((c*U**i for i, c in enumerate(tc)), P(0)), 'credited scalar derivative')
    loss = -(derivative(t, 2)+90000)
    records.append(certificate('scalar_derivative_loss', loss,
                               [(F(0), F(1)), (F(0), F(1)), (F(0), F(1,4))], True))
    require(F(637,64) < 10 and 90000/F(10)**2 == 900, 'scalar quadratic loss constants')
    require(scalar(jn, [0, 0, F(1,9)])/scalar(jd, [0, 0, F(1,9)]) == F(5472,7), 'known rational competitor')
    require(F(5472,7)-780 == F(12,7), 'losing-region gap')
    require(F(32,5)*F(12,7) > 4, 'global normalized distance bound')
    require(F(13,8)**4/F(10985,33554432) == F(106496,5), 'basin scale identity')
    lo, hi = F(2,25), F(9,100)
    require(scalar(t, [0,0,lo]) > 0 and scalar(t, [0,0,hi]) < 0, 'scalar optimizer initial bracket')
    for _ in range(40):
        mid = (lo+hi)/2
        value = scalar(t, [0,0,mid])
        if value > 0:
            lo = mid
        else:
            hi = mid
    require(scalar(t, [0,0,lo]) > 0 and scalar(t, [0,0,hi]) < 0, 'scalar optimizer final bracket')
    ni = interval_poly([2058,21912,-15876,19224,3402], (lo,hi))
    di = interval_poly([3,19,33,9], (lo,hi))
    require(ni[0] > 0 and di[0] > 0, 'positive basin interval division')
    basin = F(106496,5)*di[0]/ni[1], F(106496,5)*di[1]/ni[0]
    require(F('27.106707') < basin[0] < basin[1] < F('27.106708'), 'credited sharp basin interval')
    # Actual grouped spectral values, with both generic and singular faces.
    controls = []
    for slopes in [(F(1),F(3,4),F(1,2),F(1,4)),
                   (F(1),F(2,3),F(1,3),F(0)),
                   (F(1),F(1),F(1,2),F(1,4)),
                   (F(1),F(1,2),F(1,2),F(1,3)),
                   (F(1),F(1,2),F(1,2),F(1,2)),
                   (F(1),F(1),F(1),F(1,3)),
                   (F(1),F(1),F(1),F(1)),
                   (F(1),F(0),F(0),F(0)),
                   (F(1),F(1),F(0),F(0))]:
        theta = list(slopes)+[-v for v in slopes]
        psi, rank = pinching(theta)
        n, d, v, w = cleared([P(s*s) for s in slopes])
        vv, ww = scalar(v,[0,0,0]), scalar(w,[0,0,0])
        alpha = sum(s*s for s in theta)
        fourth = sum(s**4 for s in theta)
        j = (122*alpha*alpha+224*fourth-5760*psi)/alpha
        if ww:
            require(ww > 0 and vv/ww == psi, 'generic oracle versus grouped definition')
            require(scalar(n,[0,0,0])/scalar(d,[0,0,0]) == j, 'generic J versus definition')
        else:
            require(ww == 0 and vv == 0, 'singular generic expression is never divided')
        if slopes == (F(1),F(1),F(1),F(1,3)):
            require(j == F(5472,7) and psi == F(17,81), 'three-unit-pair rational profile')
        if slopes == (F(1),F(1),F(1),F(1)):
            require(j == 480 and psi == 1, 'all-unit collision value')
        if slopes == (F(1),F(0),F(0),F(0)):
            require(j == 378 and psi == F(1,32), 'single-nonzero-pair collision value')
        controls.append({'slopes':list(map(str,slopes)), 'Psi':str(psi), 'J':str(j), 'commutant_rank':rank, 'generic':bool(ww)})
    total = sum(r['entries'] for r in records)
    require(total == 20787, 'complete coefficient count including scalar reproduction')
    return {'agent':'six-sendov-2','role':'researcher','status':'exact author certificate; analytic premises stated in PROOF.md; independent review pending',
            'checks':CHECKS, 'Bernstein_coefficients':total, 'cube_coefficients':20781,
            'certificates':records, 'coefficient_manifest_sha256':digest(records),
            'controls':controls, 'optimizer_interval':[str(lo),str(hi)], 'basin_interval':list(map(str,basin))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-expected',type=Path)
    args = parser.parse_args()
    actual = build()
    if args.write_expected:
        args.write_expected.write_text(json.dumps(actual,indent=2)+'\n')
    else:
        expected = json.loads(args.expected.read_text())
        if expected != actual:
            raise ValueError('complete expected manifest mismatch')
    print(json.dumps({'agent':actual['agent'],'role':actual['role'],
                      'checks':actual['checks'],'cube_coefficients':actual['cube_coefficients'],
                      'Bernstein_coefficients':actual['Bernstein_coefficients'],
                      'certificate_boxes':len(actual['certificates'])-1,
                      'definition_controls':len(actual['controls']),
                      'coefficient_manifest_sha256':actual['coefficient_manifest_sha256'],
                      'manifest_match':not bool(args.write_expected)},indent=2))


if __name__ == '__main__':
    main()
