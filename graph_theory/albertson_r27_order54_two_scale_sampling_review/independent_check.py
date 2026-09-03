#!/usr/bin/env python3
"""Clean-room exact audit of the Albertson r=27 order-54 closure."""

from fractions import Fraction
from hashlib import sha256
from json import dumps
from math import comb


def ceiling(numerator: int, denominator: int) -> int:
    """Return ceil(numerator / denominator), including for negative inputs."""
    assert denominator > 0
    return -((-numerator) // denominator)


def counted_numerator_denominator(q: int, s: int) -> tuple[int, int]:
    """Sum the locally rounded s-vertex inequalities inside 32 vertices."""
    assert 0 <= q <= comb(32, 2)
    assert 4 <= s <= 32
    edge_multiplicity = comb(30, s - 2)
    sample_count = comb(32, s)
    crossing_multiplicity = comb(28, s - 4)
    local_intercept = -(203 * (s - 2) // 9)
    return (
        5 * q * edge_multiplicity + local_intercept * sample_count,
        crossing_multiplicity,
    )


def counted_ceiling(q: int, s: int) -> int:
    numerator, denominator = counted_numerator_denominator(q, s)
    return ceiling(numerator, denominator)


def ratio_form(q: int, s: int) -> Fraction:
    """Independent simplification of the two incidence ratios."""
    local_intercept = -(203 * (s - 2) // 9)
    return (
        Fraction(5 * q * 30 * 29, (s - 2) * (s - 3))
        + Fraction(
            local_intercept * 32 * 31 * 30 * 29,
            s * (s - 1) * (s - 2) * (s - 3),
        )
    )


def check_local_rounding() -> None:
    # Since 5e is integral, ceil(5e-203(s-2)/9)=5e-floor(203(s-2)/9).
    for s in range(4, 33):
        for e in range(comb(s, 2) + 1):
            exact = Fraction(5 * e) - Fraction(203 * (s - 2), 9)
            rounded = 5 * e - (203 * (s - 2) // 9)
            assert ceiling(exact.numerator, exact.denominator) == rounded


def check_two_scale_line() -> list[int]:
    equality_edge_counts = []
    for q in range(comb(32, 2) + 1):
        s = 25 if q <= 251 else 24
        numerator, denominator = counted_numerator_denominator(q, s)
        assert Fraction(numerator, denominator) == ratio_form(q, s)
        obtained = ceiling(numerator, denominator)
        claimed = 9 * q - 1573
        assert obtained >= claimed
        if obtained == claimed:
            equality_edge_counts.append(q)

    # Check the endpoint comparisons and slopes without using decimal numbers.
    b25 = ratio_form(251, 25)
    b24 = ratio_form(252, 24)
    slope25 = ratio_form(1, 25) - ratio_form(0, 25)
    slope24 = ratio_form(1, 24) - ratio_form(0, 24)
    assert b25 - (9 * 251 - 1574) == Fraction(372, 1265) > 0
    assert slope25 == Fraction(2175, 253) < 9
    assert b24 - (9 * 252 - 1574) == Fraction(998, 5313) > 0
    assert slope24 == Fraction(725, 77) > 9

    # Independently maximize over every available sample size at the switch.
    best_251 = max((counted_ceiling(251, s), s) for s in range(4, 33))
    best_252 = max((counted_ceiling(252, s), s) for s in range(4, 33))
    assert best_251 == (686, 25)
    assert best_252 == (695, 24)
    assert equality_edge_counts == [250, 251, 252, 253]
    return equality_edge_counts


def check_order54_average() -> Fraction:
    # Definition-level binomial incidence count.
    numerator = 9 * 726 * comb(52, 30) - 1573 * comb(54, 32)
    denominator = comb(50, 28)
    direct = Fraction(numerator, denominator)

    # Independent calculation after cancelling both binomial ratios.
    edge_ratio = Fraction(52 * 51, 30 * 29)
    sample_ratio = Fraction(54 * 53 * 52 * 51, 32 * 31 * 30 * 29)
    simplified = 9 * 726 * edge_ratio - 1573 * sample_ratio
    assert direct == simplified == Fraction(218768121, 35960)
    assert direct == 6083 + Fraction(23441, 35960)
    assert ceiling(direct.numerator, direct.denominator) == 6084

    z27 = (27 // 2) * (26 // 2) * (25 // 2) * (24 // 2) // 4
    assert z27 == 6084

    # The same sampled lower bound is increasing in the number of edges.
    previous = direct
    for m in range(727, comb(54, 2) + 1):
        current = 9 * m * edge_ratio - 1573 * sample_ratio
        assert current > previous
        previous = current
    return direct


def main() -> None:
    check_local_rounding()
    equality = check_two_scale_line()
    global_bound = check_order54_average()
    summary = {
        "global_bound": str(global_bound),
        "global_ceiling": 6084,
        "line": "cr(H) >= 9q-1573",
        "line_equality_q": equality,
        "switch": {"q<=251": 25, "q>=252": 24},
        "z27": 6084,
    }
    certificate = sha256(
        dumps(summary, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print("PASS independent two-scale order-54 audit")
    print("32-vertex line: cr(H) >= 9q-1573 for all 0 <= q <= 496")
    print("line equality under the chosen scales: q=250,251,252,253")
    print(f"54-vertex bound: {global_bound}; ceiling=6084=Z(27)")
    print(f"certificate_sha256={certificate}")


if __name__ == "__main__":
    main()
