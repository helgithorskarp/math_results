#!/usr/bin/env python3
"""Exact arithmetic supporting proof.md; this is not a formal proof.

Domains: Q[z,u] for the sharpness family, Q[z,u]/(z^9-1) for its
implicit root velocity, and Q[c] for the radial inequality. All coefficients
use fractions.Fraction. No numerical root finding or external package.
"""

from fractions import Fraction as F
from math import comb
import json


def polynomial(terms):
    return {key: F(value) for key, value in terms.items() if value}


def add(*polynomials):
    result = {}
    for p in polynomials:
        for key, value in p.items():
            result[key] = result.get(key, F(0)) + value
    return polynomial(result)


def scale(p, coefficient):
    return polynomial({key: F(coefficient) * value for key, value in p.items()})


def multiply(p, q):
    result = {}
    for (a, b), x in p.items():
        for (c, d), y in q.items():
            key = (a + c, b + d)
            result[key] = result.get(key, F(0)) + x * y
    return polynomial(result)


def derivative(p, variable):
    result = {}
    for exponents, value in p.items():
        power = exponents[variable]
        if power:
            key = list(exponents)
            key[variable] -= 1
            result[tuple(key)] = value * power
    return polynomial(result)


def at_z_one(p):
    result = {}
    for (_, b), value in p.items():
        result[(0, b)] = result.get((0, b), F(0)) + value
    return polynomial(result)


def at_u_zero(p):
    return polynomial({(a, 0): value for (a, b), value in p.items() if b == 0})


def modulo_ninth_roots(p):
    result = {}
    for (a, b), value in p.items():
        key = (a % 9, b)
        result[key] = result.get(key, F(0)) + value
    return polynomial(result)


def require(condition, name):
    if not condition:
        raise ArithmeticError("Exact check failed: " + name)


