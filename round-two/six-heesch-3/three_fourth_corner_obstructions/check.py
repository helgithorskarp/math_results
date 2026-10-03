#!/usr/bin/env python3
"""Exact compact original-corner chains for three literal T7 fourths.

Author six-heesch-3, researcher. The two-copy theorem is an explicit
written-proof dependency. Shared polygon primitives are not an
independent geometry audit or a proof-assistant formalization.
"""
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from functools import lru_cache
import json
from pathlib import Path
import resource
import time

import corner as c
import field as q
import geometry as g

HERE = Path(__file__).resolve().parent
KEYS = (
    '2cf5c6d72d9a4c897418ebd0f945aad00290d5f76e59ced42a6d3a9b3a68a673',
    '3b9c0692a9618002fb65ca9f777e51dcec02f472ede3b692317ccfbb6ad1093f',
    'a0adcdcf717a5b2afc42f4322691090c0c6195514fca0693dcac18c7f7bb9584',
)
DEPENDENCY = {
    'graph_ref': c.PAIR_REF,
    'source_commit': '0bc5ae35b48015e64ac07d9ae25e0ba85d26ed7f',
    'proof_sha256': 'ae8dc5a6c9ebe3e0ee8ae933b9ac648fafa43ab2e92cd0b4682e5490ef2309e6',
}


def pose_read(row):
    g.require(isinstance(row, list) and len(row) == 4 and
              type(row[0]) is int and row[0] in range(12) and
              type(row[1]) is int and row[1] in (0, 1), 'malformed pose')
    g.require(all(isinstance(v, list) and len(v) == 2 and
                  all(isinstance(x, str) for x in v) for v in row[2:]),
              'malformed exact translation')
    p = row[0], row[1], q.Q3(Fraction(row[2][0]), Fraction(row[2][1])), q.Q3(Fraction(row[3][0]), Fraction(row[3][1]))
    g.require(q.pose_serial(p) == row, 'noncanonical exact pose')
    return p


@lru_cache(None)
def original_stars(rows):
    atoms = tuple(atom for row in rows for atom in g.shape(7, row[:4])[0])
    result = {}
    for v in c.vertices(atoms):
        gap = 12-v['angle']
        if gap in (2, 3, 4, 5, 7):
            star = {'point': list(v['point']), 'gap': gap, 'start': v['end']}
            g.require(tuple(v['point']) not in result, 'repeated original corner')
            result[tuple(v['point'])] = star
    return result


def validate_star(spec, stars):
    g.require(isinstance(spec.get('point'), list) and len(spec['point']) == 2 and
              all(type(x) is int for x in spec['point']), 'bad original point')
    actual = stars.get(tuple(spec['point']))
    g.require(actual is not None and {k: spec.get(k) for k in actual} == actual,
              'certificate requests a nonoriginal or incorrect boundary gap')
    g.require(type(spec.get('unit')) is int and spec['unit'] in range(actual['gap']),
              'invalid angular unit')
    return actual


@lru_cache(None)
def overlap(p, owner):
    return c.overlap(p, owner)


def admissible(p, owners, futures):
    g.require(type(futures) is int and futures in (1, 2), 'bad future-stage license')
    # An actual S1 supplier and every owner are retained in K+S1.
    # TWO surrounds, not one, license asking S2 to cover this pair.
    pair = c.pair_occurrence(p, owners) if futures == 2 else None
    if pair is not None:
        return {'kind': 'pair_needs_second_surround', 'pair': pair}
    for i, owner in enumerate(owners):
        if p != owner and overlap(p, owner):
            return {'kind': 'interior_overlap', 'owner_index': i}
    return None


def unit_record(prototype, star, unit, owners, futures):
    entries = []
    for pose, mask in c.unit_domain(prototype, star, unit):
        g.require(mask & (1 << unit), 'supplier does not occupy the requested unit')
        entries.append({'pose': q.pose_serial(pose), 'angular_mask': mask,
                        'exclusion': admissible(pose, owners, futures)})
    return {'star': star, 'unit': unit, 'owner_count': len(owners),
            'future_surrounds_assumed': futures, 'entries': entries,
            'survivors': [r['pose'] for r in entries if r['exclusion'] is None]}


def stage_header(certificate):
    g.require(certificate['schema'] == 1 and certificate['tile_hexagons'] == 7 and
              certificate['future_surrounds_excluded'] == 2 and
              certificate['only_original_corners'] is True and
              certificate['new_forced_corners_required_in_same_stage'] is False and
              certificate['uncovered_final_layer_pruning_licensed'] is False and
              certificate['pair_dependency'] == DEPENDENCY,
              'wrong stage, original-corner scope or pair dependency')
    g.require([r['prefix_key'] for r in certificate['cases']] == list(KEYS),
              'wrong literal case set or order')


