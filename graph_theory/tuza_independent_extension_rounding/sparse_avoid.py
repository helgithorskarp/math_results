"""Role-preserving sparse packing avoiding a fixed forbidden graph.

Adapted from tuza_linear_rounding_comparable_classes/switching.py; the new
argument uses the union neighborhood and also repairs forbidden occurrences.

These routines do not implement Keevash's decomposition or evaluate N_0.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from heapq import heapify, heappop, heappush
from itertools import combinations, combinations_with_replacement
from math import ceil, comb, floor


def require(ok, message):
    if not ok:
        raise ValueError(message)


def edge(a, b):
    return (min(a, b), max(a, b))


def component_edges(row):
    return [edge(a, b) for a, b in combinations(row, 2)]


def triangle_types(d, support):
    return [t for t in combinations_with_replacement(range(d), 3)
            if set(component_edges(t)) <= set(support)]


def cyclic_components(sizes, counts):
    offsets, N = [], 0
    for size in sizes:
        require(type(size) is int and size >= 3, 'class too small')
        offsets.append(N)
        N += size
    rows, patterns = [], []
    positions = defaultdict(list)
    for p, count in sorted(counts.items()):
        require(len(p) in (2, 3) and tuple(sorted(p)) == p, 'invalid pattern')
        require(all(type(i) is int and 0 <= i < len(sizes) for i in p), 'invalid type')
        require(type(count) is int and count > 0, 'invalid count')
        multiplicity = Counter(p)
        for t in range(count):
            used, row = Counter(), []
            for i in p:
                row.append(offsets[i] + (t * multiplicity[i] + used[i]) % sizes[i])
                used[i] += 1
            cid = len(rows)
            rows.append(row)
            patterns.append(p)
            for pos, i in enumerate(p):
                positions[p, i].append((cid, pos))
    return rows, patterns, positions


def sparse_pack(sizes, counts, forbidden=()):
    """Return literal components and every same-pattern role swap for replay."""
    rows, patterns, positions = cyclic_components(sizes, counts)
    N = sum(sizes)
    forbidden = list(forbidden)
    require(len(forbidden) == len(set(forbidden)), 'repeated forbidden edge')
    fixed = set(forbidden)
    adjacency = [set() for _ in range(N)]
    for a, b in forbidden:
        require(type(a) is int and type(b) is int and 0 <= a < b < N,
                'invalid forbidden edge')
        adjacency[a].add(b)
        adjacency[b].add(a)
    fixed_degree = max(map(len, adjacency), default=0)
    owners = defaultdict(set)
    role_counts = Counter((p, v) for p, row in zip(patterns, rows) for v in row)
    degree = Counter(v for row in rows for e in component_edges(row) for v in e)
    D = max(degree.values(), default=0)
    pattern_max = {p: max((role_counts[p, v] for v in range(N)), default=0) for p in counts}
    for p, m in counts.items():
        for i in set(p):
            require((4 * (D + fixed_degree) + 5) * pattern_max[p] < p.count(i) * m,
                    'sparse switching sufficient condition fails')
    for cid, row in enumerate(rows):
        require(len(set(row)) == len(row), 'initial component has repeated vertex')
        for a, b in component_edges(row):
            owners[a, b].add(cid)
            adjacency[a].add(b)
            adjacency[b].add(a)
    initial_excess = (sum(len(s) - 1 for s in owners.values())
                      + sum(len(owners.get(e, ())) for e in fixed))
    queue = [e for e, owner in owners.items() if len(owner) > 1 or e in fixed]
    heapify(queue)
    cursors, trace, tested = Counter(), [], 0
    while queue:
        bad = queue[0]
        if not owners.get(bad) or (len(owners[bad]) <= 1 and bad not in fixed):
            heappop(queue)
            continue
        cid = min(owners[bad])
        p, u = patterns[cid], bad[0]
        pos = rows[cid].index(u)
        i = p[pos]
        others = [v for k, v in enumerate(rows[cid]) if k != pos]
        candidates = positions[p, i]
        start = cursors[p, i]
        for step in range(len(candidates)):
            index = (start + step) % len(candidates)
            did, slot = candidates[index]
            w = rows[did][slot]
            tested += 1
            if w == u or w in others or any(w in adjacency[v] for v in others):
                continue
            rest = [v for k, v in enumerate(rows[did]) if k != slot]
            if any(v == u or v in adjacency[u] for v in rest):
                continue
            break
        else:
            raise ValueError('no admissible sparse switch')
        cursors[p, i] = (index + 1) % len(candidates)
        for j in (cid, did):
            for a, b in component_edges(rows[j]):
                owners[a, b].remove(j)
                if not owners[a, b]:
                    del owners[a, b]
                    if (a, b) not in fixed:
                        adjacency[a].remove(b)
                        adjacency[b].remove(a)
        rows[cid][pos], rows[did][slot] = rows[did][slot], rows[cid][pos]
        for j in (cid, did):
            require(len(set(rows[j])) == len(rows[j]), 'switch created repeated vertex')
            for a, b in component_edges(rows[j]):
                owners[a, b].add(j)
                adjacency[a].add(b)
                adjacency[b].add(a)
                if len(owners[a, b]) == 2 or (a, b) in fixed:
                    heappush(queue, (a, b))
        trace.append((cid, pos, did, slot))
    return {'components': rows, 'patterns': patterns, 'trace': trace,
            'initial_excess': initial_excess, 'maximum_degree': D,
            'candidate_positions_examined': tested, 'forbidden_maximum_degree': fixed_degree}
