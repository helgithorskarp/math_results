#!/usr/bin/env python3
"""Exact controls for PROOF.md; no Gaussian quadrature or search.

All pair losses are quadratic polynomials in depth and are checked by
their complete coefficient vectors. The weight expectation identity is
checked coefficient by coefficient in sixteen independent variables.
The universal hinge and compactness claims are written analytic proofs.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import combinations
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c*x for x in a)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])


def rank(rows):
    a = [list(map(F, row)) for row in rows]
    pivot = 0
    for col in range(len(a[0])):
        selected = next((i for i in range(pivot, len(a)) if a[i][col]), None)
        if selected is None:
            continue
        a[pivot], a[selected] = a[selected], a[pivot]
        d = a[pivot][col]
        a[pivot] = [x/d for x in a[pivot]]
        for i in range(pivot+1, len(a)):
            d = a[i][col]
            a[i] = [x-d*y for x, y in zip(a[i], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def normals(vertices, heights):
    result = []
    for i in range(4):
        a, b, c = [vertices[j] for j in range(4) if j != i]
        n = cross(sub(b, a), sub(c, a))
        denominator = dot(n, sub(vertices[i], a))
        require(denominator != 0, 'degenerate tetrahedron')
        result.append(scale(F(heights[i], denominator), n))
    return tuple(result)


LABELS = tuple(('core', i, i) for i in range(4)) + tuple(
    ('flap', i, j) for i in range(4) for j in range(4) if i != j)
INDEX = {label: k for k, label in enumerate(LABELS)}
ZERO = (F(0), F(0), F(0))


def expected_loss(left, right, heights):
    typ, i, j = left
    other, k, ell = right
    if typ == other == 'core':
        return F(0)
    if typ == 'core':
        return 4*heights[k]*(i == k)
    if other == 'core':
        return 4*heights[i]*(k == i)
    return 4*(heights[i]*(ell == i)+heights[k]*(j == k))


def distance_polynomial(a, av, b, bv):
    d, v = sub(a, b), sub(av, bv)
    return dot(d, d), 2*dot(d, v), dot(v, v)


def gamma_polynomial(heights):
    result = Counter()
    for r, (typ, i, j) in enumerate(LABELS):
        if typ == 'core':
            continue
        for k, (_, _, tip) in enumerate(LABELS):
            if tip == i:
                result[tuple(sorted((r, k)))] += heights[i]
    return dict(result)


def control_weights():
    yield 'uniform', (F(1, 16),)*16
    yield 'asymmetric', tuple(F(i+1, 136) for i in range(16))
    isometric = [F(0)]*16
    for label, mass in [(('core', 0, 0), F(1, 6)),
                        (('core', 1, 1), F(1, 3)),
                        (('flap', 2, 0), F(1, 3)),
                        (('flap', 3, 1), F(1, 6))]:
        isometric[INDEX[label]] = mass
    yield 'nontrivial_isometry', tuple(isometric)
    epsilon = F(1, 1000)
    near = [(1-epsilon)*x for x in isometric]
    near[INDEX[('core', 2, 2)]] += epsilon
    yield 'near_isometry', tuple(near)
    two = [F(0)]*16
    two[INDEX[('flap', 0, 1)]] = F(1, 2)
    two[INDEX[('flap', 1, 0)]] = F(1, 2)
    yield 'two_flaps_no_core', tuple(two)


def analyze(name, vertices, heights):
    vertices = tuple(tuple(map(F, p)) for p in vertices)
    heights = tuple(map(F, heights))
    d = normals(vertices, heights)
    require(rank([sub(p, vertices[0]) for p in vertices[1:]]) == 3,
            'nondegenerate core')
    require(all(h > 0 for h in heights), 'positive normal heights')
    require(tuple(sum(d[i][k]/heights[i] for i in range(4)) for k in range(3)) == ZERO,
            'positive dependence of normals')
    require(all(rank([d[i] for i in ids]) == 3 for ids in combinations(range(4), 3)),
            'every three normals independent')
    gram = [[dot(x, y) for y in d] for x in d]
    require(rank(gram) == 3, 'rank-three obstruction to two auxiliary coordinates')

    # This checks each term in the quotient-rule numerator, not only its sum.
    numerator_checks = 0
    for i in range(4):
        for j in range(4):
            if i == j:
                continue
            for k in range(4):
                require(dot(d[i], sub(vertices[j], vertices[k])) ==
                        (-heights[i] if k == i else 0), 'divergence coefficient')
                numerator_checks += 1

    bases = [vertices[j] for _, _, j in LABELS]
    velocities = [ZERO if typ == 'core' else d[i] for typ, i, _ in LABELS]
    losses = {}
    expected_quadratic = gamma_polynomial(heights)
    direct_quadratic = {}
    pair_types = Counter()
    for i, j in combinations(range(16), 2):
        p = distance_polynomial(bases[i], scale(-1, velocities[i]),
                                bases[j], scale(-1, velocities[j]))
        q = distance_polynomial(bases[i], velocities[i], bases[j], velocities[j])
        loss = tuple(x-y for x, y in zip(p, q))
        coefficient = expected_loss(LABELS[i], LABELS[j], heights)
        require(loss == (0, coefficient, 0), 'complete depth polynomial')
        require(coefficient >= 0, 'all-depth contraction')
        losses[i, j] = coefficient
        pair_types['tight' if coefficient == 0 else 'strict'] += 1
        if coefficient:
            direct_quadratic[i, j] = 2*coefficient
    require(direct_quadratic == {key: 8*value for key, value in expected_quadratic.items()},
            'quadratic identity E(loss)=8t Gamma')
    require(pair_types == {'tight': 78, 'strict': 42}, 'known pair counts')

    controls = {}
    for control, weights in control_weights():
        require(sum(weights) == 1 and min(weights) >= 0, 'weight normalization')
        w = [sum(weights[k] for k, (_, _, tip) in enumerate(LABELS) if tip == i)
             for i in range(4)]
        gamma = sum(heights[i]*weights[k]*w[i]
                    for k, (typ, i, _) in enumerate(LABELS) if typ == 'flap')
        direct = sum(2*weights[i]*weights[j]*loss for (i, j), loss in losses.items())
        preserved = all(loss == 0 for (i, j), loss in losses.items() if weights[i]*weights[j])
        require(direct == 8*gamma, 'weighted direct distance sum')
        require((gamma == 0) == preserved, 'isometry equivalence')
        require((gamma == 0) == (control == 'nontrivial_isometry'), 'control classification')
        if control == 'near_isometry':
            require(gamma == heights[2]*F(999, 3000000), 'exact approach to isometry')
        controls[control] = {'Gamma': str(gamma), 'isometry': preserved}

    return {'name': name, 'vertices': [[str(x) for x in p] for p in vertices],
            'normals': [[str(x) for x in p] for p in d],
            'heights': list(map(str, heights)), 'normal_gram_rank': 3,
            'pair_polynomials': len(losses), 'pair_types': dict(sorted(pair_types.items())),
            'divergence_coefficients': numerator_checks,
            'weight_polynomial_terms': len(expected_quadratic), 'controls': controls}


def run():
    regular = ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
    asymmetric = ((0, 0, 0), (2, 0, 0), (1, 3, 0), (1, 1, 4))
    return {'scope': 'Exact geometric/coefficient controls; analytic hinge theorem is in PROOF.md',
            'fixtures': [analyze('regular', regular, (4, 4, 4, 4)),
                         analyze('asymmetric_unequal_depths', asymmetric, (1, 2, 3, 5))]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='compare complete result with EXPECTED.json')
    args = parser.parse_args()
    result = run()
    canonical = (json.dumps(result, indent=2, sort_keys=True)+'\n').encode()
    if args.check:
        expected = Path(__file__).with_name('EXPECTED.json').read_bytes()
        require(canonical == expected, 'EXPECTED.json mismatch')
        print('PASS: 240 pair polynomials; 96 divergence coefficients; two exact weight identities')
        print('PASS: asymmetric geometry, rank-three obstruction, and five weight controls per fixture')
        print('EXPECTED.json sha256', hashlib.sha256(canonical).hexdigest())
    else:
        print(canonical.decode(), end='')


if __name__ == '__main__':
    main()
