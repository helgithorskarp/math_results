#!/usr/bin/env python3
"""Exact capped H certificates for all cubic triple collections on seven points.

Only Python's standard library is used. See PROOF.md for completeness,
the empty-vertex lift, rank maximality, equality, and tensor deductions.
The integer Schur and characteristic-polynomial algorithms follow the
credited public spectral_downset_six_exact checkers, with different
mathematical positivity criteria; this is not independent peer review.
"""
import argparse
import copy
from fractions import Fraction as F
import hashlib
from itertools import combinations
import json
from math import lcm
from pathlib import Path

from cubic_seven_census import canonical_census, move, require


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':'), sort_keys=True).encode()).hexdigest()


def integral(matrix):
    n = len(matrix)
    require(n > 0 and all(len(row) == n for row in matrix), 'nonsquare matrix')
    require(all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(n)),
            'asymmetric matrix')
    denominator = lcm(*(F(x).denominator for row in matrix for x in row))
    return [[int(F(x)*denominator) for x in row] for row in matrix], denominator


def schur_psd(matrix):
    """Fraction-free Schur congruences, including singular-pivot checks."""
    a, _ = integral(matrix)
    n, previous, rank = len(a), 1, 0
    for k in range(n):
        pivot = a[k][k]
        require(pivot >= 0, 'negative Schur pivot')
        if not pivot:
            require(not any(a[k][j] for j in range(k+1, n)),
                    'zero Schur pivot with a nonzero row')
            continue
        for i in range(k+1, n):
            for j in range(i, n):
                numerator = pivot*a[i][j]-a[i][k]*a[k][j]
                a[i][j], remainder = divmod(numerator, previous)
                require(remainder == 0, 'nonexact fraction-free division')
                a[j][i] = a[i][j]
        previous = pivot
        rank += 1
    return rank


def polynomial_psd(matrix):
    """Faddeev--LeVerrier plus exact nonnegative coefficient criterion."""
    a, denominator = integral(matrix)
    n = len(a)
    b = [[int(i == j) for j in range(n)] for i in range(n)]
    coefficients = [1]
    for k in range(1, n+1):
        c = [[sum(a[i][h]*b[h][j] for h in range(n)) for j in range(n)]
             for i in range(n)]
        coefficient, remainder = divmod(-sum(c[i][i] for i in range(n)), k)
        require(remainder == 0, 'nonintegral characteristic coefficient')
        coefficients.append(coefficient)
        for i in range(n):
            c[i][i] += coefficient
        b = c
    require(not any(x for row in b for x in row), 'Cayley-Hamilton residual')
    require(all((-1)**j*x >= 0 for j, x in enumerate(coefficients)),
            'negative-root coefficient criterion fails')
    return max(j for j, x in enumerate(coefficients) if x), digest(coefficients), denominator


def lift(c):
    rows = [sum(row) for row in c]
    return [[1+sum(rows)]+[1-x for x in rows]] + [
        [1-rows[i]]+[1+x for x in row] for i, row in enumerate(c)]


def decode(case, certificate):
    require(certificate['canonical_word'] == case['canonical_word'], 'wrong class word')
    require(certificate['triple_masks'] == case['triple_masks'], 'wrong literal triples')
    nonempty = sorted([1 << i for i in range(7)] +
                      [sum(1 << i for i in t) for t in combinations(range(7), 2)] +
                      case['triple_masks'])
    require(len(nonempty) == len(set(nonempty)) == 35, 'wrong domain cardinality')
    pairs = {(a, b) for a, b in combinations(nonempty, 2) if not a & b}
    entries, sizes = {}, []
    reps, values = certificate['Q_orbit_representatives'], certificate['Q_orbit_values']
    require(len(reps) == len(values), 'orbit/value length mismatch')
    for pair, raw_value in zip(reps, values):
        require(len(pair) == 2 and tuple(pair) in pairs, 'bad disjoint-pair representative')
        a, b = pair
        orbit = {tuple(sorted((move(a, p), move(b, p)))) for p in case['point_group']}
        require(tuple(pair) == min(orbit), 'noncanonical orbit representative')
        require(orbit <= pairs and not entries.keys() & orbit, 'overlapping pair orbits')
        require(type(raw_value) is str, 'fraction must have exact string encoding')
        value = F(raw_value)
        entries.update({pair: value for pair in orbit})
        sizes.append(len(orbit))
    require(set(entries) == pairs, 'disjoint-pair orbits are incomplete')
    c = [[F(9) if a == b else F(-1) if a & b else
          entries[(min(a, b), max(a, b))]-1 for b in nonempty] for a in nonempty]
    return [0]+nonempty, c, sizes


