#!/usr/bin/env python3
"""Independent exact checks for the 24-vertex Albertson reduction.

This does not import the target artifact.  It verifies the numerical
implications of the cited inequalities, independently exhausts their finite
integer system, and checks the equality-component arithmetic.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import product
from json import dumps
from math import comb


N = 24
S = N - 2
M = 132
MAX_CROSSINGS = 164


def ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def local_line_checks() -> None:
    """Check every integer edge count in the three local ranges."""
    for edges in range(M):
        first_line = ceil_fraction(Fraction(37 * edges - 155 * S, 9))
        assert first_line >= 5 * edges - 495

    # The unproved local target supplies precisely this endpoint.
    assert 165 == 5 * M - 495

    # At larger edge counts the 4-planar deletion argument supplies five
    # crossings per removed edge.  This assertion checks its arithmetic only.
    for edges in range(M + 1, comb(N, 2) + 1):
        assert 165 + 5 * (edges - M) == 5 * edges - 495


def feasible_profiles() -> set[tuple[int, ...]]:
    """Flat exhaustive search of the published necessary integer system."""
    rows: set[tuple[int, ...]] = set()

    for a, b, c in product(range(23), repeat=3):
        if a + b + c != 22:
            continue
        for d in range(111):
            e2 = 110 - 2 * c - d
            if e2 < 0:
                continue
            for delta in range(45):
                x2 = ceil_fraction(Fraction(7 * e2 - 550 + 2 * delta, 3))
                total = 5 * a + 4 * b + 9 * c + 3 * d + x2
                if total > MAX_CROSSINGS:
                    continue

                # From Proposition 21 and the triangulation identity one has
                # 3*m0+h+t <= 3*d, so m0 <= d.  The remaining ranges follow
                # from 3*p+4*h <= 44-4*c.
                for m0 in range(d + 1):
                    for p in range(15):
                        for h in range(12):
                            t = 44 - 4 * c - 3 * p - 4 * h
                            if t < 0:
                                continue
                            if 3 * (p + h) < 44 - 4 * c - 3 * d + 3 * m0:
                                continue
                            if b > c + h + 4 * m0 + 2 * t:
                                continue
                            rows.add(
                                (
                                    a,
                                    b,
                                    c,
                                    d,
                                    delta,
                                    m0,
                                    p,
                                    h,
                                    t,
                                    e2,
                                    x2,
                                    total,
                                )
                            )
    return rows


def component_arithmetic(row: tuple[int, ...]) -> tuple[int, int, int, int]:
    """Consequences after the separately audited equality induction."""
    p = row[6]
    e2 = row[9]
    x2 = row[10]
    numerator = 2 * e2 - 8 * S
    assert numerator % 3 == 0
    c5 = numerator // 3
    k2 = x2 - 5 * c5
    free_edges = e2 - 5 * c5 - 2 * k2
    non_full_c5 = c5 - p
    assert min(c5, k2, free_edges, non_full_c5) >= 0
    return c5, k2, free_edges, non_full_c5


def sampling_check() -> Fraction:
    numerator = 5 * 726 * comb(52, 22) - 495 * comb(54, 24)
    denominator = comb(50, 20)
    bound = Fraction(numerator, denominator)
    assert bound == Fraction(1_965_795, 322)
    assert ceil_fraction(bound) == 6105 > 6084
    return bound


def main() -> None:
    local_line_checks()
    rows = feasible_profiles()
    expected = {
        (0, 20, 2, 3, 0, 0, 9, 0, 9, 103, 57, 164),
        (0, 22, 0, 4, 0, 0, 11, 0, 11, 106, 64, 164),
    }
    assert rows == expected

    components = {
        row: component_arithmetic(row) for row in sorted(rows)
    }
    assert set(components.values()) == {
        (10, 7, 39, 1),
        (12, 4, 38, 1),
    }
    bound = sampling_check()

    certificate = {
        "profiles": [list(row) for row in sorted(rows)],
        "components": [list(components[row]) for row in sorted(rows)],
        "sampling_numerator": bound.numerator,
        "sampling_denominator": bound.denominator,
        "sampling_ceiling": ceil_fraction(bound),
    }
    digest = sha256(dumps(certificate, sort_keys=True).encode()).hexdigest()

    print("PASS independent Albertson 24-vertex obstruction review")
    for row in sorted(rows):
        print(f"profile={row}; components={components[row]}")
    print(f"conditional sampling={bound}; ceiling={ceil_fraction(bound)}")
    print(f"certificate_sha256={digest}")


if __name__ == "__main__":
    main()
