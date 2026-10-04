"""Fresh exact Q[w]/(w^12-w^6+1), with w=exp(i*pi/18).

No target code, fixtures, computer algebra system or floating point.
Polynomials in r remain whole; eta jets are truncated only by degree.
"""
from fractions import Fraction as Q


class F:
    __slots__ = ('v',)

    def __init__(self, value=0):
        if isinstance(value, F):
            self.v = value.v
            return
        a = list(value) if isinstance(value, (list, tuple)) else [value]
        a = [Q(x) for x in a] + [Q(0)] * max(0, 12 - len(a))
        for j in range(len(a) - 1, 11, -1):
            a[j-6] += a[j]
            a[j-12] -= a[j]
        self.v = tuple(a[:12])

    def __add__(self, other):
        if not isinstance(other, (F, int, Q, list, tuple)):
            return NotImplemented
        other = F(other)
        return F([a+b for a, b in zip(self.v, other.v)])

    __radd__ = __add__

    def __neg__(self):
        return F([-a for a in self.v])

    def __sub__(self, other):
        if not isinstance(other, (F, int, Q, list, tuple)):
            return NotImplemented
        return self + (-F(other))

    def __rsub__(self, other):
        return F(other) - self

    def __mul__(self, other):
        if not isinstance(other, (F, int, Q, list, tuple)):
            return NotImplemented
        other = F(other)
        a = [Q(0)] * 23
        for j, x in enumerate(self.v):
            if x:
                for k, y in enumerate(other.v):
                    if y:
                        a[j+k] += x*y
        return F(a)

    __rmul__ = __mul__

    def __pow__(self, n):
        if n < 0:
            return self.inverse() ** (-n)
        a, b = F(1), self
        while n:
            if n & 1:
                a = a*b
            b = b*b
            n //= 2
        return a

    def inverse(self):
        # Solve the complete 12-coordinate multiplication matrix.
        columns = [self * F([0]*j + [1]) for j in range(12)]
        a = [[columns[k].v[j] for k in range(12)] + [Q(j == 0)]
             for j in range(12)]
        for k in range(12):
            pivot = next((j for j in range(k, 12) if a[j][k]), None)
            if pivot is None:
                raise ZeroDivisionError('singular field multiplication')
            a[k], a[pivot] = a[pivot], a[k]
            d = a[k][k]
            a[k] = [x/d for x in a[k]]
            for j in range(12):
                if j != k and a[j][k]:
                    d = a[j][k]
                    a[j] = [x-d*y for x, y in zip(a[j], a[k])]
        out = F([a[j][12] for j in range(12)])
        if self*out != F(1):
            raise ArithmeticError('inverse residual')
        return out

    def __truediv__(self, other):
        if isinstance(other, (int, Q)):
            return F([a/Q(other) for a in self.v])
        return self * F(other).inverse()

    def __rtruediv__(self, other):
        return F(other)*self.inverse()

    def __eq__(self, other):
        if not isinstance(other, (F, int, Q, list, tuple)):
            return NotImplemented
        return self.v == F(other).v

    def __bool__(self):
        return any(self.v)

    def conjugate(self):
        return sum((a*WNEG[j] for j, a in enumerate(self.v) if a), F())

    def real(self):
        return (self+self.conjugate())/2

    def imag(self):
        return (self-self.conjugate())*(-I)/2

    def record(self):
        return [[x.numerator, x.denominator] for x in self.v]


W = F([0, 1])
WNEG = [W ** ((-j) % 36) for j in range(12)]
I = W**9
C = (W**2 + W**34)/2
S = (W**2 - W**34)*(-I)/2


