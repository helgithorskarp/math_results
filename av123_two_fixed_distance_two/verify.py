#!/usr/bin/env python3
"""Exact checks for the distance-two slice of BGTW Conjecture A.2."""

from __future__ import annotations

import hashlib
import itertools
import math


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
    """Definition-level exhaustive set, without using the bijection."""
    answer: set[Permutation] = set()
    for permutation in itertools.permutations(range(n)):
        if not avoids_123(permutation):
            continue
        points = fixed_points(permutation)
        if len(points) == 2 and points[1] - points[0] == 2:
            answer.add(permutation)
    return answer


def avoiders(n: int) -> tuple[Permutation, ...]:
    return tuple(p for p in itertools.permutations(range(n)) if avoids_123(p))


def fill_pattern(
    target: list[int], positions: list[int], values: list[int], pattern: Permutation
) -> None:
    """Inflate a standardized pattern into sorted positions and values."""
    assert len(positions) == len(values) == len(pattern)
    assert positions == sorted(positions)
    assert values == sorted(values)
    for pattern_index, position in enumerate(positions):
        target[position] = values[pattern[pattern_index]]


def reverse_complement(permutation: Permutation) -> Permutation:
    n = len(permutation)
    return tuple(n - 1 - value for value in reversed(permutation))


def structural_set(n: int) -> set[Permutation]:
    """Generate the two cases of the proof, independently of direct_set."""
    if n < 4:
        return set()
    m, parity = divmod(n, 2)
    answer: set[Permutation] = set()

    if parity == 0:
        small_avoiders = avoiders(m - 1)
        for alpha in small_avoiders:
            for beta in small_avoiders:
                p = [-1] * n
                # Fixed points m-1 and m+1 in one-based notation.
                p[m - 2] = m - 2
                p[m] = m
                fill_pattern(
                    p,
                    list(range(m - 2)) + [m - 1],
                    list(range(m + 1, n)),
                    alpha,
                )
                fill_pattern(
                    p,
                    list(range(m + 1, n)),
                    list(range(m - 2)) + [m - 1],
                    beta,
                )
                first_case = tuple(p)
                answer.add(first_case)
                answer.add(reverse_complement(first_case))
    else:
        left_avoiders = tuple(p for p in avoiders(m) if p[-1] != 0)
        right_avoiders = avoiders(m - 1)
        for alpha in left_avoiders:
            for beta in right_avoiders:
                p = [-1] * n
                # Fixed points m and m+2 in one-based notation.
                p[m - 1] = m - 1
                p[m + 1] = m + 1
                fill_pattern(
                    p,
                    list(range(m - 1)) + [m],
                    [m] + list(range(m + 2, n)),
                    alpha,
                )
                fill_pattern(
                    p,
                    list(range(m + 2, n)),
                    list(range(m - 1)),
                    beta,
                )
                first_case = tuple(p)
                answer.add(first_case)
                answer.add(reverse_complement(first_case))

    return answer


def catalan(index: int) -> int:
    return math.comb(2 * index, index) // (index + 1)


def predicted_count(n: int) -> int:
    if n < 4:
        return 0
    m, parity = divmod(n, 2)
    if parity == 0:
        return 2 * catalan(m - 1) ** 2
    return 2 * catalan(m - 1) * (catalan(m) - catalan(m - 1))


def canonical_digest(permutations: set[Permutation]) -> str:
    """Hash sorted one-byte encodings; this checker only reaches n=10."""
    payload = b"".join(bytes(permutation) + b"\n" for permutation in sorted(permutations))
    return hashlib.sha256(payload).hexdigest()


def check_detector() -> None:
    for n in range(9):
        for permutation in itertools.permutations(range(n)):
            assert avoids_123(permutation) == avoids_123_literal(permutation)


def main() -> None:
    check_detector()
    expected = {4: 2, 5: 2, 6: 8, 7: 12, 8: 50, 9: 90, 10: 392}
    for n, expected_count in expected.items():
        direct = direct_set(n)
        structural = structural_set(n)
        formula = predicted_count(n)
        assert direct == structural
        assert len(direct) == formula == expected_count
        assert all(avoids_123(p) for p in structural)
        assert all(
            len(fixed_points(p)) == 2
            and fixed_points(p)[1] - fixed_points(p)[0] == 2
            for p in structural
        )
        print(f"n={n:2d} count={formula:4d} sha256={canonical_digest(direct)}")


if __name__ == "__main__":
    main()
