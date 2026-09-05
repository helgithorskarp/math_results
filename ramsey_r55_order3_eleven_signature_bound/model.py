#!/usr/bin/env python3
"""Three-triangle signature arithmetic, sharp fixtures and propagated clauses."""
from itertools import combinations
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
CORES = {8: '100100100', 11: '100110110', 13: '110110101'}
SIGNATURES = [0, 1, 1, 2, 2, 3, 4, 4, 5, 6]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def compositions(n, k):
    if k == 1:
        yield (n,)
        return
    for first in range(n+1):
        for rest in compositions(n-first, k-1):
            yield (first,)+rest


def arithmetic():
    base, stronger, all_count = [], [], 0
    for counts in compositions(10, 8):
        all_count += 1
        incidence = [sum(counts[s] for s in range(8) if s >> i & 1) for i in range(3)]
        if max(incidence) > 4 or max(counts[1], counts[2], counts[4]) > 2:
            continue
        base.append(counts)
        if all(counts[1 << i]+counts[(1 << i) | (1 << j)] <= 3
               for i in range(3) for j in range(3) if i != j):
            stronger.append(counts)
    histogram = {n: sum(10-c[0] == n for c in base) for n in range(11)}
    maximizers = [c for c in base if c[0] == 1]
    require(all_count == 19448 and len(base) == 928 and len(stronger) == 778, 'arithmetic census')
    require(histogram[10] == 0 and maximizers == [(1, 2, 2, 1, 2, 1, 1, 0)], 'sharp bound')
    return dict(compositions=all_count, basic_profiles=len(base), stronger_profiles=len(stronger),
                nonempty_histogram=histogram, maximum_nonempty=9, maximizing_profiles=maximizers)


def fixture(index):
    code = CORES[index]
    pairs = [(0, 1), (0, 2), (1, 2)]
    edges = []
    for a, b in combinations(range(19), 2):
        if b < 9:
            i, s = divmod(a, 3)
            j, t = divmod(b, 3)
            red = i == j or code[3*pairs.index((i, j))+(t-s) % 3] == '1'
        elif a < 9:
            red = bool(SIGNATURES[b-9] >> (a//3) & 1)
        else:
            red = not (SIGNATURES[a-9] & SIGNATURES[b-9])
        if red:
            edges.append((a, b))
    return '19 '+str(len(edges))+'\n'+''.join(f'{a} {b}\n' for a, b in edges)


def link(cycle, fixed):
    return 211+11*(fixed-33)+cycle


def tail():
    clauses = {(-link(i, 33),) for i in range(3)}
    for fixed in combinations(range(33, 43), 3):
        for singleton in range(3):
            clauses.add(tuple(sorted(-link(i, v) if i == singleton else link(i, v)
                                     for v in fixed for i in range(3))))
    for fixed in combinations(range(33, 43), 4):
        for red in range(3):
            for blue in range(3):
                if red != blue:
                    clauses.add(tuple(sorted(lit for v in fixed for lit in (-link(red, v), link(blue, v)))))
    require(len(clauses) == 1623, 'tail clause count')
    return sorted(clauses, key=lambda c: (len(c), c))


def core_units(index):
    return [(v if b == '1' else -v,) for v, b in zip((1, 2, 3, 4, 5, 6, 31, 32, 33), CORES[index])]


if __name__ == '__main__':
    print(json.dumps(arithmetic(), sort_keys=True))
