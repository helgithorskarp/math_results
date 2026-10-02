"""Parameterized physical forms for the enlarged core-edge face.

The two defining executable inputs are checked in full before either import.
These literal forms retain all physical orbit weights and actual members.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from math import comb
from itertools import combinations
import importlib.util

SOURCE = Path(__file__).resolve().parent.parent
import source_pins
source_pins.check()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, SOURCE/path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


literal = load('core_frontier_literal', 'small-deletion-boundary/literal.py')
exact = load('core_frontier_exact', 'triangle-majority/exact.py')
table, typ, require = literal.table, literal.typ, literal.require
schur_psd, polynomial_psd = exact.schur_psd, exact.polynomial_psd
RB = {(1, 2): 1, (2, 5): -1}
RC = {(1, 4): 1, (3, 4): -1}
BC = {(2, 4): 1}
NAMES = ('C0', 'Delta', 'Rb', 'Rc', 'B', 'U0')


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    return value


def action(matrix, vector):
    return [sum(x*y for x, y in zip(row, vector)) for row in matrix]


def pair(matrix, left, right=None):
    return sum(x*y for x, y in zip(left, action(matrix, left if right is None else right)))


def choose(n, r):
    return comb(n, r) if 0 <= r <= n else 0


def parameters(q, k):
    require(type(q) is int and type(k) is int and q >= 4 and 0 <= k <= q,
            'integer q>=4,0<=k<=q required')
    return (q*q+13*q+16)//2-k, 3*q+4


def forms(q, k):
    N, s = parameters(q, k)
    keys = sorted((c, z, w) for c in range(8) for z in range(3) for w in range(3)
                  if (1 <= c.bit_count()+z+w <= 2 or
                      c.bit_count()+z+w == 3 and c.bit_count() >= 2)
                  and (c, z, w) != (6, 1, 0)
                  and choose(k, z)*choose(q-k, w) > 0)
    sizes = [choose(k, z)*choose(q-k, w) for c, z, w in keys]
    require(min(sizes) > 0 and sum(sizes) == N-1, 'all surviving physical orbits')
    m, tab = len(keys), table(q)
    matrices = {name: [[F(0)]*m for _ in range(m)] for name in NAMES}
    for i, (c, z, w) in enumerate(keys):
        for j, (cc, zz, ww) in enumerate(keys):
            count = 0 if c & cc else choose(k-z, zz)*choose(q-k-w, ww)
            reverse = 0 if c & cc else choose(k-zz, z)*choose(q-k-ww, w)
            require(sizes[i]*count == sizes[j]*reverse, 'physical reciprocity')
            a, b = tab[tuple(sorted(((c.bit_count(), z+w), (cc.bit_count(), zz+ww))))] if count else (F(0), F(0))
            base = F(s*sizes[i]*int(i == j)-sizes[i]*sizes[j])+sizes[i]*count*a
            matrices['C0'][i][j] = base
            matrices['Delta'][i][j] = sizes[i]*count*b
            matrices['U0'][i][j] = F(N*sizes[i]*int(i == j)-sizes[i]*sizes[j])-base
            for name, edges in (('Rb', RB), ('Rc', RC), ('B', BC)):
                matrices[name][i][j] = F(edges.get(tuple(sorted((c, cc))), 0)) if z+w+zz+ww == 0 else F(0)
    require(all(A[i][j] == A[j][i] for A in matrices.values() for i in range(m) for j in range(m)),
            'every coefficient form symmetric')
    return {'q': q, 'k': k, 'N': N, 's': s, 'keys': keys, 'sizes': sizes, **matrices}


def domain(q, k):
    N, _ = parameters(q, k)
    X = [0]+sorted(sum(1 << i for i in p) for size in (1, 2, 3)
                  for p in combinations(range(q+3), size)
                  if literal.member(q, k, sum(1 << i for i in p)))
    require(len(X) == N and len(set(X)) == N, 'entire original member census')
    return X


def orbit(A, k):
    return A & 7, ((A >> 3) & ((1 << k)-1)).bit_count(), (A >> (3+k)).bit_count()


def entry(q, s, tab, A, B):
    if A == B:
        base, der = F(s-1), F(0)
    elif A & B:
        base, der = F(-1), F(0)
    else:
        base, der = tab[tuple(sorted((typ(A), typ(B))))]
        base -= 1
    edge = tuple(sorted((A, B)))
    return (base, der, F(RB.get(edge, 0)), F(RC.get(edge, 0)),
            F(BC.get(edge, 0)), F(0)-base)


def original_forms(q, k):
    """Independent actual-member sums, no counted orbit formula."""
    D = forms(q, k)
    X, tab = domain(q, k), table(q)
    ix = {key: i for i, key in enumerate(D['keys'])}
    m = len(ix)
    counted = {name: [[F(0)]*m for _ in range(m)] for name in NAMES}
    census = [0]*m
    for A in X[1:]:
        census[ix[orbit(A, k)]] += 1
    require(census == D['sizes'], 'independent all-orbit original census')
    for A in X[1:]:
        i = ix[orbit(A, k)]
        for B in X[1:]:
            j = ix[orbit(B, k)]
            values = list(entry(q, D['s'], tab, A, B))
            values[-1] += D['N']*int(A == B)-1
            for name, value in zip(NAMES, values):
                counted[name][i][j] += value
    require(all(counted[name] == D[name] for name in NAMES), 'every physical coefficient equals entire original pair sum')
    return D, (len(X)-1)**2


def evaluate(D, kappa, tb, sigma, tc=None):
    tc = tb if tc is None else tc
    m = len(D['keys'])
    C = [[D['C0'][i][j]+kappa*D['Delta'][i][j]+tb*D['Rb'][i][j]+tc*D['Rc'][i][j]+sigma*D['B'][i][j]
          for j in range(m)] for i in range(m)]
    U = [[D['U0'][i][j]-kappa*D['Delta'][i][j]-tb*D['Rb'][i][j]-tc*D['Rc'][i][j]-sigma*D['B'][i][j]
          for j in range(m)] for i in range(m)]
    return C, U


def vectors(D):
    keys, q = D['keys'], D['q']
    return {
        'one': [F(1)]*len(keys),
        'star': [F(bool(c & 1)) for c, z, w in keys],
        'z': [F(1-int(bool(c & 2))-int(bool(c & 4))+int(c.bit_count() >= 2)) for c, z, w in keys],
        'h': [F((c, z, w) in ((2, 0, 0), (4, 0, 0))) for c, z, w in keys],
        'v': [F(c == 0 and z+w == 1) for c, z, w in keys],
        'p': [F((c, z, w) == (1, 0, 0))-F(int(c == 1 and z+w == 1), q) for c, z, w in keys],
        'y': [F(c == 1 and z+w == 1) for c, z, w in keys],
        'trade_iso': [F(bool(c & 6) and (c, z, w) not in ((3, 0, 0), (5, 0, 0))) for c, z, w in keys],
    }
