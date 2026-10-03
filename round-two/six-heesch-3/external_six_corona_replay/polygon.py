#!/usr/bin/env python3
"""Positive polygon reader for uncapped and left-capped strip sources.

Actual author six-heesch-3, researcher. Standard-library exact integers.
No solver, lattice-registration theorem or finite upper is assumed.
Uses the owned convex-intersection and oriented-support boundary primitives.
The capped prototype is a new physical source, not a reused T7 obstruction.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import resource
import time
import geometry as b


def prototype(m, cap):
    atoms = b.atoms(m)
    if cap:
        atoms += (b.ccw(((-2, 2), (0, 0), (2, 2))),)
    b.boundary(atoms)
    for a, c in combinations(atoms, 2):
        b.require(not b.convex_intersection(a, c, False), 'prototype atom overlap')
    return atoms


def check(data):
    start = time.monotonic()
    atoms = prototype(data['tile_hexagons'], data.get('left_cap_triangle', False))
    rows = data['copies']
    poses = [tuple(r['pose']) for r in rows]
    levels = [r['level'] for r in rows]
    b.require(rows and all(len(p) == 4 and all(type(v) is int for v in p)
                          for p in poses), 'invalid integer physical pose')
    b.require(all(type(l) is int and l >= 0 for l in levels), 'invalid level')
    b.require(len(poses) == len(set(poses)), 'duplicate actual copy')
    b.require(levels.count(0) == 1 and poses[levels.index(0)] == (0, 0, 0, 0),
              'root is not normalized identity')
    h = max(levels)
    b.require(set(levels) == set(range(h+1)), 'missing corona layer')
    shaped = [tuple(b.ccw(tuple(b.point(p, v) for v in atom)) for atom in atoms)
              for p in poses]
    boxes = [tuple(b.box(a) for a in s) for s in shaped]
    whole_boxes = [b.box(tuple(v for a in s for v in a)) for s in shaped]
    contacts = []
    neighbors = [set() for _ in rows]
    stats = Counter()
    for i, j in combinations(range(len(rows)), 2):
        if not b.boxes_meet(whole_boxes[i], whole_boxes[j]):
            continue
        touch = False
        for a, ab in zip(shaped[i], boxes[i]):
            for c, cb in zip(shaped[j], boxes[j]):
                if not b.boxes_meet(ab, cb):
                    continue
                stats['atom_pair_tests'] += 1
                b.require(not (b.boxes_meet(ab, cb, False) and
                               b.convex_intersection(a, c, False)),
                          f'actual interiors overlap: {i},{j}')
                if not touch and b.convex_intersection(a, c, True):
                    touch = True
        if touch:
            contacts.append([i, j])
            neighbors[i].add(j)
            neighbors[j].add(i)
            b.require(abs(levels[i]-levels[j]) <= 1, 'contact skips a corona layer')
    for i, l in enumerate(levels):
        if l:
            b.require(any(levels[j] == l-1 for j in neighbors[i]),
                      'copy not grounded in preceding corona')
    records = []
    previous = None
    for l in range(h+1):
        indices = [i for i, level in enumerate(levels) if level <= l]
        cycle, edges = b.boundary(tuple(a for i in indices for a in shaped[i]))
        if previous is not None:
            b.require(not any(b.segments_meet(*a, *c) for a in previous for c in edges),
                      f'prefix{l-1} not strictly interior to prefix{l}')
        previous = edges
        records.append({'corona': l, 'copies': len(indices),
            'simple_disc': True, 'previous_strictly_inside': None if l == 0 else True,
            'twice_area_integer': b.twice_area(cycle), 'boundary_segments': len(edges),
            'whole_boundary_cycle': [list(p) for p in cycle]})
    result = {'agent': 'six-heesch-3', 'role': 'researcher',
        'status': 'exact construction-side certificate; published witness reproduced',
        'tile_hexagons': data['tile_hexagons'],
        'left_cap_triangle': data.get('left_cap_triangle', False),
        'verified_coronas': h, 'copies': len(rows),
        'level_counts': [levels.count(l) for l in range(h+1)],
        'prototype_atoms': [[list(p) for p in a] for a in atoms],
        'prefixes': records, 'all_closed_contact_pairs': contacts,
        'atom_pair_tests': stats['atom_pair_tests'],
        'skip_level_contact_excluded': True, 'whole_atom_packing_checked': True,
        'every_prefix_is_a_disc_and_strictly_surrounds_previous': True,
        'all_motion_registration_claimed': False, 'finite_upper_claimed': False,
        'new_record_or_novel_construction_claimed': False,
        'shared_owned_geometry_not_independent_review': True}
    result['stable_mathematical_sha256'] = sha256(json.dumps(result, sort_keys=True,
        separators=(',', ':')).encode()).hexdigest()
    result['elapsed_seconds'] = time.monotonic()-start
    result['peak_rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    b.require(not Path(args.out).exists(), 'refuse overwrite')
    result = check(json.loads(Path(args.input).read_text()))
    result['witness'] = args.input
    result['witness_sha256'] = sha256(Path(args.input).read_bytes()).hexdigest()
    Path(args.out).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in
                     ('prototype_atoms', 'prefixes', 'all_closed_contact_pairs')}, indent=2))
