"""Exact PD certificates by LDL and every principal integer Bareiss minor.

Derived from the credited8464 checker; no discovery/optimizer imports.
Author six-downset-3, researcher. All checks active with Python -O.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from math import lcm

def require(condition, message):
    if not condition:
        raise ValueError(message)


def transpose(a):
    return [list(row) for row in zip(*a)]


def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, column)) for column in transpose(b)]
            for row in a]


def trace(a, b):
    return sum(a[i][j]*b[j][i] for i in range(len(a)) for j in range(len(a)))


def determinant(a):
    """Integer Bareiss with pivoting and checked exact divisions."""
    z = [row[:] for row in a]
    size = len(z)
    require(size and all(len(row) == size for row in z), 'square determinant')
    require(all(type(x) is int for row in z for x in row), 'integer determinant')
    previous, sign = 1, 1
    for k in range(size-1):
        pivot = next((i for i in range(k, size) if z[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            z[k], z[pivot] = z[pivot], z[k]
            sign = -sign
        value = z[k][k]
        for i in range(k+1, size):
            for j in range(k+1, size):
                numerator = value*z[i][j]-z[i][k]*z[k][j]
                require(numerator % previous == 0, 'nonexact Bareiss division')
                z[i][j] = numerator//previous
            z[i][k] = 0
        previous = value
    return sign*z[-1][-1]


def positive_ldl(a):
    size = len(a)
    require(size and all(len(row) == size for row in a), 'square positive matrix')
    require(a == transpose(a), 'asymmetric positive matrix')
    ell = [[F(i == j) for j in range(size)] for i in range(size)]
    diagonal = []
    for j in range(size):
        value = F(a[j][j])-sum(ell[j][k]**2*diagonal[k] for k in range(j))
        require(value > 0, 'nonpositive LDL pivot')
        diagonal.append(value)
        for i in range(j+1, size):
            ell[i][j] = (F(a[i][j])-sum(ell[i][k]*ell[j][k]*diagonal[k] for k in range(j)))/value
    require([[sum(ell[i][k]*diagonal[k]*ell[j][k] for k in range(size))
              for j in range(size)] for i in range(size)] == a, 'LDL reconstruction')
    return diagonal


def positive_integer_matrix(a):
    pivots = positive_ldl(a)
    leading, checked = [], 0
    for size in range(1, len(a)+1):
        for indices in combinations(range(len(a)), size):
            minor = determinant([[a[i][j] for j in indices] for i in indices])
            require(minor > 0, 'nonpositive principal minor')
            checked += 1
            if indices == tuple(range(size)):
                leading.append(minor)
    product = F(1)
    for i, value in enumerate(pivots):
        product *= value
        require(product == leading[i], 'LDL/Bareiss determinant disagreement')
    return pivots, leading, checked


def inverse(a):
    size = len(a)
    rows = [[F(v) for v in row]+[F(i == j) for j in range(size)] for i, row in enumerate(a)]
    for j in range(size):
        pivot = next((i for i in range(j, size) if rows[i][j]), None)
        require(pivot is not None, 'singular inverse')
        rows[j], rows[pivot] = rows[pivot], rows[j]
        value = rows[j][j]
        rows[j] = [v/value for v in rows[j]]
        for i in range(size):
            if i != j:
                value = rows[i][j]
                rows[i] = [v-value*w for v, w in zip(rows[i], rows[j])]
    answer = [row[size:] for row in rows]
    require(multiply(a, answer) == [[F(i == j) for j in range(size)] for i in range(size)],
            'inverse residual')
    return answer



def positive(a):
    D = lcm(*(F(x).denominator for row in a for x in row))
    num = [[int(x*D) for x in row] for row in a]
    require([[F(x, D) for x in row] for row in num] == a, 'PD integer scaling')
    pivots, leading, count = positive_integer_matrix(num)
    return {'order': len(a), 'rank': len(a), 'positive_LDL_pivots': [str(x/D) for x in pivots],
            'integer_denominator': D, 'positive_integer_leading_minors': leading,
            'all_nonempty_principal_minors_checked': count}


def matrix_hash(a):
    h = sha256()
    for row in a:
        h.update((','.join(str(x) for x in row)+'\n').encode())
    return h.hexdigest()
