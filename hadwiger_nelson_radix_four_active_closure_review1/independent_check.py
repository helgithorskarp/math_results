#!/usr/bin/env python3
"""Independent certificate checker for the h4151 four-active closure.

The submitted forbidden-incidence export is treated only as a witness.  This
checker imports no target or ancestor module.  It reconstructs the complete
curve inventory from 7^5-1 displacement rows in a real/imaginary polynomial
basis, audits all 29,403 label pairs, enumerates the affine-hyperplane quartet
gate, verifies every supplied planar-K4 certificate, and checks that those
certificates cover every quartet not handled by an F3-linear colouring.
"""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, permutations, product
import hashlib
import json
from math import gcd
from pathlib import Path


ZERO = (0, 0)
ONE = (1, 0)
OMEGA = (0, 1)
DIGITS = (ZERO, ONE, OMEGA)
UNITS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
DISPLACEMENTS = (ZERO,) + UNITS
LABELS = tuple(product(range(3), repeat=5))

EXPECTED_INTERFACE_BYTES_SHA256 = (
    "d93f5b84600e42695b0fb53fb009ccff75002a17e31af2a2af5bc0d0834ea665"
)
EXPECTED_INTERFACE_CANONICAL_SHA256 = (
    "be8b496cffe2896c597107da3c2699a96cbe4f1e37dcdeddf408782a0dc2c24d"
)
EXPECTED_OBSTRUCTION_LIST_SHA256 = (
    "d7c61f5149b6ad0be81498649d6b0255b4294910364137547c68d635ffcbbef3"
)
EXPECTED_INVENTORY_SHA256 = (
    "85c286422c01bcb6ebb244186032bc607984471bc2b705ef7247084dd7c33db9"
)
EXPECTED_PATTERN_SHA256 = (
    "fe0863b674143b718e1c3bc907cdfe1daee0f31b6e64350a7c62f6e26a60e7a6"
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def e_mul(left, right):
    """Multiply a+b*omega with omega^2=omega-1."""
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c + b * d


def canonical_row(row):
    return min(tuple(e_mul(unit, value) for value in row) for unit in UNITS)


def p_add(left, right, scale=1):
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + scale * coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def p_mul(left, right):
    result = defaultdict(int)
    for (i, j), a in left.items():
        for (k, l), b in right.items():
            result[i + k, j + l] += a * b
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def p_shift(poly, dx, dy, scale=1):
    return {(i + dx, j + dy): scale * coefficient for (i, j), coefficient in poly.items()}


def primitive(poly):
    require(poly, "zero event polynomial")
    divisor = 0
    for coefficient in poly.values():
        divisor = gcd(divisor, abs(coefficient))
    require(divisor > 0, "zero polynomial content")
    if poly[max(poly)] < 0:
        divisor = -divisor
    return tuple((i, j, coefficient // divisor) for (i, j), coefficient in sorted(poly.items()))


def radix_powers_real_imag():
    """Return z^j=R_j+i*sqrt(3)*I_j for z=x+i*sqrt(3)y."""
    powers = [({(0, 0): 1}, {})]
    for _ in range(4):
        real, imag = powers[-1]
        next_real = p_add(p_shift(real, 1, 0), p_shift(imag, 0, 1, -3))
        next_imag = p_add(p_shift(imag, 1, 0), p_shift(real, 0, 1))
        powers.append((next_real, next_imag))
    return tuple(powers)


def distance_event(row, powers):
    """Expand |2*sum row[j] z^j|^2-4 in exact integer polynomials."""
    real = {}
    imag = {}
    for (a, b), (power_real, power_imag) in zip(row, powers):
        # 2(a+b*omega)=(2a+b)+i*sqrt(3)b.
        real = p_add(real, power_real, 2 * a + b)
        real = p_add(real, power_imag, -3 * b)
        imag = p_add(imag, power_real, b)
        imag = p_add(imag, power_imag, 2 * a + b)
    norm_minus_four = p_add(p_mul(real, real), p_mul(imag, imag), 3)
    norm_minus_four = p_add(norm_minus_four, {(0, 0): 4}, -1)
    return primitive(norm_minus_four)


def reconstruct_inventory():
    rows = sorted(
        {
            canonical_row(row)
            for row in product(DISPLACEMENTS, repeat=5)
            if any(value != ZERO for value in row)
        }
    )
    require(len(rows) == 2801, "unit-normalized displacement-class census")

    powers = radix_powers_real_imag()
    circle = primitive({(2, 0): 1, (0, 2): 3, (0, 0): -1})
    event_for_row = {}
    monomial_rows = {}
    event_rows = {}
    for row in rows:
        support = tuple(index for index, value in enumerate(row) if value != ZERO)
        if len(support) == 1:
            monomial_rows[row] = support[0]
            continue
        event = distance_event(row, powers)
        require(event != circle, "nonmonomial row collapsed to the circle")
        require(event not in event_rows, "two normalized rows define one noncircle event")
        event_rows[event] = row
        event_for_row[row] = event

    require(Counter(monomial_rows.values()) == Counter(range(5)), "five monomial classes")
    require(len(event_rows) == 2796, "noncircle event census")
    factors = sorted(tuple(event_rows) + (circle,))
    require(len(factors) == 2797 and factors.index(circle) == 342, "curve-ID inventory")
    require(digest(factors) == EXPECTED_INVENTORY_SHA256, "curve-inventory digest")
    ids = {event: index for index, event in enumerate(factors)}
    row_to_curve = {row: ids[event] for row, event in event_for_row.items()}
    return rows, factors, factors.index(circle), monomial_rows, row_to_curve


def gf4_mul(left, right):
    a0, a1 = left & 1, left >> 1
    b0, b1 = right & 1, right >> 1
    return (a0 * b0 ^ a1 * b1) | (
        (a0 * b1 ^ a1 * b0 ^ a1 * b1) << 1
    )


def gf4_dot(left, right):
    value = 0
    for a, b in zip(left, right):
        value ^= gf4_mul(a, b)
    return value


def mod2_value(value):
    a, b = value
    return (a & 1) | ((b & 1) << 1)


def signature(row):
    values = tuple(mod2_value(value) for value in row)
    pivot = next(value for value in values[1:] if value)
    inverse = next(value for value in range(1, 4) if gf4_mul(value, pivot) == 1)
    return tuple(gf4_mul(inverse, value) for value in values[1:]), gf4_mul(
        inverse, values[0]
    )


def mod3_value(value):
    return (value[0] - value[1]) % 3


def build_colour_data(row_to_curve):
    words3 = tuple((1,) + tail for tail in product(range(3), repeat=4))
    words4 = tuple((1,) + tail for tail in product(range(4), repeat=4))
    bad3 = {}
    buckets = defaultdict(list)
    hyperplane_masks = {}
    for row, curve in row_to_curve.items():
        residues3 = tuple(mod3_value(value) for value in row)
        bad3[curve] = sum(
            1 << index
            for index, word in enumerate(words3)
            if sum(a * b for a, b in zip(residues3, word)) % 3 == 0
        )
        sig = signature(row)
        buckets[sig].append(curve)
        normal, constant = sig
        hyperplane_masks[sig] = sum(
            1 << index
            for index, word in enumerate(words4)
            if gf4_dot(normal, word[1:]) == constant
        )
    require(all(mask.bit_count() == 64 for mask in hyperplane_masks.values()), "F4 hyperplane sizes")
    require(len(buckets) == 336, "realized affine-hyperplane census")
    require(len({normal for normal, _ in buckets}) == 85, "projective-normal census")
    for left, right in combinations(hyperplane_masks, 2):
        intersection = (hyperplane_masks[left] & hyperplane_masks[right]).bit_count()
        require(
            intersection == (0 if left[0] == right[0] else 16),
            "two-hyperplane intersection size",
        )
    patterns = [
        tuple((normal, constant) for constant in range(4))
        for normal in sorted({normal for normal, _ in buckets})
        if all((normal, constant) in buckets for constant in range(4))
    ]
    require(len(patterns) == 81, "eligible hyperplane partitions")
    require(digest(patterns) == EXPECTED_PATTERN_SHA256, "eligible-pattern digest")
    return words3, words4, bad3, buckets, hyperplane_masks, patterns


def gram_determinant():
    matrix = [
        [Fraction(1) if i == j else Fraction(1, 2) for j in range(3)]
        for i in range(3)
    ]
    value = Fraction(0)
    for permutation in permutations(range(3)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(3)
            for j in range(i + 1, 3)
        )
        term = Fraction(-1 if inversions % 2 else 1)
        for i, j in enumerate(permutation):
            term *= matrix[i][j]
        value += term
    require(value == Fraction(1, 2), "planar K4 Gram determinant")
    return value


def difference_row(left, right):
    return tuple(
        (DIGITS[a][0] - DIGITS[b][0], DIGITS[a][1] - DIGITS[b][1])
        for a, b in zip(left, right)
    )


def edge_owner(left_index, right_index, monomial_rows, row_to_curve, circle):
    row = canonical_row(difference_row(LABELS[left_index], LABELS[right_index]))
    if row in monomial_rows:
        exponent = monomial_rows[row]
        return "base" if exponent == 0 else circle
    return row_to_curve[row]


def direct_label_pair_audit(
    monomial_rows, row_to_curve, circle, words3, words4, bad3, hyperplane_masks
):
    owner_counts = Counter()
    for left_index, right_index in combinations(range(len(LABELS)), 2):
        raw = difference_row(LABELS[left_index], LABELS[right_index])
        row = canonical_row(raw)
        owner = "base" if monomial_rows.get(row) == 0 else (
            circle if row in monomial_rows else row_to_curve[row]
        )
        owner_counts[owner] += 1

        if owner == circle:
            continue
        residues3 = tuple(mod3_value(value) for value in raw)
        direct3 = sum(
            1 << index
            for index, word in enumerate(words3)
            if sum(a * b for a, b in zip(residues3, word)) % 3 == 0
        )
        if owner == "base":
            require(direct3 == 0, "F3 word fails a universal edge")
        else:
            require(direct3 == bad3[owner], "F3 curve mask disagrees on an actual edge")

        residues4 = tuple(mod2_value(value) for value in raw)
        direct4 = sum(
            1 << index
            for index, word in enumerate(words4)
            if gf4_dot(residues4, word) == 0
        )
        if owner == "base":
            require(direct4 == 0, "F4 word fails a universal edge")
        else:
            require(
                direct4 == hyperplane_masks[signature(row)],
                "F4 hyperplane mask disagrees on an actual edge",
            )

    require(sum(owner_counts.values()) == 29403, "unordered label-pair coverage")
    require(owner_counts["base"] == 243, "off-circle universal-edge count")
    require(owner_counts[circle] == 972, "circle-only monomial-edge count")
    require(
        sum(count for owner, count in owner_counts.items() if owner not in {"base", circle})
        == 28188,
        "noncircle-event edge count",
    )
    return owner_counts


def load_and_check_obstructions(path, monomial_rows, row_to_curve, circle):
    raw = Path(path).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_INTERFACE_BYTES_SHA256, "interface byte digest")
    data = json.loads(raw)
    require(data.get("schema") == "hn-radix-four-active-forbidden-incidences-v1", "interface schema")
    require(data.get("circle_id") == circle, "interface circle ID")
    require(data.get("curve_inventory_sha256") == EXPECTED_INVENTORY_SHA256, "interface inventory digest")
    require(digest(data) == EXPECTED_INTERFACE_CANONICAL_SHA256, "canonical interface digest")

    declared = data.get("forbidden_curve_sets_with_K4_labels")
    require(isinstance(declared, list) and len(declared) == 3006, "obstruction census")
    require(digest(declared) == EXPECTED_OBSTRUCTION_LIST_SHA256, "obstruction-list digest")
    lookup = {}
    arities = Counter()
    for item in declared:
        require(isinstance(item, list) and len(item) == 2, "obstruction record shape")
        curves_raw, labels_raw = item
        curves = tuple(curves_raw)
        labels = tuple(labels_raw)
        require(curves == tuple(sorted(set(curves))), "canonical obstruction curve set")
        require(len(curves) in (3, 4), "obstruction arity")
        require(all(type(value) is int and value in row_to_curve.values() for value in curves), "obstruction curve domain")
        require(len(labels) == 4 and len(set(labels)) == 4, "four distinct clique labels")
        require(all(type(value) is int and 0 <= value < 243 for value in labels), "clique label domain")

        used = set()
        for left, right in combinations(labels, 2):
            owner = edge_owner(left, right, monomial_rows, row_to_curve, circle)
            require(owner != circle, "claimed K4 uses a circle-only edge")
            if owner != "base":
                require(owner in curves, "claimed K4 uses an undeclared event")
                used.add(owner)
        require(used == set(curves), "obstruction includes an unused curve")
        require(curves not in lookup, "duplicate obstruction")
        lookup[curves] = labels
        arities[len(curves)] += 1
    require(arities == {3: 2376, 4: 630}, "obstruction-arity census")
    return lookup, arities


def enumerate_gate(bad3, buckets, patterns, obstruction_lookup):
    full = (1 << 81) - 1
    classification = Counter()
    support_counts = defaultdict(Counter)
    word_histogram = Counter()
    obstruction_assignments = Counter()
    used_obstructions = set()
    transcript = hashlib.sha256()

    for pattern in patterns:
        support = sum(value != 0 for value in pattern[0][0])
        for quartet in product(*(buckets[sig] for sig in pattern)):
            available = full
            for curve in quartet:
                available &= ~bad3[curve]
            if available:
                word = (available & -available).bit_length() - 1
                classification["linear_three_colourings"] += 1
                support_counts[support]["linear_three_colourings"] += 1
                word_histogram[word] += 1
                record = [list(quartet), "F3", word]
            else:
                certificate = None
                for triple in combinations(quartet, 3):
                    key = tuple(sorted(triple))
                    if key in obstruction_lookup:
                        certificate = key
                        break
                quartet_key = tuple(sorted(quartet))
                if certificate is None and quartet_key in obstruction_lookup:
                    certificate = quartet_key
                require(certificate is not None, "uncoloured eligible quartet lacks a certified K4")
                used_obstructions.add(certificate)
                classification["impossible_planar_K4"] += 1
                support_counts[support]["impossible_planar_K4"] += 1
                obstruction_assignments[len(certificate)] += 1
                record = [list(quartet), "K4", list(obstruction_lookup[certificate])]
            transcript.update(json.dumps(record, separators=(",", ":")).encode() + b"\n")

    require(sum(classification.values()) == 960768, "complete eligible-quartet census")
    require(classification == {"linear_three_colourings": 934632, "impossible_planar_K4": 26136}, "quartet classification")
    require(obstruction_assignments == {3: 26136}, "triple-only K4 coverage")
    expected_support = {
        2: {"linear_three_colourings": 1656, "impossible_planar_K4": 648},
        3: {"linear_three_colourings": 67680, "impossible_planar_K4": 6048},
        4: {"linear_three_colourings": 865296, "impossible_planar_K4": 19440},
    }
    require({key: dict(value) for key, value in support_counts.items()} == expected_support, "support-stratified classification")
    return (
        classification,
        support_counts,
        word_histogram,
        obstruction_assignments,
        used_obstructions,
        transcript.hexdigest(),
    )


def main(interface_path):
    determinant = gram_determinant()
    rows, factors, circle, monomial_rows, row_to_curve = reconstruct_inventory()
    words3, words4, bad3, buckets, hyperplane_masks, patterns = build_colour_data(row_to_curve)
    owner_counts = direct_label_pair_audit(
        monomial_rows, row_to_curve, circle, words3, words4, bad3, hyperplane_masks
    )
    obstruction_lookup, obstruction_arities = load_and_check_obstructions(
        interface_path, monomial_rows, row_to_curve, circle
    )
    (
        classification,
        support_counts,
        word_histogram,
        assignments,
        used_obstructions,
        transcript,
    ) = enumerate_gate(bad3, buckets, patterns, obstruction_lookup)

    expected_pattern_counts = {2: 2304, 3: 73728, 4: 884736}
    actual_pattern_counts = Counter()
    for pattern in patterns:
        support = sum(value != 0 for value in pattern[0][0])
        count = 1
        for sig in pattern:
            count *= len(buckets[sig])
        actual_pattern_counts[support] += count
    require(dict(actual_pattern_counts) == expected_pattern_counts, "closed-form quartet counts")

    result = {
        "schema": "hn-radix-four-active-independent-review-v1",
        "label_vertices": len(LABELS),
        "label_pairs": sum(owner_counts.values()),
        "difference_classes": len(rows),
        "noncircle_curves": len(row_to_curve),
        "active_curves_including_circle": len(factors),
        "circle_id": circle,
        "off_circle_universal_edges": owner_counts["base"],
        "circle_only_monomial_edges": owner_counts[circle],
        "noncircle_event_edges": sum(
            count for owner, count in owner_counts.items() if owner not in {"base", circle}
        ),
        "realized_hyperplanes": len(buckets),
        "projective_normals": len({normal for normal, _ in buckets}),
        "eligible_patterns": len(patterns),
        "eligible_quartets_by_support": {str(key): value for key, value in sorted(actual_pattern_counts.items())},
        "eligible_quartets": sum(classification.values()),
        **dict(classification),
        "classification_by_support": {str(key): dict(value) for key, value in sorted(support_counts.items())},
        "F3_first_word_histogram": {str(key): value for key, value in sorted(word_histogram.items())},
        "certified_forbidden_sets": len(obstruction_lookup),
        "forbidden_set_arities": {str(key): value for key, value in sorted(obstruction_arities.items())},
        "K4_coverage_arities": {str(key): value for key, value in sorted(assignments.items())},
        "distinct_triple_obstructions_used_by_greedy_coverage": len(used_obstructions),
        "four_curve_obstructions_needed_for_coverage": 0,
        "review_transcript_sha256": transcript,
        "curve_inventory_sha256": digest(factors),
        "eligible_patterns_sha256": digest(patterns),
        "obstruction_list_sha256": digest(
            [[list(curves), list(labels)] for curves, labels in obstruction_lookup.items()]
        ),
        "all_pair_colour_masks_checked_directly": True,
        "all_obstruction_K4_edges_checked_directly": True,
        "K4_gram_determinant": str(determinant),
        "unresolved_eligible_quartets": 0,
        "record_improvement": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--interface", type=Path, required=True)
    args = parser.parse_args()
    main(args.interface)
