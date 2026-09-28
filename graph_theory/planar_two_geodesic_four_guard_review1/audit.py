"""Independent finite audit of the octahedral ear family.

Run from repository root with Python 3.11+. No target imports.
The all-order weighted statement is proved in the written argument.
"""

from collections import deque


def family(ears):
    assert ears >= 0
    n = 6 + 5 * ears
    adj = [set() for _ in range(n)]
    def add(u, v):
        assert u != v
        adj[u].add(v)
        adj[v].add(u)
    for i in range(4):
        add(i, (i + 1) % 4)
        add(i, 4)
        add(i, 5)
    for j in range(ears):
        path = [0] + list(range(6 + 5 * j, 11 + 5 * j)) + [1]
        for u, v in zip(path, path[1:]):
            add(u, v)
    edges = sum(map(len, adj)) // 2
    assert edges == 12 + 6 * ears
    return tuple(frozenset(row) for row in adj)


def components(adj, removed=()):
    unseen = set(range(len(adj))) - set(removed)
    out = []
    while unseen:
        start = unseen.pop()
        part = {start}
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u] & unseen:
                unseen.remove(v)
                part.add(v)
                queue.append(v)
        out.append(part)
    return out


def distances(adj, source):
    d = {source: 0}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in d:
                d[v] = d[u] + 1
                queue.append(v)
    return d


def shortest_path(adj, start, end):
    d = distances(adj, start)
    assert end in d
    path = [end]
    while path[-1] != start:
        path.append(min(v for v in adj[path[-1]]
                        if d[v] == d[path[-1]] - 1))
    return tuple(reversed(path))


def separator_for_masses(adj, masses):
    # Follow the proof's two-stage construction, but recompute every path
    # and component in the current graph.
    total = sum(masses)
    heavy = [part for part in components(adj)
             if 2 * sum(masses[v] for v in part) > total]
    if not heavy:
        return ()
    assert len(heavy) == 1
    guard = sorted(set(range(4)) & heavy[0])
    primary = [shortest_path(adj, guard[i], guard[i + 1])
               for i in range(0, len(guard) - 1, 2)]
    if len(guard) % 2:
        primary.append((guard[-1],))
    assert len(primary) <= 2
    removed = set().union(*(set(path) for path in primary)) if primary else set()
    residual = components(adj, removed)
    heavy_residual = [part for part in residual
                      if 2 * sum(masses[v] for v in part) > total]
    if not heavy_residual:
        return primary
    assert len(heavy_residual) == 1
    part = heavy_residual[0]
    assert len(part) <= 5
    if len(part) == 5:
        triple = next(((u, mid, v) for mid in part for u in adj[mid] & part
                       for v in adj[mid] & part
                       if u < v and v not in adj[u]), None)
        assert triple is not None
        paths = [triple]
        remaining = sorted(part - set(triple))
    else:
        paths = []
        remaining = sorted(part)
    for i in range(0, len(remaining) - 1, 2):
        paths.append(shortest_path(adj, remaining[i], remaining[i + 1]))
    if len(remaining) % 2:
        paths.append((remaining[-1],))
    assert len(paths) <= 2
    for path in paths:
        assert len(path) - 1 == distances(adj, path[0])[path[-1]]
    assert part <= set().union(*(set(path) for path in paths))
    return paths


def check(ears):
    adj = family(ears)
    assert len(components(adj)) == 1
    assert all(len(components(adj, (v,))) == 1 for v in range(len(adj)))
    guard_parts = components(adj, (0, 1, 2, 3))
    assert sorted(map(len, guard_parts)) == [1, 1] + [5] * ears
    assert all(any(v not in adj[u] for u in part for v in part if u < v)
               for part in guard_parts if len(part) == 5)
    # Deterministic edge deletions and masses exercise both stages.
    sampled = 0
    edges = [(u, v) for u, row in enumerate(adj) for v in row if u < v]
    for seed in range(36):
        child = [set(row) for row in adj]
        for i, (u, v) in enumerate(edges):
            if (17 * i + 13 * seed) % 11 < 3:
                child[u].discard(v)
                child[v].discard(u)
        child = tuple(frozenset(row) for row in child)
        masses = [((7 * v + 11 * seed) % 13) for v in range(len(adj))]
        paths = separator_for_masses(child, masses)
        assert len(paths) <= 2
        removed = set().union(*(set(path) for path in paths)) if paths else set()
        assert all(2 * sum(masses[v] for v in part) <= sum(masses)
                   for part in components(child, removed))
        sampled += 1
    return len(adj), len(edges), 8 + ears, len(guard_parts), sampled


def main():
    assert all(len(family(0)[v]) == 4 for v in range(6))
    for ears in (1, 2, 3, 4, 8, 12):
        n, edges, faces, fragments, sampled = check(ears)
        print(f'ears={ears} vertices={n} edges={edges} '
              f'faces_by_insertion={faces} fragments={fragments} '
              f'sampled_subgraphs={sampled}')


if __name__ == '__main__':
    main()
