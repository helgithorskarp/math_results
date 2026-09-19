#!/usr/bin/env python3
"""Exact verifier for the unattainability of Q5 facet deficit 217.

No S=17 census is performed.  The accepted S<=16 census is replayed with
the endpoint delta=217 included in its boundary classification.  The only
possible endpoint outside that census, (E,S)=(24,17), is handled by an exact
cover/incidence lemma.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "hypercube_square_saturation_q5_gap217" / "verify.py"


def load_parent():
    spec = spec_from_file_location("accepted_gap217_engine", PARENT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load accepted gap-217 engine")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


parent = load_parent()
base = parent.base
base.MAX_SLACK = 16
base.MAX_TWICE_SLACK = 32
base.DEFICIT_LIMIT = 218

P42 = (42, 20, 0, 0)
P48 = (48, 18, 3, 0)
P85 = (85, 17, 4, 0)
P91 = (91, 15, 4, 1)
P127 = (127, 20, 3, 0)
P217_A = (217, 7, 5, 2)
P217_B = (217, 7, 7, 1)

EXPECTED_PROFILES = (
    (217, (P42, P42, P42, P91), 5, 1, 40),
    (217, (P42, P42, P48, P85), 5, 1, 40),
    (217, (P42, P48, P127), 6, 1, 40),
)

EXPECTED_ORBITS = {
    P42: [("0x18bb77ee", 32, 12)],
    P48: [("0x07ff2336", 192, 2)],
    P85: [("0x0333ff49", 192, 2), ("0x06ff1933", 384, 1)],
    P91: [("0x03337f14", 384, 1)],
    P127: [("0x19ab77ee", 384, 1)],
    P217_A: [("0x0001050f", 192, 2)],
    P217_B: [("0x0001070d", 192, 2)],
}

EXPECTED_CLOSURES = (
    (1512, 1638, 1, 0),
    (3024, 3276, 1, 0),
    (504, 560, 1, 0),
)


def extremal_q4_exact_covers():
    """Enumerate omitted edges meeting every Q4 square exactly once."""

    edge_square_masks = [0] * len(base.EDGES)
    for square_index, square in enumerate(base.SQUARES):
        for edge in square:
            edge_square_masks[edge] |= 1 << square_index
    full = (1 << len(base.SQUARES)) - 1
    covers = set()

    def visit(covered, missing):
        if covered == full:
            covers.add(tuple(sorted(missing)))
            return
        if len(missing) >= 8:
            return
        uncovered = full & ~covered
        square_index = (uncovered & -uncovered).bit_length() - 1
        for edge in base.SQUARES[square_index]:
            incident = edge_square_masks[edge]
            if incident & covered:
                continue
            visit(covered | incident, missing + (edge,))

    visit(0, ())
    spectra = Counter()
    all_edges = (1 << len(base.EDGES)) - 1
    for cover in covers:
        missing = sum(1 << edge for edge in cover)
        edges, active, pairs, slack = base.direct_q4_statistics(all_edges ^ missing)
        spectra[(edges, active, pairs, slack, 17 * slack - 3 * edges)] += 1
    expected = Counter({(24, 24, 24, 24, 336): 8})
    if spectra != expected:
        raise AssertionError("unexpected extremal Q4 spectrum")
    return len(covers), spectra


def exact_217_profiles(class_counts, capacities):
    classes = tuple(sorted(class_counts))
    survivors = set()

    def visit(start, chosen, total):
        if chosen and total == 217:
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
                exceptional = positive_count + empty_count - 1
                if any(item[2] > exceptional for item in chosen):
                    continue
                survivors.add(
                    (217, chosen, equality_count, empty_count, global_edges)
                )
            return
        if total >= 217 or len(chosen) == 9:
            return
        for index in range(start, len(classes)):
            item = classes[index]
            if total + item[0] > 217:
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


def close_profile(profile, catalogs, orbit_summaries, equality):
    _, positive, equality_count, empty_count, _ = profile
    counts = Counter(positive)
    fixed_profile = min(
        counts,
        key=lambda item: (len(orbit_summaries[item]), len(catalogs[item]), item),
    )
    counts[fixed_profile] -= 1
    if not counts[fixed_profile]:
        del counts[fixed_profile]
    if equality_count:
        counts["equality"] = equality_count
    if empty_count:
        counts["empty"] = empty_count

    fixed_facet = (0, 0)
    remaining = tuple(facet for facet in base.Q5_FACETS if facet != fixed_facet)
    cases = nodes = solutions = max_depth = 0
    for representative_hex, _, _ in orbit_summaries[fixed_profile]:
        for assignment in multiset_assignments(remaining, counts):
            candidates = {
                facet: (
                    equality
                    if assignment[facet] == "equality"
                    else (0,)
                    if assignment[facet] == "empty"
                    else catalogs[assignment[facet]]
                )
                for facet in remaining
            }
            found, visited, depth = base.exact_q5_search(
                fixed_facet, int(representative_hex, 16), candidates
            )
            cases += 1
            nodes += visited
            solutions += found
            max_depth = max(max_depth, depth)
    return cases, nodes, max_depth, solutions


def verify():
    # Solve 17S-3E=217 under E<=24.  Only S=14,E=7 is in the
    # accepted S<=16 census; the exact-cover calculation excludes S=17,E=24.
    diophantine = tuple(
        (edges, slack)
        for slack in range(18)
        for edges in range(25)
        if 17 * slack - 3 * edges == 217
    )
    if diophantine != ((7, 14), (24, 17)):
        raise AssertionError("unexpected delta-217 Diophantine frontier")
    cover_count, cover_spectrum = extremal_q4_exact_covers()

    census, census_nodes, _ = base.facet_gluing_census()
    if len(census) != 490_753 or census_nodes != 146_812_464:
        raise AssertionError("accepted S<=16 census changed")
    graph_hash = base.normalized_graph_hash(census)
    if graph_hash != "9274309488ef16e6e49a2066e83a364e704d99b716f271740427421ca90b5189":
        raise AssertionError("accepted census graph hash changed")

    equality = tuple(
        mask
        for mask, slack in census.items()
        if mask and 17 * slack - 3 * mask.bit_count() == 0
    )
    boundary, class_counts = base.boundary_classification(census, equality)
    rows = [(*profile, count) for profile, count in sorted(class_counts.items())]
    profile_hash = sha256(
        json.dumps(rows, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    if len(rows) != 182 or profile_hash != "9dc4c10874d87acd730ab6fb0741b23da45c13a4d01ba29149dcc11e8f4aefbb":
        raise AssertionError("unexpected endpoint profile table")
    certificate = json.loads((HERE / "PROFILE_CLASSES.json").read_text())
    if certificate != [list(row) for row in rows]:
        raise AssertionError("exported profile certificate disagrees with census")

    endpoint = {key: value for key, value in class_counts.items() if key[0] == 217}
    if endpoint != Counter({P217_A: 192, P217_B: 192}):
        raise AssertionError("unexpected delta-217 endpoint classes")
    capacities = {
        live: max(base.live_support_distribution(live)) for live in range(1, 11)
    }
    profiles = exact_217_profiles(class_counts, capacities)
    if profiles != EXPECTED_PROFILES:
        raise AssertionError("unexpected necessary total-217 profiles")

    needed = tuple(EXPECTED_ORBITS)
    catalogs = {
        item: parent.parent.profile_catalog(census, boundary, item)
        for item in needed
    }
    orbit_summaries = {
        item: base.orbit_summary(set(catalogs[item])) for item in needed
    }
    if orbit_summaries != EXPECTED_ORBITS:
        raise AssertionError("unexpected frontier orbit certificate")
    closures = tuple(
        close_profile(profile, catalogs, orbit_summaries, equality)
        for profile in profiles
    )
    if closures != EXPECTED_CLOSURES:
        raise AssertionError("unexpected total-217 residual closure")

    q5_ratio = Fraction(12 * 56 + 218, 34 * 56)
    global_coefficient = q5_ratio / 12
    asymptotic = Fraction(19992, 10979)
    previous = Fraction(5712, 3137)
    if (q5_ratio, global_coefficient) != (Fraction(445, 952), Fraction(445, 11424)):
        raise AssertionError("incorrect local-to-global coefficient")
    if asymptotic - previous != Fraction(2856, 34441123):
        raise AssertionError("incorrect asymptotic improvement")
    integer_bounds = []
    for dimension in range(5, 12):
        old_value = Fraction(
            5712 * dimension * 2**dimension, 3137 * dimension + 8287
        )
        new_value = Fraction(
            19992 * dimension * 2**dimension, 10979 * dimension + 29005
        )
        old_ceiling = (old_value.numerator + old_value.denominator - 1) // old_value.denominator
        new_ceiling = (new_value.numerator + new_value.denominator - 1) // new_value.denominator
        integer_bounds.append((dimension, old_ceiling, new_ceiling))
    if any(old != new for _, old, new in integer_bounds[:-1]):
        raise AssertionError("integer bound improves before dimension 11")
    if integer_bounds[-1] != (11, 3007, 3008):
        raise AssertionError("incorrect first integer improvement")

    return {
        "status": "PASS",
        "census_scope": "accepted Q4 S<=16 census; no S=17 census",
        "delta217_diophantine_cases": diophantine,
        "extremal_q4_exact_cover_count": cover_count,
        "extremal_q4_spectrum": {
            ":".join(map(str, key)): value
            for key, value in sorted(cover_spectrum.items())
        },
        "q4_patterns": len(census),
        "q4_census_nodes": census_nodes,
        "q4_graph_sha256": graph_hash,
        "profile_classes_through_217": len(rows),
        "profile_certificate_sha256": profile_hash,
        "delta217_endpoint_classes": {
            ":".join(map(str, key)): value for key, value in sorted(endpoint.items())
        },
        "necessary_total217_profiles": profiles,
        "residual_closures": closures,
        "total_cases": sum(row[0] for row in closures),
        "total_nodes": sum(row[1] for row in closures),
        "total_solutions": sum(row[3] for row in closures),
        "q5_deficit_lower_bound": 218,
        "q5_slack_edge_ratio": str(q5_ratio),
        "global_slack_coefficient": str(global_coefficient),
        "global_bound": "19992*d*2^d/(10979*d+29005)",
        "asymptotic_constant": str(asymptotic),
        "improvement_over_gap217": str(asymptotic - previous),
        "first_integer_improvement": {"dimension": 11, "old": 3007, "new": 3008},
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
