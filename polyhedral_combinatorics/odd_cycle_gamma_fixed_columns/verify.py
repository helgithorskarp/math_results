#!/usr/bin/env python3
"""Exact audits for fixed-column odd-cycle gamma recurrences.

CPython 3.11+, standard library only.  Every asserted equality uses integers.
The asymptotic estimates themselves are proved in PROOF.md; this program audits
their finite algebraic inputs without floating-point root approximation.
"""

from functools import cache
from itertools import product
import json
from math import comb


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def trim(poly):
    poly = list(poly)
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def add(left, right, scale=1):
    answer = [0] * max(len(left), len(right))
    for index in range(len(answer)):
        answer[index] = (left[index] if index < len(left) else 0)
        if index < len(right):
            answer[index] += scale * right[index]
    return trim(answer)


def multiply(left, right):
    answer = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for k, b in enumerate(right):
            answer[i + k] += a * b
    return trim(answer)


def power(poly, exponent):
    answer = [1]
    base = poly
    while exponent:
        if exponent & 1:
            answer = multiply(answer, base)
        base = multiply(base, base)
        exponent //= 2
    return answer


def generalized_binomial(a, degree):
    """Polynomial binomial(a, degree), valid for every integer a."""
    numerator = 1
    for offset in range(degree):
        numerator *= a - offset
    denominator = 1
    for value in range(2, degree + 1):
        denominator *= value
    require(numerator % denominator == 0, "nonintegral generalized binomial")
    return numerator // denominator


def factor_coefficient(m, j, degree):
    """[t^degree] (1-t)^(m+2) (1+t)^(2j+1-m)."""
    return sum((-1) ** a * comb(m + 2, a)
               * generalized_binomial(2 * j + 1 - m, degree - a)
               for a in range(degree + 1))


def determinant_table(maximum_n):
    table = [[1], [1, -1], [1, -1, -1], [1, -2, -1, 1]]
    require(maximum_n >= 3, "maximum_n must be at least three")
    for n in range(4, maximum_n + 1):
        table.append(add(multiply([2, 0, -1], table[n - 2]), table[n - 4], -1))
    return table


DETERMINANTS = determinant_table(32)


def characteristic(n):
    """Ascending coefficients of det(X I-A_n)."""
    return list(reversed(DETERMINANTS[n]))


@cache
def power_sum(n, exponent):
    """Newton recurrence for tr(A_n**exponent)."""
    if exponent == 0:
        return n
    determinant = DETERMINANTS[n]
    values = [n] + [0] * exponent
    for r in range(1, exponent + 1):
        values[r] = -r * (determinant[r] if r < len(determinant) else 0)
        values[r] -= sum(determinant[k] * values[r - k]
                         for k in range(1, min(r - 1, len(determinant) - 1) + 1))
    return values[exponent]


def matrix_multiply(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(len(right)))
             for j in range(len(right[0]))] for i in range(len(left))]


def matrix_power(matrix, exponent):
    size = len(matrix)
    answer = [[int(i == j) for j in range(size)] for i in range(size)]
    base = matrix
    while exponent:
        if exponent & 1:
            answer = matrix_multiply(answer, base)
        base = matrix_multiply(base, base)
        exponent //= 2
    return answer


def direct_power_sum(n, exponent):
    matrix = [[int(i + j <= n - 1) for j in range(n)] for i in range(n)]
    result = matrix_power(matrix, exponent)
    return sum(result[i][i] for i in range(n))


def gamma_formula(m, j):
    return sum(factor_coefficient(m, j, j - n) * power_sum(n + 1, m)
               for n in range(j + 1))


