#!/usr/bin/env python3
"""Independent global-edge check of the Q5 deficit lower bound 200.

This extends the reviewed endpoint-pair checker from the gap-166 package.
It assigns all 32 Q4 edges with local-state lower bounds and closes Q5
profiles by propagation on all 80 global edges, rather than gluing facets.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
import json
from pathlib import Path


def load_base():
    path = (
        Path(__file__).resolve().parent.parent
        / "hypercube_square_saturation_q5_gap166"
        / "independent_check.py"
    )
    spec = spec_from_file_location("gap166_global_edge_engine", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the reviewed global-edge engine")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load_base()
base.MAX_COST = 30
base.LIMIT = 200


EXPECTED_TOTALS = [42, 84, 132, 144, 161, 166, 174, 186, 188, 190, 195, 196, 198]
EXPECTED_CASES = {
    "42": 9,
    "84": 9,
    "132": 252,
    "144": 252,
    "161": 504,
    "166": 72,
    "174": 84,
    "186": 84,
    "188": 504,
    "190": 252,
    "195": 72,
    "196": 84,
    "198": 252,
}


def catalog(masks, slack, boundary, profile):
    deficit, edges, bad, empty = profile
    return tuple(
        mask
        for mask in masks
        if 17 * slack[mask] - 3 * mask.bit_count() == deficit
        and mask.bit_count() == edges
        and boundary[mask] == (bad, empty)
    )


def run(cases):
    rows = [base.edge_constraint_search(case) for case in cases]
    return {
        "cases": len(rows),
        "nodes": sum(row[1] for row in rows),
        "solutions": sum(row[0] for row in rows),
    }


def structural_profile_survivors(class_counts):
    """Independent profile enumeration with no parity assumption."""

    classes = tuple(sorted(class_counts))
    capacities = base.live_capacity_maxima()
    survivors = set()

    def visit(start, chosen, total):
        if chosen:
            positive = len(chosen)
            for equality_count in range(11 - positive):
                empty = 10 - positive - equality_count
                incidence = sum(item[1] for item in chosen) + 17 * equality_count
                if incidence % 4:
                    continue
                edges = incidence // 4
                live = positive + equality_count
                if not edges or edges > capacities[live]:
                    continue
                if any(item[2] > positive + empty - 1 for item in chosen):
                    continue
                survivors.add((total, chosen, equality_count, empty, edges))
        if len(chosen) == 9:
            return
        for index in range(start, len(classes)):
            item = classes[index]
            if total + item[0] >= 200:
                break
            visit(index, chosen + (item,), total + item[0])

    visit(0, (), 0)
    return tuple(sorted(survivors))


def parity_counterexample_delta():
    selected = {(0, 1), (0, 2), (1, 3)}
    global_mask = sum(1 << base.Q5_EDGE_INDEX[edge] for edge in selected)
    total = 0
    for facet in range(10):
        local_mask = 0
        for edge in range(len(base.EDGES)):
            if base.embed_q4(1 << edge, facet) & global_mask:
                local_mask |= 1 << edge
        slack = base.direct_slack(local_mask)
        total += 17 * slack - 3 * local_mask.bit_count()
    return total


def new_residual_searches(catalogs):
    equality = catalogs[(0, 17, 0, 0)]
    d28 = catalogs[(28, 19, 6, 0)]
    d42 = catalogs[(42, 20, 0, 0)]
    d48 = catalogs[(48, 18, 3, 0)]
    d71 = catalogs[(71, 16, 2, 1)]
    d99 = catalogs[(99, 1, 3, 5)]
    d124 = catalogs[(124, 21, 1, 0)]
    empty = (0,)
    remaining = tuple(range(1, 10))
    result = {}

    cases = []
    for position42 in remaining:
        for position48 in remaining:
            if position48 == position42:
                continue
            for empty_facet in remaining:
                if empty_facet in (position42, position48):
                    continue
                cases.append(
                    tuple(
                        (min(d71),)
                        if facet == 0
                        else d42
                        if facet == position42
                        else d48
                        if facet == position48
                        else empty
                        if facet == empty_facet
                        else equality
                        for facet in range(10)
                    )
                )
    result["161"] = run(cases)

    cases = []
    for position124 in remaining:
        for empty_facet in remaining:
            if empty_facet == position124:
                continue
            cases.append(
                tuple(
                    (min(d42),)
                    if facet == 0
                    else d124
                    if facet == position124
                    else empty
                    if facet == empty_facet
                    else equality
                    for facet in range(10)
                )
            )
    result["166"] = run(cases)

    cases = []
    for positions42 in combinations(remaining, 3):
        cases.append(
            tuple(
                (min(d48),)
                if facet == 0
                else d42
                if facet in positions42
                else equality
                for facet in range(10)
            )
        )
    result["174"] = run(cases)

    cases = []
    for positions48 in combinations(remaining, 3):
        cases.append(
            tuple(
                (min(d42),)
                if facet == 0
                else d48
                if facet in positions48
                else equality
                for facet in range(10)
            )
        )
    result["186"] = run(cases)

    cases = []
    for positions28 in combinations(remaining, 5):
        for empty_facet in remaining:
            if empty_facet in positions28:
                continue
            cases.append(
                tuple(
                    (min(d48),)
                    if facet == 0
                    else d28
                    if facet in positions28
                    else empty
                    if facet == empty_facet
                    else equality
                    for facet in range(10)
                )
            )
    result["188"] = run(cases)

    cases = []
    for positions71 in combinations(remaining, 2):
        for empty_facet in remaining:
            if empty_facet in positions71:
                continue
            cases.append(
                tuple(
                    (min(d48),)
                    if facet == 0
                    else d71
                    if facet in positions71
                    else empty
                    if facet == empty_facet
                    else equality
                    for facet in range(10)
                )
            )
    result["190"] = run(cases)

    cases = []
    for position124 in remaining:
        for empty_facet in remaining:
            if empty_facet == position124:
                continue
            cases.append(
                tuple(
                    (min(d71),)
                    if facet == 0
                    else d124
                    if facet == position124
                    else empty
                    if facet == empty_facet
                    else equality
                    for facet in range(10)
                )
            )
    result["195"] = run(cases)

    cases = []
    for other28 in combinations(remaining, 6):
        cases.append(
            tuple(
                (min(d28),)
                if facet == 0
                else d28
                if facet in other28
                else equality
                for facet in range(10)
            )
        )
    result["196"] = run(cases)

    cases = []
    for second99 in remaining:
        available = tuple(facet for facet in remaining if facet != second99)
        for empty_facets in combinations(available, 2):
            cases.append(
                tuple(
                    (min(d99),)
                    if facet == 0
                    else d99
                    if facet == second99
                    else empty
                    if facet in empty_facets
                    else equality
                    for facet in range(10)
                )
            )
    result["198"] = run(cases)
    return result


def independent_check():
    if parity_counterexample_delta() != 831:
        raise AssertionError("explicit odd-Delta counterexample changed")
    masks, nodes, pruned = base.census()
    if len(masks) != 327_553:
        raise AssertionError("unexpected S<=15 Q4 census")
    slack = {mask: base.direct_slack(mask) for mask in masks}
    if any(value > 15 for value in slack.values()):
        raise AssertionError("census contains a pattern above the cutoff")
    if any(17 * slack[mask] - 3 * mask.bit_count() < 0 for mask in masks):
        raise AssertionError("negative Q4 deficit")

    graph_hash = base.normalized_graph_hash(masks)
    boundary, classes = base.classify_boundaries(masks, slack)
    survivors = structural_profile_survivors(classes)
    if [row[0] for row in survivors] != EXPECTED_TOTALS:
        raise AssertionError("independent structural totals differ")

    equality = tuple(
        mask
        for mask in masks
        if mask and 17 * slack[mask] - 3 * mask.bit_count() == 0
    )
    profiles = (
        (0, 17, 0, 0),
        (28, 19, 6, 0),
        (42, 20, 0, 0),
        (48, 18, 3, 0),
        (71, 16, 2, 1),
        (99, 1, 3, 5),
        (124, 21, 1, 0),
    )
    catalogs = {
        profile: equality if profile[0] == 0 else catalog(masks, slack, boundary, profile)
        for profile in profiles
    }
    expected_sizes = [64, 192, 32, 192, 192, 32, 192]
    if [len(catalogs[profile]) for profile in profiles] != expected_sizes:
        raise AssertionError("unexpected independent catalog size")
    orbits = {
        str(profile[0]): base.assert_single_orbit(set(catalogs[profile]))
        for profile in profiles
    }

    old_residuals, _ = base.residual_searches(masks, slack, boundary)
    residuals = old_residuals | new_residual_searches(catalogs)
    if {key: value["cases"] for key, value in residuals.items()} != EXPECTED_CASES:
        raise AssertionError("not all labeled residual placements were checked")
    if any(value["solutions"] for value in residuals.values()):
        raise AssertionError("a residual profile below 200 has a solution")

    rows = [(*key, count) for key, count in sorted(classes.items())]
    profile_hash = sha256(
        json.dumps(rows, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    if Fraction(12 * 56 + 200, 34 * 56) != Fraction(109, 238):
        raise AssertionError("incorrect Q5 ratio")
    if Fraction(109, 238 * 12) != Fraction(109, 2856):
        raise AssertionError("incorrect global coefficient")
    if Fraction(4998, 2747) - Fraction(19992, 11005) != Fraction(84966, 30230735):
        raise AssertionError("incorrect asymptotic improvement")

    return {
        "representation": "unordered endpoint pairs",
        "q4_algorithm": "global edge branching with local-state lower bounds",
        "q5_algorithm": "global edge constraint propagation",
        "q4_edge_branch_nodes": nodes,
        "q4_edge_branch_pruned": pruned,
        "q4_patterns_with_slack_at_most_15": len(masks),
        "q4_normalized_graph_set_sha256": graph_hash,
        "q4_positive_profile_classes_below_200": len(classes),
        "profile_class_sha256": profile_hash,
        "structural_survivor_totals": EXPECTED_TOTALS,
        "parity_counterexample_delta": 831,
        "residual_catalog_orbits": orbits,
        "residual_searches": residuals,
        "q5_deficit_lower_bound": 200,
        "bound": "sat(Q_d,Q_2) >= 4998*d*2^d/(2747*d+7249) for d>=5",
    }


def main():
    print(json.dumps(independent_check(), sort_keys=True, indent=2))
    print("status=PASS")


if __name__ == "__main__":
    main()
