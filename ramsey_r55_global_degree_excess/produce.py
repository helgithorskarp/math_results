#!/usr/bin/env python3
"""Exact certificate for the global degree-excess bound; standard library only."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / 'ramsey_r55_regular18_overlap_exclusion'


def inputs():
    dependencies = json.loads((HERE / 'DEPENDENCIES.json').read_text())
    for name, digest in dependencies['parent_files'].items():
        if hashlib.sha256((PARENT / name).read_bytes()).hexdigest() != digest:
            raise ValueError('parent identity: ' + name)
    return json.loads((PARENT / 'CERTIFICATE.json').read_text())


def partitions(n, least=1):
    if n == 0:
        yield ()
    for d in range(least, n + 1):
        for rest in partitions(n - d, d):
            yield (d,) + rest


def produce():
    parent = inputs()
    buckets = []
    totals = [0, 0]
    for b in parent['buckets']:
        c = b['common_order']
        ds = b['common_degree_sequence']
        e = sum(ds) // 2
        first = c * (29 - c) + 2 * e
        second = sum(d * d for d in ds) + (40 - c) * e
        if (first, second) != (b['degree_budget'], b['edge_budget']):
            raise ValueError('parent threshold mismatch')
        failures = [0, 0]
        for x, y in itertools.combinations_with_replacement(b['profiles'], 2):
            if x[0] + y[0] + 2 < first:
                failures[0] += 1
            elif x[1] + y[1] + 2 * max(ds) < second:
                failures[1] += 1
            else:
                raise ValueError('a profile pair survives deficit two')
        for j in range(2):
            totals[j] += failures[j]
        buckets.append({'common_order': c, 'common_degree_sequence': ds,
                        'profiles': len(b['profiles']),
                        'rejected_by_first_then_second': failures})

    incidence = []
    for total in (2, 4):
        threshold = total // 2
        for excess in partitions(total):
            z = len(excess)
            f = 43 - z
            lower = (19 - z) * total + sum(d * d for d in excess)
            slope = total - threshold + 1
            high = (lower - f * (threshold - 1) + slope - 1) // slope
            if high < 5:
                raise ValueError('insufficient qualifying vertices')
            incidence.append({'total_excess': total, 'positive_excesses': list(excess),
                              'normal_vertices': f, 'qualifying_threshold': threshold,
                              'weighted_incidence_lower': lower,
                              'qualifying_count_lower': high})
    return {'status': 'CERTIFIED_GLOBAL_GOOD43_EDGE_WINDOW',
            'n': 43, 'edge_window': [390, 513],
            'catalog_profiles': parent['distinct_bucket_profiles'],
            'rooted_catalog_records': parent['root_count'],
            'profile_pairs': sum(totals),
            'rejected_by_first_then_second': totals,
            'maximum_allowed_common_excess': 2,
            'buckets': buckets, 'irregular_profiles': incidence,
            'new_irregular_degree_multisets_per_color': len(incidence),
            'regular_zero_excess_case': 'all 43 vertices qualify',
            'target_found': False, 'q10_children_decided': 0,
            'whole_packing_tasks_decided': 0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = produce()
    encoded = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded, end='')
