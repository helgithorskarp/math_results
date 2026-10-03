"""Whole-source, motion and support helpers shared with the owned pair reader.
Actual author six-heesch-3, researcher. No producer/propagation import.
"""
from hashlib import sha256
from itertools import combinations
import json
import geometry as g
RAYS = ((1,0),(3,1),(1,1),(0,1),(-1,1),(-3,1),(-1,0),(-3,-1),(-1,-1),(0,-1),(1,-1),(3,-1))
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
