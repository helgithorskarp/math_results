"""Exact Bareiss PSD/rank arithmetic reused from graph8319/7980."""
from fractions import Fraction as Q
from hashlib import sha256
from math import lcm
import json
from matrices import require, rational


def psd_rank(a):
    """Positive integer Bareiss pivots; exact Schur test including zero residuals.

    This arithmetic mechanism is reused from the credited graph7980 checker.
    The negative controls also compare it to principal-minor definitions.
    """
    require(a and all(len(row) == len(a) for row in a), 'PSD shape')
    d = 1
    for row in a:
        for value in row:
            d = lcm(d, rational(value).denominator)
    z = [[int(rational(value)*d) for value in row] for row in a]
    n = len(z)
    require(all(z[i][j] == z[j][i] for i in range(n) for j in range(n)), 'PSD asymmetry')
    previous, rank = 1, 0
    for k in range(n):
        require(all(z[i][i] >= 0 for i in range(k, n)), 'negative Schur diagonal')
        pivot_row = next((i for i in range(k, n) if z[i][i] > 0), None)
        if pivot_row is None:
            require(all(z[i][j] == 0 for i in range(k, n) for j in range(k, n)),
                    'zero diagonal with nonzero residual')
            break
        if pivot_row != k:
            z[k], z[pivot_row] = z[pivot_row], z[k]
            for row in z:
                row[k], row[pivot_row] = row[pivot_row], row[k]
        pivot = z[k][k]
        for i in range(k+1, n):
            for j in range(i, n):
                value = pivot*z[i][j]-z[i][k]*z[k][j]
                require(value % previous == 0, 'nonexact Bareiss division')
                z[i][j] = z[j][i] = value//previous
        for i in range(k+1, n):
            z[i][k] = z[k][i] = 0
        previous = pivot
        rank += 1
    return rank


def matrix_hash(a):
    return sha256(json.dumps([[str(rational(x)) for x in row] for row in a],
                             separators=(',', ':')).encode()).hexdigest()
