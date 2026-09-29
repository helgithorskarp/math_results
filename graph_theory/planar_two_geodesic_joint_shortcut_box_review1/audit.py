#!/usr/bin/env python3
"""Independent exact audit of the 14-coordinate joint shortcut box.

Uses heap-based Dijkstra, direct face incidence, and potential checks.
The only data inputs are the two small public JSON certificates.
"""

from collections import Counter
from hashlib import sha256
from heapq import heappop, heappush
from itertools import combinations
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
PREV = ROOT / 'planar_two_geodesic_icosahedron_price_region' / 'certificate.json'
HERE = ROOT / 'planar_two_geodesic_joint_shortcut_box' / 'certificate.json'
PREV_SHA = '070ac17d45f77ad18edb0ac1b9fae642982fc36db7dbd82ed5a1c3c325f1d11d'
HERE_SHA = 'def11165c5d75f0e89c1bed43f910b4fccf973d3f1b60d453be704737b7c882a'


def dijkstra(n, edges, start):
    adj = [[] for _ in range(n)]
    for (u, v), w in edges:
        assert w > 0
        adj[u].append((v, w));adj[v].append((u, w))
    d = [10 ** 30] * n;d[start] = 0
    todo = [(0, start)]
    while todo:
        cost, u = heappop(todo)
        if cost != d[u]:continue
        for v, w in adj[u]:
            new = cost + w
            if new < d[v]:d[v] = new;heappush(todo, (new, v))
    return d


def all_distances(n, edges):
    return [dijkstra(n, edges, v) for v in range(n)]


def components(n, edges, removed):
    adj = [set() for _ in range(n)]
    for (u, v), _ in edges:adj[u].add(v);adj[v].add(u)
    left = set(range(n)) - set(removed)
    result = []
    while left:
        C = {left.pop()};todo = list(C)
        while todo:
            new = adj[todo.pop()] & left
            left -= new;C |= new;todo.extend(new)
        result.append(C)
    return result


def full_edges(core, faces, assignments, D, saving):
    out = list(core.items())
    for j, (a, b, f) in enumerate(assignments):
        z = 12 + j
        c = next(v for v in faces[f] if v not in (a, b))
        x = D[a][b] - saving
        fixed = (D[a][b] - 1510) // 2
        assert 0 < fixed < x
        out.extend([((a, z), fixed), ((b, z), x - fixed),
                    ((c, z), 34580)])
    return out


