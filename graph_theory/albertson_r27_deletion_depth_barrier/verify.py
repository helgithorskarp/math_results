#!/usr/bin/env python3
"""Exact audit of low-depth induced-deletion limits at Albertson r=27."""

from bisect import bisect_right
from fractions import Fraction
from hashlib import sha256
from math import comb


N = 53
M = 713
K = 27
TOTAL_EXCESS = 2 * M - (K - 1) * N
MIN_SUPPORT = 13
# The complement is connected, so no vertex of G is universal.
MAX_EXCESS = N - 2 - (K - 1)
TARGET = 6084

LINEAR_BOUNDS = (
    (Fraction(1), Fraction(3)),
    (Fraction(7, 3), Fraction(25, 3)),
    (Fraction(37, 9), Fraction(155, 9)),
    (Fraction(5), Fraction(203, 9)),
    (Fraction(6), Fraction(266, 9)),
)


def ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def base_bound(n: int, m: int) -> int:
    return max(
        [0]
        + [
            ceil_fraction(a * m - b * (n - 2))
            for a, b in LINEAR_BOUNDS
        ]
    )


def lower_hull(values: list[int]) -> list[tuple[int, int]]:
    hull: list[tuple[int, int]] = []
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
    index = bisect_right(xs, x) - 1
    if index == len(hull) - 1 or x == hull[index][0]:
        return Fraction(hull[index][1])
    x0, y0 = hull[index]
    x1, y1 = hull[index + 1]
    return y0 + (x - x0) * Fraction(y1 - y0, x1 - x0)


def recursive_closure(max_n: int):
    """Reconstruct the preceding exact recursively sampled local table."""
    bounds: dict[int, list[int]] = {}
    hulls: dict[int, list[tuple[int, int]]] = {}
    digest = sha256()
    for n in range(4, max_n + 1):
        values = []
        for m in range(comb(n, 2) + 1):
            value = base_bound(n, m)
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


def multiplicities(sequence: tuple[int, ...]) -> dict[int, int]:
    return {x: sequence.count(x) for x in sorted(set(sequence))}


def one_deletion_extrema(local: list[int]):
    """Optimize the exact one-deletion sum over the proved degree relaxation."""
    infinity = 10**30
    minimum = {(0, 0): (0, ())}
    maximum = {(0, 0): (0, ())}
    for _ in range(N):
        next_minimum = {}
        next_maximum = {}
        for (total, support), (cost, sequence) in minimum.items():
            for x in range(min(MAX_EXCESS, TOTAL_EXCESS - total) + 1):
                key = total + x, support + (x > 0)
                candidate = cost + local[687 - x], sequence + (x,)
                if candidate[0] < next_minimum.get(key, (infinity, ()))[0]:
                    next_minimum[key] = candidate
        for (total, support), (cost, sequence) in maximum.items():
            for x in range(min(MAX_EXCESS, TOTAL_EXCESS - total) + 1):
                key = total + x, support + (x > 0)
                candidate = cost + local[687 - x], sequence + (x,)
                if candidate[0] > next_maximum.get(key, (-infinity, ()))[0]:
                    next_maximum[key] = candidate
        minimum, maximum = next_minimum, next_maximum

    allowed_minimum = [
        (cost, support, sequence)
        for (total, support), (cost, sequence) in minimum.items()
        if total == TOTAL_EXCESS and support >= MIN_SUPPORT
    ]
    allowed_maximum = [
        (cost, support, sequence)
        for (total, support), (cost, sequence) in maximum.items()
        if total == TOTAL_EXCESS and support >= MIN_SUPPORT
    ]
    return min(allowed_minimum), max(allowed_maximum)


def deletion_range(t: int) -> tuple[int, int]:
    """Range forced by excess 48, support at least 13, and x_v <= 25."""
    outside_positive = max(0, MIN_SUPPORT - t)
    maximum_inside_excess = min(
        MAX_EXCESS * t,
        TOTAL_EXCESS - outside_positive,
    )
    q_min = M - (K - 1) * t - maximum_inside_excess
    q_max = M - (K - 1) * t + comb(t, 2)
    return q_min, q_max


def chord_majorant(values: list[int], q_min: int, q_max: int):
    """Return and exactly verify the endpoint chord as an upper majorant."""
    slope = Fraction(values[q_max] - values[q_min], q_max - q_min)
    intercept = Fraction(values[q_min]) - slope * q_min
    slacks = tuple(slope * q + intercept - values[q] for q in range(q_min, q_max + 1))
    assert min(slacks) == 0
    assert all(slack >= 0 for slack in slacks)
    return slope, intercept, slacks


