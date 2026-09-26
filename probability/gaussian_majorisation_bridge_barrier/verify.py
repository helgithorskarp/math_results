#!/usr/bin/env python3
"""Exact compact certificate checks; the continuum proof is in PROOF.md.

No input fixture, floating-point arithmetic, solver, or quadrature is used.
The universal analytic claims are not inferred from finite sampling.
"""

import json
from fractions import Fraction as F


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add(a, b):
    result = [F(0)] * max(len(a), len(b))
    for polynomial in (a, b):
        for i, x in enumerate(polynomial):
            result[i] += x
    while result and result[-1] == 0:
        result.pop()
    return result


def scale(a, c):
    return [c * x for x in a]


def mul(a, b):
    result = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] += x * y
    return result


def derivative(a):
    return [i * a[i] for i in range(1, len(a))]


def hinge(values, threshold):
    return sum((max(x - threshold, 0) for x in values), F(0))


def main():
    p0, q0 = [1, 1, 4, 4, 4, 4], [2, 2, 2, 2, 2, 8]
    p, q = [[F(x, 18) for x in row] for row in (p0, q0)]
    require(sum(p) == sum(q) == 1, "probability normalization")
    require(len(p) == len(q) == 6, "equal support volumes")
    hinge_gap = hinge(q, F(1, 9)) - hinge(p, F(1, 9))
    require(hinge_gap == -F(1, 9), "negative hinge witness")

    # Recover every affine interval from the original height lists.
    pieces = []
    for left, right in ((0, 1), (1, 2), (2, 4), (4, 8), (8, 9)):
        midpoint = F(left + right, 2)
        constant = sum(x for x in q0 if x > midpoint) - sum(x for x in p0 if x > midpoint)
        slope = sum(x > midpoint for x in p0) - sum(x > midpoint for x in q0)
        require(constant + slope * midpoint == hinge(q0, midpoint) - hinge(p0, midpoint),
                "literal affine hinge piece")
        pieces.append([str(left), str(right), str(constant), str(slope)])
    require([row[2:] for row in pieces] == [["0", "0"], ["2", "-2"],
                                          ["-8", "3"], ["8", "-1"], ["0", "0"]],
            "hinge piece coefficients")
    crossing = F(8, 3)
    require(2 < crossing < 4 and hinge(q0, crossing) == hinge(p0, crossing),
            "single sign change")

    # Integrate (constant+slope*r)/r^2 exactly over dyadic endpoints.
    # The representation is constant_term + log2_coefficient * log(2).
    integral = [F(0), F(0)]
    integrals = []
    for left, right, constant, slope in ((1, 2, 2, -2), (2, 4, -8, 3), (4, 8, 8, -1)):
        term = [F(constant, left) - F(constant, right), F(slope)]
        integral = [x + y for x, y in zip(integral, term)]
        integrals.append([str(x) for x in term])
    require(integral == [0, 0], "weighted integral is identically zero")

    power_difference = [-2, 5, -4, 1]
    require(mul(mul([-1, 1], [-1, 1]), [-2, 1]) == power_difference,
            "all-order power factorization")
    numerator, denominator = [0, 5, 0, 1], [2, 0, 4]
    wronskian = add(mul(derivative(numerator), denominator),
                    scale(mul(numerator, derivative(denominator)), -1))
    lhs = add(scale(mul([0, 1], wronskian), 9),
              scale(mul(numerator, denominator), -1))
    rhs = scale(mul([0, 1], mul([-4, 0, 1], [-5, 0, 8])), 4)
    require(lhs == rhs, "uniform Renyi gap derivative factorization")

    square_difference = sum(x*x for x in q) - sum(x*x for x in p)
    require(square_difference == F(1, 18), "second moment gap")
    local_coefficient = 3 * square_difference
    require(local_coefficient == F(1, 6), "near-equality Shannon coefficient")
    for epsilon in (F(1), F(1, 2), F(1, 10), F(1, 100)):
        a = (1 - epsilon) / 6
        pe, qe = [[a + epsilon * x for x in row] for row in (p, q)]
        threshold = a + epsilon / 9
        require(hinge(qe, threshold) - hinge(pe, threshold) == -epsilon / 9,
                "near-equality hinge scaling")

    variance, tail_cap = F(1, 10**8), F(1, 10000)
    require(tail_cap**2 == variance, "Gaussian tail cap squared")
    require(24 * (F(1, 12) + variance) < 3,
            "conditional maximum-entropy constant, using pi<4 and e<3")
    require(F(8, 3)**10 > 10000, "log(10000)<10 from e>8/3")
    one_dimensional_entropy_cap = 17 * tail_cap
    cube_entropy_cap = 3 * one_dimensional_entropy_cap
    entropy_margin = F(1, 18) - cube_entropy_cap
    hinge_upper = hinge_gap + 6 * tail_cap
    require(entropy_margin == F(4541, 90000) > 0, "certified entropy margin")
    require(hinge_upper == -F(4973, 45000) < 0, "certified hinge violation")
    require(F(8)**2 + F(1, 2)**2 + F(1, 2)**2 < F(9)**2,
            "six-cube support radius")

    print(json.dumps({
        "status": "GAUSSIAN_BRIDGE_BARRIER_CHECKS_PASS",
        "arithmetic": "integer and Fraction; exact polynomial identities",
        "p": [str(x) for x in p], "q": [str(x) for x in q],
        "variance": str(variance),
        "hinge_gap_before_smoothing": str(hinge_gap),
        "hinge_gap_strict_upper_bound_after_smoothing": str(hinge_upper),
        "entropy_gap_strict_lower_bound_all_orders_ge_1": str(entropy_margin),
        "cube_Shannon_entropy_strict_upper_bound": str(cube_entropy_cap),
        "unnormalized_hinge_pieces": pieces,
        "weighted_piece_integrals_constant_and_log2": integrals,
        "weighted_total_integral": [str(x) for x in integral],
        "power_difference_coefficients": power_difference,
        "near_equality_Shannon_epsilon2_coefficient": str(local_coefficient),
        "scope": "not a contraction pair; no counterexample to Conjecture 1.1",
        "trust_boundary": "continuum inequalities and PC2 separation require PROOF.md",
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
