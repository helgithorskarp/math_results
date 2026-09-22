#!/usr/bin/env python3
"""Exact discriminant audit for the Ray--West separable-permutation CLT.

Only Python integers and fractions are used.  The quadratic field Q(rho) is
represented by pairs a+b*rho subject to rho^2=6rho-1.
"""

from __future__ import annotations

import json
from fractions import Fraction
from typing import TypeAlias


Monomial: TypeAlias = tuple[int, int]  # powers of z,u
Poly2: TypeAlias = dict[Monomial, int]
Quad: TypeAlias = tuple[Fraction, Fraction]  # a+b*rho


def add(left: Poly2, right: Poly2) -> Poly2:
    answer = dict(left)
    for monomial, coefficient in right.items():
        answer[monomial] = answer.get(monomial, 0) + coefficient
    return {monomial: coefficient for monomial, coefficient in answer.items() if coefficient}


def scale(poly: Poly2, scalar: int) -> Poly2:
    return {monomial: scalar * coefficient for monomial, coefficient in poly.items() if scalar * coefficient}


def multiply(left: Poly2, right: Poly2) -> Poly2:
    answer: Poly2 = {}
    for (zi, ui), x in left.items():
        for (zj, uj), y in right.items():
            monomial = (zi + zj, ui + uj)
            answer[monomial] = answer.get(monomial, 0) + x * y
    return {monomial: coefficient for monomial, coefficient in answer.items() if coefficient}


def derivative(poly: Poly2, variable: int) -> Poly2:
    answer: Poly2 = {}
    for powers, coefficient in poly.items():
        exponent = powers[variable]
        if exponent:
            new_powers = list(powers)
            new_powers[variable] -= 1
            answer[tuple(new_powers)] = exponent * coefficient
    return answer


def specialize_u_one(poly: Poly2) -> list[int]:
    degree = max((z_power for z_power, _ in poly), default=0)
    answer = [0] * (degree + 1)
    for (z_power, _), coefficient in poly.items():
        answer[z_power] += coefficient
    while len(answer) > 1 and answer[-1] == 0:
        answer.pop()
    return answer


def qadd(left: Quad, right: Quad) -> Quad:
    return left[0] + right[0], left[1] + right[1]


def qscale(value: Quad, scalar: Fraction) -> Quad:
    return value[0] * scalar, value[1] * scalar


def qmultiply(left: Quad, right: Quad) -> Quad:
    # (a+b*rho)(c+d*rho), with rho^2=6rho-1.
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c + 6 * b * d


def qinverse(value: Quad) -> Quad:
    a, b = value
    determinant = a * (a + 6 * b) + b * b
    if determinant == 0:
        raise ZeroDivisionError(value)
    return (a + 6 * b) / determinant, -b / determinant


def qdivide(left: Quad, right: Quad) -> Quad:
    return qmultiply(left, qinverse(right))


def evaluate_at_rho(coefficients: list[int]) -> Quad:
    answer: Quad = (Fraction(0), Fraction(0))
    power: Quad = (Fraction(1), Fraction(0))
    rho: Quad = (Fraction(0), Fraction(1))
    for coefficient in coefficients:
        answer = qadd(answer, qscale(power, Fraction(coefficient)))
        power = qmultiply(power, rho)
    return answer


def format_quad(value: Quad) -> str:
    a, b = value
    if a.denominator != 1 or b.denominator != 1:
        return f"({a})+({b})*rho"
    if b == 0:
        return str(a)
    sign = "+" if b > 0 else "-"
    return f"{a}{sign}{abs(b)}*rho"


def construct_discriminant() -> Poly2:
    one: Poly2 = {(0, 0): 1}
    z: Poly2 = {(1, 0): 1}
    u: Poly2 = {(0, 1): 1}
    uz = multiply(u, z)
    h = multiply(add(one, scale(uz, -1)), add(add(one, z), scale(uz, -2)))
    c = multiply(add(one, scale(u, -1)), multiply(z, z))
    b = add(multiply(add(z, scale(one, -1)), h), scale(c, -2))
    e = add(multiply(z, h), scale(c, -2))
    return add(multiply(b, b), scale(multiply(h, e), -4))


