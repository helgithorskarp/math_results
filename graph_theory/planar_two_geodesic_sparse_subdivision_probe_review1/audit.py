#!/usr/bin/env python3
"""Independent exact audit on the mass-support compression of a unit subdivision.

Reads only the published compact JSON data. Uses triangle enumeration and
Floyd--Warshall, rather than the target checker’s face formula and Dijkstra.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json


CERT = (Path(__file__).resolve().parents[1]
        / "planar_two_geodesic_sparse_subdivision_probe" / "certificate.json")
CERT_SHA = "5e1d780366f885723c6cd9323e3a8a88deb515025d66d356f15bc57ed5dff634"


def distances(adjacency):
    n = len(adjacency)
    inf = 10**15
    d = [[inf] * n for _ in range(n)]
    for u in range(n):
        d[u][u] = 0
        for v, w in adjacency[u].items():
            d[u][v] = w
    for m in range(n):
        for u in range(n):
            for v in range(n):
                via = d[u][m] + d[m][v]
                if via < d[u][v]:
                    d[u][v] = via
    assert all(d[u][v] == d[v][u] < inf for u in range(n) for v in range(n))
    return d


def residual_masses(adjacency, mass, paths):
    removed = set().union(*(set(p) for p in paths))
    unseen = set(range(len(adjacency))) - removed
    out = []
    while unseen:
        start = unseen.pop()
        todo = [start]
        weight = mass[start]
        while todo:
            u = todo.pop()
            reached = adjacency[u].keys() & unseen
            unseen -= reached
            todo.extend(reached)
            weight += sum(mass[v] for v in reached)
        if weight:
            out.append(weight)
    return sorted(out, reverse=True)


def main():
    assert sha256(CERT.read_bytes()).hexdigest() == CERT_SHA
    data = json.loads(CERT.read_text())
    core = {(min(u, v), max(u, v)): w
            for u, v, w in data["core_edges"]}
    assert len(core) == 30 and all(w > 0 for w in core.values())
    assert len(data["core_edges"]) == 30

    # The icosahedron has exactly 20 three-cliques; reconstruct its faces
    # without using the target checker's indexed-ring face formula.
    faces = [triple for triple in combinations(range(12), 3)
             if all(tuple(sorted(edge)) in core
                    for edge in combinations(triple, 2))]
    assert len(faces) == 20
    incidence = Counter(tuple(sorted(edge))
                        for face in faces for edge in combinations(face, 2))
    assert set(incidence) == set(core)
    assert set(incidence.values()) == {2}
    for u in range(12):
        link = {v: set() for face in faces if u in face
                for v in face if v != u}
        for face in faces:
            if u in face:
                v, w = (x for x in face if x != u)
                link[v].add(w)
                link[w].add(v)
        assert all(len(neighbors) == 2 for neighbors in link.values())
        seen = {next(iter(link))}
        todo = list(seen)
        while todo:
            for v in link[todo.pop()] - seen:
                seen.add(v)
                todo.append(v)
        assert len(seen) == len(link)

    edges = [(u, v, w) for u, v, w in data["core_edges"]]
    assert len(data["parents"]) == len(faces)
    for f, face in enumerate(faces):
        parent = data["parents"][f]
        assert parent in face
        for u in face:
            w = data["parent_length"] if u == parent else data["nonparent_length"]
            edges.append((12 + f, u, w))
    assert len(edges) == len({frozenset((u, v)) for u, v, _ in edges}) == 90
    assert all(w > 1 for _, _, w in edges)
    order = 32 + sum(w - 1 for _, _, w in edges)
    assert order == 1151795

    raw_mass = {int(v): w for v, w in data["mass_atoms"].items()}
    assert len(raw_mass) == 17 and all(w > 0 for w in raw_mass.values())
    marks = sorted(v - 32 for v in raw_mass if v >= 32)
    assert len(marks) == 16 and all(0 <= j < 90 for j in marks)
    mark_vertex = {j: 32 + i for i, j in enumerate(marks)}
    n = 32 + len(marks)
    adjacency = [dict() for _ in range(n)]

    def put(u, v, w):
        assert u != v and w > 0 and v not in adjacency[u]
        adjacency[u][v] = w
        adjacency[v][u] = w

    for j, (u, v, w) in enumerate(edges):
        if j in mark_vertex:
            m = mark_vertex[j]
            put(u, m, w // 2)
            put(m, v, w - w // 2)
        else:
            put(u, v, w)
    assert sum(map(len, adjacency)) // 2 == 90 + 16
    mass = [0] * n
    for v, w in raw_mass.items():
        mass[v if v < 32 else mark_vertex[v - 32]] = w
    assert sum(mass) == 29 and sum(sorted(mass, reverse=True)[:4]) == 8

    d = distances(adjacency)
    edge_index = {frozenset((u, v)): j for j, (u, v, _) in enumerate(edges)}

    def expand(path):
        out = [path[0]]
        for u, v in zip(path, path[1:]):
            j = edge_index[frozenset((u, v))]
            if j in mark_vertex:
                out.append(mark_vertex[j])
            out.append(v)
        return out

    def check_path(path):
        assert len(path) == len(set(path))
        length = sum(adjacency[u][v] for u, v in zip(path, path[1:]))
        assert length == d[path[0]][path[-1]]
        return length

    menu = []
    for pair in data["positive_pairs"]:
        paths = [expand(path) for path in pair]
        for path in paths:
            check_path(path)
        menu.append(residual_masses(adjacency, mass, paths)[0])
    assert menu == [21, 26, 23, 25, 25, 26, 26, 26,
                    21, 28, 28, 28, 21, 21, 21]
    assert all(2 * value > sum(mass) for value in menu)

    def decode(label):
        return label if label < 32 else mark_vertex[label - 32]

    rescue = [[decode(v) for v in path] for path in data["rescue_pair"]]
    rescue_lengths = [check_path(path) for path in rescue]
    residual = residual_masses(adjacency, mass, rescue)
    assert residual == [14, 2] and 2 * residual[0] < sum(mass)

    # Scaling every original edge length by k, and every marked position
    # by k, exactly scales this compressed metric. Hence every k>=1
    # preserves all geodesic and residual-mass certificates.
    edge_sum = sum(w for _, _, w in edges)
    assert edge_sum == 1151853
    assert 2 * edge_sum - 58 == 2303648
    print(f"unit_vertices={order} compressed_vertices={n} "
          f"faces={len(faces)} support={len(raw_mass)} mass={sum(mass)} "
          f"top_four=8 menu_min={min(menu)} rescue={residual} "
          f"rescue_lengths={rescue_lengths} scaled_k2_vertices=2303648 PASS")


if __name__ == "__main__":
    main()
