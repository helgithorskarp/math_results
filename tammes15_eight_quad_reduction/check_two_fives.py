#!/usr/bin/env python3
"""Updated exact necessary cover after TWO_FIVES.md; not geometry formalization.

CPython >=3.11; standard library. The unchanged original checker supplies
canonical codes and an independent path/cycle component generator.
"""
from fractions import Fraction as F
from itertools import combinations, product
import json
import sys

import check as prior


def legal(labels, edges):
    return labels.count('5/1') <= 1 and prior.legal(labels, edges)


def arithmetic():
    margins = {
        'two_large_corners_vs_ordinary_four_pi_units': 2 * F(2, 3) - F(5, 4),
        'half_angle_cosine_squared_vs_nine_sixteenths': F(2, 3) - F(9, 16),
        'common_neighbor_cauchy_gap': 1 - F(8, 9),
    }
    prior.need(all(v > 0 for v in margins.values()), 'nonpositive margin')
    # The strict three-corner contradiction uses each corner >y>2pi/3.
    prior.need(3 * F(2, 3) == 2, 'three-large-corner endpoint')
    prior.need(F(1, 9) - F(8, 9) * F(3, 4) == -F(5, 9),
               'separated opposite cosine endpoint')
    return {k: str(v) for k, v in sorted(margins.items())}


def cover():
    baseline = prior.cover()
    rows, profiles = [], []
    for d41, d42, d51 in product(range(5), range(3), range(5)):
        if d41 + 2 * d42 + d51 != 4:
            continue
        labels = ['4/1'] * d41 + ['4/2'] * d42 + ['5/1'] * d51
        pairs = tuple(combinations(range(len(labels)), 2))
        codes, descriptors = set(), set()
        for mask in range(1 << len(pairs)):
            edges = frozenset(e for i, e in enumerate(pairs) if (mask >> i) & 1)
            if legal(labels, edges):
                codes.add(prior.code(labels, edges))
                descriptors.add(prior.signature(labels, edges))
        independent = prior.component_cover(labels) if d51 <= 1 else set()
        prior.need(descriptors == independent, 'independent component cover mismatch')
        prior.need(len(codes) == len(descriptors), 'canonical type mismatch')
        before = next(row for row in baseline['distributions']
                      if (row['d41'], row['d42'], row['d51']) == (d41, d42, d51))
        expected_codes = before['allowed_H_codes'] if d51 <= 1 else []
        prior.need(sorted(codes) == expected_codes, 'original-cover comparison')
        for n3 in range(7):
            n4, n5 = 13 - 2 * n3, n3 + 2
            if codes and d41 + d42 <= n4 and d51 <= n5:
                profiles.append({'n3': n3, 'n4': n4, 'n5': n5,
                                 'd41': d41, 'd42': d42, 'd51': d51,
                                 'H_codes': sorted(codes)})
        rows.append({'d41': d41, 'd42': d42, 'd51': d51,
                     'vertex_colors': labels, 'allowed_H_codes': sorted(codes),
                     'surviving_degree_profiles': sum(
                         (p['d41'], p['d42'], p['d51']) == (d41, d42, d51)
                         for p in profiles)})
    filtered = [p for p in baseline['profiles'] if p['d51'] <= 1]
    prior.need(profiles == filtered, 'entry-level degree-profile comparison')
    prior.need(len(profiles) == 29, 'degree-profile count')
    prior.need(sum(len(row['allowed_H_codes']) for row in rows) == 17,
               'colored auxiliary count')
    prior.need(sum(bool(row['allowed_H_codes']) for row in rows) == 5,
               'deficit distribution count')
    removed = [p for p in baseline['profiles'] if p['d51'] >= 2]
    prior.need([p['n3'] for p in removed] == list(range(6)), 'removed degree profiles')
    prior.need(all((p['d41'], p['d42'], p['d51']) == (2, 0, 2) for p in removed),
               'removed distribution')
    return {'previous_degree_profiles': 35, 'remaining_degree_profiles': 29,
            'previous_colored_H_types': 18, 'remaining_colored_H_types': 17,
            'remaining_deficit_distributions': 5,
            'removed_profiles': removed, 'distributions': rows, 'profiles': profiles}


def selftest():
    controls = 0

    def test(condition, name):
        nonlocal controls
        prior.need(condition, name)
        controls += 1

    path = prior.normalized_edges(((0, 1), (1, 2), (2, 3)))
    cycle = prior.normalized_edges(((0, 1), (1, 2), (2, 3), (3, 0)))
    centered = prior.normalized_edges(((0, 1), (1, 2)))
    labels = ['4/1', '5/1', '5/1', '4/1']
    test(prior.legal(labels, path), 'original two-five path remains in baseline')
    test(not legal(labels, path), 'new two-five path exclusion')
    test(legal(['4/1', '5/1', '4/1', '4/1'], path), 'single-five internal path retained')
    test(legal(['5/1', '4/1', '4/1', '4/1'], cycle), 'single-five cycle retained')
    test(legal(['4/1', '5/1', '4/1', '4/1'], centered), 'single-five centered path retained')
    test(legal(['4/1', '5/1', '4/2'], centered), 'mixed deficit centered path retained')
    test(legal(['4/2', '4/2'], frozenset()), 'no-five empty cover retained')
    test(not legal(['5/1', '4/1', '4/1', '4/1'], path), 'five leaf remains rejected')
    test(arithmetic()['two_large_corners_vs_ordinary_four_pi_units'] == '1/12',
         'strict angle margin')
    test(len(cover()['profiles']) == 29, 'full exact cover')
    return controls


def main():
    prior.need(sys.argv[1:] in ([], ['--selftest']),
               'usage: check_two_fives.py [--selftest]')
    if sys.argv[1:]:
        print(json.dumps({'status': 'PASS', 'controls': selftest(),
                          'degree_profiles': 29, 'colored_H_types': 17}, sort_keys=True))
    else:
        print(json.dumps({'agent': 'six-tammes-1', 'role': 'researcher',
                          'scope': 'exact rational checks and necessary auxiliary cover; hand proof separate',
                          'strict_margins': arithmetic(), 'cover': cover()},
                         indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
