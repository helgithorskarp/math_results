#!/usr/bin/env python3
"""Exact checks for the prime-index Ehrhart Fourier criterion.

Only Python's standard library is used.  Cyclotomic elements are tuples of
Fractions in the power basis 1,z,...,z^(p-2), with Phi_p(z)=0.
"""

from fractions import Fraction
from itertools import product
from math import comb
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def scale(c, x):
    return tuple(c * a for a in x)


def reduce_powers(coeffs, p):
    """Reduce a Laurent-free polynomial modulo z^p-1 and Phi_p(z)."""
    cyclic = [Fraction(0) for _ in range(p)]
    for exponent, value in enumerate(coeffs):
        cyclic[exponent % p] += value
    top = cyclic[p - 1]
    return tuple(cyclic[i] - top for i in range(p - 1))


def mul(x, y, p):
    raw = [Fraction(0) for _ in range(len(x) + len(y) - 1)]
    for i, a in enumerate(x):
        for j, b in enumerate(y):
            raw[i + j] += a * b
    return reduce_powers(raw, p)


def one(p):
    return (Fraction(1),) + (Fraction(0),) * (p - 2)


def zeta_power(exponent, p):
    raw = [Fraction(0) for _ in range(exponent % p + 1)]
    raw[exponent % p] = Fraction(1)
    return reduce_powers(raw, p)


