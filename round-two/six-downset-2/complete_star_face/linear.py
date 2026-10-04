"""Small exact linear controls; no floating arithmetic or assert gates."""
from fractions import Fraction as Q


class Rejected(ValueError):
    pass


def require(value, message):
    if not value:
        raise Rejected(message)


def zeros(r, c):
    return [[Q(0) for _ in range(c)] for _ in range(r)]


def identity(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(x) for x in zip(*a)]


def multiply(a, b):
    require(bool(a) and bool(b) and len(a[0]) == len(b), 'Product shape')
    c = zeros(len(a), len(b[0]))
    sparse_b = [[(j, v) for j, v in enumerate(row) if v] for row in b]
    for i, row in enumerate(a):
        for k, v in enumerate(row):
            if v:
                for j, w in sparse_b[k]:
                    c[i][j] += v*w
    return c


def rref(matrix, coefficient_columns):
    """Direct Gauss--Jordan on ALL submitted original equations."""
    a = [[Q(v) for v in row] for row in matrix]
    require(bool(a) and all(len(x) == len(a[0]) for x in a), 'RREF shape')
    pivots = []
    for col in range(coefficient_columns):
        hit = next((i for i in range(len(pivots), len(a)) if a[i][col]), None)
        if hit is None:
            continue
        pos = len(pivots)
        a[pos], a[hit] = a[hit], a[pos]
        pivot = a[pos][col]
        a[pos] = [v/pivot for v in a[pos]]
        nonzero = [(j, v) for j, v in enumerate(a[pos]) if v]
        for i in range(len(a)):
            if i != pos and a[i][col]:
                scale = a[i][col]
                for j, v in nonzero:
                    a[i][j] -= scale*v
        pivots.append(col)
    for row in a[len(pivots):]:
        require(not any(row[coefficient_columns:]), 'Inconsistent original equations')
    return a, pivots


def inverse(a):
    n = len(a)
    require(n and all(len(row) == n for row in a), 'Inverse shape')
    eye = identity(n)
    rr, pivots = rref([list(row)+eye[i] for i, row in enumerate(a)], n)
    require(pivots == list(range(n)), 'Singular inverse metric')
    result = [row[n:] for row in rr]
    require(multiply(a, result) == eye and multiply(result, a) == eye,
            'Both inverse metric products')
    return result


def rank(a):
    return len(rref([list(row)+[Q(0)] for row in a], len(a[0]))[1])


def psd_rank(a):
    """Exact Schur pivots with the required zero-pivot whole-row rule."""
    n = len(a)
    require(all(len(row) == n for row in a) and a == transpose(a), 'PSD symmetric shape')
    z = [list(row) for row in a]
    out = 0
    for i in range(n):
        pivot = z[i][i]
        require(pivot >= 0, 'Negative exact PSD pivot')
        if not pivot:
            require(not any(z[i][j] for j in range(i+1, n)), 'Nonzero zero-pivot row')
            continue
        out += 1
        for j in range(i+1, n):
            for k in range(j, n):
                z[j][k] -= z[j][i]*z[i][k]/pivot
                z[k][j] = z[j][k]
    return out


def encoded(a):
    return [[str(v) for v in row] for row in a]
