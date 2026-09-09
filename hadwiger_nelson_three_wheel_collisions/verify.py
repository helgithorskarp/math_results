#!/usr/bin/env python3
"""Exact physical checker, standard library only; imports no producer or solver."""
from itertools import product, combinations, combinations_with_replacement, permutations
from fractions import Fraction as F
from functools import reduce
from math import gcd, isqrt
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
W = [(0, 0), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
LABELS = list(product(range(7), repeat=3))
# (norms, delta, common parameter denominator, u numerator, v numerator)
CASES = [
    ((1, 3, 3), 11, 12, (-3, 1, 3, -1), (-3, 1, -3, 1)),
    ((1, 4, 4), 15, 4, (-1, 0, 1, 0), (-1, 0, -1, 0)),
    ((3, 3, 4), 32, 24, (-8, 0, 4, 0), (-12, -4, -3, -1)),
    ((3, 4, 4), 39, 24, (-9, -3, 3, 1), (-9, -3, -3, -1)),
]


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(x):
    return hashlib.sha256(json.dumps(x, separators=(',', ':')).encode()).hexdigest()


def lin(z, a, b):
    """Multiply by a+b*s, using s^2=-3."""
    A, B, C, D = z
    return a*A-3*b*B, b*A+a*B, a*C-3*b*D, b*C+a*D


def add(*xs):
    return tuple(map(sum, zip(*xs)))


def norm_coeff(z, delta):
    """z*conj(z) = first + second*s*t, s*t=-sqrt(3*delta)."""
    a, b, c, d = z
    return a*a+3*b*b+delta*c*c+3*delta*d*d, 2*(a*d-b*c)


def geometry(case):
    norms, delta, q, u, v = case
    m, n, p = norms
    need(delta == 4*m*n-(p-m-n)**2 and delta > 0, 'circle discriminant')
    need(isqrt(3*delta)**2 != 3*delta, 'independent biquadratic basis')
    need(norm_coeff(u, delta) == norm_coeff(v, delta) == (q*q, 0), 'unit parameters')
    # Representatives r_1=1, r_3=1+omega, r_4=2, encoded (A+B*s)/2.
    reps = {1: (2, 0), 3: (3, 1), 4: (4, 0)}
    (a, b), (c, d), (e, f) = [reps[j] for j in norms]
    need(add((q*a, q*b, 0, 0), lin(u, c, d), lin(v, e, f)) == (0, 0, 0, 0), 'collision equation')
    # conj(r_m)*r_n*u=(p-m-n+t)/2, including the positive root choice.
    need(lin(u, a*c+3*b*d, a*d-b*c) == (2*q*(p-m-n), 0, 2*q, 0), 'circle root identity')
    raw = []
    for i, j, k in LABELS:
        (a, b), (c, d), (e, f) = [W[z] for z in (i, j, k)]
        raw.append(add((q*(2*a+b), q*b, 0, 0), lin(u, 2*c+d, d), lin(v, 2*e+f, f)))
    scale = reduce(gcd, (x for z in raw for x in z), 2*q)
    denominator = 2*q//scale
    labels = [tuple(x//scale for x in z) for z in raw]
    points = sorted(set(labels))
    index = {z: i for i, z in enumerate(points)}
    ids = [index[z] for z in labels]
    edges = []
    for i, j in combinations(range(len(points)), 2):
        diff = tuple(a-b for a, b in zip(points[i], points[j]))
        if norm_coeff(diff, delta) == (denominator*denominator, 0):
            edges.append((i, j))
    # Direct unit triangle supplies the lower bound three in all cases.
    triangle = [ids[LABELS.index(t)] for t in ((0, 0, 0), (1, 0, 0), (2, 0, 0))]
    eset = set(edges)
    need(len(set(triangle)) == 3 and all(tuple(sorted(e)) in eset for e in combinations(triangle, 2)), 'unit triangle')
    return denominator, points, edges, ids


def colour_check(word, points, edges, palette):
    need(type(word) is str and len(word) == len(points), 'colour word length')
    need(set(word) <= set('0123'[:palette]), 'colour alphabet')
    need(all(word[a] != word[b] for a, b in edges), 'proper physical colouring')


def three_patterns(ids, edges):
    c = [(a-b) % 3 for a, b in W]
    results = []
    for s, t in product((1, -1), repeat=2):
        word = [(c[a]+s*c[b]+t*c[d]) % 3 for a, b, d in LABELS]
        first = {}
        failure = None
        for i, v in enumerate(ids):
            if v in first and word[i] != word[first[v]]:
                failure = {'kind': 'coincidence', 'labels': [first[v], i]}
                break
            first[v] = i
        if failure is None:
            bad = next(((a, b) for a, b in edges if word[first[a]] == word[first[b]]), None)
            if bad is not None:
                failure = {'kind': 'unit_edge', 'vertices': list(bad)}
        results.append({'signs': [s, t], 'failure': failure})
    return results


def coverage():
    ds = {(a-c, b-d) for a, b in W for c, d in W}
    norm = lambda z: z[0]**2+z[0]*z[1]+z[1]**2
    rotate = lambda z: (-z[1], z[0]+z[1])
    need(len(ds) == 19, 'complete wheel difference set')
    for z in ds-{(0, 0)}:
        orbit = set()
        w = z
        for _ in range(6):
            orbit.add(w)
            w = rotate(w)
        need(orbit == {x for x in ds if norm(x) == norm(z)}, 'one sixth-root orbit per norm')
    need(set(map(norm, ds)) == {0, 1, 3, 4}, 'difference norms')
    histogram = Counter(tuple(sorted(map(norm, row))) for row in product(ds-{(0, 0)}, repeat=3))
    need(set(histogram) == set(combinations_with_replacement((1, 3, 4), 3)), 'all norm triples')
    remaining = {case[0] for case in CASES}
    table = []
    # Check aligned representatives directly in Q[s], without a reducible
    # four-dimensional encoding for the six square-discriminant cases.
    reps = {1: (2, 0), 3: (3, 1), 4: (4, 0)}
    roots = {(F(2*a+b, 2), F(b, 2)) for a, b in W[1:]}
    for norms in sorted(histogram):
        m, n, p = norms
        delta = 4*m*n-(p-m-n)**2
        need(histogram[norms] % 6 == 0 and delta >= 0, 'complete common-rotation row count')
        rows = histogram[norms]//6
        if norms not in remaining:
            k = isqrt(delta//3)
            need(delta == 3*k*k, 'aligned discriminant')
            (a, b), (c, d) = reps[m], reps[n]
            # d*conj(e)*(K+k*s)/(2*m*n), with reps denominator two.
            A, B = a*c+3*b*d, b*c-a*d
            u = (F(A*(p-m-n)-3*B*k, 8*m*n), F(B*(p-m-n)+A*k, 8*m*n))
            need(u in roots, 'sixth-root aligned representative')
        else:
            need(rows == 108 and delta > 0, 'unaligned parameter upper bound')
        table.append({'norms': list(norms), 'delta': delta, 'common_rotation_rows': rows,
                      'root_upper_bound': rows*(1 if delta == 0 else 2), 'pair_aligned': norms not in remaining})
    return table


def orbit_check(case):
    """216 distinct ordered parameter pairs, generated by physical symmetries."""
    _, delta, q, U, V = case
    # A second operation used only for parameter orbits, never graph edges.
    def mul(x, y):
        A, B, C, D = x
        E, F_, G, H = y
        return (A*E-3*B*F_-delta*C*G+3*delta*D*H,
                A*F_+B*E-delta*(C*H+D*G),
                A*G+C*E-3*(B*H+D*F_), A*H+D*E+B*G+C*F_)
    conj = lambda z: (z[0], -z[1], -z[2], z[3])
    one = (F(1), F(0), F(0), F(0))
    u, v = (tuple(F(a, q) for a in z) for z in (U, V))
    roots = [(F(2*a+b, 2), F(b, 2), F(0), F(0)) for a, b in W[1:]]
    orbit = set()
    for a, b, c in permutations((one, u, v)):
        b, c = mul(b, conj(a)), mul(c, conj(a))
        for x, y in ((b, c), (conj(b), conj(c))):
            for r, s in product(roots, repeat=2):
                pair = mul(x, r), mul(y, s)
                need(pair[0] not in roots and pair[1] not in roots and mul(pair[0], conj(pair[1])) not in roots, 'nonalignment')
                orbit.add(pair)
    need(len(orbit) == 216, 'distinct symmetry parameters')
    encoded = [[[[c.numerator, c.denominator] for c in z] for z in pair] for pair in sorted(orbit)]
    return {'ordered_parameter_pairs': len(orbit), 'parameter_orbit_sha256': digest(encoded)}


def run(path, controls=True):
    cert = json.loads(path.read_text())
    need(cert.get('version') == 1 and len(cert.get('cases', [])) == 4, 'certificate header')
    table = coverage()
    results = []
    rejected = []
    for case, row in zip(CASES, cert['cases']):
        need(row['norms'] == list(case[0]), 'case identity/order')
        den, points, edges, ids = geometry(case)
        patterns = three_patterns(ids, edges)
        chi = 3 if any(r['failure'] is None for r in patterns) else 4
        colour_check(row['colours'], points, edges, chi)
        orbit = orbit_check(case)
        results.append({'norms': row['norms'], 'delta': case[1], 'denominator': den,
                        'vertices': len(points), 'unit_edges': len(edges), 'chromatic_number': chi,
                        'distinct_point_pairs_checked': len(points)*(len(points)-1)//2,
                        'point_sha256': digest(points), 'edge_sha256': digest(edges),
                        'three_colour_patterns': patterns, **orbit})
        if controls:
            a, b = edges[0]
            bad = list(row['colours']); bad[b] = bad[a]
            trials = [('monochromatic unit edge', ''.join(bad)), ('truncated word', row['colours'][:-1]),
                      ('out-of-range colour', '4'+row['colours'][1:])]
            for name, word in trials:
                try:
                    colour_check(word, points, edges, chi)
                except ValueError:
                    rejected.append([row['norms'], name])
                else:
                    raise RuntimeError('accepted corrupted certificate')
    return {'status': 'ALL_NONINJECTIVE_THREE_WHEEL_SUMS_ARE_FOUR_COLOURABLE',
            'norm_reduction': table, 'unaligned_congruence_classes': results,
            'nonaligned_collision_ordered_parameters': sum(r['ordered_parameter_pairs'] for r in results),
            'physical_pairs_checked': sum(r['distinct_point_pairs_checked'] for r in results),
            'necessary_order_for_nonfour_member': 343,
            'remaining_parameter_upper_bound_using_h4065': 902481,
            'rejected_colour_corruptions': rejected,
            'certificate_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'record_improvement': False, 'proof_replay_solver_calls': 0, 'proof_replay_CAS_calls': 0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE/'certificate.json')
    parser.add_argument('--check-expected', action='store_true')
    args = parser.parse_args()
    result = run(args.certificate)
    if args.check_expected:
        need(result == json.loads((HERE/'EXPECTED.json').read_text()), 'expected output')
    print(json.dumps(result, indent=2, sort_keys=True))
