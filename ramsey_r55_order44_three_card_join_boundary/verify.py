"""Check the serialized fixture by literal monochromatic-subset tests.

No generator import, solver, graph catalogue, or external package is used.
This verifies the finite fixture; the all-s and all-good44 proofs are written.
"""

import argparse
from itertools import combinations, product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def monochromatic(matrix, vertices, color):
    return all(matrix[u][v] == color for u, v in combinations(vertices, 2))


def bad_sets(matrix, s):
    bad = []
    for vertices in combinations(range(len(matrix)), s):
        if monochromatic(matrix, vertices, True):
            bad.append(("red", list(vertices)))
        elif monochromatic(matrix, vertices, False):
            bad.append(("blue", list(vertices)))
    return bad


def clique_maximum(matrix, color):
    for k in range(len(matrix), 0, -1):
        if any(monochromatic(matrix, vertices, color)
               for vertices in combinations(range(len(matrix)), k)):
            return k
    return 0


def check(data):
    require(data["schema"] == "physical-star-arc-control-v1", "schema")
    s, n = data["s"], data["core_order"]
    require(type(s) is int and s >= 5 and n == 4 * (s - 2), "parameters")
    k = s - 2
    matrix = [[False] * n for _ in range(n)]
    edges = data["red_edges"]
    require(edges == sorted(edges), "edge ordering")
    seen = set()
    for edge in edges:
        require(len(edge) == 2 and all(type(v) is int for v in edge), "edge form")
        u, v = edge
        require(0 <= u < v < n and (u, v) not in seen, "simple core")
        seen.add((u, v))
        matrix[u][v] = matrix[v][u] = True
    require(len(edges) == 2 * k * k + 4 * k, "core edge count")
    require(not bad_sets(matrix, s), "core must be good")
    omega, alpha = clique_maximum(matrix, True), clique_maximum(matrix, False)
    require((omega, alpha) == (max(k, 4), k), "core clique numbers")

    domains = data["domains"]
    require(len(domains) == 3 and all(len(d) == 2 for d in domains), "domains")
    for domain in domains:
        require(domain[0] != domain[1], "two distinct values required")
        for star in domain:
            require(star == sorted(set(star)) and
                    all(type(v) is int and 0 <= v < n for v in star), "star")
    root_red = {tuple(e) for e in data["root_red_edges"]}
    require(root_red == {(0, 1), (1, 2)}, "root must be the specified red P3")

    def extend(roots, stars):
        m = n + len(roots)
        result = [[False] * m for _ in range(m)]
        for u in range(n):
            for v in range(n):
                result[u][v] = matrix[u][v]
        for j, star in enumerate(stars):
            for v in star:
                result[v][n + j] = result[n + j][v] = True
        for i, j in combinations(range(len(roots)), 2):
            if (roots[i], roots[j]) in root_red:
                result[n + i][n + j] = result[n + j][n + i] = True
        return result

    for root, domain in enumerate(domains):
        for star in domain:
            require(not bad_sets(extend([root], [star]), s), "unary graph")
    relations, pair_bad_counts = [], []
    for i, j in combinations(range(3), 2):
        relation, counts = [], []
        for u in range(2):
            row, row_counts = [], []
            for v in range(2):
                failures = bad_sets(extend([i, j], [domains[i][u], domains[j][v]]), s)
                row.append(not failures)
                row_counts.append(len(failures))
            relation.append(row)
            counts.append(row_counts)
        relations.append(relation)
        pair_bad_counts.append(counts)
    require(relations == data["expected_pair_relations"], "literal pair relations")
    require(all(all(any(row) for row in relation) and
                all(any(relation[i][j] for i in range(2)) for j in range(2))
                for relation in relations), "arc consistency")
    triples = list(product(range(2), repeat=3))
    compatible = [list(t) for t in triples
                  if relations[0][t[0]][t[1]] and relations[1][t[0]][t[2]]
                  and relations[2][t[1]][t[2]]]
    require(compatible == [], "negative prescribed-domain join")
    witnesses = data["full_failure_witnesses"]
    require([w["bits"] for w in witnesses] == [list(t) for t in triples], "coverage")
    full_bad_counts = []
    for t, witness in zip(triples, witnesses):
        graph = extend([0, 1, 2], [domains[i][t[i]] for i in range(3)])
        color, vertices = witness["color"], witness["vertices"]
        require(color in ("red", "blue") and len(vertices) == s and
                len(set(vertices)) == s and all(0 <= v < n + 3 for v in vertices),
                "witness form")
        require(monochromatic(graph, vertices, color == "red"), "literal witness")
        full_bad_counts.append(len(bad_sets(graph, s)))
    positive_stars = data["positive_stars_outside_prescribed_domains"]
    require(positive_stars == [domains[0][0], [], domains[2][1]], "positive control")
    require([] not in domains[1], "positive control must leave the restricted domain")
    require(not bad_sets(extend([0, 1, 2], positive_stars), s), "positive full graph")
    return {
        "status": "PASS",
        "s": s,
        "core_order": n,
        "core_red_edges": len(edges),
        "core_clique_number": omega,
        "core_independence_number": alpha,
        "unary_domain_occurrences_checked": 6,
        "distinct_unary_stars": len({tuple(star) for domain in domains for star in domain}),
        "pair_order": [[0, 1], [0, 2], [1, 2]],
        "pair_relations": relations,
        "pair_monochromatic_s_set_counts": pair_bad_counts,
        "arc_consistent": True,
        "domain_values_surviving_arc_consistency": 6,
        "valid_pair_graphs": sum(sum(sum(row) for row in r) for r in relations),
        "prescribed_domain_triples_checked": 8,
        "valid_prescribed_domain_triples": 0,
        "full_monochromatic_s_set_counts": full_bad_counts,
        "positive_full_graph_order": n + 3,
        "positive_control_uses_an_omitted_star": True,
        "endpoint_graph_verified": False,
        "role": "literal finite controls for written proofs; no order44 decision",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = check(json.loads(args.input.read_text()))
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PHYSICAL_STAR_CONTROL_VERIFIED")


if __name__ == "__main__":
    main()
