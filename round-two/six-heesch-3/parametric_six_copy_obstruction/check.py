#!/usr/bin/env python3
"""Exact six-copy real-window obstruction; no disc/mate/grid premise."""
import argparse,json,resource,time
from collections import Counter
from copy import deepcopy
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import corner as c
import geometry as g
import field as q
HERE=Path(__file__).resolve().parent
ALL = (1 << 12) - 1


@lru_cache(None)
def middle_ray(unit):
    # Equal metric lengths: their sum lies strictly inside this30deg unit.
    u = q.linear(unit, 0, (4, 0))
    v = q.linear((unit + 1) % 12, 0, (4, 0))
    return u[0] + v[0], u[1] + v[1]


@lru_cache(None)
def cone_mask(pose, point):
    """Exact local open angular units of a copy at an integer point.

    Convex atom inequalities decide containment. At active edges the
    directional derivative decides the tangent cone; no finite epsilon.
    All supporting rays are30deg multiples, so a middle-ray test decides
    the entire corresponding open unit. Internal atom boundaries cancel
    by taking the union; no connected-boundary assumption is needed.
    """
    occupied = 0
    for atom in g.shape(7, pose)[0]:
        values = [g.turn(v, atom[(i+1) % len(atom)], point)
                  for i, v in enumerate(atom)]
        if any(value < 0 for value in values):
            continue
        edges = [g.sub(atom[(i+1) % len(atom)], v)
                 for i, v in enumerate(atom) if values[i] == 0]
        for edge in edges:
            c.direction(*edge)  # Verify the angular-unit completeness premise.
        for unit in range(12):
            ray = middle_ray(unit)
            if all(g.cross(edge, ray) > 0 for edge in edges):
                occupied |= 1 << unit
    return occupied


def gap_mask(star):
    return sum(1 << ((star['start'] + j) % 12) for j in range(star['gap']))


def read_pose(row):
    from fractions import Fraction
    return row[0], row[1], q.Q3(Fraction(row[2][0]), Fraction(row[2][1])), q.Q3(Fraction(row[3][0]), Fraction(row[3][1]))


COMMON = [(0, 0, -16, -16), (6, 1, 80, -32), (6, 1, 76, -36),
          (6, 1, 72, -40), (6, 1, 68, -44)]
RESIDUAL = [(0, 0, 16, -48), (6, 1, 64, -48), (6, 1, 72, -48)]
FAMILIES = {'R': {'orientation': (6, 1), 'bounds': (16, 120), 'excluded': [64, 72]},
            'F': {'orientation': (0, 0), 'bounds': (-40, 64), 'excluded': [16]}}


def parameter_admissible(family, value):
    spec = FAMILIES[family]
    return spec['bounds'][0] < value < spec['bounds'][1] and value not in spec['excluded']


def open_union(intervals):
    out = []
    for lo, hi in sorted(intervals):
        g.require(lo < hi, 'empty positive-overlap band')
        if out and lo < out[-1][1]:
            out[-1][1] = max(hi, out[-1][1])
        else:
            out.append([lo, hi])
    return out


