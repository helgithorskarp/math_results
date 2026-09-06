"""Produce seven physical opposite-switch obstructions in every affine case."""
import json
from itertools import product
from pathlib import Path


def multiply(u, v):
    x, y, a, b = u % 7, u // 7, v % 7, v // 7
    return (x*a+3*y*b) % 7 + 7*((x*b+y*a) % 7)


def connection():
    powers = []
    x = 1
    for i in range(48):
        powers.append(x)
        x = multiply(x, 8)
    if len(set(powers)) != 48 or x != 1:
        raise ValueError('8 must be primitive')
    return {x for i, x in enumerate(powers) if i % 4 in (0, 1)}


def plane():
    return sorted({tuple(a*pow(next(t for t in v if t), -1, 7) % 7
                         for a in v)
                   for v in product(range(7), repeat=3) if any(v)})


def dot(p, line):
    return sum(a*b for a, b in zip(p, line)) % 7


def chart(arc, line):
    k = max(i for i in range(3) if line[i])
    i, j = [i for i in range(3) if i != k]
    return [(p[i]*pow(dot(p, line), -1, 7) % 7
             + 7*(p[j]*pow(dot(p, line), -1, 7) % 7)) for p in arc]


def direction_masks():
    red = connection()
    masks = set()
    directions = [(1, m) for m in range(7)]+[(0, 1)]
    for a, b, c, d in product(range(7), repeat=4):
        if (a*d-b*c) % 7 == 0:
            continue
        masks.add(sum(1 << i for i, (x, y) in enumerate(directions)
                      if (a*x+b*y) % 7+7*((c*x+d*y) % 7) in red))
    return sorted(masks)


def color(u, v, mask):
    x, y = (u % 7-v % 7) % 7, (u // 7-v // 7) % 7
    if x == y == 0:
        return 0
    direction = y*pow(x, -1, 7) % 7 if x else 7
    return (mask >> direction) & 1


def clique(rows, k, candidates, chosen=()):
    if k == 0:
        return chosen
    while candidates.bit_count() >= k:
        bit = candidates & -candidates
        candidates ^= bit
        v = bit.bit_length()-1
        q = clique(rows, k-1, candidates & rows[v], chosen+(v,))
        if q is not None:
            return q
    return None


def build():
    arcs = json.loads(Path(__file__).with_name('arcs.json').read_text())
    cases = []
    for ci, arc in enumerate(arcs):
        for li, line in enumerate(plane()):
            if any(dot(p, line) == 0 for p in arc):
                continue
            vertices = chart(arc, line)
            for mask in direction_masks():
                rows = [[sum(1 << j for j, v in enumerate(vertices)
                             if u != v and color(u, v, mask) == c)
                         for u in vertices] for c in (0, 1)]
                stars = []
                for outside in range(49):
                    if outside in vertices:
                        continue
                    for c in (0, 1):
                        candidates = sum(1 << i for i, v in enumerate(vertices)
                                         if color(v, outside, mask) != c)
                        q = clique(rows[c], 4, candidates)
                        if q is not None:
                            stars.append([outside, c, *q])
                            break
                    if len(stars) == 7:
                        break
                if len(stars) != 7:
                    raise ValueError(('insufficient forbidden stars', ci, li, mask))
                cases.append([ci, li, mask, stars])
    return {'schema': 1, 'arcs': arcs, 'cases': cases}


if __name__ == '__main__':
    print(json.dumps(build(), separators=(',', ':')))
