#!/usr/bin/env python3
"""Exact finite readers for the written curvature and circular-hex proofs.

This is not a solver, a floating-point geometry test, or a formal proof.
The local C2 interface and angle arguments are in proof.md.
"""
from collections import defaultdict
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
VERTICES = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def level(p):
    return max(abs(p[0]), abs(p[1]), abs(p[0] + p[1]))


def ball(radius):
    return {(x, y) for x in range(-radius, radius + 1)
            for y in range(-radius, radius + 1) if level((x, y)) <= radius}


def cell_vertices(p):
    center = p[0] - p[1], p[0] + 2 * p[1]
    return tuple(add(center, v) for v in VERTICES)


def mesh(cells):
    edges, stars = defaultdict(list), defaultdict(set)
    for p in sorted(cells):
        vertices = cell_vertices(p)
        for s, a in enumerate(vertices):
            b = vertices[(s + 1) % 6]
            edges[tuple(sorted((a, b)))].append((p, s))
            stars[a].add(p)
    require(all(len(entries) in (1, 2) for entries in edges.values()),
            'invalid cell-edge multiplicity')
    return dict(edges), dict(stars)


def check_disk(cells):
    edges, stars = mesh(cells)
    require(len(stars) - len(edges) + len(cells) == 1, 'wrong Euler number')
    boundary = defaultdict(set)
    for (a, b), entries in edges.items():
        if len(entries) == 1:
            boundary[a].add(b)
            boundary[b].add(a)
    require(boundary and all(len(v) == 2 for v in boundary.values()),
            'boundary is not a union of cycles')
    seen, todo = set(), [next(iter(boundary))]
    while todo:
        a = todo.pop()
        if a not in seen:
            seen.add(a)
            todo.extend(boundary[a] - seen)
    require(seen == set(boundary), 'boundary has more than one cycle')
    return edges, stars, len(boundary)


def orientations(word):
    # R^k J^h, J(q,r)=(q+r,-r); signs refer to outward displacement.
    return {tuple(word[(j - k) % 6] if h == 0
                  else word[(k - j - 1) % 6] for j in range(6))
            for h in (0, 1) for k in range(6)}


def check_witness(data, radius, expected_word):
    require(data['radius'] == radius, 'wrong claimed radius')
    require(data['word'] == list(expected_word), 'wrong prototype word')
    allowed = orientations(expected_word)
    copies = {}
    for copy in data['copies']:
        p, signs = tuple(copy['cell']), tuple(copy['signs'])
        require(len(p) == 2 and all(type(x) is int for x in p), 'invalid cell')
        require(len(signs) == 6 and all(type(x) is int for x in signs),
                'invalid signs')
        require(p not in copies, 'duplicate cell')
        require(signs in allowed, 'copy is not a prototype isometry')
        copies[p] = signs
    require(set(copies) == ball(radius), 'cell ball is incomplete or oversized')
    require(copies[(0, 0)] == expected_word, 'root is not normalized')
    edges, stars, _ = check_disk(set(copies))
    matched = 0
    for entries in edges.values():
        if len(entries) == 2:
            (p, s), (q, t) = entries
            require(copies[p][s] + copies[q][t] == 0, 'unmatched internal side')
            matched += 1
    prefixes = []
    for r in range(radius + 1):
        cells = ball(r)
        _, prefix_stars, boundary = check_disk(cells)
        if r < radius:
            _, next_stars = mesh(ball(r + 1))
            require(all(len(next_stars[v]) == 3 for v in prefix_stars),
                    'a previous vertex star is not filled')
        if r:
            previous_vertices = set(mesh(ball(r - 1))[1])
            require(all(set(cell_vertices(p)) & previous_vertices
                        for p in cells - ball(r - 1)),
                    'new copy does not touch the previous corona')
        prefixes.append({'radius': r, 'tiles': len(cells), 'boundary_sides': boundary})
    return {'copies': len(copies), 'matched_internal_sides': matched,
            'prefixes': prefixes}


def shell_certificate(radius):
    cells, inner = ball(radius), ball(radius - 1)
    edges, stars, boundary = check_disk(cells)
    shell_edges = 0
    for (a, b), entries in edges.items():
        if len(entries) == 2 and all(p not in inner for p, _ in entries):
            # An inner tile makes this endpoint strictly interior. Its two
            # matching interfaces cancel, forcing the remaining two signs
            # to sum to zero by the three-corner angle equation.
            require((stars[a] | stars[b]) & inner,
                    'outer-shell interface lacks an interior endpoint guard')
            shell_edges += 1
    require(len(cells) == 1 + 3 * radius * (radius + 1), 'ball count failed')
    require(boundary == 6 * (2 * radius + 1), 'perimeter count failed')
    return {'radius': radius, 'tiles': len(cells), 'boundary_sides': boundary,
            'guarded_shell_interfaces': shell_edges}


