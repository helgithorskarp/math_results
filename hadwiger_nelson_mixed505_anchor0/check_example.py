#!/usr/bin/env python3
"""Direct integer radical geometry for both roots of a 14-contact class.

Independent of both census implementations. Coordinates have denominator 72
in Q(sqrt(2),sqrt(3),sqrt(11)); all 127260 pairs are tested per realization.
"""

from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ZERO = (0,) * 8
FACTORS = tuple((2 if m & 1 else 1) * (3 if m & 2 else 1) *
                (11 if m & 4 else 1) for m in range(8))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def basis(**entries):
    out = [0] * 8
    for k, v in entries.items():
        out[int(k[1:])] = v
    return tuple(out)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(a, n):
    return tuple(n * x for x in a)


def multiply(a, b):
    out = [0] * 8
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    out[i ^ j] += x * y * FACTORS[i & j]
    return tuple(out)


def complex_multiply(z, w):
    x, y = z
    X, Y = w
    return (add(multiply(x, X), scale(multiply(y, Y), -1)),
            add(multiply(x, Y), multiply(y, X)))


def norm(z):
    x, y = z
    return add(multiply(x, x), multiply(y, y))


def read_points(n):
    hashes = {159: '4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02',
              214: '97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f'}
    raw = (HERE.parent / f'hadwiger_nelson_nonmono159_214_lowden2/points{n}.tsv').read_bytes()
    require(sha256(raw).hexdigest() == hashes[n], 'wrong source coordinates')
    require(raw.decode().splitlines()[0] == '# scale 12', 'wrong source scale')
    points = []
    for line in raw.decode().splitlines():
        if not line or line.startswith('#'):
            continue
        a = tuple(map(int, line.split()))
        require(len(a) == 16 and not any(a[i] for i in range(16)
                if i not in (0, 5, 9, 12)), 'unexpected source basis')
        points.append(tuple(a[i] for i in (0, 5, 9, 12)))
    require(len(points) == len(set(points)) == n, 'wrong source size')
    return points


def read_colors(path, n, digest):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == digest, 'wrong coloring library')
    rows = [tuple(map(int, line)) for line in raw.decode().splitlines()]
    require(all(len(r) == n and r[0] == 0 and set(r) <= set(range(4))
                for r in rows), 'malformed coloring')
    return rows


def main():
    A = read_points(159)
    # The first list is 72*A, the second is 72*t*A, t=(5+i*sqrt(11))/6.
    original = [(basis(k0=6*a, k6=6*b), basis(k2=6*c, k4=6*d))
                for a, b, c, d in A]
    rotated = [(basis(k0=5*a-11*d, k6=5*b-c), basis(k2=11*b+5*c, k4=a+5*d))
               for a, b, c, d in A]
    B = list(dict.fromkeys(original + rotated))
    require(len(B) == 292 and B[0] == (ZERO, ZERO), 'wrong B assembly')
    V = read_points(214)
    require(V[0] == (12, -2, 0, 0), 'wrong anchor')
    H = [(a-12, b+2, c, d) for a, b, c, d in V]
    labels = {h: i for i, h in enumerate(H)}
    reflection = [labels[(a, b, -c, -d)] for a, b, c, d in H]
    require(reflection[0] == 0 and all(reflection[reflection[i]] == i
                for i in range(214)), 'bad reflection symmetry')
    libB = read_colors(HERE.parent / 'hadwiger_nelson_nonmono159_moser_triple/colors_B.txt',
                      292, 'b9285f2967686bf5458588c6f949173ac8795412a7ffd94a60d687e5a8c260a3')
    libH = read_colors(HERE / 'colors_H.txt', 214,
                      '25a072d1c55cef2318b76cd849ce3096091d25b37981c83bc11d00c416393b58')
    expected = json.loads((HERE / 'expected.json').read_text())['max_contact_example']
    require(expected['T'] == ['-1/3', '0', '0', '1/3'] and
            expected['V'] == ['-5/6', '0', '0', '-1/6'], 'different example polynomial')
    perms = [(0,) + p for p in permutations((1, 2, 3))]
    ib, ih, ip = expected['witness']
    results = []
    for epsilon in (-1, 1):
        # 6*u = -1-epsilon*sqrt(22) + i*(sqrt(11)-epsilon*sqrt(2)).
        u = (basis(k0=-1, k5=-epsilon), basis(k4=1, k1=-epsilon))
        require(norm(u) == basis(k0=36), 'multiplier is not unit')
        T = (basis(k0=-2), basis(k4=2))  # 6*T
        V = (basis(k0=-5), basis(k4=-1))  # 6*V
        uu, Tu = complex_multiply(u, u), complex_multiply(T, u)
        require(all(add(add(uu[k], scale(Tu[k], -1)), scale(V[k], 6)) == ZERO
                    for k in (0, 1)), 'multiplier fails its quadratic')
        rotation_set = None
        for reflected in (False, True):
            image = []
            for a, b, c, d in H:
                if reflected:
                    c, d = -c, -d
                # Direct expansion of 72*u*h. No census code is imported.
                image.append((basis(k0=-a-11*d, k6=-b-c,
                                    k5=epsilon*(d-a), k3=epsilon*(c-11*b)),
                              basis(k4=a-d, k2=11*b-c,
                                    k1=-epsilon*(a+11*d), k7=-epsilon*(b+c))))
            require(image[0] == (ZERO, ZERO), 'image misses origin')
            points = B + image[1:]
            require(len(points) == len(set(points)) == 505, 'unexpected overlap')
            if reflected:
                require(set(points) == rotation_set, 'reflection changed union')
            else:
                rotation_set = set(points)
            mapping = reflection if reflected else list(range(214))
            colors = libB[ib] + tuple(perms[ip][libH[ih][mapping[j]]]
                                     for j in range(1, 214))
            edges, cross, left, right = [], [], 0, 0
            for i, (x, y) in enumerate(points):
                for j in range(i+1, len(points)):
                    X, Y = points[j]
                    difference = (add(x, scale(X, -1)), add(y, scale(Y, -1)))
                    if norm(difference) != basis(k0=72**2):
                        continue
                    require(colors[i] != colors[j], 'monochromatic unit edge')
                    edges.append((i, j))
                    if j < 292:
                        left += 1
                    elif i == 0 or i >= 292:
                        right += 1
                    else:
                        cross.append((i, mapping[j-291]))
            require((len(edges), left, right, len(cross)) == (2242, 1251, 977, 14),
                    'wrong strict edge census')
            require(sorted(cross) == [tuple(e) for e in expected['cross_edges']],
                    'direct geometry disagrees with maximum-contact class')
            results.append({'epsilon': epsilon, 'reflected': reflected,
                            'vertices': len(points), 'strict_unit_edges': len(edges),
                            'new_cross_edges': len(cross), 'proper_four_coloring': True,
                            'edge_sha256': sha256(json.dumps(edges).encode()).hexdigest(),
                            'color_sha256': sha256(bytes(colors)).hexdigest()})
    print(json.dumps({'coordinate_scale': 72, 'real_radicals': [2, 3, 11],
                      'all_pairs_per_realization': 127260,
                      'unit_norm_and_polynomial_checked': True,
                      'realizations': results}, indent=2))


if __name__ == '__main__':
    main()
