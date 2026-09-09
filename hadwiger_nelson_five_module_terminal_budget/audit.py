#!/usr/bin/env python3
"""Independent degree-polynomial and complement-case audit."""

from itertools import combinations
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def degree_polynomial_count(n):
    """Count complements by coefficients of product_(i<j)(1+x_i*x_j)."""
    allowed = {n - 1 - d for d in (4, 5) if d < n}
    cap = max(allowed)
    states = {(0,) * n: 1}
    for a, b in combinations(range(n), 2):
        updated = dict(states)
        for degrees, count in states.items():
            if degrees[a] == cap or degrees[b] == cap:
                continue
            new = list(degrees)
            new[a] += 1
            new[b] += 1
            new = tuple(new)
            updated[new] = updated.get(new, 0) + count
        states = updated
    return sum(count for degrees, count in states.items() if set(degrees) <= allowed)


def maximum_matching(n, edges):
    adjacency = [set() for _ in range(n)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)

    def visit(remaining):
        if not remaining:
            return 0
        v = min(remaining)
        best = visit(remaining - {v})
        for w in adjacency[v] & remaining:
            best = max(best, 1 + visit(remaining - {v, w}))
        return best

    return visit(set(range(n)))


def independence_number(n, edges):
    edge_set = {tuple(sorted(e)) for e in edges}
    for size in range(n, 0, -1):
        if any(
            all(tuple(sorted((a, b))) not in edge_set for a, b in combinations(s, 2))
            for s in combinations(range(n), size)
        ):
            return size
    return 0


def integer_partitions(total, maximum=None):
    if total == 0:
        yield ()
        return
    if maximum is None or maximum > total:
        maximum = total
    for first in range(maximum, 0, -1):
        for rest in integer_partitions(total - first, first):
            yield (first,) + rest


def tutte_witness_cases():
    """Component orders possible after the degree bound, before alpha<=4."""
    cases = {}
    for s in range(9):
        possible = []
        for parts in integer_partitions(8 - s):
            odd = sum(p % 2 for p in parts)
            if odd <= s:
                continue
            # A component of order p has degree at most (p-1)+s.
            if any(p - 1 + s < 2 for p in parts):
                continue
            possible.append(parts)
        cases[str(s)] = possible
    require(cases["0"] == [(5, 3)], "S=0 component cases")
    require(cases["1"] == [], "S=1 must be impossible")
    require(
        cases["2"] == [(3, 1, 1, 1), (2, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1)],
        "S=2 component cases",
    )
    require(cases["3"] == [(1, 1, 1, 1, 1)], "S=3 component cases")
    require(all(not cases[str(s)] for s in range(4, 9)), "large S cases")
    return {key: [list(parts) for parts in value] for key, value in cases.items()}


def local_matching_checks():
    edges5 = list(combinations(range(5), 2))
    min_degree_two = matching_two = 0
    receipt = hashlib.sha256()
    for mask in range(1 << len(edges5)):
        edges = {edge for bit, edge in enumerate(edges5) if mask >> bit & 1}
        degrees = [sum(v in edge for edge in edges) for v in range(5)]
        if min(degrees) < 2:
            continue
        min_degree_two += 1
        matching = maximum_matching(5, edges)
        require(matching >= 2, "five-vertex minimum-degree-two matching failure")
        matching_two += 1
        receipt.update(f"{mask}:{matching}\n".encode())

    edges6 = list(combinations(range(6), 2))
    low_matching = alpha_at_most_four = triangle_core = 0
    for mask in range(1 << len(edges6)):
        edges = {edge for bit, edge in enumerate(edges6) if mask >> bit & 1}
        if maximum_matching(6, edges) > 1:
            continue
        low_matching += 1
        if independence_number(6, edges) > 4:
            continue
        alpha_at_most_four += 1
        nonisolated = {v for edge in edges for v in edge}
        require(
            len(nonisolated) == 3
            and len(edges) == 3
            and all(tuple(sorted(e)) in edges for e in combinations(nonisolated, 2)),
            "pairwise-intersecting edge classification",
        )
        triangle_core += 1
    return {
        "five_vertex_graphs_examined": 1 << 10,
        "five_vertex_min_degree_two_graphs": min_degree_two,
        "all_have_matching_size_at_least_two": matching_two,
        "five_vertex_receipt_sha256": receipt.hexdigest(),
        "six_vertex_graphs_examined": 1 << 15,
        "six_vertex_matching_number_at_most_one": low_matching,
        "also_independence_number_at_most_four": alpha_at_most_four,
        "all_such_graphs_are_triangle_plus_isolates": triangle_core,
    }


def run():
    counts = {str(n): degree_polynomial_count(n) for n in range(5, 9)}
    require(list(counts.values()) == [1, 76, 6912, 848932], "independent counts")
    return {
        "degree_polynomial_counts": counts,
        "tutte_eight_vertex_component_cases": tutte_witness_cases(),
        "local_sublemmas": local_matching_checks(),
        "classical_input": "Tutte's one-factor theorem",
        "classical_source": "https://doi.org/10.1112/jlms/s1-22.2.107",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
