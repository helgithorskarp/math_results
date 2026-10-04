"""Independent dense rational polynomial and rational-function arithmetic."""
from fractions import Fraction as Q


def poly(a):
    a = tuple(Q(x) for x in a)
    while len(a) > 1 and a[-1] == 0:
        a = a[:-1]
    return a or (Q(0),)


def add(a, b):
    return poly([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def scale(a, c):
    return poly([x*c for x in a])


def mul(a, b):
    v = [Q(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            v[i+j] += x*y
    return poly(v)


def power(a, n):
    out = poly([1])
    for _ in range(n):
        out = mul(out, a)
    return out


def deriv(a):
    return poly([i*a[i] for i in range(1, len(a))])


def evaluate(a, x):
    out = Q(0)
    for c in reversed(a):
        out = out*x+c
    return out


class RF:
    def __init__(self, n=0, d=(1,)):
        self.n = poly(n if isinstance(n, (list, tuple)) else [n])
        self.d = poly(d)
        if self.d == (Q(0),):
            raise ValueError('zero rational-function denominator')

    @staticmethod
    def lift(x):
        return x if isinstance(x, RF) else RF(x)

    def __add__(self, other):
        o = self.lift(other)
        return RF(add(mul(self.n, o.d), mul(o.n, self.d)), mul(self.d, o.d))

    __radd__ = __add__

    def __neg__(self):
        return RF(scale(self.n, -1), self.d)

    def __sub__(self, o):
        return self + -self.lift(o)

    def __rsub__(self, o):
        return self.lift(o) + -self

    def __mul__(self, other):
        o = self.lift(other)
        return RF(mul(self.n, o.n), mul(self.d, o.d))

    __rmul__ = __mul__

    def __truediv__(self, other):
        o = self.lift(other)
        return RF(mul(self.n, o.d), mul(self.d, o.n))

    def __rtruediv__(self, o):
        return self.lift(o) / self

    def __pow__(self, n):
        if n < 0:
            return RF(power(self.d, -n), power(self.n, -n))
        return RF(power(self.n, n), power(self.d, n))

    def diff(self):
        return RF(add(mul(deriv(self.n), self.d),
                      scale(mul(self.n, deriv(self.d)), -1)), power(self.d, 2))

    def value(self, x):
        return evaluate(self.n, x)/evaluate(self.d, x)

    def residual(self, other):
        o = self.lift(other)
        return add(mul(self.n, o.d), scale(mul(o.n, self.d), -1))
