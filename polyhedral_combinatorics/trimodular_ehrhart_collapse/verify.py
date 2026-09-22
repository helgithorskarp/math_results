#!/usr/bin/env python3
"""Exact witness proof and corroboration of the uniform construction.

CPython 3.11+, standard library. The fixed q=3 all-n certificate uses only
Ehrhart's degree/denominator theorem, exhaustive vertices, and exact counts.
The all-q geometry and Fourier argument are written in PROOF.md.
"""
from collections import Counter
from fractions import Fraction as F
from functools import reduce
from hashlib import sha256
from itertools import combinations, product
from math import gcd, lcm
from pathlib import Path
import json
import sys
from construct import construct

HERE = Path(__file__).resolve().parent


def require(test, message):
    if not test:
        raise ValueError(message)


def det(a):
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def integral(v):
    return all(x.denominator == 1 for x in v)


def geometry(facets):
    require(len(facets) == 12, 'wrong facet count')
    for a, b in facets:
        require(len(a) == 3 and all(type(x) is int for x in a) and type(b) is int,
                'nonintegral facet description')
        require(reduce(gcd, map(abs, a)) == 1, 'nonprimitive normal')
    # The first six halfspaces bound three independent linear coordinates.
    require(all(facets[2 * i + 1][0] == tuple(-x for x in facets[2 * i][0])
                for i in range(3)), 'missing opposite bounding facets')
    require(det([facets[2 * i][0] for i in range(3)]) != 0, 'unbounded box coordinates')
    vertices, minors = {}, Counter()
    for ids in combinations(range(12), 3):
        a = [facets[i][0] for i in ids]
        b = [facets[i][1] for i in ids]
        d = det(a)
        minors[abs(d)] += 1
        if not d:
            continue
        v = []
        for j in range(3):
            aj = [list(row) for row in a]
            for i in range(3):
                aj[i][j] = b[i]
            v.append(F(det(aj), d))
        v = tuple(v)
        if all(dot(row, v) <= rhs for row, rhs in facets):
            vertices[v] = tuple(i for i, (row, rhs) in enumerate(facets) if dot(row, v) == rhs)
    require(len(vertices) == 20, 'wrong number of vertices')
    require(all(len(a) == 3 for a in vertices.values()), 'not simple')
    vv = list(vertices)
    require(any(det([sub(vv[i], vv[0]), sub(vv[j], vv[0]), sub(vv[k], vv[0])])
                for i, j, k in combinations(range(1, len(vv)), 3)), 'not full dimensional')
    for i in range(12):
        face = [v for v, ids in vertices.items() if i in ids]
        require(len(face) >= 3 and any(any(cross(sub(a, face[0]), sub(b, face[0])))
                    for a, b in combinations(face[1:], 2)), 'redundant facet')
    edges = []
    for i, j in combinations(range(12), 2):
        face = [v for v, ids in vertices.items() if i in ids and j in ids]
        if len(face) == 2:
            require(any(integral(v) for v in face), 'edge has no integral endpoint')
            edges.append(face)
    require(len(edges) == 30, 'wrong edge count')
    fractional = [(v, ids) for v, ids in vertices.items() if not integral(v)]
    require(len(fractional) == 2, 'wrong fractional vertex count')
    require(not set(fractional[0][1]) & set(fractional[1][1]), 'fractional vertices share a facet')
    denominator = lcm(*(x.denominator for v in vertices for x in v))
    return vertices, minors, fractional, denominator


