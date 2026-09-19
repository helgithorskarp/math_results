#!/usr/bin/env python3
"""Independent endpoint-pair verification of the Q5 deficit gap 217."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, permutations
import json
from pathlib import Path


def load_parent():
    path = (
        Path(__file__).resolve().parent.parent
        / "hypercube_square_saturation_q5_gap200"
        / "independent_check.py"
    )
    spec = spec_from_file_location("gap200_global_edge_engine", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the reviewed gap-200 global-edge engine")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


parent = load_parent()
base = parent.base
base.MAX_COST = 32
base.LIMIT = 217

P0 = (0, 17, 0, 1)
P28 = (28, 19, 6, 0)
P42_0 = (42, 20, 0, 0)
P42_6 = (42, 20, 6, 0)
P42_7 = (42, 20, 7, 0)
P48 = (48, 18, 3, 0)
P65 = (65, 18, 4, 0)
P71 = (71, 16, 2, 1)
P99 = (99, 1, 3, 5)
P124 = (124, 21, 1, 0)
EMPTY = "empty"

FRONTIER_SURVIVORS = (
    (203, (P42_0, P42_0, P48, P71), 6, 0, 44),
    (205, (P28,) * 5 + (P65,), 3, 1, 41),
    (208, (P42_0, P42_0, P124), 7, 0, 45),
    (210, (P28,) * 6 + (P42_0,), 2, 1, 42),
    (210, (P28,) * 6 + (P42_6,), 2, 1, 42),
    (210, (P28,) * 6 + (P42_7,), 2, 1, 42),
    (210, (P28,) * 3 + (P42_0,) * 3, 3, 1, 42),
    (210, (P28,) * 3 + (P42_0,) * 2 + (P42_6,), 3, 1, 42),
    (210, (P28,) * 3 + (P42_0,) + (P42_6,) * 2, 3, 1, 42),
    (210, (P28,) * 3 + (P42_6,) * 3, 3, 1, 42),
    (210, (P42_0,) * 5, 4, 1, 42),
    (215, (P48,) * 3 + (P71,), 6, 0, 43),
)
EXPECTED_FRONTIER_CASES = {
    "203": (1, 252),
    "205": (1, 1008),
    "208": (1, 36),
    "210": (8, 27090),
    "215": (1, 84),
}


def structural_profile_survivors(class_counts):
    classes = tuple(sorted(class_counts))
    capacities = base.live_capacity_maxima()
    survivors = set()

    def visit(start, chosen, total):
        if chosen:
            positive_count = len(chosen)
            positive_edges = sum(item[1] for item in chosen)
            for equality_count in range(11 - positive_count):
                empty_count = 10 - positive_count - equality_count
                incidence = positive_edges + 17 * equality_count
                if incidence % 4:
                    continue
                global_edges = incidence // 4
                live_count = positive_count + equality_count
                if not global_edges or global_edges > capacities[live_count]:
                    continue
                if any(
                    item[2] > positive_count + empty_count - 1 for item in chosen
                ):
                    continue
                survivors.add(
                    (total, chosen, equality_count, empty_count, global_edges)
                )
        if len(chosen) == 9:
            return
        for index in range(start, len(classes)):
            item = classes[index]
            if total + item[0] >= 217:
                break
            visit(index, chosen + (item,), total + item[0])

    visit(0, (), 0)
    return tuple(sorted(survivors))


def orbit_summary(masks):
    remaining = set(masks)
    result = []
    coordinate_permutations = tuple(permutations(range(base.DIM)))
    while remaining:
        representative = min(remaining)
        orbit = {
            base.transform(representative, translation, permutation)
            for translation in base.VERTICES
            for permutation in coordinate_permutations
        }
        if not orbit <= set(masks):
            raise AssertionError("an asserted profile is not automorphism-invariant")
        result.append(
            (f"0x{representative:08x}", len(orbit), 384 // len(orbit))
        )
        remaining -= orbit
    return result


def multiset_assignments(facets, counts):
    items = tuple(sorted(counts, key=str))

    def visit(remaining, index, assigned):
        item = items[index]
        count = counts[item]
        if index == len(items) - 1:
            if len(remaining) == count:
                yield assigned | {facet: item for facet in remaining}
            return
        for chosen in combinations(remaining, count):
            chosen_set = frozenset(chosen)
            yield from visit(
                tuple(facet for facet in remaining if facet not in chosen_set),
                index + 1,
                assigned | {facet: item for facet in chosen},
            )

    yield from visit(tuple(facets), 0, {})


def search_profile(
    positive_profiles,
    equality_count,
    empty_count,
    fixed_profile,
    catalogs,
    orbit_summaries,
):
    counts = Counter(positive_profiles)
    counts[fixed_profile] -= 1
    if not counts[fixed_profile]:
        del counts[fixed_profile]
    counts[P0] = equality_count
    if empty_count:
        counts[EMPTY] = empty_count
    if sum(counts.values()) != 9:
        raise AssertionError("residual profile does not have ten facets")

    rows = []
    for representative_hex, _, _ in orbit_summaries[fixed_profile]:
        for assignment in multiset_assignments(range(1, 10), counts):
            case = tuple(
                (int(representative_hex, 16),)
                if facet == 0
                else (0,)
                if assignment[facet] == EMPTY
                else catalogs[assignment[facet]]
                for facet in range(10)
            )
            rows.append(base.edge_constraint_search(case))
    return {
        "cases": len(rows),
        "nodes": sum(row[1] for row in rows),
        "solutions": sum(row[0] for row in rows),
    }


def frontier_residual_searches(catalogs, orbit_summaries):
    specs = (
        (203, (P42_0, P42_0, P48, P71), 6, 0, P71),
        (205, (P28,) * 5 + (P65,), 3, 1, P65),
        (208, (P42_0, P42_0, P124), 7, 0, P124),
        (210, (P28,) * 6 + (P42_0,), 2, 1, P42_0),
        (210, (P28,) * 6 + (P42_6,), 2, 1, P42_6),
        (210, (P28,) * 6 + (P42_7,), 2, 1, P42_7),
        (210, (P28,) * 3 + (P42_0,) * 3, 3, 1, P42_0),
        (210, (P28,) * 3 + (P42_0,) * 2 + (P42_6,), 3, 1, P42_6),
        (210, (P28,) * 3 + (P42_0,) + (P42_6,) * 2, 3, 1, P42_6),
        (210, (P28,) * 3 + (P42_6,) * 3, 3, 1, P42_6),
        (210, (P42_0,) * 5, 4, 1, P42_0),
        (215, (P48,) * 3 + (P71,), 6, 0, P71),
    )
    grouped = {}
    for total, positive, equality, empty, fixed in specs:
        row = search_profile(
            positive,
            equality,
            empty,
            fixed,
            catalogs,
            orbit_summaries,
        )
        key = str(total)
        grouped.setdefault(
            key, {"profiles": 0, "cases": 0, "nodes": 0, "solutions": 0}
        )
        grouped[key]["profiles"] += 1
        grouped[key]["cases"] += row["cases"]
        grouped[key]["nodes"] += row["nodes"]
        grouped[key]["solutions"] += row["solutions"]
    return grouped


def independent_check():
    masks, nodes, pruned = base.census()
    if len(masks) != 490_753:
        raise AssertionError("unexpected independent S<=16 Q4 census")
    slack = {mask: base.direct_slack(mask) for mask in masks}
    if any(value > 16 for value in slack.values()):
        raise AssertionError("census contains a pattern above the cutoff")
    if any(17 * slack[mask] - 3 * mask.bit_count() < 0 for mask in masks):
        raise AssertionError("negative Q4 deficit")

    graph_hash = base.normalized_graph_hash(masks)
    boundary, classes = base.classify_boundaries(masks, slack)
    survivors = structural_profile_survivors(classes)
    # Compare directly with the reviewed sub-200 rows plus the explicit frontier.
    sub_200 = tuple(row for row in survivors if row[0] < 200)
    if [row[0] for row in sub_200] != parent.EXPECTED_TOTALS:
        raise AssertionError("reviewed sub-200 structural rows changed")
    if tuple(row for row in survivors if row[0] >= 200) != FRONTIER_SURVIVORS:
        raise AssertionError("independent frontier profile list differs")

    equality = tuple(
        mask
        for mask in masks
        if mask and 17 * slack[mask] - 3 * mask.bit_count() == 0
    )
    profiles = (P0, P28, P42_0, P42_6, P42_7, P48, P65, P71, P99, P124)
    catalogs = {
        profile: (
            equality
            if profile == P0
            else parent.catalog(masks, slack, boundary, profile)
        )
        for profile in profiles
    }
    expected_sizes = (64, 192, 32, 32, 896, 192, 576, 192, 32, 192)
    if tuple(len(catalogs[profile]) for profile in profiles) != expected_sizes:
        raise AssertionError("unexpected independent residual catalog size")
    orbit_summaries = {
        profile: orbit_summary(set(catalogs[profile])) for profile in profiles
    }
    expected_orbit_counts = (1, 1, 1, 1, 3, 1, 2, 1, 1, 1)
    if tuple(len(orbit_summaries[profile]) for profile in profiles) != expected_orbit_counts:
        raise AssertionError("unexpected independent orbit decomposition")

    old_residuals, _ = base.residual_searches(masks, slack, boundary)
    gap200_residuals = old_residuals | parent.new_residual_searches(catalogs)
    if {key: row["cases"] for key, row in gap200_residuals.items()} != parent.EXPECTED_CASES:
        raise AssertionError("reviewed sub-200 placement counts changed")
    if any(row["solutions"] for row in gap200_residuals.values()):
        raise AssertionError("a reviewed sub-200 residual row has a solution")

    frontier_residuals = frontier_residual_searches(catalogs, orbit_summaries)
    actual_cases = {
        key: (row["profiles"], row["cases"])
        for key, row in frontier_residuals.items()
    }
    if actual_cases != EXPECTED_FRONTIER_CASES:
        raise AssertionError("independent frontier placement counts differ")
    if any(row["solutions"] for row in frontier_residuals.values()):
        raise AssertionError("an independent frontier residual row has a solution")

    deficit_200 = sum(
        17 * slack[mask] - 3 * mask.bit_count() == 200 for mask in masks
    )
    if deficit_200:
        raise AssertionError("an independent Q4 facet has deficit 200")

    rows = [(*key, count) for key, count in sorted(classes.items())]
    profile_hash = sha256(
        json.dumps(rows, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    if Fraction(12 * 56 + 217, 34 * 56) != Fraction(127, 272):
        raise AssertionError("incorrect Q5 ratio")
    if Fraction(127, 272 * 12) != Fraction(127, 3264):
        raise AssertionError("incorrect global coefficient")
    if Fraction(5712, 3137) - Fraction(4998, 2747) != Fraction(12138, 8617339):
        raise AssertionError("incorrect asymptotic improvement")

    public_orbits = {
        ":".join(map(str, profile)): orbit_summaries[profile]
        for profile in profiles
    }
    return {
        "representation": "unordered endpoint pairs",
        "q4_algorithm": "global edge branching with local-state lower bounds",
        "q5_algorithm": "global edge constraint propagation",
        "q4_edge_branch_nodes": nodes,
        "q4_edge_branch_pruned": pruned,
        "q4_patterns_with_slack_at_most_16": len(masks),
        "q4_normalized_graph_set_sha256": graph_hash,
        "q4_positive_profile_classes_below_217": len(classes),
        "profile_class_sha256": profile_hash,
        "q4_patterns_with_deficit_200": deficit_200,
        "structural_survivor_total_counts": dict(
            sorted(Counter(row[0] for row in survivors).items())
        ),
        "residual_catalog_orbits": public_orbits,
        "sub_200_residual_searches": gap200_residuals,
        "frontier_residual_searches": frontier_residuals,
        "q5_deficit_lower_bound": 217,
        "bound": "sat(Q_d,Q_2) >= 5712*d*2^d/(3137*d+8287) for d>=5",
    }


def main():
    print(json.dumps(independent_check(), sort_keys=True, indent=2))
    print("status=PASS")


if __name__ == "__main__":
    main()
