#!/usr/bin/env python3
"""Independent exact audit using Macdonald's weighted descent recurrence."""

from __future__ import annotations

import argparse
import math
from fractions import Fraction
from functools import cache
from itertools import permutations


Permutation = tuple[int, ...]


def strip_fixed_suffix(w: Permutation) -> Permutation:
    while w and w[-1] == len(w) - 1:
        w = w[:-1]
    return w


def inversion_count(w: Permutation) -> int:
    return sum(a > b for i, a in enumerate(w) for b in w[i + 1 :])


@cache
def upsilon_descent(w: Permutation) -> int:
    """Macdonald recurrence: U_w = sum(i U_{w s_i}) / length(w)."""
    w = strip_fixed_suffix(w)
    length = inversion_count(w)
    if length == 0:
        return 1

    numerator = 0
    for i in range(len(w) - 1):
        if w[i] > w[i + 1]:
            child_list = list(w)
            child_list[i], child_list[i + 1] = child_list[i + 1], child_list[i]
            numerator += (i + 1) * upsilon_descent(tuple(child_list))

    quotient, remainder = divmod(numerator, length)
    assert remainder == 0
    return quotient


def inflate_identity(w: Permutation, k: int = 2) -> Permutation:
    return tuple(k * value + offset for value in w for offset in range(k))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=5)
    return parser.parse_args()


def main() -> None:
    max_n = parse_args().max_n
    if not 1 <= max_n <= 6:
        raise ValueError("the audited range is 1 <= MAX_N <= 6")

    grand_total = 0
    expected_ratio = Fraction(5, 4)
    for n in range(1, max_n + 1):
        failures = 0
        min_ratio: Fraction | None = None
        two_term_count = 0

        for w in permutations(range(n)):
            base = upsilon_descent(w)
            image = upsilon_descent(inflate_identity(w))
            target = base**4
            grand_total += 1
            failures += image < target
            if base == 2:
                two_term_count += 1
                assert image == 20
            if base > 1:
                ratio = Fraction(image, target)
                min_ratio = ratio if min_ratio is None else min(min_ratio, ratio)

        expected_two_term_count = 0 if n < 3 else math.comb(2 * n - 3, n - 3)
        assert two_term_count == expected_two_term_count
        assert failures == 0
        if min_ratio is not None:
            assert min_ratio == expected_ratio
        ratio_text = "none" if min_ratio is None else "5/4"
        print(
            f"n={n}: tested={math.factorial(n)} two_term={two_term_count} "
            f"failures=0 min_nontrivial_ratio={ratio_text}"
        )

    info = upsilon_descent.cache_info()
    print(
        f"independent Macdonald-descent audit passed for {grand_total} "
        f"permutations through S_{max_n}; cache_states={info.currsize}"
    )


if __name__ == "__main__":
    main()
