#!/usr/bin/env python3
"""Independent exact audit of light-attachment mass transfer on a plane theta fixture.

No routines or data are imported from the research checker. The four internally
disjoint 0--1 branches have length six. Attachments sit in consecutive branch
faces; the last one has two surviving support neighbors but has zero mass.
"""

from heapq import heappop, heappush
from itertools import product


N = 15
BRANCHES = ((0, 2, 3, 1), (0, 4, 5, 1), (0, 6, 7, 1), (0, 8, 9, 1))
LENGTHS = ((1, 2, 3), (2, 1, 3), (1, 3, 2), (2, 2, 2))
P = frozenset(BRANCHES[0])


def graph():
    adj = [dict() for _ in range(N)]

    def edge(u, v, weight):
        assert u != v and v not in adj[u] and weight > 0
        adj[u][v] = adj[v][u] = weight

    for branch, lengths in zip(BRANCHES, LENGTHS):
        for (u, v), length in zip(zip(branch, branch[1:]), lengths):
            edge(u, v, length)
    edge(2, 10, 20)
    edge(10, 4, 20)
    edge(6, 11, 20)
    edge(11, 12, 1)
    edge(3, 13, 20)
    edge(5, 14, 20)
    edge(14, 7, 20)
    return adj


def distances(adj, source):
    result = [10**9] * len(adj)
    result[source] = 0
    queue = [(0, source)]
    while queue:
        length, u = heappop(queue)
        if length != result[u]:
            continue
        for v, edge_length in adj[u].items():
            candidate = length + edge_length
            if candidate < result[v]:
                result[v] = candidate
                heappush(queue, (candidate, v))
    return result


def components(adj, deleted):
    unseen = set(range(len(adj))) - set(deleted)
    result = []
    while unseen:
        component = {unseen.pop()}
        frontier = list(component)
        while frontier:
            u = frontier.pop()
            new = set(adj[u]) & unseen
            unseen.difference_update(new)
            component.update(new)
            frontier.extend(new)
        result.append(component)
    return result


def main():
    adj = graph()
    ds, dt = distances(adj, 0), distances(adj, 1)
    assert ds[1] == 6
    support = {v for v in range(N) if ds[v] + dt[v] == 6}
    assert support == set(range(10))
    for branch in BRANCHES:
        assert sum(adj[u][v] for u, v in zip(branch, branch[1:])) == ds[1]
    outside = components(adj, support)
    assert {frozenset(c) for c in outside} == {
        frozenset({10}), frozenset({11, 12}), frozenset({13}), frozenset({14})
    }
    survivors = support - P
    assert {
        frozenset(c): set().union(*(set(adj[u]) for u in c)) & survivors
        for c in outside
    } == {
        frozenset({10}): {4}, frozenset({11, 12}): {6},
        frozenset({13}): set(), frozenset({14}): {5, 7}
    }

    checked = positive_attachment = discarded = zero_connector = 0
    # Every binary mass assignment on 14 vertices; vertex 14 is always zero.
    for values in product((0, 1), repeat=N - 1):
        mass = values + (0,)
        total = sum(mass)
        part_masses = [sum(mass[u] for u in c) for c in outside]
        if any(2 * value > total for value in part_masses):
            continue
        proxy = [mass[u] if u in survivors else 0 for u in range(N)]
        gone = 0
        for part, part_mass in zip(outside, part_masses):
            if not part_mass:
                continue
            boundary = set().union(*(set(adj[u]) for u in part)) & survivors
            assert len(boundary) <= 1
            if boundary:
                proxy[next(iter(boundary))] += part_mass
            else:
                gone += part_mass
        available = total - sum(mass[u] for u in P) - gone
        assert sum(proxy) == available
        bound_twice = max(available, 2 * max(part_masses))
        found = False
        for q in BRANCHES:
            residual = components(adj, P | set(q))
            if all(2 * sum(proxy[u] for u in c) <= available for c in residual):
                assert all(2 * sum(mass[u] for u in c) <= bound_twice for c in residual)
                assert all(2 * sum(mass[u] for u in c) <= total for c in residual)
                for c in residual:
                    if c & support:
                        assert sum(proxy[u] for u in c) == sum(mass[u] for u in c)
                found = True
                break
        assert found, mass
        checked += 1
        positive_attachment += int(mass[10] + mass[11] + mass[12] > 0)
        discarded += int(gone > 0)
        zero_connector += int(mass[14] == 0)
    assert checked > 10000 and positive_attachment and discarded
    print(f'vertices={N} support={len(support)} prescribed_paths={len(BRANCHES)} '
          f'binary_assignments={checked} positive_attachment={positive_attachment} '
          f'discarded_mass={discarded} zero_connector={zero_connector}')


if __name__ == '__main__':
    main()
