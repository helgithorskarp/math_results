"""Small exact truncated power-series rings; no numerical root solving."""
from fractions import Fraction as F


def series_ring(order, coefficient):
    class Series:
        N = order

        def __init__(self, value=0):
            if isinstance(value, Series):
                self.a = value.a
            elif isinstance(value, (list, tuple)):
                self.a = tuple(coefficient(x) for x in value[:order+1])
                self.a += tuple(coefficient(0) for _ in range(order+1-len(self.a)))
            else:
                self.a = (coefficient(value),) + tuple(coefficient(0) for _ in range(order))

        def __add__(self, other):
            other = Series(other)
            return Series([a+b for a,b in zip(self.a,other.a)])

        __radd__ = __add__

        def __neg__(self):
            return Series([-x for x in self.a])

        def __sub__(self, other):
            return self+-Series(other)

        def __rsub__(self, other):
            return Series(other)+-self

        def __mul__(self, other):
            other = Series(other)
            out = [coefficient(0) for _ in range(order+1)]
            for i,x in enumerate(self.a):
                if x == 0:
                    continue
                for j,y in enumerate(other.a[:order+1-i]):
                    if y != 0:
                        out[i+j] += x*y
            return Series(out)

        __rmul__ = __mul__

        def __pow__(self, exponent):
            if not isinstance(exponent,int) or exponent < 0:
                raise ValueError('nonnegative integer series power')
            result = Series(1)
            base = self
            while exponent:
                if exponent & 1:
                    result *= base
                exponent >>= 1
                if exponent:
                    base *= base
            return result

        def inv(self):
            out = [self.a[0].inv()]
            for n in range(1,order+1):
                out.append(-sum((self.a[j]*out[n-j] for j in range(1,n+1)),coefficient(0))*out[0])
            return Series(out)

        def __truediv__(self, other):
            return self*Series(other).inv()

        def __rtruediv__(self, other):
            return Series(other)*self.inv()

        def __eq__(self, other):
            return self.a == Series(other).a

        def with_coefficient(self, index, value):
            out = list(self.a)
            out[index] = coefficient(value)
            return Series(out)

        def record(self):
            return [x.record() for x in self.a]

    return Series