def ceil_fraction(x):
    return -(-x.numerator // x.denominator)


def exceptional_angles(curvature_matching=False):
    values = set()
    for corners in range(6):
        for smooth in range(3):
            residual = 2 - Fraction(2 * corners, 3) - smooth
            for coefficient in range(-2 * corners, 2 * corners + 1):
                if curvature_matching:
                    allowed = {-2 * total for total in range(-smooth, smooth + 1)}
                    if coefficient not in allowed:
                        continue
                if coefficient:
                    candidate = residual / coefficient
                    if 0 < candidate < Fraction(1, 6):
                        values.add(candidate)
    return sorted(values)


def curvature_bound(alpha, area_lower, diameter_squared_upper):
    require(alpha > 1 and area_lower > 0 and diameter_squared_upper > 0,
            'invalid certified geometric bound')
    c = Fraction(22, 7) * diameter_squared_upper / area_lower
    m = 1
    for k in range(1000):
        upper = (c * (k + 1) ** 2).__floor__()
        if m > upper:
            return {'first_excluded_depth': k, 'required_tiles': m,
                    'area_capacity': upper, 'upper_Heesch': k - 1}
        m = ceil_fraction(alpha * m)
    raise RuntimeError('bound refinement incomplete; no exclusion certified')


def controls(three, one):
    rejected = []
    bad = deepcopy(three)
    bad['copies'].pop()
    cases = [('missing_copy', bad)]
    bad = deepcopy(three)
    bad['copies'].append(deepcopy(bad['copies'][0]))
    cases.append(('duplicate_copy', bad))
    bad = deepcopy(three)
    bad['copies'][0]['signs'] = [1] * 6
    cases.append(('wrong_isometry', bad))
    bad = deepcopy(three)
    bad['copies'][0]['signs'] = [bad['copies'][0]['signs'][-1]] + bad['copies'][0]['signs'][:-1]
    cases.append(('broken_pairing', bad))
    bad = deepcopy(three)
    bad['copies'][0]['signs'][0] = True
    cases.append(('boolean_sign', bad))
    bad = deepcopy(three)
    bad['radius'] = 7
    cases.append(('false_depth', bad))
    for name, bad in cases:
        try:
            check_witness(bad, 3, (0, 1, 1, 1, -1, -1))
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('malformed control accepted: ' + name)
    # Positive control: globally reflected sign/cell data must still work.
    reflected = deepcopy(one)
    reflected['word'] = [one['word'][(-j - 1) % 6] for j in range(6)]
    for copy in reflected['copies']:
        x, y = copy['cell']
        # Fine-vertex J conjugated by center(x,y)=(x-y,x+2y).
        copy['cell'] = [x, -x - y]
        copy['signs'] = [copy['signs'][(-j - 1) % 6] for j in range(6)]
    # Root word is now normalized to the reflected prototype.
    check_witness(reflected, 1, tuple(reflected['word']))
    return {'rejected': rejected, 'reflected_witness': 'passed'}


def run():
    three = json.loads((HERE / 'three_coronas.json').read_text())
    one = json.loads((HERE / 'one_corona.json').read_text())
    require(Fraction(13, 10) ** 2 - Fraction(1, 2) ** 2 == Fraction(6, 5) ** 2,
            'circle endpoint identity failed')
    tangent = Fraction(5, 12)
    require(tangent ** 2 < Fraction(1, 3), 'endpoint angle is too large')
    stars = [[c, s] for c in range(4) for s in range(3) if 2 * c + 3 * s == 6]
    require(stars == [[0, 2], [3, 0]], 'angle-star enumeration failed')
    exceptional = exceptional_angles()
    require(exceptional == [Fraction(1, 12), Fraction(2, 21), Fraction(1, 9),
                            Fraction(2, 15), Fraction(4, 27)],
            'exceptional-angle enumeration failed')
    matched_exceptions = exceptional_angles(curvature_matching=True)
    require(matched_exceptions == [], 'a curvature-compatible exception remains')
    shells = [shell_certificate(r) for r in (1, 2, 4)]
    for row, excess in zip(shells, (3, 2, 1)):
        require(excess * row['tiles'] > row['boundary_sides'], 'charge cut failed')
    result = {
        'three_corona_witness': check_witness(three, 3, (0, 1, 1, 1, -1, -1)),
        'one_corona_witness': check_witness(one, 1, (1, 1, 1, 1, -1, -1)),
        'shell_certificates': shells,
        'star_types_corner_smooth': stars,
        'angle_only_exceptional_endpoint_angle_over_pi': [str(x) for x in exceptional],
        'curvature_matched_exceptional_endpoint_angle_over_pi': [str(x) for x in matched_exceptions],
        'curvature_capacity': curvature_bound(Fraction(3, 2), Fraction(5, 2),
                                               Fraction(121, 25)),
        'controls': controls(three, one),
        'witness_sha256': {
            name: sha256((HERE / name).read_bytes()).hexdigest()
            for name in ('three_coronas.json', 'one_corona.json')},
    }
    return result


if __name__ == '__main__':
    output = run()
    if len(sys.argv) > 1:
        require(sys.argv[1:] == ['--expected'], 'usage: check.py [--expected]')
        require(output == json.loads((HERE / 'expected.json').read_text()),
                'output differs from expected.json')
    print(json.dumps(output, indent=2, sort_keys=True))
