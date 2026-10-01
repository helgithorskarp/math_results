#!/usr/bin/env python3
"""Exact arithmetic for the fourth boundary packet.

Adapted from six-sendov-3 cubic-boundary verify.py, published commit
52a408f210846d246b5c8dfd890cc142d480d2c4 (parent independently reviewed8781).
Only field, sparse-polynomial and residual-root arithmetic is retained;
no previous claim checker, fixture, external data or solver is imported.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

class AlgebraError(RuntimeError):
    pass


def require(ok, label):
    if not ok:
        raise AlgebraError(label)


class K:
    """Q[c]/(c^3-3c/4-1/8), normal form (1,c,c^2)."""

    def __init__(self, value=0):
        if isinstance(value, K):
            self.a = value.a
        elif isinstance(value, (tuple, list)):
            require(len(value) == 3, 'cubic normal form length')
            self.a = tuple(map(F, value))
        else:
            self.a = (F(value), F(0), F(0))

    def __add__(self, other):
        other = K(other)
        return K(tuple(a+b for a, b in zip(self.a, other.a)))

    __radd__ = __add__

    def __neg__(self):
        return K(tuple(-a for a in self.a))

    def __sub__(self, other):
        return self + -K(other)

    def __rsub__(self, other):
        return K(other) + -self

    def __mul__(self, other):
        other = K(other)
        a = [F(0)]*5
        for i, x in enumerate(self.a):
            for j, y in enumerate(other.a):
                a[i+j] += x*y
        for i in (4, 3):
            a[i-2] += F(3, 4)*a[i]
            a[i-3] += F(1, 8)*a[i]
        return K(tuple(a[:3]))

    __rmul__ = __mul__

    def __pow__(self, n):
        require(isinstance(n, int) and n >= 0, 'nonnegative field power')
        ans = K(1)
        for _ in range(n):
            ans *= self
        return ans

    def inv(self):
        columns = [(self*K(tuple(int(i == j) for i in range(3)))).a
                   for j in range(3)]
        rows = [[columns[j][i] for j in range(3)] + [F(i == 0)]
                for i in range(3)]
        for j in range(3):
            pivot = next((i for i in range(j, 3) if rows[i][j]), None)
            require(pivot is not None, 'invertible cubic field element')
            rows[j], rows[pivot] = rows[pivot], rows[j]
            q = rows[j][j]
            rows[j] = [v/q for v in rows[j]]
            for i in range(3):
                if i != j:
                    q = rows[i][j]
                    rows[i] = [v-q*w for v, w in zip(rows[i], rows[j])]
        return K(tuple(rows[i][3] for i in range(3)))

    def __truediv__(self, other):
        return self*K(other).inv()

    def __rtruediv__(self, other):
        return K(other)*self.inv()

    def __eq__(self, other):
        return self.a == K(other).a

    def record(self):
        return [str(a) for a in self.a]

    def interval(self, lo, hi):
        # Here 0 < lo < hi, so powers preserve the ordered endpoints.
        lower = upper = self.a[0]
        for i in (1, 2):
            ends = self.a[i]*lo**i, self.a[i]*hi**i
            lower += min(ends)
            upper += max(ends)
        return lower, upper


# Gaussian-rational moment jets: eta,z,ten real moments,six imaginary moments.
NV = 18
ORDER = 3
ZERO_EXP = (0,)*NV


def gadd(a, b):
    return a[0]+b[0], a[1]+b[1]


def gmul(a, b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def pc(v=0, imag=0):
    v = F(v), F(imag)
    return {ZERO_EXP: v} if v != (0, 0) else {}


def pv(i):
    a = [0]*NV
    a[i] = 1
    return {tuple(a): (F(1), F(0))}


def padd(*ps):
    ans = {}
    for p in ps:
        for e, v in p.items():
            ans[e] = gadd(ans.get(e, (F(0), F(0))), v)
            if ans[e] == (0, 0):
                del ans[e]
    return ans


def pscale(p, real=1, imag=0):
    return {e: w for e, v in p.items()
            if (w := gmul(v, (F(real), F(imag)))) != (0, 0)}


def pmul(*ps):
    ans = pc(1)
    for p in ps:
        new = {}
        for e, v in ans.items():
            for f, w in p.items():
                if e[0]+f[0] > ORDER:
                    continue
                key = tuple(a+b for a, b in zip(e, f))
                new[key] = gadd(new.get(key, (F(0), F(0))), gmul(v, w))
                if new[key] == (0, 0):
                    del new[key]
        ans = new
    return ans


def ppow(p, n):
    return pmul(*([p]*n))


def pdiff(p, i):
    ans = {}
    for e, v in p.items():
        if e[i]:
            f = list(e)
            f[i] -= 1
            ans[tuple(f)] = gmul(v, (F(e[i]), F(0)))
    return ans


def pint(p, i):
    ans = {}
    for e, v in p.items():
        f = list(e)
        f[i] += 1
        ans[tuple(f)] = gmul(v, (F(1, f[i]), F(0)))
    return ans


def psubst(p, i, replacement):
    ans = {}
    for e, v in p.items():
        f = list(e)
        power = f[i]
        f[i] = 0
        # Accumulate directly. Rebuilding the entire partial sum per
        # monomial is quadratic in the sparse output size.
        for key, w in pmul({tuple(f): v}, ppow(replacement, power)).items():
            ans[key] = gadd(ans.get(key, (F(0), F(0))), w)
            if ans[key] == (0, 0):
                del ans[key]
    return ans


def precord(p):
    return [[list(e), str(v[0]), str(v[1])] for e, v in sorted(p.items())]


def phash(p):
    raw = json.dumps(precord(p), separators=(',', ':')).encode()
    return sha256(raw).hexdigest()


class Z:
    """K[s,i]/(s^2-q,i^2+1), with conjugation fixing the real s."""

    def __init__(self, value=0, *, q=None):
        if isinstance(value, Z):
            self.q, self.a = value.q, value.a
        else:
            require(q is not None, 'quadratic extension specified')
            self.q = K(q)
            vals = value if isinstance(value, (list, tuple)) else (value, 0, 0, 0)
            require(len(vals) == 4, 'quadratic Gaussian length')
            self.a = tuple(K(v) for v in vals)

    def coerce(self, other):
        ans = other if isinstance(other, Z) else Z(other, q=self.q)
        require(ans.q == self.q, 'same quadratic extension')
        return ans

    def __add__(self, other):
        other = self.coerce(other)
        return Z(tuple(a+b for a, b in zip(self.a, other.a)), q=self.q)

    __radd__ = __add__

    def __neg__(self):
        return Z(tuple(-a for a in self.a), q=self.q)

    def __sub__(self, other):
        return self+-self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other)+-self

    def __mul__(self, other):
        other = self.coerce(other)
        a, b, c, d = self.a
        e, f, g, h = other.a
        q = self.q
        return Z((a*e+b*f*q-c*g-d*h*q,
                  a*f+b*e-c*h-d*g,
                  a*g+b*h*q+c*e+d*f*q,
                  a*h+b*g+c*f+d*e), q=q)

    __rmul__ = __mul__

    def __truediv__(self, other):
        # Only real-field scalar divisions occur in this checker.
        return self*K(other).inv()

    def __pow__(self, n):
        require(isinstance(n, int) and n >= 0, 'nonnegative extension power')
        ans = Z(1, q=self.q)
        for _ in range(n):
            ans *= self
        return ans

    def conj(self):
        a, b, c, d = self.a
        return Z((a, b, -c, -d), q=self.q)

    def real_field(self):
        require(self.a[1] == 0, 'real part descends to cubic field')
        return self.a[0]

    def __eq__(self, other):
        return self.a == self.coerce(other).a

    def record(self):
        return [a.record() for a in self.a]


# Independent sparse K[eta,z,m,theta], retaining all eta orders <=4.
KNV = 4; KORDER = 4; KZERO = (0,)*KNV
def kpc(a=0):
    return {KZERO: K(a)} if K(a) != 0 else {}
def kpv(j):
    e = [0]*KNV; e[j] = 1
    return {tuple(e): K(1)}
def kadd(*ps):
    out = {}
    for p in ps:
        for e, a in p.items():
            out[e] = out.get(e, K(0))+a
            if out[e] == 0: del out[e]
    return out
def kscale(p, a):
    return {e: b for e, v in p.items() if (b := v*a) != 0}
def kmul(*ps):
    out = kpc(1)
    for p in ps:
        new = {}
        for e, a in out.items():
            for f, b in p.items():
                if e[0]+f[0] > KORDER: continue
                key = tuple(x+y for x, y in zip(e, f))
                new[key] = new.get(key, K(0))+a*b
                if new[key] == 0: del new[key]
        out = new
    return out
def kpower(p, n):
    return kmul(*([p]*n))
def kintegrate(p):
    out = {}
    for e, a in p.items():
        f = list(e); f[1] += 1
        out[tuple(f)] = a/f[1]
    return out
def ksubstitute(p, j, replacement):
    out = {}
    for e, a in p.items():
        f = list(e); n = f[j]; f[j] = 0
        out = kadd(out, kmul({tuple(f): a}, kpower(replacement, n)))
    return out
def kcoefficient(p, order):
    return {tuple([0]+list(e[1:])): a for e, a in p.items() if e[0] == order}
def kevaluate(p, order, omega, mm=0, tt=0, derivative=0):
    out = Z(0, q=omega.q)
    for (a, b, g, h), coeff in p.items():
        if a == order and b >= derivative:
            coeff *= K(mm)**g*K(tt)**h
            for j in range(derivative): coeff *= b-j
            out += omega**(b-derivative)*coeff
    return out
def kphash(p):
    record = [[list(e), a.record()] for e, a in sorted(p.items())]
    return sha256(json.dumps(record, separators=(',', ':')).encode()).hexdigest()


def residual_roots(poly, omega, mm, tt):
    """Independent implicit solving by complete polynomial residual coefficients."""
    zero=lambda:[Z(0,q=omega.q) for _ in range(KORDER+1)]
    def add(a,b):return [x+y for x,y in zip(a,b)]
    def mul(a,b):
        out=zero()
        for i,x in enumerate(a):
            for j,y in enumerate(b[:KORDER+1-i]):
                out[i+j]+=x*y
        return out
    byz={}
    for (a,b,g,h),v in poly.items():
        byz.setdefault(b,zero())[a]+=v*K(mm)**g*K(tt)**h
    def evaluate(r):
        ans=zero()
        for b in range(9,-1,-1):ans=add(mul(ans,r),byz.get(b,zero()))
        return ans
    r=zero();r[0]=omega
    for n in range(1,KORDER+1):
        # r_n=0 here; p0'(omega)=9/omega determines the new coefficient.
        residual=evaluate(r)[n]
        r[n]=-residual*omega/9
    residual=evaluate(r)
    rad=[]
    for n in range(1,KORDER+1):
        coeff=sum((r[j]*r[n-j].conj() for j in range(n+1)),
                  Z(0,q=omega.q))/2
        rad.append(coeff.real_field())
    return r,residual,rad,evaluate
