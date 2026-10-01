#!/usr/bin/env python3
"""Independent exact audit by six-reviewer-1, independent mathematical reviewer.

Python 3.10+ standard library only. No target verifier is imported or translated.
Determinants use the defining permutation sum; inverses use cofactor adjugates.
The real PSD necessity and spectral minimization bridges are proved in REVIEW.md.
"""
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations
import json
from math import comb, lcm, prod
from pathlib import Path
import re


def check(ok, message):
    if not ok:
        raise ValueError(message)


def square(a):
    check(type(a) is list and len(a) > 0 and
          all(type(row) is list and len(row) == len(a) for row in a),
          'nonempty square matrix required')


def transpose(a):
    return [list(col) for col in zip(*a)]


def matmul(a, b):
    cols = transpose(b)
    return [[sum(x*y for x, y in zip(row, col)) for col in cols] for row in a]


def determinant(a):
    """Literal signed sum of n! products, including det(empty)=1."""
    n = len(a)
    check(all(len(row) == n for row in a), 'determinant dimensions')
    result = 0
    for p in permutations(range(n)):
        parity = sum(p[i] > p[j] for i in range(n) for j in range(i+1, n)) % 2
        result += (-1 if parity else 1)*prod(a[i][p[i]] for i in range(n))
    return result


def adjugate(a):
    square(a)
    n = len(a)
    answer = [[(-1)**(i+j)*determinant(
        [[a[r][c] for c in range(n) if c != i] for r in range(n) if r != j])
        for j in range(n)] for i in range(n)]
    det = determinant(a)
    expected = [[det*int(i == j) for j in range(n)] for i in range(n)]
    check(matmul(a, answer) == expected, 'left adjugate identity')
    check(matmul(answer, a) == expected, 'right adjugate identity')
    return det, answer


def minors(a):
    return [determinant([row[:k] for row in a[:k]]) for k in range(1, len(a)+1)]


def trace_product(a, b):
    return sum(a[i][j]*b[j][i] for i in range(len(a)) for j in range(len(a)))


def rational(s):
    check(type(s) is str and re.fullmatch(r'-?\d+(?:/[1-9]\d*)?', s),
          'exact rational string required')
    return Q(s)


def decode(c):
    check(c['n'] == 9 and type(c['n']) is int and c['layers'] == list(range(2, 8))
          and all(type(x) is int for x in c['layers']),
          'fixed order and layer order required')
    H, P = c['H'], c['P']
    check(type(H) is list and len(H) == 6 and all(type(x) is int for x in H),
          'six exact vector integers required')
    square(P)
    check(len(P) == 6 and all(type(x) is int for row in P for x in row),
          'six by six exact integer matrix required')
    check(P == transpose(P), 'symmetric upper dual required')
    check(type(c['h_scale']) is int and c['h_scale'] == 5000 and
          type(c['Y_scale']) is int and c['Y_scale'] == c['h_scale']**2,
          'dual scales required')
    check(c['uniform_surplus'] == 17 and type(c['uniform_surplus']) is int and
          c['relaxation_upper_bracket'] == 18 and
          type(c['relaxation_upper_bracket']) is int, 'fixed bracket required')
    beta = rational(c['beta'])
    check(beta == Q(6693928918269, 25371875000), 'fixed original bound required')
    h = [Q(x, c['h_scale']) for x in H]
    Y = [[Q(x, c['Y_scale']) for x in row] for row in P]
    return H, P, h, Y, beta


