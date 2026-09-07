#!/usr/bin/env python3
"""Independent exact geometry, complete residue census, and positive-word audit."""
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


def projection(points):
    columns = [i for i in range(16) if any(p[i] for p in points)]
    divisors = [math.gcd(*(abs(p[i]) for p in points)) for i in columns]
    demand(columns == [0, 2, 5, 7, 9, 11, 12, 14], 'x coefficient columns')
    demand(divisors == [1, 3, 1, 1, 3, 3, 3, 9], 'primitive column divisors')
    values = [tuple((p[i]//d) % 3 for i, d in zip(columns, divisors)) for p in points]
    return columns, divisors, values


def normal_vectors(dimension):
    # Unique leading nonzero position, then a leading 1, then every possible tail.
    for pivot in range(dimension):
        for tail in product(range(3), repeat=dimension-pivot-1):
            yield (0,)*pivot + (1,) + tail


def family_census(values, limit, dimension=None):
    if dimension is None:
        demand(bool(values), 'dimension required for an empty fixture')
        dimension = len(values[0])
    demand(dimension > 0 and all(len(row) == dimension for row in values), 'residue dimensions')
    records = []
    for normal in normal_vectors(dimension):
        masks = [0, 0, 0]
        # Evaluate every point directly, without the producer's residue fibres.
        for v, row in enumerate(values):
            level = sum(a*b for a, b in zip(normal, row)) % 3
            masks[level] += 1 << v
        for b, mask in enumerate(masks):
            records.append((normal, b, mask))
    demand(len(records) == 3*(3**dimension-1)//2, 'hyperplane census count')
    admissible = [r for r in records if r[2].bit_count() <= limit]
    return records, admissible


def check_certificate(points, edges, values, admissible, certificate):
    demand(certificate.get('version') == 'degrey-residue-hyperplanes-v1', 'certificate version')
    demand(type(certificate.get('target')) is int and certificate['target'] == 508, 'target')
    n = len(points)
    deleted = certificate.get('deleted')
    demand(type(deleted) is int and 0 <= deleted < n, 'deleted label')
    demand(points[deleted] == (2*SCALE,)+(0,)*31 and not any(values[deleted]), 'endpoint or zero residue')
    base = certificate.get('base_word')
    demand(type(base) is str and len(base) == n, 'base word length')
    demand(all(c in ('-' if v == deleted else '0123') for v, c in enumerate(base)), 'base support or colour')
    base_checks = 0
    for u, v in edges:
        if u != deleted and v != deleted:
            demand(base[u] != base[v], 'base monochromatic edge')
            base_checks += 1
    zero_masks = {mask for normal, b, mask in admissible if b == 0}
    equation_masks = {''.join(map(str, normal)): mask for normal, b, mask in admissible if b == 0}
    entries = certificate.get('exceptions')
    demand(type(entries) is list, 'exception list')
    supplied = set()
    exception_checks = 0
    for entry in entries:
        normal, word = entry.get('normal'), entry.get('word')
        demand(type(normal) is str and normal in equation_masks, 'invalid or ineligible normal')
        mask = equation_masks[normal]
        demand(mask not in supplied, 'duplicate support')
        supplied.add(mask)
        vertices = [v for v in range(n) if mask >> v & 1]
        demand(type(word) is str and len(word) == len(vertices), 'exception word length')
        demand(all(c in '0123' for c in word), 'exception colour')
        colours = dict(zip(vertices, word))
        for u, v in edges:
            if u in colours and v in colours:
                demand(colours[u] != colours[v], 'exception monochromatic edge')
                exception_checks += 1
    demand(supplied == zero_masks, 'missing zero-level support')
    for normal, b, mask in admissible:
        if b:
            demand(not (mask >> deleted & 1), 'base fails to cover section')
        else:
            demand(mask in supplied, 'uncovered zero-level section')
    return dict(base_edge_checks=base_checks, exception_edge_checks=exception_checks,
                total_colour_edge_checks=base_checks+exception_checks,
                exception_words=len(entries), deleted=deleted)


def verify(certificate):
    points = reconstruct()
    edges, survivors = edge_census(points)
    columns, divisors, values = projection(points)
    records, admissible = family_census(values, 508)
    result = check_certificate(points, edges, values, admissible, certificate)
    result.update(verified=True, record_improvement=False, arbitrary_target_subsets_classified=False,
                  vertices=len(points), edges=len(edges), pair_checks=len(points)*(len(points)-1)//2,
                  modular_survivors=survivors, modulus=MODULUS,
                  x_columns=columns, x_divisors=divisors, residue_fibres=len(set(values)),
                  canonical_normals=len(records)//3, affine_hyperplanes=len(records),
                  admissible_hyperplanes=len(admissible), distinct_admissible_supports=len({m for a, b, m in admissible}),
                  admissible_by_level=[sum(b == c for a, b, m in admissible) for c in range(3)],
                  exact_target_sections=sum(m.bit_count() == 508 for a, b, m in admissible),
                  target=508, admissible_order_range=[min(m.bit_count() for a, b, m in admissible), max(m.bit_count() for a, b, m in admissible)],
                  zero_level_order_range=[min(m.bit_count() for a, b, m in admissible if not b), max(m.bit_count() for a, b, m in admissible if not b)],
                  coordinate_sha256=hashlib.sha256(''.join(' '.join(map(str, p))+'\n' for p in points).encode()).hexdigest(),
                  edge_sha256=hashlib.sha256(''.join(f'{u} {v}\n' for u, v in edges).encode()).hexdigest(),
                  hyperplane_stream_sha256=hashlib.sha256(''.join(''.join(map(str, a))+f' {b} {m:x}\n' for a, b, m in sorted(records)).encode()).hexdigest())
    return result


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--certificate', type=Path, default=HERE/'certificate.json')
    ap.add_argument('--check-expected', action='store_true')
    args = ap.parse_args()
    result = verify(json.loads(args.certificate.read_text()))
    if args.check_expected:
        demand(result == json.loads((HERE/'expected.json').read_text()), 'expected report mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))
