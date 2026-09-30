"""Independent triangle-anchor inventory and bitset clause audits.

This oracle does not enumerate vertex types, D12 matrices, or composed corner
pose pools. It maps every tile triangle bijectively onto every missing triangle.
"""
from itertools import permutations
from geometry import inputs, catalogues, complete, key, IDENTITY, star


def affine(source, target):
    (x, y), (x1, y1), (x2, y2) = source
    (u, v), (u1, v1), (u2, v2) = target
    ax, ay, bx, by = x1-x, y1-y, x2-x, y2-y
    det = ax*by-bx*ay
    assert abs(det) == 1
    u1, v1, u2, v2 = u1-u, v1-v, u2-u, v2-v
    a, b = (u1*by-u2*ay)//det, (-u1*bx+u2*ax)//det
    c, d = (v1*by-v2*ay)//det, (-v1*bx+v2*ax)//det
    assert a*a+a*c+c*c == b*b+b*d+d*d == 1
    assert 2*a*b+a*d+b*c+2*c*d == 1
    return (a, b, c, d), (u-a*x-b*y, v-c*x-d*y)


def apply(v, posekey):
    (a, b, c, d), (x, y) = posekey
    return a*v[0]+b*v[1]+x, c*v[0]+d*v[1]+y


def footprint(shape, posekey):
    return {tuple(sorted(apply(v, posekey) for v in t)) for t in shape}


def inventory(shape, fixed):
    occupied = set().union(*(footprint(shape, key(p)) for p in fixed))
    vertices = set().union(*map(set, shape))
    corners = {apply(v, key(p)) for p in fixed for v in vertices
               if len(star(v) & shape) in (4, 5)}
    missing = set().union(*(star(v)-occupied for v in corners))
    candidates = {affine(t, g) for t in shape for gap in missing for g in permutations(gap)}
    rotated = {}
    out = set()
    for m, shift in candidates:
        if m not in rotated:
            rotated[m] = footprint(shape, (m, (0, 0)))
        x, y = shift
        if all(tuple(sorted((a+x, b+y) for a, b in t)) not in occupied for t in rotated[m]):
            out.add((m, shift))
    return out, len(candidates), len(missing)


def audit_clauses(shape, corners, wide, fixed):
    poses, feet, cs, occupied, clauses = complete(shape, corners, wide, fixed)
    assert occupied == set().union(*(footprint(shape, key(p)) for p in fixed))
    assert all(f == footprint(shape, key(p)) for p, f in zip(poses, feet))
    missing = sorted(set().union(*(star(v)-occupied for v in cs)))
    reference_covers = [[i for i, f in enumerate(feet, 1) if t in f] for t in missing]
    assert clauses[:len(missing)] == reference_covers
    domain = sorted(set().union(*feet))
    index = {t: i for i, t in enumerate(domain)}
    masks = [sum(1 << index[t] for t in f) for f in feet]
    expected = {(-(j+1), -(k+1)) for j, f in enumerate(masks)
                for k, g in enumerate(masks[:j]) if f & g}
    assert len(clauses)-len(missing) == len(expected)
    assert {tuple(c) for c in clauses[len(missing):]} == expected
    return {'poses': len(poses), 'clauses': len(clauses), 'required_cells': len(missing)}


def cardinality_audit():
    """Exhaust every flag assignment; no native solver is used by this audit."""
    from pysat.card import CardEnc, EncType
    flags = list(range(22, 33))
    checked = 0
    for bound in (8, 9):
        card = CardEnc.atleast(lits=flags, bound=bound, top_id=32, encoding=EncType.totalizer)
        for mask in range(1 << len(flags)):
            assigned = {v if mask >> j & 1 else -v for j, v in enumerate(flags)}
            conflict = False
            while True:
                changed = False
                for clause in card.clauses:
                    if any(v in assigned for v in clause):
                        continue
                    rest = [v for v in clause if -v not in assigned]
                    if not rest:
                        conflict = True
                        break
                    if len(rest) == 1:
                        assigned.add(rest[0]); changed = True
                if conflict or not changed:
                    break
            expected = mask.bit_count() >= bound
            if conflict:
                assert not expected
            else:
                assert expected
                positive = {v for v in assigned if v > 0}
                # Unassigned auxiliaries are set false; check the full witness.
                assert all(any(v in positive if v > 0 else -v not in positive
                               for v in clause) for clause in card.clauses)
            checked += 1
    return {'flags': 11, 'bounds': [8, 9], 'assignments': checked,
            'method': 'input unit propagation or directly satisfying auxiliary assignment'}


def run():
    shape, _ = inputs()
    _, _, corners, raw, wide = catalogues(shape)
    counts = []
    for fixed in ([IDENTITY], [IDENTITY, raw[0]]):
        independent, candidates, missing = inventory(shape, fixed)
        production = {key(p) for p in complete(shape, corners, wide, fixed)[0]}
        assert independent == production
        counts.append({'fixed_copies': len(fixed), 'triangle_anchor_candidates': candidates,
                       'missing_cells': missing, 'accepted_poses': len(independent),
                       'clause_audit': audit_clauses(shape, corners, wide, fixed)})
    return {'agent': 'six-heesch-2', 'role': 'researcher', 'independent_inventories': counts,
            'cardinality_audit': cardinality_audit()}


if __name__ == '__main__':
    import json
    print(json.dumps(run(), indent=2, sort_keys=True))
