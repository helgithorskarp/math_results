#!/usr/bin/env python3
"""Exact facet-gluing verifier for the Q5 deficit lower bound 200.

The already reviewed gap-166 package supplies the definition-level Q3/Q4
incidence engine.  This verifier raises its complete cutoff from S<=13 to
S<=15, removes the old false parity filter, derives every admissible Q5
profile below 200, and closes nine new profiles by exact labeled-facet gluing.
"""

from __future__ import annotations

from collections import Counter
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
        / "verify.py"
    )
    spec = spec_from_file_location("gap166_facet_engine", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the reviewed facet-gluing engine")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load_base()
base.MAX_SLACK = 15
base.MAX_TWICE_SLACK = 30
base.DEFICIT_LIMIT = 200


EXPECTED_SURVIVORS = (
    (42, ((42, 20, 0, 0),), 8, 1, 39),
    (84, ((42, 20, 0, 0), (42, 20, 0, 0)), 8, 0, 44),
    (
        132,
        ((42, 20, 0, 0), (42, 20, 0, 0), (48, 18, 3, 0)),
        6,
        1,
        40,
    ),
    (144, ((48, 18, 3, 0),) * 3, 6, 1, 39),
    (
        161,
        ((42, 20, 0, 0), (48, 18, 3, 0), (71, 16, 2, 1)),
        6,
        1,
        39,
    ),
    (166, ((42, 20, 0, 0), (124, 21, 1, 0)), 7, 1, 40),
    (
        174,
        ((42, 20, 0, 0),) * 3 + ((48, 18, 3, 0),),
        6,
        0,
        45,
    ),
    (
        186,
        ((42, 20, 0, 0),) + ((48, 18, 3, 0),) * 3,
        6,
        0,
        44,
    ),
    (
        188,
        ((28, 19, 6, 0),) * 5 + ((48, 18, 3, 0),),
        3,
        1,
        41,
    ),
    (
        190,
        ((48, 18, 3, 0),) + ((71, 16, 2, 1),) * 2,
        6,
        1,
        38,
    ),
    (195, ((71, 16, 2, 1), (124, 21, 1, 0)), 7, 1, 39),
    (196, ((28, 19, 6, 0),) * 7, 3, 0, 46),
    (198, ((99, 1, 3, 5),) * 2, 6, 2, 26),
)


EXPECTED_RESIDUALS = {
    "42": {"cases": 9, "nodes": 10, "max_depth": 1, "solutions": 0},
    "84": {"cases": 9, "nodes": 18, "max_depth": 1, "solutions": 0},
    "132": {"cases": 252, "nodes": 252, "max_depth": 0, "solutions": 0},
    "144": {"cases": 252, "nodes": 252, "max_depth": 0, "solutions": 0},
    "161": {"cases": 504, "nodes": 504, "max_depth": 0, "solutions": 0},
    "166": {"cases": 72, "nodes": 80, "max_depth": 1, "solutions": 0},
    "174": {"cases": 84, "nodes": 84, "max_depth": 0, "solutions": 0},
    "186": {"cases": 84, "nodes": 175, "max_depth": 1, "solutions": 0},
    "188": {"cases": 504, "nodes": 504, "max_depth": 0, "solutions": 0},
    "190": {"cases": 252, "nodes": 252, "max_depth": 0, "solutions": 0},
    "195": {"cases": 72, "nodes": 72, "max_depth": 0, "solutions": 0},
    "196": {"cases": 84, "nodes": 85, "max_depth": 1, "solutions": 0},
    "198": {"cases": 252, "nodes": 252, "max_depth": 0, "solutions": 0},
}


def profile_catalog(census, boundary, profile):
    deficit, edges, bad, empty = profile
    return tuple(
        mask
        for mask, slack in census.items()
        if 17 * slack - 3 * mask.bit_count() == deficit
        and mask.bit_count() == edges
        and boundary[mask] == (bad, empty)
    )


def summarize(rows):
    return {
        "cases": len(rows),
        "nodes": sum(row[1] for row in rows),
        "max_depth": max(row[2] for row in rows),
        "solutions": sum(row[0] for row in rows),
    }


def structural_profile_survivors(class_counts, capacity_maxima):
    """Enumerate profiles without the false assumption that Delta_K is even."""

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
                if not global_edges or global_edges > capacity_maxima[live_count]:
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
            if total + item[0] >= 200:
                break
            visit(index, chosen + (item,), total + item[0])

    visit(0, (), 0)
    return tuple(sorted(survivors))


def parity_counterexample_delta():
    """Return Delta_K for three selected edges of one Q5 square."""

    selected = {(0, 0), (0, 1), (1, 1)}
    global_mask = sum(1 << base.Q5_EDGE_INDEX[edge] for edge in selected)
    total = 0
    for facet in base.Q5_FACETS:
        local_mask = 0
        for edge in range(len(base.EDGES)):
            if base.embed_q4(1 << edge, facet) & global_mask:
                local_mask |= 1 << edge
        edges, _, _, slack = base.direct_q4_statistics(local_mask)
        total += 17 * slack - 3 * edges
    return total


def new_residual_searches(census, boundary, catalogs):
    equality = catalogs[(0, 17, 0, 0)]
    d28 = catalogs[(28, 19, 6, 0)]
    d42 = catalogs[(42, 20, 0, 0)]
    d48 = catalogs[(48, 18, 3, 0)]
    d71 = catalogs[(71, 16, 2, 1)]
    d99 = catalogs[(99, 1, 3, 5)]
    d124 = catalogs[(124, 21, 1, 0)]
    special = (0, 0)
    remaining = tuple(facet for facet in base.Q5_FACETS if facet != special)
    result = {}

    rows = []
    for position42 in remaining:
        for position48 in remaining:
            if position48 == position42:
                continue
            for empty_facet in remaining:
                if empty_facet in (position42, position48):
                    continue
                candidates = {
                    facet: (
                        d42
                        if facet == position42
                        else d48
                        if facet == position48
                        else (0,)
                        if facet == empty_facet
                        else equality
                    )
                    for facet in remaining
                }
                rows.append(base.exact_q5_search(special, min(d71), candidates))
    result["161"] = summarize(rows)

    rows = []
    for position124 in remaining:
        for empty_facet in remaining:
            if empty_facet == position124:
                continue
            candidates = {
                facet: d124 if facet == position124 else (0,) if facet == empty_facet else equality
                for facet in remaining
            }
            rows.append(base.exact_q5_search(special, min(d42), candidates))
    result["166"] = summarize(rows)

    rows = []
    for positions42 in combinations(remaining, 3):
        candidates = {
            facet: d42 if facet in positions42 else equality for facet in remaining
        }
        rows.append(base.exact_q5_search(special, min(d48), candidates))
    result["174"] = summarize(rows)

    rows = []
    for positions48 in combinations(remaining, 3):
        candidates = {
            facet: d48 if facet in positions48 else equality for facet in remaining
        }
        rows.append(base.exact_q5_search(special, min(d42), candidates))
    result["186"] = summarize(rows)

    rows = []
    for positions28 in combinations(remaining, 5):
        for empty_facet in remaining:
            if empty_facet in positions28:
                continue
            candidates = {
                facet: d28 if facet in positions28 else (0,) if facet == empty_facet else equality
                for facet in remaining
            }
            rows.append(base.exact_q5_search(special, min(d48), candidates))
    result["188"] = summarize(rows)

    rows = []
    for positions71 in combinations(remaining, 2):
        for empty_facet in remaining:
            if empty_facet in positions71:
                continue
            candidates = {
                facet: d71 if facet in positions71 else (0,) if facet == empty_facet else equality
                for facet in remaining
            }
            rows.append(base.exact_q5_search(special, min(d48), candidates))
    result["190"] = summarize(rows)

    rows = []
    for position124 in remaining:
        for empty_facet in remaining:
            if empty_facet == position124:
                continue
            candidates = {
                facet: d124 if facet == position124 else (0,) if facet == empty_facet else equality
                for facet in remaining
            }
            rows.append(base.exact_q5_search(special, min(d71), candidates))
    result["195"] = summarize(rows)

    rows = []
    for other28 in combinations(remaining, 6):
        candidates = {
            facet: d28 if facet in other28 else equality for facet in remaining
        }
        rows.append(base.exact_q5_search(special, min(d28), candidates))
    result["196"] = summarize(rows)

    rows = []
    for second99 in remaining:
        available = tuple(facet for facet in remaining if facet != second99)
        for empty_facets in combinations(available, 2):
            candidates = {
                facet: d99 if facet == second99 else (0,) if facet in empty_facets else equality
                for facet in remaining
            }
            rows.append(base.exact_q5_search(special, min(d99), candidates))
    result["198"] = summarize(rows)
    return result


def verify():
    if parity_counterexample_delta() != 831:
        raise AssertionError("the explicit odd-Delta counterexample changed")
    census, census_nodes, local_table = base.facet_gluing_census()
    if len(census) != 327_553 or census_nodes != 110_747_623:
        raise AssertionError("unexpected S<=15 Q4 census")
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
        raise AssertionError("unexpected structural profile list below 200")

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
        profile: (
            equality if profile[0] == 0 else profile_catalog(census, boundary, profile)
        )
        for profile in profiles
    }
    expected_sizes = [64, 192, 32, 192, 192, 32, 192]
    if [len(catalogs[profile]) for profile in profiles] != expected_sizes:
        raise AssertionError("unexpected residual catalog size")
    orbits = {
        str(profile[0]): base.orbit_summary(set(catalogs[profile]))
        for profile in profiles
    }
    if any(len(summary) != 1 for summary in orbits.values()):
        raise AssertionError("a residual catalog is not one Q4 orbit")

    old_residuals, _ = base.residual_searches(census, boundary)
    residuals = old_residuals | new_residual_searches(census, boundary, catalogs)
    if residuals != EXPECTED_RESIDUALS:
        raise AssertionError("a residual profile below 200 was not excluded")

    deficit_spectrum = Counter(
        17 * slack - 3 * mask.bit_count() for mask, slack in census.items()
    )
    if deficit_spectrum[183] or deficit_spectrum[186]:
        raise AssertionError("unexpected high-density deficit class")

    rows = [(*key, count) for key, count in sorted(class_counts.items())]
    profile_hash = sha256(
        json.dumps(rows, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    q4_hash = base.normalized_graph_hash(census)

    q5_ratio = Fraction(12 * 56 + 200, 34 * 56)
    global_coefficient = q5_ratio / 12
    new_constant = Fraction(4998, 2747)
    old_constant = Fraction(19992, 11005)
    if q5_ratio != Fraction(109, 238):
        raise AssertionError("incorrect Q5 ratio")
    if global_coefficient != Fraction(109, 2856):
        raise AssertionError("incorrect global coefficient")
    if new_constant - old_constant != Fraction(84966, 30230735):
        raise AssertionError("incorrect asymptotic improvement")

    canonical = {
        "local_table": [(*key, count) for key, count in sorted(local_table.items())],
        "profile_classes": rows,
        "survivors": survivors,
        "residuals": residuals,
        "orbits": orbits,
        "capacities": capacities,
    }
    audit_hash = sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    return {
        "q4_facet_gluing_nodes": census_nodes,
        "q4_patterns_with_slack_at_most_15": len(census),
        "q4_normalized_graph_set_sha256": q4_hash,
        "q4_positive_profile_classes_below_200": len(class_counts),
        "profile_class_sha256": profile_hash,
        "structural_survivor_totals": [row[0] for row in survivors],
        "parity_counterexample_delta": 831,
        "residual_catalog_orbits": orbits,
        "residual_searches": residuals,
        "q5_deficit_lower_bound": 200,
        "q5_slack_edge_ratio": str(q5_ratio),
        "global_slack_coefficient": str(global_coefficient),
        "bound": "sat(Q_d,Q_2) >= 4998*d*2^d/(2747*d+7249) for d>=5",
        "asymptotic_constant": str(new_constant),
        "improvement_over_gap166_constant": str(new_constant - old_constant),
        "finite_bound_cross_difference": "84966*(d-1)",
        "integer_lower_bounds_d7_d8": [170, 351],
        "audit_sha256": audit_hash,
    }


def main():
    print(json.dumps(verify(), sort_keys=True, indent=2))
    print("status=PASS")


if __name__ == "__main__":
    main()
