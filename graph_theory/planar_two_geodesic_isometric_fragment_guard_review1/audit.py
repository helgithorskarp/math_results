#!/usr/bin/env python3
"""Independent weighted audits for the isometric-fragment guard theorem.

The graph builder, BFS, path cover, and separator routine do not import target
code. Finite samples exercise the written all-order argument, not replace it.
"""

from collections import deque
from random import Random


def make_graph(lengths):
    n = 6 + sum(lengths)
    adj = [set() for _ in range(n)]

    def edge(u, v):
        assert u != v and v not in adj[u]
        adj[u].add(v)
        adj[v].add(u)

    for u, v in ((0, 1), (1, 2), (2, 3), (3, 0)):
        edge(u, v)
    for pole in (4, 5):
        for equator in range(4):
            edge(pole, equator)
    cycles = []
    next_vertex = 6
    for m in lengths:
        assert m >= 3
        cycle = tuple(range(next_vertex, next_vertex + m))
        next_vertex += m
        for i in range(m):
            edge(cycle[i], cycle[(i + 1) % m])
        edge(0, cycle[0])
        edge(1, cycle[-1])
        cycles.append(cycle)
    assert next_vertex == n
    assert sum(map(len, adj)) // 2 == 12 + sum(m + 2 for m in lengths)
    return adj, cycles


def components(adj, deleted=()):
    unseen = set(range(len(adj))) - set(deleted)
    answer = []
    while unseen:
        start = unseen.pop()
        part = {start}
        queue = [start]
        while queue:
            new = adj[queue.pop()] & unseen
            unseen -= new
            part |= new
            queue.extend(new)
        answer.append(part)
    return answer


def shortest(adj, source, terminal):
    if source == terminal:
        return (source,)
    previous = {source: None}
    queue = deque([source])
    while queue and terminal not in previous:
        u = queue.popleft()
        for v in sorted(adj[u]):
            if v not in previous:
                previous[v] = u
                queue.append(v)
    assert terminal in previous
    path = []
    u = terminal
    while u is not None:
        path.append(u)
        u = previous[u]
    return tuple(reversed(path))


def distance(adj, source, terminal):
    return len(shortest(adj, source, terminal)) - 1


def cycle_cover(adj, cycle, part):
    if len(part) == 1:
        return [tuple(part)]
    degrees = {u: len(adj[u] & part) for u in part}
    endpoints = [u for u, degree in degrees.items() if degree == 1]
    if endpoints:
        assert len(endpoints) == 2
        order = [min(endpoints)]
        while len(order) < len(part):
            choices = (adj[order[-1]] & part) - set(order)
            assert len(choices) == 1
            order.append(choices.pop())
    else:
        assert part == set(cycle) and all(degree == 2 for degree in degrees.values())
        order = list(cycle)
    assert set(order) == part
    split = (len(order) + 1) // 2
    blocks = [tuple(order[:split]), tuple(order[split:])]
    answer = [block for block in blocks if block]
    assert all(all(v in adj[u] for u, v in zip(block, block[1:]))
               for block in answer)
    assert all(len(block) - 1 == distance(adj, block[0], block[-1])
               for block in answer)
    return answer


def separator(adj, cycles, mass):
    total = sum(mass)
    initial = components(adj)
    heavy = next((part for part in initial if 2 * sum(mass[u] for u in part) > total), None)
    if heavy is None:
        return 0
    guard = sorted({0, 1, 2, 3} & heavy)
    primary = [shortest(adj, guard[i], guard[min(i + 1, len(guard) - 1)])
               for i in range(0, len(guard), 2)]
    assert len(primary) <= 2
    removed = set().union(*map(set, primary)) if primary else set()
    residual = components(adj, removed)
    bad = next((part for part in residual if 2 * sum(mass[u] for u in part) > total), None)
    if bad is None:
        return 0
    assert bad <= heavy and not bad & set(guard)
    if bad <= {4, 5}:
        replacement = [tuple(bad)]
    else:
        cycle = next(c for c in cycles if bad <= set(c))
        replacement = cycle_cover(adj, cycle, bad)
    assert len(replacement) <= 2
    assert bad <= set().union(*map(set, replacement))
    for path in replacement:
        assert len(path) - 1 == distance(adj, path[0], path[-1])
    final_removed = set().union(*map(set, replacement))
    assert all(2 * sum(mass[u] for u in part) <= total
               for part in components(adj, final_removed))
    return 1


def main():
    rng = Random(20260928)
    families = ((7, 8, 9, 10, 11), (7, 11, 13, 17, 19),
                (3, 4, 5, 6, 7), (7,) * 6)
    instances = replacements = 0
    for lengths in families:
        graph, cycles = make_graph(lengths)
        assert {frozenset(c) for c in components(graph, {0, 1, 2, 3})} == (
            {frozenset((4,)), frozenset((5,))} |
            {frozenset(c) for c in cycles})
        assert all(len(components(graph, {v})) == 1 for v in range(len(graph)))
        for cycle in cycles:
            m = len(cycle)
            for i, u in enumerate(cycle):
                for j, v in enumerate(cycle):
                    assert distance(graph, u, v) == min(abs(i-j), m-abs(i-j))
        edge_list = [(u, v) for u, row in enumerate(graph) for v in row if u < v]
        for index in range(180):
            if index == 0:
                keep = 1.0
            else:
                keep = (0.45, 0.7, 1.0)[index % 3]
            subgraph = [set() for _ in graph]
            for u, v in edge_list:
                if rng.random() < keep:
                    subgraph[u].add(v)
                    subgraph[v].add(u)
            if index % 3 == 0:
                mass = [1] * len(graph)
                for u in cycles[index % len(cycles)]:
                    mass[u] = 20
            elif index % 3 == 1:
                mass = [rng.randrange(6) for _ in graph]
            else:
                mass = [1] * len(graph)
            replacements += separator(subgraph, cycles, mass)
            instances += 1
    assert replacements > 0
    print(f'families={len(families)} edge_subgraph_mass_instances={instances} '
          f'complete_residual_replacements={replacements}')


if __name__ == '__main__':
    main()
