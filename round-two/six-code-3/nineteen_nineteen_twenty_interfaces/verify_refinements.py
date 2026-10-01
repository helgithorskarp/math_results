"""Literal leave and anchor-cycle refinements of the checked mixed census.

No old nineteen-star statistic or native graph decoder is imported.
Full color verification precedes the independent invariant readout.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

from verify_colors import require, sha
from verify_full import check


def leave_count(words, center):
    link = [word - {center} for word in words if center in word]
    require(len(link) == 19, 'literal refinement nineteen-link')
    points = [p for p in range(18) if p != center]
    degrees = {p: sum(p in word for word in link) for p in points}
    require(sum(degrees.values()) == 76 and max(degrees.values()) <= 5,
            'literal refinement link degrees')
    covered = {tuple(pair) for word in link for pair in combinations(sorted(word), 2)}
    low = [p for p in points if degrees[p] == 5]
    return sum(tuple(pair) not in covered for pair in combinations(low, 2))


def anchor_cycles(words):
    rows = [word - {17, 15} for word in words if {17, 15} <= word]
    cols = [word - {17, 16} for word in words if {17, 16} <= word]
    require(len(rows) == len(cols) == 5 and all(len(q) == 3 for q in rows + cols),
            'literal anchor five triple partitions')
    ordinary = set(range(15))
    require(set.union(*rows) == set.union(*cols) == ordinary and
            sum(len(q) for q in rows) == sum(len(q) for q in cols) == 15,
            'literal anchor partitions cover all ordinary points')
    require(all(len(a & b) <= 1 for a in rows for b in cols), 'literal anchor simple occupancy')
    adjacent = [set() for _ in range(10)]
    for r, row in enumerate(rows):
        for c, col in enumerate(cols):
            if not row & col:
                adjacent[r].add(5 + c)
                adjacent[5 + c].add(r)
    require(all(len(row) == 2 for row in adjacent), 'literal anchor complement two-regular')
    unseen, lengths = set(range(10)), []
    while unseen:
        pending = [min(unseen)]; unseen.remove(pending[0]); vertices = 0
        while pending:
            point = pending.pop(); vertices += 1
            for neighbor in adjacent[point]:
                if neighbor in unseen:
                    unseen.remove(neighbor); pending.append(neighbor)
        require(vertices % 2 == 0, 'literal bipartite cycle size')
        lengths.append(vertices // 2)
    lengths.sort()
    require(lengths in ([5], [2, 3]), 'literal anchor cycle forms')
    return lengths


def run(census_work, color_work, expected, residual_expected, witness, refinement_expected):
    checked = check(census_work, color_work, expected, residual_expected, witness)
    cores = []
    for row in expected['cases']:
        cores.extend(json.loads((census_work / f"fast-case-{row['case']}-{row['orientation']}.json").read_text())['cores'])
    require(sha(cores) == expected['core_records_sha256'], 'literal refinement unchanged full core inventory')
    records, invariants, groups = [], [], {}
    for index, core in enumerate(cores):
        words = [set(p for p in range(18) if mask & (1 << p)) for mask in core['blocks']]
        mx, my = leave_count(words, 17), leave_count(words, 15)
        cycles = anchor_cycles(words)
        require(my == core['y_m'], 'literal refinement old/new leave readout mismatch')
        row = json.loads((color_work / f'color-{index}.json').read_text())
        records.append(row)
        require(row['index'] == index and row['core_sha256'] == core['core_sha256'],
                'literal refinement core/color alignment')
        invariant = {'index': index, 'core_sha256': core['core_sha256'],
                     'anchor_cycle_half_lengths': cycles, 'm_x': mx, 'm_y': my,
                     'capacity': row['capacity']}
        invariants.append(invariant)
        key = (tuple(cycles), mx, my)
        groups.setdefault(key, []).append(row['capacity'])
    certificate = {'status': 'COMPLETE_ALL_CORE_PROPER_COLOR_RECORDS',
                   'domain_sha256': sha(expected), 'core_count': 4871, 'records': records}
    require(sha(certificate) == residual_expected['certificate_sha256'],
            'literal refinement unchanged full color certificate')
    summary = [{'anchor_cycle_half_lengths': list(cycles), 'm_x': mx, 'm_y': my,
                'cores': len(values), 'maximum_capacity': max(values), 'certified_total_upper_bound': 44 + max(values)}
               for (cycles, mx, my), values in sorted(groups.items())]
    require(summary == refinement_expected['groups'], 'literal complete refinement census')
    require(sum(row['cores'] for row in summary) == 4871, 'literal refinement complete domain')
    return {'status': 'PASS_ALL4871_LITERAL_INVARIANTS_AND_COLOR_REFINEMENTS',
            'groups': summary, 'invariant_records_sha256': sha(invariants),
            'per_core_color_checks_sha256': checked['per_core_checks_sha256'],
            'scope': 'Same uncovered19/19/20, pair5/5/4 hypotheses; subgroup bounds are not asserted sharp.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--census-work', type=Path, required=True)
    parser.add_argument('--color-work', type=Path, required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    data = [json.loads((here / name).read_text()) for name in
            ('expected.json', 'RESIDUAL_SUMMARY.json', 'witness67.json', 'REFINEMENTS.json')]
    print(json.dumps(run(args.census_work, args.color_work, *data), sort_keys=True))
