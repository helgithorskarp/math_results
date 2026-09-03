#!/usr/bin/env python3
"""Avoidance-pruned verification of Dahlberg's length-four involution cases.

The program uses a unique-parent generating tree for involutions and four
specialized exact pattern detectors.  It proves only the finite range that it
finishes and reports; it does not extrapolate to arbitrary n.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from collections import Counter
from collections.abc import Callable, Iterator

Permutation = tuple[int, ...]
DescentSet = tuple[int, ...]

PATTERNS = ("1432", "2134", "1243", "3214")


def interval_mask(low: int, high: int) -> int:
    """Bit mask of the integer values v satisfying low < v < high."""
    if high <= low + 1:
        return 0
    return ((1 << (high - 1)) - 1) & ~((1 << low) - 1)


def prefix_masks(perm: Permutation) -> list[int]:
    """At index j, return the mask of values strictly before position j."""
    result = [0] * len(perm)
    mask = 0
    for j, value in enumerate(perm):
        result[j] = mask
        mask |= 1 << (value - 1)
    return result


def suffix_masks(perm: Permutation) -> list[int]:
    """At index k, return the mask of values strictly after position k."""
    result = [0] * len(perm)
    mask = 0
    for k in range(len(perm) - 1, -1, -1):
        result[k] = mask
        mask |= 1 << (perm[k] - 1)
    return result


def suffix_maxima(perm: Permutation) -> list[int]:
    """At index k, return the maximum value strictly after position k."""
    result = [0] * len(perm)
    maximum = 0
    for k in range(len(perm) - 1, -1, -1):
        result[k] = maximum
        maximum = max(maximum, perm[k])
    return result


def contains_1432(perm: Permutation) -> bool:
    # i<j<k<l and perm[i] < perm[l] < perm[k] < perm[j].
    pre = prefix_masks(perm)
    post = suffix_masks(perm)
    for j in range(1, len(perm) - 2):
        for k in range(j + 1, len(perm) - 1):
            if perm[k] < perm[j]:
                lower = min(perm[:j])
                if post[k] & interval_mask(lower, perm[k]):
                    return True
    return False


def contains_2134(perm: Permutation) -> bool:
    # i<j<k<l and perm[j] < perm[i] < perm[k] < perm[l].
    pre = prefix_masks(perm)
    post_max = suffix_maxima(perm)
    for j in range(1, len(perm) - 2):
        for k in range(j + 1, len(perm) - 1):
            if post_max[k] > perm[k] and pre[j] & interval_mask(perm[j], perm[k]):
                return True
    return False


def contains_1243(perm: Permutation) -> bool:
    # i<j<k<l and perm[i] < perm[j] < perm[l] < perm[k].
    post = suffix_masks(perm)
    for j in range(1, len(perm) - 2):
        if min(perm[:j]) >= perm[j]:
            continue
        for k in range(j + 1, len(perm) - 1):
            if post[k] & interval_mask(perm[j], perm[k]):
                return True
    return False


def contains_3214(perm: Permutation) -> bool:
    # i<j<k<l and perm[k] < perm[j] < perm[i] < perm[l].
    pre = prefix_masks(perm)
    post_max = suffix_maxima(perm)
    for j in range(1, len(perm) - 2):
        for k in range(j + 1, len(perm) - 1):
            if perm[k] < perm[j] and pre[j] & interval_mask(perm[j], post_max[k]):
                return True
    return False


CONTAINS: dict[str, Callable[[Permutation], bool]] = {
    "1432": contains_1432,
    "2134": contains_2134,
    "1243": contains_1243,
    "3214": contains_3214,
}


def standardize(values: tuple[int, ...]) -> tuple[int, ...]:
    rank = {value: j + 1 for j, value in enumerate(sorted(values))}
    return tuple(rank[value] for value in values)


def definition_contains(perm: Permutation, pattern: str) -> bool:
    target = tuple(map(int, pattern))
    return any(
        standardize(tuple(perm[i] for i in indices)) == target
        for indices in itertools.combinations(range(len(perm)), 4)
    )


def self_test_detectors() -> None:
    """Exhaustively compare optimized detectors to the definition through S_7."""
    for n in range(8):
        for perm in itertools.permutations(range(1, n + 1)):
            for pattern in PATTERNS:
                expected = definition_contains(perm, pattern)
                actual = CONTAINS[pattern](perm)
                if actual != expected:
                    raise AssertionError(("detector mismatch", perm, pattern, actual, expected))


def insert_pair(parent: Permutation, i: int) -> Permutation:
    """Insert the 2-cycle (i,n) into an involution on [n-2]."""
    n = len(parent) + 2

    def relabel(value: int) -> int:
        return value + (value >= i)

    child = []
    for position in range(1, n):
        if position == i:
            child.append(n)
        else:
            old_position = position - (position > i)
            child.append(relabel(parent[old_position - 1]))
    child.append(i)
    return tuple(child)


def next_avoiders(
    n: int,
    previous: tuple[Permutation, ...],
    two_back: tuple[Permutation, ...],
    contains: Callable[[Permutation], bool],
) -> tuple[Permutation, ...]:
    """Generate every avoiding involution of size n from its unique parent."""
    children: list[Permutation] = []
    for parent in previous:
        child = parent + (n,)
        if not contains(child):
            children.append(child)
    for parent in two_back:
        for i in range(1, n):
            child = insert_pair(parent, i)
            if not contains(child):
                children.append(child)
    if len(children) != len(set(children)):
        raise AssertionError(("non-unique child", n))
    return tuple(children)


def descent_set(perm: Permutation) -> DescentSet:
    return tuple(i for i in range(1, len(perm)) if perm[i - 1] > perm[i])


def descent_counter(perms: tuple[Permutation, ...]) -> Counter[DescentSet]:
    return Counter(map(descent_set, perms))


def counter_digest(counter: Counter[DescentSet]) -> str:
    canonical = [[list(descent_set_), counter[descent_set_]] for descent_set_ in sorted(counter)]
    data = json.dumps(canonical, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(data).hexdigest()


def complement_counter(counter: Counter[DescentSet], n: int) -> Counter[DescentSet]:
    universe = frozenset(range(1, n))
    return Counter({tuple(sorted(universe - set(descent_set_))): count
                    for descent_set_, count in counter.items()})


def motzkin_numbers(max_n: int) -> list[int]:
    values = [1]
    for n in range(1, max_n + 1):
        total = values[n - 1]
        total += sum(values[j] * values[n - 2 - j] for j in range(n - 1))
        values.append(total)
    return values


def verify(max_n: int) -> None:
    if max_n < 0:
        raise ValueError("--max-n must be nonnegative")
    self_test_detectors()
    motzkin = motzkin_numbers(max_n)

    # Only the two irredundant classes are generated.  The other pair follows
    # rigorously by reverse-complement, as explained in README.md.
    levels: dict[str, list[tuple[Permutation, ...]]] = {
        "1432": [((),)],
        "2134": [((),)],
    }
    print("optimized detectors agree with definition on every permutation through S_7")
    for n in range(max_n + 1):
        for pattern in ("1432", "2134"):
            if n:
                previous = levels[pattern][n - 1]
                two_back = levels[pattern][n - 2] if n >= 2 else ()
                levels[pattern].append(
                    next_avoiders(n, previous, two_back, CONTAINS[pattern])
                )
            if len(levels[pattern][n]) != motzkin[n]:
                raise AssertionError(("Motzkin check failed", pattern, n,
                                      len(levels[pattern][n]), motzkin[n]))

        left = descent_counter(levels["1432"][n])
        right = descent_counter(levels["2134"][n])
        if left != complement_counter(right, n):
            raise AssertionError(("descent-complement failure", n))
        print(
            f"n={n:2d} count={len(levels['1432'][n]):8d} "
            f"descent_sets={len(left):6d} "
            f"sha256_1432={counter_digest(left)} "
            f"sha256_2134={counter_digest(right)}"
        )

        # The unique-parent recurrence only needs the preceding two levels.
        if n >= 2:
            for pattern in ("1432", "2134"):
                levels[pattern][n - 2] = ()

    print(
        f"verified descent-set complementation for 1432/2134 through n={max_n}; "
        "reverse-complement proves the same finite range for 1243/3214"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=15)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    try:
        verify(arguments.max_n)
    except (AssertionError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
