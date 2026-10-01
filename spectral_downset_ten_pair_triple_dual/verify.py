#!/usr/bin/env python3
"""Exact n10 cap dual; Python3.10+ standard library only.

Author six-downset-3, researcher. No optimizer, Decimal, floating input,
prior verifier, imported matrices, or external certificate is used.
The necessity bridge for all real matrices is the ordinary proof.
"""
import argparse
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path
import re


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rational(value):
    require(type(value) is str and re.fullmatch(r'-?\d+(?:/[1-9]\d*)?', value),
            'exact rational string required')
    return F(value)


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


def constant_geometry():
    layers = list(range(2, 9))
    b = [comb(10, k) for k in layers]
    g = [[F(b[i] if i == j else 0)+F(k*l*b[i]*b[j], 10)
          +(k-1)*(l-1)*b[i]*b[j] for j, l in enumerate(layers)] for i, k in enumerate(layers)]
    a = 10+sum(k*k*b[i] for i, k in enumerate(layers))
    e = sum(k*(k-1)*b[i] for i, k in enumerate(layers))
    d = 1+sum((k-1)**2*b[i] for i, k in enumerate(layers))
    delta = a*d-e*e
    require(delta > 0, 'positive rank-two determinant required')
    u, v = [k*b[i] for i, k in enumerate(layers)], [(k-1)*b[i] for i, k in enumerate(layers)]
    wnum = [[delta*(b[i] if i == j else 0)
             -d*u[i]*u[j]+e*(u[i]*v[j]+v[i]*u[j])-a*v[i]*v[j]
             for j in range(7)] for i in range(7)]
    w = [[F(x, delta) for x in row] for row in wnum]
    gi = inverse(g)
    require(w == [[b[i]*b[j]*gi[i][j] for j in range(7)] for i in range(7)],
            'Woodbury/full Gram inverse disagreement')
    positive_ldl(g)
    positive_ldl(w)
    return layers, b, g, w, wnum, [[a, e], [e, d]], delta


def decode(c):
    require(type(c['n']) is int and c['n'] == 10, 'only n10 is claimed')
    require(type(c['N']) is int and c['N'] == 1013, 'wrong cap scale')
    require(type(c['s']) is int and c['s'] == 502, 'wrong star size')
    require(c['layers'] == list(range(2, 9)), 'canonical layer order')
    K = c['common_denominator']
    require(type(K) is int and K > 0, 'positive integer common denominator')
    matrices = [c['lower_numerator'], c['upper_numerator']]
    for a in matrices:
        require(len(a) == 7 and all(len(row) == 7 for row in a), 'seven by seven certificate')
        require(all(type(x) is int for row in a for x in row), 'integer coefficients only')
        require(a == transpose(a), 'symmetric certificate required')
    allowed = [[2, 2], [2, 3], [2, 8], [3, 7], [4, 6], [5, 5]]
    require(c['cancelled_unordered_layer_pairs'] == allowed, 'exact claimed support list')
    gamma = [[matrices[0][i][j]-matrices[1][i][j] for j in range(7)] for i in range(7)]
    require(all(gamma[k-2][l-2] == 0 for k, l in allowed), 'allowed orbit failed to cancel')
    beta = rational(c['weighted_mass_lower_bound'])
    simple = rational(c['simple_strict_lower_bound'])
    require(simple == F(11, 2500) and beta > simple, 'positive simple strict bound')
    return matrices[0], matrices[1], gamma, K, beta, allowed


