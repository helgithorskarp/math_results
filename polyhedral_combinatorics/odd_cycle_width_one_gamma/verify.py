#!/usr/bin/env python3
"""Exact checks for the odd-cycle spectral-to-gamma bridge.

CPython 3.11+, standard library only.  All arithmetic used for claims is
integer or Fraction arithmetic.  Sturm sequences certify root locations;
no floating point approximation is used.
"""
from fractions import Fraction as F
from itertools import permutations, product
import json
from math import comb


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def trim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p or [0]


def add(p, q, scale=1):
    out = [F(0)] * max(len(p), len(q))
    for i in range(len(out)):
        out[i] = (p[i] if i < len(p) else 0) + scale * (q[i] if i < len(q) else 0)
    return trim(out)


def mul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return trim(out)


def derivative(p):
    return trim([i * p[i] for i in range(1, len(p))])


def divrem(p, q):
    p, q = list(map(F, trim(p))), list(map(F, trim(q)))
    require(q != [0], "polynomial division by zero")
    if len(p) < len(q):
        return [F(0)], p
    quotient = [F(0)] * (len(p) - len(q) + 1)
    while p != [0] and len(p) >= len(q):
        shift = len(p) - len(q)
        coefficient = p[-1] / q[-1]
        quotient[shift] = coefficient
        for i, value in enumerate(q):
            p[i + shift] -= coefficient * value
        p = trim(p)
    return trim(quotient), p


def determinant_polynomial_direct(n):
    """Permutation definition of det(I-z A_n), for small independent audits."""
    if n == 0:
        return [F(1)]
    answer = [F(0)]
    for sigma in permutations(range(n)):
        inversions = sum(sigma[i] > sigma[j] for i in range(n) for j in range(i + 1, n))
        term = [F(1)]
        for i, j in enumerate(sigma):
            entry = [F(int(i == j)), F(-int(i + j <= n - 1))]
            term = mul(term, entry)
        answer = add(answer, term, -1 if inversions % 2 else 1)
    return answer


def determinant_table(maximum_n):
    table = [[1], [1, -1], [1, -1, -1], [1, -2, -1, 1]]
    require(maximum_n >= 3, "maximum_n must be at least three")
    for n in range(4, maximum_n + 1):
        twice_minus_z2 = [2, 0, -1]
        table.append([int(x) for x in add(mul(twice_minus_z2, table[n - 2]),
                                                  table[n - 4], -1)])
    return table


DETERMINANTS = determinant_table(110)


def power_sum(n, exponent):
    """Newton recurrence for tr(A_n**exponent)."""
    d = DETERMINANTS[n]
    p = [0] * (exponent + 1)
    for r in range(1, exponent + 1):
        p[r] = -r * (d[r] if r < len(d) else 0)
        p[r] -= sum(d[k] * p[r - k] for k in range(1, min(r, len(d) - 1) + 1))
    return p[exponent]


def matrix_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def matrix_power(a, exponent):
    n = len(a)
    answer = [[int(i == j) for j in range(n)] for i in range(n)]
    base = a
    while exponent:
        if exponent & 1:
            answer = matrix_mul(answer, base)
        base = matrix_mul(base, base)
        exponent //= 2
    return answer


def transfer_power_sum(n, exponent):
    a = [[int(i + j <= n - 1) for j in range(n)] for i in range(n)]
    p = matrix_power(a, exponent)
    return sum(p[i][i] for i in range(n))


def definition_count(m, dilation):
    return sum(all(x[i] + x[(i + 1) % m] <= dilation for i in range(m))
               for x in product(range(dilation + 1), repeat=m))


def factor_coefficient(m, j, degree):
    """[t^degree] (1-t)^(m+2) (1+t)^(2j+1-m)."""
    exponent = 2 * j + 1 - m
    total = 0
    for a in range(degree + 1):
        if a > m + 2:
            continue
        b = degree - a
        if exponent >= 0:
            plus = comb(exponent, b) if b <= exponent else 0
        else:
            # (1+t)^(-s): coefficient (-1)^b C(s+b-1,b)
            s = -exponent
            plus = (-1) ** b * comb(s + b - 1, b)
        total += (-1) ** a * comb(m + 2, a) * plus
    return total


def gamma_vector(m):
    require(m >= 3 and m % 2 == 1, "odd m at least three required")
    q = (m - 1) // 2
    counts = [power_sum(n + 1, m) for n in range(q + 1)]
    return [sum(factor_coefficient(m, j, j - n) * counts[n] for n in range(j + 1))
            for j in range(q + 1)]


