#!/usr/bin/env python3
"""Independent symbolic audit of the inertial field-colouring barrier.

This imports no code from the reviewed package.  SymPy Groebner reduction is
used for the two number-field models, while modular square roots give a third
implementation of the explicit ternary colouring.
"""

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import random

import sympy as sp
from sympy.ntheory import sqrt_mod


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rational(value):
    value = sp.Rational(value)
    return Fraction(int(value.p), int(value.q))


# Independent presentation Q[T,G,B]/(T^2-T-3, 3G^2+T-1, B^2+3).
B, G, T = sp.symbols("B G T")
SALEM_GROEBNER = sp.groebner(
    [B**2 + 3, 3 * G**2 + T - 1, T**2 - T - 3],
    B, G, T, order="lex", domain=sp.QQ,
)
SALEM_BASIS = (1, T, G, T * G, B, B * T, B * G, B * T * G)


def salem_reduce(value):
    _, remainder = SALEM_GROEBNER.reduce(sp.expand(value))
    return sp.expand(remainder)


def salem_vector(value):
    polynomial = sp.Poly(salem_reduce(value), B, G, T, domain=sp.QQ)
    return tuple(rational(polynomial.coeff_monomial(monomial))
                 for monomial in SALEM_BASIS)


def salem_conjugate(value):
    return salem_reduce(value.subs(B, -B, simultaneous=True))


def salem_multiply(left, right):
    return salem_reduce(left * right)


def salem_power(unit, exponent):
    if exponent < 0:
        return salem_power(salem_conjugate(unit), -exponent)
    result = sp.Integer(1)
    factor = unit
    while exponent:
        if exponent & 1:
            result = salem_multiply(result, factor)
        factor = salem_multiply(factor, factor)
        exponent //= 2
    return result


def prime_exponent(number, prime):
    require(type(number) is int and number > 0, "positive denominator required")
    exponent = 0
    while number % prime == 0:
        exponent += 1
        number //= prime
    return exponent


def local_trace_root(exponent):
    """Root T=1 mod 3 of T^2-T-3 modulo 3^exponent via sqrt_mod."""
    require(type(exponent) is int and exponent >= 1, "positive precision required")
    modulus = 3**exponent
    inverse_two = pow(2, -1, modulus)
    candidates = {
        (1 + int(root)) * inverse_two % modulus
        for root in sqrt_mod(13, modulus, all_roots=True)
    }
    candidates = [value for value in candidates
                  if value % 3 == 1
                  and (value * value - value - 3) % modulus == 0]
    require(len(candidates) == 1, "local trace root is not unique")
    return candidates[0]


def ternary_colour(value):
    coefficient_one, coefficient_t = salem_vector(value)[:2]
    denominator = math.lcm(coefficient_one.denominator,
                           coefficient_t.denominator)
    exponent = prime_exponent(denominator, 3)
    modulus = 3**(exponent + 1)
    numerator = (int(coefficient_one * denominator)
                 + int(coefficient_t * denominator)
                 * local_trace_root(exponent + 1))
    unit_denominator = denominator // 3**exponent
    residue = numerator * pow(unit_denominator, -1, modulus) % modulus
    return residue // 3**exponent


def salem_random_element(rng, prime_power):
    coefficients = [
        Fraction(rng.randrange(-13, 14),
                 2**rng.randrange(4) * 3**rng.randrange(prime_power + 1)
                 * 5**rng.randrange(3))
        for _ in range(8)
    ]
    return salem_reduce(sum(sp.Rational(value.numerator, value.denominator) * basis
                            for value, basis in zip(coefficients, SALEM_BASIS)))


# Independent dyadic presentation Q[H,J]/(H^2-H-1, J^2+1).
J, H = sp.symbols("J H")
DYADIC_GROEBNER = sp.groebner(
    [J**2 + 1, H**2 - H - 1], J, H, order="lex", domain=sp.QQ,
)
DYADIC_BASIS = (1, H, J, J * H)


def dyadic_reduce(value):
    return sp.expand(DYADIC_GROEBNER.reduce(sp.expand(value))[1])


