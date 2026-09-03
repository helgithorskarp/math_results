#!/usr/bin/env python3
"""Exact verifier for iterated deletion sampling at Albertson r=27."""

from fractions import Fraction as Q
from math import comb


def ceil_q(x: Q) -> int:
    return -((-x.numerator) // x.denominator)


def sampled_bound(n: int, m: int, s: int) -> Q:
    """Simplified form of integer-aware sampled BK Theorem 3.9(b)."""
    assert 4 <= s <= n
    local_constant = -(203 * (s - 2) // 9)
    return (
        Q(5 * m * (n - 2) * (n - 3), (s - 2) * (s - 3))
        + Q(
            local_constant * n * (n - 1) * (n - 2) * (n - 3),
            s * (s - 1) * (s - 2) * (s - 3),
        )
    )


def sampled_bound_by_counts(n: int, m: int, s: int) -> Q:
    """Same bound before evaluating the two binomial ratios."""
    local_constant = -(203 * (s - 2) // 9)
    return Q(
        5 * m * comb(n - 2, s - 2) + local_constant * comb(n, s),
        comb(n - 4, s - 4),
    )


def check_sampling_identity() -> None:
    for n in (51, 52):
        for s in range(4, n + 1):
            for m in (0, n, comb(n, 2)):
                assert sampled_bound(n, m, s) == sampled_bound_by_counts(
                    n, m, s
                )


def check_order_713() -> Q:
    # Endpoint and slope used in the paper proof of the local affine line.
    endpoint = sampled_bound(52, 687, 24)
    slope = sampled_bound(52, 687, 24) - sampled_bound(52, 686, 24)
    assert endpoint == Q(4234475, 759)
    assert slope == Q(20125, 759) < 27

    # Exhaust every possible degree of a vertex in a 53-vertex simple graph.
    for degree in range(26, 53):
        q = 713 - degree
        local_floor = ceil_q(sampled_bound(52, q, 24))
        assert local_floor >= 27 * q - 12969
        assert local_floor >= 5580 - 27 * (degree - 26)

    degree_excess = 2 * 713 - 53 * 26
    assert degree_excess == 48
    deletion_sum = 53 * 5580 - 27 * degree_excess
    assert deletion_sum == 294444
    bound = Q(deletion_sum, 53 - 4)
    assert bound == Q(294444, 49)
    assert bound == 6009 + Q(3, 49)
    assert ceil_q(bound) == 6010
    return bound


def check_order_715() -> Q:
    endpoint = sampled_bound(51, 661, 24)
    slope = sampled_bound(51, 661, 24) - sampled_bound(51, 660, 24)
    assert endpoint == Q(1305640, 253)
    assert slope == Q(1960, 77) < 27

    expected_high = {
        662: Q(119308, 23),
        663: Q(119952, 23),
        664: Q(120596, 23),
    }
    for q in range(0, 665):
        if q <= 661:
            local_floor = ceil_q(sampled_bound(51, q, 24))
        else:
            value = sampled_bound(51, q, 23)
            assert value == expected_high[q]
            local_floor = ceil_q(value)
        assert local_floor >= 27 * q - 12686

    vertex_pairs = comb(53, 2)
    edge_survival = comb(51, 2)
    crossing_survival = comb(49, 2)
    assert (vertex_pairs, edge_survival, crossing_survival) == (1378, 1275, 1176)

    deletion_sum = 27 * 715 * edge_survival - 12686 * vertex_pairs
    assert deletion_sum == 7132567
    bound = Q(deletion_sum, crossing_survival)
    assert bound == Q(7132567, 1176)
    assert bound == 6065 + Q(127, 1176)
    assert ceil_q(bound) == 6066
    return bound


def main() -> None:
    check_sampling_identity()
    bound_713 = check_order_713()
    bound_715 = check_order_715()
    print("PASS iterated deletion sampling")
    print(f"n=53,m=713: {bound_713}, hence cr(G)>=6010 (previously 6009)")
    print(f"n=53,m=715: {bound_715}, hence cr(G)>=6066 (previously 6064)")
    print("n=53,m=714 remains at 6037 under these estimates")
    print("both improved floors remain below Z(27)=6084")


if __name__ == "__main__":
    main()
