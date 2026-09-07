#!/usr/bin/env python3
"""A physical five-set from a cut with a zero row and a zero column."""
import hashlib
import itertools
import json
import sys


def parse(obj):
    if not isinstance(obj, dict) or set(obj) != {'n', 'red_hex', 'cut', 'color'}:
        raise ValueError('graph fields')
    if type(obj['n']) is not int or obj['n'] != 43:
        raise ValueError('order')
    word = obj['red_hex']
    if not isinstance(word, str) or len(word) != 226 or any(c not in '0123456789abcdef' for c in word):
        raise ValueError('packed graph')
    word = int(word, 16)
    if word >= 1 << 903:
        raise ValueError('graph padding')
    cut = obj['cut']
    if not isinstance(cut, list) or any(type(v) is not int or not 0 <= v < 43 for v in cut):
        raise ValueError('cut vertices')
    if not 1 <= len(cut) <= 42 or cut != sorted(set(cut)):
        raise ValueError('cut')
    if type(obj['color']) is not int or obj['color'] not in (0, 1):
        raise ValueError('color')
    adj = [0] * 43
    i = 0
    for u in range(43):
        for v in range(u + 1, 43):
            if (word >> i) & 1:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
            i += 1
    return adj, cut, [v for v in range(43) if v not in cut]


def clique(adj, vertices, size):
    if size == 0:
        return []
    while vertices:
        if vertices.bit_count() < size:
            break
        bit = vertices & -vertices
        v = bit.bit_length() - 1
        vertices ^= bit
        rest = clique(adj, vertices & adj[v], size - 1)
        if rest is not None:
            return [v] + rest
    return None


def extract(obj):
    red, a, b = parse(obj)
    universe = (1 << 43) - 1
    blue = [universe ^ (1 << v) ^ red[v] for v in range(43)]
    colors = [blue, red]
    c = obj['color']
    adj, other = colors[c], colors[1 - c]
    aa = sum(1 << v for v in a)
    bb = sum(1 << v for v in b)
    rows = [v for v in a if not adj[v] & bb]
    cols = [v for v in b if not adj[v] & aa]
    if not rows or not cols:
        return {'status': 'OUTSIDE_ZERO_PAIR_FAMILY'}
    u, v = rows[0], cols[0]
    if adj[u].bit_count() >= 18:
        pool = sum(1 << w for w in list(w for w in range(43) if adj[u] >> w & 1)[:18])
        q = clique(adj, pool, 4)
        if q is not None:
            q.append(u)
            color = c
        else:
            q = clique(other, pool, 4)
            if q is None:
                raise RuntimeError('R(4,4) extraction failed')
            q.append(v)
            color = 1 - c
        route = 'mixed_eighteen'
    else:
        # At least 25 opposite-color neighbors; R(4,5)<=25.
        pool = sum(1 << w for w in list(w for w in range(43) if other[u] >> w & 1)[:25])
        q = clique(adj, pool, 5)
        if q is not None:
            color = c
        else:
            q = clique(other, pool, 4)
            if q is None:
                raise RuntimeError('R(4,5) extraction failed')
            q.append(u)
            color = 1 - c
        route = 'low_degree_twenty_five'
    canonical = json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()
    return {'status': 'EXCLUDED_WITH_PHYSICAL_FIVE', 'input_sha256': hashlib.sha256(canonical).hexdigest(),
            'zero_pair': [u, v], 'route': route, 'five': sorted(q), 'five_color': color}


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        obj = json.load(f)
    print(json.dumps(extract(obj), sort_keys=True))
