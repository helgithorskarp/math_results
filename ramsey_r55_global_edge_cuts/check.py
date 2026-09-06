#!/usr/bin/env python3
"""Separate arithmetic reconstruction and literal graph/cut controls."""
from copy import deepcopy
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def validate(data):
    require([data[k] for k in ("order", "minimum_degree", "maximum_degree", "clique_number_at_most")]
            == [43, 18, 24, 4], "Scope")
    expected = []
    for a in range(1, 22):
        # Enumerate four-partite extremizers independently of the floor formula.
        capacity = max(sum(x*y for x, y in combinations(parts, 2))
                       for parts in combinations_with_replacement(range(a+1), 4) if sum(parts) == a)
        expected.append({"smaller_side": a, "internal_edges_at_most": capacity,
                         "boundary_at_least": sum([18]*a)-capacity-capacity})
    require(data["cuts"] == expected, "Cut arithmetic or coverage")
    require(data["both_sides_at_least_two_cut_lower"] == min(r["boundary_at_least"] for r in expected[1:]) == 34,
            "Two-side gap")
    require(data["both_sides_at_least_three_cut_lower"] == min(r["boundary_at_least"] for r in expected[2:]) == 48,
            "Three-side gap")
    require(data["vertex_boundary_upper"] == 24 < 34, "Ordinary gap")
    require(data["edge_boundary_upper"] == 2*24-2 == 46 < 48, "Restricted gap")
    require(data["all_minimum_edge_cuts_isolate_minimum_degree_vertex"] is True, "Ordinary conclusion")
    require(data["all_minimum_restricted_edge_cuts_isolate_minimum_edge_degree_edge"] is True, "Restricted conclusion")
    require(data["target_graph_found"] is False, "No target")
    return len(expected)


def components(n, edges, removed=0):
    adj = [set() for _ in range(n)]
    for index, (u, v) in enumerate(edges):
        if not (removed >> index & 1):
            adj[u].add(v)
            adj[v].add(u)
    unseen, answer = set(range(n)), []
    while unseen:
        v = min(unseen)
        unseen.remove(v)
        part, todo = {v}, [v]
        while todo:
            fresh = adj[todo.pop()] & unseen
            unseen -= fresh
            part |= fresh
            todo.extend(fresh)
        answer.append(part)
    return answer


def boundary(edges, side):
    return sum(1 << index for index, (u, v) in enumerate(edges) if (u in side) != (v in side))


def minima(entries):
    entries = set(entries)
    if not entries:
        return set()
    value = min(x.bit_count() for x in entries)
    return {x for x in entries if x.bit_count() == value}


def partition_cuts(n, edges):
    ordinary, restricted = [], []
    for word in range((1 << (n-1))-1):
        side = {0} | {v for v in range(1, n) if word >> (v-1) & 1}
        cut = boundary(edges, side)
        ordinary.append(cut)
        if min(map(len, components(n, edges, cut))) >= 2:
            restricted.append(cut)
    return minima(ordinary), minima(restricted)


