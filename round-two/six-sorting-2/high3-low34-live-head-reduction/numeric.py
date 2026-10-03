"""Credited exact numeric primitives, extracted verbatim from public9836.
No old Context, prefix, negative data or private input is imported.
"""
import hashlib
import json
from itertools import combinations


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def bool_word(x, word):
    for a, b in word:
        if x >> a & 1 and not x >> b & 1:
            x ^= (1 << a) | (1 << b)
    return x


def fresh_domain(lo, hi):
    need(type(lo) is int and type(hi) is int and 0 <= lo < 8192 and 0 <= hi < 8192 and not lo & hi, 'invalid original masks')
    lows = [q for q in range(13) if lo >> q & 1]
    highs = [q for q in range(13) if hi >> q & 1]
    free = [q for q in range(13) if not (lo | hi) >> q & 1]
    base = [0] * 13
    for j, q in enumerate(lows):
        base[q] = j - len(lows)
    for j, q in enumerate(highs):
        base[q] = j + 2
    rows = []
    for x in range(1 << len(free)):
        v = list(base)
        for j, q in enumerate(free):
            v[q] = x >> j & 1
        rows.append(v)
    return [lo, hi, lo, hi, 0, 0, 0], rows


def follow(domain, word, start):
    old, rows = domain
    result = []
    touch_mask = None
    tags = None
    active_mask = 0
    for old_row in rows:
        v = list(old_row)
        touches = 0
        for t, (a, b) in enumerate(word):
            u, w = v[a], v[b]
            if u < 0 or u > 1 or w < 0 or w > 1:
                touches |= 1 << t
            elif u > w:
                active_mask |= 1 << t
            if u > w:
                v[a], v[b] = w, u
        current = (sum(1 << q for q, w in enumerate(v) if w < 0),
                   sum(1 << q for q, w in enumerate(v) if w > 1))
        if touch_mask is None:
            touch_mask, tags = touches, current
        need(touches == touch_mask and current == tags, 'marked route varies over original cube')
        result.append(v)
    identities = ((1 << len(word)) - 1) & ~(touch_mask | active_mask)
    return [old[0], old[1], *tags, old[4] + touch_mask.bit_count(),
            old[5] + identities.bit_count(), old[6] | (identities << start)], result


def all_equal_tails(costs, word=()):
    if len(costs) == 1:
        yield [list(g) for g in word]
        return
    for a, b in combinations(sorted(costs), 2):
        if costs[a] != costs[b]:
            continue
        after = dict(costs)
        after[a] += 1
        del after[b]
        yield from all_equal_tails(after, word + ((a, b),))
