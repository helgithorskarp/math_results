#!/usr/bin/env python3
"""Exact diameter certificate; Python 3.11+ standard library only.

Q(phi), phi^2=phi+1; rational intervals never use float for a decision.
The finite witness consists of nonnegative integer weighted halfspaces.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import isqrt
from pathlib import Path
import hashlib
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


@dataclass(frozen=True)
class Q:
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, 'a', F(self.a))
        object.__setattr__(self, 'b', F(self.b))

    @staticmethod
    def coerce(v):
        return v if isinstance(v, Q) else Q(F(v))

    def __add__(self, other):
        o = Q.coerce(other)
        return Q(self.a+o.a, self.b+o.b)

    __radd__ = __add__

    def __neg__(self):
        return Q(-self.a, -self.b)

    def __sub__(self, other):
        return self+-Q.coerce(other)

    def __rsub__(self, other):
        return Q.coerce(other)+-self

    def __mul__(self, other):
        o = Q.coerce(other)
        return Q(self.a*o.a+self.b*o.b,
                 self.a*o.b+self.b*o.a+self.b*o.b)

    __rmul__ = __mul__

    def inv(self):
        norm = self.a*self.a+self.a*self.b-self.b*self.b
        require(norm != 0, 'division by zero in Q(phi)')
        return Q((self.a+self.b)/norm, -self.b/norm)

    def __truediv__(self, other):
        return self*Q.coerce(other).inv()

    def __rtruediv__(self, other):
        return Q.coerce(other)*self.inv()

    def sign(self):
        # Twice this number is A+B sqrt(5). Exact sign by squaring
        # only when the two summands have opposite signs.
        A, B = 2*self.a+self.b, self.b
        if B == 0:
            return (A > 0)-(A < 0)
        if A == 0:
            return (B > 0)-(B < 0)
        if A > 0 and B > 0:
            return 1
        if A < 0 and B < 0:
            return -1
        delta = A*A-5*B*B
        require(delta != 0, 'nonzero rational square equals 5 times a square')
        return ((delta > 0)-(delta < 0))*((A > 0)-(A < 0))


Z, ONE, PHI = Q(), Q(1), Q(0, 1)
H = PHI+2
N = (ONE, Z, PHI)


@dataclass(frozen=True)
class I:
    lo: F
    hi: F

    def __post_init__(self):
        object.__setattr__(self, 'lo', F(self.lo))
        object.__setattr__(self, 'hi', F(self.hi))
        require(self.lo <= self.hi, 'reversed interval')

    @staticmethod
    def coerce(x):
        return x if isinstance(x, I) else I(F(x), F(x))

    def __add__(self, other):
        o = I.coerce(other)
        return I(self.lo+o.lo, self.hi+o.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self+-I.coerce(other)

    def __rsub__(self, other):
        return I.coerce(other)+-self

    def __mul__(self, other):
        o = I.coerce(other)
        v = (self.lo*o.lo, self.lo*o.hi, self.hi*o.lo, self.hi*o.hi)
        return I(min(v), max(v))

    __rmul__ = __mul__

    def inv(self):
        require(not self.lo <= 0 <= self.hi, 'interval division contains zero')
        return I(1/self.hi, 1/self.lo)

    def __truediv__(self, other):
        return self*I.coerce(other).inv()

    def __rtruediv__(self, other):
        return I.coerce(other)*self.inv()

    def sqrt(self, digits=35):
        require(self.lo >= 0, 'negative square root')
        scale = 10**digits
        low = isqrt(self.lo.numerator*scale*scale//self.lo.denominator)
        high = isqrt(self.hi.numerator*scale*scale//self.hi.denominator)+1
        return I(F(low, scale), F(high, scale))

    def square(self):
        if self.lo >= 0:
            return I(self.lo*self.lo, self.hi*self.hi)
        if self.hi <= 0:
            return I(self.hi*self.hi, self.lo*self.lo)
        return I(0, max(self.lo*self.lo, self.hi*self.hi))


P = (I(5, 5).sqrt()+1)/2


def qi(q):
    q = Q.coerce(q)
    return q.a+q.b*P


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), Z)


def mv(M, v):
    return tuple(dot(row, v) for row in M)


def mm(A, B):
    return tuple(tuple(dot(row, col) for col in zip(*B)) for row in A)


ID = ((ONE, Z, Z), (Z, ONE, Z), (Z, Z, ONE))
CROSS = ((Z, -PHI, Z), (PHI, Z, -ONE), (Z, ONE, Z))
G = tuple(tuple((PHI-1)/2*ID[i][j]+(2-PHI)/2*N[i]*N[j]
                +CROSS[i][j]/2 for j in range(3)) for i in range(3))
T = ((-ONE, Z, Z), (Z, -ONE, Z), (Z, Z, ONE))
TY = ((-ONE, Z, Z), (Z, ONE, Z), (Z, Z, -ONE))
CYCLIC = ((Z, ONE, Z), (Z, Z, ONE), (ONE, Z, Z))
W = ((ONE, Z, PHI), (-ONE, Z, PHI), (PHI, ONE, Z),
     (PHI, -ONE, Z), (Z, PHI, ONE), (Z, PHI, -ONE))


def group():
    found = {ID}
    todo = [ID]
    while todo:
        M = todo.pop()
        for gen in (G, T):
            new = mm(gen, M)
            if new not in found:
                require(len(found) < 60, 'group exceeds sixty elements')
                found.add(new)
                todo.append(new)
    require(len(found) == 60, 'wrong icosahedral group order')
    require(TY in found and CYCLIC in found, 'missing tetrahedral symmetry')
    for M in found:
        require(mm(M, tuple(zip(*M))) == ID, 'not orthogonal')
        det = (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
               -M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
               +M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
        require(det == ONE, 'improper body transformation')
    return sorted(found, key=lambda M: tuple((x.a, x.b) for row in M for x in row))


# Linear forms in (1,u,r,a,t), with exact Q(phi) coefficients.
def lf(index, coefficient=ONE):
    return tuple(coefficient if j == index else Z for j in range(5))


def ladd(a, b):
    return tuple(x+y for x, y in zip(a, b))


def lscale(c, a):
    return tuple(c*x for x in a)


def lmv(M, v):
    return tuple(tuple(sum((M[i][j]*v[j][k] for j in range(3)), Z)
                       for k in range(5)) for i in range(3))


def ldot(n, v):
    return tuple(sum((n[j]*v[j][k] for j in range(3)), Z) for k in range(5))


def linterval(v, parameters):
    return sum((qi(c)*p for c, p in zip(v, parameters)), I(0, 0))


BOX = (I(1, 1), I(F(919831, 10**7), F(919833, 10**7)),
       I(F(1041858, 10**7), F(1041860, 10**7)),
       I(F(5565538, 10**7), F(5565540, 10**7)),
       I(F(5828994, 10**7), F(5828997, 10**7)))
B0 = F(1147, 1000)


def named_parameters():
    # Unique positive root of x^3-2x-phi=0; exact signs in Q(phi).
    lo, hi = F(17, 10), F(18, 10)
    require((Q(lo**3-2*lo)-PHI).sign() < 0, 'root lower endpoint')
    require((Q(hi**3-2*hi)-PHI).sign() > 0, 'root upper endpoint')
    for _ in range(90):
        mid = (lo+hi)/2
        if (Q(mid**3-2*mid)-PHI).sign() < 0:
            lo = mid
        else:
            hi = mid
    x = I(lo, hi)
    q = x*(x+P)+1
    u = ((3-x.square())/q).sqrt()
    r = (P*(x-1-1/x)/q).sqrt()/x
    aa = (x.square()*(392+225*P)+x*(249+670*P)+470+157*P)
    a = (aa/(961*P.square()*q)).sqrt()
    t = 1/x
    p = (I(1, 1), u, r, a, t)
    for v, box in zip(p, BOX):
        require(box.lo < v.lo <= v.hi < box.hi or box.lo == box.hi == 1,
                'named-solid parameter outside fixed box')
    return x, p, P*q.sqrt()/2


def vertices(mats):
    generic = (lf(1, -ONE), lf(2, -ONE), lf(0, -ONE))
    vs = [lmv(M, generic) for M in mats]
    for w in W:
        for s in (-1, 1):
            vs.append(tuple(lf(3, s*c) for c in w))
    for signs in product((-1, 1), repeat=3):
        vs.append(tuple(lf(4, Q(s)) for s in signs))
    for s1, s2 in product((-1, 1), repeat=2):
        v = (lf(0, Z), lf(4, s1/PHI), lf(4, s2*PHI))
        for _ in range(3):
            vs.append(v)
            v = lmv(CYCLIC, v)
    require(len(vs) == len(set(vs)) == 92, 'vertex orbit cardinality')
    V = set(vs)
    for M in mats:
        require({lmv(M, v) for v in vs} == V, 'body does not preserve vertices')
    return vs


def poly_square(l):
    out = {}
    for i, a in enumerate(l):
        for j, b in enumerate(l):
            k = tuple(sorted((i, j)))
            out[k] = out.get(k, Z)+a*b
    return {e: c for e, c in out.items() if c != Z}


def poly_add(p, q, scale=ONE):
    out = dict(p)
    for e, c in q.items():
        out[e] = out.get(e, Z)+scale*c
        if out[e] == Z:
            del out[e]
    return out


def poly_interval(p, box):
    return sum((qi(c)*(box[i].square() if i == j else box[i]*box[j])
                for (i, j), c in p.items()), I(0, 0))


def receiver_diameter(vs):
    # D0^2 = 4*(1+r^2*(h-1)/h), in C19-normalized units.
    expected = {(0, 0): Q(4), (2, 2): 4*(H-1)/H}
    active = []
    strict = []
    for i, v in enumerate(vs):
        for j in range(i):
            d = tuple(ladd(a, lscale(-ONE, b)) for a, b in zip(v, vs[j]))
            projected = {}
            for coord in d:
                projected = poly_add(projected, poly_square(coord))
            projected = poly_add(projected, poly_square(ldot(N, d)), -ONE/H)
            gap = poly_add(expected, projected, -ONE)
            if not gap:
                active.append((i, j))
            else:
                bound = poly_interval(gap, BOX)
                require(bound.lo > 0, f'nonactive receiver pair {i},{j}')
                strict.append(bound.lo)
    require(len(active) == 10 and len(strict) == 4176, 'wrong diameter pair counts')
    return min(strict)


def radius_check(vs):
    radius2 = {(3, 3): H}
    active, strict = 0, 0
    for v in vs:
        norm = {}
        for l in v:
            norm = poly_add(norm, poly_square(l))
        gap = poly_add(radius2, norm, -ONE)
        if not gap:
            active += 1
        else:
            require(poly_interval(gap, BOX).lo > 0, 'outer radius comparison')
            strict += 1
    require((active, strict) == (12, 80), 'radius orbit counts')


def orbit_rows(vs):
    # Each row is half a genuine difference of two vertices.
    first = (lf(2), lf(0), lf(0, Z))
    second = (lf(2), lf(0, -ONE), lf(0, Z))
    D, E = [], []
    for _ in range(5):
        D.append(first)
        E.append(second)
        first, second = lmv(G, first), lmv(G, second)
    require(first == D[0] and second == E[0], 'fivefold orbit does not close')
    diffs = set()
    for v in vs:
        for w in vs:
            diffs.add(tuple(lscale(F(1, 2), ladd(a, lscale(-ONE, b)))
                            for a, b in zip(v, w)))
    for row in D+E:
        require(row in diffs, 'row is not a genuine half-difference')
        norm = {}
        for l in row:
            norm = poly_add(norm, poly_square(l))
        require(norm == {(0, 0): ONE, (2, 2): ONE}, 'wrong difference length')
        require(ldot(N, row) == lf(2), 'wrong axial height')
    total = tuple(tuple(sum((v[j][k] for v in D), Z) for k in range(5))
                  for j in range(3))
    require(total == tuple(lf(2, 5*n/H) for n in N), 'fivefold average identity')
    return D, E


def signed_rows(Wi, signs):
    require(isinstance(signs, list) and len(signs) == len(Wi)
            and all(type(s) is int and s in (-1, 1) for s in signs), 'bad signs')
    return [tuple(lscale(s, coord) for coord in row) for row, s in zip(Wi, signs)]


def dual_check(rows, rhs, certificate):
    require(set(certificate) == {'rows', 'weights'}, 'unexpected dual fields')
    ix, weights = certificate['rows'], certificate['weights']
    require(isinstance(ix, list) and isinstance(weights, list)
            and 1 <= len(ix) == len(weights) <= 4, 'dual size')
    require(all(type(i) is int and 0 <= i < len(rows) for i in ix)
            and len(set(ix)) == len(ix), 'dual index')
    require(all(type(x) is int and x >= 0 for x in weights) and sum(weights) > 0,
            'dual weight')
    v = [tuple(sum((w*rows[i][j][k] for i, w in zip(ix, weights)), Z)
               for k in range(5)) for j in range(3)]
    b = tuple(sum((w*rhs[i][k] for i, w in zip(ix, weights)), Z) for k in range(5))
    vi = [linterval(c, BOX) for c in v]
    bi = linterval(b, BOX)
    require(bi.lo > 0, 'weighted right side not positive')
    norm = sum((c.square() for c in vi), I(0, 0))
    gap = bi.square()-qi(H)*norm
    require(gap.lo > 0, 'weighted sphere separation fails')
    # Integer weights make the cancellation visible; this ratio measures
    # only the proved strict gap, never a floating-point score.
    return gap.lo/bi.hi**2


def cover_check(mats, D, E, cert):
    require(set(cert) == {'ico', 'stage1', 'stage2', 'ico_special', 'remaining'},
            'unexpected cover fields')
    # Necessary ico threshold B^2 = h^2-[h+r^2(h-1)]/a^2.
    h, r, a = qi(H), BOX[2], BOX[3]
    lower = h.square()-(h+r.square()*(h-1))/a.square()
    require(lower.lo > B0*B0, 'icosahedral threshold lower bound')
    ico_rows = [tuple(lf(0, c) for c in w) for w in W]
    ico_rhs = [lf(0, Q(B0))]*6
    all6 = set(product((-1, 1), repeat=6))
    special = {tuple(s) for s in cert['ico_special']}
    require(len(special) == 12, 'wrong special ico pattern count')
    patterns = set()
    margins = []
    for item in cert['ico']:
        require(set(item) == {'signs', 'certificate'}, 'ico record')
        rows = signed_rows(ico_rows, item['signs'])
        s = tuple(item['signs'])
        require(s not in patterns, 'repeated ico pattern')
        patterns.add(s)
        margins.append(dual_check(rows, ico_rhs, item['certificate']))
    require(len(patterns) == 52 and patterns.isdisjoint(special)
            and patterns|special == all6, 'incomplete ico cover')
    # Every unexcluded pattern is that of an actual oriented fivefold axis,
    # and these axes form one proper-body orbit.
    axes = {mv(M, N) for M in mats}
    require(len(axes) == 12, 'fivefold axis orbit')
    actual = {tuple(dot(w, n).sign() for w in W) for n in axes}
    require(actual == special, 'special patterns lack proper orbit coverage')
    base = tuple(dot(w, N).sign() for w in W)
    Wi = signed_rows(ico_rows, list(base))
    first_seen = set()
    for item in cert['stage1']:
        require(set(item) == {'signs', 'certificate'}, 'first-stage record')
        s = tuple(item['signs'])
        require(s not in first_seen, 'repeated first-stage pattern')
        first_seen.add(s)
        rows = Wi+signed_rows(D, item['signs'])
        rhs = ico_rhs+[lf(2)]*5
        margins.append(dual_check(rows, rhs, item['certificate']))
    remaining = {tuple(s) for s in cert['remaining']}
    all5 = set(product((-1, 1), repeat=5))
    positive = (1,)*5
    require(len(first_seen) == 26 and len(remaining) == 5
            and first_seen.isdisjoint(remaining)
            and first_seen|remaining|{positive} == all5,
            'incomplete first-stage cover')
    second_seen = set()
    for item in cert['stage2']:
        require(set(item) == {'signs', 'second_signs', 'certificate'},
                'second-stage record')
        s, e = tuple(item['signs']), tuple(item['second_signs'])
        require(s in remaining and (s, e) not in second_seen,
                'repeated or unrelated second-stage pattern')
        second_seen.add((s, e))
        rows = Wi+signed_rows(D, list(s))+signed_rows(E, list(e))
        rhs = ico_rhs+[lf(2)]*10
        margins.append(dual_check(rows, rhs, item['certificate']))
    require(second_seen == {(s, e) for s in remaining for e in all5},
            'incomplete second-stage cover')
    return min(margins)


def main():
    path = Path(__file__).with_name('duals.json')
    cert = json.loads(path.read_text())
    mats = group()
    x, params, scale = named_parameters()
    vs = vertices(mats)
    radius_check(vs)
    receiver_gap = receiver_diameter(vs)
    D, E = orbit_rows(vs)
    dual_gap = cover_check(mats, D, E, cert)
    value = 2*scale*(1+params[2].square()*(qi(H)-1)/qi(H)).sqrt()
    require(value.lo > F(4210546827, 10**9)
            and value.hi < F(4210546828, 10**9), 'physical diameter enclosure')
    scaling_bound = params[3]*qi(H).sqrt()/(1+params[2].square()*(qi(H)-1)/qi(H)).sqrt()
    require(scaling_bound.lo > F(1054495195, 10**9)
            and scaling_bound.hi < F(1054495196, 10**9), 'scaling upper-bound enclosure')
    result = {
        'agent': 'six-rupert-1', 'role': 'researcher',
        'claim': 'global minimum projected diameter; fivefold receivers exclude strict passage',
        'proper_group_order': len(mats), 'vertices': len(vs),
        'receiving_pair_checks': 4186, 'active_receiving_pairs': 10,
        'strict_receiving_pairs': 4176, 'difference_rows': 10,
        'excluded_ico_sign_patterns': 52, 'remaining_ico_patterns': 12,
        'first_stage_duals': 26, 'second_stage_duals': 160,
        'total_integer_duals': 238, 'unoriented_minimizing_axes': 6,
        'normalized_receiver_gap_lower_bound': str(receiver_gap),
        'relative_dual_gap_lower_bound': str(dual_gap),
        'physical_minimum_diameter': ['4.210546827', '4.210546828'],
        'global_passage_scale_upper_bound': ['1.054495195', '1.054495196'],
        'parameter_box': [[str(z.lo), str(z.hi)] for z in BOX[1:]],
        'duals_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'full_rupert_problem': 'OPEN', 'floating_point_proof_decisions': 0,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
