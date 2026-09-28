#!/usr/bin/env python3
"""Exact coordinate and graph audit of the three-port/path gluing family.

Uses only the Python standard library.  Straight-line crossings are tested
with rational arithmetic; this is an audit of the explicit all-order drawing,
not an enumeration of edge subgraphs or vertex weights.
"""

from collections import deque
from fractions import Fraction as F


def mix(a, b, t):
    return tuple((1 - t) * a[i] + t * b[i] for i in range(2))


def build(m):
    assert m >= 12
    length = m - 8
    xy = {}
    edges = set()
    routes = {}

    def vertex(v, p):
        assert v not in xy
        xy[v] = tuple(F(z) for z in p)

    def edge(u, v):
        assert u in xy and v in xy and u != v
        e = frozenset((u, v))
        assert e not in edges
        edges.add(e)

    def subdivide(u, v, count, name):
        path = [u]
        for i in range(1, count):
            w = f'{name}{i}'
            vertex(w, mix(xy[u], xy[v], F(i, count)))
            path.append(w)
        path.append(v)
        for s, t in zip(path, path[1:]):
            edge(s, t)
        routes[name] = path

    inner = {'v1': (-1, 0), 'v3': (1, 0), 'v5': (0, 2)}
    for v, point in inner.items():
        vertex(v, point)
    vertex('v2', (0, 0))
    vertex('v4', (F(1, 2), 1))
    for i, v in enumerate(list(range(6, m)) + [0], 1):
        vertex(f'v{v}', mix(xy['v5'], xy['v1'], F(i, m - 4)))
    vertex(f'v{m}', mix(xy['v0'], (F(0), F(2, 3)), F(1, 4)))
    for i in range(m):
        edge(f'v{i}', f'v{(i + 1) % m}')
    edge('v0', f'v{m}')

    for v, point in {'a': (-4, -3), 'b': (4, -3),
                     'c': (0, 8), 'd': (-5, -7),
                     'q': (-12, -3)}.items():
        vertex(v, point)
    for u, v in [('a', 'v1'), ('b', 'v3'), ('c', 'v5')]:
        edge(u, v)
    for u, v, name in [('a', 'b', 'ab'), ('b', 'c', 'bc'),
                       ('c', 'a', 'ca'), ('d', 'b', 'db')]:
        subdivide(u, v, length, name)
    edge('a', 'd')

    # Octahedron on {a,d,q,x,y,p}, with outer face a-d-q.
    outer = (xy['a'], xy['d'], xy['q'])
    weights = {'x': (F(3, 20), F(17, 40), F(17, 40)),
               'y': (F(17, 40), F(3, 20), F(17, 40)),
               'p': (F(17, 40), F(17, 40), F(3, 20))}
    for v, w in weights.items():
        vertex(v, tuple(sum(w[j] * outer[j][i] for j in range(3))
                        for i in range(2)))
    for u, v in [('a', 'q'), ('d', 'q'), ('x', 'y'), ('y', 'p'),
                 ('p', 'x'), ('a', 'y'), ('a', 'p'), ('d', 'x'),
                 ('d', 'p'), ('q', 'x'), ('q', 'y')]:
        edge(u, v)
    return xy, edges, routes


def adjacency(xy, edges):
    adj = {v: set() for v in xy}
    for u, v in (tuple(e) for e in edges):
        adj[u].add(v)
        adj[v].add(u)
    return adj


def components(adj, allowed):
    todo = set(allowed)
    result = []
    while todo:
        start = todo.pop()
        comp = {start}
        queue = [start]
        for u in queue:
            new = adj[u] & todo
            todo -= new
            comp |= new
            queue.extend(new)
        result.append(comp)
    return result


def restricted_distance(adj, m, src, dst):
    allowed = set(adj) - {f'v{i}' for i in range(m + 1)} | {src, dst}
    queue = deque([(src, 0)])
    seen = {src}
    while queue:
        u, dist = queue.popleft()
        if u == dst:
            return dist
        for v in adj[u] & allowed - seen:
            seen.add(v)
            queue.append((v, dist + 1))
    return None


def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def on_segment(a, b, p):
    return (cross(a, b, p) == 0 and
            all(min(a[i], b[i]) <= p[i] <= max(a[i], b[i])
                for i in range(2)))


def meet(a, b, c, d):
    ab_c, ab_d = cross(a, b, c), cross(a, b, d)
    cd_a, cd_b = cross(c, d, a), cross(c, d, b)
    if ab_c == ab_d == cd_a == cd_b == 0:
        return any(on_segment(a, b, p) for p in (c, d)) or any(
            on_segment(c, d, p) for p in (a, b))
    return ab_c * ab_d <= 0 and cd_a * cd_b <= 0


def audit(m):
    xy, edges, routes = build(m)
    adj = adjacency(xy, edges)
    length = m - 8
    assert len(xy) == 5 * m - 27
    assert len(edges) == 5 * m - 16
    assert len(components(adj, set(xy))) == 1
    assert len(set(xy.values())) == len(xy)

    segments = [tuple(e) for e in edges]
    for i, (u, v) in enumerate(segments):
        for s, t in segments[:i]:
            if {u, v}.isdisjoint({s, t}):
                assert not meet(xy[u], xy[v], xy[s], xy[t]), (u, v, s, t)
            else:
                shared = ({u, v} & {s, t}).pop()
                r = v if u == shared else u
                w = t if s == shared else s
                assert not (cross(xy[shared], xy[r], xy[w]) == 0 and
                            on_segment(xy[shared], xy[r], xy[w]))
                assert not (cross(xy[shared], xy[w], xy[r]) == 0 and
                            on_segment(xy[shared], xy[w], xy[r]))

    guard = {'a', 'b', 'c', 'd'}
    residual = components(adj, set(xy) - guard)
    expected = [{f'v{i}' for i in range(m + 1)},
                *[set(path[1:-1]) for path in routes.values()],
                {'q', 'x', 'y', 'p'}]
    assert {frozenset(c) for c in residual} == {frozenset(c) for c in expected}
    assert all(len(routes[name]) == length + 1
               for name in ('ab', 'bc', 'ca', 'db'))
    for name, path in routes.items():
        interior = path[1:-1]
        assert all((adj[v] - set(interior)) <= {path[0], path[-1]}
                   for v in interior), name
    for src, dst in [('v1', 'v3'), ('v1', 'v5'), ('v3', 'v5')]:
        assert restricted_distance(adj, m, src, dst) == m - 6

    octa = {'a', 'd', 'q', 'x', 'y', 'p'}
    assert all(len(adj[v] & octa) == 4 for v in octa)
    assert sum(len(adj[v] & octa) for v in octa) == 24
    print(f'm={m} vertices={len(xy)} edges={len(edges)} '
          f'residuals={sorted(map(len, residual))} '
          f'exterior_lengths={(m - 6,) * 3} planar=PASS')


if __name__ == '__main__':
    for size in (12, 13, 16, 32, 100):
        audit(size)
    print('PASS')