def solve_linear(matrix, rhs):
    n = len(rhs)
    aug = [list(map(Fraction, matrix[i])) + [Fraction(rhs[i])]
           for i in range(n)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        q = aug[col][col]
        aug[col] = [v / q for v in aug[col]]
        for row in range(n):
            if row == col:
                continue
            q = aug[row][col]
            if q:
                aug[row] = [a - q * b
                            for a, b in zip(aug[row], aug[col])]
    return tuple(aug[i][-1] for i in range(n))


def inverse(x, p):
    degree = p - 1
    columns = []
    for j in range(degree):
        basis = tuple(Fraction(i == j) for i in range(degree))
        columns.append(mul(x, basis, p))
    matrix = [[columns[j][i] for j in range(degree)]
              for i in range(degree)]
    return solve_linear(matrix, one(p))


def power(x, exponent, p):
    answer = one(p)
    while exponent:
        if exponent & 1:
            answer = mul(answer, x, p)
        x = mul(x, x, p)
        exponent //= 2
    return answer


def interpolate(points):
    """Return monomial coefficients through exact Vandermonde solving."""
    matrix = [[Fraction(x) ** j for j in range(len(points))]
              for x, _ in points]
    return solve_linear(matrix, [y for _, y in points])


def simplex_product_count(p, g, f, n):
    base = sum(comb(n - p * y + g - 1, g - 1)
               for y in range(n // p + 1))
    return (n + 1) ** f * base


def coefficient_by_residue(p, g, f):
    degree = g + f
    result = []
    for residue in range(p):
        points = []
        for m in range(degree + 1):
            n = residue + p * m
            points.append((n, simplex_product_count(p, g, f, n)))
        coeffs = interpolate(points)
        # One unused point detects an interpolation or counting error.
        n = residue + p * (degree + 1)
        value = sum(coeffs[j] * n ** j for j in range(degree + 1))
        require(value == simplex_product_count(p, g, f, n),
                f"unused count mismatch for {(p, g, f, residue)}")
        result.append(coeffs[f])
    return result


def dft(values, h, p):
    answer = tuple(Fraction(0) for _ in range(p - 1))
    for residue, value in enumerate(values):
        answer = add(answer, scale(value, zeta_power(h * residue, p)))
    return scale(Fraction(1, p), answer)


def predicted_unique(p, g, h):
    denominator = power(add(one(p), scale(-1, zeta_power(h, p))), g, p)
    return scale(Fraction(1, p), inverse(denominator, p))


def matrix_image(matrix, p):
    rows = len(matrix)
    columns = len(matrix[0])
    return {
        tuple(sum(matrix[i][j] * x[j] for j in range(columns)) % p
              for i in range(rows))
        for x in product(range(p), repeat=columns)
    }


def left_kernel_lines(matrix, p):
    rows = len(matrix)
    vectors = []
    for epsilon in product(range(p), repeat=rows):
        if not any(epsilon):
            continue
        if all(sum(epsilon[i] * matrix[i][j] for i in range(rows)) % p == 0
               for j in range(len(matrix[0]))):
            first = next(a for a in epsilon if a)
            inverse_first = pow(first, -1, p)
            normalized = tuple(a * inverse_first % p for a in epsilon)
            if normalized not in vectors:
                vectors.append(normalized)
    return vectors


def active_image_checks():
    """Compare character and direct residue membership on small systems."""
    systems = 0
    rhs_checks = 0
    proper_checks = 0
    full_support_misses = 0
    for p in (2, 3, 5):
        for rows, columns in ((2, 2), (2, 3), (3, 3)):
            candidates = product(range(p), repeat=rows * columns)
            # A deterministic bounded prefix plus diagonal witnesses keeps
            # this exact check small while covering rectangular systems.
            selected = []
            for flat in candidates:
                matrix = [flat[i * columns:(i + 1) * columns]
                          for i in range(rows)]
                lines = left_kernel_lines(matrix, p)
                if len(lines) == 1:
                    selected.append((matrix, lines[0]))
                    if len(selected) == 24:
                        break
            for matrix, epsilon in selected:
                systems += 1
                image = matrix_image(matrix, p)
                for b in product(range(p), repeat=rows):
                    rhs_checks += 1
                    by_character = sum(epsilon[i] * b[i]
                                       for i in range(rows)) % p == 0
                    require((b in image) == by_character,
                            f"image character mismatch for {(p, matrix, b)}")
                if all(epsilon):
                    for omitted in range(rows):
                        projected = {u[:omitted] + u[omitted + 1:]
                                     for u in image}
                        proper_checks += 1
                        require(len(projected) == p ** (rows - 1),
                                f"proper projection failed for {(p, matrix)}")
                else:
                    full_support_misses += 1
    return systems, rhs_checks, proper_checks, full_support_misses


def cancellation_checks():
    checks = 0
    for h in (1, 2):
        q_plus = inverse(power(add(one(3), scale(-1, zeta_power(h, 3))),
                               3, 3), 3)
        q_minus = inverse(power(add(one(3), scale(-1, zeta_power(2 * h, 3))),
                                3, 3), 3)
        require(add(q_plus, q_minus) == (Fraction(0), Fraction(0)),
                f"cancellation failed in mode {h}")
        checks += 1
    return checks


def main():
    simplex_cases = 0
    mode_checks = 0
    residue_polynomials = 0
    unused_values = 0
    for p in (2, 3, 5, 7):
        for g in range(1, 5):
            for f in range(3):
                values = coefficient_by_residue(p, g, f)
                simplex_cases += 1
                residue_polynomials += p
                unused_values += p
                for h in range(1, p):
                    require(dft(values, h, p) == predicted_unique(p, g, h),
                            f"Fourier mismatch for {(p, g, f, h)}")
                    mode_checks += 1

    systems, rhs_checks, proper_checks, misses = active_image_checks()
    cancellation = cancellation_checks()
    report = {
        "active_image": {
            "full_support_systems": systems - misses,
            "partial_support_systems": misses,
            "proper_projection_checks": proper_checks,
            "residue_membership_checks": rhs_checks,
            "systems": systems,
        },
        "cancellation": {
            "p3_g3_nonzero_modes": cancellation,
        },
        "simplex_products": {
            "cases": simplex_cases,
            "cyclotomic_mode_checks": mode_checks,
            "primes": [2, 3, 5, 7],
            "residue_polynomials": residue_polynomials,
            "unused_count_values": unused_values,
        },
        "status": "all exact checks passed",
    }
    expected_path = Path(__file__).with_name("expected.json")
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    require(report == expected, "report differs from expected.json")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
