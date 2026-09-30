"""Full-matrix exact PSD/rank check by fraction-free Schur elimination.

Clearing all denominators by a positive integer preserves positivity/rank.
At each positive pivot d the residual is updated by
    (d*A[i,j] - A[i,p]*A[p,j])/previous_pivot.
Bareiss divisibility is checked, never assumed. Every residual is a positive
multiple of the rational Schur complement. The zero-diagonal stopping rule
is necessary and sufficient for a positive semidefinite residual.
No invariant-space bridge or floating arithmetic is used.
"""
from fractions import Fraction as F
from math import lcm


def integer_psd_rank(Q):
    n = len(Q)
    assert all(len(row) == n for row in Q)
    assert all(Q[i][j] == Q[j][i] for i in range(n) for j in range(n))
    scale = lcm(*(F(x).denominator for row in Q for x in row))
    A = [[int(F(x)*scale) for x in row] for row in Q]
    previous, rank = 1, 0
    while A:
        p = max(range(len(A)), key=lambda i: A[i][i])
        d = A[p][p]
        if d < 0:
            raise ValueError('negative diagonal in integer residual')
        if d == 0:
            if any(x for row in A for x in row):
                raise ValueError('nonzero integer residual with zero diagonal')
            return rank
        pivot_row = A.pop(p)
        column = pivot_row[:p]+pivot_row[p+1:]
        for row in A:
            row.pop(p)
        for i, row in enumerate(A):
            for j in range(i, len(A)):
                numerator = d*row[j]-column[i]*column[j]
                value, remainder = divmod(numerator, previous)
                assert remainder == 0, 'fraction-free divisibility failure'
                row[j] = value
                A[j][i] = value
        previous = d
        rank += 1
    return rank
