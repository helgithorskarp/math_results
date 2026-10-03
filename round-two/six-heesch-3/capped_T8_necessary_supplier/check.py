#!/usr/bin/env python3
"""Read a necessary-copy certificate without importing its discovery trace.

six-heesch-3, researcher. Shared owned whole-source/support primitives;
independent of the exploratory corner engine and producer's convex clipping.
This is a retained-template implication, not a global Heesch upper.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import resource
import time

import support as base

g = base.g
POINT = (-110, -6)
FORCED = (8, 1, -82, 26)


def suppliers(cycle):
    vertices = base.corners(cycle)
    angles = sorted({v[3] for v in vertices})
    g.require(min(angles) == 2 and base.complete_words(4, angles) == [(2, 2), (4,)],
              'whole source does not have the claimed complete gap compositions')
    result = set()
    for vertex, first, last, angle in vertices:
        if angle not in (2, 4):
            continue
        for reflection in (0, 1):
            rotation = (2 + last if reflection else 2 - first) % 12
            g.require(rotation % 2 == 0, 'a nonnative supplier needs a field reader')
            x, y = g.point((rotation, reflection, 0, 0), vertex)
            pose = rotation, reflection, POINT[0] - x, POINT[1] - y
            g.require(pose not in result, 'distinct source roles collapse to one pose')
            result.add(pose)
    g.require(len(result) == 50, 'complete first-sector domain changed')
    return result


def read(document, witness_path=None):
    c = document['certificate']
    g.require(base.canonical(c) == document['certificate_sha256'], 'certificate seal differs')
    g.require(c['source_identity_sha256'] == base.SOURCE_SHA and
              c['tile_hexagons'] == 8 and c['left_cap_triangle'] is True,
              'literal capped source differs')
    g.require(c['point'] == list(POINT) and c['gap_steps'] == 4 and
              c['gap_start_step'] == 2 and c['unit'] == 0 and
              c['forced_pose'] == list(FORCED), 'different local implication')
    g.require(c['literal_prefix_level'] == 5 and c['prior_forced_copies_used'] is False and
              c['global_shape_Heesch_upper_claimed'] is False, 'unsupported scope')
    atoms, cycle = base.source()
    template = c['template']
    poses = [base.pose_record(row['pose']) for row in template]
    g.require(poses and len(set(poses)) == len(poses), 'empty or duplicate template')
    shapes = [base.shape(atoms, pose) for pose in poses]
    for i, j in combinations(range(len(shapes)), 2):
        g.require(all(base.separated(a, z) for a in shapes[i] for z in shapes[j]),
                  'template bodies overlap internally')
    occupied = 0
    roots = []
    for i, pose in enumerate(poses):
        sector = base.local_sector(atoms, cycle, pose, POINT)
        if sector is None:
            continue
        mask = sum(1 << ((sector['start'] + j) % 12) for j in range(sector['angle']))
        g.require(not occupied & mask, 'retained local sectors overlap')
        occupied |= mask
        roots.append({'template_index': i, **sector})
    g.require(occupied == sum(1 << j for j in range(12) if j not in range(2, 6)),
              'template does not leave exactly the gap sixty to one-eighty degrees')
    g.require(roots == c['root_sectors'], 'proposed root sectors differ from whole bodies')
    complete = suppliers(cycle)
    g.require(FORCED in complete and FORCED not in poses, 'forced pose is not a new supplier')
    forced_shape = base.shape(atoms, FORCED)
    g.require(all(base.separated(a, z) for shape in shapes for a in forced_shape for z in shape),
              'surviving supplier overlaps the retained template')
    sector = base.local_sector(atoms, cycle, FORCED, POINT)
    g.require(sector is not None and sector['start'] == 2 and sector['angle'] in (2, 4),
              'survivor does not supply the first sector')
    proposed = [base.pose_record(row['pose']) for row in c['overlap_points']]
    g.require(len(proposed) == len(set(proposed)) and
              set(proposed) == complete - {FORCED}, 'not precisely the other forty-nine suppliers')
    supports = []
    for row, pose in zip(c['overlap_points'], proposed):
        g.require(all(type(row[k]) is int for k in ('blocker', 'candidate_atom', 'blocker_atom')),
                  'invalid atom or blocker encoding')
        owner, ai, zi = row['blocker'], row['candidate_atom'], row['blocker_atom']
        g.require(0 <= owner < len(template) and 0 <= ai < len(atoms) and 0 <= zi < len(atoms),
                  'invalid atom or blocker index')
        encoded = row['strict_interior_point']
        g.require(isinstance(encoded, list) and len(encoded) == 2 and
                  all(type(v) is str for v in encoded), 'invalid rational point encoding')
        p = tuple(Fraction(v) for v in encoded)
        values = [[g.turn(v, atom[(i+1) % len(atom)], p) for i, v in enumerate(atom)]
                  for atom in (base.shape(atoms, pose)[ai], shapes[owner][zi])]
        g.require(all(v > 0 for group in values for v in group),
                  'point is not strictly inside both atoms')
        supports.append({'pose': list(pose), 'blocker': owner,
                         'strict_support_values': [[str(v) for v in group] for group in values]})
    application = None
    if witness_path:
        raw = Path(witness_path).read_bytes()
        g.require(sha256(raw).hexdigest() == c['original_six_witness_sha256'] == base.WITNESS_SHA,
                  'normalized source witness changed')
        data = json.loads(raw)
        g.require(data['tile_hexagons'] == 8 and data['left_cap_triangle'] is True and
                  len(data['copies']) == 258, 'construction input changed')
        original_ids = []
        for row in template:
            index = row['original_index']
            g.require(type(index) is int and 0 <= index < 258, 'invalid original index')
            actual = data['copies'][index]
            g.require(actual['pose'] == row['pose'] and actual['level'] == row['original_level'] <= 5,
                      'template is not retained in the literal fifth prefix')
            original_ids.append(index)
        matches = [i for i, row in enumerate(data['copies']) if tuple(row['pose']) == FORCED]
        g.require(len(matches) == 1 and data['copies'][matches[0]]['level'] == 6,
                  'forced supplier is absent from the known sixth control')
        application = {'witness_sha256': base.WITNESS_SHA, 'original_template_indices': original_ids,
                       'known_sixth_supplier_index': matches[0], 'known_sixth_is_control_only': True}
    return {'agent': 'six-heesch-3', 'role': 'researcher',
            'status': 'necessary retained-template supplier checked by strict rational supports',
            'certificate_sha256': document['certificate_sha256'],
            'source_identity_sha256': base.SOURCE_SHA,
            'source_whole_boundary': [list(p) for p in cycle],
            'retained_template': [list(pose) for pose in poses], 'root_sectors': roots,
            'complete_first_sector_poses': [list(pose) for pose in sorted(complete)],
            'necessary_supplier_pose': list(FORCED), 'necessary_supplier_sector': sector,
            'strict_overlap_support_records': supports,
            'all_other_49_suppliers_strictly_blocked': True,
            'prior_force_trace_used': False, 'producer_clipping_used': False,
            'point_interior_to_larger_union_is_required_hypothesis': True,
            'all_Euclidean_congruences_allowed': True,
            'application_to_literal_fifth': application,
            'global_Heesch_upper_claimed': False, 'independent_review_claimed': False}


def run():
    started=time.monotonic()
    here=Path(__file__).resolve().parent
    document=json.loads((here/'certificate.json').read_text())
    result=read(document)
    result['stable_mathematical_sha256']=base.canonical(result)
    result['elapsed_seconds']=time.monotonic()-started
    result['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return result

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
