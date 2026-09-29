"""Separate triangle-enumeration and Floyd audit of the 30-site guard.

Uses published JSON only; imports no code from verify.py. Python 3.11+.
"""

import json
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
CLAIM = json.loads((HERE / "certificate.json").read_text())
SOURCE = HERE.parent / "planar_two_geodesic_sparse_subdivision_probe" / "certificate.json"
assert sha256(SOURCE.read_bytes()).hexdigest() == CLAIM["parent_certificate_sha256"]
DATA = json.loads(SOURCE.read_text())


def main():
    core = {frozenset((a, b)): length for a, b, length in DATA["core_edges"]}
    assert len(core) == 30
    faces = [face for face in combinations(range(12), 3)
             if all(frozenset(edge) in core for edge in combinations(face, 2))]
    assert len(faces) == 20
    incidence = Counter(frozenset(edge) for face in faces
                        for edge in combinations(face, 2))
    assert set(incidence) == set(core) and set(incidence.values()) == {2}
    for vertex in range(12):
        link = {}
        for face in faces:
            if vertex in face:
                x, y = (z for z in face if z != vertex)
                link.setdefault(x, set()).add(y)
                link.setdefault(y, set()).add(x)
        assert all(len(nbr) == 2 for nbr in link.values())
        reached = {next(iter(link))}
        frontier = list(reached)
        while frontier:
            for x in link[frontier.pop()] - reached:
                reached.add(x)
                frontier.append(x)
        assert len(reached) == len(link)
    assert 12 - 30 + len(faces) == 2

    edges = [tuple(item) for item in DATA["core_edges"]]
    for number, face in enumerate(faces):
        parent = DATA["parents"][number]
        assert parent in face
        for vertex in face:
            weight = (DATA["parent_length"] if vertex == parent
                      else DATA["nonparent_length"])
            edges.append((12 + number, vertex, weight))
    assert len(edges) == 90
    assert 32 + sum(weight - 1 for _, _, weight in edges) == 1151795
    marked = sorted(int(label) - 32 for label in DATA["mass_atoms"]
                    if int(label) >= 32)
    mark = {edge: 32 + rank for rank, edge in enumerate(marked)}
    assert len(mark) == 16
    n = 48
    adjacency = [dict() for _ in range(n)]
    for edge, (a, b, weight) in enumerate(edges):
        pieces = ([(a, mark[edge], weight // 2),
                   (mark[edge], b, weight - weight // 2)]
                  if edge in mark else [(a, b, weight)])
        for u, v, length in pieces:
            assert length > 0 and v not in adjacency[u]
            adjacency[u][v] = adjacency[v][u] = length
    assert sum(map(len, adjacency)) // 2 == 106

    infinity = 10**30
    d = [[infinity] * n for _ in range(n)]
    for u, row in enumerate(adjacency):
        d[u][u] = 0
        for v, length in row.items():
            d[u][v] = length
    for middle in range(n):
        for u in range(n):
            via = d[u][middle]
            for v in range(n):
                if via + d[middle][v] < d[u][v]:
                    d[u][v] = via + d[middle][v]

    paths = CLAIM["guard_paths"]
    lengths = []
    for path in paths:
        assert len(path) == len(set(path))
        length = sum(adjacency[u][v] for u, v in zip(path, path[1:]))
        assert length == d[path[0]][path[-1]]
        lengths.append(length)
    assert lengths == [1772, 1784]
    support = set(CLAIM["support"])
    assert len(support) == 30
    old = {int(v) if int(v) < 32 else mark[int(v) - 32]
           for v in DATA["mass_atoms"]}
    assert len(old) == 17 and old <= support
    unseen = set(range(n)) - set(paths[0]) - set(paths[1])
    cells = []
    while unseen:
        start = unseen.pop()
        queue = [start]
        reached = {start}
        while queue:
            u = queue.pop()
            for v in adjacency[u].keys() & unseen:
                unseen.remove(v)
                reached.add(v)
                queue.append(v)
        cells.append(frozenset(reached & support))
    expected = [
        {0, 1, 32, 37}, {25, 38}, {28, 41, 42, 43},
        {30, 44, 45}, {31, 46, 47}, {33}, {34}, {35}, {36}, {40},
    ]
    assert set(cells) == {frozenset(cell) for cell in expected}
    assert sum(map(len, cells)) == len(support - set(paths[0]) - set(paths[1]))
    print("faces=20 unit_vertices=1151795 compressed_edges=106 "
          "paths=1772,1784 residual_site_max=4 old_sites=17 PASS")


if __name__ == "__main__":
    main()