def small_controls():
    graphs = connected = deletions = cut_checks = degree_checks = 0
    for n in range(2, 6):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            edges = [edge for index, edge in enumerate(pairs) if mask >> index & 1]
            graphs += 1
            degrees = [sum(v in e for e in edges) for v in range(n)]
            k5_free = n < 5 or len(edges) < 10
            for word in range(1, (1 << n)-1):
                side = {v for v in range(n) if word >> v & 1}
                cross = boundary(edges, side).bit_count()
                internal = sum(u in side and v in side for u, v in edges)
                require(cross == sum(degrees[v] for v in side)-2*internal, "Cut degree identity")
                if k5_free:
                    a = len(side)
                    require(internal <= 3*a*a//8, "Turan interpretation")
                    require(cross >= min(degrees)*a-2*(3*a*a//8), "Cut lower bound")
                cut_checks += 1
            for u, v in edges:
                require(boundary(edges, {u, v}).bit_count() == degrees[u]+degrees[v]-2,
                        "Edge-degree identity")
                if min(degrees) >= 3:
                    require(min(map(len, components(n, edges, boundary(edges, {u, v})))) >= 2,
                            "Isolating edge created singleton")
                degree_checks += 1
            if len(components(n, edges)) != 1:
                continue
            connected += 1
            ordinary, restricted = [], []
            for removed in range(1 << len(edges)):
                parts = components(n, edges, removed)
                deletions += 1
                if len(parts) > 1:
                    ordinary.append(removed)
                    if min(map(len, parts)) >= 2:
                        restricted.append(removed)
            exact = minima(ordinary), minima(restricted)
            require(exact == partition_cuts(n, edges), "Partition/deletion cut minima differ")
            for cut in exact[1]:
                require(len(components(n, edges, cut)) == 2, "Minimum restricted cut has extra component")
    return {"labeled_graphs_orders_2_to_5": graphs, "connected_graphs": connected,
            "literal_edge_deletions": deletions, "cut_identity_checks": cut_checks,
            "edge_degree_checks": degree_checks}


def fixtures():
    # K(2,2,2) has equality in the generic strict-gap test, and a minimum
    # restricted cut leaving two triangles. Replacing > by >= is invalid.
    edges = [(u, v) for u, v in combinations(range(6), 2) if u//2 != v//2]
    _, restricted = partition_cuts(6, edges)
    witness = boundary(edges, {0, 2, 4})
    require(witness in restricted and witness.bit_count() == 6, "Strict-gap counterexample")
    require(sorted(map(len, components(6, edges, witness))) == [3, 3], "Non-edge minimum cut")
    # K(2,2,2,2) is a nonvacuous positive finite control.
    edges8 = [(u, v) for u, v in combinations(range(8), 2) if u//2 != v//2]
    ordinary8, restricted8 = partition_cuts(8, edges8)
    require({x.bit_count() for x in ordinary8} == {6}, "K2222 ordinary")
    require({x.bit_count() for x in restricted8} == {10}, "K2222 restricted")
    require(all(sorted(map(len, components(8, edges8, x))) == [2, 6] for x in restricted8), "K2222 structure")
    # Complete cut-orbit enumeration for K21,22: a non-Ramsey graph
    # satisfying the localized K5-free degree-window theorem on43 vertices.
    ordinary, restricted, cases = [], [], 0
    for x in range(22):
        for y in range(23):
            a = x+y
            if a in (0, 43):
                continue
            cut = x*(22-y)+(21-x)*y
            s = min(a, 43-a)
            require(cut >= 18*s-2*(3*s*s//8), "K21,22 cut bound")
            ordinary.append((cut, x, y))
            if 0 < x < 21 and 0 < y < 22:
                restricted.append((cut, x, y))
            cases += 1
    require(min(c for c, _, _ in ordinary) == 21, "K21,22 ordinary")
    require(min(c for c, _, _ in restricted) == 41, "K21,22 restricted")
    require({(x, y) for c, x, y in restricted if c == 41} == {(1, 1), (20, 21)}, "K21,22 minimum edges")
    return {"strict_gap_counterexample_K222": True, "positive_K2222": True,
            "non_Ramsey_K21_22_cut_orbits": cases, "K21_22_lambda": 21, "K21_22_lambda_prime": 41}


def main():
    data = json.loads(Path(__file__).with_name("certificate.json").read_text())
    count = validate(data)
    mutants = [deepcopy(data) for _ in range(4)]
    mutants[0]["cuts"].pop()
    mutants[1]["cuts"][5]["internal_edges_at_most"] += 1
    mutants[2]["minimum_degree"] = 17
    mutants[3]["both_sides_at_least_three_cut_lower"] = 49
    for mutant in mutants:
        try:
            validate(mutant)
        except ValueError:
            continue
        raise ValueError("Accepted corrupted certificate")
    result = {"status": "VERIFIED_GLOBAL_EDGE_CUT_ARITHMETIC", "cut_rows": count,
              "certificate_mutations_rejected": len(mutants), **small_controls(), **fixtures(),
              "independent_peer_review": False, "formalization": False}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
