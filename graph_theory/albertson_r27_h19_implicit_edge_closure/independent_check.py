#!/usr/bin/env python3
"""Independent labelled-set reconstruction of the h=19 row-clique budgets."""

from hashlib import sha256
from itertools import combinations, product


N = 19


def clique_edges(vertices: tuple[int, ...]) -> frozenset[tuple[int, int]]:
    return frozenset(combinations(vertices, 2))


def form_c_candidates() -> tuple[object, ...]:
    base_vertices = tuple(range(9))
    base = clique_edges(base_vertices)
    candidates = []
    for row in combinations(range(N), 9):
        needed = clique_edges(row) - base
        if len(needed) <= 10:
            candidates.append((row, needed))

    by_external_order = {}
    for row, _ in candidates:
        outside = len(set(row) - set(base_vertices))
        by_external_order[outside] = by_external_order.get(outside, 0) + 1
    assert by_external_order == {0: 1, 1: 90}

    alternatives = [(row, needed) for row, needed in candidates if len(needed) == 8]
    budget_compatible_pairs = 0
    forced_k10_pairs = 0
    permitted_distinct_pairs = 0
    for (row_a, needed_a), (row_b, needed_b) in combinations(alternatives, 2):
        union = needed_a | needed_b
        if len(union) > 10:
            continue
        budget_compatible_pairs += 1
        vertices = set(row_a) | set(row_b)
        forced = base | union
        is_k10 = len(vertices) == 10 and clique_edges(tuple(sorted(vertices))) <= forced
        if is_k10:
            forced_k10_pairs += 1
        else:
            permitted_distinct_pairs += 1
    assert budget_compatible_pairs == forced_k10_pairs == 360
    assert permitted_distinct_pairs == 0
    return len(tuple(combinations(range(N), 9))), by_external_order, budget_compatible_pairs


def form_b_candidates() -> tuple[object, ...]:
    core_vertices = tuple(range(10))
    core = clique_edges(core_vertices)
    candidates = []
    for row in combinations(range(N), 8):
        needed = clique_edges(row) - core
        if len(needed) <= 11:
            candidates.append((row, needed))

    by_external_order = {}
    for row, _ in candidates:
        outside = len(set(row) - set(core_vertices))
        by_external_order[outside] = by_external_order.get(outside, 0) + 1
    assert by_external_order == {0: 45, 1: 1080}

    external_candidates = [
        (next(iter(set(row) - set(core_vertices))), needed)
        for row, needed in candidates
        if len(set(row) - set(core_vertices)) == 1
    ]
    distinct_external_pairs = 0
    budget_compatible_distinct_external_pairs = 0
    for (external_a, needed_a), (external_b, needed_b) in combinations(
        external_candidates, 2
    ):
        if external_a == external_b:
            continue
        distinct_external_pairs += 1
        if len(needed_a | needed_b) <= 11:
            budget_compatible_distinct_external_pairs += 1
    assert distinct_external_pairs == 518400
    assert budget_compatible_distinct_external_pairs == 0
    return (
        len(tuple(combinations(range(N), 8))),
        by_external_order,
        distinct_external_pairs,
    )


def scaffold_type_enumeration(c: int, rainbow_order: int) -> tuple[int, ...]:
    """Enumerate x-only/y-only/common types in the forced Kc scaffold."""
    counts = {0: 0, 1: 0}
    maxima = {0: 0, 1: 0}
    # 0 means x-only, 1 y-only, and 2 common.
    for types in product(range(3), repeat=c):
        common = types.count(2)
        if common > 1 or 0 not in types or 1 not in types:
            continue
        counts[common] += 1
        residual_edges = 1 - common
        possible = 2 + common + 2 * residual_edges
        maxima[common] = max(maxima[common], possible)
        assert possible < rainbow_order
    return counts[0], counts[1], maxima[0], maxima[1]


def main() -> None:
    c_rows = form_c_candidates()
    b_rows = form_b_candidates()
    scaffolds = (
        scaffold_type_enumeration(9, 9),
        scaffold_type_enumeration(10, 8),
    )
    record = repr((c_rows, b_rows, scaffolds))
    digest = sha256(record.encode("ascii")).hexdigest()
    assert digest == "44c7cc33fbf10947b91cdaf9621f27ec86d16b4f66b2fea8bc9f79d022e4792f"

    print("PASS independent Albertson h=19 implicit-edge reconstruction")
    print(f"form_C_row_enumeration={c_rows}")
    print(f"form_B_row_enumeration={b_rows}")
    print(f"scaffold_type_counts={scaffolds}")
    print(f"independent_sha256={digest}")


if __name__ == "__main__":
    main()
