#!/usr/bin/env python3
"""Exact verifier for the recursive convex induced-sampling bound."""

from bisect import bisect_right
from fractions import Fraction
from hashlib import sha256
from math import comb


def ceil_fraction(x):
    return -((-x.numerator) // x.denominator)


LINEAR_BOUNDS = (
    (Fraction(1), Fraction(3)),
    (Fraction(7, 3), Fraction(25, 3)),
    (Fraction(37, 9), Fraction(155, 9)),
    (Fraction(5), Fraction(203, 9)),
)


def base_bound(n, m):
    """Rounded maximum of the four imported universal linear bounds and 0."""
    return max(
        [0]
        + [ceil_fraction(a * m - b * (n - 2)) for a, b in LINEAR_BOUNDS]
    )


def monotone_chain_hull(values):
    """Lower convex hull of (q, values[q]), by the orientation test."""
    hull = []
    for point in enumerate(values):
        while len(hull) >= 2:
            x0, y0 = hull[-2]
            x1, y1 = hull[-1]
            x2, y2 = point
            left_slope = Fraction(y1 - y0, x1 - x0)
            right_slope = Fraction(y2 - y1, x2 - x1)
            if left_slope >= right_slope:
                hull.pop()
            else:
                break
        hull.append(point)
    return hull


def pava_hull(values):
    """Independent lower-hull construction by pooling decreasing secant slopes."""
    blocks = []
    for i in range(len(values) - 1):
        blocks.append([1, values[i + 1] - values[i]])  # horizontal run, rise
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


def hull_value(hull, x):
    xs = [point[0] for point in hull]
    i = bisect_right(xs, x) - 1
    if i == len(hull) - 1 or x == hull[i][0]:
        return Fraction(hull[i][1])
    x0, y0 = hull[i]
    x1, y1 = hull[i + 1]
    return y0 + (x - x0) * Fraction(y1 - y0, x1 - x0)


def verify_hull(values, hull):
    """Check convex slopes, endpoints, and the minorant inequality at every q."""
    assert hull[0][0] == 0
    assert hull[-1][0] == len(values) - 1
    slopes = []
    for (x0, y0), (x1, y1) in zip(hull, hull[1:]):
        assert values[x0] == y0 and values[x1] == y1
        slopes.append(Fraction(y1 - y0, x1 - x0))
    assert all(a < b for a, b in zip(slopes, slopes[1:]))
    for q, value in enumerate(values):
        assert hull_value(hull, Fraction(q)) <= value


def sampling_bound(n, m, s, local_hull):
    mean_edges = Fraction(m * s * (s - 1), n * (n - 1))
    summed_local_floor = comb(n, s) * hull_value(local_hull, mean_edges)
    crossing_multiplicity = comb(n - 4, s - 4)
    return ceil_fraction(summed_local_floor / crossing_multiplicity)


def recursive_closure(max_n):
    bounds = {}
    hulls = {}
    digest = sha256()
    for n in range(4, max_n + 1):
        values = []
        for m in range(comb(n, 2) + 1):
            value = base_bound(n, m)
            for s in range(4, n):
                value = max(value, sampling_bound(n, m, s, hulls[s]))
            values.append(value)
            digest.update(f"{n}:{m}:{value}\n".encode("ascii"))
        hull_a = monotone_chain_hull(values)
        hull_b = pava_hull(values)
        assert hull_a == hull_b
        verify_hull(values, hull_a)
        bounds[n] = values
        hulls[n] = hull_a
    return bounds, hulls, digest.hexdigest()


def lifted_fifty_vertex_line(m):
    numerator = 26 * m * comb(51, 48) - 11706 * comb(53, 50)
    denominator = comb(49, 46)
    return Fraction(numerator, denominator)


def main():
    bounds, hulls, table_digest = recursive_closure(53)

    # This is the reusable computer-assisted lemma.  Checking every q avoids
    # any assumption about which edge count occurs in the final application.
    line_slacks = [
        bounds[50][q] - (26 * q - 11706) for q in range(comb(50, 2) + 1)
    ]
    assert min(line_slacks) == 0
    equality = [q for q, slack in enumerate(line_slacks) if slack == 0]
    assert equality == list(range(633, 640))

    expected = {
        713: (Fraction(55914547, 9212), 6070),
        714: (Fraction(14046318, 2303), 6100),
        715: (Fraction(56455997, 9212), 6129),
    }
    for m, (fraction, ceiling) in expected.items():
        actual = lifted_fifty_vertex_line(m)
        assert actual == fraction
        assert ceil_fraction(actual) == ceiling

    # The full recursion is slightly stronger at the endpoints than the one
    # 50-vertex line needed to eliminate the final two rows.
    assert [bounds[53][m] for m in (713, 714, 715)] == [6071, 6100, 6130]

    print("PASS recursive convex induced-sampling audit")
    print("universal 50-vertex line: cr(H) >= 26q-11706")
    print("line equality in computed closure: q=633,...,639")
    for m in (713, 714, 715):
        fraction, ceiling = expected[m]
        print(
            f"50-to-53 lift at m={m}: {fraction}; ceiling={ceiling}; "
            f"full_closure={bounds[53][m]}"
        )
    print(f"recursive_table_sha256={table_digest}")


if __name__ == "__main__":
    main()
