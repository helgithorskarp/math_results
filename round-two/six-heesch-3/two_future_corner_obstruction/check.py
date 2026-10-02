#!/usr/bin/env python3
"""Compact exact four-corner certificates; no lattice or prescribed mate premise."""
import argparse, json, resource, time
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

import geometry as g
import field as q

HERE = Path(__file__).resolve().parent
PAIR_REF = 'bafkreibrkjof54wz2lzqjnbmf4cy76d3g4dpz3q4ypj4hnlho3g7hmlhxm'


def digest(obj):
    return sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def unpack(fixture):
    return {'tile_hexagons': fixture['tile_hexagons'], 'level_counts': fixture['level_counts'],
            'copies': [{'pose': row[:4], 'level': row[4]} for row in fixture['rows']]}


def prefix_key(data):
    obj = {'tile_hexagons': data['tile_hexagons'],
           'copies': sorted((row['level'], tuple(row['pose'])) for row in data['copies'])}
    return digest(obj)


def direction(dx, dy):
    g.require(dx or dy, 'zero edge')
    if dy == 0: return 0 if dx > 0 else 6
    if dx == 0: return 3 if dy > 0 else 9
    if dx == 3*dy: return 1 if dx > 0 else 7
    if dx == dy: return 2 if dx > 0 else 8
    if dx == -dy: return 4 if dy > 0 else 10
    if dx == -3*dy: return 5 if dy > 0 else 11
    raise ValueError('edge outside30-degree directions')


def vertices(atoms):
    cycle, _ = g.boundary(atoms)
    rays = [direction(*g.sub(cycle[(i+1) % len(cycle)], p)) for i, p in enumerate(cycle)]
    return [{'point': p, 'start': rays[i], 'end': (rays[i-1]+6) % 12,
             'angle': 6-((rays[i]-rays[i-1]+6) % 12-6)} for i, p in enumerate(cycle)]


def words(total):
    return [()] if total == 0 else [(a,)+tail for a in (2, 3, 4, 5)
                                  if a <= total for tail in words(total-a)]


def native(p):
    a, f, x, y = p
    if a % 2 or x.b or y.b or x.a.denominator != 1 or y.a.denominator != 1:
        return None
    return a, f, int(x.a), int(y.a)


def overlap(p, c):
    a, b = native(p), native(c)
    return g.pair(7, a, b)[0] if a is not None and b is not None else q.pair(7, p, c)[0]


def original_gap(data, point, expected_gap):
    atoms = tuple(atom for row in data['copies'] for atom in g.shape(7, tuple(row['pose']))[0])
    matching = [v for v in vertices(atoms) if v['point'] == tuple(point)]
    g.require(len(matching) == 1 and 12-matching[0]['angle'] == expected_gap,
              'named point is not the stated original boundary gap')
    return {'point': tuple(point), 'gap': expected_gap, 'start': matching[0]['end']}


def unit_domain(prototype, star, unit):
    g.require(star['gap'] in (2, 5, 7) and unit in range(star['gap']), 'unproved corner domain')
    # Gap7 admits no180-degree edge: the remaining30 degrees is below
    # the minimum positive prototype angle60. Other prototype angles
    # <=210 are exactly2/3/4/5/6;6 cannot occur in a word of7.
    roles = set()
    for word in words(star['gap']):
        partial = 0
        for angle in word:
            if partial <= unit < partial+angle:
                roles.add((partial, angle))
            partial += angle
    raw = {}
    for partial, angle in sorted(roles):
        for vertex in prototype:
            if vertex['angle'] != angle:
                continue
            for reflected in (0, 1):
                wanted = (star['start']+partial) % 12
                rotation = (wanted-vertex['start'] if not reflected else wanted+vertex['end']) % 12
                pose = q.anchor(rotation, reflected, vertex['point'], star['point'])
                raw[pose] = raw.get(pose, 0) | (((1 << angle)-1) << partial)
    return sorted(raw.items(), key=lambda item: json.dumps(q.pose_serial(item[0])))


def pair_occurrence(pose, owners):
    indexed = {p: i for i, p in enumerate(owners)}
    a, f, x, y = pose
    for r in range(1, 7):
        dx, dy = q.linear(a, f, (8*r+4, -4))
        for other, role in (((a, f, x+dx, y+dy), 'A'), ((a, f, x-dx, y-dy), 'B')):
            if other not in indexed:
                continue
            common = pose if role == 'A' else other
            vx, vy = q.linear(common[0], common[1], (8*r+4, -4))
            image_b = (common[0], common[1], common[2]+vx, common[3]+vy)
            g.require({common, image_b} == {pose, other}, 'pair image differs')
            return {'m': 7, 'r': r, 'candidate_role': role, 'owner_index': indexed[other],
                    'common_isometry': q.pose_serial(common),
                    'members': {'A': q.pose_serial(common), 'B': q.pose_serial(image_b)}}
    return None


