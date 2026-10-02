"""Literal shifted-pair prefix, original demands and proved E1 cuts."""
import json
from pathlib import Path

import deps
import strip_contact_reader as R
import strip_parametric_geometry as G
from strip_point_suppliers import IDENTITY

HERE = Path(__file__).absolute().parent
SHIFT = ((1, 0, 0, 1), (0, 6), (-1, 4))
HALFTURN = ((-1, 0, 0, -1), (0, 5), (0, 3))
P = ((2, -3, 1, -2), (3, 6), (2, 5))
ANGLE = ((2, -3, 1, -2), (0, 5), (0, 3))
FIXED = (IDENTITY, SHIFT, HALFTURN, P)
POINTS = (((0, 4), (0, 6)), ((0, 5), (0, 6)))


def models(entries):
    all_entries = list(entries)
    for directory in ('strip-e2-branches', 'strip-e2-forced-p'):
        all_entries += json.loads((HERE.parent/directory/'inputs.json').read_text())['cases']
    return tuple(R.freeze(e['pose']) for e in all_entries)


def bad(relative, excluded):
    # 9404's angle obstruction and full shifted-side E1 classification.
    rows = [G.allowed(relative, (ANGLE, G.inverse(ANGLE)))]
    for pose in (relative, G.inverse(relative)):
        if pose[0] == IDENTITY[0]:
            endpoints = G.either(G.atom('eq', G.sub(pose[2], (-1, 3))),
                                G.atom('eq', G.sub(pose[2], (-1, 4))))
            rows.append(G.both(G.atom('eq', G.sub(pose[1], (0, 6))), G.neg(endpoints)))
    rows.append(G.either(G.allowed(relative, excluded), G.allowed(G.inverse(relative), excluded)))
    return G.both(G.touching(relative), G.either(*rows))


def predicates(atlas, entries):
    excluded = models(entries)
    coverage = [[G.point_membership(g, p) for p in POINTS] for g in atlas]
    eligibility = [G.both(*(
        G.both(G.neg(G.intersection(G.relative(f, g))),
               G.neg(bad(G.relative(f, g), excluded))) for f in FIXED)) for g in atlas]
    # Physical overlap alone closes the final two-demand collar. E1 cuts
    # between added suppliers are deliberately unnecessary in this relaxation.
    clashes = {(i, j): G.intersection(G.relative(g, h))
               for j, h in enumerate(atlas) for i, g in enumerate(atlas[:j])}
    demanded = []
    for point in POINTS:
        occupied = G.either(*(G.point_membership(f, point) for f in FIXED))
        near_original = G.either(*(
            G.point_membership(f, (G.sub(point[0], (0, u)), G.sub(point[1], (0, v))))
            for f in FIXED[:2] for u, v in G.UV_DIRS))
        demanded.append(G.both(G.neg(occupied), near_original))
    return coverage, eligibility, clashes, demanded


def flat(rows):
    coverage, eligibility, clashes, demanded = rows
    return [p for row in coverage for p in row]+eligibility+list(clashes.values())+demanded
