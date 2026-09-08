"""Definition-level integer arithmetic in an eight-element radical basis.

The bit positions correspond to sqrt(3), sqrt(11), sqrt(247). Coordinates
below are physical coordinates multiplied by 4608. Python integers are
unbounded; the rational coefficient filter never uses floating point.
"""
from itertools import combinations
WEIGHTS = (1, 3, 11, 33, 247, 741, 2717, 8151)
SCALE = 4608

def point(row, rotated=False):
    a, b, c, d = row
    if not rotated:
        return ((0, 128 * a, 128 * b, 0, 0, 0, 0, 0), (128 * c, 0, 0, 128 * d, 0, 0, 0, 0))
    return ((0, 119 * a, 119 * b, 0, -3 * c, 0, 0, -3 * d), (119 * c, 0, 0, 119 * d, 0, 3 * a, 3 * b, 0))

def square(axis):
    out = [0] * 8
    for i, x in enumerate(axis):
        if not x:
            continue
        for j, y in enumerate(axis):
            if y:
                out[i ^ j] += WEIGHTS[i & j] * x * y
    return out

def distance(p, q):
    d = [tuple((x - y for x, y in zip(a, b))) for a, b in zip(p, q)]
    ss = [square(axis) for axis in d]
    return tuple((x + y for x, y in zip(*ss)))

def points(rows):
    zero = rows.index((0, 0, 0, 0))
    return [point(r) for r in rows] + [point(r, True) for k, r in enumerate(rows) if k != zero]

def edges(vertices):
    result = []
    survivors = 0
    for i, p in enumerate(vertices):
        for j in range(i + 1, len(vertices)):
            q = vertices[j]
            constant = sum((WEIGHTS[k] * (p[a][k] - q[a][k]) ** 2 for a in range(2) for k in range(8)))
            if constant != SCALE * SCALE:
                continue
            survivors += 1
            if distance(p, q) == (SCALE * SCALE, 0, 0, 0, 0, 0, 0, 0):
                result.append((i, j))
    return (result, survivors)
