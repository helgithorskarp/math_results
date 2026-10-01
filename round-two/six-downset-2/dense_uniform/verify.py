"""Independent exact checks of the dense formula and its original-index lift.

This corroborates the ordinary infinite proof; it is not an enumeration
proof for untested n,r. No solver, float tolerance, imported certificate,
third-party package or assertion is used. Python 3.11+ stdlib only.
"""
import argparse
from dataclasses import replace
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path

from exact import psd_rank
from matrices import (coefficient, falling, harmonic_moment, literal_matrix,
                      parameters, require, sectors, slack_entry, trade)
from math import comb


def schur_rank(A):
    """Independent rational Schur complements; no denominator clearing."""
    d = len(A)
    require(all(len(row) == d for row in A), "Schur shape")
    require(all(type(x) in (int, Q) for row in A for x in row), "Schur exact input")
    require(all(A[i][k] == A[k][i] for i in range(d) for k in range(d)), "Schur symmetry")
    Z = [[Q(x) for x in row] for row in A]
    rank = 0
    while Z:
        require(all(Z[i][i] >= 0 for i in range(len(Z))), "Negative Schur pivot")
        p = next((i for i in range(len(Z)) if Z[i][i]), None)
        if p is None:
            require(all(x == 0 for row in Z for x in row), "Zero diagonal off-diagonal obstruction")
            break
        others = [i for i in range(len(Z)) if i != p]
        Z = [[Z[i][k]-Z[i][p]*Z[p][k]/Z[p][p] for k in others] for i in others]
        rank += 1
    return rank


def both(A, rank=None):
    a, b = psd_rank(A), schur_rank(A)
    require(a == b and (rank is None or a == rank), "Two PSD/rank algorithms agree")
    return a


def gram(g, K, shift=Q(0)):
    return [[g[i]*(v-shift*int(i == k)) for k, v in enumerate(row)]
            for i, row in enumerate(K)]


def multiply(A, B):
    return [[sum((x*y for x, y in zip(row, col)), Q(0)) for col in zip(*B)]
            for row in A]


def quadratic(A, x):
    return sum((x[i]*A[i][k]*x[k] for i in range(len(A)) for k in range(len(A))), Q(0))


def validate_affine(P):
    require(P.N == sum(comb(P.n, a) for a in range(P.r+1)), "N count")
    require(P.s == sum(comb(P.n-1, a) for a in range(P.r)), "Star count")
    require(len(P.beta) == P.r+1 and all(len(row) == P.r+1 for row in P.beta), "Beta shape")
    require(all(type(v) is Q for row in P.beta for v in row), "Rational weights")
    require(all(P.beta[a][b] == P.beta[b][a] for a in range(P.r+1)
                for b in range(P.r+1)), "Beta symmetry")
    for a in range(1, P.r+1):
        require(sum(P.beta[a][b]*comb(P.n-a, b) for b in range(1, P.r+1)) == P.N-1-P.s,
                "Centered disjoint row")
        require(sum(b*P.beta[a][b]*comb(P.n-a, b) for b in range(1, P.r+1)) == (P.n-a)*P.s,
                "Weighted star row")
    require(P.moment[0][1] == P.n*P.s, "First moment ns")


