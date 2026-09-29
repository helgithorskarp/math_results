#!/usr/bin/env python3
"""Check the 29-edge completion certificate using only integer/Fraction arithmetic.

Polynomial primitives and the 24-edge reflected blocks are shared with verify.py.
See DELETED_CONTACT.md for the geometric implication of the checked identities.
"""
import copy
from functools import reduce
from itertools import combinations_with_replacement
from math import gcd
from pathlib import Path
import json
import sys
import verify as base
from verify import (Z, ONE, T, F, ROOT_LO, ROOT_HI, need, trim, add, sub,
                    mul, scale, power, divrem, exactdiv, primitive, prem,
                    pgcd, det, value, bernstein, blocks, mm)

EXTRA_SAFE = (
    (1, 1, -1, 3), (-1, -1, 4), (-1, 2, 11), (1, 7, 23, 25),
    (1, 2, -8, -16, 1), (-2, -1, 33, 42, -76, -57, 93),
    (3, 17, 30, 18, 31, 61), (1, 8, 21, 4, -49, -12, 59),
    (3, 4, -39, -34, 157, 0, -281, 126),
    (1, -8, -29, 38, -1, -476, -323, 350))
SAFE = base.SAFE + EXTRA_SAFE
PIVOT = (1, 2, 3, 4, 5)
FREE = (0, 6, 7, 8)
QUAD = tuple(combinations_with_replacement(range(1, 5), 2))
MON = ((0, 0),) + tuple((0, i) for i in range(1, 5)) + QUAD


def strip_safe(p):
    need(bool(p), 'zero cannot certify invertibility')
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


