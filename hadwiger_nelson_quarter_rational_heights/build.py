#!/usr/bin/env python3
"""Deterministic finite evidence; the universal theorem is in README.md."""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from math import gcd
from pathlib import Path


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':')).encode()


def digest(x):
    return sha256(canonical(x)).hexdigest()


def level(s):
    return 0 if s % 8 == 7 else 1 if s % 8 == 3 else 2


def squarepart(n):
    b, s, p = 1, 1, 2
    while p * p <= n:
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        b *= p ** (e // 2)
        if e % 2:
            s *= p
        p += 1
    return b, s * n


def point(x, y):
    return tuple(sorted((s, F(b)) for s, b in x.items() if b)), F(y)


def add(p, q):
    x = dict(p[0])
    for s, b in q[0]:
        x[s] = x.get(s, F(0)) + b
    return point(x, p[1] + q[1])


def neg(p):
    return point({s: -b for s, b in p[0]}, -p[1])


def encode(p):
    return [[[s, b.numerator, b.denominator] for s, b in p[0]],
            [p[1].numerator, p[1].denominator]]


def colour(p):
    first = 0
    for s, b in p[0]:
        z = b / 2 ** level(s)
        if z.denominator % 2 == 0:
            raise ValueError('outside horizontal module')
        first ^= z.numerator % 2
    y = p[1]
    if y.denominator % 2 == 0:
        raise ValueError('outside vertical ring')
    residue = (y.numerator * pow(y.denominator, -1, 8)) % 8
    return first + 2 * (residue // 4)


def square(x):
    answer = Counter()
    for s, a in x:
        for t, b in x:
            g = gcd(s, t)
            answer[s * t // (g * g)] += a * b * g
    return {s: b for s, b in answer.items() if b}


def edge(p, q):
    d = add(p, neg(q))
    sq = square(d[0])
    sq[1] = sq.get(1, F(0)) + d[1] ** 2 - 16
    return all(b == 0 for b in sq.values())


SPECS = [
    {'name': 'integer_quarters', 'denominators': [1]},
    {'name': 'twelfths', 'denominators': [3]},
    {'name': 'twentieths', 'denominators': [5]},
    {'name': 'twenty_eighths', 'denominators': [7]},
    {'name': 'thirty_sixths', 'denominators': [9]},
    {'name': 'sixtieths', 'denominators': [15]},
    {'name': 'mixed_odd_denominators', 'denominators': [3, 5, 7]},
]


def generators(denominators):
    out = {point({}, 4), point({}, -4)}
    for t in denominators:
        numerators = {0, 1, 2, 3, 4, t, 2*t, 3*t, 4*t-1}
        for a in sorted(numerators):
            if a >= 4*t:
                continue
            b, s = squarepart(16*t*t-a*a)
            for sign in (-1, 1):
                for side in (-1, 1):
                    out.add(point({s: F(sign*b, t)}, F(side*a, t)))
    return sorted(out)


def fixture(spec):
    g = generators(spec['denominators'])
    shifts = [point({}, 0), point({1: 4}, 0), point({}, 4), g[0]]
    return sorted({add(p, q) for p in [point({}, 0)] + g for q in shifts})


def modular_summary():
    counts = Counter()
    remaining = Counter()
    for s in range(64):
        if s % 4 == 0:
            continue
        l = level(s)
        for a in range(64):
            for b in range(64):
                if (a*a+s*b*b-16) % 64:
                    continue
                if b % (2 ** l):
                    raise ValueError('module lemma fails')
                counts[str(s % 8)] += 1
                if (b // 2 ** l) % 2 == 0:
                    if a % 8 != 4:
                        raise ValueError('remaining-step lemma fails')
                    remaining[str(s % 8)] += 1
    return {'modulus': 64, 'tested': 48*64*64,
            'solutions': dict(sorted(counts.items())),
            'first_bit_unchanged': dict(sorted(remaining.items()))}


def rational_summary():
    rows = []
    for t in range(1, 32, 2):
        for a in range(-4*t, 4*t+1):
            if gcd(a, t) != 1:
                continue
            n = 16*t*t-a*a
            if n:
                b, s = squarepart(n)
                steps = [point({s: F(sign*b, t)}, F(a, t)) for sign in (-1, 1)]
            else:
                steps = [point({}, F(a, t))]
            for p in steps:
                for r in range(8):
                    start = point({}, r)
                    if colour(start) == colour(add(start, p)):
                        raise ValueError('rational step not separated')
                rows.append(encode(p))
    return {'odd_denominator_max': 31, 'signed_steps': len(rows),
            'origin_residue_checks': 8*len(rows), 'steps_sha256': digest(rows)}


def produce():
    cases = []
    for spec in SPECS:
        pts = fixture(spec)
        edges = [(i,j) for i,j in combinations(range(len(pts)), 2) if edge(pts[i],pts[j])]
        cols = [colour(p) for p in pts]
        if any(cols[i] == cols[j] for i,j in edges):
            raise ValueError('fixture has monochromatic edge')
        cases.append({**spec, 'vertices': len(pts), 'edges': len(edges),
                      'point_sha256': digest([encode(p) for p in pts]),
                      'edge_sha256': digest(edges), 'colours': ''.join(map(str, cols))})
    return {'schema': 1, 'claim': 'full support R x (1/4) Z_(2) is four-colourable',
            'levels_by_squarefree_residue_mod8': {str(s): level(s) for s in (1,2,3,5,6,7)},
            'modular': modular_summary(), 'rational': rational_summary(), 'cases': cases,
            'target_found': False, 'exact_chromatic_number_claimed': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=Path('out'))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    cert = produce()
    raw = (json.dumps(cert, indent=2, sort_keys=True) + '\n').encode()
    (args.out/'certificate.json').write_bytes(raw)
    print(json.dumps({'status': 'PASS', 'certificate_bytes': len(raw),
                      'certificate_sha256': sha256(raw).hexdigest(),
                      'cases': len(cert['cases']),
                      'vertices': sum(c['vertices'] for c in cert['cases']),
                      'edges': sum(c['edges'] for c in cert['cases'])}, sort_keys=True))


if __name__ == '__main__':
    main()
