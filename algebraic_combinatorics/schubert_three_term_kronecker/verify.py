#!/usr/bin/env python3
"""Exact checks for identity inflation on the Upsilon=3 stratum."""

from __future__ import annotations

from collections import Counter
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
def upsilon(w: Permutation) -> int:
    """Principal specialization via the exact transition recurrence."""
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


def lehmer_code(w: Permutation) -> tuple[int, ...]:
    return tuple(sum(y < x for y in w[i + 1 :]) for i, x in enumerate(w))


def is_dominant(w: Permutation) -> bool:
    code = lehmer_code(w)
    return all(code[i] >= code[i + 1] for i in range(len(code) - 1))


def swap_adjacent(w: Permutation, i: int) -> Permutation:
    result = list(w)
    result[i], result[i + 1] = result[i + 1], result[i]
    return tuple(result)


def count_132(w: Permutation) -> int:
    return sum(
        w[i] < w[k] < w[j]
        for i in range(len(w))
        for j in range(i + 1, len(w))
        for k in range(j + 1, len(w))
    )


def count_1432(w: Permutation) -> int:
    return sum(
        w[i] < w[l] < w[k] < w[j]
        for i in range(len(w))
        for j in range(i + 1, len(w))
        for k in range(j + 1, len(w))
        for l in range(k + 1, len(w))
    )


def two_move_types(w: Permutation) -> set[str]:
    """Find all dominantizations having one of the three lemma forms."""
    types: set[str] = set()
    n = len(w)
    for i in range(n - 1):
        if w[i] > w[i + 1]:
            continue
        v = swap_adjacent(w, i)

        if is_dominant(v):
            d = lehmer_code(v)
            if d[i] == d[i + 1] + 3:
                types.add("h2")

        if i > 0 and v[i - 1] < v[i]:
            u = swap_adjacent(v, i - 1)
            if is_dominant(u):
                d = lehmer_code(u)
                a = d[i + 1]
                if d[i - 1] == a + 3 and d[i] in (a, a + 1):
                    types.add("h1")

        if i + 2 < n and v[i + 1] < v[i + 2]:
            u = swap_adjacent(v, i + 1)
            if is_dominant(u):
                d = lehmer_code(u)
                a = d[i + 2]
                if d[i] == a + 2 and d[i + 1] == a + 2:
                    types.add("e2")
    return types


def inflate_identity(w: Permutation, k: int) -> Permutation:
    return tuple(k * value + offset for value in w for offset in range(k))


def boxed_plane_partitions(k: int) -> int:
    value = Fraction(1)
    for i in range(1, k + 1):
        for j in range(1, k + 1):
            value *= Fraction(2 * k + i + j - 1, i + j - 1)
    assert value.denominator == 1
    return value.numerator


def classification_census(max_n: int = 8) -> None:
    expected = {1: 0, 2: 0, 3: 0, 4: 4, 5: 22, 6: 98, 7: 408, 8: 1650}
    for n in range(1, max_n + 1):
        type_counts: Counter[str] = Counter()
        count = 0
        for w in permutations(range(n)):
            base = upsilon(w)
            patterns = count_132(w)
            assert is_dominant(w) == (patterns == 0)
            avoids_1432 = count_1432(w) == 0
            if base == 3:
                count += 1
                assert patterns == 2 and avoids_1432
                types = two_move_types(w)
                assert types
                for kind in types:
                    type_counts[kind] += 1
        assert count == expected[n]
        summary = ",".join(f"{kind}:{type_counts[kind]}" for kind in sorted(type_counts))
        print(f"classification n={n}: three_term={count} types={summary or 'none'}")


def inflation_census(k: int, max_n: int) -> None:
    expected_value = boxed_plane_partitions(k)
    grand_total = 0
    for n in range(1, max_n + 1):
        count = 0
        for w in permutations(range(n)):
            if upsilon(w) != 3:
                continue
            count += 1
            grand_total += 1
            image = upsilon(inflate_identity(w, k))
            assert image == expected_value
        print(
            f"inflation k={k} n={n}: three_term={count} "
            f"image={expected_value} failures=0"
        )
    print(f"inflation k={k}: verified={grand_total} through S_{max_n}")


def main() -> None:
    classification_census()
    for k, max_n in ((2, 7), (3, 6), (4, 5)):
        inflation_census(k, max_n)
    for k in range(2, 51):
        assert boxed_plane_partitions(k) > 3 ** (k * k)
    info = upsilon.cache_info()
    print(f"all exact checks passed; transition_cache_states={info.currsize}")


if __name__ == "__main__":
    main()
