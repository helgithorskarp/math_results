"""Complete univariate polynomial identities; standard library only.

Dense coefficient arithmetic checks the closed dual, all reduced minors,
and their positive half-line signs. No CAS or interpolation is an input.
"""
from itertools import permutations
from math import comb
from forms import require


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(a, b):
    out = [0]*max(len(a), len(b))
    for p in (a, b):
        for i, x in enumerate(p):
            out[i] += x
    return trim(out)


def scale(a, t):
    return trim([t*x for x in a])


def mul(a, b):
    out = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return trim(out)


def shift4(p):
    return trim([sum(p[j]*comb(j, i)*4**(j-i) for j in range(i, len(p)))
                 for i in range(len(p))])


def at(p, q):
    return sum(x*q**i for i, x in enumerate(p))


def determinant(A):
    out, n = [0], len(A)
    for perm in permutations(range(n)):
        term = [1]
        for i, j in enumerate(perm):
            term = mul(term, A[i][j])
        sign = (-1)**sum(perm[i] > perm[j] for i in range(n) for j in range(i+1, n))
        out = add(out, scale(term, sign))
    return out


D = [-12, 12, 57, 36]
THETA = [[12, 4, -21, -18], [0, 16, 12], [4, 12, 9], [-4, 0, 9]]
FIRST = [-12, 4, 39, 27]
COST = mul(mul([2, 3], [4, 3]), [-2, 3, 3])
M = [[[1, 6], [-1], [-3], [0, -3]],
     [[-1], [3, 3], [-1], [2, 2]],
     [[-3], [-1], [3, 3], [0, -1]],
     [[0, -3], [2, 2], [0, -1], [0, 4, 2]]]
B = [[0, 3], [-2], [-2], [0, -2]]


def check():
    require(all(x >= 0 for x in shift4(D)) and shift4(D)[0] > 0,
            'entire closed dual denominator positive on q>=4')
    for i in range(4):
        lhs = mul(B[i], D)
        for j in range(4):
            lhs = add(lhs, mul(M[i][j], THETA[j]))
        require(lhs == [0], 'every entire polynomial minimization equation')
    require(scale(FIRST, 2) == add(D, scale(THETA[0], -1)), 'entire first elimination coefficient identity')
    rhs = mul([2, 3], D)
    for i in range(4):
        rhs = add(rhs, mul(B[i], THETA[i]))
    require(rhs == scale(COST, 2), 'entire closed lower cost polynomial identity')
    records = []
    for n in range(1, 5):
        p = determinant([row[:n] for row in M[:n]])
        coeff = shift4(p)
        require(coeff[0] > 0 and all(x >= 0 for x in coeff), 'whole shifted leading minor positive on q>=4')
        records.append({'size': n, 'polynomial': p, 'coefficients_at_q4_plus_u': coeff})
    require(all(x >= 0 for x in shift4(COST)) and shift4(COST)[0] > 0,
            'whole lower cost positive')
    return {'complete_minimization_equations': 4, 'first_elimination_identity': True,
            'closed_energy_identity': True, 'denominator': D, 'cost_numerator': COST,
            'leading_minors': records, 'total_positive_minor_coefficients': sum(len(x['polynomial']) for x in records)}
