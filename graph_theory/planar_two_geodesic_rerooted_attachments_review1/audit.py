#!/usr/bin/env python3
"""Independent exact checks for subset transfer and annular rerooting.

This script imports no target or earlier research modules. Its weighted
four-branch fixture has a proper interval subset, a positive outside piece
that a second geodesic can enter, a detached piece, and a zero-mass connector.
"""

from heapq import heappop, heappush
from itertools import combinations, product


def edge(graph, u, v, length):
    assert u != v and length > 0 and v not in graph[u]
    graph[u][v] = graph[v][u] = length


def distances(graph, source):
    result = [10**9] * len(graph)
    result[source] = 0
    todo = [(0, source)]
    while todo:
        cost, u = heappop(todo)
        if cost != result[u]:
            continue
        for v, length in graph[u].items():
            if cost + length < result[v]:
                result[v] = cost + length
                heappush(todo, (result[v], v))
    return result


def components(graph, deleted):
    unseen = set(range(len(graph))) - set(deleted)
    answer = []
    while unseen:
        part = {unseen.pop()}
        todo = list(part)
        while todo:
            new = set(graph[todo.pop()]) & unseen
            unseen -= new
            part |= new
            todo.extend(new)
        answer.append(part)
    return answer


def annulus(k):
    graph = [dict() for _ in range(2 * k + 1)]
    for i in range(k):
        a, b = 1 + i, 1 + (i + 1) % k
        c, d = 1 + k + i, 1 + k + (i + 1) % k
        for u, v in ((0, a), (a, b), (a, c), (a, d), (c, d)):
            if v not in graph[u]:
                edge(graph, u, v, 1)
    return graph


def core_checks():
    path_checks = subset_checks = 0
    for k in range(5, 15):
        graph = annulus(k)
        cycle = set(range(k + 1, 2 * k + 1))
        all_distances = [distances(graph, source) for source in range(len(graph))]
        for a in range(1, k + 1):
            da = all_distances[a]
            assert all(any(da[v] + all_distances[v][c] == da[c]
                           for c in cycle) for v in range(len(graph)))
            for b in range(1, k + 1):
                if a == b or b in graph[a]:
                    continue
                witnesses = [c for c in cycle & set(graph[b]) if da[c] == 3]
                assert witnesses
                path_checks += 1
        for mask in range(1 << k):
            selected = [i for i in range(k) if mask & (1 << i)]
            has_cover = any(all(i in pair or (i + 1) % k in pair for i in selected)
                            for pair in combinations(range(k), 2))
            nonadjacent_cover = any(
                all(i in pair or (i + 1) % k in pair for i in selected)
                for pair in combinations(range(k), 2)
                if (pair[1] - pair[0]) not in (1, k - 1)
            )
            assert has_cover == nonadjacent_cover
            subset_checks += 1
    return path_checks, subset_checks


BRANCHES = ((0, 2, 3, 4, 1), (0, 5, 6, 7, 1),
            (0, 8, 9, 10, 1), (0, 11, 12, 13, 1))
LENGTHS = ((1, 2, 2, 2), (2, 1, 2, 2),
           (1, 1, 3, 2), (2, 2, 1, 2))


def subset_fixture():
    graph = [dict() for _ in range(16)]
    for branch, lengths in zip(BRANCHES, LENGTHS):
        for (u, v), length in zip(zip(branch, branch[1:]), lengths):
            edge(graph, u, v, length)
    edge(graph, 6, 9, 20)
    edge(graph, 5, 14, 20)
    edge(graph, 14, 7, 20)
    edge(graph, 3, 15, 20)
    ds, dt = distances(graph, 0), distances(graph, 1)
    interval = {v for v in range(16) if ds[v] + dt[v] == ds[1]}
    support = {0, 1, 2, 3, 4, 5, 6, 7, 11, 12, 13}
    first = set(BRANCHES[0])
    assert ds[1] == 7 and interval == set(range(14)) and support < interval
    for branch in BRANCHES:
        assert sum(graph[u][v] for u, v in zip(branch, branch[1:])) == 7
    outside = components(graph, support | first)
    reduced_support = support - {3}
    assert not first <= reduced_support
    assert {frozenset(c) for c in components(graph, reduced_support | first)} == {
        frozenset(c) for c in outside}
    assert reduced_support - first == support - first
    assert {frozenset(c) for c in outside} == {
        frozenset({8, 9, 10}), frozenset({14}), frozenset({15})
    }
    boundaries = {frozenset(c): set().union(*(set(graph[u]) for u in c)) &
                  (support - first) for c in outside}
    assert boundaries == {frozenset({8, 9, 10}): {6},
                          frozenset({14}): {5, 7},
                          frozenset({15}): set()}
    checked = entered = strict_inequality = detached = 0
    for values in product((0, 1), repeat=15):
        mass = values[:14] + (0, values[14])
        total = sum(mass)
        masses = [sum(mass[u] for u in c) for c in outside]
        if any(2 * value > total for value in masses):
            continue
        proxy = [mass[u] if u in support - first else 0 for u in range(16)]
        discard = 0
        for part, value in zip(outside, masses):
            if not value:
                continue
            near = boundaries[frozenset(part)]
            assert len(near) <= 1
            if near:
                proxy[next(iter(near))] += value
            else:
                discard += value
        available = total - sum(mass[u] for u in first) - discard
        assert sum(proxy) == available
        bound_twice = max(available, 2 * max(masses))
        found = False
        for q in BRANCHES:
            residual = components(graph, first | set(q))
            if any(2 * sum(proxy[u] for u in c) > available for c in residual):
                continue
            found = True
            for part in residual:
                actual = sum(mass[u] for u in part)
                asserted = sum(proxy[u] for u in part)
                assert 2 * actual <= bound_twice and 2 * actual <= total
                if part & support:
                    assert actual <= asserted
                    strict_inequality += int(actual < asserted)
                else:
                    assert any(part <= original for original in outside)
            if q == BRANCHES[2] and mass[8] + mass[9] + mass[10] > 0:
                entered += 1
        assert found, mass
        checked += 1
        detached += int(discard > 0)
    assert checked > 10000 and entered and strict_inequality and detached, (
        checked, entered, strict_inequality, detached)
    return checked, entered, strict_inequality, detached


def main():
    path_checks, subset_checks = core_checks()
    checked, entered, strict, detached = subset_fixture()
    print(f'core_path_checks={path_checks} cycle_edge_subsets={subset_checks} '
          f'binary_assignments={checked} positive_piece_entered={entered} '
          f'strict_proxy_inequalities={strict} discarded_mass={detached}')


if __name__ == '__main__':
    main()
