"""Pinned inventories and exact arithmetic for the four rotation-only systems."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'hadwiger_nelson_radix_reflection_pair_stratum'))
import geometry as G
V, X = G.V, G.X
PAIRS = [[318,340,7,32,10], [318,341,7,32,10],
         [319,340,7,32,10], [319,341,7,32,10]]
INPUT_SHA = '8810828aa75a2d4a83cc18322d0312f58cb484b3683869eee38b63927d9246c1'
CURVE_SHA = '85c286422c01bcb6ebb244186032bc607984471bc2b705ef7247084dd7c33db9'


def coefficients(poly):
    return [str(c) for c in poly]


def coordinate_digest(points):
    return X.digest([[coefficients(x), coefficients(y)] for x,y in points])


def inventory():
    _, fs, circle, monos, rowids = V.reconstruct_inventory()
    X.need(X.digest(fs) == CURVE_SHA, 'pinned reviewed norm-curve inventory')
    ident = tuple(range(len(fs)))
    lookup = {G.primitive_bivariate({(i,j):c for i,j,c in f}):k
              for k,f in enumerate(fs)}
    rot = tuple(lookup[G.transform(f,True)] for f in fs)
    conj = tuple(lookup[G.transform(f,False)] for f in fs)
    rot2 = G.compose(rot,rot)
    group = (ident,rot,rot2,conj,G.compose(rot,conj),G.compose(rot2,conj))
    X.need(len(set(group)) == 6 and
           all(G.compose(g,h) in group for g in group for h in group),
           'complete named D3 action')
    # These elementary digit identities establish the physical isometries.
    power = (1,0)
    shifts = []
    for _ in range(5):
        points = [V.e_mul(power,d) for d in V.DIGITS]
        candidates = [s for s in points if
                      {(a-s[0],b-s[1]) for a,b in points} == set(V.DIGITS)]
        X.need(len(candidates) == 1, 'rotation translates each digit triangle')
        shifts.append(candidates[0]); power = V.e_mul(power,(-1,1))
    X.need(shifts == [(0,0),(-1,0),(0,-1),(0,0),(-1,0)],
           'physical A5 rotation identity')
    X.need({V.e_mul((0,1),(a+b,-b)) for a,b in V.DIGITS} == set(V.DIGITS),
           'physical A5 conjugation identity')
    images = set()
    for a,b,mask,bound,allowance in PAIRS:
        orbit = [tuple(sorted((g[a],g[b]))) for g in group]
        actual = sum(1<<j for j,p in enumerate(orbit) if p == (a,b))
        X.need(min(orbit) == (a,b) and actual == mask == 7,
               'canonical pair with exactly the three rotations as stabilizer')
        X.need(bound == max(i+j for i,j,c in fs[a]) *
               max(i+j for i,j,c in fs[b]) // 2 and allowance == bound//3,
               'inherited intersection allowance')
        images.update(orbit)
    X.need(len(images) == 8, 'all eight expanded pair conjunctions')
    return fs, circle, monos, rowids, sorted(images)
