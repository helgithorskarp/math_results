#!/usr/bin/env python3
"""Independent arithmetic checks for the h4165 four-concurrence theorem.

This checker imports no h4165 code.  It reuses reviewer-1's independent h4151
curve reconstruction, rebuilds the F4 cover buckets, and computes actual
projected resultants with Sylvester determinants and Vandermonde elimination.
It checks every submitted primary survivor, the complete secondary survivor
chain, and deterministic primary-exclusion samples from every realized normal.
"""

import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
INVENTORY_SOURCE = (
    HERE.parent
    / "hadwiger_nelson_radix_four_active_closure_review1"
    / "independent_check.py"
)
SPEC = importlib.util.spec_from_file_location("reviewer_h4151_inventory", INVENTORY_SOURCE)
R = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(R)

EXPECTED_CERTIFICATE_BYTES_SHA256 = (
    "9c2d6c362a4b8d206ac1aa8f141d9b093285f453c390ae7a75adba72d34ce3c6"
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
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def is_prime(value):
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1 if divisor == 2 else 2
    return True


def trim(poly):
    poly = list(poly)
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def poly_remainder(left, right, prime):
    left = trim(entry % prime for entry in left)
    right = trim(entry % prime for entry in right)
    require(right, "polynomial division by zero")
    inverse = pow(right[-1], -1, prime)
    while len(left) >= len(right):
        scale = left[-1] * inverse % prime
        shift = len(left) - len(right)
        for index, coefficient in enumerate(right):
            left[index + shift] = (
                left[index + shift] - scale * coefficient
            ) % prime
        left = trim(left)
    return left


def gcd_degree(left, right, prime):
    left, right = trim(left), trim(right)
    while right:
        left, right = right, poly_remainder(left, right, prime)
    return len(left) - 1


def determinant(matrix, prime):
    """Direct Gaussian determinant over F_p."""
    matrix = [[entry % prime for entry in row] for row in matrix]
    answer = 1
    size = len(matrix)
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if matrix[row][column]), None
        )
        if pivot is None:
            return 0
        if pivot != column:
            matrix[pivot], matrix[column] = matrix[column], matrix[pivot]
            answer = -answer
        pivot_value = matrix[column][column]
        answer = answer * pivot_value % prime
        inverse = pow(pivot_value, -1, prime)
        for row in range(column + 1, size):
            if not matrix[row][column]:
                continue
            scale = matrix[row][column] * inverse % prime
            for entry in range(column, size):
                matrix[row][entry] = (
                    matrix[row][entry] - scale * matrix[column][entry]
                ) % prime
    return answer % prime


def sylvester_resultant(left, right, prime):
    """Definition-level determinant of the Sylvester matrix."""
    left, right = trim(left), trim(right)
    require(left and right, "zero input polynomial")
    m, n = len(left) - 1, len(right) - 1
    if m == 0:
        return pow(left[0], n, prime)
    if n == 0:
        return pow(right[0], m, prime)
    high_left, high_right = left[::-1], right[::-1]
    matrix = []
    for shift in range(n):
        matrix.append([0] * shift + high_left + [0] * (n - 1 - shift))
    for shift in range(m):
        matrix.append([0] * shift + high_right + [0] * (m - 1 - shift))
    return determinant(matrix, prime)


def substituted_y_polynomial(curve, t_value, slope, prime):
    """Evaluate x=t-slope*y by multiplying linear powers explicitly."""
    maximum = max(i + j for i, j, _ in curve)
    answer = [0] * (maximum + 1)
    for x_power, y_power, coefficient in curve:
        linear_power = [1]
        for _ in range(x_power):
            following = [0] * (len(linear_power) + 1)
            for exponent, value in enumerate(linear_power):
                following[exponent] += value * t_value
                following[exponent + 1] -= value * slope
            linear_power = following
        for exponent, value in enumerate(linear_power):
            answer[y_power + exponent] += coefficient * value
    return trim(entry % prime for entry in answer)


def vandermonde_interpolate(values, prime):
    """Solve the full Vandermonde system, independently of Newton differences."""
    size = len(values)
    matrix = [
        [pow(point, power, prime) for power in range(size)] + [values[point] % prime]
        for point in range(size)
    ]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if matrix[row][column]), None
        )
        require(pivot is not None, "singular Vandermonde matrix")
        matrix[pivot], matrix[column] = matrix[column], matrix[pivot]
        inverse = pow(matrix[column][column], -1, prime)
        matrix[column] = [entry * inverse % prime for entry in matrix[column]]
        for row in range(size):
            if row == column or matrix[row][column] == 0:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                (left - scale * right) % prime
                for left, right in zip(matrix[row], matrix[column])
            ]
    return trim(matrix[row][-1] for row in range(size))


