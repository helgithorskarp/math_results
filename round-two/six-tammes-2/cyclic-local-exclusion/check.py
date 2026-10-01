#!/usr/bin/env python3
"""Exact, standard-library verification of the cyclic Tammes-15 certificate."""
import argparse
import copy
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

F = tuple(map(Q, (-1, -3, 2, 6, -1, 13)))
ZERO = (Q(0),) * 5
ONE = (Q(1),) + ZERO[1:]
T = (Q(0), Q(1), Q(0), Q(0), Q(0))
LO = Q('0.59260590292507377809642492233275')
HI = Q('0.59260590292507377809642492233276')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def sub(a, b):
    return add(a, neg(b))


def mul(a, b):
    c = [Q(0)] * 9
    for i in range(5):
        for j in range(5):
            c[i+j] += a[i] * b[j]
    for k in range(8, 4, -1):
        z = c[k] / F[5]
        for j in range(6):
            c[k-5+j] -= z * F[j]
    return tuple(c[:5])


def scale(a, c):
    return tuple(c*x for x in a)


def vsum(vectors):
    result = ZERO
    for v in vectors:
        result = add(result, v)
    return result


def matvec(H, v):
    return tuple(vsum(mul(H[i][j], v[j]) for j in range(3)) for i in range(3))


def dot(a, b):
    return vsum(mul(x, y) for x, y in zip(a, b))


def iadd(a, b):
    return a[0]+b[0], a[1]+b[1]


def imul(a, b):
    values = (a[0]*b[0], a[0]*b[1], a[1]*b[0], a[1]*b[1])
    return min(values), max(values)


def interval(poly, domain=(LO, HI)):
    result = (Q(0), Q(0))
    for c in reversed(poly):
        result = iadd(imul(result, domain), (c, c))
    return result


def evaluate(poly, x):
    result = Q(0)
    for c in reversed(poly):
        result = result*x+c
    return result


def readpoly(p):
    require(isinstance(p, list) and len(p) == 5, 'polynomial must have five coefficients')
    return tuple(Q(c) for c in p)


def reflected(V, new, i, j, old):
    # This identity avoids division in the independent checker.
    for k in range(3):
        left = mul(add(ONE, T), add(V[new][k], V[old][k]))
        right = scale(mul(T, add(V[i][k], V[j][k])), Q(2))
        require(left == right, 'triangle reflection identity failed')


def nearest_integer(x):
    return (2*x.numerator+x.denominator)//(2*x.denominator)


