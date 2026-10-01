"""Small exact polynomial arithmetic over Q; coefficients ascend in degree.

Author: six-downset-2, researcher. Standard library only. No interpolation,
modular reconstruction or floating-point arithmetic is used.
"""
from fractions import Fraction
from itertools import permutations, combinations


def require(condition, message):
    if not condition:
        raise ValueError(message)


class P:
    def __init__(self, value=0):
        if isinstance(value, P):
            self.c = value.c
            return
        c = list(value) if isinstance(value, (list, tuple)) else [value]
        require(all(isinstance(x, (int, Fraction)) for x in c), 'exact polynomial coefficients required')
        c = [x.numerator if isinstance(x, Fraction) and x.denominator == 1 else x for x in c]
        while len(c) > 1 and c[-1] == 0:
            c.pop()
        self.c = tuple(c or [0])

    def __add__(self, other):
        b = P(other)
        return P([(self.c[i] if i < len(self.c) else 0) +
                  (b.c[i] if i < len(b.c) else 0)
                  for i in range(max(len(self.c), len(b.c)))])

    __radd__ = __add__

    def __neg__(self):
        return P([-x for x in self.c])

    def __sub__(self, other):
        return self + (-P(other))

    def __rsub__(self, other):
        return P(other) - self

    def __mul__(self, other):
        b = P(other)
        c = [0] * (len(self.c) + len(b.c) - 1)
        for i, x in enumerate(self.c):
            for j, y in enumerate(b.c):
                c[i+j] += x*y
        return P(c)

    __rmul__ = __mul__

    def __truediv__(self, other):
        require(isinstance(other, (int, Fraction)) and other != 0, 'polynomial division by a nonzero scalar only')
        return P([x*Fraction(1, other) for x in self.c])

    def __pow__(self, k):
        require(type(k) is int and k >= 0, 'nonnegative integer exponent required')
        v = P(1)
        for _ in range(k):
            v *= self
        return v

    def __eq__(self, other):
        return self.c == P(other).c

    def value(self, x):
        v = 0
        for a in reversed(self.c):
            v = v*x+a
        return v

    def integers(self):
        require(all(type(x) is int for x in self.c), 'integer polynomial required')
        return list(self.c)


def determinant(A):
    n = len(A)
    require(all(len(row) == n for row in A), 'square determinant required')
    result = 0
    for p in permutations(range(n)):
        term = 1
        for i in range(n):
            term *= A[i][p[i]]
        if sum(p[i] > p[j] for i in range(n) for j in range(i+1, n)) % 2:
            term = -term
        result += term
    return result


def elementary(A):
    return [1] + [sum(determinant([[A[i][j] for j in ix] for i in ix])
                      for ix in combinations(range(len(A)), k))
                  for k in range(1, len(A)+1)]
