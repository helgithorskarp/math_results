"""Exact graph primitives. No solver is part of the checker trust base."""
from itertools import combinations


def require(condition, message):
    if not condition:
        raise ValueError(message)


def decode(s):
    s = s.strip()
    require(s and 63 <= ord(s[0]) < 126, 'short graph6 header required')
    n = ord(s[0]) - 63
    require(len(s) == 1 + (n * (n - 1) // 2 + 5) // 6,
            'incorrect graph6 length')
    require(all(63 <= ord(x) <= 126 for x in s), 'invalid graph6 byte')
    a = [0] * n
    k = 0
    for v in range(1, n):
        for u in range(v):
            if (ord(s[1 + k // 6]) - 63) >> (5 - k % 6) & 1:
                a[u] |= 1 << v
                a[v] |= 1 << u
            k += 1
    if k % 6:
        require((ord(s[-1]) - 63) & ((1 << (6 - k % 6)) - 1) == 0,
                'nonzero graph6 padding')
    return a


def complement(a):
    u = (1 << len(a)) - 1
    return [u ^ ((1 << v) | a[v]) for v in range(len(a))]


def clique_masks(a, k):
    def rec(candidates, left, chosen):
        if left == 0:
            yield chosen
            return
        while candidates.bit_count() >= left:
            bit = candidates & -candidates
            candidates ^= bit
            v = bit.bit_length() - 1
            yield from rec(candidates & a[v], left - 1, chosen | bit)
    yield from rec((1 << len(a)) - 1, k, 0)


def good(a, s=5, t=5):
    return next(clique_masks(a, s), None) is None and next(
        clique_masks(complement(a), t), None) is None


def maximum_codegree(a):
    b = complement(a)
    return max(((a[u] & a[v]) if a[u] >> v & 1 else (b[u] & b[v]))
               .bit_count() for u, v in combinations(range(len(a)), 2))


def cyclic_core():
    return [sum(1 << ((v + d) % 13) for d in (1, 5, 8, 12))
            for v in range(13)]


SEEDS = {'5': [0, 1, 2, 5, 6], '6': [0, 1, 2, 6, 9]}


def frame(seed, kind):
    require(str(seed) in SEEDS and kind in ('A', 'T'), 'bad frame')
    a = [0] * 16
    def edge(u, v):
        a[u] |= 1 << v
        a[v] |= 1 << u
    edge(0, 1)
    for u in (0, 1):
        for v in range(2, 15):
            edge(u, v)
    h = cyclic_core()
    for u, v in combinations(range(13), 2):
        if h[u] >> v & 1:
            edge(u + 2, v + 2)
    for v in SEEDS[str(seed)]:
        edge(v + 2, 15)
    if kind == 'A':
        edge(0, 15)
    return a
