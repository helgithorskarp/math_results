"""Exact center-metric shortcut thresholds with whole-graph controls."""

from collections import Counter
from pathlib import Path
import hashlib
import json


CERTIFICATE = (Path(__file__).resolve().parent.parent /
               "planar_two_geodesic_icosahedron_price_region/certificate.json")
CERTIFICATE_SHA256 = "070ac17d45f77ad18edb0ac1b9fae642982fc36db7dbd82ed5a1c3c325f1d11d"
EXPECTED = {
    (0, 1): (28237, 15251), (0, 3): (17214, 4228),
    (0, 5): (10570, 302), (1, 2): (27180, 6946),
    (1, 10): (26274, 3171), (2, 3): (25519, 5285),
    (2, 6): (18271, 4530), (2, 7): (14647, 3322),
    (3, 4): (16157, 3171), (3, 8): (14798, 2265),
    (4, 5): (11627, 1359), (6, 10): (22952, 604),
    (7, 8): (15402, 13892), (10, 11): (19177, 4379),
}


def certificate():
    raw = CERTIFICATE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == CERTIFICATE_SHA256
    return json.loads(raw)


def check_sphere(n, edges, faces):
    undirected = {tuple(sorted(edge[:2])) for edge in edges}
    assert len(undirected) == len(edges)
    face_edges = Counter(tuple(sorted((a, b)))
                         for F in faces for a, b in
                         ((F[0], F[1]), (F[1], F[2]), (F[2], F[0])))
    assert set(face_edges) == undirected
    assert all(face_edges[e] == 2 for e in undirected)
    assert n - len(undirected) + len(faces) == 2
    for v in range(n):
        link = {}
        for F in faces:
            if v not in F:
                continue
            a, b = [u for u in F if u != v]
            link.setdefault(a, set()).add(b)
            link.setdefault(b, set()).add(a)
        assert link and all(len(other) == 2 for other in link.values())
        reached = {min(link)}
        frontier = [min(link)]
        while frontier:
            for u in link[frontier.pop()] - reached:
                reached.add(u)
                frontier.append(u)
        assert reached == set(link)


def floyd(n, edges):
    inf = 10 ** 30
    D = [[0 if i == j else inf for j in range(n)] for i in range(n)]
    for a, b, w in edges:
        assert 0 <= a < n and 0 <= b < n and a != b and w > 0
        D[a][b] = min(D[a][b], w)
        D[b][a] = min(D[b][a], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                D[i][j] = min(D[i][j], D[i][k] + D[k][j])
    assert all(D[i][j] < inf for i in range(n) for j in range(n))
    return D


def threshold(a, b, paths, D):
    values = [0]
    for P in paths:
        s, t = P[0], P[-1]
        L = D[s][t]
        values.extend((L - D[s][a] - D[b][t],
                       L - D[s][b] - D[a][t]))
    return max(values)


def face_graph(core_edges, faces, face, a, b, x, diameter):
    assert a in face and b in face and x >= 2
    c = next(v for v in face if v not in (a, b))
    edges = list(core_edges) + [(a, 12, x // 2),
                                (b, 12, x - x // 2),
                                (c, 12, diameter + 1)]
    new_faces = [F for F in faces if F != face]
    new_faces.extend(((face[0], face[1], 12),
                      (face[1], face[2], 12),
                      (face[2], face[0], 12)))
    check_sphere(13, edges, new_faces)
    return floyd(13, edges)


def main():
    data = certificate()
    assert data["vertices"] == 32 and len(data["faces"]) == 20
    core_edges = [(a, b, 151 * price)
                  for a, b, price in data["core_edges"]]
    assert len(core_edges) == 30
    faces = [tuple(F) for F in data["faces"]]
    check_sphere(12, core_edges, faces)
    D = floyd(12, core_edges)
    paths = [tuple(P) for pair in data["candidate_pairs"] for P in pair]
    assert len(paths) == 6
    edge_prices = {tuple(sorted((a, b))): w for a, b, w in core_edges}
    for P in paths:
        assert len(P) == len(set(P))
        length = sum(edge_prices[tuple(sorted((a, b)))]
                     for a, b in zip(P, P[1:]))
        assert length == D[P[0]][P[-1]]

    diameter = max(max(row) for row in D)
    strict = {}
    for a, b, _ in core_edges:
        T = threshold(a, b, paths, D)
        assert 2 <= T <= D[a][b]
        containing = [F for F in faces if a in F and b in F]
        assert len(containing) == 2
        at = face_graph(core_edges, faces, containing[0], a, b, T, diameter)
        below = face_graph(core_edges, faces, containing[0], a, b,
                           T - 1, diameter)
        assert all(at[P[0]][P[-1]] == D[P[0]][P[-1]] for P in paths)
        assert any(below[P[0]][P[-1]] < D[P[0]][P[-1]] for P in paths)
        assert at[a][b] == min(T, D[a][b])
        if T < D[a][b]:
            strict[a, b] = (D[a][b], T)
    assert strict == EXPECTED
    print(f"core: vertices=12 edges=30 faces=20 paths=6 diameter={diameter}")
    print("single_shortcut_edges=30 strict_shortcuts=14 threshold_controls=60")
    print("max_distance_saving=23103 min_threshold=302 PASS")


if __name__ == "__main__":
    main()