def numerator_direct(m):
    values = [power_sum(n + 1, m) for n in range(2 * m + 2)]
    return trim([sum((-1) ** k * comb(m + 1, k) * values[n - 2 * k]
                     for k in range(min(m + 1, n // 2) + 1))
                 for n in range(2 * m + 2)])


def divide_plus(p):
    quotient = [p[0]]
    for value in p[1:-1]:
        quotient.append(value - quotient[-1])
    require(quotient[-1] == p[-1], "nonzero remainder on division by 1+t")
    return trim(quotient)


def gamma_from_palindromic(p):
    require(p == p[::-1], "gamma input is not palindromic")
    degree = len(p) - 1
    remaining = p[:]
    answer = []
    for j in range(degree // 2 + 1):
        value = remaining[j]
        answer.append(value)
        for k in range(degree - 2 * j + 1):
            remaining[j + k] -= value * comb(degree - 2 * j, k)
    require(not any(remaining), "gamma reconstruction failed")
    return answer


def variations(signs):
    signs = [s for s in signs if s]
    return sum(a != b for a, b in zip(signs, signs[1:]))


def sign_at_infinity(p, positive):
    sign = 1 if p[-1] > 0 else -1
    if not positive and (len(p) - 1) % 2:
        sign = -sign
    return sign


def sturm_location_counts(p):
    """Return distinct negative and positive real-root counts, and squarefree degree."""
    p = list(map(F, trim(p)))
    sequence = [p, derivative(p)]
    while sequence[-1] != [0]:
        _, remainder = divrem(sequence[-2], sequence[-1])
        if remainder == [0]:
            break
        sequence.append([-x for x in remainder])
    gcd = sequence[-1]
    squarefree, remainder = divrem(p, gcd)
    require(remainder == [0], "Sturm gcd division failed")
    v_minus = variations([sign_at_infinity(s, False) for s in sequence])
    v_plus = variations([sign_at_infinity(s, True) for s in sequence])
    v_zero = variations([(1 if s[0] > 0 else -1 if s[0] < 0 else 0) for s in sequence])
    return v_minus - v_zero, v_zero - v_plus, len(squarefree) - 1


def run():
    determinant_audits = 0
    for n in range(0, 8):
        require(list(map(F, DETERMINANTS[n])) == determinant_polynomial_direct(n),
                f"determinant mismatch at n={n}")
        determinant_audits += 1

    newton_audits = direct_count_audits = 0
    for n in range(1, 8):
        for exponent in range(1, 12):
            require(power_sum(n, exponent) == transfer_power_sum(n, exponent),
                    f"Newton trace mismatch at {(n, exponent)}")
            newton_audits += 1
    for m, dilation in [(3, 0), (3, 1), (3, 2), (5, 1), (5, 2), (7, 1)]:
        require(power_sum(dilation + 1, m) == definition_count(m, dilation),
                f"definition count mismatch at {(m, dilation)}")
        direct_count_audits += 1

    expected = {
        3: [1, -1],
        5: [1, 2, 1],
        7: [1, 16, 27, -1],
        9: [1, 59, 429, 392, 1],
        11: [1, 178, 3768, 14584, 8661, -1],
        13: [1, 496, 25499, 264622, 632065, 261838, 1],
    }
    bridge_audits = 0
    for m, target in expected.items():
        gamma = gamma_vector(m)
        require(gamma == target, f"gamma control mismatch at m={m}")
        numerator = numerator_direct(m)
        reduced = numerator
        for _ in range(m):
            reduced = divide_plus(reduced)
        require(gamma_from_palindromic(reduced) == gamma,
                f"Lagrange/direct gamma mismatch at m={m}")
        bridge_audits += 1

    sign_cases = 0
    for m in range(3, 202, 2):
        gamma = gamma_vector(m)
        q = (m - 1) // 2
        require(gamma[0] == 1, "constant gamma coefficient")
        if m >= 5:
            require(gamma[1] > 0 and gamma[2] > 0, "positive-prefix theorem")
        require(gamma[-1] == (-1) ** q, "terminal gamma sign")
        if m % 4 == 1:
            require(all(value > 0 for value in gamma), "conjectural sign pattern failed")
        else:
            require(all(value > 0 for value in gamma[:-1]) and gamma[-1] == -1,
                    "conjectural sign pattern failed")
        sign_cases += 1

    sturm_cases = repeated_cases = 0
    for m in range(3, 42, 2):
        gamma = gamma_vector(m)
        negative, positive, squarefree_degree = sturm_location_counts(gamma)
        if m == 5:
            require((negative, positive, squarefree_degree) == (1, 0, 1),
                    "Gamma_5 repeated-root control")
            repeated_cases += 1
        elif m % 4 == 1:
            require((negative, positive) == (squarefree_degree, 0),
                    f"root-location pattern failed at m={m}")
        else:
            require((negative, positive) == (squarefree_degree - 1, 1),
                    f"root-location pattern failed at m={m}")
        require(squarefree_degree == (m - 1) // 2 if m != 5 else squarefree_degree == 1,
                f"unexpected repeated root at m={m}")
        sturm_cases += 1

    # Formula (18), including its independent scalar recurrence.
    lucas = [2, 1]
    trace3 = [3, 2, 6]
    for n in range(2, 202):
        lucas.append(lucas[-1] + lucas[-2])
    for n in range(3, 202):
        trace3.append(2 * trace3[-1] + trace3[-2] - trace3[-3])
    prefix_formula_audits = 0
    for m in range(5, 202, 2):
        gamma = gamma_vector(m)
        require(gamma[1] == lucas[m] - 2 * m + 1, "gamma_1 formula")
        require(gamma[2] == trace3[m] + (3 - 2 * m) * lucas[m] + 2 * m * m - 6 * m + 1,
                "gamma_2 formula")
        prefix_formula_audits += 1

    return {
        "status": "PASS",
        "arithmetic": "exact Python int/Fraction; no floating point",
        "determinant_permutation_audits": determinant_audits,
        "newton_matrix_power_audits": newton_audits,
        "definition_count_audits": direct_count_audits,
        "direct_gamma_bridge_audits": bridge_audits,
        "prefix_formula_cases": prefix_formula_audits,
        "coefficient_sign_cases_through_m": 201,
        "coefficient_sign_cases": sign_cases,
        "sturm_root_cases_through_m": 41,
        "sturm_root_cases": sturm_cases,
        "known_repeated_root_cases": repeated_cases,
        "gamma_201_digits_by_coefficient": [len(str(abs(x))) for x in gamma_vector(201)],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))

