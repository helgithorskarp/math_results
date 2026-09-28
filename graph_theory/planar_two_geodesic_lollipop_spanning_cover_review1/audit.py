#!/usr/bin/env python3
"""Independent exact finite audit of the one-ear all-spanning cover theorem.

No target code is imported.  Unlike the target's shortest-path-DAG enumerator,
this checker lists every simple path and filters it by separately computed
BFS distances.  The infinite classification still needs the written proof.
"""

from collections import deque
from random import Random


def family(m, s):
    assert m >= 5 and s >= 2
    cycle = tuple(f"v{i}" for i in range(m))
    tail = "tail"
    ear = (cycle[1],) + tuple(f"ear{i}" for i in range(1, s)) + (cycle[3],)
    edges = {frozenset((cycle[i], cycle[(i + 1) % m])) for i in range(m)}
    edges.add(frozenset((cycle[0], tail)))
    edges.update(frozenset((u, v)) for u, v in zip(ear, ear[1:]))
    vertices = tuple(sorted(set(cycle) | {tail} | set(ear)))
    assert len(edges) == m + s + 1 and len(vertices) == m + s
    return vertices, tuple(sorted((tuple(sorted(e)) for e in edges))), set(cycle) | {tail}, ear


def adjacency(vertices, edges):
    graph = {u: set() for u in vertices}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
    return graph


def distance(graph, source):
    out = {source: 0}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in out:
                out[v] = out[u] + 1
                queue.append(v)
    return out


def geodesic_masks(graph, index):
    """Exhaustive simple-path search, including all choices of endpoints."""
    masks = set()
    for source in graph:
        dist = distance(graph, source)
        stack = [(source, 1 << index[source], 0)]
        while stack:
            u, mask, steps = stack.pop()
            if steps == dist[u]:
                masks.add(mask)
            for v in graph[u]:
                if not mask >> index[v] & 1:
                    stack.append((v, mask | (1 << index[v]), steps + 1))
    return masks


def target_components(graph, fragment):
    unseen = set(fragment)
    while unseen:
        first = unseen.pop()
        todo = [first]
        piece = {first}
        while todo:
            for v in graph[todo.pop()] & unseen:
                unseen.remove(v)
                todo.append(v)
                piece.add(v)
        yield piece


def max_cover(masks, target):
    projected = {mask & target for mask in masks}
    return max(((p | q).bit_count() for p in projected for q in projected), default=0)


def path_is_shortest(graph, path):
    assert len(path) == len(set(path))
    assert all(v in graph[u] for u, v in zip(path, path[1:]))
    assert len(path) - 1 == distance(graph, path[0])[path[-1]]


def delete(graph, pair):
    out = {u: neighbors.copy() for u, neighbors in graph.items()}
    u, v = pair
    out[u].remove(v)
    out[v].remove(u)
    return out


def check_23_witness(m, s, graph, ear):
    long = ("v0",) + tuple(f"v{i}" for i in range(m - 1, 2, -1))
    L = m - 3
    assert len(long) == L + 1
    if s >= L - 1:
        first = ("tail",) + long
        second = ("v2", "v1")
    else:
        i = (s + L - 2) // 2
        first = ("tail",) + long[:i + 1]
        second = ("v2",) + ear + tuple(reversed(long[i + 1:-1]))
    changed = delete(graph, ("v2", "v3"))
    path_is_shortest(changed, first)
    path_is_shortest(changed, second)
    assert set(first + second) >= {f"v{j}" for j in range(m)} | {"tail"}
    # If 12 is also deleted, vertex 2 becomes isolated.  Trim that endpoint;
    # the surviving subpath is still shortest after a further deletion.
    changed_again = delete(changed, ("v1", "v2"))
    path_is_shortest(changed_again, first)
    path_is_shortest(changed_again, second[1:])
    assert set(first + second[1:]) >= ({f"v{j}" for j in range(m)} | {"tail"}) - {"v2"}


