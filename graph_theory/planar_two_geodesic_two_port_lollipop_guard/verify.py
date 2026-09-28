#!/usr/bin/env python3
"""Exact finite audits for the two-port lollipop guard theorem."""

from collections import deque
from random import Random


def family(r, m=11):
    assert r >= 1 and m >= 5
    rotation = [[1, 4, 3, 5], [2, 4, 0, 5], [3, 4, 1, 5],
                [0, 4, 2, 5], [0, 1, 2, 3], [0, 3, 2, 1]]
    gadgets = []
    for _ in range(r):
        base = len(rotation)
        c = [base + i for i in range(m + 1)]
        rotation[0].insert(rotation[0].index(1) + 1, c[1])
        rotation[1].insert(rotation[1].index(0), c[3])
        for i in range(m + 1):
            if i == 0:
                around = [c[1], c[m - 1], c[m]]
            elif i == 1:
                around = [c[0], c[2], 0]
            elif i == 3:
                around = [c[2], c[4], 1]
            elif i == m - 1:
                around = [c[0], c[m - 2]]
            elif i == m:
                around = [c[0]]
            else:
                around = [c[i - 1], c[i + 1]]
            rotation.append(around)
        gadgets.append(c)
    graph = [set(row) for row in rotation]
    return graph, rotation, gadgets


def check_rotation(graph, rotation, r, m):
    assert len(graph) == 6 + r * (m + 1)
    assert all(len(rotation[u]) == len(graph[u]) == len(set(rotation[u]))
               for u in range(len(graph)))
    darts = {(u, v) for u, row in enumerate(graph) for v in row}
    assert all(u != v and (v, u) in darts for u, v in darts)
    edges = len(darts) // 2
    faces = 0
    while darts:
        first = min(darts)
        u, v = first
        while True:
            assert (u, v) in darts
            darts.remove((u, v))
            around = rotation[v]
            u, v = v, around[(around.index(u) - 1) % len(around)]
            if (u, v) == first:
                break
        faces += 1
    assert edges == 12 + r * (m + 3)
    assert faces == 8 + 2 * r and len(graph) - edges + faces == 2
    return len(graph), edges, faces


def distances(graph, source, allowed=None):
    d = [-1] * len(graph)
    d[source] = 0
    todo = deque([source])
    while todo:
        u = todo.popleft()
        for v in graph[u]:
            if d[v] < 0 and (allowed is None or v in allowed):
                d[v] = d[u] + 1
                todo.append(v)
    return d


def components(graph, allowed):
    remaining = set(allowed)
    answer = []
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
        answer.append(part)
    return answer


def outside_route(graph, fragment, ports=None):
    start, goal = ports if ports is not None else (fragment[1], fragment[3])
    allowed = set(range(len(graph))) - set(fragment) | {start, goal}
    parent = {start: None}
    todo = deque([start])
    while todo:
        u = todo.popleft()
        if u == goal:
            route = []
            while u is not None:
                route.append(u)
                u = parent[u]
            return route[::-1]
        for v in sorted(graph[u] & allowed):
            if v not in parent:
                parent[v] = u
                todo.append(v)
    return []


def outside_length(graph, gadget):
    route = outside_route(graph, gadget)
    return len(route) - 1 if route else -1


def reduced(graph, gadget, length):
    m = len(gadget) - 1
    n = m + 1 + (length - 1 if length >= 0 else 0)
    result = [set() for _ in range(n)]

    def add(u, v):
        result[u].add(v)
        result[v].add(u)

    for u in range(m + 1):
        for v in range(u + 1, m + 1):
            if gadget[v] in graph[gadget[u]]:
                add(u, v)
    if length >= 0:
        assert length >= 2
        path = [1] + list(range(m + 1, n)) + [3]
        assert len(path) - 1 == length
        for u, v in zip(path, path[1:]):
            add(u, v)
    return result


def geodesic_masks(graph):
    masks = set()
    for source in range(len(graph)):
        d = distances(graph, source)

        def visit(u, mask):
            masks.add(mask)
            for v in graph[u]:
                if d[v] == d[u] + 1:
                    visit(v, mask | (1 << v))

        visit(source, 1 << source)
    return masks


def has_two_cover(masks, target):
    projected = {mask & target for mask in masks}
    return any((a | b) == target for a in projected for b in projected)