def audit(case, certificate, positivity=True):
    members, c, sizes = decode(case, certificate)
    n, s = len(members), 10
    included = set(members)
    require(n == 36 and all((a & ~(1 << i)) in included
                           for a in members for i in range(7) if a >> i & 1),
            'downward closure fails')
    stars = [[int(a >> i & 1) for a in members] for i in range(7)]
    require(all(sum(x) == s for x in stars), 'actual star sizes differ')
    l = lift(c)
    m = [[F(l[i][j]-s*int(i == j), n-s) for j in range(n)] for i in range(n)]
    require(all(sum(row) == 1 for row in m), 'row-sum condition fails')
    require(all(m[i][j] == m[j][i] for i in range(n) for j in range(n)), 'symmetry fails')
    require(all(not m[i][j] for i, a in enumerate(members)
                for j, b in enumerate(members) if a & b), 'intersection support fails')
    require(all(sum(c[i][j]*star[j+1] for j in range(n-1)) == 0
                for i in range(n-1) for star in stars), 'exact star kernel fails')
    require(all(sum(l[i][j]*(n*star[j]-s) for j in range(n)) == 0
                for i in range(n) for star in stars), 'centered star kernel fails')
    u = [[F(n*int(i == j)-1)-c[i][j] for j in range(n-1)] for i in range(n-1)]
    upper = [[F(n*int(i == j))-l[i][j] for j in range(n)] for i in range(n)]
    upper_lift = lift(u)
    require(all(upper_lift[i][j]-1 == upper[i][j] for i in range(n) for j in range(n)),
            'full upper congruence identity fails')
    if not positivity:
        return None
    require(schur_psd(c) == 28 and schur_psd(u) == 35, 'core PSD ranks differ')
    require(schur_psd(l) == 29 and schur_psd(upper) == 35, 'full PSD ranks differ')
    c_rank, c_poly, c_den = polynomial_psd(c)
    u_rank, u_poly, u_den = polynomial_psd(u)
    require(c_rank == 28 and u_rank == 35, 'polynomial PSD ranks differ')
    numerators, denominator = integral(m)
    return {'canonical_word': case['canonical_word'], 'triple_masks': case['triple_masks'],
            'automorphism_order': case['automorphism_order'],
            'labelled_orbit_size': case['labelled_orbit_size'],
            'point_transitive': case['point_transitive'], 'N': n, 's': s,
            'rank_C': 28, 'rank_L': 29, 'rank_upper_core': 35, 'rank_I_minus_M': 35,
            'Q_pair_orbits': len(sizes), 'Q_pair_orbit_sizes': sizes,
            'C_denominator': c_den, 'upper_core_denominator': u_den,
            'C_polynomial_sha256': c_poly, 'upper_core_polynomial_sha256': u_poly,
            'M_denominator': denominator, 'M_numerators_sha256': digest(numerators)}


def check_fixture_domain(cases, fixtures):
    require(type(fixtures) is list, 'class fixture is not a list')
    require([f['canonical_word'] for f in fixtures] == [c['canonical_word'] for c in cases],
            'certificate class list does not exactly match the canonical domain')