def projected_resultant(curves, pair, slope, prime, cache, counters):
    key = slope, tuple(pair)
    if key in cache:
        return cache[key]
    degrees = [max(i + j for i, j, _ in curves[curve]) for curve in pair]
    require(all(degree % 2 == 0 for degree in degrees), "odd event degree")
    k, ell = degrees[0] // 2, degrees[1] // 2
    bound = 2 * k * ell
    values = []
    for t_value in range(bound + 1):
        left = substituted_y_polynomial(curves[pair[0]], t_value, slope, prime)
        right = substituted_y_polynomial(curves[pair[1]], t_value, slope, prime)
        require(len(left) - 1 == 2 * k, "left eliminated-variable degree drop")
        require(len(right) - 1 == 2 * ell, "right eliminated-variable degree drop")
        values.append(sylvester_resultant(left, right, prime))
    result = vandermonde_interpolate(values, prime)
    require(len(result) - 1 == bound, "projected resultant degree below bound")
    inverse = pow(result[-1], -1, prime)
    result = tuple(coefficient * inverse % prime for coefficient in result)
    cache[key] = result
    counters["pair_resultants"] += 1
    counters["sylvester_determinants"] += len(values)
    return result


def quartet_pairs(quartet, ownership):
    entries = [ownership[curve] for curve in quartet]
    normals = {normal for normal, _ in entries}
    require(len(normals) == 1, "quartet mixes signature normals")
    by_constant = {constant: curve for curve, (_, constant) in zip(quartet, entries)}
    require(set(by_constant) == {0, 1, 2, 3}, "quartet lacks four sections")
    return (by_constant[0], by_constant[1]), (by_constant[2], by_constant[3])


def check_quartets(curves, quartets, ownership, slope, prime, cache, counters):
    histogram = Counter()
    survivors = []
    for quartet in quartets:
        left_pair, right_pair = quartet_pairs(quartet, ownership)
        left = projected_resultant(curves, left_pair, slope, prime, cache, counters)
        right = projected_resultant(curves, right_pair, slope, prime, cache, counters)
        degree = gcd_degree(left, right, prime)
        histogram[degree] += 1
        if degree:
            survivors.append(list(quartet))
    return dict(sorted(histogram.items())), survivors


def mixed_radix_quartet(index, sections):
    choices = [None] * 4
    for position in range(3, -1, -1):
        index, offset = divmod(index, len(sections[position]))
        choices[position] = sections[position][offset]
    require(index == 0, "quartet index overflow")
    return tuple(sorted(choices))