def run() -> dict[str, object]:
    discriminant = construct_discriminant()
    specialized = specialize_u_one(discriminant)
    delta = [1, -6, 1]
    one_minus_z_four = [1, -4, 6, -4, 1]
    factored = [0] * 7
    for i, x in enumerate(one_minus_z_four):
        for j, y in enumerate(delta):
            factored[i + j] += x * y
    if specialized != factored:
        raise AssertionError((specialized, factored))

    derivatives: dict[str, Quad] = {}
    derivative_polys = {
        "R_z": derivative(discriminant, 0),
        "R_u": derivative(discriminant, 1),
        "R_zz": derivative(derivative(discriminant, 0), 0),
        "R_zu": derivative(derivative(discriminant, 0), 1),
        "R_uu": derivative(derivative(discriminant, 1), 1),
    }
    for name, poly in derivative_polys.items():
        derivatives[name] = evaluate_at_rho(specialize_u_one(poly))

    expected_derivatives: dict[str, Quad] = {
        "R_z": (Fraction(-96), Fraction(544)),
        "R_u": (Fraction(-272), Fraction(1584)),
        "R_zz": (Fraction(-160), Fraction(1088)),
        "R_zu": (Fraction(-976), Fraction(5696)),
        "R_uu": (Fraction(-2248), Fraction(13104)),
    }
    if derivatives != expected_derivatives:
        raise AssertionError((derivatives, expected_derivatives))
    if derivatives["R_z"] == (0, 0):
        raise AssertionError("dominant discriminant root is not simple")

    rho: Quad = (Fraction(0), Fraction(1))
    rho_prime = qscale(qdivide(derivatives["R_u"], derivatives["R_z"]), Fraction(-1))
    numerator = qadd(
        qadd(
            qmultiply(derivatives["R_zz"], qmultiply(rho_prime, rho_prime)),
            qscale(qmultiply(derivatives["R_zu"], rho_prime), Fraction(2)),
        ),
        derivatives["R_uu"],
    )
    rho_second = qscale(qdivide(numerator, derivatives["R_z"]), Fraction(-1))
    if rho_prime != (Fraction(0), Fraction(-1, 2)):
        raise AssertionError(rho_prime)
    if rho_second != (Fraction(-1, 2), Fraction(7, 2)):
        raise AssertionError(rho_second)

    ratio = qdivide(rho_prime, rho)
    variance = qadd(
        qadd(qscale(qdivide(rho_second, rho), Fraction(-1)), qmultiply(ratio, ratio)),
        qscale(ratio, Fraction(-1)),
    )
    expected_variance = (Fraction(1, 4), Fraction(-1, 2))
    if ratio != (Fraction(-1, 2), Fraction(0)) or variance != expected_variance:
        raise AssertionError((ratio, variance))

    by_u: list[list[int]] = []
    max_u = max(u_power for _, u_power in discriminant)
    max_z = max(z_power for z_power, _ in discriminant)
    for u_power in range(max_u + 1):
        by_u.append([
            discriminant.get((z_power, u_power), 0)
            for z_power in range(max_z + 1)
        ])

    return {
        "status": "PASS",
        "discriminant_coefficients_by_u": by_u,
        "u1_factorization": "(1-z)^4*(1-6*z+z^2)",
        "partials_at_rho": {
            name: format_quad(value) for name, value in derivatives.items()
        },
        "rho_prime": "-rho/2",
        "rho_second": "(-1+7*rho)/2",
        "mean_rate": "1/2",
        "variance_rate": "1/4-rho/2=sqrt(2)-5/4",
        "variance_positive": True,
        "arithmetic": "exact integers and fractions in Q(rho), rho^2-6*rho+1=0",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
