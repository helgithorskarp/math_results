#!/usr/bin/env python3
"""Solver-free audit of the incidence lemma and its sharpness fixture."""
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def arithmetic():
    m = (13 * 20 + 30 * 21) // 2
    mono = comb(43, 3) - (13 * 20 * 22 + 30 * 21 * 21) // 2
    red_caps = 13 * 93 + 30 * 100
    blue_caps = 13 * 107 + 30 * 100
    total_excess = red_caps + blue_caps - 3 * mono
    possible_red_excess = [s for s in range(total_excess + 1) if (red_caps - s) % 3 == 0]
    require((m, mono, red_caps, blue_caps, total_excess) == (445, 2866, 4209, 4391, 2), "arithmetic mismatch")
    require(possible_red_excess == [0], "red exactness not forced")
    for d, red_cap, blue_cap in ((20, 93, 107), (21, 100, 100)):
        for a in range(14):
            local_total = comb(42 - d, 2) - m + 21 * d - a
            blue_count = local_total - red_cap
            require(local_total == 206 - a, "local identity mismatch")
            require(blue_cap - blue_count == a - 6, "wrong blue excess")
    require(13 * 20 - 43 * 6 == 2, "wrong incidence budget")
    return {"red_edges": m, "monochromatic_triangles": mono, "red_triangles": red_caps // 3,
            "blue_triangles": mono - red_caps // 3, "total_excess": total_excess,
            "central_exact_anchor_lower_bound": 28, "anchor_cross_edges": 445 - 21 - 100 - 110}


def fixed_graph_audit():
    results = []
    for f, e in ((1, 1), (4, 1), (4, 4)):
        pairs = list(combinations(range(f), 2))
        congruent = 0
        survivors = 0
        residue_histogram = Counter()
        for mask in range(1 << len(pairs)):
            degree = [0] * f
            exceptional_neighbors = [0] * f
            for bit, (u, v) in enumerate(pairs):
                if (mask >> bit) & 1:
                    degree[u] += 1
                    degree[v] += 1
                    exceptional_neighbors[u] += v < e
                    exceptional_neighbors[v] += u < e
            if any(degree[v] % 3 != (2 if v < e else 0) for v in range(f)):
                continue
            congruent += 1
            residue_sum = sum(x % 3 for x in exceptional_neighbors)
            residue_histogram[residue_sum] += 1
            survivors += residue_sum == 2
        results.append({"fixed_vertices": f, "fixed_exceptional": e,
                        "graphs_scanned": 1 << len(pairs), "degree_congruent": congruent,
                        "residue_sums": dict(sorted(residue_histogram.items())), "survivors": survivors})
    require([r["degree_congruent"] for r in results] == [0, 0, 3], "wrong fixed-graph counts")
    require(all(r["survivors"] == 0 for r in results), "forbidden fixed graph survived")
    return results


def fixture_audit(path):
    rows = [tuple(map(int, line.split())) for line in path.read_text().splitlines()]
    require(rows[0] == (43, 445), "wrong fixture header")
    edges = rows[1:]
    require(len(edges) == 445 and edges == sorted(set(edges)), "bad edge list")
    require(all(len(p) == 2 and 0 <= p[0] < p[1] < 43 for p in edges), "invalid edge")
    adjacency = [set() for _ in range(43)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    degrees = [len(neighbors) for neighbors in adjacency]
    require(Counter(degrees) == {20: 13, 21: 30}, "wrong degree profile")
    exceptional = {v for v, degree in enumerate(degrees) if degree == 20}
    a = [len(neighbors & exceptional) for neighbors in adjacency]
    require(min(a) >= 6 and sum(x - 6 for x in a) == 2, "wrong incidence budget")
    permutation = [3 * (v // 3) + (v + 1) % 3 if v < 36 else v for v in range(43)]
    require(len(set(permutation)) == 43, "not a permutation")
    require(all(permutation[permutation[permutation[v]]] == v for v in range(43)), "order does not divide three")
    require(sum(permutation[v] != v for v in range(43)) == 36, "wrong moving count")
    mapped_edges = {tuple(sorted((permutation[u], permutation[v]))) for u, v in edges}
    require(mapped_edges == set(edges), "not an automorphism")
    witness = [0, 1, 2, 40, 41]
    require(all(v not in adjacency[u] for u, v in combinations(witness, 2)), "blue K5 witness invalid")
    red_local = [sum(v in adjacency[u] for u, v in combinations(sorted(neighbors), 2))
                 for neighbors in adjacency]
    failures = [v for v in range(43) if red_local[v] != (93 if v in exceptional else 100)]
    require(bool(failures), "fixture unexpectedly satisfies every local red equality")
    return {"vertices": 43, "edges": len(edges), "degree_profile": dict(sorted(Counter(degrees).items())),
            "exceptional_vertices": sorted(exceptional), "moving_3cycles": 12,
            "fixed_vertices": 7, "incidence_excess": [[v, x - 6] for v, x in enumerate(a) if x > 6],
            "independent_five_set": witness, "red_triangle_equality_failures": failures,
            "is_ramsey_graph": False}


def compatible_counts():
    counts = []
    for k in range(10, 13):
        for q in range(1, 5):
            exceptional_fixed = 13 - 3 * q
            central_fixed = 30 - 3 * (k - q)
            if exceptional_fixed >= 0 and central_fixed >= 3:
                counts.append({"moving_cycles": k, "exceptional_moving_cycles": q,
                               "fixed_exceptional": exceptional_fixed, "fixed_central": central_fixed})
    require(len(counts) == 9, "wrong degree-class count patterns")
    return counts


def incompatible_label_audit():
    # Compute the orbits of the prior k=10 action and compare actual prescribed
    # degrees from the independently fixed OPB labeling.
    sigma = [3 * (v // 3) + (v + 1) % 3 if v < 30 else v for v in range(43)]
    degree = [20 if v < 13 else 21 for v in range(43)]
    unseen = set(range(43))
    bad = []
    while unseen:
        v = min(unseen)
        orbit = []
        while v not in orbit:
            orbit.append(v)
            unseen.remove(v)
            v = sigma[v]
        if len({degree[w] for w in orbit}) > 1:
            bad.append(orbit)
    require(bad == [[12, 13, 14]], "unexpected label incompatibility")
    return bad


def audit():
    root = Path(__file__).resolve().parent
    from construct_fixture import construct
    _, constructed = construct()
    expected_bytes = "43 445\n" + "".join(f"{u} {v}\n" for u, v in sorted(constructed))
    require((root / "degree_incidence43.edges").read_text() == expected_bytes, "constructor/fixture disagreement")
    return {"arithmetic": arithmetic(), "fixed_graph_audit": fixed_graph_audit(),
            "fixture": fixture_audit(root / "degree_incidence43.edges"),
            "necessary_degree_class_counts": compatible_counts(),
            "naively_combined_labelings_incompatible_orbits": incompatible_label_audit(),
            "m214_moving_3cycle_range_with_imported_minimum": [10, 12],
            "full_opb_solver_verdict": "NOT_RUN", "target_graph_found": False}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