def main():
    assert sha256(PREV.read_bytes()).hexdigest() == PREV_SHA
    assert sha256(HERE.read_bytes()).hexdigest() == HERE_SHA
    old = json.loads(PREV.read_text());new = json.loads(HERE.read_text())
    assert new['core_scale'] == 151 and new['uniform_saving'] == 1510
    core = {tuple(sorted((u, v))): 151 * c for u, v, c in old['core_edges']}
    faces = [tuple(F) for F in old['faces']]
    paths = [P for pair in old['candidate_pairs'] for P in pair]
    assignment = [tuple(row) for row in new['edge_faces']]
    assert len(core) == 30 and len(faces) == 20 and len(paths) == 6
    assert len(assignment) == len({f for _, _, f in assignment}) == 14
    assert all(tuple(sorted((a, b))) in core and a in faces[f] and b in faces[f]
               for a, b, f in assignment)
    incidence = Counter(tuple(sorted(e)) for F in faces
                        for e in zip(F, F[1:] + F[:1]))
    assert set(incidence) == set(core) and set(incidence.values()) == {2}
    D = all_distances(12, core.items())
    assert max(max(row) for row in D) == 34579
    lengths = [sum(core[tuple(sorted(e))] for e in zip(P, P[1:]))
               for P in paths]
    assert all(lengths[i] == D[P[0]][P[-1]] for i, P in enumerate(paths))

    potentials = {int(s): p for s, p in new['potentials'].items()}
    assert set(potentials) == {0, 1, 2, 5}
    inequalities = 0
    for s, pi in potentials.items():
        assert len(pi) == 12 and pi[s] == 0
        for (u, v), w in core.items():
            assert abs(pi[u] - pi[v]) <= w
            inequalities += 1
        for a, b, f in assignment:
            c = next(v for v in faces[f] if v not in (a, b))
            x = D[a][b] - 1510
            fixed = x // 2
            assert abs(pi[a] - pi[b]) <= x
            assert abs(pi[a] - pi[c]) <= fixed + 34580
            assert abs(pi[b] - pi[c]) <= x - fixed + 34580
            inequalities += 3
    assert inequalities == 288
    assert all(potentials[P[0]][P[-1]] == L for P, L in zip(paths, lengths))

    lower = full_edges(core, faces, assignment, D, 1510)
    upper = full_edges(core, faces, assignment, D, 0)
    mixed = list(lower)
    for j in range(14):
        if j % 2:
            # Only b-z changes; all other edges keep their lower price.
            mixed[30 + 3 * j + 1] = upper[30 + 3 * j + 1]
    assert len(lower) == 72
    for edges in (lower, mixed, upper):
        metric = all_distances(26, edges)
        assert all(metric[P[0]][P[-1]] == L for P, L in zip(paths, lengths))
    full = all_distances(26, lower)
    assert all(full[a][b] == D[a][b] - 1510 for a, b, _ in assignment)
    shortened = sum(full[a][b] < D[a][b] for a, b in combinations(range(12), 2))
    assert shortened == 27

    # The assignment fills distinct core faces, so each insertion
    # replaces one face by three and adds exactly three edges.
    assert 12 + 14 == 26 and 30 + 3 * 14 == 72 and 20 + 2 * 14 == 48
    q_edges = list(core.items())
    for f, F in enumerate(faces):
        q_edges.extend(((u, 12 + f), 1) for u in F)
    projected = 0
    for P, R in old['candidate_pairs']:
        removed = set(P) | set(R)
        qparts = components(32, q_edges, removed)
        for C in components(26, lower, removed):
            image = {v if v < 12 else 12 + assignment[v - 12][2] for v in C}
            assert any(image <= Q for Q in qparts)
            projected += 1
    assert projected == 18

    # A wider asymmetric rectangle uses the same thirteen other lower
    # corners, but splits the 6-10 face shortcut equally at length 604.
    # First recompute the exact one-edge threshold in the graph where
    # that one face shortcut is ineffective.
    j = next(i for i, (a, b, _) in enumerate(assignment)
             if (a, b) == (6, 10))
    base = list(lower)
    base[30 + 3 * j] = ((6, 12 + j), D[6][10] // 2)
    base[30 + 3 * j + 1] = ((10, 12 + j), D[6][10] - D[6][10] // 2)
    base_d = all_distances(26, base)
    assert all(base_d[P[0]][P[-1]] == L for P, L in zip(paths, lengths))
    threshold = max([0] + [value for P, L in zip(paths, lengths)
                           for value in (L - base_d[P[0]][6] - base_d[10][P[-1]],
                                         L - base_d[P[0]][10] - base_d[6][P[-1]])])
    assert threshold == 604
    wide = list(lower)
    wide[30 + 3 * j] = ((6, 12 + j), 302)
    wide[30 + 3 * j + 1] = ((10, 12 + j), 302)
    wide_d = all_distances(26, wide)
    assert wide_d[6][10] == 604
    assert all(wide_d[P[0]][P[-1]] == L for P, L in zip(paths, lengths))
    # Dijkstra distances give four fresh full-graph potentials at the
    # wider lower corner, independently of the target's 12-entry data.
    wide_inequalities = 0
    for s in (0, 1, 2, 5):
        pi = wide_d[s]
        assert pi[s] == 0
        for (u, v), w in wide:
            assert abs(pi[u] - pi[v]) <= w
            wide_inequalities += 1
        for P, L in zip(paths, lengths):
            if P[0] == s:
                assert pi[P[-1]] == L
    assert wide_inequalities == 288
    below_wide = list(wide)
    below_wide[30 + 3 * j] = ((6, 12 + j), 301)
    below_wide_d = all_distances(26, below_wide)
    assert below_wide_d[5][10] == 21743 < lengths[3] == 21744

    beyond = full_edges(core, faces, assignment, D, 1511)
    route = (0, 4, 8, 24, 7, 11, 6)
    prices = {frozenset(edge): w for edge, w in beyond}
    route_length = sum(prices[frozenset((u, v))]
                       for u, v in zip(route, route[1:]))
    assert route_length == 20837 < lengths[4] == 20838
    assert dijkstra(26, beyond, 0)[6] <= route_length
    print('four_potentials=4 inequalities=288 shortcuts=14 dimensions=14 '
          f'shortened_core_pairs={shortened} projected_components={projected} '
          'saving_1511_route=20837 prescribed_length=20838 '
          'asymmetric_6_10_threshold=604 wide_inequalities=288 '
          'at_603_5_to_10=21743 PASS')


if __name__ == '__main__':main()
