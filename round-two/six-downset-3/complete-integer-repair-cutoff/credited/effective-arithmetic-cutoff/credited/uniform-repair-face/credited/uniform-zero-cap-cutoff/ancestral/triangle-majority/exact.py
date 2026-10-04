"""Literal matrix checks adapted from the credited cubic-seven source.

Exact integer Schur congruence and characteristic polynomials are two
algorithms by the same author; they are not independent peer review.
"""
from fractions import Fraction as F
import hashlib
import json
from math import lcm


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':'), sort_keys=True).encode()).hexdigest()


def integral(matrix):
    n = len(matrix)
    require(n > 0 and all(len(row) == n for row in matrix), 'nonsquare matrix')
    require(all(isinstance(x, (int, F)) for row in matrix for x in row), 'inexact matrix entry')
    require(all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(n)),
            'asymmetric matrix')
    denominator = lcm(*(F(x).denominator for row in matrix for x in row))
    return [[int(F(x)*denominator) for x in row] for row in matrix], denominator


def schur_psd(matrix):
    """Fraction-free Schur congruences, including singular-pivot checks."""
    a, _ = integral(matrix)
    n, previous, rank = len(a), 1, 0
    for k in range(n):
        pivot = a[k][k]
        require(pivot >= 0, 'negative Schur pivot')
        if not pivot:
            require(not any(a[k][j] for j in range(k+1, n)),
                    'zero Schur pivot with a nonzero row')
            continue
        for i in range(k+1, n):
            for j in range(i, n):
                numerator = pivot*a[i][j]-a[i][k]*a[k][j]
                a[i][j], remainder = divmod(numerator, previous)
                require(remainder == 0, 'nonexact fraction-free division')
                a[j][i] = a[i][j]
        previous = pivot
        rank += 1
    return rank


def polynomial_psd(matrix):
    """Faddeev--LeVerrier plus exact nonnegative coefficient criterion."""
    a, denominator = integral(matrix)
    n = len(a)
    b = [[int(i == j) for j in range(n)] for i in range(n)]
    coefficients = [1]
    for k in range(1, n+1):
        c = [[sum(a[i][h]*b[h][j] for h in range(n)) for j in range(n)]
             for i in range(n)]
        coefficient, remainder = divmod(-sum(c[i][i] for i in range(n)), k)
        require(remainder == 0, 'nonintegral characteristic coefficient')
        coefficients.append(coefficient)
        for i in range(n):
            c[i][i] += coefficient
        b = c
    require(not any(x for row in b for x in row), 'Cayley-Hamilton residual')
    require(all((-1)**j*x >= 0 for j, x in enumerate(coefficients)),
            'negative-root coefficient criterion fails')
    return max(j for j, x in enumerate(coefficients) if x), digest(coefficients), denominator


def lift(c):
    rows = [sum(row) for row in c]
    return [[1+sum(rows)]+[1-x for x in rows]] + [
        [1-rows[i]]+[1+x for x in row] for i, row in enumerate(c)]
