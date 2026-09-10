#!/usr/bin/env python3
"""Exact checks for the weighted gap lemma; Python standard library only.

No optimizer, graph-generation completeness claim, or floating point is used.
"""
import json
from itertools import combinations
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def q(d, s):
    return {6: (s - 8) ** 2, 7: (s - 7) * (s - 8),
            8: (s - 5) * (s - 9)}[d]


def local_types():
    for d in (6, 7, 8):
        for a in range(d + 1):
            for b in range(d - a + 1):
                c = d - a - b
                if 6*a + 7*b + 8*c <= 53:
                    yield d, (a, b, c)


def verify_weighted_certificate():
    """Combine integer pair-capacity and handshake rows independently of q."""
    count = 0
    for d, (a, b, c) in local_types():
        pair77 = b*(b-1) + (d == 7)*b
        pair88 = c*(c-1) + (d == 8)*c
        pair78 = b*c + (d == 7)*c
        hand67 = (d == 6)*b - (d == 7)*a
        hand68 = (d == 6)*c - (d == 8)*a
        hand78 = (d == 7)*c - (d == 8)*b
        row = (pair77 + 4*pair88 + 4*pair78
               + {6: 64, 7: -49, 8: -179}[d]
               - 15*hand67 - 28*hand68 - 15*hand78)
        require(row == q(d, b+2*c), "weighted row mismatch")
        require(row >= 0, "negative local coefficient")
        count += 1
    require(count == 72, "wrong local type count")
    for z in range(26):
        n6, n7, n8 = z+4, 50-2*z, z
        rhs = (n7*(n7-1) + 4*n8*(n8-1) + 4*n7*n8
               + 64*n6 - 49*n7 - 179*n8)
        require(rhs == 256-19*z, "right-hand side mismatch")
        require((rhs >= 0) == (z <= 13), "wrong integral bound")