def algebra(c):
    H, P, h, Y, beta = decode(c)
    mp = minors(P)
    check(all(x > 0 for x in mp), 'Y must be positive definite')
    b = [comb(9, k) for k in range(2, 8)]
    G9 = [[9*b[i]*int(i == j)+(i+2)*b[i]*(j+2)*b[j]
           +9*(i+1)*b[i]*(j+1)*b[j] for j in range(6)] for i in range(6)]
    dg, ag = adjugate(G9)
    check(dg > 0 and all(x > 0 for x in minors(G9)), 'positive layer Gram')
    K = [[Q(4518*b[i]*ag[i][j]*b[j], dg) for j in range(6)] for i in range(6)]
    Ki = [[Q(G9[i][j], 4518*b[i]*b[j]) for j in range(6)] for i in range(6)]
    check(matmul(K, Ki) == [[Q(i == j) for j in range(6)] for i in range(6)],
          'K inverse residual')
    Gamma = [[h[i]*h[j]-Y[i][j] for j in range(6)] for i in range(6)]
    check(Gamma[0][0] == 0 and all(Gamma[i][5-i] == 0 for i in range(6)),
          'individual excluded-layer cancellation')
    C0 = [[247*b[i]*int(i == j)-b[i]*b[j] for j in range(6)] for i in range(6)]
    constant = trace_product(Y, K)+trace_product(Gamma, C0)
    check(constant == -beta, 'original affine constant identity')
    u = sum(h[i]*K[i][j]*h[j] for i in range(6) for j in range(6))
    dp, ap = adjugate(P)
    q = Q(sum(H[i]*ap[i][j]*H[j] for i in range(6) for j in range(6)), dp)
    check(q > 1, 'exactly one positive direction required')
    shift17 = [[Y[i][j]+(u-17)*Ki[i][j]-h[i]*h[j] for j in range(6)]
               for i in range(6)]
    shift18 = [[Y[i][j]+(u-18)*Ki[i][j]-h[i]*h[j] for j in range(6)]
               for i in range(6)]
    grid = lcm(*(x.denominator for row in shift17 for x in row),
               *(x.denominator for row in shift18 for x in row))
    check(type(c['Z17_grid']) is int and c['Z17_grid'] == grid,
          'exact common certificate grid required')
    z17 = [[int(grid*x) for x in row] for row in shift17]
    z18 = [[int(grid*x) for x in row] for row in shift18]
    square(c['Z17_integer_matrix'])
    check(len(c['Z17_integer_matrix']) == 6 and
          all(type(x) is int for row in c['Z17_integer_matrix'] for x in row) and
          all(type(x) is int for x in c['Z17_leading_minors']) and
          all(type(x) is int for x in c['Z18_leading_minors_on_same_grid']),
          'exact integer shift certificate required')
    check(all(Q(z17[i][j], grid) == shift17[i][j] and
              Q(z18[i][j], grid) == shift18[i][j] for i in range(6) for j in range(6)),
          'no truncation in certificate grid')
    check(c['Z17_integer_matrix'] == z17, 'shift certificate reconstruction')
    m17, m18 = minors(z17), minors(z18)
    check(c['Z17_leading_minors'] == m17 and
          c['Z18_leading_minors_on_same_grid'] == m18, 'shift minors reconstruction')
    check(all(x > 0 for x in m17), 'Z17 must be positive definite')
    check(all(x > 0 for x in m18[:5]) and m18[5] < 0, 'strict upper bracket')
    return b, G9, K, h, Y, Gamma, beta, {
        'Y_leading_minors': mp, 'G9_determinant': dg,
        'u_hKh': str(u), 'h_Y_inverse_h': str(q),
        'constant': str(constant), 'uniform_surplus_proved_strict': 17,
        'relaxed_optimal_surplus_open_interval': [17, 18],
        'weighted_ordered_sum_proved_strict_bound': str(beta+17),
        'Z_common_grid': grid, 'Z17_leading_minors': m17,
        'Z18_leading_minors': m18,
        'adjugate_residual_checks': 4, 'K_inverse_residual_entries': 36}


