#!/usr/bin/env python3
"""Exhaustive small physical controls and rejected certificate corruptions."""
import argparse
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path

import produce
import verify


def check():
    cases = []
    saw_improvement = saw_worsening = saw_neutral = saw_zero = False
    # Exhaust every visible coloring, then every grouped star assignment.
    # Repeated variable contacts and constant (mask-zero) five-sets occur.
    for n, f, groups in [(5, 4, {0: 0, 1: 0, 2: 1}),
                          (6, 5, {0: 0, 1: 0, 2: 1})]:
        visible = [e for e in combinations(range(n), 2)
                   if not (f in e and (e[1] if e[0] == f else e[0]) in groups)]
        assignments = 0
        constants = 0
        for pattern in range(1 << len(visible)):
            red = {e for i, e in enumerate(visible) if pattern & (1 << i)}
            coeff = produce.coefficients(n, red, f, groups)
            verify.need(coeff == verify.reconstruct(n, red, f, groups), 'small K4 reconstruction')
            computed = produce.scores(coeff, 2)
            verify.need(computed == verify.direct_scores(coeff, 2), 'small direct/zeta agreement')
            constants += sum(c.get(0, 0) for c in coeff)
            for a in range(4):
                graph = red | {tuple(sorted((f, v))) for v, i in groups.items() if a & (1 << i)}
                physical = list(map(len, verify.literal(n, graph)))
                verify.need(computed[a] == physical, 'small physical count')
                assignments += 1
                saw_improvement |= sum(physical) < sum(computed[0])
                saw_worsening |= sum(physical) > sum(computed[0])
                saw_neutral |= a != 0 and physical == computed[0]
                saw_zero |= sum(physical) == 0
        cases.append({'vertices': n, 'visible_colorings': 1 << len(visible),
                      'star_assignments_per_coloring': 4, 'physical_scores_checked': assignments,
                      'constant_weight_sum': constants})
    verify.need(all((saw_improvement, saw_worsening, saw_neutral, saw_zero)), 'control outcome coverage')
    # Additional all-fixed K5 through f: its mask-zero term must survive too.
    red = set(combinations(range(7), 2))
    groups = {0: 0, 1: 0}
    coeff = produce.coefficients(7, red, 6, groups)
    verify.need(coeff == verify.reconstruct(7, red, 6, groups), 'constant through f')
    verify.need(coeff[1][0] == 7, 'six avoiding f plus one through f')
    for a, counts in enumerate(produce.scores(coeff, 1)):
        graph = red - {(v, 6) for v in groups if a == 0}
        verify.need(counts == list(map(len, verify.literal(7, graph))), 'constant-through-f physical count')

    certificate = json.loads((produce.HERE / 'certificate.json').read_text())
    block = certificate['blocks'][0]
    graph = verify.read(produce.HERE / 'input.edges')
    coeff = verify.reconstruct(43, graph, 33, {v: v//3 for v in range(33)})
    table = verify.direct_scores(coeff, 11)
    base = sum(1 << t for t in range(11) if (3*t, 33) in graph)
    verify.validate_block(block, coeff, 33, base, table)
    rejected = []
    for name in ['weight', 'omit_constant', 'duplicate_support', 'out_of_range', 'negative_weight',
                 'wrong_vertex', 'wrong_base', 'false_minimum', 'omit_argmin', 'false_changed_minimum',
                 'corrupt_table']:
        b, t = deepcopy(block), deepcopy(table)
        records = b['coefficients_blue_red'][0]
        if name == 'weight': records[-1][1] += 1
        elif name == 'omit_constant': records.pop(0)
        elif name == 'duplicate_support': records.insert(0, records[0][:])
        elif name == 'out_of_range': records[-1][0] = 2048
        elif name == 'negative_weight': records[-1][1] = -1
        elif name == 'wrong_vertex': b['fixed_vertex'] = 34
        elif name == 'wrong_base': b['base_mask'] ^= 1
        elif name == 'false_minimum': b['minimum'] -= 1
        elif name == 'omit_argmin': b['argmin_masks'] = []
        elif name == 'false_changed_minimum': b['minimum_changed'] -= 1
        elif name == 'corrupt_table': t[0][0] += 1
        try:
            verify.validate_block(b, coeff, 33, base, t)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('accepted corrupt certificate: ' + name)
    return {'small_cases': cases, 'extra_constant_through_root_checks': 2,
            'outcomes_seen': {'improvement': saw_improvement, 'worsening': saw_worsening,
                              'neutral': saw_neutral, 'zero': saw_zero},
            'rejected_corruptions': rejected}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    result = check()
    a.report.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print('VERIFIED controls:', sum(r['physical_scores_checked'] for r in result['small_cases'])+2,
          'physical scores;', len(result['rejected_corruptions']), 'corruptions rejected')
