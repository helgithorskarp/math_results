#!/usr/bin/env python3
"""Exact supplementary algebra for PROOF.md; CPython >=3.11, stdlib only.

No finite calculation here certifies the analytic limits or their uniformity.
Those are proved in PROOF.md. Checks are active with python -O too.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from math import factorial
from pathlib import Path


NAMES = ("L", "G", "B", "lam", "w", "r", "b", "z", "q", "p", "v")
ZERO = (0,) * len(NAMES)


class Poly:
    """Small exact Laurent-polynomial ring with rational coefficients."""

    def __init__(self, terms):
        if not isinstance(terms, dict):
            terms = {ZERO: F(terms)}
        self.terms = {k: F(c) for k, c in terms.items() if c}

    def __add__(self, other):
        other = aspoly(other)
        out = dict(self.terms)
        for k, c in other.terms.items():
            out[k] = out.get(k, F(0)) + c
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -c for k, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-aspoly(other))

    def __rsub__(self, other):
        return aspoly(other) - self

    def __mul__(self, other):
        other = aspoly(other)
        out = {}
        for k, c in self.terms.items():
            for j, d in other.terms.items():
                e = tuple(a + b for a, b in zip(k, j))
                out[e] = out.get(e, F(0)) + c * d
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, power):
        if power < 0:
            if len(self.terms) != 1:
                raise ValueError("Negative powers require a nonzero monomial")
            k, c = next(iter(self.terms.items()))
            return Poly({tuple(power * e for e in k): c ** power})
        out = Poly(1)
        for _ in range(power):
            out = out * self
        return out

    def __truediv__(self, other):
        return self * aspoly(other) ** -1

    def substitute(self, substitutions):
        out = Poly(0)
        for k, c in self.terms.items():
            term = Poly(c)
            for name, power in zip(NAMES, k):
                term = term * aspoly(substitutions.get(name, var(name))) ** power
            out = out + term
        return out

    def antiderivative(self, name):
        idx = NAMES.index(name)
        out = {}
        for k, c in self.terms.items():
            if k[idx] == -1:
                raise ValueError("Logarithmic antiderivative is outside this ring")
            exponents = list(k)
            exponents[idx] += 1
            out[tuple(exponents)] = c / exponents[idx]
        return Poly(out)

    def exponential_moment(self):
        """Integrate in w against exp(-lam*w), for lam>0."""
        wi, li = NAMES.index("w"), NAMES.index("lam")
        out = {}
        for k, c in self.terms.items():
            n = k[wi]
            if n < 0:
                raise ValueError("A polynomial in w is required")
            exponents = list(k)
            exponents[wi] = 0
            exponents[li] -= n + 1
            j = tuple(exponents)
            out[j] = out.get(j, F(0)) + c * factorial(n)
        return Poly(out)


def aspoly(value):
    return value if isinstance(value, Poly) else Poly(value)


def var(name):
    exponents = list(ZERO)
    exponents[NAMES.index(name)] = 1
    return Poly({tuple(exponents): 1})


def require(condition, description):
    if not condition:
        raise RuntimeError(description)


def same(lhs, rhs, description):
    require(not (aspoly(lhs) - rhs).terms, description)


def signed_constant(radius, b):
    return -b * max(radius - b, F(0)) / 4


def audit():
    L, G, B, lam, w, r, b, z, q, p, v = map(var, NAMES)

    # The angular signed integral is checked as a formal identity, not a grid.
    angular = (F(3, 2) * r*r*z*z - 2*r*b*z + b*b/2 - r*r/2) / 2
    primitive = angular.antiderivative("z")
    angular_value = primitive.substitute({"z": 1}) - primitive.substitute({"z": b/r})
    same(angular_value, -b*(r-b)/4, "signed angular integral (16)")
    h_primitive = ((r*z-b)/2).antiderivative("z")
    leading = h_primitive.substitute({"z": 1}) - h_primitive.substitute({"z": b/r})
    same(leading, (r-b)**2/(4*r), "leading positive-part average")

    # Formal t coefficients in u^2=lam^2+2t F_t(u).
    u1 = L/lam
    u2 = -B/(2*lam) + L*G/lam**2 - L**2/(2*lam**3)
    same(2*lam*u1, 2*L, "boundary order t")
    same(u1**2 + 2*lam*u2, 2*G*u1-B, "boundary order t^2")
    volume1 = lam*u2 + u1**2
    same(volume1, -B/2+L*G/lam+L**2/(2*lam**2), "volume order t")

    prefactor0 = lam
    prefactor1 = 2*(u1+w)
    exponent1 = -u1*w-w**2/2+G*w
    exterior0 = prefactor0.exponential_moment()
    exterior1 = (prefactor1+prefactor0*exponent1).exponential_moment()
    same(exterior0, 1, "exterior constant")
    same(exterior1, (L+1)/lam**2+G/lam, "exterior order t")
    C = -B/2+(L+1)*G/lam+(L**2/2+L)/lam**2
    same(volume1+exterior1, C+lam**-2, "combined signed coefficient")

    # A Dirac law has L=lam*q, G=q, and E_theta(q^2)=B/3.
    dirac = C.substitute({"L": lam*q, "G": q})
    spherical = Poly(0)
    qi = NAMES.index("q")
    for exponents, coefficient in dirac.terms.items():
        power = exponents[qi]
        require(power in (0, 1, 2), "unexpected Dirac angular degree")
        remainder = list(exponents)
        remainder[qi] = 0
        moment = (Poly(1), Poly(0), B/3)[power]
        spherical = spherical + Poly({tuple(remainder): coefficient}) * moment
    same(spherical, 0, "point-mass translation normalization")

    # Integration by parts underlying (27): G now denotes posterior P(z).
    V = L**2/2+L
    density = -r*r*G/2 + r*z*(L+1)*G/lam + V/lam**2
    primitive_derivative = -r*r*G/2 + r*r/v**2*(V+z*(L+1)*v*G)
    same(density, primitive_derivative.substitute({"v": lam*r}),
         "two-atom boundary primitive")

    # Negative control: removing the exterior correction changes the answer.
    require((volume1-(C+lam**-2)).terms, "omitted exterior correction must fail")
    require((angular_value-b*(r-b)/4).terms, "reversed signed constant must fail")

    # Rational monotone bounds valid simultaneously for every integer m>=12.
    p0, rootp0, ell0, v0 = F(1, 4096), F(1, 64), F(8), F(4)
    source_upper = -F(1, 16)+(1+p0)/(8*ell0)+(5*p0*p0+2*p0)/(16*ell0**2)
    target_abs = F(1, 16)*((rootp0+2*p0)/(4*v0)
                  +(p0+4*p0*p0)/(4*v0*v0)+(rootp0+2*p0)/(2*v0*v0))
    combined = source_upper+target_abs
    margin = -F(1, 32)-combined
    require(margin > 0, "uniform negative fixed-law coefficient margin")
    require(source_upper == F(-805232635, 17179869184), "source rational bound")
    require(target_abs == F(406529, 4294967296), "target rational bound")
    require(combined == F(-803606519, 17179869184), "combined rational bound")

    # Mean pair-distance and entropy upper bound for alpha=1/4, symbolically.
    alpha = F(1, 4)
    deficit = 2*p*(1-p)*r*r*(1-alpha*alpha)
    same(deficit, F(15, 8)*p*(1-p)*r*r, "exact pair-distance deficit")
    same(p*(1-p)*r*r/2, F(4, 15)*deficit, "entropy upper bound times s")

    fixtures = []
    for radius in map(F, (1, 2, 3, 4)):
        for shrink in (F(1, 4), F(1, 2), F(3, 4)):
            for fraction in (F(1, 4), F(1, 2), F(3, 4)):
                intercept = radius*fraction
                limit = signed_constant(radius, intercept)-signed_constant(shrink*radius, intercept)
                require(limit < 0, "nontrivial contraction has negative moving-weight limit")
                fixtures.append(str(limit/(radius*radius)))
        for intercept in (radius, 2*radius):
            require(signed_constant(radius, intercept) == 0, "empty active spherical cap")
    require(signed_constant(F(1), F(1, 2))
            - signed_constant(F(1, 4), F(1, 2)) == -F(1, 16), "explicit limit")

    return {
        "status": "PASS",
        "arithmetic": "integer and rational Laurent polynomials; no floating point",
        "formal_identities": 12,
        "negative_controls": 2,
        "moving_weight_fixtures": len(fixtures),
        "empty_cap_checks": 8,
        "normalized_limits": fixtures,
        "source_coefficient_upper": str(source_upper),
        "target_coefficient_absolute_upper": str(target_abs),
        "coefficient_difference_upper": str(combined),
        "margin_below_minus_one_over_32": str(margin),
        "explicit_fixed_variance_limit_times_s_over_R2": "-1/16",
        "deficit_over_p_one_minus_p_R2": "15/8",
        "entropy_upper_times_s_over_deficit": "4/15",
        "trust_boundary": "Analytic limits, dominated convergence, uniform remainders, and cited endpoint theorems require the written proof. This is supplementary algebra, not independent review."
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare the exact record with EXPECTED.json")
    args = parser.parse_args()
    encoded = (json.dumps(audit(), indent=2, sort_keys=True)+"\n").encode()
    if args.check:
        expected = Path(__file__).with_name("EXPECTED.json").read_bytes()
        require(encoded == expected, "audit record differs from EXPECTED.json")
        print("PASS", hashlib.sha256(encoded).hexdigest())
    else:
        print(encoded.decode(), end="")


if __name__ == "__main__":
    main()
