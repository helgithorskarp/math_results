"""Small exact univariate rational-function arithmetic over Q[u]."""
from fractions import Fraction as F


def trim(p):
    p = list(p)
    while len(p) > 1 and not p[-1]:
        p.pop()
    return tuple(p or [F(0)])


def polynomial(value):
    entries = value if isinstance(value, (tuple, list)) else (value,)
    if any(not isinstance(v, (int, F)) for v in entries):
        raise TypeError('polynomial coefficients must be literal integers or Fraction values')
    return trim(tuple(F(v) for v in entries))


def add(a, b):
    return trim((a[i] if i < len(a) else 0)+(b[i] if i < len(b) else 0)
                for i in range(max(len(a), len(b))))


def neg(a):
    return tuple(-x for x in a)


def mul(a, b):
    result = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i+j] += x*y
    return trim(result)


def divide(a, b):
    if b == (0,):
        raise ZeroDivisionError('zero polynomial divisor')
    remainder = list(a)
    quotient = [F(0)]*max(1, len(a)-len(b)+1)
    while len(remainder) >= len(b) and trim(remainder) != (0,):
        degree = len(remainder)-len(b)
        factor = remainder[-1]/b[-1]
        quotient[degree] = factor
        for j, coefficient in enumerate(b):
            remainder[degree+j] -= factor*coefficient
        remainder = list(trim(remainder))
    return trim(quotient), trim(remainder)


def exact_divide(a, b):
    quotient, remainder = divide(a, b)
    if remainder != (0,):
        raise ValueError('nonexact polynomial division')
    return quotient


def gcd(a, b):
    while b != (0,):
        a, b = b, divide(a, b)[1]
    return tuple(x/a[-1] for x in a)


class R:
    def __init__(self, numerator=0, denominator=1):
        if isinstance(numerator, R) and denominator == 1:
            self.n, self.d = numerator.n, numerator.d
            return
        n, d = polynomial(numerator), polynomial(denominator)
        if d == (0,):
            raise ZeroDivisionError('zero rational-function denominator')
        if n == (0,):
            self.n, self.d = (F(0),), (F(1),)
            return
        common = gcd(n, d)
        n, d = exact_divide(n, common), exact_divide(d, common)
        scale = d[-1]
        self.n, self.d = tuple(x/scale for x in n), tuple(x/scale for x in d)

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
        other = R(other)
        return R(mul(self.n, other.d), mul(self.d, other.n))

    def __rtruediv__(self, other):
        return R(other)/self

    def __pow__(self, exponent):
        if not isinstance(exponent, int) or exponent < 0:
            raise ValueError('only nonnegative integer powers')
        result = R(1)
        for _ in range(exponent):
            result *= self
        return result

    def __eq__(self, other):
        other = R(other)
        return self.n == other.n and self.d == other.d

    def at(self, u):
        def evaluate(p):
            result = F(0)
            for c in reversed(p):
                result = result*u+c
            return result
        return evaluate(self.n)/evaluate(self.d)

    def coefficients_positive(self, strict=True):
        if not all(c >= 0 for c in self.d) or self.d[0] <= 0:
            raise ValueError('denominator not coefficient-positive')
        if not all(c >= 0 for c in self.n) or (strict and self.n[0] <= 0):
            raise ValueError('numerator not coefficient-positive')
        return True

    def record(self):
        return {'numerator': [str(c) for c in self.n], 'denominator': [str(c) for c in self.d]}
