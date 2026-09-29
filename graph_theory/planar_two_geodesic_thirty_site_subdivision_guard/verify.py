"""Exact verification of a 30-site mass guard in planar unit subdivisions.

Python 3.11+ and standard library only. The all-real-mass step is proved in
README.md; this checks its finite graph and metric premises.
"""

import hashlib
import json
from collections import Counter
from heapq import heappop, heappush
from pathlib import Path


HERE = Path(__file__).resolve().parent
CLAIM = json.loads((HERE / "certificate.json").read_text())
PARENT_FILE = HERE.parent / "planar_two_geodesic_sparse_subdivision_probe" / "certificate.json"
PARENT_BYTES = PARENT_FILE.read_bytes()
assert hashlib.sha256(PARENT_BYTES).hexdigest() == CLAIM["parent_certificate_sha256"]
PARENT = json.loads(PARENT_BYTES)


def faces_and_planarity():
    faces = []
    for i in range(5):
        u, v = 1 + i, 1 + (i + 1) % 5
        a, b = 6 + i, 6 + (i + 1) % 5
        faces += [(0, u, v), (v, u, a), (v, a, b), (11, b, a)]
    faces = sorted(set(tuple(sorted(f)) for f in faces))
    assert len(faces) == 20
    core_edges = {frozenset((u, v)) for u, v, _ in PARENT["core_edges"]}
    incidences = Counter(frozenset((f[i], f[(i + 1) % 3]))
                         for f in faces for i in range(3))
    assert len(core_edges) == 30 and set(incidences) == core_edges
    assert all(value == 2 for value in incidences.values())
    assert 12 - 30 + 20 == 2
    for center in range(12):
        link = {}
        for face in faces:
            if center not in face:
                continue
            a, b = [v for v in face if v != center]
            link.setdefault(a, set()).add(b)
            link.setdefault(b, set()).add(a)
        assert all(len(neighbors) == 2 for neighbors in link.values())
        seen, queue = set(), [next(iter(link))]
        for v in queue:
            if v in seen:
                continue
            seen.add(v)
            queue.extend(link[v] - seen)
        assert len(seen) == len(link)
    return faces


def graph():
    faces = faces_and_planarity()
    edges = [tuple(item) for item in PARENT["core_edges"]]
    for f, face in enumerate(faces):
        for u in face:
            length = (PARENT["parent_length"] if u == PARENT["parents"][f]
                      else PARENT["nonparent_length"])
            edges.append((12 + f, u, length))
    assert len(edges) == 90 and all(L > 0 for _, _, L in edges)
    marked = sorted(int(site) - 32 for site in PARENT["mass_atoms"] if int(site) >= 32)
    assert len(marked) == 16 and all(0 <= j < 90 for j in marked)
    midpoint = {j: 32 + rank for rank, j in enumerate(marked)}
    adj = [dict() for _ in range(48)]
    for j, (u, v, L) in enumerate(edges):
        if j in midpoint:
            z = midpoint[j]
            sections = [(u, z, L // 2), (z, v, L - L // 2)]
        else:
            sections = [(u, v, L)]
        for a, b, length in sections:
            assert length > 0 and b not in adj[a]
            adj[a][b] = adj[b][a] = length
    assert sum(map(len, adj)) // 2 == 106
    edge_sum = sum(L for _, _, L in edges)
    assert edge_sum == 1151853
    assert 32 + edge_sum - 90 == 1151795
    assert 32 + 2 * edge_sum - 90 == 2303648
    return adj, midpoint, edge_sum


def distance(adj, source, target):
    d = [10**30] * len(adj)
    d[source] = 0
    queue = [(0, source)]
    while queue:
        value, u = heappop(queue)
        if value != d[u]:
            continue
        if u == target:
            return value
        for v, length in adj[u].items():
            if value + length < d[v]:
                d[v] = value + length
                heappush(queue, (d[v], v))
    raise AssertionError("disconnected")


def components_after_paths(adj, paths):
    deleted = set().union(*(set(path) for path in paths))
    seen = set(deleted)
    components = []
    for start in range(len(adj)):
        if start in seen:
            continue
        queue = [start]
        seen.add(start)
        for u in queue:
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    queue.append(v)
        components.append(set(queue))
    return components


def main():
    adj, midpoint, edge_sum = graph()
    support = set(CLAIM["support"])
    assert len(support) == 30 and support <= set(range(48))
    old_support = {int(v) if int(v) < 32 else midpoint[int(v) - 32]
                   for v in PARENT["mass_atoms"]}
    assert len(old_support) == 17 and old_support <= support
    paths = CLAIM["guard_paths"]
    lengths = []
    for path in paths:
        assert len(set(path)) == len(path)
        length = sum(adj[u][v] for u, v in zip(path, path[1:]))
        assert length == distance(adj, path[0], path[-1])
        lengths.append(length)
    assert lengths == [1772, 1784]
    components = components_after_paths(adj, paths)
    cells = sorted(tuple(sorted(component & support)) for component in components)
    expected = sorted(tuple(cell) for cell in [
        (0, 1, 32, 37), (25, 38), (28, 41, 42, 43),
        (30, 44, 45), (31, 46, 47), (33,), (34,), (35,), (36,), (40,),
    ])
    assert cells == expected
    assert max(map(len, cells)) == 4
    print("core_vertices=32 core_edges=90 compressed_vertices=48 compressed_edges=106")
    print("unit_vertices_k1=1151795 unit_vertices_k2=2303648")
    print("marked_sites=30 old_sites_contained=17 path_lengths=1772,1784")
    print("residual_site_counts=" + ",".join(map(str, sorted(map(len, cells), reverse=True))))
    print("PASS")


if __name__ == "__main__":
    main()
