# Retained from near_full_pair_separation, commit 428da8d6789562e364812a871c76b97177ffe928.
"""Two exact PSD/rank algorithms, credited to the earlier public checkers."""
from fractions import Fraction as Q
from math import lcm
from model import require


def bareiss_rank(matrix):
    d = len(matrix)
    require(all(len(row) == d for row in matrix), "PSD square input")
    require(all(type(v) in (int, Q) for row in matrix for v in row), "Exact PSD input")
    require(all(matrix[i][j] == matrix[j][i] for i in range(d) for j in range(d)),
            "PSD symmetry")
    if not d:
        return 0
    den = lcm(*(Q(v).denominator for row in matrix for v in row))
    A = [[int(Q(v)*den) for v in row] for row in matrix]
    previous, rank = 1, 0
    for k in range(d):
        require(all(A[i][i] >= 0 for i in range(k, d)), "Negative Schur diagonal")
        hit = next((i for i in range(k, d) if A[i][i] > 0), None)
        if hit is None:
            require(all(A[i][j] == 0 for i in range(k, d) for j in range(k, d)),
                    "Nonzero zero-diagonal residual")
            break
        if hit != k:
            A[k], A[hit] = A[hit], A[k]
            for row in A:
                row[k], row[hit] = row[hit], row[k]
        pivot = A[k][k]
        for i in range(k+1, d):
            for j in range(i, d):
                value = pivot*A[i][j]-A[i][k]*A[k][j]
                require(value % previous == 0, "Bareiss divisibility")
                A[i][j] = A[j][i] = value//previous
        previous = pivot
        rank += 1
    return rank


def schur_rank(matrix):
    d = len(matrix)
    require(all(len(row) == d for row in matrix), "Schur square input")
    require(all(type(v) in (int, Q) for row in matrix for v in row), "Exact Schur input")
    require(all(matrix[i][j] == matrix[j][i] for i in range(d) for j in range(d)),
            "Schur symmetry")
    A = [[Q(v) for v in row] for row in matrix]
    rank = 0
    while A:
        require(all(A[i][i] >= 0 for i in range(len(A))), "Negative rational diagonal")
        hit = next((i for i in range(len(A)) if A[i][i]), None)
        if hit is None:
            require(all(not v for row in A for v in row), "Nonzero null Schur residual")
            break
        keep = [i for i in range(len(A)) if i != hit]
        pivot = A[hit][hit]
        A = [[A[i][j]-A[i][hit]*A[hit][j]/pivot for j in keep] for i in keep]
        rank += 1
    return rank


def both(matrix, rank=None):
    a, b = bareiss_rank(matrix), schur_rank(matrix)
    require(a == b and (rank is None or a == rank), "Exact rank agreement")
    return a
