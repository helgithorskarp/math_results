#!/usr/bin/env python3
"""Exact cyclic thirteen-vertex/twenty-four-edge core; Python stdlib only.

The hand reduction and the completeness of both branches are in CYCLIC_CORE.md.
Integer rational-function helpers come from verify_contact_core.py.
"""
from fractions import Fraction
from pathlib import Path
import copy
import json
import sys
import verify as base
from verify import (T, ONE, F, ROOT_LO, ROOT_HI, need, trim, pgcd,
                    bernstein, value, interval)
from verify_contact_core import (Rat, determinant, positive, nonzero,
                                 strip_factors)


def model():
    ap, bp, cross = base.model('cyclic')
    return ([step for step in ap if step[0] != 14],
            [step for step in bp if step[0] != 3],
            [edge for edge in cross if edge[0] != 14 and edge[1] != 3])


def root_equal(x, y):
    delta = x-y
    nonzero(delta.d, 'root identity denominator')
    return pgcd(delta.n, F) == F


def root_interval(x):
    nlo, nhi = interval(x.n)
    dlo, dhi = interval(x.d)
    need(dlo*dhi > 0, 'root interval denominator has uncertain sign')
    quotients = [n/d for n in (nlo, nhi) for d in (dlo, dhi)]
    return min(quotients), max(quotients)


