#!/usr/bin/env python3
"""Independent exact audit of the gap-free Gaussian frontier cell."""

import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "gaussian_frontier_middle_cell"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def ceiling(q):
    return (q.numerator + q.denominator - 1) // q.denominator


@lru_cache(maxsize=None)
def exp_neg(q, bits):
    """Dyadic enclosure from a positive exp(q) series and reciprocal bounds."""
    require(q >= 0 and bits >= 16, "invalid exponential request")
    scale = 1 << bits
    if q == 0:
        return scale, scale
    total = term = F(1)
    n = 0
    while True:
        n += 1
        term *= q / n
        total += term
        next_term = term * q / (n + 1)
        ratio = q / (n + 2)
        if ratio < 1:
            remainder = next_term / (1 - ratio)
            low = int(scale / (total + remainder))
            high = ceiling(scale / total)
            if high - low <= 2:
                require(F(low, scale) <= exp_upper_proxy(q, total, remainder)
                        and low <= high <= scale, "exponential enclosure invariant")
                return low, high


def exp_upper_proxy(q, total, remainder):
    """A rational value known not to exceed exp(-q), used only as a check."""
    del q
    return 1 / (total + remainder)


def atan_bounds(x, bits):
    total = F(0)
    term = x
    n = 0
    while True:
        total += term / (2 * n + 1)
        next_term = -term * x * x
        next_sum = total + next_term / (2 * n + 3)
        if abs(next_sum - total) < F(1, 1 << bits):
            return min(total, next_sum), max(total, next_sum)
        term = next_term
        n += 1


def dyadic_sqrt_bounds(q, bits):
    require(q >= 0, "negative square root")
    scale = 1 << bits
    low, high = 0, 1
    bound = q.numerator * scale * scale
    while high * high * q.denominator <= bound:
        low, high = high, 2 * high
    while high - low > 1:
        middle = (low + high) // 2
        if middle * middle * q.denominator <= bound:
            low = middle
        else:
            high = middle
    lower = F(low, scale)
    upper = lower if lower * lower == q else F(high, scale)
    require(lower * lower <= q <= upper * upper, "square-root enclosure")
    return lower, upper


def gaussian_constant_bounds(bits):
    # atan(1/2)+atan(1/3)=pi/4 by the tangent addition formula and quadrant.
    a0, a1 = atan_bounds(F(1, 2), bits + 20)
    b0, b1 = atan_bounds(F(1, 3), bits + 20)
    pi_low, pi_high = 4 * (a0 + b0), 4 * (a1 + b1)
    require(F(3) < pi_low < pi_high < F(22, 7), "pi enclosure")
    lower = dyadic_sqrt_bounds(1 / (2 * pi_high) ** 3, bits)[0]
    upper = dyadic_sqrt_bounds(1 / (2 * pi_low) ** 3, bits)[1]
    return lower, upper


def pins():
    manifest = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    require(manifest["schema"] == 1, "manifest schema")
    for relative, expected in manifest["files"].items():
        actual = sha256((HERE / relative).read_bytes()).hexdigest()
        require(actual == expected, f"changed target or dependency: {relative}")
    return manifest


def orbit_multiplicity(i, j, k):
    signs = (1 if i == 0 else 2) * (1 if j == 0 else 2) * (1 if k == 0 else 2)
    permutations = 1 if i == k else (3 if i == j or j == k else 6)
    return signs * permutations


def orbit_histograms(h, half_grid, bits):
    scale = 1 << bits
    a = [exp_neg((h * j) ** 2 / 2, bits) for j in range(half_grid + 1)]
    b = [(exp_neg((h * j - 1) ** 2 / 2, bits)[0]
          + exp_neg((h * j + 1) ** 2 / 2, bits)[0],
          exp_neg((h * j - 1) ** 2 / 2, bits)[1]
          + exp_neg((h * j + 1) ** 2 / 2, bits)[1])
         for j in range(half_grid + 1)]
    source, target = Counter(), Counter()
    stream = sha256()
    representatives = total_sites = 0
    divisor = 78 * scale * scale
    for i in range(half_grid + 1):
        for j in range(i, half_grid + 1):
            for k in range(j, half_grid + 1):
                multiplicity = orbit_multiplicity(i, j, k)
                ai, aj, ak = a[i][1], a[j][1], a[k][1]
                numerator = (12 * ai * aj * ak
                             + 11 * (b[i][1] * aj * ak
                                     + ai * b[j][1] * ak
                                     + ai * aj * b[k][1]))
                source_upper = ceiling(F(numerator, divisor))
                target_lower = a[i][0] * a[j][0] * a[k][0] // (scale * scale)
                source[source_upper] += multiplicity
                target[target_lower] += multiplicity
                stream.update(
                    f"{i}:{j}:{k}:{multiplicity}:{source_upper}:{target_lower}\n".encode()
                )
                representatives += 1
                total_sites += multiplicity
    require(total_sites == (2 * half_grid + 1) ** 3, "orbit coverage")
    return source, target, representatives, stream.hexdigest()


