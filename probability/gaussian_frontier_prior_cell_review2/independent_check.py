#!/usr/bin/env python3
"""Independent exact audit of the full-prior Gaussian frontier cell.

The asymmetric vertex is reconstructed with its first coordinate explicit and
only the last two coordinates quotiented.  This deliberately avoids the
author certificate's signed-permutation orbit splitting.
"""

import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
import json
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "gaussian_frontier_prior_cell"
INHERITED = HERE.parent / "gaussian_frontier_middle_cell"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def ceiling(q):
    return (q.numerator + q.denominator - 1) // q.denominator


@lru_cache(maxsize=None)
def exp_neg(q, bits):
    """Enclose exp(-q) by reciprocating a positive exp(q) series."""
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
            high = ceiling(F(scale, 1) / total)
            if high - low <= 2:
                require(0 <= low <= high <= scale, "exponential enclosure")
                return low, high


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
    bound = q.numerator * scale * scale
    low, high = 0, 1
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
    # atan(1/2)+atan(1/3)=pi/4, with both angles in the first quadrant.
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


def symmetric_multiplicity(i, j, k):
    signs = (1 if i == 0 else 2) * (1 if j == 0 else 2) * (1 if k == 0 else 2)
    permutations = 1 if i == k else (3 if i == j or j == k else 6)
    return signs * permutations


def yz_multiplicity(j, k):
    signs = (1 if j == 0 else 2) * (1 if k == 0 else 2)
    swaps = 1 if j == k else 2
    return signs * swaps


def kernel_tables(h, half_grid, bits):
    a = {n: exp_neg((h * n) ** 2 / 2, bits)
         for n in range(-half_grid, half_grid + 1)}
    plus = {n: exp_neg((h * n - 1) ** 2 / 2, bits)
            for n in range(-half_grid, half_grid + 1)}
    minus = {n: exp_neg((h * n + 1) ** 2 / 2, bits)
             for n in range(-half_grid, half_grid + 1)}
    return a, plus, minus


def central_histograms(h, half_grid, bits):
    """Full octahedral quotient for residual mass at the origin."""
    scale = 1 << bits
    denominator = 156 * scale * scale
    a, plus, minus = kernel_tables(h, half_grid, bits)
    source, target = Counter(), Counter()
    stream = sha256()
    representatives = total_sites = 0
    for i in range(half_grid + 1):
        for j in range(i, half_grid + 1):
            for k in range(j, half_grid + 1):
                multiplicity = symmetric_multiplicity(i, j, k)
                ai, aj, ak = a[i][1], a[j][1], a[k][1]
                outer = (plus[i][1] + minus[i][1]) * aj * ak
                outer += ai * (plus[j][1] + minus[j][1]) * ak
                outer += ai * aj * (plus[k][1] + minus[k][1])
                source_upper = ceiling(F(30 * ai * aj * ak + 21 * outer,
                                         denominator))
                target_lower = a[i][0] * a[j][0] * a[k][0] // (scale * scale)
                source[source_upper] += multiplicity
                target[target_lower] += multiplicity
                stream.update(
                    f"{i}:{j}:{k}:{multiplicity}:{source_upper}:{target_lower}\n".encode()
                )
                representatives += 1
                total_sites += multiplicity
    require(total_sites == (2 * half_grid + 1) ** 3, "central orbit coverage")
    return source, target, representatives, stream.hexdigest()


def outer_histograms(h, half_grid, bits):
    """Keep x explicit; quotient (y,z) only under signs and interchange."""
    scale = 1 << bits
    denominator = 156 * scale * scale
    a, plus, minus = kernel_tables(h, half_grid, bits)
    source, target = Counter(), Counter()
    stream = sha256()
    representatives = total_sites = 0
    for x in range(-half_grid, half_grid + 1):
        ax = a[x][1]
        px, nx = plus[x][1], minus[x][1]
        for j in range(half_grid + 1):
            for k in range(j, half_grid + 1):
                multiplicity = yz_multiplicity(j, k)
                aj, ak = a[j][1], a[k][1]
                pair_sum = (px + nx) * aj * ak
                pair_sum += ax * (plus[j][1] + minus[j][1]) * ak
                pair_sum += ax * aj * (plus[k][1] + minus[k][1])
                # This vertex has weight 51/156 at +e1, 21/156 at the
                # other five outer centres, and no mass at the origin.
                numerator = 21 * pair_sum + 30 * px * aj * ak
                source_upper = ceiling(F(numerator, denominator))
                target_lower = a[x][0] * a[j][0] * a[k][0] // (scale * scale)
                source[source_upper] += multiplicity
                target[target_lower] += multiplicity
                stream.update(
                    f"{x}:{j}:{k}:{multiplicity}:{source_upper}:{target_lower}\n".encode()
                )
                representatives += 1
                total_sites += multiplicity
    require(total_sites == (2 * half_grid + 1) ** 3, "outer quotient coverage")
    return source, target, representatives, stream.hexdigest()


