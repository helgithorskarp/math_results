#!/usr/bin/env python3
"""Verify complete enumeration, integer duals, and exact upper witnesses."""

import hashlib
import json
from itertools import combinations
from pathlib import Path

from classify import incidence, types

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    certificate_bytes = (ROOT / 'certificate.json').read_bytes()
    records = json.loads(certificate_bytes)
    labelled, classes = types()
    require(len(labelled) == len(set(labelled)), 'duplicate labelled vector')
    require(len(records) == len(classes), 'certificate census mismatch')
    five_sets = tuple(map(frozenset, combinations(range(11), 5)))
    summary = []
    for index, (record, (key, orbit_size)) in enumerate(zip(records, classes)):
        require(tuple(record['edges']) == key, f'class {index}: wrong representative')
        columns, rows = incidence(key)
        require(len(columns) == 11, 'wrong number of points')
        require(sorted(c.bit_count() for c in columns) == [1, 1] + [2] * 9,
                'wrong column degrees')
        require(all(r.bit_count() == 4 for r in rows), 'wrong row size')
        weights = {}
        for u, v, weight in record['weights']:
            require(type(u) is int and type(v) is int and 0 <= u < v < 11,
                    'invalid pair')
            require(type(weight) is int and weight > 0, 'invalid integer weight')
            require((u, v) not in weights, 'duplicate weighted pair')
            require(columns[u] & columns[v] == 0, 'weight on an already covered pair')
            weights[u, v] = weight
        total = sum(weights.values())
        capacity = max(sum(weight for (u, v), weight in weights.items()
                           if u in block and v in block) for block in five_sets)
        require(total == record['total'] and capacity == record['capacity'],
                'incorrect recorded weight or capacity')
        require(total > 4 * capacity, f'class {index}: insufficient dual gap')
        summary.append(dict(index=index, orbit_size=orbit_size,
                            total=total, capacity=capacity, gap=total - 4 * capacity))

    sharp = json.loads((ROOT / 'sharp_link.json').read_text())
    blocks = [frozenset(block) for block in sharp['blocks']]
    h = sharp['distinguished_point']
    require(len(blocks) == len(set(blocks)) == 9, 'invalid sharp-link block count')
    require(all(len(b) == 5 and b <= set(range(12)) for b in blocks),
            'invalid sharp-link block')
    require(all(any(set(pair) <= b for b in blocks)
                for pair in combinations(range(12), 2)), 'sharp link misses a pair')
    require(sum(h in b for b in blocks) == 5, 'distinguished degree is not five')
    codegrees = sorted(sum(h in b and q in b for b in blocks)
                       for q in range(12) if q != h)
    require(codegrees == [1] * 3 + [2] * 7 + [3], 'sharp codegrees differ')

    links = json.loads((ROOT / 'six_links.json').read_text())
    completion_summary = []
    for record in links['classes']:
        a = record['rows']
        require(len(a) == len(set(a)) == 12, 'invalid through-family size')
        require(all(type(r) is int and 0 <= r < 4096 and r.bit_count() == 5 for r in a),
                'invalid through row')
        require(all(sum(r >> q & 1 for r in a) == 5 for q in range(12)),
                'through family is not five-regular')
        require(all(1 <= sum(r & pair == pair for r in a) <= 2
                    for pair in (sum(1 << q for q in p)
                                 for p in combinations(range(12), 2))),
                'through pair multiplicity is outside one or two')
        require(all((r & s).bit_count() <= 2 for r, s in combinations(a, 2)),
                'through row intersection exceeds two')
        out = dict(label=record['label'], residual_lower_bound=10)
        if 'completion' in record:
            b = record['completion']
            require(len(b) == len(set(b)) and len(b) in (10, 11), 'wrong completion size')
            require(all(type(r) is int and 0 <= r < 4096 and r.bit_count() == 6 for r in b),
                    'invalid completion row')
            require(all(sum(r >> q & 1 for r in b) >= 5 for q in range(12)),
                    'completion violates the local lower bound')
            require(all(any(r & triple == triple for r in a + b)
                        for triple in (sum(1 << q for q in t)
                                       for t in combinations(range(12), 3))),
                    'completion misses a triple')
            out['residual_upper_bound'] = len(b)
        completion_summary.append(out)
    require(len(completion_summary) == 6, 'wrong six-link fixture census')
    result = dict(status='VERIFIED_DEGREE5_PAIR_MULTIPLICITY',
                  labelled_types=len(labelled), isomorphism_types=len(classes),
                  labelled_census_sha256=hashlib.sha256(
                      json.dumps(labelled, separators=(',', ':')).encode()).hexdigest(),
                  five_set_capacity_checks=len(five_sets) * len(classes),
                  certificate_sha256=hashlib.sha256(certificate_bytes).hexdigest(),
                  classes=summary, sharp_link_codegrees=codegrees,
                  completions=completion_summary)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
