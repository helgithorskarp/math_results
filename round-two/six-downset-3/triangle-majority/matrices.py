"""Build actual domains/matrices, decode boundaries, and check H literally."""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path
from model import TYPES, formula
from exact import require, lift, schur_psd, polynomial_psd, integral, digest


def parameter(q):
    require(type(q) is int and q >= 2, 'q must be a literal integer at least 2')


def orbit_keys(q):
    parameter(q)
    return [tuple(pair) for pair in combinations_with_replacement(TYPES, 2)
            if sum(t[0] for t in pair) <= 3 and sum(t[1] for t in pair) <= q]


def decode(record):
    q = record['q']
    parameter(q)
    require(q in [2, 3], 'boundary table scope differs')
    require(record.keys() == {'q', 'keys', 'values'}, 'boundary fields differ')
    keys = [tuple(tuple(t) for t in key) for key in record['keys']]
    require(keys == orbit_keys(q), 'boundary orbit keys are incomplete or duplicated')
    require(len(record['values']) == len(keys), 'boundary key/value coverage differs')
    require(all(type(v) is str for v in record['values']), 'boundary fractions require exact strings')
    return dict(zip(keys, map(F, record['values'])))


def weights(q):
    parameter(q)
    if q < 4:
        records = json.loads(Path(__file__).with_name('BOUNDARIES.json').read_text())
        require(len(records) == 2 and [r['q'] for r in records] == [2, 3], 'boundary coverage differs')
        return decode(records[q-2])
    result = formula(F(q))
    require(set(result) == set(orbit_keys(q)), 'generic disjoint orbit coverage differs')
    return result


def build(q, values=None):
    parameter(q)
    members = [0]+sorted(sum(1 << i for i in t) for size in [1, 2, 3]
                         for t in combinations(range(q+3), size)
                         if size < 3 or sum(i < 3 for i in t) >= 2)
    typ = lambda mask: ((mask & 7).bit_count(), (mask >> 3).bit_count())
    values = weights(q) if values is None else values
    require(set(values) == set(orbit_keys(q)), 'literal disjoint orbit coverage differs')
    require(all(isinstance(v, (int, F)) for v in values.values()), 'inexact disjoint weight')
    values = {key: F(value) for key, value in values.items()}
    n, s = len(members), 3*q+4
    c = [[F(s-1) if a == b else F(-1) if a & b else values[tuple(sorted((typ(a), typ(b))))]-1
          for b in members[1:]] for a in members[1:]]
    families = [{a for a in members if a >> i & 1} for i in range(3)]
    families.append({a for a in members if a.bit_count() == 3 or (a.bit_count() == 2 and a & 7 == a)})
    return members, s, families, c


def affine(members, s, families, c):
    n = len(members)
    require(len(c) == n-1 and all(len(row) == n-1 for row in c), 'literal core dimensions differ')
    require(all(len(f) == s and all(a & b for a in f for b in f) for f in families),
            'literal known maximum families differ')
    require(all(sum(c[i][j] for j, b in enumerate(members[1:]) if b in f) == 0
                for i in range(n-1) for f in families), 'literal four-family kernel differs')


def audit(q):
    members, s, families, c = build(q)
    n, included = len(members), set(members)
    require(n == (q*q+13*q+16)//2, 'literal N differs')
    require(all(a ^ (1 << i) in included for a in members for i in range(q+3) if a >> i & 1),
            'literal downward closure differs')
    require([sum(a >> i & 1 for a in members) for i in range(q+3)] == [s]*3+[q+6]*q,
            'literal actual stars differ')
    affine(members, s, families, c)
    u = [[F(n*int(i == j)-1)-c[i][j] for j in range(n-1)] for i in range(n-1)]
    require(schur_psd(c) == n-5 and schur_psd(u) == n-1, 'literal core/cap Schur ranks differ')
    cp, up = polynomial_psd(c), polynomial_psd(u)
    require(cp[0] == n-5 and up[0] == n-1, 'literal characteristic positivity/ranks differ')
    l = lift(c)
    upper = [[F(n*int(i == j))-l[i][j] for j in range(n)] for i in range(n)]
    require(schur_psd(l) == n-4 and schur_psd(upper) == n-1, 'literal full Schur ranks differ')
    upper_lift = lift(u)
    require(all(upper_lift[i][j]-1 == upper[i][j] for i in range(n) for j in range(n)),
            'literal full upper congruence identity differs')
    m = [[F(l[i][j]-s*int(i == j))/(n-s) for j in range(n)] for i in range(n)]
    require(all(sum(row) == 1 for row in m), 'literal full row sums differ')
    require(all(m[i][j] == m[j][i] for i in range(n) for j in range(n)), 'literal full symmetry differs')
    require(all(not m[i][j] for i, a in enumerate(members) for j, b in enumerate(members) if a & b),
            'literal full support differs')
    require(all(sum(l[i][j]*(n*int(members[j] in f)-s) for j in range(n)) == 0
                for i in range(n) for f in families), 'literal centered full kernel differs')
    integers, denominator = integral(m)
    return {'q': q, 'N': n, 's': s, 'rank_L': n-4, 'rank_upper': n-1,
            'M_denominator': denominator, 'M_numerators_sha256': digest(integers),
            'C_polynomial_sha256': cp[1], 'U_polynomial_sha256': up[1]}
