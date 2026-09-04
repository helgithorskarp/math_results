#!/usr/bin/env python3
"""Exact audit of degree-conditioned recursive sampling at Albertson r=27."""

from bisect import bisect_right
from fractions import Fraction
from hashlib import sha256
from math import comb


def ceil_fraction(x: Fraction) -> int:
    return -((-x.numerator) // x.denominator)


# The first four lines are the inputs of the preceding recursive certificate.
# The final line follows from the current 5-planar density theorem and deletion.
LINEAR_BOUNDS = (
    (Fraction(1), Fraction(3)),
    (Fraction(7, 3), Fraction(25, 3)),
    (Fraction(37, 9), Fraction(155, 9)),
    (Fraction(5), Fraction(203, 9)),
    (Fraction(6), Fraction(266, 9)),
)


def base_bound(n: int, m: int) -> int:
    return max(
        [0]
        + [ceil_fraction(a * m - b * (n - 2)) for a, b in LINEAR_BOUNDS]
    )


def lower_hull(values: list[int]) -> list[tuple[int, int]]:
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


def hull_value(hull: list[tuple[int, int]], x: Fraction) -> Fraction:
    xs = [point[0] for point in hull]
    i = bisect_right(xs, x) - 1
    if i == len(hull) - 1 or x == hull[i][0]:
        return Fraction(hull[i][1])
    x0, y0 = hull[i]
    x1, y1 = hull[i + 1]
    return y0 + (x - x0) * Fraction(y1 - y0, x1 - x0)


def recursive_closure(max_n: int, seeds=None):
    seeds = {} if seeds is None else seeds
    bounds = {}
    hulls = {}
    digest = sha256()
    for n in range(4, max_n + 1):
        values = []
        for m in range(comb(n, 2) + 1):
            value = max(base_bound(n, m), seeds.get((n, m), 0))
            for s in range(4, n):
                mean = Fraction(m * s * (s - 1), n * (n - 1))
                local_sum = comb(n, s) * hull_value(hulls[s], mean)
                value = max(
                    value,
                    ceil_fraction(Fraction(local_sum, comb(n - 4, s - 4))),
                )
            values.append(value)
            digest.update(f"{n}:{m}:{value}\n".encode("ascii"))
        bounds[n] = values
        hulls[n] = lower_hull(values)
    return bounds, digest.hexdigest()


def degree_support_dp(local: list[int]):
    """Minimize sum_v F_52(687-x_v), by excess sum and support size."""
    infinity = 10**30
    dp = {(0, 0): (0, ())}  # (excess sum, positive support): (cost, sequence)
    for _ in range(53):
        next_dp = {}
        for (total, support), (cost, sequence) in dp.items():
            for x in range(min(26, 48 - total) + 1):
                key = total + x, support + (x > 0)
                candidate = cost + local[687 - x]
                if candidate < next_dp.get(key, (infinity, ()))[0]:
                    next_dp[key] = candidate, sequence + (x,)
        dp = next_dp
    return {
        h: dp[48, h]
        for h in range(1, 49)
        if (48, h) in dp
    }


def multiplicities(sequence):
    return {x: sequence.count(x) for x in sorted(set(sequence))}


def seeded_frontier(baseline, seed_values):
    bounds, _ = recursive_closure(53, seed_values)
    return bounds[53][713]


def main() -> None:
    bounds, table_digest = recursive_closure(53)
    assert [bounds[53][m] for m in (713, 714, 715)] == [6071, 6100, 6130]

    by_h = degree_support_dp(bounds[52])
    expected = {
        10: (297484, {0: 43, 3: 6, 7: 3, 9: 1}, 6072),
        11: (297482, {0: 42, 3: 8, 7: 2, 10: 1}, 6072),
        12: (297479, {0: 41, 3: 9, 7: 3}, 6071),
    }
    for h, (cost, mult, floor) in expected.items():
        actual_cost, sequence = by_h[h]
        assert actual_cost == cost
        assert multiplicities(sequence) == mult
        assert ceil_fraction(Fraction(actual_cost, 49)) == floor

    # One local unit at q=152 is amplified, but not enough to close the row.
    one_seed = {(25, 152): bounds[25][152] + 1}
    assert bounds[25][152] == 242
    one_seed_floor = seeded_frontier(bounds, one_seed)
    assert one_seed_floor == 6077

    # cr(25,138)>=173 plus 4-planar deletion gives 5q-517 for q>=138.
    # Relative to the computed table this adds one exactly on q=138,...,152.
    prrt_seeds = {}
    for q in range(138, comb(25, 2) + 1):
        candidate = 5 * q - 517
        if candidate > bounds[25][q]:
            prrt_seeds[25, q] = candidate
    assert sorted(q for (_, q) in prrt_seeds) == list(range(138, 153))
    prrt_floor = seeded_frontier(bounds, prrt_seeds)
    assert prrt_floor == 6079

    # A one-unit improvement across the longer active band would close the row.
    band_seeds = {
        (25, q): bounds[25][q] + 1 for q in range(138, 164)
    }
    band_floor = seeded_frontier(bounds, band_seeds)
    assert band_floor == 6100

    print("PASS Albertson r=27 degree-support limitation audit")
    print("enhanced recursive frontier: m=713,714,715 -> 6071,6100,6130")
    for h in (10, 11, 12):
        cost, sequence = by_h[h]
        print(
            f"h={h}: minimum sum={cost}; ceiling(sum/49)="
            f"{ceil_fraction(Fraction(cost, 49))}; excesses={multiplicities(sequence)}"
        )
    print(f"conditional cr(25,152)>=243 frontier={one_seed_floor}")
    print(f"conditional cr(25,138)>=173 deletion-line frontier={prrt_floor}")
    print(f"conditional +1 on F_25(q), q=138,...,163 frontier={band_floor}")
    print(f"enhanced_recursive_table_sha256={table_digest}")


if __name__ == "__main__":
    main()
