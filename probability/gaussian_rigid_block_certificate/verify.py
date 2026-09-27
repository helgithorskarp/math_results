#!/usr/bin/env python3
"""Exact endpoint guards and deterministic controls; CPython 3.11, stdlib.

No arguments: reproduce EXPECTED.json, failing on any mismatch.
One JSON path: certify the supplied finite input (see README.md).
This checks rational hypotheses, not the handwritten motion theorem.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import comb
from pathlib import Path
import json
import sys


def need(test, message):
    if not test:
        raise ValueError(message)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), Q(0))


def sub(a, b):
    return [x-y for x, y in zip(a, b)]


def add(a, b):
    return [x+y for x, y in zip(a, b)]


def scale(a, c):
    return [c*x for x in a]


def norm2(a):
    return dot(a, a)


def center(rows):
    mean = [sum(v[j] for v in rows)/len(rows) for j in range(len(rows[0]))]
    return [sub(v, mean) for v in rows]


def det(a):
    a = [list(r) for r in a]
    answer = Q(1)
    for j in range(len(a)):
        p = next((i for i in range(j, len(a)) if a[i][j]), None)
        if p is None:
            return Q(0)
        if p != j:
            a[j], a[p] = a[p], a[j]
            answer = -answer
        v = a[j][j]
        answer *= v
        for i in range(j+1, len(a)):
            f = a[i][j]/v
            a[i] = [x-f*y for x, y in zip(a[i], a[j])]
    return answer


def psd(a):
    return all(det([[a[i][j] for j in ids] for i in ids]) >= 0
               for k in range(1, len(a)+1)
               for ids in combinations(range(len(a)), k))


def orthogonal_basis(rows):
    basis = []
    for row in rows:
        v = list(row)
        for u in basis:
            v = sub(v, scale(u, dot(v, u)/norm2(u)))
        if norm2(v):
            basis.append(v)
    return basis


def scatter(rows):
    return [[sum(v[i]*v[j] for v in rows) for j in range(3)] for i in range(3)]


def block_bound(rows, kappa):
    a = center(rows)
    basis = orthogonal_basis(a)
    p = [[sum((u[i]*u[j]/norm2(u) for u in basis), Q(0))
          for j in range(3)] for i in range(3)]
    s = scatter(a)
    return len(basis), psd([[s[i][j]-kappa*p[i][j] for j in range(3)]
                           for i in range(3)])


def rational(value):
    need(isinstance(value, (str, int)) and not isinstance(value, bool),
         'coordinates/bounds must be rational strings or integers')
    return Q(value)


def certify(data):
    need(isinstance(data, dict), 'input must be an object')
    need(set(data) <= {'x', 'y', 'blocks', 'kappa', 'k', 'mode'}, 'unknown field')
    x = [[rational(v) for v in row] for row in data['x']]
    y = [[rational(v) for v in row] for row in data['y']]
    n = len(x)
    need(n >= 2 and len(y) == n and all(len(r) == 3 for r in x+y), 'bad shape')
    need(len(set(map(tuple, x))) == n, 'source duplicates must be merged')
    blocks = data['blocks']
    need(isinstance(blocks, list) and len(blocks) >= 2
         and all(isinstance(b, list) and len(b) for b in blocks), 'bad blocks')
    labels = [i for b in blocks for i in b]
    need(all(type(i) is int for i in labels) and sorted(labels) == list(range(n)),
         'blocks must partition the labels')
    kappa = rational(data['kappa'])
    need(kappa > 0, 'kappa must be positive')
    mode = data.get('mode', 'direct')
    need(mode in ('direct', 'invariant'), 'bad mode')
    owner = {i: b for b, ids in enumerate(blocks) for i in ids}
    pairs = list(combinations(range(n), 2))
    lengths = {(i, j): norm2(sub(x[i], x[j])) for i, j in pairs}
    loss = {(i, j): lengths[i, j]-norm2(sub(y[i], y[j])) for i, j in pairs}
    base = {'sites': n, 'pairs': len(pairs), 'mode': mode}

    def no(reason):
        return dict(base, status='NOT_CERTIFIED', reason=reason)

    if min(loss.values()) < 0:
        return no('endpoint_expansion')
    if any(v != 0 for (i, j), v in loss.items() if owner[i] == owner[j]):
        return no('within_block_distance_changed')
    ranks = []
    for b in blocks:
        r, ok = block_bound([x[i] for i in b], kappa)
        if not ok:
            return no('block_scatter_bound')
        ranks.append(r)
    d2 = max(lengths.values())
    c = 8+2*d2/kappa
    cross = min(v for (i, j), v in loss.items() if owner[i] != owner[j])
    error = sum(norm2(sub(a, b)) for a, b in zip(x, y))
    if mode == 'invariant':
        a, b = center(x), center(y)
        gram = [[dot(a[i], a[j])-dot(b[i], b[j]) for j in range(n)]
                for i in range(n)]
        f = sum(norm2(row) for row in gram)
        # Different representation: reconstruct the Gram error from distances.
        delta = [[Q(0) if i == j else loss[min(i, j), max(i, j)]
                  for j in range(n)] for i in range(n)]
        means = [sum(row)/n for row in delta]
        overall = sum(means)/n
        reconstructed = [[-(delta[i][j]-means[i]-means[j]+overall)/2
                          for j in range(n)] for i in range(n)]
        need(gram == reconstructed, 'double-centering identity failed')
        if f == 0:
            return dict(base, status='CERTIFIED_CONGRUENT', block_ranks=ranks)
        k = rational(data['k'])
        need(k > 0, 'k must be positive')
        s = scatter(a)
        if not psd([[s[i][j]-(k if i == j else 0) for j in range(3)]
                    for i in range(3)]):
            return no('global_scatter_bound')
        error = 2*f/k
    if error > kappa:
        return no('displacement_budget')
    if cross < c*error:
        return no('cross_budget')
    return dict(base, status='CERTIFIED_ALL_VARIANCES', block_ranks=ranks,
                error_bound=str(error), diameter_squared=str(d2),
                budget_factor=str(c), cross_loss=str(cross),
                cross_margin=str(cross-c*error),
                tight_pairs=sum(v == 0 for v in loss.values()))


def rot(v, t, axis):
    if axis is None:
        return v[:]
    c, s = (1-t*t)/(1+t*t), 2*t/(1+t*t)
    i, j = (0, 1) if axis == 'z' else (1, 2)
    out = v[:]
    out[i], out[j] = c*v[i]-s*v[j], s*v[i]+c*v[j]
    return out


V = [[Q(v) for v in row] for row in
     [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]]
CENTERS = [[Q(v) for v in row] for row in [(-16, 0, 0), (16, 0, 0), (0, 16, 0)]]


def family(t, mixed=False):
    offsets = ([[-1, 0, 0], [1, 0, 0]],
               [[-1, -1, 0], [-1, 1, 0], [1, -1, 0], [1, 1, 0]],
               [[0, 0, 0]]) if mixed else (V, V, V)
    x, y, blocks = [], [], []
    for c, vs, axis in zip(CENTERS, offsets, (None, 'z', 'x')):
        ids = []
        for v in vs:
            v = list(map(Q, v))
            ids.append(len(x))
            x.append(add(c, v))
            y.append(add(scale(c, 1-t), rot(v, t, axis)))
        blocks.append(ids)
    return {'x': x, 'y': y, 'blocks': blocks, 'kappa': 2 if mixed else 4,
            'k': 12, 'mode': 'direct'}


def serial(data):
    if isinstance(data, Q):
        return str(data)
    if isinstance(data, dict):
        return {k: serial(v) for k, v in data.items()}
    if isinstance(data, list):
        return [serial(v) for v in data]
    return data


# Low-degree exact polynomials, coefficients in increasing order.
def trim(p):
    p = list(p)
    while len(p) > 1 and not p[-1]:
        p.pop()
    return p


def pa(a, b):
    return trim([(a[i] if i < len(a) else 0)+(b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def pm(a, b):
    p = [Q(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            p[i+j] += x*y
    return trim(p)


def ps(a, c):
    return trim([c*x for x in a])


def bernstein(p, endpoint):
    n = len(p)-1
    return [sum((p[j]*endpoint**j*Q(comb(i, j), comb(n, j))
                 for j in range(i+1)), Q(0)) for i in range(n+1)]


def polynomial_controls():
    den = [Q(1), Q(0), Q(1)]
    den2 = pm(den, den)
    x, nums = [], []
    for c, axis in zip(CENTERS, (None, 'z', 'x')):
        for v in V:
            x.append(add(c, v))
            rv = [ps(den, a) for a in v]
            if axis is not None:
                i, j = (0, 1) if axis == 'z' else (1, 2)
                rv[i] = [v[i], -2*v[j], -v[i]]
                rv[j] = [v[j], 2*v[i], -v[j]]
            nums.append([pa(ps(pm([Q(1), Q(-1)], den), c[j]), rv[j])
                         for j in range(3)])
    energy = [Q(0)]
    for v, u in zip(x, nums):
        for j in range(3):
            change = pa(u[j], ps(den, -v[j]))
            energy = pa(energy, pm(change, change))
    expected = pm(pa(ps(pm([Q(0), Q(0), Q(1)], den), Q(3072)),
                     [Q(0), Q(0), Q(64)]), den)
    need(energy == expected, 'family energy polynomial')
    tight, strict = 0, 0
    margins = []
    for i, j in combinations(range(12), 2):
        p = ps(den2, norm2(sub(x[i], x[j])))
        for k in range(3):
            diff = pa(nums[i][k], ps(nums[j][k], -1))
            p = pa(p, ps(pm(diff, diff), -1))
        if i//4 == j//4:
            need(p == [0], 'within-block polynomial')
            tight += 1
        else:
            p = pa(p, ps(pm([Q(0), Q(1)], den2), -192))
            need(p[0] == 0, 'loss polynomial constant')
            b = bernstein(p[1:], Q(1, 4))
            need(min(b) > 0, 'whole-interval cross-loss bound')
            margins.append(min(b))
            strict += 1
    # The exact square completion from the universal proof.
    lhs = [Q(8)-Q(185, 32), -Q(5, 2), Q(2)]
    rhs = pa(ps(pm([-Q(5, 8), Q(1)], [-Q(5, 8), Q(1)]), 2), [Q(23, 16)])
    need(lhs == rhs, 'universal budget square completion')
    need(Q(588)*3136/192 == 9604 and 9604 < 16384, 'family guard interval')
    need(Q(3136, 16384**2) < 4, 'family displacement interval')
    return {'tight_polynomials': tight, 'cross_polynomials': strict,
            'cross_interval': '0<t<=1/4',
            'minimum_positive_Bernstein_coefficient': str(min(margins)),
            'certified_motion_interval': '0<t<=1/16384',
            'energy_numerator_degree': len(energy)-1,
            'square_completion_remainder': '23/16'}


def controls():
    results = {}

    def run(name, data, status, reason=None):
        out = certify(serial(data))
        need(out['status'] == status, f'{name}: unexpected status {out}')
        if reason is not None:
            need(out['reason'] == reason, f'{name}: unexpected reason')
        results[name] = out
        return out

    small = family(Q(1, 16384))
    main = run('three_tetrahedra_direct', small, 'CERTIFIED_ALL_VARIANCES')
    need(main['diameter_squared'] == '1160' and main['budget_factor'] == '588',
         'family geometry')
    pairs = [a+b for a, b in zip(small['x'], small['y'])]
    rank = len(orthogonal_basis([sub(p, pairs[0]) for p in pairs[1:]]))
    need(rank == 6, 'paired affine rank')
    delta = sub(sub(small['x'][4], small['x'][5]),
                sub(small['y'][4], small['y'][5]))
    need(norm2(delta) > 0, 'straight-path positive endpoint derivative')
    invariant = family(Q(1, 2**32))
    invariant['mode'] = 'invariant'
    invariant['y'] = [[-v[0]+7, v[1]-3, v[2]+5] for v in invariant['y']]
    run('reflected_translated_invariant', invariant, 'CERTIFIED_ALL_VARIANCES')
    run('mixed_block_dimensions', family(Q(1, 2**20), True), 'CERTIFIED_ALL_VARIANCES')
    identity = family(Q(0))
    run('identity', identity, 'CERTIFIED_ALL_VARIANCES')
    identity['mode'] = 'invariant'
    identity['y'] = [[-v[0]+7, v[1]-3, v[2]+5] for v in identity['x']]
    run('congruent_independent_frames', identity, 'CERTIFIED_CONGRUENT')
    reverse = family(Q(1, 16384))
    reverse['x'], reverse['y'] = reverse['y'], reverse['x']
    run('expansion', reverse, 'NOT_CERTIFIED', 'endpoint_expansion')
    shrink = family(Q(0))
    shrink['y'] = [scale(v, Q(999, 1000)) for v in shrink['x']]
    run('broken_block', shrink, 'NOT_CERTIFIED', 'within_block_distance_changed')
    bad = family(Q(1, 16384)); bad['kappa'] = 5
    run('invalid_block_floor', bad, 'NOT_CERTIFIED', 'block_scatter_bound')
    big = family(Q(1, 4))
    run('large_displacement', big, 'NOT_CERTIFIED', 'displacement_budget')
    insufficient = family(Q(1, 256))
    run('insufficient_cross_loss', insufficient, 'NOT_CERTIFIED', 'cross_budget')
    invalid_global = family(Q(1, 2**32))
    invalid_global.update(mode='invariant', k=100)
    run('invalid_global_floor', invalid_global, 'NOT_CERTIFIED', 'global_scatter_bound')
    malformed = 0
    for key, value in [('kappa', 0), ('blocks', [[0], [0]]), ('mode', 'unknown')]:
        case = serial(family(Q(1, 16384)))
        case[key] = value
        try:
            certify(case)
        except ValueError:
            malformed += 1
        else:
            raise ValueError('malformed input accepted')
    return {'status': 'RIGID_BLOCK_ALL_VARIANCE_CONTROLS_PASSED',
            'paired_affine_rank': rank,
            'straight_path_endpoint_derivative': str(norm2(delta)),
            'polynomial_controls': polynomial_controls(),
            'malformed_inputs_rejected': malformed, 'controls': results}


def main():
    if len(sys.argv) == 2:
        result = certify(json.loads(Path(sys.argv[1]).read_text()))
    else:
        need(len(sys.argv) == 1, 'usage: python3 -B verify.py [INPUT.json]')
        result = controls()
        expected = json.loads(Path(__file__).with_name('EXPECTED.json').read_text())
        need(result == expected, 'EXPECTED.json mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
