"""Closed rational intervals with exact dyadic square-root rounding.

No floating arithmetic, libm or native interval package. Square roots use
integer isqrt on a rational radicand, with verified outward endpoints.
"""
from fractions import Fraction as Q
from math import isqrt

BITS = 64
SCALE = 1 << BITS


class I:
    def __init__(self, lo, hi=None):
        if isinstance(lo, I) and hi is None:
            self.lo, self.hi = lo.lo, lo.hi
        else:
            self.lo, self.hi = Q(lo), Q(lo if hi is None else hi)
        if self.lo > self.hi:
            raise ValueError('Reversed interval')

    def __add__(self, other):
        b = I(other)
        return I(self.lo+b.lo, self.hi+b.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self+-I(other)

    def __rsub__(self, other):
        return I(other)+-self

    def __mul__(self, other):
        b = I(other)
        values = [x*y for x in (self.lo, self.hi) for y in (b.lo, b.hi)]
        return I(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other):
        b = I(other)
        if b.lo <= 0 <= b.hi:
            raise ValueError('Division interval contains zero')
        return self*I(1/b.hi, 1/b.lo)

    def square(self):
        if self.lo <= 0 <= self.hi:
            return I(0, max(self.lo*self.lo, self.hi*self.hi))
        return I(min(self.lo*self.lo, self.hi*self.hi), max(self.lo*self.lo, self.hi*self.hi))

    def sqrt(self):
        if self.lo < 0:
            raise ValueError('Negative square-root interval')
        def floor_sqrt(x):
            n = isqrt((x.numerator*SCALE*SCALE)//x.denominator)
            if not Q(n, SCALE)**2 <= x < Q(n+1, SCALE)**2:
                raise ValueError('Dyadic square-root floor certificate failed')
            return n
        lower, upper = floor_sqrt(self.lo), floor_sqrt(self.hi)
        if Q(upper, SCALE)**2 != self.hi:
            upper += 1
        result = I(Q(lower, SCALE), Q(upper, SCALE))
        if result.lo**2 > self.lo or result.hi**2 < self.hi:
            raise ValueError('Outward square-root certificate failed')
        return result

    def output(self):
        return [str(self.lo), str(self.hi)]


def norm(x, y):
    return (I(x).square()+I(y).square()).sqrt()


def example_reciprocals(epsilon):
    """Enclose all 8 reciprocals using the exact derivative factorization.

    Six repeated critical roots are i(eps +/-99/100). The remaining two
    reciprocal roots solve D(A)q^2-10Aq+9=0, A=9/10-i eps.
    """
    a, t = Q(9, 10), Q(99, 100)
    eps = Q(epsilon)
    q = []
    for y in (eps+t, eps-t):
        den = a*a+y*y
        q.extend([(I(a/den), I(y/den))]*3)
    x, y = 64*(a*a-eps*eps)-36*t*t, -128*a*eps
    if x <= 0:
        raise ValueError('Principal square-root branch not isolated')
    absolute = norm(x, y)
    U = ((absolute+x)/2).sqrt()
    V = I(y)/(2*U)
    # U>0 and 2UV=y determine the principal square root uniquely.
    if U.lo <= 0:
        raise ValueError('Square-root branch ambiguity')
    dr, di = 2*(a*a-eps*eps+t*t), -4*a*eps
    den = dr*dr+di*di
    for sign in (1, -1):
        nr, ni = 10*a+sign*U, -10*eps+sign*V
        q.append(((nr*dr+ni*di)/den, (ni*dr-nr*di)/den))
    return q


def costs(q):
    singles = []
    for x, y in q:
        r = norm(x, y)
        singles.append(norm(x-r, y))
    pairs = {(i, j): norm(q[i][0]-q[j][0], q[i][1]+q[j][1])
             for i in range(len(q)) for j in range(i+1, len(q))}
    return singles, pairs
