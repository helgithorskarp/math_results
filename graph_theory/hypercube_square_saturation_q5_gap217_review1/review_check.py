#!/usr/bin/env python3
"""Reviewer-owned checks for the Q5 facet-deficit gap 217.

This standard-library checker imports only the preceding reviewer-owned
definition-level checker, not either gap-217 target engine.  It independently
rebuilds every new proof-critical Q4 orbit, tests the extremal 24-edge Q4
case by exact cover, derives all frontier placement counts from multiset
multiplicities, closes the 28,470 placements with a generic boundary gluer,
and verifies the global rational algebra.  It is not a third complete census
of all Q4 patterns with slack at most 16.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
from math import factorial
from pathlib import Path
import json


def load_review_base():
    path = (
        Path(__file__).resolve().parent.parent
        / "hypercube_square_saturation_q5_gap200_review1"
        / "review_check.py"
    )
    spec = spec_from_file_location("gap200_reviewer_engine", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the preceding reviewer checker")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load_review_base()


ORBIT_REPRESENTATIVES = {
    "eq": (0x000DFFDD,),
    "28": (0x00BDFFEC,),
    "42_0": (0x0DFFE55A,),
    "42_6": (0x1E7F96EC,),
    "42_7": (0x14FF9D1F, 0x14FF9D6E, 0x14FF9EEC),
    "48": (0x001F7EFE,),
    "65": (0x00BF7F6C, 0x00BFEF6C),
    "71": (0x000D5FFE,),
    "124": (0x0DFF753B,),
}


EXPECTED_ORBIT_SIZES = {
    "eq": (64,),
    "28": (192,),
    "42_0": (32,),
    "42_6": (32,),
    "42_7": (128, 384, 384),
    "48": (192,),
    "65": (384, 192),
    "71": (192,),
    "124": (192,),
}


EXPECTED_STATISTICS = {
    "eq": (17, 15, 3, 0),
    "28": (19, 17, 5, 28),
    "42_0": (20, 18, 6, 42),
    "42_6": (20, 18, 6, 42),
    "42_7": (20, 18, 6, 42),
    "48": (18, 16, 6, 48),
    "65": (18, 15, 7, 65),
    "71": (16, 13, 7, 71),
    "124": (21, 19, 11, 124),
}


EXPECTED_BOUNDARIES = {
    "eq": (0, 1),
    "28": (6, 0),
    "42_0": (0, 0),
    "42_6": (6, 0),
    "42_7": (7, 0),
    "48": (3, 0),
    "65": (4, 0),
    "71": (2, 1),
    "124": (1, 0),
}


# (total, profile-count dictionary, fixed profile).  Distinct rows at total
# 210 are deliberately retained rather than compressed into a target table.
FRONTIER_ROWS = (
    (203, {"42_0": 2, "48": 1, "71": 1, "eq": 6}, "71"),
    (205, {"28": 5, "65": 1, "eq": 3, "empty": 1}, "65"),
    (208, {"42_0": 2, "124": 1, "eq": 7}, "124"),
    (210, {"28": 6, "42_0": 1, "eq": 2, "empty": 1}, "42_0"),
    (210, {"28": 6, "42_6": 1, "eq": 2, "empty": 1}, "42_6"),
    (210, {"28": 6, "42_7": 1, "eq": 2, "empty": 1}, "42_7"),
    (210, {"28": 3, "42_0": 3, "eq": 3, "empty": 1}, "42_0"),
    (210, {"28": 3, "42_0": 2, "42_6": 1, "eq": 3, "empty": 1}, "42_6"),
    (210, {"28": 3, "42_0": 1, "42_6": 2, "eq": 3, "empty": 1}, "42_6"),
    (210, {"28": 3, "42_6": 3, "eq": 3, "empty": 1}, "42_6"),
    (210, {"42_0": 5, "eq": 4, "empty": 1}, "42_0"),
    (215, {"48": 3, "71": 1, "eq": 6}, "71"),
)


def disjoint_orbit_catalogs():
    catalogs = {}
    orbit_sizes = {}
    for label, representatives in ORBIT_REPRESENTATIVES.items():
        pieces = tuple(base.orbit(mask) for mask in representatives)
        union = frozenset(pattern for piece in pieces for pattern in piece)
        if len(union) != sum(map(len, pieces)):
            raise AssertionError(f"overlapping asserted orbits for {label}")
        catalogs[label] = tuple(union)
        orbit_sizes[label] = tuple(len(piece) for piece in pieces)
    catalogs["empty"] = (frozenset(),)
    if orbit_sizes != EXPECTED_ORBIT_SIZES:
        raise AssertionError("unexpected proof-critical orbit sizes")
    return catalogs, orbit_sizes


def extremal_q4_exact_covers():
    """Enumerate all 8-edge sets meeting each Q4 square exactly once."""

    edge_index = {edge: index for index, edge in enumerate(base.Q4_EDGES)}
    square_edges = tuple(
        tuple(edge_index[edge] for edge in square) for square in base.Q4_SQUARES
    )
    edge_square_masks = [0] * len(base.Q4_EDGES)
    for square_index, square in enumerate(square_edges):
        for edge in square:
            edge_square_masks[edge] |= 1 << square_index
    all_squares = (1 << len(square_edges)) - 1
    covers = set()

    def visit(covered, missing):
        if covered == all_squares:
            covers.add(frozenset(missing))
            return
        if len(missing) >= 8:
            return
        uncovered = all_squares & ~covered
        square = (uncovered & -uncovered).bit_length() - 1
        for edge in square_edges[square]:
            incident = edge_square_masks[edge]
            if incident & covered:
                continue
            visit(covered | incident, missing + (edge,))

    visit(0, ())
    spectra = Counter()
    for missing in covers:
        chosen = frozenset(
            edge for index, edge in enumerate(base.Q4_EDGES) if index not in missing
        )
        edges, _, slack, deficit = base.q4_statistics(chosen)
        spectra[(edges, slack, deficit)] += 1
    if len(covers) != 8 or spectra != Counter({(24, 24, 336): 8}):
        raise AssertionError("unexpected extremal Q4 exact-cover spectrum")
    return len(covers), spectra


def seven_edge_q4_audit():
    """Exhaust the other Diophantine possibility for Q4 deficit 200."""

    edge_index = {edge: index for index, edge in enumerate(base.Q4_EDGES)}
    squares = []
    for square in base.Q4_SQUARES:
        edges = tuple(edge_index[edge] for edge in square)
        squares.append((sum(1 << edge for edge in edges), edges))
    spectrum = Counter()
    square_free_count = 0
    for chosen_edges in combinations(range(len(base.Q4_EDGES)), 7):
        mask = sum(1 << edge for edge in chosen_edges)
        if any(mask & square_mask == square_mask for square_mask, _ in squares):
            continue
        square_free_count += 1
        missing = []
        for square_mask, edges in squares:
            if (mask & square_mask).bit_count() == 3:
                missing.append(next(edge for edge in edges if not (mask >> edge) & 1))
        multiplicities = Counter(missing)
        pairs = sum(value * (value - 1) // 2 for value in multiplicities.values())
        slack = 42 - 7 * len(missing) + 2 * pairs
        spectrum[slack] += 1
    if square_free_count != 3_287_328 or spectrum[13] != 0:
        raise AssertionError("unexpected seven-edge Q4 spectrum")
    return square_free_count, dict(sorted(spectrum.items()))


def expected_placement_count(counts, fixed_label):
    remaining = dict(counts)
    remaining[fixed_label] -= 1
    if remaining[fixed_label] == 0:
        del remaining[fixed_label]
    result = factorial(9)
    for count in remaining.values():
        result //= factorial(count)
    return result * len(ORBIT_REPRESENTATIVES[fixed_label]), remaining


def check_frontier(catalogs):
    embedded = {
        label: tuple(
            tuple(base.embed_q4(pattern, facet) for pattern in catalog)
            for facet in base.Q5_FACETS
        )
        for label, catalog in catalogs.items()
    }
    grouped = {}
    for total, counts, fixed_label in FRONTIER_ROWS:
        expected, remaining = expected_placement_count(counts, fixed_label)
        cases = 0
        solutions = 0
        for representative in ORBIT_REPRESENTATIVES[fixed_label]:
            fixed_pattern = base.mask_edges(representative)
            for labels in base.multiset_words(remaining):
                cases += 1
                solutions += base.gluing_solutions(labels, fixed_pattern, embedded)
        if cases != expected or solutions:
            raise AssertionError(f"frontier row {total} failed")
        row = grouped.setdefault(
            str(total), {"profiles": 0, "cases": 0, "solutions": 0}
        )
        row["profiles"] += 1
        row["cases"] += cases
        row["solutions"] += solutions
    expected = {
        "203": {"profiles": 1, "cases": 252, "solutions": 0},
        "205": {"profiles": 1, "cases": 1008, "solutions": 0},
        "208": {"profiles": 1, "cases": 36, "solutions": 0},
        "210": {"profiles": 8, "cases": 27090, "solutions": 0},
        "215": {"profiles": 1, "cases": 84, "solutions": 0},
    }
    if grouped != expected:
        raise AssertionError("unexpected grouped frontier closure")
    return grouped


def check():
    catalogs, orbit_sizes = disjoint_orbit_catalogs()
    equality = catalogs["eq"]
    extendable = frozenset(
        base.facet_signature(pattern, facet)
        for pattern in equality
        for facet in base.Q4_FACETS
    )
    statistics = {}
    boundaries = {}
    for label in ORBIT_REPRESENTATIVES:
        values = set(map(base.q4_statistics, catalogs[label]))
        if values != {EXPECTED_STATISTICS[label]}:
            raise AssertionError(f"incorrect statistics for {label}")
        statistics[label] = EXPECTED_STATISTICS[label]
        boundaries[label] = base.boundary_profile(catalogs[label], extendable)
    if boundaries != EXPECTED_BOUNDARIES:
        raise AssertionError("incorrect boundary data for frontier catalogs")

    deficit_200_solutions = tuple(
        (edges, slack)
        for slack in range(17)
        for edges in range(25)
        if 17 * slack - 3 * edges == 200
    )
    if deficit_200_solutions != ((7, 13), (24, 16)):
        raise AssertionError("unexpected Diophantine cases for deficit 200")
    seven_edge_count, seven_edge_spectrum = seven_edge_q4_audit()
    cover_count, cover_spectrum = extremal_q4_exact_covers()
    frontier = check_frontier(catalogs)
    if sum(row["cases"] for row in frontier.values()) != 28_470:
        raise AssertionError("incorrect total frontier placement count")

    capacities = base.live_capacity_maxima()
    if capacities != [0, 0, 0, 1, 5, 9, 16, 28, 48, 80]:
        raise AssertionError("incorrect live-facet capacities")
    q5_ratio = Fraction(12 * 56 + 217, 34 * 56)
    global_coefficient = q5_ratio / 12
    new_constant = Fraction(5712, 3137)
    old_constant = Fraction(4998, 2747)
    if (q5_ratio, global_coefficient) != (Fraction(127, 272), Fraction(127, 3264)):
        raise AssertionError("incorrect local-to-global coefficients")
    if new_constant - old_constant != Fraction(12138, 8617339):
        raise AssertionError("incorrect improvement over gap 200")
    integer_comparison = {}
    for dimension in range(5, 12):
        new_value = Fraction(
            5712 * dimension * 2**dimension, 3137 * dimension + 8287
        )
        old_value = Fraction(
            4998 * dimension * 2**dimension, 2747 * dimension + 7249
        )
        integer_comparison[str(dimension)] = (
            (old_value.numerator + old_value.denominator - 1) // old_value.denominator,
            (new_value.numerator + new_value.denominator - 1) // new_value.denominator,
        )
    if any(integer_comparison[str(d)][0] != integer_comparison[str(d)][1] for d in range(5, 11)):
        raise AssertionError("integer bound improves before dimension 11")
    if integer_comparison["11"] != (3006, 3007):
        raise AssertionError("incorrect first integer improvement")

    return {
        "cutoff_arithmetic": {
            "max_q4_edges": 24,
            "largest_slack_below_217": 16,
            "next_layer_minimum_deficit": 217,
        },
        "deficit_200_diophantine_cases": deficit_200_solutions,
        "square_free_q4_patterns_with_7_edges": seven_edge_count,
        "seven_edge_minimum_slack": min(seven_edge_spectrum),
        "seven_edge_patterns_with_slack_13": seven_edge_spectrum.get(13, 0),
        "extremal_q4_exact_cover_count": cover_count,
        "extremal_q4_spectrum": {
            f"E={edges},S={slack},delta={deficit}": count
            for (edges, slack, deficit), count in sorted(cover_spectrum.items())
        },
        "proof_critical_orbit_sizes": orbit_sizes,
        "proof_critical_statistics": statistics,
        "proof_critical_boundaries": boundaries,
        "frontier_gluing": frontier,
        "total_frontier_placements": 28_470,
        "live_facet_capacity_maxima": capacities,
        "q5_slack_edge_ratio": str(q5_ratio),
        "global_slack_coefficient": str(global_coefficient),
        "asymptotic_constant": str(new_constant),
        "improvement_over_gap200": str(new_constant - old_constant),
        "first_integer_improvement": {
            "dimension": 11,
            "old": 3006,
            "new": 3007,
        },
        "status": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2, sort_keys=True))
