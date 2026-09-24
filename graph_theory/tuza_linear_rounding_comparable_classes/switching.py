"""Exact finite constructions for the two switching lemmas in PROOF.md.

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


def sparse_pack(sizes, counts):
    """Return literal components and every same-pattern role swap for replay."""
    rows, patterns, positions = cyclic_components(sizes, counts)
    N = sum(sizes)
    adjacency = [set() for _ in range(N)]
    owners = defaultdict(set)
    role_counts = Counter((p, v) for p, row in zip(patterns, rows) for v in row)
    degree = Counter(v for row in rows for e in component_edges(row) for v in e)
    D = max(degree.values(), default=0)
    pattern_max = {p: max((role_counts[p, v] for v in range(N)), default=0) for p in counts}
    for p, m in counts.items():
        for i in set(p):
            require((4 * D + 5) * pattern_max[p] < p.count(i) * m,
                    'sparse switching sufficient condition fails')
    for cid, row in enumerate(rows):
        require(len(set(row)) == len(row), 'initial component has repeated vertex')
        for a, b in component_edges(row):
            owners[a, b].add(cid)
            adjacency[a].add(b)
            adjacency[b].add(a)
    initial_excess = sum(len(s) - 1 for s in owners.values())
    queue = [e for e, owner in owners.items() if len(owner) > 1]
    heapify(queue)
    cursors, trace, tested = Counter(), [], 0
    while queue:
        bad = queue[0]
        if len(owners.get(bad, ())) <= 1:
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
                    adjacency[a].remove(b)
                    adjacency[b].remove(a)
        rows[cid][pos], rows[did][slot] = rows[did][slot], rows[cid][pos]
        for j in (cid, did):
            require(len(set(rows[j])) == len(rows[j]), 'switch created repeated vertex')
            for a, b in component_edges(rows[j]):
                owners[a, b].add(j)
                adjacency[a].add(b)
                adjacency[b].add(a)
                if len(owners[a, b]) == 2:
                    heappush(queue, (a, b))
        trace.append((cid, pos, did, slot))
    return {'components': rows, 'patterns': patterns, 'trace': trace,
            'initial_excess': initial_excess, 'maximum_degree': D,
            'candidate_positions_examined': tested}


def avoid_degree_lists(left, forbidden, right=None):
    """Construct positive bounded degrees while avoiding given simple edges.