def core_check(certificate, fixtures):
    g.require(certificate['schema'] == 1 and certificate['pair_lemma_ref'] == PAIR_REF and
              certificate['future_surrounds_excluded'] == 2 and
              certificate['minimum_prototype_angle_steps'] == 2 and
              certificate['words_210'] == [list(w) for w in words(7)], 'wrong stage/angle premise')
    prototype = vertices(g.atoms(7))
    angle_counts = Counter(v['angle'] for v in prototype)
    g.require(min(angle_counts) == 2 and set(a for a in angle_counts if a <= 7) == {2, 3, 4, 5, 6},
              'prototype angle classification differs')
    full = unpack(fixtures['pending_T7_five'])
    fourth = {'tile_hexagons': 7, 'copies': [row for row in full['copies'] if row['level'] <= 4]}
    c0a = unpack(fixtures['c0a_fourth'])
    rows = []
    for name, data in (('bfe', fourth), ('c0a', c0a)):
        claimed = certificate['cases'][name]
        g.require(prefix_key(data) == claimed['prefix_key'], 'wrong exact prefix')
        base = g.check(data)
        g.require(base['verified_coronas'] == 4 and base['copies'] == 74 and
                  base['level_counts'] == [1, 6, 10, 21, 36], 'old prefix not the literal four-corona disc')
        owners = [q.int_pose(tuple(row['pose'])) for row in data['copies']]
        forced = []
        actual_steps = []
        for specification in claimed['forces']:
            g.require(specification['one_future_only'] is True, 'force uses an extra future')
            star = original_gap(data, specification['point'], specification['gap'])
            unit = specification['unit']
            entries = []
            surviving = []
            for pose, mask in unit_domain(prototype, star, unit):
                blocker = next((i for i, owner in enumerate(owners) if pose != owner and overlap(pose, owner)), None)
                entries.append([q.pose_serial(pose), mask, blocker])
                if blocker is None:
                    surviving.append(pose)
            g.require(len(surviving) == 1 and q.pose_serial(surviving[0]) == specification['pose'],
                      'claimed original angular unit is not a unique force')
            actual = {'point': list(star['point']), 'gap': star['gap'], 'start': star['start'],
                      'unit': unit, 'pose': q.pose_serial(surviving[0]), 'one_future_only': True,
                      'entries': entries}
            g.require(actual == specification, 'complete unit certificate differs entrywise')
            forced.append(surviving[0])
            owners.append(surviving[0])
            actual_steps.append(actual)
        g.require(len(forced) == 3, 'three force chain required')
        final = claimed['final_gap']
        g.require(final['two_futures_required'] is True, 'pair exclusions require a SECOND surround')
        star = original_gap(data, final['point'], final['gap'])
        g.require(star['gap'] == 2, 'final domain must be a complete60-degree gap')
        entries = []
        for pose, mask in unit_domain(prototype, star, 0):
            blocker = next((i for i, owner in enumerate(owners) if pose != owner and overlap(pose, owner)), None)
            if blocker is not None:
                obstruction = {'kind': 'interior_overlap', 'owner_index': blocker}
            else:
                pair = pair_occurrence(pose, owners)
                g.require(pair is not None, 'a final supplier remains without a valid obstruction')
                obstruction = {'kind': 'published_pair_requires_second_surround', 'occurrence': pair}
            entries.append([q.pose_serial(pose), mask, obstruction])
        actual_final = {'point': list(star['point']), 'gap': star['gap'], 'start': star['start'],
                        'two_futures_required': True, 'entries': entries}
        g.require(len(entries) == 14 and actual_final == final, 'complete final domain differs')
        rows.append({'case': name, 'prefix_key': claimed['prefix_key'],
                     'old_copy_count': 74, 'verified_old_coronas': 4,
                     'complete_one_future_forces': actual_steps, 'final_gap': actual_final,
                     'odd_candidates_retained': sum(entry[0][0] % 2 for step in actual_steps for entry in step['entries']),
                     'unconditional_all_motion_no_two_futures': True})
    controls = []
    for name in ('basic_T6', 'pending_T7_five'):
        data = unpack(fixtures[name])
        result = g.check(data)
        result.pop('elapsed_seconds')
        result.pop('peak_rss_kib')
        controls.append(result)
    actual_next = {q.int_pose(tuple(row['pose'])) for row in full['copies'] if row['level'] == 5}
    bfe_forces = [(step['pose'][0], step['pose'][1],
                   q.Q3(Fraction(step['pose'][2][0]), Fraction(step['pose'][2][1])),
                   q.Q3(Fraction(step['pose'][3][0]), Fraction(step['pose'][3][1])))
                  for step in rows[0]['complete_one_future_forces']]
    g.require(set(bfe_forces) <= actual_next and [r['verified_coronas'] for r in controls] == [6, 5],
              'actual positive controls differ')
    g.require(pair_occurrence(bfe_forces[-1], tuple(actual_next)) is not None,
              'actual uncovered final fifth lacks the licensed distinction')
    return {'agent': 'six-heesch-3', 'role': 'researcher',
            'status': 'author-checked two fixed-prefix all-motion no-two-surround certificates',
            'prototype_angle_counts': dict(sorted((str(k), v) for k, v in angle_counts.items())),
            'cases': rows, 'actual_positive_controls': controls,
            'actual_final_fifth_with_forbidden_pair_preserved': True,
            'each_force_uses_one_surround': True, 'final_exclusions_need_two_surrounds': True,
            'mate_premise_used': False, 'grid_assumption_used': False,
            'arbitrary_added_motions_allowed': True, 'holes_elsewhere_allowed': True,
            'shape_Heesch_upper_claimed': False, 'historical_priority_claimed': False,
            'shared_polygon_primitives': True, 'formalized': False, 'independently_reviewed': False}


