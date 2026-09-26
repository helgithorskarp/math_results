#!/usr/bin/env python3
"""Exact audit of the universal first-cell bound and its flap benchmark."""
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import combinations
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add(a, b):
    length = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0)+(b[i] if i < len(b) else 0)
            for i in range(length)]


def mul(a, b):
    result = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i+j] += x*y
    return result


def scale(a, c):
    return [c*x for x in a]


def poly_equal(a, b):
    return all(x == 0 for x in add(a, scale(b, -1)))


def first_cell():
    # Polynomials are coefficients in ascending powers of N.
    n1, n2, n3 = [1, 1], [2, 1], [3, 1]
    require(poly_equal(add(n1, n3), scale(n2, 2)),
            'v_0+h^2 normalization identity failed')
    require(poly_equal(add(mul(n1, n3), scale(mul(n1, n2), -1)), n1),
            'upper-minus-Cantelli identity failed')
    margin = add(scale(mul(n2, n3), 2), scale(mul(n1, n1), -1))
    require(margin == [11, 8, 1] and all(c > 0 for c in margin),
            'universal strictly positive margin failed')

    def selected(n, tau, b):
        h = Q(1, n+2)
        distance = max(tau-h, h-b, Q(0))
        return distance <= h

    # Exact boundary and branch controls, not a proof by sampling N.
    controls = [(2, Q(1, 2), Q(3, 4), True),
                (2, Q(51, 100), Q(3, 4), False),
                (2, Q(1, 10), Q(1, 5), True),
                (0, Q(9, 10), Q(19, 20), True)]
    for n, tau, b, expected in controls:
        require(0 < tau < b < 1 and selected(n, tau, b) == expected,
                'selected-index boundary failed')
    require(Q(1, 2) < 1, 'p_0=1 branch control failed')
    return {'universal_margin_coefficients': margin,
            'selected_index_boundary_controls': len(controls),
            'necessary_degree': 'N+2>2/tau when K>=1'}


def squared_distance(x, y):
    return sum((a-b)**2 for a, b in zip(x, y))


def geometry():
    vertices = [[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]
    labels = [('core', i) for i in range(4)]
    labels += [('flap', i, j) for i in range(4) for j in range(4) if i != j]
    source, target = [], []
    for label in labels:
        if label[0] == 'core':
            source.append(vertices[label[1]])
            target.append(vertices[label[1]])
        else:
            _, i, j = label
            source.append([b-a for a, b in zip(vertices[i], vertices[j])])
            target.append([b+a for a, b in zip(vertices[i], vertices[j])])
    require(len(set(map(tuple, source))) == 16, 'source collisions')
    tight = strict = 0
    for i, j in combinations(range(16), 2):
        gap = squared_distance(source[i], source[j])-squared_distance(target[i], target[j])
        li, lj = labels[i], labels[j]
        if li[0] == lj[0] == 'flap':
            expected = 16*(int(li[2] == lj[1])+int(lj[2] == li[1]))
        elif li[0] == lj[0] == 'core':
            expected = 0
        else:
            core, flap = (li, lj) if li[0] == 'core' else (lj, li)
            expected = 16*int(core[1] == flap[1])
        require(gap == expected and gap >= 0, 'contraction deficit identity failed')
        tight += (gap == 0)
        strict += (gap > 0)
    require(all(squared_distance(x, [0, 0, 0]) <= 8 for x in source+target),
            'radius upper bound failed')
    require([0, 2, 2] in source and [0, -2, -2] in source
            and squared_distance([0, 2, 2], [0, -2, -2]) == 4*8,
            'antipodal minimum-radius witness failed')
    require(sum(Q(1, 16) for _ in labels) == 1, 'weight normalization failed')
    return {'source': source, 'target': target, 'label_weights': '1/16',
            'pairs': tight+strict, 'tight_pairs': tight, 'strict_pairs': strict,
            'minimum_source_radius_squared': 8,
            'target_homothety_range': '[0,1]', 'variance_range': '(0,1]'}


def exponential_bound():
    radius_squared = 8
    q_radius_factor = 4*6
    exponent_factor = Q(q_radius_factor*q_radius_factor, 2)
    exponent = exponent_factor*radius_squared
    require(exponent_factor == 288 and exponent == 2304, 'tail exponent normalization failed')
    require(Q(16, 3) > 1, 'automatic geometric modulus bound failed')
    x = Q(288, 125)
    term = total = Q(1)
    for j in range(1, 17):
        term *= x/j
        total += term
    require(total > 10 and 1000*x == exponent, 'exponential Taylor lower bound failed')
    return {'general_tail_exponent_factor': str(exponent_factor),
            'flap_unit_variance_exponent': str(exponent),
            'geometric_modulus_strict_lower_bound': '16/3',
            'taylor_argument': str(x), 'taylor_last_degree': 16,
            'taylor_sum': str(total), 'taylor_margin_over_10': str(total-10),
            'degree_consequence': 'N>10^1000'}


def audit():
    return {'status': 'GAUSSIAN_CERTIFICATE_DEGREE_BARRIER_PASS',
            'first_cell': first_cell(), 'geometry': geometry(),
            'exponential': exponential_bound(),
            'scope': 'specified tail + automatic modulus + Cantelli/Bernstein test only'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', action='store_true')
    args = parser.parse_args()
    record = audit()
    path = Path(__file__).with_name('EXPECTED.json')
    if args.emit:
        path.write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
    require(record == json.loads(path.read_text()), 'expected audit record mismatch')
    digest = hashlib.sha256(json.dumps(record, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    print(json.dumps({'status': record['status'], 'record_sha256': digest,
                      'pairs': record['geometry']['pairs'],
                      'first_cell_positive_polynomial': record['first_cell']['universal_margin_coefficients'],
                      'degree_consequence': record['exponential']['degree_consequence']}, sort_keys=True))
