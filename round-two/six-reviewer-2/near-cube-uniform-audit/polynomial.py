"""Small independent sparse Q[n,x,T,a] coefficient engine; no CAS input."""
from fractions import Fraction
from math import comb


class P:
    names = ("n", "x", "T", "a")

    def __init__(self, terms=0):
        if isinstance(terms, P):
            self.terms = dict(terms.terms)
        elif isinstance(terms, dict):
            self.terms = {e: Fraction(c) for e, c in terms.items() if c}
        elif type(terms) in (int, Fraction):
            self.terms = {(0, 0, 0, 0): Fraction(terms)} if terms else {}
        else:
            raise TypeError("Exact integer/Fraction coefficients required")

    @classmethod
    def variable(cls, name):
        e = tuple(int(k == name) for k in cls.names)
        if not sum(e):
            raise ValueError(name)
        return cls({e: 1})

    def __add__(self, other):
        t = dict(self.terms)
        for e, c in P(other).terms.items():
            t[e] = t.get(e, 0) + c
        return P(t)

    __radd__ = __add__

    def __neg__(self):
        return P({e: -c for e, c in self.terms.items()})

    def __sub__(self, other):
        return self + -P(other)

    def __rsub__(self, other):
        return P(other) + -self

    def __mul__(self, other):
        t = {}
        for e, c in self.terms.items():
            for f, d in P(other).terms.items():
                ef = tuple(u + v for u, v in zip(e, f))
                t[ef] = t.get(ef, 0) + c * d
        return P(t)

    __rmul__ = __mul__

    def __pow__(self, power):
        if type(power) is not int or power < 0:
            raise ValueError("nonnegative integer power required")
        out, base = P(1), self
        while power:
            if power & 1:
                out = out * base
            base = base * base
            power //= 2
        return out

    def substitute(self, name, value):
        i = self.names.index(name)
        out = P()
        for e, c in self.terms.items():
            f = list(e)
            f[i] = 0
            out += P({tuple(f): c}) * P(value) ** e[i]
        return out

    def divide_n(self):
        if any(e[0] == 0 for e in self.terms):
            raise ValueError("not polynomial-divisible by n")
        return P({(e[0] - 1, *e[1:]): c for e, c in self.terms.items()})

    def coefficient(self, name, power):
        i = self.names.index(name)
        t = {}
        for e, c in self.terms.items():
            if e[i] == power:
                f = list(e)
                f[i] = 0
                t[tuple(f)] = c
        return P(t)

    def n_coefficients(self):
        if any(any(e[1:]) for e in self.terms):
            raise ValueError("not univariate in n")
        degree = max((e[0] for e in self.terms), default=0)
        return [self.terms.get((k, 0, 0, 0), Fraction()) for k in range(degree + 1)]

    def evaluate(self, **values):
        result = Fraction()
        for e, c in self.terms.items():
            for name, power in zip(self.names, e):
                if power:
                    c *= values[name] ** power
            result += c
        return result

    def require_equal(self, other, label):
        d = self - other
        if d.terms:
            raise ValueError(label + ": nonzero coefficients " + repr(d.terms))


def from_coefficients(values):
    return P({(k, 0, 0, 0): c for k, c in enumerate(values)})


def shift_coefficients(poly, offset):
    """Independent binomial substitution, without P.substitute."""
    cs = poly.n_coefficients()
    return [sum(cs[j] * comb(j, k) * offset ** (j - k)
                for j in range(k, len(cs))) for k in range(len(cs))]
