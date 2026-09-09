#!/usr/bin/env python3
"""Exact disjoint-support phase pencils and constant-offset exclusions."""
import argparse
from collections import Counter, defaultdict
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'hadwiger_nelson_complex_radix_architecture'))
import geometry as G


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def inventory():
    all_rows, _ = G.inventory()
    circle = G.primitive({(2, 0): 1, (0, 2): 3, (0, 0): -1})
    events = {G.distance_event(r): r for r in all_rows if sum(d != (0, 0) for d in r) >= 2}
    factors = sorted(list(events) + [circle])
    rows = {i: events[f] for i, f in enumerate(factors) if f != circle}
    if len(rows) != 2796 or len(set(rows.values())) != 2796:
        raise ValueError('noncircle event inventory')
    return factors, factors.index(circle), rows


def compute(export=None):
    factors, circle, rows = inventory()
    ids = {r: c for c, r in rows.items()}
    pencils, exclusions = {}, set()

    def curve(r):
        support = [j for j, d in enumerate(r) if d != (0, 0)]
        if len(support) == 1:
            return None if support[0] == 0 else circle
        return ids[G.canon(r)]

    def exclude(cs):
        if circle in cs:
            return
        support = tuple(sorted({c for c in cs if c is not None}))
        if len(support) < 2:
            raise ValueError('degenerate exclusion')
        exclusions.add(support)

    for row in rows.values():
        support = [j for j, d in enumerate(row) if d != (0, 0)]
        for bits in product((0, 1), repeat=len(support) - 1):
            bpart = {j for j, bit in zip(support[1:], bits) if bit}
            if not bpart:
                continue
            p = tuple((0, 0) if j in bpart else d for j, d in enumerate(row))
            q = tuple(d if j in bpart else (0, 0) for j, d in enumerate(row))
            members = tuple(curve(tuple(G.emul(u, d) if j in bpart else d for j, d in enumerate(row))) for u in G.U)
            key = tuple(sorted(members))
            if key in pencils:
                continue
            if len(set(members)) != 6:
                raise ValueError('six distinct phase events')
            endpoints = [curve(p), curve(q)]
            pencils[key] = [p, q, members, endpoints]
            for triple in combinations(members, 3):
                exclude(triple)
            for member in members:
                exclude(endpoints + [member])
            for i, j in combinations(range(6), 2):
                a, b = G.U[i][0] - G.U[j][0], G.U[i][1] - G.U[j][1]
                if a * a + a * b + b * b == 1:
                    continue
                for endpoint in endpoints:
                    exclude([endpoint, members[i], members[j]])

    bundles = defaultdict(list)
    for cid, row in rows.items():
        bundles[G.canon(row[1:])].append(cid)
    offset_pairs = sorted({tuple(sorted(pair)) for group in bundles.values() for pair in combinations(group, 2)})
    pencil_keys = sorted(pencils)
    forbidden = sorted(exclusions)
    combined = sorted(exclusions | set(offset_pairs))
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
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--export-interface', type=Path)
    args = parser.parse_args()
    result = compute(args.export_interface)
    with args.out.open('x') as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write('\n')
    print(json.dumps(result, indent=2, sort_keys=True))
