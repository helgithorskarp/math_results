"""Exact Q[X]/(F) arithmetic, specialized at the bracketed real root.

Actual author: six-tammes-2, researcher. Characteristic zero. F need not
be assumed irreducible: every requested inverse has a checked Bezout
identity. No floating-point coefficient or root approximation is used.
"""
from fractions import Fraction as Q

F = tuple(map(Q, (-1, -3, 2, 6, -1, 13)))
LO = Q('0.59260590292507377809642492233275')
HI = Q('0.59260590292507377809642492233276')
INVERSES = {}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def trim(p):
    p = list(p)
    while p and not p[-1]:
        p.pop()
    return p

def padd(a, b):
    out = [Q(0)] * max(len(a), len(b))
    for i, x in enumerate(a): out[i] += x
    for i, x in enumerate(b): out[i] += x
    return trim(out)

def pmul(a, b):
    if not a or not b: return []
    out = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): out[i+j] += x*y
    return trim(out)

def pscale(a, b):
    return trim([x*b for x in a])

def divrem(a, b):
    a, b = trim(a), trim(b)
    require(bool(b), 'nonzero polynomial divisor')
    q = [Q(0)] * max(0, len(a)-len(b)+1)
    while a and len(a) >= len(b):
        k, c = len(a)-len(b), a[-1]/b[-1]
        q[k] += c
        for j, x in enumerate(b): a[k+j] -= c*x
        a = trim(a)
    return trim(q), a

def evaluate(p, x):
    out = Q(0)
    for c in reversed(p): out = out*x+c
    return out

def enclosure(p, lo=LO, hi=HI):
    out = (Q(0), Q(0))
    for c in reversed(p):
        products = [a*b for a in out for b in (lo, hi)]
        out = (min(products)+c, max(products)+c)
    return out

class E:
    __slots__ = ('c',)
    def __init__(self, value=0):
        if isinstance(value, E):
            self.c = value.c
            return
        if isinstance(value, (str, int, Q)):
            value = [Q(value)]
        require(isinstance(value, (list, tuple)) and
                all(isinstance(x, (str, int, Q)) for x in value),
                'exact rational coefficients only')
        _, r = divrem([Q(x) for x in value], F)
        self.c = tuple(r + [Q(0)]*(5-len(r)))
    def __add__(self, other): return E(padd(self.c, E(other).c))
    __radd__ = __add__
    def __neg__(self): return E(pscale(self.c, -1))
    def __sub__(self, other): return self + (-E(other))
    def __rsub__(self, other): return E(other) + (-self)
    def __mul__(self, other): return E(pmul(self.c, E(other).c))
    __rmul__ = __mul__
    def __truediv__(self, other): return self*E(other).inverse()
    def __rtruediv__(self, other): return E(other)*self.inverse()
    def __pow__(self, n):
        require(type(n) is int and n >= 0, 'nonnegative integer exponent')
        out, base = E(1), self
        while n:
            if n % 2: out = out*base
            base, n = base*base, n//2
        return out
    def __eq__(self, other):
        return self.c == E(other).c
    def sign(self):
        if not any(self.c): return 0
        lo, hi = enclosure(self.c)
        if lo > 0: return 1
        if hi < 0: return -1
        raise ValueError('unresolved exact sign in the fixed root bracket')
    def inverse(self):
        require(self.sign() != 0, 'divisor nonzero at the chosen real root')
        if self.c in INVERSES: return E(INVERSES[self.c])
        a, b, u, v = list(F), trim(self.c), [], [Q(1)]
        while b:
            q, r = divrem(a, b)
            a, b, u, v = b, r, v, padd(u, pscale(pmul(q, v), -1))
        require(len(a) == 1 and a[0] != 0, 'divisor coprime to F')
        out = E(pscale(u, 1/a[0]))
        require(self*out == E(1), 'checked Bezout inverse modulo F')
        INVERSES[self.c] = out.c
        return out

T, ZERO, ONE = E([0, 1]), E(0), E(1)

def verify_root():
    require(evaluate(F, LO) < 0 < evaluate(F, HI), 'exact opposite root signs')
    derivative = [i*F[i] for i in range(1, len(F))]
    lower, _ = enclosure(derivative, Q(577, 1000), Q(593, 1000))
    require(lower > 0, 'strict F derivative on the full interval J')
    require(E(F) == ZERO, 'literal quotient relation F=0')
    return str(lower)