def hex_windows():
    # A normalized hexagon's horizontal midline interior is (-4,4).
    # At equal y, |center_x difference|<8 therefore gives a shared
    # interior point. Open bands overlap strictly, so their unions cover
    # all real parameter values in the asserted window, irrational too.
    rows = []
    families = {}
    for family, specification in FAMILIES.items():
        a, f = specification['orientation']
        endpoints = []
        for supplier in RESIDUAL:
            bands = []
            for i in range(7):
                sx, sy = g.point(supplier, (4+8*i, 0))
                for j in range(7):
                    bx, by = g.point((a, f, 0, -48), (4+8*j, 0))
                    g.require(sy == by == -48, 'hexagon centers have different heights')
                    lo, hi = sx-bx-8, sx-bx+8
                    bands.append([lo, hi, i, j])
            merged = open_union([row[:2] for row in bands])
            g.require(len(merged) == 1, 'horizontal support is not one open interval')
            endpoints.append(merged[0])
            rows.append({'family': family, 'supplier_pose': list(supplier),
                         'all49_hex_pair_bands': bands, 'real_open_union': merged[0]})
        intersection = [max(x[0] for x in endpoints), min(x[1] for x in endpoints)]
        g.require(intersection == list(specification['bounds']), 'all-supplier real window changed')
        exclusions = [p[2] for p in RESIDUAL if tuple(p[:2]) == specification['orientation']]
        g.require(exclusions == specification['excluded'], 'same-copy exception list incomplete')
        for value in intersection + exclusions:
            g.require(not parameter_admissible(family, value), 'endpoint/coincident copy incorrectly licensed')
        families[family] = {'blocker_orientation': list(specification['orientation']), 'blocker_y': -48,
                            'real_open_window': intersection, 'excluded_same_copy_values': exclusions,
                            'endpoints_and_same_copy_exceptions_rejected': True}
    return {'axis_half_width': 4, 'strict_center_distance_threshold': 8,
            'six_complete_hex_window_certificates': rows, 'families': families,
            'sampled_reals_used_as_proof': False, 'window_optimality_claimed': False}


def common_certificate(baseline):
    source = baseline['cases'][0]
    g.require(source['core_poses'][:-1] == [list(p) for p in COMMON], 'extracted common core changed')
    for p, z in combinations(COMMON, 2):
        g.require(not g.pair(7, p, z)[0], 'common core not a packing')
    stars = source['original_local_sectors']
    g.require(len(stars) == 4, 'four original local points needed')
    sectors = []
    for star in stars:
        masks = [cone_mask(p, tuple(star['point'])) for p in COMMON]
        mask = 0
        for value in masks:
            mask |= value
        g.require(mask == ALL ^ gap_mask(star) == star['occupied_mask'], 'reduced tangent sector differs')
        sectors.append(dict(star, common_owner_masks=masks))
    prototype = c.vertices(g.atoms(7))
    owners = [q.int_pose(p) for p in COMMON]
    forces = []
    for star, spec in zip(stars, source['one_future_forces']):
        entries = []
        survivors = []
        for pose, mask in c.unit_domain(prototype, star, spec['unit']):
            blocker = next((i for i, owner in enumerate(owners) if pose != owner and c.overlap(pose, owner)), None)
            entries.append([q.pose_serial(pose), mask, blocker])
            if blocker is None:
                survivors.append(pose)
        g.require(len(survivors) == 1 and q.pose_serial(survivors[0]) == spec['pose'], 'common-only force not unique')
        forces.append(dict(spec, entries=entries))
        owners.append(survivors[0])
    final = []
    residual = []
    for pose, mask in c.unit_domain(prototype, stars[-1], 0):
        occurrence = c.pair_occurrence(pose, owners)
        if occurrence is None:
            g.require(c.native(pose) in RESIDUAL, 'unclassified final supplier')
            residual.append(c.native(pose))
        final.append([q.pose_serial(pose), mask, occurrence])
    g.require(residual == RESIDUAL and len(final) == 14 and
              [len(f['entries']) for f in forces] == [18, 18, 48], 'complete common domain differs')
    return {'common_five_poses': [list(p) for p in COMMON],
            'four_complete_tangent_sector_certificates': sectors,
            'three_ONE_surround_force_certificates': forces,
            'final14_supplier_domain': final,
            'residual_three_suppliers': [list(p) for p in RESIDUAL],
            'remaining_eleven_excluded_only_under_TWO_surrounds': True,
            'fifty_odd_force_motions_retained': sum(p[0][0] % 2 for f in forces for p in f['entries']) == 50,
            'extra_blocker_not_used_for_common_forcing': True}


