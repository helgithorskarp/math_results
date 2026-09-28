#!/usr/bin/env python3
"""Exact finite audits for the isometric-fragment guard proof (Python >=3.11)."""

from collections import deque


def components(rows, banned=0):
    unseen = ((1 << len(rows)) - 1) & ~banned
    out = []
    while unseen:
        start = (unseen & -unseen).bit_length() - 1
        todo = [start]
        unseen &= ~(1 << start)
        comp = {start}
        while todo:
            u = todo.pop()
            neighbors = rows[u] & unseen
            while neighbors:
                bit = neighbors & -neighbors
                v = bit.bit_length() - 1
                unseen &= ~bit
                neighbors &= ~bit
                comp.add(v)
                todo.append(v)
        out.append(comp)
    return out


def distance(rows, source):
    dist = [-1] * len(rows)
    dist[source] = 0
    todo = deque([source])
    while todo:
        u = todo.popleft()
        neighbors = rows[u]
        while neighbors:
            bit = neighbors & -neighbors
            v = bit.bit_length() - 1
            neighbors &= ~bit
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                todo.append(v)
    return dist


def audit_cycle_restrictions(m):
    """Try every H[C] edge set and every connected H[C]-vertex set D."""
    count = 0
    for edge_mask in range(1 << m):
        rows = [0] * m
        for i in range(m):
            if edge_mask >> i & 1:
                j = (i + 1) % m
                rows[i] |= 1 << j
                rows[j] |= 1 << i
        for vertex_mask in range(1, 1 << m):
            vertices = {v for v in range(m) if vertex_mask >> v & 1}
            if len(components(rows, ((1 << m) - 1) ^ vertex_mask)) != 1:
                continue
            count += 1
            degrees = {v: (rows[v] & vertex_mask).bit_count() for v in vertices}
            if len(vertices) == 1:
                order = list(vertices)
            else:
                endpoints = [v for v in vertices if degrees[v] == 1]
                if endpoints:
                    assert len(endpoints) == 2
                    start = min(endpoints)
                else:
                    assert len(vertices) == m and all(degrees[v] == 2 for v in vertices)
                    start = min(vertices)
                order = [start]
                previous = -1
                while len(order) < len(vertices):
                    u = order[-1]
                    choices = [v for v in vertices if rows[u] >> v & 1 and v != previous]
                    if previous == -1:
                        choices.sort()
                    v = choices[0]
                    assert v not in order
                    previous = u
                    order.append(v)
            assert set(order) == vertices
            split = (len(order) + 1) // 2
            for block in (order[:split], order[split:]):
                if not block:
                    continue
                assert all(rows[u] >> v & 1 for u, v in zip(block, block[1:]))
                arc_length = len(block) - 1
                if len(block) > 1:
                    delta = abs(block[0] - block[-1])
                    assert arc_length == min(delta, m - delta)
                assert arc_length <= m // 2
    return count


def family(lengths):
    # Counterclockwise neighbor orders for the octahedron.
    rotation = [[1, 4, 3, 5], [2, 4, 0, 5], [3, 4, 1, 5],
                [0, 4, 2, 5], [0, 1, 2, 3], [0, 3, 2, 1]]
    cycles = []
    for m in lengths:
        assert m >= 3
        cycle = list(range(len(rotation), len(rotation) + m))
        a, f = cycle[0], cycle[-1]
        rotation[0].insert(rotation[0].index(1) + 1, a)
        rotation[1].insert(rotation[1].index(0), f)
        for i in range(m):
            if i == 0:
                rotation.append([0, f, cycle[1]])
            elif i == m - 1:
                rotation.append([cycle[i - 1], a, 1])
            else:
                rotation.append([cycle[i - 1], cycle[i + 1]])
        cycles.append(cycle)
    rows = [sum(1 << v for v in neighbors) for neighbors in rotation]
    return rows, rotation, cycles


def audit_family(lengths):
    rows, rotation, cycles = family(lengths)
    n = len(rows)
    darts = {(u, v) for u in range(n) for v in range(n) if rows[u] >> v & 1}
    assert all(u != v and (v, u) in darts for u, v in darts)
    assert all(len(order) == len(set(order)) for order in rotation)
    unseen = darts.copy()
    faces = 0
    while unseen:
        first = min(unseen)
        dart = first
        while True:
            assert dart in unseen
            unseen.remove(dart)
            u, v = dart
            order = rotation[v]
            dart = (v, order[(order.index(u) - 1) % len(order)])
            if dart == first:
                break
        faces += 1
    edges = len(darts) // 2
    assert (n, edges, faces) == (
        6 + sum(lengths), 12 + sum(m + 2 for m in lengths), 8 + 2 * len(lengths)
    )
    assert n - edges + faces == 2  # orientable connected rotation: sphere
    assert len(components(rows)) == 1
    assert all(len(components(rows, 1 << v)) == 1 for v in range(n))
    guard = sum(1 << v for v in range(4))
    observed = {frozenset(c) for c in components(rows, guard)}
    expected = {frozenset([4]), frozenset([5])} | {frozenset(c) for c in cycles}
    assert observed == expected
    assert rows[0] >> 1 & 1 and rows[2] >> 3 & 1
    for cycle in cycles:
        m = len(cycle)
        for i, u in enumerate(cycle):
            dist = distance(rows, u)
            for j, v in enumerate(cycle):
                assert dist[v] == min(abs(i - j), m - abs(i - j))
    return n, edges, faces


def main():
    counts = [(m, audit_cycle_restrictions(m)) for m in range(3, 10)]
    print("connected restrictions by cycle order:", counts)
    for lengths in ((3,), (6,), (7,), (7, 8, 9, 10, 11),
                    (3, 7, 12, 20, 50), (7,) * 5):
        n, edges, faces = audit_family(lengths)
        print(f"lengths={lengths} vertices={n} edges={edges} faces={faces} "
              "planar=yes biconnected=yes isometric=yes")
    print("PASS")


if __name__ == "__main__":
    main()
