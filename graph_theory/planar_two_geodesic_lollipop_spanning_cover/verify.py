#!/usr/bin/env python3
"""Exact audits of the all-spanning one-ear lollipop cover rule."""

from collections import deque


def construct(m, s):
    assert m >= 5 and s >= 2
    graph = [set() for _ in range(m + s)]

    def add(u, v):
        graph[u].add(v)
        graph[v].add(u)

    for u in range(m):
        add(u, (u + 1) % m)
    add(0, m)  # t
    ear = [1] + list(range(m + 1, m + s)) + [3]
    for u, v in zip(ear, ear[1:]):
        add(u, v)
    return graph, ear


def rotation(m, s):
    last = m + s - 1
    order = [[1, m - 1, m], [0, 2, m + 1], [1, 3], [2, 4, last]]
    order.extend([[u - 1, u + 1] for u in range(4, m - 1)])
    order += [[0, m - 2], [0]]
    for u in range(m + 1, last + 1):
        order.append([1 if u == m + 1 else u - 1,
                      3 if u == last else u + 1])
    return order


def check_planarity(graph, order):
    assert len(order) == len(graph)
    assert all(len(order[u]) == len(graph[u]) and set(order[u]) == graph[u]
               for u in range(len(graph)))
    darts = {(u, v) for u, row in enumerate(graph) for v in row}
    edges = len(darts) // 2
    faces = 0
    while darts:
        start = min(darts)
        u, v = start
        while True:
            assert (u, v) in darts
            darts.remove((u, v))
            cyclic = order[v]
            u, v = v, cyclic[(cyclic.index(u) - 1) % len(cyclic)]
            if (u, v) == start:
                break
        faces += 1
    assert faces == 3 and len(graph) - edges + faces == 2
    return edges


def distances(graph, start):
    seen = [-1] * len(graph)
    seen[start] = 0
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if seen[v] < 0:
                seen[v] = seen[u] + 1
                queue.append(v)
    return seen


def geodesic_masks(graph):
    masks = set()
    for start in range(len(graph)):
        depth = distances(graph, start)

        def visit(u, mask):
            masks.add(mask)
            for v in graph[u]:
                if depth[v] == depth[u] + 1:
                    visit(v, mask | (1 << v))

        visit(start, 1 << start)
    return masks


def brute_masks(graph):
    n = len(graph)
    far = n + 1
    d = [[0 if u == v else (1 if v in graph[u] else far)
          for v in range(n)] for u in range(n)]
    for k in range(n):
        for u in range(n):
            for v in range(n):
                d[u][v] = min(d[u][v], d[u][k] + d[k][v])
    found = set()
    paths = 0
    for start in range(n):

        def visit(u, mask, length):
            nonlocal paths
            paths += 1
            if length == d[start][u]:
                found.add(mask)
            for v in graph[u]:
                if not (mask >> v & 1):
                    visit(v, mask | (1 << v), length + 1)

        visit(start, 1 << start, 0)
    return found, paths


def components(graph, m):
    remaining = set(range(m + 1))
    while remaining:
        first = remaining.pop()
        component = {first}
        todo = [first]
        while todo:
            u = todo.pop()
            for v in graph[u] & remaining:
                remaining.remove(v)
                component.add(v)
                todo.append(v)
        yield component


def has_cover(masks, target):
    projected = {mask & target for mask in masks}
    return any((left | right) == target
               for left in projected for right in projected)


def check_path(graph, path):
    assert path and len(path) == len(set(path))
    assert all(v in graph[u] for u, v in zip(path, path[1:]))
    assert len(path) - 1 == distances(graph, path[0])[path[-1]]


def delete(graph, u, v):
    result = [row.copy() for row in graph]
    result[u].remove(v)
    result[v].remove(u)
    return result


def witness_23(m, s, graph, ear):
    L = m - 3
    old = [0] + list(range(m - 1, 2, -1))
    assert len(old) == L + 1
    if s >= L - 1:
        first = [m] + old
        second = [2, 1]
    else:
        i = (s + L - 2) // 2  # ceil((s+L-3)/2)
        assert 0 <= i < L
        assert 2 * i >= s + L - 3 and 2 * i <= s + L + 1
        first = [m] + old[:i + 1]
        second = [2] + ear + list(reversed(old[i + 1:-1]))
    changed = delete(graph, 2, 3)
    check_path(changed, first)
    check_path(changed, second)
    assert set(first + second) >= set(range(m + 1))
    return changed


def witness_12(m, s, graph, ear):
    assert s >= m - 8
    L = m - 3
    old = [0] + list(range(m - 1, 2, -1))
    if s + 1 <= L:
        first = [m, 0] + ear + [2]
        second = old[1:-1]
    else:
        first = [m] + old + [2]
        second = [1]
    changed = delete(graph, 1, 2)
    check_path(changed, first)
    check_path(changed, second)
    assert set(first + second) >= set(range(m + 1))


def check_family_grid():
    cases = 0
    for m in range(5, 23):
        for s in range(2, m + 2):
            graph, ear = construct(m, s)
            assert check_planarity(graph, rotation(m, s)) == m + s + 1
            fragment = [row & set(range(m + 1)) for row in graph]
            for u in range(m + 1):
                d_full = distances(graph, u)
                d_fragment = distances(fragment, u)
                assert d_full[:m + 1] == d_fragment[:m + 1]
            changed = witness_23(m, s, graph, ear)
            if (m, s) in {(11, 2), (12, 4)}:
                other, count = brute_masks(changed)
                assert other == geodesic_masks(changed)
                print(f"independent (m,s)=({m},{s}) simple_paths={count} geodesic_masks={len(other)}")
            if s >= m - 8:
                witness_12(m, s, graph, ear)
            cases += 1
    print(f"parameter_grid={cases} planar_isometric_and_23_witnesses=PASS")


def check_all_spanning(m, s):
    graph, _ = construct(m, s)
    edges = [(u, v) for u, row in enumerate(graph) for v in row if u < v]
    assert len(edges) == m + s + 1
    checked_targets = 0
    nontrivial_states = 0
    for edge_mask in range(1 << len(edges)):
        current = [set() for _ in graph]
        for bit, (u, v) in enumerate(edges):
            if edge_mask >> bit & 1:
                current[u].add(v)
                current[v].add(u)
        targets = [sum(1 << u for u in part)
                   for part in components(current, m) if len(part) > 4]
        if not targets:
            continue  # four vertices are coverable by two geodesics by pairing
        masks = geodesic_masks(current)
        for target in targets:
            assert has_cover(masks, target), (m, s, edge_mask, target)
            checked_targets += 1
        nontrivial_states += 1
    print(f"all_spanning m={m} s={s} edges={len(edges)} states={1 << len(edges)} nontrivial={nontrivial_states} targets={checked_targets} PASS")


def check_negative():
    graph, _ = construct(11, 2)
    changed = delete(graph, 1, 2)
    target = (1 << 12) - 1
    masks = geodesic_masks(changed)
    assert not has_cover(masks, target)
    best = max(((u | v) & target).bit_count() for u in masks for v in masks)
    assert best == 11
    print("below_threshold m=11 s=2 deletion=12 covered=11/12")


def main():
    check_family_grid()
    for m, s in ((5, 2), (10, 2), (11, 3), (12, 4)):
        check_all_spanning(m, s)
    check_negative()
    print("PASS")


if __name__ == "__main__":
    main()
