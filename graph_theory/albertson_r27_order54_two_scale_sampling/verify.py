#!/usr/bin/env python3
"""Exact verifier for the Albertson r=27 order-54 two-scale bound."""

from fractions import Fraction as Q
from math import comb


def ceil_q(value: Q) -> int:
    return -((-value.numerator) // value.denominator)


def sampled_bound(n: int, m: int, sample_size: int) -> Q:
    """Integer-aware sampling of cr >= 5e-203(v-2)/9."""
    s = sample_size
    assert 4 <= s <= n
    local_constant = -(203 * (s - 2) // 9)
    return Q(
        5 * m * comb(n - 2, s - 2) + local_constant * comb(n, s),
        comb(n - 4, s - 4),
    )


def sampled_bound_simplified(n: int, m: int, sample_size: int) -> Q:
    """The same count after simplifying the two binomial ratios."""
    s = sample_size
    local_constant = -(203 * (s - 2) // 9)
    return (
        Q(5 * m * (n - 2) * (n - 3), (s - 2) * (s - 3))
        + Q(
            local_constant * n * (n - 1) * (n - 2) * (n - 3),
            s * (s - 1) * (s - 2) * (s - 3),
        )
    )


def check_sampling_identity() -> None:
    for n in range(4, 55):
        for s in range(4, n + 1):
            for m in (0, n, comb(n, 2)):
                assert sampled_bound(n, m, s) == sampled_bound_simplified(
                    n, m, s
                )


def check_local_line() -> None:
    b25_251 = sampled_bound(32, 251, 25)
    b24_252 = sampled_bound(32, 252, 24)
    slope25 = sampled_bound(32, 1, 25) - sampled_bound(32, 0, 25)
    slope24 = sampled_bound(32, 1, 24) - sampled_bound(32, 0, 24)

    assert b25_251 == Q(866897, 1265)
    assert b25_251 - (9 * 251 - 1574) == Q(372, 1265) > 0
    assert slope25 == Q(2175, 253) < 9

    assert b24_252 == Q(3688220, 5313)
    assert b24_252 - (9 * 252 - 1574) == Q(998, 5313) > 0
    assert slope24 == Q(725, 77) > 9

    # Exhaust the complete edge-count range independently of the endpoint proof.
    for q in range(comb(32, 2) + 1):
        s = 25 if q <= 251 else 24
        assert ceil_q(sampled_bound(32, q, s)) >= 9 * q - 1573


def check_global_bound() -> Q:
    edge_incidence = comb(52, 30)
    crossing_incidence = comb(50, 28)
    sample_count = comb(54, 32)

    bound = Q(
        9 * 726 * edge_incidence - 1573 * sample_count,
        crossing_incidence,
    )
    assert bound == Q(218768121, 35960)
    assert bound == 6083 + Q(23441, 35960)
    assert ceil_q(bound) == 6084
    return bound


def main() -> None:
    check_sampling_identity()
    check_local_line()
    bound = check_global_bound()
    print("PASS Albertson r=27 order-54 two-scale sampling")
    print("32-vertex line: cr(H) >= 9e(H)-1573")
    print("switch: s=25 for q<=251; s=24 for q>=252")
    print(f"n=54,m=726: {bound} = 6083+23441/35960, hence cr(G)>=6084")
    print("conclusion: the order-54 survivor is eliminated; order 53 remains")


if __name__ == "__main__":
    main()
