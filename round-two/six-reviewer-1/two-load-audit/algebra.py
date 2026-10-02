"""Reviewer QQ polynomial arithmetic and division-free minor reconstruction.

Own9049 arithmetic reused; no author imports, integer packing, supplied factors, saved sign polynomials,
interpolation or floating point. Uses SymPy's sparse polynomial ring for
multiplication, factorization and exact division. Denominators are tracked as
primitive factors, discovered at each division. Internal UFD cross-cancellation
precedes products; only equal denominator exponents can cancel in sums. A subset recurrence computes
determinants; it does not use the author's permutation implementation.
"""
import hashlib
import json
from fractions import Fraction
from math import lcm
from sympy import QQ
from sympy.polys.rings import ring

POLY, Q, tvar, Dvar, avar, uvar = ring('Q,t,D,a,u', QQ)
ZERO = (0, 0, 0, 0, 0)
ATOMS = {}
CACHE = {}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def factors(p):
    require(bool(p), 'nonzero rational divisor')
    unit, out = p.factor_list()
    answer = {}
    for a, power in out:
        # monic normalization separates a rational scalar; no sign is lost.
        lead = a.LC
        a = a / lead
        unit *= lead ** power
        key = tuple(sorted((k, str(v)) for k, v in a.items()))
        ATOMS[key] = a
        answer[key] = answer.get(key, 0) + power
    return unit, answer


def product(d):
    key = tuple(sorted(d.items()))
    if key not in CACHE:
        p = POLY.one
        for k, e in key:
            p *= ATOMS[k] ** e
            require(len(p) <= 30000, 'fixed denominator polynomial term guard')
        CACHE[key] = p
    return CACHE[key]


class Rat:
    def __init__(self, n=0, d=None):
        if isinstance(n, Rat) and d is None:
            self.n, self.d = n.n, n.d.copy()
            return
        self.n = POLY(n)
        self.d = dict(d or {})
        if not self.n:
            self.d = {}
            return
        for k in tuple(self.d):
            while self.d[k]:
                quo, rem = self.n.div(ATOMS[k])
                if rem:
                    break
                self.n = quo
                self.d[k] -= 1
            if not self.d[k]:
                del self.d[k]
        require(len(self.n) <= 30000, 'fixed polynomial term guard')

    @classmethod
    def reduced(cls,n,den):
        # Internal constructor: caller proves numerator coprime to every
        # irreducible denominator factor. Never used for arbitrary inputs.
        value=object.__new__(cls);value.n=POLY(n)
        value.d={k:e for k,e in den.items() if e} if value.n else {}
        require(len(value.n)<=30000,'fixed polynomial term guard')
        return value

    @staticmethod
    def cancel(n,den,candidates):
        den=den.copy()
        for k in candidates:
            while den.get(k,0):
                quo,rem=n.div(ATOMS[k])
                if rem:break
                n=quo;den[k]-=1
            if not den.get(k,0):den.pop(k,None)
        return n,den

    def __add__(self, other):
        other = Rat(other)
        if not self.n:
            return other
        if not other.n:
            return Rat(self)
        den = self.d.copy()
        for k, e in other.d.items():
            den[k] = max(den.get(k, 0), e)
        left = {k: e - self.d.get(k, 0) for k, e in den.items() if e > self.d.get(k, 0)}
        right = {k: e - other.d.get(k, 0) for k, e in den.items() if e > other.d.get(k, 0)}
        n=self.n*product(left)+other.n*product(right)
        # For unequal factor exponents exactly one summand is indivisible
        # by the factor. Only equal positive exponents can cancel in a sum.
        equal=[k for k in den if self.d.get(k,0)==other.d.get(k,0)]
        n,den=self.cancel(n,den,equal)
        return Rat.reduced(n,den)

    __radd__ = __add__

    def __neg__(self):
        return Rat.reduced(-self.n, self.d)

    def __sub__(self, other):
        return self + -Rat(other)

    def __rsub__(self, other):
        return Rat(other) + -self

    def __mul__(self, other):
        other = Rat(other)
        if not self.n or not other.n:
            return Rat()
        # Reduced fractions can cancel only across the two operands.
        # Cancel before multiplying to avoid dividing a much larger product.
        left,dr=self.cancel(self.n,other.d,tuple(other.d))
        right,dl=self.cancel(other.n,self.d,tuple(self.d))
        den=dl.copy()
        for k,e in dr.items():den[k]=den.get(k,0)+e
        return Rat.reduced(left*right,den)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Rat(other)
        unit, den = factors(other.n)
        return self * Rat.reduced(product(other.d) / unit, den)

    def __rtruediv__(self, other):
        return Rat(other) / self

    def __pow__(self, power):
        require(type(power) is int and power >= 0, 'nonnegative integral power')
        if power==0:return Rat(1)
        return Rat.reduced(self.n ** power, {k: e * power for k, e in self.d.items()})

    def __eq__(self, other):
        other = Rat(other)
        if not self.n or not other.n:
            return bool(self.n) == bool(other.n)
        if self.d == other.d:
            return self.n == other.n
        return self.n * product(other.d) == other.n * product(self.d)


def determinant(a):
    """Exterior row recurrence with a subset state, no divisions or permutations."""
    require(all(len(row) == len(a) for row in a), 'square determinant')
    values = {0: Rat(1)}
    for row in a:
        new = {}
        for mask, value in values.items():
            for j, entry in enumerate(row):
                if mask & (1 << j):
                    continue
                if not Rat(entry).n:
                    continue
                # Insert column j after the previously selected columns.
                sign = (-1) ** (mask >> (j + 1)).bit_count()
                out = mask | (1 << j)
                new[out] = new.get(out, Rat()) + sign * value * entry
        values = new
    return values.get((1 << len(a)) - 1, Rat())


def dot(metric, x, y):
    return sum((x[i] * metric[i][j] * y[j] for i in range(len(x))
                for j in range(len(y)) if metric[i][j] != 0), Rat())


def linear(*terms):
    return [sum((c * v[i] for c, v in terms), Rat()) for i in range(len(terms[0][1]))]


def digest(p):
    payload = sorted((list(k), str(v)) for k, v in p.items())
    return hashlib.sha256(json.dumps(payload, separators=(',', ':')).encode()).hexdigest()


def portable_digest(p):
    """Exact encoding comparison only; independent sign arithmetic is unchanged."""
    d = 1
    for v in p.values():
        d = lcm(d, Fraction(str(v)).denominator)
    payload = {'den': d, 'terms': sorted((list(k), str(int(Fraction(str(v)) * d))) for k, v in p.items())}
    return hashlib.sha256(json.dumps(payload, separators=(',', ':')).encode()).hexdigest()
