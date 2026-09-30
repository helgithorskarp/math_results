"""Exact unmarked214-iamond and complete reentrant-corner pose pools.

Agent six-heesch-2, researcher. The geometric mesh primitives and the known
131-copy fixture are pinned from the earlier hexapillar reproduction.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
PRIOR = BASE.parent / 'heesch_polyiamond_hexapillar'
PINS = {
    'check.py': '820808ac68609cad81bc14e4cba39d836ae635685d69a69142c9f84db5049b26',
    'generate.py': 'cbe4fe40bd3f59b1f6c5febb6b69ea1b1261b485a50e9cb02bbeeced25079439',
    'marked_fixture.json': 'd857774a28daa5e8f28e45a4ce711cc45ebc11cb759904fa98309122892aed0a',
    'coronas.json': '2676333fd8e15d4c3a6b073cd251204518322d778af755615c65481541f3ce18',
}
for name, expected in PINS.items():
    assert hashlib.sha256((PRIOR / name).read_bytes()).hexdigest() == expected, name


def module(name):
    spec = importlib.util.spec_from_file_location('deficit_' + name, PRIOR / (name + '.py'))
    out = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(out)
    return out


check = module('check')
generate = module('generate')
cell, mesh, star = check.cell, check.mesh, check.star
IDENTITY = {'matrix': [1, 0, 0, 1], 'translation': [0, 0]}


def inputs():
    w = json.loads((PRIOR / 'marked_fixture.json').read_text())
    side = 3
    shape = {generate.translated(t, generate.center(c, side))
             for c in w['tile'] for t in generate.hexagon(side)}
    ports = sorted((tuple(c), (c[0]+dx, c[1]+dy)) for c in w['tile']
                   for dx, dy in generate.DIRECTIONS if [c[0]+dx, c[1]+dy] not in w['tile'])
    feature = {generate.up(0, 2), generate.up(2, 0)}
    outside = {tuple(sorted((side-y, side-x) for x, y in t)) for t in feature}
    assert len(ports) == len(w['signs']) == 18
    for (c, n), sign in zip(ports, w['signs']):
        if not sign:
            continue
        direction = generate.DIRECTIONS.index((n[0]-c[0], n[1]-c[1]))
        changed = {generate.translated(tuple(sorted(generate.fine_motion(v, False, direction)
                                                   for v in t)), generate.center(c, side))
                   for t in (feature if sign == 1 else outside)}
        if sign == 1:
            assert changed <= shape
            shape -= changed
        else:
            assert changed.isdisjoint(shape)
            shape |= changed
    assert len(shape) == 214
    raw = json.dumps({'triangles': sorted(shape)}, separators=(',', ':')) + '\n'
    assert hashlib.sha256(raw.encode()).hexdigest() == '8d42c74f1e219ae37f34d5706f83ab4eb20e921ada66d70090c8a539f481335f'
    return shape, json.loads((PRIOR / 'coronas.json').read_text())['placements']


def key(p):
    return tuple(p['matrix']), tuple(p['translation'])


def point(v, p):
    a, b, c, d = p['matrix']; x, y = p['translation']
    return a*v[0]+b*v[1]+x, c*v[0]+d*v[1]+y


def move(t, p):
    return tuple(sorted(point(v, p) for v in t))


def compose(p, q):
    a, b, c, d = p['matrix']; e, f, g, h = q['matrix']
    return {'matrix': [a*e+b*g, a*f+b*h, c*e+d*g, c*f+d*h],
            'translation': list(point(q['translation'], p))}


def inverse(p):
    a, b, c, d = p['matrix']; x, y = p['translation']; det = a*d-b*c
    assert abs(det) == 1
    q = {'matrix': [d//det, -b//det, -c//det, a//det], 'translation': [0, 0]}
    q['translation'] = list(point((-x, -y), q))
    assert key(compose(p, q)) == key(IDENTITY)
    return q


def matrices():
    out = []
    for reflected in (False, True):
        for turns in range(6):
            def f(x, y):
                if reflected:
                    x, y = y, x
                for _ in range(turns):
                    x, y = -y, x+y
                return x, y
            a, c = f(1, 0); b, d = f(0, 1)
            out.append((a, b, c, d))
    assert len(set(out)) == 12
    return out


def catalogues(shape):
    _, vertices, _ = mesh(shape)
    pockets = sorted(v for v in vertices if len(star(v) & shape) == 5)
    tips = sorted(v for v in vertices if len(star(v) & shape) == 1)
    reentrant = sorted(v for v in vertices if len(star(v) & shape) in (4, 5))
    convex = sorted(v for v in vertices if len(star(v) & shape) in (1, 2))
    narrow, wide = {}, {}
    for v in pockets:
        gap, = star(v) - shape
        for w in tips:
            triangle, = star(w) & shape
            for m in matrices():
                a, b, c, d = m
                p = {'matrix': list(m), 'translation': [v[0]-a*w[0]-b*w[1], v[1]-c*w[0]-d*w[1]]}
                if move(triangle, p) == gap and shape.isdisjoint({move(t, p) for t in shape}):
                    narrow[key(p)] = p
    for m in matrices():
        rotated_pose = {'matrix': list(m), 'translation': [0, 0]}
        rotated = {move(t, rotated_pose) for t in shape}
        for v in reentrant:
            gap = star(v) - shape
            for w in convex:
                u = point(w, rotated_pose)
                p = {'matrix': list(m), 'translation': [v[0]-u[0], v[1]-u[1]]}
                sector = {move(t, p) for t in star(w) & shape}
                if not sector <= gap:
                    continue
                x, y = p['translation']
                f = {tuple(sorted((a+x, b+y) for a, b in t)) for t in rotated}
                if shape.isdisjoint(f):
                    assert star(v) & f == sector
                    wide[key(p)] = p
    assert set(narrow) <= set(wide)
    assert (len(pockets), len(tips), len(reentrant), len(narrow), len(wide)) == (8, 11, 33, 59, 475)
    return pockets, tips, reentrant, [narrow[k] for k in sorted(narrow)], [wide[k] for k in sorted(wide)]


def complete(shape, reentrant, raw, fixed):
    occupied = set()
    for p in fixed:
        f = {move(t, p) for t in shape}
        assert occupied.isdisjoint(f)
        occupied.update(f)
    pool = {key(compose(p, q)): compose(p, q) for p in fixed for q in raw}
    for p in fixed:
        pool.pop(key(p), None)
    poses, footprints = [], []
    for k in sorted(pool):
        p = pool[k]; f = {move(t, p) for t in shape}
        if occupied.isdisjoint(f):
            poses.append(p); footprints.append(f)
    corners = [point(v, p) for p in fixed for v in reentrant]
    assert len(set(corners)) == len(corners)
    missing = set()
    for v in corners:
        gap = star(v) - occupied
        assert len(gap) <= 2
        missing.update(gap)
    clauses = [[i for i, f in enumerate(footprints, 1) if t in f] for t in sorted(missing)]
    owners, conflicts = {}, set()
    for j, f in enumerate(footprints):
        for t in f:
            previous = owners.setdefault(t, [])
            conflicts.update((j, k) for k in previous)
            previous.append(j)
    clauses.extend([-(j+1), -(k+1)] for j, k in sorted(conflicts))
    return poses, footprints, corners, occupied, clauses
