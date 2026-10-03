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
    g.require(star['gap'] in (2, 3, 4, 5, 7) and unit in range(star['gap']), 'unproved corner domain')
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
