"""Exact primitives reused from six-reviewer-5's own uniform-three audit.
No author implementation is imported. CPython standard library only.
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import comb, factorial, gcd, lcm

def need(condition, message):
    if not condition:
        raise ValueError(message)

def poly(v):
    a = list(map(F, v))
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return tuple(a)

def add(a, b):
    return poly([(a[i] if i < len(a) else 0) +
                 (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])

def scale(a, c):
    return poly([x*c for x in a])

def sub(a, b):
    return add(a, scale(b, -1))

def mul(a, b):
    c = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return poly(c)

def pmul(*a):
    r = (F(1),)
    for x in a:
        r = mul(r, x)
    return r

def psum(a):
    r = (F(0),)
    for x in a:
        r = add(r, x)
    return r

def choose(a, k):
    if k < 0:
        return (F(0),)
    return scale(pmul(*[sub(a, (F(i),)) for i in range(k)]),
                 F(1, factorial(k)))

def integer_record(num, den):
    need(num[0] > 0 and den[0] > 0, 'nonpositive constant')
    need(all(x >= 0 for x in num+den), 'negative coefficient')
    d = lcm(*(x.denominator for x in num+den))
    nn, dd = [int(d*x) for x in num], [int(d*x) for x in den]
    g = gcd(*nn, *dd)
    return {'numerator_ascending': [x//g for x in nn],
            'denominator_ascending': [x//g for x in dd]}

def matvec(A, v):
    return [sum((a*x for a, x in zip(row, v)), F(0)) for row in A]

def rank(A):
    A = [list(map(F, row)) for row in A]
    if not A:
        return 0
    r = 0
    for c in range(len(A[0])):
        p = next((i for i in range(r, len(A)) if A[i][c]), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        d = A[r][c]
        for i in range(r+1, len(A)):
            if A[i][c]:
                t = A[i][c]/d
                for j in range(c, len(A[0])):
                    A[i][j] -= t*A[r][j]
        r += 1
        if r == len(A):
            break
    return r

def psd_rank(A):
    """Positive pivots and Schur complements; zero diagonal requires zero row."""
    A = [list(map(F, row)) for row in A]
    n = len(A)
    need(all(len(row) == n for row in A), 'nonsquare')
    need(all(A[i][j] == A[j][i] for i in range(n) for j in range(i)), 'asymmetric')
    r = 0
    for k in range(n):
        need(all(A[i][i] >= 0 for i in range(k, n)), 'negative pivot')
        p = next((i for i in range(k, n) if A[i][i]), None)
        if p is None:
            need(all(A[i][j] == 0 for i in range(k, n) for j in range(k, n)),
                 'zero form with nonzero image')
            break
        if p != k:
            A[p], A[k] = A[k], A[p]
            for row in A:
                row[p], row[k] = row[k], row[p]
        d = A[k][k]
        for i in range(k+1, n):
            t = A[i][k]/d
            for j in range(i, n):
                A[i][j] -= t*A[k][j]
                A[j][i] = A[i][j]
        r += 1
    return r

def determinant3(a):
    return sum(((-1 if sum(p[i] > p[j] for i in range(3) for j in range(i+1, 3)) % 2 else 1)
                *a[0][p[0]]*a[1][p[1]]*a[2][p[2]] for p in permutations(range(3))), F(0))

def controls():
    count = 0
    for values in product((-1, 0, 1), repeat=6):
        a, b, c, d, e, f = values
        A = [[a, d, e], [d, b, f], [e, f, c]]
        expected = min(a, b, c, a*b-d*d, a*c-e*e, b*c-f*f, determinant3(A)) >= 0
        try:
            psd_rank(A)
            got = True
        except ValueError:
            got = False
        need(got == expected, 'PSD/principal-minor disagreement')
        count += 1
    rejected = 0
    for A in [[[0, 1], [1, 0]], [[-1]], [[1, 2], [0, 1]], [[1, 0]],
              [[1, 1], [1, F(1, 2)]]]:
        try:
            psd_rank(A)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('malformed or indefinite control accepted')
    need(psd_rank([[F(1, 3), F(2, 3)], [F(2, 3), F(4, 3)]]) == 1, 'rational Gram control')
    try:
        integer_record((F(-1), F(1)), (F(1),))
    except ValueError:
        rejected += 1
    else:
        raise ValueError('invalid positivity record accepted')
    return {'symmetric_3_by_3_principal_minor_comparisons': count,
            'invalid_inputs_rejected': rejected, 'rational_Gram_rank': 1}
