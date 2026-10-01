"""Check the complete deterministic twelve-shape certificate."""
import argparse
import json
from math import gcd
from pathlib import Path
import bounds as B


def check(c):
    B.require(c['agent'] == 'six-covering-1' and c['role'] == 'researcher', 'wrong authorship')
    B.require(c['period'] == 720 and c['original_labels'] == B.LABELS and
              c['fixed'] == {'8': 5, '9': 6}, 'wrong normalization or original labels')
    raw = sum(720 // m for m in B.LABELS)
    present, loss = {8}, 0
    anchors = [(9, 8), (16, 9), (10, 9), (15, 8), (20, 9), (40, 9), (80, 9)]
    B.require(c['forced_anchor_pairs'] == [list(p) for p in anchors], 'wrong anchor order')
    for m, anchor in anchors:
        B.require(m not in present and anchor in present and gcd(m, anchor) == 1,
                  'invalid sequential forced overlap')
        loss += 720 // (m * anchor)
        present.add(m)
    hole_lower = 720 - raw + loss
    B.require((raw, loss, hole_lower) == (c['raw_mass'], c['forced_overlap'],
                                        c['hole_lower_bound']) == (654, 36, 102),
              'wrong first-stage union bound')
    envelopes = {}
    for e in c['envelope_cases']:
        rep = tuple(e['representative'])
        B.require(rep not in envelopes, 'duplicate envelope representative')
        R, _ = B.residual(*rep)
        value = B.count_envelope(R)
        B.require(value == {k: e[k] for k in ('odd_demand', 'even_demand', 'even_upper')},
                  'count envelope differs from certificate')
        B.require(value['even_upper'] is None or value['even_upper'] < value['even_demand'],
                  'count envelope does not exclude')
        envelopes[rep] = value
    seen, rows = set(), []
    counts = {'hole_count': 0, 'singleton_budget': 0, 'pair_budget': 0, 'count_envelope': 0}
    scalar_combinations = 0
    for row in c['excluded_shapes']:
        shape = row['a18'], row['c6']
        B.require(shape not in seen, 'duplicate target case')
        seen.add(shape)
        R, allowed = B.residual(*shape)
        reason = row['reason']
        if reason == 'hole_count':
            B.require(allowed.bit_count() == row['allowed_holes'] < hole_lower,
                      'hole-count certificate does not exclude')
            counts['hole_count'] += 1
            detail = {'allowed_holes': allowed.bit_count()}
        elif reason == 'scalar_budget':
            p = row['partition_id']
            B.require(type(p) is int and 0 <= p < len(c['resource_partitions']), 'invalid partition ID')
            groups = c['resource_partitions'][p]
            D, C, caps, combinations = B.scalar_budget(R, groups, *row['weights'])
            B.require((D, C) == (row['demand'], row['capacity']) and C < D,
                      'scalar partition budget does not exclude')
            key = 'pair_budget' if any(len(g) == 2 for g in groups) else 'singleton_budget'
            counts[key] += 1
            scalar_combinations += combinations
            detail = {'weights': row['weights'], 'demand': D, 'capacity': C,
                      'group_capacities': caps}
        elif reason == 'count_envelope':
            rep, (u, t) = tuple(row['representative']), row['affine_map']
            B.require(rep in envelopes and B.valid_affine(u, t) and
                      ((u * rep[0] + t) % 18, (u * rep[1] + t) % 6) == shape,
                      'invalid affine transfer of a strict envelope')
            counts['count_envelope'] += 1
            detail = {'representative': list(rep), 'affine_map': [u, t]}
        else:
            raise RuntimeError('unknown exclusion reason')
        rows.append({'shape': list(shape), 'reason': reason, **detail})
    remaining = [tuple(s) for s in c['remaining_shapes']]
    B.require(len(remaining) == len(set(remaining)) == 12, 'wrong remaining shape count')
    B.require(not seen.intersection(remaining) and seen.union(remaining) ==
              {(a, c) for a in range(18) for c in range(6)}, 'incomplete108-case partition')
    B.require(counts == {'hole_count': 32, 'singleton_budget': 20, 'pair_budget': 32,
                         'count_envelope': 12}, 'wrong exclusion counts')
    maps = B.affine_maps()
    covered_orbits = set()
    for orbit in c['remaining_orbits']:
        a, c6 = orbit['representative']
        actual = {((u * a + t) % 18, (u * c6 + t) % 6) for u, t in maps}
        supplied = {tuple(s) for s in orbit['members']}
        B.require(actual == supplied and actual.isdisjoint(covered_orbits), 'remaining orbit is incorrect')
        covered_orbits.update(actual)
    B.require(covered_orbits == set(remaining) and len(c['remaining_orbits']) == 6,
              'remaining twelve shapes do not make six orbits')
    return {'agent': 'six-covering-1', 'role': 'researcher', 'status': 'CHECKED',
            'period': 720, 'original_labels': B.LABELS, 'hole_lower': hole_lower,
            'excluded_counts': counts, 'excluded_shape_evidence': rows,
            'scalar_original_phase_combinations': scalar_combinations,
            'strict_envelopes': [{'representative': list(rep), **e} for rep, e in envelopes.items()],
            'remaining_shapes': c['remaining_shapes'], 'remaining_orbits': c['remaining_orbits'],
            'remaining_shapes_claimed_feasible': False, 'solver_status_used': False,
            'global_numerical_bound_changed': False}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--certificate', type=Path, default=Path(__file__).with_name('certificate.json'))
    ap.add_argument('--expected', type=Path)
    args = ap.parse_args()
    evidence = check(json.loads(args.certificate.read_text()))
    if args.expected:
        B.require(evidence == json.loads(args.expected.read_text()), 'complete frozen evidence mismatch')
    print(json.dumps(evidence, sort_keys=True))
