#!/usr/bin/env python3
"""Independent audit using Macdonald's weighted descent recurrence."""

from __future__ import annotations

import argparse
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
    """Macdonald recurrence: ell(w) U_w = sum_i i U_{w s_i}."""
    w = strip_fixed_suffix(w)
    length = inversion_count(w)
    if length == 0:
        return 1

    numerator = 0
    for i in range(len(w) - 1):
        if w[i] > w[i + 1]:
            child = list(w)
            child[i], child[i + 1] = child[i + 1], child[i]
            numerator += (i + 1) * upsilon_descent(tuple(child))

    quotient, remainder = divmod(numerator, length)
    assert remainder == 0
    return quotient


def inflate_identity(w: Permutation, k: int = 2) -> Permutation:
    return tuple(k * value + offset for value in w for offset in range(k))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=5)
    max_n = parser.parse_args().max_n
    if not 1 <= max_n <= 6:
        raise ValueError("the audited range is 1 <= MAX_N <= 6")

    grand_total = 0
    for n in range(1, max_n + 1):
        count = 0
        for w in permutations(range(n)):
            if upsilon_descent(w) != 3:
                continue
            count += 1
            grand_total += 1
            assert upsilon_descent(inflate_identity(w)) == 105
        print(f"descent n={n}: three_term={count} image=105 failures=0")

    info = upsilon_descent.cache_info()
    print(
        "independent Macdonald-descent audit passed for "
        f"{grand_total} three-term permutations through S_{max_n}; "
        f"cache_states={info.currsize}"
    )


if __name__ == "__main__":
    main()
