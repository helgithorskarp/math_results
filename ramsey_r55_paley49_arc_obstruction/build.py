"""Construct three four-arcs and physical witnesses for all affine charts."""
import json
from itertools import combinations, product


def normalize(v):
    scale = pow(next(x for x in v if x), -1, 7)
    return tuple(x*scale % 7 for x in v)


def dot(u, v):
    return sum(x*y for x, y in zip(u, v)) % 7


def cross(u, v):
    return normalize(((u[1]*v[2]-u[2]*v[1]) % 7,
                      (u[2]*v[0]-u[0]*v[2]) % 7,
                      (u[0]*v[1]-u[1]*v[0]) % 7))


def multiply(u, v):
    a, b, c, d = u % 7, u//7, v % 7, v//7
    return (a*c+3*b*d) % 7 + 7*((a*d+b*c) % 7)


def field_graph():
    squares = {multiply(x, x) for x in range(1, 49)}
    return [[int(u != v and ((u % 7-v % 7) % 7
                 + 7*((u//7-v//7) % 7)) in squares)
             for v in range(49)] for u in range(49)]


def clique(rows, k=5, todo=None, chosen=()):
    if k == 0:
        return chosen
    if todo is None:
        todo = (1 << len(rows))-1
    while todo.bit_count() >= k:
        bit = todo & -todo
        todo ^= bit
        v = bit.bit_length()-1
        found = clique(rows, k-1, todo & rows[v], chosen+(v,))
        if found is not None:
            return found
    return None


def build():
    plane = sorted({normalize(p) for p in product(range(7), repeat=3) if any(p)})
    conic = [p for p in plane if (p[0]*p[2]-p[1]*p[1]) % 7 == 0]
    tangents = [normalize((p[2], -2*p[1] % 7, p[0])) for p in conic]
    internal = {p for p in plane if not any(dot(p, t) == 0 for t in tangents)}
    first = internal | {conic[0]}
    chord = cross(conic[0], conic[1])
    removed = next(p for p in sorted(internal) if dot(p, chord) == 0)
    second = (internal-{removed}) | set(conic[:2])
    third = None
    for a, b, c, d in combinations(conic, 4):
        diagonals = {cross(cross(a, b), cross(c, d)),
                     cross(cross(a, c), cross(b, d)),
                     cross(cross(a, d), cross(b, c))}
        if diagonals <= internal:
            third = (internal-diagonals) | {a, b, c, d}
            break
    if third is None:
        raise ValueError('no internal-diagonal quadrangle')
    arcs = [sorted(x) for x in (first, second, third)]
    a = field_graph()
    units = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    cases = []
    for ci, arc in enumerate(arcs):
        for li, line in enumerate(plane):
            if any(dot(p, line) == 0 for p in arc):
                continue
            e, f = next((e, f) for e, f in combinations(units, 2)
                        if dot(cross(e, f), line))
            chart = [(dot(p, e)*pow(dot(p, line), -1, 7) % 7,
                      dot(p, f)*pow(dot(p, line), -1, 7) % 7) for p in arc]
            for z in range(7, 49):
                image = [(x+(z % 7)*y) % 7+7*((z//7)*y % 7) for x, y in chart]
                rows = [sum(1 << j for j, v in enumerate(image) if a[u][v]) for u in image]
                witness = clique(rows)
                color = 1
                if witness is None:
                    color = 0
                    witness = clique([((1 << 22)-1) ^ row ^ (1 << i)
                                      for i, row in enumerate(rows)])
                if witness is None:
                    raise ValueError(('counterexample to 22-point lemma', ci, li, z, image))
                cases.append([ci, li, z, color, *witness])
    return {'schema': 1, 'arcs': arcs, 'cases': cases}


if __name__ == '__main__':
    print(json.dumps(build(), separators=(',', ':')))
