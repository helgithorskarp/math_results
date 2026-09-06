#!/usr/bin/env python3
"""Exhaustive small paired-star colorings, including all mutual-edge colors."""
import argparse
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
import time

import produce
import verify


def compare(n, roots, contacts, red, k):
    variables = {tuple(sorted((f, v))): bit for f in roots for v, bit in contacts[f].items()}
    coeff = produce.coefficients(n, red, variables)
    reconstructed, _ = verify.reconstruct(n, red, roots, contacts)
    verify.need(coeff == reconstructed, 'toy physical coefficients')
    blue, red_counts = [produce.zeta(c, k) for c in coeff]
    blue.reverse()
    tables = [blue, red_counts]
    for a in range(1 << k):
        graph = {e for e in red if e not in variables}
        graph.update(e for e, bit in variables.items() if a & (1 << bit))
        counts = list(map(len, verify.literal(n, graph)))
        verify.need(counts == [t[a] for t in tables], 'toy literal count')
    gray = verify.gray_check(reconstructed, k, tables)
    verify.need(gray['complete'] and gray['checked_assignments'] == (1 << k), 'complete toy Gray scan')
    return coeff, tables


def run():
    cases = []
    # Distinct contacts allow six-bit interaction supports; repeated contacts
    # exercise their collapse to a single Boolean without losing multiplicity.
    for n, roots, contacts, k in [
        (5, (3, 4), {3: {0: 0, 1: 1, 2: 2}, 4: {0: 3, 1: 4, 2: 5}}, 6),
        (6, (4, 5), {4: {0: 0, 1: 0, 2: 1}, 5: {0: 2, 1: 2, 2: 3}}, 4)]:
        variables = {tuple(sorted((f, v))) for f in roots for v in contacts[f]}
        visible = [e for e in combinations(range(n), 2) if e not in variables]
        max_support = 0
        for pattern in range(1 << len(visible)):
            graph = {e for i, e in enumerate(visible) if pattern & (1 << i)}
            coeff, _ = compare(n, roots, contacts, graph, k)
            max_support = max(max_support, max((s.bit_count() for c in coeff for s in c), default=0))
        cases.append({'vertices': n, 'bits': k, 'visible_colorings': 1 << len(visible),
                      'physical_scores': (1 << len(visible)) * (1 << k), 'maximum_support': max_support})
    verify.need(cases[0]['maximum_support'] == 6, 'six-bit coupled support exercised')
    # Seven unconditional sets: one avoiding both roots, two using one root,
    # and four using both. Check both monochromatic visible colors.
    for color in (0, 1):
        graph = set(combinations(range(7), 2)) if color else set()
        coeff, tables = compare(7, (5, 6), {5: {0: 0}, 6: {0: 1}}, graph, 2)
        verify.need(coeff[color][0] == 7, 'constant sets in all three root strata')
    # Directly exercise actual Gray checker failure and incomplete semantics.
    coeff = [{0: 3, 1: 2, 6: 4}, {0: 1, 2: 5, 5: 3}]
    tables = [[verify.direct(coeff, a)[c] for a in range(8)] for c in (0, 1)]
    verify.need(verify.gray_check(coeff, 3, tables)['complete'], 'valid control table')
    prefix = verify.gray_check(coeff, 3, tables, 4)
    verify.need(not prefix['complete'] and prefix['checked_assignments'] == 4, 'prefix must not claim completion')
    rejected = []
    for name in ('blue_count', 'red_count', 'constant', 'interaction', 'empty_prefix', 'oversized_prefix'):
        cs, ts = deepcopy(coeff), deepcopy(tables)
        limit = None
        if name == 'blue_count': ts[0][3] += 1
        elif name == 'red_count': ts[1][7] += 1
        elif name == 'constant': cs[0][0] += 1
        elif name == 'interaction': cs[1].pop(5)
        elif name == 'empty_prefix': limit = 0
        elif name == 'oversized_prefix': limit = 9
        try:
            verify.gray_check(cs, 3, ts, limit)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('accepted corrupt Gray case '+name)
    return {'exhaustive_cases': cases, 'extra_physical_scores': 8,
            'total_physical_scores': sum(c['physical_scores'] for c in cases)+8,
            'constant_strata_checked': [0, 1, 2], 'rejected_corruptions': rejected,
            'prefix_reported_incomplete': True}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    begin = time.perf_counter()
    result = run()
    a.report.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print('VERIFIED', result['total_physical_scores'], 'physical controls;',
          len(result['rejected_corruptions']), 'corruptions; seconds', round(time.perf_counter()-begin, 6))