def replay_case(spec, fixture, prototype, futures=2):
    g.require(futures == 2, 'these chains require two future surrounds')
    data = c.unpack(fixture)
    g.require(c.prefix_key(data) == fixture['prefix_key'] == spec['prefix_key'] and
              spec['fixed_depth'] == 4 and fixture['level_counts'] in
              ([1, 6, 10, 21, 36], [1, 6, 10, 21, 37]) and
              len(data['copies']) == spec['old_copy_count'], 'wrong retained literal fourth')
    stars = original_stars(tuple(tuple(row) for row in fixture['rows']))
    owners = [q.int_pose(tuple(r['pose'])) for r in data['copies']]
    g.require(all(c.pair_occurrence(p, owners) is None for p in owners),
              'old pair already obstructs the next surround')
    records = []
    for force in spec['forces']:
        star = validate_star(force, stars)
        record = unit_record(prototype, star, force['unit'], owners, futures)
        pose = pose_read(force['forced_pose'])
        g.require(record['survivors'] == [force['forced_pose']] and pose not in owners,
                  'claimed angular-unit force is not a unique new actual copy')
        records.append(record)
        owners.append(pose)
    final = spec['final']
    star = validate_star(final, stars)
    record = unit_record(prototype, star, final['unit'], owners, futures)
    g.require(not record['survivors'], 'final original angular unit still has a supplier')
    records.append(record)
    return {'label': spec['label'], 'prefix_key': spec['prefix_key'],
            'forced_count': len(spec['forces']), 'final_original_point': final['point'],
            'final_zero_unit': final['unit'], 'records': records,
            'stable_chain_sha256': c.digest(records), 'complete_no_two_futures': True}


def controls(fixtures, prototype, cases, certificate):
    positives = []
    for name in ('basic_T6', 'pending_T7_five'):
        data = c.unpack(fixtures[name])
        result = g.check(data)
        for key in ('elapsed_seconds', 'peak_rss_kib'): result.pop(key)
        positives.append(result)
    g.require([r['verified_coronas'] for r in positives] == [6, 5], 'positive lower changed')
    # Recompute every eligible ORIGINAL corner of the actual R96 fourth,
    # using ONE surround. Every actual level-five supplier remains legal
    # and the actual fifth covers every open30-degree unit.
    full = c.unpack(fixtures['pending_T7_five'])
    old = [r for r in full['copies'] if r['level'] <= 4]
    rows = tuple(tuple(r['pose']+[r['level']]) for r in old)
    owners = [q.int_pose(tuple(r['pose'])) for r in old]
    actual = {q.int_pose(tuple(r['pose'])) for r in full['copies'] if r['level'] == 5}
    positive_units = []
    for point, star in sorted(original_stars(rows).items()):
        for unit in range(star['gap']):
            domain = c.unit_domain(prototype, star, unit)
            required = [p for p, mask in domain if p in actual and mask & (1 << unit)]
            g.require(required and all(admissible(p, owners, 1) is None for p in required),
                      'one-surround reader excluded or missed an actual fifth supplier')
            positive_units.append([list(point), unit, [q.pose_serial(p) for p in required]])
    pair_final = next((c.pair_occurrence(p, tuple(actual)) for p in actual
                       if c.pair_occurrence(p, tuple(actual)) is not None), None)
    g.require(pair_final is not None, 'actual uncovered fifth should contain an admissible final pair')
    # Same-copy equality must not be converted into an interior conflict.
    p = q.int_pose((0, 0, 0, 0))
    g.require(overlap(p, p) and admissible(p, [p], 1) is None and
              admissible(p, [p], 2) is None, 'same-copy control rejected')
    odd = sum(r['pose'][0] % 2 for case in cases for record in case['records'] for r in record['entries'])
    g.require(odd > 0, 'odd30-degree suppliers were lost')
    damaged = []

    def reject(name, fn):
        try: fn()
        except (ValueError, KeyError, TypeError, ZeroDivisionError): damaged.append(name)
        else: raise ValueError('damaged certificate accepted: '+name)

    for name, key, value in (
        ('one_surround_stage', 'future_surrounds_excluded', 1),
        ('uncovered_final_layer', 'uncovered_final_layer_pruning_licensed', True),
        ('new_force_same_stage_corners', 'new_forced_corners_required_in_same_stage', True),
        ('missing_original_corner_condition', 'only_original_corners', False),
        ('changed_pair_dependency', 'pair_dependency', {}),
    ):
        bad = deepcopy(certificate); bad[key] = value
        reject(name, lambda bad=bad: stage_header(bad))
    s = certificate['cases'][0]; f = fixtures['fourths'][0]
    reject('chain_requested_with_one_future', lambda: replay_case(s, f, prototype, 1))
    mutations = (
        ('moved_original_point', lambda x: x['forces'][0]['point'].__setitem__(0, 25)),
        ('wrong_gap', lambda x: x['forces'][0].__setitem__('gap', 4)),
        ('wrong_start_ray', lambda x: x['forces'][0].__setitem__('start', 4)),
        ('unit_outside_gap', lambda x: x['forces'][0].__setitem__('unit', 5)),
        ('wrong_forced_pose', lambda x: x['forces'][0]['forced_pose'][2].__setitem__(0, '-33')),
        ('missing_required_force', lambda x: x['forces'].pop(0)),
        ('repeated_force', lambda x: x['forces'].insert(1, deepcopy(x['forces'][0]))),
        ('noncanonical_pose', lambda x: x['forces'][0]['forced_pose'][2].__setitem__(0, '-64/2')),
        ('moved_final_point', lambda x: x['final']['point'].__setitem__(0, 65)),
        ('wrong_retained_key', lambda x: x.__setitem__('prefix_key', '0'*64)),
    )
    for name, mutate in mutations:
        bad = deepcopy(s); mutate(bad)
        reject(name, lambda bad=bad: replay_case(bad, f, prototype))
    bad_fixture = deepcopy(f); bad_fixture['rows'][0][2] += 1
    reject('changed_retained_copy', lambda: replay_case(s, bad_fixture, prototype))
    return {'positive_geometry': positives, 'one_future_positive_original_units': len(positive_units),
            'one_future_positive_units_sha256': c.digest(positive_units),
            'actual_final_pair_admitted_without_later_surround': True,
            'same_copy_admitted': True, 'odd30_supplier_occurrences_retained': odd,
            'damaged_certificates_rejected': damaged}


