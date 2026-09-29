#!/usr/bin/env python3
"""Exact polynomial certificate checker; Python >=3.11, standard library only.

Polynomials are integer tuples in ascending coefficient order; () is zero.
The geometric reduction and interpretation are proved in README.md.
"""
from fractions import Fraction
from functools import reduce
from math import comb, gcd
from pathlib import Path
import copy
import json
import sys

Z = ()
ONE = (1,)
T = (0, 1)
F = (-1, -3, 2, 6, -1, 13)
ROOT_LO = Fraction('0.59260590292507377809642492233275')
ROOT_HI = Fraction('0.59260590292507377809642492233276')
MON = ((0, 0), (0, 1), (0, 2), (0, 3), (1, 1),
       (1, 2), (1, 3), (2, 2), (2, 3), (3, 3))
# Every member has a strictly constant sign on [1/2,3/5], checked below.
SAFE = (T, (-1, 1), (1, 1), (1, 2), (1, 3), (-1, 3),
        (-1, 0, 5), (-3, -2, 9), (1, -1, -1, 9),
        (1, 3, -1, -3, 8), (-1, -2, 1), (-2, -7, 0, 13),
        (-3, -11, -5, 11))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def trim(p):
    p = list(p)
    while p and not p[-1]:
        p.pop()
    return tuple(p)