def audit_family(r, m=11):
    graph, rotation, gadgets = family(r, m)
    counts = check_rotation(graph, rotation, r, m)
    expected = [{4}, {5}] + [set(gadget) for gadget in gadgets]
    actual = components(graph, set(range(len(graph))) - set(range(4)))
    assert {frozenset(x) for x in actual} == {frozenset(x) for x in expected}
    for gadget in gadgets:
        assert {v for u in gadget for v in graph[u] if v not in gadget} == {0, 1}
        assert graph[gadget[1]] - set(gadget) == {0}
        assert graph[gadget[3]] - set(gadget) == {1}
        assert outside_length(graph, gadget) == 3
        for u in gadget:
            in_host = distances(graph, u)
            in_gadget = distances(graph, u, set(gadget))
            assert all(in_host[v] == in_gadget[v] for v in gadget)
    print(f"family r={r} vertices={counts[0]} edges={counts[1]} faces={counts[2]} ports=3 isometric=yes")
    return graph, gadgets


def random_subgraphs(graph, gadgets, samples=100):
    rng = Random(310031)
    edges = [(u, v) for u, row in enumerate(graph) for v in row if u < v]
    reductions = covers = isometries = routed = 0
    for trial in range(samples):
        current = [set() for _ in graph]
        retain = 0.45 + 0.5 * ((trial % 13) / 12)
        for u, v in edges:
            if rng.random() < retain:
                current[u].add(v)
                current[v].add(u)
        masks = geodesic_masks(current)
        for gadget in gadgets:
            route = outside_route(current, gadget)
            routed += bool(route)
            length = len(route) - 1 if route else -1
            model = reduced(current, gadget, length)
            embedded = gadget + route[1:-1]
            assert len(embedded) == len(model)
            for i, u in enumerate(embedded):
                host_d = distances(current, u)
                model_d = distances(model, i)
                assert all(host_d[v] == model_d[j]
                           for j, v in enumerate(embedded))
            reductions += 1
            isometries += 1
            for part in components(current, gadget):
                target = sum(1 << v for v in part)
                assert has_two_cover(masks, target)
                covers += 1
    print(f"sampled_subgraphs={samples} exact_distance_reductions={reductions} full_isometries={isometries} routed={routed} component_covers={covers} PASS")


def short_route_obstruction():
    m = 11
    gadget = list(range(m + 1))
    graph = [set() for _ in range(m + 5)]

    def add(u, v):
        graph[u].add(v)
        graph[v].add(u)

    for i in range(m):
        add(i, (i + 1) % m)
    add(0, m)
    add(1, m + 1)
    add(m + 1, 3)
    long_route = [1, m + 2, m + 3, m + 4, 3]
    for u, v in zip(long_route, long_route[1:]):
        add(u, v)
    assert outside_length(graph, gadget) == 2
    witness = [set(row) for row in graph]
    witness[1].remove(2)
    witness[2].remove(1)
    for u, v in zip(long_route, long_route[1:]):
        witness[u].remove(v)
        witness[v].remove(u)
    assert len(components(witness, gadget)) == 1
    target = sum(1 << u for u in gadget)
    assert not has_two_cover(geodesic_masks(witness), target)
    print("two_route_host shortest_exterior=2 m=11 deletion=12 two_cover=no PASS")


def exhaustive_tiny_host():
    fragment = {0, 1, 2, 3}
    edges = [(0, 2), (2, 1), (1, 3), (3, 0),
             (0, 4), (4, 1), (0, 5), (5, 6), (6, 1),
             (4, 5), (4, 6)]
    routed = 0
    for mask in range(1 << len(edges)):
        host = [set() for _ in range(7)]
        for i, (u, v) in enumerate(edges):
            if mask & (1 << i):
                host[u].add(v)
                host[v].add(u)
        route = outside_route(host, fragment, (0, 1))
        routed += bool(route)
        keep = set(fragment) | set(route)
        model = [set() for _ in host]
        for u in fragment:
            for v in host[u] & fragment:
                model[u].add(v)
        for u, v in zip(route, route[1:]):
            model[u].add(v)
            model[v].add(u)
        for u in keep:
            host_d = distances(host, u)
            model_d = distances(model, u)
            assert all(host_d[v] == model_d[v] for v in keep)
    print(f"tiny_host_spanning={1 << len(edges)} routed={routed} isometric={1 << len(edges)} PASS")


def main():
    for r in (1, 5, 8):
        audit_family(r)
    graph, gadgets = audit_family(2)
    random_subgraphs(graph, gadgets)
    short_route_obstruction()
    exhaustive_tiny_host()
    print("PASS")


if __name__ == "__main__":
    main()
