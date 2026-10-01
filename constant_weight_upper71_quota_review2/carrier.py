"""six-reviewer-2: complete two-anchor carrier for unit high-core e=5,6.

All labeled five-high placements and all possible remaining low-low pairs
are included. No authored negative certificate or carrier code is imported.
"""
from itertools import combinations, permutations
from hashlib import sha256
import json
from incidence import canonical, image, need

PAIRS = tuple(combinations(range(15), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}


def points(mask, n=17):
    return tuple(z for z in range(n) if mask >> z & 1)


def mask(zs):
    return sum(1 << z for z in zs)


def pairmask(word):
    return sum(1 << PINDEX[p] for p in combinations(points(word, 15), 2))


def mapped(word, p):
    return mask(p[z] for z in points(word))


def model(kind, audit_group=True):
    if kind == 0:
        missing = {(i, j) for i in range(5) for j in (i, (i - 1) % 5)}
    elif kind == 1:
        missing = {(i, j) for i in range(3) for j in (i, (i + 1) % 3)} | {(i, j) for i in (3, 4) for j in (3, 4)}
    else:
        raise ValueError('invalid model')
    cells = tuple((i, j) for i in range(5) for j in range(5) if (i, j) not in missing)
    index = {p: z for z, p in enumerate(cells)}
    anchors = tuple(sorted([mask([15] + [z for z, (i, j) in enumerate(cells) if i == r]) for r in range(5)]
                           + [mask([16] + [z for z, (i, j) in enumerate(cells) if j == c]) for c in range(5)]))
    need(len(cells) == 15 and len(set(anchors)) == 10, 'invalid anchor model')
    need(all(w.bit_count() == 4 for w in anchors), 'invalid anchor word')
    need(all((u & v).bit_count() <= 1 for u, v in combinations(anchors, 2)), 'anchor pair conflict')
    covered = 0
    for w in anchors:
        q = pairmask(w)
        need(not covered & q, 'duplicate cell pair in anchors')
        covered |= q
    eligible = ((1 << 105) - 1) ^ covered
    columns = tuple(sorted(mask(zs) for zs in combinations(range(15), 4)
                           if len({cells[z][0] for z in zs}) == 4 and len({cells[z][1] for z in zs}) == 4))
    need(all(pairmask(w) & covered == 0 for w in columns), 'invalid matching column')
    # Literal permutation construction independent of incidence refinement.
    group = []
    cellset = set(cells)
    for a in permutations(range(5)):
        for b in permutations(range(5)):
            for swap in (False, True):
                target = tuple((b[j], a[i]) if swap else (a[i], b[j]) for i, j in cells)
                if set(target) == cellset:
                    p = tuple(index[t] for t in target) + ((16, 15) if swap else (15, 16))
                    need(image(anchors, p) == anchors, 'false literal anchor automorphism')
                    group.append(p)
    group = tuple(sorted(set(group)))
    intrinsic = canonical(anchors, 17, (tuple(range(15)), (15, 16))) if audit_group else None
    if intrinsic is not None:
        need(group == intrinsic['automorphisms'], 'literal/incidence group mismatch')
    return dict(kind=kind, cells=cells, anchors=anchors, columns=columns,
                covered=covered, eligible=eligible, group=group,
                group_audit={k: intrinsic[k] for k in ('states', 'leaves', 'order')} if intrinsic else None)


def raw_cases(m, extra):
    """extra=0: e=5; extra=1: e=6. Both chosen anchors are low."""
    need(extra in (0, 1), 'invalid remaining low-edge count')
    result = set()
    for hs in combinations(range(15), 5):
        h = mask(hs)
        if not extra:
            result.add((h, 0))
        else:
            lows = [z for z in range(15) if not h >> z & 1]
            for u, v in combinations(lows, 2):
                if m['eligible'] >> PINDEX[u, v] & 1:
                    result.add((h, (1 << u) | (1 << v)))
    return result


def orbits(m, extra):
    todo = raw_cases(m, extra)
    total = len(todo)
    result = []
    mass = 0
    for rep in sorted(todo):
        if rep not in todo:
            continue
        orbit = {(mapped(rep[0], p), mapped(rep[1], p)) for p in m['group']}
        need(orbit <= todo and rep == min(orbit), 'raw orbit missing, overlapping or noncanonical')
        stabilizer = sum((mapped(rep[0], p), mapped(rep[1], p)) == rep for p in m['group'])
        need(stabilizer * len(orbit) == len(m['group']), 'orbit/stabilizer mass mismatch')
        todo.difference_update(orbit)
        mass += len(orbit)
        result.append(dict(high=rep[0], low_edge=rep[1], mass=len(orbit), stabilizer=stabilizer))
    need(mass == total, 'incomplete raw orbit mass')
    return result, total


def problem(m, case, extra):
    h, edge = case['high'], case['low_edge']
    high_pairs = pairmask(h)
    anchor_high = (m['covered'] & high_pairs).bit_count()
    budget = 5 - extra - anchor_high
    forbidden = pairmask(edge)
    lows = ((1 << 15) - 1) ^ h
    mandatory = m['eligible'] & pairmask(lows) & ~forbidden
    columns = tuple(w for w in m['columns'] if not pairmask(w) & forbidden
                    and (pairmask(w) & high_pairs).bit_count() <= budget)
    return dict(quotas=tuple(2 if h >> z & 1 else 3 for z in range(15)),
                budget=budget, columns=columns, mandatory=mandatory, high=h)


def build():
    models = [model(i) for i in range(2)]
    cases, summary = [], []
    for m in models:
        for extra in (0, 1):
            reps, raw = orbits(m, extra)
            direct = direct_mass = 0
            for rep in reps:
                p = problem(m, rep, extra)
                if p['budget'] < 0:
                    direct += 1
                    direct_mass += rep['mass']
                else:
                    cases.append(dict(model=m['kind'], extra=extra, **{**rep, **p}))
            summary.append(dict(model=m['kind'], extra=extra, raw=raw, orbits=len(reps),
                                direct=direct, direct_mass=direct_mass, quota=len(reps)-direct,
                                group_order=len(m['group']), candidates=len(m['columns']), group_audit=m['group_audit']))
    payload = json.dumps(dict(summary=summary, cases=cases), sort_keys=True, separators=(',', ':')).encode()
    return models, cases, dict(summary=summary, cases=len(cases), stream_sha256=sha256(payload).hexdigest())


def write_native(cases, path):
    with open(path, 'w') as f:
        f.write(str(len(cases)) + '\n')
        for c in cases:
            cols = c['columns']; q = c['quotas']; r = c['mandatory']
            f.write(f"{len(cols)} {c['high']} {c['budget']} {r & ((1 << 64)-1)} {r >> 64}\n")
            f.write(' '.join(map(str, q)) + '\n')
            f.write(' '.join(map(str, cols)) + '\n')


if __name__ == '__main__':
    import sys
    models, cases, summary = build()
    write_native(cases, sys.argv[1])
    print(json.dumps(summary, indent=2))
