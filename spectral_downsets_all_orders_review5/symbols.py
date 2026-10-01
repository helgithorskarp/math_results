"""Dense nested polynomial rows over Q: rows are v-degree, entries l-degree.

Six-reviewer-5 independent symbolic arithmetic. Affine domains are built into
the variables before forming expressions; no author polynomial code is used.
Cross multiplication and explicit coefficient signs are exact; no interpolation.
"""
from fractions import Fraction as F
from hashlib import sha256
import json
from exact import need, poly, add, mul, scale

ZERO = ((F(0),),)
ONE = ((F(1),),)


def trim(rows):
    rows = [poly(r) for r in rows] or [(F(0),)]
    while len(rows) > 1 and rows[-1] == (F(0),):
        rows.pop()
    return tuple(rows)


def plus(a, b):
    return trim(add(a[i] if i < len(a) else (F(0),), b[i] if i < len(b) else (F(0),))
                for i in range(max(len(a), len(b))))


def times(a, b):
    out = [(F(0),)]*(len(a)+len(b)-1)
    for i, row in enumerate(a):
        if row == (F(0),):
            continue
        for j, other in enumerate(b):
            if other != (F(0),):
                out[i+j] = add(out[i+j], mul(row, other))
    return trim(out)


def coefficients(rows):
    return [[i, j, str(c)] for i, row in enumerate(rows) for j, c in enumerate(row) if c]


class Rat:
    def __init__(self, numerator, denominator=ONE):
        self.n = trim(numerator) if isinstance(numerator, (list, tuple)) else ((F(numerator),),)
        self.d = trim(denominator)
        need(self.d != ZERO, 'zero symbolic denominator')
        if self.n == ZERO:
            self.d = ONE
        elif len(self.d) == len(self.d[0]) == 1:
            value = self.d[0][0]
            self.n = tuple(scale(r, 1/value) for r in self.n)
            self.d = ONE

    @staticmethod
    def cast(x):
        return x if isinstance(x, Rat) else Rat(x)

    def __add__(self, x):
        x = self.cast(x)
        if self.n == ZERO:
            return x
        if x.n == ZERO:
            return self
        return Rat(plus(times(self.n, x.d), times(x.n, self.d)), times(self.d, x.d))

    __radd__ = __add__

    def __neg__(self):
        return Rat(tuple(scale(r, -1) for r in self.n), self.d)

    def __sub__(self, x):
        return self+-self.cast(x)

    def __rsub__(self, x):
        return self.cast(x)+-self

    def __mul__(self, x):
        x = self.cast(x)
        return Rat(times(self.n, x.n), times(self.d, x.d))

    __rmul__ = __mul__

    def __truediv__(self, x):
        x = self.cast(x)
        need(x.n != ZERO, 'divide by zero symbolic numerator')
        return Rat(times(self.n, x.d), times(self.d, x.n))

    def __rtruediv__(self, x):
        return self.cast(x)/self

    def __pow__(self, k):
        need(type(k) is int and k >= 0, 'invalid symbolic power')
        out = Rat(1)
        for _ in range(k):
            out *= self
        return out

    def equals(self, x):
        x = self.cast(x)
        return times(self.n, x.d) == times(x.n, self.d)

    def strict_record(self, name):
        need(self.n[0][0] > 0 and self.d[0][0] > 0, 'nonpositive symbolic constant: '+name)
        need(all(x >= 0 for p in (self.n, self.d) for row in p for x in row),
             'negative shifted coefficient: '+name)
        values = [coefficients(self.n), coefficients(self.d)]
        return {'numerator_terms': len(values[0]), 'denominator_terms': len(values[1]),
                'numerator_constant': str(self.n[0][0]), 'denominator_constant': str(self.d[0][0]),
                'coefficient_sha256': sha256(json.dumps(values, separators=(',', ':')).encode()).hexdigest()}
