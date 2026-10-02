"""Reject damaged original equations and compact certificate hypotheses."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import json
import inputs
from literal import require
from exact import digest, lift
from radical import check
from schur import solve_pd
from whole import matrices, original


def rejected(name, call, out):
    try:
        call()
    except ValueError as error:
        out.append({'damage': name, 'rejection': str(error)})
    else:
        raise ValueError('Undetected certificate damage: '+name)


def controls():
    fixture = json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
    records = []
    for name, change in (
        ('primitive-polynomial', lambda d: d['polynomial'].__setitem__(2, d['polynomial'][2]+1)),
        ('missing-orbit', lambda d: d['orbits'].pop()),
        ('wrong-original-count', lambda d: d['orbits'][0].__setitem__('count', 4)),
        ('altered-constant-coefficient', lambda d: d['orbits'][0]['value'].__setitem__(0, d['orbits'][0]['value'][0]+1)),
        ('altered-root-coefficient', lambda d: d['orbits'][0]['value'].__setitem__(1, d['orbits'][0]['value'][1]+1)),
        ('zero-vector-is-not-a-dual', lambda d: [row.__setitem__('value', [0, 0]) for row in d['orbits']]),
        ('duplicate-orbit-key', lambda d: d['orbits'][1].__setitem__('key', d['orbits'][0]['key'])),
    ):
        damaged = deepcopy(fixture)
        change(damaged)
        rejected(name, lambda: check(damaged), records)
    wrong = dict(inputs.PINS)
    wrong['small-deletion-boundary/literal.py'] = '0'*64
    rejected('changed-published-input', lambda: inputs.setup(wrong), records)
    X, C, L, M = matrices(F(0), F(1, 2))
    broken = deepcopy(M); broken[0][0] += 1
    rejected('wrong-actual-empty-diagonal', lambda: original(X, L, broken), records)
    rejected('omitted-actual-empty-set', lambda: original(X[1:], L[1:], M[1:]), records)
    i, j = X[1:].index(1), X[1:].index(3)
    broken = deepcopy(C); broken[i][j] += 1; broken[j][i] += 1
    h, ell = X[1:].index(2), X[1:].index(4)
    broken[h][ell] -= 1; broken[ell][h] -= 1
    bad_L = lift(broken)
    bad_M = [[(bad_L[a][b]-28*int(a == b))/F(61) for b in range(89)] for a in range(89)]
    require(all(sum(row) == 89 for row in bad_L) and bad_L[0][0] == 76,
            'damage preserves all whole rows and the actual empty diagonal')
    rejected('row-preserving-intersection-damage', lambda: original(X, bad_L, bad_M), records)
    identity = [[F(int(i == j)) for j in range(82)] for i in range(82)]
    rhs = [[F(0)]*4 for _ in range(82)]
    negative = deepcopy(identity); negative[0][0] = F(-1)
    rejected('negative-physical-pivot', lambda: solve_pd(negative, rhs), records)
    asymmetric = deepcopy(identity); asymmetric[0][1] = F(1)
    rejected('asymmetric-physical-compression', lambda: solve_pd(asymmetric, rhs), records)
    inexact = deepcopy(M); inexact[1][2] = float(inexact[1][2])
    rejected('floating-original-entry', lambda: original(X, L, inexact), records)
    rec = {'agent': 'six-downset-3', 'role': 'researcher', 'damage_count': len(records),
           'damages': records, 'assertions_required': False}
    rec['record_sha256'] = digest(rec)
    return rec


if __name__ == '__main__':
    print(json.dumps(controls(), sort_keys=True, indent=2))
