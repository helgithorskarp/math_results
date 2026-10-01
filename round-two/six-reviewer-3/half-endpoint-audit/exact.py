"""Independent cubic field and flat eta/delta jets. Standard library only.

Field inverses use extended polynomial Euclid. Jets live in
Q[c]/(8c^3-6c-1)[eta,delta]/(eta^4,delta^3).
Complex values are R + i*sin(theta_0)*I, with sin(theta_0)^2=q.
"""
from fractions import Fraction as F


def require(ok, message):
    if not ok:
        raise ValueError(message)


def trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def add(a, b):
    return trim([(a[i] if i < len(a) else F(0)) +
                 (b[i] if i < len(b) else F(0)) for i in range(max(len(a), len(b)))])


def mul(a, b):
    out = [F(0)] * max(0, len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return trim(out)


def divrem(a, b):
    a, b = trim(a), trim(b)
    require(bool(b), 'zero polynomial divisor')
    out = [F(0)] * max(0, len(a)-len(b)+1)
    while len(a) >= len(b):
        k, t = len(a)-len(b), a[-1]/b[-1]
        out[k] += t
        for j, y in enumerate(b):
            a[k+j] -= t*y
        a = trim(a)
    return trim(out), a


MOD = [F(-1, 8), F(-3, 4), F(0), F(1)]


class E:
    def __init__(self, value=0):
        if isinstance(value, E):
            self.a = value.a
            return
        require(not isinstance(value, bool), 'boolean field input')
        if isinstance(value, (int, F)):
            value = [F(value)]
        require(isinstance(value, (tuple, list)) and
                all(isinstance(x, (int, F)) and not isinstance(x, bool) for x in value),
                'malformed field polynomial')
        a = divrem([F(x) for x in value], MOD)[1]
        self.a = tuple(a + [F(0)]*(3-len(a)))

    def __add__(self, other):
        if not isinstance(other, (E, int, F)):
            return NotImplemented
        return E(add(self.a, E(other).a))
    __radd__ = __add__

    def __neg__(self):
        return E([-x for x in self.a])

    def __sub__(self, other):
        if not isinstance(other, (E, int, F)):
            return NotImplemented
        return self + -E(other)

    def __rsub__(self, other):
        return E(other) + -self

    def __mul__(self, other):
        if not isinstance(other, (E, int, F)):
            return NotImplemented
        return E(mul(self.a, E(other).a))
    __rmul__ = __mul__

    def inv(self):
        require(self != 0, 'zero field inverse')
        oldr, r, oldt, t = MOD, trim(self.a), [], [F(1)]
        while r:
            q, rem = divrem(oldr, r)
            oldr, r = r, rem
            oldt, t = t, add(oldt, [-x for x in mul(q, t)])
        require(len(oldr) == 1, 'nonunit field inverse')
        result = E([x/oldr[0] for x in oldt])
        require(self*result == 1, 'Euclidean field inverse identity')
        return result

    def __truediv__(self, other):
        return self*E(other).inv()

    def __rtruediv__(self, other):
        return E(other)*self.inv()

    def __pow__(self, n):
        require(isinstance(n, int), 'integer field exponent required')
        if n < 0:
            return self.inv()**(-n)
        out, b = E(1), self
        while n:
            if n % 2:
                out = out*b
            b, n = b*b, n//2
        return out

    def __eq__(self, other):
        if not isinstance(other, (E, int, F)):
            return False
        return self.a == E(other).a

    def record(self):
        return [str(x) for x in self.a]

    def interval(self, lo, hi):
        bounds = [self.a[0], self.a[0]]
        for j in (1, 2):
            ends = [self.a[j]*lo**j, self.a[j]*hi**j]
            bounds = [bounds[0]+min(ends), bounds[1]+max(ends)]
        return tuple(bounds)


class J:
    def __init__(self, value=0):
        if isinstance(value, J):
            self.a = dict(value.a)
            return
        if isinstance(value, dict):
            require(all(isinstance(k, tuple) and len(k) == 2 and
                        all(isinstance(n, int) and not isinstance(n, bool) for n in k) and
                        0 <= k[0] <= 3 and 0 <= k[1] <= 2 for k in value), 'malformed flat jet degree')
            self.a = {k: E(v) for k, v in value.items() if E(v) != 0}
        else:
            self.a = {} if E(value) == 0 else {(0, 0): E(value)}

    @staticmethod
    def term(n, m, value=1):
        return J({(n, m): value})

    def at(self, n, m=0):
        return self.a.get((n, m), E(0))

    def __add__(self, other):
        if isinstance(other, Z):
            return NotImplemented
        other = J(other)
        out = dict(self.a)
        for k, value in other.a.items():
            out[k] = out.get(k, E(0))+value
        return J(out)
    __radd__ = __add__

    def __neg__(self):
        return J({k: -v for k, v in self.a.items()})

    def __sub__(self, other):
        if isinstance(other, Z):
            return NotImplemented
        return self + -J(other)

    def __rsub__(self, other):
        return J(other) + -self

    def __mul__(self, other):
        if isinstance(other, Z):
            return NotImplemented
        other = J(other)
        out = {}
        for (n, m), x in self.a.items():
            for (k, l), y in other.a.items():
                if n+k <= 3 and m+l <= 2:
                    key = (n+k, m+l)
                    out[key] = out.get(key, E(0))+x*y
        return J(out)
    __rmul__ = __mul__

    def __pow__(self, n):
        require(isinstance(n, int) and n >= 0, 'nonnegative integer jet exponent')
        out, b = J(1), self
        while n:
            if n % 2:
                out = out*b
            b, n = b*b, n//2
        return out

    def inv(self):
        a = self.at(0, 0)
        require(a != 0, 'jet inverse needs nonzero constant')
        h = 1-self*a.inv()
        power, result = J(1), J(1)
        for _ in range(5):
            power = power*h
            result += power
        result *= a.inv()
        require(self*result == 1, 'flat-jet inverse identity')
        return result

    def __truediv__(self, other):
        return self*J(other).inv()

    def __rtruediv__(self, other):
        return J(other)*self.inv()

    def __eq__(self, other):
        if isinstance(other, Z):
            return False
        return self.a == J(other).a

    def record(self):
        return [[self.at(n, m).record() for m in range(3)] for n in range(4)]


def binomial(value, exponent):
    value = J(value)
    require(value.at(0, 0) == 1, 'binomial expansion requires unit constant')
    h, power, coefficient, out = value-1, J(1), F(1), J(1)
    for n in range(1, 6):
        power = power*h
        coefficient *= (exponent-n+1)/n
        out += coefficient*power
    return out


class Z:
    def __init__(self, real=0, imag=0, q=1):
        self.real, self.imag, self.q = J(real), J(imag), E(q)

    def cast(self, other):
        if isinstance(other, Z):
            require(self.q == other.q, 'different complex quadratic fields')
            return other
        return Z(other, q=self.q)

    def __add__(self, other):
        other = self.cast(other)
        return Z(self.real+other.real, self.imag+other.imag, self.q)
    __radd__ = __add__

    def __neg__(self):
        return Z(-self.real, -self.imag, self.q)

    def __sub__(self, other):
        return self + -self.cast(other)

    def __rsub__(self, other):
        return self.cast(other) + -self

    def __mul__(self, other):
        other = self.cast(other)
        return Z(self.real*other.real-self.q*self.imag*other.imag,
                 self.real*other.imag+self.imag*other.real, self.q)
    __rmul__ = __mul__

    def __pow__(self, n):
        require(isinstance(n, int) and n >= 0, 'complex nonnegative integer exponent')
        out, b = Z(1, q=self.q), self
        while n:
            if n % 2:
                out = out*b
            b, n = b*b, n//2
        return out

    def conj(self):
        return Z(self.real, -self.imag, self.q)

    def __eq__(self, other):
        other = self.cast(other)
        return self.real == other.real and self.imag == other.imag

    def author_record(self, sine_scale):
        zero = E(0).record()
        return [[[self.real.at(n,m).record(), zero, zero,
                  (sine_scale*self.imag.at(n,m)).record()] for m in range(3)] for n in range(4)]
