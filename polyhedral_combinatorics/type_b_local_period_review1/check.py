#!/usr/bin/env python3
"""Independent exact checks for the type-B local-period review.

No code or expected data from the reviewed package is imported.  The main
fixtures form a two-parameter family built from a canonical unbalanced signed
cycle and a free cube.  Counts use a closed stars-and-bars summation, with
small cases checked by literal tuple enumeration.
"""

from fractions import Fraction
from itertools import product
from math import comb, factorial
from pathlib import Path
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trim(poly):
    poly = list(poly)
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def poly_add(left, right):
    result = [Fraction(0)] * max(len(left), len(right))
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += value
    return trim(result)


def poly_scale(poly, scalar):
    return trim([scalar * value for value in poly])


def poly_multiply(left, right):
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            result[i + j] += x * y
    return trim(result)


def poly_evaluate(poly, value):
    result = Fraction(0)
    for coefficient in reversed(poly):
        result = result * value + coefficient
    return result


def interpolate(nodes, values):
    require(len(nodes) == len(values) and len(set(nodes)) == len(nodes),
            "bad interpolation data")
    result = [Fraction(0)]
    for i, (node, value) in enumerate(zip(nodes, values)):
        basis = [Fraction(1)]
        denominator = Fraction(1)
        for j, other in enumerate(nodes):
            if i == j:
                continue
            basis = poly_multiply(basis, [-other, 1])
            denominator *= node - other
        result = poly_add(result, poly_scale(basis, Fraction(value) / denominator))
    return trim(result)


def canonical_cycle_count(rank, dilation):
    """Count the canonical unbalanced-cycle polytope at one dilation.

    Coordinates lie in [-n,n] and obey
      x0+x1<=n, x1<=x2<=...<=x_(r-1)<=x0.
    For fixed x0,x1, stars and bars counts the remaining chain.
    """
    require(rank >= 2 and dilation >= 0, "bad cycle parameters")
    total = 0
    for x0 in range(-dilation, dilation + 1):
        top = min(x0, dilation - x0)
        for x1 in range(-dilation, top + 1):
            total += comb(x0 - x1 + rank - 2, rank - 2)
    return total


def canonical_cycle_literal(rank, dilation):
    total = 0
    for values in product(range(-dilation, dilation + 1), repeat=rank):
        if values[0] + values[1] > dilation:
            continue
        if any(values[i] > values[i + 1] for i in range(1, rank - 1)):
            continue
        if values[-1] > values[0]:
            continue
        total += 1
    return total


def family_count(rank, free_dimension, dilation):
    return canonical_cycle_count(rank, dilation) * (dilation + 1) ** free_dimension


