"""Reviewer-owned exact linear algebra helpers, reused from source e759ea9f.
No author checker or factor is an input.
"""
from fractions import Fraction
from itertools import combinations
from math import lcm,isqrt

def need(ok, message):
    if not ok:
        raise ValueError(message)

def rank_mod(rows, p=1009):
    need(p >= 2 and all(p % d for d in range(2, isqrt(p) + 1)), 'modular rank prime')
    a = [[v % p for v in row] for row in rows]
    rank = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][col], -1, p)
        a[rank] = [v * inv % p for v in a[rank]]
        for i in range(rank + 1, len(a)):
            if a[i][col]:
                factor = a[i][col]
                a[i] = [(v - factor * w) % p for v, w in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank

def pair_kernel(n):
    pairs = list(combinations(range(n), 2))
    a = [[Fraction(int(i in pair)) for pair in pairs] for i in range(n)]
    pivots = []
    row = 0
    for col in range(len(pairs)):
        pivot = next((i for i in range(row, n) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        scale = a[row][col]
        a[row] = [v / scale for v in a[row]]
        for i in range(n):
            if i != row and a[i][col]:
                scale = a[i][col]
                a[i] = [v - scale * w for v, w in zip(a[i], a[row])]
        pivots.append(col)
        row += 1
        if row == n:
            break
    need(row == (1 if n == 2 else n), 'unsigned pair incidence rank, including K2 boundary')
    answer = []
    for col in range(len(pairs)):
        if col in pivots:
            continue
        v = [Fraction(0)] * len(pairs)
        v[col] = Fraction(1)
        for i, pivot in enumerate(pivots):
            v[pivot] = -a[i][col]
        scale = lcm(*(x.denominator for x in v))
        ints = [int(x * scale) for x in v]
        need(all(sum(ints[j] for j, pair in enumerate(pairs) if i in pair) == 0
                 for i in range(n)), 'kernel original incidence')
        answer.append(dict(zip(pairs, ints)))
    need(len(answer) == max(0, n * (n - 3) // 2), 'kernel dimension')
    return answer
