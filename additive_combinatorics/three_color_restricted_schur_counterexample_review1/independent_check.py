#!/usr/bin/env python3
"""Independent finite checks for the restricted-Schur counterexample.

This file deliberately imports none of the target contribution's Python
modules.  It implements the seven intervals directly from the theorem and
uses a distinct-value dynamic program, rather than the author's recurrence,
to enumerate every nonconstant k-term multiset sum up to the colored endpoint.
"""

from __future__ import annotations

import hashlib
import itertools
import json


COLORS = ("red", "blue", "green")


def parameters(k: int) -> tuple[int, int, int, int]:
    if k < 2:
        raise ValueError("k must be at least 2")
    ell = k * k + 2 * k
    upper = k * ell
    proposed = k**3 + 3 * k * k + k - 1
    bound = proposed + k - 1
    return ell, upper, proposed, bound


def color_of(x: int, k: int) -> str:
    ell, upper, proposed, bound = parameters(k)
    if not 1 <= x < bound:
        raise ValueError("integer lies outside the colored interval")
    if x <= k:
        return "red"
    if x <= k * k + k:
        return "blue"
    if x < ell:
        return "red"
    if x <= upper:
        return "green"
    if x < upper + k:
        return "red"
    if x < proposed:
        return "blue"
    return "red"


def member_bits(values: list[int]) -> int:
    result = 0
    for value in values:
        result |= 1 << value
    return result


def nonconstant_sum_bits(values: list[int], terms: int, limit: int) -> int:
    """Return sums <= limit using exactly terms and >=2 distinct values.

    The initial bitset contains every sum of two *different* class members.
    Repeated Minkowski addition by the whole class then gives exactly the sums
    of ``terms`` entries whose multiset is nonconstant.  This formulation also
    preserves a nonconstant representation when its sum happens to equal the
    sum of a constant representation.
    """

    mask = (1 << (limit + 1)) - 1
    values_bits = member_bits(values)
    sums = 0
    for value in values:
        higher_values = values_bits & ~((1 << (value + 1)) - 1)
        sums |= (higher_values << value) & mask
    for _ in range(2, terms):
        next_sums = 0
        for value in values:
            next_sums |= (sums << value) & mask
        sums = next_sums
    return sums


def literal_nonconstant_sum_bits(values: list[int], terms: int, limit: int) -> int:
    result = 0
    for entries in itertools.combinations_with_replacement(values, terms):
        if entries[0] != entries[-1] and sum(entries) <= limit:
            result |= 1 << sum(entries)
    return result


def self_check_sum_enumerator() -> int:
    comparisons = 0
    universe = range(1, 8)
    for size in range(1, 8):
        for subset in itertools.combinations(universe, size):
            values = list(subset)
            for terms in range(2, 5):
                limit = terms * 7
                fast = nonconstant_sum_bits(values, terms, limit)
                literal = literal_nonconstant_sum_bits(values, terms, limit)
                if fast != literal:
                    raise AssertionError((values, terms, fast, literal))
                comparisons += 1
    return comparisons


def check_coloring(k: int) -> dict[str, object]:
    _, _, proposed, bound = parameters(k)
    endpoint = bound - 1
    classes = {
        color: [x for x in range(1, endpoint + 1) if color_of(x, k) == color]
        for color in COLORS
    }
    conflicts: dict[str, list[int]] = {}
    attainable_counts: dict[str, int] = {}
    for color, values in classes.items():
        sums = nonconstant_sum_bits(values, k, endpoint)
        conflict_bits = sums & member_bits(values)
        conflicts[color] = [x for x in values if (conflict_bits >> x) & 1]
        attainable_counts[color] = sums.bit_count()
    if any(conflicts.values()):
        raise AssertionError({"k": k, "conflicts": conflicts})
    return {
        "k": k,
        "proposed_value": proposed,
        "colored_endpoint": endpoint,
        "proved_lower_bound": bound,
        "class_sizes": {color: len(values) for color, values in classes.items()},
        "nonconstant_sum_counts": attainable_counts,
    }


def check_fixed_prefix_extension(k: int, *, exhaustive: bool = True) -> int:
    ell, upper, proposed, bound = parameters(k)
    checked = 0
    if exhaustive:
        targets = range(proposed, bound + 1)
    else:
        targets = (proposed, proposed + (k - 1) // 2, bound)
    for target in targets:
        blue_tail = target - (k - 1) * (k + 1)
        green_tail = target - (k - 1) * ell
        if color_of(k + 1, k) != "blue" or color_of(blue_tail, k) != "blue":
            raise AssertionError((k, target, "blue witness"))
        if color_of(ell, k) != "green" or color_of(green_tail, k) != "green":
            raise AssertionError((k, target, "green witness"))
        if not (blue_tail != k + 1 and green_tail != ell):
            raise AssertionError((k, target, "witness distinctness"))
        if (k - 1) * (k + 1) + blue_tail != target:
            raise AssertionError((k, target, "blue equation"))
        if (k - 1) * ell + green_tail != target:
            raise AssertionError((k, target, "green equation"))
        checked += 2
    if color_of(1, k) != "red" or color_of(proposed, k) != "red":
        raise AssertionError((k, "red endpoint witness"))
    if (k - 1) + proposed != bound:
        raise AssertionError((k, "red endpoint equation"))
    return checked + 1


def main() -> None:
    enumerator_self_checks = self_check_sum_enumerator()
    finite = [check_coloring(k) for k in range(2, 13)]
    extension_witnesses = sum(check_fixed_prefix_extension(k) for k in range(2, 201))
    large_parameters = [10**6, 10**30 + 57, 10**100 + 267]
    large_witnesses = sum(
        check_fixed_prefix_extension(k, exhaustive=False) for k in large_parameters
    )
    payload: dict[str, object] = {
        "status": "PASS",
        "method": "independent nonconstant-sum bitset DP; no target-code imports",
        "enumerator_self_checks": enumerator_self_checks,
        "finite_cases": finite,
        "extension_k_range": [2, 200],
        "extension_witnesses_checked": extension_witnesses,
        "large_parameters": [str(k) for k in large_parameters],
        "large_witnesses_checked": large_witnesses,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["record_sha256"] = hashlib.sha256(canonical).hexdigest()
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
