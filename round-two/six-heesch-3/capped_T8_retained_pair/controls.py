#!/usr/bin/env python3
"""Semantic damage controls and full normal/optimized record comparison.

six-heesch-3, researcher. Damaged certificates are canonically resealed, so
the rejection must come from mathematics or scope rather than a stale hash.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import resource
import time

import check as reader


def rejected(document, mutation):
    damaged = deepcopy(document)
    mutation(damaged['certificate'])
    damaged['certificate_sha256'] = reader.canonical(damaged['certificate'])
    try:
        reader.read(damaged)
    except ValueError as error:
        return str(error)
    raise ValueError('semantic damage was accepted')


def lose_flat_root(c):
    c['template'] = c['template'][1:]
    c['root_sectors'] = c['root_sectors'][1:]
    c['root_sectors'][0]['template_index'] = 0
    for row in c['overlap_points']:
        row['blocker'] = 0


def make():
    started = time.monotonic()
    document = json.loads((Path(__file__).resolve().parent / 'certificate.json').read_text())
    reader.read(document)
    mutations = {
        'omit_supplier': lambda c: c['overlap_points'].pop(),
        'duplicate_supplier': lambda c: c['overlap_points'].append(deepcopy(c['overlap_points'][0])),
        'point_outside': lambda c: c['overlap_points'][0].update(strict_interior_point=['100000', '100000']),
        'invalid_atom': lambda c: c['overlap_points'][0].update(candidate_atom=100000),
        'lose_flat_root': lose_flat_root,
        'uncapped_source': lambda c: c.update(left_cap_triangle=False),
        'unsupported_global_upper': lambda c: c.update(global_shape_Heesch_upper_claimed=True),
    }
    rejection = {name: rejected(document, mutation) for name, mutation in mutations.items()}
    poses = [tuple(row['pose']) for row in document['certificate']['template']]
    first, second = poses
    reader.g.require(first == (8, 1, -98, 18) and second == (8, 1, -82, 26),
                     'normalization is for these exact two copies')
    linear = (8, 1, 0, 0)
    atoms, _ = reader.source()
    vertices = {p for atom in atoms for p in atom}
    reader.g.require(all(reader.g.point(linear, reader.g.point(linear, p)) == p
                         for p in vertices), 'normalizing reflected motion is not its inverse')
    delta = reader.g.sub(second[2:], first[2:])
    relative = reader.g.point(linear, delta)
    reader.g.require(relative == (-20, -4), 'relative normalized translation differs')
    p = tuple(document['certificate']['point'])
    reader.g.require(reader.g.point(linear, reader.g.sub(p, first[2:])) == (0, 0),
                     'normalized critical point differs')
    reader.g.require(all(reader.g.point(linear, reader.g.sub(reader.g.point(second, v), first[2:])) ==
                         (v[0] - 20, v[1] - 4) for v in vertices),
                     'normalized second whole body differs')
    result = {'agent': 'six-heesch-3', 'role': 'researcher',
        'status': 'seven resealed semantic damages and whole-source pair normalization checked',
        'certificate_sha256': document['certificate_sha256'],
        'valid_rational_reading_checked': True,
        'all_fifty_overlap_owners_are_second_root': all(row['blocker'] == 1
            for row in document['certificate']['overlap_points']),
        'resealed_damage_rejections': rejection,
        'normalized_pair': [[0, 0, 0, 0], [0, 0, -20, -4]],
        'normalized_point': [0, 0], 'whole_source_normalization_checked': True,
        'global_Heesch_upper_claimed': False, 'independent_review_claimed': False}
    result['stable_mathematical_sha256'] = reader.canonical(result)
    result['elapsed_seconds'] = time.monotonic() - started
    result['peak_rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    reader.g.require(not Path(args.out).exists(), 'do not overwrite frozen controls')
    result = make()
    Path(args.out).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
