"""Exact necessary charge selectors and conditional saturation formulae."""
from geometry import IDENTITY, key, point, compose, inverse, move, star


def text_cnf(nv, clauses):
    return f'p cnf {nv} {len(clauses)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in clauses)


def interior_constraints(poses, fixed, raw_keys, allowed_keys):
    def forbidden(p, q):
        relative = key(compose(inverse(p), q))
        return relative in raw_keys and relative not in allowed_keys
    def bad(p, q):
        return forbidden(p, q) or forbidden(q, p)
    clauses = []
    for j, p in enumerate(fixed):
        if any(bad(p, q) for q in fixed[:j]):
            clauses.append([])
    for j, p in enumerate(poses):
        if any(bad(p, q) for q in fixed):
            clauses.append([-(j+1)])
        for k, q in enumerate(poses[:j]):
            if bad(p, q):
                clauses.append([-(j+1), -(k+1)])
    return clauses


def selector(shape, tips, raw, admitted, bound):
    from pysat.card import CardEnc, EncType
    raw_keys = {key(p) for p in raw}
    allowed = {key(p) for i, p in enumerate(raw, 1) if i in admitted}
    inv = {key(inverse(p)): inverse(p) for i, p in enumerate(raw, 1) if i in admitted}
    poses = [inv[k] for k in sorted(inv)]
    feet = [{move(t, p) for t in shape} for p in poses]
    assert all(shape.isdisjoint(f) for f in feet)
    clauses = interior_constraints(poses, [IDENTITY], raw_keys, allowed)
    coverings = []
    for j, v in enumerate(tips):
        assert len(star(v) & shape) == 1
        covers = {i for i, f in enumerate(feet, 1) if len(star(v) & f) == 5}
        coverings.append(covers)
        flag = len(poses) + j + 1
        clauses.append([-flag, *sorted(covers)])
        clauses.extend([-i, flag] for i in sorted(covers))
    for j, f in enumerate(feet):
        for k, g in enumerate(feet[:j]):
            if not f.isdisjoint(g):
                clauses.append([-(j+1), -(k+1)])
    flags = list(range(len(poses)+1, len(poses)+len(tips)+1))
    card = CardEnc.atleast(lits=flags, bound=bound, top_id=max(flags), encoding=EncType.totalizer)
    return poses, feet, coverings, clauses + card.clauses, max(max(flags), card.nv)


def saturation(shape, tips, raw, allowed_indices, fixed, bound=8):
    from pysat.card import CardEnc, EncType
    raw_keys = {key(p) for p in raw}
    allowed_keys = {key(p) for i, p in enumerate(raw, 1) if i in allowed_indices}
    active = [inverse(p) for i, p in enumerate(raw, 1) if i in allowed_indices]
    fixedfeet = [{move(t, p) for t in shape} for p in fixed]
    occupied = set()
    for f in fixedfeet:
        assert occupied.isdisjoint(f)
        occupied.update(f)
    pool = {key(compose(p, q)): compose(p, q) for p in fixed for q in active}
    for p in fixed:
        pool.pop(key(p), None)
    poses, feet = [], []
    for k in sorted(pool):
        p = pool[k]; f = {move(t, p) for t in shape}
        if occupied.isdisjoint(f):
            poses.append(p); feet.append(f)
    clauses = interior_constraints(poses, fixed, raw_keys, allowed_keys)
    for j, f in enumerate(feet):
        for k, g in enumerate(feet[:j]):
            if not f.isdisjoint(g):
                clauses.append([-(j+1), -(k+1)])
    nv = len(poses) + len(fixed)*len(tips)
    coverings = []
    for k, p in enumerate(fixed):
        flags, row = [], []
        for j, tip in enumerate(tips):
            v = point(tip, p)
            assert len(star(v) & fixedfeet[k]) == 1
            auto = any(len(star(v) & f) == 5 for i, f in enumerate(fixedfeet) if i != k)
            covers = {i for i, f in enumerate(feet, 1) if len(star(v) & f) == 5}
            flag = len(poses) + k*len(tips) + j + 1
            flags.append(flag)
            if auto:
                assert not covers
                clauses.append([flag])
            else:
                clauses.append([-flag, *sorted(covers)])
                clauses.extend([-i, flag] for i in sorted(covers))
            row.append((auto, covers))
        card = CardEnc.atleast(lits=flags, bound=bound, top_id=nv, encoding=EncType.totalizer)
        nv = max(nv, card.nv)
        clauses += card.clauses
        coverings.append(row)
    return poses, feet, occupied, clauses, nv, coverings
