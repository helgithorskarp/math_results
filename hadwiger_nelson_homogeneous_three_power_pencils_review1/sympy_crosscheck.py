#!/usr/bin/env python3
"""Secondary exact lex-Groebner cross-check using SymPy, not target files."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import product
from pathlib import Path

import sympy as sym


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def add(left, right):
    return left[0] + right[0], left[1] + right[1]


def scale(coefficient, value):
    return coefficient * value[0], coefficient * value[1]


def multiply(left, right):
    return (
        sym.expand(left[0] * right[0] - 3 * left[1] * right[1]),
        sym.expand(left[0] * right[1] + left[1] * right[0]),
    )


def norm(value):
    return sym.expand(value[0] ** 2 + 3 * value[1] ** 2)


def equations(signs, variables):
    d, c, b, a = variables
    u = (a, b)
    v = (1 - a, -b)
    w = (c, d)
    omega = (sym.Rational(1, 2), sym.Rational(1, 2))
    omega2 = (-sym.Rational(1, 2), sym.Rational(1, 2))
    epsilon, sigma, tau, kappa, lam = signs
    forms = (
        add(u, w),
        add(v, scale(epsilon, w)),
        add(
            add(u, scale(sigma, multiply(omega, v))),
            scale(tau, multiply(omega2, w)),
        ),
        add(
            add(u, scale(kappa, multiply(omega2, v))),
            scale(lam, multiply(omega, w)),
        ),
    )
    return [sym.expand(norm(value) - 1) for value in forms], tuple(
        map(norm, (u, v, w))
    )


def encode(polynomial, variables):
    return [
        [list(monomial), str(coefficient)]
        for monomial, coefficient in sym.Poly(
            polynomial, *variables, domain=sym.QQ
        ).terms()
    ]


def run():
    variables = sym.symbols("d c b a")
    cases = []
    sizes = Counter()
    for signs in product((-1, 1), repeat=5):
        defining, radii = equations(signs, variables)
        basis = sym.groebner(defining, *variables, order="lex")
        delta = sym.prod(
            radii[i] - radii[j] for i, j in ((0, 1), (0, 2), (1, 2))
        )
        if basis.reduce(delta)[1] == 0:
            classification = "equal_radius"
        else:
            classification = "exceptional_radii"
            for radius in radii:
                target = sym.expand(
                    delta * sym.prod(4 * radius - root for root in (1, 3, 7))
                )
                if basis.reduce(target)[1] != 0:
                    raise ValueError("SymPy exceptional-radius consequence")
        polynomials = [polynomial.as_expr() for polynomial in basis.polys]
        sizes[len(polynomials)] += 1
        cases.append(
            {
                "signs": signs,
                "classification": classification,
                "basis": [encode(polynomial, variables) for polynomial in polynomials],
            }
        )
    counts = Counter(row["classification"] for row in cases)
    if counts != {"equal_radius": 20, "exceptional_radii": 12}:
        raise ValueError("SymPy classification")
    return {
        "status": "PASS",
        "sympy_version": sym.__version__,
        "order": "lex d>c>b>a",
        "sign_cases": len(cases),
        "equal_radius_cases": counts["equal_radius"],
        "exceptional_radius_cases": counts["exceptional_radii"],
        "reduced_basis_size_histogram": {
            str(key): value for key, value in sorted(sizes.items())
        },
        "reduced_lex_bases_sha256": digest(cases),
        "classification_sha256": digest(
            [[row["signs"], row["classification"]] for row in cases]
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    arguments = parser.parse_args()
    result = run()
    if arguments.check_expected:
        expected = json.loads(
            Path(__file__).resolve().with_name("EXPECTED_SYMPY.json").read_text()
        )
        if result != expected:
            raise ValueError("EXPECTED_SYMPY.json mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))
