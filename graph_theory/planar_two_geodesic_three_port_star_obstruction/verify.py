#!/usr/bin/env python3
"""Exact certificate for the sharp three-port boundary of cycle terminals.

Enumerates every ambient geodesic, including paths with the hub as an
endpoint. The all-order extension is proved separately by tail trimming.
"""

from collections import deque
from fractions import Fraction as F


PORTS = (0, 3, 8)
EXPECTED_MAXIMAL = (0x007, 0x039, 0x07e, 0x0f0, 0x18c,
                    0x1c3, 0x303, 0x30c, 0x318, 0x3e0)


def graph(m, close=True):
    assert m >= 10
    adj = [set() for _ in range(m + 1)]
    for u in range(m - 1):
        adj[u].add(u + 1)
        adj[u + 1].add(u)
    if close:
        adj[0].add(m - 1)
        adj[m - 1].add(0)
    for u in PORTS:
        adj[u].add(m)
        adj[m].add(u)
    return adj


def geodesic_traces(adj, m):
    """Return C-vertex masks of all shortest paths with ANY endpoints."""
    n = len(adj)
    traces = set()
    path_count = 0
    for source in range(n):
        dist = [-1] * n
        dist[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        assert all(d >= 0 for d in dist)
        for target in range(source, n):
            def visit(u, trace):
                nonlocal path_count
                if u == target:
                    traces.add(trace)
                    path_count += 1
                    return
                for v in adj[u]:
                    if dist[v] == dist[u] + 1 and dist[v] <= dist[target]:
                        visit(v, trace | ((1 << v) if v < m else 0))
            visit(source, (1 << source) if source < m else 0)
    return traces, path_count


def components(adj, allowed):
    todo = set(allowed)
    result = []
    while todo:
        queue = [todo.pop()]
        comp = set(queue)
        for u in queue:
            fresh = adj[u] & todo
            todo -= fresh
            comp |= fresh
            queue.extend(fresh)
        result.append(comp)
    return result


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


def geometry_audit(m):
    adj = graph(m)
    # Points on a strictly convex parabola, closed by one chord.
    xy = [(F(i), F(i * i)) for i in range(m)]
    xy.append(tuple(sum(xy[v][j] for v in PORTS) / 3 for j in range(2)))
    assert len(set(xy)) == m + 1
    edges = [(u, v) for u in range(m + 1) for v in adj[u] if u < v]
    assert len(edges) == m + 3
    for i, (u, v) in enumerate(edges):
        for s, t in edges[:i]:
            shared = {u, v} & {s, t}
            if not shared:
                assert not meet(xy[u], xy[v], xy[s], xy[t]), (m, u, v, s, t)
            else:
                h = shared.pop()
                r = v if u == h else u
                w = t if s == h else s
                assert not on_segment(xy[h], xy[r], xy[w])
                assert not on_segment(xy[h], xy[w], xy[r])
    assert len(components(adj, range(m + 1))) == 1
    assert all(len(components(adj, set(range(m + 1)) - {v})) == 1
               for v in range(m + 1))
    assert {u for u in range(m) if m in adj[u]} == set(PORTS)
    return len(edges)


def main():
    for m in (10, 11, 12, 20, 50):
        e = geometry_audit(m)
        print(f'cycle_order={m} vertices={m+1} edges={e} '
              'planar=PASS biconnected=PASS')

    for m in (10, 11, 12, 13):
        adj = graph(m, close=False)  # delete the closing cycle edge
        assert components(adj, range(m)) == [set(range(m))]
        traces, path_count = geodesic_traces(adj, m)
        maximal = tuple(sorted(x for x in traces if not any(
            x != y and x & y == x for y in traces)))
        max_pair = max((x | y).bit_count() for x in traces for y in traces)
        assert max_pair < m
        if m == 10:
            assert len(traces) == 57
            assert maximal == EXPECTED_MAXIMAL
            assert max_pair == 9
        print(f'deleted_order={m} geodesics={path_count} '
              f'distinct_traces={len(traces)} maximal={len(maximal)} '
              f'max_pair_coverage={max_pair} PASS')
    print('PASS')


if __name__ == '__main__':
    main()
