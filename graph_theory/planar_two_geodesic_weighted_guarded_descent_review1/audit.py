"""Independent finite audit of the weighted guarded descent example.

Run from repository root with Python 3.11+:
python3 graph_theory/planar_two_geodesic_weighted_guarded_descent_review1/audit.py
"""

from collections import deque
from functools import cache
from itertools import combinations


# Published 16-vertex adjacency certificate, copied as input data only.
ROWS = (656, 2052, 2058, 2052, 33, 4176, 8352, 321,
        9856, 1281, 13056, 49166, 9248, 5440, 34816, 18432)
ROT = ((4, 9, 7), (2, 11), (1, 3, 11), (2, 11), (0, 5),
       (4, 6, 12), (5, 7, 13), (6, 0, 8), (7, 9, 10, 13),
       (8, 0, 10), (9, 12, 13, 8), (3, 1, 2, 14, 15),
       (10, 5, 13), (12, 6, 8, 10), (11, 15), (14, 11))
ADJ = tuple(frozenset(j for j in range(16) if row >> j & 1)
            for row in ROWS)
CORE = frozenset((0, 4, 5, 6, 7, 8, 9, 10, 12, 13))
OTHER = frozenset(range(16)) - CORE
PRIMARY = ((1,), (4, 0, 7, 8))
SECONDARY = (((2, 11, 14), (3, 11, 15)),
             ((5, 12), (6, 13, 10, 9)))


def parts(vertices, adj=ADJ):
    unseen = set(vertices)
    output = []
    while unseen:
        start = unseen.pop()
        component = {start}
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u] & unseen:
                unseen.remove(v)
                component.add(v)
                queue.append(v)
        output.append(frozenset(component))
    return output


def distances(start):
    d = {start: 0}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in ADJ[u]:
            if v not in d:
                d[v] = d[u] + 1
                queue.append(v)
    return d


DIST = tuple(distances(s) for s in range(16))


def check_path(path):
    assert all(b in ADJ[a] for a, b in zip(path, path[1:]))
    assert DIST[path[0]][path[-1]] == len(path) - 1


def geodesic_masks():
    masks = {frozenset((v,)) for v in range(16)}
    # Enumerate all simple walks up to the endpoint distance. A walk is
    # admitted only at its endpoint, using an independently computed BFS.
    for s in range(16):
        for t in range(s + 1, 16):
            if t not in DIST[s]:
                continue
            limit = DIST[s][t]
            stack = [(s, (s,))]
            while stack:
                u, path = stack.pop()
                if u == t:
                    if len(path) - 1 == limit:
                        masks.add(frozenset(path))
                    continue
                if len(path) - 1 >= limit:
                    continue
                for v in ADJ[u] - set(path):
                    stack.append((v, path + (v,)))
    return masks


def planar_rotation_check():
    assert all(set(ROT[v]) == ADJ[v] for v in range(16))
    assert all(u in ADJ[v] for u in range(16) for v in ADJ[u])
    result = []
    for component in parts(range(16)):
        darts = {(u, v) for u in component for v in ADJ[u]}
        unseen = darts.copy()
        faces = 0
        while unseen:
            first = next(iter(unseen))
            dart = first
            while True:
                assert dart in unseen
                unseen.remove(dart)
                u, v = dart
                cyclic = ROT[v]
                dart = (v, cyclic[(cyclic.index(u) + 1) % len(cyclic)])
                if dart == first:
                    break
            faces += 1
        e = len(darts) // 2
        assert len(component) - e + faces == 2
        result.append((len(component), e, faces))
    return sorted(result)


def tw_at_most_three(vertices, adj):
    vertices = tuple(sorted(vertices))
    initial = tuple(tuple(sorted(adj[v] & set(vertices))) for v in vertices)

    @cache
    def solve(live, neighborhoods):
        if not live:
            return True
        live_set = set(live)
        for i, v in enumerate(live):
            neighbors = set(neighborhoods[i]) & live_set
            if len(neighbors) > 3:
                continue
            next_live = live[:i] + live[i + 1:]
            next_adj = []
            for j, u in enumerate(live):
                if u == v:
                    continue
                row = (set(neighborhoods[j]) - {v}) & set(next_live)
                if u in neighbors:
                    row |= neighbors - {u}
                next_adj.append(tuple(sorted(row)))
            if solve(next_live, tuple(next_adj)):
                return True
        return False

    return solve(vertices, initial)


def main():
    assert all(u not in ADJ[u] for u in range(16))
    assert not any(all(v in ADJ[u] for u, v in combinations(five, 2))
                   for five in combinations(range(16), 5))
    embedding = planar_rotation_check()
    assert embedding == [(6, 8, 4), (10, 16, 8)]
    paths = geodesic_masks()
    unions = {p | q for p in paths for q in paths}
    minimum = min(max((len(c) for c in parts(set(range(16)) - pair)),
                      default=0) for pair in unions)
    assert (len(paths), len(unions), minimum) == (102, 2521, 6)

    for path in PRIMARY + SECONDARY[0] + SECONDARY[1]:
        check_path(path)
    removed = set().union(*(set(p) for p in PRIMARY))
    residual = parts(set(range(16)) - removed)
    assert set(residual) == {
        frozenset((2, 3, 11, 14, 15)),
        frozenset((5, 6, 9, 10, 12, 13))}
    for comp, pair in zip(sorted(residual, key=len), SECONDARY):
        assert comp <= set(pair[0]) | set(pair[1])

    protected = {frozenset((u, v)) for path in
                 PRIMARY + SECONDARY[0] + SECONDARY[1]
                 for u, v in zip(path, path[1:])}
    assert len(protected) == 11
    core_witness = ((4, 0, 9, 10), (7, 6, 13, 12))
    for path in core_witness:
        check_path(path)
    assert all(len(c) == 1 for c in parts(
        CORE - set().union(*(set(p) for p in core_witness))))
    assert not tw_at_most_three(CORE, ADJ)
    core_edges = [frozenset((u, v)) for u in CORE for v in ADJ[u] & CORE
                  if u < v]
    assert len(core_edges) == 16
    for edge in core_edges:
        child = tuple(ADJ[u] - (edge - {u}) if u in edge else ADJ[u]
                      for u in range(16))
        assert tw_at_most_three(CORE, child), edge
    assert tw_at_most_three(OTHER, ADJ)
    print('embedding=', embedding)
    print('geodesic_masks=', len(paths), 'pair_unions=', len(unions),
          'minimum_largest_residual=', minimum)
    print('guarded_residuals=', sorted(map(len, residual)),
          'protected_edges=', len(protected))
    print('core_treewidth_gt_3=True deletion_children_tw_le_3=',
          len(core_edges), 'other_tw_le_3=True')


if __name__ == '__main__':
    main()