def numerator_direct(m):
    """Numerator H_m=(1-t^2)^(m+1) sum p_m(n+1)t^n."""
    values = [power_sum(n + 1, m) for n in range(2 * m + 2)]
    answer = []
    for degree in range(2 * m + 2):
        answer.append(sum((-1) ** k * comb(m + 1, k) * values[degree - 2 * k]
                          for k in range(min(m + 1, degree // 2) + 1)))
    return trim(answer)


def divide_plus(poly):
    quotient = [poly[0]]
    for value in poly[1:-1]:
        quotient.append(value - quotient[-1])
    require(quotient[-1] == poly[-1], "division by 1+t has a remainder")
    return trim(quotient)


def gamma_from_palindromic(poly):
    require(poly == poly[::-1], "input is not palindromic")
    degree = len(poly) - 1
    remainder = poly[:]
    answer = []
    for j in range(degree // 2 + 1):
        coefficient = remainder[j]
        answer.append(coefficient)
        for k in range(degree - 2 * j + 1):
            remainder[j + k] -= coefficient * comb(degree - 2 * j, k)
    require(not any(remainder), "gamma reconstruction failed")
    return answer


def annihilator(j):
    answer = [1]
    for n in range(1, j + 2):
        answer = multiply(answer, power(characteristic(n), j + 2 - n))
    return answer


def finite_differences(values, depth):
    row = list(values)
    for _ in range(depth):
        row = [right - left for left, right in zip(row, row[1:])]
    return row


def run():
    trace_audits = 0
    for n in range(1, 8):
        for m in range(0, 13):
            require(power_sum(n, m) == direct_power_sum(n, m),
                    f"trace mismatch at n={n}, m={m}")
            trace_audits += 1

    coefficient_audits = 0
    for j in range(1, 8):
        for degree in range(j + 1):
            start = 2 * j + 3
            values = [factor_coefficient(m, j, degree)
                      for m in range(start, start + degree + 2)]
            require(all(value == 0 for value in finite_differences(values, degree + 1)),
                    f"coefficient degree exceeds {degree} at j={j}")
            leading_difference = finite_differences(values, degree)[0]
            require(leading_difference == (-2) ** degree,
                    f"wrong leading coefficient at j={j}, r={degree}")
            coefficient_audits += 1
        require(factor_coefficient(37, j, 0) == 1, "c0 identity")
        require(factor_coefficient(37, j, 1) == 2 * j - 75, "c1 identity")

    controls = {
        3: [1, -1],
        5: [1, 2, 1],
        7: [1, 16, 27, -1],
        9: [1, 59, 429, 392, 1],
        11: [1, 178, 3768, 14584, 8661, -1],
        13: [1, 496, 25499, 264622, 632065, 261838, 1],
    }
    bridge_audits = 0
    for m, expected in controls.items():
        q = (m - 1) // 2
        formula = [gamma_formula(m, j) for j in range(q + 1)]
        require(formula == expected, f"gamma control mismatch at m={m}")
        reduced = numerator_direct(m)
        for _ in range(m):
            reduced = divide_plus(reduced)
        require(gamma_from_palindromic(reduced) == formula,
                f"direct numerator mismatch at m={m}")
        bridge_audits += 1

    recurrence_audits = 0
    recurrence_orders = {}
    for j in range(1, 7):
        recurrence = annihilator(j)
        order = len(recurrence) - 1
        require(order == comb(j + 3, 3), f"annihilator order at j={j}")
        recurrence_orders[str(j)] = order
        for start in range(0, 10):
            total = sum(coefficient * gamma_formula(start + shift, j)
                        for shift, coefficient in enumerate(recurrence))
            require(total == 0, f"recurrence mismatch at j={j}, m={start}")
            recurrence_audits += 1

    layer_audits = 0
    for j in range(1, 9):
        for m in range(2 * j + 1, 80, 2):
            leading_two = (power_sum(j + 1, m)
                           - (2 * m - 2 * j + 1) * power_sum(j, m))
            remainder = sum(factor_coefficient(m, j, j - n) * power_sum(n + 1, m)
                            for n in range(j - 1))
            require(gamma_formula(m, j) == leading_two + remainder,
                    f"two-layer split mismatch at j={j}, m={m}")
            layer_audits += 1

    return {
        "status": "PASS",
        "arithmetic": "exact Python integers; no floating point",
        "transfer_trace_audits": trace_audits,
        "coefficient_polynomial_audits": coefficient_audits,
        "direct_gamma_bridge_audits": bridge_audits,
        "fixed_column_recurrence_audits": recurrence_audits,
        "annihilator_orders": recurrence_orders,
        "two_spectral_layer_audits": layer_audits,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