def run(certificate, fixtures):
    stage_header(certificate)
    g.require([f['prefix_key'] for f in fixtures['fourths']] == list(KEYS), 'wrong fixture set')
    prototype = c.vertices(g.atoms(7))
    g.require(dict(Counter(v['angle'] for v in prototype)) ==
              {2: 7, 3: 1, 4: 15, 5: 1, 6: 1, 8: 13, 10: 6}, 'prototype angle atlas differs')
    g.require(len(c.words(7)) == 7 and all(6 not in word for word in c.words(7)),
              '210-degree edge exclusion or finite fan words differ')
    cases = []
    for spec, fixture in zip(certificate['cases'], fixtures['fourths']):
        geometry = g.check(c.unpack(fixture))
        for key in ('elapsed_seconds', 'peak_rss_kib'): geometry.pop(key)
        g.require(geometry['verified_coronas'] == 4, 'literal fourth lower failed')
        case = replay_case(spec, fixture, prototype)
        case['geometry'] = geometry
        cases.append(case)
    g.require([r['forced_count'] for r in cases] == [10, 4, 10], 'chain lengths differ')
    result = {'agent': 'six-heesch-3', 'role': 'researcher', 'status': 'three complete fixed-prefix no-two-future certificates',
              'cases': cases, 'controls': controls(fixtures, prototype, cases, certificate),
              'pair_dependency': DEPENDENCY, 'grid_or_mate_premise': False,
              'arbitrary_added_motions_allowed': True, 'final_holes_allowed': True,
              'all_forcing_corners_belong_to_original_prefix': True,
              'global_Heesch_upper_claimed': False, 'finite_seven_target_solved': False,
              'shared_polygon_primitives': True, 'independently_reviewed': False, 'formalized': False}
    result['stable_evidence_sha256'] = c.digest(result)
    return result


def compact(result):
    out = deepcopy(result)
    for case in out['cases']:
        records = case.pop('records')
        case['unit_domain_counts'] = [len(r['entries']) for r in records]
        case['unit_survivor_counts'] = [len(r['survivors']) for r in records]
        case['pair_exclusion_counts'] = [sum(e['exclusion'] is not None and
            e['exclusion']['kind'] == 'pair_needs_second_surround' for e in r['entries']) for r in records]
        case['exact_forced_poses'] = [r['survivors'][0] for r in records[:-1]]
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', help='optional new full local evidence file')
    parser.add_argument('--write-expected', action='store_true', help='maintainer: generate a new expected.json')
    args = parser.parse_args()
    started = time.monotonic()
    certificate = json.loads((HERE/'certificate.json').read_text())
    fixtures = json.loads((HERE/'fixtures.json').read_text())
    result = run(certificate, fixtures)
    expected = compact(result)
    if args.write_expected:
        g.require(not (HERE/'expected.json').exists(), 'refuse overwrite expected evidence')
        (HERE/'expected.json').write_text(json.dumps(expected, indent=2)+'\n')
    else:
        g.require(expected == json.loads((HERE/'expected.json').read_text()), 'full compact evidence differs')
    if args.out:
        path = Path(args.out); g.require(not path.exists(), 'refuse overwrite full evidence')
        path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(expected, indent=2))
    import sys
    print(json.dumps({'elapsed_seconds': time.monotonic()-started,
                      'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}), file=sys.stderr)
