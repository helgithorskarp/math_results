"""Separate original-member/counting reader; imports no producer or polynomial engine.

Ten exact points prove each univariate degree<=9 identity. A complete
10-by-3 rectangle proves the independently counted bivariate scalar
identities, by the explicit degree bound (9 in q, 2 in k).
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from math import comb
import argparse
import hashlib
import importlib.util
import json
import sys

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
import sourcecheck
SOURCE = sourcecheck.check_bundle(BASE)
LITERAL_PIN = '46218af58a0654279231ade1bc40106d9eb390b6c0b2ceee5f3c4c5b7bedbf39'


def require(value, message):
    if not value:
        raise ValueError(message)


def literal_input():
    path = BASE/'credited-original/literal.py'
    require(hashlib.sha256(path.read_bytes()).hexdigest() == LITERAL_PIN,
            'entire immutable original table/member executable checked before import')
    spec = importlib.util.spec_from_file_location('original_literal', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def value(core, outside):
    # Independent semantic case table: entries are lower, cap, orientation.
    if core == 0:
        return F(0), F(2), F(1)
    if outside == 0:
        return ((F(1), F(1), F(0)) if core in (2, 4) else
                (F(1, 2), F(2), F(-1)) if core == 7 else (F(0), F(2), F(0)))
    return F({1: 2, 2: 3, 4: 3, 3: -1, 5: -1, 6: 0}[core], 4), F(2), F(0)


def quadratic(matrix, x):
    return sum(matrix[i][i]*x[i]*x[i] for i in range(len(x))) + 2*sum(
        matrix[i][j]*x[i]*x[j] for i in range(len(x)) for j in range(i+1, len(x)))


def choose(n, r):
    return comb(n, r) if 0 <= r <= n else 0


def parameters(q, k):
    require(type(q) is int and type(k) is int and q >= 4 and 0 <= k <= q,
            'original integer carrier range')
    return (q*q+13*q+16)//2-k, 3*q+4


def six_forms(keys, masses, pairs, q, k, literal):
    N, s = parameters(q, k)
    names = ('C0', 'Delta', 'Rb', 'Rc', 'B', 'U0')
    matrices = {name: [[F(0) for _ in keys] for _ in keys] for name in names}
    tab = literal.table(q)
    repairs = {'Rb': {(1, 2): 1, (2, 5): -1}, 'Rc': {(1, 4): 1, (3, 4): -1}, 'B': {(2, 4): 1}}
    for i, (core, outside) in enumerate(keys):
        for j, (other, out2) in enumerate(keys):
            disjoint = pairs(i, j)
            base, slope = tab[tuple(sorted(((core.bit_count(), outside), (other.bit_count(), out2))))] if disjoint else (0, 0)
            C = F(s*masses[i]*int(i == j)-masses[i]*masses[j]) + disjoint*base
            matrices['C0'][i][j] = C
            matrices['Delta'][i][j] = disjoint*slope
            matrices['U0'][i][j] = N*masses[i]*int(i == j)-masses[i]*masses[j]-C
            for name, edges in repairs.items():
                matrices[name][i][j] = F(edges.get(tuple(sorted((core, other))), 0)) if outside == out2 == 0 else F(0)
    require(all(A[i][j] == A[j][i] for A in matrices.values() for i in range(len(keys)) for j in range(len(keys))),
            'ALL separately counted original forms symmetric')
    return matrices


def two_pool(q, k, literal):
    keys = sorted((core, z, w) for core in range(8) for z in range(3) for w in range(3)
                  if (1 <= core.bit_count()+z+w <= 2 or core.bit_count()+z+w == 3 and core.bit_count() >= 2)
                  and (core, z, w) != (6, 1, 0) and choose(k, z)*choose(q-k, w))
    masses = [choose(k, z)*choose(q-k, w) for core, z, w in keys]
    def pairs(i, j):
        ci, zi, wi = keys[i]
        cj, zj, wj = keys[j]
        return 0 if ci & cj else masses[i]*choose(k-zi, zj)*choose(q-k-wi, wj)
    forms = six_forms([(core, z+w) for core, z, w in keys], masses, pairs, q, k, literal)
    return keys, masses, forms


def one_pool(q, k, literal):
    # Fifteen core/size classes. Only bcx has restricted outside choices.
    # These vector values ignore membership in Z; this is an energy count,
    # not a quotient or a claimed invariant subspace of the original matrix.
    keys = sorted((core, size) for core in range(8) for size in range(3)
                  if 1 <= core.bit_count()+size <= 2 or core.bit_count()+size == 3 and core.bit_count() >= 2)
    require(len(keys) == 15, 'entire independent core/size census')
    masses = [q-k if key == (6, 1) else choose(q, key[1]) for key in keys]
    def pairs(i, j):
        ci, ri = keys[i]
        cj, rj = keys[j]
        if ci & cj:
            return 0
        if keys[i] == (6, 1):
            return (q-k)*choose(q-1, rj)
        if keys[j] == (6, 1):
            return (q-k)*choose(q-1, ri)
        return choose(q, ri)*choose(q-ri, rj)
    require(sum(masses) == parameters(q, k)[0]-1, 'independent full physical mass')
    return keys, masses, six_forms(keys, masses, pairs, q, k, literal)


def scalar_identities(q, k, literal):
    keys, masses, forms = one_pool(q, k, literal)
    low, cap, zz = (list(xs) for xs in zip(*(value(*key) for key in keys)))
    lower = [quadratic(forms['C0'], low)] + [quadratic(forms[name], low) for name in ('Delta', 'Rb', 'Rc', 'B')]
    upper = [quadratic(forms['U0'], cap)] + [-quadratic(forms[name], cap) for name in ('Delta', 'Rb', 'Rc', 'B')]
    constant = F(3*q*q+33*q+28-12*k*q+4*k*k-14*k)
    slope = -F(2*q*(q+1))-F(4*(3*q+1-2*k), 3*q+5)
    require(lower == [F(3*q, 2)+F(9, 4), 0, 0, 0, 2], 'every independent original lower affine coefficient')
    require(upper == [constant, slope, 0, 0, -2], 'every independent original cap affine coefficient')
    alpha = F(q*(q+1), 2)+F(3*(q+1), 3*q+5)
    require([quadratic(forms[name], zz) for name in ('C0', 'Delta', 'Rb', 'Rc', 'B')] == [0, alpha, 0, 0, 0],
            'every independent original orientation coefficient')
    A = F(3*q*q-12*k*q+4*k*k-14*k)+F(69*q, 2)+F(121, 4)
    require(lower[0]+upper[0] == A, 'whole bivariate quadratic combined-energy identity')
    ones = [F(1) for _ in keys]
    require(quadratic(forms['C0'], ones) == 3*k*q-k*k+4*k, 'whole original constant-vector lower energy')
    b = keys.index((2, 0))
    require(sum(forms['C0'][b]) == k, 'whole original row at singleton b')
    return {'q': q, 'k': k, 'lower_plane': list(map(str, lower)), 'cap_plane': list(map(str, upper)),
            'orientation_delta': str(alpha), 'A': str(A), 'negative_kappa_coefficient': str(slope)}


def evaluate(poly, k):
    require(type(poly) is list and len(poly) <= 10 and all(type(x) is str for x in poly),
            'entire untrusted degree<=9 polynomial encoding')
    out = F(0)
    for text in reversed(poly):
        out = out*k+F(text)
    return out


def actual_members(q, k, literal, counted):
    N, s = parameters(q, k)
    members = [0] + sorted(sum(1 << x for x in points)
                          for size in (1, 2, 3) for points in combinations(range(q+3), size)
                          if literal.member(q, k, sum(1 << x for x in points)))
    require(len(members) == N and len(set(members)) == N, 'actual-empty whole member census')
    keys, masses, expected = counted
    ix = {key: i for i, key in enumerate(keys)}
    def orbit(A):
        return A & 7, ((A >> 3) & ((1 << k)-1)).bit_count(), (A >> (3+k)).bit_count()
    census = [0]*len(keys)
    for A in members[1:]:
        census[ix[orbit(A)]] += 1
    require(census == masses, 'EVERY original orbit mass from literal members')
    forms = {name: [[F(0) for _ in keys] for _ in keys] for name in expected}
    tab = literal.table(q)
    repairs = {'Rb': {(1, 2): 1, (2, 5): -1}, 'Rc': {(1, 4): 1, (3, 4): -1}, 'B': {(2, 4): 1}}
    for A in members[1:]:
        i = ix[orbit(A)]
        for B in members[1:]:
            j = ix[orbit(B)]
            if A == B:
                C, delta = F(s-1), F(0)
            elif A & B:
                C, delta = F(-1), F(0)
            else:
                C, delta = tab[tuple(sorted((literal.typ(A), literal.typ(B))))]
                C -= 1
            forms['C0'][i][j] += C
            forms['Delta'][i][j] += delta
            forms['U0'][i][j] += N*int(A == B)-1-C
            edge = tuple(sorted((A, B)))
            for name, values in repairs.items():
                forms[name][i][j] += values.get(edge, 0)
    require(forms == expected, 'ALL six entire forms equal independently aggregated actual-member pairs')
    return {'q': q, 'k': k, 'actual_empty_present': True, 'ordered_original_nonempty_pairs': (N-1)**2,
            'whole_six_forms_positions': 6*len(keys)**2}


def finite_certificate(data, original):
    expected = [(q, k) for k in range(8, 17) for q in range(k, 3*k)
                if 12*q*q-48*k*q+16*k*k+138*q-56*k+121 >= 0]
    require(len(expected) == 33, 'exact remaining original finite coverage')
    require(type(data['points']) is list and [(row['q'], row['k']) for row in data['points']] == expected,
            'EVERY required original point exactly once in canonical order')
    require(data['dyadic_denominator'] == 256, 'intended compact dyadic certificate domain')
    rows = []
    for row in data['points']:
        q, k = row['q'], row['k']
        keys, masses, forms = two_pool(q, k, original)
        require(data['coordinate_order'] == [list(x) for x in keys], 'ENTIRE finite original member coordinate order')
        low, cap = list(map(F, row['lower'])), list(map(F, row['cap']))
        require(len(low) == len(cap) == 23 and all((x*256).denominator == 1 for x in low+cap),
                'every original finite vector is a complete dyadic member vector')
        require(row['positive_weights'] == ['1', '1'], 'strictly positive original endpoint weights')
        lo = [quadratic(forms['C0'], low)] + [quadratic(forms[name], low) for name in ('Delta', 'Rb', 'Rc', 'B')]
        up = [quadratic(forms['U0'], cap)] + [-quadratic(forms[name], cap) for name in ('Delta', 'Rb', 'Rc', 'B')]
        total = [lo[i]+up[i] for i in range(5)]
        require(list(map(F, row['whole_original_affine_sum'])) == total, 'ALL five complete finite original affine coefficients')
        require(total[0] < 0 and total[1] < 0 and total[2:] == [0, 0, 0],
                'each entire REAL original repair face excluded without a rank premise')
        zz = [value(core, z+w)[2] for core, z, w in keys]
        alpha = F(q*(q+1), 2)+F(3*(q+1), 3*q+5)
        require([quadratic(forms[name], zz) for name in ('C0', 'Delta', 'Rb', 'Rc', 'B')] == [0, alpha, 0, 0, 0]
                and alpha > 0, 'whole actual lower cone forces kappa nonnegative at every finite point')
        rows.append({'q': q, 'k': k, 'whole_original_lower_plane': list(map(str, lo)),
                     'whole_original_cap_plane': list(map(str, up)), 'combined_plane': list(map(str, total)),
                     'orientation_delta': str(alpha), 'full_physical_metric_masses': masses})
    return rows


def checked(record, certificate):
    original = literal_input()
    require(record['domain'] == 'ALL integers k>=8, q=2k, EVERY deletion set Z of size k', 'precise univariate claim scope')
    require(record['A'] == ['121/4', '55', '-8'] and record['A_shift8'] == ['-167/4', '-73', '-8'], 'entire strict sign certificate')
    require(record['negative_kappa_numerator'] == ['4', '36', '64', '48'] and record['slope_and_orientation_denominator'] == ['5', '6'], 'entire strictly positive kappa coefficient certificate')
    require(record['orientation_numerator'] == ['3', '11', '16', '12'], 'entire positive orientation certificate')
    matrices = record['complete_cleared_original_forms']
    require(set(matrices) == {'C0', 'Delta', 'Rb', 'Rc', 'B', 'U0'}, 'six complete original coefficient forms')
    require(all(len(G) == 23 and all(len(row) == 23 for row in G) for G in matrices.values()), 'complete original matrix shapes')
    require(len(record['masses']) == 23 and set(record['physical_vectors']) == {'lower', 'cap', 'orientation'}, 'all original masses and vectors')
    require(all(len(record['physical_vectors'][name]) == 23 for name in record['physical_vectors']), 'all original vector coordinates')
    require(len(record['complete_cleared_affine_planes']) == 2 and all(len(row) == 5 for row in record['complete_cleared_affine_planes'])
            and len(record['complete_cleared_combined_plane']) == 5, 'every affine coefficient supplied')
    grid = []
    for k in range(8, 18):
        q = 2*k
        keys, masses, forms = two_pool(q, k, original)
        require(record['keys'] == [list(x) for x in keys], 'ENTIRE original key order')
        require([evaluate(poly, k) for poly in record['masses']] == masses, 'EVERY whole mass coefficient identity')
        P = 4*q*(q-1)*(q-2)*(q-3)*(3*q+5)
        require(evaluate(record['clearing'], k) == P > 0, 'exact original positive denominator')
        for name, G in matrices.items():
            require(all(evaluate(G[i][j], k) == P*forms[name][i][j] for i in range(23) for j in range(23)),
                    'ALL original coefficients by complete exact determinant-free grid')
        low, cap, zz = (list(xs) for xs in zip(*(value(core, z+w) for core, z, w in keys)))
        for name, vector in (('lower', low), ('cap', cap), ('orientation', zz)):
            require(list(map(F, record['physical_vectors'][name])) == vector, 'every actual member vector value')
        lo = [quadratic(forms['C0'], low)] + [quadratic(forms[name], low) for name in ('Delta', 'Rb', 'Rc', 'B')]
        up = [quadratic(forms['U0'], cap)] + [-quadratic(forms[name], cap) for name in ('Delta', 'Rb', 'Rc', 'B')]
        require([[evaluate(poly, k)/P for poly in row] for row in record['complete_cleared_affine_planes']] == [lo, up], 'all complete original dual planes')
        total = [lo[j]+up[j] for j in range(5)]
        require([evaluate(poly, k)/P for poly in record['complete_cleared_combined_plane']] == total, 'all full combined polynomial coefficients')
        require(total[0] < 0 and total[1] < 0 and total[2:] == [0, 0, 0], 'exact original all-real dual signs at each control')
        grid.append({'q': q, 'k': k, 'original_form_positions': 3174})
    # Complete bivariate rectangular grid. Degree <=(9,2) follows from
    # the rational table clearing and explicit disjoint-choice degrees;
    # it is not inferred from the number of sampled points.
    rectangle = [scalar_identities(q, k, original) for q in range(8, 18) for k in (6, 7, 8)]
    members = [actual_members(2*k, k, original, two_pool(2*k, k, original)) for k in (7, 8)]
    require(scalar_identities(14, 7, original)['A'] == '93/4', 'k7 constant-vector proposal fails; no false boundary extension')
    zero_rows = []
    for q in range(8, 18):
        keys, _, forms = one_pool(q, 0, original)
        require(all(sum(row) == 0 for row in forms['C0']),
                'EVERY whole undeleted original C0 row sums to zero')
        zero_rows.append({'q': q, 'original_core_size_rows': len(keys)})
    endpoint_shifts = {'A(k,k),k=17+x': ['-4265/4', '-299/2', '-5'],
                       'A(3k-1,k),k=17+x': ['-107/4', '-173/2', '-5']}
    for k in (17, 18, 19):
        x = k-17
        for q, tag in ((k, 'A(k,k),k=17+x'), (3*k-1, 'A(3k-1,k),k=17+x')):
            A = F(3*q*q-12*k*q+4*k*k-14*k)+F(69*q, 2)+F(121, 4)
            require(A == sum(F(a)*x**i for i, a in enumerate(endpoint_shifts[tag])) < 0,
                    'whole degree-two endpoint shift by complete three-point identity grid')
    finite = finite_certificate(certificate, original)
    return {'actual_agent': 'six-downset-3', 'role': 'researcher', 'completed': True,
            'independent_of_producer_code': True, 'independent_person_review': False,
            'degree_bound_q_k': [9, 2], 'complete_bivariate_grid': rectangle,
            'complete_univariate_form_grid': grid, 'literal_original_controls': members,
            'whole_undeleted_zero_row_grid': zero_rows,
            'strict_negative_endpoint_shifts': endpoint_shifts,
            'complete_33_finite_original_duals': finite,
            'every_integer_k_ge8_q_between_k_and_3k_minus1_excluded': True,
            'complete_k_ge7_q_ge_k_classification_uses_explicit_10032_10206_premises': True,
            'uniform_all_real_obstruction_proved_relative_to_ordinary_decoding': True,
            'q_ge_3k_theorem_not_used_for_new_dual': True,
            'ordinary_counting_polynomial_identity_and_empty_lift_bridges_unformalized': True}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('record', type=Path)
    ap.add_argument('--certificate', type=Path, default=BASE/'FINITE-CERTIFICATE.json')
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args()
    result = checked(json.loads(args.record.read_text()), json.loads(args.certificate.read_text()))
    args.out.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps({'completed': True, 'bivariate_grid_points': 30, 'univariate_grid_points': 10,
                      'all_original_form_positions': 31740,
                      'complete_finite_original_duals': 33,
                      'literal_original_pairs': sum(row['ordered_original_nonempty_pairs'] for row in result['literal_original_controls']),
                      'whole_check_SHA256': hashlib.sha256(args.out.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