def verify(data):
    need(set(data) == {'residual_num', 'residual_den', 'bad_pair', 'bad_pair_lower'},
         'certificate field names')
    for name, length in (('residual_num', 12), ('residual_den', 11)):
        need(type(data[name]) is list and len(data[name]) == length and
             all(type(c) is int for c in data[name]), 'integer residual coefficients')
    need(type(data['bad_pair']) is list and len(data['bad_pair']) == 2 and
         all(type(c) is int for c in data['bad_pair']), 'integer packing witness pair')
    need(data['bad_pair_lower'] == [49, 50], 'packing witness threshold')
    for factor in base.SAFE:
        signs = bernstein(factor)
        need(all(c > 0 for c in signs) or all(c < 0 for c in signs), 'base factor sign')
    t, one, zero = Rat(T), Rat(ONE), Rat()
    h = [[one if i == j else t for j in range(3)] for i in range(3)]
    hi = [[(one/(one-t) if i == j else zero)-t/((one-t)*(one+2*t))
           for j in range(3)] for i in range(3)]
    def matvec(matrix, vector):
        return [sum((x*y for x, y in zip(row, vector)), zero) for row in matrix]
    def dot(x, y):
        return sum((x[i]*h[i][j]*y[j] for i in range(3) for j in range(3)), zero)
    need(all(sum((h[i][k]*hi[k][j] for k in range(3)), zero) == (one if i == j else zero)
             for i in range(3) for j in range(3)), 'anchor inverse identity')
    a = {i: [one if j == k else zero for j in range(3)]
         for k, i in enumerate((0, 5, 11))}
    b = {i: [one if j == k else zero for j in range(3)]
         for k, i in enumerate((1, 2, 4))}
    ap, bp, cross = model()
    edges = set()
    for group, steps in ((a, ap), (b, bp)):
        roots = list(group)
        edges.update(tuple(sorted((i, j))) for i in roots for j in roots if i < j)
        for new, i, j, old in steps:
            need(new not in a and new not in b, 'repeated reflection label')
            need(all(tuple(sorted(e)) in edges for e in ((i, j), (i, old), (j, old))),
                 'reflection lacks its existing contact triangle')
            group[new] = [2*t/(one+t)*(group[i][k]+group[j][k])-group[old][k]
                          for k in range(3)]
            edges.update((tuple(sorted((new, i))), tuple(sorted((new, j)))))
    edges.update(tuple(sorted(e)) for e in cross)
    vertices = set(range(15)) - {3, 14}
    need(set(a) | set(b) == vertices and len(edges) == 24, 'cyclic core graph size')
    for group in (a, b):
        need(all(dot(v, v) == one for v in group.values()), 'reflected block unit norms')
        need(all(dot(group[i], group[j]) == t for i, j in edges if i in group and j in group),
             'reflected block contacts')
    kappa = t*(9*t*t-2*t-3)/(one+t)**2
    need(dot(b[8], b[10]) == kappa, 'B reflected pair inner product')
    positive(one-kappa, 'forced B pair independence')
    positive(one+kappa, 'forced B pair nonantipodality')
    forced = {}
    common_det = 16*t**2*(one-t)**2*(2*t+one)*(t*t-2*t-one)**2/(one+t)**6
    positive(common_det, 'common-neighbor triple determinant')
    for new, i, j, old in ((8, 6, 13, 11), (10, 9, 12, 5)):
        w = dot(a[i], a[j])
        need(w == (16*t**4-7*t**3-5*t*t+3*t+one)/(one+t)**3,
             'common-neighbor pair inner product identity')
        positive(one-w, 'common-neighbor pair independence')
        positive(one+w, 'common-neighbor pair nonantipodality')
        need(dot(a[old], a[i]) == t and dot(a[old], a[j]) == t,
             'existing common neighbor contact identity')
        vectors = (a[old], a[i], a[j])
        need(determinant([[dot(x, y) for y in vectors] for x in vectors]) == common_det,
             'common-neighbor determinant identity')
        forced[new] = [2*t/(one+w)*(x+y)-z for x, y, z in zip(a[i], a[j], a[old])]
        need(dot(forced[new], forced[new]) == one and
             dot(forced[new], a[i]) == t and dot(forced[new], a[j]) == t,
             'forced distinct common-neighbor identity')
    residual = dot(forced[8], forced[10])-kappa
    nonzero(trim(data['residual_den']), 'certificate residual denominator')
    proposal = Rat(trim(data['residual_num']), trim(data['residual_den']))
    need(residual == proposal, 'residual certificate identity')
    cubic = Rat((-3, -11, -5, 11))
    q4 = Rat((1, 3, -1, -3, 8))
    factorized = -2*t*(t-one)*(2*t+one)*cubic*Rat(F)/((t+one)**2*q4**2)
    need(residual == factorized, 'residual factorization identity')
    need(strip_factors(residual.n, base.SAFE) == F, 'residual has an extra interval factor')
    need(all(c > 0 for c in bernstein(tuple(i*F[i] for i in range(1, len(F))))),
         'F derivative sign')
    need(value(F, Fraction(1, 2)) < 0 < value(F, Fraction(3, 5)), 'F endpoint signs')
    need(value(F, ROOT_LO) < 0 < value(F, ROOT_HI), 'F root bracket')
    # At F=0 the parent exact realization has the specified circulant cross Gram.
    aa = Rat((-54, -12, 140, -96, 234), (4,))
    bb = Rat((-31, -38, 136, -106, 195), (4,))
    cc = Rat((81, 42, -276, 202, -429), (4,))
    m = [[aa, bb, cc], [cc, aa, bb], [bb, cc, aa]]
    good = {j: matvec(hi, matvec(m, x)) for j, x in b.items()}
    need(all(root_equal(x, y) for j in (8, 10) for x, y in zip(good[j], forced[j])),
         'parent realization does not realize the forced pair')
    bad = {}
    for j, x in good.items():
        d8, d10 = dot(x, forced[8]), dot(x, forced[10])
        q8 = (d8-kappa*d10)/(one-kappa**2)
        q10 = (d10-kappa*d8)/(one-kappa**2)
        bad[j] = [2*(q8*u+q10*v)-z for u, v, z in zip(forced[8], forced[10], x)]
    for name, block in (('incumbent', good), ('reflected', bad)):
        points = {**a, **block}
        need(all(root_equal(dot(x, x), one) for x in points.values()), name+' root unit norms')
        need(all(root_equal(dot(points[i], points[j]), t) for i, j in edges), name+' root contacts')
    need(all(root_equal(x, y) for j in (8, 10) for x, y in zip(bad[j], forced[j])),
         'reflected branch does not fix its spanning plane')
    need(all(root_equal(dot(bad[i], bad[j]), dot(good[i], good[j]))
             for i in b for j in b if i < j), 'plane reflection Gram identity')
    # Within each block distinctness follows from the checked parent realization
    # and an orthogonal reflection. All cross-block pairs are checked explicitly.
    need(all(root_interval(one-dot(x, y))[0] > 0 for x in bad.values() for y in a.values()),
         'reflected core distinctness')
    bj, ai = data['bad_pair']
    need(bj in bad and ai in a, 'packing witness label domains')
    guard = dot(bad[bj], a[ai])
    lower, _ = root_interval(guard)
    need(lower > Fraction(*data['bad_pair_lower']), 'packing exclusion guard')
    need(root_interval(dot(good[bj], a[ai])-guard)[1] < 0, 'two Gram branches coincide')
    old_data = json.loads(Path(__file__).with_name('certificate.json').read_text())
    base.check_variant('cyclic', old_data['cyclic'])
    return {'status': 'VERIFIED', 'vertices': sorted(vertices), 'vertex_count': 13,
            'prescribed_edges': 24, 'interval': '(1/2,3/5)', 'common_obstruction': list(F),
            'distinct_labeled_Gram_branches_up_to_O3': 2, 'packing_Gram_branches': 1,
            'reflected_branch_all_points_distinct': True,
            'reflected_branch_unprescribed_pair': [ai, bj],
            'reflected_branch_pair_dot_greater_than': '49/50',
            'all_geometric_divisors_certified_nonzero': True,
            'incumbent_existence_checked': True, 'global_Tammes15_bound_improved': False}


def selftest(data):
    bad = copy.deepcopy(data)
    bad['residual_num'][0] += 1
    try:
        verify(bad)
    except ValueError as error:
        need('residual certificate identity' in str(error), 'corrupt residual rejected for wrong reason')
    else:
        raise ValueError('corrupted residual accepted')
    bad = copy.deepcopy(data)
    bad['bad_pair'] = [8, 6]  # A prescribed edge remains t in either branch.
    try:
        verify(bad)
    except ValueError as error:
        need('packing exclusion guard' in str(error), 'false witness rejected for wrong reason')
    else:
        raise ValueError('false packing witness accepted')
    need(root_equal(Rat(F), 0), 'root identity control')
    need(not root_equal(Rat((1, 1)), 0), 'root nonidentity control')


if __name__ == '__main__':
    data = json.loads(Path(__file__).with_name('certificate_cyclic_contact_core.json').read_text())
    result = verify(data)
    if '--selftest' in sys.argv:
        selftest(data)
        result['controls'] = 'corrupted residual and false packing witness rejected; root arithmetic controls passed'
    print(json.dumps(result, sort_keys=True, indent=2))
