"""Exact scalar polynomial helpers reused from author9111, source756a258f441731aff17d6d39bb493b12edb967f2. No external theorem-code import."""
from fractions import Fraction as Q
from math import comb
import hashlib
import json

def digest(record):
    return hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trim(p):
    p = list(map(Q, p))
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(*ps):
    out = [Q(0)] * max(map(len, ps))
    for p in ps:
        for k, c in enumerate(p):
            out[k] += c
    return trim(out)


def scale(p, c):
    return trim([c * x for x in p])


def mul(*ps):
    out = [Q(1)]
    for p in ps:
        nxt = [Q(0)] * (len(out) + len(p) - 1)
        for i, a in enumerate(out):
            for j, b in enumerate(p):
                nxt[i + j] += a * b
        out = trim(nxt)
    return out


def power(p, n):
    return mul(*([p] * n))


def value(p, x):
    out = Q(0)
    for c in reversed(p):
        out = out * x + c
    return out


def integral(k, n):
    return [Q((-1)**j * comb(n, j), k + j + 1) for j in range(n + 1)]


def to_a(p):
    """(1+a)^degree p(a/(1+a)), with its exact degree retained."""
    n = len(p) - 1
    return add(*(scale(mul(power([0, 1], k), power([1, 1], n-k)), c)
                 for k, c in enumerate(p)))


def compose_interval(p, lo, hi):
    n = len(p) - 1
    return trim([sum(p[j] * comb(j, k) * lo**(j-k) * (hi-lo)**k
                     for j in range(k, n+1)) for k in range(n+1)])


def bernstein(p, lo, hi):
    n = len(p) - 1
    pw = compose_interval(p, lo, hi)
    b = [sum(pw[k] * Q(comb(i, k), comb(n, k))
             for k in range(min(i+1, len(pw)))) for i in range(n+1)]
    reverse = [Q(0)] * (n+1)
    for i, c in enumerate(b):
        for j in range(n-i+1):
            reverse[i+j] += c * comb(n, i) * comb(n-i, j) * (-1)**j
    require(trim(reverse) == pw, 'complete reverse Bernstein identity')
    return b
