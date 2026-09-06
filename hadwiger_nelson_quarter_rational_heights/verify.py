#!/usr/bin/env python3
"""Independent exact norm checker. No producer imports or floating arithmetic."""
import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from math import prod
from pathlib import Path

Q = Fraction
LEVELS = {1: 2, 2: 2, 3: 1, 5: 2, 6: 2, 7: 0}
NAMES = [('integer_quarters', [1]), ('twelfths', [3]), ('twentieths', [5]),
         ('twenty_eighths', [7]), ('thirty_sixths', [9]), ('sixtieths', [15]),
         ('mixed_odd_denominators', [3, 5, 7])]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def hashed(obj):
    return sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def prime_root(n):
    """Square root as coefficient and a set of primes; trial division."""
    require(n > 0, 'positive radicand required')
    primes, outside, divisor = set(), 1, 2
    while divisor <= n:
        if divisor * divisor > n:
            primes.add(n)
            break
        multiplicity = 0
        while n % divisor == 0:
            n //= divisor
            multiplicity += 1
        outside *= divisor ** (multiplicity // 2)
        if multiplicity & 1:
            primes.add(divisor)
        divisor += 1
    return Q(outside), frozenset(primes)


def clean(x, y):
    return {s: Q(b) for s,b in x.items() if b}, Q(y)


def plus(p, q):
    x = p[0].copy()
    for s,b in q[0].items():
        x[s] = x.get(s, Q(0)) + b
    return clean(x, p[1] + q[1])


def ordering(p):
    return tuple(sorted((prod(s), b) for s,b in p[0].items())), p[1]


def encoded(p):
    return [[[s, b.numerator, b.denominator] for s,b in ordering(p)[0]],
            [p[1].numerator, p[1].denominator]]


@lru_cache(None)
def inverse_odd(n, modulus):
    """Enumerate inverses instead of using the producer's modular pow."""
    require(n % 2 == 1, 'non-localized denominator')
    return next(x for x in range(modulus) if x*n % modulus == 1)


def residue(z, modulus):
    return z.numerator * inverse_odd(z.denominator, modulus) % modulus


def bits(p, levels=LEVELS):
    terms = [b / (2**levels[prod(s) % 8]) for s,b in p[0].items()]
    require(all(b.denominator % 2 for b in terms), 'outside horizontal module')
    z = sum(terms, Q(0))
    return residue(z, 2), int(residue(p[1], 8) in (4,5,6,7))


def norm(p, q):
    terms = p[0].copy()
    for s,b in q[0].items():
        terms[s] = terms.get(s, Q(0)) - b
    terms = {s: b for s,b in terms.items() if b}
    square = Counter({frozenset(): (p[1]-q[1])**2})
    for s,b in terms.items():
        for t,c in terms.items():
            square[s ^ t] += b*c*prod(s & t)
    return {s: b for s,b in square.items() if b}


def is_edge(p, q):
    return norm(p, q) == {frozenset(): Q(16)}


def gen(ts):
    points = {}
    for y in (-4,4):
        p = clean({},y)
        points[ordering(p)] = p
    for t in ts:
        aa = {0,1,2,3,4,t,2*t,3*t,4*t-1}
        for a in aa:
            if a >= 4*t:
                continue
            b, s = prime_root(16*t*t-a*a)
            for u in (-1,1):
                for v in (-1,1):
                    p = clean({s: u*b/t}, Q(v*a,t))
                    points[ordering(p)] = p
    return [points[k] for k in sorted(points)]


def fixture(ts):
    g = gen(ts)
    shifts = [clean({},0), clean({frozenset(): 4},0), clean({},4), g[0]]
    pts = {}
    for p in [clean({},0)] + g:
        for q in shifts:
            z = plus(p,q)
            pts[ordering(z)] = z
    return [pts[k] for k in sorted(pts)]


def all_modular():
    roots = {n: [] for n in range(64)}
    for a in range(64):
        roots[a*a % 64].append(a)
    solutions, residual = Counter(), Counter()
    for s in range(64):
        if s % 4 == 0:
            continue
        ell = LEVELS[s % 8]
        for b in range(64):
            for a in roots[(16-s*b*b) % 64]:
                require(b % (2**ell) == 0, 'universal module residue failure')
                solutions[str(s % 8)] += 1
                if b % (2**(ell+1)) == 0:
                    require(a % 8 == 4, 'universal remaining-step residue failure')
                    residual[str(s % 8)] += 1
    return {'modulus': 64, 'tested': 196608,
            'solutions': dict(sorted(solutions.items())),
            'first_bit_unchanged': dict(sorted(residual.items()))}


def rational():
    rows = []
    for t in range(1,32,2):
        for a in range(-4*t,4*t+1):
            r = Q(a,t)
            if r.denominator != t:
                continue
            n = 16*t*t-a*a
            if n == 0:
                steps = [clean({},r)]
            else:
                b,s = prime_root(n)
                steps = [clean({s: u*b/t},r) for u in (-1,1)]
            for p in steps:
                require(is_edge(clean({},0),p), 'step has wrong exact length')
                for a0 in range(8):
                    z = clean({},a0)
                    require(bits(z) != bits(plus(z,p)), 'rational colour failure')
                rows.append(encoded(p))
    return {'odd_denominator_max': 31, 'signed_steps': len(rows),
            'origin_residue_checks': len(rows)*8, 'steps_sha256': hashed(rows)}


def independent():
    cases, totals = [], Counter()
    critical = {'vertical_edges': 0, 'first_bit_unchanged_edges': 0,
                'first_bit_only_edges': 0}
    wrong_bit_detected = False
    for name,ts in NAMES:
        pts = fixture(ts)
        cols = [bits(p) for p in pts]
        edges = []
        for i,j in combinations(range(len(pts)),2):
            totals['point_pairs'] += 1
            if not is_edge(pts[i],pts[j]):
                continue
            edges.append((i,j))
            require(cols[i] != cols[j], 'monochromatic exact unit edge')
            critical['vertical_edges'] += pts[i][0] == pts[j][0]
            critical['first_bit_unchanged_edges'] += cols[i][0] == cols[j][0]
            critical['first_bit_only_edges'] += cols[i][1] == cols[j][1]
            wrong_bit_detected |= cols[i][0] == cols[j][0]
        totals['vertices'] += len(pts)
        totals['edges'] += len(edges)
        cases.append({'name': name, 'denominators': ts, 'vertices': len(pts),
                      'edges': len(edges), 'point_sha256': hashed([encoded(p) for p in pts]),
                      'edge_sha256': hashed(edges),
                      'colours': ''.join(str(a+2*b) for a,b in cols)})
    require(wrong_bit_detected, 'missing control for vertical-bit deletion')
    triangle = [clean({},0), clean({},4), clean({frozenset({3}):2},2)]
    require(all(is_edge(p,q) for p,q in combinations(triangle,2)), 'triangle control')
    require(len({bits(p) for p in triangle}) == 3, 'triangle colouring control')
    expected = {'schema': 1, 'claim': 'full support R x (1/4) Z_(2) is four-colourable',
                'levels_by_squarefree_residue_mod8': {str(k):v for k,v in LEVELS.items()},
                'modular': all_modular(), 'rational': rational(), 'cases': cases,
                'target_found': False, 'exact_chromatic_number_claimed': False}
    return expected, {**totals, **critical, 'triangle_edges': 3}


def accept(cert, expected):
    require(cert == expected, 'certificate differs from independently reconstructed evidence')


def controls(expected):
    mutations = []
    x = deepcopy(expected); x['cases'].pop(); mutations.append(('omitted fixture',x))
    x = deepcopy(expected); x['cases'][0]['colours'] = '0'*x['cases'][0]['vertices']; mutations.append(('monochromatic fixture',x))
    x = deepcopy(expected); x['cases'][0]['point_sha256'] = '0'*64; mutations.append(('wrong coordinates',x))
    x = deepcopy(expected); x['levels_by_squarefree_residue_mod8']['7'] = 1; mutations.append(('wrong radical divisibility',x))
    x = deepcopy(expected); x['modular']['tested'] -= 1; mutations.append(('incomplete residue audit',x))
    x = deepcopy(expected); x['rational']['signed_steps'] -= 1; mutations.append(('omitted rational step',x))
    x = deepcopy(expected); x['target_found'] = True; mutations.append(('false record claim',x))
    x = deepcopy(expected); x['exact_chromatic_number_claimed'] = True; mutations.append(('unproved sharpness',x))
    rejected = []
    for label, x in mutations:
        try:
            accept(x,expected)
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('accepted mutation: '+label)
    for label,p in [('even vertical denominator',clean({},Q(1,2))),
                    ('insufficient horizontal divisibility',clean({frozenset({3}):1},0))]:
        try:
            bits(p)
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('accepted invalid module input')
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=Path(__file__).with_name('certificate.json'))
    parser.add_argument('--out', type=Path, default=Path('out'))
    args = parser.parse_args()
    expected, checks = independent()
    raw = args.certificate.read_bytes()
    accept(json.loads(raw),expected)
    report = {'status': 'PASS', 'scope': 'universal modular lemma and exact finite controls; full-support bridge in README',
              **checks, 'modular': expected['modular'], 'rational': expected['rational'],
              'malformed_controls_rejected': controls(expected), 'target_found': False,
              'native_solver_calls': 0, 'floating_point_operations': 0,
              'certificate_bytes': len(raw), 'certificate_sha256': sha256(raw).hexdigest()}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,sort_keys=True))


if __name__ == '__main__':
    main()
