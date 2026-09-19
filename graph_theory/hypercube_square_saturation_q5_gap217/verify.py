#!/usr/bin/env python3
"""Exact facet-gluing verifier for the Q5 deficit lower bound 217."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
import json
from pathlib import Path


def load_parent():
    path = (
        Path(__file__).resolve().parent.parent
        / "hypercube_square_saturation_q5_gap200"
        / "verify.py"
    )
    spec = spec_from_file_location("gap200_facet_engine", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the reviewed gap-200 facet engine")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


parent = load_parent()
base = parent.base
base.MAX_SLACK = 16
base.MAX_TWICE_SLACK = 32
base.DEFICIT_LIMIT = 217

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
EXPECTED_SURVIVORS = tuple(
    sorted(parent.EXPECTED_SURVIVORS + FRONTIER_SURVIVORS)
)
EXPECTED_FRONTIER_RESIDUALS = {
    "203": {
        "profiles": 1,
        "cases": 252,
        "nodes": 252,
        "max_depth": 0,
        "solutions": 0,
    },
    "205": {
        "profiles": 1,
        "cases": 1008,
        "nodes": 1008,
        "max_depth": 0,
        "solutions": 0,
    },
    "208": {
        "profiles": 1,
        "cases": 36,
        "nodes": 36,
        "max_depth": 0,
        "solutions": 0,
    },
    "210": {
        "profiles": 8,
        "cases": 27090,
        "nodes": 27361,
        "max_depth": 1,
        "solutions": 0,
    },
    "215": {
        "profiles": 1,
        "cases": 84,
        "nodes": 84,
        "max_depth": 0,
        "solutions": 0,
    },
}


def structural_profile_survivors(class_counts, capacities):
    """Enumerate all necessary profiles of total deficit below 217."""

    classes = tuple(sorted(class_counts))
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
                exceptional_neighbors = positive_count + empty_count - 1
                if any(item[2] > exceptional_neighbors for item in chosen):
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

    fixed_facet = (0, 0)
    remaining = tuple(facet for facet in base.Q5_FACETS if facet != fixed_facet)
    rows = []
    for representative_hex, _, _ in orbit_summaries[fixed_profile]:
        for assignment in multiset_assignments(remaining, counts):
            candidates = {
                facet: (
                    (0,)
                    if assignment[facet] == EMPTY
                    else catalogs[assignment[facet]]
                )
                for facet in remaining
            }
            rows.append(
                base.exact_q5_search(
                    fixed_facet,
                    int(representative_hex, 16),
                    candidates,
                )
            )
    return {
        "cases": len(rows),
        "nodes": sum(row[1] for row in rows),
        "max_depth": max(row[2] for row in rows),
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
        if key not in grouped:
            grouped[key] = {
                "profiles": 0,
                "cases": 0,
                "nodes": 0,
                "max_depth": 0,
                "solutions": 0,
            }
        grouped[key]["profiles"] += 1
        grouped[key]["cases"] += row["cases"]
        grouped[key]["nodes"] += row["nodes"]
        grouped[key]["max_depth"] = max(grouped[key]["max_depth"], row["max_depth"])
        grouped[key]["solutions"] += row["solutions"]
    return grouped


def integer_bound(d):
    numerator = 5712 * d * (1 << d)
    denominator = 3137 * d + 8287
    return (numerator + denominator - 1) // denominator


def verify():
    census, census_nodes, local_table = base.facet_gluing_census()
    if len(census) != 490_753 or census_nodes != 146_812_464:
        raise AssertionError("unexpected S<=16 Q4 census")
    for mask, slack in census.items():
        if base.direct_q4_statistics(mask)[3] != slack:
            raise AssertionError("direct and facet slack computations disagree")
        if 17 * slack - 3 * mask.bit_count() < 0:
            raise AssertionError("negative Q4 deficit")

    equality = tuple(
        mask
        for mask, slack in census.items()
        if mask and 17 * slack - 3 * mask.bit_count() == 0
    )
    boundary, class_counts = base.boundary_classification(census, equality)
    capacities = {
        live: max(base.live_support_distribution(live)) for live in range(1, 11)
    }
    survivors = structural_profile_survivors(class_counts, capacities)
    if survivors != EXPECTED_SURVIVORS:
        raise AssertionError("unexpected structural profile list below 217")

    profiles = (P0, P28, P42_0, P42_6, P42_7, P48, P65, P71, P99, P124)
    catalogs = {
        profile: (
            equality
            if profile == P0
            else parent.profile_catalog(census, boundary, profile)
        )
        for profile in profiles
    }
    expected_sizes = (64, 192, 32, 32, 896, 192, 576, 192, 32, 192)
    if tuple(len(catalogs[profile]) for profile in profiles) != expected_sizes:
        raise AssertionError("unexpected residual catalog size")
    orbit_summaries = {
        profile: base.orbit_summary(set(catalogs[profile])) for profile in profiles
    }
    expected_orbit_counts = (1, 1, 1, 1, 3, 1, 2, 1, 1, 1)
    if tuple(len(orbit_summaries[profile]) for profile in profiles) != expected_orbit_counts:
        raise AssertionError("unexpected residual orbit decomposition")

    old_residuals, _ = base.residual_searches(census, boundary)
    gap200_residuals = old_residuals | parent.new_residual_searches(
        census, boundary, catalogs
    )
    if gap200_residuals != parent.EXPECTED_RESIDUALS:
        raise AssertionError("the reviewed sub-200 residual closure changed")
    frontier_residuals = frontier_residual_searches(catalogs, orbit_summaries)
    if frontier_residuals != EXPECTED_FRONTIER_RESIDUALS:
        raise AssertionError("a residual profile in the 200--216 window survived")

    deficit_spectrum = Counter(
        17 * slack - 3 * mask.bit_count() for mask, slack in census.items()
    )
    if deficit_spectrum[200]:
        raise AssertionError("a Q4 facet has deficit 200")

    rows = [(*key, count) for key, count in sorted(class_counts.items())]
    profile_hash = sha256(
        json.dumps(rows, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    q4_hash = base.normalized_graph_hash(census)

    q5_ratio = Fraction(12 * 56 + 217, 34 * 56)
    global_coefficient = q5_ratio / 12
    new_constant = Fraction(5712, 3137)
    old_constant = Fraction(4998, 2747)
    if q5_ratio != Fraction(127, 272):
        raise AssertionError("incorrect Q5 ratio")
    if global_coefficient != Fraction(127, 3264):
        raise AssertionError("incorrect global coefficient")
    if new_constant - old_constant != Fraction(12138, 8617339):
        raise AssertionError("incorrect asymptotic improvement")

    public_orbits = {
        ":".join(map(str, profile)): orbit_summaries[profile]
        for profile in profiles
    }
    canonical = {
        "local_table": [(*key, count) for key, count in sorted(local_table.items())],
        "profile_classes": rows,
        "survivors": survivors,
        "gap200_residuals": gap200_residuals,
        "frontier_residuals": frontier_residuals,
        "orbits": public_orbits,
        "capacities": capacities,
    }
    audit_hash = sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    total_counts = dict(sorted(Counter(row[0] for row in survivors).items()))
    return {
        "q4_facet_gluing_nodes": census_nodes,
        "q4_patterns_with_slack_at_most_16": len(census),
        "q4_normalized_graph_set_sha256": q4_hash,
        "q4_positive_profile_classes_below_217": len(class_counts),
        "profile_class_sha256": profile_hash,
        "q4_patterns_with_deficit_200": deficit_spectrum[200],
        "structural_survivor_total_counts": total_counts,
        "residual_catalog_orbits": public_orbits,
        "sub_200_residual_searches": gap200_residuals,
        "frontier_residual_searches": frontier_residuals,
        "q5_deficit_lower_bound": 217,
        "q5_slack_edge_ratio": str(q5_ratio),
        "global_slack_coefficient": str(global_coefficient),
        "bound": "sat(Q_d,Q_2) >= 5712*d*2^d/(3137*d+8287) for d>=5",
        "asymptotic_constant": str(new_constant),
        "improvement_over_gap200_constant": str(new_constant - old_constant),
        "finite_bound_cross_difference": "12138*(d-1)",
        "integer_lower_bounds_d7_d8_d11": [
            integer_bound(7),
            integer_bound(8),
            integer_bound(11),
        ],
        "audit_sha256": audit_hash,
    }


def main():
    print(json.dumps(verify(), sort_keys=True, indent=2))
    print("status=PASS")


if __name__ == "__main__":
    main()
