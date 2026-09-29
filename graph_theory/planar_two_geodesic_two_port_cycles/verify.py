#!/usr/bin/env python3
"""Independent finite controls for an all-order two-port path/cycle theorem.

No third-party packages. Exact rational coordinates certify the displayed
planar family; shortest-path enumeration checks small cycle edge masks.
"""

from collections import deque
from fractions import Fraction as F
from itertools import combinations


def components(adj, allowed):
    unseen = set(allowed)
    result = []
    while unseen:
        queue = [unseen.pop()]
        comp = set(queue)
        for u in queue:
            fresh = adj[u] & unseen
            unseen -= fresh
            comp |= fresh
            queue.extend(fresh)
        result.append(comp)
    return result


def cycle_cover(m, a, b, ear, mask):
    """Check all anchored shortest-path traces in one finite theta model."""
    n = m if ear is None else m + ear - 1
    adj = [set() for _ in range(n)]
    for i in range(m):
        if mask & (1 << i):
            u, v = i, (i + 1) % m
            adj[u].add(v)
            adj[v].add(u)
    if ear is not None:
        route = [a] + list(range(m, n)) + [b]
        for u, v in zip(route, route[1:]):
            adj[u].add(v)
            adj[v].add(u)

    for comp in components(adj, range(m)):
        target = sum(1 << v for v in comp)
        geodesic_masks = set()
        for u in comp:
            dist = [-1] * n
            dist[u] = 0
            queue = deque([u])
            while queue:
                x = queue.popleft()
                for y in adj[x]:
                    if dist[y] < 0:
                        dist[y] = dist[x] + 1
                        queue.append(y)
            for v in comp:
                if v < u:
                    continue
                if v == u:
                    geodesic_masks.add(1 << u)
                    continue

                def walk(x, seen, length, trace):
                    if length > dist[v]:
                        return
                    if x == v:
                        if length == dist[v]:
                            geodesic_masks.add(trace)
                        return
                    for y in adj[x] - seen:
                        walk(y, seen | {y}, length + 1,
                             trace | ((1 << y) if y < m else 0))

                walk(u, {u}, 0, 1 << u)
        if not any(x | y == target
                   for x in geodesic_masks for y in geodesic_masks):
            return False
    return True


def small_cycle_audit():
    for m in range(4, 10):
        states = 0
        for a, b in combinations(range(m), 2):
            # Any route of length >=m cannot improve a connected cycle
            # component's internal distance; infinity represents the cap.
            for ear in [None] + list(range(2, m + 1)):
                for mask in range(1 << m):
                    assert cycle_cover(m, a, b, ear, mask), (m, a, b, ear, mask)
                    states += 1
        print(f'cycle_order={m} profiles={states} PASS')


def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def on_segment(a, b, p):
    return cross(a, b, p) == 0 and all(
        min(a[i], b[i]) <= p[i] <= max(a[i], b[i]) for i in range(2))


def meet(a, b, c, d):
    ab_c, ab_d = cross(a, b, c), cross(a, b, d)
    cd_a, cd_b = cross(c, d, a), cross(c, d, b)
    if ab_c == ab_d == cd_a == cd_b == 0:
        return (any(on_segment(a, b, p) for p in (c, d)) or
                any(on_segment(c, d, p) for p in (a, b)))
    return ab_c * ab_d <= 0 and cd_a * cd_b <= 0


def family(m):
    assert m >= 8
    k = m // 2
    xy = {}
    edges = set()

    def point(v, x, y):
        assert v not in xy
        xy[v] = (F(x), F(y))

    def edge(u, v):
        assert u in xy and v in xy and u != v
        pair = frozenset((u, v))
        assert pair not in edges
        edges.add(pair)

    for i in range(k + 1):
        x = -2 + F(4 * i, k)
        point(f'v{i}', x, 2 - x*x/2)
    for j in range(1, m - k):
        x = 2 - F(4 * j, m - k)
        point(f'v{k+j}', x, -2 + x*x/2)
    for i in range(m):
        edge(f'v{i}', f'v{(i + 1) % m}')

    for v, x, y in [('a', -3, 3), ('b', 3, 3), ('q', 0, 9)]:
        point(v, x, y)
    for u, v in [('v0', 'a'), (f'v{k}', 'b'), ('a', 'b')]:
        edge(u, v)
    outer = (xy['a'], xy['b'], xy['q'])
    weights = {'x': (F(3, 20), F(17, 40), F(17, 40)),
               'y': (F(17, 40), F(3, 20), F(17, 40)),
               'p': (F(17, 40), F(17, 40), F(3, 20))}
    for v, coeffs in weights.items():
        point(v, *(sum(coeffs[j] * outer[j][i] for j in range(3))
                   for i in range(2)))
    for u, v in [('a', 'q'), ('b', 'q'), ('x', 'y'), ('y', 'p'),
                 ('p', 'x'), ('a', 'y'), ('a', 'p'), ('b', 'x'),
                 ('b', 'p'), ('q', 'x'), ('q', 'y')]:
        edge(u, v)
    return xy, edges


def family_audit(m):
    xy, edges = family(m)
    adj = {v: set() for v in xy}
    for u, v in (tuple(e) for e in edges):
        adj[u].add(v)
        adj[v].add(u)
    assert len(xy) == m + 6 and len(edges) == m + 14
    assert len(set(xy.values())) == len(xy)
    segments = [tuple(e) for e in edges]
    for i, (u, v) in enumerate(segments):
        for s, t in segments[:i]:
            shared = {u, v} & {s, t}
            if not shared:
                assert not meet(xy[u], xy[v], xy[s], xy[t]), (u, v, s, t)
            else:
                h = shared.pop()
                r = v if u == h else u
                w = t if s == h else s
                assert not on_segment(xy[h], xy[r], xy[w])
                assert not on_segment(xy[h], xy[w], xy[r])
    assert len(components(adj, set(xy))) == 1
    assert all(len(components(adj, set(xy) - {v})) == 1 for v in xy)
    residual = components(adj, set(xy) - {'a', 'b'})
    assert {frozenset(c) for c in residual} == {
        frozenset(f'v{i}' for i in range(m)), frozenset({'q', 'x', 'y', 'p'})}
    octa = {'a', 'b', 'q', 'x', 'y', 'p'}
    assert all(len(adj[v] & octa) == 4 for v in octa)
    queue = deque([('v0', 0)])
    seen = {'v0'}
    outside = set(xy) - {f'v{i}' for i in range(m)} | {'v0', f'v{m//2}'}
    while queue:
        u, d = queue.popleft()
        if u == f'v{m//2}':
            assert d == 3
            break
        for v in adj[u] & outside - seen:
            seen.add(v)
            queue.append((v, d + 1))
    else:
        raise AssertionError('missing exterior route')
    assert m//2 > 3
    print(f'family_order={m} vertices={len(xy)} edges={len(edges)} '
          'biconnected=PASS planar=PASS exterior=3')


if __name__ == '__main__':
    small_cycle_audit()
    for size in (8, 9, 16, 32, 100):
        family_audit(size)
    print('PASS')
