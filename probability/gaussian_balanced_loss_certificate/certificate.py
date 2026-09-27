#!/usr/bin/env python3
"""Exact sufficient motion certificate. Standard-library Python 3.11+."""
import hashlib
import json
import sys
from fractions import Fraction as F
from itertools import combinations


def rational(x):
    if type(x) not in (int, str):
        raise ValueError('rational inputs must be integers or strings')
    return F(x)


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def det(a):
    if len(a) == 1:
        return a[0][0]
    return sum((-1)**j*a[0][j]*det([r[:j]+r[j+1:] for r in a[1:]])
               for j in range(len(a)))


def psd(a):
    return all(det([[a[i][j] for j in s] for i in s]) >= 0
               for m in (1, 2, 3) for s in combinations(range(3), m))


def encode(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()


def certify(data):
    if not isinstance(data, dict) or not {'x', 'y'} <= data.keys() or not set(data) <= {'x', 'y', 'scatter_floor'}:
        raise ValueError('expected x, y and optional scatter_floor')
    if any(not isinstance(data[name], list) or any(not isinstance(p, list) for p in data[name]) for name in ('x', 'y')):
        raise ValueError('point lists must be JSON arrays')
    x, y = [list(tuple(rational(t) for t in p) for p in data[name]) for name in ('x', 'y')]
    n = len(x)
    if not n or n != len(y) or any(len(p) != 3 for p in x+y):
        raise ValueError('nonempty paired R3 lists required')
    if len(set(x)) != n:
        raise ValueError('merge duplicate source labels first')
    low, high = None, F(0)
    for i, j in combinations(range(n), 2):
        dx, dy = sub(x[i], x[j]), sub(y[i], y[j])
        loss = dot(dx, dx)-dot(dy, dy)
        if loss < 0:
            raise ValueError('an endpoint pair expands')
        low, high = min(low, loss) if low is not None else loss, max(high, loss)
    low = F(0) if low is None else low
    cx = tuple(sum(p[j] for p in x)/n for j in range(3))
    cy = tuple(sum(p[j] for p in y)/n for j in range(3))
    a, b = [[sub(p, c) for p in z] for z, c in ((x, cx), (y, cy))]
    scatter = [[sum(p[i]*p[j] for p in a) for j in range(3)] for i in range(3)]
    gram2 = sum((dot(a[i], a[j])-dot(b[i], b[j]))**2
                for i in range(n) for j in range(n))
    trace = sum(scatter[i][i] for i in range(3))
    if 'scatter_floor' in data:
        k = rational(data['scatter_floor'])
        if k <= 0:
            raise ValueError('scatter_floor must be positive')
    else:
        k = det(scatter)/trace**2 if trace else F(0)
    if not psd([[scatter[i][j]-(k if i == j else 0) for j in range(3)] for i in range(3)]):
        raise ValueError('invalid source scatter floor')
    slack = k*low-4*gram2
    status = ('ISOMETRIC_ZERO' if gram2 == 0 else
              'UNRESOLVED_SOURCE_RANK' if k == 0 else
              'SIGNED_ALL_VARIANCES_ALL_THRESHOLDS' if slack >= 0 else 'UNRESOLVED')
    return {'schema': 'balanced-loss-v1', 'input_sha256': hashlib.sha256(encode(data)).hexdigest(),
            'n': n, 'status': status, 'scatter_floor': str(k),
            'gram_frobenius_squared': str(gram2), 'minimum_pair_loss': str(low),
            'maximum_pair_loss': str(high), 'guard_slack': str(slack),
            'pair_error_upper': str(4*gram2/k) if k else None,
            'law_scope': 'every probability vector on the supplied labels'}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python3 certificate.py INPUT.json')
    with open(sys.argv[1]) as f:
        record = certify(json.load(f))
    print(json.dumps(record, indent=2, sort_keys=True))
