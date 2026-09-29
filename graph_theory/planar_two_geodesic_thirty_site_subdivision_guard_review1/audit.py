#!/usr/bin/env python3
"""Independent exact audit of the 30-site subdivision guard.

Only the two small public JSON certificates are inputs. The script
enumerates core triangles, reconstructs 48 retained sites, computes
Floyd distances, and checks the full residual partition.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "planar_two_geodesic_sparse_subdivision_probe" / "certificate.json"
NEW = ROOT / "planar_two_geodesic_thirty_site_subdivision_guard" / "certificate.json"
OLD_SHA = "5e1d780366f885723c6cd9323e3a8a88deb515025d66d356f15bc57ed5dff634"
NEW_SHA = "19b49189d7ef8cbed8f62b618b1b831e35c0c90c9a47ee1ea89db4d00383f505"


def floyd(adjacency):
    n = len(adjacency)
    inf = 10**15
    d = [[inf] * n for _ in range(n)]
    for u, row in enumerate(adjacency):
        d[u][u] = 0
        for v, w in row.items():
            d[u][v] = w
    for k in range(n):
        for u in range(n):
            for v in range(n):
                if d[u][k] + d[k][v] < d[u][v]:
                    d[u][v] = d[u][k] + d[k][v]
    return d


def components(adjacency, removed):
    unseen = set(range(len(adjacency))) - set(removed)
    found = []
    while unseen:
        start = unseen.pop()
        todo = [start]
        part = {start}
        while todo:
            v = todo.pop()
            new = adjacency[v].keys() & unseen
            unseen -= new
            part |= new
            todo.extend(new)
        found.append(part)
    return sorted(found, key=lambda c: (-len(c), min(c)))


def main():
    assert sha256(OLD.read_bytes()).hexdigest() == OLD_SHA
    assert sha256(NEW.read_bytes()).hexdigest() == NEW_SHA
    old, new = json.loads(OLD.read_text()), json.loads(NEW.read_text())
    assert new["parent_certificate_sha256"] == OLD_SHA
    core = {tuple(sorted((u, v))): w for u, v, w in old["core_edges"]}
    assert len(core) == 30
    faces = [f for f in combinations(range(12), 3)
             if all(tuple(sorted(e)) in core for e in combinations(f, 2))]
    assert len(faces) == 20
    incidence = Counter(tuple(sorted(e)) for f in faces
                        for e in combinations(f, 2))
    assert set(incidence) == set(core) and set(incidence.values()) == {2}
    for v in range(12):
        link = {u: set() for f in faces if v in f for u in f if u != v}
        for f in faces:
            if v in f:
                u, w = (a for a in f if a != v)
                link[u].add(w)
                link[w].add(u)
        assert all(len(neighbors) == 2 for neighbors in link.values())
        seen = {next(iter(link))}
        todo = list(seen)
        while todo:
            fresh = link[todo.pop()] - seen
            seen |= fresh
            todo.extend(fresh)
        assert len(seen) == len(link)

    edges = [tuple(row) for row in old["core_edges"]]
    assert len(old["parents"]) == len(faces)
    for f, face in enumerate(faces):
        parent = old["parents"][f]
        assert parent in face
        for v in face:
            edges.append((12 + f, v, old["parent_length"]
                          if v == parent else old["nonparent_length"]))
    assert len(edges) == len({frozenset((u, v)) for u, v, _ in edges}) == 90
    edge_sum = sum(w for _, _, w in edges)
    assert edge_sum == 1151853
    marked = sorted(int(v) - 32 for v in old["mass_atoms"] if int(v) >= 32)
    assert len(marked) == 16 and all(0 <= e < 90 for e in marked)
    labels = {e: 32 + i for i, e in enumerate(marked)}
    adjacency = [dict() for _ in range(48)]

    def put(u, v, w):
        assert w > 0 and v not in adjacency[u]
        adjacency[u][v] = w
        adjacency[v][u] = w

    for j, (u, v, w) in enumerate(edges):
        if j in labels:
            z = labels[j]
            put(u, z, w // 2)
            put(z, v, w - w // 2)
        else:
            put(u, v, w)
    assert sum(map(len, adjacency)) // 2 == 106
    assert 32 + edge_sum - 90 == 1151795
    assert 32 + 2 * edge_sum - 90 == 2303648

    X = set(new["support"])
    assert len(X) == 30 and X <= set(range(48))
    old_sites = {int(v) if int(v) < 32 else labels[int(v) - 32]
                 for v in old["mass_atoms"]}
    assert len(old_sites) == 17 and old_sites <= X
    P, Q = new["guard_paths"]
    assert len(set(P)) == len(P) and len(set(Q)) == len(Q)
    d = floyd(adjacency)
    lengths = []
    for path in (P, Q):
        L = sum(adjacency[u][v] for u, v in zip(path, path[1:]))
        assert L == d[path[0]][path[-1]]
        lengths.append(L)
    assert lengths == [1772, 1784]

    gone = set(P) | set(Q)
    assert len(gone) == 9 and gone <= X
    parts = components(adjacency, gone)
    assert [len(C) for C in parts] == [22, 4, 3, 3, 2, 1, 1, 1, 1, 1]
    cells = {frozenset(C & X) for C in parts}
    expected = [
        {0, 1, 32, 37}, {25, 38}, {28, 41, 42, 43},
        {30, 44, 45}, {31, 46, 47},
        {33}, {34}, {35}, {36}, {40},
    ]
    assert cells == {frozenset(C) for C in expected}
    assert max(map(len, cells)) == 4
    assert sum(map(len, cells)) + len(gone) == len(X)
    # For this fixed P,Q, no support obeying the four-site guard can
    # include more than all removed sites plus min(4,|C|) in each cell.
    max_support = len(gone) + sum(min(4, len(C)) for C in parts)
    assert max_support == len(X) == 30
    assert X == gone | set().union(*(C & X for C in parts))
    print("core_faces=20 compressed_vertices=48 compressed_edges=106 "
          "unit_vertices=1151795 guard_lengths=1772,1784 "
          "full_component_sizes=22,4,3,3,2,1,1,1,1,1 "
          "residual_site_max=4 old_sites=17 fixed_guard_max_sites=30 PASS")


if __name__ == "__main__":
    main()
