#!/usr/bin/env python3
"""Independent witness discovery: rational biquadratic arithmetic and SAT.

Edges are obtained from labelled differences before quotienting. The verifier
instead scans all distinct physical point pairs using an integer norm identity.
"""
from fractions import Fraction as F
from itertools import product, combinations
from math import lcm
from pathlib import Path
import argparse
import hashlib
import json
import time

W = [(0, 0), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
LABELS = list(product(range(7), repeat=3))
CASES = [(1, 3, 3), (1, 4, 4), (3, 3, 4), (3, 4, 4)]


class Field:
    """Q[s,t], s^2=-3, t^2=-delta; embedding s=i sqrt3,t=i sqrt(delta)."""
    def __init__(self, delta):
        self.delta = delta

    @staticmethod
    def add(*xs):
        return tuple(sum(x[i] for x in xs) for i in range(4))

    @staticmethod
    def scale(x, a):
        return tuple(c*a for c in x)

    @staticmethod
    def conj(x):
        return x[0], -x[1], -x[2], x[3]

    def mul(self, x, y):
        z = [F(0)]*4
        for i, a in enumerate(x):
            for j, b in enumerate(y):
                z[i ^ j] += a*b*(-3 if i & j & 1 else 1)*(-self.delta if i & j & 2 else 1)
        return tuple(z)

    @staticmethod
    def lattice(a, b):
        return F(2*a+b, 2), F(b, 2), F(0), F(0)


def construct(case):
    m, n, p = case
    k = p-m-n
    delta = 4*m*n-k*k
    q = Field(delta)
    reps = {1: (1, 0), 3: (1, 1), 4: (2, 0)}
    d, e, f = [q.lattice(*reps[j]) for j in case]
    u = q.scale(q.mul((F(k), F(0), F(1), F(0)), q.mul(d, q.conj(e))), F(1, 2*m*n))
    v = q.scale(q.mul(q.add(d, q.mul(u, e)), q.conj(f)), F(-1, p))
    one = (F(1), F(0), F(0), F(0))
    if q.mul(u, q.conj(u)) != one or q.mul(v, q.conj(v)) != one:
        raise ValueError('nonunit parameter')
    ws = [q.lattice(*z) for z in W]
    zs = [q.add(ws[a], q.mul(u, ws[b]), q.mul(v, ws[c])) for a, b, c in LABELS]
    denominator = lcm(*(x.denominator for z in zs for x in z))
    points = sorted({tuple(int(x*denominator) for x in z) for z in zs})
    index = {p: i for i, p in enumerate(points)}
    ids = [index[tuple(int(x*denominator) for x in z)] for z in zs]
    # The predicate is full field multiplication, cached by exact difference.
    cache = {}
    edges = set()
    for a, b in combinations(range(343), 2):
        d = q.add(zs[a], q.scale(zs[b], -1))
        if d not in cache:
            cache[d] = q.mul(d, q.conj(d)) == one
        if cache[d]:
            if ids[a] == ids[b]:
                raise ValueError('collapsed unit edge')
            edges.add(tuple(sorted((ids[a], ids[b]))))
    return points, sorted(edges), ids


def formula_word(points, edges, ids):
    c = [(a-b) % 3 for a, b in W]
    for s, t in product((1, -1), repeat=2):
        word = [None]*len(points)
        good = True
        for i, (a, b, d) in enumerate(LABELS):
            colour = (c[a]+s*c[b]+t*c[d]) % 3
            if word[ids[i]] not in (None, colour):
                good = False
                break
            word[ids[i]] = colour
        if good and all(word[a] != word[b] for a, b in edges):
            return word
    return None


def sat_word(n, edges):
    from pysat.solvers import Glucose42
    var = lambda v, c: 4*v+c+1
    clauses = []
    for v in range(n):
        clauses.append([var(v, c) for c in range(4)])
        clauses.extend([-var(v, c), -var(v, d)] for c, d in combinations(range(4), 2))
    for a, b in edges:
        clauses.extend([-var(a, c), -var(b, c)] for c in range(4))
    clauses.append([1])  # Global palette permutation may make vertex zero colour zero.
    with Glucose42(bootstrap_with=clauses) as solver:
        if not solver.solve():
            raise RuntimeError('No SAT witness: preserve an UNSAT proof before making any claim.')
        model = {x for x in solver.get_model() if x > 0}
    word = [next(c for c in range(4) if var(v, c) in model) for v in range(n)]
    if not all(word[a] != word[b] for a, b in edges):
        raise ValueError('invalid decoded witness')
    return word


def main(out):
    start = time.monotonic()
    out.mkdir(parents=True, exist_ok=False)
    rows = []
    calls = 0
    for case in CASES:
        points, edges, ids = construct(case)
        word = formula_word(points, edges, ids)
        if word is None:
            calls += 1
            word = sat_word(len(points), edges)
        rows.append({'norms': list(case), 'colours': ''.join(map(str, word))})
    data = (json.dumps({'version': 1, 'cases': rows}, separators=(',', ':'))+'\n').encode()
    (out/'certificate.json').write_bytes(data)
    print(json.dumps({'certificate_bytes': len(data), 'certificate_sha256': hashlib.sha256(data).hexdigest(),
                      'SAT_calls': calls, 'seconds': time.monotonic()-start}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    main(parser.parse_args().out)
