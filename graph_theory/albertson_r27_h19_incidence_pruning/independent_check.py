#!/usr/bin/env python3
"""Independent residual-edge enumeration for the h=19 incidence pruning."""

from hashlib import sha256
from itertools import combinations
from math import comb


def available_edges(core_order: int) -> tuple[tuple[int, int], ...]:
    core_edges = set(combinations(range(core_order), 2))
    return tuple(edge for edge in combinations(range(19), 2) if edge not in core_edges)


def max_degree_sum_on_triple(core_order: int, residual_edges: int) -> int:
    """Brute-force the A-case degree sum for {one core, two outsiders}."""
    triple = {0, core_order, core_order + 1}
    baseline = core_order - 1
    best = -1
    for chosen in combinations(available_edges(core_order), residual_edges):
        incidences = sum((u in triple) + (v in triple) for u, v in chosen)
        best = max(best, baseline + incidences)
    return best


def max_core_vertex_degree(core_order: int, residual_edges: int) -> int:
    """Brute-force the largest possible degree of a fixed core vertex."""
    best = core_order - 1
    for chosen in combinations(available_edges(core_order), residual_edges):
        incidences = sum(0 in edge for edge in chosen)
        best = max(best, core_order - 1 + incidences)
    return best


def main() -> None:
    cases_a = {"A0": (9, 38), "A1": (9, 39)}
    triple_caps = {}
    incidence_margins = {}
    placement_counts = {}
    for name, (core, high_edges) in cases_a.items():
        residual = high_edges - comb(core, 2)
        available = available_edges(core)
        placement_counts[name] = comb(len(available), residual)
        cap = max_degree_sum_on_triple(core, residual)
        triple_caps[name] = cap
        forced = 3 * 27 - 3 * 16 - cap
        incidence_margins[name] = forced - 18
        assert incidence_margins[name] > 0

    assert triple_caps == {"A0": 12, "A1": 14}
    assert incidence_margins == {"A0": 3, "A1": 1}

    endpoint_cases = {"B,c=11": (11, 56, 15), "C,c=10": (10, 46, 16)}
    total_caps = {}
    for name, (core, high_edges, small_low_order) in endpoint_cases.items():
        residual = high_edges - comb(core, 2)
        cap = max_core_vertex_degree(core, residual) + small_low_order
        total_caps[name] = cap
        assert cap == 26

    record = repr((sorted(placement_counts.items()), sorted(triple_caps.items()),
                   sorted(incidence_margins.items()), sorted(total_caps.items())))
    digest = sha256(record.encode("ascii")).hexdigest()
    assert digest == "7b9441024d2ffc037a7413ade07bf85e5245ea51a3b2f4309c0fd9958e9a5e4e"

    print("PASS independent h=19 residual-edge enumeration")
    print(f"residual_placements={placement_counts}")
    print(f"A_triple_degree_caps={triple_caps}")
    print(f"A_incidence_margins={incidence_margins}")
    print(f"outside_F_total_degree_caps={total_caps}")
    print(f"result_sha256={digest}")


if __name__ == "__main__":
    main()
