"""Exact four-potential certificate for a 14-dimensional shortcut box."""

from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "planar_two_geodesic_icosahedron_price_region/certificate.json"
SOURCE_SHA256 = "070ac17d45f77ad18edb0ac1b9fae642982fc36db7dbd82ed5a1c3c325f1d11d"


def load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA256
    return json.loads(raw), json.loads((HERE / "certificate.json").read_text())


def sphere(n, edges, faces):
    undirected = {tuple(sorted((a, b))) for a, b, _ in edges}
    assert len(undirected) == len(edges)
    incidence = Counter(tuple(sorted((a, b))) for F in faces
                        for a, b in ((F[0], F[1]), (F[1], F[2]), (F[2], F[0])))
    assert set(incidence) == undirected
    assert all(incidence[e] == 2 for e in undirected)
    assert n - len(edges) + len(faces) == 2
    for v in range(n):
        link = {}
        for F in faces:
            if v in F:
                a, b = [x for x in F if x != v]
                link.setdefault(a, set()).add(b)
                link.setdefault(b, set()).add(a)
        assert link and all(len(neighbors) == 2 for neighbors in link.values())
        seen = {min(link)}
        stack = [min(link)]
        while stack:
            for u in link[stack.pop()] - seen:
                seen.add(u)
                stack.append(u)
        assert seen == set(link)