def verify(c, controls=True):
    xnum, ynum, gamma_num, K, beta, allowed = decode(c)
    xp, xm, xc = positive_integer_matrix(xnum)
    yp, ym, yc = positive_integer_matrix(ynum)
    layers, b, g, w, wnum, H, delta = constant_geometry()
    integer_part = 502*sum(b[i]*gamma_num[i][i] for i in range(7))
    integer_part -= sum(b[i]*b[j]*gamma_num[i][j] for i in range(7) for j in range(7))
    constant = F(1013*trace(ynum, wnum)+delta*integer_part, K*delta)
    require(constant == -beta, 'exact dual constant differs')
    x, y = [[[F(v, K) for v in row] for row in a] for a in [xnum, ynum]]
    gamma = [[F(v, K) for v in row] for row in gamma_num]
    c0 = [[F(502*b[i] if i == j else 0)-b[i]*b[j] for j in range(7)] for i in range(7)]
    u0 = [[1013*w[i][j]-c0[i][j] for j in range(7)] for i in range(7)]
    require(trace(x, c0)+trace(y, u0) == constant, 'independent compressed trace constant')
    cancellations = []
    for k, l in allowed:
        coefficient = b[k-2]*comb(10-k, l)
        direction = [[0]*7 for _ in range(7)]
        direction[k-2][l-2] = coefficient
        direction[l-2][k-2] = coefficient
        cancellations.append(trace(gamma_num, direction))
    require(cancellations == [0]*6, 'affine coefficient cancellation')
    require(gamma[0][2] > 0, 'positive added two/four coefficient')
    two_four_ordered_count = 2*comb(10, 2)*comb(8, 4)
    two_four_bound = beta/(two_four_ordered_count*gamma[0][2])
    require(two_four_ordered_count == 6300 and two_four_bound == F(51782073223, 946576514520),
            'two/four extension normalization')
    result = {
        'agent': 'six-downset-3', 'role': 'researcher', 'n': 10, 'N': 1013, 's': 502,
        'proof_status': 'Exact rational architecture obstruction and strict signed inequality; author-checked, unformalized, independently unreviewed.',
        'constant': str(constant), 'weighted_mass_lower_bound': str(beta),
        'simple_strict_lower_bound': '11/2500', 'dual_ranks': [7, 7],
        'affine_cancellations': cancellations, 'Woodbury_2x2': H,
        'Woodbury_determinant': delta, 'all_principal_minors_checked': [xc, yc],
        'lower_LDL_pivots_integer_numerator': list(map(str, xp)),
        'upper_LDL_pivots_integer_numerator': list(map(str, yp)),
        'lower_leading_principal_minors': xm, 'upper_leading_principal_minors': ym,
        'sole_two_four_extension': {'ordered_pairs': two_four_ordered_count,
                                    'strict_average_L_entry_lower_bound': str(two_four_bound),
                                    'individual_weights_may_be_nonuniform': True},
        'additional_disjoint_layer_pairs': [
            {'sizes': [k, l], 'coefficient': str(gamma[i][j])}
            for i, k in enumerate(layers) for j, l in enumerate(layers)
            if i <= j and k+l <= 10 and [k, l] not in allowed],
    }
    if controls:
        result['literal_controls'] = literal_controls(b, g, w, x, y, gamma_num, K, beta, allowed)
        result['negative_controls'] = negative_controls(c)
    return result


