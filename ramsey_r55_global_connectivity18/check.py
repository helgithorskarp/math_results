#!/usr/bin/env python3
"""Different component-cover enumeration and direct small-graph controls.

This audits finite arithmetic and translations, not the imported R(4,5)
theorem or the universal written proof in a proof assistant.
"""
import argparse
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def cover():
    types = [(size, alpha) for size in range(1, 25) for alpha in range(1, 4)
             if alpha <= size <= {1: 4, 2: 13, 3: 24}[alpha]]
    result = set()
    def visit(parts, start, order, alpha):
        if len(parts) >= 2 and 26 <= order <= 43:
            separator = 43-order
            if all(size+separator >= 19 for size, _ in parts):
                result.add((separator, tuple(parts)))
        if len(parts) == 4:
            return
        for index in range(start, len(types)):
            size, value = types[index]
            if order+size <= 43 and alpha+value <= 4:
                visit(parts+[(size, value)], index, order+size, alpha+value)
    visit([], 0, 0, 0)
    return result


def validate(certificate):
    require(certificate["vertices"] == 43 and certificate["minimum_degree_at_least"] == 18, "Scope")
    require(certificate["clique_number_at_most"] == certificate["independence_number_at_most"] == 4, "Ramsey scope")
    require(certificate["separator_orders"] == [0, 17], "Separator range")
    require(certificate["component_order_bounds_by_independence"] == {"1": 4, "2": 13, "3": 24}, "Ramsey order bounds")
    rows = certificate["rows"]
    supplied = {(row["separator"], tuple(map(tuple, row["components"]))) for row in rows}
    require(len(supplied) == len(rows) and supplied == cover(), "Incomplete or repeated cover")
    for row in rows:
        k = row["separator"]
        parts = row["components"]
        if row["rule"] == "clique_common_neighbors":
            a = row["clique_order"]
            require([a, 1] in parts and 2 <= a <= 4, "Not a clique component")
            # Each member misses at most k-(18-(a-1)) separator vertices.
            common = k-a*(k-18+a-1)
            limit = [None, 24, 13, 4, 0][a]
            require(row["common_neighbor_lower"] == common and row["common_neighbor_upper"] == limit,
                    "Wrong common-neighbor certificate")
            require(common > limit, "No clique contradiction")
        elif row["rule"] == "two_saturated_components":
            require(parts == [[13, 2], [13, 2]] and k == 17, "Wrong saturated boundary")
            require(row["outside_vertex_exists"] is True, "Missing outside vertex")
            require(row["red_neighbors_in_each_at_most"] == 8, "R(4,3) bound")
            require(row["blue_neighbors_in_each_at_least"] == 13-8, "Blue difference")
            require(row["blue_pair_in_each"] is True and 13-8 > 4, "Missing blue pair")
        else:
            raise ValueError("Unknown rule")
    require(certificate["whole_separator_branch_excluded"] is True, "Conclusion")
    require(certificate["classifies_separators_of_order18"] is False, "Overstated scope")
    return len(rows)


def components(adj, remaining):
    answer = []
    while remaining:
        seed = next(iter(remaining))
        part, todo = {seed}, [seed]
        remaining.remove(seed)
        while todo:
            vertex = todo.pop()
            fresh = adj[vertex] & remaining
            remaining -= fresh
            part |= fresh
            todo.extend(fresh)
        answer.append(part)
    return answer


def alpha(adj, subset):
    vertices = sorted(subset)
    for size in range(len(vertices), -1, -1):
        if any(all(v not in adj[u] for u, v in combinations(choice, 2))
               for choice in combinations(vertices, size)):
            return size
    raise RuntimeError("No empty independent set")


def clique(adj, subset):
    return all(v in adj[u] for u, v in combinations(sorted(subset), 2))


def controls():
    graphs = separators = clique_checks = outside_checks = 0
    for n in range(1, 6):
        pairs = list(combinations(range(n), 2))
        vertices = set(range(n))
        for mask in range(1 << len(pairs)):
            adj = [set() for _ in range(n)]
            for index, (u, v) in enumerate(pairs):
                if mask >> index & 1:
                    adj[u].add(v)
                    adj[v].add(u)
            if alpha(adj, vertices) >= 5 or any(clique(adj, set(q)) for q in combinations(range(n), 5)):
                continue
            graphs += 1
            degree = min(map(len, adj))
            for removed in range(1 << n):
                separator = {v for v in range(n) if removed >> v & 1}
                parts = components(adj, vertices-separator)
                if len(parts) < 2:
                    continue
                separators += 1
                require(sum(alpha(adj, part) for part in parts) == alpha(adj, vertices-separator),
                        "Independence not additive")
                require(sum(alpha(adj, part) for part in parts) <= 4, "Independence budget")
                for part in parts:
                    require(all(adj[v] <= part | separator for v in part), "Not a component")
                    a, k = len(part), len(separator)
                    require(a-1+k >= degree, "Component degree inequality")
                    if clique(adj, part):
                        common = set.intersection(*(adj[v] & separator for v in part))
                        require(len(common) >= a*(degree-a+1)-(a-1)*k, "Common-neighbor lower bound")
                        require(len(common) <= [None, 24, 13, 4, 0][a], "Common-neighbor upper bound")
                        clique_checks += 1
                # If both anticomplete parts have a blue pair missed by z,
                # those two pairs together with z would be a blue K5.
                for left, right in combinations(parts, 2):
                    for z in separator:
                        blue_left, blue_right = left-adj[z], right-adj[z]
                        require(clique(adj, blue_left) or clique(adj, blue_right), "Outside-vertex obstruction")
                        outside_checks += 1
    # Dropping the no-K5 condition is unsound: K19 disjoint union K24.
    n = 43
    bad = [{v for v in range(n) if v != u and (u < 19) == (v < 19)} for u in range(n)]
    require(min(map(len, bad)) == 18 and len(components(bad, set(range(n)))) == 2,
            "Negative fixture")
    require(clique(bad, set(range(5))), "Negative fixture must violate Ramsey")
    return {"small_ramsey_graphs": graphs, "separator_instances": separators,
            "clique_common_neighbor_checks": clique_checks, "outside_vertex_checks": outside_checks,
            "non_Ramsey_counterexample_rejected": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path, nargs="?", default=Path(__file__).with_name("certificate.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    count = validate(certificate)
    mutants = []
    missing = deepcopy(certificate)
    missing["rows"].pop()
    mutants.append(missing)
    bound = deepcopy(certificate)
    bound["rows"][0]["common_neighbor_upper"] = 100
    mutants.append(bound)
    saturated = deepcopy(certificate)
    saturated["rows"][-1]["red_neighbors_in_each_at_most"] = 9
    mutants.append(saturated)
    scope = deepcopy(certificate)
    scope["separator_orders"] = [0, 18]
    mutants.append(scope)
    for mutant in mutants:
        try:
            validate(mutant)
        except ValueError:
            continue
        raise ValueError("Certificate mutation accepted")
    result = {"status": "VERIFIED_SEPARATOR18_ARITHMETIC", "cover_rows": count,
              "certificate_mutations_rejected": len(mutants), **controls(),
              "formal_proof_assistant_check": False, "independent_peer_review": False}
    text = json.dumps(result, indent=2)+"\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