def floyd(n, edges):
    inf = 10 ** 20
    D = [[0 if i == j else inf for j in range(n)] for i in range(n)]
    for a, b, w in edges:
        assert a != b and w > 0
        D[a][b] = min(D[a][b], w)
        D[b][a] = min(D[b][a], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                D[i][j] = min(D[i][j], D[i][k] + D[k][j])
    assert all(D[i][j] < inf for i in range(n) for j in range(n))
    return D


def components(n, edges, removed):
    adj = [set() for _ in range(n)]
    for a, b, _ in edges:
        adj[a].add(b)
        adj[b].add(a)
    left = set(range(n)) - set(removed)
    out = []
    while left:
        block = {left.pop()}
        todo = list(block)
        while todo:
            fresh = adj[todo.pop()] & left
            left -= fresh
            block |= fresh
            todo.extend(fresh)
        out.append(frozenset(block))
    return out


def threshold(a, b, paths, D):
    values = [0]
    for P in paths:
        s, t = P[0], P[-1]
        values.extend((D[s][t] - D[s][a] - D[b][t],
                       D[s][t] - D[s][b] - D[a][t]))
    return max(values)


def build(core_edges, core_faces, assignment, D, saving):
    n = 12 + len(assignment)
    diameter = max(max(row) for row in D)
    edges = list(core_edges)
    selected = {}
    for j, (a, b, f) in enumerate(assignment):
        x = D[a][b] - saving
        assert x >= 2
        c = next(v for v in core_faces[f] if v not in (a, b))
        z = 12 + j
        edges.extend(((a, z, x // 2), (b, z, x - x // 2),
                      (c, z, diameter + 1)))
        selected[f] = z
    faces = []
    for f, F in enumerate(core_faces):
        if f not in selected:
            faces.append(F)
        else:
            z = selected[f]
            faces.extend(((F[0], F[1], z), (F[1], F[2], z),
                          (F[2], F[0], z)))
    sphere(n, edges, faces)
    return edges, faces


def quotient_test(core_edges, core_faces, assignment, paths, expanded_edges):
    quotient = list(core_edges)
    for f, F in enumerate(core_faces):
        quotient.extend((u, 12 + f, 1) for u in F)
    H = []
    actual_parts = 0
    for i in range(3):
        p, q = paths[2 * i:2 * i + 2]
        removed = set(p) | set(q)
        qparts = components(32, quotient, removed)
        core_parts = [C for C in qparts if C & set(range(12))]
        if i < 2:
            assert len(core_parts) == 1
            H.append(core_parts[0])
        else:
            assert all(C.isdisjoint(H[0]) or C.isdisjoint(H[1])
                       for C in core_parts)
        for C in components(26, expanded_edges, removed):
            projection = {v if v < 12 else 12 + assignment[v - 12][2]
                          for v in C}
            assert any(projection <= Q for Q in qparts)
            actual_parts += 1
    return actual_parts


def main():
    source, cert = load()
    scale = cert["core_scale"]
    saving = cert["uniform_saving"]
    assert scale == 151 and saving == 1510
    core_edges = [(a, b, scale * price)
                  for a, b, price in source["core_edges"]]
    core_faces = [tuple(F) for F in source["faces"]]
    assert len(core_edges) == 30 and len(core_faces) == 20
    sphere(12, core_edges, core_faces)
    D = floyd(12, core_edges)
    paths = [tuple(P) for pair in source["candidate_pairs"] for P in pair]
    assert len(paths) == 6
    prices = {tuple(sorted((a, b))): w for a, b, w in core_edges}
    for P in paths:
        length = sum(prices[tuple(sorted((a, b)))]
                     for a, b in zip(P, P[1:]))
        assert length == D[P[0]][P[-1]]

    assignment = [tuple(row) for row in cert["edge_faces"]]
    strict = {(a, b) for a, b, _ in core_edges
              if threshold(a, b, paths, D) < D[a][b]}
    assert len(strict) == len(assignment) == 14
    assert {(a, b) for a, b, _ in assignment} == strict
    assert len({f for _, _, f in assignment}) == 14
    assert all(a in core_faces[f] and b in core_faces[f]
               for a, b, f in assignment)
    assert min(D[a][b] - saving for a, b, _ in assignment) > 0
    assert any(D[a][b] - threshold(a, b, paths, D) == saving
               for a, b, _ in assignment)

    # Four core potentials certify six paths throughout the whole box.
    potentials = {int(s): pi for s, pi in cert["potentials"].items()}
    assert set(potentials) == {0, 1, 2, 5}
    assert all(len(pi) == 12 and pi[s] == 0
               for s, pi in potentials.items())
    inequalities = 0
    for s, pi in potentials.items():
        for a, b, w in core_edges:
            assert abs(pi[a] - pi[b]) <= w
            inequalities += 1
        for a, b, f in assignment:
            x = D[a][b] - saving
            c = next(v for v in core_faces[f] if v not in (a, b))
            assert abs(pi[a] - pi[b]) <= x
            assert abs(pi[a] - pi[c]) <= x // 2 + max(max(row) for row in D) + 1
            assert abs(pi[b] - pi[c]) <= x - x // 2 + max(max(row) for row in D) + 1
            inequalities += 3
    assert inequalities == 4 * (30 + 3 * 14)
    for P in paths:
        assert potentials[P[0]][P[-1]] == D[P[0]][P[-1]]

    expanded_edges, faces = build(core_edges, core_faces, assignment, D, saving)
    assert len(expanded_edges) == 72 and len(faces) == 48
    full = floyd(26, expanded_edges)
    assert all(full[P[0]][P[-1]] == D[P[0]][P[-1]] for P in paths)
    assert all(full[a][b] == D[a][b] - saving for a, b, _ in assignment)
    shortened = sum(full[a][b] < D[a][b]
                    for a, b in combinations(range(12), 2))
    assert shortened == 27
    parts = quotient_test(core_edges, core_faces, assignment,
                          paths, expanded_edges)

    # A literal path witnesses sharpness of the common saving.
    below_edges, _ = build(core_edges, core_faces, assignment, D, saving + 1)
    edge_prices = {frozenset((a, b)): w for a, b, w in below_edges}
    route = (0, 4, 8, 24, 7, 11, 6)
    route_length = sum(edge_prices[frozenset((a, b))]
                       for a, b in zip(route, route[1:]))
    assert route_length == D[0][6] - 1 == 20837
    assert floyd(26, below_edges)[0][6] < D[0][6]

    print("core=12 full_vertices=26 full_edges=72 full_faces=48")
    print(f"shortcuts=14 box_saving=1510 potential_inequalities={inequalities}")
    print(f"shortened_core_pairs={shortened} projected_components={parts}")
    print("saving_1511_witness_length=20837 original_length=20838 PASS")


if __name__ == "__main__":
    main()