def verify(data, verbose=True):
    require(evaluate(F, LO) < 0 < evaluate(F, HI), 'root bracket failed')
    derivative = tuple(i*F[i] for i in range(1, 6))
    require(interval(derivative)[0] > 0, 'root uniqueness in bracket failed')
    require(Q(0) < LO < HI < Q(3, 5), 'metric domain failed')
    require(len(data['vectors']) == 15, 'wrong number of vectors')
    V = []
    for v in data['vectors']:
        require(len(v) == 3, 'vector dimension failed')
        V.append(tuple(readpoly(p) for p in v))
    H = tuple(tuple(ONE if i == j else T for j in range(3)) for i in range(3))
    HV = [matvec(H, v) for v in V]
    for i in range(15):
        require(dot(V[i], HV[i]) == ONE, 'unit vector identity failed')
    for k, i in enumerate((0, 5, 11)):
        require(V[i] == tuple(ONE if j == k else ZERO for j in range(3)), 'anchor basis failed')
    for step in ((6, 0, 11, 5), (7, 0, 5, 11), (9, 5, 11, 0), (14, 0, 6, 11), (12, 5, 7, 0), (13, 11, 9, 5),
                 (3, 1, 4, 2), (8, 2, 4, 1), (10, 1, 2, 4)):
        reflected(V, *step)
    # Circulant cross Gram matrix of the two anchor triples.
    a = tuple(map(Q, ('-27/2', '-3', '35', '-24', '117/2')))
    b = tuple(map(Q, ('-31/4', '-19/2', '34', '-53/2', '195/4')))
    c = tuple(map(Q, ('81/4', '21/2', '-69', '101/2', '-429/4')))
    M = ((a, b, c), (c, a, b), (b, c, a))
    for i, ai in enumerate((0, 5, 11)):
        for j, bj in enumerate((1, 2, 4)):
            require(dot(V[ai], HV[bj]) == M[i][j], 'cross Gram identity failed')
    gram = [[dot(V[i], HV[j]) for j in range(15)] for i in range(15)]
    contacts = []
    for i in range(15):
        for j in range(i+1, 15):
            g = gram[i][j]
            if g == T:
                contacts.append([i, j])
            else:
                require(interval(g)[1] < Q(17, 40), 'noncontact bound failed')
    require(len(contacts) == 30 and contacts == data['edges'], 'contact list failed')
    permutation = list(range(15))
    for cycle in ((0,5,11), (1,2,4), (6,7,9), (14,12,13), (3,10,8)):
        for i,j in zip(cycle, cycle[1:]+cycle[:1]):
            permutation[i] = j
    require(all(gram[i][j] == gram[permutation[i]][permutation[j]]
                for i in range(15) for j in range(15)), 'threefold Gram symmetry failed')
    remaining = {tuple(e) for e in contacts}
    orbits = []
    while remaining:
        edge = min(remaining)
        orbit = []
        while edge not in orbit:
            orbit.append(edge)
            edge = tuple(sorted((permutation[edge[0]], permutation[edge[1]])))
        require(len(orbit) == 3 and set(orbit) <= remaining, 'threefold edge orbit failed')
        orbits.append([list(e) for e in orbit])
        remaining -= set(orbit)
    require(orbits == data['orbits'], 'ten exact edge orbits failed')
    require(len(data['weights']) == 30, 'wrong stress size')
    weights = [readpoly(w) for w in data['weights']]
    edge_weights = {tuple(e):w for e,w in zip(contacts,weights)}
    require(all(len({edge_weights[tuple(e)] for e in orbit}) == 1 for orbit in orbits),
            'invariant stress failed')
    for w in weights:
        require(w == ONE or interval(sub(w, ONE))[0] > 0, 'stress weight below one')
    require(interval(vsum(weights))[1] < 183, 'stress sum bound failed')
    equilibrium = [[ZERO]*3 for _ in range(15)]
    for (i, j), w in zip(contacts, weights):
        for k in range(3):
            equilibrium[i][k] = add(equilibrium[i][k], mul(w, sub(V[j][k], mul(T, V[i][k]))))
            equilibrium[j][k] = add(equilibrium[j][k], mul(w, sub(V[i][k], mul(T, V[j][k]))))
    require(all(x == ZERO for row in equilibrium for x in row), 'stress equilibrium failed')
    chosen = data['selected_edges']
    require(len(chosen) == 27 and len(set(chosen)) == 27 and
            all(isinstance(k, int) and 0 <= k < 30 for k in chosen), 'selected contacts failed')
    R = []
    for i in range(15):
        row = [ZERO]*45
        row[3*i:3*i+3] = HV[i]
        R.append(row)
    for k in chosen:
        i, j = contacts[k]
        row = [ZERO]*45
        row[3*i:3*i+3] = HV[j]
        row[3*j:3*j+3] = HV[i]
        R.append(row)
    for k in (1, 2, 17):
        row = [ZERO]*45
        row[k] = ONE
        R.append(row)
    scaleR = 10**8
    enclosures = [[interval(p) for p in row] for row in R]
    grid = [[nearest_integer((lo+hi)*scaleR/2) for lo, hi in row] for row in enclosures]
    errorR = max(sum(max(abs(lo-Q(g, scaleR)), abs(hi-Q(g, scaleR)))
                     for (lo, hi), g in zip(row, rowgrid))
                 for row, rowgrid in zip(enclosures, grid))
    A = data['inverse_numerators']
    scaleA = data['inverse_scale']
    require(isinstance(scaleA, int) and scaleA > 0, 'inverse scale failed')
    require(len(A) == 45 and all(len(row) == 45 and all(type(x) is int for x in row)
                               for row in A), 'inverse shape failed')
    normA = Q(max(sum(abs(x) for x in row) for row in A), scaleA)
    require(normA < 46, 'approximate inverse norm bound failed')
    denominator = scaleA*scaleR
    row_errors = []
    for i in range(45):
        row_errors.append(sum(abs((denominator if i == j else 0)-
                                 sum(A[i][k]*grid[k][j] for k in range(45)))
                              for j in range(45)))
    error = Q(max(row_errors), denominator)+normA*errorR
    require(error < Q(1, 1000), 'Neumann inverse residual failed')
    require(normA/(1-error) < 46, 'inverse norm certification failed')
    require(Q(144,5)*46*183*Q(1, 250000) < 1, 'local radius inequality failed')
    # PROOF.md derives these scalar bridges from the two pinned prior theorems.
    require(Q(8,5)*Q(1,400000) == Q(1,250000), 'Euclidean to coefficient radius')
    require(2*46*183 == 16836 and 3*16836 == 50508, 'linear growth constants')
    tolerance = Q(1,10**16)
    require(tolerance <= Q(1,10**13), 'entry into the prior completion theorem')
    require(2100000000*tolerance <= Q(1,100), 'rotation gauge domain')
    require(10*2100000000*tolerance <= Q(1,400000),
            'both local exclusion neighborhoods reached')
    result = {'status': 'VERIFIED', 'points': 15, 'contacts': 30,
              'noncontact_cosine_upper': '17/40', 'stress_minimum_lower': '1',
              'stress_sum_upper': '183', 'spherical_rigidity_rank': 42,
              'gauged_inverse_norm_upper': '46', 'inverse_residual_upper': '1/1000',
              'coefficient_radius': '1/250000', 'linear_growth_lower': '1/16836',
              'euclidean_radius': '1/400000', 'euclidean_linear_growth_lower': '1/50508',
              'twenty_six_contact_tolerance': '1/10000000000000000'}
    if verbose:
        print(json.dumps(result, sort_keys=True))
    return result


def selftest(data):
    require(mul(ONE, T) == T and interval((Q(1), Q(-2)), (Q(2), Q(3))) == (Q(-5), Q(-3)),
            'arithmetic self-test failed')
    bad = copy.deepcopy(data)
    bad['weights'][0][0] = str(Q(bad['weights'][0][0])+Q(1, 1000))
    try:
        verify(bad, False)
    except ValueError:
        pass
    else:
        raise ValueError('corrupt stress accepted')
    bad = copy.deepcopy(data)
    bad['inverse_numerators'] = [[0]*45 for _ in range(45)]
    try:
        verify(bad, False)
    except ValueError:
        pass
    else:
        raise ValueError('singular inverse accepted')
    print('SELFTEST: corrupt stress and inverse rejected')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, default=Path(__file__).with_name('certificate.json'))
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    data = json.loads(raw)
    verify(data)
    print('certificate_sha256='+hashlib.sha256(raw).hexdigest())
    if args.selftest:
        selftest(data)
