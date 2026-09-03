#!/usr/bin/env python3
"""Exact rational audit of the constants in the asymptotic proof."""

from fractions import Fraction


def separation_polynomial(m: int) -> Fraction:
    """Lower exponent minus the uniform symmetric-broom upper exponent."""
    return (
        Fraction(215, 72) * m * m
        - Fraction(323, 4) * m
        - Fraction(329, 8)
    )


def main() -> None:
    # log_2(27(m+1)) <= m/3 begins at m=32.  Cubing avoids floating point.
    assert 891**3 < 2**32

    # The ratio 2^(m/3)/(27(m+1)) then increases: for m >= 32,
    # (m+2)/(m+1) <= 34/33 < 2^(1/3).
    assert 34**3 < 2 * 33**3

    # At the smallest parametric witness (m=2), the p-hub potential wins.
    # Thereafter its exponential side is multiplied by 512 while the linear
    # comparison side increases by only 15.
    assert 2 ** (9 * 2 - 7) > 15 * 2 + 8
    assert 512 > 1 + 15

    # The final exponent gap is positive at m=32 and strictly increasing.
    base_gap = separation_polynomial(32)
    first_increment = separation_polynomial(33) - base_gap
    second_difference = (
        separation_polynomial(34)
        - 2 * separation_polynomial(33)
        + separation_polynomial(32)
    )
    assert base_gap > 0
    assert first_increment > 0
    assert second_difference > 0

    print(f"log_bound_base_integer_gap={2**32 - 891**3}")
    print(f"log_bound_ratio_integer_gap={2 * 33**3 - 34**3}")
    print(f"potential_base_gap={2 ** (9 * 2 - 7) - (15 * 2 + 8)}")
    print(f"separation_gap_m32={base_gap.numerator}/{base_gap.denominator}")
    print(
        "separation_first_increment="
        f"{first_increment.numerator}/{first_increment.denominator}"
    )
    print(
        "separation_second_difference="
        f"{second_difference.numerator}/{second_difference.denominator}"
    )
    print("status=VERIFIED")


if __name__ == "__main__":
    main()