class R:
    """Exact polynomial in the unrestricted real parameter r."""
    __slots__ = ('v',)

    def __init__(self, value=0):
        if isinstance(value, R):
            self.v = value.v
            return
        a = list(value) if isinstance(value, (list, tuple)) else [value]
        a = [F(x) for x in a]
        while len(a) > 1 and not a[-1]:
            a.pop()
        self.v = tuple(a or [F()])

    def __add__(self, other):
        if isinstance(other, J):
            return NotImplemented
        other = R(other)
        return R([self.at(j)+other.at(j)
                  for j in range(max(len(self.v), len(other.v)))])

    __radd__ = __add__

    def __neg__(self):
        return R([-a for a in self.v])

    def __sub__(self, other):
        if isinstance(other, J):
            return NotImplemented
        return self + (-R(other))

    def __rsub__(self, other):
        return R(other)-self

    def __mul__(self, other):
        if isinstance(other, J):
            return NotImplemented
        other = R(other)
        a = [F()] * (len(self.v)+len(other.v)-1)
        for j, x in enumerate(self.v):
            if x:
                for k, y in enumerate(other.v):
                    if y:
                        a[j+k] = a[j+k]+x*y
        return R(a)

    __rmul__ = __mul__

    def __pow__(self, n):
        if n < 0:
            raise ValueError('negative polynomial power')
        a, b = R(1), self
        while n:
            if n & 1:
                a = a*b
            b = b*b
            n //= 2
        return a

    def __truediv__(self, other):
        return R([a/other for a in self.v])

    def at(self, n):
        return self.v[n] if n < len(self.v) else F()

    def conjugate(self):
        return R([a.conjugate() for a in self.v])

    def real(self):
        return R([a.real() for a in self.v])

    def imag(self):
        return R([a.imag() for a in self.v])

    def __eq__(self, other):
        return self.v == R(other).v

    def __bool__(self):
        return any(self.v)

    def record(self):
        return [a.record() for a in self.v]


class J:
    """Epsilon jet through degree ten, coefficients in F[r]."""
    __slots__ = ('v',)

    def __init__(self, value=0):
        if isinstance(value, J):
            self.v = value.v
            return
        a = list(value) if isinstance(value, (list, tuple)) else [value]
        self.v = tuple((list(map(R, a))+[R()]*11)[:11])

    def __add__(self, other):
        other = J(other)
        return J([a+b for a, b in zip(self.v, other.v)])

    __radd__ = __add__

    def __neg__(self):
        return J([-a for a in self.v])

    def __sub__(self, other):
        return self + (-J(other))

    def __rsub__(self, other):
        return J(other)-self

    def __mul__(self, other):
        other = J(other)
        return J([sum((self.v[j]*other.v[n-j] for j in range(n+1) if self.v[j] and other.v[n-j]), R())
                  for n in range(11)])

    __rmul__ = __mul__

    def __truediv__(self, other):
        return J([a/other for a in self.v])

    def __pow__(self, n):
        a, b = J(1), self
        while n:
            if n & 1:
                a = a*b
            b = b*b
            n //= 2
        return a

    def conjugate(self):
        return J([a.conjugate() for a in self.v])

    def real(self):
        return J([a.real() for a in self.v])

    def imag(self):
        return J([a.imag() for a in self.v])

    def __eq__(self, other):
        return self.v == J(other).v

    def record(self):
        return [a.record() for a in self.v]


def zproduct(a, b):
    """Literal polynomial product in z, jet coefficients."""
    out = [J()] * (len(a)+len(b)-1)
    for j, x in enumerate(a):
        for k, y in enumerate(b):
            out[j+k] = out[j+k]+x*y
    return out


def zeval(a, z):
    out = a[-1]
    for v in reversed(a[:-1]):
        out = out*z+v
    return out


def zderivative(a):
    return [v*(j+1) for j, v in enumerate(a[1:])]


def inverse_sqrt(a):
    if a.v[0] != R(1):
        raise ValueError('nonunit constant in inverse sqrt')
    u = a-1
    return 1-u/2+3*(u*u)/8-5*(u*u*u)/16+35*(u**4)/128-63*(u**5)/256
