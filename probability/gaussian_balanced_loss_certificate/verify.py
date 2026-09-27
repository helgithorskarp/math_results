#!/usr/bin/env python3
"""Independent distance-matrix checker; no producer import in record mode."""
import hashlib
import json
import sys
from copy import deepcopy
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(test, message):
    if not test:
        raise ValueError(message)


def q(x):
    need(type(x) in (str, int), 'exact rational type')
    return Q(x)


def ldl_psd(a):
    a = [r[:] for r in a]
    for k in range(len(a)):
        if a[k][k] < 0:
            return False
        if a[k][k] == 0:
            if any(a[k][j] != 0 for j in range(k+1, len(a))):
                return False
        else:
            for i in range(k+1, len(a)):
                for j in range(k+1, len(a)):
                    a[i][j] -= a[i][k]*a[k][j]/a[k][k]
    return True


def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(',', ':')).encode()


def check(data, record):
    need(isinstance(record, dict) and type(record.get('n')) is int, 'record atom count type')
    need(isinstance(data, dict) and {'x', 'y'} <= data.keys()
         and set(data) <= {'x', 'y', 'scatter_floor'}, 'input fields')
    need(all(isinstance(data[name], list) and all(isinstance(p, list) for p in data[name]) for name in ('x', 'y')), 'point arrays')
    x, y = [[tuple(q(v) for v in row) for row in data[name]] for name in ('x', 'y')]
    n = len(x)
    need(n > 0 and len(y) == n and all(len(p) == 3 for p in x+y), 'R3 input size')
    need(len(set(x)) == n, 'source labels must be distinct')
    dx, dy = [], []
    for points, distances in ((x, dx), (y, dy)):
        for p in points:
            distances.append([sum((a-b)**2 for a, b in zip(p, r)) for r in points])
    delta = [[dx[i][j]-dy[i][j] for j in range(n)] for i in range(n)]
    need(all(v >= 0 for row in delta for v in row), 'pair expansion')
    row = [sum(r)/n for r in delta]
    grand = sum(row)/n
    gram2 = sum((delta[i][j]-row[i]-row[j]+grand)**2
                for i in range(n) for j in range(n))/4
    # Scatter from ordered differences; no explicit centering or Gram product.
    scatter = [[sum((x[i][a]-x[j][a])*(x[i][b]-x[j][b])
                    for i in range(n) for j in range(n))/(2*n)
                for b in range(3)] for a in range(3)]
    if 'scatter_floor' in data:
        k = q(data['scatter_floor'])
        need(k > 0, 'positive requested floor')
    else:
        a = scatter
        determinant = (a[0][0]*a[1][1]*a[2][2] + 2*a[0][1]*a[0][2]*a[1][2]
                       - a[0][0]*a[1][2]**2-a[1][1]*a[0][2]**2-a[2][2]*a[0][1]**2)
        tr = sum(a[i][i] for i in range(3))
        k = determinant/tr**2 if tr else Q(0)
    need(ldl_psd([[scatter[i][j]-(k if i == j else 0) for j in range(3)] for i in range(3)]), 'scatter bound')
    vals = [delta[i][j] for i, j in combinations(range(n), 2)]
    low, high = min(vals, default=Q(0)), max(vals, default=Q(0))
    slack = k*low-4*gram2
    status = ('ISOMETRIC_ZERO' if gram2 == 0 else 'UNRESOLVED_SOURCE_RANK' if k == 0
              else 'SIGNED_ALL_VARIANCES_ALL_THRESHOLDS' if slack >= 0 else 'UNRESOLVED')
    expected = {'schema': 'balanced-loss-v1', 'input_sha256': hashlib.sha256(canonical(data)).hexdigest(),
                'n': n, 'status': status, 'scatter_floor': str(k),
                'gram_frobenius_squared': str(gram2), 'minimum_pair_loss': str(low),
                'maximum_pair_loss': str(high), 'guard_slack': str(slack),
                'pair_error_upper': str(4*gram2/k) if k else None,
                'law_scope': 'every probability vector on the supplied labels'}
    need(record == expected, 'certificate fields do not match independent reconstruction')
    return expected


def family(t):
    x = [tuple(Q(s, 4) for s in p) for p in product((-1, 1), repeat=3)]
    y = [((1-t)*p[0]+2*t*p[1]*p[2],
          (1-t)*p[1]+2*t*p[0]*p[2],
          (1-t)*p[2]+2*t*p[0]*p[1]) for p in x]
    # A reflection and unrelated translation deliberately invalidate raw alignment.
    y = [(-p[0]+3, p[1]-2, p[2]+5) for p in y]
    return {'x': [[str(a) for a in p] for p in x],
            'y': [[str(a) for a in p] for p in y], 'scatter_floor': '1/2'}


