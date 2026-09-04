#!/usr/bin/env python3
"""Exact audit of the conditional local-24 reduction for Albertson r=27."""

from bisect import bisect_right
from fractions import Fraction
from hashlib import sha256
from math import comb


def ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


# Published universal crossing-number inequalities.  The conditional local
# input below is separate and is never asserted unconditionally.
LINEAR_BOUNDS = (
    (Fraction(1), Fraction(3)),
    (Fraction(7, 3), Fraction(25, 3)),
    (Fraction(37, 9), Fraction(155, 9)),
    (Fraction(5), Fraction(203, 9)),
)


def base_bound(n: int, m: int) -> int:
    return max(
        [0]
        + [
            ceil_fraction(slope * m - intercept * (n - 2))
            for slope, intercept in LINEAR_BOUNDS
        ]
    )


def conditional_seed(n: int, m: int) -> int:
    """Consequence of the explicit assumption cr(24,132) >= 165."""
    return max(0, 5 * m - 495) if n == 24 else 0


def monotone_chain_hull(values: list[int]) -> list[tuple[int, int]]:
    hull = []
    for point in enumerate(values):
        while len(hull) >= 2:
            x0, y0 = hull[-2]
            x1, y1 = hull[-1]
            x2, y2 = point
            if Fraction(y1 - y0, x1 - x0) >= Fraction(y2 - y1, x2 - x1):
                hull.pop()
            else:
                break
        hull.append(point)
    return hull


def pooled_slope_hull(values: list[int]) -> list[tuple[int, int]]:
    """Independent hull construction by pooling nonincreasing secants."""
    blocks = []
    for left, right in zip(values, values[1:]):
        blocks.append([1, right - left])
        while len(blocks) >= 2:
            run0, rise0 = blocks[-2]
            run1, rise1 = blocks[-1]
            if Fraction(rise0, run0) < Fraction(rise1, run1):
                break
            blocks[-2:] = [[run0 + run1, rise0 + rise1]]
    hull = [(0, values[0])]
    x, y = hull[0]
    for run, rise in blocks:
        x += run
        y += rise
        hull.append((x, y))
    return hull


def hull_value(hull: list[tuple[int, int]], x: Fraction) -> Fraction:
    xs = [point[0] for point in hull]
    index = bisect_right(xs, x) - 1
    if index == len(hull) - 1 or x == hull[index][0]:
        return Fraction(hull[index][1])
    x0, y0 = hull[index]
    x1, y1 = hull[index + 1]
    return y0 + (x - x0) * Fraction(y1 - y0, x1 - x0)


def verify_hull(values: list[int], hull: list[tuple[int, int]]) -> None:
    assert hull[0][0] == 0
    assert hull[-1][0] == len(values) - 1
    slopes = []
    for (x0, y0), (x1, y1) in zip(hull, hull[1:]):
        assert values[x0] == y0
        assert values[x1] == y1
        slopes.append(Fraction(y1 - y0, x1 - x0))
    assert all(left < right for left, right in zip(slopes, slopes[1:]))
    for q, value in enumerate(values):
        assert hull_value(hull, Fraction(q)) <= value


def sampling_bound(
    n: int, m: int, sample_order: int, local_hull: list[tuple[int, int]]
) -> int:
    mean_edges = Fraction(
        m * sample_order * (sample_order - 1), n * (n - 1)
    )
    local_sum = comb(n, sample_order) * hull_value(local_hull, mean_edges)
    crossing_multiplicity = comb(n - 4, sample_order - 4)
    return ceil_fraction(local_sum / crossing_multiplicity)


def recursive_closure(max_order: int):
    bounds = {}
    hulls = {}
    digest = sha256()
    for n in range(4, max_order + 1):
        values = []
        for m in range(comb(n, 2) + 1):
            value = max(base_bound(n, m), conditional_seed(n, m))
            for sample_order in range(4, n):
                value = max(
                    value,
                    sampling_bound(n, m, sample_order, hulls[sample_order]),
                )
            values.append(value)
            digest.update(f"{n}:{m}:{value}\n".encode("ascii"))
        hull_a = monotone_chain_hull(values)
        hull_b = pooled_slope_hull(values)
        assert hull_a == hull_b
        verify_hull(values, hull_a)
        bounds[n] = values
        hulls[n] = hull_a
    return bounds, hulls, digest.hexdigest()


def main() -> None:
    # Check the complete bridge from the one assumed endpoint to the local
    # line.  Above 132 edges this additionally uses the published simple
    # 4-planar density bound, as explained in README.md.
    for m in range(132):
        assert base_bound(24, m) >= 5 * m - 495
    assert 165 == 5 * 132 - 495
    for m in range(133, comb(24, 2) + 1):
        assert 165 + 5 * (m - 132) == 5 * m - 495

    bounds, hulls, table_digest = recursive_closure(53)

    # A compact supporting line extracted from the exact closure.  The
    # pointwise check makes it valid for every 52-vertex edge count, without
    # an assumption on the degree sequence in the final graph.
    slacks = [
        5 * bounds[52][q] - (136 * q - 65166)
        for q in range(comb(52, 2) + 1)
    ]
    assert min(slacks) == 0
    equality = [q for q, slack in enumerate(slacks) if slack == 0]
    assert equality == [686, 691]
    assert (686, 5626) in hulls[52]
    assert (691, 5762) in hulls[52]

    # Delete each vertex of a 53-vertex, 713-edge graph.  Each crossing
    # survives 49 deletions and the sum of the remaining edge counts is
    # 53*713-2*713=36363.
    local_sum_floor = Fraction(136 * 36363 - 53 * 65166, 5)
    assert local_sum_floor == 298314
    assert local_sum_floor == 49 * 6088 + 2
    conditional_floor = ceil_fraction(local_sum_floor / 49)
    assert conditional_floor == 6089
    assert bounds[53][713] == 6089

    print("PASS conditional local-24 Albertson r=27 reduction")
    print("assumption: cr(24,132)>=165")
    print("conditional local line: cr(24,m)>=5m-495")
    print("recursive 52-vertex line: 5cr(H)>=136|E(H)|-65166")
    print("line equality in the computed closure: q=686,691")
    print("53-vertex deletion sum floor=298314=49*6088+2")
    print("conditional conclusion: cr(53,713)>=6089>6084")
    print(f"conditional_recursive_table_sha256={table_digest}")


if __name__ == "__main__":
    main()