def apply_to_fourths(state):
    applications = []
    for key, record in state['closed'].items():
        data = record['input']
        if max(r['level'] for r in data['copies']) != 4:
            continue
        poses = {tuple(r['pose']) for r in data['copies']}
        g.require(set(COMMON) <= poses, 'saved fourth lacks the common core')
        matching = []
        for pose in sorted(poses):
            for family, specification in FAMILIES.items():
                if tuple(pose[:2]) == specification['orientation'] and pose[3] == -48 and parameter_admissible(family, pose[2]):
                    matching.append({'family': family, 'parameter': pose[2], 'pose': list(pose)})
        g.require(len(matching) == 1, 'saved fourth does not have one qualifying sixth blocker')
        result = g.check(data)
        g.require(result['verified_coronas'] == 4 and c.prefix_key(data) == key, 'literal fourth geometry/key differs')
        for p, z in combinations(COMMON + [tuple(matching[0]['pose'])], 2):
            g.require(not g.pair(7, p, z)[0], 'six-copy application is not a packing')
        applications.append({'prefix_key': key, 'verified_old_coronas': 4,
            'literal_copy_count': len(poses), 'level_counts': result['level_counts'],
            'sixth_blocker': matching[0], 'common_five_present': True,
            'unconditional_all_motion_no_two_futures': True,
            'unconditional_no_ONE_future_claimed': False,
            'no_global_shape_upper': True})
    g.require(len(applications) == 7, 'seven saved fourths expected')
    return applications


BASELINE = {'cases': [{'core_poses': [[0, 0, -16, -16], [6, 1, 80, -32], [6, 1, 76, -36], [6, 1, 72, -40], [6, 1, 68, -44], [6, 1, 96, -48]], 'original_local_sectors': [{'point': [24, -32], 'gap': 5, 'start': 3, 'occupied_mask': 3847}, {'point': [16, -40], 'gap': 5, 'start': 3, 'occupied_mask': 3847}, {'point': [12, -44], 'gap': 7, 'start': 3, 'occupied_mask': 3079}, {'point': [20, -44], 'gap': 2, 'start': 8, 'occupied_mask': 3327}], 'one_future_forces': [{'point': [24, -32], 'gap': 5, 'start': 3, 'unit': 3, 'pose': [0, 0, ['-32', '0'], ['-32', '0']], 'one_future_only': True}, {'point': [16, -40], 'gap': 5, 'start': 3, 'unit': 3, 'pose': [0, 0, ['-40', '0'], ['-40', '0']], 'one_future_only': True}, {'point': [12, -44], 'gap': 7, 'start': 3, 'unit': 0, 'pose': [0, 0, ['-44', '0'], ['-44', '0']], 'one_future_only': True}]}]}
PREFIX_KEYS = ['d77714fc0b907e842dc6fd32c812c710980afeaf4da93d30882185dc8b9a368d', '72e6a0c7271a9e6d3adb24b75ab14b688992dcf8e755af5338105d34e964c623', 'ba459ec8ccac882047c1735746f3d22e0666ddde860ff476c04e675c507db57d', 'cc722a91b15e206ac550c50abb955d8feeb970ffa72347b79b3a6921195268ad', 'bfe0a1ac4726d42ba48ac83616a064b399237716fb3f11a5ad99bf313f7fc65e', '90a0d8d19c486de85fe56d1b16a32ff1972b81e9d7de93ac1b1098f1be1f1fea', 'c0a54a208ae29ab57ef26cf15c42691cb750bb585fec78c5a36c714869fe9fc2']

def fixture_state(fixtures):
    closed = {}
    for fixture in fixtures['fourths']:
        key = fixture['prefix_key']
        g.require(key not in closed and fixture['tile_hexagons'] == 7, 'wrong or repeated literal tile')
        closed[key] = {'input': c.unpack(fixture)}
    g.require(set(closed) == set(PREFIX_KEYS), 'wrong seven literal prefixes')
    return {'closed': closed}


def make_certificate(fixtures):
    return {'schema': 1, 'future_surrounds_excluded': 2, 'minimum_prototype_angle_steps': 2,
            'words_210': [list(w) for w in c.words(7)],
            'uncovered_final_layer_pruning_licensed': False,
            'common_certificate': common_certificate(BASELINE),
            'real_hex_overlap_windows': hex_windows(),
            'applications': apply_to_fourths(fixture_state(fixtures))}