def numerator(dimension, even_poly, odd_poly):
    def value(n):
        if n < 0:
            return Fraction(0)
        return poly_evaluate(even_poly if n % 2 == 0 else odd_poly, n)

    coefficients = []
    for degree in range(2 * dimension + 2):
        coefficient = Fraction(0)
        for j in range(min(dimension + 1, degree // 2) + 1):
            coefficient += (-1) ** j * comb(dimension + 1, j) * value(degree - 2 * j)
        coefficients.append(coefficient)
    for degree in range(2 * dimension + 2, 2 * dimension + 6):
        coefficient = sum(
            Fraction((-1) ** j * comb(dimension + 1, j)) * value(degree - 2 * j)
            for j in range(dimension + 2)
        )
        require(coefficient == 0, "nonzero numerator tail")
    return trim(coefficients)


def divide_at_minus_one(poly):
    poly = trim(poly)
    order = 0
    while poly_evaluate(poly, -1) == 0:
        require(len(poly) > 1, "zero polynomial")
        quotient = [Fraction(0)] * (len(poly) - 1)
        quotient[-1] = poly[-1]
        for i in range(len(poly) - 2, 0, -1):
            quotient[i - 1] = poly[i] - quotient[i]
        require(poly[0] == quotient[0], "synthetic-division remainder")
        poly = trim(quotient)
        order += 1
    return order, poly_evaluate(poly, -1)


def fraction_text(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def check_family(rank, free_dimension):
    dimension = rank + free_dimension
    evens = [2 * i for i in range(dimension + 1)]
    odds = [2 * i + 1 for i in range(dimension + 1)]
    even_poly = interpolate(evens, [family_count(rank, free_dimension, n) for n in evens])
    odd_poly = interpolate(odds, [family_count(rank, free_dimension, n) for n in odds])

    for n in (2 * dimension + 2, 2 * dimension + 3):
        selected = even_poly if n % 2 == 0 else odd_poly
        require(poly_evaluate(selected, n) == family_count(rank, free_dimension, n),
                "definition-level holdout failed")

    parity = poly_scale(poly_add(even_poly, poly_scale(odd_poly, -1)), Fraction(1, 2))
    expected_leading = Fraction(1, 2 ** (rank + 1))
    require(len(parity) - 1 == free_dimension, "wrong parity degree")
    require(parity[-1] == expected_leading, "wrong leading parity coefficient")

    h_poly = numerator(dimension, even_poly, odd_poly)
    order, residual = divide_at_minus_one(h_poly)
    expected_residual = 2 ** free_dimension * factorial(free_dimension)
    require(order == rank, "wrong root order")
    require(residual == expected_residual, "wrong residual")

    return {
        "cycle_rank": rank,
        "free_dimension": free_dimension,
        "dimension": dimension,
        "degree_B": len(parity) - 1,
        "leading_B": fraction_text(parity[-1]),
        "root_order": order,
        "residual": fraction_text(residual),
        "holdouts": 2,
    }


def count_stanley(dilation):
    total = 0
    for x in range(dilation // 2 + 1):
        total += (dilation - 2 * x + 1) ** 2
    return total


def count_mcallister_woods_triangle(dilation):
    # D=2 case: conv((0,0),(1,1/2),(2,0)).
    total = 0
    for x in range(2 * dilation + 1):
        for y in range(dilation + 1):
            if 2 * y <= x and x + 2 * y <= 2 * dilation:
                total += 1
    return total


def main():
    literal_checks = 0
    for rank in range(2, 6):
        for dilation in range(4):
            require(canonical_cycle_count(rank, dilation) ==
                    canonical_cycle_literal(rank, dilation),
                    "cycle stars-and-bars count disagrees with literal enumeration")
            literal_checks += 1

    families = [check_family(rank, free)
                for rank in range(2, 8) for free in range(4)]

    for n in range(18):
        require(count_stanley(n) == comb(n + 3, 3), "Stanley count mismatch")
        require(count_mcallister_woods_triangle(n) == comb(n + 2, 2),
                "McAllister--Woods triangle count mismatch")

    canonical = json.dumps(families, sort_keys=True, separators=(",", ":"))
    output = {
        "implementation": "independent cycle-chain summation and exact interpolation",
        "imports_reviewed_code": False,
        "cycle_cube_families": {
            "cases": len(families),
            "cycle_ranks": list(range(2, 8)),
            "free_dimensions": list(range(4)),
            "leading_B_by_cycle_rank": {
                str(rank): fraction_text(Fraction(1, 2 ** (rank + 1)))
                for rank in range(2, 8)
            },
            "residual_by_free_dimension": {
                str(free): str(2 ** free * factorial(free))
                for free in range(4)
            },
            "definition_level_holdouts": 2 * len(families),
        },
        "literal_cycle_checks": literal_checks,
        "negative_controls": {
            "Stanley_nonsimple_type_B": {
                "dilations_checked": 18,
                "denominator": 2,
                "period": 1,
                "formula": "binom(n+3,3)",
            },
            "McAllister_Woods_simple_non_type_B_triangle": {
                "dilations_checked": 18,
                "denominator": 2,
                "period": 1,
                "formula": "binom(n+2,2)",
            },
        },
        "family_record_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "status": "PASS",
    }
    expected_path = Path(__file__).with_name("expected.json")
    if expected_path.exists():
        expected = json.loads(expected_path.read_text())
        require(output == expected, "computed record differs from expected.json")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
