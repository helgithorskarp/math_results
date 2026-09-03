#!/usr/bin/env python3
"""Exact verification for the general BGTW fixed-distance formula."""

from __future__ import annotations

import functools
import hashlib
import itertools
import math
from fractions import Fraction


Permutation = tuple[int, ...]


@functools.cache
def binom(n: int, k: int) -> int:
    return math.comb(n, k) if 0 <= k <= n else 0


@functools.cache
def catalan(n: int) -> int:
    return math.comb(2 * n, n) // (n + 1)


def avoids_123_literal(permutation: Permutation) -> bool:
    n = len(permutation)
    return not any(
        permutation[i] < permutation[j] < permutation[k]
        for i in range(n)
        for j in range(i + 1, n)
        for k in range(j + 1, n)
    )


def avoids_123(permutation: Permutation) -> bool:
    n = len(permutation)
    suffix_max = [-1] * n
    maximum = -1
    for index in range(n - 1, -1, -1):
        suffix_max[index] = maximum
        maximum = max(maximum, permutation[index])
    prefix_min = n
    for index, value in enumerate(permutation):
        if prefix_min < value < suffix_max[index]:
            return False
        prefix_min = min(prefix_min, value)
    return True


@functools.cache
def avoiders(n: int) -> tuple[Permutation, ...]:
    """Generate Av_n(123) by inserting the maximum after a decreasing prefix."""
    if n == 0:
        return ((),)
    maximum = n - 1
    answer: list[Permutation] = []
    for parent in avoiders(n - 1):
        for position in range(n):
            if all(parent[i] > parent[i + 1] for i in range(position - 1)):
                answer.append(parent[:position] + (maximum,) + parent[position:])
    assert len(answer) == len(set(answer)) == catalan(n)
    return tuple(answer)


def fixed_points(permutation: Permutation) -> tuple[int, ...]:
    return tuple(i for i, value in enumerate(permutation) if i == value)


def direct_set(n: int, d: int) -> set[Permutation]:
    return {
        permutation
        for permutation in avoiders(n)
        if len(fixed_points(permutation)) == 2
        and fixed_points(permutation)[1] - fixed_points(permutation)[0] == d
    }


def hook_ok(permutation: Permutation, x: int, y: int) -> bool:
    n = len(permutation)
    if x + y > n:
        return False
    split = n - y
    low_positions = [permutation.index(value) for value in range(x)]
    return (
        all(position < split for position in low_positions)
        and low_positions == sorted(low_positions, reverse=True)
        and all(value >= x for value in permutation[split:])
        and all(
            permutation[index] > permutation[index + 1]
            for index in range(split, n - 1)
        )
    )


@functools.cache
def hook_patterns(j: int, x: int, y: int) -> tuple[Permutation, ...]:
    n = j + x + y
    return tuple(
        permutation
        for permutation in itertools.permutations(range(n))
        if hook_ok(permutation, x, y) and avoids_123_literal(permutation)
    )


@functools.cache
def hook_formula(j: int, x: int, y: int) -> int:
    s = x + y
    return (s + 1) * math.comb(2 * j + s, j) // (j + s + 1)


def psi_word(permutation: Permutation) -> str:
    """Krattenthaler's right-to-left-maximum Dyck word, with U/D steps."""
    maximum = -1
    maxima: list[tuple[int, int]] = []
    for index in range(len(permutation) - 1, -1, -1):
        if permutation[index] > maximum:
            maxima.append((index, permutation[index] + 1))
            maximum = permutation[index]
    word: list[str] = []
    previous_value = 0
    for number, (index, value) in enumerate(maxima):
        word.extend("U" * (value - previous_value))
        next_index = maxima[number + 1][0] if number + 1 < len(maxima) else -1
        word.extend("D" * (index - next_index))
        previous_value = value
    return "".join(word)


def is_dyck(word: str) -> bool:
    height = 0
    for step in word:
        height += 1 if step == "U" else -1
        if height < 0:
            return False
    return height == 0


def dyck_hook_condition(word: str, x: int, y: int) -> bool:
    """Path translation of H(j,x,y), valid for y >= 1."""
    assert y >= 1
    runs: list[tuple[str, int]] = []
    for step, group in itertools.groupby(word):
        runs.append((step, sum(1 for _ in group)))
    up_runs = runs[0::2]
    down_runs = runs[1::2]
    return (
        len(up_runs) >= y
        and up_runs[0][1] >= x + 1
        and len(down_runs) >= y - 1
        and all(run == ("D", 1) for run in down_runs[: y - 1])
    )


def anti_diagonal(permutation: Permutation) -> Permutation:
    """Reflect the plot in the anti-diagonal."""
    n = len(permutation)
    inverse = [0] * n
    for position, value in enumerate(permutation):
        inverse[value] = position
    return tuple(n - 1 - inverse[n - 1 - index] for index in range(n))


def reverse_complement(permutation: Permutation) -> Permutation:
    n = len(permutation)
    return tuple(n - 1 - value for value in reversed(permutation))


def inflate(
    target: list[int], positions: list[int], values: list[int], pattern: Permutation
) -> None:
    assert positions == sorted(positions)
    assert values == sorted(values)
    assert len(positions) == len(values) == len(pattern)
    for pattern_index, position in enumerate(positions):
        target[position] = values[pattern[pattern_index]]


