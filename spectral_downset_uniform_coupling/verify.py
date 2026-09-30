#!/usr/bin/env python3
"""Exact finite checks of arbitrary-rank stable uniform H coupling.

Author six-downset-3, role researcher. CPython 3.11.2 standard library.
PROOF.md supplies the all-parameter completeness and Schur arguments;
this finite checker is validation, not an inference from samples.
No imported campaign code, CAS, solver, floats or external inputs.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from math import comb, gcd, lcm
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def choose(n, k):
    require(n >= 0, 'negative binomial upper argument')
    return comb(n, k) if 0 <= k <= n else 0


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def psd_rank(matrix):
    """Exact symmetric pivoted Schur elimination over Q, including zeros."""
    size = len(matrix)
    require(all(len(row) == size for row in matrix), 'PSD square input')
    require(all(matrix[i][j] == matrix[j][i]
                for i in range(size) for j in range(size)), 'PSD symmetry')
    a = [[Q(x) for x in row] for row in matrix]
    rank = 0
    while a:
        require(all(a[i][i] >= 0 for i in range(len(a))), 'negative diagonal')
        p = next((i for i in range(len(a)) if a[i][i]), None)
        if p is None:
            require(all(not x for row in a for x in row),
                    'zero diagonal with nonzero image')
            break
        indices = [i for i in range(len(a)) if i != p]
        pivot = a[p][p]
        a = [[a[i][j]-a[i][p]*a[p][j]/pivot
              for j in indices] for i in indices]
        rank += 1
    return rank


def nullspace(rows, width):
    """RREF free-column basis, normalized to primitive integer vectors."""
    require(all(len(row) == width for row in rows), 'nullspace input width')
    a = [[Q(x) for x in row] for row in rows]
    pivots = []
    top = 0
    for col in range(width):
        p = next((i for i in range(top, len(a)) if a[i][col]), None)
        if p is None:
            continue
        a[top], a[p] = a[p], a[top]
        divisor = a[top][col]
        a[top] = [x/divisor for x in a[top]]
        for i in range(len(a)):
            if i != top and a[i][col]:
                t = a[i][col]
                a[i] = [x-t*y for x, y in zip(a[i], a[top])]
        pivots.append(col)
        top += 1
        if top == len(a):
            break
    basis = []
    for free in range(width):
        if free in pivots:
            continue
        h = [Q(0)]*width
        h[free] = 1
        for i, p in enumerate(pivots):
            h[p] = -a[i][free]
        scale = lcm(*(x.denominator for x in h))
        v = [int(x*scale) for x in h]
        common = gcd(*v)
        v = [x//common for x in v]
        require(all(dot(row, v) == 0 for row in rows), 'literal nullspace')
        basis.append(v)
    return basis, len(pivots)


def weights(n, r, fraction=Q(1)):
    require(isinstance(n, int) and isinstance(r, int) and r >= 2 and n >= 2*r,
            'stable uniform parameters')
    require(0 <= fraction <= 1, 'coupling fraction in checked interval')
    m = sum(comb(n, a) for a in range(1, r+1))
    N = m+1
    s = sum(comb(n-1, k) for k in range(r))
    epsilon = Q(fraction, 8*N**6)
    gamma = [[comb(n-a-1, b-1) for b in range(1, r+1)]
             for a in range(1, r+1)]
    beta = [[epsilon for _ in range(r)] for _ in range(r)]
    delta = [[Q(1) for _ in range(r)] for _ in range(r)]
    for a in range(r):
        cross = sum(gamma[a][b] for b in range(r) if a != b)
        beta[a][a] = (s-epsilon*cross)/gamma[a][a]
        delta[a][a] = -Q(cross, gamma[a][a])
    return N, s, epsilon, gamma, beta, delta


def check_star_equations(beta, gamma, s):
    r = len(beta)
    require(all(beta[a][b] == beta[b][a]
                for a in range(r) for b in range(r)), 'beta symmetry')
    require(all(sum(beta[a][b]*gamma[a][b] for b in range(r)) == s
                for a in range(r)), 'all star row equations')


def blocks(n, r, s, beta, j):
    layers = list(range(max(1, j), r+1))
    G = [comb(n-2*j, a-j) for a in layers]
    K = [[s*(a == b) - (comb(n, b) if j == 0 else 0)
          + (-1)**j*beta[a-1][b-1]*choose(n-a-j, b-j)
          for b in layers] for a in layers]
    A = [[G[i]*K[i][k] for k in range(len(layers))]
         for i in range(len(layers))]
    return layers, G, K, A


def compressed_case(n, r):
    N, s, epsilon, gamma, beta, delta = weights(n, r)
    check_star_equations(beta, gamma, s)
    check_star_equations(delta, gamma, 0)
    require(all(x > 0 for row in beta for x in row), 'positive disjoint weights')
    require(sum(a*comb(n, a) for a in range(1, r+1)) == n*s,
            'cardinality identity')
    require(all(1 <= gamma[a][a] <= N for a in range(r)), 'integer gap denominator')
    require(all(sum(row) <= s for row in gamma), 'row coefficient bound')
    for a in range(1, r+1):
        for j in range(1, a+1):
            ratio = Q(choose(n-a-j, a-j), gamma[a-1][a-1])
            product = Q(1)
            for t in range(1, j):
                product *= Q(a-t, n-a-t)
            require(ratio == product and ratio <= 1, 'exact Kneser eigenvalue ratio')
            require((ratio == 1) == (j == 1 or n == 2*a), 'all ratio equality cases')
            if j % 2 and ratio < 1:
                require(s*(1-ratio) >= Q(1, N), 'baseline odd positive gap')
    metric = [comb(n-2, a-1) for a in range(1, r+1)]
    lap = [[-gamma[a][b] if a != b else sum(gamma[a][k] for k in range(r) if a != k)
            for b in range(r)] for a in range(r)]
    sym_lap = [[metric[a]*lap[a][b] for b in range(r)] for a in range(r)]
    require(psd_rank(sym_lap) == r-1, 'degree one complete Laplacian rank')
    require(all(metric[a]*gamma[a][b] == metric[b]*gamma[b][a] >= 1
                for a in range(r) for b in range(r) if a != b), 'integer conductances')
    # Independent exact check of the claimed gap on the weighted zero-mean subspace.
    z = [[Q(int(a == i), metric[i])-Q(int(a == r-1), metric[r-1])
          for a in range(r)] for i in range(r-1)]
    restricted = [[sum(x[a]*sym_lap[a][b]*y[b] for a in range(r) for b in range(r))
                   - Q(1, N)*sum(metric[a]*x[a]*y[a] for a in range(r))
                   for y in z] for x in z]
    psd_rank(restricted)
    B = N**2
    g = a_gap = Q(1, N)
    positive_block = g-epsilon*B
    schur_margin = a_gap-epsilon*B*B/positive_block
    require(positive_block >= Q(7, 8*N), 'uniform lower block estimate')
    require(schur_margin >= Q(6, 7*N), 'uniform Schur estimate')
    require((s+1)*(N-1) <= B, 'literal Delta row bound')
    sectors = []
    repaired_rank = baseline_rank = 0
    _, _, _, _, half_beta, _ = weights(n, r, Q(1, 2))
    _, _, _, _, baseline, _ = weights(n, r, Q(0))
    for j in range(r+1):
        layers, G, K, A = blocks(n, r, s, beta, j)
        rank = psd_rank(A)
        expected = len(layers)-int(j in (0, 1))
        require(rank == expected, 'all repaired sector ranks')
        _, _, _, baseA = blocks(n, r, s, baseline, j)
        brank = psd_rank(baseA)
        b_expected = (r-1 if j == 0 else 0 if j == 1 else
                      len(layers)-int(n == 2*r and j % 2 == 1))
        require(brank == b_expected, 'all baseline sector ranks')
        require(psd_rank(blocks(n, r, s, half_beta, j)[3]) == expected,
                'interior coupling has same exact ranks')
        mult = comb(n, j)-(comb(n, j-1) if j else 0)
        repaired_rank += mult*rank
        baseline_rank += mult*brank
        sectors.append({'j': j, 'size': len(layers), 'multiplicity': mult,
                        'baseline_rank': brank, 'coupled_rank': rank})
    require(1+repaired_rank == N-n, 'maximal full lower rank')
    extra_boundary = sum(comb(n, j)-comb(n, j-1)
                         for j in range(3, r+1, 2)) if n == 2*r else 0
    require(N-1-baseline_rank == 1+r*(n-1)+extra_boundary, 'all baseline null directions')
    upper = Q(N-n*s)+epsilon*(n-1)*sum(gamma[0][b] for b in range(1, r))
    require(upper == Q(N-s)-beta[0][0]*(n-1) < 0, 'exact upper cap obstruction')
    return {'n': n, 'r': r, 'N': N, 's': s, 'epsilon': str(epsilon),
            'baseline_core_rank': baseline_rank, 'coupled_lower_rank': repaired_rank+1,
            'forced_star_kernel_dimension': n, 'boundary_extra_nullity': extra_boundary,
            'Schur_margin_lower_bound': str(schur_margin),
            'upper_degree_zero_layer_one_entry': str(upper), 'sectors': sectors}


def subsets(n, a):
    return [sum(1 << i for i in indices) for indices in itertools.combinations(range(n), a)]


def literal_core(n, r, beta):
    vertices = sorted(A for A in range(1, 1 << n) if A.bit_count() <= r)
    s = sum(comb(n-1, k) for k in range(r))
    C = [[Q(s*(A == B)-1)+(beta[A.bit_count()-1][B.bit_count()-1] if not A & B else 0)
          for B in vertices] for A in vertices]
    return vertices, C


def harmonic_basis(n, j):
    level = subsets(n, j)
    if j == 0:
        return level, [[1]]
    below = subsets(n, j-1)
    rows = [[int(T & J == T) for J in level] for T in below]
    basis, rank = nullspace(rows, len(level))
    require(rank == len(below), 'lowering map has full row rank')
    require(len(basis) == comb(n, j)-comb(n, j-1), 'harmonic multiplicity')
    return level, basis


def literal_case(n, r):
    N, s, epsilon, gamma, beta, delta = weights(n, r)
    vertices, C = literal_core(n, r, beta)
    m = len(vertices)
    scale = lcm(*(x.denominator for row in C for x in row))
    C_int = [[int(x*scale) for x in row] for row in C]
    require(N == m+1, 'literal vertex count including empty')
    require(all(C[i][j] == C[j][i] for i in range(m) for j in range(m)), 'literal symmetry')
    require(all(C[i][i] == s-1 for i in range(m)), 'literal diagonal')
    require(all(C[i][j] == -1 for i, A in enumerate(vertices)
                for j, B in enumerate(vertices) if A != B and A & B), 'intersecting core entries')
    stars = [[int(A >> i & 1) for A in vertices] for i in range(n)]
    require(all(sum(x) == s for x in stars), 'literal full stars')
    require(all(dot(row, x) == 0 for row in C_int for x in stars), 'literal star kernel')
    # Reconstruct the empty row and column from E C E^T without importing a constructor.
    sums = [sum(row) for row in C]
    L = [[Q(0)]*N for _ in range(N)]
    L[0][0] = 1+sum(sums)
    for i in range(m):
        L[0][i+1] = L[i+1][0] = 1-sums[i]
        for j in range(m):
            L[i+1][j+1] = 1+C[i][j]
    require(all(sum(row) == N for row in L), 'all full row sums')
    require(all(L[i+1][j+1] == s*(i == j)
                for i, A in enumerate(vertices) for j, B in enumerate(vertices) if A & B),
            'all full H support entries')
    for x in stars:
        y = [Q(-s, N)]+[Q(z)-Q(s, N) for z in x]
        require(all(dot(row, y) == 0 for row in L), 'full centered star kernel')
    _, Delt = literal_core(n, r, delta)
    Delt = [[Delt[i][j]-Q(s*(i == j)-1) for j in range(m)] for i in range(m)]
    norm_bound = max(sum(abs(x) for x in row) for row in Delt)
    require(norm_bound <= N**2, 'literal full Delta row norm bound')
    direct = None
    if n <= 6:
        direct = {'core_psd_rank': psd_rank(C), 'lower_psd_rank': psd_rank(L)}
        require(direct == {'core_psd_rank': m-n, 'lower_psd_rank': N-n}, 'dense PSD and rank')
    levels = {a: subsets(n, a) for a in range(1, r+1)}
    position = {A: i for i, A in enumerate(vertices)}
    all_lifts = {a: [] for a in levels}
    action_checks = 0
    basis_count = 0
    for j in range(r+1):
        h_level, h_basis = harmonic_basis(n, j)
        layers, G, K, _ = blocks(n, r, s, beta, j)
        lifts = {}
        for a in layers:
            lifts[a] = [[sum(h[t] for t, J in enumerate(h_level) if J & A == J)
                         for A in levels[a]] for h in h_basis]
            for q, x in enumerate(lifts[a]):
                for p, y in enumerate(lifts[a]):
                    require(dot(x, y) == comb(n-2*j, a-j)*dot(h_basis[q], h_basis[p]),
                            'every lifted Gram entry')
                for old_j, old in all_lifts[a]:
                    if old_j != j:
                        require(dot(x, old) == 0, 'all different harmonic degrees orthogonal')
                all_lifts[a].append((j, x))
                basis_count += 1
        for b_index, b in enumerate(layers):
            for q, h in enumerate(h_basis):
                full = [0]*m
                for t, B in enumerate(levels[b]):
                    full[position[B]] = lifts[b][q][t]
                image = [dot(row, full) for row in C_int]
                for a in range(1, r+1):
                    if a in layers:
                        a_index = layers.index(a)
                        factor = scale*K[a_index][b_index]
                        for t, A in enumerate(levels[a]):
                            require(image[position[A]] == factor*lifts[a][q][t],
                                    'literal full matrix action on every lifted basis vector')
                    else:
                        require(all(image[position[A]] == 0 for A in levels[a]),
                                'no action below harmonic degree')
                    action_checks += len(levels[a])
    require(basis_count == m, 'complete lifted basis exhausts literal matrix')
    for a in levels:
        require(len(all_lifts[a]) == len(levels[a]), 'each level basis is complete')
    upper_entry = Q(N-s)-beta[0][0]*(n-1)
    require(upper_entry < 0, 'literal upper core negative constant-singleton form')
    # U=NI-J-C is congruent to NI-L by the same full-column E.
    upper_form = sum(Q(N*(i == j)-1)-C[i][j]
                     for i, A in enumerate(vertices) for j, B in enumerate(vertices)
                     if A.bit_count() == B.bit_count() == 1)
    require(upper_form == n*upper_entry < 0, 'definition-level upper cap failure')
    digest = hashlib.sha256(json.dumps([[str(x) for x in row] for row in L],
                                     separators=(',', ':')).encode()).hexdigest()
    return {'n': n, 'r': r, 'N': N, 's': s, 'complete_lifted_basis_size': basis_count,
            'literal_action_coordinates_checked': action_checks, 'dense_PSD': direct,
            'Delta_max_absolute_row_sum': str(norm_bound),
            'literal_upper_core_form': str(upper_form), 'full_L_sha256': digest}


def small_census(n, r):
    vertices = [A for A in range(1, 1 << n) if A.bit_count() <= r]
    optimum = 0
    maxima = []
    count = 0
    def visit(chosen, available):
        nonlocal optimum, maxima, count
        if not available:
            count += 1
            size = len(chosen)
            if size > optimum:
                optimum = size
                maxima = []
            if size == optimum:
                maxima.append(tuple(chosen))
            return
        A = available[0]
        visit(chosen, available[1:])
        visit(chosen+[A], [B for B in available[1:] if A & B])
    visit([], vertices)
    expected = {tuple(A for A in vertices if A >> i & 1) for i in range(n)}
    require(set(maxima) == expected, 'complete small census has precisely the stars')
    return {'n': n, 'r': r, 'all_intersecting_families': count,
            'maximum_size': optimum, 'maximum_families': len(maxima)}


def controls():
    rejected = []
    for name, matrix in [('negative', [[-1]]), ('indefinite', [[1, 2], [2, 1]]),
                         ('zero_diagonal_image', [[0, 1], [1, 0]]),
                         ('asymmetric', [[1, 1], [0, 1]]), ('nonsquare', [[1, 0]])]:
        try:
            psd_rank(matrix)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('bad PSD input accepted: '+name)
    N, s, eps, gamma, beta, _ = weights(6, 3)
    bad = [row[:] for row in beta]
    bad[0][0] += eps
    try:
        check_star_equations(bad, gamma, s)
    except ValueError:
        rejected.append('corrupted_diagonal_star_constraint')
    else:
        raise ValueError('corrupted table accepted')
    # Zero coupling leaves the independently counted excess kernel.
    _, _, _, _, baseline, delta = weights(6, 3, Q(0))
    require(psd_rank(blocks(6, 3, s, baseline, 1)[3]) == 0,
            'zero coupling does not repair degree one')
    rejected.append('zero_coupling_maximal_rank')
    negative = [[baseline[a][b]-eps*delta[a][b] for b in range(3)] for a in range(3)]
    try:
        psd_rank(blocks(6, 3, s, negative, 1)[3])
    except ValueError:
        rejected.append('negative_coupling_PSD')
    else:
        raise ValueError('negative coupling accepted')
    for args in [(5, 3), (4, 1)]:
        try:
            weights(*args)
        except ValueError:
            rejected.append('invalid_parameters_'+str(args))
        else:
            raise ValueError('invalid parameters accepted')
    checked = positives = 0
    for a, b, c, d, e, f in itertools.product((-1, 0, 1), repeat=6):
        A = [[a, b, c], [b, d, e], [c, e, f]]
        principal = (min(a, d, f) >= 0 and min(a*d-b*b, a*f-c*c, d*f-e*e) >= 0
                     and a*d*f+2*b*c*e-a*e*e-d*c*c-f*b*b >= 0)
        try:
            psd_rank(A)
            answer = True
        except ValueError:
            answer = False
        require(answer == principal, 'all ternary PSD controls versus principal minors')
        positives += answer
        checked += 1
    return {'rejected': rejected, 'ternary_symmetric_3_by_3': checked,
            'ternary_positive_semidefinite': positives}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    compressed = [compressed_case(n, r) for r in range(2, 11) for n in (2*r, 2*r+1, 3*r)]
    literal = [literal_case(n, r) for n, r in [(4, 2), (5, 2), (6, 3), (7, 3), (8, 4)]]
    result = {'agent': 'six-downset-3', 'role': 'researcher', 'arithmetic': 'Q and integers',
              'scope': 'finite exact validation; the unbounded proof is PROOF.md; ordinary H only',
              'compressed': compressed, 'literal': literal,
              'complete_small_censuses': [small_census(4, 2), small_census(5, 2)],
              'controls': controls()}
    encoded = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.check:
        require(json.loads(args.check.read_text()) == result, 'expected results mismatch')
    if args.output:
        args.output.write_text(encoded)
    print(json.dumps({'ok': True, 'agent': 'six-downset-3', 'role': 'researcher',
                      'compressed_cases': len(compressed), 'literal_cases': len(literal),
                      'complete_lifted_basis_sizes': [x['complete_lifted_basis_size'] for x in literal],
                      'literal_lower_ranks': [x['N']-x['n'] for x in literal],
                      'negative_controls': len(result['controls']['rejected']),
                      'upper_cap': 'exactly fails',
                      'results_sha256': hashlib.sha256(encoded.encode()).hexdigest()}))


if __name__ == '__main__':
    main()
