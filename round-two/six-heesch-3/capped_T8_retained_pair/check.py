#!/usr/bin/env python3
"""Read a retained-copy obstruction using strict rational support witnesses.

six-heesch-3, researcher. No exploratory producer or clipping code is imported.
The owned source/boundary/integer-motion primitives remain a shared trust base.
This certifies a local obstruction, not a shape-wide finite Heesch upper.
"""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import resource
import time

import geometry as g

RAYS = ((1, 0), (3, 1), (1, 1), (0, 1), (-1, 1), (-3, 1),
        (-1, 0), (-3, -1), (-1, -1), (0, -1), (1, -1), (3, -1))
SOURCE_SHA = 'e0be853cddead80f6ddb1e353c6d7aa4b869024b532e107d9cae8c76c4eae71f'
WITNESS_SHA = 'a5a4d492c8f15a46ee9b3c78b9450d4ac5061f80361670281390af07802e1704'


def canonical(obj):
    obj = json.loads(json.dumps(obj))
    return sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def direction(vector):
    dx, dy = vector
    hits = [i for i, (a, b) in enumerate(RAYS)
            if dx * b == dy * a and dx * a + dy * b > 0]
    g.require(len(hits) == 1, 'boundary ray is not an exact thirty-degree direction')
    return hits[0]


def source():
    atoms = g.atoms(8) + (g.ccw(((-2, 2), (0, 0), (2, 2))),)
    for a, z in combinations(atoms, 2):
        g.require(separated(a, z), 'literal source atoms overlap')
    cycle, _ = g.boundary(atoms)
    identity = {'coordinates': 'physical(x,sqrt(3)y)/4', 'tile_hexagons': 8,
                'left_cap_triangle': True, 'prototype_atoms':
                [[list(p) for p in a] for a in atoms]}
    g.require(canonical(identity) == SOURCE_SHA, 'literal capped-source identity differs')
    return atoms, cycle


def separated(a, z):
    # Convex supporting-axis separation; boundary contact is permitted.
    return any(max(g.turn(v, poly[(i + 1) % len(poly)], w) for w in other) <= 0
               for poly, other in ((a, z), (z, a)) for i, v in enumerate(poly))


def shape(atoms, pose):
    return tuple(g.ccw(tuple(g.point(pose, p) for p in atom)) for atom in atoms)


def corners(cycle):
    result = []
    for i, p in enumerate(cycle):
        first = direction(g.sub(cycle[(i + 1) % len(cycle)], p))
        last = direction(g.sub(cycle[i - 1], p))
        angle = (last - first) % 12
        g.require(0 < angle < 12, 'invalid whole-boundary sector')
        result.append((p, first, last, angle))
    g.require(sum(6 - row[3] for row in result) == 12, 'whole turning sum differs')
    return result


def complete_words(total, values):
    if total == 0:
        return [()]
    return [(a,) + rest for a in values if a <= total
            for rest in complete_words(total - a, values)]


def pose_record(value):
    g.require(isinstance(value, list) and len(value) == 4 and
              all(type(v) is int for v in value), 'invalid integer pose')
    angle, reflected, x, y = value
    g.require(angle in range(0, 12, 2) and reflected in (0, 1),
              'invalid derived motion')
    return tuple(value)


def complete_suppliers(cycle, point):
    vertices = corners(cycle)
    values = sorted({row[3] for row in vertices})
    g.require(min(values) == 2 and complete_words(4, values) == [(2, 2), (4,)],
              'complete 120-degree supplier-angle compositions changed')
    supplied = set()
    for vertex, first, last, angle in vertices:
        if angle not in (2, 4):
            continue
        for reflection in (0, 1):
            # No registration premise: the gap's first ray fixes this rotation.
            rotation = (last if reflection else -first) % 12
            g.require(rotation % 2 == 0, 'odd rotation needs a field-valued reader')
            image = g.point((rotation, reflection, 0, 0), vertex)
            pose = (rotation, reflection, point[0] - image[0], point[1] - image[1])
            g.require(pose not in supplied, 'different roles give an identical pose')
            supplied.add(pose)
    g.require(len(supplied) == 50, 'complete pinned first-sector domain changed')
    return supplied


def local_sector(atoms, cycle, pose, point):
    polygons = shape(atoms, pose)
    inside = any(all(g.turn(v, atom[(i + 1) % len(atom)], point) >= 0
                     for i, v in enumerate(atom)) for atom in polygons)
    if not inside:
        return None
    boundary = g.ccw(tuple(g.point(pose, p) for p in cycle))
    hits = [row for row in corners(boundary) if row[0] == point]
    if hits:
        g.require(len(hits) == 1, 'repeated boundary point')
        _, first, last, angle = hits[0]
    else:
        edges = [(a, boundary[(i + 1) % len(boundary)])
                 for i, a in enumerate(boundary)
                 if g.on_segment(point, a, boundary[(i + 1) % len(boundary)])]
        g.require(len(edges) == 1, 'retained body already covers the point internally')
        first = direction(g.sub(edges[0][1], edges[0][0]))
        angle, last = 6, (first + 6) % 12
    return {'angle': angle, 'start': first, 'end': last}


