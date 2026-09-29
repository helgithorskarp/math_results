"""Exact controls for the connected-deletion representative theorem."""

from collections import deque
from itertools import combinations


def theta():
    rotation = [[2, 4, 6], [3, 7, 5], [0, 3], [2, 1],
                [0, 5], [4, 1], [0, 7], [6, 1]]
    edges = [(0, 2), (2, 3), (3, 1),
             (0, 4), (4, 5), (5, 1),
             (0, 6), (6, 7), (7, 1)]
    return rotation, edges


def face_lengths(rotation, edges):
    darts = {(u, v) for u, v in edges} | {(v, u) for u, v in edges}
    assert darts == {(u, v) for u, row in enumerate(rotation) for v in row}
    unseen = set(darts)
    result = []
    while unseen:
        first = min(unseen)
        dart = first
        length = 0
        while True:
            assert dart in unseen
            unseen.remove(dart)
            u, v = dart
            order = rotation[v]
            dart = (v, order[(order.index(u) - 1) % len(order)])
            length += 1
            if dart == first:
                break
        result.append(length)
    assert len(rotation) - len(edges) + len(result) == 2
    return sorted(result)


def rows_from_edges(n, edges):
    rows = [set() for _ in range(n)]
    for u, v in edges:
        assert u != v and v not in rows[u]
        rows[u].add(v)
        rows[v].add(u)
    return rows


def components(rows, vertices):
    unseen = set(vertices)
    result = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        comp = {root}
        todo = [root]
        while todo:
            u = todo.pop()
            for v in rows[u] & unseen:
                unseen.remove(v)
                comp.add(v)
                todo.append(v)
        result.append(comp)
    return result


def all_distances(rows):
    result = []
    for source in range(len(rows)):
        dist = [None] * len(rows)
        dist[source] = 0
        todo = deque([source])
        while todo:
            u = todo.popleft()
            for v in rows[u]:
                if dist[v] is None:
                    dist[v] = dist[u] + 1
                    todo.append(v)
        result.append(dist)
    return result


def geodesic_masks(rows, dist, component):
    masks = set()
    for source in component:
        stack = [(source, (source,))]
        while stack:
            end, path = stack.pop()
            if len(path) - 1 == dist[source][end]:
                masks.add(frozenset(path))
            for v in rows[end] & component:
                if v not in path:
                    stack.append((v, path + (v,)))
    return masks


def two_cover(rows, dist, component):
    masks = geodesic_masks(rows, dist, component)
    return any(a | b == component for a in masks for b in masks)


def audit_theta():
    rotation, edges = theta()
    assert face_lengths(rotation, edges) == [6, 6, 6]
    n, m = len(rotation), len(edges)
    assert (n, m, m - n + 1) == (8, 9, 2)
    representatives = 0
    connected_by_size = [0, 0, 0]
    checked_components = 0
    for mask in range(1 << m):
        kept = [edge for i, edge in enumerate(edges) if mask & (1 << i)]
        rows = rows_from_edges(n, kept)
        dist = all_distances(rows)
        comps = components(rows, range(n))
        for component in comps:
            checked_components += 1
            assert two_cover(rows, dist, component), (mask, component)
        if len(comps) == 1:
            deleted = m - len(kept)
            assert deleted <= 2
            connected_by_size[deleted] += 1
            representatives += 1
            assert two_cover(rows, dist, set(range(n)))
    assert representatives == 37
    assert sum(connected_by_size) == representatives
    return representatives, connected_by_size, 1 << m, checked_components


def audit_k5_boundary():
    edges = list(combinations(range(5), 2))
    intact = rows_from_edges(5, edges)
    assert not two_cover(intact, all_distances(intact), set(range(5)))
    spanning_trees = 0
    for selected in combinations(edges, 4):
        rows = rows_from_edges(5, selected)
        if len(components(rows, range(5))) != 1:
            continue
        spanning_trees += 1
        assert two_cover(rows, all_distances(rows), set(range(5)))
    assert spanning_trees == 125
    return spanning_trees


def main():
    reps, by_size, masks, comps = audit_theta()
    print(f"theta_vertices=8 edges=9 cycle_rank=2 faces=[6,6,6] "
          f"connected_representatives={reps} by_deleted_size={by_size} "
          f"all_masks={masks} checked_components={comps} PASS")
    trees = audit_k5_boundary()
    print(f"K5_maximal_representatives={trees} all_cover=YES "
          "intact_cover=NO PASS")
    print("PASS")


if __name__ == "__main__":
    main()
