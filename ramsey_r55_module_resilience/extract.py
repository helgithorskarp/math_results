#!/usr/bin/env python3
"""Physical forbidden-five extractor for the exceptional-module family."""
import itertools
import json
import sys


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load_graph(obj):
    require(set(obj) == {'n', 'red_edges', 'module', 'deleted'}, 'input fields')
    require(type(obj['n']) is int and obj['n'] == 43, 'order must be 43')
    edges = obj['red_edges']
    require(isinstance(edges, list), 'edge list')
    for e in edges:
        require(isinstance(e, list) and len(e) == 2, 'edge shape')
        require(all(type(v) is int for v in e) and 0 <= e[0] < e[1] < 43,
                'edge labels')
    require(edges == sorted(edges) and len({tuple(e) for e in edges}) == len(edges),
            'sorted distinct edges')
    parts = []
    for name in ('module', 'deleted'):
        part = obj[name]
        require(isinstance(part, list) and all(type(v) is int and 0 <= v < 43
                                             for v in part), 'subset labels')
        require(part == sorted(set(part)), 'sorted distinct subset')
        parts.append(set(part))
    m, deleted = parts
    require(not m & deleted and 2 <= len(m) < 43 - len(deleted), 'proper module')
    red = [0] * 43
    for u, v in edges:
        red[u] |= 1 << v
        red[v] |= 1 << u
    adjacency = [[((1 << 43) - 1) ^ (1 << v) ^ red[v] for v in range(43)], red]
    mask = sum(1 << v for v in m)
    for v in set(range(43)) - m - deleted:
        require(red[v] & mask in (0, mask), 'not a module after deletion')
    mono = len(m) == 3 and len({bool(red[u] >> v & 1)
                              for u, v in itertools.combinations(m, 2)}) == 1
    require(len(deleted) <= 7 or (len(m) >= 3 and len(deleted) <= 15)
            or (len(m) == 3 and len(deleted) <= (17 if mono else 16)),
            'outside the proved exceptional-module family')
    return adjacency, sorted(m), sorted(set(range(43)) - m - deleted)


def clique(rows, vertices, size):
    """Exact ascending bitset recursion; no orbit/census/solver input."""
    def visit(mask, need):
        if need == 0:
            return []
        while mask.bit_count() >= need:
            bit = mask & -mask
            mask ^= bit
            v = bit.bit_length() - 1
            rest = visit(mask & rows[v], need - 1)
            if rest is not None:
                return [v] + rest
        return None
    return visit(sum(1 << v for v in vertices), size)


def vertices(mask):
    return [v for v in range(43) if mask >> v & 1]


def extract(obj):
    adj, module, uniform = load_graph(obj)

    def result(color, q, reason):
        require(len(q) == 5 and len(set(q)) == 5, 'decoder size failure')
        require(all(adj[color][u] >> v & 1 for u, v in itertools.combinations(q, 2)),
                'decoder physical failure')
        return {'color': color, 'vertices': sorted(q), 'reason': reason}

    def lift(color, anchor, pool, reason):
        q = clique(adj[color], pool, 5 - len(anchor))
        if q is not None:
            return result(color, anchor + q, reason)
        q = clique(adj[1-color], pool, 5)
        require(q is not None, 'small Ramsey bound failed; no certificate emitted')
        return result(1-color, q, reason)

    # Classical degree and common-neighborhood obstructions, restricted to M.
    for color in (0, 1):
        for v in module:
            if adj[color][v].bit_count() < 18:
                return lift(1-color, [v], vertices(adj[1-color][v]), 'degree')
        for pair in itertools.combinations(module, 2):
            u, v = pair
            if not (adj[color][u] >> v & 1):
                continue
            common = adj[color][u] & adj[color][v]
            if common.bit_count() > 13:
                return lift(color, list(pair), vertices(common), 'edge_common')
        for triple in itertools.combinations(module, 3):
            if not all(adj[color][u] >> v & 1 for u, v in itertools.combinations(triple, 2)):
                continue
            common = adj[color][triple[0]] & adj[color][triple[1]] & adj[color][triple[2]]
            if common.bit_count() > 4:
                return lift(color, list(triple), vertices(common), 'triangle_common')

    # The general module table uses only the internal clique numbers and the
    # two uniform parts of the undeleted graph. All exceptional edges are free.
    caps = {1: 24, 2: 13, 3: 4, 4: 0}
    for color in (0, 1):
        q = clique(adj[color], module, 5)
        if q is not None:
            return result(color, q, 'inside_module')
        k = 4
        while (anchor := clique(adj[color], module, k)) is None:
            k -= 1
        pool = [v for v in uniform if adj[color][v] >> module[0] & 1]
        if len(pool) > caps[k]:
            return lift(color, anchor, pool, 'uniform_capacity')
    # The only module-table boundary with |M|>=6 and |H|>=28 is
    # |M|=24, |H\M|=4, (omega,alpha)=(3,4) or its reversal.
    # The four uniform vertices see all24 module vertices in one color.
    if len(module) == 24 and len(uniform) == 4:
        color = int(bool(adj[1][uniform[0]] >> module[0] & 1))
        if all(adj[color][v] >> module[0] & 1 for v in uniform):
            for v in uniform:
                if adj[color][v].bit_count() > 24:
                    return lift(color, [v], vertices(adj[color][v]), 'uniform_vertex_degree')
            deleted = obj['deleted']
            require(deleted, 'missing boundary exceptions')
            return result(1-color, uniform + [deleted[0]], 'degree_saturated_module')
    raise RuntimeError('proved family failed to yield a witness; this is not a SAT verdict')


if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf8') as f:
        print(json.dumps(extract(json.load(f)), sort_keys=True))
