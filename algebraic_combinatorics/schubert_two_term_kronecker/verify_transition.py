#!/usr/bin/env python3
"""Exact transition-recurrence checks for Schubert identity inflation."""

from __future__ import annotations

import argparse
import math
from collections import Counter
from fractions import Fraction
from functools import cache
from itertools import permutations


Permutation = tuple[int, ...]


def strip_fixed_suffix(w: Permutation) -> Permutation:
    """Remove trailing fixed points, which do not change the specialization."""
    while w and w[-1] == len(w) - 1:
        w = w[:-1]
    return w


def inversion_count(w: Permutation) -> int:
    return sum(a > b for i, a in enumerate(w) for b in w[i + 1 :])


@cache
def upsilon(w: Permutation) -> int:
    """Evaluate Upsilon_w by the exact transition recurrence."""
    w = strip_fixed_suffix(w)
    if len(w) < 2:
        return 1

    descents = [i for i in range(len(w) - 1) if w[i] > w[i + 1]]
    if not descents:
        return 1
    r = descents[-1]
    s = max(j for j in range(r + 1, len(w)) if w[j] < w[r])

    v_list = list(w)
    v_list[r], v_list[s] = v_list[s], v_list[r]
    v = tuple(v_list)
    length_v = inversion_count(v)

    total = upsilon(v)
    for q in range(r):
        child_list = list(v)
        child_list[q], child_list[r] = child_list[r], child_list[q]
        child = tuple(child_list)
        if inversion_count(child) == length_v + 1:
            total += upsilon(child)
    return total


def inflate_identity(w: Permutation, k: int) -> Permutation:
    return tuple(k * value + offset for value in w for offset in range(k))


def boxed_plane_partitions(k: int) -> int:
    """MacMahon product for a k by k by k box, evaluated exactly."""
    value = Fraction(1)
    for i in range(1, k + 1):
        for j in range(1, k + 1):
            value *= Fraction(k + i + j - 1, i + j - 1)
    assert value.denominator == 1
    return value.numerator


def census(k: int, max_n: int) -> None:
    rectangle = boxed_plane_partitions(k)
    expected_two_term_ratio = Fraction(rectangle, 2 ** (k * k))
    grand_total = 0

    for n in range(1, max_n + 1):
        failures: list[tuple[Permutation, int, int]] = []
        nontrivial_min: tuple[Fraction, Permutation, int, int] | None = None
        base_histogram: Counter[int] = Counter()
        two_term_images: set[int] = set()

        for w in permutations(range(n)):
            base = upsilon(w)
            image = upsilon(inflate_identity(w, k))
            target = base ** (k * k)
            grand_total += 1
            base_histogram[base] += 1

            if image < target:
                failures.append((w, image, target))
            if base == 2:
                two_term_images.add(image)
            if base > 1:
                candidate = (Fraction(image, target), w, image, target)
                if nontrivial_min is None or candidate[0] < nontrivial_min[0]:
                    nontrivial_min = candidate

        expected_two_term_count = 0 if n < 3 else math.comb(2 * n - 3, n - 3)
        assert base_histogram[2] == expected_two_term_count
        assert two_term_images == (set() if n < 3 else {rectangle})
        assert not failures
        if nontrivial_min is not None:
            assert nontrivial_min[0] == expected_two_term_ratio

        ratio_text = "none"
        witness_text = "none"
        if nontrivial_min is not None:
            ratio, witness, image, target = nontrivial_min
            ratio_text = f"{ratio.numerator}/{ratio.denominator}"
            witness_text = "".join(str(x + 1) for x in witness)
            assert image * ratio.denominator == target * ratio.numerator

        print(
            f"k={k} n={n}: tested={math.factorial(n)} "
            f"two_term={base_histogram[2]} failures=0 "
            f"min_nontrivial_ratio={ratio_text} witness={witness_text}"
        )

    info = upsilon.cache_info()
    print(
        f"k={k}: verified {grand_total} permutations through S_{max_n}; "
        f"cache_states={info.currsize}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--regime",
        action="append",
        metavar="K:MAX_N",
        help="inflation factor and largest symmetric group; may be repeated",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    regimes = [(2, 7), (3, 5), (4, 4)]
    if args.regime:
        regimes = []
        for item in args.regime:
            k_text, n_text = item.split(":", 1)
            k, max_n = int(k_text), int(n_text)
            if k < 1 or max_n < 1:
                raise ValueError("K and MAX_N must be positive")
            regimes.append((k, max_n))

    for k, max_n in regimes:
        census(k, max_n)
    print("all requested exact transition censuses passed")


if __name__ == "__main__":
    main()
