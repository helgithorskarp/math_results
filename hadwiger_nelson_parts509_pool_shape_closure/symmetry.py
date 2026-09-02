#!/usr/bin/env python3
"""Exact isometries of the plane preserving L (and U) setwise.

Candidates: rotations by multiples of 30 degrees about the origin and their compositions
with the reflection y -> -y (all of these have matrices over K = Q(sqrt3, sqrt5, sqrt11)).
Everything is exact; an isometry is accepted only if it maps the point set onto itself.
"""
import json, sys
from fractions import Fraction
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from exactgeom import build, scale_points, imul, NB

pts, cp = build()
D, ipts = scale_points(pts)
pool = json.loads((Path.home() / 'math_results' / 'hadwiger_nelson_parts509_s_replacement_budget' / 'pool_S.json').read_text())
U = set(pool['W_S']); L = set(range(374)); S = set(range(374, 509))
key = {}
for i, (x, y) in enumerate(ipts):
    key[(tuple(x), tuple(y))] = i

HALF = Fraction(1, 2)
# sqrt3/2 as a K-element (integer 8-tuple scaled by 2 -> use Fractions)
def fvec(d):
    v = [Fraction(0)] * NB
    for m, c in d.items():
        v[m] = Fraction(c)
    return v

COS = {0: fvec({0: 1}), 30: fvec({1: Fraction(1, 2)}), 60: fvec({0: Fraction(1, 2)}),
       90: fvec({0: 0}), 120: fvec({0: Fraction(-1, 2)}), 150: fvec({1: Fraction(-1, 2)}),
       180: fvec({0: -1}), 210: fvec({1: Fraction(-1, 2)}), 240: fvec({0: Fraction(-1, 2)}),
       270: fvec({0: 0}), 300: fvec({0: Fraction(1, 2)}), 330: fvec({1: Fraction(1, 2)})}
SIN = {0: fvec({0: 0}), 30: fvec({0: Fraction(1, 2)}), 60: fvec({1: Fraction(1, 2)}),
       90: fvec({0: 1}), 120: fvec({1: Fraction(1, 2)}), 150: fvec({0: Fraction(1, 2)}),
       180: fvec({0: 0}), 210: fvec({0: Fraction(-1, 2)}), 240: fvec({1: Fraction(-1, 2)}),
       270: fvec({0: -1}), 300: fvec({1: Fraction(-1, 2)}), 330: fvec({0: Fraction(-1, 2)})}


def fmul(x, y):
    return [Fraction(t) for t in imul([Fraction(a) for a in x], [Fraction(b) for b in y])]


def apply(idx, ang, refl):
    x, y = ipts[idx]
    x = [Fraction(t) for t in x]; y = [Fraction(t) for t in y]
    if refl:
        y = [-t for t in y]
    c, s = COS[ang], SIN[ang]
    nx = [a - b for a, b in zip(fmul(c, x), fmul(s, y))]
    ny = [a + b for a, b in zip(fmul(s, x), fmul(c, y))]
    if any(t.denominator != 1 for t in nx + ny):
        return None
    return (tuple(int(t) for t in nx), tuple(int(t) for t in ny))


found = []
for refl in (False, True):
    for ang in sorted(COS):
        ok = True
        img = {}
        for i in sorted(L):
            k = apply(i, ang, refl)
            if k is None or k not in key:
                ok = False; break
            img[i] = key[k]
        if not ok or set(img.values()) != L:
            continue
        # extend to U
        okU = True
        imgU = {}
        for i in sorted(U):
            k = apply(i, ang, refl)
            if k is None or k not in key:
                okU = False; break
            imgU[i] = key[k]
        preservesU = okU and set(imgU.values()) == U
        preservesS = okU and set(imgU[i] for i in S) == S
        found.append((ang, refl, preservesU, preservesS))
        print(f'isometry rot{ang} refl={refl}: preserves L=True, U={preservesU}, S={preservesS}', flush=True)
print('total isometries preserving L:', len(found))
