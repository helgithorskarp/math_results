#!/usr/bin/env python3
"""Independent rational-interval audit of the Gaussian beta cell certificate.

This checker deliberately does not import the submitted certificate, its bounds
module, or its expected output.  In particular, exp(-x) is enclosed by an
alternating Taylor series after binary range reduction, followed by interval
squaring.  The submitted checker instead bounds exp(+x) by a positive Taylor
series and geometric tail and then takes reciprocals.
"""

from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations
from math import comb, factorial, isqrt
import json


N = 5
M = N + 2
ETA = Q(1, 100)
EXP_GRID = 10**36
KERNEL_GRID = 10**28
MARGINS = tuple(map(Q, (
    "1/100", "1/500", "1/3000", "1/50000", "1/1500000",
    "1/125000000",
)))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def floor_grid(x, scale):
    return Q((x.numerator * scale) // x.denominator, scale)


def ceil_grid(x, scale):
    return -floor_grid(-x, scale)


@lru_cache(None)
def exp_minus(x):
    """Enclose exp(-x), x >= 0, using only exact rational arithmetic.

    Reduce x to u <= 1/8.  For such u the alternating exponential series has
    decreasing terms, so its odd and even partial sums are rigorous lower and
    upper bounds.  Outward rounding before each interval squaring prevents
    denominator growth without sacrificing rigor.
    """
    require(isinstance(x, Q) and x >= 0, "invalid exponential argument")
    if x == 0:
        return Q(1), Q(1)
    reductions = 0
    u = x
    while u > Q(1, 8):
        u /= 2
        reductions += 1

    partial = Q(0)
    even_upper = None
    odd_lower = None
    for n in range(32):
        term = u**n / factorial(n)
        partial += term if n % 2 == 0 else -term
        if n == 30:
            even_upper = partial
        elif n == 31:
            odd_lower = partial
    require(0 < odd_lower <= even_upper <= 1, "alternating enclosure failed")

    lo = floor_grid(odd_lower, EXP_GRID)
    hi = ceil_grid(even_upper, EXP_GRID)
    for _ in range(reductions):
        lo = floor_grid(lo * lo, EXP_GRID)
        hi = ceil_grid(hi * hi, EXP_GRID)
    require(0 <= lo <= hi <= 1, "range-reduced exponential enclosure failed")
    return lo, hi


@lru_cache(None)
def sqrt_interval(n):
    """Enclose sqrt(n) on the same exact decimal grid."""
    q = isqrt(n * EXP_GRID * EXP_GRID)
    lo = Q(q, EXP_GRID)
    hi = lo if q*q == n * EXP_GRID * EXP_GRID else Q(q + 1, EXP_GRID)
    require(lo*lo <= n <= hi*hi, "square-root enclosure failed")
    return lo, hi


def geometry():
    vertices = ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
    source = list(vertices)
    target = list(vertices)
    for i in range(4):
        for j in range(4):
            if i != j:
                source.append(tuple(b-a for a, b in zip(vertices[i], vertices[j])))
                target.append(tuple(b+a for a, b in zip(vertices[i], vertices[j])))
    return tuple(source), tuple(target)


def squared_distance_matrix(points):
    return tuple(tuple(sum((a-b)**2 for a, b in zip(u, v)) for v in points)
                 for u in points)


def centroid_pair_sum(points, row):
    m = len(row)
    return m * sum(sum(a*a for a in points[i]) for i in row) - sum(
        sum(points[i][coordinate] for i in row)**2 for coordinate in range(3)
    )


def kernel_interval(m, sy, sx):
    """Enclose m^(-3/2)(exp(-Sy/(2m))-exp(-Sx/(2m)))."""
    error = comb(m, 2) * ETA
    yl = max(Q(0), Q(sy) - error) / (2*m)
    yh = (Q(sy) + error) / (2*m)
    xl = max(Q(0), Q(sx) - error) / (2*m)
    xh = (Q(sx) + error) / (2*m)

    e_yh_lo, _ = exp_minus(yh)
    _, e_xl_hi = exp_minus(xl)
    _, e_yl_hi = exp_minus(yl)
    e_xh_lo, _ = exp_minus(xh)
    numerator_lo = max(Q(0), e_yh_lo - e_xl_hi)
    numerator_hi = max(Q(0), e_yl_hi - e_xh_lo)

    sqrt_lo, sqrt_hi = sqrt_interval(m)
    lo = floor_grid(numerator_lo / (m*sqrt_hi), KERNEL_GRID)
    hi = ceil_grid(numerator_hi / (m*sqrt_lo), KERNEL_GRID)
    require(0 <= lo <= hi, "kernel enclosure failed")
    return int(lo*KERNEL_GRID), int(hi*KERNEL_GRID)


def beta_factor(k, m):
    j = m-k-2
    return (Q((N+1)*comb(N, k)*(-1)**j*comb(N-k, j),
              m*(m-1)*comb(M, m)))


def main():
    source, target = geometry()
    require(len(source) == len(target) == 16, "unexpected fixture size")
    dx = squared_distance_matrix(source)
    dy = squared_distance_matrix(target)
    pairs = tuple(combinations(range(16), 2))
    require(all(dx[i][j] >= dy[i][j] for i, j in pairs),
            "centre is not a contraction")
    require(min(dx[i][j] for i, j in pairs) > ETA,
            "source labels might collide in the cell")
    require(max(dx[0]) + ETA < 36 and max(dy[0]) + ETA < 36,
            "anchored radius-six check failed")

    rows = {}
    row_count = 0
    exponent_pairs = set()
    for m in range(2, M+1):
        for row in combinations(range(16), m):
            sx = sum(dx[i][j] for i, j in combinations(row, 2))
            sy = sum(dy[i][j] for i, j in combinations(row, 2))
            require(sx == centroid_pair_sum(source, row),
                    "source pair-sum identity failed")
            require(sy == centroid_pair_sum(target, row),
                    "target pair-sum identity failed")
            rows[row] = kernel_interval(m, sy, sx)
            exponent_pairs.add((m, sy, sx))
            row_count += 1
    require(row_count == sum(comb(16, m) for m in range(2, M+1)) == 26316,
            "incomplete row coverage")

    minima = [None]*(N+1)
    minimizers = [None]*(N+1)
    maxima = [None]*(N+1)
    tested = 0
    for alpha in combinations(range(16), M):
        sums = {}
        for m in range(2, M+1):
            lo = hi = 0
            for row in combinations(alpha, m):
                row_lo, row_hi = rows[row]
                lo += row_lo
                hi += row_hi
            sums[m] = lo, hi

        for k in range(N+1):
            coeff_lo = Q(0)
            coeff_hi = Q(0)
            for m in range(k+2, M+1):
                factor = beta_factor(k, m)
                row_lo, row_hi = sums[m]
                if factor >= 0:
                    coeff_lo += factor * row_lo / KERNEL_GRID
                    coeff_hi += factor * row_hi / KERNEL_GRID
                else:
                    coeff_lo += factor * row_hi / KERNEL_GRID
                    coeff_hi += factor * row_lo / KERNEL_GRID
            require(coeff_lo <= coeff_hi, "reversed coefficient enclosure")
            require(coeff_lo > MARGINS[k],
                    "margin failure: " + repr((alpha, k, coeff_lo, MARGINS[k])))
            if minima[k] is None or coeff_lo < minima[k]:
                minima[k] = coeff_lo
                minimizers[k] = alpha
            if maxima[k] is None or coeff_hi > maxima[k]:
                maxima[k] = coeff_hi
        tested += 1
    require(tested == comb(16, M) == 11440,
            "incomplete seven-label coverage")

    result = {
        "method": "alternating exp(-x) Taylor bounds, binary range reduction, interval squaring",
        "imports_submitted_code_or_expected_output": False,
        "eta": str(ETA),
        "kernel_grid_digits": 28,
        "rows_checked": row_count,
        "distinct_kernel_arguments": len(exponent_pairs),
        "distinct_seven_label_tuples": tested,
        "signs_checked": tested*(N+1),
        "minimum_lower_bounds": [str(x) for x in minima],
        "minimum_lower_bounds_decimal": [f"{float(x):.15g}" for x in minima],
        "claimed_margins": [str(x) for x in MARGINS],
        "gaps_above_claimed_margins_decimal": [
            f"{float(minima[k]-MARGINS[k]):.15g}" for k in range(N+1)
        ],
        "minimizers": [list(x) for x in minimizers],
        "maximum_upper_bounds_decimal": [f"{float(x):.15g}" for x in maxima],
        "status": "PASS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
