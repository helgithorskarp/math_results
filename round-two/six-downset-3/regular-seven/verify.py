#!/usr/bin/env python3
"""Complete rational capped H verification for all regular seven-point triples.

Default replay regenerates all canonical inputs and checks every matrix.
Decimal arithmetic only proposes rational coordinates. Every accepted
support, row-sum, kernel and positivity statement uses exact arithmetic.
"""
import argparse
from collections import Counter
import copy
from fractions import Fraction as F
import hashlib
import inspect
import json
from pathlib import Path
import resource
import sys
from time import monotonic

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cubic_seven_census import degrees, selected, require
from verify_cubic_seven import digest, integral, lift, polynomial_psd, schur_psd
from census import census
from constructor import prepare, candidate, fractionfree_echelon

TARGETS = (-3, -2, -1, 0, -4, -6, -8)
GRIDS = (20, 40, 80, 160, 320, 640, 1280, 2560)
COUNTS = {0: 1, 3: 10, 6: 311, 9: 311, 12: 10, 15: 1}


def check_domain(cases):
    require(Counter(c['degree'] for c in cases) == COUNTS, 'class degree counts differ')
    require(len({c['canonical_word'] for c in cases}) == 644, 'class words repeat or are missing')
    for c in cases:
        require(c['triple_masks'] == selected(c['canonical_word']), 'literal triples differ from word')
        require(degrees(c['triple_masks']) == (c['degree'],)*7, 'literal input degree differs')


def checked_proposal(case):
    for target in TARGETS:
        prepared = prepare(case, target)
        for grid in GRIDS:
            members, s, c, stats = candidate(prepared, grid)
            n = len(members)+1
            u = [[F(n*int(i == j)-1)-c[i][j] for j in range(n-1)] for i in range(n-1)]
            try:
                cr, ur = schur_psd(c), schur_psd(u)
            except ValueError:
                continue
            if cr == n-8 and ur == n-1:
                return [0]+members, s, c, u, stats
    raise ValueError('bounded proposal recovery failed; no claim of real infeasibility')


