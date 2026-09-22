#!/usr/bin/env python3
"""Independent small-case audit for the perfect-or-pentagon product theorem.

The target package enumerates active constraints of the two C5 polytopes.
This checker instead starts from graph definitions: it exhausts all labelled
graphs through five vertices, all binary weights on the perfect ones, and
literal substitutions of small modules.  Exact integer and Fraction
arithmetic is used throughout; no graph or optimization package is imported.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


Graph = tuple[int, ...]  # adjacency bit masks


def graph_from_edges(n: int, edges: list[tuple[int, int]]) -> Graph:
    adjacency = [0] * n
    for u, v in edges:
        if not (0 <= u < v < n):
            raise ValueError("edges must have 0 <= u < v < n")
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    return tuple(adjacency)


def all_graphs(n: int):
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    for edge_mask in range(1 << len(pairs)):
        yield graph_from_edges(
            n, [edge for k, edge in enumerate(pairs) if edge_mask & (1 << k)]
        )


def induced(graph: Graph, vertices: tuple[int, ...]) -> Graph:
    index = {old: new for new, old in enumerate(vertices)}
    edges = []
    for i, u in enumerate(vertices):
        for v in vertices[i + 1 :]:
            if graph[u] & (1 << v):
                edges.append((index[u], index[v]))
    return graph_from_edges(len(vertices), edges)


def is_clique(graph: Graph, mask: int) -> bool:
    members = [i for i in range(len(graph)) if mask & (1 << i)]
    return all(graph[u] & (1 << v) for u, v in itertools.combinations(members, 2))


def is_stable(graph: Graph, mask: int) -> bool:
    members = [i for i in range(len(graph)) if mask & (1 << i)]
    return all(not (graph[u] & (1 << v)) for u, v in itertools.combinations(members, 2))


def alpha_omega(graph: Graph) -> tuple[int, int]:
    alpha = omega = 0
    for mask in range(1, 1 << len(graph)):
        size = mask.bit_count()
        if size > alpha and is_stable(graph, mask):
            alpha = size
        if size > omega and is_clique(graph, mask):
            omega = size
    return alpha, omega


def chromatic_number(graph: Graph) -> int:
    n = len(graph)
    stable = [is_stable(graph, mask) for mask in range(1 << n)]
    dp = [n + 1] * (1 << n)
    dp[0] = 0
    for mask in range(1, 1 << n):
        first = mask & -mask
        sub = mask
        best = n + 1
        while sub:
            if sub & first and stable[sub]:
                best = min(best, 1 + dp[mask ^ sub])
            sub = (sub - 1) & mask
        dp[mask] = best
    return dp[-1]


def is_perfect(graph: Graph) -> bool:
    n = len(graph)
    for mask in range(1, 1 << n):
        vertices = tuple(i for i in range(n) if mask & (1 << i))
        subgraph = induced(graph, vertices)
        if chromatic_number(subgraph) != alpha_omega(subgraph)[1]:
            return False
    return True


def c5() -> Graph:
    return graph_from_edges(5, [(i, (i + 1) % 5) for i in range(5) if i < (i + 1) % 5] + [(0, 4)])


def substitute(outer: Graph, modules: tuple[Graph, ...]) -> Graph:
    if len(outer) != len(modules) or any(len(module) == 0 for module in modules):
        raise ValueError("one nonempty module is required per outer vertex")
    offsets = []
    total = 0
    for module in modules:
        offsets.append(total)
        total += len(module)
    edges: list[tuple[int, int]] = []
    for offset, module in zip(offsets, modules, strict=True):
        for u in range(len(module)):
            for v in range(u + 1, len(module)):
                if module[u] & (1 << v):
                    edges.append((offset + u, offset + v))
    for i in range(len(outer)):
        for j in range(i + 1, len(outer)):
            if outer[i] & (1 << j):
                edges.extend(
                    (offsets[i] + u, offsets[j] + v)
                    for u in range(len(modules[i]))
                    for v in range(len(modules[j]))
                )
    return graph_from_edges(total, edges)


def weighted_max(graph: Graph, weights: tuple[int, ...], stable: bool) -> int:
    predicate = is_stable if stable else is_clique
    return max(
        sum(weights[i] for i in range(len(graph)) if mask & (1 << i))
        for mask in range(1 << len(graph))
        if predicate(graph, mask)
    )


def check_all_graphs_through_five() -> dict[str, int]:
    checked = perfect = nonperfect_five = 0
    for n in range(1, 6):
        for graph in all_graphs(n):
            checked += 1
            alpha, omega = alpha_omega(graph)
            if is_perfect(graph):
                perfect += 1
                # This is the integer small-case form of the imported
                # perfect-graph product bound; q<1 then gives n^q <= n.
                assert alpha * omega >= n
            else:
                assert n == 5
                assert all(row.bit_count() == 2 for row in graph)
                assert (alpha, omega) == (2, 2)
                nonperfect_five += 1
    assert (checked, perfect, nonperfect_five) == (1099, 1087, 12)
    return {
        "labelled_graphs_checked": checked,
        "perfect_graphs_checked": perfect,
        "labelled_c5_obstructions": nonperfect_five,
    }


def check_perfect_binary_weights() -> int:
    """Attack the a/b orientation in the Chvatal-polytope step exactly."""
    pairs = 0
    for n in range(1, 6):
        for graph in all_graphs(n):
            if not is_perfect(graph):
                continue
            stable_masks = [m for m in range(1 << n) if is_stable(graph, m)]
            clique_masks = [m for m in range(1 << n) if is_clique(graph, m)]
            a_max = [max((a & s).bit_count() for s in stable_masks) for a in range(1 << n)]
            b_max = [max((b & k).bit_count() for k in clique_masks) for b in range(1 << n)]
            for a in range(1 << n):
                for b in range(1 << n):
                    # Stronger than the desired p-power inequality for binary
                    # weights, and includes A=0 or B=0 boundary cases.
                    assert (a & b).bit_count() <= a_max[a] * b_max[b]
                    pairs += 1
    assert pairs == 1_053_220
    return pairs


def cycle_edges(step: int) -> tuple[tuple[int, int], ...]:
    return tuple(sorted({tuple(sorted((i, (i + step) % 5))) for i in range(5)}))


def cycle_polytope_candidates(step: int) -> set[tuple[Fraction, ...]]:
    edges = cycle_edges(step)
    candidates = {(Fraction(1, 2),) * 5}
    for mask in range(1 << 5):
        if all(not (mask & (1 << i) and mask & (1 << j)) for i, j in edges):
            candidates.add(tuple(Fraction(bool(mask & (1 << i))) for i in range(5)))
    assert len(candidates) == 12
    return candidates


def check_c5_reduction() -> dict[str, int]:
    original_edges = set(cycle_edges(1))
    a_vertices = cycle_polytope_candidates(2)
    b_vertices = cycle_polytope_candidates(1)
    half = (Fraction(1, 2),) * 5
    categories = {"integral_integral": 0, "half_integral": 0, "half_half": 0}
    for a in a_vertices:
        for b in b_vertices:
            assert all(x >= 0 for x in a + b)
            assert all(a[i] + a[j] <= 1 for i, j in cycle_edges(2))
            assert all(b[i] + b[j] <= 1 for i, j in cycle_edges(1))
            if a == half and b == half:
                # The identity 4^p=5 makes this the equality obstruction.
                categories["half_half"] += 1
            elif a == half or b == half:
                integral = b if a == half else a
                support_size = sum(bool(x) for x in integral)
                assert support_size <= 2  # gives 2*(1/2)^p < 1 for p>1
                categories["half_integral"] += 1
            else:
                a_support = {i for i, x in enumerate(a) if x}
                b_support = {i for i, x in enumerate(b) if x}
                assert all(tuple(sorted(e)) in original_edges for e in itertools.combinations(a_support, 2))
                assert all(tuple(sorted(e)) not in original_edges for e in itertools.combinations(b_support, 2))
                assert len(a_support & b_support) <= 1
                categories["integral_integral"] += 1
    assert categories == {
        "integral_integral": 121,
        "half_integral": 22,
        "half_half": 1,
    }

    # Exhaust all zero-one weight systems directly, including all 0/0
    # normalization boundaries.  With A,B in {0,1,2}, the four cases below
    # use only 2^p=sqrt(5)>2 and 4^p=5, so no floating arithmetic is needed.
    graph = c5()
    binary_pairs = 0
    for a in range(1 << 5):
        a_weights = tuple(bool(a & (1 << i)) for i in range(5))
        A = weighted_max(graph, a_weights, stable=True)
        for b in range(1 << 5):
            b_weights = tuple(bool(b & (1 << i)) for i in range(5))
            B = weighted_max(graph, b_weights, stable=False)
            terms = (a & b).bit_count()
            product = A * B
            if product == 0:
                assert terms == 0
            elif product == 1:
                assert terms <= 1
            elif product == 2:
                assert terms <= 2
            else:
                assert product == 4 and terms <= 5
            binary_pairs += 1
    assert binary_pairs == 1024
    return {**categories, "binary_boundary_pairs": binary_pairs}


def check_substitution_projection() -> dict[str, int]:
    one = graph_from_edges(1, [])
    empty_two = graph_from_edges(2, [])
    edge_two = graph_from_edges(2, [(0, 1)])
    modules_available = (one, empty_two, edge_two)
    outers = (
        graph_from_edges(2, []),
        graph_from_edges(2, [(0, 1)]),
        graph_from_edges(3, [(0, 1), (1, 2)]),
        graph_from_edges(4, [(0, 1), (1, 2), (2, 3), (0, 3)]),
        c5(),
    )
    assignments = 0
    largest_order = 0
    for outer in outers:
        assert is_perfect(outer) or outer == c5()
        for modules in itertools.product(modules_available, repeat=len(outer)):
            graph = substitute(outer, modules)
            alpha, omega = alpha_omega(graph)
            module_parameters = [alpha_omega(module) for module in modules]
            predicted_alpha = weighted_max(
                outer, tuple(x[0] for x in module_parameters), stable=True
            )
            predicted_omega = weighted_max(
                outer, tuple(x[1] for x in module_parameters), stable=False
            )
            assert (alpha, omega) == (predicted_alpha, predicted_omega)
            assignments += 1
            largest_order = max(largest_order, len(graph))
    assert assignments == 369 and largest_order == 10
    return {"module_assignments": assignments, "largest_substitution_order": largest_order}


def check_empty_module_and_sharp_boundaries() -> dict[str, int]:
    one = graph_from_edges(1, [])
    empty_two = graph_from_edges(2, [])
    edge_two = graph_from_edges(2, [(0, 1)])
    cycle = c5()
    prototypes = (
        substitute(cycle, (edge_two, one, one, one, one)),
        substitute(cycle, (empty_two, one, one, one, one)),
        substitute(graph_from_edges(2, []), (cycle, one)),
        substitute(graph_from_edges(2, [(0, 1)]), (cycle, one)),
    )
    induced_checked = 0
    for graph in prototypes:
        assert len(graph) == 6
        alpha, omega = alpha_omega(graph)
        assert alpha * omega >= len(graph)
        for mask in range(1, 1 << len(graph)):
            subgraph = induced(graph, tuple(i for i in range(len(graph)) if mask & (1 << i)))
            a, w = alpha_omega(subgraph)
            n = len(subgraph)
            # The only nonperfect induced case of order <=5 is C5, where
            # a*w=4=5^q.  Every other case has a*w>=n>=n^q.
            if is_perfect(subgraph):
                assert a * w >= n
            else:
                if n == 5:
                    assert (a, w) == (2, 2)
                else:
                    assert n == 6 and a * w >= n
            induced_checked += 1
    assert induced_checked == 252
    return {"six_vertex_prototypes": len(prototypes), "induced_subgraphs": induced_checked}


def main() -> None:
    result = {
        "c5_finite_reduction": check_c5_reduction(),
        "empty_module_and_sharp_boundaries": check_empty_module_and_sharp_boundaries(),
        "perfect_binary_weight_pairs": check_perfect_binary_weights(),
        "small_graphs": check_all_graphs_through_five(),
        "substitution_projection": check_substitution_projection(),
        "trust_boundary": (
            "small exact adversarial audit; the universal theorem still uses "
            "Chvatal's perfect-graph polytope theorem and the written convexity induction"
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
