"""Exact PSD/rank by integer Bareiss; algorithm credited to predecessors.

The independent Fraction Schur algorithm lives in verify.py. Checks use
explicit exceptions, including under python -O; no floating arithmetic.
"""
from fractions import Fraction as Q
from math import lcm
from matrices import require


def psd_rank(A):
    d = len(A)
    require(all(len(row) == d for row in A), "PSD shape")
    require(all(type(v) in (int, Q) for row in A for v in row), "Exact PSD input")
    require(all(A[i][j] == A[j][i] for i in range(d) for j in range(d)), "PSD symmetry")
    if not d:
        return 0
    den = lcm(*(Q(v).denominator for row in A for v in row))
    z = [[int(Q(v)*den) for v in row] for row in A]
    previous, rank = 1, 0
    for k in range(d):
        require(all(z[i][i] >= 0 for i in range(k, d)), "Negative Schur diagonal")
        p = next((i for i in range(k, d) if z[i][i] > 0), None)
        if p is None:
            require(all(z[i][b] == 0 for i in range(k, d) for b in range(k, d)),
                    "Nonzero zero-diagonal residual")
            break
        if p != k:
            z[k], z[p] = z[p], z[k]
            for row in z:
                row[k], row[p] = row[p], row[k]
        pivot = z[k][k]
        for i in range(k+1, d):
            for b in range(i, d):
                value = pivot*z[i][b]-z[i][k]*z[k][b]
                require(value % previous == 0, "Integer elimination divisibility")
                z[i][b] = z[b][i] = value//previous
        previous = pivot
        rank += 1
    return rank
