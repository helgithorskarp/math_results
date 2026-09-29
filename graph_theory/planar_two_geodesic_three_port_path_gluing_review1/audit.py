#!/usr/bin/env python3
"""Independent terminal and combinatorial-family audit for path gluing."""

from collections import deque


def distance(adj, source, target, allowed=None):
    allowed = set(adj) if allowed is None else set(allowed)
    assert source in allowed and target in allowed
    seen = {source}
    queue = deque([(source, 0)])
    while queue:
        u, d = queue.popleft()
        if u == target:
            return d
        for v in adj[u] & allowed - seen:
            seen.add(v)
            queue.append((v, d + 1))
    return None


def components(adj, allowed):
    unseen = set(allowed)
    result = []
    while unseen:
        seed = unseen.pop()
        part = {seed}
        stack = [seed]
        while stack:
            u = stack.pop()
            new = adj[u] & unseen
            unseen.difference_update(new)
            part.update(new)
            stack.extend(new)
        result.append(part)
    return result


def path_terminal_audit():
    # A crosslinked two-port exterior, with every edge optionally deleted.
    checked = 0
    for ell in range(1, 9):
        outside = (ell + 1, ell + 2, ell + 3)
        x, y, z = outside
        edges = [(i, i + 1) for i in range(ell)] + [
            (0, x), (x, ell), (0, y), (y, z), (z, ell), (x, z)]
        for mask in range(1 << len(edges)):
            adj = {v: set() for v in range(ell + 4)}
            for j, (a, b) in enumerate(edges):
                if mask >> j & 1:
                    adj[a].add(b)
                    adj[b].add(a)
            fragment = set(range(ell + 1))
            parts = components(adj, fragment)
            if all(mask >> j & 1 for j in range(ell)):
                k = ell // 2
                assert distance(adj, 0, k) == k
                if k + 1 <= ell:
                    assert distance(adj, k + 1, ell) == ell - k - 1
                assert parts == [fragment]
            else:
                for part in parts:
                    indices = sorted(part)
                    assert indices == list(range(indices[0], indices[-1] + 1))
                    assert not (0 in part and ell in part)
                    for u in indices:
                        for v in indices:
                            assert distance(adj, u, v) == abs(u - v)
            checked += 1
    return checked


def family(m):
    assert m >= 12
    L = m - 8
    adj = {v: set() for v in range(m + 1)}
    next_vertex = m + 1
    a, b, c, d = range(next_vertex, next_vertex + 4)
    for v in (a, b, c, d):
        adj[v] = set()
    next_vertex += 4
    def edge(u, v):
        assert u != v and v not in adj[u]
        adj[u].add(v)
        adj[v].add(u)
    for i in range(m):
        edge(i, (i + 1) % m)
    edge(0, m)
    for port, guard in ((1, a), (3, b), (5, c)):
        edge(port, guard)
    routes = {}
    for name, u, v in (("ab", a, b), ("bc", b, c), ("ca", c, a), ("db", d, b)):
        path = [u]
        for _ in range(L - 1):
            adj[next_vertex] = set()
            path.append(next_vertex)
            next_vertex += 1
        path.append(v)
        for left, right in zip(path, path[1:]):
            edge(left, right)
        routes[name] = path
    edge(a, d)
    q, x, y, p = range(next_vertex, next_vertex + 4)
    for v in (q, x, y, p):
        adj[v] = set()
    for u, v in ((a, q), (d, q), (x, y), (y, p), (p, x),
                 (a, y), (a, p), (d, x), (d, p), (q, x), (q, y)):
        edge(u, v)
    guard = {a, b, c, d}
    octa = {a, d, q, x, y, p}
    expected = [set(range(m + 1)),
                *(set(path[1:-1]) for path in routes.values()),
                {q, x, y, p}]
    assert {frozenset(K) for K in components(adj, set(adj) - guard)} == {
        frozenset(K) for K in expected}
    assert all(len(adj[v] & octa) == 4 for v in octa)
    assert len(adj) == 5 * m - 27
    assert sum(map(len, adj.values())) // 2 == 5 * m - 16
    for first, second in ((1, 3), (1, 5), (3, 5)):
        allowed = (set(adj) - set(range(m + 1))) | {first, second}
        assert distance(adj, first, second, allowed) == L + 2
    if m >= 17:
        ab = routes["ab"]
        left, right = ab[1], ab[-2]
        internal = len(ab) - 3
        assert internal == L - 2 > 6
        assert distance(adj, left, right) <= 6
    return len(adj), sum(map(len, adj.values())) // 2


def main():
    masks = path_terminal_audit()
    sizes = {m: family(m) for m in list(range(12, 61)) + [100]}
    assert sizes[12] == (33, 44) and sizes[100] == (473, 484)
    print(f"terminal_subgraphs={masks} family_orders={len(sizes)} "
          "exterior_lengths_and_counts=PASS nonisometric_m17plus=PASS")


if __name__ == "__main__":
    main()
