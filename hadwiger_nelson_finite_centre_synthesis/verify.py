"""Independent exact certificate checker: no geometry, SAT or build imports.

Coordinates are physical coordinates times 36, in basis 1,sqrt3,sqrt11,sqrt33.
Reconstruct circle centres by solving two linear bisector equations. Rebuild
every unit edge using generic radical multiplication, then check colour words.
All checks are explicit exceptions and remain active under python -O.
"""
import copy
import hashlib
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ZERO = (0, 0, 0, 0)
UNIT = (1296, 0, 0, 0)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def plus(a, b):
    return tuple(x + y for x, y in zip(a, b))


def minus(a, b):
    return tuple(x - y for x, y in zip(a, b))


def times(a, b):
    out = [0] * 4
    for i, x in enumerate(a):
        if not x:
            continue
        for j, y in enumerate(b):
            if y:
                common = i & j
                factor = (3 if common & 1 else 1) * (11 if common & 2 else 1)
                out[i ^ j] += x * y * factor
    return tuple(out)


def conjugate(a, mask):
    return tuple(-x if (i & mask).bit_count() % 2 else x
                 for i, x in enumerate(a))


def divide(a, b):
    require(b != ZERO, 'Zero determinant')
    product = times(times(conjugate(b, 1), conjugate(b, 2)), conjugate(b, 3))
    norm = times(b, product)
    require(norm[1:] == (0, 0, 0) and norm[0] != 0, 'Bad field norm')
    return tuple(Fraction(x, norm[0]) for x in times(a, product))


def norm(point):
    return plus(times(point[0], point[0]), times(point[1], point[1]))


def distance(a, b):
    return norm((minus(a[0], b[0]), minus(a[1], b[1])))


def circle_centre(p, q, r):
    x1, y1 = minus(q[0], p[0]), minus(q[1], p[1])
    x2, y2 = minus(r[0], p[0]), minus(r[1], p[1])
    det = minus(times(x1, y2), times(x2, y1))
    denominator = tuple(2 * x for x in det)
    l1, l2 = norm((x1, y1)), norm((x2, y2))
    ox = divide(minus(times(l1, y2), times(l2, y1)), denominator)
    oy = divide(minus(times(x1, l2), times(x2, l1)), denominator)
    v = plus(p[0], ox), plus(p[1], oy)
    require(all(distance(v, z) == UNIT for z in (p, q, r)),
            'Parents do not have a unit circumcircle')
    return v


def reconstruct(seed_rows, triples):
    require(len(seed_rows) == 51 and len(triples) == 973, 'Wrong construction size')
    require(all(len(row) == 4 and all(type(v) is int for v in row)
                for row in seed_rows), 'Malformed seed')
    points = [((0, a, b, 0), (c, 0, 0, d)) for a, b, c, d in seed_rows]
    known = set(points)
    require(len(known) == 51, 'Repeated seed point')
    for parents in triples:
        require(len(parents) == 3 and len(set(parents)) == 3 and
                all(type(i) is int and 0 <= i < len(points) for i in parents),
                'Malformed parents')
        p = circle_centre(*(points[i] for i in parents))
        require(p not in known, 'Repeated constructed point')
        require(all(Fraction(v).denominator == 1 for xy in p for v in xy),
                'Fixture has nonintegral physical numerator')
        p = tuple(tuple(int(v) for v in xy) for xy in p)
        points.append(p)
        known.add(p)
    return points


def digest(value):
    data = json.dumps(value, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(data).hexdigest()


def scaled_rows(points):
    rows = []
    for x, y in points:
        require(x[0] == x[3] == y[1] == y[2] == 0 and x[2] % 3 == 0,
                'Wrong scaled coefficient form')
        rows.append([x[1], x[2] // 3, y[0], y[3]])
    return rows


def check_word(word, count, edges):
    require(type(word) is str and len(word) == count and set(word) <= set('0123'),
            'Malformed colouring')
    require(word[0] == word[1] == word[2], 'Terminals are not monochromatic')
    require(all(word[i] != word[j] for i, j in edges if j < count),
            'Monochromatic unit edge')


def check_certificate(cert, points, edges):
    require(cert['vertices'] == len(points) == 1024 and
            cert['edges'] == len(edges) == 6317, 'Wrong graph size')
    require(cert['point_sha256'] == digest(scaled_rows(points)), 'Wrong point hash')
    require(cert['edge_sha256'] == digest(edges), 'Wrong edge hash')
    require(cert['monochromatic_terminal_indices'] == [0, 1, 2], 'Wrong terminals')
    require(cert['target_found'] is False and cert['forcing_gate_reached'] is False,
            'Colouring contradicts claimed success')
    require(all(distance(points[i], points[j]) == (432, 0, 0, 0)
                for i, j in combinations(range(3), 2)), 'Wrong marked triangle')
    check_word(cert['colouring'], 1024, edges)
    blockers = cert['blocking_additions']
    require(len(blockers) == 18 and len({b['index'] for b in blockers}) == 18,
            'Wrong blocking witness count')
    for b in blockers:
        i, word = b['index'], b['prior_colouring']
        require(type(i) is int and 51 <= i < 1024, 'Invalid blocking index')
        check_word(word, i, edges)
        colours = {word[j] for j, k in edges if k == i}
        require(colours == set('0123'), 'Added point does not block this colouring')


def controls(seed, triples, cert, points, edges):
    def reject(action):
        try:
            action()
        except ValueError:
            return
        raise RuntimeError('Malformed control accepted')
    reject(lambda: reconstruct(seed, triples[:-1]))
    for bad_parents in ([7, 7, 35], [7, 24, 51]):
        reject(lambda: reconstruct(seed, [bad_parents] + triples[1:]))
    reject(lambda: circle_centre((ZERO, ZERO), ((36, 0, 0, 0), ZERO),
                                ((72, 0, 0, 0), ZERO)))
    mutations = [
        ('colouring', cert['colouring'][:-1]),
        ('colouring', '4' + cert['colouring'][1:]),
        ('colouring', '1' + cert['colouring'][1:]),
        ('colouring', '0' * 1024),
        ('point_sha256', '0' * 64),
        ('edge_sha256', '0' * 64),
        ('target_found', True),
        ('forcing_gate_reached', True),
    ]
    for key, value in mutations:
        bad = copy.deepcopy(cert)
        bad[key] = value
        reject(lambda: check_certificate(bad, points, edges))
    bad = copy.deepcopy(cert)
    bad['blocking_additions'][0]['prior_colouring'] = '0' * 51
    reject(lambda: check_certificate(bad, points, edges))
    return 13


def main():
    seed = json.loads((ROOT / 'seed.json').read_text())
    triples = json.loads((ROOT / 'construction.json').read_text())
    cert = json.loads((ROOT / 'certificate.json').read_text())
    points = reconstruct(seed, triples)
    edges = [[i, j] for i, j in combinations(range(len(points)), 2)
             if distance(points[i], points[j]) == UNIT]
    check_certificate(cert, points, edges)
    rejected = controls(seed, triples, cert, points, edges)
    print(json.dumps({'verified': True, 'vertices': len(points), 'edges': len(edges),
                      'additions': len(triples), 'blocking_witnesses': 18,
                      'monochromatic_terminals': True, 'proper_four_colouring': True,
                      'malformed_controls_rejected': rejected,
                      'point_sha256': digest(scaled_rows(points)),
                      'edge_sha256': digest(edges), 'forcing_gate_reached': False,
                      'target_found': False}, sort_keys=True))


if __name__ == '__main__':
    main()
