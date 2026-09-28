"""Independent exact audit of the prescribed-first-path interval statement.

Run: python3 graph_theory/planar_two_geodesic_interval_sweep_review1/audit.py
No imports from the theorem author's checker and no third-party packages.
"""

from collections import deque
from random import Random


def fixture(n):
    # In each unit square draw its northwest-to-southeast diagonal.  Put a
    # zero-mass vertex in the triangle with top and right sides, joined to
    # its three corners by length-5 edges.  This is a plane graph.
    cells = n * n
    edges = []
    def v(i, j):
        return i * n + j
    for i in range(n):
        for j in range(n):
            if i + 1 < n:
                edges.append((v(i, j), v(i + 1, j), 1))
            if j + 1 < n:
                edges.append((v(i, j), v(i, j + 1), 1))
            if i + 1 < n and j + 1 < n:
                edges.append((v(i, j), v(i + 1, j + 1), 2))
                k = cells + i * (n - 1) + j
                for corner in (v(i, j), v(i, j + 1), v(i + 1, j + 1)):
                    edges.append((k, corner, 5))
    return cells + (n - 1) ** 2, edges


def distances(size, edges, source):
    # Unit and integer-length Dijkstra, deliberately distinct from the
    # author's Floyd-Warshall implementation.
    import heapq
    adj = [[] for _ in range(size)]
    for u, v, length in edges:
        adj[u].append((v, length))
        adj[v].append((u, length))
    dist = [10**9] * size
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue
        for v, length in adj[u]:
            if d + length < dist[v]:
                dist[v] = d + length
                heapq.heappush(heap, (d + length, v))
    return dist, adj


def geodesics(size, edges, s, t):
    ds, adj = distances(size, edges, s)
    dt, _ = distances(size, edges, t)
    limit = ds[t]
    forward = [[] for _ in range(size)]
    for u in range(size):
        for v, length in adj[u]:
            if ds[u] + length == ds[v] and ds[v] + dt[v] == limit:
                forward[u].append(v)
    paths = []
    def walk(u, path):
        if u == t:
            paths.append(tuple(path))
            return
        for v in forward[u]:
            walk(v, path + [v])
    walk(s, [s])
    return paths, ds, dt, adj


def residual_masks(adj, removed):
    unseen = set(range(len(adj))) - removed
    masks = []
    while unseen:
        start = unseen.pop()
        found = {start}
        queue = deque([start])
        while queue:
            for v, _ in adj[queue.popleft()]:
                if v in unseen:
                    unseen.remove(v)
                    found.add(v)
                    queue.append(v)
        masks.append(sum(1 << v for v in found))
    return masks


def check(n, assignments):
    size, edges = fixture(n)
    s, t = 0, n * n - 1
    paths, ds, dt, adj = geodesics(size, edges, s, t)
    assert all(ds[v] + dt[v] == ds[t] for v in range(n * n))
    assert all(ds[v] + dt[v] > ds[t] for v in range(n * n, size))
    path_masks = [sum(1 << v for v in path) for path in paths]
    pair_components = [
        [residual_masks(adj, set(p) | set(q)) for q in paths]
        for p in paths
    ]
    checked = 0
    for masses in assignments:
        assert len(masses) == size and all(x >= 0 for x in masses)
        assert all(x == 0 for x in masses[n * n:])
        total = sum(masses)
        for i, p_mask in enumerate(path_masks):
            outside_p = total - sum(m for v, m in enumerate(masses)
                                    if p_mask >> v & 1)
            good = False
            for components in pair_components[i]:
                if all(2 * sum(m for v, m in enumerate(masses)
                               if component >> v & 1) <= outside_p
                       for component in components):
                    good = True
                    break
            assert good, (n, i, masses)
            checked += 1
    return len(paths), len(assignments), checked


def assignments(n):
    core = n * n
    padding = (n - 1) ** 2
    if n == 3:
        for bits in range(1 << core):
            yield tuple((bits >> v) & 1 for v in range(core)) + (0,) * padding
    else:
        rng = Random(20260928)
        yield (1,) * core + (0,) * padding
        for v in range(core):
            yield tuple(int(u == v) for u in range(core)) + (0,) * padding
        for _ in range(128):
            yield tuple(rng.randrange(8) for _ in range(core)) + (0,) * padding


def main():
    for n in (3, 4):
        paths, masses, checks = check(n, list(assignments(n)))
        print(f"n={n} geodesics={paths} mass_assignments={masses} "
              f"prescribed_path_checks={checks}")


if __name__ == "__main__":
    main()