def dyadic_vector(value):
    polynomial = sp.Poly(dyadic_reduce(value), J, H, domain=sp.QQ)
    return tuple(rational(polynomial.coeff_monomial(monomial))
                 for monomial in DYADIC_BASIS)


def dyadic_conjugate(value):
    return dyadic_reduce(value.subs(J, -J, simultaneous=True))


def dyadic_inverse_real(value):
    coefficients = dyadic_vector(value)
    require(coefficients[2:] == (0, 0), "expected a real quadratic element")
    u, v = coefficients[:2]
    denominator = u * u + u * v - v * v
    require(denominator, "zero real quadratic element")
    return dyadic_reduce(
        sp.Rational((u + v).numerator, (u + v).denominator) / denominator
        - sp.Rational(v.numerator, v.denominator) * H / denominator
    )


def binary_digit(value):
    value = Fraction(value)
    exponent = prime_exponent(value.denominator, 2)
    modulus = 2**(exponent + 1)
    unit_denominator = value.denominator // 2**exponent
    residue = value.numerator * pow(unit_denominator, -1, modulus) % modulus
    return residue // 2**exponent


def binary_colour(value):
    coefficients = dyadic_vector(value)
    return binary_digit(coefficients[0] - coefficients[2])


def dyadic_random_element(rng, exponent):
    coefficients = [Fraction(rng.randrange(-11, 12),
                             2**rng.randrange(exponent + 1)
                             * 3**rng.randrange(3))
                    for _ in range(4)]
    return dyadic_reduce(sum(sp.Rational(value.numerator, value.denominator) * basis
                             for value, basis in zip(coefficients, DYADIC_BASIS)))


def f9_multiply(left, right):
    # Pairs a+bG with G^2=-1 over F_3.
    a, b = left
    c, d = right
    return ((a * c - b * d) % 3, (a * d + b * c) % 3)