def primary_samples(patterns, buckets, survivor_set):
    samples = []
    per_normal = Counter()
    for pattern in patterns:
        normal = pattern[0][0]
        sections = [sorted(buckets[(normal, constant)]) for constant in range(4)]
        count = 1
        for section in sections:
            count *= len(section)
        require(count > 0, "empty realized section")
        seed = int(hashlib.sha256(repr(normal).encode()).hexdigest(), 16) % count
        indices = [0, count // 2, count - 1, seed]
        for index in indices:
            for _ in range(count):
                quartet = mixed_radix_quartet(index, sections)
                if quartet not in survivor_set:
                    break
                index = (index + 1) % count
            require(quartet not in survivor_set, "normal has only primary survivors")
            if quartet not in samples:
                samples.append(quartet)
                per_normal[normal] += 1
    require(len(per_normal) == 81, "sample does not cover all normals")
    return sorted(samples), Counter(per_normal.values())


def main(certificate_path):
    raw = certificate_path.read_bytes()
    require(
        hashlib.sha256(raw).hexdigest() == EXPECTED_CERTIFICATE_BYTES_SHA256,
        "submitted certificate byte hash",
    )
    certificate = json.loads(raw)
    require(certificate.get("schema") == "hn-complex-radix-four-concurrence-v1", "schema")
    result = certificate["result"]
    prime = result["prime"]
    require(prime == 1_000_003 and prime > 32 and is_prime(prime), "invalid proof prime")
    require(result["projection_slopes"] == [2, 3, 4], "projection slopes")
    require(result["all_eligible_quartets_excluded"] and not result["final_survivors"], "final exclusion flag")

    rows, curves, circle, monomial_rows, row_to_curve = R.reconstruct_inventory()
    require(digest(curves) == EXPECTED_INVENTORY_SHA256, "curve inventory digest")
    words3, words4, bad3, buckets, masks, patterns = R.build_colour_data(row_to_curve)
    require(digest(patterns) == EXPECTED_PATTERN_SHA256, "four-section pattern digest")
    owner_counts = R.direct_label_pair_audit(
        monomial_rows, row_to_curve, circle, words3, words4, bad3, masks
    )

    ownership = {}
    for (normal, constant), members in buckets.items():
        for curve in members:
            require(curve not in ownership, "curve assigned two F4 signatures")
            ownership[curve] = normal, constant
    eligible_count = 0
    pair_count = 0
    pair_degree_histogram = Counter()
    pair_inventory = []
    for pattern in patterns:
        normal = pattern[0][0]
        sections = {constant: sorted(buckets[(normal, constant)]) for constant in range(4)}
        eligible_count += (
            len(sections[0]) * len(sections[1]) * len(sections[2]) * len(sections[3])
        )
        for left_constants in ((0, 1), (2, 3)):
            side = 0 if left_constants == (0, 1) else 1
            for left in sections[left_constants[0]]:
                for right in sections[left_constants[1]]:
                    pair_count += 1
                    pair_inventory.append((normal, side, (left, right)))
                    k = max(i + j for i, j, _ in curves[left]) // 2
                    ell = max(i + j for i, j, _ in curves[right]) // 2
                    pair_degree_histogram[2 * k * ell] += 1
    require(len(ownership) == len(curves) - 1, "off-circle ownership incomplete")
    require(eligible_count == result["eligible_no_circle_quartets"] == 960_768, "quartet census")
    require(pair_count == result["primary"]["distinct_pair_resultants"] == 14_256, "pair census")
    require(pair_degree_histogram == {8: 72, 18: 1008, 32: 13176}, "pair degree census")
    bucket_serialization = [
        [list(normal), constant, sorted(members)]
        for (normal, constant), members in sorted(buckets.items())
    ]
    require(digest(bucket_serialization) == result["curve_bucket_sha256"], "curve bucket digest")
    require(digest(pair_inventory) == result["primary"]["pair_inventory_sha256"], "pair inventory digest")

    primary = [tuple(quartet) for quartet in result["primary"]["survivors"]]
    require(len(primary) == 70 and len(set(primary)) == 70, "primary survivor shape")
    require(digest([list(item) for item in primary]) == result["primary"]["survivor_sha256"], "primary digest")
    primary_set = set(primary)
    samples, sample_multiplicity = primary_samples(patterns, buckets, primary_set)

    cache = {}
    counters = Counter()
    primary_histogram, confirmed_primary = check_quartets(
        curves, primary, ownership, 2, prime, cache, counters
    )
    require(primary_histogram == {1: 70}, "submitted primary survivor is false")
    require(confirmed_primary == [list(item) for item in primary], "primary survivor order")

    sample_histogram, sample_survivors = check_quartets(
        curves, samples, ownership, 2, prime, cache, counters
    )
    require(sample_histogram == {0: len(samples)} and not sample_survivors, "primary exclusion sample")

    slope3_histogram, slope3_survivors = check_quartets(
        curves, primary, ownership, 3, prime, cache, counters
    )
    require(slope3_histogram == {0: 68, 2: 2}, "slope-3 histogram")
    require(slope3_survivors == result["secondary"][0]["survivors"], "slope-3 survivors")

    slope4_input = [tuple(item) for item in slope3_survivors]
    slope4_histogram, slope4_survivors = check_quartets(
        curves, slope4_input, ownership, 4, prime, cache, counters
    )
    require(slope4_histogram == {0: 2} and not slope4_survivors, "slope-4 exclusion")

    output = {
        "schema": "hn-complex-radix-four-concurrence-independent-review-v1",
        "difference_classes": len(rows),
        "active_curves": len(curves),
        "noncircle_curves": len(curves) - 1,
        "circle_id": circle,
        "label_pairs_audited": sum(owner_counts.values()),
        "realized_affine_hyperplanes": len(buckets),
        "projective_normals": len({normal for normal, _ in buckets}),
        "complete_four_section_normals": len(patterns),
        "eligible_quartets": eligible_count,
        "primary_pair_resultants": pair_count,
        "curve_bucket_sha256": digest(bucket_serialization),
        "pair_inventory_sha256": digest(pair_inventory),
        "primary_pair_degree_histogram": {
            str(key): value for key, value in sorted(pair_degree_histogram.items())
        },
        "submitted_primary_survivors_checked": len(primary),
        "primary_survivor_gcd_histogram": {
            str(key): value for key, value in primary_histogram.items()
        },
        "primary_exclusion_samples_checked": len(samples),
        "primary_exclusion_sample_normal_multiplicity_histogram": {
            str(key): value for key, value in sorted(sample_multiplicity.items())
        },
        "primary_exclusion_sample_sha256": digest([list(item) for item in samples]),
        "primary_exclusion_sample_gcd_histogram": {
            str(key): value for key, value in sample_histogram.items()
        },
        "slope3_gcd_histogram": {
            str(key): value for key, value in slope3_histogram.items()
        },
        "slope3_survivors": slope3_survivors,
        "slope4_gcd_histogram": {
            str(key): value for key, value in slope4_histogram.items()
        },
        "slope4_survivors": slope4_survivors,
        "actual_pair_resultants_by_direct_sylvester": counters["pair_resultants"],
        "actual_sylvester_determinants": counters["sylvester_determinants"],
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "curve_inventory_sha256": digest(curves),
        "four_section_pattern_sha256": digest(patterns),
        "all_checked_projected_resultants_attain_sharp_degree": True,
        "all_checked_quartets_consistent_with_certificate": True,
        "record_improvement": False,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, required=True)
    arguments = parser.parse_args()
    main(arguments.certificate)