def ceil_q(x):
    return -((-x.numerator) // x.denominator)


def count_h(facets, vertices, n, literal=False):
    """Direct Z^3 counts from the stored halfspaces, not congruence counting."""
    bounds = [(ceil_q(n * min(v[i] for v in vertices)),
               (n * max(v[i] for v in vertices)).__floor__()) for i in range(3)]
    if literal:
        return sum(all(dot(a, v) <= n * b for a, b in facets)
                   for v in product(*(range(lo, hi + 1) for lo, hi in bounds)))
    total = 0
    for x in range(bounds[0][0], bounds[0][1] + 1):
        for y in range(bounds[1][0], bounds[1][1] + 1):
            lo, hi = bounds[2]
            for (a, b, c), rhs in facets:
                z = n * rhs - a * x - b * y
                if c > 0:
                    hi = min(hi, z // c)
                elif c < 0:
                    lo = max(lo, -((-z) // c))
                elif z < 0:
                    hi = lo - 1
                    break
            if lo <= hi:
                total += hi - lo + 1
    return total


def count_caps(model, n):
    """Different representation: congruence-filtered cube minus open caps."""
    q, side = model['q'], model['side']
    total = ((side * n + 1) ** 3 - 1) // q + int(n % q == 0)
    for cut in model['cuts']:
        steps, signs = cut['steps'], cut['signs']
        scale = lcm(*steps)
        weights = [scale // r for r in steps]
        alpha = (signs[0], signs[1], -2 * signs[2])
        inv = pow(alpha[2], -1, q)
        removed = 0
        for a in range(steps[0] * n):
            for b in range(steps[1] * n):
                hi = (scale * n - 1 - weights[0] * a - weights[1] * b) // weights[2]
                if hi < 0:
                    break
                residue = ((-n - alpha[0] * a - alpha[1] * b) * inv) % q
                if residue <= hi:
                    removed += (hi - residue) // q + 1
        total -= removed
    return total


def polynomial(q):
    s = (q - 1) // 2
    epsilon = gcd(s + 1, 2)
    volume = F(95 * q * q - q, 12)
    quadratic = F(s * s + 45 * s + 22 + epsilon, 2)
    at_one = 8 * q * q + 12 * q + 6 - 2 * (s // 2)
    linear = at_one - 1 - volume - quadratic
    return [F(1), linear, quadratic, volume]


def evaluate(coefficients, n):
    return sum(a * n ** j for j, a in enumerate(coefficients))


def reduce_cyclic(a):
    # Q[z]/(1+z+...+z^(q-1)): all nontrivial qth roots, not only primitive ones.
    return tuple(x - a[-1] for x in a)


def multiply(a, b):
    q = len(a)
    out = [F(0)] * q
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[(i + j) % q] += x * y
    return reduce_cyclic(out)


def reciprocal(q, a):
    require(gcd(a, q) == 1, 'nonunit character exponent')
    out = [F(0)] * q
    for r in range(1, q):
        out[(a * r) % q] -= F(r, q)
    out = reduce_cyclic(out)
    factor = [F(0)] * q
    factor[0] += 1
    factor[a % q] -= 1
    require(multiply(out, factor) == (F(1),) + (F(0),) * (q - 1), 'bad reciprocal')
    return out


def profile(q, exponents):
    out = (F(1),) + (F(0),) * (q - 1)
    for a in exponents:
        out = multiply(out, reciprocal(q, a))
    return out


def main():
    witness_path = HERE / 'WITNESS.json'
    witness = json.loads(witness_path.read_text())
    require(len(witness['A']) == len(witness['b']) == 12, 'truncated witness')
    facets = [(tuple(a), b) for a, b in zip(witness['A'], witness['b'])]
    vertices, minors, bad, denominator = geometry(facets)
    require(denominator == witness['vertex_denominator'] == 3, 'denominator')
    require(max(minors) == witness['maximum_full_minor'] == 3, 'not trimodular')
    require(sum(minors.values()) == 220, 'minor enumeration incomplete')
    require(all(abs(det([facets[i][0] for i in ids])) == 3 for v, ids in bad), 'bad active index')
    expected_bad = {(F(1), F(0), F(-2, 3)), (F(7), F(6), F(-20, 3))}
    require({v for v, ids in bad} == expected_bad, 'wrong fractional vertices')
    model = construct(3)
    require(model['facets'] == facets, 'literal witness and construction differ')
    coefficients = witness['ehrhart_coefficients_constant_first']
    require(coefficients == [1, 7, 35, 71] == polynomial(3), 'wrong cubic')
    counts = []
    for n in range(15):
        direct = count_h(facets, vertices, n)
        decomposed = count_caps(model, n)
        require(direct == decomposed == evaluate(coefficients, n), 'exact count mismatch')
        if n <= 3:
            require(count_h(facets, vertices, n, literal=True) == direct, 'literal Z3 count mismatch')
        counts.append(direct)
    require(all(len([n for n in range(12) if n % 3 == r]) == 4 for r in range(3)),
            'insufficient constituent-polynomial certificate')

    general = []
    for q in (3, 5, 7, 9, 15, 25):
        model = construct(q)
        vv, mm, bad, denominator = geometry(model['facets'])
        require(denominator == q, 'general denominator')
        require(all(abs(det([model['facets'][i][0] for i in ids])) == q for v, ids in bad),
                'general active index')
        values = []
        for n in range(7):
            a = count_h(model['facets'], vv, n)
            b = count_caps(model, n)
            require(a == b == evaluate(polynomial(q), n), 'uniform formula count mismatch')
            values.append(a)
        plus, minus = profile(q, (1, 1, -2)), profile(q, (-1, -1, 2))
        require(all(a + b == 0 for a, b in zip(plus, minus)), 'paired modes do not cancel')
        general.append({'q': q, 'counts_n_0_through_6': values,
                        'coefficients_constant_first': list(map(str, polynomial(q))),
                        'maximum_full_minor': max(mm)})
    # Exact real-part exhaustion underlying the low-dimensional obstruction.
    real_parts = {}
    for g in (1, 2):
        values = set()
        for eta in product((1, 2), repeat=g):
            a, b = profile(3, eta), profile(3, tuple(-x for x in eta))
            real = tuple((x + y) / 2 for x, y in zip(a, b))
            require(all(x == 0 for x in real[1:]) and real[0] > 0, 'nonpositive ternary mode')
            values.add(str(real[0]))
        real_parts[str(g)] = sorted(values)
    wrong1, wrong2 = profile(5, (1, 1, 1)), profile(5, (-1, -1, -1))
    require(any(a + b for a, b in zip(wrong1, wrong2)), 'non-zero-sum profile control')
    rejected = 0
    for q in (1, 2, 4, -3, 3.0):
        try:
            construct(q)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('invalid modulus accepted')
    wrong_coefficients = coefficients[:]
    wrong_coefficients[1] += 1
    require(evaluate(wrong_coefficients, 1) != counts[1], 'wrong polynomial survived')
    result = {'status': 'pass', 'fixed_witness': {
        'vertices': len(vertices), 'edges': 30, 'facets': 12, 'simple': True,
        'denominator': 3,
        'absolute_full_minor_histogram': {str(k): minors[k] for k in sorted(minors)},
        'fractional_vertices': [list(map(str, v)) for v in sorted(expected_bad)],
        'counts_n_0_through_14': counts,
        'all_n_certificate': 'degree<=3 and period dividing3; four values in each residue suffice',
        'independent_holdouts': 3, 'literal_Z3_counts': 4,
        'witness_sha256': sha256(witness_path.read_bytes()).hexdigest()},
        'uniform_family_checks': general, 'ternary_positive_real_parts': real_parts,
        'invalid_inputs_rejected': rejected,
        'universal_geometry_and_Fourier_proof': 'PROOF.md; finite checks are corroboration'}
    if '--check' in sys.argv:
        require(result == json.loads((HERE / 'EXPECTED.json').read_text()), 'expected output mismatch')
        print('PASS: trimodular geometry, all-n Ehrhart certificate, odd-denominator construction, and cancellation.')
    else:
        print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
