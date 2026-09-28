#!/usr/bin/env python3
"""Exact three-port regression for the exterior metric-closure theorem."""

from collections import deque


FRAGMENT = frozenset(range(5))
PORTS = (0, 1, 2)
PAIRS = ((0, 1), (0, 2), (1, 2))
EDGES = ((0, 3), (3, 1), (1, 4), (4, 2),
         (0, 5), (5, 1), (1, 6), (6, 2),
         (5, 6), (0, 7), (7, 2))


def add(graph, u, v):
    graph[u].add(v)
    graph[v].add(u)


def subgraph(mask):
    graph = [set() for _ in range(8)]
    for i, (u, v) in enumerate(EDGES):
        if mask & (1 << i):
            add(graph, u, v)
    return graph


def distances(graph, source, allowed=None):
    dist = [-1] * len(graph)
    dist[source] = 0
    todo = deque([source])
    while todo:
        u = todo.popleft()
        for v in graph[u]:
            if dist[v] < 0 and (allowed is None or v in allowed):
                dist[v] = dist[u] + 1
                todo.append(v)
    return dist


def exterior_array(graph):
    exterior = [set() for _ in graph]
    for u, neighbors in enumerate(graph):
        for v in neighbors:
            if u not in FRAGMENT or v not in FRAGMENT:
                exterior[u].add(v)
    answer = []
    for a, b in PAIRS:
        allowed = (set(range(len(graph))) - FRAGMENT) | {a, b}
        value = distances(exterior, a, allowed)[b]
        assert value == -1 or value >= 2
        answer.append(value)
    return tuple(answer)


def model(graph, delta):
    result = [set() for _ in FRAGMENT]
    for u in FRAGMENT:
        for v in graph[u] & FRAGMENT:
            if u < v:
                add(result, u, v)
    for (a, b), length in zip(PAIRS, delta):
        if length < 0:
            continue
        path = [a]
        for _ in range(length - 1):
            path.append(len(result))
            result.append(set())
        path.append(b)
        for u, v in zip(path, path[1:]):
            add(result, u, v)
    return result


def geodesic_traces(graph):
    result = {}
    for source in FRAGMENT:
        dist = distances(graph, source)

        def visit(u, mask):
            if u in FRAGMENT:
                result.setdefault((source, u), set()).add(mask)
            for v in graph[u]:
                if dist[v] == dist[u] + 1:
                    visit(v, mask | ((1 << v) if v in FRAGMENT else 0))

        visit(source, 1 << source)
    return result


def components(graph):
    remaining = set(FRAGMENT)
    parts = []
    while remaining:
        start = remaining.pop()
        part = {start}
        todo = [start]
        while todo:
            u = todo.pop()
            for v in graph[u] & remaining:
                remaining.remove(v)
                part.add(v)
                todo.append(v)
        parts.append(sum(1 << v for v in part))
    return parts


def coverable(target, traces, k):
    masks = {mask & target for family in traces.values() for mask in family}
    if k == 1:
        return target in masks
    return any((a | b) == target for a in masks for b in masks)


def main():
    arrays = set()
    nonmetric = set()
    trace_count = cover_checks = 0
    for mask in range(1 << len(EDGES)):
        host = subgraph(mask)
        delta = exterior_array(host)
        arrays.add(delta)
        if delta[0] >= 0 and delta[2] >= 0 and (
                delta[1] < 0 or delta[1] > delta[0] + delta[2]):
            nonmetric.add(delta)
        reduced = model(host, delta)
        host_traces = geodesic_traces(host)
        model_traces = geodesic_traces(reduced)
        assert host_traces == model_traces
        trace_count += sum(len(x) for x in host_traces.values())
        for u in FRAGMENT:
            host_dist = distances(host, u)
            model_dist = distances(reduced, u)
            assert all(host_dist[v] == model_dist[v] for v in FRAGMENT)
        for part in components(host):
            for k in (1, 2):
                assert coverable(part, host_traces, k) == coverable(
                    part, model_traces, k)
                cover_checks += 1
    assert nonmetric
    print(f"states={1 << len(EDGES)} distinct_arrays={len(arrays)} "
          f"nonmetric_arrays={len(nonmetric)} geodesic_traces={trace_count} "
          f"cover_checks={cover_checks} PASS")


if __name__ == "__main__":
    main()
