"""Exact elementary constructions; no dense-design existence is implemented."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import floor


def require(ok, message):
    if not ok:
        raise ValueError(message)


def edge(a, b):
    return (min(a, b), max(a, b))


def balanced(total, size):
    require(type(total) is int and total >= 0 and type(size) is int and size > 0,
            'invalid balanced-list input')
    q, r = divmod(total, size)
    return [q + (v < r) for v in range(size)]


def realize_degrees(left, forbidden=(), right=None, scale=None, enforce_bound=True):
    """Near-regular allowed graph, with internal or consecutive bipartite labels.

    The proof's hypotheses are checked by default. With enforce_bound=False,
    a successful output is only a finite witness; failure makes no claim.
    The augmenting construction extends the preceding package's algorithm
    to zero target degrees and the new near-regular sufficient inequality.
    """
    sides = [list(left)] + ([] if right is None else [list(right)])
    require(all(sides), 'empty side')
    targets = sum(sides, [])
    n = len(targets)
    require(all(type(x) is int and x >= 0 for x in targets), 'invalid degree')
    require(all(max(row) - min(row) <= 1 for row in sides), 'unbalanced degree list')
    if right is None:
        require(sum(targets) % 2 == 0, 'odd total degree')
        m = sum(targets) // 2
    else:
        require(sum(left) == sum(right), 'unequal bipartite sums')
        m = sum(left)
    forbidden = list(forbidden)
    require(len(forbidden) == len(set(forbidden)), 'repeated forbidden edge')
    blocked = [set() for _ in range(n)]
    for a, b in forbidden:
        require(type(a) is int and type(b) is int and 0 <= a < b < n,
                'invalid forbidden edge')
        if right is not None:
            require(a < len(left) <= b, 'forbidden edge in wrong pair')
        blocked[a].add(b)
        blocked[b].add(a)
    U, D = max(targets), max(map(len, blocked), default=0)
    if m == 0:
        return [], {'direct_additions': 0}
    if scale is None:
        scale = max(1, U, D)
    require(type(scale) is int and scale >= max(1, U, D), 'invalid scale bound')
    if enforce_bound:
        require(min(map(len, sides)) >= 48 * (scale + 1), 'side-size bound fails')
        require(m >= 12 * (scale + 1), 'edge-count cutoff fails')
        require(m > 3 * U * (D + U + 1), 'augmenting count fails')
    residual = targets.copy()
    adjacency = [set() for _ in range(n)]
    result = set()
    stats = Counter()

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

    for a in range(len(left)):
        possible = range(a + 1, n) if right is None else range(len(left), n)
        for b in possible:
            if residual[a] == 0:
                break
            if residual[b] and b not in blocked[a]:
                add(a, b)
                stats['direct_additions'] += 1
    while any(residual):
        deficient = [v for v in range(n) if residual[v]]
        pairs = (combinations(deficient, 2) if right is None else
                 ((a, b) for a in deficient if a < len(left)
                  for b in deficient if b >= len(left)))
        available = next(((a, b) for a, b in pairs
                          if b not in blocked[a] and b not in adjacency[a]), None)
        if available is not None:
            add(*available)
            stats['direct_additions'] += 1
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
            stats['two_vertex_augmentations'] += 1
        elif len(deficient) >= 2:
            a, b = deficient[:2]
            excluded = blocked[a] | blocked[b] | adjacency[a] | adjacency[b] | {a, b}
            selected = next(((c, d) for c, d in sorted(result)
                             if c not in excluded and d not in excluded), None)
            require(selected is not None, 'internal augmenting edge missing')
            c, d = selected
            remove(c, d)
            add(a, c)
            add(b, d)
            stats['two_vertex_augmentations'] += 1
        else:
            a = deficient[0]
            require(residual[a] >= 2, 'single odd deficiency')
            excluded = blocked[a] | adjacency[a] | {a}
            selected = next(((c, d) for c, d in sorted(result)
                             if c not in excluded and d not in excluded), None)
            require(selected is not None, 'one-vertex augmenting edge missing')
            c, d = selected
            remove(c, d)
            add(a, c)
            add(a, d)
            stats['single_vertex_augmentations'] += 1
    return sorted(result), dict(stats)


def edge_color(n, edges):
    """Classical Vizing fan/Kempe construction using Delta+1 colors.

    Returns every edge with a color and counts of the recoloring branches.
    This is not an optimal edge-coloring algorithm or a new coloring result.
    """
    edges = list(edges)
    require(type(n) is int and n >= 0, 'invalid vertex count')
    require(len(edges) == len(set(edges)), 'repeated coloring edge')
    degree = [0] * n
    for a, b in edges:
        require(type(a) is int and type(b) is int and 0 <= a < b < n,
                'invalid coloring edge')
        degree[a] += 1
        degree[b] += 1
    delta = max(degree, default=0)
    palette = range(delta + 1)
    at = [dict() for _ in range(n)]
    colors = {}
    stats = Counter()

    def missing(v):
        return next(c for c in palette if c not in at[v])

    def add(a, b, c):
        e = edge(a, b)
        require(e not in colors and c not in at[a] and c not in at[b],
                'improper coloring update')
        colors[e] = c
        at[a][c] = b
        at[b][c] = a

    def remove(a, b):
        c = colors.pop(edge(a, b))
        del at[a][c]
        del at[b][c]
        return c

    def rotate(u, fan, c):
        old = [remove(u, v) for v in fan[1:]]
        for v, color in zip(fan[:-1], old):
            add(u, v, color)
        add(u, fan[-1], c)
        stats['fan_rotations'] += 1
        stats['rotated_positions'] += len(fan)

    for u, v in sorted(edges):
        alpha = missing(u)
        fan = [v]
        while True:
            beta = missing(fan[-1])
            if beta not in at[u]:
                rotate(u, fan, beta)
                stats['direct_fan_completion'] += 1
                break
            w = at[u][beta]
            if w not in fan:
                fan.append(w)
                continue
            j = fan.index(w)
            require(j >= 1, 'uncolored fan head has a color')
            pivot = fan[j - 1]
            seen, stack, component_edges = {u}, [u], set()
            while stack:
                a = stack.pop()
                for c in (alpha, beta):
                    b = at[a].get(c)
                    if b is not None:
                        component_edges.add(edge(a, b))
                        if b not in seen:
                            seen.add(b)
                            stack.append(b)
            changed = [(a, b, colors[a, b]) for a, b in sorted(component_edges)]
            for a, b, c in changed:
                remove(a, b)
            for a, b, c in changed:
                add(a, b, beta if c == alpha else alpha)
            stats['kempe_components'] += 1
            stats['kempe_recolored_edges'] += len(changed)
            if pivot in seen:
                rotate(u, fan, beta)
                stats['kempe_full_fan'] += 1
            else:
                rotate(u, fan[:j], beta)
                stats['kempe_prefix_fan'] += 1
            break
    return [(a, b, colors[a, b]) for a, b in sorted(edges)], dict(stats)


def external_counts(d, small_sizes, profile):
    """Round exact exceptional triangle masses keyed by (h,i,j)."""
    s, c = sum(small_sizes), d + 2
    cutoff = 12 * (s + 1)
    result = {}
    for (h, i, j), z in sorted(profile.items()):
        require(0 <= h < len(small_sizes) and 0 <= i <= j < d, 'invalid profile index')
        z = Fraction(z)
        require(z >= 0, 'negative profile')
        sh = small_sizes[h]
        t = floor((1 - Fraction(c, sh)) * z) if sh > c else 0
        result[h, i, j] = t if t >= cutoff else 0
    return result


def independent_extension(sizes, small_sizes, profile):
    """Construct exceptional triangles and every colored core-edge witness.

    The caller/checker specifies host support and verifies profile capacities.
    This constructor enforces its numerical degree and avoidance conditions.
    """
    require(all(type(x) is int and x >= 1 for x in sizes), 'invalid core size')
    require(all(type(x) is int and x >= 0 for x in small_sizes), 'invalid extension size')
    n, s, d = sum(sizes), sum(small_sizes), len(sizes)
    offsets = [sum(sizes[:i]) for i in range(d)]
    independent_offsets = [n + sum(small_sizes[:h]) for h in range(len(small_sizes))]
    counts = external_counts(d, small_sizes, profile)
    prior_by_type = {(i, j): set() for i in range(d) for j in range(i, d)}
    records, triangles, degree_stats, coloring_stats = [], [], Counter(), Counter()
    for h, sh in enumerate(small_sizes):
        pieces = []
        for i in range(d):
            for j in range(i, d):
                m = counts.get((h, i, j), 0)
                if not m:
                    continue
                ni, nj = sizes[i], sizes[j]
                left = balanced(2 * m if i == j else m, ni)
                right = None if i == j else balanced(m, nj)
                local, stats = realize_degrees(left, prior_by_type[i, j], right,
                                               scale=max(1, s))
                degree_stats.update(stats)
                prior_by_type[i, j].update(local)
                global_edges = [(offsets[i] + a,
                                 offsets[i] + b if i == j else offsets[j] + b - ni)
                                for a, b in local]
                pieces.extend(global_edges)
        deg = Counter(v for e in pieces for v in e)
        require(not pieces or max(deg.values()) <= sh - 2, 'exceptional color budget fails')
        colored, stats = edge_color(n, pieces)
        coloring_stats.update(stats)
        require(all(c < sh for _, _, c in colored), 'too many independent vertices')
        records.append(colored)
        triangles.extend((a, b, independent_offsets[h] + c) for a, b, c in colored)
    return {'counts': counts, 'colored_edges': records, 'triangles': triangles,
            'degree_operations': dict(degree_stats), 'coloring_operations': dict(coloring_stats)}