def cancel_safe_common(vector):
    """Divide a vector only by proved nonzero factors and nonzero integers.

    Used on rows for determinant evaluation and on columns for commutators;
    column cancellation preserves the normalized left-kernel vector.
    """
    vector = list(vector)
    if not any(vector):
        return vector
    for factor in SAFE:
        while True:
            divided = [divrem(p, factor) for p in vector]
            if any(q is None or r for q, r in divided):
                break
            vector = [q for q, _ in divided]
    content = reduce(gcd, (c for p in vector for c in p))
    return [trim([c // content for c in p]) for p in vector]


def decode(record, rows):
    need(set(record) == {'den', 'num'}, 'table keys')
    need(type(record['den']) is list and type(record['num']) is list,
         'table arrays required')
    need(len(record['num']) == rows and
         all(type(r) is list and len(r) == 5 for r in record['num']),
         'table dimensions')
    need(all(type(p) is list for r in record['num'] for p in r) and
         all(type(c) is int for r in record['num'] for p in r for c in p) and
         all(type(c) is int for c in record['den']), 'integer coefficients required')
    nums = [[trim(p) for p in row] for row in record['num']]
    denominator = trim(record['den'])
    nonsingular(denominator, 'table denominator')
    return nums, denominator


def verify(data):
    for p in SAFE:
        b = bernstein(p)
        need(all(x > 0 for x in b) or all(x < 0 for x in b), 'unsafe factor sign')
    need(all(x > 0 for x in bernstein(tuple(i * F[i] for i in range(1, len(F))))),
         'F derivative sign')
    need(value(F, ROOT_LO) < 0 < value(F, ROOT_HI), 'root bracket')
    need(value(F, base.Fraction(1, 2)) < 0 < value(F, base.Fraction(3, 5)),
         'F endpoint signs')
    need(set(data) == {'linear', 'quadratic'}, 'certificate layers')
    a, b, cross, r, edges = blocks('asymmetric')
    need(cross.count((7, 3)) == 1, 'deleted contact must occur once')
    cross = [edge for edge in cross if edge != (7, 3)]
    edges = [edge for edge in edges if edge != (3, 7)]
    need(len(edges) == 29 and len(cross) == 5, 'deleted graph size')
    v = [[mul(a[i][j], b[k][l]) for j in range(3) for l in range(3)]
         for i, k in cross]
    v0 = [[row[j] for j in PIVOT] for row in v]
    nonsingular(det(v0), 'linear pivot determinant')
    u, dm = decode(data['linear'], 9)
    rhs = [[mul(T, power(r, 2))] + [scale(row[j], -1) for j in FREE] for row in v]
    need(mm(v0, [u[j] for j in PIVOT]) ==
         [[mul(p, dm) for p in row] for row in rhs], 'five cross-contact identity')
    need([u[j] for j in FREE] ==
         [[Z] + [dm if k == i else Z for k in range(4)] for i in range(4)],
         'free variables must be M00 and the bottom row')
    g = [[(1, 1) if i == j else (0, -1) for j in range(3)] for i in range(3)]
    h = mul((-1, 1), (-1, -2))
    e = []
    for side in ('columns', 'rows'):
        for i in range(3):
            for j in range(i, 3):
                row = [Z] * 15
                for k in range(3):
                    for l in range(3):
                        x, y = ((u[3*k+i], u[3*l+j]) if side == 'columns'
                                else (u[3*i+k], u[3*j+l]))
                        for n, (p, q) in enumerate(MON):
                            w = mul(x[p], y[q])
                            if p != q:
                                w = add(w, mul(x[q], y[p]))
                            row[n] = add(row[n], mul(g[k][l], w))
                row[0] = sub(row[0], mul(mul(h, power(dm, 2)), ONE if i == j else T))
                e.append(row)
    c, ell = [row[5:] for row in e[:10]], [row[:5] for row in e[:10]]
    nonsingular(det([cancel_safe_common(row) for row in c]),
                'ten-quadratic pivot determinant')
    n, dn = decode(data['quadratic'], 10)
    need(mm(c, n) == [[scale(mul(p, dn), -1) for p in row] for row in ell],
         'ten quadratic normal-form identity')
    def multiplication(i):
        columns = [[dn if k == i else Z for k in range(5)]]
        columns += [n[QUAD.index(tuple(sorted((i, j))))] for j in range(1, 5)]
        return [list(row) for row in zip(*columns)]
    x, y, z = [multiplication(i) for i in (1, 2, 3)]
    def commutator(p, q):
        pq, qp = mm(p, q), mm(q, p)
        return [[sub(pq[i][j], qp[i][j]) for j in range(5)] for i in range(5)]
    xy, xz = commutator(x, y), commutator(x, z)
    w = [xy[i] + xz[i] for i in range(5)]
    w = [list(row) for row in zip(*(cancel_safe_common(column) for column in zip(*w)))]
    minors = [strip_safe(det([[row[j] for j in (1, 2, 3, 6, last)] for row in w]))
              for last in (7, 8)]
    need(pgcd(*minors) == F, 'common determinant obstruction differs from F')
    aa = (-54, -12, 140, -96, 234)
    bb = (-31, -38, 136, -106, 195)
    cc = (81, 42, -276, 202, -429)
    beta = ((4,), aa, bb, cc, aa)
    def zero_mod_f(p):
        return not prem(p, F)
    need(all(zero_mod_f(p) for p in mm([beta], w)[0]), 'incumbent kernel identity')
    rank_minor = det([[w[i][j] for j in (1, 2, 3, 6)] for i in (1, 2, 3, 4)])
    need(pgcd(rank_minor, F) == ONE, 'rank-four minor vanishes at an F root')
    mc = (aa, bb, cc, cc, aa, bb, bb, cc, aa)
    ub = mm(u, [[p] for p in beta])
    need(all(zero_mod_f(sub(ub[i][0], mul(dm, mc[i]))) for i in range(9)),
         'forced incumbent cross Gram identity')
    missing = mm(mm([a[7]], [list(mc[3*i:3*i+3]) for i in range(3)]),
                 [[p] for p in b[3]])[0][0]
    need(zero_mod_f(sub(missing, scale(mul(T, power(r, 2)), 4))),
         'deleted contact completion identity')
    return {'status': 'VERIFIED', 'points': 15, 'prescribed_edges': 29,
            'deleted_contact_forced': [3, 7], 'interval': '(1/2,3/5)',
            'common_obstruction': list(F), 'residual_minor_degrees': [len(p)-1 for p in minors],
            'F_unique_root_in_interval': True, 'all_divisors_certified_nonzero': True,
            'unique_cross_Gram_at_root': True}


def selftest(data):
    for layer in ('linear', 'quadratic'):
        bad = copy.deepcopy(data)
        p = bad[layer]['num'][PIVOT[0] if layer == 'linear' else 0][0]
        if p:
            p[0] += 1
        else:
            p.append(1)
        try:
            verify(bad)
        except ValueError as error:
            need('identity' in str(error), 'corruption rejected for wrong reason')
        else:
            raise ValueError('corrupted certificate accepted')
    need(pgcd(mul(F, (2, 1)), mul(F, (3, 1))) == F, 'gcd control')
    need(pgcd(mul(F, (2, 1)), mul(F, (2, 1))) != F, 'extra-factor control')


if __name__ == '__main__':
    data = json.loads(Path(__file__).with_name('certificate_deleted_contact.json').read_text())
    result = verify(data)
    if '--selftest' in sys.argv:
        selftest(data)
        result['controls'] = 'two corrupted algebraic layers rejected; gcd controls passed'
    print(json.dumps(result, sort_keys=True, indent=2))
