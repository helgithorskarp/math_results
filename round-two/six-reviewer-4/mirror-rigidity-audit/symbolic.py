"""Portable exact coefficient audit of the translated mirror mechanism.

Independent sparse integer-polynomial ring in 17 variables; characteristic zero.
The physical frame is m=e_z and E=z=0. Proper covariance gives every unit m.
All denominators are cleared explicitly; no CAS or researcher code is imported.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
VARIABLES = 'a b rx ry px py rho Cx Cy Bx By Kc vx vy nx ny k'.split()
DIM = len(VARIABLES)
ZERO = (0,)*DIM


def need(ok, why):
    if not ok:
        raise ValueError(why)


class P:
    def __init__(self, terms=0):
        if isinstance(terms, P):
            self.terms = terms.terms
        elif type(terms) is int:
            self.terms = {ZERO: terms} if terms else {}
        else:
            need(isinstance(terms, dict) and all(len(m) == DIM and
                 all(type(x) is int and x >= 0 for x in m) and type(c) is int
                 for m, c in terms.items()), 'literal integer polynomial data')
            self.terms = {m: c for m, c in terms.items() if c}

    def __add__(self, other):
        out = dict(self.terms)
        for m, c in P(other).terms.items():
            out[m] = out.get(m, 0)+c
        return P(out)
    __radd__ = __add__

    def __neg__(self):
        return P({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self+-P(other)

    def __rsub__(self, other):
        return P(other)+-self

    def __mul__(self, other):
        out = {}
        for a, c in self.terms.items():
            for b, d in P(other).terms.items():
                m = tuple(x+y for x, y in zip(a, b))
                out[m] = out.get(m, 0)+c*d
        return P(out)
    __rmul__ = __mul__

    def __pow__(self, exponent):
        need(type(exponent) is int and exponent >= 0, 'nonnegative integer exponent')
        out = P(1)
        for _ in range(exponent):
            out *= self
        return out

    def __eq__(self, other):
        return self.terms == P(other).terms

    def record(self):
        return [[list(m), c] for m, c in sorted(self.terms.items())]


def symbol(name):
    m = [0]*DIM
    m[VARIABLES.index(name)] = 1
    return P({tuple(m): 1})


def add(a, b):
    return [x+y for x, y in zip(a, b)]


def sub(a, b):
    return [x-y for x, y in zip(a, b)]


def scale(t, v):
    return [t*x for x in v]


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), P())


def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]


def skew(v):
    x, y, z = v
    return [[P(), -z, y], [z, P(), -x], [-y, x, P()]]


def eye():
    return [[P(i == j and 1 or 0) for j in range(3)] for i in range(3)]


def mscale(t, a):
    return [scale(t, row) for row in a]


def madd(a, b):
    return [add(x, y) for x, y in zip(a, b)]


def msub(a, b):
    return [sub(x, y) for x, y in zip(a, b)]


def mul(a, b):
    return [[dot(row, col) for col in zip(*b)] for row in a]


def matvec(a, v):
    return [dot(row, v) for row in a]


def outer(a, b):
    return [[x*y for y in b] for x in a]


def flatten(a):
    return [x for row in a for x in row]


def verify():
    a, b, rx, ry, px, py, rho, Cx, Cy, Bx, By, Kc, vx, vy, nx, ny, k = map(symbol, VARIABLES)
    z = P()
    m = [z, z, P(1)]
    r, p = [rx, ry, z], [px, py, z]
    w, u = add(p, scale(rho, m)), add(m, r)
    w0 = cross(m, r)
    C, v, n0 = [Cx, Cy, z], [vx, vy, z], [nx, ny, z]
    normal = add(sub(n0, scale(dot(n0, r), m)), scale(k, w0))
    row = dot(normal, add(add(cross(w, v), cross(w, cross(w, v))), C))
    moments = {
        (1, 0, 1, 0, 0): a, (1, 0, 0, 1, 0): b,
        (0, 1, 1, 0, 0): b, (0, 1, 0, 1, 0): 1-a,
        (1, 0, 0, 0, 1): Bx, (0, 1, 0, 0, 1): By,
        (0, 0, 0, 0, 1): Kc,
        (0, 0, 1, 0, 0): 0, (0, 0, 0, 1, 0): 0}
    weighted = P()
    for monomial, coefficient in row.terms.items():
        key = monomial[-5:]
        need(key in moments, 'every actual weighted row moment accounted for')
        base = monomial[:-5]+(0,)*5
        weighted += P({base: coefficient})*moments[key]
    S = [[a, b, z], [b, 1-a, z], [z, z, z]]
    projection = [[P(1), z, z], [z, P(1), z], [z, z, z]]
    A = msub(projection, S)
    B = [Bx, By, z]
    D = 1+dot(w0, p)
    tn = add(sub(w0, p), scale(rho, r))
    an = rho+dot(r, p)
    tnum = add(tn, scale(an, m))
    bracket = lambda x, y: dot(m, cross(x, y))
    # Published identity, with the known D denominator cancelled explicitly.
    bilinear = (dot(p, matvec(A, tn))-bracket(p, tn)*bracket(p, B)
                +rho*(dot(B, r)-dot(p, r)+bracket(p, r)*bracket(p, B))
                -rho*rho*(1+dot(w0, B))+Kc*dot(w0, C))
    differences = [weighted-bilinear]
    rn, wn = 1+dot(r, r), 1+dot(w, w)
    reflection_numerator = msub(mscale(rn, eye()), mscale(2, outer(u, u)))
    cayley_numerator = madd(mscale(wn, eye()),
                           madd(mscale(2, skew(w)), mscale(2, mul(skew(w), skew(w)))))
    differences += [D*D+dot(tnum, tnum)-rn*wn]
    mirror = [[P(1), z, z], [z, P(1), z], [z, z, P(-1)]]
    reflected = mul(mul(reflection_numerator, cayley_numerator), mirror)
    companion = madd(mscale(rn*wn, eye()),
                     madd(mscale(2*D, skew(tnum)), mscale(2, mul(skew(tnum), skew(tnum)))))
    differences += flatten(msub(reflected, companion))
    differences += [D+dot(w0, tn)-rn, an+dot(r, tn)-rho*rn]
    differences += sub(add(sub(scale(D, w0), tn), scale(an, r)), scale(rn, p))
    # Clear the exact translation-lift denominator before comparison.
    t_numerator = sub(scale(rn, C), scale(dot(u, C), u))
    differences += sub(sub(t_numerator, scale(t_numerator[2], u)), scale(rn, C))
    differences += flatten(msub(mul(skew(m), S), mul(A, skew(m))))
    need(all(x == 0 for x in differences), 'all exact coefficient identities')
    omission = weighted-(bilinear-Kc*dot(w0, C))
    need(omission != 0 and omission == Kc*dot(w0, C), 'actual translation omission detected')
    wrong_D = 1-dot(w0, p)
    wrong = madd(mscale(rn*wn, eye()),
                 madd(mscale(2*wrong_D, skew(tnum)), mscale(2, mul(skew(tnum), skew(tnum)))))
    need(any(x != 0 for x in flatten(msub(reflected, wrong))), 'wrong companion denominator detected')
    coefficient_record = [x.record() for x in [weighted, bilinear, tn[0], tn[1], an, D]]
    return {'actual_reviewer': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
            'domain': 'Integer coefficients in17 variables, interpreted in characteristic zero.',
            'implementation': 'Independent sparse integer polynomial v1, standard library only.',
            'zero_coefficient_identities': len(differences),
            'generic_common_row_moment_types': len(moments),
            'translation_omission_control': True, 'incorrect_companion_control': True,
            'coefficient_record_sha256': hashlib.sha256(
                json.dumps(coefficient_record, separators=(',', ':')).encode()).hexdigest(),
            'trust': 'Proper covariance and rechecked physical stresses supply the geometric interpretation.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit', action='store_true')
    args = parser.parse_args()
    result = verify()
    if args.emit:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        need(result == json.loads((HERE/'symbolic-expected.json').read_text()), 'complete symbolic expected record')
        print('PASS')
