#!/usr/bin/env python3
"""Exact checks for the distance-three slice of BGTW Conjecture A.2."""

from __future__ import annotations

import functools
import hashlib
import itertools
import math
from fractions import Fraction


Permutation = tuple[int, ...]


def avoids_123_literal(permutation: Permutation) -> bool:
    """Apply the definition using all triples of indices."""
    n = len(permutation)
    return not any(
        permutation[i] < permutation[j] < permutation[k]
        for i in range(n)
        for j in range(i + 1, n)
        for k in range(j + 1, n)
    )


def avoids_123(permutation: Permutation) -> bool:
    """Detect a 123 from a prefix minimum and a strict suffix maximum."""
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


def fixed_points(permutation: Permutation) -> tuple[int, ...]:
    """Return fixed points using zero-based positions and values."""
    return tuple(index for index, value in enumerate(permutation) if index == value)


def direct_set(n: int) -> set[Permutation]:
    """Definition-level exhaustive set, without the grid decomposition."""
    answer: set[Permutation] = set()
    for permutation in itertools.permutations(range(n)):
        if not avoids_123(permutation):
            continue
        points = fixed_points(permutation)
        if len(points) == 2 and points[1] - points[0] == 3:
            answer.add(permutation)
    return answer


@functools.cache
def hook_patterns(j: int, x: int, y: int) -> tuple[Permutation, ...]:
    """Enumerate H(j,x,y) literally, as standardized hook permutations."""
    n = j + x + y
    split = j + x
    answer: list[Permutation] = []
    for permutation in itertools.permutations(range(n)):
        low_positions = [permutation.index(value) for value in range(x)]
        if any(position >= split for position in low_positions):
            continue
        # Values x-1,...,0 must occur from left to right.
        if low_positions != sorted(low_positions, reverse=True):
            continue
        suffix = permutation[split:]
        if any(value < x for value in suffix):
            continue
        if any(suffix[index] <= suffix[index + 1] for index in range(y - 1)):
            continue
        if avoids_123_literal(permutation):
            answer.append(permutation)
    return tuple(answer)


def reverse_complement(permutation: Permutation) -> Permutation:
    n = len(permutation)
    return tuple(n - 1 - value for value in reversed(permutation))


def inflate(
    target: list[int], positions: list[int], values: list[int], pattern: Permutation
) -> None:
    """Inflate a standardized pattern into sorted positions and values."""
    assert positions == sorted(positions)
    assert values == sorted(values)
    assert len(positions) == len(values) == len(pattern)
    for pattern_index, position in enumerate(positions):
        target[position] = values[pattern[pattern_index]]


def structural_set(n: int) -> set[Permutation]:
    """Construct all distance-three avoiders via the two-hook decomposition."""
    d = 3
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

            # The first fixed point is a0 and the second is b0, zero based.
            a0 = j + x
            b0 = a0 + d
            middle = tuple(range(a0 + 1, b0))
            assert len(middle) == middle_size

            for left_middle_values in itertools.combinations(middle, x):
                left_middle_values_set = set(left_middle_values)
                right_middle_values = [
                    value for value in middle if value not in left_middle_values_set
                ]
                for upper_middle_positions in itertools.combinations(middle, y):
                    upper_middle_positions_set = set(upper_middle_positions)
                    lower_middle_positions = [
                        position
                        for position in middle
                        if position not in upper_middle_positions_set
                    ]

                    nw_positions = list(range(a0)) + list(upper_middle_positions)
                    nw_values = list(left_middle_values) + list(range(b0 + 1, n))
                    se_positions = lower_middle_positions + list(range(b0 + 1, n))
                    se_values = list(range(a0)) + right_middle_values

                    assert len(nw_positions) == j + x + y
                    assert len(se_positions) == k + (d - 1 - x) + (d - 1 - y)

                    for northwest in hook_patterns(j, x, y):
                        for southeast_hook in hook_patterns(
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
                                reverse_complement(southeast_hook),
                            )
                            candidate = tuple(permutation)
                            assert sorted(candidate) == list(range(n))
                            assert avoids_123_literal(candidate)
                            answer.add(candidate)

    return answer


def catalan(index: int) -> int:
    return math.comb(2 * index, index) // (index + 1)


