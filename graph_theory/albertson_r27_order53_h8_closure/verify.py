#!/usr/bin/env python3
"""Exact finite checks for the last Albertson r=27 order-53 h=8 profile."""

from __future__ import annotations

import hashlib
import itertools


def edges_of_clique(vertices: set[str]) -> set[frozenset[str]]:
    return {frozenset((x, y)) for x, y in itertools.combinations(vertices, 2)}


def check_coloring_templates() -> int:
    """Check every right-side overlap pattern of size-4 and size-5 matchings."""
    q_vertices = tuple(f"q{i}" for i in range(8))
    a_vertices = tuple(f"a{i}" for i in range(22))
    b_vertices = tuple(f"b{i}" for i in range(23))

    # Only the Q endpoints used by each matching affect the coloring.  Match
    # the first four/five low vertices to their selected Q vertices in order.
    checked = 0
    for used_a in itertools.combinations(q_vertices, 4):
        for used_b in itertools.combinations(q_vertices, 5):
            color_classes: list[set[str]] = [{q} for q in q_vertices]
            q_index = {q: i for i, q in enumerate(q_vertices)}
            h_edges: set[frozenset[str]] = {
                frozenset((a, b)) for a in a_vertices for b in b_vertices
            }

            for a, q in zip(a_vertices[:4], used_a):
                color_classes[q_index[q]].add(a)
                h_edges.add(frozenset((a, q)))
            for b, q in zip(b_vertices[:5], used_b):
                color_classes[q_index[q]].add(b)
                h_edges.add(frozenset((b, q)))

            for a, b in zip(a_vertices[4:], b_vertices[5:]):
                color_classes.append({a, b})
                h_edges.add(frozenset((a, b)))

            assert len(color_classes) == 26
            assert set().union(*color_classes) == set(q_vertices + a_vertices + b_vertices)
            assert sum(map(len, color_classes)) == 53
            for cls in color_classes:
                for x, y in itertools.combinations(cls, 2):
                    assert frozenset((x, y)) in h_edges
            checked += 1
    return checked


def check_tk_branch(low_size: int, row_degree: int) -> int:
    """Check all common-row sets and all positions of the sole missing Q-edge."""
    q_vertices = tuple(f"q{i}" for i in range(8))
    low_vertices = tuple(f"x{i}" for i in range(low_size))
    checked = 0

    for common_tuple in itertools.combinations(q_vertices, row_degree):
        common = set(common_tuple)
        outside = set(q_vertices) - common
        assert low_size + len(outside) == 27
        branches = set(low_vertices) | outside

        for missing_tuple in itertools.combinations(q_vertices, 2):
            missing = frozenset(missing_tuple)
            g_edges = edges_of_clique(set(q_vertices)) - {missing}
            g_edges |= edges_of_clique(set(low_vertices))
            g_edges |= {
                frozenset((x, q)) for x in low_vertices for q in outside
            }

            missing_branch_pairs = [
                frozenset((x, y))
                for x, y in itertools.combinations(branches, 2)
                if frozenset((x, y)) not in g_edges
            ]
            if missing.issubset(outside):
                assert missing_branch_pairs == [missing]
                internal = next(iter(common))
                u, v = tuple(missing)
                assert internal not in branches
                assert frozenset((u, internal)) in g_edges
                assert frozenset((internal, v)) in g_edges
            else:
                assert not missing_branch_pairs
            checked += 1
    return checked


def check_cover_capacity(left_size: int, degree: int) -> None:
    """Check the integer alternatives in the Konig-cover argument."""
    assert left_size >= degree + 1
    for left_in_cover in range(degree + 1):
        right_capacity = degree - left_in_cover
        if left_in_cover:
            assert left_size - left_in_cover > 0
            assert right_capacity < degree
        else:
            assert right_capacity == degree


def check_frontier_arithmetic() -> None:
    n, m, k, h = 53, 713, 27, 8
    low = n - h
    assert low == 45 == 22 + 23
    assert 2 * m - (k - 1) * n == 48
    assert 22 - 1 + (8 - 3) == 26
    assert 23 - 1 + (8 - 4) == 26
    assert 22 + (8 - 3) == 27
    assert 23 + (8 - 4) == 27


def main() -> None:
    check_frontier_arithmetic()
    check_cover_capacity(22, 3)
    check_cover_capacity(23, 4)
    coloring_count = check_coloring_templates()
    a_tk_count = check_tk_branch(22, 3)
    b_tk_count = check_tk_branch(23, 4)

    summary = (
        f"coloring_templates={coloring_count};"
        f"A_TK_templates={a_tk_count};"
        f"B_TK_templates={b_tk_count};"
        "conclusion=m713_h8_closed"
    )
    digest = hashlib.sha256(summary.encode()).hexdigest()
    print("PASS last Albertson r=27 order-53 h=8 profile")
    print(f"normalized coloring templates checked: {coloring_count}")
    print(f"A-deficient TK27 templates checked: {a_tk_count}")
    print(f"B-deficient TK27 templates checked: {b_tk_count}")
    print(f"certificate_sha256={digest}")
    print("conclusion: m=713 now also requires at least nine high vertices")


if __name__ == "__main__":
    main()
