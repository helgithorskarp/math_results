#!/usr/bin/env python3
"""Check the complete enumeration, six finite orbits, and integer duals."""
import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from classify import (column_permutations, cycle_neighbors, enumerate_all,
                      move, require)


def check_design(rows, parts):
    require(len(rows) == len(set(rows)) == 12, 'need twelve distinct rows')
    require(all(type(r) is int and 0 <= r < 4096 and r.bit_count() == 5
                for r in rows), 'bad row mask')
    columns = [sum(1 << i for i, r in enumerate(rows) if r >> j & 1)
               for j in range(12)]
    require(all(c.bit_count() == 5 for c in columns), 'bad point degree')
    require(all((a & b).bit_count() in (1, 2)
                for a, b in combinations(rows, 2)), 'bad row intersection')
    neighbors = cycle_neighbors(parts)
    require(all((columns[i] & columns[j]).bit_count() ==
                (1 if j in neighbors[i] else 2)
                for i in range(12) for j in range(i)), 'wrong column cycle graph')


def check_dual(record):
    rows = record['rows']
    capacity = record['capacity']
    require(type(capacity) is int and capacity > 0, 'bad capacity')
    pairs = record['weights']
    require(len({t for t, _ in pairs}) == len(pairs), 'duplicate triple')
    for triple, weight in pairs:
        require(type(triple) is int and 0 <= triple < 4096
                and triple.bit_count() == 3, 'bad triple mask')
        require(type(weight) is int and weight > 0, 'bad weight')
        require(not any(triple & row == triple for row in rows),
                'weight assigned to an already covered triple')
    loads = []
    for block in combinations(range(12), 6):
        mask = sum(1 << j for j in block)
        loads.append(sum(w for t, w in pairs if t & mask == t))
    require(max(loads) <= capacity, 'a six-set exceeds the capacity')
    total = sum(w for _, w in pairs)
    require(total > 8 * capacity, 'dual does not exclude eight blocks')
    return dict(case=record['case'], total_weight=total, capacity=capacity,
                maximum_load=max(loads), positive_triples=len(pairs),
                lower_bound=(total + capacity - 1) // capacity)


def rejection_controls(record):
    bad = deepcopy(record)
    bad['capacity'] = 1
    try:
        check_dual(bad)
    except ValueError:
        pass
    else:
        raise ValueError('overweight certificate accepted')
    bad = deepcopy(record)
    block = record['rows'][0]
    covered = next(sum(1 << j for j in t) for t in combinations(range(12), 3)
                   if sum(1 << j for j in t) & block == sum(1 << j for j in t))
    bad['weights'][0][0] = covered
    try:
        check_dual(bad)
    except ValueError:
        pass
    else:
        raise ValueError('covered-triple weight accepted')
    return 2


def verify(path):
    raw = path.read_bytes()
    certificate = json.loads(raw)
    require(certificate['schema'] == 1, 'unsupported certificate schema')
    cases = certificate['cases']
    require(len(cases) == len({r['case'] for r in cases}) == 6, 'case list')
    classification, normalized = enumerate_all()
    class_report, dual_report = [], []
    controls = 0
    for parts, targets in normalized.items():
        relevant = [r for r in cases if tuple(r['parts']) == parts]
        orbits = set()
        sizes = []
        coverage = []
        for record in relevant:
            check_design(record['rows'], parts)
            orbit = {move(record['rows'], p, sort_rows=True)
                     for p in column_permutations(parts, exchange_components=True)}
            require(not (orbits & orbit), 'two representatives are isomorphic')
            orbits |= orbit
            sizes.append(len(orbit))
            coverage.append(len(targets & orbit))
            dual_report.append(check_dual(record))
            controls += rejection_controls(record)
        require(targets <= orbits, 'unrepresented normalized matrix')
        require(bool(targets) == bool(relevant), 'extraneous or missing class')
        class_report.append(dict(parts=parts, classes=len(relevant),
                                 orbit_sizes=sizes, normalized_coverage=coverage,
                                 normalized_count=len(targets)))
    require(sum(r['classes'] for r in class_report) == 6, 'unvisited case')
    return dict(status='VERIFIED_SIX_CLASSES_AND_EIGHT_BLOCK_EXCLUSION',
                certificate_sha256=sha256(raw).hexdigest(),
                spectral_and_enumeration=classification,
                isomorphism_classes=class_report, dual_certificates=dual_report,
                rejection_controls=controls,
                proof_scope='At least nine residual six-sets; no upper bound claimed.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path,
                        default=Path(__file__).with_name('certificate.json'))
    args = parser.parse_args()
    print(json.dumps(verify(args.certificate), indent=2, sort_keys=True))
