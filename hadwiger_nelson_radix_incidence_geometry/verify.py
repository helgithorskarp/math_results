#!/usr/bin/env python3
"""Independent enumeration by pairs of separately normalized disjoint rows."""
import argparse
from collections import Counter, defaultdict
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'hadwiger_nelson_radix_four_active_closure' / 'verify.py'
SPEC = importlib.util.spec_from_file_location('direct_pair_inventory', SOURCE)
V = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def need(ok, message):
    if not ok:
        raise ValueError(message)


def compute(export=None):
    # This imported inventory enumerates actual unordered label pairs and
    # expands norms independently of the producer's geometry implementation.
    factors, circle, data, base = V.inventory()
    row_ids = {row: cid for cid, (row, edges) in data.items()}
    monomials = [V.canonical(tuple((1, 0) if k == j else (0, 0) for k in range(5))) for j in range(5)]
    rows = sorted(list(row_ids) + monomials)
    support = {r: sum(1 << j for j, d in enumerate(r) if d != (0, 0)) for r in rows}
    need(len(rows) == 2801 and len(base) == 243, 'full pair inventory')

    def cid(row):
        row = V.canonical(row)
        return row_ids[row] if row in row_ids else (None if support[row] == 1 else circle)

    pencils, forbidden = set(), set()

    def exclude(cs):
        if circle not in cs:
            q = tuple(sorted(c for c in set(cs) if c is not None))
            need(len(q) >= 2, 'nontrivial excluded event set')
            forbidden.add(q)

    for p, q in combinations(rows, 2):
        if support[p] & support[q]:
            continue
        members = []
        for unit in V.UNITS:
            scaled = [V.times(unit, d) for d in q]
            row = tuple((a[0] + b[0], a[1] + b[1]) for a, b in zip(p, scaled))
            members.append(cid(row))
        need(len(set(members)) == 6 and circle not in members and None not in members, 'six noncircle norm events')
        key = tuple(sorted(members))
        need(key not in pencils, 'unique disjoint-row pair for each pencil')
        pencils.add(key)
        endpoints = [cid(p), cid(q)]
        for triple in combinations(members, 3):
            exclude(triple)
        for member in members:
            exclude(endpoints + [member])
        for i, j in combinations(range(6), 2):
            a, b = V.UNITS[i]
            c, d = V.UNITS[j]
            separation = (a - c) ** 2 + (a - c) * (b - d) + (b - d) ** 2
            need(separation in (1, 3, 4), 'hexagonal separation')
            if separation == 3:
                # The forced ratio is minus the sum of these units, also a unit.
                x, y = a + c, b + d
                need(x * x + x * y + y * y == 1, 'forced collision ratio is a unit')
            if separation != 1:
                for endpoint in endpoints:
                    exclude([endpoint, members[i], members[j]])

    for a, b, c in combinations(V.UNITS, 3):
        determinant = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        need(determinant != 0, 'three distinct phase centres are not collinear')

    # Normalize by the tail, rather than the whole row, and check each of the
    # seven possible constant offsets occurs at most once in a bundle.
    bundles = defaultdict(dict)
    for row, index in row_ids.items():
        tail = V.canonical(row[1:])
        scales = [u for u in V.UNITS if tuple(V.times(u, d) for d in row[1:]) == tail]
        need(len(scales) == 1, 'unique tail normalization')
        constant = V.times(scales[0], row[0])
        need(constant not in bundles[tail] and constant in ((0, 0),) + V.UNITS, 'distinct constant offsets')
        bundles[tail][constant] = index
    offset_pairs = sorted({tuple(sorted(pair)) for group in bundles.values() for pair in combinations(group.values(), 2)})
    pencil_keys, forbidden = sorted(pencils), sorted(forbidden)
    combined = sorted(set(forbidden) | set(offset_pairs))
    interface = {
        'schema': 'hn-radix-incidence-geometry-v1',
        'curve_inventory_sha256': digest(factors), 'circle_id': circle,
        'injectivity_excluded_sets': forbidden,
        'monic_degree_four_excluded_pairs': offset_pairs,
        'six_event_phase_pencils': pencil_keys,
        'scope': 'All fields use original h4105 curve IDs. The first list forces label collision; the second forces a monic Eisenstein relation of degree at most four. Either excludes a non-four-colourable physical A5 member. Higher active incidence does not evade these exclusions.',
    }
    if export is not None:
        with Path(export).open('x') as f:
            json.dump(interface, f, sort_keys=True, separators=(',', ':'))
            f.write('\n')
    return {
        'schema': 'hn-radix-incidence-geometry-certificate-v1',
        'active_curves': len(factors), 'circle_id': circle,
        'curve_inventory_sha256': digest(factors),
        'phase_pencils': len(pencils), 'phase_pencils_sha256': digest(pencil_keys),
        'injectivity_excluded_sets': len(forbidden),
        'injectivity_excluded_arity_histogram': {str(k): v for k, v in sorted(Counter(map(len, forbidden)).items())},
        'injectivity_excluded_sets_sha256': digest(forbidden),
        'constant_offset_bundles': len(bundles),
        'constant_offset_bundle_size_histogram': {str(k): v for k, v in sorted(Counter(map(len, bundles.values())).items())},
        'monic_degree_four_excluded_pairs': len(offset_pairs),
        'monic_degree_four_excluded_pairs_sha256': digest(offset_pairs),
        'combined_nonfour_excluded_sets': len(combined),
        'combined_nonfour_excluded_sets_sha256': digest(combined),
        'interface_sha256': digest(interface),
        'proof_solver_calls': 0, 'proof_CAS_calls': 0,
        'eight_active_gate_closed': False, 'record_improvement': False,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    parser.add_argument('--export-interface', type=Path)
    args = parser.parse_args()
    result = compute(args.export_interface)
    need(result == json.loads(args.certificate.read_text()), 'full certificate and entrywise set hashes')
    print(json.dumps(result, indent=2, sort_keys=True))