def hook_formula(j: int, x: int, y: int) -> int:
    """The nine entries in the Catalan-hook table."""
    if (x, y) == (0, 0):
        return catalan(j)
    if (x, y) in {(1, 0), (0, 1)}:
        return catalan(j + 1)
    if (x, y) in {(2, 0), (1, 1), (0, 2)}:
        return catalan(j + 2) - catalan(j + 1)
    if (x, y) in {(2, 1), (1, 2)}:
        return catalan(j + 3) - 2 * catalan(j + 2)
    if (x, y) == (2, 2):
        return catalan(j + 4) - 3 * catalan(j + 3) + catalan(j + 2)
    raise ValueError((j, x, y))


def decomposition_count(n: int) -> int:
    """Evaluate the hook sum, independently of structural_set generation."""
    d = 3
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


def theorem_count(n: int) -> int:
    """Evaluate the displayed Catalan-product theorem."""
    m, parity = divmod(n, 2)
    if m < 3:
        return 0
    if parity == 0:
        return 6 * (catalan(m - 1) - catalan(m - 2)) ** 2 + 2 * catalan(
            m - 2
        ) * (catalan(m) - 3 * catalan(m - 1) + catalan(m - 2))
    return 8 * catalan(m - 1) * (catalan(m) - 2 * catalan(m - 1))


def simplified_count(n: int) -> Fraction:
    """Evaluate the rational forms in the theorem exactly."""
    m, parity = divmod(n, 2)
    if parity == 0:
        return Fraction(
            4 * (m - 2) * (16 * m * m - 21 * m - 27) * catalan(m - 2) ** 2,
            m * m * (m + 1),
        )
    return Fraction(16 * (m - 2) * catalan(m - 1) ** 2, m + 1)


def bgtw_d3_count(n: int) -> Fraction:
    """Specialize Conjecture A.2 literally at d=3; only i=1 survives."""
    m, parity = divmod(n, 2)
    d = 3
    factor = Fraction(math.comb(n - d, m) ** 2, (n - d) ** 2)
    bracket = Fraction(0)
    if parity == 0:
        bracket += Fraction(math.comb(2 * d, d) * d**3, 4 * d - 2)

    i = 1
    top_index = 2 * i - 1 + d - parity
    if 0 <= top_index <= 2 * d - 2 and i - parity >= 0:
        bracket += Fraction(
            2
            * math.comb(m, i - parity)
            * math.comb(m - d + parity, i)
            * math.comb(2 * d - 2, top_index)
            * (d * d - (2 * i - parity) ** 2),
            math.comb(m + i, m)
            * math.comb(m - d + i, m - d + parity),
        )
    return factor * bracket


def canonical_digest(permutations: set[Permutation]) -> str:
    """Hash sorted one-byte encodings; the checker only reaches n=10."""
    payload = b"".join(bytes(permutation) + b"\n" for permutation in sorted(permutations))
    return hashlib.sha256(payload).hexdigest()


def check_detector() -> None:
    for n in range(9):
        for permutation in itertools.permutations(range(n)):
            assert avoids_123(permutation) == avoids_123_literal(permutation)


def check_hooks() -> None:
    for j in range(7):
        for x in range(3):
            for y in range(3):
                assert len(hook_patterns(j, x, y)) == hook_formula(j, x, y)


def check_symbolic_specialization() -> None:
    for m in range(3, 201):
        for n in (2 * m, 2 * m + 1):
            expected = theorem_count(n)
            assert decomposition_count(n) == expected
            assert simplified_count(n) == expected
            assert bgtw_d3_count(n) == expected


def main() -> None:
    check_detector()
    check_hooks()
    check_symbolic_specialization()
    expected = {6: 6, 7: 16, 8: 58, 9: 160, 10: 536}
    for n, expected_count in expected.items():
        direct = direct_set(n)
        structural = structural_set(n)
        formula = theorem_count(n)
        assert direct == structural
        assert len(direct) == formula == expected_count
        assert all(avoids_123(permutation) for permutation in structural)
        assert all(
            len(fixed_points(permutation)) == 2
            and fixed_points(permutation)[1] - fixed_points(permutation)[0] == 3
            for permutation in structural
        )
        print(f"n={n:2d} count={formula:4d} sha256={canonical_digest(direct)}")


if __name__ == "__main__":
    main()
