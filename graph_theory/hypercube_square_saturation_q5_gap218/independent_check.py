#!/usr/bin/env python3
"""Compact independent replay of the exact deficit-217 frontier.

This checker uses reviewer-owned cube definitions, the exported 182-row
profile certificate, independently regenerated Q4 automorphism orbits, and
generic endpoint-edge gluing.  It does not import the target verifier and it
does not rerun a low-slack or S=17 census.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent / "hypercube_square_saturation_q5_gap217_review1" / "review_check.py"


def load_review():
    spec = spec_from_file_location("independent_gap217_review", REVIEW)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load reviewer-owned gap-217 checker")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


review = load_review()
base = review.base

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

# Reviewer edge ordering; these representatives were converted by their
# actual endpoint pairs, not by assuming agreement with target bit positions.
REPRESENTATIVES = {
    "eq": (0x000DFFDD,),
    "42": (0x0DFFE55A,),
    "48": (0x001F7EFE,),
    "85": (0x71E2A07F, 0x0F7087E7),
    "91": (0x21F0B07E,),
    "127": (0xBBA27CBE,),
    "217a": (0x00023087,),
    "217b": (0x00023017,),
}

EXPECTED_SIZES = {
    "eq": 64,
    "42": 32,
    "48": 192,
    "85": 576,
    "91": 384,
    "127": 384,
    "217a": 192,
    "217b": 192,
}

EXPECTED_STATISTICS = {
    "eq": (17, 15, 3, 0),
    "42": (20, 18, 6, 42),
    "48": (18, 16, 6, 48),
    "85": (17, 14, 8, 85),
    "91": (15, 12, 8, 91),
    "127": (20, 17, 11, 127),
    "217a": (7, 4, 14, 217),
    "217b": (7, 4, 14, 217),
}

EXPECTED_BOUNDARIES = {
    "eq": (0, 1),
    "42": (0, 0),
    "48": (3, 0),
    "85": (4, 0),
    "91": (4, 1),
    "127": (3, 0),
    "217a": (5, 2),
    "217b": (7, 1),
}

ROWS = (
    ({"42": 3, "91": 1, "eq": 5, "empty": 1}, "42", 1512),
    ({"42": 2, "48": 1, "85": 1, "eq": 5, "empty": 1}, "42", 3024),
    ({"42": 1, "48": 1, "127": 1, "eq": 6, "empty": 1}, "42", 504),
)


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
                if not global_edges or global_edges > capacities[live_count - 1]:
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


def check():
    rows = json.loads((HERE / "PROFILE_CLASSES.json").read_text())
    profile_hash = sha256(
        json.dumps(rows, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    if len(rows) != 182 or profile_hash != "9dc4c10874d87acd730ab6fb0741b23da45c13a4d01ba29149dcc11e8f4aefbb":
        raise AssertionError("profile certificate hash or size changed")
    class_counts = Counter({tuple(row[:4]): row[4] for row in rows})
    endpoint = {key: value for key, value in class_counts.items() if key[0] == 217}
    if endpoint != {P217_A: 192, P217_B: 192}:
        raise AssertionError("unexpected endpoint profile rows")

    capacities = base.live_capacity_maxima()
    if capacities != [0, 0, 0, 1, 5, 9, 16, 28, 48, 80]:
        raise AssertionError("unexpected live-facet capacities")
    profiles = exact_217_profiles(class_counts, capacities)
    if profiles != EXPECTED_PROFILES:
        raise AssertionError("profile certificate has a different frontier")

    catalogs = {}
    orbit_sizes = {}
    for label, representatives in REPRESENTATIVES.items():
        pieces = tuple(base.orbit(mask) for mask in representatives)
        union = tuple(frozenset(pattern for piece in pieces for pattern in piece))
        if len(union) != sum(map(len, pieces)):
            raise AssertionError(f"overlapping asserted orbits for {label}")
        catalogs[label] = union
        orbit_sizes[label] = tuple(map(len, pieces))
    catalogs["empty"] = (frozenset(),)
    if {label: len(catalogs[label]) for label in EXPECTED_SIZES} != EXPECTED_SIZES:
        raise AssertionError("unexpected frontier catalog size")
    for label in EXPECTED_SIZES:
        if set(map(base.q4_statistics, catalogs[label])) != {EXPECTED_STATISTICS[label]}:
            raise AssertionError(f"incorrect statistics for {label}")

    extendable = frozenset(
        base.facet_signature(pattern, facet)
        for pattern in catalogs["eq"]
        for facet in base.Q4_FACETS
    )
    boundaries = {
        label: base.boundary_profile(catalogs[label], extendable)
        for label in EXPECTED_SIZES
    }
    if boundaries != EXPECTED_BOUNDARIES:
        raise AssertionError("unexpected independently regenerated boundaries")

    embedded = {
        label: tuple(
            tuple(base.embed_q4(pattern, facet) for pattern in catalog)
            for facet in base.Q5_FACETS
        )
        for label, catalog in catalogs.items()
    }
    closures = []
    for counts, fixed_label, expected_cases in ROWS:
        remaining = dict(counts)
        remaining[fixed_label] -= 1
        cases = solutions = 0
        fixed_pattern = base.mask_edges(REPRESENTATIVES[fixed_label][0])
        for labels in base.multiset_words(remaining):
            cases += 1
            solutions += base.gluing_solutions(labels, fixed_pattern, embedded)
        if cases != expected_cases or solutions:
            raise AssertionError("independent residual gluing failed")
        closures.append((cases, solutions))

    cover_count, cover_spectrum = review.extremal_q4_exact_covers()
    if cover_count != 8 or cover_spectrum != Counter({(24, 24, 336): 8}):
        raise AssertionError("unexpected exact-cover boundary spectrum")
    q5_ratio = Fraction(12 * 56 + 218, 34 * 56)
    coefficient = q5_ratio / 12
    asymptotic = Fraction(19992, 10979)
    previous = Fraction(5712, 3137)
    if (q5_ratio, coefficient) != (Fraction(445, 952), Fraction(445, 11424)):
        raise AssertionError("incorrect global coefficient")
    if asymptotic - previous != Fraction(2856, 34441123):
        raise AssertionError("incorrect improvement")
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
        "profile_rows": len(rows),
        "profile_certificate_sha256": profile_hash,
        "necessary_total217_profiles": profiles,
        "frontier_orbit_sizes": orbit_sizes,
        "frontier_boundaries": boundaries,
        "independent_residual_closures": closures,
        "total_cases": sum(row[0] for row in closures),
        "total_solutions": sum(row[1] for row in closures),
        "extremal_q4_exact_cover_count": cover_count,
        "extremal_q4_spectrum": {
            ":".join(map(str, key)): value
            for key, value in sorted(cover_spectrum.items())
        },
        "q5_deficit_lower_bound": 218,
        "q5_slack_edge_ratio": str(q5_ratio),
        "global_slack_coefficient": str(coefficient),
        "global_bound": "19992*d*2^d/(10979*d+29005)",
        "asymptotic_constant": str(asymptotic),
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2, sort_keys=True))
