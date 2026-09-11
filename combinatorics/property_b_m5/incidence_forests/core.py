"""Exact overlap-graph forests and clique-incidence reconstruction.

All probabilities are integer counts of L-subsets divided by binomial(N,L).
See proof.md for the event definitions and enumeration completeness proofs.
"""
from itertools import combinations, permutations, product
from math import comb


def C(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def canonical(n, edges):
    """Lexicographic minimum over all degree-respecting vertex labelings."""
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    groups = {}
    for i, a in enumerate(adj):
        groups.setdefault(a.bit_count(), []).append(i)
    groups = [groups[k] for k in sorted(groups)]
    best = None
    for parts in product(*(permutations(g) for g in groups)):
        order = sum(parts, ())
        rev = [0] * n
        for i, u in enumerate(order):
            rev[u] = i
        z = tuple(sorted((min(rev[u], rev[v]), max(rev[u], rev[v]))
                         for u, v in edges))
        if best is None or z < best:
            best = z
    return best


def all_graphs(d, max_edges):
    """Every simple d-vertex graph with at most max_edges, up to isomorphism."""
    level = {()}
    counts = []
    for n in range(1, d + 1):
        nxt = set()
        for edges in level:
            for k in range(min(n - 1, max_edges - len(edges)) + 1):
                for nei in combinations(range(n - 1), k):
                    es = edges + tuple((u, n - 1) for u in nei)
                    nxt.add(canonical(n, es))
        level = nxt
        counts.append(len(level))
    return tuple(sorted(level, key=lambda z: (len(z), z))), counts


def forest_numerator(N, L, rows, edges, weights):
    """Hunter maximum-forest bound on all oriented critical-pair events.

rows contains (free size, flag), with flag bits 1=left and 2=right.
edges is the support of the positive intersections; zero weights on this
support are permitted as lower estimates for the event-intersection terms.
    """
    d = len(rows)
    ov = [[0] * d for _ in rows]
    for (u, v), w in zip(edges, weights):
        ov[u][v] = ov[v][u] = w
    support = set(edges)

    def disjoint(i, j):
        return i != j and (min(i, j), max(i, j)) not in support

    events = [(i, j) for i, (a, fi) in enumerate(rows)
              for j, (b, fj) in enumerate(rows)
              if fi & 1 and fj & 2 and disjoint(i, j)]
    total = sum(C(N - rows[i][0] - rows[j][0], L - rows[i][0])
                for i, j in events)
    pairs = []
    for x, y in combinations(range(len(events)), 2):
        i, j = events[x]
        k, ell = events[y]
        if not disjoint(i, ell) or not disjoint(k, j):
            continue
        a = rows[i][0] if i == k else rows[i][0] + rows[k][0] - ov[i][k]
        b = rows[j][0] if j == ell else rows[j][0] + rows[ell][0] - ov[j][ell]
        value = C(N - a - b, L - a)
        if value:
            pairs.append((value, x, y))
    parent = list(range(len(events)))

    def root(u):
        while parent[u] != u:
            u = parent[u]
        return u

    for value, j, k in sorted(pairs, reverse=True):
        j, k = root(j), root(k)
        if j != k:
            parent[j] = k
            total -= value
    return total


def independence_tests(d, edges):
    """In each row, intersections with independent neighbors are disjoint."""
    support = set(edges)
    out = []
    for u in range(d):
        ix = [(i, v if a == u else a)
              for i, (a, v) in enumerate(edges) if a == u or v == u]
        for mask in range(1, 1 << len(ix)):
            pairs = [ix[j] for j in range(len(ix)) if mask >> j & 1]
            if all((min(a, b), max(a, b)) not in support
                   for (_, a), (_, b) in combinations(pairs, 2)):
                out.append((u, tuple(i for i, _ in pairs)))
    return out


def feasible(rows, weights, excess, tests):
    return (sum(weights) >= excess and
            all(sum(weights[i] for i in ix) <= rows[u][0] for u, ix in tests))


def count_critical(rows, columns, L):
    """Count colors of shared columns, then use a private-column polynomial."""
    q = len(columns)
    masks = [sum(1 << j for j, col in enumerate(columns) if i in col)
             for i in range(len(rows))]
    private = [a - mask.bit_count() for (a, _), mask in zip(rows, masks)]
    assert min(private, default=0) >= 0
    total = 0
    for colors in range(1 << q):
        used = colors.bit_count()
        if used > L:
            continue
        dp = {(used, 0): 1}
        for (a, flags), mask, h in zip(rows, masks, private):
            allow_left = flags & 1 and mask & ~colors == 0
            allow_right = flags & 2 and mask & colors == 0
            nxt = {}
            for (t, seen), count in dp.items():
                for j in range(min(h, L - t) + 1):
                    ff = seen | (1 if allow_left and j == h else 0)
                    ff |= 2 if allow_right and j == 0 else 0
                    key = t + j, ff
                    nxt[key] = nxt.get(key, 0) + count * C(h, j)
            dp = nxt
        total += dp.get((L, 3), 0)
    return total, q + sum(private)


def incidence_envelope(N, L, rows, edges, weights):
    """Exhaust all clique-column multiplicities with prescribed pair overlaps.

Returns (-1,0,None) when no covering family realizes the input matrix.
    """
    d = len(rows)
    excess = sum(a for a, _ in rows) - N
    index = {p: i for i, p in enumerate(edges)}
    large = []
    for k in range(3, d + 1):
        for us in combinations(range(d), k):
            pairs = list(combinations(us, 2))
            if all(p in index for p in pairs):
                large.append((us, tuple(index[p] for p in pairs)))
    caps = [a for a, _ in rows]
    residual = list(weights)
    columns = []
    best, count, witness = -1, 0, None

    def rec(t):
        nonlocal best, count, witness
        if t == len(large):
            cols, remaining = columns.copy(), caps.copy()
            for (u, v), w in zip(edges, residual):
                remaining[u] -= w
                remaining[v] -= w
                if remaining[u] < 0 or remaining[v] < 0:
                    return
                cols.extend([(u, v)] * w)
            if sum(len(c) - 1 for c in cols) != excess:
                return
            value, n = count_critical(rows, cols, L)
            assert n == N
            count += 1
            if value > best:
                best, witness = value, cols
            return
        us, ix = large[t]
        limit = min([caps[u] for u in us] + [residual[i] for i in ix])
        for c in range(limit + 1):
            for u in us:
                caps[u] -= c
            for i in ix:
                residual[i] -= c
            columns.extend([us] * c)
            rec(t + 1)
            if c:
                del columns[-c:]
            for u in us:
                caps[u] += c
            for i in ix:
                residual[i] += c

    rec(0)
    return best, count, witness