def direct_small_histograms(h, half_grid, bits, residual):
    """Definition-level, unquotiented control for either residual vertex."""
    require(residual in ("central", "outer"), "unknown residual vertex")
    scale = 1 << bits
    denominator = 156 * scale * scale
    a, plus, minus = kernel_tables(h, half_grid, bits)
    source, target = Counter(), Counter()
    for x in range(-half_grid, half_grid + 1):
        for y in range(-half_grid, half_grid + 1):
            for z in range(-half_grid, half_grid + 1):
                ax, ay, az = a[x][1], a[y][1], a[z][1]
                pair_sum = (plus[x][1] + minus[x][1]) * ay * az
                pair_sum += ax * (plus[y][1] + minus[y][1]) * az
                pair_sum += ax * ay * (plus[z][1] + minus[z][1])
                numerator = 21 * pair_sum
                numerator += 30 * (ax * ay * az if residual == "central"
                                   else plus[x][1] * ay * az)
                source[ceiling(F(numerator, denominator))] += 1
                target[a[x][0] * a[y][0] * a[z][0] // (scale * scale)] += 1
    return source, target


def suffix_window_max(source, target, left, right):
    """Definition-level maximum of the difference of discrete hinges."""
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
    best = argmax = None
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
    sign = 1
    previous = 1
    for k in range(len(a) - 1):
        pivot = next((r for r in range(k, len(a)) if a[r][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        for i in range(k + 1, len(a)):
            for j in range(k + 1, len(a)):
                numerator = a[i][j] * a[k][k] - a[i][k] * a[k][j]
                require(numerator % previous == 0, "Bareiss divisibility")
                a[i][j] = numerator // previous
        previous = a[k][k]
    return sign * a[-1][-1]


def audit():
    manifest = pins()
    cell = json.loads((TARGET / "CELL.json").read_text())
    inherited = json.loads((INHERITED / "CELL.json").read_text())
    centers = cell["source_centers"]
    require(centers == [[0, 0, 0], [1, 0, 0], [-1, 0, 0],
                        [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]],
            "source centres")
    required = {
        "variance": "1", "source_coordinate_radius": "1/256",
        "target_coordinate_radius": "1/16", "outer_source_mass_floor": "21/156",
        "origin_source_mass_floor": "0", "weight_denominator": 156,
        "middle_window": ["1/256", "7/10"],
        "claimed_adverse_middle_upper": "-1/256",
        "quadrature_step": "1/16", "quadrature_half_grid": 112,
    }
    require(all(cell.get(key) == value for key, value in required.items()),
            "changed cell parameters")

    alpha, beta = F(21, 156), F(30, 156)
    epsilon, target_radius, rho = F(1, 128), F(7, 64), F(25, 8)
    left, right = map(F, cell["middle_window"])
    require(6 * alpha + beta == 1, "prior simplex mass")
    require(comb(36, 6) == 1_947_792, "denominator-156 prior count")
    # Exact barycentric identity: lambda_0=p_0/beta and
    # lambda_i=(p_i-alpha)/beta.  The following generic symbolic sample also
    # checks reconstruction away from the vertices.
    sample = [F(7, 60), F(1, 5), F(1, 10), F(1, 12), F(1, 15), F(1, 20), F(23, 60)]
    sample = [beta * sample[0]] + [alpha + beta * value for value in sample[1:]]
    lambdas = [sample[0] / beta] + [(value - alpha) / beta for value in sample[1:]]
    require(sum(lambdas) == 1 and all(value >= 0 for value in lambdas),
            "barycentric coordinates")
    require(sample == [beta * lambdas[0]]
            + [alpha + beta * value for value in lambdas[1:]],
            "barycentric reconstruction")

    require(F(3, 256 ** 2) < epsilon ** 2, "source Euclidean radius")
    require(F(3, 16 ** 2) < target_radius ** 2, "target Euclidean radius")
    loss_floor = (1 - 2 * epsilon) ** 2 - F(3, 64)
    require(loss_floor == F(3777, 4096) > F(1, 256), "pair-loss floor")

    numerators = inherited["rank_six_target_integer_numerators"]
    rows = []
    for i in range(1, 7):
        rows.append([256 * (centers[i][j] - centers[0][j]) for j in range(3)]
                    + [numerators[i][j] - numerators[0][j] for j in range(3)])
    determinant = F(bareiss_determinant(rows), 256 ** 6)
    require(determinant == F(-2105, 16777216), "rank-six determinant")

    endpoint_bits = 80
    endpoint_scale = 1 << endpoint_bits
    slope = F(4, 7) - epsilon - target_radius
    exponent = rho * slope - F(1, 2) - epsilon - epsilon ** 2 / 2 + target_radius ** 2 / 2
    require(slope == F(407, 896) and exponent == F(210485, 229376),
            "outer constants")
    outer_exp_upper = F(exp_neg(exponent, endpoint_bits)[1], endpoint_scale)
    constant = F(1, 2) + epsilon + epsilon ** 2 / 2
    source_inside = 3 * alpha * min(
        F(exp_neg(constant, endpoint_bits)[0], endpoint_scale),
        F(exp_neg(rho ** 2 / 2 - (F(4, 7) - epsilon) * rho + constant,
                  endpoint_bits)[0], endpoint_scale),
    )
    target_inside = F(exp_neg((rho + target_radius) ** 2 / 2,
                              endpoint_bits)[0], endpoint_scale)
    require(outer_exp_upper < 3 * alpha, "outer density comparison")
    require(min(source_inside, target_inside) > left, "low endpoint clipping")
    peak = 6 * alpha * F(61, 100) + beta + epsilon
    require(F(exp_neg(F(1, 2), endpoint_bits)[1], endpoint_scale) < F(61, 100),
            "peak exponential")
    require(peak == F(2217, 3200) < right, "upper endpoint")

    # Definition-level unquotiented controls ensure each independent quotient
    # reproduces the same rounded density histogram on a small grid.
    control_h, control_m, control_bits = F(1, 3), 3, 40
    central_control = central_histograms(control_h, control_m, control_bits)[:2]
    outer_control = outer_histograms(control_h, control_m, control_bits)[:2]
    require(central_control == direct_small_histograms(
        control_h, control_m, control_bits, "central"), "central quotient control")
    require(outer_control == direct_small_histograms(
        control_h, control_m, control_bits, "outer"), "outer quotient control")

    bits = 56
    scale = 1 << bits
    h, half_grid = F(1, 16), 112
    central, target_c, central_reps, central_digest = central_histograms(
        h, half_grid, bits)
    outer, target_o, outer_reps, outer_digest = outer_histograms(
        h, half_grid, bits)
    require(target_c == target_o, "target quotient disagreement")
    c_low, c_high = gaussian_constant_bounds(96)
    require(c_low < c_high, "Gaussian constant enclosure")
    g = 1 + h ** 2 / 8
    quadrature = h ** 2 * (1 + g + g ** 2) / 4
    tail = 3 * g ** 2 * F(exp_neg(F(18), endpoint_bits)[1], endpoint_scale) / 6
    perturbation = epsilon / 2 + F(3, 1024)
    require(perturbation == F(7, 1024), "diffuse-cell transfer")

    records = []
    for name, histogram, representatives, digest, multiplicity in [
        ("central_residual", central, central_reps, central_digest, 1),
        ("outer_residual", outer, outer_reps, outer_digest, 6),
    ]:
        maximum, argmax, thresholds = suffix_window_max(
            histogram, target_c, left * scale, right * scale)
        require(maximum < 0, f"{name} reference polygon is not negative")
        discrete = c_low * h ** 3 * maximum / scale
        reference_upper = discrete + quadrature + tail
        cell_upper = reference_upper + perturbation
        require(cell_upper < -F(1, 256), f"{name} lacks claimed margin")
        records.append({
            "vertex_orbit": name,
            "number_of_vertices": multiplicity,
            "quotient_representatives": representatives,
            "quotient_stream_sha256": digest,
            "evaluated_thresholds": thresholds,
            "polygon_maximum_units": str(maximum),
            "argmax_over_C": str(argmax / scale),
            "discrete_adverse_upper": str(discrete),
            "reference_adverse_upper": str(reference_upper),
            "cell_adverse_upper": str(cell_upper),
        })

    return {
        "status": "INDEPENDENT_PRIOR_SIMPLEX_CELL_REVIEW_PASS",
        "target_commit": manifest["target_commit"],
        "target_graph_ref": manifest["target_graph_ref"],
        "pinned_files": len(manifest["files"]),
        "method": "positive-series reciprocal exponentials; explicit first coordinate at the asymmetric vertex; two-coordinate sign/swap quotient; suffix hinge sums",
        "precision_bits": bits,
        "full_lattice_sites_per_vertex": (2 * half_grid + 1) ** 3,
        "vertex_orbits": records,
        "gaussian_constant_lower": str(c_low),
        "gaussian_constant_upper": str(c_high),
        "quadrature_error": str(quadrature),
        "tail_error": str(tail),
        "cell_perturbation_loss": str(perturbation),
        "uniform_cell_adverse_upper": str(max(F(row["cell_adverse_upper"])
                                                   for row in records)),
        "claimed_upper": "-1/256",
        "outer_exp_upper": str(outer_exp_upper),
        "outer_coefficient": str(3 * alpha),
        "source_inside_lower": str(source_inside),
        "target_inside_lower": str(target_inside),
        "source_peak_upper": str(peak),
        "uniform_pair_loss_lower": str(loss_floor),
        "inherited_rank_six_determinant": str(determinant),
        "denominator156_weight_vectors": comb(36, 6),
        "small_unquotiented_sites_per_vertex": (2 * control_m + 1) ** 3,
        "verdict": "accept the stated variance-one all-threshold prior-simplex measure cell; this is not the full frontier or an all-variance result",
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
