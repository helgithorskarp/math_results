"""Exact finite checks for cactus deletion representatives."""

from collections import deque
from fractions import Fraction
from itertools import combinations, product


def hub_cycle(m, ports):
    hub = m
    rotation = []
    for i in range(m):
        previous, following = (i - 1) % m, (i + 1) % m
        rotation.append([previous, following, hub] if i in ports else [previous, following])
    rotation.append(list(ports))
    edges = [(i, (i + 1) % m) for i in range(m)] + [(hub, p) for p in ports]
    return rotation, edges, set(range(m))


def two_squares():
    rotation = [[1, 3, 4, 6], [0, 2], [1, 3], [2, 0],
                [0, 5], [4, 6], [5, 0]]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0),
             (0, 4), (4, 5), (5, 6), (6, 0)]
    cycles = [edges[:4], edges[4:]]
    return rotation, edges, set(range(7)), cycles


def facial_lengths(rotation, edges):
    darts = {(a, b) for a, b in edges} | {(b, a) for a, b in edges}
    assert {(u, v) for u, row in enumerate(rotation) for v in row} == darts
    unseen = set(darts)
    lengths = []
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
        lengths.append(length)
    assert len(rotation) - len(edges) + len(lengths) == 2
    return sorted(lengths)


def graph(n, edges):
    rows = [set() for _ in range(n)]
    for a, b in edges:
        assert a != b and b not in rows[a]
        rows[a].add(b)
        rows[b].add(a)
    return rows


def distances(rows):
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


def geodesic_masks(rows, dist, component):
    # Enumerate every simple internal path; retain precisely those that
    # achieve the full ambient endpoint distance.
    masks = set()
    for source in component:
        stack = [(source, (source,))]
        while stack:
            end, path = stack.pop()
            if dist[source][end] == len(path) - 1:
                masks.add(frozenset(path))
            for next_vertex in rows[end] & component:
                if next_vertex not in path:
                    stack.append((next_vertex, path + (next_vertex,)))
    return masks


def cover_component(rows, dist, component):
    masks = geodesic_masks(rows, dist, component)
    return any(a | b == component for a in masks for b in masks)


def all_spanning_audit(n, edges, fragment):
    checked_components = 0
    for mask in range(1 << len(edges)):
        selected = [edge for i, edge in enumerate(edges) if mask & (1 << i)]
        rows = graph(n, selected)
        internal = [row & fragment if u in fragment else set()
                    for u, row in enumerate(rows)]
        dist = distances(rows)
        for component in components(internal, fragment):
            checked_components += 1
            assert cover_component(internal, dist, component), (mask, component)
    return 1 << len(edges), checked_components


def windows_after_cycle_edge(m, ports, edges, removed):
    kept = [edge for edge in edges
            if frozenset(edge) != frozenset((removed, (removed + 1) % m))]
    dist = distances(graph(m + 1, kept))
    order = [(removed + 1 + i) % m for i in range(m)]
    position = {v: i for i, v in enumerate(order)}
    active = {}
    for a, b in combinations(sorted(ports, key=position.get), 2):
        i, j = position[a], position[b]
        delta = dist[a][b]
        if delta < j - i:
            active[(a, b)] = (Fraction(i + j - delta, 2),
                              Fraction(i + j + delta, 2))
    cuts = [(order[k], order[k + 1]) for k in range(m - 1)
            if all(k <= upper and k + 1 >= lower
                   for lower, upper in active.values())]
    internal = graph(m + 1, kept)
    internal = [row & set(range(m)) if u < m else set()
                for u, row in enumerate(internal)]
    assert len(components(internal, range(m))) == 1
    return kept, active, cuts, cover_component(internal, dist, set(range(m)))


def audit_positive_cycle():
    m, ports = 8, (0, 2, 4)
    rotation, edges, fragment = hub_cycle(m, ports)
    assert facial_lengths(rotation, edges) == [4, 4, 6, 8]
    dist = distances(graph(m + 1, edges))
    assert dist[0][4] == 2 < 4
    internal = graph(m + 1, edges)
    internal = [row & fragment if u in fragment else set()
                for u, row in enumerate(internal)]
    assert cover_component(internal, dist, fragment)
    cuts = []
    for e in range(m):
        _, active, possible, direct = windows_after_cycle_edge(m, ports, edges, e)
        assert possible and direct
        cuts.append((e, possible[0], len(active)))
    masks, components_checked = all_spanning_audit(m + 1, edges, fragment)
    return masks, components_checked, cuts


def audit_two_squares():
    rotation, edges, fragment, cycles = two_squares()
    assert facial_lengths(rotation, edges) == [4, 4, 8]
    representatives = 0
    for choice in product(*[[None] + cycle for cycle in cycles]):
        removed = {frozenset(edge) for edge in choice if edge is not None}
        selected = [edge for edge in edges if frozenset(edge) not in removed]
        rows = graph(7, selected)
        assert len(components(rows, fragment)) == 1
        assert cover_component(rows, distances(rows), fragment)
        representatives += 1
    assert representatives == 25
    masks, components_checked = all_spanning_audit(7, edges, fragment)
    return representatives, masks, components_checked


def audit_negative_cycle():
    m, ports = 10, (0, 3, 8)
    rotation, edges, fragment = hub_cycle(m, ports)
    assert facial_lengths(rotation, edges) == [4, 5, 7, 10]
    rows = graph(m + 1, edges)
    internal = [row & fragment if u in fragment else set()
                for u, row in enumerate(rows)]
    assert cover_component(internal, distances(rows), fragment)
    _, active, cuts, direct = windows_after_cycle_edge(m, ports, edges, 9)
    assert not cuts and not direct
    return active


def main():
    masks, checked, cuts = audit_positive_cycle()
    print(f"three_port_cycle masks={masks} components={checked} "
          f"representative_cuts={cuts} PASS")
    reps, masks2, checked2 = audit_two_squares()
    print(f"two_cycle_cactus representatives={reps} masks={masks2} "
          f"components={checked2} PASS")
    active = audit_negative_cycle()
    print(f"negative_star active_after_edge_9_0={active} "
          "intact_cover=YES deleted_cover=NO PASS")
    print("PASS")


if __name__ == "__main__":
    main()
