#!/usr/bin/env python3
"""Supplementary exact audits for PROOF.md; Python standard library only.

The radius-two reduction and the imported sphere theorems are human-proof
inputs. This is not an exhaustive search for eighteen-vertex spheres.
Validation is kept active under python -O.
"""
from collections import Counter
from itertools import combinations, product
from math import comb
import json
import random


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def graph(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        require(0 <= u < v < n and v not in adj[u], "invalid edge list")
        adj[u].add(v)
        adj[v].add(u)
    return adj


def edge_count(adj, vertices):
    return sum(v in adj[u] for u, v in combinations(sorted(vertices), 2))


def triangles_at(adj):
    return [edge_count(adj, ns) for ns in adj]


def independent_counts(adj, maximum):
    return [sum(all(v not in adj[u] for u, v in combinations(S, 2))
                for S in combinations(range(len(adj)), k))
            for k in range(maximum + 1)]


def h_vector(f, d):
    return [sum((-1)**(k-i)*comb(d-i, k-i)*f[i] for i in range(k+1))
            for k in range(d+1)]


def initial_profile_graph():
    """Deterministic Havel--Hakimi, used only to make algebra test fixtures."""
    residual = [3]*10 + [4]*8
    edges = []
    while any(residual):
        vertices = sorted(range(18), key=lambda v: (-residual[v], v))
        u = vertices[0]
        degree = residual[u]
        residual[u] = 0
        for v in vertices[1:degree+1]:
            require(residual[v] > 0, "nongraphical test degree sequence")
            residual[v] -= 1
            edges.append(tuple(sorted((u, v))))
    return set(edges)


def audit_identities():
    """Definition-level induced edge counts versus local algebra.

    The fixtures are general graphs of the target degree sequence, not
    homology spheres. Positivity and Dehn--Sommerville are not assumed.
    """
    rng = random.Random(202609194)
    edges = initial_profile_graph()
    counts = Counter()
    for sample in range(128):
        for _ in range(64):
            first, second = rng.sample(sorted(edges), 2)
            a, b = first
            c, d = second
            if rng.randrange(2):
                c, d = d, c
            if len({a, b, c, d}) != 4:
                continue
            x, y = tuple(sorted((a, c))), tuple(sorted((b, d)))
            if x in edges or y in edges:
                continue
            edges.difference_update((first, second))
            edges.update((x, y))
        adj = graph(18, sorted(edges))
        q = list(map(len, adj))
        require(q == [3]*10+[4]*8, "switches preserve individual degrees")
        t = triangles_at(adj)
        L = []
        vertex_sets = []
        for v in range(18):
            B = set(range(18)) - {v} - adj[v]
            vertex_sets.append(B)
            value = comb(len(B), 2)-edge_count(adj, B)-7*len(B)+30
            if v < 10:
                expected = 4-len(adj[v] & set(range(10)))-t[v]
            else:
                expected = 2-len(adj[v] & set(range(10)))-t[v]
            require(value == expected, "local link formula")
            L.append(value)
        f = independent_counts(adj, 3)
        T = sum(t)//3
        require(f[2]-9*f[1]+48 == 8, "gamma2 definition")
        require(f[3]-6*f[2]+22*f[1]-64 == -2-T,
                "gamma3 initial-coefficient definition")
        for u, v in combinations(range(10), 2):
            if v in adj[u]:
                continue
            common = adj[u] & adj[v]
            if len(common) > 1:
                continue
            A, B = adj[u]-common, adj[v]-common
            z = sum(y in adj[x] for x in A for y in B)
            W = vertex_sets[u] & vertex_sets[v]
            E = comb(len(W), 2)-edge_count(adj, W)-5*len(W)+16
            expected = L[u]+L[v]-4-z
            if common:
                w, = common
                expected = L[u]+L[v]+1-q[w]-z
            require(E == expected, "edge-link identity")
            counts["empty" if not common else "common_degree_"+str(q[w])] += 1
        counts["graphs"] += 1
    require(all(counts[key] > 0 for key in
                ("empty", "common_degree_3", "common_degree_4")),
            "all three edge-link cases exercised")
    return dict(sorted(counts.items()))


def necessary_cubic_bounds(adj):
    """An optimistic upper bound, using only J, on every cubic E_uv.

    With no common J-neighbor, a common quartic neighbor is allowed only
    if both vertices have a free degree slot; allowing it can only help.
    Mixed triangles and additional cross-neighborhood edges are discarded.
    """
    d = list(map(len, adj))
    t = triangles_at(adj)
    if max(d) > 3 or max(t) > 1:
        return False
    for u, v in combinations(range(10), 2):
        if v in adj[u]:
            continue
        common = adj[u] & adj[v]
        if len(common) >= 2:
            return False
        z = sum(y in adj[x] for x in adj[u]-common for y in adj[v]-common)
        if common:
            bound = 6-d[u]-d[v]-t[u]-t[v]-z
        elif max(d[u], d[v]) == 3:
            bound = 4-d[u]-d[v]-t[u]-t[v]-z
        else:
            bound = 5-d[u]-d[v]-t[u]-t[v]-z
        if bound < 0:
            return False
    return True


def theta_with_remainder(remainder_edge):
    edges = {(0, 1), (0, 2), (2, 3), (3, 4), (1, 4),
             (0, 5), (5, 6), (6, 7), (1, 7)}
    if remainder_edge:
        edges.add((8, 9))
    return graph(10, sorted(edges))


def degree_signature(adj):
    return sorted(map(len, adj))


def audit_rooted_configurations():
    """All branch-size triples and all child graphs after radius two.

    Root=0, neighbors=1,2,3. The root's neighborhood has either no edge
    or a single edge 1--2 (all one-edge choices are isomorphic). Each
    child has a unique parent, as proved from the common-neighbor bound.
    All possible edges among the at most six children are tried. Outside
    components have degree at most one, so their isomorphism type is
    determined by the number of disjoint edges. When the root lies in a
    triangle the proof forces those outside vertices to be isolated.
    """
    counts = Counter()
    maxima = Counter()
    equality_degrees = set()
    for root_triangle in (False, True):
        for ks in product(range(3), repeat=3):
            if root_triangle and (ks[0] > 1 or ks[1] > 1):
                continue
            base = {(0, 1), (0, 2), (0, 3)}
            if root_triangle:
                base.add((1, 2))
            parent = {}
            n = 4
            for a, k in enumerate(ks, 1):
                for _ in range(k):
                    base.add((a, n))
                    parent[n] = a
                    n += 1
            pairs = list(combinations(range(4, n), 2))
            for mask in range(1 << len(pairs)):
                core = base | {edge for i, edge in enumerate(pairs) if mask >> i & 1}
                preliminary = graph(10, sorted(core))
                counts["child_graphs_examined"] += 1
                if max(map(len, preliminary)) > 3:
                    continue
                for matching_size in range(1 if root_triangle else (10-n)//2+1):
                    edges = core | {(n+2*i, n+2*i+1) for i in range(matching_size)}
                    adj = graph(10, sorted(edges))
                    counts["configurations_examined"] += 1
                    if not necessary_cubic_bounds(adj):
                        continue
                    counts["after_necessary_bounds"] += 1
                    if len(edges) < 7:
                        continue
                    counts["at_least_seven_edges"] += 1
                    require(not any(triangles_at(adj)), "cubic triangles excluded")
                    require(len(edges) <= 10, "cubic edge bound")
                    require(all(len(adj[x] & set(parent)) <= 1 for x in parent),
                            "children form a matching")
                    if len(edges) >= 9:
                        require(sum(len(ns) <= 1 for ns in adj) <= 2,
                                "at most two low-degree cubic vertices")
                    maxima[str(len(edges))] += 1
                    if len(edges) == 10:
                        equality_degrees.add(tuple(degree_signature(adj)))
                        require(n == 8 and matching_size == 1 and sorted(ks) == [1, 1, 2],
                                "theta plus edge equality structure")
    require(equality_degrees == {tuple(degree_signature(theta_with_remainder(True)))},
            "degree signature at rooted equality")
    return {"counts": dict(sorted(counts.items())),
            "surviving_edge_counts": dict(sorted(maxima.items())),
            "equality_degree_sequences": [list(x) for x in sorted(equality_degrees)]}


def small_link_models():
    # Type I is the complement of C6 together with two disjoint K2s.
    cycle = {tuple(sorted((i, (i+1) % 6))) for i in range(6)}
    first = (set(combinations(range(6), 2))-cycle) | {(6, 7), (8, 9)}
    # Construct type II in the primal graph by an actual edge subdivision.
    primal = {tuple(sorted((i, (i+1) % 5))) for i in range(5)}
    primal |= {(i, s) for i in range(5) for s in (5, 6)}
    original = graph(7, sorted(primal))
    common = original[0] & original[5]
    primal.remove((0, 5))
    primal |= {(v, 7) for v in common | {0, 5}}
    second = (set(combinations(range(8), 2))-primal) | {(8, 9)}
    result = []
    for edges in (first, second):
        adj = graph(10, sorted(edges))
        f = independent_counts(adj, 5)
        require(f[5] == 0, "small link dimension is three")
        h = h_vector(f[:5], 4)
        require(h == [1, 6, 10, 6, 1], "small link gamma=1+2t")
        suspension_pairs = [(u, v) for u, v in sorted(edges)
                            if adj[u] == {v} and adj[v] == {u}]
        require(suspension_pairs, "classified link is a suspension")
        result.append({"faces_including_empty": f[:5], "h": h,
                       "suspension_pairs": suspension_pairs})
    return result


def numerical_consequences():
    records = []
    for e in range(7, 11):
        for U, V in product(range(4), repeat=2):
            if 2*U+3*V > 2*e-14 or (e >= 9 and U > 2):
                continue
            require(U+V <= 2, "two-triangle bound")
            link_sum = 2*e-14-2*U-3*V
            require(link_sum <= 6, "at least two zero quartic links")
            records.append({"e": e, "mixed_triangles": U, "quartic_triangles": V,
                            "quartic_gamma2_sum": link_sum,
                            "minimum_suspension_links": 8-link_sum})
    require({r["mixed_triangles"]+r["quartic_triangles"] for r in records} == {0, 1, 2},
            "numerical frontier is not overclaimed")
    return records


def main():
    result = {"status": "PASS", "identity_audit": audit_identities(),
              "rooted_configuration_audit": audit_rooted_configurations(),
              "small_link_models": small_link_models(),
              "numerical_frontier": numerical_consequences(),
              "scope": "Supplementary exact checks; the human proof and primary-source sphere inputs remain the trust boundary."}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
