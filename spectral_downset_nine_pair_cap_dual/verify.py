#!/usr/bin/env python3
"""Exact order-nine cap dual. Actual author six-downset-3, researcher.

Standard library only. The mathematical necessity bridge is in PROOF.md.
No numerical optimizer, prior verifier or external data is imported.
"""
import argparse
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


def inverse(a):
    n = len(a)
    b = [[F(x) for x in row]+[F(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if b[i][j]), None)
        require(pivot is not None, 'singular inverse')
        b[j], b[pivot] = b[pivot], b[j]
        divisor = b[j][j]
        b[j] = [x/divisor for x in b[j]]
        for i in range(n):
            if i != j:
                scale = b[i][j]
                b[i] = [x-scale*y for x, y in zip(b[i], b[j])]
    answer = [row[n:] for row in b]
    require(multiply(a, answer) == [[F(i == j) for j in range(n)] for i in range(n)],
            'inverse residual')
    return answer


def determinant(a):
    """Integer Bareiss determinant with row permutations, no PSD premise."""
    z = [row[:] for row in a]
    require(all(type(x) is int for row in z for x in row), 'integer determinant')
    n, previous, sign = len(z), 1, 1
    for k in range(n-1):
        pivot = next((i for i in range(k, n) if z[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            z[k], z[pivot] = z[pivot], z[k]
            sign = -sign
        divisor = z[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                numerator = divisor*z[i][j]-z[i][k]*z[k][j]
                require(numerator % previous == 0, 'nonexact Bareiss division')
                z[i][j] = numerator//previous
            z[i][k] = 0
        previous = divisor
    return sign*z[-1][-1]


def positive_ldl(a):
    n = len(a)
    require(n and all(len(row) == n for row in a), 'square PSD matrix required')
    require(a == transpose(a), 'asymmetric PSD matrix')
    l = [[F(i == j) for j in range(n)] for i in range(n)]
    pivots = []
    for j in range(n):
        pivot = F(a[j][j])-sum(l[j][k]**2*pivots[k] for k in range(j))
        require(pivot > 0, 'nonpositive LDL pivot')
        pivots.append(pivot)
        for i in range(j+1, n):
            l[i][j] = (F(a[i][j])-sum(l[i][k]*l[j][k]*pivots[k] for k in range(j)))/pivot
    require([[sum(l[i][k]*pivots[k]*l[j][k] for k in range(n)) for j in range(n)]
             for i in range(n)] == a, 'LDL reconstruction')
    return pivots


def trace_product(a, b):
    return sum(a[i][j]*b[j][i] for i in range(len(a)) for j in range(len(a)))


def quadratic(v, a):
    return sum(v[i]*a[i][j]*v[j] for i in range(len(v)) for j in range(len(v)))


def data(certificate):
    require(certificate['n'] == 9 and type(certificate['n']) is int, 'only order nine proved')
    require(certificate['layers'] == list(range(2, 8)), 'canonical layer order')
    H, P = certificate['vector_numerator'], certificate['upper_numerator']
    d = certificate['vector_denominator']
    require(type(d) is int and d > 0, 'positive integer vector denominator')
    require(type(certificate['upper_denominator']) is int and
            certificate['upper_denominator'] == d*d, 'shared squared denominator')
    require(len(H) == 6 and all(type(x) is int for x in H), 'integer vector of length six')
    require(len(P) == 6 and all(len(row) == 6 for row in P) and
            all(type(x) is int for row in P for x in row), 'integer six by six matrix')
    require(P[0][0] == H[0]*H[0], 'two-set coefficient does not cancel')
    require(all(P[i][5-i] == H[i]*H[5-i] for i in range(6)), 'complement coefficients do not cancel')
    pivots = positive_ldl(P)
    minors = []
    for size in range(1, 7):
        for indices in combinations(range(6), size):
            minor = determinant([[P[i][j] for j in indices] for i in indices])
            require(minor > 0, 'nonpositive principal minor')
            if indices == tuple(range(size)):
                minors.append(minor)
    h, y = [F(x, d) for x in H], [[F(x, d*d) for x in row] for row in P]
    beta = rational(certificate['weighted_mass_lower_bound'])
    require(beta > 0, 'positive obstruction required')
    return h, y, beta, pivots, minors


def blocks():
    layers = list(range(2, 8)); b = [comb(9, k) for k in layers]
    D = [[F(b[i] if i == j else 0) for j in range(6)] for i in range(6)]
    G = [[D[i][j]+F(k*l*b[i]*b[j], 9)+(k-1)*(l-1)*b[i]*b[j]
          for j, l in enumerate(layers)] for i, k in enumerate(layers)]
    K = [[502*x for x in row] for row in multiply(multiply(D, inverse(G)), D)]
    A = [[F(247*b[i] if i == j else 0)-b[i]*b[j]
          +(247*b[i] if i+j == 5 else 0) for j in range(6)] for i in range(6)]
    B = [[K[i][j]-A[i][j] for j in range(6)] for i in range(6)]
    return layers, b, G, K, A, B


def woodbury_constant(h, y):
    """Independent rank-two formula: no six by six Gram inverse or blocks."""
    layers = list(range(2, 8)); b = [comb(9, k) for k in layers]
    T = [[9+sum(k*k*comb(9, k) for k in layers),
          sum(k*(k-1)*comb(9, k) for k in layers)],
         [sum(k*(k-1)*comb(9, k) for k in layers),
          1+sum((k-1)**2*comb(9, k) for k in layers)]]
    determinant_T = T[0][0]*T[1][1]-T[0][1]*T[1][0]
    require(determinant_T > 0, 'rank-two Gram determinant')
    inv = [[F(T[1][1], determinant_T), F(-T[0][1], determinant_T)],
           [F(-T[1][0], determinant_T), F(T[0][0], determinant_T)]]
    moments = [[sum(b[i]*b[j]*[layers[i], layers[i]-1][a]
                    *[layers[j], layers[j]-1][c]*y[i][j]
                    for i in range(6) for j in range(6)) for c in range(2)] for a in range(2)]
    return (502*sum(b[i]*y[i][i] for i in range(6))-502*trace_product(inv, moments)
            +247*sum(b[i]*(h[i]**2-y[i][i]) for i in range(6))
            -sum(b[i]*h[i] for i in range(6))**2
            +sum(b[i]*b[j]*y[i][j] for i in range(6) for j in range(6))), T


def verify(certificate, controls=True):
    h, y, beta, pivots, minors = data(certificate)
    layers, b, G, K, A, B = blocks()
    constant = quadratic(h, A)+trace_product(y, B)
    independent, T = woodbury_constant(h, y)
    require(constant == independent == -beta, 'wrong dual constant')
    affine = []
    for i in range(3):
        direction = [[F(0) for _ in layers] for _ in layers]
        direction[i][5-i] = direction[5-i][i] = -b[i]
        affine.append(direction)
    extra = [[F(0) for _ in layers] for _ in layers]
    extra[0][0] = comb(7, 2)*b[0]
    affine.append(extra)
    coefficients = [quadratic(h, a)-trace_product(y, a) for a in affine]
    require(coefficients == [0]*4, 'affine parameter cancellation')
    weights = [[h[i]*h[j]-y[i][j] for j in range(6)] for i in range(6)]
    orbits = [{'sizes':[k,l], 'coefficient':str(weights[i][j])}
              for i,k in enumerate(layers) for j,l in enumerate(layers)
              if i <= j and k+l <= 8 and (k,l) != (2,2)]
    result = {'agent':'six-downset-3','role':'researcher','n':9,'N':502,'s':247,
              'proof_status':'Exact rational cap obstruction and signed support inequality; author-checked, unformalized, unreviewed.',
              'constant':str(constant),'weighted_mass_lower_bound':str(beta),
              'affine_coefficients':[str(x) for x in coefficients],
              'upper_dual_rank':6,'lower_dual_rank':1,
              'LDL_pivots_integer_numerator':[str(x) for x in pivots],
              'leading_principal_minors':minors,'all_principal_minors_checked':63,
              'Woodbury_2x2':T,'signed_orbit_coefficients':orbits}
    if controls:
        result['literal_controls'] = literal_controls(h, y, beta, G, K)
        result['negative_controls'] = negative_controls(certificate)
    return result


def literal_controls(h, y, beta, expected_G, K):
    middle = [a for a in range(512) if 2 <= a.bit_count() <= 7]
    layers = list(range(2, 8)); sizes = [a.bit_count()-2 for a in middle]
    groups = [[a for a in middle if a.bit_count() == k] for k in layers]
    images = [[sum(k-1 for _ in group)]
              +[-sum(int(bool(a >> i & 1)) for a in group) for i in range(9)]
              +[int(a.bit_count() == k) for a in middle] for k,group in zip(layers, groups)]
    literal_G = [[sum(x*y for x,y in zip(a,b)) for b in images] for a in images]
    require(literal_G == expected_G, 'literal forced-face Gram')
    # One synthetic affine-face member with arbitrary signed, nonuniform
    # middle entries. It is not claimed PSD or feasible.
    aggregate = [[F(247*len(groups[i]) if i == j else 0)-len(groups[i])*len(groups[j])
                  for j in range(6)] for i in range(6)]
    core = [[-1 for _ in middle] for _ in middle]
    for i in range(len(middle)):
        core[i][i] = 246
    mass = F(0); pairs = 0; excluded = 0; by_orbit = {}
    for i,a in enumerate(middle):
        for j in range(i+1, len(middle)):
            bb = middle[j]
            if a & bb:
                continue
            pairs += 1
            ki, kj = sizes[i], sizes[j]
            value = ((a+bb)*7+(a^bb)*3) % 17-8
            core[i][j] = core[j][i] = value-1
            aggregate[ki][kj] += value
            aggregate[kj][ki] += value
            coefficient = h[ki]*h[kj]-y[ki][kj]
            if bb == (511 ^ a) or ki == kj == 0:
                require(coefficient == 0, 'individual excluded edge coefficient')
                excluded += 1
            else:
                mass += 2*coefficient*value
                key = tuple(sorted((ki+2,kj+2)))
                by_orbit[key] = by_orbit.get(key,0)+1
    upper = [[K[i][j]-aggregate[i][j] for j in range(6)] for i in range(6)]
    functional = quadratic(h,aggregate)+trace_product(y,upper)
    require(functional+beta == mass, 'literal signed aggregate identity')
    incidence = [[j for j,a in enumerate(middle) if a >> i & 1] for i in range(9)]
    rq = [[sum(core[j][k] for j in incidence[i]) for k in range(len(middle))] for i in range(9)]
    members = [0]+[1 << i for i in range(9)]+middle
    L = [[0 for _ in members] for _ in members]
    for i in range(len(middle)):
        for j in range(len(middle)):
            L[i+10][j+10] = core[i][j]+1
        for point in range(9):
            L[point+1][i+10] = L[i+10][point+1] = 1-rq[point][i]
    for i in range(9):
        for j in range(9):
            L[i+1][j+1] = 1+sum(rq[i][k] for k in incidence[j])
    for i in range(1,502):
        L[0][i] = L[i][0] = 502-sum(L[i][1:])
    L[0][0] = 502-sum(L[0][1:])
    stars = [[j for j,a in enumerate(members) if a >> point & 1] for point in range(9)]
    for i,a in enumerate(members):
        require(sum(L[i]) == 502, 'synthetic row completion')
        require(not a or L[i][i] == 247, 'synthetic nonempty diagonal')
        require(all(L[i][j] == L[j][i] and (i==j or not a&bb or L[i][j]==0)
                    for j,bb in enumerate(members)), 'synthetic symmetry/support')
        require(all(sum(L[i][j] for j in star) == 247 for star in stars), 'synthetic forced stars')
    return {'middle_vertices':len(middle),'full_vertices':502,'Gram_entries':36,
            'all_unordered_disjoint_middle_pairs':pairs,'zero_weight_pairs':excluded,
            'nonzero_orbit_pair_counts':[{'sizes':list(k),'pairs':v} for k,v in sorted(by_orbit.items())],
            'synthetic_full_affine_face_entries':502*502,
            'synthetic_is_PSD_claim':False,'synthetic_signed_mass':str(mass)}


def negative_controls(certificate):
    rejected = []
    def reject(name, mutation):
        c = json.loads(json.dumps(certificate)); mutation(c)
        try:
            verify(c, controls=False)
        except (ValueError, ZeroDivisionError):
            rejected.append(name)
        else:
            raise ValueError('corrupt certificate accepted: '+name)
    reject('wrong_order', lambda c:c.update(n=8))
    reject('permuted_layers', lambda c:c.update(layers=[3,2,4,5,6,7]))
    reject('wrong_squared_denominator', lambda c:c.update(upper_denominator=25))
    reject('float_vector', lambda c:c['vector_numerator'].__setitem__(0,5000.0))
    reject('corrupted_complement_weight', lambda c:c['upper_numerator'][0].__setitem__(5,1))
    reject('indefinite_upper_dual', lambda c:c['upper_numerator'][1].__setitem__(1,-1))
    reject('wrong_constant', lambda c:c.update(weighted_mass_lower_bound='1'))
    reject('decimal_bound', lambda c:c.update(weighted_mass_lower_bound='0.5'))
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, default=Path(__file__).with_name('CERTIFICATE.json'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    result = verify(json.loads(raw))
    result['certificate_sha256'] = sha256(raw).hexdigest()
    text = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