def literal_checks(b, G9, K, h, Y, Gamma, beta):
    sets = [a for a in range(512) if 2 <= a.bit_count() <= 7]
    groups = [[j for j, a in enumerate(sets) if a.bit_count() == k] for k in range(2, 8)]
    check(list(map(len, groups)) == b and len(sets) == 492, 'complete middle layers')
    members = [0]+[1 << i for i in range(9)]+sets
    stars = [[j for j, a in enumerate(members) if a & (1 << p)] for p in range(9)]
    check(len(members) == 502 and all(len(v) == 247 for v in stars), 'complete family stars')
    # Literal columns of S; no formula for the compressed Gram is used here.
    columns = [[a.bit_count()-1]+[-int(a & (1 << p) != 0) for p in range(9)]
               +[int(i == j) for i in range(len(sets))] for j, a in enumerate(sets)]
    check(all(sum(col) == 0 for col in columns), 'S columns centered')
    check(all(sum(col[i] for i in star) == 0 for col in columns for star in stars),
          'all star annihilations')
    sf = [[sum(columns[j][i] for j in group) for i in range(502)] for group in groups]
    gram = [[sum(x*y for x, y in zip(v, w)) for w in sf] for v in sf]
    check([[9*x for x in row] for row in gram] == G9, 'literal compressed Gram')
    # G=I+R^T R+t t^T on all middle vertices, not just the layer aggregates.
    for i, a in enumerate(sets):
        for k, group in enumerate(groups):
            literal = sum(int(i == j)+(a & sets[j]).bit_count()
                          +(a.bit_count()-1)*(sets[j].bit_count()-1) for j in group)
            check(literal*b[a.bit_count()-2] == gram[a.bit_count()-2][k],
                  'GF invariant layer identity')
    # Independently chosen, nonconstant signed entries for every disjoint edge.
    core = [[247*int(i == j)-1 for j in range(492)] for i in range(492)]
    counts, zero_counts = Counter(), Counter()
    weighted_numerator = 0
    A = [[0]*6 for _ in range(6)]
    weights = [[int(25000000*x) for x in row] for row in Gamma]
    for i, a in enumerate(sets):
        for j in range(i+1, 492):
            other = sets[j]
            if a & other:
                continue
            k, ell = sorted((a.bit_count(), other.bit_count()))
            counts[k, ell] += 1
            coefficient = Gamma[k-2][ell-2]
            excluded = (other == (511 ^ a) or k == ell == 2)
            check((coefficient == 0) == excluded, 'individual edge cancellation equivalence')
            if excluded:
                zero_counts[k, ell] += 1
            value = (37*a+101*other+13*a*other) % 23-11
            core[i][j] = core[j][i] = value-1
            weighted_numerator += 2*weights[k-2][ell-2]*value
    for i, a in enumerate(sets):
        for j, other in enumerate(sets):
            A[a.bit_count()-2][other.bit_count()-2] += core[i][j]
    mass = Q(weighted_numerator, 25000000)
    B = [[K[i][j]-A[i][j] for j in range(6)] for i in range(6)]
    functional = sum(h[i]*A[i][j]*h[j] for i in range(6) for j in range(6))+trace_product(Y, B)
    check(functional+beta == mass, 'full ordered signed trace identity')
    for (k, ell), number in counts.items():
        closed_count = comb(9, k)*comb(9-k, ell)//(2 if k == ell else 1)
        check(number == closed_count, 'edge completeness binomial count')
    check(sum(counts.values()) == 7071 and sum(zero_counts.values()) == 624,
          'exact edge census')
    # Construct J+SQS^T directly, including the t row, not via prescribed row sums.
    rq = [[sum(core[i][j] for i, a in enumerate(sets) if a & (1 << p))
           for j in range(492)] for p in range(9)]
    tq = [sum((a.bit_count()-1)*core[i][j] for i, a in enumerate(sets)) for j in range(492)]
    L = [[1]*502 for _ in range(502)]
    L[0][0] += sum(tq[j]*(a.bit_count()-1) for j, a in enumerate(sets))
    for p in range(9):
        L[0][p+1] = L[p+1][0] = 1-sum(tq[j] for j, a in enumerate(sets) if a & (1 << p))
        for r in range(9):
            L[p+1][r+1] += sum(rq[p][j] for j, a in enumerate(sets) if a & (1 << r))
    for j in range(492):
        L[0][j+10] = L[j+10][0] = 1+tq[j]
        for p in range(9):
            L[p+1][j+10] = L[j+10][p+1] = 1-rq[p][j]
        for i in range(492):
            L[i+10][j+10] = 1+core[i][j]
    for i, a in enumerate(members):
        check(sum(L[i]) == 502, 'literal full row normalization')
        check(a == 0 or L[i][i] == 247, 'literal nonempty diagonal')
        for j, other in enumerate(members):
            check(L[i][j] == L[j][i], 'literal full symmetry')
            check(i == j or a & other == 0 or L[i][j] == 0, 'literal intersecting off-diagonal')
        for star in stars:
            check(sum(L[i][j] for j in star) == 247, 'literal full forced star identity')
    # This is deliberately an affine control; it cannot be a capped PSD witness.
    check(functional < 0, 'synthetic matrix must not certify the PSD pair')
    coefficients = [{'sizes': [k, ell], 'coefficient': str(Gamma[k-2][ell-2]),
                     'unordered_pairs': number}
                    for (k, ell), number in sorted(counts.items()) if (k, ell) not in zero_counts]
    return {'middle_vertices':492, 'full_vertices':502, 'all_star_sizes':247,
            'literal_Gram_entries':36, 'GF_entries':492*6,
            'centered_S_columns':492, 'S_star_annihilations':492*9,
            'unordered_disjoint_middle_pairs':sum(counts.values()),
            'individually_zero_weight_pairs':sum(zero_counts.values()),
            'nonzero_coefficients_and_pair_counts':coefficients,
            'synthetic_affine_entries_checked':502*502,
            'synthetic_signed_ordered_sum':str(mass),
            'synthetic_dual_functional':str(functional),
            'synthetic_is_capped_PSD_witness':False}


