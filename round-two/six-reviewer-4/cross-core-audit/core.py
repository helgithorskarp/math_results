"""Independent literal known-core/page-bound audit. Integers and sets only."""
from itertools import combinations

X = tuple(range(3, 9))
SX, SY, T = (9, 10), (11, 12), (13, 14, 15)
CYCLE = ((0, 4), (4, 3), (3, 1), (1, 2), (2, 5), (5, 0))
RANK = (0, 6, 0, 3, 3, 4, 4, 4, 4, 4, 4, 2, 2, 3, 2, 3)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def frame(r=0, sy_swap=0):
    require(r in (0, 1) and sy_swap in (0, 1), 'frame label')
    adj = [set() for _ in range(16)]
    def edge(i, j):
        require(i != j, 'loop')
        adj[i].add(j)
        adj[j].add(i)
    for i in (1, 2) + X + SX:
        edge(0, i)
    for i in (2,) + SY:
        edge(1, i)
    for i in SX + SY + T:
        edge(2, i)
    for i, j in CYCLE:
        edge(X[i], X[j])
    for s, own in zip(SX, ((3, 5), (2, 4))):
        for i in own:
            edge(s, X[i])
    for s, mask in zip(SY, ((13, 50) if not sy_swap else (50, 13))):
        for i in range(6):
            if mask >> i & 1:
                edge(s, X[i])
    for s, mask in zip(SX, ((6, 5) if not r else (5, 6))):
        for i in range(3):
            if mask >> i & 1:
                edge(s, T[i])
    for s, mask in zip(SY, (6, 3)):
        for i in range(3):
            if mask >> i & 1:
                edge(s, T[i])
    for t, mask in zip(T, ((43, 23, 3) if not r else (23, 43, 3))):
        for i in range(6):
            if mask >> i & 1:
                edge(t, X[i])
    return adj


def degrees(adj):
    return tuple(len(row) + rank for row, rank in zip(adj, RANK))


def fixed_pairs(adj):
    deg = degrees(adj)
    pairs = []
    for i, j in combinations(range(16), 2):
        pages = sorted(adj[i] & adj[j])
        cap = 3 if j in adj[i] else deg[i] + deg[j] - 14
        upper = cap - len(pages)
        lower = max(0, RANK[i] + RANK[j] - 6)
        require(lower <= upper, 'inconsistent fixed-pair lower/upper')
        pairs.append({'pair': [i, j], 'red': j in adj[i],
                      'pages': pages, 'cap': cap, 'upper': upper, 'lower': lower,
                      'union': upper == RANK[i] + RANK[j] - 6})
    return pairs


def column(adj, pairs, word, blue_minimum=True):
    # Every one of the 13 unknown incidences is covered exactly once.
    near = {1} | {i + 3 for i in range(13) if word >> i & 1}
    sy_t = sum(i in near for i in SY + T)
    h = 4 - sy_t
    if not 0 <= h <= 4:
        return None
    dq = len(near) + h
    deg = degrees(adj)
    for pair in pairs:
        i, j = pair['pair']
        if int(i in near and j in near) > pair['upper']:
            return None
        if pair['union'] and not (i in near or j in near):
            return None
    for i in range(16):
        red = i in near
        minimum = max(0, RANK[i] + h - (6 if red else 5))
        if not red and not blue_minimum:
            minimum = 0
        pages = len(adj[i] & near) + minimum
        cap = 3 if red else deg[i] + dq - 14
        if pages > cap:
            return None
    return {'word': word, 'missing': [i for i, x in enumerate(X) if x not in near],
            'p': [int(s in near) for s in SX],
            's': [int(s in near) for s in SY],
            't': [int(t in near) for t in T], 'h': h, 'degree': dq}


def all_columns(adj, blue_minimum=True):
    pairs = fixed_pairs(adj)
    return [c for word in range(8192)
            if (c := column(adj, pairs, word, blue_minimum)) is not None]


ROLE_FLAGS = {
    'A0': ([1, 0], [1, 0, 0]), 'A1U': ([1, 0], [0, 0, 1]),
    'A1V': ([1, 0], [1, 0, 1]), 'B': ([0, 1], [0, 0, 1]),
    'C': ([0, 0], [1, 1, 0]), 'D': ([0, 0], [0, 1, 0])}


def role_columns(columns):
    return {name: [c for c in columns if (c['s'], c['t']) == flags]
            for name, flags in ROLE_FLAGS.items()}


def permutation(r, sy_swap):
    p = list(range(16))
    if r:
        for i, j in ((5, 6), (7, 8), (9, 10)):
            p[i], p[j] = p[j], p[i]
    if sy_swap:
        f = dict((i, j) for i, j in ((3, 4), (4, 3), (5, 7),
                                    (7, 5), (6, 8), (8, 6)))
        p = [f.get(i, i) for i in p]
    return p


def transported_word(word, p):
    near = {1} | {i + 3 for i in range(13) if word >> i & 1}
    return sum(1 << (p[i] - 3) for i in near if p[i] >= 3)


def endpoint_inventory():
    # All actual labelled sets, no assumption that the host has an automorphism.
    ground = frozenset(range(6))
    records = []
    for a in combinations(ground, 2):
        sa = frozenset(a)
        for b in combinations(ground - sa, 2):
            sb = frozenset(b)
            t1 = ground - sa - sb
            for extra in sa:
                t2 = sb | {extra}
                for c in combinations(ground - sb, 3):
                    t0 = frozenset(c)
                    if t0 | t1 | t2 != ground:
                        continue
                    flags = [[int(q in s) for s in (sa, sb, t0, t1, t2)]
                             for q in range(6)]
                    kinds = sorted(tuple(f) for f in flags)
                    kind = 'U' if len(t0 & sa) == 1 else 'V'
                    records.append({'case': kind, 'flags': flags})
    return records
