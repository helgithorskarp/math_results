"""Exact independent controls for the edge-window path-cover theorem."""

from collections import deque
from fractions import Fraction
from itertools import combinations


def strict_example():
    # Path 0..8, with ears 0-x-5 and 2-y-8 on opposite sides.
    path_order = list(range(9))
    edges = [(i, i + 1) for i in range(8)] + [(0, 9), (9, 5), (2, 10), (10, 8)]
    rotation = {
        0: [1, 9], 1: [0, 2], 2: [1, 10, 3], 3: [2, 4],
        4: [3, 5], 5: [4, 6, 9], 6: [5, 7], 7: [6, 8],
        8: [7, 10], 9: [0, 5], 10: [2, 8],
    }
    return path_order, edges, rotation


def distant_ears():
    # Path 0..9, with ears 0-x-3 and 6-y-9.
    path_order = list(range(10))
    edges = [(i, i + 1) for i in range(9)] + [(0, 10), (10, 3), (6, 11), (11, 9)]
    return path_order, edges


def distances(n, edges):
    adjacency = [[] for _ in range(n)]
    for a, b in edges:
        adjacency[a].append(b)
        adjacency[b].append(a)
    result = []
    for source in range(n):
        row = [None] * n
        row[source] = 0
        todo = deque([source])
        while todo:
            a = todo.popleft()
            for b in adjacency[a]:
                if row[b] is None:
                    row[b] = row[a] + 1
                    todo.append(b)
        result.append(row)
    return result


def windows(path_order, edges, dist):
    path_edges = {frozenset((a, b)) for a, b in zip(path_order, path_order[1:])}
    ports = set()
    path_vertices = set(path_order)
    for a, b in edges:
        if frozenset((a, b)) in path_edges:
            continue
        if a in path_vertices:
            ports.add(a)
        if b in path_vertices:
            ports.add(b)
    result = {}
    for a, b in combinations(sorted(ports), 2):
        if dist[a][b] is not None and dist[a][b] < b - a:
            delta = dist[a][b]
            result[(a, b)] = (Fraction(a + b - delta, 2), Fraction(a + b + delta, 2))
    return ports, result


def covering_edges(path_order, win):
    return [k for k in path_order[:-1] if all(k <= upper and k + 1 >= lower for lower, upper in win.values())]


def path_components(path_order, edges):
    edge_set = {frozenset(e) for e in edges}
    components = []
    start = 0
    for k in range(len(path_order) - 1):
        if frozenset((path_order[k], path_order[k + 1])) not in edge_set:
            components.append(path_order[start:k + 1])
            start = k + 1
    components.append(path_order[start:])
    return components


def all_geodesic_interval_pairs_cover(component, dist):
    # Enumerates every internal geodesic interval and every pair, including
    # overlaps; this does not assume an endpoint-anchored split.
    intervals = []
    target = set(component)
    for i in range(len(component)):
        for j in range(i, len(component)):
            if dist[component[i]][component[j]] == j - i:
                intervals.append(frozenset(component[i:j + 1]))
    if any(x == target for x in intervals):
        return True
    return any(a | b == target for a, b in combinations(intervals, 2))


def facial_lengths(rotation, edges):
    darts = {(a, b) for a, b in edges} | {(b, a) for a, b in edges}
    assert set(rotation) == set().union(*(set(e) for e in edges))
    assert all(set(rotation[v]) == {b for a, b in darts if a == v} for v in rotation)
    faces = []
    unseen = set(darts)
    while unseen:
        start = min(unseen)
        dart = start
        size = 0
        while True:
            assert dart in unseen
            unseen.remove(dart)
            a, b = dart
            neighbors = rotation[b]
            dart = (b, neighbors[(neighbors.index(a) - 1) % len(neighbors)])
            size += 1
            if dart == start:
                break
        faces.append(size)
    return sorted(faces)


def main():
    path, edges, rotation = strict_example()
    assert len(path) + 2 == 11 and len(edges) == 12
    faces = facial_lengths(rotation, edges)
    assert len(faces) == len(edges) - 11 + 2 == 3 and sum(faces) == 2 * len(edges)
    full_dist = distances(11, edges)
    ports, win = windows(path, edges, full_dist)
    assert ports == {0, 2, 5, 8}
    assert win == {
        (0, 5): (Fraction(3, 2), Fraction(7, 2)),
        (0, 8): (Fraction(2), Fraction(6)),
        (2, 8): (Fraction(4), Fraction(6)),
    }
    assert max(left for left, _ in win.values()) > min(right for _, right in win.values())
    assert covering_edges(path, win) == [3]

    checked_components = 0
    for mask in range(1 << len(edges)):
        surviving = [edge for i, edge in enumerate(edges) if mask & (1 << i)]
        dist = distances(11, surviving)
        for component in path_components(path, surviving):
            checked_components += 1
            assert all_geodesic_interval_pairs_cover(component, dist), (mask, component)
            if frozenset((3, 4)) not in {frozenset(e) for e in surviving}:
                assert dist[component[0]][component[-1]] == len(component) - 1

    path2, edges2 = distant_ears()
    dist2 = distances(12, edges2)
    ports2, win2 = windows(path2, edges2, dist2)
    assert ports2 == {0, 3, 6, 9}
    assert not covering_edges(path2, win2)
    assert not all_geodesic_interval_pairs_cover(path2, dist2)
    print(f"strict_planar_faces={faces} active_windows={win} edge_cut=3-4")
    print(f"spanning_subgraphs={1 << len(edges)} checked_components={checked_components} PASS")
    print(f"distant_ear_windows={win2} internal_pair_cover=NO PASS")
    print("PASS")


if __name__ == "__main__":
    main()
