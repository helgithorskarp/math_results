#!/usr/bin/env python3
"""Independent exact audit of the pentagonal-core 90-edge metric box.

Reads only the target's small JSON certificate. Rebuilds the embedding
from cyclic pentagons, checks all potential inequalities, uses Floyd
distances, and tests all four-vertex deletions.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json


CERT = (Path(__file__).resolve().parents[1]
        / "planar_two_geodesic_pentagonal_core_price_box" / "certificate.json")
CERT_SHA = "f2bb6517f68e6554bd7648a4f1e41ef5af47c5e7b7428fe3efb97b0e95ecd4c1"


def components(adjacency, removed):
    left = set(range(len(adjacency))) - set(removed)
    result = []
    while left:
        root = left.pop()
        todo = [root]
        found = {root}
        while todo:
            new = adjacency[todo.pop()] & left
            left -= new
            found |= new
            todo.extend(new)
        result.append(found)
    return sorted(result, key=lambda s: (len(s), sorted(s)))


def floyd(n, edges):
    inf = 10**9
    d = [[inf] * n for _ in range(n)]
    for u in range(n):
        d[u][u] = 0
    for (u, v), w in edges.items():
        d[u][v] = d[v][u] = w
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d


def main():
    assert sha256(CERT.read_bytes()).hexdigest() == CERT_SHA
    data = json.loads(CERT.read_text())
    pentagons = [tuple(p) for p in data["pentagons"]]
    assert len(pentagons) == 12 and all(len(p) == len(set(p)) == 5
                                        for p in pentagons)
    assert set(v for p in pentagons for v in p) == set(range(20))
    directed = Counter((p[i], p[(i + 1) % 5])
                       for p in pentagons for i in range(5))
    boundary = {tuple(sorted((u, v))) for u, v in directed}
    assert len(boundary) == 30
    assert all(directed[(u, v)] == directed[(v, u)] == 1
               for u, v in boundary)
    faces = []
    for f, p in enumerate(pentagons):
        z = 20 + f
        faces.extend((p[i], p[(i + 1) % 5], z) for i in range(5))
    assert len(faces) == 60
    incidence = Counter((face[i], face[(i + 1) % 3])
                        for face in faces for i in range(3))
    edges = {tuple(sorted((u, v))): c
             for u, v, c in data["edge_centers"]}
    assert len(edges) == 90 and len(data["edge_centers"]) == 90
    assert set(c for c in edges.values()) == {7, 8, 9, 10, 11, 13, 14}
    assert set(tuple(sorted((u, v))) for u, v in incidence) == set(edges)
    assert all(incidence[(u, v)] == incidence[(v, u)] == 1
               for u, v in edges)
    assert 32 - 90 + 60 == 2
    adjacency = [set() for _ in range(32)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    assert set(len(adjacency[v]) for v in range(20)) == {6}
    assert set(len(adjacency[v]) for v in range(20, 32)) == {5}
    for v in range(32):
        link = {u: set() for u in adjacency[v]}
        for face in faces:
            if v in face:
                u, w = (x for x in face if x != v)
                link[u].add(w)
                link[w].add(u)
        assert all(len(neighbors) == 2 for neighbors in link.values())
        seen = {next(iter(link))}
        todo = list(seen)
        while todo:
            new = link[todo.pop()] - seen
            seen |= new
            todo.extend(new)
        assert len(seen) == len(link)

    paths = [p for pair in data["pairs"] for p in pair]
    assert len(paths) == len(data["adverse_corner_potentials"]) == 6
    adverse_lengths = []
    inequalities = 0
    for path, potential in zip(paths, data["adverse_corner_potentials"]):
        assert len(path) == len(set(path))
        assert len(potential) == 32
        path_edges = {tuple(sorted(edge)) for edge in zip(path, path[1:])}
        assert len(path_edges) == len(path) - 1
        prices = {edge: center + 1 if edge in path_edges else center - 1
                  for edge, center in edges.items()}
        assert all(price >= 6 for price in prices.values())
        length = sum(prices[tuple(sorted(edge))]
                     for edge in zip(path, path[1:]))
        for (u, v), price in prices.items():
            assert abs(potential[u] - potential[v]) <= price
            inequalities += 1
        assert potential[path[-1]] - potential[path[0]] == length
        assert floyd(32, prices)[path[0]][path[-1]] == length
        adverse_lengths.append(length)
    assert inequalities == 540
    assert adverse_lengths == [40, 37, 32, 25, 41, 39]

    parts = [components(adjacency, set(pair[0]) | set(pair[1]))
             for pair in data["pairs"]]
    assert [[len(c) for c in part] for part in parts] == [
        [4, 17], [4, 19], [9, 12]]
    A, B = parts[0][1], parts[1][1]
    C, D = parts[2]
    assert not (C & A) and not (D & B)
    assert 1 not in set(v for path in paths for v in path)

    # This checks vertex connectivity >=5 independently of target code.
    checked = 0
    for removed in combinations(range(32), 4):
        assert len(components(adjacency, removed)) == 1
        checked += 1
    assert checked == 35960

    # A concrete route makes radius one exact for these six fixed paths.
    P = paths[0]
    Q = [24, 2, 1, 0, 10, 29]
    pe = {tuple(sorted(edge)) for edge in zip(P, P[1:])}
    qe = {tuple(sorted(edge)) for edge in zip(Q, Q[1:])}
    assert len(pe) == len(qe) == 5 and not (pe & qe)
    assert sum(edges[e] for e in pe) == 35
    assert sum(edges[e] for e in qe) == 45
    assert all(e in edges for e in qe)
    # At radius r, P at its adverse corner costs 35+5r,
    # while Q costs 45-5r: equality exactly at r=1.
    assert 35 + 5 == 45 - 5 and 35 + 5 * 2 > 45 - 5 * 2
    print("vertices=32 edges=90 faces=60 dimensions=90 "
          f"potential_inequalities={inequalities} adverse_lengths={adverse_lengths} "
          f"four_deletions={checked} mass_component_orders="
          f"{[[len(c) for c in part] for part in parts]} "
          "sharp_radius=1 limiting_route=24,2,1,0,10,29 PASS")


if __name__ == "__main__":
    main()