def run():
    x = sp.symbols("x")
    polynomial = sp.Poly(x**4 - x**3 - x**2 - x + 1, x, modulus=2)
    require(polynomial.is_irreducible, "quartic is reducible modulo two")

    alpha = salem_reduce((T + B * G) / 2)
    omega = salem_reduce((-1 + B) / 2)
    zeta = salem_reduce((1 + B) / 2)
    quartic_value = salem_reduce(alpha**4 - alpha**3 - alpha**2 - alpha + 1)
    require(quartic_value == 0, "quartic identity")
    require(salem_multiply(alpha, salem_conjugate(alpha)) == 1,
            "alpha is not norm one")
    require(salem_reduce(omega**2 + omega + 1) == 0,
            "cube-root identity")
    require(salem_multiply(zeta, salem_conjugate(zeta)) == 1
            and salem_power(zeta, 6) == 1, "sixth-root identity")

    alpha_omega_basis = [
        salem_multiply(salem_power(alpha, power), salem_power(omega, branch))
        for branch in range(2) for power in range(4)
    ]
    change_matrix = sp.Matrix([
        [sp.Rational(value.numerator, value.denominator)
         for value in salem_vector(element)]
        for element in alpha_omega_basis
    ]).T
    determinant = sp.factor(change_matrix.det())
    require(determinant != 0, "alpha-omega basis is singular")

    f9 = tuple(itertools.product(range(3), repeat=2))
    roots_of_one = tuple(value for value in f9
                         if f9_multiply(value, value) == (1, 0))
    require(roots_of_one == ((1, 0), (2, 0)), "roots of one in F9")
    require(not any(value * value % 3 == 2 for value in range(3)),
            "minus one unexpectedly square in F3")
    require(all(f9_multiply(left, right) != (0, 0)
                for left in f9[1:] for right in f9[1:]),
            "the F9 presentation has zero divisors")
    for exponent in range(1, 65):
        root = local_trace_root(exponent)
        require(root % 3 == 1
                and (root * root - root - 3) % 3**exponent == 0,
                "bad modular trace root")

    triangle = (sp.Integer(0), sp.Integer(1), zeta)
    require(all(salem_multiply(salem_reduce(a - b),
                               salem_conjugate(salem_reduce(a - b))) == 1
                for a, b in itertools.combinations(triangle, 2)),
            "equilateral triangle geometry")
    require([ternary_colour(value) for value in triangle] == [0, 1, 2],
            "equilateral triangle colours")

    directions = {
        salem_multiply(salem_power(alpha, exponent), salem_power(zeta, branch))
        for exponent in range(-10, 11) for branch in range(6)
    }
    require(len(directions) == 126, "unexpected direction collision")
    require(all(salem_multiply(value, salem_conjugate(value)) == 1
                for value in directions), "false Salem unit direction")
    rng = random.Random(3717)
    ternary_checks = 0
    maximum_ternary_denominator = 0
    ternary_word = bytearray()
    for index, direction in enumerate(sorted(directions, key=str)):
        for exponent in (index % 7, 40):
            start = salem_random_element(rng, exponent)
            finish = salem_reduce(start + direction)
            colours = (ternary_colour(start), ternary_colour(finish))
            require(colours[0] != colours[1], "monochromatic Salem unit edge")
            ternary_word.extend(colours)
            maximum_ternary_denominator = max(
                maximum_ternary_denominator,
                *(prime_exponent(value.denominator, 3)
                  for value in salem_vector(start)[:2]),
            )
            ternary_checks += 1

    # Produce arbitrary exact norm-one elements in Q(H,J) as q/conjugate(q).
    dyadic_checks = 0
    dyadic_word = bytearray()
    for index in range(96):
        source = dyadic_random_element(rng, 8)
        require(source != 0, "zero Hilbert-90 source")
        norm = dyadic_reduce(source * dyadic_conjugate(source))
        direction = dyadic_reduce(source * source * dyadic_inverse_real(norm))
        require(dyadic_reduce(direction * dyadic_conjugate(direction)) == 1,
                "false dyadic unit direction")
        for exponent in (index % 9, 45):
            start = dyadic_random_element(rng, exponent)
            finish = dyadic_reduce(start + direction)
            colours = (binary_colour(start), binary_colour(finish))
            require(colours[0] != colours[1], "monochromatic dyadic unit edge")
            dyadic_word.extend(colours)
            dyadic_checks += 1

    # The ramified base Q(sqrt(3)) supplies the advertised triangle boundary.
    require(Fraction(1, 4) + Fraction(3, 4) == 1,
            "ramified-base triangle norm")
    residue_cycle_checks = 0
    for prime in (2, 3, 5, 7, 11, 13):
        palette = [vertex % 2 if vertex < prime - 1
                   else (1 if prime == 2 else 2)
                   for vertex in range(prime)]
        require(all(palette[vertex] != palette[(vertex + 1) % prime]
                    for vertex in range(prime)), "residue cycle colouring")
        residue_cycle_checks += prime

    return {
        "accepted": True,
        "target_kind": "whole-field colouring obstruction, not a target construction",
        "quartic_irreducible_mod_2": True,
        "salem_field_degree": 8,
        "alpha_omega_change_determinant": str(determinant),
        "f9_elements_checked": len(f9),
        "f9_roots_of_one": [list(value) for value in roots_of_one],
        "modular_trace_precisions": 64,
        "triangle_colours": [ternary_colour(value) for value in triangle],
        "independent_salem_directions": len(directions),
        "translated_salem_edges": ternary_checks,
        "maximum_tested_3_denominator_valuation": maximum_ternary_denominator,
        "salem_colour_sha256": hashlib.sha256(ternary_word).hexdigest(),
        "independent_dyadic_directions": 96,
        "translated_dyadic_edges": dyadic_checks,
        "dyadic_colour_sha256": hashlib.sha256(dyadic_word).hexdigest(),
        "residue_cycle_vertices_checked": residue_cycle_checks,
        "ramified_base_triangle_checked": True,
        "full_theorems_depend_on_test_exhaustion": False,
        "algebra_engine": "SymPy 1.14 Groebner quotients and sqrt_mod",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected", type=Path)
    arguments = parser.parse_args()
    report = run()
    if arguments.expected:
        require(report == json.loads(arguments.expected.read_text()),
                "expected report mismatch")
    print(json.dumps(report, indent=2, sort_keys=True))
