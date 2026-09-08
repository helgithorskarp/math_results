#!/usr/bin/env python3
"""Reconstruct the new certificate from literal complete-catalog graphs.

No producer or parent implementation is imported. A Boolean matrix and an
edge-sum definition of Q replace the parent vertex-weight calculation.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / 'ramsey_r55_regular18_overlap_exclusion'
CATALOG_SHA = '83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(catalog, certificate):
    raw = Path(catalog).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == CATALOG_SHA, 'complete catalog SHA256')
    rows = raw.splitlines()
    require(len(rows) == 352366, 'complete catalog size')
    kept = []
    groups = collections.defaultdict(list)
    for row in rows:
        require(len(row) == 47 and row[0] == 87 and
                all(63 <= x <= 126 for x in row), 'graph6 syntax')
        word = ''.join(format(x - 63, '06b') for x in row[1:])
        require(len(word) == 276, 'graph6 bit length')
        if word.count('1') < 128:
            continue
        kept.append(row)
        a = [[False] * 24 for _ in range(24)]
        position = 0
        for v in range(1, 24):
            for u in range(v):
                a[u][v] = a[v][u] = word[position] == '1'
                position += 1
        degrees = [sum(r) for r in a]
        for root in range(24):
            cset = [w for w in range(24) if a[root][w]]
            ds = [sum(a[w][z] for z in cset) for w in cset]
            p = sum(degrees[w] for w in cset)
            q = 0
            for w, z in itertools.combinations(cset, 2):
                if a[w][z]:
                    require(not any(a[w][t] and a[z][t] for t in cset),
                            'common graph must be triangle-free')
                    q += degrees[w] + degrees[z] - sum(a[w][t] and a[z][t]
                                                       for t in range(24))
            groups[(len(cset), tuple(sorted(ds)))].append((p, q))
    retained = b'\n'.join(kept) + b'\n'
    require(retained == (PARENT / 'RETAINED.g6').read_bytes(), 'all dense catalog records')
    require(len(kept) == 1027, 'dense catalog count')
    old = json.loads((PARENT / 'CERTIFICATE.json').read_text())
    require(len(groups) == len(old['buckets']) == 39, 'bucket count')
    summary = []
    totals = [0, 0]
    for ((c, ds), roots), saved in zip(sorted(groups.items()), old['buckets']):
        profiles = sorted(set(roots))
        require(c == saved['common_order'] and list(ds) == saved['common_degree_sequence']
                and len(roots) == saved['root_count']
                and [list(x) for x in profiles] == saved['profiles'],
                'literal root-profile reconstruction')
        edge_count = sum(ds) // 2
        first = c * (29 - c) + sum(ds)
        second = sum(d * d for d in ds) + (40 - c) * edge_count
        counts = [0, 0]
        # Inspect the complete upper triangle; ordering is irrelevant to feasibility.
        for i in range(len(profiles)):
            for j in range(i, len(profiles)):
                pu, qu = profiles[i]
                pv, qv = profiles[j]
                first_margin = first - pu - pv
                second_margin = second - qu - qv
                if first_margin >= 3:
                    counts[0] += 1
                else:
                    require(second_margin > 2 * ds[-1], 'robustness-two failure')
                    counts[1] += 1
        totals = [x + y for x, y in zip(totals, counts)]
        summary.append({'common_order': c, 'common_degree_sequence': list(ds),
                        'profiles': len(profiles),
                        'rejected_by_first_then_second': counts})

    # Enumerate excess histograms, independently of the producer's partitions.
    incidence = []
    internal_graphs_checked = 0
    for counts in itertools.product(range(5), repeat=4):
        excess = tuple(d for d in range(1, 5) for _ in range(counts[d - 1]))
        total = sum(excess)
        if total not in (2, 4):
            continue
        z = len(excess)
        f = 43 - z
        pairs = list(itertools.combinations(range(z), 2))
        actual_minimum = None
        for mask in range(1 << len(pairs)):
            loss = sum(excess[u] + excess[v] for i, (u, v) in enumerate(pairs)
                       if mask >> i & 1)
            value = sum(d * (18 + d) for d in excess) - loss
            actual_minimum = value if actual_minimum is None else min(actual_minimum, value)
            internal_graphs_checked += 1
        k = total // 2
        high = next(h for h in range(f + 1)
                    if h * total + (f - h) * (k - 1) >= actual_minimum)
        require(high >= 5, 'global incidence contradiction')
        incidence.append({'total_excess': total, 'positive_excesses': list(excess),
                          'normal_vertices': f, 'qualifying_threshold': k,
                          'weighted_incidence_lower': actual_minimum,
                          'qualifying_count_lower': high})
    incidence.sort(key=lambda x: (x['total_excess'], x['positive_excesses']))
    expected = {'status': 'CERTIFIED_GLOBAL_GOOD43_EDGE_WINDOW',
                'n': 43, 'edge_window': [390, 513],
                'catalog_profiles': sum(len(set(v)) for v in groups.values()),
                'rooted_catalog_records': sum(map(len, groups.values())),
                'profile_pairs': sum(totals),
                'rejected_by_first_then_second': totals,
                'maximum_allowed_common_excess': 2,
                'buckets': summary, 'irregular_profiles': incidence,
                'new_irregular_degree_multisets_per_color': len(incidence),
                'regular_zero_excess_case': 'all 43 vertices qualify',
                'target_found': False, 'q10_children_decided': 0,
                'whole_packing_tasks_decided': 0}
    require(expected == json.loads(Path(certificate).read_text()), 'complete certificate comparison')
    return {'status': 'VERIFIED_GLOBAL_GOOD43_EDGE_WINDOW',
            'edge_window': [390, 513], 'catalog_graphs': len(rows),
            'retained_graphs': len(kept), 'root_profiles': expected['catalog_profiles'],
            'profile_pairs': sum(totals), 'rejected_by_first_then_second': totals,
            'irregular_profiles': len(incidence),
            'small_exception_graphs': internal_graphs_checked}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--certificate', type=Path, default=HERE / 'CERTIFICATE.json')
    args = parser.parse_args()
    print(json.dumps(verify(args.catalog, args.certificate), sort_keys=True))
