#!/usr/bin/env python3
"""Exact polynomial arithmetic for verify.py, standard library.

Domain Q[m,r], with rational-function denominators products of m,
3m+2 and m+2. Characteristic zero; monomials are ordered (m,r).
Adapted from six-sendov-2's published two-block checker (source c8fc799).
This author reuse supplies arithmetic, not independent verification.
"""
from fractions import Fraction as F
from math import factorial
import json


def require(condition, label):
    if not condition:
        raise AssertionError(label)


class Poly:
    def __init__(self, terms=0):
        if isinstance(terms, (int, F)):
            terms = {(0, 0): F(terms)}
        self.t = {k: F(v) for k, v in terms.items() if v}

    def __add__(self, other):
        other = poly(other)
        out = dict(self.t)
        for k, v in other.t.items():
            out[k] = out.get(k, F(0)) + v
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.t.items()})

    def __sub__(self, other):
        return self + -poly(other)

    def __rsub__(self, other):
        return poly(other) + -self

    def __mul__(self, other):
        if not isinstance(other, (Poly, int, F)):
            return NotImplemented
        other = poly(other)
        out = {}
        for (a, b), v in self.t.items():
            for (c, d), w in other.t.items():
                k = (a+c, b+d)
                out[k] = out.get(k, F(0)) + v*w
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0, "nonnegative integer exponent")
        out = Poly(1)
        for _ in range(exponent):
            out *= self
        return out

    def at(self, variable, value):
        out = Poly(0)
        for k, c in self.t.items():
            base = list(k)
            base[variable] = 0
            out += Poly({tuple(base): c}) * poly(value)**k[variable]
        return out

    def coefficient(self, variable, degree):
        out = {}
        for k, c in self.t.items():
            if k[variable] == degree:
                base = list(k)
                base[variable] = 0
                out[tuple(base)] = c
        return Poly(out)

    def __eq__(self, other):
        return self.t == poly(other).t

    def divide_linear_m(self, root, leading):
        """Division by leading*(m-root), independently for each r degree."""
        quotient = {}
        remainder = {}
        for r in sorted({b for a, b in self.t}):
            coeff = {a: v for (a, b), v in self.t.items() if b == r}
            top = max(coeff)
            carry = coeff.get(top, F(0))
            if top:
                quotient[(top-1, r)] = carry/leading
            for a in range(top-1, 0, -1):
                carry = coeff.get(a, F(0)) + root*carry
                quotient[(a-1, r)] = carry/leading
            rem = coeff.get(0, F(0)) + (root*carry if top else F(0))
            if rem:
                remainder[(0, r)] = rem
        return Poly(quotient), Poly(remainder)

    def terms(self):
        return [[a, b, str(c)] for (a, b), c in sorted(self.t.items())]


def poly(x):
    return x if isinstance(x, Poly) else Poly(x)


m = Poly({(1, 0): 1})
r = Poly({(0, 1): 1})
D = 3*m+2
M = m+2
FACTORS = (m, D, M)
ROOTS = ((F(0), F(1)), (F(-2, 3), F(3)), (F(-2), F(1)))


class RF:
    def __init__(self, numerator=0, denominator=(0, 0, 0)):
        self.p = poly(numerator)
        self.d = list(denominator)
        if self.p == 0:
            self.d = [0, 0, 0]
        for i, (root, leading) in enumerate(ROOTS):
            while self.d[i] and self.p != 0:
                quotient, remainder = self.p.divide_linear_m(root, leading)
                if remainder != 0:
                    break
                self.p = quotient
                self.d[i] -= 1
        self.d = tuple(self.d)

    def __add__(self, other):
        other = rf(other)
        exps = tuple(max(x, y) for x, y in zip(self.d, other.d))
        n1, n2 = self.p, other.p
        for i in range(3):
            n1 *= FACTORS[i]**(exps[i]-self.d[i])
            n2 *= FACTORS[i]**(exps[i]-other.d[i])
        return RF(n1+n2, exps)

    __radd__ = __add__

    def __neg__(self):
        return RF(-self.p, self.d)

    def __sub__(self, other):
        return self + -rf(other)

    def __rsub__(self, other):
        return rf(other) + -self

    def __mul__(self, other):
        other = rf(other)
        return RF(self.p*other.p, tuple(x+y for x, y in zip(self.d, other.d)))

    __rmul__ = __mul__

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0, "nonnegative integer exponent")
        return RF(self.p**exponent, tuple(exponent*x for x in self.d))

    def __eq__(self, other):
        return (self-rf(other)).p == 0

    def coefficient(self, degree):
        return RF(self.p.coefficient(1, degree), self.d)

    def data(self):
        return {'numerator_terms_m_r': self.p.terms(),
                'denominator_exponents_m_3mplus2_mplus2': list(self.d)}


def rf(x):
    return x if isinstance(x, RF) else RF(x)