def main():
    checks = []
    certificate = {}

    def check(condition, name):
        require(condition, name)
        checks.append(name)

    cap = F(1, 10000)
    certificate["epsilon_energy_cap"] = str(cap)
    b_ratio = 8 * (2 - cap) / (1 - cap) ** 2
    certificate["B_over_epsilon_cap"] = str(b_ratio)
    check(b_ratio < 17, "B/e <= 17")
    # d/de ((2-e)/(1-e)^2) = (3-e)/(1-e)^3 > 0.
    check(3 - cap > 0 and cap < 1, "B/e monotonicity domain")
    check(17 * cap <= F(1, 24) ** 2, "sqrt(B) <= 1/24")
    q_ratio = F(17) / F(23, 24) ** 2
    certificate["Q_over_epsilon_cap"] = str(q_ratio)
    check(q_ratio < 20, "Q <= 20 e")
    check(20 * cap <= F(1, 22) ** 2, "T <= 1/22")
    check(F(8) / (1 - cap) < 9, "radial D <= 9 e")

    coefficients = [
        F(9, 9 - k) * F(comb(8, k), 8) for k in range(2, 9)
    ]
    check([8 * c for c in coefficients] == [36, 84, 126, 126, 84, 36, 9],
          "integrated symmetric coefficients")
    for k in range(2, 9):
        pair_count = F(comb(6, k - 2), comb(k, 2)) * F(7, 2)
        check(pair_count == F(comb(8, k), 8), f"pair-count identity k={k}")
    e_ratio = sum(8 * c * F(1, 22) ** j for j, c in enumerate(coefficients))
    certificate["E_over_Q_eighth_cap"] = str(e_ratio)
    check(e_ratio < 41, "E <= 41 Q/8")
    check(F(41 * 20, 8) <= 103, "E <= 103 e")
    c1_ratio = F(45, 2) * F(1, 22) ** 6
    certificate["c1_over_epsilon_cap"] = str(c1_ratio)
    check(c1_ratio < 1, "|c1| <= e")
    real_lower = F(9, 16) * (16 + 20)
    real_upper = F(9, 8) * 20 / F(21, 22)
    certificate["negative_Re_c8_cap"] = str(real_lower)
    certificate["positive_Re_c8_cap"] = str(real_upper)
    check(real_lower <= 24 and real_upper <= 24, "|Re c8| <= 24 e")
    check(2 * (24 + 103) == 254, "constant coefficient deficit")
    check(8 * 254 + 1 == 2033, "|c8| <= 2033 e")
    check(2033 + 103 < 2200, "coefficient l1 < 2200 e")

    rho = F(1, 100)
    tail = sum(F(comb(9, k)) * rho ** (k - 1) for k in range(2, 10))
    certificate["Rouche_tail_over_rho_cap"] = str(tail)
    check(tail < 1, "|z^9-1| >= 8 rho")
    multiplier = (1 + rho) ** 8 + 1
    certificate["Rouche_perturbation_multiplier"] = str(multiplier)
    check(multiplier < F(21, 10), "Rouche multiplier < 21/10")
    check(F(21, 10) * 2200 < 8000, "strict Rouche separation")
    check(F(4, 9) > 2 * rho, "root disks disjoint")
    check(1000 * F(1, 100000) == rho, "matching epsilon cap")

    check(8 * cap <= F(1, 32) ** 2, "quadratic sqrt(8 delta) <= 1/32")
    check(F(8) / F(31, 32) ** 2 < 9, "quadratic Q <= 9 delta")
    check(9 * cap <= F(1, 32) ** 2, "quadratic T <= 1/32")
    quadratic_real = F(9, 8) * (4 + F(9) / F(31, 32))
    certificate["quadratic_Re_c8_over_delta_cap"] = str(quadratic_real)
    check(quadratic_real < 15, "quadratic |Re c8| <= 15 delta")
    check(F(41 * 9, 8) <= 47, "quadratic E <= 47 delta")
    check(F(81, 8) * F(1, 32) ** 6 < 1, "quadratic |c1| <= delta")
    check(16 * (15 + 47) + 1 == 993, "quadratic |c8| <= 993 delta")
    check(993 + 47 < 1100, "quadratic coefficient l1 < 1100 delta")
    check(500 * F(2, 100000) == rho, "quadratic matching delta cap")
    check(F(21, 10) * 1100 < 8 * 500, "quadratic strict Rouche separation")

    family = polynomial({
        (9, 0): 1,
        (8, 1): -F(27, 4),
        (7, 1): F(9, 7),
        (7, 2): F(81, 7),
        (0, 0): -1,
        (0, 1): F(27, 4) - F(9, 7),
        (0, 2): -F(81, 7),
    })
    factored_derivative = scale(multiply(
        polynomial({(6, 0): 1}),
        polynomial({(2, 0): 1, (1, 1): -6, (0, 1): 1, (0, 2): 9}),
    ), 9)
    check(derivative(family, 0) == factored_derivative,
          "sharpness derivative factorization")
    check(at_z_one(family) == {}, "sharpness distinguished root")
    check(at_u_zero(family) == polynomial({(9, 0): 1, (0, 0): -1}),
          "sharpness limiting polynomial")

    velocity = multiply(polynomial({(1, 0): 1}), polynomial({
        (8, 0): F(3, 4), (7, 0): -F(1, 7),
        (0, 0): -F(3, 4) + F(1, 7),
    }))
    implicit_residual = add(
        multiply(at_u_zero(derivative(family, 0)), velocity),
        at_u_zero(derivative(family, 1)),
    )
    check(modulo_ninth_roots(implicit_residual) == {},
          "implicit root velocity modulo z^9-1")
    # Here the first polynomial variable denotes c = cos(theta).
    radial = polynomial({(1, 0): F(3, 4), (0, 0): -F(3, 4) + F(2, 7),
                         (2, 0): -F(2, 7)})
    radial_factor = multiply(polynomial({(0, 0): 1, (1, 0): -1}),
                             polynomial({(0, 0): -F(13, 28), (1, 0): F(2, 7)}))
    check(radial == radial_factor, "inward radial identity")
    upper_radial = polynomial({(0, 0): -F(5, 28), (1, 0): F(5, 28)})
    nonnegative_difference = scale(multiply(
        polynomial({(0, 0): 1, (1, 0): -1}),
        polynomial({(0, 0): 1, (1, 0): -1}),
    ), F(2, 7))
    check(add(upper_radial, scale(radial, -1)) == nonnegative_difference,
          "strict inward estimate certificate")
    critical_distance_square = add(multiply(
        polynomial({(0, 0): 1, (0, 1): -3}),
        polynomial({(0, 0): 1, (0, 1): -3}),
    ), polynomial({(0, 1): 1}))
    check(critical_distance_square == polynomial({(0, 0): 1, (0, 1): -5, (0, 2): 9}),
          "critical distance square")
    check(add(polynomial({(0, 0): 1}), scale(critical_distance_square, -1))
          == polynomial({(0, 1): 5, (0, 2): -9}),
          "quadratic sharpness deficit numerator")
    check(F(5, 2) > 0 and F(5, 28) > 0, "sharpness nonzero limits")

    # A changed coefficient must break the exact derivative certificate.
    mutated = add(family, polynomial({(8, 1): 1}))
    rejected = False
    try:
        require(derivative(mutated, 0) == factored_derivative, "intentional mutation")
    except ArithmeticError:
        rejected = True
    check(rejected, "incorrect derivative mutation rejected")

    print(json.dumps(certificate, sort_keys=True, indent=2))
    print(f"PASS: {len(checks)} exact checks; derivative mutation rejected.")


if __name__ == "__main__":
    main()