def controls(cases, fixtures):
    rejected = []

    def expect_rejection(label, operation):
        try:
            operation()
        except (ValueError, KeyError, ZeroDivisionError, TypeError):
            rejected.append(label)
            return
        raise ValueError('corruption control was accepted: '+label)

    for name, bad in [('negative_diagonal', [[-1]]),
                      ('indefinite_positive_diagonal', [[1, 2], [2, 1]]),
                      ('singular_nonzero_row', [[0, 1], [1, 1]]),
                      ('asymmetric', [[1, 2], [0, 1]]),
                      ('nonsquare', [[1, 0]])]:
        for checker in (schur_psd, polynomial_psd):
            expect_rejection(checker.__name__+'_'+name, lambda b=bad, f=checker: f(b))
    positive_checks = 0
    for matrix, rank in [([[0]], 0), ([[2, 0], [0, 0]], 1), ([[2, 1], [1, 2]], 2)]:
        require(schur_psd(matrix) == polynomial_psd(matrix)[0] == rank,
                'positive/singular PSD control failed')
        positive_checks += 2
    expect_rejection('missing_class', lambda: check_fixture_domain(cases, fixtures[:-1]))
    expect_rejection('duplicated_class', lambda: check_fixture_domain(cases, fixtures+[fixtures[0]]))
    for name in ['wrong_class_word', 'wrong_triple_domain', 'missing_orbit',
                 'duplicate_orbit', 'intersecting_representative', 'wrong_affine_entry']:
        damaged = copy.deepcopy(fixtures[0])
        if name == 'wrong_class_word':
            damaged['canonical_word'] += 1
        elif name == 'wrong_triple_domain':
            damaged['triple_masks'][0] = 7
        elif name == 'missing_orbit':
            damaged['Q_orbit_representatives'].pop()
            damaged['Q_orbit_values'].pop()
        elif name == 'duplicate_orbit':
            damaged['Q_orbit_representatives'].append(damaged['Q_orbit_representatives'][0])
            damaged['Q_orbit_values'].append(damaged['Q_orbit_values'][0])
        elif name == 'intersecting_representative':
            damaged['Q_orbit_representatives'][0] = [1, 3]
        elif name == 'wrong_affine_entry':
            damaged['Q_orbit_values'][0] = str(F(damaged['Q_orbit_values'][0])+1)
        expect_rejection(name, lambda d=damaged: audit(cases[0], d, positivity=False))
    return {'rejected_controls': rejected, 'rejected_control_count': len(rejected),
            'positive_or_singular_algorithm_checks': positive_checks}


def run(certificate_path):
    cases, coverage = canonical_census()
    require(coverage['labelled_collections'] == 11205 and coverage['permutation_classes'] == 10
            and coverage['point_transitive_classes'] == 2, 'coverage differs from stated cohort')
    document = json.loads(certificate_path.read_text())
    require(document['format_version'] == 1, 'unsupported fixture format')
    fixtures = document['classes']
    check_fixture_domain(cases, fixtures)
    records = [audit(case, fixture) for case, fixture in zip(cases, fixtures)]
    return {'agent': 'six-downset-3', 'role': 'researcher', 'coverage': coverage,
            'class_records': records, 'controls': controls(cases, fixtures),
            'all_core_schur_and_polynomial_checks_pass': True,
            'all_full_support_rowsum_and_schur_checks_pass': True,
            'product_scope': {'k': 'every integer k>=1', 'factors': 'arbitrary choices from the ten classes',
                              'N': '36^k', 'largest_star': '10*36^(k-1)',
                              'rank_L': '36^k-7*k', 'maximum_families': 'exactly the 7*k coordinate stars'}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path,
                        default=Path(__file__).with_name('CUBIC_SEVEN_CERTIFICATES.json'))
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = run(args.certificate)
    if args.check:
        require(result == json.loads(args.check.read_text()), 'expected result differs')
        print('exact ten-class cubic seven-point coverage, capped ranks, and 18 rejection controls match')
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    elif not args.check:
        print(json.dumps(result, indent=2, sort_keys=True))
