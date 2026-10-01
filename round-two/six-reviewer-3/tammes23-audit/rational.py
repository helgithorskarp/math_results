"""Independent integer-polynomial rational functions and primitive Sturm chains.

No research imports. Euclidean polynomial division is rational; Sturm
remainders use only positive integer rescalings, preserving their signs.
"""
from fractions import Fraction as Q
from functools import lru_cache
from math import gcd, isqrt, lcm


def need(ok, message):
    if not ok:
        raise ValueError(message)


def trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return tuple(p)


def add(a, b):
    return trim((a[i] if i < len(a) else 0)+(b[i] if i < len(b) else 0)
                for i in range(max(len(a), len(b))))


def neg(a):
    return tuple(-x for x in a)


def mul(a, b):
    if not a or not b:
        return ()
    out = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return trim(out)


def value(p, t):
    out = Q(0)
    for x in reversed(p):
        out = out*t+x
    return out


def division(a, b):
    need(bool(b), 'polynomial divisor')
    a = list(map(Q, trim(a))); b = tuple(map(Q, b))
    quotient = [Q(0)]*max(0, len(a)-len(b)+1)
    while a and len(a) >= len(b):
        shift = len(a)-len(b); coefficient = a[-1]/b[-1]
        quotient[shift] = coefficient
        for i, x in enumerate(b):
            a[i+shift] -= coefficient*x
        a = list(trim(a))
    return trim(quotient), tuple(a)


def primitive(p):
    p = trim(p)
    if not p:
        return ()
    scale = lcm(*(Q(x).denominator for x in p))
    p = tuple(int(x*scale) for x in p)
    content = gcd(*p)
    return tuple(x//content for x in p)


@lru_cache(maxsize=None)
def polynomial_gcd(a, b):
    while b:
        a, b = b, primitive(division(a, b)[1])
    return tuple(Q(x, a[-1]) for x in a) if a else (Q(1),)


@lru_cache(maxsize=None)
def normal(n, d):
    n, d = trim(n), trim(d)
    need(bool(d), 'rational denominator')
    if not n:
        return (), (1,)
    g = polynomial_gcd(n, d)
    n, rn = division(n, g); d, rd = division(d, g)
    need(not rn and not rd, 'exact polynomial cancellation')
    scale = lcm(*(x.denominator for x in n+d))
    n, d = tuple(int(x*scale) for x in n), tuple(int(x*scale) for x in d)
    content = gcd(*(n+d))
    sign = 1 if d[-1] > 0 else -1
    return tuple(sign*x//content for x in n), tuple(sign*x//content for x in d)


class R:
    def __init__(self, n=(), d=(1,)):
        if isinstance(n, R):
            self.n, self.d = n.n, n.d
            return
        if isinstance(n, (int, Q)):
            n = (Q(n),)
        self.n, self.d = normal(tuple(map(Q, n)), tuple(map(Q, d)))

    def __add__(self, other):
        other = R(other)
        return R(add(mul(self.n, other.d), mul(other.n, self.d)), mul(self.d, other.d))

    __radd__ = __add__

    def __neg__(self):
        return R(neg(self.n), self.d)

    def __sub__(self, other):
        return self+-R(other)

    def __rsub__(self, other):
        return R(other)+-self

    def __mul__(self, other):
        other = R(other)
        return R(mul(self.n, other.n), mul(self.d, other.d))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = R(other); need(bool(other.n), 'nonzero rational divisor')
        return R(mul(self.n, other.d), mul(self.d, other.n))

    def __rtruediv__(self, other):
        return R(other)/self

    def __pow__(self, exponent):
        need(type(exponent) is int and exponent >= 0, 'nonnegative power')
        out = R(1)
        while exponent:
            if exponent & 1:
                out = out*self
            self = self*self; exponent //= 2
        return out

    def __eq__(self, other):
        other = R(other)
        return self.n == other.n and self.d == other.d

    def __bool__(self):
        return bool(self.n)

    def at(self, t):
        denominator = value(self.d, t); need(bool(denominator), 'evaluation denominator')
        return value(self.n, t)/denominator

    def manifest(self):
        return {'n': list(self.n), 'd': list(self.d)}


def solve(matrix, rhs):
    """Pivoted Gaussian elimination, including quadratic-algebra RHS vectors."""
    a = [list(map(R, row)) for row in matrix]; b = list(rhs); n = len(a)
    need(all(len(row) == n for row in a) and len(b) == n, 'square linear system')
    for k in range(n):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        need(pivot is not None, 'nonsingular symbolic system')
        a[k], a[pivot] = a[pivot], a[k]; b[k], b[pivot] = b[pivot], b[k]
        for i in range(k+1, n):
            factor = a[i][k]/a[k][k]
            for j in range(k, n):
                a[i][j] -= factor*a[k][j]
            b[i] -= b[k]*factor
    out = [None]*n
    for i in reversed(range(n)):
        out[i] = (b[i]-sum((out[j]*a[i][j] for j in range(i+1, n)), 0))/a[i][i]
    return out


def polynomial_sqrt(p):
    need(bool(p) and len(p) % 2 == 1 and p[-1] > 0, 'polynomial square shape')
    top = isqrt(p[-1]); need(top*top == p[-1], 'square leading coefficient')
    degree = (len(p)-1)//2; out = [Q(0)]*(degree+1); out[-1] = Q(top)
    for shift in range(1, degree+1):
        current = mul(out, out)
        i = 2*degree-shift
        out[degree-shift] = (Q(p[i])-(current[i] if i < len(current) else 0))/(2*top)
    need(mul(out, out) == tuple(p), 'complete polynomial square identity')
    return tuple(out)


def sqrt_rational(r):
    return R(polynomial_sqrt(r.n), polynomial_sqrt(r.d))


def positive_remainder(a, b):
    """Euclidean remainder up to a strictly positive rational multiplier."""
    r = primitive(a)
    while r and len(r) >= len(b):
        shift = len(r)-len(b); lead = abs(b[-1]); sign = 1 if b[-1] > 0 else -1
        r = primitive(add(tuple(lead*x for x in r),
                          (0,)*shift+tuple(-sign*r[-1]*x for x in b)))
    return r


@lru_cache(maxsize=None)
def sturm(p):
    p = primitive(p); need(bool(p), 'nonzero Sturm input')
    derivative = primitive(tuple(i*p[i] for i in range(1, len(p))))
    sequence = [p]
    if derivative:
        sequence.append(derivative)
        while sequence[-1]:
            rem = neg(positive_remainder(sequence[-2], sequence[-1]))
            if not rem:
                break
            sequence.append(primitive(rem))
    return tuple(sequence)


def variations(sequence, endpoint):
    signs = [1 if v > 0 else -1 for p in sequence if (v := value(p, endpoint))]
    return sum(a != b for a, b in zip(signs, signs[1:]))


@lru_cache(maxsize=None)
def sign_certificate(p, left, right):
    p = primitive(p)
    if not p:
        return 0, {'degree': -1, 'identically_zero': True}
    lo, hi = value(p, left), value(p, right)
    need(lo != 0 and hi != 0, 'strict sign at closed endpoints')
    sequence = sturm(p); vl, vr = variations(sequence, left), variations(sequence, right)
    need(vl == vr and lo*hi > 0, 'no sign root on complete closed interval')
    return 1 if lo > 0 else -1, {'degree': len(p)-1, 'sturm_degrees': [len(x)-1 for x in sequence],
                                'variations': [vl, vr], 'closed_root_count': vl-vr}