def read(document, witness_path=None):
    certificate = document['certificate']
    g.require(canonical(certificate) == document['certificate_sha256'],
              'certificate canonical checksum differs')
    g.require(certificate['tile_hexagons'] == 8 and
              certificate['left_cap_triangle'] is True and
              certificate['source_identity_sha256'] == SOURCE_SHA,
              'different literal source')
    g.require(certificate['point'] == [-98, 18] and certificate['gap_steps'] == 4 and
              certificate['gap_start_step'] == 0 and certificate['unit'] == 0,
              'different local sector; completeness needs a new derivation')
    g.require(certificate['forced_copy_used'] is False and
              certificate['global_shape_Heesch_upper_claimed'] is False,
              'unsupported scope')
    point = tuple(certificate['point'])
    atoms, cycle = source()
    template = certificate['template']
    poses = [pose_record(row['pose']) for row in template]
    g.require(poses and len(set(poses)) == len(poses), 'empty or duplicate retained template')
    shapes = [shape(atoms, pose) for pose in poses]
    for i, j in combinations(range(len(shapes)), 2):
        g.require(all(separated(a, z) for a in shapes[i] for z in shapes[j]),
                  'retained copies do not form a packing')
    roots = []
    occupied = 0
    for i, pose in enumerate(poses):
        root = local_sector(atoms, cycle, pose, point)
        if root is None:
            continue
        mask = sum(1 << ((root['start'] + j) % 12) for j in range(root['angle']))
        g.require(occupied & mask == 0, 'retained local sectors overlap')
        occupied |= mask
        roots.append({'template_index': i, **root})
    g.require(occupied == sum(1 << j for j in range(4, 12)),
              'retained sectors do not leave precisely the required 120-degree gap')
    proposal_roots = [{k: row[k] for k in ('template_index', 'angle', 'start', 'end')}
                      for row in certificate['root_sectors']]
    g.require(roots == proposal_roots, 'root sectors are not fresh whole-body sectors')
    suppliers = complete_suppliers(cycle, point)
    proposed = [pose_record(row['pose']) for row in certificate['overlap_points']]
    g.require(len(proposed) == len(set(proposed)) and set(proposed) == suppliers,
              'rational witnesses omit, duplicate, or introduce a supplier')
    support_records = []
    for row, pose in zip(certificate['overlap_points'], proposed):
        g.require(all(type(row[k]) is int for k in
                      ('blocker', 'candidate_atom', 'blocker_atom')), 'invalid atom index')
        owner, ai, zi = row['blocker'], row['candidate_atom'], row['blocker_atom']
        g.require(0 <= owner < len(template) and 0 <= ai < len(atoms) and
                  0 <= zi < len(atoms), 'atom or blocker index is outside the literal body')
        encoded = row['strict_interior_point']
        g.require(isinstance(encoded, list) and len(encoded) == 2 and
                  all(type(v) is str for v in encoded), 'invalid rational witness encoding')
        rational_point = tuple(Fraction(v) for v in encoded)
        pair = (shape(atoms, pose)[ai], shapes[owner][zi])
        values = [[g.turn(v, atom[(i + 1) % len(atom)], rational_point)
                   for i, v in enumerate(atom)] for atom in pair]
        g.require(all(value > 0 for group in values for value in group),
                  'point is not strictly inside both indicated convex atoms')
        support_records.append({'pose': list(pose), 'blocker': owner,
            'strict_support_values': [[str(v) for v in group] for group in values]})
    application = None
    if witness_path is not None:
        raw = Path(witness_path).read_bytes()
        g.require(sha256(raw).hexdigest() == WITNESS_SHA and
                  certificate['original_six_witness_sha256'] == WITNESS_SHA,
                  'original six-corona input changed')
        data = json.loads(raw)
        g.require(data['tile_hexagons'] == 8 and data['left_cap_triangle'] is True and
                  len(data['copies']) == 258, 'wrong construction-side input')
        for row in template:
            i = row['original_index']
            g.require(type(i) is int and 0 <= i < 258, 'invalid original copy index')
            actual = data['copies'][i]
            g.require(actual['pose'] == row['pose'] and
                      actual['level'] == row['original_level'], 'template is not retained in the input')
        application = {'literal_six_witness_sha256': WITNESS_SHA,
                       'original_indices': [row['original_index'] for row in template],
                       'original_levels': [row['original_level'] for row in template],
                       'not_extended_to_other_six_layouts': True}
    return {'agent': 'six-heesch-3', 'role': 'researcher',
        'status': 'complete strict-rational-point local obstruction checked',
        'source_identity_sha256': SOURCE_SHA,
        'source_angle_histogram': dict(sorted(Counter(row[3] for row in corners(cycle)).items())),
        'source_whole_boundary': [list(p) for p in cycle],
        'certificate_sha256': document['certificate_sha256'],
        'retained_template': [list(pose) for pose in poses], 'root_sectors': roots,
        'complete_first_sector_poses': [list(pose) for pose in sorted(suppliers)],
        'strict_overlap_support_records': support_records,
        'packing_and_sector_gap_checked': True, 'all_50_suppliers_strictly_blocked': True,
        'common_arbitrary_Euclidean_isometry_allowed': True,
        'additional_actual_copies_allowed_monotonically': True,
        'source_primitives_shared_with_owned_positive_reader': True,
        'producer_clipping_or_live_flags_used': False,
        'application_to_literal_six': application,
        'global_Heesch_upper_claimed': False, 'independent_reviewer_verdict_claimed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True)
    parser.add_argument('--witness')
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    g.require(not Path(args.out).exists(), 'do not overwrite a frozen reading')
    started = time.monotonic()
    result = read(json.loads(Path(args.input).read_text()), args.witness)
    result['stable_mathematical_sha256'] = canonical(result)
    result['elapsed_seconds'] = time.monotonic() - started
    result['peak_rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    Path(args.out).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in
        ('source_whole_boundary', 'complete_first_sector_poses', 'strict_overlap_support_records')}, indent=2))