def rank(a):
    a = [r[:] for r in a]
    r = 0
    for j in range(len(a[0])):
        p = next((i for i in range(r, len(a)) if a[i][j]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        d = a[r][j]
        a[r] = [v/d for v in a[r]]
        for i in range(r+1, len(a)):
            c = a[i][j]
            a[i] = [v-c*w for v, w in zip(a[i], a[r])]
        r += 1
    return r


def padd(a, b):
    return [(a[i] if i < len(a) else Q(0))+(b[i] if i < len(b) else Q(0))
            for i in range(max(len(a), len(b)))]


def pmul(a, b):
    c = [Q(0)]*(len(a)+len(b)-1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            c[i+j] += u*v
    return c


def pscale(a, c):
    return [c*v for v in a]


def bernstein_on(a, end):
    d = len(a)-1
    return [sum(a[j]*end**j*Q(comb(i, j), comb(d, j))
                for j in range(i+1)) for i in range(d+1)]


def polynomial_family():
    x = [tuple(Q(s, 4) for s in p) for p in product((-1, 1), repeat=3)]
    y = [[[p[i], 2*p[(i+1)%3]*p[(i+2)%3]-p[i]] for i in range(3)] for p in x]
    need(all(sum(y[i][j][k] for i in range(8)) == 0
             for j in range(3) for k in range(2)), 'family centering')
    gram2 = [Q(0)]*5
    low = [Q(0), Q(1, 2), Q(-3, 8)]
    need(min(bernstein_on(low[1:], Q(1, 128))) > 0, 'positive family loss away from zero')
    for i in range(8):
        for j in range(8):
            gram = [sum(x[i][k]*x[j][k] for k in range(3))]
            for k in range(3):
                gram = padd(gram, pscale(pmul(y[i][k], y[j][k]), -1))
            gram2 = padd(gram2, pmul(gram, gram))
            if i < j:
                loss = [sum((x[i][k]-x[j][k])**2 for k in range(3))]
                for k in range(3):
                    d = padd(y[i][k], pscale(y[j][k], -1))
                    loss = padd(loss, pscale(pmul(d, d), -1))
                residual = padd(loss, pscale(low, -1))
                need(residual[0] == 0 and min(bernstein_on(residual[1:], Q(1, 128))) >= 0,
                     'family pair-loss lower envelope')
    need(gram2 == [Q(0), Q(0), Q(27, 8), Q(-15, 4), Q(75, 64)], 'family Gram polynomial')
    guard = padd(pscale(low, Q(1, 2)), pscale(gram2, -4))
    need(guard[0] == 0, 'zero-loss factor')
    power = pscale(guard[1:], 16)
    need(power == [Q(4), Q(-219), Q(240), Q(-75)], 'guard polynomial')
    bernstein = bernstein_on(power, Q(1, 128))
    need(min(bernstein) > 0, 'uniform family guard')
    return bernstein


def controls():
    # Imported only here: the separately supplied record checker is independent.
    from certificate import certify
    fixtures = []
    for t in (Q(0), Q(1, 32), Q(1, 128), Q(1, 2**40), Q(1, 2**200)):
        a = family(t)
        fixtures.append(a)
    for scale in (Q(1, 7), Q(13)):
        a = family(Q(1, 128))
        for name in ('x', 'y'):
            a[name] = [[str(scale*q(v)) for v in row] for row in a[name]]
        a['scatter_floor'] = str(scale**2/2)
        fixtures.append(a)
    a = family(Q(1, 1024)); a.pop('scatter_floor'); fixtures.append(a)
    # A non-diagonal positive source scatter, and independent endpoint frames.
    a = family(Q(1, 2**20)); a.pop('scatter_floor')
    a['x'] = [[str(q(p[0])+q(p[1])/5), p[1], p[2]] for p in a['x']]
    # Construct a small homothety of this skew source; test producer default k.
    a['y'] = [[str((1-Q(1, 2**20))*q(v)) for v in p] for p in a['x']]
    fixtures.append(a)
    a = family(Q(0)); r = Q(127, 128)
    a['y'] = [[str(r*q(v)) for v in p] for p in a['x']]
    a['scatter_floor'] = str(12*(1-r*r))
    boundary = check(a, certify(a))
    need(boundary['guard_slack'] == '0' and boundary['status'] == 'SIGNED_ALL_VARIANCES_ALL_THRESHOLDS', 'closed guard boundary')
    fixtures.append(a)
    plane = {'x': [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
             'y': [[0, 0, 0], ['99/100', 0, 0], [0, '99/100', 0]]}
    fixtures.extend([plane, {'x': [[1, 2, 3]], 'y': [[4, 5, 6]]}])
    states = []
    for a in fixtures:
        states.append(check(a, certify(a))['status'])
    need(states[:5] == ['ISOMETRIC_ZERO', 'UNRESOLVED'] + ['SIGNED_ALL_VARIANCES_ALL_THRESHOLDS']*3, 'state controls')
    need(states[-2:] == ['UNRESOLVED_SOURCE_RANK', 'ISOMETRIC_ZERO'], 'boundary controls')

    a = family(Q(1, 128)); c = certify(a)
    need(check(a, json.loads((HERE/'CERTIFICATE.json').read_text())) == c, 'stored certificate')
    need(a == json.loads((HERE/'INPUT.json').read_text()), 'stored input')
    damaged = 0
    for key, value in [('gram_frobenius_squared', '0'), ('guard_slack', '0'),
                       ('minimum_pair_loss', '1'), ('scatter_floor', '1'),
                       ('pair_error_upper', '0'), ('n', 9), ('input_sha256', '0'*64),
                       ('law_scope', 'some weights'), ('status', 'UNRESOLVED')]:
        z = dict(c); z[key] = value
        try:
            check(a, z)
        except ValueError:
            damaged += 1
        else:
            raise ValueError('damaged record accepted')
    wrong = []
    for val in (0.5, True):
        z = deepcopy(a); z['x'][0][0] = val; wrong.append(z)
    z = deepcopy(a); z['scatter_floor'] = '3/4'; wrong.append(z)
    z = deepcopy(a); z['y'][0][0] = '100'; wrong.append(z)
    z = deepcopy(a); z['x'][0] = z['x'][1][:]; wrong.append(z)
    z = deepcopy(a); z['y'].pop(); wrong.append(z)
    z = deepcopy(a); z['x'][0].append('0'); wrong.append(z)
    z = deepcopy(a); z['weights'] = ['1/8']*8; wrong.append(z)
    z = deepcopy(a); z['scatter_floor'] = '0'; wrong.append(z)
    for z in wrong:
        for test in (lambda: certify(z), lambda: check(z, c)):
            try:
                test()
            except (ValueError, TypeError):
                damaged += 1
            else:
                raise ValueError('invalid input accepted')

    # Reconstruct the polynomial identities before checking the entire interval.
    bernstein = polynomial_family()
    x = [[q(v) for v in row] for row in a['x']]
    y = [[q(v) for v in row] for row in a['y']]
    need(rank([[Q(1)]+p+r for p, r in zip(x, y)]) == 7, 'paired rank six')
    # Walsh orthogonality proves the rank for all t>0, not just this sample.
    w = [[Q(s) for s in (u, v, z, v*z, u*z, u*v)] for u, v, z in product((-1, 1), repeat=3)]
    need(all(sum(r[i]*r[j] for r in w) == (8 if i == j else 0)
             for i in range(6) for j in range(6)), 'Walsh rank identity')

    # Whole normalized parameter cover, all 4<=n<=19; no numerical tuning.
    rho, kappa, radius2, meanloss = Q(1, 4), Q(1, 2**15), Q(1, 4), Q(1, 2**40)
    budgets = []
    for n in range(4, 20):
        limit = 3*rho*rho*kappa*kappa/(2*radius2*n*n)
        need(meanloss <= limit, 'uniform 19-atom budget')
        budgets.append({'n': n, 'sufficient_mean_loss': str(limit)})
    pins = json.loads((HERE/'INPUTS.json').read_text())
    for entry in pins:
        content = (HERE.parent/entry['path']).read_bytes()
        need(hashlib.sha256(content).hexdigest() == entry['sha256'], 'dependency digest')
    return {'status': 'BALANCED_LOSS_ALL_THRESHOLD_PASS', 'fixture_states': states,
            'damaged_or_malformed_rejections': damaged,
            'family_bernstein_coefficients': [str(v) for v in bernstein],
            'family_paired_rank': 6, 'parameter_budgets': budgets,
            'dependency_files': len(pins),
            'canonical_certificate_sha256': hashlib.sha256(canonical(c)).hexdigest()}


if __name__ == '__main__':
    if len(sys.argv) == 3:
        with open(sys.argv[1]) as f:
            supplied = json.load(f)
        with open(sys.argv[2]) as f:
            evidence = json.load(f)
        result = check(supplied, evidence)
    elif len(sys.argv) == 1:
        result = controls()
        expected = HERE/'EXPECTED.json'
        if expected.exists():
            need(result == json.loads(expected.read_text()), 'expected output differs')
    else:
        raise SystemExit('usage: python3 verify.py [INPUT.json CERTIFICATE.json]')
    print(json.dumps(result, indent=2, sort_keys=True))
