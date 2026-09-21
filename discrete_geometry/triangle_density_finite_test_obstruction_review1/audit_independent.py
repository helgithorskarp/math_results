#!/usr/bin/env python3
"""Independent exact audit of the finite triangle-suite obstruction.

The target constructs norm polynomials and relative norms by multiplying
Galois conjugates in a bit-mask model of a multiquadratic field.  This audit
imports no target module or fixture.  It instead obtains the norm polynomial
as the characteristic polynomial of multiplication by theta, and obtains
each relative norm as a determinant over the relevant quadratic subfield.

CPython 3.11+, standard library only; all calculations use integers or
fractions.Fraction and all checks remain active under ``python -O``.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from json import dumps
from math import isqrt, lcm


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rational_square_root(value):
    value = F(value)
    if value < 0:
        return None
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if numerator * numerator == value.numerator and denominator * denominator == value.denominator:
        return F(numerator, denominator)
    return None


def mask_product(radicands, mask):
    value = 1
    for index, radicand in enumerate(radicands):
        if mask & (1 << index):
            value *= radicand
    return value


def class_coordinates(radicand, basis):
    """Return mask,z with prod(basis[mask]) = z^2 radicand, if present."""
    for mask in range(1 << len(basis)):
        scale = rational_square_root(F(mask_product(basis, mask), radicand))
        if scale is not None:
            return mask, scale
    return None


def square_class_basis(determinants):
    basis = []
    for determinant in determinants:
        determinant = F(determinant)
        radicand = -determinant.numerator * determinant.denominator
        if class_coordinates(radicand, basis) is None:
            basis.append(radicand)
    return basis or [-1]


def matrix_multiply(first, second):
    return [
        [sum(first[row][inner] * second[inner][column]
             for inner in range(len(second)))
         for column in range(len(second[0]))]
        for row in range(len(first))
    ]


def identity(size):
    return [[F(row == column) for column in range(size)] for row in range(size)]


def theta_multiplication_matrix(radicands):
    """Multiplication by sum sqrt(r_i) on the monomial radical basis."""
    size = 1 << len(radicands)
    matrix = [[F(0) for _ in range(size)] for _ in range(size)]
    for column in range(size):
        for index, radicand in enumerate(radicands):
            bit = 1 << index
            row = column ^ bit
            matrix[row][column] += radicand if column & bit else 1
    return matrix


def characteristic_polynomial(matrix):
    """Faddeev--LeVerrier coefficients, low degree first."""
    size = len(matrix)
    accumulator = identity(size)
    descending = []
    for degree in range(1, size + 1):
        product_matrix = matrix_multiply(matrix, accumulator)
        coefficient = -sum(product_matrix[index][index] for index in range(size)) / degree
        descending.append(coefficient)
        accumulator = [row[:] for row in product_matrix]
        for index in range(size):
            accumulator[index][index] += coefficient
    require(all(value.denominator == 1 for value in descending),
            "nonintegral characteristic polynomial")
    return list(reversed(descending)) + [F(1)]


def polynomial_value(coefficients, value):
    result = F(0)
    for coefficient in reversed(coefficients):
        result = result * value + coefficient
    return result


def polynomial_multiply(first, second):
    result = [F(0)] * (len(first) + len(second) - 1)
    for i, left in enumerate(first):
        for j, right in enumerate(second):
            result[i + j] += left * right
    return result


def polynomial_square_part(coefficients):
    """Polynomial part Q of sqrt(P) at infinity and R=P-Q^2."""
    coefficients = list(map(F, coefficients))
    degree = len(coefficients) - 1
    require(degree >= 2 and degree % 2 == 0 and coefficients[-1] == 1,
            "monic positive even degree required")
    half = degree // 2
    square_part = [F(0)] * half + [F(1)]
    for index in range(half - 1, -1, -1):
        current_square = polynomial_multiply(square_part, square_part)
        square_part[index] = (coefficients[half + index] - current_square[half + index]) / 2
    square = polynomial_multiply(square_part, square_part)
    remainder = [left - right for left, right in zip(coefficients, square)]
    while remainder and remainder[-1] == 0:
        remainder.pop()
    require(remainder and len(remainder) <= half,
            "polynomial square or invalid square-part construction")
    denominator = lcm(*(coefficient.denominator for coefficient in square_part))
    lower_square_bound = sum(abs(coefficient) for coefficient in square_part[:-1])
    remainder_size = sum(abs(coefficient) for coefficient in remainder)
    root_bound = 1 + sum(abs(coefficient) for coefficient in remainder[:-1]) / abs(remainder[-1])
    bound = max(F(1), 2 * lower_square_bound,
                2 * denominator * remainder_size, root_bound)
    threshold = bound.numerator // bound.denominator + 1
    return square_part, remainder, denominator, threshold


def qadd(left, right):
    return left[0] + right[0], left[1] + right[1]


def qneg(value):
    return -value[0], -value[1]


def qmul(left, right, radicand):
    return (left[0] * right[0] + radicand * left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def qdiv(left, right, radicand):
    norm = right[0] * right[0] - radicand * right[1] * right[1]
    require(norm != 0, "division by zero in quadratic field")
    numerator = qmul(left, (right[0], -right[1]), radicand)
    return numerator[0] / norm, numerator[1] / norm


def quadratic_determinant(matrix, radicand):
    """Gaussian determinant over Q(sqrt(radicand))."""
    matrix = [[(F(value[0]), F(value[1])) for value in row] for row in matrix]
    size = len(matrix)
    determinant = (F(1), F(0))
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if matrix[row][column] != (0, 0)), None)
        require(pivot is not None, "singular relative multiplication matrix")
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            determinant = qneg(determinant)
        pivot_value = matrix[column][column]
        determinant = qmul(determinant, pivot_value, radicand)
        for row in range(column + 1, size):
            if matrix[row][column] == (0, 0):
                continue
            factor = qdiv(matrix[row][column], pivot_value, radicand)
            for inner in range(column, size):
                matrix[row][inner] = qadd(
                    matrix[row][inner],
                    qneg(qmul(factor, matrix[column][inner], radicand)),
                )
    return determinant


def relative_norm_by_determinant(radicands, value, subfield_mask):
    """N_{K/Q(sqrt(v))}(value-theta), v=product on subfield_mask."""
    require(subfield_mask, "nontrivial quadratic subfield required")
    pivot_bit = (subfield_mask & -subfield_mask).bit_length() - 1
    representatives = [mask for mask in range(1 << len(radicands))
                       if not mask & (1 << pivot_bit)]
    locations = {mask: index for index, mask in enumerate(representatives)}
    dimension = len(representatives)
    relative_matrix = [[(F(0), F(0)) for _ in range(dimension)]
                       for _ in range(dimension)]
    for column, basis_mask in enumerate(representatives):
        relative_matrix[column][column] = (F(value), F(0))
        for index, radicand in enumerate(radicands):
            bit = 1 << index
            coefficient = -F(radicand if basis_mask & bit else 1)
            output_mask = basis_mask ^ bit
            if not output_mask & (1 << pivot_bit):
                row = locations[output_mask]
                relative_matrix[row][column] = qadd(
                    relative_matrix[row][column], (coefficient, F(0)))
            else:
                representative = output_mask ^ subfield_mask
                conversion = F(mask_product(radicands,
                                            representative & subfield_mask))
                # e_rep * sqrt(v) = conversion * e_output.
                row = locations[representative]
                relative_matrix[row][column] = qadd(
                    relative_matrix[row][column],
                    (F(0), coefficient / conversion),
                )
    subfield_radicand = mask_product(radicands, subfield_mask)
    return quadratic_determinant(relative_matrix, subfield_radicand)


def determinant_of_form(form):
    return form[0][0] * form[1][1] - form[0][1] * form[1][0]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def similarity_matrix(form, determinant, u, v):
    a, b = form[0]
    change = [[F(1), b / a], [F(0), F(1, 1) / a]]
    inverse = [[F(1), -b], [F(0), a]]
    norm_matrix = [[u, -determinant * v], [v, u]]
    return matrix_multiply(matrix_multiply(inverse, norm_matrix), change)


def check_similarity(form, matrix, multiplier):
    transformed = matrix_multiply(matrix_multiply(transpose(matrix), form), matrix)
    require(transformed == [[multiplier * entry for entry in row] for row in form],
            "similitude identity failed")
    require(matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0] == multiplier,
            "similitude determinant failed")


def form_value(form, vector):
    return sum(vector[i] * form[i][j] * vector[j]
               for i in range(2) for j in range(2))


def factor_integer(value):
    factors = {}
    divisor = 2
    value = abs(value)
    while divisor * divisor <= value:
        while value % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            value //= divisor
        divisor += 1
    if value > 1:
        factors[value] = factors.get(value, 0) + 1
    return factors


def valuation(value, prime):
    value = F(value)
    require(value != 0, "zero has no finite valuation")
    def integer_valuation(integer):
        exponent = 0
        integer = abs(integer)
        while integer % prime == 0:
            integer //= prime
            exponent += 1
        return exponent
    return integer_valuation(value.numerator) - integer_valuation(value.denominator)


def odd_valuation_prime(value):
    value = F(value)
    primes = sorted(set(factor_integer(value.numerator)) |
                    set(factor_integer(value.denominator)))
    return next(prime for prime in primes if valuation(value, prime) % 2)


def obstruction_d(prime):
    if prime == 2:
        return 3
    squares = {value * value % prime for value in range(prime)}
    return next(d for d in range(1, prime) if (-d) % prime not in squares)


def matrix_suite_audit(forms):
    forms = [[[F(entry) for entry in row] for row in form] for form in forms]
    determinants = [determinant_of_form(form) for form in forms]
    require(all(form[0][1] == form[1][0] and form[0][0] > 0 and determinant > 0
                for form, determinant in zip(forms, determinants)),
            "non-positive-definite audit form")
    radicands = square_class_basis(determinants)
    theta_matrix = theta_multiplication_matrix(radicands)
    polynomial = characteristic_polynomial(theta_matrix)
    square_part, remainder, denominator, threshold = polynomial_square_part(polynomial)

    # This audit deliberately chooses the first small nonsquare norm value;
    # the target instead always uses its sufficient asymptotic threshold.
    chosen = None
    for integer in range(1, threshold + 3):
        norm = polynomial_value(polynomial, integer)
        if norm > 0 and norm.denominator == 1 and rational_square_root(norm) is None:
            chosen = integer, norm
            break
    require(chosen is not None, "no small nonsquare norm value found")
    integer, common_norm = chosen
    epsilon = F(1, 1000)
    numerator = 1
    while True:
        floor_value = isqrt(common_norm.numerator * numerator * numerator)
        if floor_value and F(1, floor_value) < epsilon:
            break
        numerator *= 2
    rational_factor = F(numerator, floor_value)
    near_identity_square = common_norm * rational_factor * rational_factor
    require(1 < near_identity_square < (1 + epsilon) ** 2,
            "rational rescaling missed the near-identity interval")
    require(rational_square_root(near_identity_square) is None,
            "rational rescaling made the irrational scale rational")

    records = []
    sample_vectors = [(F(x, denominator_value), F(y, denominator_value))
                      for denominator_value in (1, 2, 3)
                      for x, y in product(range(-2, 3), repeat=2)]
    for form, determinant in zip(forms, determinants):
        field_radicand = -determinant.numerator * determinant.denominator
        subfield_mask, scale = class_coordinates(field_radicand, radicands)
        relative = relative_norm_by_determinant(radicands, integer, subfield_mask)
        u = relative[0]
        v = relative[1] * scale * determinant.denominator
        require(u * u + determinant * v * v == common_norm,
                "relative determinant is not the common norm")
        similitude = similarity_matrix(form, determinant, u, v)
        check_similarity(form, similitude, common_norm)
        near_similitude = [[rational_factor * entry for entry in row]
                           for row in similitude]
        check_similarity(form, near_similitude, near_identity_square)
        for vector in sample_vectors:
            image = tuple(sum(similitude[row][column] * vector[column]
                              for column in range(2)) for row in range(2))
            require(form_value(form, image) == common_norm * form_value(form, vector),
                    "sampled rational value-set identity failed")
        records.append({
            "determinant": str(determinant),
            "subfield_mask": subfield_mask,
            "u": str(u),
            "v": str(v),
        })

    # Verify the written eventual nonsquare certificate at and after its
    # threshold, separately from the deliberately small chosen value.
    square = polynomial_multiply(square_part, square_part)
    padded_remainder = remainder + [F(0)] * (len(square) - len(remainder))
    require([left + right for left, right in zip(square, padded_remainder)] == polynomial,
            "square-part identity failed")
    for test_value in range(threshold, threshold + 5):
        value = polynomial_value(polynomial, test_value)
        require(value > 0 and value.denominator == 1 and rational_square_root(value) is None,
                "nonsquare threshold check failed")

    return {
        "field_degree": len(theta_matrix),
        "radicands": radicands,
        "norm_polynomial": [str(value) for value in polynomial],
        "small_nonsquare_t": integer,
        "small_common_norm": str(common_norm),
        "threshold": threshold,
        "square_part_denominator": denominator,
        "near_identity_squared_scale": str(near_identity_square),
        "forms": records,
    }


def main():
    suites = {
        "empty": [],
        "single_and_nonsquare_class": [
            [[F(2), F(0)], [F(0), F(2)]],
        ],
        "dependent_fields_and_negative_form": [
            [[F(1), F(0)], [F(0), F(1)]],
            [[F(1), F(0)], [F(0), F(2)]],
            [[F(1), F(0)], [F(0), F(3)]],
            [[F(1), F(0)], [F(0), F(6)]],
            [[F(2), F(0)], [F(0), F(6)]],
        ],
        "rational_basis_changes": [
            [[F(1, 2), F(1, 3)], [F(1, 3), F(5, 2)]],
            [[F(3), F(1)], [F(1), F(2)]],
            [[F(2), F(1)], [F(1), F(2)]],
            [[F(5), F(-2)], [F(-2), F(1)]],
        ],
    }
    suite_results = {name: matrix_suite_audit(forms) for name, forms in suites.items()}

    # The empty suite and the one-field case are the smallest quantifier
    # boundaries.  Repeated/squareful radicands must not inflate field degree.
    require(suite_results["empty"]["field_degree"] == 2, "empty-suite convention")
    require(suite_results["single_and_nonsquare_class"]["field_degree"] == 2,
            "squareful radicand changed the quadratic field")
    require(suite_results["dependent_fields_and_negative_form"]["field_degree"] == 8,
            "dependent determinant classes changed compositum degree")

    # The rational negative instance 2x^2+6y^2 does not represent one: every
    # nonzero value of x^2+3y^2 has even 2-adic valuation.
    bounded = [F(value, denominator) for denominator in (1, 2, 3, 4)
               for value in range(-5, 6)]
    negative_instance_checks = 0
    for x, y in product(bounded, repeat=2):
        if x == 0 and y == 0:
            continue
        norm = x * x + 3 * y * y
        require(valuation(norm, 2) % 2 == 0, "dyadic negative-instance parity")
        require(2 * norm != 1, "negative rational form represented one")
        negative_instance_checks += 1

    # Odd-valuation missed triangles include primes in numerators and
    # denominators.  Exhaustive residue checks certify each local form.
    valuation_certificates = set()
    numerator_cases = denominator_cases = 0
    for numerator in range(1, 19):
        for denominator in range(1, 19):
            scale = F(numerator, denominator)
            if rational_square_root(scale) is not None:
                continue
            prime = odd_valuation_prime(scale)
            d = obstruction_d(prime)
            if prime == 2:
                primitive_values = []
                for x, y in product(range(8), repeat=2):
                    if x % 2 or y % 2:
                        primitive_values.append(valuation(F(x * x + 3 * y * y), 2))
                require(set(primitive_values) == {0, 2}, "dyadic local control")
            else:
                zeros = [(x, y) for x, y in product(range(prime), repeat=2)
                         if (x * x + d * y * y) % prime == 0]
                require(zeros == [(0, 0)], "odd-prime local form is isotropic")
            valuation_certificates.add((prime, d))
            numerator_cases += valuation(scale, prime) > 0
            denominator_cases += valuation(scale, prime) < 0
    require(numerator_cases and denominator_cases, "valuation sign boundary omitted")

    # The explicit smallest two-field illustration and its missed triangle.
    require(13 == 2 * 2 + 3 * 3 == 1 * 1 + 3 * 2 * 2, "13 common norm")
    squared_scale = F(325, 324)
    require(1 < squared_scale < F(101, 100) ** 2,
            "explicit scale is not near identity")
    squares_mod_13 = {value * value % 13 for value in range(13)}
    require((-2) % 13 not in squares_mod_13, "explicit T_2 obstruction failed")

    # An irrational Gram entry stays irrational after multiplying by any
    # nonzero rational squared scale.  Pairs encode a+b*sqrt(2).
    # These are the independent entries of diag(1,sqrt(2)), a positive
    # definite Gram matrix with an irrational entry.
    irrational_gram = ((F(1), F(0)), (F(0), F(0)), (F(0), F(1)))
    irrational_status_checks = 0
    for scale in (F(1, 7), F(2), F(325, 324), F(17, 5)):
        scaled = tuple((scale * rational, scale * irrational)
                       for rational, irrational in irrational_gram)
        require(any(irrational for _, irrational in scaled),
                "rational scaling erased irrational Gram data")
        irrational_status_checks += 1

    # Fractional polynomial-part adversary for the written effective lemma.
    adversary = list(map(F, (1, 1, 1, 1, 1)))
    part, remainder, denominator, threshold = polynomial_square_part(adversary)
    require(denominator == 8 and remainder == [F(55, 64), F(5, 8)],
            "fractional square-part adversary changed")
    for integer in range(threshold, threshold + 20):
        require(rational_square_root(polynomial_value(adversary, integer)) is None,
                "fractional polynomial adversary attained a square")

    result_without_digest = {
        "arithmetic": "fractions.Fraction; no floating point",
        "explicit_example": {
            "common_norm": 13,
            "missed_d": 2,
            "squared_scale": str(squared_scale),
        },
        "fractional_polynomial_control": {
            "square_part": [str(value) for value in part],
            "remainder": [str(value) for value in remainder],
            "threshold": threshold,
            "tested_values": 20,
        },
        "irrational_status_checks": irrational_status_checks,
        "negative_instance_checks": negative_instance_checks,
        "suite_results": suite_results,
        "valuation_local_forms": [list(values) for values in sorted(valuation_certificates)],
        "valuation_nonsquare_scales": numerator_cases + denominator_cases,
        "valuation_with_denominator_prime": denominator_cases,
        "status": "pass",
    }
    digest = sha256(dumps(result_without_digest, sort_keys=True,
                          separators=(",", ":")).encode()).hexdigest()
    result = dict(result_without_digest)
    result["independent_digest_sha256"] = digest
    print(dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
