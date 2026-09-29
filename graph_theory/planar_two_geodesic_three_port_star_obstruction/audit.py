#!/usr/bin/env python3
"""Independent rotation and full-simple-path audit of the 11-vertex witness."""


def rotation_check():
    n = 10
    rotation = {u: [(u + 1) % n, (u - 1) % n] for u in range(n)}
    for port in (0, 3, 8):
        rotation[port] = [(port + 1) % n, n, (port - 1) % n]
    rotation[n] = [0, 3, 8]
    darts = {(u, v) for u in rotation for v in rotation[u]}
    assert len(darts) == 26 and all((v, u) in darts for u, v in darts)
    remaining = set(darts)
    faces = []
    while remaining:
        start = min(remaining)
        dart = start
        length = 0
        while True:
            assert dart in remaining
            remaining.remove(dart)
            length += 1
            u, v = dart
            order = rotation[v]
            dart = (v, order[(order.index(u) - 1) % len(order)])
            if dart == start:
                break
        faces.append(length)
    assert sorted(faces) == [4, 5, 7, 10]
    assert 11 - 13 + len(faces) == 2
    return faces


def shortest_path_audit():
    n = 11
    edges = [(u, u + 1) for u in range(9)]
    edges += [(10, u) for u in (0, 3, 8)]
    neighbors = [set() for _ in range(n)]
    dist = [[n + 1] * n for _ in range(n)]
    for u in range(n):
        dist[u][u] = 0
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
        dist[u][v] = dist[v][u] = 1
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    traces = set()
    path_count = 0
    for source in range(n):
        for target in range(source, n):
            def visit(u, seen, length, trace):
                nonlocal path_count
                if length > dist[source][target]:
                    return
                if u == target:
                    if length == dist[source][target]:
                        traces.add(trace)
                        path_count += 1
                    return
                for v in neighbors[u] - seen:
                    visit(v, seen | {v}, length + 1,
                          trace | ((1 << v) if v < 10 else 0))
            visit(source, {source}, 0,
                  (1 << source) if source < 10 else 0)
    maximal = sorted(x for x in traces if not any(
        x != y and x & y == x for y in traces))
    assert path_count == 67 and len(traces) == 57
    assert maximal == [0x007, 0x039, 0x07e, 0x0f0, 0x18c,
                       0x1c3, 0x303, 0x30c, 0x318, 0x3e0]
    assert max((x | y).bit_count() for x in traces for y in traces) == 9
    assert not any(x | y == 0x3ff for x in traces for y in traces)
    return path_count, len(traces), len(maximal)


if __name__ == '__main__':
    faces = rotation_check()
    paths, traces, maximal = shortest_path_audit()
    print(f'faces={sorted(faces)} geodesics={paths} distinct_traces={traces} '
          f'maximal={maximal} max_pair_coverage=9 PASS')