def add(a, b):
    return trim([(a[i] if i < len(a) else 0) +
                 (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def scale(p, a):
    return trim([a * x for x in p])


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    if not a or not b:
        return Z
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return trim(c)


def power(p, k):
    v = ONE
    for _ in range(k):
        v = mul(v, p)
    return v


def divrem(a, b):
    """Integer polynomial division when all quotient coefficients are integral."""
    need(bool(b), 'division by zero')
    r = list(a)
    q = [0] * max(0, len(a) - len(b) + 1)
    while r and len(r) >= len(b):
        if r[-1] % b[-1]:
            return None, trim(r)
        v = r[-1] // b[-1]
        k = len(r) - len(b)
        q[k] = v
        for j, x in enumerate(b):
            r[k + j] -= v * x
        r = list(trim(r))
    return trim(q), trim(r)


def exactdiv(a, b):
    q, r = divrem(a, b)
    need(q is not None and not r, 'nonexact polynomial division')
    return q


def primitive(p):
    if not p:
        return p
    g = reduce(gcd, p)
    if p[-1] < 0:
        g = -g
    return tuple(x // g for x in p)


def prem(a, b):
    """Primitive pseudoremainder: preserves the Q[t] gcd up to a unit."""
    while a and len(a) >= len(b):
        shift = (0,) * (len(a) - len(b)) + scale(b, a[-1])
        a = primitive(sub(scale(a, b[-1]), shift))
    return a


def pgcd(a, b):
    a, b = primitive(a), primitive(b)
    while b:
        a, b = b, prem(a, b)
    return primitive(a)


def strip_safe(p):
    need(bool(p), 'zero polynomial cannot certify invertibility')
    p = primitive(p)
    for factor in SAFE:
        while len(p) >= len(factor):
            q, r = divrem(p, factor)
            if q is None or r:
                break
            p = primitive(q)
    return p


def nonsingular(p, label):
    need(len(strip_safe(p)) == 1, label + ': uncertified zero or extra factor')


def det(a):
    """Fraction-free Bareiss determinant over Z[t], with row pivoting."""
    a = [list(r) for r in a]
    n = len(a)
    previous, sign = ONE, 1
    for k in range(n - 1):
        row = next((i for i in range(k, n) if a[i][k]), None)
        if row is None:
            return Z
        if row != k:
            a[k], a[row] = a[row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = exactdiv(sub(mul(pivot, a[i][j]),
                                       mul(a[i][k], a[k][j])), previous)
            a[i][k] = Z
        previous = pivot
    return scale(a[-1][-1], sign)


def value(p, x):
    a = Fraction(0)
    for y in reversed(p):
        a = a * x + y
    return a


def bernstein(p, lo=Fraction(1, 2), hi=Fraction(3, 5)):
    """Coefficients in the degree-n Bernstein basis on [lo,hi]."""
    n = len(p) - 1
    a = [sum(Fraction(p[j]) * comb(j, k) * lo ** (j - k) *
             (hi - lo) ** k for j in range(k, n + 1)) for k in range(n + 1)]
    return [sum(a[k] * Fraction(comb(i, k), comb(n, k))
                for k in range(i + 1)) for i in range(n + 1)]


def interval(p):
    lo = hi = Fraction(0)
    for c in reversed(p):
        products = (lo*ROOT_LO, lo*ROOT_HI, hi*ROOT_LO, hi*ROOT_HI)
        lo, hi = min(products)+c, max(products)+c
    return lo, hi


def model(variant):
    ap = [(6, 0, 11, 5), (7, 0, 5, 11), (9, 5, 11, 0), (14, 0, 6, 11)]
    bp = [(3, 1, 4, 2), (8, 2, 4, 1), (10, 1, 2, 4)]
    if variant == 'asymmetric':
        bp += [(12, 1, 10, 2), (13, 2, 8, 4)]
        cross = [(7, 3), (14, 3), (6, 8), (7, 12), (9, 10), (9, 13)]
    elif variant == 'cyclic':
        ap += [(12, 5, 7, 0), (13, 11, 9, 5)]
        cross = [(7, 3), (14, 3), (6, 8), (13, 8), (9, 10), (12, 10)]
    else:
        raise ValueError('unknown pattern')
    return ap, bp, cross


def blocks(variant):
    r = power((1, 1), 2)
    a = {i: [r if j == k else Z for j in range(3)]
         for k, i in enumerate((0, 5, 11))}
    b = {i: [r if j == k else Z for j in range(3)]
         for k, i in enumerate((1, 2, 4))}
    ap, bp, cross = model(variant)
    edges = set()
    for group, steps in ((a, ap), (b, bp)):
        roots = list(group)
        edges.update(tuple(sorted((i, j))) for i in roots for j in roots if i < j)
        for new, i, j, old in steps:
            need(new not in a and new not in b, 'repeated point label')
            need(all(tuple(sorted(e)) in edges for e in ((i, j), (i, old), (j, old))),
                 'reflection lacks its old equilateral triangle')
            group[new] = [sub(exactdiv(mul((0, 2), add(group[i][k], group[j][k])),
                                          (1, 1)), group[old][k]) for k in range(3)]
            edges.update((tuple(sorted((new, i))), tuple(sorted((new, j)))))
    edges.update(tuple(sorted(e)) for e in cross)
    need(set(a) | set(b) == set(range(15)) and len(edges) == 30, 'graph model size')
    return a, b, cross, r, sorted(edges)


def mm(a, b):
    return [[reduce(add, (mul(x, y) for x, y in zip(row, col)), Z)
             for col in zip(*b)] for row in a]


def decode(record, rows):
    d = trim(record['den'])
    nums = [[trim(p) for p in row] for row in record['num']]
    need(len(nums) == rows and all(len(r) == 4 for r in nums), 'table dimensions')
    need(all(type(c) is int for r in nums for p in r for c in p) and
         all(type(c) is int for c in d), 'integer coefficients required')
    nonsingular(d, 'table denominator')
    return nums, d


def check_variant(variant, record):
    a, b, cross, r, edges = blocks(variant)
    v = [[mul(a[i][j], b[k][l]) for j in range(3) for l in range(3)]
         for i, k in cross]
    v0 = [row[:6] for row in v]
    nonsingular(det(v0), 'linear pivot determinant')
    u, dm = decode(record['linear'], 9)
    rhs = [[mul(T, power(r, 2))] + [scale(p, -1) for p in row[6:]] for row in v]
    need(mm(v0, u[:6]) == [[mul(p, dm) for p in row] for row in rhs],
         'cross-contact linear solution identity')
    need(u[6:] == [[Z, dm, Z, Z], [Z, Z, dm, Z], [Z, Z, Z, dm]],
         'the free variables must be the bottom row')
    # H^{-1}=G/h, H has diagonal 1 and off-diagonal t.
    g = [[(1, 1) if i == j else (0, -1) for j in range(3)] for i in range(3)]
    h = mul((-1, 1), (-1, -2))
    e = []
    for i in range(3):
        for j in range(i, 3):
            row = [Z] * 10
            for k in range(3):
                for l in range(3):
                    x, y = u[3*k+i], u[3*l+j]
                    for n, (p, q) in enumerate(MON):
                        w = mul(x[p], y[q])
                        if p != q:
                            w = add(w, mul(x[q], y[p]))
                        row[n] = add(row[n], mul(g[k][l], w))
            row[0] = sub(row[0], mul(mul(h, power(dm, 2)), ONE if i == j else T))
            e.append(row)
    c, ell = [row[4:] for row in e], [row[:4] for row in e]
    nonsingular(det(c), 'quadratic pivot determinant')
    q, dq = decode(record['quadratic'], 6)
    need(mm(c, q) == [[scale(mul(p, dq), -1) for p in row] for row in ell],
         'quadratic normal-form identity')
    def columns(cols):
        return [list(row) for row in zip(*cols)]
    mx = columns([[Z, dq, Z, Z], q[0], q[1], q[2]])
    my = columns([[Z, Z, dq, Z], q[1], q[3], q[4]])
    mz = columns([[Z, Z, Z, dq], q[2], q[4], q[5]])
    def comm(x, y):
        xy, yx = mm(x, y), mm(y, x)
        return [[sub(xy[i][j], yx[i][j]) for j in range(4)] for i in range(4)]
    xy, xz = comm(mx, my), comm(mx, mz)
    w = [xy[i] + xz[i] for i in range(4)]
    minors = [strip_safe(det([[row[j] for j in (1, 2, 3, last)] for row in w]))
              for last in (5, 6)]
    obstruction = pgcd(*minors)
    need(obstruction == F, 'common determinant obstruction differs from F')
    # At F(t)=0 the first commutator has rank three and a unique normalized
    # left kernel. Its kernel vector supplies the bottom row of the incumbent M.
    aa = (-54, -12, 140, -96, 234)
    bb = (-31, -38, 136, -106, 195)
    cc = (81, 42, -276, 202, -429)
    bn = ((4,), bb, cc, aa)  # four times (1,x,y,z)
    def zero_mod_f(p):
        quotient, remainder = divrem(p, F)
        return quotient is not None and not remainder
    kernel = mm([bn], w)[0]
    need(all(zero_mod_f(p) for p in kernel), 'incumbent commutator kernel identity')
    rank_minor = det([[xy[i][j] for j in (1, 2, 3)] for i in (1, 2, 3)])
    need(pgcd(rank_minor, F) == ONE, 'rank-three minor vanishes at an F root')
    mc = (aa, bb, cc, cc, aa, bb, bb, cc, aa)
    ub = mm(u, [[p] for p in bn])
    need(all(zero_mod_f(sub(ub[i][0], mul(dm, mc[i]))) for i in range(9)),
         'forced circulant cross Gram identity')
    # Certify the explicit realization too. M=mc/4; H^{-1}=G/h.
    mcm = [list(mc[3*i:3*i+3]) for i in range(3)]
    compat = mm(mm([list(row) for row in zip(*mcm)], g), mcm)
    need(all(zero_mod_f(sub(compat[i][j], scale(mul(h, ONE if i == j else T), 16)))
             for i in range(3) for j in range(3)), 'incumbent metric compatibility')
    hh = [[ONE if i == j else T for j in range(3)] for i in range(3)]
    den = power(r, 2)
    for group in (a, b):
        need(all(mm(mm([p], hh), [[x] for x in p])[0][0] == den
                 for p in group.values()), 'unit-vector construction identity')
    edge_set = set(edges)
    contacts = 0
    for i in range(15):
        for j in range(i+1, 15):
            if i in a and j in a:
                numerator = mm(mm([a[i]], hh), [[x] for x in a[j]])[0][0]
                denominator = den
            elif i in b and j in b:
                numerator = mm(mm([b[i]], hh), [[x] for x in b[j]])[0][0]
                denominator = den
            else:
                ai, bj = (i, j) if i in a else (j, i)
                numerator = mm(mm([a[ai]], mcm), [[x] for x in b[bj]])[0][0]
                denominator = scale(den, 4)
            if (i, j) in edge_set:
                need(zero_mod_f(sub(numerator, mul(T, denominator))), 'contact realization')
                contacts += 1
            else:
                need(interval(sub(scale(numerator, 40), scale(denominator, 17)))[1] < 0,
                     'noncontact realization bound')
    need(contacts == 30, 'realized contact count')
    return {'points': 15, 'edges': len(edges), 'residual_minor_degrees':
            [len(p)-1 for p in minors], 'common_obstruction': list(obstruction),
            'unique_cross_Gram_at_root': True, 'construction_noncontacts_below': '17/40'}


def verify(data):
    for p in SAFE:
        b = bernstein(p)
        need(all(x > 0 for x in b) or all(x < 0 for x in b), 'unsafe factor sign')
    derivative = tuple(i * F[i] for i in range(1, len(F)))
    need(all(x > 0 for x in bernstein(derivative)), 'F is not strictly increasing')
    need(value(F, Fraction(1, 2)) < 0 < value(F, Fraction(3, 5)), 'F endpoint signs')
    need(value(F, ROOT_LO) < 0 < value(F, ROOT_HI), 'incumbent root bracket')
    need(set(data) == {'asymmetric', 'cyclic'}, 'certificate must cover both patterns')
    result = {variant: check_variant(variant, data[variant]) for variant in sorted(data)}
    return {'status': 'VERIFIED', 'interval': '(1/2,3/5)', 'patterns': result,
            'all_divisors_certified_nonzero': True, 'F_unique_root_in_interval': True}


def selftest(data):
    # Corrupt both algebraic layers, so acceptance cannot be mere presence of data.
    for layer in ('linear', 'quadratic'):
        bad = copy.deepcopy(data)
        p = bad['asymmetric'][layer]['num'][0][0]
        if not p:
            p.append(1)
        else:
            p[0] += 1
        try:
            verify(bad)
        except ValueError as error:
            need('identity' in str(error), 'corruption rejected for wrong reason')
        else:
            raise ValueError('corrupted certificate accepted')
    # Arithmetic controls distinguish a true constant gcd from an extra root.
    need(pgcd(mul(F, (2, 1)), mul(F, (3, 1))) == F, 'gcd control')
    need(pgcd(mul(F, (2, 1)), mul(F, (2, 1))) != F, 'gcd extra-factor control')


if __name__ == '__main__':
    certificate = json.loads(Path(__file__).with_name('certificate.json').read_text())
    result = verify(certificate)
    if '--selftest' in sys.argv:
        selftest(certificate)
        result['controls'] = 'two corrupted algebraic layers rejected; gcd controls passed'
    print(json.dumps(result, sort_keys=True, indent=2))
