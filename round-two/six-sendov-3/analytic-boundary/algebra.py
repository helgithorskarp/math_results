#!/usr/bin/env python3
"""Exact cubic and quadratic-Gaussian arithmetic for the analytic-boundary packet.

The K and Z arithmetic is copied, with attribution, from six-sendov-3
fourth-boundary/arithmetic.py, published commit
9b8581c53cd6d06feaa7e0c0001791293264ae4e. This imports no prior checker,
fixture, experimental output or theorem. The new sparse ring below checks
only the finite identities stated in PROOF.md, not its analytic bridges.
"""
from fractions import Fraction as F
from hashlib import sha256
import json

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


class Ring:
    """Sparse Gaussian-K ring with a total-degree or single-axis truncation."""

    def __init__(self, names, order, axis=None):
        self.names = tuple(names)
        self.order = order
        self.axis = axis
        self.zero = (0,)*len(names)

    def allowed(self, exponent):
        degree = sum(exponent) if self.axis is None else exponent[self.axis]
        return degree <= self.order

    def constant(self, real=0, imaginary=0):
        pair = (K(real), K(imaginary))
        return {self.zero: pair} if pair != (K(0), K(0)) else {}

    def variable(self, name):
        e = list(self.zero)
        e[self.names.index(name)] = 1
        return {tuple(e): (K(1), K(0))}

    def add(self, *polys):
        out = {}
        for p in polys:
            for e, (a, b) in p.items():
                x, y = out.get(e, (K(0), K(0)))
                pair = (x+a, y+b)
                if pair == (K(0), K(0)):
                    out.pop(e, None)
                else:
                    out[e] = pair
        return out

    def scale(self, p, real=0, imaginary=0):
        return self.mul(p, self.constant(real, imaginary))

    def mul(self, *polys):
        out = self.constant(1)
        for p in polys:
            nxt = {}
            for e, (a, b) in out.items():
                for f, (x, y) in p.items():
                    key = tuple(u+v for u, v in zip(e, f))
                    if not self.allowed(key):
                        continue
                    v0, v1 = nxt.get(key, (K(0), K(0)))
                    pair = (v0+a*x-b*y, v1+a*y+b*x)
                    if pair == (K(0), K(0)):
                        nxt.pop(key, None)
                    else:
                        nxt[key] = pair
            out = nxt
        return out

    def power(self, p, n):
        require(isinstance(n, int) and n >= 0, 'nonnegative sparse power')
        out = self.constant(1)
        for _ in range(n):
            out = self.mul(out, p)
        return out

    def substitute(self, p, name, value):
        j = self.names.index(name)
        out = {}
        for e, pair in p.items():
            key = list(e)
            key[j] = 0
            term = {tuple(key): pair}
            out = self.add(out, self.mul(term, self.power(value, e[j])))
        return out

    def coefficient(self, p, name, power):
        j = self.names.index(name)
        out = {}
        for e, pair in p.items():
            if e[j] == power:
                key = list(e)
                key[j] = 0
                out[tuple(key)] = pair
        return out

    def record(self, p):
        return [[list(e), a.record(), b.record()]
                for e, (a, b) in sorted(p.items())]

    def digest(self, p):
        raw = json.dumps(self.record(p), separators=(',', ':')).encode()
        return sha256(raw).hexdigest()

