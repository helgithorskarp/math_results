#!/usr/bin/env python3
"""Exact verifier for integer-aware induced crossing-number sampling."""

from fractions import Fraction as Q
from math import comb


TARGET = 6084
CASES = ((54, 726), (53, 713), (53, 714), (53, 715))


def ceil_q(x: Q) -> int:
    return -((-x.numerator) // x.denominator)


def raw_bound(n: int, m: int, s: int) -> Q:
    """Continuous sampled form of cr(H) >= 5e-203(v-2)/9."""
    assert 4 <= s <= n
    return (
        Q(5 * m * (n - 2) * (n - 3), (s - 2) * (s - 3))
        - Q(
            203 * n * (n - 1) * (n - 2) * (n - 3),
            9 * s * (s - 1) * (s - 3),
        )
    )


def integral_bound(n: int, m: int, s: int) -> Q:
    """Lemma in README.md, before taking the final ceiling."""
    assert 4 <= s <= n
    local_constant = ceil_q(Q(-203 * (s - 2), 9))
    return (
        Q(5 * m * (n - 2) * (n - 3), (s - 2) * (s - 3))
        + Q(
            local_constant * n * (n - 1) * (n - 2) * (n - 3),
            s * (s - 1) * (s - 2) * (s - 3),
        )
    )


def integral_bound_by_counts(n: int, m: int, s: int) -> Q:
    """Same bound in its unevaluated double-counting form."""
    local_constant = ceil_q(Q(-203 * (s - 2), 9))
    numerator = 5 * m * comb(n - 2, s - 2) + local_constant * comb(n, s)
    return Q(numerator, comb(n - 4, s - 4))


def best(function, n: int, m: int) -> tuple[Q, int]:
    bound, negative_s = max((function(n, m, s), -s) for s in range(4, n + 1))
    return bound, -negative_s


def main() -> None:
    # Check the algebraic simplification for more than the four applications.
    for n in range(4, 65):
        for s in range(4, n + 1):
            for m in (0, n, n * (n - 1) // 2):
                assert integral_bound(n, m, s) == integral_bound_by_counts(
                    n, m, s
                )

    expected = {
        (54, 726): (Q(10759164, 1771), 24, 6076),
        (53, 713): (Q(31923025, 5313), 24, 6009),
        (53, 714): (Q(32069650, 5313), 24, 6037),
        (53, 715): (Q(1952535, 322), 23, 6064),
    }
    continuous_integer_conclusions = {
        (54, 726): 6069,
        (53, 713): 6003,
        (53, 714): 6030,
        (53, 715): 6058,
    }

    results = {}
    for case in CASES:
        n, m = case
        new_bound, s = best(integral_bound, n, m)
        old_bound, old_s = best(raw_bound, n, m)
        assert (new_bound, s, ceil_q(new_bound)) == expected[case]
        assert ceil_q(old_bound) == continuous_integer_conclusions[case]
        assert new_bound > old_bound
        results[case] = (new_bound, s, old_bound, old_s)

    new_54, s_54, old_54, old_s_54 = results[(54, 726)]
    assert old_54 == Q(977041, 161) and old_s_54 == 24
    assert new_54 - old_54 == Q(11713, 1771)
    assert TARGET - new_54 == Q(15600, 1771)
    assert TARGET - ceil_q(new_54) == 8

    # The refinement changes the bound, not the edge closure threshold.
    for function in (raw_bound, integral_bound):
        threshold = next(
            m
            for m in range(726, 740)
            if ceil_q(best(function, 54, m)[0]) >= TARGET
        )
        assert threshold == 727

    print("PASS integer-aware induced sampling")
    for (n, m), (bound, s, old_bound, old_s) in results.items():
        print(
            f"n={n}, m={m}: new s={s}, bound={bound}, ceil={ceil_q(bound)}; "
            f"continuous s={old_s}, bound={old_bound}, ceil={ceil_q(old_bound)}"
        )
    print("n=54,m=726: remaining integer deficit to Z(27)=6084 is 8")


if __name__ == "__main__":
    main()
