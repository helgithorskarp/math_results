"""Four core-independent, complete physical43 q8 bases. No target solver."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from math import comb
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
EDGES = tuple(combinations(range(43), 2))
INTERNAL = {e for b in range(8) for e in combinations(range(4*b, 4*b+4), 2)}
VARIABLES = {e: k+2 for k, e in enumerate(e for e in EDGES if e not in INTERNAL)}
CORE_FIRST, CORE_STOP = 802, 857


def checked_r(r):
    if type(r) is not int or r not in range(5, 9):
        raise ValueError('Only the complete q8 classes r=5..8 are in scope')
    return r


def comparisons(r):
    checked_r(r)
    return [(i, i+1) for i in range(1, 7) if i+1 != r]


def dimensions(r):
    checked_r(r)
    counts = []
    for color in (1, 0):
        p = [comb(11, k) for k in range(6)]
        for b in range(8):
            q = [comb(4, k) for k in range(5)] if int(b < r) == color else [1, 4]
            p = [sum(p[i-j]*q[j] for j in range(min(i+1, len(q)))) for i in range(6)]
        counts.append(p[5])
    closure = sum(4**j * comb(8-r, j) * comb(11, 4-j) for j in range(5) if j <= 8-r)
    groups = dict(constant=1, root=2520, red5=counts[0], blue5=counts[1],
                  red4=closure, order=91*len(comparisons(r)))
    return dict(r=r, variables=856+15*len(comparisons(r)), physical_variables=855,
                cross_variables=800, core_variables=55, clauses=sum(groups.values()), groups=groups)


def lex(left, right, first):
    prefix = 1
    for i, (x, y) in enumerate(zip(left, right)):
        yield (-prefix, x, -y)
        if i < 15:
            z = first+i
            yield (-z, prefix)
            yield (-z, -x, y)
            yield (-z, x, -y)
            yield (z, -prefix, x, y)
            yield (z, -prefix, -x, -y)
            prefix = z


def clauses(r):
    checked_r(r)
    fixed = {e: int(e[0]//4 < r) for e in INTERNAL}
    yield 'constant', (1,)
    for b in range(1, 8):
        for col in range(3):
            for lo in range(16):
                for hi in range(lo+1, 16):
                    yield 'root', tuple((-1 if value >> row & 1 else 1)*VARIABLES[row, 4*b+c]
                                        for c, value in ((col, lo), (col+1, hi)) for row in range(4))
    for vertices in combinations(range(43), 5):
        pairs = tuple(combinations(vertices, 2))
        colors = {fixed[e] for e in pairs if e in fixed}
        free = tuple(VARIABLES[e] for e in pairs if e not in fixed)
        for color in (1, 0):
            if not colors or colors == {color}:
                yield 'red5' if color else 'blue5', tuple(-v if color else v for v in free)
    for vertices in combinations(range(4*r, 43), 4):
        pairs = tuple(combinations(vertices, 2))
        if not any(e in fixed for e in pairs):
            yield 'red4', tuple(-VARIABLES[e] for e in pairs)
    first = 857
    for a, b in comparisons(r):
        words = [[VARIABLES[u, 4*k+v] for u in reversed(range(4)) for v in reversed(range(4))]
                 for k in (a, b)]
        for c in lex(*words, first):
            yield 'order', c
        first += 15


def write(r, path):
    start = time.monotonic()
    meta = dimensions(r)
    counts = Counter()
    digest = hashlib.sha256()
    with Path(path).open('xb') as f:
        def emit(raw):
            f.write(raw)
            digest.update(raw)
        emit(f"p cnf {meta['variables']} {meta['clauses']}\n".encode())
        for group, clause in clauses(r):
            counts[group] += 1
            emit((' '.join(map(str, clause))+' 0\n').encode())
    if dict(counts) != meta['groups']:
        raise ValueError('Complete base clause counts disagree')
    return dict(meta, bytes=Path(path).stat().st_size, sha256=digest.hexdigest(),
                generation_seconds=time.monotonic()-start)


def read_cnf(path):
    with Path(path).open() as f:
        header = f.readline().split()
        if len(header) != 4 or header[:2] != ['p', 'cnf']:
            raise ValueError('Strict DIMACS header')
        nv, nc = map(int, header[2:])
        count = 0
        for line in f:
            a = [int(x) for x in line.split()]
            if not a or a[-1] != 0 or any(x == 0 or abs(x) > nv for x in a[:-1]):
                raise ValueError('Strict DIMACS clause')
            count += 1
            yield a[:-1]
        if count != nc:
            raise ValueError('Truncated or oversized base')


def project(clause, word):
    out = []
    for lit in clause:
        v = abs(lit)
        if 802 <= v < 857:
            if bool(word >> (v-802) & 1) == (lit > 0):
                return None
        else:
            out.append((1 if lit > 0 else -1)*(v-55 if v >= 857 else v))
    return tuple(out)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('r', type=int)
    p.add_argument('output')
    args = p.parse_args()
    print(json.dumps(write(args.r, args.output), indent=2))
