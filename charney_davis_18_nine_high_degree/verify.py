#!/usr/bin/env python3
"""Supplementary exact checks for PROOF.md; Python standard library only.

This does not enumerate homology spheres. Graphs that are not spheres are
used to check the polynomial/counting identities at the level of definitions.
"""
from itertools import combinations
from math import comb
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def graph(n, edges):
    adj = [0] * n
    for u, v in edges:
        require(0 <= u < v < n, "invalid edge")
        require(not (adj[u] >> v & 1), "duplicate edge")
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return adj


def edge_count(adj, vertices):
    return sum(bool(adj[u] >> v & 1) for u, v in combinations(vertices, 2))


def faces(adj, vertices, max_size):
    """Face counts of the independence complex, including the empty face."""
    return [sum(all(not (adj[u] >> v & 1) for u, v in combinations(face, 2))
                for face in combinations(vertices, k))
            for k in range(max_size + 1)]


def h_coefficients(f, d):
    return [sum(f[i] * (-1) ** (k-i) * comb(d-i, k-i)
                for i in range(k+1)) for k in range(len(f))]


def gamma_coefficients(f, d):
    h = h_coefficients(f, d)
    gamma = []
    for k in range(len(f)):
        require(d >= 2*k, "only the triangular gamma coefficients requested")
        gamma.append(h[k] - sum(gamma[i] * comb(d-2*i, k-i)
                                for i in range(k)))
    return gamma


def link_vertices(adj, face):
    return [u for u in range(len(adj)) if u not in face
            and all(not (adj[u] >> v & 1) for v in face)]


def direct_gamma2(adj, face, d=6):
    vertices = link_vertices(adj, face)
    return gamma_coefficients(faces(adj, vertices, 2), d-len(face))[2]


def audit_graph(adj, dimension_parameter=6):
    """Check identities by direct face counts, not sphere recognition."""
    n = len(adj)
    V = list(range(n))
    d = dimension_parameter
    m = edge_count(adj, V)
    degree = [row.bit_count() for row in adj]
    triangles = sum(all(adj[u] >> v & 1 for u, v in combinations(t, 2))
                    for t in combinations(V, 3))
    f = faces(adj, V, 3)
    independent_triples = (comb(n, 3) if n >= 3 else 0) - (n-2)*m
    independent_triples += sum(comb(q, 2) for q in degree) - triangles
    require(f[3] == independent_triples, "independent triple identity")
    a = gamma_coefficients(f[:3], d)[2]
    links = [direct_gamma2(adj, [v], d) for v in V]
    for v in V:
        N = [u for u in V if adj[v] >> u & 1]
        B = link_vertices(adj, [v])
        tv = edge_count(adj, N)
        require(edge_count(adj, B) == m-sum(degree[u] for u in N)+tv,
                "one-vertex complement edge count")
    checked = 0
    for u, v in combinations(V, 2):
        if adj[u] >> v & 1 or adj[u] & adj[v]:
            continue
        Nu = [x for x in V if adj[u] >> x & 1]
        Nv = [x for x in V if adj[v] >> x & 1]
        z = sum(bool(adj[x] >> y & 1) for x in Nu for y in Nv)
        rhs = links[u]+links[v]-a+(degree[u]-1)*(degree[v]-1)-z
        require(direct_gamma2(adj, [u, v], d) == rhs,
                "disjoint-neighborhood edge-link identity")
        checked += 1
    if d == 6:
        b = gamma_coefficients(f, d)[3]
        require(sum(links) == 3*b+4*a, "vertex-link coefficient identity")
        if n == 18:
            require(a == 39-m, "eighteen-vertex gamma2")
            require(2*b == 460+sum(q*(q-11) for q in degree)-2*triangles,
                    "eighteen-vertex gamma3")
            require(2*sum(links) ==
                    1692+sum(q*(3*q-37) for q in degree)-6*triangles,
                    "degree moment identity")
    return checked


def all_small_graphs():
    graphs = checks = 0
    for n in range(1, 7):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            adj = graph(n, [e for i, e in enumerate(pairs) if mask >> i & 1])
            checks += audit_graph(adj)
            graphs += 1
    require(graphs == 33867, "small graph coverage")
    return graphs, checks


def deterministic_samples():
    # Explicit 64-bit LCG, with no dependence on a library PRNG's version.
    state = 20260919
    checks = 0
    pairs = list(combinations(range(18), 2))
    for sample in range(128):
        edges = []
        threshold = sample % 17
        for e in pairs:
            state = (6364136223846793005*state + 1442695040888963407) % (1 << 64)
            if (state >> 32) % 16 < threshold:
                edges.append(e)
        adj = graph(18, edges)
        checks += audit_graph(adj)
        # Check the dimension-independent version separately at d=7,8.
        if sample < 16:
            audit_graph(adj, 7)
            audit_graph(adj, 8)
    return checks