def sector_checks(n, r):
    seed = parameters(n, r, Q(0))
    validate_affine(seed)
    F, M = coefficient(seed), harmonic_moment(seed, 0)
    FM = multiply(F, M)
    detM = M[0][0]*M[1][1]-M[0][1]**2
    detF = F[0][0]*F[1][1]-F[0][1]**2
    require(detF == -Q(seed.s*(seed.N-1-seed.s), detM) < 0, "Indefinite rank-two coefficient")
    require(FM[0][0]+FM[1][1] == seed.N-1-2*seed.s, "Global spectral trace")
    require(FM[0][0]*FM[1][1]-FM[0][1]*FM[1][0] == -seed.s*(seed.N-1-seed.s),
            "Global spectral determinant")
    seed_blocks = sectors(seed)
    moment_ranks = []
    for j, aa, g, K, U in seed_blocks:
        d = len(aa)
        require(all(x > 0 for x in g), "Positive harmonic metric")
        require(both(gram(g, K)) == d-(2 if j == 0 else 1 if j == 1 else 0), "Seed kernel")
        both(gram(g, [[2*seed.s*int(i == k)-K[i][k] for k in range(d)] for i in range(d)]))
        both(gram(g, U), d)
        if j == 0:
            for i, a in enumerate(aa):
                for k, b in enumerate(aa):
                    expected = seed.s*int(i == k)-seed.s*comb(n, b)*(
                        seed.inverse[0][0]+(a+b)*seed.inverse[0][1]+a*b*seed.inverse[1][1])
                    require(K[i][k] == expected, "Exact degree-zero projection")
        else:
            W = [[(-1)**j*(K[i][k]-seed.s*int(i == k)) for k in range(d)] for i in range(d)]
            R = [[Q(1, falling(n-a, j)), Q(a, falling(n-a, j))] for a in aa]
            T = [[comb(n, b)*falling(b, j), b*comb(n, b)*falling(b, j)] for b in aa]
            reconstructed = multiply(multiply(R, F), list(map(list, zip(*T))))
            require(W == reconstructed, "Rank-two harmonic factorization")
            for a, weight in zip(aa, g):
                require(Q(weight, falling(n-a, j)) == Q(comb(n, a)*falling(a, j), falling(n, 2*j)),
                        "Harmonic metric identity")
            if j == 1:
                require(all(sum(row) == seed.s for row in W), "Sole positive degree-one eigenvalue")
                total = sum(g)
                gap = [[g[i]*(K[i][k]-seed.s*int(i == k))+Q(seed.s*g[i]*g[k], total)
                        for k in range(d)] for i in range(d)]
                both(gap)
        Mj = harmonic_moment(seed, j)
        both(Mj)
        if j:
            M1 = harmonic_moment(seed, 1)
            diff = [[M1[i][k]-Mj[i][k] for k in range(2)] for i in range(2)]
            rd = both(diff)
            require(rd == (0 if j == 1 else 1 if (n, r) == (4, 2) else 2), "Strict moment descent")
            moment_ranks.append(rd)
        core_margin = seed.N-2*seed.s-1
        margin_form = gram(g, U, Q(1+core_margin))
        if j == 0:
            for i in range(d):
                for k in range(d):
                    margin_form[i][k] += Q(core_margin*g[i]*g[k], seed.N-1)
        both(margin_form)
    repaired = []
    for t in (1/(2*seed.alpha), 1/seed.alpha):
        P = parameters(n, r, t)
        lower, upper = 0, 0
        for j, aa, g, K, U in sectors(P):
            d = len(aa)
            expected = d-(1 if j in (0, 1) else 0)
            both(gram(g, K), expected)
            both(gram(g, U), d)
            both(gram(g, U, P.gap))
            lower += expected*(comb(n, j)-(comb(n, j-1) if j else 0))
            upper += d*(comb(n, j)-(comb(n, j-1) if j else 0))
            D = [[(-1)**j*trade(n, a, b)*comb(n-a-j, b-j) for b in aa] for a in aa]
            ev = P.alpha if j == 0 else -P.negative_trade if j == 1 else Q(1) if j == 2 else Q(0)
            require(multiply(D, D) == [[ev*x for x in row] for row in D], "Trade spectral identity")
            if j <= 2:
                both(gram(g, D if j != 1 else [[-x for x in row] for row in D]), 1)
            else:
                require(all(x == 0 for row in D for x in row), "Trade absent in higher degrees")
        require(lower == P.N-1-n and upper == P.N-1, "Weighted complete sector ranks")
        require(P.gap >= Q(4, 7) and P.alpha >= 7, "Uniform certified upper margin")
        require(P.N-2*P.s == comb(n-1, r) >= 3, "Combinatorial cap slack")
        cosine2 = Q(n*(n-1), 2*(P.N-1)*(2*n-1))
        require(cosine2 <= Q(1, 9), "Repair/constant angle bound")
        repaired.append({'t': str(t), 'lower_core_rank': lower, 'upper_core_rank': upper})
    return {'n': n, 'r': r, 'N': seed.N, 's': seed.s, 'harmonic_sectors': r+1,
            'strict_moment_difference_ranks': moment_ranks, 'gap': str(seed.gap),
            'repairs': repaired}