def run(certificate, fixtures):
    evidence = core_check(certificate, fixtures)
    mutations = []
    bad = deepcopy(certificate); bad['future_surrounds_excluded'] = 1
    mutations.append(('uncovered-final-pair-pruning', bad))
    bad = deepcopy(certificate); bad['minimum_prototype_angle_steps'] = 1
    mutations.append(('false-minimum-angle', bad))
    bad = deepcopy(certificate); bad['words_210'].append([6, 1])
    mutations.append(('unlicensed180-plus30-word', bad))
    bad = deepcopy(certificate); step = bad['cases']['bfe']['forces'][0]
    idx = next(i for i, row in enumerate(step['entries']) if row[0][0] % 2)
    step['entries'].pop(idx)
    mutations.append(('omitted-odd-motion', bad))
    bad = deepcopy(certificate); bad['cases']['bfe']['forces'][0]['entries'][0][2] = 9999
    mutations.append(('forged-blocker-owner', bad))
    bad = deepcopy(certificate); bad['cases']['bfe']['forces'][2]['gap'] = 6
    mutations.append(('continuous180-gap-substitution', bad))
    bad = deepcopy(certificate); bad['cases']['bfe']['forces'][0]['pose'][2][0] = '999'
    mutations.append(('wrong-forced-motion', bad))
    bad = deepcopy(certificate); bad['cases']['c0a']['final_gap']['two_futures_required'] = False
    mutations.append(('missing-second-surround-license', bad))
    rejected = []
    for label, bad in mutations:
        try:
            core_check(bad, fixtures)
        except (ValueError, KeyError):
            rejected.append(label)
        else:
            raise ValueError('damaged certificate accepted: '+label)
    evidence['damaged_certificates_rejected'] = rejected
    return evidence


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out')
    args = parser.parse_args()
    if args.out:
        g.require(not Path(args.out).exists(), 'refuse overwrite')
    started = time.monotonic()
    evidence = run(json.loads((HERE/'certificate.json').read_text()),
                   json.loads((HERE/'fixtures.json').read_text()))
    expected = json.loads((HERE/'expected.json').read_text())
    g.require(evidence == expected, 'complete expected evidence differs')
    out = {'stable_evidence_sha256': digest(evidence), 'evidence': evidence,
           'elapsed_seconds': time.monotonic()-started,
           'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.out:
        Path(args.out).write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'evidence'} | {
        'fixed_prefixes': 2, 'complete_unit_candidates_per_case': [18, 18, 48, 14],
        'odd_candidates_per_case': [row['odd_candidates_retained'] for row in evidence['cases']],
        'positive_coronas': [row['verified_coronas'] for row in evidence['actual_positive_controls']],
        'damaged_certificates_rejected': len(evidence['damaged_certificates_rejected'])}, indent=2))