def graph(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        require(type(u) is int and type(v) is int, "noninteger endpoint")
        require(0 <= u < n and 0 <= v < n and u != v, "invalid edge")
        require(v not in adj[u], "duplicate edge")
        adj[u].add(v)
        adj[v].add(u)
    return adj


def check_girth_and_identities(adj, check_gap=False):
    n = len(adj)
    d = list(map(len, adj))
    w = [x-6 for x in d]
    s = [sum(w[u] for u in row) for row in adj]
    distant = [set() for _ in adj]
    edge_weight = path_weight = far_weight = all_weight = 0
    for u, v in combinations(range(n), 2):
        common = len(adj[u] & adj[v])
        require(common <= 1, "quadrilateral detected")
        require(not (v in adj[u] and common), "triangle detected")
        all_weight += w[u]*w[v]
        if v in adj[u]:
            edge_weight += w[u]*w[v]
        elif common:
            path_weight += w[u]*w[v]
        else:
            distant[u].add(v)
            distant[v].add(u)
            far_weight += w[u]*w[v]
    require(all_weight == edge_weight+path_weight+far_weight,
            "weighted partition mismatch")
    require(sum(s[v]**2 - sum(w[u]**2 for u in adj[v]) for v in range(n))
            == 2*path_weight, "weighted two-path count mismatch")
    for u in range(n):
        require(n-len(distant[u]) == 1+sum(d[v] for v in adj[u]),
                "ball identity mismatch")
        for v in range(n):
            ab = len(adj[u] & distant[v])
            ba = len(distant[u] & adj[v])
            require(ab-ba == (d[u]-d[v])*(v not in adj[u]),
                    "commutator identity mismatch")
    if check_gap:
        require(all(x in (6, 7, 8) for x in d), "gap domain violation")
        S = sum(w)
        lhs = sum(q(d[v], s[v]) for v in range(n)) + 2*far_weight
        rhs = S*S-114*S+64*n-19*d.count(8)
        require(lhs == rhs, "gap identity mismatch")
    return sum(d)//2


def hoffman_singleton_edges():
    """Five pentagons, five pentagrams, and modular cross edges."""
    edges = set()
    for i in range(5):
        for j in range(5):
            edges.add(tuple(sorted((5*i+j, 5*i+(j+1) % 5))))
            edges.add(tuple(sorted((25+5*i+j, 25+5*i+(j+2) % 5))))
            for k in range(5):
                edges.add((5*i+j, 25+5*k+(i*k+j) % 5))
    return edges


def verify_graph_controls():
    edges = hoffman_singleton_edges()
    require(len(edges) == 175, "control size mismatch")
    for deleted in (set(), {(0, 1)}, {(0, 1), (2, 3)}):
        require(check_girth_and_identities(graph(50, sorted(edges-deleted)), True)
                == 175-len(deleted), "edge-deletion control mismatch")
    # These controls check that the cycle detector rejects both forbidden cycles.
    for n, bad in ((3, [(0, 1), (1, 2), (0, 2)]),
                   (4, [(0, 1), (1, 2), (2, 3), (0, 3)])):
        try:
            check_girth_and_identities(graph(n, bad))
        except ValueError as error:
            require("detected" in str(error), "unexpected rejection")
        else:
            raise ValueError("forbidden-cycle control was accepted")


def verify_lower_bound():
    data = json.loads((HERE / "lower_bound_54_185.json").read_text())
    require(data["n"] == 54 and len(data["edges"]) == 185,
            "lower-bound dimensions mismatch")
    require(check_girth_and_identities(graph(data["n"], data["edges"])) == 185,
            "lower-bound size mismatch")


def verify_boundary_profile():
    """Check an integral relaxation, NOT a graph-realization certificate.

    Type i has degree d_i, counts a_ij of neighbors in degree class j,
    and multiplicity X_i. E_ik counts edges between types; E_ii counts
    internal edges once. I_ik is E_ik off diagonal and 2E_ii on diagonal.

    Constraints checked:
    * class sizes and local ball bounds;
    * sum_{k: d_k=j} I_ik = X_i a_ij;
    * sum_k I_ik a_kj + X_i a_ij
          <= X_i [n_j+(d_i-1)1_{d_i=j}];
    * all six degree-class pair capacities (edges plus two-paths);
    * E_ik <= X_i X_k and E_ii <= choose(X_i,2).

    The third line is the average over vertices of type i of the count
    of distinct class-j vertices at distance one or two, with returns
    to the starting vertex subtracted. Its validity follows from girth.
    """
    data = json.loads((HERE / "boundary_profile.json").read_text())
    types = data["types"]
    D = [t["degree"] for t in types]
    N = [t["neighbors"] for t in types]
    X = [t["count"] for t in types]
    nt = len(types)
    allowed = set(local_types())
    require(len(set((D[i], tuple(N[i])) for i in range(nt))) == nt,
            "repeated type")
    for i in range(nt):
        require(type(X[i]) is int and X[i] > 0, "invalid multiplicity")
        require((D[i], tuple(N[i])) in allowed, "invalid local type")
    sizes = [sum(X[i] for i in range(nt) if D[i] == j) for j in (6, 7, 8)]
    require(sizes == [17, 24, 13], "wrong boundary class sizes")
    E = [[0]*nt for _ in types]
    seen = set()
    for i, k, e in data["edges_between_types"]:
        require(all(type(v) is int for v in (i, k, e)), "noninteger entry")
        require(0 <= i <= k < nt and e > 0 and (i, k) not in seen,
                "invalid aggregate edge")
        seen.add((i, k))
        require(e <= (comb(X[i], 2) if i == k else X[i]*X[k]),
                "simple type-pair capacity exceeded")
        E[i][k] = E[k][i] = e
    I = [[E[i][k]*(2 if i == k else 1) for k in range(nt)] for i in range(nt)]
    for i in range(nt):
        for j in range(3):
            require(N[i][j] <= sizes[j]-(D[i] == j+6), "class capacity")
            require(sum(I[i][k] for k in range(nt) if D[k] == j+6)
                    == X[i]*N[i][j], "incidence balance mismatch")
            lhs = sum(I[i][k]*N[k][j] for k in range(nt)) + X[i]*N[i][j]
            rhs = X[i]*(sizes[j]+(D[i]-1)*(D[i] == j+6))
            require(lhs <= rhs, "type-averaged two-step capacity")
    for a in range(3):
        for b in range(a, 3):
            edge_count = sum(E[i][k] for i in range(nt) for k in range(i, nt)
                             if sorted((D[i]-6, D[k]-6)) == [a, b])
            paths = sum(X[i]*(comb(N[i][a], 2) if a == b
                             else N[i][a]*N[i][b]) for i in range(nt))
            capacity = comb(sizes[a], 2) if a == b else sizes[a]*sizes[b]
            require(edge_count+paths <= capacity, "class pair capacity")
    require(sum(e for i, k, e in data["edges_between_types"]) == 187,
            "wrong aggregate edge total")
    require(sum(X[i]*q(D[i], N[i][1]+2*N[i][2]) for i in range(nt)) == 9,
            "boundary gap mismatch")
    require(all(N[i][1]+2*N[i][2] == 5 for i in range(nt) if D[i] == 8),
            "expected degree-eight sink types")
    return nt, len(seen)


def main():
    verify_weighted_certificate()
    print("PASS: 72 local types; exact weighted certificate; z <= 13")
    verify_graph_controls()
    print("PASS: Hoffman-Singleton and two edge-deletion controls")
    verify_lower_bound()
    print("PASS: independently checked 54-vertex, 185-edge lower-bound fixture")
    nt, ne = verify_boundary_profile()
    print(f"PASS: integral z=13 aggregate certificate ({nt} types, {ne} nonzero edge counts)")


if __name__ == "__main__":
    main()