def check_tail_deleted_witness(m, graph):
    """New case: after deleting 12 and 0-tail, full old arc and ear remain."""
    long = ("v0",) + tuple(f"v{i}" for i in range(m - 1, 2, -1))
    L = m - 3
    i = (L - 1) // 2
    first = ("v1",) + long[:i + 1]
    second = ("v2",) + tuple(reversed(long[i + 1:]))
    changed = delete(delete(graph, ("v1", "v2")), ("v0", "tail"))
    path_is_shortest(changed, first)
    path_is_shortest(changed, second)
    assert set(first + second) >= {f"v{j}" for j in range(m)}


def threshold_grid():
    instances = failures = 0
    for m in range(5, 19):
        for s in range(2, m + 1):
            vertices, edges, fragment, ear = family(m, s)
            full = adjacency(vertices, edges)
            inner = adjacency(tuple(fragment), (e for e in edges if set(e) <= fragment))
            assert all(distance(full, u)[v] == distance(inner, u)[v]
                       for u in fragment for v in fragment)
            check_23_witness(m, s, full, ear)
            check_tail_deleted_witness(m, full)
            changed = delete(full, ("v1", "v2"))
            index = {v: i for i, v in enumerate(vertices)}
            target = sum(1 << index[v] for v in fragment)
            best = max_cover(geodesic_masks(changed, index), target)
            expected = m + 1 if s >= m - 8 else m
            assert best == expected, (m, s, best, expected)
            instances += 1
            failures += best == m
    return instances, failures


def spanning_grid(m, s, sample=None):
    vertices, edges, fragment, _ = family(m, s)
    index = {v: i for i, v in enumerate(vertices)}
    states = range(1 << len(edges))
    if sample is not None:
        rng = Random(2026092817 + m)
        states = sorted({0, (1 << len(edges)) - 1} |
                        {rng.randrange(1 << len(edges)) for _ in range(sample)})
    examined = targets = 0
    for bits in states:
        present = [e for j, e in enumerate(edges) if bits >> j & 1]
        graph = adjacency(vertices, present)
        pieces = [sum(1 << index[v] for v in D)
                  for D in target_components(graph, fragment) if len(D) > 4]
        if not pieces:
            continue
        masks = geodesic_masks(graph, index)
        for target in pieces:
            assert max_cover(masks, target) == target.bit_count(), (m, s, bits, target)
            targets += 1
        examined += 1
    return len(states), examined, targets


def classify_below_threshold(m, s):
    assert 2 <= s < m - 8
    vertices, edges, fragment, _ = family(m, s)
    index = {v: i for i, v in enumerate(vertices)}
    expected = sum((1 << j) for j, edge in enumerate(edges)
                   if set(edge) != {"v1", "v2"})
    failures = []
    for bits in range(1 << len(edges)):
        graph = adjacency(vertices, (edge for j, edge in enumerate(edges) if bits >> j & 1))
        pieces = [sum(1 << index[v] for v in D)
                  for D in target_components(graph, fragment) if len(D) > 4]
        if not pieces:
            continue
        masks = geodesic_masks(graph, index)
        if any(max_cover(masks, target) < target.bit_count() for target in pieces):
            failures.append(bits)
    assert failures == [expected], (m, s, failures, expected)
    return 1 << len(edges)


def main():
    instances, failures = threshold_grid()
    print(f"threshold_instances={instances} below_threshold={failures} PASS")
    for m, s, sample in ((5, 2, None), (10, 2, None), (11, 3, None), (12, 4, None)):
        states, examined, targets = spanning_grid(m, s, sample)
        print(f"spanning m={m} s={s} states={states} nontrivial={examined} targets={targets} PASS")
    for m, s in ((11, 2), (12, 2), (12, 3)):
        states = classify_below_threshold(m, s)
        print(f"below_threshold m={m} s={s} states={states} failing_subgraphs=1 PASS")
    print("PASS")


if __name__ == "__main__":
    main()
