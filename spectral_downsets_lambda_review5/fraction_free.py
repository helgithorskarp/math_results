"""Exact symmetric fraction-free Schur PSD/rank, independently implemented.

This is the standard Bareiss recurrence, not imported from the author. A
positive previous pivot scales the residual Schur form; symmetric swaps do
not change its sign. Every division must be exact. Zero residual diagonals
with a nonzero residual block reject PSD.
"""
from fractions import Fraction as F
from math import lcm
from exact import need


def psd_rank(A):
    n = len(A)
    need(all(len(row) == n for row in A), 'nonsquare integer Schur input')
    need(all(A[i][j] == A[j][i] for i in range(n) for j in range(i)), 'asymmetric integer Schur input')
    denominator = lcm(*(F(x).denominator for row in A for x in row)) if n else 1
    a = [[int(F(x)*denominator) for x in row] for row in A]
    previous, result = 1, 0
    for k in range(n):
        need(all(a[i][i] >= 0 for i in range(k, n)), 'negative Schur diagonal')
        p = next((i for i in range(k, n) if a[i][i] > 0), None)
        if p is None:
            need(all(a[i][j] == 0 for i in range(k, n) for j in range(i, n)),
                 'zero form has nonzero image')
            break
        if p != k:
            a[p], a[k] = a[k], a[p]
            for row in a:
                row[p], row[k] = row[k], row[p]
        pivot = a[k][k]
        for i in range(k+1, n):
            row, factor = a[i], a[i][k]
            for j in range(i, n):
                quotient, remainder = divmod(pivot*row[j]-factor*a[k][j], previous)
                need(remainder == 0, 'inexact fraction-free division')
                row[j] = a[j][i] = quotient
        previous = pivot
        result += 1
    return result
