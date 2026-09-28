"""Independent exact audit of the prescribed-path attachment family.

Run from the repository root with Python 3.11 or later. No target imports.
"""

from collections import deque
from itertools import combinations


def build(k, m):
    assert k >= 4 and m >= 2
    r, a, b, c = 0, 1, 2, 3
    x = list(range(4, 4 + m))
    y = list(range(4 + m, 4 + 2 * m))
    z = list(range(4 + 2 * m, 4 + 3 * m))
    h_n = 3 * m + 4
    u = [x[0], x[1]] + list(range(h_n, h_n + k - 2))
    v = list(range(h_n + k - 2, h_n + 2 * k - 2))
    n = h_n + 2 * k - 2
    adj = [set() for _ in range(n)]
    def add(p, q):
        assert p != q
        adj[p].add(q)
        adj[q].add(p)
    for p, q in ((a, b), (b, c), (c, a)):
        add(p, q)
    for chain in ([a] + x + [b], [b] + y + [c], [c] + z + [a]):
        for p, q in zip(chain, chain[1:]):
            add(p, q)
    for w in range(1, h_n):
        add(r, w)
    for i in range(k):
        add(r, u[i])
        add(u[i], u[(i + 1) % k])
        add(v[i], v[(i + 1) % k])
        add(u[i], v[i])
        add(u[i], v[(i + 1) % k])
    assert n == 3 * m + 2 * k + 2
    assert set(range(n)) - adj[r] - {r} == set(v)
    assert all(adj[w] & set(v) == {v[(i - 1) % k], v[(i + 1) % k]}
               for i, w in enumerate(v))
    return adj, (x, y, z), u, v


def bfs(adj, start):
    dist = [-1] * len(adj)
    dist[start] = 0
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)
    assert min(dist) == 0
    return dist


def components(adj, removed):
    unseen = set(range(len(adj))) - set(removed)
    out = []
    while unseen:
        start = unseen.pop()
        part = {start}
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u] & unseen:
                unseen.remove(v)
                part.add(v)
                queue.append(v)
        out.append(part)
    return out


def path_check(path, adj, dist):
    assert len(path) == len(set(path))
    assert all(q in adj[p] for p, q in zip(path, path[1:]))
    assert len(path) - 1 == dist[path[0]][path[-1]]


def geodesics(adj, dist):
    n = len(adj)
    for start in range(n):
        yield (start,)
        for end in range(start + 1, n):
            length = dist[start][end]
            stack = [(start, (start,))]
            while stack:
                u, path = stack.pop()
                if u == end:
                    if len(path) - 1 == length:
                        yield path
                    continue
                if len(path) - 1 >= length:
                    continue
                for v in adj[u]:
                    if dist[start][v] == dist[start][u] + 1 and \
                       dist[start][v] + dist[v][end] == length:
                        stack.append((v, path + (v,)))


def audit_instance(k, m):
    adj, (x, y, z), u, v = build(k, m)
    dist = [bfs(adj, start) for start in range(len(adj))]
    p = (0, u[2], v[2])
    q_star = (1, 2, y[0])
    free = ((0, 1), (2, 3))
    for path in (p, q_star, *free):
        path_check(path, adj, dist)
    internal = set(x + y + z)
    best_uniform = len(adj)
    best_supported = 3 * m
    path_count = 0
    for q in geodesics(adj, dist):
        removed = set(p) | set(q)
        parts = components(adj, removed)
        best_uniform = min(best_uniform, max(map(len, parts), default=0))
        best_supported = min(best_supported, max((len(c & internal) for c in parts), default=0))
        path_count += 1
    assert best_supported == 2 * m - 1
    assert best_uniform >= 2 * m
    if m >= 2 * k - 4:
        assert best_uniform == 2 * m
    q_parts = components(adj, set(p) | set(q_star))
    assert max(len(part & internal) for part in q_parts) == 2 * m - 1
    assert max(map(len, q_parts)) <= max(2 * m, m + 2 * k - 4)
    free_parts = components(adj, {0, 1, 2, 3})
    assert sorted(map(len, free_parts)) == [m, m, m + 2 * k - 2]
    assert sorted(len(part & internal) for part in free_parts) == [m, m, m]
    return path_count, best_uniform, best_supported, max(map(len, free_parts))


def local_audit(m):
    # The induced outerplanar H_m, with no universal vertex or annulus.
    adj, (x, y, z), _, _ = build(4, m)
    internal = set(x + y + z)
    h = set(range(1, 3 * m + 4))
    induced = [adj[u] & h for u in range(len(adj))]
    triples = {frozenset((p, mid, q)) for mid in h
               for p, q in combinations(induced[mid], 2)
               if q not in induced[p]}
    sets = [frozenset()] + [frozenset((u,)) for u in h]
    sets += [frozenset(pair) for pair in combinations(h, 2)]
    sets += list(triples)
    for deleted in sets:
        central = {1, 2, 3} - deleted
        assert central
        part = next(c for c in components(induced, set(range(len(adj))) - h | set(deleted))
                    if c & central)
        assert central <= part
        assert len(part & internal) >= 2 * m - 1
        assert len(part) >= 2 * m
    return len(sets)


def main():
    local = sum(local_audit(m) for m in range(2, 17))
    assert local == 8880
    for k, m in ((4, 3), (4, 10), (4, 11), (5, 13)):
        count, uniform, supported, unrestricted = audit_instance(k, m)
        print(f'k={k} m={m} vertices={3*m+2*k+2} geodesics={count} '
              f'prescribed_uniform={uniform} prescribed_supported={supported} '
              f'unrestricted_largest={unrestricted}')
    print(f'local_deletion_sets={local}')


if __name__ == '__main__':
    main()