def negative_controls(c):
    mutations = [
        ('wrong_order', lambda x: x.update(n=8)),
        ('wrong_layer_order', lambda x: x.update(layers=[3,2,4,5,6,7])),
        ('float_vector_entry', lambda x: x['H'].__setitem__(0, 5000.0)),
        ('wrong_scale', lambda x: x.update(Y_scale=2500)),
        ('asymmetric_upper_dual', lambda x: x['P'][0].__setitem__(5, 136090001)),
        ('indefinite_upper_dual', lambda x: x['P'][0].__setitem__(0, -1)),
        ('wrong_bound', lambda x: x.update(beta='1')),
        ('wrong_grid', lambda x: x.update(Z17_grid=x['Z17_grid']+1)),
        ('wrong_shift_entry', lambda x: x['Z17_integer_matrix'][0].__setitem__(0, 0)),
        ('wrong_shift_minor', lambda x: x['Z17_leading_minors'].__setitem__(5, 0)),
        ('wrong_upper_bracket_minor', lambda x: x['Z18_leading_minors_on_same_grid'].__setitem__(5, 1)),
        ('unsupported_surplus_18', lambda x: x.update(uniform_surplus=18))]
    rejected = []
    for name, mutate in mutations:
        corrupt = deepcopy(c)
        mutate(corrupt)
        try:
            algebra(corrupt)
        except (ValueError, ZeroDivisionError):
            rejected.append(name)
        else:
            raise ValueError('corrupt certificate accepted: '+name)
    controls = [([], 1), ([[0]], 0), ([[0,1],[1,0]], -1),
                ([[1,2],[2,4]], 0), ([[1,0,0],[0,2,0],[0,0,3]], 6),
                ([[1,2,3],[0,1,4],[5,6,0]], 1)]
    check(all(determinant(a) == expected for a, expected in controls), 'determinant controls')
    return rejected, len(controls)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--certificate', type=Path, default=Path(__file__).with_name('CERTIFICATE.json'))
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    raw = args.certificate.read_bytes()
    c = json.loads(raw)
    b, G9, K, h, Y, Gamma, beta, exact = algebra(c)
    literal = literal_checks(b, G9, K, h, Y, Gamma, beta)
    rejected, det_controls = negative_controls(c)
    result = {'agent':'six-reviewer-1', 'role':'independent mathematical reviewer',
              'target_ref':c['target_ref'], 'proof_status':'Scoped independent exact audit; unformalized written PSD and spectral bridges.',
              'arithmetic':'exact integers and fractions; permutation determinants and cofactor adjugates',
              'exact':exact, 'literal':literal, 'negative_controls':rejected,
              'determinant_controls':det_controls, 'certificate_sha256':sha256(raw).hexdigest()}
    text = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
