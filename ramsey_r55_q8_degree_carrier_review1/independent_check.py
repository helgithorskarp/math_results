#!/usr/bin/env python3
"""Third exact audit of the h4029 current-q8 carrier reduction.

This program imports no target module.  It enumerates literal eight-vertex
graphs in Python, uses dense bivariate dynamic programming (neither the
producer's Counter convolution nor the supplied checker's integer packing),
and regenerates the complete target EXPECTED.json object.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools as it
import json
import math
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
TARGET = REPOSITORY / "ramsey_r55_q8_degree_carrier"
SOURCE = REPOSITORY / "ramsey_r55_maximal_block_order"
EXPECTED_SHA256 = "b652d2e5fb5a30fbfd7e3236e50aa7f9c9bff22188d1bf8967cc4d2138d7416c"
TASKS_SHA256 = "657e2585f5fce56abc4bb7806bd093d1978c39ea791b9d02695ed19e22ef1f4c"
SOURCE_MANIFEST_SHA256 = "452b38de607c4bfecd9f6addbf363b47b1400c8c63eaee954d68466648f534e6"
CORE_COUNT = 546_356


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def cross_data(five: tuple[int, ...], left: int, right: int) -> tuple[int, int]:
    """Return fixed red edges and the cross-edge mask of a five-set."""
    fixed = mask = 0
    for u, v in it.combinations(five, 2):
        if v < 4:
            fixed += left
        elif u >= 4:
            fixed += right
        else:
            mask |= 1 << (4 * u + v - 4)
    return fixed, mask


def enumerate_domain(left: int, right: int, root_order: int) -> tuple[int, ...]:
    """Enumerate cross matrices by literal monochromatic-five testing."""
    five_data = [cross_data(five, left, right)
                 for five in it.combinations(range(8), 5)]
    allowed = []
    for word in range(1 << 16):
        if any((red := fixed + (word & mask).bit_count()) in (0, 10)
               for fixed, mask in five_data):
            continue
        if root_order:
            columns = [sum(((word >> (4 * row + column)) & 1) << row
                           for row in range(4)) for column in range(4)]
            if any(columns[j] < columns[j + 1] for j in range(3)):
                continue
        allowed.append(word)
    return tuple(allowed)


def matrix_histogram(words: tuple[int, ...], side: int,
                     selected: tuple[int, int]) -> list[int]:
    histogram = [0] * 25
    for word in words:
        if side == 0:
            degrees = [((word >> (4 * row)) & 15).bit_count()
                       for row in range(4)]
        else:
            degrees = [sum((word >> (4 * row + column)) & 1
                           for row in range(4)) for column in range(4)]
        histogram[5 * degrees[selected[0]] + degrees[selected[1]]] += 1
    return histogram


def star_histogram(red_block: bool, selected: tuple[int, int]) -> list[int]:
    histogram = [0] * 25
    forbidden = 15 if red_block else 0
    for word in range(16):
        if word == forbidden:
            continue
        a = (word >> selected[0]) & 1
        b = (word >> selected[1]) & 1
        histogram[5 * a + b] += 1
    return histogram


def dense_convolution(polynomials: list[list[int]]) -> tuple[list[list[int]], int]:
    """Multiply bivariate polynomials as dense rectangular coefficient arrays."""
    product = [[1]]
    total = 1
    for histogram in polynomials:
        support = [(degree // 5, degree % 5, count)
                   for degree, count in enumerate(histogram) if count]
        new = [[0] * (len(product[0]) + 4) for _ in range(len(product) + 4)]
        for i, row in enumerate(product):
            for j, old_count in enumerate(row):
                if not old_count:
                    continue
                for di, dj, count in support:
                    new[i + di][j + dj] += old_count * count
        product = new
        total *= sum(histogram)
    require(sum(map(sum, product)) == total, "dense convolution lost mass")
    return product, total


def block_marginal(histograms: dict[tuple[tuple[int, int, int], int,
                                          tuple[int, int]], list[int]],
                   r: int, block: int, selected: tuple[int, int]) -> dict:
    colors = [int(i < r) for i in range(8)]
    polynomials = []
    for other in range(8):
        if other == block:
            continue
        first, second = sorted((block, other))
        key = colors[first], colors[second], int(first == 0)
        polynomials.append(histograms[key, int(block == second), selected])
    star = star_histogram(bool(colors[block]), selected)
    polynomials.extend([star] * 11)
    product, total = dense_convolution(polynomials)
    offset = 3 if colors[block] else 0
    accepted = sum(product[i][j]
                   for i in range(len(product))
                   for j in range(len(product[i]))
                   if 18 <= offset + i <= 24 and 18 <= offset + j <= 24)
    return {"selected": list(selected), "accepted": accepted, "total": total}


def core_marginal(r: int) -> dict:
    product = [1]
    for block in range(8):
        forbidden = 15 if block < r else 0
        histogram = [0] * 5
        for word in range(16):
            if word != forbidden:
                histogram[word.bit_count()] += 1
        new = [0] * (len(product) + 4)
        for degree, count in enumerate(product):
            for increment, ways in enumerate(histogram):
                new[degree + increment] += count * ways
        product = new
    require(sum(product) == 15 ** 8, "core convolution lost mass")
    counts = [sum(count for external, count in enumerate(product)
                  if 18 <= internal + external <= 24)
              for internal in range(11)]
    return {"accepted_by_fixed_degree": counts,
            "maximum": max(counts), "total": 15 ** 8}


def ceil_sqrt_fraction(value: Fraction, scale: int) -> Fraction:
    scaled_numerator = value.numerator * scale * scale
    root = math.isqrt(scaled_numerator // value.denominator)
    if root * root * value.denominator < scaled_numerator:
        root += 1
    answer = Fraction(root, scale)
    require((answer - Fraction(1, scale)) ** 2 < value <= answer ** 2,
            "not the least upward grid square root")
    return answer


def parent_carrier(domain_sizes: dict[tuple[int, int, int], int], r: int) -> int:
    a, b = r - 1, 8 - r
    return (domain_sizes[(1, 1, 1)] ** a
            * domain_sizes[(1, 0, 1)] ** b
            * domain_sizes[(1, 1, 0)] ** math.comb(a, 2)
            * domain_sizes[(0, 0, 0)] ** math.comb(b, 2)
            * domain_sizes[(1, 0, 0)] ** (a * b)
            * 15 ** 88)


def ordered_transfer(classes: list[dict],
                     domain_sizes: dict[tuple[int, int, int], int]) -> dict:
    rows = []
    carrier = 0
    retained = Fraction(0)
    red_roots = domain_sizes[(1, 1, 1)]
    blue_roots = domain_sizes[(1, 0, 1)]
    for parent in classes:
        r = parent["r"]
        a, b = r - 1, 8 - r
        sequences = red_roots ** a * blue_roots ** b
        multisets = (math.comb(red_roots + a - 1, a)
                     * math.comb(blue_roots + b - 1, b))
        distinct = math.comb(red_roots, a) * math.comb(blue_roots, b)
        orders = math.factorial(a) * math.factorial(b)
        rest, remainder = divmod(parent["per_task_carrier"], sequences)
        require(remainder == 0, "parent carrier does not split at root words")
        pairs = [row["best"]["selected"] for row in parent["blocks"]]
        require(all(pairs[i] == pairs[1] for i in range(1, r)),
                "red child event is not block-permutation invariant")
        if b:
            require(all(pairs[i] == pairs[r] for i in range(r, 8)),
                    "blue child event is not block-permutation invariant")
        upper = Fraction(**parent["probability_upper"])
        current_bound = (upper * Fraction(sequences, orders * multisets)
                         + Fraction(multisets - distinct, multisets))
        sorted_size = multisets * rest
        rows.append({
            "r": r,
            "root_sequences": sequences,
            "root_multisets": multisets,
            "distinct_root_multisets": distinct,
            "label_orders": orders,
            "remaining_coordinate_count": rest,
            "sorted_per_task_carrier": sorted_size,
            "sorted_fraction_bound": fraction(current_bound),
            "current_task_factor16": 16 * current_bound <= 1,
        })
        carrier += CORE_COUNT * sorted_size
        retained += CORE_COUNT * sorted_size * current_bound
    return {
        "source": "h3887",
        "classes": rows,
        "sorted_q8_carrier": carrier,
        "sorted_retained_upper": fraction(retained),
        "declared_gate_factor16": 16 * retained <= carrier,
    }


def regenerate() -> tuple[dict, dict[str, int]]:
    keys = ((0, 0, 0), (0, 1, 0), (1, 0, 0),
            (1, 0, 1), (1, 1, 0), (1, 1, 1))
    domains = {key: enumerate_domain(*key) for key in keys}
    sizes = {key: len(words) for key, words in domains.items()}
    histograms = {
        (key, side, pair): matrix_histogram(words, side, pair)
        for key, words in domains.items()
        for side in (0, 1)
        for pair in it.combinations(range(4), 2)
    }
    classes = []
    for r in range(5, 9):
        block_rows = []
        probability_squared = Fraction(1)
        for block in range(8):
            choices = [block_marginal(histograms, r, block, pair)
                       for pair in it.combinations(range(4), 2)]
            best = min(choices,
                       key=lambda row: Fraction(row["accepted"], row["total"]))
            probability_squared *= Fraction(best["accepted"], best["total"])
            block_rows.append({"block": block, "choices": choices, "best": best})
        core = core_marginal(r)
        probability_squared *= Fraction(core["maximum"], core["total"]) ** 11
        upper = ceil_sqrt_fraction(probability_squared, 1 << 40)
        classes.append({
            "r": r,
            "blocks": block_rows,
            "core": core,
            "probability_squared_upper": fraction(probability_squared),
            "probability_upper": fraction(upper),
            "per_task_carrier": parent_carrier(sizes, r),
            "each_task_factor16": 256 * probability_squared <= 1,
        })
    carrier = CORE_COUNT * sum(row["per_task_carrier"] for row in classes)
    retained = sum(CORE_COUNT * row["per_task_carrier"]
                   * Fraction(**row["probability_upper"]) for row in classes)
    result = {
        "q": 8,
        "core_count": CORE_COUNT,
        "tasks": 4 * CORE_COUNT,
        "classes": classes,
        "carrier": carrier,
        "retained_upper_rational": fraction(retained),
        "parent_source": "h3873",
        "parent_factor16": 16 * retained <= carrier,
        "ordered_transfer": ordered_transfer(classes, sizes),
        "new_q10_decisions": 0,
        "new_q7r5_decisions": 0,
    }
    return result, {"".join(map(str, key)): size for key, size in sizes.items()}


def audit_source_registry(regenerated: dict) -> dict:
    tasks_path = SOURCE / "TASKS.json"
    require(sha256(tasks_path) == TASKS_SHA256, "h3887 task registry hash")
    require(sha256(SOURCE / "SHA256SUMS") == SOURCE_MANIFEST_SHA256,
            "h3887 source-manifest hash")
    source = json.loads(tasks_path.read_text())
    q8 = [row for row in source["classes"] if row["q"] == 8]
    require([row["r"] for row in q8] == [5, 6, 7, 8], "h3887 q8 classes")
    pins = json.loads((TARGET / "CARRIER_PINS.json").read_text())
    require(pins["source_registry_sha256"] == TASKS_SHA256 and
            pins["source_manifest_sha256"] == SOURCE_MANIFEST_SHA256,
            "target source hashes")
    require(pins["q8_classes"] == q8, "target q8 pins differ from h3887")
    ordered = regenerated["ordered_transfer"]["classes"]
    require([row["sorted_per_task_carrier"] for row in ordered]
            == [row["per_task"] for row in q8], "regenerated task sizes differ")
    require(all(row["core_start"] == 0 and row["core_stop"] == CORE_COUNT
                for row in q8), "q8 core range")
    require(all(q8[i]["code_stop"] == q8[i + 1]["code_start"]
                for i in range(3)), "q8 registry intervals are not contiguous")
    q8_size = q8[-1]["code_stop"] - q8[0]["code_start"]
    require(q8_size == regenerated["ordered_transfer"]["sorted_q8_carrier"],
            "q8 code interval size")
    return {"macro_classes": len(q8), "tasks": sum(row["core_stop"] for row in q8),
            "physical_variables": sorted({row["physical_variables"] for row in q8})}


def audit_summary(regenerated: dict) -> dict:
    ordered = regenerated["ordered_transfer"]
    retained = Fraction(**ordered["sorted_retained_upper"])
    carrier = ordered["sorted_q8_carrier"]
    ratio = retained / carrier
    integer_upper = (retained.numerator + retained.denominator - 1) // retained.denominator
    summary = json.loads((TARGET / "SUMMARY.json").read_text())
    require(int(summary["exact_q8_carrier"]) == carrier, "summary carrier")
    require(int(summary["retained_integer_upper"]) == integer_upper,
            "summary retained ceiling")
    require(ratio < Fraction(681, 12_500), "aggregate 5.448 percent gate")
    require(ratio < Fraction(1, 18), "aggregate factor-eighteen gate")
    require(integer_upper < 2 ** 748, "retained bit bound")
    class_bounds = [Fraction(**row["sorted_fraction_bound"])
                    for row in ordered["classes"]]
    require(all(value < Fraction(1, 16) for value in class_bounds),
            "strict per-task factor-sixteen gate")
    return {
        "retained_fraction": fraction(ratio),
        "retained_integer_upper": integer_upper,
        "class_fraction_bounds": [fraction(value) for value in class_bounds],
        "strict_below_681_over_12500": True,
        "strict_reduction_more_than_18": True,
        "strict_each_class_below_1_over_16": True,
        "retained_below_2_to_748": True,
    }


def tie_control() -> dict:
    # Two blocks, two root keys, and one free cross bit.  Sorting allows ties.
    parent = [(a, b, edge) for a in range(2) for b in range(2) for edge in range(2)]
    sorted_rows = [row for row in parent if row[0] >= row[1]]
    repeated = [row for row in sorted_rows if row[0] == row[1]]
    distinct_parent = [row for row in parent if row[0] != row[1]]
    distinct_sorted = [row for row in sorted_rows if row[0] != row[1]]
    require((len(parent), len(sorted_rows), len(repeated)) == (8, 6, 4),
            "tie microcase counts")
    require(len(distinct_parent) == 2 * len(distinct_sorted),
            "distinct-key orbit transfer")
    require(len(sorted_rows) > Fraction(len(parent), 2),
            "microcase does not refute naive factorial division")
    require(len(sorted_rows) <= Fraction(len(parent), 2) + len(repeated),
            "safe repeated-key charge failed")
    return {"parent": 8, "sorted": 6, "repeated_sorted": 4,
            "naive_factorial_division_refuted": True}


def controls(expected: dict, regenerated: dict) -> list[str]:
    rejected = []
    mutations = {
        "marginal_count": lambda data: data["classes"][0]["blocks"][0]
        ["choices"][0].__setitem__("accepted", 0),
        "unsafe_rounding": lambda data: data["classes"][0]
        ["probability_upper"].__setitem__("numerator", 0),
        "missing_macro_class": lambda data: data["classes"].pop(),
        "false_sorted_bound": lambda data: data["ordered_transfer"]["classes"][0]
        ["sorted_fraction_bound"].__setitem__("numerator", 0),
    }
    for name, mutate in mutations.items():
        altered = copy.deepcopy(expected)
        mutate(altered)
        try:
            require(altered == regenerated, "certificate differs from regeneration")
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("accepted corruption: " + name)
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    parser.add_argument("--controls", action="store_true")
    args = parser.parse_args()
    expected_path = TARGET / "EXPECTED.json"
    require(sha256(expected_path) == EXPECTED_SHA256, "target EXPECTED hash")
    expected = json.loads(expected_path.read_text())
    regenerated, domain_sizes = regenerate()
    require(regenerated == expected, "full exact target certificate mismatch")
    canonical = (json.dumps(regenerated, indent=2, sort_keys=True) + "\n").encode()
    require(canonical == expected_path.read_bytes(),
            "regenerated target certificate bytes differ")
    registry = audit_source_registry(regenerated)
    bounds = audit_summary(regenerated)
    receipt = {
        "status": "INDEPENDENT_H4029_ACCEPT",
        "target_expected_sha256": EXPECTED_SHA256,
        "h3887_tasks_sha256": TASKS_SHA256,
        "literal_matrix_words_tested": 6 * 65_536,
        "domain_sizes": domain_sizes,
        "bivariate_marginals_regenerated": 4 * 8 * 6,
        "events_per_parent_task": 19,
        "independent_coordinates_per_parent_task": 116,
        "reads_per_coordinate": 2,
        "registry": registry,
        "bounds": bounds,
        "tie_control": tie_control(),
        "new_task_decisions": 0,
        "target_found": False,
    }
    if args.controls or args.check_expected:
        receipt["rejected_controls"] = controls(expected, regenerated)
    if args.check_expected:
        pinned = json.loads((HERE / "EXPECTED.json").read_text())
        require(receipt == pinned, "review receipt differs")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
