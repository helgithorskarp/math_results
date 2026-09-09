#!/usr/bin/env python3
"""Definition-level independent checker for the h4119 collision theorem.

This file imports neither the claimed verifier nor its certificate.  It uses a
different finite-field presentation, searches for all colour functionals from
scratch, enumerates every reduced-polynomial type, and reconstructs the radix
collision-polynomial inventory directly from the 243 digit words.
"""

from itertools import combinations, product
import json
from math import gcd


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def trim(poly):
    poly = tuple(x % 3 for x in poly)
    while poly and poly[-1] == 0:
        poly = poly[:-1]
    return poly


def monic_polynomials(degree):
    return [tuple(coeffs) + (1,) for coeffs in product(range(3), repeat=degree)]


def polynomial_divmod(dividend, divisor):
    dividend = list(trim(dividend))
    divisor = trim(divisor)
    require(divisor and divisor[-1] == 1, "division requires a monic divisor")
    quotient = [0] * max(0, len(dividend) - len(divisor) + 1)
    while len(dividend) >= len(divisor):
        coefficient = dividend[-1] % 3
        shift = len(dividend) - len(divisor)
        quotient[shift] = coefficient
        for j, value in enumerate(divisor):
            dividend[shift + j] = (dividend[shift + j] - coefficient * value) % 3
        dividend = list(trim(dividend))
    return trim(quotient), trim(dividend)