For a bipartite input, left labels are 0,...,len(left)-1 and right labels
continue after them. Otherwise left is the single prescribed degree list.
"""
    targets = list(left) + ([] if right is None else list(right))
    n = len(targets)
    require(n > 0 and all(type(x) is int and x >= 1 for x in targets), 'invalid degree list')
    U = max(targets)
    require(len(forbidden) == len(set(forbidden)), 'repeated forbidden edge')
    blocked = [set() for _ in range(n)]
    for a, b in forbidden:
        require(0 <= a < b < n, 'invalid forbidden edge')
        if right is not None:
            require(a < len(left) <= b, 'forbidden edge crosses wrong parts')
        blocked[a].add(b)
        blocked[b].add(a)
    D = max(map(len, blocked), default=0)
    L = len(left) if right is None else min(len(left), len(right))
    require(L > 8 * (U + 1) * (D + U + 1), 'forbidden-degree sufficient condition fails')
    if right is None:
        require(sum(targets) % 2 == 0, 'odd total degree')
    else:
        require(sum(left) == sum(right), 'unequal bipartite sums')
    residual = targets.copy()
    adjacency = [set() for _ in range(n)]
    result = set()
    statistics = Counter()

    def add(a, b):
        require(a != b and b not in blocked[a] and b not in adjacency[a], 'invalid added edge')
        require(residual[a] > 0 and residual[b] > 0, 'degree exceeded')
        result.add(edge(a, b))
        adjacency[a].add(b)
        adjacency[b].add(a)
        residual[a] -= 1
        residual[b] -= 1

    def remove(a, b):
        result.remove(edge(a, b))
        adjacency[a].remove(b)
        adjacency[b].remove(a)
        residual[a] += 1
        residual[b] += 1

    # An initial single sweep makes the graph maximal for adding one edge.
    for a in range(len(left)):
        possible = range(a + 1, n) if right is None else range(len(left), n)
        for b in possible:
            if residual[a] == 0:
                break
            if residual[b] and b not in blocked[a]:
                add(a, b)
                statistics['direct_additions'] += 1
    while any(residual):
        deficient = [v for v in range(n) if residual[v]]
        if right is None:
            pairs = combinations(deficient, 2)
        else:
            pairs = ((a, b) for a in deficient if a < len(left)
                     for b in deficient if b >= len(left))
        possible = next(((a, b) for a, b in pairs if b not in blocked[a] and b not in adjacency[a]), None)
        if possible is not None:
            add(*possible)
            statistics['direct_additions'] += 1
            continue
        if right is not None:
            a = next(v for v in deficient if v < len(left))
            b = next(v for v in deficient if v >= len(left))
            bad_left = blocked[b] | adjacency[b] | {a}
            bad_right = blocked[a] | adjacency[a] | {b}
            selected = next(((c, d) for c, d in sorted(result)
                             if c not in bad_left and d not in bad_right), None)
            require(selected is not None, 'bipartite augmenting edge missing')
            c, d = selected
            remove(c, d)
            add(a, d)
            add(c, b)
            statistics['two_vertex_augmentations'] += 1
        elif len(deficient) >= 2:
            a, b = deficient[:2]
            excluded = blocked[a] | blocked[b] | adjacency[a] | adjacency[b] | {a, b}
            selected = next(((c, d) for c, d in sorted(result) if c not in excluded and d not in excluded), None)
            require(selected is not None, 'simple augmenting edge missing')
            c, d = selected
            remove(c, d)
            add(a, c)
            add(b, d)
            statistics['two_vertex_augmentations'] += 1
        else:
            a = deficient[0]
            require(residual[a] >= 2, 'single odd deficiency')
            excluded = blocked[a] | adjacency[a] | {a}
            selected = next(((c, d) for c, d in sorted(result) if c not in excluded and d not in excluded), None)
            require(selected is not None, 'single-vertex augmenting edge missing')
            c, d = selected
            remove(c, d)
            add(a, c)
            add(a, d)
            statistics['single_vertex_augmentations'] += 1
    return sorted(result), dict(statistics)


def truncated_roles(sizes, support, profile, alpha):
    """Exact compressed roles for equation (3), including the N-sized cutoff."""
    d, N = len(sizes), sum(sizes)
    M = comb(d + 2, 3) + comb(d + 1, 2)
    lam = 8 * M / Q(alpha)
    B = M * (6 / Q(alpha) + 2)
    U = ceil(lam + B)
    theta = 1 - lam / N
    require(theta > 0, 'order too small')
    counts = {}
    for p, value in profile.items():
        t = floor(theta * value)
        counts[p] = t if t >= N else 0
    blocks = []
    for i, size in enumerate(sizes):
        division = {p: divmod(count * p.count(i), size) for p, count in counts.items() if count and i in p}
        breaks = sorted({0, size} | {r for q, r in division.values()})
        rows = []
        for lo, hi in zip(breaks, breaks[1:]):
            roles = {p: q + int(lo < r) for p, (q, r) in division.items()}
            degree = Counter()
            for p, value in roles.items():
                remaining = list(p)
                remaining.remove(i)
                for j in remaining:
                    degree[edge(i, j)] += value
            deficit = {}
            for a, b in support:
                if i in (a, b):
                    complete = size - 1 if a == b else sizes[b if a == i else a]
                    deficit[a, b] = complete - degree[a, b]
            rows.append({'start': lo, 'stop': hi, 'roles': roles,
                         'degree': dict(degree), 'deficit': deficit})
        blocks.append(rows)
    return {'counts': counts, 'blocks': blocks, 'M': M, 'lambda': lam, 'B': B, 'U': U}


def empty_band(values, levels):
    require(all(a > b > 0 for a, b in zip(levels, levels[1:])), 'invalid levels')
    require(len(values) <= len(levels) - 2 and all(0 <= x < levels[0] for x in values), 'invalid band input')
    for j in range(len(levels) - 1):
        if not any(levels[j + 1] <= x < levels[j] for x in values):
            return j
    raise ValueError('no empty interval')
