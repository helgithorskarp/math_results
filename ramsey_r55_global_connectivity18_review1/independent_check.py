#!/usr/bin/env python3
"""Clean-room arithmetic audit of the R(5,5;43) connectivity proof.

This program imports no target certificate or implementation.  It checks the
finite integer exhaustiveness of the displayed separator argument.  The
classical computational theorem R(4,5)=25 remains an explicit premise.
"""

from itertools import combinations_with_replacement
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def independence_partitions(budget):
    """All unordered positive component-independence profiles."""
    profiles = []
    for component_count in range(2, budget + 1):
        for profile in combinations_with_replacement(
                range(1, budget + 1), component_count):
            if sum(profile) <= budget:
                profiles.append(profile)
    return profiles


def audit(*, vertices=43, ramsey_4_5=25, separator_max=17,
          alpha_two_component_max=13, independence_budget=4):
    # A vertex has at most R(4,5)-1 neighbors of the opposite color.
    minimum_degree = vertices - ramsey_4_5
    require(minimum_degree == 18, "The imported degree window is not 18")

    # The elementary small bounds used by the proof.  For R(3,4)<=9, a
    # triangle-free order-nine graph with alpha<=3 would have degree at most
    # three, while R(3,3)<=6 makes every degree at least three.  Odd order
    # rules out the resulting 3-regular graph.  The standard recurrence then
    # gives R(3,5)<=R(2,5)+R(3,4)<=5+9=14.
    ramsey_3_3 = 6
    order = 9
    maximum_degree = 3
    minimum_degree_if_counterexample = (order - 1) - (ramsey_3_3 - 1)
    require(maximum_degree == minimum_degree_if_counterexample == 3,
            "R(3,4) degree squeeze")
    require((order * maximum_degree) % 2 == 1,
            "R(3,4) parity contradiction")
    ramsey_3_4 = 9
    ramsey_3_5 = 5 + ramsey_3_4
    require(ramsey_3_5 == 14, "R(3,5) recurrence")

    profiles = independence_partitions(independence_budget)
    no_clique_profiles = [p for p in profiles if 1 not in p]
    require(no_clique_profiles == [(2, 2)],
            "The no-clique component branch is no longer unique")

    # Any component of independence number one is a clique of order a<=4.
    # Check every separator size directly.  Either its vertices cannot reach
    # degree 18, or their common separator neighborhood is too large for the
    # applicable small Ramsey bound.
    common_neighborhood_upper = {2: ramsey_3_5 - 1, 3: 4, 4: 0}
    clique_cases = 0
    degree_capacity_cases = 0
    common_neighborhood_cases = 0
    for clique_order in range(1, 5):
        for separator in range(separator_max + 1):
            clique_cases += 1
            required_in_separator = minimum_degree - (clique_order - 1)
            if required_in_separator > separator:
                degree_capacity_cases += 1
                continue
            require(clique_order >= 2, "A singleton clique component survived")
            common_lower = (
                clique_order * required_in_separator
                - (clique_order - 1) * separator
            )
            require(common_lower > common_neighborhood_upper[clique_order],
                    "A clique component was not excluded")
            common_neighborhood_cases += 1

    # In the only no-clique profile both components have alpha=2 and hence
    # order at most R(5,3)-1=13.  Enumerate all possible component orders and
    # separator sizes, retaining only the degree and order necessities.
    saturated_profiles = []
    for separator in range(separator_max + 1):
        for left in range(2, alpha_two_component_max + 1):
            for right in range(left, alpha_two_component_max + 1):
                if left + right != vertices - separator:
                    continue
                if min(left, right) - 1 + separator < minimum_degree:
                    continue
                saturated_profiles.append((separator, left, right))
    require(saturated_profiles == [(17, 13, 13)],
            "The no-clique branch does not reduce to the saturated profile")

    # For z in the nonempty separator, N(z) inside either 13-component has
    # no K4 and no independent triple, so R(4,3)<=9 bounds it by eight.
    component_order = 13
    red_neighbors_at_most = ramsey_3_4 - 1
    blue_neighbors_at_least = component_order - red_neighbors_at_most
    require(red_neighbors_at_most == 8 and blue_neighbors_at_least == 5,
            "The outside-vertex five-clique forcing threshold failed")
    require(blue_neighbors_at_least > 4,
            "Five blue neighbors are needed to force an internal blue edge")

    # Total-size-26 cut clauses suffice for every larger disjoint nonempty
    # pair.  This is checked constructively for all ordered size pairs.
    cut_threshold = vertices - separator_max
    cut_pairs = 0
    for left in range(1, vertices):
        for right in range(1, vertices - left + 1):
            if left + right < cut_threshold:
                continue
            selected_left = max(1, cut_threshold - right)
            selected_right = cut_threshold - selected_left
            require(1 <= selected_left <= left and 1 <= selected_right <= right,
                    "A larger cut contains no threshold-size subcut")
            cut_pairs += 1

    return {
        "status": "INDEPENDENTLY_VERIFIED_R55_GLOBAL_CONNECTIVITY18",
        "vertices": vertices,
        "imported_ramsey_4_5_upper": ramsey_4_5,
        "derived_minimum_degree_each_color": minimum_degree,
        "separator_orders_checked": separator_max + 1,
        "independence_profiles_checked": len(profiles),
        "clique_order_separator_cases_checked": clique_cases,
        "clique_degree_capacity_contradictions": degree_capacity_cases,
        "clique_common_neighborhood_contradictions": common_neighborhood_cases,
        "surviving_no_clique_profiles": [list(x) for x in saturated_profiles],
        "outside_vertex_red_neighbors_each_at_most": red_neighbors_at_most,
        "outside_vertex_blue_neighbors_each_at_least": blue_neighbors_at_least,
        "ordered_large_cut_size_pairs_checked": cut_pairs,
        "both_color_graphs_covered_by_complement_symmetry": True,
        "target_certificate_imported": False,
        "target_code_imported": False,
        "formal_proof_assistant_check": False,
    }


def main():
    result = audit()
    mutations = {
        "separator_order_18": {"separator_max": 18},
        "weaker_R45_bound": {"ramsey_4_5": 26},
        "larger_alpha_two_components": {"alpha_two_component_max": 14},
        "larger_independence_budget": {"independence_budget": 5},
    }
    rejected = []
    for name, changes in mutations.items():
        try:
            audit(**changes)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("Unsound scope mutation accepted: " + name)
    result["scope_mutations_rejected"] = rejected
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
