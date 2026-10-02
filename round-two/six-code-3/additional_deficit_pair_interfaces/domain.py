"""Literal marked-star domain. No published search program is imported."""
import hashlib
import itertools
import json
from pathlib import Path

FIXTURE_SHA256 = 'c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7'
POINTS = frozenset(range(17))

def require(test, message):
    if not test:
        raise ValueError(message)

def compact(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()

def digest(value):
    return hashlib.sha256(compact(value)).hexdigest()

def mask(points):
    return sum(1 << p for p in points)

def load(path, check_pin=True):
    raw = Path(path).read_bytes()
    if check_pin:
        require(hashlib.sha256(raw).hexdigest() == FIXTURE_SHA256, 'fixture bytes differ from pinned source')
    data = json.loads(raw)
    require(len(data['stars']) == len(data['groups']) == 23, '23 fixture/group records required')
    stars = []
    for i, (blocks, maps) in enumerate(zip(data['stars'], data['groups'])):
        Q = frozenset(frozenset(q) for q in blocks)
        require(len(Q) == len(blocks) == 20, 'twenty distinct quadruples required')
        covered = set()
        rho = [0] * 17
        for q in Q:
            require(len(q) == 4 and q <= POINTS, 'invalid quadruple')
            for p in q:
                rho[p] += 1
            for pair in itertools.combinations(sorted(q), 2):
                require(pair not in covered, 'repeated point pair')
                covered.add(pair)
        delta = tuple(5 - count for count in rho)
        require(min(delta) >= 0 and sum(delta) == 5, 'invalid deficit row')
        high = frozenset(p for p in POINTS if delta[p] > 0)
        low = POINTS - high
        leave = tuple(frozenset(q for q in POINTS - {p} if tuple(sorted((p, q))) not in covered)
                      for p in range(17))
        require(all(len(leave[p]) == 1 and not leave[p] & low for p in low), 'low leave condition')
        group = frozenset(tuple(g) for g in (maps or [list(range(17))]))
        require(len(group) == len(maps or [list(range(17))]), 'duplicated supplied maps')
        require(tuple(range(17)) in group, 'missing group identity')
        for g in group:
            require(len(g) == 17 and frozenset(g) == POINTS, 'nonbijective supplied map')
            require(frozenset(frozenset(g[p] for p in q) for q in Q) == Q, 'not a star automorphism')
        for g in group:
            for h in group:
                require(tuple(g[h[p]] for p in range(17)) in group, 'supplied group not closed')
        first = []
        for u in sorted(high):
            if delta[u] != 1 or sorted(delta[p] for p in high - {u}) != [1, 1, 2] or leave[u] & high:
                continue
            for v in sorted(low):
                y = next(iter(leave[v]))
                if y not in high - {u} or delta[y] != 1 or u in leave[v] or y in leave[u]:
                    continue
                first.append((u, v, y))
        second = []
        if all(delta[p] == 1 for p in high):
            for v in sorted(low):
                x = next(iter(leave[v]))
                for u in sorted(low - {v}):
                    if x in leave[u] or v in leave[u]:
                        continue
                    b = next(iter(leave[u]))
                    second.append((u, v, x, b))
        stars.append(dict(index=i, blocks=Q, delta=delta, high=high, low=low, leave=leave,
                          group=group, first=tuple(sorted(first)), second=tuple(sorted(second))))
    return stars

def orbit_cover(star, kind):
    remaining = set(star[kind])
    out = []
    while remaining:
        mark = min(remaining)
        images = {tuple(g[p] for p in mark) for g in star['group']}
        require(images <= remaining, 'mark orbit not contained in remaining literal domain')
        out.append(dict(representative=list(mark), members=[list(t) for t in sorted(images)]))
        remaining -= images
    return out

def domains(stars):
    rows, first, second = [], [], []
    for star in stars:
        a, z = orbit_cover(star, 'first'), orbit_cover(star, 'second')
        rows.append(dict(fixture=star['index'], first_raw=len(star['first']), second_raw=len(star['second']),
                         first_orbits=a, second_orbits=z, subgroup_order=len(star['group'])))
        first.extend((star['index'], tuple(orb['representative'])) for orb in a)
        second.extend((star['index'], tuple(orb['representative'])) for orb in z)
    return dict(rows=rows, first=first, second=second)

def carrier(stars, first, second):
    fi, (u, v, y) = first
    si, (su, sv, sx, sb) = second
    a, z = stars[fi], stars[si]
    require((u, v, y) in a['first'] and (su, sv, sx, sb) in z['second'], 'invalid product mark')
    target_tails = tuple(sorted(tuple(sorted(q - {y})) for q in a['blocks'] if y in q))
    source_tails = tuple(sorted(tuple(sorted(q - {sx})) for q in z['blocks'] if sx in q))
    require(len(target_tails) == len(source_tails) == 4, 'four common tails required')
    require(len(set(itertools.chain.from_iterable(target_tails))) == 12, 'target tails not disjoint')
    require(len(set(itertools.chain.from_iterable(source_tails))) == 12, 'source tails not disjoint')
    ut = next(t for t in target_tails if u in t)
    us = next(t for t in source_tails if su in t)
    require(all(v not in t for t in target_tails) and all(sv not in t for t in source_tails), 'v lies in common tail')
    uv_quad = [q for q in a['blocks'] if {u, v} <= q]
    require(len(uv_quad) == 1 and y not in uv_quad[0], 'unique private first uv word required')
    forbidden_high_targets = frozenset(p for p in (a['leave'][y] & a['high']) - {u} if a['delta'][p] == 1)
    return dict(first_index=fi, second_index=si, first_mark=(u, v, y), second_mark=(su, sv, sx, sb),
                source_tails=source_tails, target_tails=target_tails, source_u_tail=us, target_u_tail=ut,
                target_private=tuple(sorted(mask(q) for q in a['blocks'] if y not in q)),
                source_private=tuple(sorted(tuple(sorted(q)) for q in z['blocks'] if sx not in q)),
                source_high=z['high'], forbidden_high_targets=forbidden_high_targets,
                first_words=tuple(sorted(mask(q | {17}) for q in a['blocks'])))

def rejection(c, mapping):
    """Sound even for a partial map. Missing images cannot erase a collision."""
    for q in c['source_private']:
        image = mask(mapping[p] for p in q if mapping[p] >= 0)
        if image.bit_count() >= 3 and any((image & w).bit_count() >= 3 for w in c['target_private']):
            return 'private_word_collision'
    return None

def core(c, mapping, stars):
    require(all(p >= 0 for p in mapping) and len(set(mapping)) == 17, 'complete point bijection required')
    u, v, y = c['first_mark']
    su, sv, sx, sb = c['second_mark']
    require(mapping[su] == u and mapping[sv] == v and mapping[sx] == 17, 'distinguished point images')
    require(set(mapping) == set(range(18)) - {y}, 'target complement incorrect')
    mapped = [frozenset(mapping[p] for p in q) | {y} for q in stars[c['second_index']]['blocks']]
    original = [frozenset(q) | {17} for q in stars[c['first_index']]['blocks']]
    words = sorted(set(mask(w) for w in original + mapped))
    require(len(words) == 36, 'star union must have36 words')
    literal = [frozenset(p for p in range(18) if w >> p & 1) for w in words]
    require(all(len(w) == 5 for w in literal), 'core weights')
    require(all(len(a & b) <= 2 for a, b in itertools.combinations(literal, 2)), 'core collision')
    uv_words = [w for w in literal if {u, v} <= w]
    require(len(uv_words) == 2, 'two observed uv words')
    require(rejection(c, mapping) is None, 'core fails a necessary condition')
    return words

def triangle_points(c, mapping):
    """All known-center uncovered deficit triangles, after raw compatibility."""
    return sorted(mapping[p] for p in c['source_high']
                  if mapping[p] in c['forbidden_high_targets'])
