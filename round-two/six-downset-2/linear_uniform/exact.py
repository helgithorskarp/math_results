"""Exact PSD checking, adapted with credit from published rank-four/five code."""
from fractions import Fraction as Q
from math import lcm
from matrices import require


def psd_rank(A):
    d = len(A)
    require(all(len(row) == d for row in A), "PSD shape")
    require(all(type(v) in (int,Q) for row in A for v in row), "PSD input must be exact")
    require(all(A[i][j] == A[j][i] for i in range(d) for j in range(d)), "PSD symmetry")
    if not d:
        return 0
    den = lcm(*(Q(v).denominator for row in A for v in row))
    z = [[int(Q(v)*den) for v in row] for row in A]
    previous, rank = 1, 0
    for k in range(d):
        require(all(z[i][i] >= 0 for i in range(k,d)), "Negative Schur diagonal")
        i = next((i for i in range(k,d) if z[i][i] > 0), None)
        if i is None:
            require(all(z[i][j] == 0 for i in range(k,d) for j in range(k,d)),
                    "Zero diagonal with nonzero residual")
            break
        if i != k:
            z[k], z[i] = z[i], z[k]
            for row in z:
                row[k], row[i] = row[i], row[k]
        pivot = z[k][k]
        for i in range(k+1,d):
            for j in range(i,d):
                value = pivot*z[i][j]-z[i][k]*z[k][j]
                require(value % previous == 0, "Nonintegral elimination step")
                z[i][j] = z[j][i] = value//previous
        previous, rank = pivot, rank+1
    return rank


def matrix_product(A, B):
    return [[sum((x*y for x,y in zip(row,col)),Q(0)) for col in zip(*B)] for row in A]


def transpose(A):
    return list(map(list,zip(*A)))


def fails_psd(A):
    try:
        psd_rank(A)
    except ValueError:
        return True
    return False
