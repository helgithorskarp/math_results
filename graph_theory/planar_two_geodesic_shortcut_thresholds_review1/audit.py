#!/usr/bin/env python3
"""Independent Dijkstra audit of patch compression and shortcut thresholds.

No target code is imported. The predecessor's public certificate is the
only shared data input; the fourteen-row table is compared explicitly.
"""

from hashlib import sha256
from heapq import heappop, heappush
from itertools import combinations
from pathlib import Path
import json


CERT = Path(__file__).resolve().parents[1] / 'planar_two_geodesic_icosahedron_price_region' / 'certificate.json'
CERT_SHA = '070ac17d45f77ad18edb0ac1b9fae642982fc36db7dbd82ed5a1c3c325f1d11d'
EXPECTED = {
    (0, 1): (28237, 15251), (0, 3): (17214, 4228),
    (0, 5): (10570, 302), (1, 2): (27180, 6946),
    (1, 10): (26274, 3171), (2, 3): (25519, 5285),
    (2, 6): (18271, 4530), (2, 7): (14647, 3322),
    (3, 4): (16157, 3171), (3, 8): (14798, 2265),
    (4, 5): (11627, 1359), (6, 10): (22952, 604),
    (7, 8): (15402, 13892), (10, 11): (19177, 4379),
}


def distances(n, weighted_edges, start):
    adj = [[] for _ in range(n)]
    for (u, v), weight in weighted_edges:
        assert weight > 0
        adj[u].append((v, weight));adj[v].append((u, weight))
    d = [10 ** 30] * n;d[start] = 0
    todo = [(0, start)]
    while todo:
        cost, v = heappop(todo)
        if cost != d[v]:continue
        for u, weight in adj[v]:
            new = cost + weight
            if new < d[u]:d[u] = new;heappush(todo, (new, u))
    return d


def all_distances(n, edges):
    return [distances(n, edges, s) for s in range(n)]


def patch_star(core, face, edge, price, z, diameter):
    a, b = edge
    c = next(v for v in face if v not in edge)
    return list(core.items()) + [((a, z), price // 2),
                                  ((b, z), price - price // 2),
                                  ((c, z), diameter + 1)]


def compression_control():
    core = { (0, 1): 5, (0, 2): 7, (1, 2): 6 }
    patch = { (0, 3): 2, (3, 4): 1, (1, 4): 1, (2, 4): 5 }
    full = all_distances(5, list(core.items()) + list(patch.items()))
    virtual = list(core.items()) + [((0, 1), 4), ((0, 2), 8), ((1, 2), 6)]
    reduced = all_distances(3, virtual)
    assert all(full[u][v] == reduced[u][v]
               for u in range(3) for v in range(3))
    assert (full[0][1], full[0][2], full[1][2]) == (4, 7, 6)


def main():
    compression_control()
    assert sha256(CERT.read_bytes()).hexdigest() == CERT_SHA
    cert = json.loads(CERT.read_text())
    core = {tuple(sorted((u, v))): 151 * c for u, v, c in cert['core_edges']}
    faces = [tuple(F) for F in cert['faces']]
    paths = [P for pair in cert['candidate_pairs'] for P in pair]
    assert len(core) == 30 and len(faces) == 20 and len(paths) == 6
    assert {tuple(F) for F in combinations(range(12), 3)
            if all(tuple(sorted(e)) in core for e in combinations(F, 2))} == set(faces)
    D = all_distances(12, core.items())
    diameter = max(max(row) for row in D)
    assert diameter == 34579
    lengths = [sum(core[tuple(sorted(e))] for e in zip(P, P[1:]))
               for P in paths]
    assert all(lengths[i] == D[P[0]][P[-1]] for i, P in enumerate(paths))
    strict = {}
    controls = 0
    for edge in core:
        a, b = edge
        deficits = [0]
        for P, L in zip(paths, lengths):
            s, t = P[0], P[-1]
            deficits.append(L - D[s][a] - D[b][t])
            deficits.append(L - D[s][b] - D[a][t])
        T = max(deficits)
        assert 2 <= T <= D[a][b]
        supporting = [F for F in faces if a in F and b in F]
        assert len(supporting) == 2
        at = all_distances(13, patch_star(core, supporting[0], edge, T, 12, diameter))
        below = all_distances(13, patch_star(core, supporting[0], edge, T - 1, 12, diameter))
        assert all(at[P[0]][P[-1]] == L for P, L in zip(paths, lengths))
        assert any(below[P[0]][P[-1]] < L for P, L in zip(paths, lengths))
        assert at[a][b] == min(T, D[a][b])
        if T < D[a][b]:strict[edge] = (D[a][b], T)
        controls += 2
    assert strict == EXPECTED and controls == 60

    # Each shortcut is safe alone at its threshold, but two distinct
    # face stellations can combine to break a menu path.
    first = patch_star(core, (0, 1, 2), (0, 1), 15251, 12, diameter)
    second = patch_star({}, (0, 3, 4), (0, 3), 4228, 13, diameter)
    together = all_distances(14, first + second)
    assert together[1][3] == 19479 < lengths[0] == 32465
    print('compression_triangle=PASS edges=30 strict_shortcuts=14 '
          'threshold_controls=60 joint_shortcuts_1_to_3=19479 '
          'original_path_1_to_3=32465 PASS')


if __name__ == '__main__':main()