def boundary_profiles():
    survivors = []
    examined = 0
    for n3 in range(9):
        for n4 in range(19-n3):
            for n5 in range(19-n3-n4):
                for n6 in range(19-n3-n4-n5):
                    n7 = 18-n3-n4-n5-n6
                    counts = (n3, n4, n5, n6, n7)
                    examined += 1
                    total_degree = sum(q*c for q, c in zip(range(3, 8), counts))
                    if total_degree % 2:
                        continue
                    moment = 90-8*n4-13*n5-15*n6-14*n7
                    if moment < 0:
                        continue
                    a = 39-total_degree//2
                    for T in range(moment//3+1):
                        twice_b = 460+sum(q*(q-11)*c
                                          for q, c in zip(range(3, 8), counts))-2*T
                        require(twice_b % 2 == 0, "gamma integrality")
                        survivors.append([list(counts), T, a, twice_b//2])
    expected = [[[8, 8, 2, 0, 0], 0, 6, -8]]
    expected += [[[8, 9, 0, 1, 0], T, 6, -7-T] for T in range(2)]
    expected += [[[8, 10, 0, 0, 0], T, 7, -6-T] for T in range(4)]
    require(survivors == expected, "boundary profile classification")
    return examined, survivors


def component_check():
    # Every graph of maximum degree two is a disjoint union of paths/cycles.
    types = [("P", n) for n in range(1, 9)] + [("C", n) for n in range(5, 9)]
    types.sort()
    candidates = []

    def visit(start, remaining, components):
        if not remaining:
            count = sum(n-(kind == "P") for kind, n in components)
            if count >= 7:
                candidates.append(tuple(components))
            return
        for i in range(start, len(types)):
            kind, n = types[i]
            if n <= remaining:
                visit(i, remaining-n, components+[(kind, n)])

    visit(0, 8, [])
    expected = {(('P', 8),), (('C', 8),), (('C', 7), ('P', 1)),
                (('C', 6), ('P', 2)), (('C', 5), ('P', 3))}
    require(set(candidates) == expected, "degree-two component classification")
    for components in candidates:
        edges, offset = [], 0
        for kind, n in components:
            edges += [(offset+i, offset+i+1) for i in range(n-1)]
            if kind == "C":
                edges.append((offset, offset+n-1))
            offset += n
        adj = graph(8, edges)
        witnesses = [(u, v) for u, v in combinations(range(8), 2)
                     if adj[u].bit_count() == adj[v].bit_count() == 2
                     and not (adj[u] >> v & 1) and not (adj[u] & adj[v])]
        require(bool(witnesses), "missing final edge-link witness")
    return [[kind+str(n) for kind, n in c] for c in sorted(candidates)]


def join_of_cycles(lengths, suspensions=0):
    """Return the complement graph of a join of cycles and S^0 factors."""
    edges, offset = [], 0
    for length in lengths:
        for i, j in combinations(range(length), 2):
            if (j-i) not in (1, length-1):
                edges.append((offset+i, offset+j))
        offset += length
    for _ in range(suspensions):
        edges.append((offset, offset+1))
        offset += 2
    return graph(offset, edges)


def positive_controls():
    H = join_of_cycles([6, 6, 6])
    f = faces(H, list(range(18)), 6)
    h = h_coefficients(f, 6)
    g = gamma_coefficients(f[:4], 6)
    require(h == list(reversed(h)), "join Dehn--Sommerville")
    require(g == [1, 6, 12, 8], "six-cycle join gamma")
    require(all(row.bit_count() == 3 for row in H), "sharp polar example")
    audit_graph(H)
    Y = join_of_cycles([5, 5], 1)
    fy = faces(Y, list(range(12)), 5)
    gy = gamma_coefficients(fy[:3], 5)
    sum_edge_link = sum(direct_gamma2(Y, [v], 5) for v in range(12))
    require(gy == [1, 2, 1] and sum_edge_link == 2,
            "correct four-dimensional normalization")
    require(fy == [1, 12, 55, 120, 125, 50], "normalization fixture faces")
    return {"C6_C6_C6": {"faces": f, "h": h, "gamma": g},
            "C5_C5_S0": {"faces": fy, "gamma": gy,
                          "sum_vertex_link_gamma2": sum_edge_link}}


def main():
    graphs, small_checks = all_small_graphs()
    sample_checks = deterministic_samples()
    examined, profiles = boundary_profiles()
    report = {"status": "VERIFIED", "all_graphs_orders_1_through_6": graphs,
              "small_graph_disjoint_neighborhood_checks": small_checks,
              "eighteen_vertex_samples": 128,
              "sample_disjoint_neighborhood_checks": sample_checks,
              "degree_count_vectors_examined": examined,
              "eight_cubic_boundary_profiles": profiles,
              "final_degree_two_components": component_check(),
              "positive_controls": positive_controls()}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