def validate_literal(P, V, L):
    N = len(V)
    require(N == P.N and V[0] == 0, "Original empty vertex")
    require(all(len(row) == N for row in L), "Literal shape")
    require(all(L[i][k] == L[k][i] for i in range(N) for k in range(N)), "Literal symmetry")
    require(all(sum(row) == N for row in L), "Full row normalization")
    for i, A in enumerate(V):
        for k, B in enumerate(V):
            require(not (A & B) or L[i][k] == P.s*int(i == k), "Intersecting support")
    require(L[0][0] == 1+P.t*P.delta, "Empty loop")
    stars = [[Q(int(bool(A & (1 << p))))-Q(P.s, N) for A in V] for p in range(P.n)]
    require(all(all(sum(L[i][k]*v[k] for k in range(N)) == 0 for i in range(N)) for v in stars),
            "All original centered stars in lower kernel")
    both(L, N-P.n)
    upper = [[N*int(i == k)-L[i][k] for k in range(N)] for i in range(N)]
    both(upper, N-1)
    margin = [[upper[i][k]-P.gap*(int(i == k)-Q(1, N)) for k in range(N)] for i in range(N)]
    both(margin, N-1)


def literal_checks(n, r):
    P = parameters(n, r)
    V, L = literal_matrix(P)
    validate_literal(P, V, L)
    F = V[1:]
    C = [[L[i+1][k+1]-1 for k in range(len(F))] for i in range(len(F))]
    column_count = 0
    for j, aa, g, K, U in sectors(P):
        pol = []
        for A in F:
            v = 1
            for p in range(j):
                v *= int(bool(A & (1 << (2*p))))-int(bool(A & (1 << (2*p+1))))
            pol.append(v)
        for col, b in enumerate(aa):
            x = [Q(v if A.bit_count() == b else 0) for A, v in zip(F, pol)]
            require(sum(v*v for v in x) == 2**j*comb(n-2*j, b-j), "Literal matching harmonic norm")
            actual = [sum(C[i][k]*x[k] for k in range(len(F))) for i in range(len(F))]
            expected = [Q(v)*K[aa.index(A.bit_count())][col] if A.bit_count() in aa else Q(0)
                        for A, v in zip(F, pol)]
            require(actual == expected, "Every original coordinate of harmonic action")
            column_count += 1
    return {'n': n, 'r': r, 'N': P.N, 'lower_rank': P.N-n, 'upper_rank': P.N-1,
            'harmonic_action_columns': column_count, 'endpoint': str(P.t)}


def product_checks(cases):
    factors = [parameters(n, r) for n, r in cases]
    data = [literal_matrix(P) for P in factors]
    vertices = list(product(*(range(P.N) for P in factors)))
    N = len(vertices)
    require(N <= 192, "Literal product guard")
    density = max(Q(P.s, P.N) for P in factors)
    eligible = [k for k, P in enumerate(factors) if Q(P.s, P.N) == density]
    nullity = sum(factors[k].n for k in eligible)
    star_size = density*N
    require(star_size.denominator == 1, "Product star cardinality")
    MH = []
    for A in vertices:
        row = []
        for B in vertices:
            v = Q(1)
            for k, P in enumerate(factors):
                v *= (data[k][1][A[k]][B[k]]-P.s*int(A[k] == B[k]))/(P.N-P.s)
            row.append(v)
        MH.append(row)
    require(all(sum(row) == 1 for row in MH), "Product row normalization")
    for i, A in enumerate(vertices):
        for b, B in enumerate(vertices):
            intersects = any(data[k][0][A[k]] & data[k][0][B[k]] for k in range(len(factors)))
            require(not intersects or MH[i][b] == 0, "Product original support")
    L = [[(N-star_size)*MH[i][b]+star_size*int(i == b) for b in range(N)] for i in range(N)]
    both(L, N-nullity)
    both([[N*int(i == b)-L[i][b] for b in range(N)] for i in range(N)], N-1)
    return {'factors': [list(v) for v in cases], 'N': N, 's': int(star_size),
            'eligible_factors': eligible, 'lower_rank': N-nullity, 'upper_rank': N-1}


