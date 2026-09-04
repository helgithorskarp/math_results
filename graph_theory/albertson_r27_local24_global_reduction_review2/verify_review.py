#!/usr/bin/env python3
"""Independent exact verifier for the conditional local-24 Albertson reduction.

This implementation uses an exact recursive QuickHull construction.  The
reviewed implementation instead uses a monotone chain and pooled adjacent
slopes, so agreement is not agreement between two spellings of one hull
routine.
"""

from bisect import bisect_right
from fractions import Fraction
from hashlib import sha256


def ceil_ratio(numerator: int, denominator: int) -> int:
    assert denominator > 0
    return -((-numerator) // denominator)


def universal_floor(n: int, m: int) -> int:
    """Integer-rounded maximum of the four imported universal lines."""
    z = n - 2
    return max(
        0,
        m - 3 * z,
        ceil_ratio(7 * m - 25 * z, 3),
        ceil_ratio(37 * m - 155 * z, 9),
        ceil_ratio(45 * m - 203 * z, 9),
    )


def conditional_floor(n: int, m: int) -> int:
    # For n=24 this is the consequence of cr(24,132)>=165, the 37/9 line
    # below 132, and Ackerman's 6n-12 deletion argument above 132.
    return max(0, 5 * m - 495) if n == 24 else 0


Point = tuple[int, int]


def orientation(a: Point, b: Point, p: Point) -> int:
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def quickhull_arc(a: Point, b: Point, points: list[Point]) -> list[Point]:
    """Return the lower-hull arc from a to b by recursive farthest-point splits."""
    below = [p for p in points if orientation(a, b, p) < 0]
    if not below:
        return [a, b]
    pivot = min(below, key=lambda p: (orientation(a, b, p), p[0]))
    left = quickhull_arc(a, pivot, below)
    right = quickhull_arc(pivot, b, below)
    return left[:-1] + right


def lower_hull(values: list[int]) -> list[Point]:
    points = list(enumerate(values))
    return quickhull_arc(points[0], points[-1], points[1:-1])


def hull_value(hull: list[Point], numerator: int, denominator: int) -> Fraction:
    """Evaluate the lower hull at numerator/denominator."""
    assert 0 <= numerator <= denominator * hull[-1][0]
    x_floor = numerator // denominator
    index = bisect_right([p[0] for p in hull], x_floor) - 1
    x0, y0 = hull[index]
    if numerator == x0 * denominator:
        return Fraction(y0)
    x1, y1 = hull[index + 1]
    left_weight = x1 * denominator - numerator
    right_weight = numerator - x0 * denominator
    return Fraction(y0 * left_weight + y1 * right_weight, (x1 - x0) * denominator)


def audit_hull(values: list[int], hull: list[Point]) -> None:
    assert hull[0] == (0, values[0])
    assert hull[-1] == (len(values) - 1, values[-1])
    assert all(a[0] < b[0] for a, b in zip(hull, hull[1:]))
    assert all(
        orientation(a, b, c) > 0
        for a, b, c in zip(hull, hull[1:], hull[2:])
    )
    for q, bound in enumerate(values):
        assert hull_value(hull, q, 1) <= bound


def sampled_floor(n: int, m: int, s: int, hull: list[Point]) -> int:
    mean_numerator = m * s * (s - 1)
    mean_denominator = n * (n - 1)
    local = hull_value(hull, mean_numerator, mean_denominator)
    incidence_ratio = Fraction(
        n * (n - 1) * (n - 2) * (n - 3),
        s * (s - 1) * (s - 2) * (s - 3),
    )
    result = incidence_ratio * local
    return ceil_ratio(result.numerator, result.denominator)


def build_tables(max_order: int) -> tuple[dict[int, list[int]], str]:
    tables: dict[int, list[int]] = {}
    hulls: dict[int, list[Point]] = {}
    digest = sha256()
    for n in range(4, max_order + 1):
        row = []
        for m in range(n * (n - 1) // 2 + 1):
            candidates = [universal_floor(n, m), conditional_floor(n, m)]
            candidates.extend(sampled_floor(n, m, s, hulls[s]) for s in range(4, n))
            value = max(candidates)
            row.append(value)
            digest.update(f"{n}:{m}:{value}\n".encode("ascii"))
        hull = lower_hull(row)
        audit_hull(row, hull)
        tables[n] = row
        hulls[n] = hull
    return tables, digest.hexdigest()


def main() -> None:
    # Hand-checkable tests for the independent QuickHull implementation.
    assert lower_hull([0, 10, 0]) == [(0, 0), (2, 0)]
    assert lower_hull([0, 0, 10]) == [(0, 0), (1, 0), (2, 10)]

    # The order-24 line really follows arithmetically below and at the assumed
    # endpoint.  The above-endpoint step additionally imports Ackerman's
    # simple 4-planar density theorem.
    assert all(universal_floor(24, m) >= 5 * m - 495 for m in range(132))
    assert 165 == 5 * 132 - 495
    assert all(165 + 5 * (m - 132) == 5 * m - 495 for m in range(133, 277))

    tables, digest = build_tables(53)

    slacks = [
        5 * tables[52][q] - (136 * q - 65166)
        for q in range(52 * 51 // 2 + 1)
    ]
    assert min(slacks) == 0
    assert [q for q, slack in enumerate(slacks) if slack == 0] == [686, 691]
    assert tables[52][686] == 5626
    assert tables[52][691] == 5762

    edge_sum = 51 * 713
    numerator = 136 * edge_sum - 53 * 65166
    assert edge_sum == 36363
    assert numerator == 5 * 298314
    assert 298314 == 49 * 6088 + 2
    assert ceil_ratio(298314, 49) == 6089
    assert tables[53][713] == 6089

    expected = "79e615e691c84d697b2dbc3d6fded0d9657c37d3f91f4bebc1a61097fb39f7f6"
    assert digest == expected
    print("PASS independent QuickHull reproduction")
    print("assumption: cr(24,132)>=165")
    print("F_52(686)=5626; F_52(691)=5762")
    print("5 F_52(q) >= 136q-65166, equality only at q=686,691")
    print("conditional conclusion: cr(53,713)>=6089>6084")
    print(f"conditional_recursive_table_sha256={digest}")


if __name__ == "__main__":
    main()