def is_irreducible(poly):
    degree = len(poly) - 1
    for factor_degree in range(1, degree // 2 + 1):
        for factor in monic_polynomials(factor_degree):
            if not polynomial_divmod(poly, factor)[1]:
                return False
    return True


def irreducible_census():
    return [
        poly
        for degree in range(1, 5)
        for poly in monic_polynomials(degree)
        if is_irreducible(poly)
    ]


class FiniteField:
    """GF(3)[x]/(modulus), with base-three coefficient encoding."""

    def __init__(self, modulus):
        self.modulus = tuple(modulus)
        self.degree = len(self.modulus) - 1
        self.order = 3 ** self.degree
        require(is_irreducible(self.modulus), "field modulus is reducible")
        self.vectors = [
            tuple((value // (3 ** j)) % 3 for j in range(self.degree))
            for value in range(self.order)
        ]

    @staticmethod
    def encode(vector):
        return sum((coefficient % 3) * (3 ** j) for j, coefficient in enumerate(vector))

    def subtract(self, left, right):
        return self.encode(a - b for a, b in zip(self.vectors[left], self.vectors[right]))

    def multiply(self, left, right):
        raw = [0] * (2 * self.degree - 1)
        for i, a in enumerate(self.vectors[left]):
            for j, b in enumerate(self.vectors[right]):
                raw[i + j] = (raw[i + j] + a * b) % 3
        for exponent in range(2 * self.degree - 2, self.degree - 1, -1):
            coefficient = raw[exponent] % 3
            for j in range(self.degree):
                raw[exponent - self.degree + j] = (
                    raw[exponent - self.degree + j] - coefficient * self.modulus[j]
                ) % 3
        return self.encode(raw[: self.degree])

    def power(self, value, exponent):
        result = 1
        while exponent:
            if exponent & 1:
                result = self.multiply(result, value)
            value = self.multiply(value, value)
            exponent //= 2
        return result

    def inverse(self, value):
        require(value != 0, "zero has no inverse")
        return self.power(value, self.order - 2)


def dot(weight, vector):
    return sum(a * b for a, b in zip(weight, vector)) % 3


def find_functional(connection_vectors, dimension):
    for weight in product(range(3), repeat=dimension):
        if any(weight) and all(dot(weight, vector) != 0 for vector in connection_vectors):
            return weight
    raise AssertionError("no F3-linear three-colouring exists")


def classify_reduced_polynomials(irreducibles):
    types = set()
    factorizations = 0
    for degree in range(1, 5):
        for poly in monic_polynomials(degree):
            factorizations += 1
            remaining = poly
            factors = []
            while len(remaining) > 1:
                for factor in irreducibles:
                    quotient, remainder = polynomial_divmod(remaining, factor)
                    if not remainder:
                        factors.append(factor)
                        remaining = quotient
                        break
                else:
                    raise AssertionError("irreducible factorization did not complete")
            distinct = sorted(set(factors))
            for left in distinct:
                r = len(left) - 1
                for right in distinct:
                    s = len(right) - 1
                    if left == right:
                        for frobenius_power in range(r):
                            size = gcd(3**r - 1, 3**frobenius_power + 1)
                            types.add(("same", r, frobenius_power, size))
                    else:
                        require(r + s <= 4, "distinct factors exceed degree budget")
                        types.add(("different", r, s, 3 ** gcd(r, s) - 1))
    return factorizations, sorted(types)


def verify_same_factor(case, fields):
    _, degree, frobenius_power, expected_size = case
    field = fields[degree]
    connections = [
        value
        for value in range(1, field.order)
        if field.power(value, 1 + 3**frobenius_power) == 1
    ]
    require(len(connections) == expected_size, "same-factor connection size")
    connection_vectors = [field.vectors[value] for value in connections]
    weight = find_functional(connection_vectors, degree)
    colours = [dot(weight, vector) for vector in field.vectors]
    edges = 0
    for left in range(field.order):
        for right in range(left + 1, field.order):
            if field.subtract(left, right) in connections:
                require(colours[left] != colours[right], "same-factor monochromatic edge")
                edges += 1
    require(edges == field.order * expected_size // 2, "same-factor edge count")
    return {
        "type": list(case),
        "vertices": field.order,
        "pair_tests": field.order * (field.order - 1) // 2,
        "edges": edges,
        "functional": list(weight),
        "modulus_low_first": list(field.modulus),
    }


def verify_different_factors(case, fields):
    _, left_degree, right_degree, expected_size = case
    left_field = fields[left_degree]
    right_field = fields[right_degree]
    if gcd(left_degree, right_degree) == 1:
        connections = [(1, 1), (2, 2)]
    else:
        require(left_degree == right_degree == 2, "unexpected common subfield")
        right_field = left_field
        connections = [
            (value, left_field.inverse(value)) for value in range(1, left_field.order)
        ]
    require(len(connections) == expected_size, "different-factor connection size")
    connection_vectors = [
        left_field.vectors[left] + right_field.vectors[right]
        for left, right in connections
    ]
    dimension = left_degree + right_degree
    weight = find_functional(connection_vectors, dimension)
    vertices = [
        (left, right)
        for left in range(left_field.order)
        for right in range(right_field.order)
    ]
    colours = [
        dot(weight, left_field.vectors[left] + right_field.vectors[right])
        for left, right in vertices
    ]
    connection_set = set(connections)
    edges = 0
    for i, (left_a, right_a) in enumerate(vertices):
        for j in range(i + 1, len(vertices)):
            left_b, right_b = vertices[j]
            difference = (
                left_field.subtract(left_a, left_b),
                right_field.subtract(right_a, right_b),
            )
            if difference in connection_set:
                require(colours[i] != colours[j], "different-factor monochromatic edge")
                edges += 1
    require(edges == len(vertices) * expected_size // 2, "different-factor edge count")
    return {
        "type": list(case),
        "vertices": len(vertices),
        "pair_tests": len(vertices) * (len(vertices) - 1) // 2,
        "edges": edges,
        "functional": list(weight),
        "left_modulus_low_first": list(left_field.modulus),
        "right_modulus_low_first": list(right_field.modulus),
    }


def e_add(left, right):
    return left[0] + right[0], left[1] + right[1]


def e_neg(value):
    return -value[0], -value[1]


def e_multiply(left, right):
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c + b * d


def e_norm(value):
    a, b = value
    return a * a + a * b + b * b


def collision_polynomial_audit():
    zero = (0, 0)
    one = (1, 0)
    digits = (zero, one, (0, 1))
    units = {e_add(left, e_neg(right)) for left in digits for right in digits} - {zero}
    require(len(units) == 6 and all(e_norm(unit) == 1 for unit in units), "digit differences")
    inverses = {}
    for unit in units:
        candidates = [other for other in units if e_multiply(unit, other) == one]
        require(len(candidates) == 1, "unit inverse")
        inverses[unit] = candidates[0]

    labels = list(product(digits, repeat=5))
    normalized = set()
    rootless_constants = set()
    for left, right in combinations(labels, 2):
        coefficients = [e_add(a, e_neg(b)) for a, b in zip(left, right)]
        require(any(value != zero for value in coefficients), "distinct labels gave zero polynomial")
        while coefficients and coefficients[-1] == zero:
            coefficients.pop()
        while coefficients and coefficients[0] == zero:
            coefficients.pop(0)
        inverse_lead = inverses[coefficients[-1]]
        monic = tuple(e_multiply(value, inverse_lead) for value in coefficients)
        require(monic[0] != zero and monic[-1] == one, "collision normalization")
        if len(monic) == 1:
            rootless_constants.add(monic)
        else:
            normalized.add(monic)

    triangle = (zero, one, (0, 1))
    triangle_edges = sum(
        e_norm(e_add(left, e_neg(right))) == 1 for left, right in combinations(triangle, 2)
    )
    return {
        "digit_words": len(labels),
        "normalized_nonzero_root_polynomials": len(normalized),
        "rootless_constant_polynomials": len(rootless_constants),
        "degree_sum": sum(len(poly) - 1 for poly in normalized),
        "maximum_degree": max(len(poly) - 1 for poly in normalized),
        "triangle_unit_edges": triangle_edges,
    }


def main():
    irreducibles = irreducible_census()
    degree_counts = {
        degree: sum(len(poly) - 1 == degree for poly in irreducibles)
        for degree in range(1, 5)
    }
    require(degree_counts == {1: 3, 2: 3, 3: 8, 4: 18}, "irreducible census")
    monic_count, cases = classify_reduced_polynomials(irreducibles)
    require(monic_count == 120 and len(cases) == 16, "case-space completeness")

    # Deliberately choose the last presentation in each degree, rather than the
    # certificate's x^2+1 and x^4+x+2 presentations.
    fields = {
        degree: FiniteField([p for p in irreducibles if len(p) - 1 == degree][-1])
        for degree in range(1, 5)
    }
    require(fields[2].modulus != (1, 0, 1), "quadratic presentation was not independent")
    require(fields[4].modulus != (2, 1, 0, 0, 1), "quartic presentation was not independent")

    verified_cases = []
    for case in cases:
        if case[0] == "same":
            verified_cases.append(verify_same_factor(case, fields))
        else:
            verified_cases.append(verify_different_factors(case, fields))

    collision_audit = collision_polynomial_audit()
    require(
        collision_audit
        == {
            "digit_words": 243,
            "normalized_nonzero_root_polynomials": 2400,
            "rootless_constant_polynomials": 1,
            "degree_sum": 9204,
            "maximum_degree": 4,
            "triangle_unit_edges": 3,
        },
        "collision-polynomial inventory",
    )

    result = {
        "verified": True,
        "arithmetic": "exact Python integers modulo 3",
        "imports_target_code_or_certificate": False,
        "monic_polynomials_audited": monic_count,
        "irreducible_counts_by_degree": degree_counts,
        "residue_case_count": len(cases),
        "residue_cases": verified_cases,
        "collision_audit": collision_audit,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
