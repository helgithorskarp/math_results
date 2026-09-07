#!/usr/bin/env python3
"""Integer producer for the explicit de Grey construction and exact sections."""
import json
import math
from collections import defaultdict
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = (1, 3, 5, 15, 11, 33, 55, 165, 7, 21, 35, 105, 77, 231, 385, 1155)
SCALE = 3072


def require(test, message):
    if not test:
        raise ValueError(message)


def plus(x, y):
    return tuple(a+b for a, b in zip(x, y))


def minus(x, y):
    return tuple(a-b for a, b in zip(x, y))


def scale(x, a):
    return tuple(a*b for b in x)


def rootmul(x, k):
    return tuple(x[i ^ k] * D[(i ^ k) & k] for i in range(16))


def rotate60(p):
    a, b, c, d = p
    q = (a-3*c, b-d, a+c, 3*b+d)
    require(all(v % 2 == 0 for v in q), 'nonintegral seed rotation')
    return tuple(v//2 for v in q)


def unpack(p):
    a, b, c, d = p
    x, y = [0]*16, [0]*16
    x[0], x[5], y[1], y[4] = a, b, c, d
    return tuple(x), tuple(y)


def outside_image(p):
    anchor = (-2*SCALE,) + (0,)*15
    x, y = minus(p[:16], anchor), p[16:]
    q = (plus(minus(scale(x, 31), scale(rootmul(y, 8), 3)), scale(anchor, 32))
         + plus(scale(rootmul(x, 8), 3), scale(y, 31)))
    require(all(v % 32 == 0 for v in q), 'outer coordinate denominator')
    return tuple(v//32 for v in q)


def construction():
    data = json.loads((HERE/'seeds.json').read_text())
    require(data['scale'] == 12 and len(data['points']) == 39, 'seed format')
    sb = set()
    for a, b, c, d in data['points']:
        for sign in (-1, 1):
            p = (a, b, sign*c, sign*d)
            for _ in range(6):
                sb.add(p)
                p = rotate60(p)
    require(len(sb) == 397, 'Sb order')
    sa = sb - {(-4, 0, 0, 0), (4, 0, 0, 0)}
    require(len(sa) == 395, 'Sa order')
    half96 = set()
    for p in sa:
        x, y = unpack(p)
        half96.add((scale(x, 8), scale(y, 8)))
    for p in sb:
        x, y = unpack(p)
        half96.add((minus(scale(x, 7), rootmul(y, 3)), plus(rootmul(x, 3), scale(y, 7))))
    half = {scale(x, 32)+scale(y, 32) for x, y in half96}
    require(len(half) == 791, 'half order')
    points = sorted(half | {outside_image(p) for p in half})
    require(len(points) == 1581, 'host order')
    labels = {p: i for i, p in enumerate(points)}
    return points, sorted(labels[p] for p in half)


def exact_edges(points):
    columns = [i for i in range(32) if any(p[i] for p in points)]
    weights = [D[i % 16] for i in columns]
    edges, survivors = [], 0
    for u, a in enumerate(points):
        for v in range(u):
            b = points[v]
            delta = [a[i]-b[i] for i in columns]
            # This is the exact constant coefficient, not a real-norm bound.
            if sum(w*z*z for w, z in zip(weights, delta)) != SCALE*SCALE:
                continue
            survivors += 1
            d = [a[i]-b[i] for i in range(32)]
            out = [0]*16
            for start in (0, 16):
                for i in range(16):
                    if d[start+i]:
                        for j in range(i+1, 16):
                            if d[start+j]:
                                out[i ^ j] += 2*d[start+i]*d[start+j]*D[i & j]
            if not any(out):
                edges.append((v, u))
    return sorted(edges), survivors


def residues(points):
    columns = [i for i in range(16) if any(p[i] for p in points)]
    gcds = [math.gcd(*(p[i] for p in points)) for i in columns]
    values = [tuple(p[i]//g % 3 for i, g in zip(columns, gcds)) for p in points]
    require(len(columns) == 8, 'residue dimension')
    return columns, gcds, values


def section_family(values, target=508):
    classes = defaultdict(int)
    for v, r in enumerate(values):
        classes[r] |= 1 << v
    classes = sorted(classes.items())
    normals = [a for a in product(range(3), repeat=len(values[0]))
               if next((t for t in a if t), 0) == 1]
    supports = {}
    counts = [0, 0, 0]
    for a in normals:
        masks = [0, 0, 0]
        for r, mask in classes:
            masks[sum(x*y for x, y in zip(a, r)) % 3] |= mask
        for b, mask in enumerate(masks):
            if mask.bit_count() <= target:
                counts[b] += 1
                supports.setdefault(mask, []).append((a, b))
    return supports, counts
