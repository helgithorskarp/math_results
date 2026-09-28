#!/usr/bin/env python3
"""Independent Dijkstra/DAG audit for the three-port lollipop region."""

from collections import deque
from heapq import heappop, heappush

N = 11
FRAGMENT_EDGES = [(i, (i + 1) % 10) for i in range(10)] + [(0, 10)]
PORT_PAIRS = ((1, 3), (1, 5), (3, 5))
FULL = (1 << N) - 1


def fragment(mask):
    graph = [[] for _ in range(N)]
    for i, (u, v) in enumerate(FRAGMENT_EDGES):
        if mask & (1 << i):
            graph[u].append((v, 1))
            graph[v].append((u, 1))
    return graph


def components(graph):
    unseen = set(range(N))
    answer = []
    while unseen:
        start = unseen.pop()
        part = {start}
        todo = [start]
        while todo:
            u = todo.pop()
            for v, _ in graph[u]:
                if v in unseen:
                    unseen.remove(v)
                    part.add(v)
                    todo.append(v)
        answer.append(sum(1 << u for u in part))
    return answer


def weighted_model(base, lengths):
    graph = [list(row) for row in base]
    for (u, v), length in zip(PORT_PAIRS, lengths):
        if length is not None:
            graph[u].append((v, length))
            graph[v].append((u, length))
    return graph


def dijkstra(graph, source):
    dist = [10**9] * len(graph)
    dist[source] = 0
    todo = [(0, source)]
    while todo:
        length, u = heappop(todo)
        if length != dist[u]:
            continue
        for v, edge_length in graph[u]:
            new = length + edge_length
            if new < dist[v]:
                dist[v] = new
                heappush(todo, (new, v))
    return dist


def endpoint_traces(graph, target):
    traces = set()
    for source in range(N):
        if not (target & (1 << source)):
            continue
        dist = dijkstra(graph, source)

        def visit(u, mask):
            if target & (1 << u):
                traces.add(mask & target)
            for v, edge_length in graph[u]:
                if dist[u] + edge_length == dist[v]:
                    visit(v, mask | (1 << v))

        visit(source, 1 << source)
    return traces


def has_two_cover(traces, target):
    return any((a | b) == target for a in traces for b in traces)


def check_state(mask, lengths):
    base = fragment(mask)
    graph = weighted_model(base, lengths)
    for part in components(base):
        traces = endpoint_traces(graph, part)
        assert has_two_cover(traces, part), (mask, lengths, part)


def negative_unit_host():
    graph = [set() for _ in range(14)]

    def add(u, v):
        graph[u].add(v)
        graph[v].add(u)

    for i in range(10):
        if i != 2:
            add(i, (i + 1) % 10)
    add(0, 10)
    for route in ((1, 11, 3), (1, 12, 13, 5)):
        for u, v in zip(route, route[1:]):
            add(u, v)
    masks = set()
    for source in range(N):
        dist = [-1] * len(graph)
        dist[source] = 0
        todo = deque([source])
        while todo:
            u = todo.popleft()
            for v in graph[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    todo.append(v)

        def visit(u, mask):
            if u < N:
                masks.add(mask)
            for v in graph[u]:
                if dist[v] == dist[u] + 1:
                    visit(v, mask | ((1 << v) if v < N else 0))

        visit(source, 1 << source)
    best = max((a | b).bit_count() for a in masks for b in masks)
    assert best == 10 and not has_two_cover(masks, FULL)
    return best


def planar_example_audit():
    """Check the explicit 18-vertex core-and-fragment embedding."""
    rotation = [
        [1, 8, 4, 3, 5], [2, 6, 10, 0, 5], [3, 4, 1, 5],
        [0, 4, 2, 5], [0, 6, 2, 3], [0, 3, 2, 1],
        [1, 4, 12], [16, 8, 17], [7, 0, 9], [8, 10],
        [9, 1, 11], [10, 12], [11, 6, 13], [12, 14],
        [13, 15], [14, 16], [15, 7], [7],
    ]
    graph = [set(row) for row in rotation]
    assert len(graph) == 18
    assert all(u in graph[v] for u, row in enumerate(graph) for v in row)
    assert all(len(row) == len(set(row)) and u not in row
               for u, row in enumerate(rotation))
    darts = {(u, v) for u, row in enumerate(rotation) for v in row}
    assert len(darts) == 54
    unseen = darts.copy()
    faces = 0
    while unseen:
        start = min(unseen)
        dart = start
        while True:
            assert dart in unseen
            unseen.remove(dart)
            u, v = dart
            row = rotation[v]
            dart = (v, row[(row.index(u) - 1) % len(row)])
            if dart == start:
                break
        faces += 1
    assert faces == 11 and 18 - 27 + faces == 2
    fragment = set(range(7, 18))
    assert {v for u in fragment for v in graph[u] - fragment} == {0, 1, 6}
    assert {u for u in fragment if graph[u] - fragment} == {8, 10, 12}
    expected_fragment = {(7 + u, 7 + v) for u, v in FRAGMENT_EDGES}
    assert {tuple(sorted((u, v))) for u in fragment for v in graph[u] & fragment
            if u < v} == {tuple(sorted(pair)) for pair in expected_fragment}
    for source, target, expected in ((8, 10, 3), (8, 12, 4), (10, 12, 3)):
        allowed = set(range(7)) | {source, target}
        restricted = [[(v, 1) for v in row if v in allowed]
                      if u in allowed else [] for u, row in enumerate(graph)]
        dist = dijkstra(restricted, source)
        assert dist[target] == expected
    guard = {0, 1, 2, 6}
    assert fragment.isdisjoint(guard)
    unseen = set(range(len(graph))) - guard
    actual = set()
    while unseen:
        start = unseen.pop()
        part = {start}
        todo = [start]
        while todo:
            u = todo.pop()
            for v in graph[u] & unseen:
                unseen.remove(v)
                part.add(v)
                todo.append(v)
        actual.add(frozenset(part))
    assert actual == {frozenset(fragment), frozenset({3, 4, 5})}
    return faces


def main():
    boundary_profiles = ((2, 4, 2), (3, 4, 3), (10, 10, 10),
                         (None, None, None))
    for lengths in boundary_profiles:
        for mask in range(1 << len(FRAGMENT_EDGES)):
            check_state(mask, lengths)
    selected_masks = (0, 1, 511, 1023, 1535, 2041, 2043, 2045, 2046, 2047)
    profiles = 0
    for x in (*range(2, 11), None):
        for y in (*range(4, 11), None):
            for z in (*range(2, 11), None):
                profiles += 1
                for mask in selected_masks:
                    check_state(mask, (x, y, z))
    assert profiles == 800
    best = negative_unit_host()
    faces = planar_example_audit()
    print(f"full_masks={len(boundary_profiles) * (1 << len(FRAGMENT_EDGES))} "
          f"selected_masks={len(selected_masks)} profiles={profiles} "
          f"selected_states={len(selected_masks) * profiles} "
          f"negative_max_cover={best}/11 example_faces={faces} PASS")


if __name__ == "__main__":
    main()
