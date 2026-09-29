#!/usr/bin/env python3
"""Independent certificate and non-stacked face-patch audit.

Uses only the predecessor's public JSON certificate as shared input; it
imports no target construction, verification, or audit code.
"""

from hashlib import sha256
from itertools import combinations
from pathlib import Path
from random import Random
import json


CERT = Path(__file__).resolve().parents[1] / 'planar_two_geodesic_icosahedron_price_region' / 'certificate.json'
EXPECTED_HASH = '070ac17d45f77ad18edb0ac1b9fae642982fc36db7dbd82ed5a1c3c325f1d11d'


def floyd(n, edges):
    infinity = sum(edges.values()) + 1
    d = [[0 if u == v else infinity for v in range(n)] for u in range(n)]
    for (u, v), cost in edges.items():
        d[u][v] = d[v][u] = cost
    for k in range(n):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    return d


def parts(n, edges, removed):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v);adj[v].add(u)
    left = set(range(n)) - set(removed)
    out = []
    while left:
        found = {left.pop()};todo = list(found)
        while todo:
            new = adj[todo.pop()] & left
            left -= new;found |= new;todo.extend(new)
        out.append(found)
    return out


def main():
    assert sha256(CERT.read_bytes()).hexdigest() == EXPECTED_HASH
    cert = json.loads(CERT.read_text())
    prices = {tuple(sorted((u, v))): c for u, v, c in cert['core_edges']}
    faces = [tuple(F) for F in cert['faces']]
    pairs = cert['candidate_pairs']
    paths = [P for pair in pairs for P in pair]
    potentials = cert['critical_corner_potentials']
    assert len(prices) == 30 and len(faces) == 20 and len(paths) == len(potentials) == 6
    assert {tuple(F) for F in combinations(range(12), 3)
            if all(tuple(sorted(e)) in prices for e in combinations(F, 2))} == set(faces)
    assert all(sum(set(e) <= set(F) for F in faces) == 2 for e in prices)
    inequalities = 0
    for P, pi in zip(paths, potentials):
        selected = {tuple(sorted(e)) for e in zip(P, P[1:])}
        assert selected <= prices.keys() and len(P) == len(set(P))
        adverse = {e: c * (158 if e in selected else 144) for e, c in prices.items()}
        d = floyd(12, adverse)
        length = sum(adverse[e] for e in selected)
        assert pi[P[0]] == 0 and pi[P[-1]] == length == d[P[0]][P[-1]]
        for (u, v), cost in adverse.items():
            assert abs(pi[u] - pi[v]) <= cost
            inequalities += 1
    assert inequalities == 180

    q_edges = set(prices)
    for f, F in enumerate(faces):
        q_edges.update(tuple(sorted((u, 12 + f))) for u in F)
    partitions = [parts(32, q_edges, set(P) | set(R)) for P, R in pairs]
    atom = lambda C: len(C) == 1 and next(iter(C)) >= 12
    heavy = [[C for C in part if not atom(C)] for part in partitions]
    assert [list(map(len, family)) for family in heavy] == [[13], [21], [13, 6]]
    assert heavy[2][0].isdisjoint(heavy[0][0])
    assert heavy[2][1].isdisjoint(heavy[1][0])
    core_deletions = 0
    for k in range(5):
        for removed in combinations(range(12), k):
            assert len(parts(12, prices, removed)) == 1
            intact_bound = sum(not set(F) <= set(removed) for F in faces) - (4 - k)
            assert intact_bound >= 16
            core_deletions += 1
    assert core_deletions == 794

    # Each face contains a K4 rooted on its boundary triangle, with a
    # pendant interior vertex. This is planar, connected, width three,
    # and differs from the target's recursively stacked triangulations.
    core = {e: 151 * c for e, c in prices.items()}
    core_d = floyd(12, core)
    A = max(max(row) for row in core_d) + 1
    edges = dict(core)
    patches = []
    for f, F in enumerate(faces):
        z, y = 12 + 2 * f, 13 + 2 * f
        for u in F:
            edges[tuple(sorted((u, z)))] = A
        edges[z, y] = f + 1
        patches.append({z, y})
    n = 52
    d = floyd(n, edges)
    assert all(d[u][v] == core_d[u][v] for u in range(12) for v in range(12))
    assert all(sum(edges[tuple(sorted(e))] for e in zip(P, P[1:])) == d[P[0]][P[-1]]
               for P in paths)
    profile = [[0] * n, [1] * n]
    for K in patches:
        for vertex in K:
            w = [0] * n;w[vertex] = 1;profile.append(w)
        w = [0] * n
        for vertex in K:w[vertex] = 1
        w[0] = 2
        profile.append(w)
    rng = Random(2026092930)
    profile.extend([rng.randrange(7) for _ in range(n)] for _ in range(30))
    all_parts = [parts(n, edges, set(P) | set(R)) for P, R in pairs]
    projected = 0
    for expanded, quotient in zip(all_parts, partitions):
        for C in expanded:
            image = {v if v < 12 else 12 + (v - 12) // 2 for v in C}
            assert any(image <= Q for Q in quotient)
            projected += 1
    heavy_cases = 0
    for w in profile:
        M = sum(w);B = max(sum(w[v] for v in K) for K in patches)
        largest = [max((sum(w[v] for v in C) for C in part), default=0)
                   for part in all_parts]
        assert 2 * min(largest) <= max(M, 2 * B)
        if 2 * B <= M:
            assert 2 * min(largest) <= M
            continue
        heavy_cases += 1
        f = next(f for f, K in enumerate(patches) if 2 * sum(w[v] for v in K) > M)
        z, y = sorted(patches[f])
        bags = [set(faces[f]) | {z}, {z, y}]
        assert any(all(2 * sum(w[v] for v in C) <= M
                       for C in parts(n, edges, bag)) for bag in bags)
    assert len(profile) == 92 and heavy_cases >= 40
    short = dict(edges)
    for u in faces[0]:short[tuple(sorted((u, 12)))] = 1
    short_d = floyd(n, short)
    assert any(short_d[u][v] < core_d[u][v] for u, v in combinations(faces[0], 2))
    # A milder shortcut violates full core isometry but preserves every
    # displayed path. The quotient and torso arguments therefore still
    # certify all masses for this concrete metric.
    partial = dict(edges)
    partial[0, 12] = partial[1, 12] = 10000
    partial_d = floyd(n, partial)
    assert core_d[0][1] == 28237 and partial_d[0][1] == 20000
    assert all(sum(core[tuple(sorted(e))] for e in zip(P, P[1:]))
               == partial_d[P[0]][P[-1]] for P in paths)
    print(f'potentials={inequalities} quotient_partitions={list(map(len, partitions))} '
          f'nonstacked_vertices={n} projected_components={projected} '
          f'core_deletions={core_deletions} mass_profiles={len(profile)} '
          f'heavy_bag_cases={heavy_cases} '
          'shortening_patch_detected=YES nonisometric_six_paths=YES PASS')


if __name__ == '__main__':main()