def structural_set(n: int, d: int) -> set[Permutation]:
    if n < 2 * d:
        return set()
    answer: set[Permutation] = set()
    middle_size = d - 1
    for x in range(d):
        for y in range(d):
            numerator = n - d - 1 - x - y
            if numerator < 0 or numerator % 2:
                continue
            j = numerator // 2
            k = n - 2 * d - j
            if k < 0:
                continue
            a0 = j + x
            b0 = a0 + d
            middle = tuple(range(a0 + 1, b0))
            assert len(middle) == middle_size
            for left_values in itertools.combinations(middle, x):
                left_values_set = set(left_values)
                right_values = [v for v in middle if v not in left_values_set]
                for upper_positions in itertools.combinations(middle, y):
                    upper_positions_set = set(upper_positions)
                    lower_positions = [
                        p for p in middle if p not in upper_positions_set
                    ]
                    nw_positions = list(range(a0)) + list(upper_positions)
                    nw_values = list(left_values) + list(range(b0 + 1, n))
                    se_positions = lower_positions + list(range(b0 + 1, n))
                    se_values = list(range(a0)) + right_values
                    for northwest in hook_patterns(j, x, y):
                        for southeast in hook_patterns(
                            k, d - 1 - x, d - 1 - y
                        ):
                            permutation = [-1] * n
                            permutation[a0] = a0
                            permutation[b0] = b0
                            inflate(permutation, nw_positions, nw_values, northwest)
                            inflate(
                                permutation,
                                se_positions,
                                se_values,
                                reverse_complement(southeast),
                            )
                            candidate = tuple(permutation)
                            assert sorted(candidate) == list(range(n))
                            assert avoids_123_literal(candidate)
                            answer.add(candidate)
    return answer


def full_xy_hook_count(n: int, d: int) -> int:
    answer = 0
    for x in range(d):
        for y in range(d):
            numerator = n - d - 1 - x - y
            if numerator < 0 or numerator % 2:
                continue
            j = numerator // 2
            k = n - 2 * d - j
            if k < 0:
                continue
            answer += (
                math.comb(d - 1, x)
                * math.comb(d - 1, y)
                * hook_formula(j, x, y)
                * hook_formula(k, d - 1 - x, d - 1 - y)
            )
    return answer


@functools.cache
def ballot_from_length(length: int, height: int) -> int:
    if height < 0 or length < height or (length - height) % 2:
        return 0
    down = (length - height) // 2
    return binom(length, down) - binom(length, down - 1)


def reduced_hook_count(n: int, d: int) -> int:
    length = n - d - 1
    return sum(
        math.comb(2 * d - 2, s)
        * ballot_from_length(length, s)
        * ballot_from_length(length, 2 * d - 2 - s)
        for s in range(2 * d - 1)
    )


def bgtw_count(n: int, d: int) -> Fraction:
    m, parity = divmod(n, 2)
    if not (1 <= d <= m):
        return Fraction(0)
    factor = Fraction(binom(n - d, m) ** 2, (n - d) ** 2)
    bracket = Fraction(0)
    if parity == 0:
        bracket += Fraction(binom(2 * d, d) * d**3, 4 * d - 2)
    for i in range(1, (m + 1) // 3 + 1):
        numerator = (
            2
            * binom(m, i - parity)
            * binom(m - d + parity, i)
            * binom(2 * d - 2, 2 * i - 1 + d - parity)
            * (d * d - (2 * i - parity) ** 2)
        )
        denominator = binom(m + i, m) * binom(
            m - d + i, m - d + parity
        )
        if numerator:
            assert denominator
            bracket += Fraction(numerator, denominator)
    return factor * bracket


def canonical_digest(permutations: set[Permutation]) -> str:
    payload = b"".join(bytes(p) + b"\n" for p in sorted(permutations))
    return hashlib.sha256(payload).hexdigest()


def check_detectors_and_generator() -> None:
    for n in range(9):
        literal = {
            p for p in itertools.permutations(range(n)) if avoids_123_literal(p)
        }
        assert literal == set(avoiders(n))
        assert all(avoids_123(p) for p in literal)


def check_hooks_and_paths() -> None:
    for n in range(9):
        level = avoiders(n)
        for x in range(n + 1):
            for y in range(n - x + 1):
                j = n - x - y
                hooks = {p for p in level if hook_ok(p, x, y)}
                assert hooks == set(hook_patterns(j, x, y))
                assert len(hooks) == hook_formula(j, x, y)
                reflected = {anti_diagonal(p) for p in hooks}
                assert reflected == {p for p in level if hook_ok(p, y, x)}
                if y >= 1:
                    assert hooks == {
                        p for p in level if dyck_hook_condition(psi_word(p), x, y)
                    }
        assert all(is_dyck(psi_word(p)) for p in level)
        assert len({psi_word(p) for p in level}) == catalan(n)


def check_grid_sets() -> None:
    for n in range(2, 11):
        for d in range(1, n // 2 + 1):
            direct = direct_set(n, d)
            structural = structural_set(n, d)
            assert direct == structural
            assert len(direct) == full_xy_hook_count(n, d)
            print(
                f"n={n:2d} d={d:2d} count={len(direct):6d} "
                f"sha256={canonical_digest(direct)}"
            )


def check_formulas() -> None:
    for m in range(1, 31):
        for n in (2 * m, 2 * m + 1):
            for d in range(1, m + 1):
                xy = full_xy_hook_count(n, d)
                reduced = reduced_hook_count(n, d)
                source = bgtw_count(n, d)
                assert xy == reduced == source
    for m in range(31, 201):
        for n in (2 * m, 2 * m + 1):
            for d in range(1, m + 1):
                reduced = reduced_hook_count(n, d)
                source = bgtw_count(n, d)
                assert reduced == source


def main() -> None:
    check_detectors_and_generator()
    check_hooks_and_paths()
    check_formulas()
    check_grid_sets()
    print("general_formula_check=PASS")


if __name__ == "__main__":
    main()