def literal_controls(b, g, w, x, y, gamma_num, K, beta, allowed):
    members = [a for a in range(1 << 10) if a.bit_count() <= 8]
    middle = [a for a in members if a.bit_count() >= 2]
    require(len(members) == 1013 and len(middle) == 1002, 'literal family size')
    require([sum(bool(a & (1 << i)) for a in members) for i in range(10)] == [502]*10,
            'literal star sizes')
    groups = [[a for a in middle if a.bit_count() == k] for k in range(2, 9)]
    require(list(map(len, groups)) == b, 'literal layer sizes')
    images = [[sum(a.bit_count()-1 for a in group)]
              + [-sum(bool(a & (1 << i)) for a in group) for i in range(10)]
              + [int(a.bit_count() == k) for a in middle]
              for k, group in zip(range(2, 9), groups)]
    require([[sum(u*v for u, v in zip(row, other)) for other in images]
             for row in images] == g, 'all literal forced-face Gram entries')
    aggregate = [[F(502*b[i] if i == j else 0)-b[i]*b[j] for j in range(7)] for i in range(7)]
    mass_num, pairs, cancelled = 0, 0, 0
    histogram = {}
    for i, a in enumerate(middle):
        k = a.bit_count()
        for other in middle[i+1:]:
            if a & other:
                continue
            l = other.bit_count()
            pair = tuple(sorted((k, l)))
            histogram[pair] = histogram.get(pair, 0)+1
            pairs += 1
            # Synthetic, signed, nonuniform entries; no PSD or cap is asserted.
            value = ((a+other)*7+(a ^ other)*3) % 19-9
            aggregate[k-2][l-2] += value
            aggregate[l-2][k-2] += value
            mass_num += 2*gamma_num[k-2][l-2]*value
            if list(pair) in allowed:
                require(gamma_num[k-2][l-2] == 0, 'individual allowed edge cancellation')
                cancelled += 1
    expected = {}
    for k in range(2, 9):
        for l in range(k, 9):
            if k+l <= 10:
                count = comb(10, k)*comb(10-k, l)
                if k == l:
                    require(count % 2 == 0, 'unordered equal-layer count')
                    count //= 2
                expected[(k, l)] = count
    require(histogram == expected, 'complete literal disjoint orbit counts')
    upper = [[1013*w[i][j]-aggregate[i][j] for j in range(7)] for i in range(7)]
    functional = trace(x, aggregate)+trace(y, upper)
    mass = F(mass_num, K)
    require(functional+beta == mass, 'literal unsymmetrized signed identity')
    require(mass and functional+beta != mass/2, 'ordered factor-two control')
    return {'middle_sets': len(middle), 'literal_Gram_entries': 49,
            'all_unordered_disjoint_middle_pairs': pairs,
            'individual_allowed_pairs_cancelled': cancelled,
            'disjoint_orbits': [{'sizes': list(key), 'unordered_pairs': value}
                                for key, value in sorted(histogram.items())],
            'synthetic_signed_mass': str(mass), 'ordered_factor_two_control': True,
            'synthetic_fixture_is_not_a_feasible_matrix': True}


def negative_controls(c):
    cases = []
    def add(name, change):
        damaged = deepcopy(c)
        change(damaged)
        cases.append((name, damaged))
    add('float_coefficient', lambda d: d['lower_numerator'][0].__setitem__(0, 1.0))
    add('boolean_coefficient', lambda d: d['lower_numerator'][0].__setitem__(0, True))
    add('wrong_order', lambda d: d.__setitem__('n', 9))
    add('wrong_cap_scale', lambda d: d.__setitem__('N', 1012))
    add('reversed_layers', lambda d: d.__setitem__('layers', d['layers'][::-1]))
    add('zero_denominator', lambda d: d.__setitem__('common_denominator', 0))
    add('asymmetric_lower', lambda d: d['lower_numerator'][0].__setitem__(2, d['lower_numerator'][0][2]+1))
    add('negative_lower_pivot', lambda d: d['lower_numerator'][2].__setitem__(2, -1))
    add('negative_upper_pivot', lambda d: d['upper_numerator'][2].__setitem__(2, -1))
    def remove23(d):
        d['upper_numerator'][0][1] -= 1
        d['upper_numerator'][1][0] -= 1
    add('uncancelled_two_triple_orbit', remove23)
    add('wrong_dual_constant', lambda d: d.__setitem__('weighted_mass_lower_bound', str(rational(d['weighted_mass_lower_bound'])+1)))
    rejected = []
    for name, damaged in cases:
        try:
            verify(damaged, controls=False)
        except (ValueError, KeyError, TypeError, ZeroDivisionError):
            rejected.append(name)
        else:
            raise ValueError('Damaged certificate accepted: '+name)
    # Small determinant/LDL controls exercise pivoting and indefinite input.
    require(determinant([[0, 1], [1, 0]]) == -1, 'Bareiss row-pivot control')
    require(determinant([[1, 2], [2, 4]]) == 0, 'Bareiss singular control')
    require(determinant([[3, 1], [1, 2]]) == 5, 'Bareiss positive control')
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    path = Path(__file__).with_name('CERTIFICATE.json')
    content = path.read_bytes()
    result = verify(json.loads(content))
    result['certificate_sha256'] = sha256(content).hexdigest()
    output = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(output)
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
