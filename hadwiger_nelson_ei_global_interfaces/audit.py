"""Independent four-coordinate reconstruction; no generic radical imports.

[a,b,c,d] means (a sqrt(3)+b sqrt(11), c+d sqrt(33)), before /36.
Isometry multipliers have form u+v sqrt(33)+i(w sqrt(3)+x sqrt(11)).
"""
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(folder, name):
    return json.loads((REPO / folder / name).read_text())


def distance(p, q):
    a, b, c, d = (x-y for x, y in zip(p, q))
    return 3*a*a + 11*b*b + c*c + 33*d*d, 2*(a*b+c*d)


def transform(s0, s1, t0, t1, points, reflect=False):
    def reflect_point(p):
        a, b, c, d = p
        return a, b, -c, -d
    if reflect:
        s0, s1 = reflect_point(s0), reflect_point(s1)
        points = list(map(reflect_point, points))
    a, b, c, d = (x-y for x, y in zip(s1, s0))
    A, B, C, D = (x-y for x, y in zip(t1, t0))
    length, cross = distance(s0, s1)
    require(cross == 0 and length > 0 and distance(t0, t1) == (length, 0), 'anchor lengths')
    u = F(3*A*a + 11*B*b + C*c + 33*D*d, length)
    v = F(A*b + B*a + C*d + D*c, length)
    w = F(C*a + 11*D*b - A*c - 11*B*d, length)
    x = F(C*b + 3*D*a - B*c - 3*A*d, length)
    require(u*u+33*v*v+3*w*w+11*x*x == 1 and u*v+w*x == 0, 'multiplier norm')
    def linear(p):
        a, b, c, d = p
        return (u*a+11*v*b-w*c-11*x*d, u*b+3*v*a-x*c-3*w*d,
                u*c+33*v*d+3*w*a+11*x*b, u*d+v*c+w*b+x*a)
    origin = linear(s0)
    return [tuple(q+t-o for q, t, o in zip(linear(p), t0, origin)) for p in points]


def half_layer():
    folder = 'hadwiger_nelson_ei_interface_minima'
    g40 = list(map(tuple, read(folder, 'g40.json')))
    g49 = list(map(tuple, read(folder, 'g49.json')))
    cert = read(folder, 'certificate.json')
    pairs = [p for p in combinations(range(40), 2) if distance(*(g40[v] for v in p)) == (4752, 0)]
    triangles = [t for t in combinations(range(49), 3)
                 if all(distance(g49[i], g49[j]) == (432, 0) for i, j in combinations(t, 2))]
    selected = set(cert['g40']['essential']) | {v for k, v in enumerate(cert['g40']['optional']) if 1682 >> k & 1}
    union = set(g40)
    targets = set()
    for k in sorted(selected):
        i, j = pairs[k]
        placed = transform(g49[0], g49[1], g40[i], g40[j], g49)
        union.update(placed)
        for k in cert['g49']['essential']:
            targets.add(tuple(sorted(placed[v] for v in triangles[k])))
    require(all(v.denominator == 1 for p in union for v in p), 'unexpected denominators')
    points = sorted(tuple(map(int, p)) for p in union)
    labels = {p: i for i, p in enumerate(points)}
    edges = [(i, j) for i, j in combinations(range(len(points)), 2) if distance(points[i], points[j]) == (1296, 0)]
    return points, sorted(tuple(labels[p] for p in t) for t in targets), [labels[p] for p in g40[:2]], edges


def forcer():
    folder = 'hadwiger_nelson_small_triangle_forcer375'
    reference = set()
    for p in read(folder, 'appendix.json'):
        for _ in range(3):
            a, b, c, d = p
            reference.add(tuple(p))
            reference.add((-a, -b, c, d))
            p = (F(-a-c, 2), F(-b-3*d, 2), F(3*a-c, 2), F(b-d, 2))
    terminals = [(0, 0, 12, 0), (-6, 0, -6, 0), (6, 0, -6, 0)]
    reference = terminals + sorted(reference-set(terminals))
    require(len(reference) == 627, 'reference order')
    return [reference[i] for i in read(folder, 'certificate.json')['retained_reference_indices']]


def completed_half(points, triangles):
    gadget = forcer()
    union = set(points)
    for triangle in triangles:
        target = [points[v] for v in triangle]
        placed = transform(gadget[0], gadget[1], target[0], target[1], gadget)
        if placed[2] != target[2]:
            placed = transform(gadget[0], gadget[1], target[0], target[1], gadget, True)
        require(placed[:3] == target and len(set(placed)) == 375, 'placed gadget')
        union.update(placed)
    require(all(v.denominator == 1 for p in union for v in p), 'completed denominators')
    return sorted(tuple(map(int, p)) for p in union)
