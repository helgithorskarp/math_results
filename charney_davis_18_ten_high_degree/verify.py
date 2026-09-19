#!/usr/bin/env python3
"""Supplementary exact checks; no sphere enumeration or solver is used.

All assertions use require(), so python -O does not disable validation.
The completeness of the two small-link types is an external theorem,
not a claim established by this program.
"""
from itertools import combinations, product
from collections import Counter
from math import comb
import json


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def graph(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        require(0 <= u < v < n, "invalid edge")
        require(v not in adj[u], "duplicate edge")
        adj[u].add(v)
        adj[v].add(u)
    return adj


def edge_count(adj, vertices):
    return sum(v in adj[u] for u, v in combinations(vertices, 2))


def faces(adj, vertices, max_size):
    return [sum(all(v not in adj[u] for u, v in combinations(f, 2))
                for f in combinations(vertices, k))
            for k in range(max_size+1)]


def h_vector(f, d):
    return [sum(f[i]*(-1)**(k-i)*comb(d-i, k-i)
                for i in range(k+1)) for k in range(d+1)]


def profiles():
    records = []
    considered = 0
    for n4 in range(10):
        for n5 in range(10-n4):
            for n6 in range(10-n4-n5):
                n7 = 9-n4-n5-n6
                counts = [9, n4, n5, n6, n7]
                considered += 1
                degree_sum = sum(d*n for d, n in zip(range(3, 8), counts))
                if degree_sum % 2:
                    continue
                moment = 90-8*n4-13*n5-15*n6-14*n7
                for T in range(moment//3+1):
                    a = 39-degree_sum//2
                    twice_b = 460+sum(d*(d-11)*n
                                      for d, n in zip(range(3, 8), counts))-2*T
                    require(twice_b % 2 == 0, "gamma integrality")
                    b = twice_b//2
                    require(3*b+4*a == moment-3*T, "profile moment")
                    require(b < 0, "every boundary profile is negative")
                    records.append([counts, T, a, b])
    require(considered == 220, "all weak compositions of nine")
    expected = [([9, 8, 0, 0, 1], 6, 4, -4),
                ([9, 6, 0, 0, 3], 3, 0, -4),
                ([9, 7, 0, 1, 1], 5, 1, -5),
                ([9, 8, 1, 0, 0], 7, 4, -5),
                ([9, 6, 1, 0, 2], 4, 0, -5),
                ([9, 7, 1, 1, 0], 6, 2, -6),
                ([9, 6, 2, 0, 1], 5, 0, -6),
                ([9, 6, 3, 0, 0], 6, 1, -7)]
    expanded = [[ns, T, a, b0-T] for ns, a, maxT, b0 in expected
                for T in range(maxT+1)]
    require(sorted(records) == sorted(expanded), "eight-row table")
    return considered, sorted(records)


def audit_identities():
    """Direct independent-set counts versus the formulas in PROOF.md."""
    state = 202609192
    samples = 128
    for sample in range(samples):
        es = []
        for e in combinations(range(18), 2):
            state = (6364136223846793005*state+1442695040888963407) % 2**64
            if (state >> 32) % 16 < sample % 17:
                es.append(e)
        adj = graph(18, es)
        q = list(map(len, adj))
        f = faces(adj, range(18), 3)
        a = f[2]-9*f[1]+48
        b = f[3]-6*f[2]+22*f[1]-64
        T = sum(all(v in adj[u] for u, v in combinations(tri, 2))
                for tri in combinations(range(18), 3))
        require(a == 39-len(es), "gamma2 formula")
        require(2*b == 460+sum(d*(d-11) for d in q)-2*T, "gamma3 formula")
        L = []
        for v in range(18):
            B = set(range(18))-{v}-adj[v]
            fv = faces(adj, sorted(B), 2)
            value = fv[2]-7*fv[1]+30
            tv = edge_count(adj, sorted(adj[v]))
            require(2*value == 2*a+16+q[v]*(q[v]-19)
                    +2*sum(q[u] for u in adj[v])-2*tv, "local formula")
            L.append(value)
        require(sum(L) == 3*b+4*a, "sum of vertex links")
    return samples


def type_one():
    cycle = {tuple(sorted((i, (i+1) % 6))) for i in range(6)}
    es = set(combinations(range(6), 2))-cycle
    es.update({(6, 7), (8, 9), (10, 11)})
    return graph(12, sorted(es))


def type_two():
    # Build the primal graph, then subdivide the actual edge {0,5}.
    # 0,...,4 form C5 and 5,6 are its suspension vertices.
    primal = {tuple(sorted((i, (i+1) % 5))) for i in range(5)}
    primal.update((i, s) for i in range(5) for s in (5, 6))
    adj = graph(7, sorted(primal))
    common = adj[0] & adj[5]
    primal.remove((0, 5))
    primal.update((v, 7) for v in common | {0, 5})
    # Subdivision followed by two suspensions: in the complement, add 2K2.
    es = set(combinations(range(8), 2))-primal
    es.update({(8, 9), (10, 11)})
    result = graph(12, sorted(es))
    expected_core = {(0, 2), (0, 3), (0, 5), (1, 3), (1, 4),
                     (2, 4), (2, 7), (3, 7), (5, 6), (6, 7)}
    require(es == expected_core | {(8, 9), (10, 11)}, "subdivided K4 core")
    return result


def audit_link(adj):
    f = faces(adj, range(12), 6)
    require(f[6] == 0, "link has dimension four")
    h = h_vector(f[:6], 5)
    require(h == [1, 7, 16, 16, 7, 1], "link gamma-polynomial 1+2t")
    counts = Counter()
    surviving_degree_patterns = Counter()
    for triple in combinations(range(12), 3):
        W = set(triple)
        C = set(range(12))-W
        counts["placements"] += 1
        # This test uses only common neighbors inside the link. Extra
        # neighbors outside it could only strengthen the obstruction.
        if any(v not in adj[u] and len(adj[u] & adj[v]) >= 2
               for u, v in combinations(sorted(C), 2)):
            counts["nonsuspension_pair_obstruction"] += 1
            continue
        capacity = sum(4-len(adj[w]) for w in W)
        if capacity < 5:
            counts["too_few_U_W_edges"] += 1
            continue
        counts["placements_after_pair_and_capacity"] += 1
        surviving_degree_patterns[str(sorted(len(adj[w]) for w in W))] += 1
        # Direct upper bound on L_w: its external neighbors all belong to
        # U and are quartic; discard the nonnegative triangle subtraction.
        upper = []
        for w in W:
            neighbor_degree_sum = sum(4 if v in W else 3 for v in adj[w])
            neighbor_degree_sum += 4*(4-len(adj[w]))
            upper.append(7+8+4*(4-19)//2+neighbor_degree_sum)
        require(min(upper) < 0, "a surviving quartic link must be negative")
        counts["negative_quartic_link_obstruction"] += 1
    return {"faces_including_empty": f[:6], "h": h,
            "complement_degrees": sorted(map(len, adj)),
            "placement_audit": dict(sorted(counts.items())),
            "surviving_W_internal_degrees": dict(surviving_degree_patterns)}


def main():
    considered, numerical = profiles()
    first = audit_link(type_one())
    second = audit_link(type_two())
    require(first["placement_audit"].get("placements_after_pair_and_capacity", 0) == 0,
            "type I eliminated before quartic link test")
    require(second["placement_audit"]["placements_after_pair_and_capacity"] == 16,
            "type II has sixteen labeled placements before final obstruction")
    result = {"status": "PASS", "degree_count_vectors": considered,
              "numerical_cases": numerical,
              "definition_level_graph_samples": audit_identities(),
              "type_I": first, "type_II": second,
              "scope": "Supplementary checks; human proof plus cited small-link classification."}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
