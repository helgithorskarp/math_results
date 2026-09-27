#!/usr/bin/env python3
"""Exact finite controls, not a formal proof of the analytic theorem."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from pathlib import Path
import argparse
import hashlib
import json
import random

HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), F(0))


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def dist2(x, y):
    z = sub(x, y)
    return dot(z, z)


def mean(points, weights):
    return tuple(sum((w*x[j] for w, x in zip(weights, points)), F(0))
                 for j in range(3))


def centered(points, weights):
    m = mean(points, weights)
    return [sub(x, m) for x in points]


def matrix_moment(x, y, p):
    return [[sum((w*a[i]*b[j] for w, a, b in zip(p, x, y)), F(0))
             for j in range(3)] for i in range(3)]


def norm2_matrix(a):
    return sum((v*v for row in a for v in row), F(0))


def moments(x, y, p):
    """Q from a constant-sized centered moment table, no pair loop."""
    x, y = centered(x, p), centered(y, p)
    a, b, c = matrix_moment(x, x, p), matrix_moment(y, y, p), matrix_moment(x, y, p)
    h = [dot(v, v)-dot(w, w) for v, w in zip(x, y)]
    eh = sum((w*z for w, z in zip(p, h)), F(0))
    eh2 = sum((w*z*z for w, z in zip(p, h)), F(0))
    q = 2*eh2+2*eh**2+4*(norm2_matrix(a)+norm2_matrix(b)-2*norm2_matrix(c))
    return 2*eh, q, a


def pair_moments(x, y, p):
    d = q = F(0)
    losses = []
    for i in range(len(p)):
        for j in range(i):
            loss = dist2(x[i], x[j])-dist2(y[i], y[j])
            losses.append(loss)
            weight = 2*p[i]*p[j]
            d += weight*loss
            q += weight*loss**2
    return d, q, losses


def raw_second_loss(x, y, p):
    """Uncentered six-coordinate formula for a fixed sixteen-feature list."""
    z = [a+b for a, b in zip(x, y)]
    sign = [1, 1, 1, -1, -1, -1]
    m = [sum((w*a[i] for w, a in zip(p, z)), F(0)) for i in range(6)]
    mm = [[sum((w*a[i]*a[j] for w, a in zip(p, z)), F(0)) for j in range(6)]
          for i in range(6)]
    h = [sum((sign[i]*a[i]**2 for i in range(6)), F(0)) for a in z]
    v = [sum((w*b*a[i] for w, b, a in zip(p, h, z)), F(0)) for i in range(6)]
    eh = sum((w*a for w, a in zip(p, h)), F(0))
    eh2 = sum((w*a*a for w, a in zip(p, h)), F(0))
    trace = sum((sign[i]*sign[j]*mm[i][j]**2 for i in range(6) for j in range(6)), F(0))
    return 2*eh2+2*eh**2+4*trace-8*sum((v[i]*sign[i]*m[i] for i in range(6)), F(0))


def det(a):
    if len(a) == 1:
        return a[0][0]
    return sum(((-1)**j*a[0][j]*det([row[:j]+row[j+1:] for row in a[1:]])
                for j in range(len(a))), F(0))


def psd(a):
    return all(det([[a[i][j] for j in s] for i in s]) >= 0
               for k in range(1, 4) for s in combinations(range(3), k))


def guard(x, y, p, s=F(1)):
    need(len(x) == len(y) == len(p) and len(p) > 0, 'lengths')
    need(all(len(z) == 3 for z in x+y), 'dimension')
    need(all(isinstance(a, (int, F)) for z in x+y for a in z)
         and all(isinstance(a, (int, F)) for a in p)
         and isinstance(s, (int, F)), 'exact rational input required')
    s = F(s)
    need(s > 0, 'variance')
    need(all(w >= 0 for w in p) and sum(p) == 1, 'prior')
    active = [i for i, w in enumerate(p) if w > 0]
    x, y, p = [x[i] for i in active], [y[i] for i in active], [p[i] for i in active]
    d, q, losses = pair_moments(x, y, p)
    need(all(z >= 0 for z in losses), 'not a contraction')
    dm, qm, cov = moments(x, y, p)
    need((d, q) == (dm, qm), 'moment formula mismatch')
    d, q = d/s, q/(s*s)
    if d == 0:
        return {'status': 'ZERO_LOSS', 'd': d, 'Q': q, 'middle_margin': F(0)}
    if any(dot(z, z) > s/4 for z in centered(x, p)):
        return {'status': 'UNRESOLVED', 'reason': 'radius'}
    a = [[cov[i][j]/s-(F(1, 2**15) if i == j else 0) for j in range(3)]
         for i in range(3)]
    if not psd(a):
        return {'status': 'UNRESOLVED', 'reason': 'covariance'}
    if q > d/F(2**48):
        return {'status': 'UNRESOLVED', 'reason': 'loss_moment'}
    return {'status': 'SIGNED_MIDDLE', 'd': d, 'Q': q,
            'middle_margin': d/F(2**40)}


VERTICES = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]


def family(t, alpha, core, outer):
    need(0 <= t <= F(1, 2**40), 't range')
    need(0 <= alpha <= t/F(2**65), 'alpha range')
    need(sum(core) == sum(outer) == 1, 'conditional prior')
    need(min(core) >= F(1, 8) and min(outer) >= 0, 'conditional prior range')
    x = [tuple(F(z, 80) for z in v) for v in VERTICES]
    x += [tuple(-F(z, 4) for z in v) for v in VERTICES]
    y = [tuple((1-t)*F(z, 80) for z in v) for v in VERTICES]
    y += [tuple((1-t)*F(29*z, 120) for z in v) for v in VERTICES]
    p = [(1-alpha)*w for w in core]+[alpha*w for w in outer]
    return x, y, p


def monomials(degree):
    return [(i, j, k) for i in range(degree+1)
            for j in range(degree+1-i) for k in range(degree+1-i-j)
            if i+j+k > 0]


def feature_columns(x, y, p, q=2):
    powers = monomials(2*q)
    xc, yc = centered(x, p), centered(y, p)
    columns = []
    for a, b, ac, bc in zip(x, y, xc, yc):
        column = [F(1)]
        column += [a[0]**i*a[1]**j*a[2]**k for i, j, k in powers]
        column += [b[0]**i*b[1]**j*b[2]**k for i, j, k in powers]
        column += [ac[i]*bc[j] for i in range(3) for j in range(3)]
        column += [dot(ac, ac)*dot(bc, bc)]
        columns.append(column)
    need(all(len(c) == 2*comb(2*q+3, 3)-1+10 for c in columns), 'feature count')
    return columns


def null_vector(columns):
    """Definition-level rational elimination; return one exact dependence."""
    n = len(columns)
    rows = [list(r) for r in zip(*columns)]
    pivot_columns = []
    r = 0
    for j in range(n):
        k = next((i for i in range(r, len(rows)) if rows[i][j]), None)
        if k is None:
            continue
        rows[r], rows[k] = rows[k], rows[r]
        value = rows[r][j]
        rows[r] = [z/value for z in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][j]:
                c = rows[i][j]
                rows[i] = [a-c*b for a, b in zip(rows[i], rows[r])]
        pivot_columns.append(j)
        r += 1
        if r == len(rows):
            break
    free = next((j for j in range(n) if j not in pivot_columns), None)
    if free is None:
        return None
    v = [F(0)]*n
    v[free] = F(1)
    for i, j in enumerate(pivot_columns):
        v[j] = -rows[i][free]
    need(all(sum((v[j]*columns[j][i] for j in range(n)), F(0)) == 0
             for i in range(len(columns[0]))), 'bad affine dependence')
    return v


def compress(columns, weights):
    active, w = list(range(len(weights))), list(weights)
    while True:
        v = null_vector([columns[i] for i in active])
        if v is None:
            break
        step = min(w[i]/v[i] for i in range(len(w)) if v[i] > 0)
        w = [a-step*b for a, b in zip(w, v)]
        keep = [i for i, a in enumerate(w) if a > 0]
        need(all(a >= 0 for a in w) and len(keep) < len(active), 'bad elimination')
        active, w = [active[i] for i in keep], [w[i] for i in keep]
    return active, w


def run():
    checks = {}
    inputs = json.loads((HERE/'INPUTS.json').read_text())
    root = HERE.parent.parent
    for item in inputs['files']:
        need(hashlib.sha256((root/item['path']).read_bytes()).hexdigest() == item['sha256'],
             'dependency bytes changed: '+item['path'])
    checks['dependency_pins'] = len(inputs['files'])
    constants = [F(1)+F(3, 4)+F(3, 4)**2/2 > 2,
                 3**16 < 2**26, F(44, 7)**3 < 256,
                 F(121, 96) > 1, F(363, 1600) < F(1, 4),
                 F(1, 25600) > F(1, 2**15),
                 F(2161, 2400) == F(2**8, 400)+F(102400, 3*2**17),
                 F(2161, 2400) < 1,
                 F(6400, 2**40) < F(1, 100),
                 F(1, 2**48)*2**15 == F(1, 2**33),
                 F(1, 2**33)/128 == F(1, 2**40),
                 (1+F(399, 2**105))/6400 < F(1, 6000),
                 1-F(1163, 3*2**105) > 0,
                 3*(20+F(58, 3)*(1-F(1, 2**40)))**2/F(80**2) > F(9, 16)]
    need(all(constants), 'constant chain')
    checks['rational_constant_comparisons'] = len(constants)

    core = [[F(1, 4)]*4]
    core += [[F(5, 8) if i == j else F(1, 8) for i in range(4)] for j in range(4)]
    outer = [[F(1, 4)]*4]
    outer += [[F(int(i == j)) for i in range(4)] for j in range(4)]
    count = 0
    representative = None
    for exponent, part, c, r in product([40, 64, 100], [F(0), F(1, 2), F(1)], core, outer):
        t = F(1, 2**exponent)
        alpha = part*t/F(2**65)
        x, y, p = family(t, alpha, c, r)
        result = guard(x, y, p)
        need(result['status'] == 'SIGNED_MIDDLE', 'family guard failed')
        d, q, _ = pair_moments(x, y, p)
        need(d >= 3*t/F(51200), 'uniform d bound')
        need(q <= F(2161, 2400*2**48)*d, 'uniform ratio bound')
        count += 1
        if exponent == 40 and part == 1 and c == core[0] and r == outer[0]:
            representative = result
    checks['family_finite_controls'] = count
    checks['representative'] = representative
    x, y, p = family(F(1, 2**40), F(1, 2**105), core[0], outer[0])
    for scale in [F(1, 3), F(3, 2), F(7)]:
        result = guard([tuple(scale*z for z in a) for a in x],
                       [tuple(scale*z for z in a) for a in y], p, scale*scale)
        need(result == representative, 'variance normalization')
    checks['exact_variance_rescalings'] = 3
    x, y, p = family(F(0), F(0), core[0], outer[0])
    need(guard(x, y, p)['status'] == 'ZERO_LOSS', 'zero endpoint')
    checks['zero_loss_endpoint'] = True
    for i, j in combinations(range(8), 2):
        if j < 4:
            expected = (F(8), F(8))
        elif i >= 4:
            expected = (F(3200), F(26912, 9))
        elif i == j-4:
            expected = (F(1323), F(3025, 3))
        else:
            expected = (F(1163), F(1163))
        need((6400*dist2(x[i], x[j]), 6400*dist2(y[i], y[j])) == expected,
             'template distance table')
    checks['template_pairs'] = 28

    rng = random.Random(16032026)
    for n in range(2, 11):
        for _ in range(8):
            x = [tuple(F(rng.randrange(-9, 10), 20) for j in range(3)) for i in range(n)]
            y = [tuple(abs(z)/2 for z in a) for a in x]
            w = [rng.randrange(1, 10) for i in range(n)]
            p = [F(a, sum(w)) for a in w]
            d, q, losses = pair_moments(x, y, p)
            dm, qm, _ = moments(x, y, p)
            need((d, q) == (dm, qm) and q == raw_second_loss(x, y, p)
                 and min(losses) >= 0, 'independent Q expansion')
    checks['independent_pair_vs_moment_controls'] = 72
    checks['uncentered_six_coordinate_controls'] = 72

    x = [(F(i), F(0), F(0)) for i in [0, 1, 3]]
    y = [(F(i, 10), F(0), F(0)) for i in [0, 1, 2]]
    p = [F(1, 3)]*3
    d1, q1, _ = pair_moments(x, y, p)
    d2, q2, _ = pair_moments(x, [y[1], y[0], y[2]], p)
    need(d1 == d2 and q1 != q2, 'marginal-only countercontrol')
    checks['same_marginals_different_Q'] = {'d': d1, 'Q1': q1, 'Q2': q2}

    x = [(F(i, 2**16), F(i*i, 2**16), F(i**3, 2**16)) for i in range(-15, 16)]
    y = [tuple(abs(z)/2 for z in a) for a in x]
    p = [F(1, len(x))]*len(x)
    columns = feature_columns(x, y, p)
    active, weights = compress(columns, p)
    need(len(active) < len(x) and len(active) <= 79, 'no cubature reduction')
    before = [sum((w*c[j] for w, c in zip(p, columns)), F(0)) for j in range(79)]
    after = [sum((w*columns[i][j] for i, w in zip(active, weights)), F(0)) for j in range(79)]
    need(before == after, 'feature mismatch')
    dm, qm, covariance = moments(x, y, p)
    dn, qn, covariance_n = moments([x[i] for i in active], [y[i] for i in active], weights)
    need((dm, qm, covariance) == (dn, qn, covariance_n), 'guard moments changed')
    checks['cubature'] = {'input_pairs': len(x), 'output_pairs': len(active),
                          'features_matched': 79, 'active_indices': active,
                          'weights': weights, 'd': dm, 'Q': qm}

    rejected = []
    x, y, p = family(F(1, 2**100), F(0), core[0], outer[0])
    bad_p = p.copy(); bad_p[0] = F(-1)
    try:
        guard(x, y, bad_p)
    except ValueError:
        rejected.append('negative_prior')
    else:
        raise ValueError('accepted negative prior')
    try:
        guard(x, [tuple(2*z for z in a) for a in x], p)
    except ValueError:
        rejected.append('expanding_map')
    else:
        raise ValueError('accepted expanding map')
    large_x = [tuple(100*z for z in a) for a in x]
    large_y = [tuple(100*z for z in a) for a in y]
    need(guard(large_x, large_y, p).get('reason') == 'radius', 'radius rejection')
    rejected.append('radius')
    need(guard([(F(-1, 8), F(0), F(0)), (F(1, 8), F(0), F(0))],
               [(F(0),)*3]*2, [F(1, 2)]*2).get('reason') == 'covariance', 'covariance rejection')
    rejected.append('covariance')
    t = F(1, 2**100)
    x, y, _ = family(t, F(0), core[0], outer[0])
    p = [(1-t)/4]*4+[t/4]*4
    d, q, _ = pair_moments(x, y, p)
    need(d*d <= d/F(2**48) < q, 'Q is not d squared control')
    need(guard(x, y, p).get('reason') == 'loss_moment', 'loss moment rejection')
    rejected.append('substitution_of_d_squared_for_Q')
    # A signed family certificate cannot be accepted with a changed atom weight.
    altered = weights.copy(); altered[0] += F(1, 10**6); altered[1] -= F(1, 10**6)
    changed = [sum((w*columns[i][j] for i, w in zip(active, altered)), F(0)) for j in range(79)]
    need(changed != before, 'corrupted cubature was invisible')
    rejected.append('altered_cubature_weight')
    checks['rejected_controls'] = rejected
    checks['status'] = 'LOSS_MOMENT_MIDDLE_PASS'
    return checks


def encode(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {k: encode(v) for k, v in x.items()}
    if isinstance(x, list):
        return [encode(v) for v in x]
    return x


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit', action='store_true', help='print compact computed record')
    args = parser.parse_args()
    record = encode(run())
    if args.emit:
        print(json.dumps(record, indent=2, sort_keys=True))
    else:
        need(record == json.loads((HERE/'EXPECTED.json').read_text()), 'expected record mismatch')
        print(record['status'])
