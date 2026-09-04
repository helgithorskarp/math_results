#!/usr/bin/env python3
"""Solver-free finite checks accompanying the analytic field obstruction."""

import hashlib
import itertools
import json
from fractions import Fraction as F
from math import lcm
from pathlib import Path

import coloring as K

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parent / 'hadwiger_nelson_nonmono159_214_lowden2'
INPUT_HASHES = {
    'points159.tsv': '4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02',
    'points214.tsv': '97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f',
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def points(name):
    raw = (INPUTS / name).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == INPUT_HASHES[name], 'coordinate hash mismatch')
    lines = raw.decode().splitlines()
    require(lines[0] == '# scale 12', 'unexpected coordinate scale')
    out = []
    for line in lines:
        if not line or line.startswith('#'):
            continue
        v = tuple(map(int, line.split()))
        require(len(v) == 16, 'bad coordinate row')
        require(all(v[i] == 0 for i in range(16) if i not in (0, 5, 9, 12)),
                'point lies outside the claimed complex field')
        out.append(K.element(*(F(v[i], 12) for i in (0, 5, 9, 12))))
    require(len(set(out)) == len(out), 'duplicate input point')
    return out


def edges(vertices):
    """Direct coefficient identity for Euclidean distance, without K.multiply."""
    out = []
    for i, x in enumerate(vertices):
        for j in range(i):
            a, b, c, d = (x[k]-vertices[j][k] for k in range(4))
            if (a*b+c*d == 0 and a*a+33*b*b+3*c*c+11*d*d == 1):
                out.append((j, i))
    return out


def check_graph(vertices):
    colors = [K.color(z) for z in vertices]
    ee = edges(vertices)
    require(all(0 <= c < 4 for c in colors), 'bad color value')
    require(all(colors[u] != colors[v] for u, v in ee), 'monochromatic unit edge')
    encoded = ''.join(map(str, colors)).encode()
    return {'vertices': len(vertices), 'edges': len(ee),
            'coloring_sha256': hashlib.sha256(encoded).hexdigest()}


def main():
    for bits in range(1, 81):
        r = K.root33_mod_power2(bits)
        require((r*r-33) % (1 << bits) == 0, 'bad 2-adic root')
        if bits > 1:
            require(r % (1 << (bits-1)) == K.root33_mod_power2(bits-1), 'incompatible roots')
    translations = 0
    representations = 0
    for k, (a, b, c, d) in enumerate(itertools.product(range(-2, 3), repeat=4)):
        w = K.element(0, 0, F(a, 2**(k % 13)), F(b, 3**(k % 3)))
        u = K.multiply(K.add(K.ONE, w), K.inverse(K.add(K.ONE, K.negate(w))))
        require(K.is_unit(u), 'Cayley parametrization failed')
        z = K.element(F(a, 2**(k % 21)), F(b, 3), F(c, 5*2**(k % 17)), F(d, 7))
        require(K.color(z) != K.color(K.add(z, u)), 'unit-translation counterexample')
        translations += 1
        denominator = lcm(*(v.denominator for v in z))
        numerators = tuple(int(v*denominator) for v in z)
        for scale in (2, 3, 4, 5, 12, 64):
            require(K.color_numerators(tuple(v*scale for v in numerators), denominator*scale)
                    == K.color(z), 'representation-dependent coloring')
            representations += 1
    A, B = points('points159.tsv'), points('points214.tsv')
    a_check, b_check = check_graph(A), check_graph(B)
    require((a_check['vertices'], a_check['edges']) == (159, 646), 'wrong A graph')
    require((b_check['vertices'], b_check['edges']) == (214, 977), 'wrong B graph')
    samples = []
    for sample in json.loads((HERE / 'samples.json').read_text()):
        u = K.element(*(F(v, sample['u_denominator']) for v in sample['u_numerators']))
        t = K.element(*(F(v, sample['t_denominator']) for v in sample['t_numerators']))
        require(K.is_unit(u), 'sample map is not an isometry')
        image = [K.add(K.multiply(u, K.conjugate(z) if sample['reflected'] else z), t) for z in B]
        require(len(set(A) & set(image)) == sample['overlaps'], 'wrong sample overlap')
        result = check_graph(list(dict.fromkeys(A+image)))
        result.update({'reflected': sample['reflected'],
                       'orientation_denominator': sample['u_denominator'],
                       'overlaps': sample['overlaps']})
        samples.append(result)
    spindle = [K.element(*(F(v, 12) for v in p)) for p in
               ((0,0,0,0), (12,0,0,0), (6,0,6,0), (18,0,6,0),
                (10,0,0,2), (5,-1,5,1), (15,-1,5,3))]
    spindle_edges = edges(spindle)
    require(len(spindle_edges) == 11, 'wrong Moser spindle')
    three_colorings = sum(all(colors[u] != colors[v] for u, v in spindle_edges)
                          for colors in itertools.product(range(3), repeat=7))
    require(three_colorings == 0, 'Moser spindle unexpectedly 3-colorable')
    spindle_check = check_graph(spindle)
    result = {'field': 'Q(sqrt(-3),sqrt(-11))', 'root_precisions_checked': 80,
              'unit_translation_checks': translations, 'representation_checks': representations,
              'gadget159': a_check, 'gadget214': b_check, 'mixed_samples': samples,
              'moser_spindle': spindle_check, 'moser_three_colorings': three_colorings,
              'exact_arithmetic': True, 'sat_solver_used': False}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