def deletion_potential(bounds: dict[int, list[int]], t: int):
    """Upper-bound what the current t-deletion sum could numerically certify."""
    s = N - t
    q_min, q_max = deletion_range(t)
    slope, intercept, slacks = chord_majorant(bounds[s], q_min, q_max)
    sample_count = comb(N, t)
    crossing_multiplicity = comb(N - 4, t)
    edge_count_sum = M * comb(N - 2, t)
    mean = Fraction(edge_count_sum, sample_count)
    assert q_min <= mean <= q_max
    upper_sum = slope * edge_count_sum + intercept * sample_count
    integer_upper_sum = upper_sum.numerator // upper_sum.denominator
    certificate_ceiling = ceil_fraction(Fraction(integer_upper_sum, crossing_multiplicity))
    threshold_sum = (TARGET - 1) * crossing_multiplicity + 1
    return {
        "t": t,
        "s": s,
        "range": (q_min, q_max),
        "endpoints": ((q_min, bounds[s][q_min]), (q_max, bounds[s][q_max])),
        "line": (slope, intercept),
        "mean": mean,
        "upper_sum": upper_sum,
        "integer_upper_sum": integer_upper_sum,
        "crossing_multiplicity": crossing_multiplicity,
        "certificate_ceiling": certificate_ceiling,
        "threshold_sum": threshold_sum,
        "shortfall": threshold_sum - integer_upper_sum,
        "slack_digest": sha256(
            "\n".join(str(slack) for slack in slacks).encode("ascii")
        ).hexdigest(),
    }


def main() -> None:
    assert TOTAL_EXCESS == 48
    assert MAX_EXCESS == 25
    bounds, table_digest = recursive_closure(53)
    assert table_digest == "55da0a3d413620951dba0ac52618fa24f09d59de43a0c7e8a0f3927283036f43"
    assert [bounds[53][q] for q in (713, 714, 715)] == [6071, 6100, 6130]

    one_min, one_max = one_deletion_extrema(bounds[52])
    assert (one_min[0], one_min[1], multiplicities(one_min[2])) == (
        297470,
        16,
        {0: 37, 3: 16},
    )
    assert (one_max[0], one_max[1], multiplicities(one_max[2])) == (
        297517,
        13,
        {0: 40, 1: 11, 12: 1, 25: 1},
    )
    assert ceil_fraction(Fraction(one_min[0], 49)) == 6071
    assert ceil_fraction(Fraction(one_max[0], 49)) == 6072

    results = [deletion_potential(bounds, t) for t in range(1, 5)]
    expected = {
        1: ((662, 687), ((662, 4977), (687, 5638)), Fraction(661, 25), Fraction(-313157, 25), 6073, 524),
        2: ((624, 662), ((624, 4300), (662, 5243)), Fraction(943, 38), Fraction(-212516, 19), 6077, 7198),
        3: ((597, 638), ((597, 3908), (638, 4882)), Fraction(974, 41), Fraction(-421250, 41), 6082, 25178),
        4: ((570, 615), ((570, 3529), (615, 4555)), Fraction(114, 5), Fraction(-9467), 6090, -1458376),
    }
    for result in results:
        t = result["t"]
        wanted = expected[t]
        assert (
            result["range"],
            result["endpoints"],
            result["line"][0],
            result["line"][1],
            result["certificate_ceiling"],
            result["shortfall"],
        ) == wanted

    print("PASS Albertson r=27 low-depth deletion barrier audit")
    print(
        "one-deletion exact range over h>=13: "
        f"min={one_min[0]} ({multiplicities(one_min[2])}), "
        f"max={one_max[0]} ({multiplicities(one_max[2])}); "
        "certificate ceilings 6071..6072"
    )
    for result in results:
        slope, intercept = result["line"]
        print(
            f"t={result['t']}, local_order={result['s']}, "
            f"q_range={result['range']}, mean={result['mean']}, "
            f"majorant={slope}*q+({intercept}), "
            f"integer_sum_cap={result['integer_upper_sum']}, "
            f"certificate_ceiling={result['certificate_ceiling']}, "
            f"target_sum_shortfall={result['shortfall']}"
        )
    print("conclusion: t<=3 cannot reach 6084 from the current local tables; t=4 is the first depth with numerical headroom")
    print(f"recursive_table_sha256={table_digest}")


if __name__ == "__main__":
    main()
