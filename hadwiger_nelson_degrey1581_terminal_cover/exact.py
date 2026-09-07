#!/usr/bin/env python3
"""Exact radical geometry reused from the independent residue-section audit."""
import argparse
import hashlib
import json
import math
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAD = (1, 3, 5, 15, 11, 33, 55, 165, 7, 21, 35, 105, 77, 231, 385, 1155)
SCALE = 3072
MODULUS = 2269
ROOTS = {3: 931, 5: 158, 11: 418, 7: 1063}


def demand(test, message):
    if not test:
        raise ValueError(message)


def clean(a):
    return {d: v for d, v in a.items() if v}


def add(a, b):
    c = a.copy()
    for d, v in b.items():
        c[d] = c.get(d, 0) + v
    return clean(c)


def neg(a):
    return {d: -v for d, v in a.items()}


def mul(a, b):
    c = {}
    for d, u in a.items():
        for e, v in b.items():
            common = math.gcd(d, e)
            radical = d*e//(common*common)
            c[radical] = c.get(radical, 0) + u*v*common
    return clean(c)


def turn(p, r):
    x, y = p
    a, b = r
    return add(mul(x, a), neg(mul(y, b))), add(mul(x, b), mul(y, a))


def key(p):
    return tuple(F(c.get(d, 0)) for c in p for d in RAD)


def unkey(p):
    return tuple({d: p[start+i] for i, d in enumerate(RAD) if p[start+i]}
                 for start in (0, 16))


def reconstruct():
    seeds = json.loads((HERE/'seeds.json').read_text())
    demand(seeds['scale'] == 12 and len(seeds['points']) == 39, 'seed format')
    # Twelve explicit matrices, independently of the producer's iterative orbit.
    rotations = [({1: F(1)}, {}), ({1: F(1, 2)}, {3: F(1, 2)}),
                 ({1: F(-1, 2)}, {3: F(1, 2)}), ({1: F(-1)}, {}),
                 ({1: F(-1, 2)}, {3: F(-1, 2)}), ({1: F(1, 2)}, {3: F(-1, 2)})]
    sb = set()
    for row in seeds['points']:
        demand(len(row) == 4 and all(type(v) is int for v in row), 'seed row')
        a, b, c, d = row
        p = clean({1: F(a, 12), 33: F(b, 12)}), clean({3: F(c, 12), 11: F(d, 12)})
        for reflection in (p, (p[0], neg(p[1]))):
            for rotation in rotations:
                sb.add(key(turn(reflection, rotation)))
    sa = sb - {key(({1: F(1, 3)}, {})), key(({1: F(-1, 3)}, {}))}
    inner = ({1: F(7, 8)}, {15: F(1, 8)})
    half = sa | {key(turn(unkey(p), inner)) for p in sb}
    outer = ({1: F(31, 32)}, {7: F(3, 32)})
    image = set()
    for p in half:
        x, y = unkey(p)
        qx, qy = turn((add(x, {1: F(2)}), y), outer)
        image.add(key((add(qx, {1: F(-2)}), qy)))
    scaled = [tuple(v*SCALE for v in p) for p in half | image]
    demand(all(v.denominator == 1 for p in scaled for v in p), 'coordinate denominator')
    points = sorted(tuple(int(v) for v in p) for p in scaled)
    demand((len(sb), len(sa), len(half), len(points)) == (397, 395, 791, 1581), 'construction counts')
    return points


def edge_census(points):
    # A homomorphism from the integer radical algebra to Z/2269Z supplies only
    # a necessary test. Every surviving pair is expanded exactly afterwards.
    demand(all(r*r % MODULUS == d for d, r in ROOTS.items()), 'invalid modular roots')
    images = []
    for radical in RAD:
        image, rest = 1, radical
        for d, r in ROOTS.items():
            if rest % d == 0:
                image = image*r % MODULUS
                rest //= d
        demand(rest == 1, 'unrepresented radical')
        images.append(image)
    projected = [(sum(p[i]*images[i] for i in range(16)) % MODULUS,
                  sum(p[16+i]*images[i] for i in range(16)) % MODULUS) for p in points]
    edges, survivors = [], 0
    for u, (x, y) in enumerate(projected):
        for v in range(u):
            xx, yy = projected[v]
            if ((x-xx)**2 + (y-yy)**2 - SCALE*SCALE) % MODULUS:
                continue
            survivors += 1
            norm = {}
            for start in (0, 16):
                delta = {d: points[u][start+i]-points[v][start+i]
                         for i, d in enumerate(RAD) if points[u][start+i] != points[v][start+i]}
                norm = add(norm, mul(delta, delta))
            if norm == {1: SCALE*SCALE}:
                edges.append((v, u))
    return sorted(edges), survivors
