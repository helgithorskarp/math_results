#!/usr/bin/env python3
"""Independent exact checks for the all-vertex two-port substitution theorem.

The finite checks use a cross-linked exterior network different from the
target fixture.  They do not replace the all-order isometry argument.
"""

from collections import deque


def graph(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def floyd(adj):
    n = len(adj)
    far = float("inf")
    d = [[0 if u == v else (1 if v in adj[u] else far) for v in range(n)]
         for u in range(n)]
    for k in range(n):
        for u in range(n):
            for v in range(n):
                d[u][v] = min(d[u][v], d[u][k] + d[k][v])
    return d


def shortest_exterior(adj, fragment, a, b):
    allowed = set(range(len(adj))) - set(fragment) | {a, b}
    parent = {a: None}
    queue = deque([a])
    while queue:
        u = queue.popleft()
        if u == b:
            path = [u]
            while parent[u] is not None:
                u = parent[u]
                path.append(u)
            return tuple(reversed(path))
        for v in adj[u] & allowed:
            if v not in parent:
                parent[v] = u
                queue.append(v)
    return ()


def exterior_paths(adj, fragment, a, b):
    allowed = set(range(len(adj))) - set(fragment) | {a, b}
    paths = []
    stack = [(a, (a,), {a})]
    while stack:
        u, path, seen = stack.pop()
        if u == b:
            paths.append(path)
            continue
        for v in adj[u] & allowed - seen:
            stack.append((v, path + (v,), seen | {v}))
    return paths


def test_isometry():
    fragment = set(range(5))
    core_edges = [(0, 1), (1, 2), (2, 3), (3, 4), (1, 3)]
    exterior_edges = [(0, 5), (5, 4), (0, 6), (6, 7), (7, 4), (5, 6), (5, 7)]
    edges = core_edges + exterior_edges
    assert len(edges) == 12
    routed = no_route = comparisons = 0
    route_lengths = set()
    for mask in range(1 << len(edges)):
        H = graph(8, (edge for i, edge in enumerate(edges) if mask >> i & 1))
        path = shortest_exterior(H, fragment, 0, 4)
        kept_edges = [edge for edge in core_edges if edge[1] in H[edge[0]]]
        kept_edges.extend(zip(path, path[1:]))
        J = graph(8, kept_edges)
        keep = fragment | set(path)
        dH, dJ = floyd(H), floyd(J)
        assert all(dH[u][v] == dJ[u][v] for u in keep for v in keep), mask
        comparisons += len(keep) ** 2
        routed += bool(path)
        no_route += not path
        if path:
            route_lengths.add(len(path) - 1)
    full = graph(8, edges)
    routes = exterior_paths(full, fragment, 0, 4)
    lengths = sorted({len(path) - 1 for path in routes})
    assert lengths == [2, 3, 4]
    assert route_lengths == {2, 3, 4}
    return edges, routes, routed, no_route, comparisons


def test_converse_embedding(edges, routes):
    core = edges[:5]
    one = {}
    for path in routes:
        one.setdefault(len(path) - 1, path)
    embeddings = 0
    for s, path in sorted(one.items()):
        # The model uses fresh vertices 5,...,s+3; the host uses path vertices.
        model_ear = (0,) + tuple(range(5, s + 4)) + (4,)
        assert len(model_ear) == len(path)
        model_edges = core + list(zip(model_ear, model_ear[1:]))
        mapping = {u: u for u in range(5)}
        mapping.update(zip(model_ear[1:-1], path[1:-1]))
        for mask in range(1 << len(model_edges)):
            model = graph(s + 4, (edge for i, edge in enumerate(model_edges) if mask >> i & 1))
            host = graph(8, ((mapping[u], mapping[v]) for i, (u, v) in enumerate(model_edges)
                             if mask >> i & 1))
            dm, dh = floyd(model), floyd(host)
            assert all(dm[u][v] == dh[mapping[u]][mapping[v]]
                       for u in mapping for v in mapping)
            embeddings += 1
    # Also delete every exterior edge: F_infinity embeds in the host.
    for mask in range(1 << len(core)):
        model = graph(5, (edge for i, edge in enumerate(core) if mask >> i & 1))
        host = graph(8, (edge for i, edge in enumerate(core) if mask >> i & 1))
        dm, dh = floyd(model), floyd(host)
        assert all(dm[u][v] == dh[u][v] for u in range(5) for v in range(5))
        embeddings += 1
    return embeddings


def simple_geodesic_masks(adj):
    n = len(adj)
    d = floyd(adj)
    masks = set()
    for source in range(n):
        stack = [(source, 1 << source, 0)]
        while stack:
            u, mask, length = stack.pop()
            if length == d[source][u]:
                masks.add(mask)
            for v in adj[u]:
                if not mask >> v & 1:
                    stack.append((v, mask | (1 << v), length + 1))
    return masks


def test_short_route():
    m = 11
    edges = [(i, (i + 1) % m) for i in range(m)] + [(0, 11)]
    edges += [(1, 12), (12, 3)]
    edges += [(1, 13), (13, 14), (14, 15), (15, 3)]
    full = graph(16, edges)
    assert len(shortest_exterior(full, set(range(12)), 1, 3)) - 1 == 2
    H = graph(16, (edge for edge in edges
                   if set(edge) != {1, 2} and edge not in
                   [(1, 13), (13, 14), (14, 15), (15, 3)]))
    target = (1 << 12) - 1
    masks = simple_geodesic_masks(H)
    projected = {mask & target for mask in masks}
    best = max((a | b).bit_count() for a in projected for b in projected)
    assert best == 11 and target.bit_count() == 12
    return best


def main():
    edges, routes, routed, no_route, comparisons = test_isometry()
    embeddings = test_converse_embedding(edges, routes)
    best = test_short_route()
    print(f"crosslinked_host_subgraphs={1 << len(edges)} routed={routed} "
          f"no_route={no_route} all_vertex_distance_comparisons={comparisons} PASS")
    print(f"converse_model_embeddings={embeddings} exterior_lengths=2,3,4 PASS")
    print(f"short_route_m11_target_coverage={best}/12 PASS")
    print("PASS")


if __name__ == "__main__":
    main()