def core_check(certificate, fixtures):
    g.require(certificate['schema'] == 1 and certificate['future_surrounds_excluded'] == 2 and
              certificate['minimum_prototype_angle_steps'] == 2 and
              certificate['words_210'] == [list(w) for w in c.words(7)] and
              certificate['uncovered_final_layer_pruning_licensed'] is False and
              len(certificate['applications']) == 7, 'incorrect stage, minimum angle or literal count')
    angles = Counter(v['angle'] for v in c.vertices(g.atoms(7)))
    g.require(dict(angles) == {2:7,3:1,4:15,5:1,6:1,8:13,10:6}, 'prototype angle classification changed')
    common = common_certificate(BASELINE)
    g.require(common == certificate['common_certificate'] and
              sum(e[2] is not None for e in common['final14_supplier_domain']) == 11,
              'complete common local/force/pair certificate changed')
    windows = hex_windows()
    g.require(windows == certificate['real_hex_overlap_windows'], 'real bands or same-copy exceptions changed')
    applications = apply_to_fourths(fixture_state(fixtures))
    g.require(applications == certificate['applications'], 'literal application certificate changed')
    controls = []
    for name in ('basic_T6', 'pending_T7_five'):
        data = c.unpack(fixtures[name])
        result = g.check(data)
        result.pop('elapsed_seconds'); result.pop('peak_rss_kib')
        controls.append(result)
    g.require([r['verified_coronas'] for r in controls] == [6,5], 'known positive corona depths changed')
    full = c.unpack(fixtures['pending_T7_five'])
    poses4 = {tuple(r['pose']) for r in full['copies'] if r['level']<=4}
    final_poses = [q.int_pose(tuple(r['pose'])) for r in full['copies'] if r['level']==5]
    g.require(set(COMMON+[(6,1,96,-48)]) <= poses4 and
              c.pair_occurrence(q.int_pose((0,0,-44,-44)), final_poses) is not None,
              'actual fifth/core or final-layer pair control changed')
    parameter_controls = []
    for family, bad_values, good_values in (
            ('R', [16,120,64,72], [80,88,96,104]),
            ('F', [-40,64,16], [32,40,48])):
        for value in bad_values:
            g.require(not parameter_admissible(family,value), 'endpoint/coincidence incorrectly admissible')
            parameter_controls.append([family,value,False])
        for value in good_values:
            g.require(parameter_admissible(family,value), 'positive application parameter rejected')
            parameter_controls.append([family,value,True])
    hex_control = []
    h = g.atoms(7)[0]
    for dx in (-9,-8,-7,0,7,8,9):
        shifted = tuple((x+dx,y) for x,y in h)
        overlap = g.convex_intersection(h,shifted,False)
        g.require(overlap == (abs(dx)<8), 'horizontal hexagon strict-boundary calibration failed')
        hex_control.append([dx,overlap])
    return {'agent':'six-heesch-3','role':'researcher',
            'status':'author-checked parametric six-copy no-TWO-surround obstruction',
            'prototype_angle_counts':dict(sorted((str(k),v) for k,v in angles.items())),
            'common_certificate':common,'real_hex_overlap_windows':windows,
            'literal_fourth_applications':applications,'actual_positive_controls':controls,
            'parameter_endpoint_and_coincidence_controls':parameter_controls,
            'strict_hex_overlap_controls':hex_control,
            'actual_final_fifth_with_forbidden_pair_preserved':True,
            'core_copy_count':6,'arbitrary_initial_superpackings_and_common_isometries_allowed':True,
            'arbitrary_added_motions_allowed':True,'holes_elsewhere_allowed':True,
            'connectedness_or_disc_premise_used':False,'mate_premise_used':False,'global_grid_premise_used':False,
            'real_parameter_samples_used_as_proof':False,'parameter_windows_claimed_optimal':False,
            'shape_Heesch_upper_claimed':False,'historical_priority_claimed':False,
            'independently_reviewed':False,'formalized':False,'shared_author_polygon_primitives':True,
            'pair_lemma_dependency':c.PAIR_REF}


