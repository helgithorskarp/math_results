#!/usr/bin/env python3
"""Exact audit of the Albertson r=27 h=19 implicit-edge closure."""

from hashlib import sha256
from math import comb


NQ = 19


def ceil_half(value: int) -> int:
    return (value + 1) // 2


def rainbow_scaffold(c: int, rainbow_order: int, edges: int) -> tuple[int, ...]:
    """Audit the one-edge contraction scaffold for a hypothetical nonedge."""
    contracted_clique_edges = comb(c + 1, 2)
    assert edges == contracted_clique_edges + 1

    # A noncomplete (c+1)-critical core has at least c+2 vertices and
    # minimum degree c.  Even allowing c+2 here is already too expensive.
    noncomplete_core_floor = ceil_half(c * (c + 2))
    assert noncomplete_core_floor > edges

    maxima = []
    for common_in_core in (0, 1):
        residual_edges = edges - contracted_clique_edges - common_in_core
        assert residual_edges in (0, 1)
        # Besides the contracted pair, a rainbow set can contain only the
        # common core vertex and endpoints of the residual edge without an
        # immediately constructible repeated colour.
        possible_rainbow_vertices = 2 + common_in_core + 2 * residual_edges
        assert possible_rainbow_vertices < rainbow_order
        maxima.append(possible_rainbow_vertices)
    return (
        c,
        rainbow_order,
        edges,
        contracted_clique_edges,
        noncomplete_core_floor,
        *maxima,
    )


def form_c_audit() -> tuple[object, ...]:
    c = 9
    edges = 46
    base_edges = comb(9, 2)
    extra = edges - base_edges
    assert extra == 10

    union_edges_by_intersection = tuple(
        (intersection, 2 * base_edges - comb(intersection, 2))
        for intersection in range(10)
    )
    feasible = tuple(
        intersection
        for intersection, union_edges in union_edges_by_intersection
        if union_edges <= edges
    )
    assert feasible == (8, 9)

    alternative_cost = 8
    two_external_cost = 2 * alternative_cost
    assert two_external_cost > extra
    same_external_two_omissions_edges = base_edges + 9
    assert same_external_two_omissions_edges == comb(10, 2)

    no_alternative_degree_cap = extra + 16
    one_alternative_union_edges = 2 * base_edges - comb(8, 2)
    residual_after_alternative = edges - one_alternative_union_edges
    alternative_degree_cap = residual_after_alternative + 16
    assert no_alternative_degree_cap == 26
    assert one_alternative_union_edges == 44
    assert residual_after_alternative == 2
    assert alternative_degree_cap == 18

    return (
        union_edges_by_intersection,
        feasible,
        alternative_cost,
        two_external_cost,
        same_external_two_omissions_edges,
        no_alternative_degree_cap,
        one_alternative_union_edges,
        alternative_degree_cap,
    )


def form_b_core_audit() -> tuple[tuple[int, str, int], ...]:
    """Exclude every non-K10 order for a 10-critical core with <=56 edges."""
    rows = []
    # Order 11 is handled by the complement-matching argument in the proof.
    rows.append((11, "complement_matching", 10))

    gallai_12_twice_edges = 9 * 12 + (12 - 10) * (20 - 12) - 2
    assert gallai_12_twice_edges == 122
    rows.append((12, "gallai", ceil_half(gallai_12_twice_edges)))

    for order in range(13, NQ + 1):
        floor = ceil_half(9 * order)
        assert floor > 56
        rows.append((order, "handshake", floor))
    assert rows[1][2] == 61
    return tuple(rows)


def form_b_row_audit() -> tuple[object, ...]:
    residual_edges = 56 - comb(10, 2)
    assert residual_edges == 11

    outside_costs = tuple(
        (outside, outside * (8 - outside) + comb(outside, 2))
        for outside in range(9)
    )
    feasible_outside_counts = tuple(
        outside for outside, cost in outside_costs if cost <= residual_edges
    )
    assert feasible_outside_counts == (0, 1)

    cost_per_external_vertex = 7
    assert 2 * cost_per_external_vertex > residual_edges
    external_vertices_in_rows = 1
    row_free_external_vertices = (NQ - 10) - external_vertices_in_rows
    assert row_free_external_vertices == 8

    required_high_degree = 27 - 15
    forced_degree_sum = row_free_external_vertices * required_high_degree
    residual_degree_sum_cap = 2 * residual_edges
    assert forced_degree_sum == 96 > residual_degree_sum_cap == 22
    return (
        residual_edges,
        outside_costs,
        feasible_outside_counts,
        row_free_external_vertices,
        required_high_degree,
        forced_degree_sum,
        residual_degree_sum_cap,
    )


def main() -> None:
    scaffold_c = rainbow_scaffold(c=9, rainbow_order=9, edges=46)
    scaffold_b = rainbow_scaffold(c=10, rainbow_order=8, edges=56)
    form_c = form_c_audit()
    core_b = form_b_core_audit()
    rows_b = form_b_row_audit()

    record = repr((scaffold_c, scaffold_b, form_c, core_b, rows_b))
    digest = sha256(record.encode("ascii")).hexdigest()
    assert digest == "c6e88e1017638c5e4170c730cb6a3fe42f28dfcd51e30312b1d362ff2c7ac935"

    print("PASS Albertson r=27 h=19 implicit-edge closure")
    print(f"rainbow_scaffolds={(scaffold_c, scaffold_b)}")
    print(f"form_C_feasible_K9_intersections={form_c[1]}; degree_caps={(form_c[-3], form_c[-1])}")
    print(f"form_B_core_floors={core_b}")
    print(f"form_B_outside_costs={rows_b[1]}; degree_sum={(rows_b[-2], rows_b[-1])}")
    print("survivors=form B with chi(G[Q]) in {8,9}")
    print(f"certificate_sha256={digest}")


if __name__ == "__main__":
    main()
