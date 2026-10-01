#!/usr/bin/env python3
"""Exact two-vector H dual and weighted-face checks; six-downset-3 researcher."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, lcm
from pathlib import Path
import argparse
import copy
import hashlib
import json
import re


def require(ok, why):
    if not ok:
        raise ValueError(why)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def sparse_rank(rows):
    basis = {}
    for source in rows:
        row = {i: Q(v) for i, v in source.items() if v}
        while row:
            p = min(row)
            if p not in basis:
                scale = row[p]
                basis[p] = {i: v/scale for i, v in row.items()}
                break
            t = row[p]
            for i, v in basis[p].items():
                row[i] = row.get(i, 0)-t*v
                if not row[i]:
                    del row[i]
    return len(basis)


def integer_matrix(a):
    require(a and all(len(row) == len(a) for row in a), 'matrix shape')
    d = 1
    for row in a:
        for x in row:
            d = lcm(d, Q(x).denominator)
    return [[int(Q(x)*d) for x in row] for row in a], d


def psd_rank(a):
    z, _ = integer_matrix(a)
    N = len(z)
    require(all(z[i][j] == z[j][i] for i in range(N) for j in range(N)), 'PSD asymmetry')
    previous = 1
    rank = 0
    for k in range(N):
        require(all(z[i][i] >= 0 for i in range(k, N)), 'negative Schur diagonal')
        piv = next((i for i in range(k, N) if z[i][i] > 0), None)
        if piv is None:
            require(all(z[i][j] == 0 for i in range(k, N) for j in range(k, N)),
                    'zero diagonal with nonzero residual')
            break
        if piv != k:
            z[k], z[piv] = z[piv], z[k]
            for row in z:
                row[k], row[piv] = row[piv], row[k]
        pivot = z[k][k]
        for i in range(k+1, N):
            for j in range(i, N):
                value = pivot*z[i][j] - z[i][k]*z[k][j]
                require(value % previous == 0, 'nonexact Bareiss division')
                z[i][j] = z[j][i] = value//previous
        for i in range(k+1, N):
            z[i][k] = z[k][i] = 0
        previous = pivot
        rank += 1
    return rank



def data(n):
    require(n >= 4, 'n')
    full = (1 << n)-1
    F = [1 << i for i in range(n)]+[a for a in range(1 << n)
                                    if 2 <= a.bit_count() <= n-2]
    pairs = [(a, full ^ a) for a in F[n:] if a < (full ^ a)]
    index = {a: i for i, a in enumerate(F)}
    p = 2**(n-1)-n-1
    require(len(pairs) == p and len(F) == n+2*p, 'counts')
    return F, pairs, index, p+1, len(F)+1


def matrix(n, z):
    F, pairs, index, s, N = data(n)
    require(len(z) == len(pairs), 'weights')
    K = [[s*int(i == j) for j in range(len(F))] for i in range(len(F))]
    for i in range(n):
        for j in range(i):
            K[i][j] = K[j][i] = s
    for (A, B), weight in zip(pairs, z):
        a, b = index[A], index[B]
        K[a][b] = K[b][a] = s-weight
        for i in range(n):
            if A & (1 << i):
                K[i][b] = K[b][i] = weight
            else:
                K[i][a] = K[a][i] = weight
            for j in range(i):
                if bool(A & (1 << i)) != bool(A & (1 << j)):
                    K[i][j] -= weight
                    K[j][i] -= weight
    C = [[v-1 for v in row] for row in K]
    sums = [sum(row) for row in C]
    L = [[1+sum(sums)]+[1-v for v in sums]]+[
        [1-sums[i]]+[v+1 for v in row] for i, row in enumerate(C)]
    return C, K, L


def lift(C):
    totals = [sum(row) for row in C]
    return [[1+sum(totals)]+[1-x for x in totals]]+[
        [1-totals[i]]+[1+x for x in row] for i, row in enumerate(C)]


def from_middle(n, middle):
    """Independent forced-star block construction C=[-R;I]Q[-R^T,I]."""
    F, _, _, s, _ = data(n)
    T = F[n:]
    require(len(middle) == len(T), 'middle shape')
    RQ = [[sum(middle[a][b] for a, A in enumerate(T) if A & (1 << i))
           for b in range(len(T))] for i in range(n)]
    C = [[sum(RQ[i][a] for a, A in enumerate(T) if A & (1 << j))
          for j in range(n)]+[-x for x in RQ[i]] for i in range(n)]
    C += [[-RQ[i][a] for i in range(n)]+list(row)
          for a, row in enumerate(middle)]
    K = [[x+1 for x in row] for row in C]
    require(all(K[i][i] == s for i in range(len(F))), 'factor diagonal')
    return C, K, lift(C)


def edge_direction(n, A, B):
    """Sparse derivative of the literal K and row-normalized full L."""
    F, _, index, _, _ = data(n)
    require(A in index and B in index and not A & B and
            min(A.bit_count(), B.bit_count()) >= 2, 'free middle edge')
    K = {}

    def add(i, j, x):
        for a, b in ((i, j), (j, i)):
            K[a, b] = K.get((a, b), 0)+x
            if K[a, b] == 0:
                del K[a, b]

    a, b = index[A], index[B]
    add(a, b, 1)
    for i in range(n):
        if B & (1 << i):
            add(i, a, -1)
        if A & (1 << i):
            add(i, b, -1)
            for j in range(n):
                if B & (1 << j):
                    add(i, j, 1)
    totals = [0]*len(F)
    L = {(i+1, j+1): x for (i, j), x in K.items()}
    for (i, _), x in K.items():
        totals[i] += x
    L[0, 0] = sum(totals)
    for i, x in enumerate(totals):
        if x:
            L[0, i+1] = L[i+1, 0] = -x
    return K, L


def affine_audit(n, complement_only):
    F, pairs, _, s, _ = data(n)
    full = (1 << n)-1
    free = [(A, B) for a, A in enumerate(F[n:]) for B in F[n:][a+1:]
            if not A & B and (not complement_only or A ^ B == full)]
    unknown = [(i, j) for i in range(len(F)) for j in range(i)
               if not F[i] & F[j] and
               (not complement_only or j < n or F[i] ^ F[j] == full)]
    lookup = {tuple(sorted(pair)): k for k, pair in enumerate(unknown)}
    rows = []
    for i in range(n):
        for a, A in enumerate(F):
            if A & (1 << i):
                continue
            row = {}
            for b, B in enumerate(F):
                key = tuple(sorted((a, b)))
                if B & (1 << i) and key in lookup:
                    row[lookup[key]] = 1
            rows.append(row)
    zero = matrix(n, [Q(0)]*len(pairs))[1]
    require(all(sum(zero[unknown[k][0]][unknown[k][1]]*v for k, v in row.items()) == s
                for row in rows), 'affine constant solution')
    rank = sparse_rank(rows)
    require(len(unknown)-rank == len(free), 'complete affine dimension')
    for A, B in free:
        direction, _ = edge_direction(n, A, B)
        values = [direction.get((i, j), 0) for i, j in unknown]
        require(all(sum(values[k]*v for k, v in row.items()) == 0 for row in rows),
                'every independent middle derivative in star kernel')
    return {'n': n, 'complement_only': complement_only,
            'unknowns': len(unknown), 'equations': len(rows), 'rank': rank,
            'affine_dimension': len(free)}



def audit(n, z, dense=True):
    F, pairs, index, s, N = data(n)
    p, m = len(pairs), len(F)
    C, K, L = matrix(n, z)
    independent = from_middle(n, [row[n:] for row in C[n:]])
    require(independent == (C, K, L), 'independent forced-star construction')
    require(all(sum(row) == N for row in L), 'row normalization')
    require(all(K[i][i] == s and all(K[i][j] == 0 for j in range(m)
                if i != j and F[i] & F[j]) for i in range(m)), 'support')
    for i in range(n):
        star = [int(bool(A & (1 << i))) for A in F]
        require(sum(star) == s and all(dot(row, star) == 0 for row in C), 'stars')
    anti, symmetric = [], []
    for A, B in pairs:
        a, b = index[A], index[B]
        anti.append((a, b))
        symmetric.append((a, b))
    # Gram of the complete basis stars, pair differences, pair sums.
    for k, (a, b) in enumerate(anti):
        for ell, (c, d) in enumerate(anti):
            require(C[a][c]-C[a][d]-C[b][c]+C[b][d] == 2*z[k]*int(k == ell),
                    'anti Gram')
            require(C[a][c]+C[a][d]+C[b][c]+C[b][d] ==
                    2*(2*s-z[k])*int(k == ell)-4, 'symmetric Gram')
            require(C[a][c]+C[a][d]-C[b][c]-C[b][d] == 0, 'mixed Gram')
    d = [2*s-v for v in z]
    ordinary = all(0 <= v <= s for v in z) and 2*sum(Q(1, a) for a in d) <= 1
    if not ordinary:
        return {'ordinary': False}
    boundary = int(2*sum(Q(1, a) for a in d) == 1)
    rank = N-n-sum(v == 0 for v in z)-boundary
    if dense:
        require(psd_rank(C) == rank-1 and psd_rank(L) == rank, 'lower rank')
    require(sum(z) <= 2*p, 'linear middle-indicator budget')
    for (A, B), weight in zip(pairs, z):
        if weight == 0:
            require(all(row[index[A]] == row[index[B]] for row in C),
                    'literal zero-pair kernel')
    if boundary:
        v = [Q(0)]*m
        for (A, B), denominator in zip(pairs, d):
            v[index[A]] = v[index[B]] = 1/denominator
        require(all(dot(row, v) == 0 for row in C), 'literal boundary kernel')
    empty = s*(n-2)**2-(n-1)*(n-3)-2*sum(
        (A.bit_count()-1)*(n-A.bit_count()-1)*v for (A, _), v in zip(pairs, z))
    require(L[0][0] == empty, 'empty diagonal')
    V = [[N*int(i == j)-K[i][j] for j in range(m)] for i in range(m)]
    for k, (a, b) in enumerate(anti):
        for ell, (c, d) in enumerate(anti):
            require(V[a][c]-V[a][d]-V[b][c]+V[b][d] ==
                    2*(N-z[k])*int(k == ell), 'upper anti Gram')
            require(V[a][c]+V[a][d]+V[b][c]+V[b][d] ==
                    2*(n-1+z[k])*int(k == ell), 'upper symmetric Gram')
            require(V[a][c]+V[a][d]-V[b][c]-V[b][d] == 0, 'upper mixed Gram')
    B = s-Q(n-1, 2)*sum(v/(n-1+v) for v in z)
    W = [[N*int(i == j)-B-Q(N, 2)*sum(
        v/(N-v)*(2*int(bool(A & (1 << i)))-1)*(2*int(bool(A & (1 << j)))-1)
        for (A, _), v in zip(pairs, z)) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            literal = V[i][j]
            for k, (a, b) in enumerate(anti):
                cp_i, cm_i = V[i][a]+V[i][b], V[i][a]-V[i][b]
                cp_j, cm_j = V[j][a]+V[j][b], V[j][a]-V[j][b]
                literal -= cp_i*cp_j/(2*(n-1+z[k]))+cm_i*cm_j/(2*(N-z[k]))
            require(literal == W[i][j], 'literal upper Schur')
    capped = True
    try:
        wrank = psd_rank(W)
    except ValueError:
        capped, wrank = False, None
    if capped and dense:
        require(psd_rank(V) == 2*p+wrank, 'upper core rank')
        full_upper = [[N*int(i == j)-L[i][j] for j in range(N)] for i in range(N)]
        require(psd_rank(full_upper) == 2*p+wrank, 'full upper rank')
    return {'ordinary': True, 'lower_rank': rank, 'zero_weights': sum(v == 0 for v in z),
            'boundary': boundary, 'capped': capped, 'upper_schur_rank': wrank}


def exact_number(value):
    require(type(value) is str and re.fullmatch(r'-?\d+(?:/[1-9]\d*)?', value),
            'integer or rational string required')
    return Q(value)


def quadratic(a, v):
    return sum(v[i]*dot(row, v) for i, row in enumerate(a))


def sparse_quadratic(a, v):
    return sum(x*v[i]*v[j] for (i, j), x in a.items())


def matrix_hash(a):
    raw = json.dumps([[str(Q(x)) for x in row] for row in a],
                     separators=(',', ':')).encode()
    return hashlib.sha256(raw).hexdigest()


def certificate_vectors(certificate):
    require((certificate['n'], certificate['N'], certificate['s']) == (6, 57, 26)
            and all(type(certificate[k]) is int for k in ('n', 'N', 's')),
            'certificate parameters')
    F, _, _, _, N = data(6)
    layers = certificate['upper_vector_by_set_size']
    require(type(layers) is list and len(layers) == 5, 'upper vector layers')
    layers = [exact_number(x) for x in layers]
    require(certificate['lower_vector'] == '1_(2<=|A|<=4)-(50/57)*1_full',
            'lower vector definition')
    w = [layers[A.bit_count()] for A in [0]+F]
    u = [Q(2 <= A.bit_count() <= 4)-Q(50, N) for A in [0]+F]
    multiplier = exact_number(certificate['lower_multiplier'])
    require(multiplier > 0 and any(w) and any(u), 'rank-one PSD multipliers')
    return w, u, multiplier


def dual_audit(certificate):
    F, pairs, _, s, N = data(6)
    w, u, multiplier = certificate_vectors(certificate)
    _, _, L = matrix(6, [Q(0)]*len(pairs))
    constant = N*dot(w, w)-quadratic(L, w)+multiplier*quadratic(L, u)
    require(constant == exact_number(certificate['identity_constant']) == -Q(86, 15),
            'full dual constant')
    types = {(2, 2): ('identity_22_coefficient', 'unordered_22_edges'),
             (2, 3): ('identity_23_coefficient', 'unordered_23_edges'),
             (2, 4): ('identity_complement_coefficient', None),
             (3, 3): ('identity_complement_coefficient', None)}
    records, counts = [], {key: 0 for key in types}
    for a, A in enumerate(F[6:]):
        for B in F[6:][a+1:]:
            if A & B:
                continue
            Kdir, Ldir = edge_direction(6, A, B)
            full_members = [0]+F
            require(all(not x or (i != j and not full_members[i] & full_members[j])
                        for (i, j), x in Ldir.items() if i or j), 'derivative support')
            require(all(sum(x for (a, _), x in Ldir.items() if a == i) == 0
                        for i in range(N)), 'derivative row sums')
            for i in range(6):
                require(all(sum(x for (a, b), x in Kdir.items()
                                if a == j and F[b] & (1 << i)) == 0
                            for j in range(len(F))), 'derivative forced stars')
            coefficient = -sparse_quadratic(Ldir, w)+multiplier*sparse_quadratic(Ldir, u)
            key = tuple(sorted((A.bit_count(), B.bit_count())))
            require(key in types, 'free edge type coverage')
            field, _ = types[key]
            require(coefficient == exact_number(certificate[field]), 'full dual coefficient')
            counts[key] += 1
            records.append([A, B, str(coefficient)])
    require(len(records) == 130 and counts == {(2, 2): 45, (2, 3): 60,
                                             (2, 4): 15, (3, 3): 10}, 'all free edges')
    for key, (_, countfield) in types.items():
        if countfield:
            require(type(certificate[countfield]) is int and
                    certificate[countfield] == counts[key], 'unordered edge count')
    ratio = exact_number(certificate['identity_22_coefficient'])/exact_number(
        certificate['capped_M_22_coefficient'])
    require(ratio == exact_number(certificate['identity_23_coefficient'])/exact_number(
        certificate['capped_M_23_coefficient']) == Q(16, 25), 'dual scaling ratio')
    require(-constant/(ratio*(N-s)) == exact_number(certificate['capped_M_rhs']) == Q(215, 744),
            'capped M quantitative bound')
    raw = json.dumps(records, separators=(',', ':')).encode()
    return {'full_vertices': N, 'free_middle_edges': len(records),
            'constant': str(constant), 'coefficient_counts': {
                '/'.join(map(str, k)): v for k, v in counts.items()},
            'coefficient_record_sha256': hashlib.sha256(raw).hexdigest(),
            'M_rhs': '215/744', 'dual_PSD_ranks': [1, 1]}


def partition_audit(n):
    F, pairs, index, s, N = data(n)
    partitions = []
    origin = [[1 << i for i in range(n)]]+[list(pair) for pair in pairs]
    # Origin clique: all singletons. Other cliques: each complementary pair.
    partitions.append(origin)
    for A, B in pairs:
        partition = [[A]+[1 << i for i in range(n) if B & (1 << i)],
                     [B]+[1 << i for i in range(n) if A & (1 << i)]]
        partition += [list(pair) for pair in pairs if set(pair) != {A, B}]
        partitions.append(partition)
    total = [[Q(0) for _ in F] for _ in F]
    for k, partition in enumerate(partitions):
        require(len(partition) == s and sorted(x for part in partition for x in part) == sorted(F),
                'partition coverage')
        require(all(not A & B for part in partition for A, B in combinations(part, 2)),
                'partition cliques')
        cell = {A: j for j, part in enumerate(partition) for A in part}
        gram = [[s*int(cell[A] == cell[B])-1 for B in F] for A in F]
        z = [Q(0)]*len(pairs)
        if k:
            z[k-1] = s
        C, _, _ = matrix(n, z)
        require(gram == C, 'literal clique partition coefficient identity')
        for i, row in enumerate(C):
            for j, value in enumerate(row):
                total[i][j] += Q(value)/s
    require(total == matrix(n, [Q(1)]*len(pairs))[0], 'literal partition barycenter')
    basis = [{i: 1 for i, A in enumerate(F) if A & (1 << j)} for j in range(n)]
    for A, B in pairs:
        basis += [{index[A]: 1, index[B]: -1}, {index[A]: 1, index[B]: 1}]
    require(sparse_rank(basis) == N-1, 'complete pair/star basis')
    return {'n': n, 'partitions': len(partitions), 'complete_basis_rank': N-1}


def known_capped_six(certificate):
    """Literal reproduction of graph7980; feasibility is an attributed baseline."""
    n = 6
    F, _, _, s, N = data(n)
    beta = [[Q(x) for x in row] for row in
            [[-2, 0, 2, 4], [0, Q(4, 3), 0, 22], [2, 0, 24, 0], [4, 22, 0, 0]]]
    C = [[s*int(A == B)-1+(beta[A.bit_count()-1][B.bit_count()-1] if not A & B else 0)
          for B in F] for A in F]
    trade = {(1, 1): 12, (1, 2): -3, (2, 2): 1}
    D = [[trade.get(tuple(sorted((A.bit_count(), B.bit_count()))), 0)
          if A != B and not A & B else 0 for B in F] for A in F]
    epsilon = Q(1, 40320)
    w, u, multiplier = certificate_vectors(certificate)
    output = []
    for name, core, target in (('published_centered', C, 50),
                               ('published_repaired', [[C[i][j]+epsilon*D[i][j]
                                  for j in range(len(F))] for i in range(len(F))], 51)):
        L = lift(core)
        require(all(sum(row) == N for row in L), 'known capped row sums')
        require(all(L[i+1][j+1] == s*int(i == j) for i, A in enumerate(F)
                    for j, B in enumerate(F) if A & B), 'known capped support')
        require(psd_rank(core) == target-1 and psd_rank(L) == target,
                'known capped exact lower ranks')
        upper = [[N*int(i == j)-L[i][j] for j in range(N)] for i in range(N)]
        require(psd_rank(upper) == N-1, 'known capped exact upper rank')
        value = quadratic(upper, w)+multiplier*quadratic(L, u)
        sums = {(2, 2): Q(0), (2, 3): Q(0)}
        for i, A in enumerate(F):
            for j in range(i):
                B = F[j]
                key = tuple(sorted((A.bit_count(), B.bit_count())))
                if not A & B and key in sums:
                    sums[key] += L[i+1][j+1]
        identity = -Q(86, 15)+Q(128, 25)*sums[2, 2]+Q(16, 5)*sums[2, 3]
        require(value == identity >= 0, 'known capped full dual identity')
        require((8*sums[2, 2]+5*sums[2, 3])/(N-s) >= Q(215, 744),
                'known capped necessary inequality')
        output.append({'name': name, 'lower_rank': target, 'upper_rank': N-1,
                       'sum22_L': str(sums[2, 2]), 'sum23_L': str(sums[2, 3]),
                       'dual_value': str(value), 'full_L_sha256': matrix_hash(L)})
    return {'attribution': 'six-downset-3 researcher, prior graph7980; validation only',
            'epsilon': str(epsilon), 'cases': output}


def determinant3(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]**2)
            -a[0][1]*(a[0][1]*a[2][2]-a[0][2]*a[1][2])
            +a[0][2]*(a[0][1]*a[1][2]-a[0][2]*a[1][1]))


def backend_audit():
    positive = 0
    for values in product((-1, 0, 1), repeat=6):
        a, b, c, d, e, f = values
        matrix3 = [[a, b, c], [b, d, e], [c, e, f]]
        criterion = (min(a, d, f) >= 0 and min(a*d-b*b, a*f-c*c, d*f-e*e) >= 0
                     and determinant3(matrix3) >= 0)
        try:
            psd_rank(matrix3)
            accepted = True
        except ValueError:
            accepted = False
        require(accepted == criterion, 'PSD engine versus independent principal minors')
        positive += accepted
    require(positive == 24, 'ternary PSD count')
    return {'symmetric_ternary_3x3_matrices': 729, 'PSD_count': positive}


def negative_controls(certificate):
    rejected = []

    def reject(name, work):
        try:
            work()
        except (ValueError, ZeroDivisionError):
            rejected.append(name)
            return
        raise ValueError('negative control accepted: '+name)

    wrong = copy.deepcopy(certificate)
    wrong['upper_vector_by_set_size'][2] = '81/100'
    reject('wrong_upper_vector', lambda: dual_audit(wrong))
    wrong = copy.deepcopy(certificate)
    wrong['lower_multiplier'] = '5'
    reject('wrong_lower_multiplier', lambda: dual_audit(wrong))
    wrong = copy.deepcopy(certificate)
    wrong['capped_M_rhs'] = '216/744'
    reject('wrong_quantitative_bound', lambda: dual_audit(wrong))
    reject('float_certificate_entry', lambda: exact_number(0.8))
    reject('decimal_certificate_entry', lambda: exact_number('0.8'))
    reject('zero_denominator', lambda: exact_number('1/0'))
    reject('indefinite_zero_diagonal', lambda: psd_rank([[0, 1], [1, 0]]))
    for name, weights in (('negative_pair_weight', [-Q(1), Q(0), Q(0)]),
                          ('missing_denominator_domain', [Q(9)]*3),
                          ('false_boundary_PSD', [Q(3)]*3)):
        require(not audit(4, weights, dense=False)['ordinary'], 'invalid domain was accepted')
        reject(name, lambda z=weights: psd_rank(matrix(4, z)[0]))
    require(not audit(6, [Q(1)]*25, dense=False)['capped'], 'false capped family claim')
    rejected.append('false_six_point_cap')
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    certificate = json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
    dual = dual_audit(certificate)
    records = []
    for n in (4, 5, 6):
        _, pairs, _, s, _ = data(n)
        samples = [('zero', [Q(0)]*len(pairs)), ('one', [Q(1)]*len(pairs)),
                   ('two', [Q(2)]*len(pairs)),
                   ('asymmetric', [Q(k % 4, 5) for k in range(len(pairs))]),
                   ('single_partition', [Q(s)]+[Q(0)]*(len(pairs)-1))]
        if n < 6:
            cap = Q(3, 2) if n == 4 else Q(19, 10)
            samples.append(('asymmetric_cap', [cap+Q(1, 100)]+[cap]*(len(pairs)-1)))
        if n == 4:
            samples.append(('left_cap_endpoint', [Q(15, 13)]*len(pairs)))
        for name, weights in samples:
            record = audit(n, weights)
            require(record['ordinary'], 'sample ordinary')
            if name in ('asymmetric_cap', 'left_cap_endpoint'):
                require(record['capped'], 'sample cap')
            records.append({'n': n, 'name': name, **record})
    result = {'agent': 'six-downset-3', 'role': 'researcher',
              'status': 'Written unformalized author-checked proof; exact finite supplementary validation; not independently reviewed.',
              'dual_identity': dual,
              'complement_only_affine_constraints': [affine_audit(n, True) for n in (4, 5, 6, 7)],
              'full_face_affine_constraints': [affine_audit(n, False) for n in (4, 5, 6)],
              'partition_baselines': [partition_audit(n) for n in (4, 5, 6)],
              'literal_weighted_cases': records,
              'known_capped_six_reproduction': known_capped_six(certificate),
              'PSD_engine': backend_audit(), 'negative_controls': negative_controls(certificate)}
    raw = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.write_text(raw)
    print(raw, end='')


if __name__ == '__main__':
    main()