def run(certificate, fixtures):
    evidence = core_check(certificate,fixtures)
    mutations = []
    bad=deepcopy(certificate);bad['future_surrounds_excluded']=1
    mutations.append(('only-one-future-pair-license',bad))
    bad=deepcopy(certificate);bad['minimum_prototype_angle_steps']=1
    mutations.append(('false-minimum-angle',bad))
    bad=deepcopy(certificate);bad['words_210'].append([6,1])
    mutations.append(('unlicensed-edge-plus30-word',bad))
    bad=deepcopy(certificate);bad['uncovered_final_layer_pruning_licensed']=True
    mutations.append(('uncovered-final-layer-pair-pruning',bad))
    bad=deepcopy(certificate);step=bad['common_certificate']['three_ONE_surround_force_certificates'][0]
    idx=next(i for i,e in enumerate(step['entries']) if e[0][0]%2)
    step['entries'].pop(idx);mutations.append(('omitted-odd-motion',bad))
    bad=deepcopy(certificate);bad['common_certificate']['three_ONE_surround_force_certificates'][0]['pose'][2][0]='999'
    mutations.append(('forged-forced-pose',bad))
    bad=deepcopy(certificate);bad['common_certificate']['four_complete_tangent_sector_certificates'][0]['occupied_mask']=0
    mutations.append(('forged-local-sector',bad))
    bad=deepcopy(certificate);bad['common_certificate']['three_ONE_surround_force_certificates'][2]['gap']=6
    mutations.append(('continuous180-gap-substitution',bad))
    bad=deepcopy(certificate);domain=bad['common_certificate']['final14_supplier_domain']
    idx=next(i for i,e in enumerate(domain) if e[2] is not None)
    domain[idx][2]=None;mutations.append(('omitted-eleventh-pair-exclusion',bad))
    bad=deepcopy(certificate);bad['real_hex_overlap_windows']['families']['R']['excluded_same_copy_values']=[]
    mutations.append(('R-self-overlap-as-distinct-copy-conflict',bad))
    bad=deepcopy(certificate);bad['real_hex_overlap_windows']['families']['F']['excluded_same_copy_values']=[]
    mutations.append(('F-self-overlap-as-distinct-copy-conflict',bad))
    bad=deepcopy(certificate);bad['real_hex_overlap_windows']['six_complete_hex_window_certificates'][0]['all49_hex_pair_bands'][0][0]-=1
    mutations.append(('forged-positive-hex-band',bad))
    bad=deepcopy(certificate);bad['applications'].pop()
    mutations.append(('omitted-literal-fourth-application',bad))
    rejected=[]
    for label,bad in mutations:
        try:core_check(bad,fixtures)
        except (ValueError,KeyError):rejected.append(label)
        else:raise ValueError('damaged certificate accepted: '+label)
    evidence['damaged_certificates_rejected']=rejected
    return evidence


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--build',action='store_true')
    ap.add_argument('--output')
    args=ap.parse_args()
    started=time.monotonic()
    fixtures=json.loads((HERE/'fixtures.json').read_text())
    if args.build:
        certificate=make_certificate(fixtures)
        (HERE/'certificate.json').write_text(json.dumps(certificate,indent=1)+'\n')
    else:certificate=json.loads((HERE/'certificate.json').read_text())
    evidence=run(certificate,fixtures)
    stable=c.digest(evidence)
    if args.build:
        expected={'stable_evidence_sha256':stable,'core_copy_count':6,'literal_fourth_count':7,
                  'pair_excluded_suppliers':11,'residual_suppliers':3,'positive_depths':[6,5],
                  'damaged_certificates_rejected':13}
        (HERE/'expected.json').write_text(json.dumps(expected,indent=2)+'\n')
    else:
        expected=json.loads((HERE/'expected.json').read_text())
        g.require(stable==expected['stable_evidence_sha256'],'complete expected evidence hash mismatch')
    result={'stable_evidence_sha256':stable,'evidence':evidence,'elapsed_seconds':time.monotonic()-started,
            'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='evidence'} |
                     {'literal_fourths':7,'damaged_rejected':13,'positive_depths':[6,5]},indent=2))


if __name__=='__main__':main()
