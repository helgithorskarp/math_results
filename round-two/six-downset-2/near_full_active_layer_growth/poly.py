"""Exact sparse polynomials in two indeterminates over Q, characteristic 0.

six-downset-2, researcher. No CAS, interpolation, numerical evaluation or
modular reconstruction is used. All identities are coefficient identities.
"""
from fractions import Fraction as Q


def require(condition, message):
    if not condition:
        raise ValueError(message)


class P:
    def __init__(self, value=0):
        if isinstance(value, P):
            self.c = dict(value.c)
            return
        if isinstance(value, dict):
            require(all(type(i) is tuple and len(i) == 2 and all(type(k) is int and k >= 0 for k in i)
                        for i in value), 'Two nonnegative integral exponents')
            require(all(type(v) in (int, Q) for v in value.values()), 'Exact coefficients')
            self.c = {i: Q(v) for i, v in value.items() if v}
        else:
            require(type(value) in (int, Q), 'Exact scalar')
            self.c = {(0, 0): Q(value)} if value else {}

    def __add__(self, other):
        b, c = P(other), dict(self.c)
        for i, v in b.c.items():
            c[i] = c.get(i, Q(0))+v
        return P(c)

    __radd__ = __add__

    def __neg__(self):
        return P({i: -v for i, v in self.c.items()})

    def __sub__(self, other):
        return self+-P(other)

    def __rsub__(self, other):
        return P(other)+-self

    def __mul__(self, other):
        b, c = P(other), {}
        for i, u in self.c.items():
            for j, v in b.c.items():
                k = (i[0]+j[0], i[1]+j[1])
                c[k] = c.get(k, Q(0))+u*v
        return P(c)

    __rmul__ = __mul__

    def __truediv__(self, other):
        require(type(other) in (int, Q) and other != 0, 'Nonzero scalar division')
        return P({i: v/Q(other) for i, v in self.c.items()})

    def __pow__(self, exponent):
        require(type(exponent) is int and exponent >= 0, 'Nonnegative integral power')
        out = P(1)
        for _ in range(exponent):
            out = out*self
        return out

    def __eq__(self, other):
        return self.c == P(other).c

    def substitute(self, first, second):
        return sum((v*P(first)**i*P(second)**j for (i, j), v in self.c.items()), P(0))

    def divide_first_monomial(self, power):
        require(type(power) is int and power >= 0 and all(i >= power for i, _ in self.c),
                'Exact monomial division')
        return P({(i-power, j): v for (i, j), v in self.c.items()})

    def coefficient_second(self, exponent):
        return P({(i, 0): v for (i, j), v in self.c.items() if j == exponent})

    def integers(self):
        require(all(j == 0 and v.denominator == 1 for (i, j), v in self.c.items()), 'Integral univariate polynomial')
        return [int(self.c.get((i, 0), 0)) for i in range(1+max((i for i, _ in self.c), default=0))]


FIRST = P({(1, 0): 1})
SECOND = P({(0, 1): 1})