def audit(case):
    members, s, c, u, stats = checked_proposal(case)
    n, degree = len(members), case['degree']
    require(n == 29+7*degree//3 and s == 7+degree, 'domain/star parameters differ')
    require(len(set(members)) == n and members[0] == 0, 'empty vertex/domain multiplicity differs')
    included = set(members)
    require(all((a & ~(1 << i)) in included for a in members for i in range(7) if a >> i & 1),
            'literal downward closure fails')
    stars = [[int(a >> i & 1) for a in members] for i in range(7)]
    require(all(sum(x) == s for x in stars), 'actual star sizes differ')
    l = lift(c)
    m = [[F(l[i][j]-s*int(i == j), n-s) for j in range(n)] for i in range(n)]
    require(all(sum(row) == 1 for row in m), 'full row sum fails')
    require(all(m[i][j] == m[j][i] for i in range(n) for j in range(n)), 'full symmetry fails')
    require(all(not m[i][j] for i, a in enumerate(members)
                for j, b in enumerate(members) if a & b), 'full intersection support fails')
    require(all(sum(c[i][j]*star[j+1] for j in range(n-1)) == 0
                for i in range(n-1) for star in stars), 'exact core star kernel fails')
    require(all(sum(l[i][j]*(n*star[j]-s) for j in range(n)) == 0
                for i in range(n) for star in stars), 'full centered star kernel fails')
    upper = [[F(n*int(i == j))-l[i][j] for j in range(n)] for i in range(n)]
    upper_lift = lift(u)
    require(all(upper_lift[i][j]-1 == upper[i][j] for i in range(n) for j in range(n)),
            'full upper congruence fails')
    require(schur_psd(l) == n-7 and schur_psd(upper) == n-1, 'full Schur ranks differ')
    single = [i for i, a in enumerate(members[1:]) if a.bit_count() == 1]
    rest = [i for i, a in enumerate(members[1:]) if a.bit_count() > 1]
    require(len(single) == 7 and len(rest) == n-8, 'star quotient dimensions differ')
    b = [[c[i][j] for j in rest] for i in rest]
    # Reconstruct the other blocks independently from the singleton-pivot star kernel.
    for j in single:
        point = members[j+1].bit_length()-1
        column = [r for r in rest if members[r+1] >> point & 1]
        require(all(c[i][j] == -sum(c[i][r] for r in column) for i in rest),
                'star quotient cross-block identity fails')
    for i in single:
        pi = members[i+1].bit_length()-1
        ri = [r for r in rest if members[r+1] >> pi & 1]
        for j in single:
            pj = members[j+1].bit_length()-1
            rj = [r for r in rest if members[r+1] >> pj & 1]
            require(c[i][j] == sum(c[r][t] for r in ri for t in rj),
                    'star quotient singleton block identity fails')
    b_rank, b_poly, b_den = polynomial_psd(b)
    u_rank, u_poly, u_den = polynomial_psd(u)
    require(b_rank == n-8 and u_rank == n-1, 'polynomial quotient/upper ranks differ')
    numerators, denominator = integral(m)
    return {'degree': degree, 'canonical_word': case['canonical_word'],
            'automorphism_order': case['automorphism_order'],
            'labelled_orbit_size': case['labelled_orbit_size'],
            'point_transitive': case['point_transitive'], 'N': n, 's': s,
            'rank_C': n-8, 'rank_L': n-7, 'rank_I_minus_M': n-1,
            'singleton_quotient_denominator': b_den, 'upper_core_denominator': u_den,
            'singleton_quotient_polynomial_sha256': b_poly,
            'upper_core_polynomial_sha256': u_poly,
            'M_denominator': denominator, 'M_numerators_sha256': digest(numerators),
            'proposal': stats}


def controls(cases):
    rejected = []

    def reject(label, operation):
        try:
            operation()
        except (ValueError, KeyError, ZeroDivisionError, TypeError):
            rejected.append(label)
            return
        raise ValueError('corruption control accepted: '+label)

    for name, matrix in [('negative_diagonal', [[-1]]),
                         ('indefinite_positive_diagonal', [[1, 2], [2, 1]]),
                         ('zero_pivot_nonzero_row', [[0, 1], [1, 1]]),
                         ('asymmetric', [[1, 2], [0, 1]]), ('nonsquare', [[1, 0]])]:
        for checker in (schur_psd, polynomial_psd):
            reject(checker.__name__+'_'+name, lambda a=matrix, f=checker: f(a))
    positive = 0
    for matrix, rank in [([[0]], 0), ([[2, 0], [0, 0]], 1), ([[2, 1], [1, 2]], 2)]:
        require(schur_psd(matrix) == polynomial_psd(matrix)[0] == rank, 'positive PSD control fails')
        positive += 2
    reject('missing_class', lambda: check_domain(cases[:-1]))
    reject('duplicate_class', lambda: check_domain(cases+[cases[0]]))
    damaged = copy.deepcopy(cases)
    damaged[0]['triple_masks'] = [7]
    reject('wrong_literal_domain', lambda: check_domain(damaged))
    reject('inconsistent_zero_equation', lambda: fractionfree_echelon([{}], 1, 1))
    reject('inconsistent_dependent_equations',
           lambda: fractionfree_echelon([{0: 1, 1: 1}, {0: 2, 1: 2}], 2, 3))
    echelon, pivots, _ = fractionfree_echelon([{0: 1, 1: 1}, {0: 1, 1: 1}], 2, 3)
    require(len(echelon) == 1 and pivots == [0], 'singular consistent affine control fails')
    echelon, pivots, _ = fractionfree_echelon([{1: 1}, {0: 1}], 2, 3)
    require(len(echelon) == 2 and pivots == [0, 1], 'affine pivoting control fails')
    return {'rejected_controls': rejected, 'rejected_control_count': len(rejected),
            'positive_PSD_algorithm_checks': positive, 'positive_affine_elimination_checks': 2}


def fingerprint():
    root = Path(__file__).resolve().parent
    files = ['constructor.py', 'census.py', '../cubic_seven_census.py', '../verify_cubic_seven.py']
    return digest({'files': {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in files},
                   'audit_source': inspect.getsource(audit), 'targets': TARGETS, 'grids': GRIDS})


def summary(cases, coverage, records, control_results):
    return {'agent': 'six-downset-3', 'role': 'researcher', 'source_fingerprint': fingerprint(),
            'scope_complete': len(records) == 644, 'verified_classes': len(records),
            'coverage': coverage, 'controls': control_results,
            'canonical_words': {str(d): [c['canonical_word'] for c in cases if c['degree'] == d] for d in COUNTS},
            'record_aggregate_sha256': digest(records),
            'by_degree': {str(d): {
                'verified_classes': sum(r['degree'] == d for r in records), 'N': 29+7*d//3, 's': 7+d,
                'rank_L': 22+7*d//3, 'rank_I_minus_M': 28+7*d//3,
                'target_grid_profile': dict(Counter(str((r['proposal']['target'], r['proposal']['grid']))
                                                   for r in records if r['degree'] == d)),
                'matrix_denominator_profile': {str(k): v for k, v in sorted(Counter(r['M_denominator'] for r in records if r['degree'] == d).items())}}
                          for d in COUNTS},
            'all_full_support_rowsum_and_kernel_checks_pass': True,
            'all_full_Schur_and_quotient_upper_polynomial_checks_pass': True,
            'product_scope': {'factors': 'every finite nonempty sequence of certified regular-seven factors',
                              'N': 'product_j (29+7*d_j/3)', 'eligible_factors': 'those with greatest d_j',
                              'largest_star': 'N*(7+d_max)/(29+7*d_max/3)',
                              'rank_L': 'N-7*(number of eligible factors)',
                              'maximum_families': 'exactly the coordinate stars in eligible factors'}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', type=Path)
    parser.add_argument('--progress', type=Path, help='local compact resumable per-class evidence, never needed for default replay')
    parser.add_argument('--resume', type=Path, help='author-side resume; trusts prior per-class records matching the source fingerprint')
    parser.add_argument('--smoke', action='store_true', help='explicit partial eight-case check, never complete coverage')
    args = parser.parse_args()
    require(not (args.check and args.smoke), 'partial smoke cannot check a complete result')
    start = monotonic()
    cases, coverage = census()
    check_domain(cases)
    print('complete canonical census', len(cases), 'classes;', coverage['total_labelled_collections'],
          'labelled; seconds', round(monotonic()-start, 3), flush=True)
    chosen = cases
    if args.smoke:
        chosen = [next(c for c in cases if c['degree'] == d) for d in COUNTS]
        chosen += [next(c for c in cases if c['degree'] == d and c['automorphism_order'] == 1) for d in [6, 9]]
        chosen.sort(key=lambda c: (c['degree'], c['canonical_word']))
    records = []
    if args.resume:
        saved = json.loads(args.resume.read_text())
        require(saved['source_fingerprint'] == fingerprint(), 'resume source fingerprint differs')
        records = saved['records']
        require([(r['degree'], r['canonical_word']) for r in records] ==
                [(c['degree'], c['canonical_word']) for c in chosen[:len(records)]], 'resume prefix differs')
    for case in chosen[len(records):]:
        records.append(audit(case))
        if args.progress:
            temporary = args.progress.with_name(args.progress.name+'.tmp')
            temporary.write_text(json.dumps({'source_fingerprint': fingerprint(), 'records': records},
                                            separators=(',', ':'), sort_keys=True)+'\n')
            temporary.replace(args.progress)
        if len(records) % 10 == 0 or len(records) == len(chosen):
            print('exact verified classes', len(records), '/', len(chosen), 'last degree', case['degree'],
                  'word', case['canonical_word'], 'seconds', round(monotonic()-start, 3), flush=True)
    result = summary(cases, coverage, records, controls(cases))
    if args.check:
        require(result == json.loads(args.check.read_text()), 'expected complete result differs')
        print('all 644 regular-seven classes: exact capped maximal ranks and equality/product scope match', flush=True)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    elif not args.check:
        print(json.dumps(result, sort_keys=True), flush=True)
    print('seconds', round(monotonic()-start, 3), 'peak_RSS_KiB',
          resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, flush=True)
