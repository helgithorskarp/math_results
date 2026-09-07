#!/usr/bin/env python3
"""Independent audit of the rank-five global sieve and four-set lemma.

No target module is imported.  Capped spanning words are reconstructed by
explicit linear/affine subspace posets and exponential generating functions.
The four-set contradiction is checked over every distribution of its sixteen
distinguishing contact signatures.
"""

from __future__ import annotations

import argparse
import base64
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from math import comb, factorial, prod
from pathlib import Path


RANK = 5
LEFT = 20
RIGHT = 23
GL5 = 9_999_360
CLAIMED_BASELINE = 5_265_776_463_769_286_448_156_565_145_344_760_253_473_964_876_758_764_876_800
CLAIMED_REMOVED = 2_066_365_377_174_402_749_659_084_812_993_090_655_368_806_390_234_845_516_800
CLAIMED_REMAINING = 3_199_411_086_594_883_698_497_480_332_351_669_598_105_158_486_523_919_360_000
CLAIMED_FRACTION = Fraction(
    72_250_993_667_250_533_318_774_539_803_589_602_314_409_997,
    184_119_220_220_965_173_622_650_664_548_131_290_651_799_397,
)
CLAIMED_INCREMENTAL = 319_639_601_769_240_155_564_925_006_980_617_339_728_513_107_340_597_120_000
CLAIMED_INCREMENTAL_FRACTION = Fraction(
    1_381_295_518_673_381_498_026_176_252_447_729,
    15_207_280_070_793_831_858_140_556_386_411_641,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


@lru_cache(None)
def bounded_words(length: int, letters: int, cap: int) -> int:
    """length! [x^length] (sum_(j=0)^cap x^j/j!)^letters."""
    require(length >= 0 and letters >= 0 and cap >= 1, "bounded-word parameters")
    coefficients = [Fraction(0) for _ in range(length + 1)]
    coefficients[0] = Fraction(1)
    letter = [Fraction(1, factorial(j)) for j in range(min(cap, length) + 1)]
    for _ in range(letters):
        updated = [Fraction(0) for _ in range(length + 1)]
        for old_degree, old_value in enumerate(coefficients):
            if not old_value:
                continue
            for added_degree, added_value in enumerate(letter):
                if old_degree + added_degree <= length:
                    updated[old_degree + added_degree] += old_value * added_value
        coefficients = updated
    answer = coefficients[length] * factorial(length)
    require(answer.denominator == 1, "nonintegral exponential coefficient")
    return answer.numerator


@lru_cache(None)
def linear_subspaces(rank: int) -> tuple[frozenset[int], ...]:
    """Generate every concrete subspace of F_2^rank exactly once."""
    spaces = {frozenset({0})}
    for vector in range(1, 1 << rank):
        snapshot = tuple(spaces)
        for space in snapshot:
            spaces.add(frozenset(space | {x ^ vector for x in space}))
    return tuple(sorted(spaces, key=lambda space: (len(space), tuple(sorted(space)))))


@lru_cache(None)
def affine_hyperplane_subspaces(rank: int) -> tuple[frozenset[int], ...]:
    """Every affine subspace of {x: high_bit(x)=1} in F_2^rank."""
    require(rank >= 1, "positive affine rank")
    high = 1 << (rank - 1)
    hyperplane = range(high, 2 * high)
    spaces: set[frozenset[int]] = set()
    for direction in linear_subspaces(rank - 1):
        for point in hyperplane:
            spaces.add(frozenset(point ^ vector for vector in direction))
    return tuple(sorted(spaces, key=lambda space: (len(space), tuple(sorted(space)))))


@lru_cache(None)
def predecessor_indices(kind: str, rank: int) -> tuple[tuple[int, ...], ...]:
    spaces = linear_subspaces(rank) if kind == "linear" else affine_hyperplane_subspaces(rank)
    return tuple(
        tuple(j for j, smaller in enumerate(spaces[:i]) if smaller < space)
        for i, space in enumerate(spaces)
    )


@lru_cache(None)
def exact_nonzero_span(length: int, rank: int, cap: int) -> int:
    spaces = linear_subspaces(rank)
    predecessors = predecessor_indices("linear", rank)
    exact: list[int] = []
    for i, space in enumerate(spaces):
        value = bounded_words(length, len(space) - 1, cap)
        value -= sum(exact[j] for j in predecessors[i])
        require(value >= 0, "negative exact linear-span count")
        exact.append(value)
    require(len(spaces[-1]) == 1 << rank, "missing full linear space")
    return exact[-1]


@lru_cache(None)
def exact_affine_span(length: int, rank: int, cap: int) -> int:
    require(length > 0, "positive affine word length")
    spaces = affine_hyperplane_subspaces(rank)
    predecessors = predecessor_indices("affine", rank)
    exact: list[int] = []
    for i, space in enumerate(spaces):
        value = bounded_words(length, len(space), cap)
        value -= sum(exact[j] for j in predecessors[i])
        require(value >= 0, "negative exact affine-span count")
        exact.append(value)
    require(len(spaces[-1]) == 1 << (rank - 1), "missing full affine hyperplane")
    return exact[-1]


@lru_cache(None)
def exact_all_vector_span(length: int, rank: int) -> int:
    spaces = linear_subspaces(rank)
    predecessors = predecessor_indices("linear", rank)
    exact: list[int] = []
    for i, space in enumerate(spaces):
        value = len(space) ** length
        value -= sum(exact[j] for j in predecessors[i])
        require(value >= 0, "negative unrestricted span count")
        exact.append(value)
    return exact[-1]


def divide_by_gl(numerator: int) -> int:
    quotient, remainder = divmod(numerator, GL5)
    require(remainder == 0, "nonintegral GL(5,2) quotient")
    return quotient


def table_cap(cap: int) -> int:
    return 23 if cap >= 20 else cap


def complement_rank_four(left_cap: int, right_cap: int) -> int:
    numerator = (
        31 * 16
        * exact_affine_span(LEFT, RANK, table_cap(left_cap))
        * exact_affine_span(RIGHT, RANK, table_cap(right_cap))
    )
    return divide_by_gl(numerator)


def capped_pair_count(left_cap: int, right_cap: int, left_zero: int, right_zero: int) -> int:
    numerator = 0
    for i in range(left_zero + 1):
        for j in range(right_zero + 1):
            if i and j:
                continue
            numerator += (
                comb(LEFT, i)
                * comb(RIGHT, j)
                * exact_nonzero_span(LEFT - i, RANK, table_cap(left_cap))
                * exact_nonzero_span(RIGHT - j, RANK, table_cap(right_cap))
            )
    return divide_by_gl(numerator)


def counting_audit() -> dict[str, object]:
    require(len(linear_subspaces(5)) == 374, "rank-five subspace census")
    require(len(affine_hyperplane_subspaces(5)) == 307, "affine-subspace census")
    require(GL5 == prod((1 << 5) - (1 << i) for i in range(5)), "GL order")

    # These are all 212 word-count entries claimed as cross-checked by the target.
    entries = 0
    for cap in (3, 4, 5, 23):
        for length in range(24):
            exact_nonzero_span(length, 5, cap)
            entries += 1
            if length:
                exact_affine_span(length, 5, cap)
                entries += 1
    for length in range(24):
        exact_all_vector_span(length, 5)
        entries += 1
    require(entries == 212, "word-entry coverage")

    total = divide_by_gl(
        exact_all_vector_span(LEFT, RANK) * exact_all_vector_span(RIGHT, RANK)
    )
    stages: list[dict[str, object]] = []

    def append(stage: str, raw: int, overlap: int) -> None:
        stages.append(
            {
                "stage": stage,
                "raw": raw,
                "complement_rank_four": overlap,
                "remaining": raw - overlap,
            }
        )

    append(
        "rank_five_with_blue_rank_at_least_five",
        total,
        complement_rank_four(20, 23),
    )
    for stage, left_cap, right_cap, left_zero, right_zero in (
        ("no_zero_pair", 20, 23, 20, 23),
        ("zero_multiplicity_caps", 20, 23, 1, 2),
        ("previous_row_cap_four", 4, 23, 1, 2),
        ("column_cap_five", 4, 5, 1, 2),
        ("new_row_cap_three", 3, 5, 1, 2),
    ):
        append(
            stage,
            capped_pair_count(left_cap, right_cap, left_zero, right_zero),
            complement_rank_four(left_cap, right_cap),
        )

    baseline = stages[0]["remaining"]
    remaining = stages[-1]["remaining"]
    require(type(baseline) is int and type(remaining) is int, "integer stage values")
    removed = baseline - remaining
    removed_fraction = Fraction(removed, baseline)
    incremental = stages[-2]["remaining"] - remaining
    require(type(incremental) is int, "integer incremental value")
    incremental_fraction = Fraction(incremental, stages[-2]["remaining"])
    require(baseline == CLAIMED_BASELINE, "baseline disagreement")
    require(removed == CLAIMED_REMOVED, "removed disagreement")
    require(remaining == CLAIMED_REMAINING, "remaining disagreement")
    require(removed_fraction == CLAIMED_FRACTION, "removed fraction disagreement")
    require(incremental == CLAIMED_INCREMENTAL, "incremental disagreement")
    require(incremental_fraction == CLAIMED_INCREMENTAL_FRACTION,
            "incremental fraction disagreement")
    return {
        "method": "explicit subspace posets plus exponential generating functions",
        "linear_subspaces_F2_5": 374,
        "affine_subspaces_F2_4": 307,
        "spanning_word_entries": entries,
        "factor_fiber": GL5,
        "rank5_total": total,
        "stages": stages,
        "baseline": baseline,
        "removed": removed,
        "remaining": remaining,
        "removed_fraction": [removed_fraction.numerator, removed_fraction.denominator],
        "quadruple_additional_removed": incremental,
        "quadruple_fraction_after_old_caps": [
            incremental_fraction.numerator,
            incremental_fraction.denominator,
        ],
        "internal_free_bits": 443,
    }


def compositions(total: int, parts: int, prefix: tuple[int, ...] = ()):
    if parts == 1:
        yield prefix + (total,)
        return
    for first in range(total + 1):
        yield from compositions(total - first, parts - 1, prefix + (first,))


def four_set_audit() -> dict[str, object]:
    vertices = range(4)
    pairs = list(combinations(vertices, 2))
    triples = list(combinations(vertices, 3))
    for signature in range(8):
        x0, x1, x2 = ((signature >> bit) & 1 for bit in range(3))
        require(
            x0 * x1 + x0 * x2 + (1 - x1) * (1 - x2)
            == int(x0 == x1 == x2) + x0,
            "mixed-triple identity",
        )
    equality = [
        (distinguishers, degree)
        for distinguishers in range(18)
        for degree in range(18, 25)
        if 38 - distinguishers + degree <= 39
    ]
    require(equality == [(17, 18)], "mixed-triple equality boundary")
    distinguishing_signatures = [mask for mask in range(16) if mask.bit_count() == 2]
    require(
        all(
            all(len({(mask >> vertex) & 1 for vertex in triple}) == 2 for triple in triples)
            for mask in distinguishing_signatures
        ),
        "weight-two signature characterization",
    )
    distributions = list(compositions(16, len(distinguishing_signatures)))
    require(len(distributions) == comb(21, 5) == 20_349, "signature distribution census")
    valid_internal = 0
    feasibility_checks = 0
    for graph_mask in range(64):
        edge = {pair: (graph_mask >> index) & 1 for index, pair in enumerate(pairs)}

        def colour(x: int, y: int) -> int:
            return edge[tuple(sorted((x, y)))]

        if any(len({colour(x, y) for x, y in combinations(triple, 2)}) == 1
               for triple in triples):
            continue
        internal_degree = [sum(colour(v, w) for w in vertices if w != v) for v in vertices]
        require(all(value in (1, 2) for value in internal_degree), "internal degree class")
        forced_total = [18 if value == 2 else 24 for value in internal_degree]
        for counts in distributions:
            red_from_distinguishers = [
                sum(count for count, signature in zip(counts, distinguishing_signatures)
                    if signature >> vertex & 1)
                for vertex in vertices
            ]
            for uniform_red in range(10, 14):
                feasibility_checks += 1
                require(
                    any(
                        internal_degree[vertex]
                        + red_from_distinguishers[vertex]
                        + uniform_red
                        != forced_total[vertex]
                        for vertex in vertices
                    ),
                    "feasible forbidden four-set signature distribution",
                )
        valid_internal += 1
    require(valid_internal == 18, "nonmonochromatic K4 census")
    require(feasibility_checks == 18 * 20_349 * 4, "feasibility coverage")
    return {
        "mixed_signatures_checked": 8,
        "K4_colourings_checked": 64,
        "nonmonochromatic_K4_colourings": valid_internal,
        "four_contact_signatures_checked": 16,
        "distinguishing_weight_two_signatures": distinguishing_signatures,
        "signature_distributions_checked_per_K4": len(distributions),
        "degree_feasibility_checks": feasibility_checks,
        "global_four_set_distinguisher_minimum": 17,
        "row_class_cap_on_20_side": 3,
    }


def binary_rank(rows: list[int]) -> int:
    pivots: dict[int, int] = {}
    for row in rows:
        value = row
        while value:
            pivot = value.bit_length() - 1
            if pivot in pivots:
                value ^= pivots[pivot]
            else:
                pivots[pivot] = value
                break
    return len(pivots)


def physical_fixture_audit(target: Path) -> dict[str, object]:
    parameters = json.loads((target / "fixture_parameters.json").read_text())
    graph = json.loads((target / "fixture_graph.json").read_text())
    certificate = json.loads((target / "fixture_certificate.json").read_text())
    rows, columns = parameters["rows"], parameters["columns"]
    require(len(rows) == 20 and len(columns) == 23, "fixture factor lengths")
    require(binary_rank(rows) == binary_rank(columns) == 5, "fixture factor ranks")
    cross = [sum(((x & y).bit_count() & 1) << j for j, y in enumerate(columns)) for x in rows]
    blue_cross = [value ^ ((1 << 23) - 1) for value in cross]
    require(binary_rank(cross) == 5 and binary_rank(blue_cross) >= 5,
            "fixture baseline ranks")
    row_counts, column_counts = Counter(rows), Counter(columns)
    require(max(row_counts.values()) == 4, "fixture new row obstruction")
    require(
        not (row_counts[0] and column_counts[0])
        and row_counts[0] <= 1
        and column_counts[0] <= 2
        and max(column_counts.values()) <= 5,
        "fixture earlier predicates",
    )
    internal_hex = parameters["internal_hex"]
    require(type(internal_hex) is str and len(internal_hex) == 111, "fixture internal bits")
    internal_bits = int(internal_hex, 16)
    require(internal_bits < (1 << 443), "fixture internal overflow")
    red_bits = 0
    internal_index = 0
    pair_list = list(combinations(range(43), 2))
    for pair_index, (x, y) in enumerate(pair_list):
        if x < 20 <= y:
            value = (rows[x] & columns[y - 20]).bit_count() & 1
        else:
            value = (internal_bits >> internal_index) & 1
            internal_index += 1
        red_bits |= value << pair_index
    require(internal_index == 443, "fixture internal coordinate coverage")
    require(graph == {"n": 43, "red_hex": format(red_bits, "0226x")},
            "fixture physical reconstruction")
    vertices = certificate["vertices"]
    require(certificate["color"] in ("red", "blue"), "fixture certificate colour")
    require(vertices == sorted(set(vertices)) and len(vertices) == 5, "fixture five-set")
    position = {pair: index for index, pair in enumerate(pair_list)}
    want = int(certificate["color"] == "red")
    require(
        all(((red_bits >> position[tuple(sorted(pair))]) & 1) == want
            for pair in combinations(vertices, 2)),
        "fixture monochromatic certificate",
    )
    return {
        "cross_rank": binary_rank(cross),
        "complement_cross_rank": binary_rank(blue_cross),
        "internal_coordinates_reconstructed": internal_index,
        "cross_coordinates_reconstructed": 460,
        "first_failing_predicate": "new_row_cap_three",
        "certificate_colour": certificate["color"],
        "certificate_vertices": vertices,
        "certificate_pairs_checked": 10,
    }


def manifest_audit(target: Path) -> dict[str, object]:
    entries: dict[str, str] = {}
    for line in (target / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split("  ", 1)
        require("/" not in name and name not in entries and len(digest) == 64,
                "target manifest shape")
        entries[name] = digest
    files = {path.name for path in target.iterdir() if path.is_file()}
    require(set(entries) == files - {"SHA256SUMS"}, "target manifest coverage")
    for name, digest in entries.items():
        require(sha256((target / name).read_bytes()).hexdigest() == digest,
                "target manifest digest")
    return {
        "package_files": len(files),
        "manifest_entries": len(entries),
        "package_bytes": sum(path.stat().st_size for path in target.iterdir() if path.is_file()),
    }


def audit(target: Path) -> dict[str, object]:
    return {
        "verified": True,
        "status": "INDEPENDENT_RANK5_GLOBAL_SIEVE_ACCEPTANCE",
        "target_manifest": manifest_audit(target),
        "four_set": four_set_audit(),
        "counting": counting_audit(),
        "physical_fixture": physical_fixture_audit(target),
        "scope": {
            "fixed_partition": [20, 23],
            "red_cut_rank": 5,
            "blue_cut_rank_minimum": 5,
            "all_internal_edges_free": True,
            "whole_rank5_excluded": False,
            "good43_constructed": False,
            "ramsey_bound_improved": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "target",
        type=Path,
        nargs="?",
        default=Path(__file__).resolve().parent.parent / "ramsey_r55_rank5_global_sieve",
    )
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = audit(args.target)
    if args.check_expected:
        expected = json.loads((Path(__file__).resolve().parent / "EXPECTED.json").read_text())
        require(result == expected, "expected result disagreement")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