def controls():
    rejected = []
    def reject(name, fn):
        try:
            fn()
        except (ValueError, TypeError, IndexError):
            rejected.append(name)
            return
        raise ValueError('Control accepted: '+name)
    for name, args in [('r_one', (4, 1)), ('below_stable', (5, 3)),
                       ('bool_n', (True, 2)), ('float_r', (8, 3.0)),
                       ('negative_t', (4, 2, Q(-1, 7))), ('float_t', (4, 2, 0.1)),
                       ('above_sufficient_interval', (4, 2, Q(1, 6)))]:
        reject(name, lambda args=args: parameters(*args))
    P = parameters(4, 2)
    for name, A in [('negative_vertex', -1), ('vertex_outside_ground', 16),
                     ('vertex_above_layer', 7), ('bool_vertex', True)]:
        reject(name, lambda A=A: slack_entry(P, A, 0))
    for name, matrix in [('negative_diagonal', [[Q(-1)]]),
                          ('zero_diagonal_nonzero_row', [[Q(0), Q(1)], [Q(1), Q(0)]]),
                          ('negative_schur', [[Q(1), Q(2)], [Q(2), Q(1)]]),
                          ('asymmetric', [[Q(1), Q(0)], [Q(1), Q(1)]]),
                          ('floating_matrix', [[1.0]]), ('nonsquare', [[Q(1), Q(0)]])]:
        reject('Bareiss_'+name, lambda matrix=matrix: psd_rank(matrix))
        reject('Schur_'+name, lambda matrix=matrix: schur_rank(matrix))
    beta = [list(row) for row in P.beta]
    beta[1][1] += Q(1)
    reject('wrong_seed_moment', lambda: validate_affine(replace(P, beta=tuple(tuple(row) for row in beta))))
    V, L = literal_matrix(P)
    bad = [row[:] for row in L]
    bad[0][0] += 1
    reject('wrong_empty_loop_and_row', lambda: validate_literal(P, V, bad))
    bad2 = [row[:] for row in L]
    bad2[1][1] += 1
    reject('nonzero_hoffman_diagonal', lambda: validate_literal(P, V, bad2))
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    certificate = json.loads(Path(__file__).with_name('certificate.json').read_text())
    require(certificate['schema'] == 'dense-two-moment-v1', "Certificate schema")
    cases = [(2*r+d, r) for r in range(2, 11) for d in (0, 1)]
    cases += [(24, 12), (32, 16), (40, 20), (48, 24), (32, 8), (80, 10)]
    require(certificate['sector_cases'] == [list(v) for v in cases], "Exact finite coverage manifest")
    require(certificate['literal_cases'] == [[4, 2], [5, 2], [6, 3]], "Literal coverage manifest")
    require(certificate['product_cases'] == [[[4, 2], [4, 2]], [[4, 2], [5, 2]]], "Product manifest")
    result = {'schema': 'dense-two-moment-check-v1', 'agent': 'six-downset-2', 'role': 'researcher',
              'arithmetic': 'Python integers/Fraction; Bareiss plus independent rational Schur',
              'sector_cases': [sector_checks(*v) for v in cases],
              'literal_cases': [literal_checks(*v) for v in certificate['literal_cases']],
              'product_cases': [product_checks(v) for v in certificate['product_cases']],
              'rejected_controls': controls(), 'passed': True,
              'infinite_scope_trust_boundary': 'Unformalized ordinary proof in PROOF.md, not finite extrapolation'}
    if args.check:
        require(result == json.loads(args.check.read_text()), "Expected result agreement")
    out = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(out)
    print(json.dumps({'passed': True, 'sector_cases': len(cases),
                      'harmonic_blocks_per_parameter': sum(r+1 for n, r in cases),
                      'literal_cases': len(result['literal_cases']),
                      'literal_product_orders': [v['N'] for v in result['product_cases']],
                      'rejected_controls': len(result['rejected_controls'])}))


if __name__ == '__main__':
    main()