def direct_small_histograms(h, half_grid, bits):
    scale = 1 << bits
    a = [exp_neg((h * j) ** 2 / 2, bits) for j in range(half_grid + 1)]
    b = [(exp_neg((h * j - 1) ** 2 / 2, bits)[0]
          + exp_neg((h * j + 1) ** 2 / 2, bits)[0],
          exp_neg((h * j - 1) ** 2 / 2, bits)[1]
          + exp_neg((h * j + 1) ** 2 / 2, bits)[1])
         for j in range(half_grid + 1)]
    source, target = Counter(), Counter()
    divisor = 78 * scale * scale
    for ii in range(-half_grid, half_grid + 1):
        for jj in range(-half_grid, half_grid + 1):
            for kk in range(-half_grid, half_grid + 1):
                i, j, k = abs(ii), abs(jj), abs(kk)
                ai, aj, ak = a[i][1], a[j][1], a[k][1]
                numerator = (12 * ai * aj * ak
                             + 11 * (b[i][1] * aj * ak
                                     + ai * b[j][1] * ak
                                     + ai * aj * b[k][1]))
                source[ceiling(F(numerator, divisor))] += 1
                target[a[i][0] * a[j][0] * a[k][0] // (scale * scale)] += 1
    return source, target


def suffix_window_max(source, target, left, right):
    """Definition-level hinge values from active suffix counts and sums."""
    require(sum(source.values()) == sum(target.values()), "lattice totals")
    candidates = sorted({left, right} | {
        value for value in source.keys() | target.keys() if left < value < right
    })
    source_items = sorted(source.items())
    target_items = sorted(target.items())
    total_sc = sum(source.values())
    total_ss = sum(value * count for value, count in source.items())
    total_tc = sum(target.values())
    total_ts = sum(value * count for value, count in target.items())
    below_sc = below_ss = below_tc = below_ts = 0
    si = ti = 0
    best = None
    argmax = None
    for threshold in candidates:
        while si < len(source_items) and source_items[si][0] <= threshold:
            value, count = source_items[si]
            below_sc += count
            below_ss += value * count
            si += 1
        while ti < len(target_items) and target_items[ti][0] <= threshold:
            value, count = target_items[ti]
            below_tc += count
            below_ts += value * count
            ti += 1
        hinge = ((total_ss - below_ss) - threshold * (total_sc - below_sc)
                 - (total_ts - below_ts) + threshold * (total_tc - below_tc))
        if best is None or hinge > best:
            best, argmax = hinge, threshold
    return best, argmax, len(candidates)


def bareiss_determinant(matrix):
    a = [row[:] for row in matrix]
    n = len(a)
    sign = 1
    previous = 1
    for k in range(n - 1):
        pivot = next((r for r in range(k, n) if a[r][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * a[k][k] - a[i][k] * a[k][j]
                require(numerator % previous == 0, "Bareiss divisibility")
                a[i][j] = numerator // previous
        previous = a[k][k]
    return sign * a[-1][-1]


def audit():
    manifest = pins()
    cell = json.loads((TARGET / "CELL.json").read_text())
    centers = cell["source_centers"]
    weights = [F(value) for value in cell["weights"]]
    require(weights == [F(2, 13)] + [F(11, 78)] * 6 and sum(weights) == 1,
            "weights")
    epsilon = F(1, 128)
    target_radius = F(7, 64)
    rho = F(25, 8)
    left, right = map(F, cell["middle_window"])
    loss_floor = (1 - 2 * epsilon) ** 2 - F(3, 64)
    require(loss_floor == F(3777, 4096) > F(1, 256), "uniform contraction")
    require(1 + 2 * epsilon == F(65, 64) < 3, "source frontier radius")
    require(2 * target_radius == F(7, 32) < 3, "target frontier radius")

    target_numerators = cell["rank_six_target_integer_numerators"]
    integer_rows = []
    for i in range(1, 7):
        integer_rows.append(
            [256 * (centers[i][j] - centers[0][j]) for j in range(3)]
            + [target_numerators[i][j] - target_numerators[0][j] for j in range(3)]
        )
    determinant = F(bareiss_determinant(integer_rows), 256 ** 6)
    require(determinant == F(-2105, 16777216), "paired determinant")
    example = [[F(value, 256) for value in row] for row in target_numerators]
    losses = []
    for i in range(7):
        for j in range(i):
            source_distance = sum(F(centers[i][k] - centers[j][k]) ** 2 for k in range(3))
            target_distance = sum((example[i][k] - example[j][k]) ** 2 for k in range(3))
            losses.append(source_distance - target_distance)
    require(min(losses) == F(32657, 32768), "example minimum loss")

    endpoint_bits = 80
    endpoint_scale = 1 << endpoint_bits
    slope = F(4, 7) - epsilon - target_radius
    exponent = rho * slope - F(1, 2) - epsilon - epsilon ** 2 / 2 + target_radius ** 2 / 2
    require(slope == F(407, 896) and exponent == F(210485, 229376), "outer constants")
    outer_upper = F(exp_neg(exponent, endpoint_bits)[1], endpoint_scale)
    source_inside = F(exp_neg((rho + epsilon) ** 2 / 2 + F(11, 26) + epsilon,
                              endpoint_bits)[0], endpoint_scale)
    target_inside = F(exp_neg((rho + target_radius) ** 2 / 2,
                              endpoint_bits)[0], endpoint_scale)
    peak_exp = F(exp_neg(F(1, 2), endpoint_bits)[1], endpoint_scale)
    require(outer_upper < F(11, 26), "outer domination")
    require(source_inside > left and target_inside > left, "low endpoint clipping")
    peak = F(2, 13) + F(11, 13) * peak_exp + epsilon
    require(peak < right, "upper endpoint")

    # Direct enumeration on a small grid checks the orbit reconstruction.
    small_orbit = orbit_histograms(F(1, 3), 3, 40)[:2]
    small_direct = direct_small_histograms(F(1, 3), 3, 40)
    require(small_orbit == small_direct, "orbit reconstruction")

    bits = 56
    scale = 1 << bits
    h = F(1, 16)
    half_grid = 112
    source, target, representatives, digest = orbit_histograms(h, half_grid, bits)
    maximum, argmax, thresholds = suffix_window_max(
        source, target, int(left * scale), int(right * scale)
    )
    require(maximum < 0, "reference polygon is not negative")
    c_low, c_high = gaussian_constant_bounds(96)
    require(c_low < c_high, "Gaussian constant enclosure")
    discrete = c_low * h ** 3 * F(maximum, scale)
    g = 1 + h ** 2 / 8
    quadrature = h ** 2 * (1 + g + g ** 2) / 4
    tail = 3 * g ** 2 * F(exp_neg(F(18), endpoint_bits)[1], endpoint_scale) / 6
    reference_upper = discrete + quadrature + tail
    perturbation = epsilon / 2 + F(3, 1024)
    cell_upper = reference_upper + perturbation
    require(perturbation == F(7, 1024), "cell perturbation")
    require(cell_upper < -F(1, 200), "middle margin")

    return {
        "status": "INDEPENDENT_GAP_FREE_CELL_REVIEW_PASS",
        "target_commit": manifest["target_commit"],
        "target_graph_ref": manifest["target_graph_ref"],
        "pinned_files": len(manifest["files"]),
        "method": "positive-series reciprocal exponentials, atan(1/2)+atan(1/3), Bareiss determinant, suffix hinge sums",
        "bits": bits,
        "full_lattice_sites": (2 * half_grid + 1) ** 3,
        "orbit_representatives": representatives,
        "orbit_stream_sha256": digest,
        "evaluated_thresholds": thresholds,
        "polygon_maximum_units": maximum,
        "argmax_over_C": str(F(argmax, scale)),
        "gaussian_constant_lower": str(c_low),
        "gaussian_constant_upper": str(c_high),
        "discrete_adverse_upper": str(discrete),
        "quadrature_error": str(quadrature),
        "tail_error": str(tail),
        "reference_adverse_upper": str(reference_upper),
        "cell_perturbation_loss": str(perturbation),
        "cell_adverse_upper": str(cell_upper),
        "claimed_upper": "-1/200",
        "outer_exp_upper": str(outer_upper),
        "source_inside_lower": str(source_inside),
        "target_inside_lower": str(target_inside),
        "source_peak_upper": str(peak),
        "uniform_pair_loss_lower": str(loss_floor),
        "example_paired_determinant": str(determinant),
        "example_minimum_loss": str(min(losses)),
        "small_direct_lattice_sites": 7 ** 3,
        "verdict": "accept explicit continuous all-threshold cell at variance one; no full-frontier or all-variance conclusion"
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--expected", type=Path, default=HERE / "REVIEW_EXPECTED.json")
    args = parser.parse_args()
    result = audit()
    if args.check:
        require(result == json.loads(args.expected.read_text()), "review record differs")
        print(result["status"])
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
