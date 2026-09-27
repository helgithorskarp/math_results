#!/usr/bin/env python3
"""Independent exact audit of the deep-flap Gaussian frontier cell.

The new signed radial cover is replayed with a positive-series reciprocal
exponential enclosure, rather than the target's alternating-series routine.
The middle lattice is reconstructed by explicit tetrahedral group orbits,
rather than the target's closed multiplicity formula.
"""

import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from math import ceil, exp
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "gaussian_deep_flap_cell"

D = 44
Q = 1 << D
ROOT_BITS = 22
ROOT_Q = 1 << ROOT_BITS
EXP_POWER = D + ROOT_BITS + 1
EXP_BITS = 58
EXP_Q = 1 << EXP_BITS
EPSILON = F(1, 1024)

V = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
X = [tuple(F(value, 2) for value in vertex) for vertex in V]
Y = [tuple(F(63 * value, 128) for value in vertex) for vertex in V]
for first in range(4):
    for second in range(4):
        if first != second:
            X.append(tuple(F(V[second][k] - 2 * V[first][k], 2) for k in range(3)))
            Y.append(tuple(F(63 * (V[second][k] + 2 * V[first][k]), 128)
                           for k in range(3)))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def ceiling(q):
    return (q.numerator + q.denominator - 1) // q.denominator


def pins():
    manifest = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    require(manifest["schema"] == 1, "manifest schema")
    for relative, expected in manifest["files"].items():
        actual = sha256((HERE / relative).read_bytes()).hexdigest()
        require(actual == expected, f"changed target or dependency: {relative}")
    return manifest


@lru_cache(maxsize=None)
def sqrt_bounds(q, bits):
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


@lru_cache(maxsize=None)
def exp_neg_fraction(q, bits):
    """Dyadic enclosure from a positive exp(q) series and reciprocals."""
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
                require(0 <= low <= high <= scale, "fraction exponential enclosure")
                return low, high


def exp_neg_dyadic_positive(num, power, bits=EXP_BITS):
    """Enclose exp(-num/2^power) using a positive fixed-point series.

    This is deliberately different from the target's alternating-series
    enclosure.  Range reduction is followed by a positive exp(r) sum, a
    geometric remainder, reciprocal bounds, and outward squaring.
    """
    require(num >= 0 and power >= 0 and bits >= 16, "invalid dyadic exponential")
    output_scale = 1 << bits
    if num == 0:
        return output_scale, output_scale
    squarings = max(0, num.bit_length() - power + 3)
    work_bits = bits + 2 * squarings + 24
    scale = 1 << work_bits
    denominator = 1 << (power + squarings)
    r_low = num * scale // denominator
    r_high = (num * scale + denominator - 1) // denominator
    require(0 <= r_low <= r_high <= scale // 8, "positive-series range reduction")

    term_low = term_high = scale
    sum_low = sum_high = scale
    n = 0
    while True:
        n += 1
        divisor = scale * n
        term_low = term_low * r_low // divisor
        term_high = (term_high * r_high + divisor - 1) // divisor
        sum_low += term_low
        sum_high += term_high
        next_divisor = scale * (n + 1)
        next_high = (term_high * r_high + next_divisor - 1) // next_divisor
        if next_high <= 1:
            # Every subsequent term ratio is at most 1/8, so the whole
            # remaining tail is at most (8/7) times this next term.
            exp_low = sum_low
            exp_high = sum_high + (8 * next_high + 6) // 7
            break
        require(n <= 200, "positive exponential series did not terminate")

    low = scale * scale // exp_high
    high = (scale * scale + exp_low - 1) // exp_low
    for _ in range(squarings):
        low = low * low // scale
        high = min(scale, (high * high + scale - 1) // scale)
    projection = 1 << (work_bits - bits)
    low //= projection
    high = min(output_scale, (high + projection - 1) // projection)
    require(0 <= low <= high <= output_scale, "positive exponential projection")
    return low, high


def exp_signed_dyadic(num):
    if num <= 0:
        return exp_neg_dyadic_positive(-num, EXP_POWER)
    low, high = exp_neg_dyadic_positive(num, EXP_POWER)
    require(low > 0, "positive relative exponential overflow")
    return EXP_Q * EXP_Q // high, (EXP_Q * EXP_Q + low - 1) // low


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


def gaussian_constant_bounds(bits):
    a0, a1 = atan_bounds(F(1, 2), bits + 20)
    b0, b1 = atan_bounds(F(1, 3), bits + 20)
    pi_low, pi_high = 4 * (a0 + b0), 4 * (a1 + b1)
    require(F(3) < pi_low < pi_high < F(22, 7), "pi enclosure")
    lower = sqrt_bounds(1 / (2 * pi_high) ** 3, bits)[0]
    upper = sqrt_bounds(1 / (2 * pi_low) ** 3, bits)[1]
    return lower, upper


@lru_cache(maxsize=None)
def make_patches(n):
    """Two triangular charts with exact areas and tighter angular radii."""
    patches = []
    for i in range(n):
        for j in range(i, n):
            u = F(2 * i + 1, 2 * n)
            v = F(2 * j + 1, 2 * n)
            inv_norm_low, inv_norm_high = sqrt_bounds(1 / (1 + u * u + v * v), D + 12)
            angular_radius = sqrt_bounds(
                1 / (2 * n * n * (1 + F(i, n) ** 2 + F(j, n) ** 2)),
                D + 12,
            )[1]
            jacobian_low = sqrt_bounds(
                1 / (1 + F(i + 1, n) ** 2 + F(j + 1, n) ** 2) ** 3,
                D + 12,
            )[0]
            jacobian_high = sqrt_bounds(
                1 / (1 + F(i, n) ** 2 + F(j, n) ** 2) ** 3,
                D + 12,
            )[1]
            area = F(1, n * n * (1 if i < j else 2))
            for parity in (1, -1):
                records = []
                for centres, source_lower in ((X, True), (Y, False)):
                    dots, norms = [], []
                    for centre in centres:
                        norm_squared = sum(value * value for value in centre)
                        norm_upper = sqrt_bounds(norm_squared, D + 12)[1]
                        numerator = parity * centre[0] * u + centre[1] * v + centre[2]
                        dot_low = numerator * (inv_norm_low if numerator >= 0 else inv_norm_high)
                        dot_high = numerator * (inv_norm_high if numerator >= 0 else inv_norm_low)
                        if source_lower:
                            dot = dot_low - norm_upper * angular_radius - EPSILON
                            norm = norm_squared + 2 * norm_upper * EPSILON + EPSILON ** 2
                            dots.append((dot * Q).__floor__())
                            norms.append(ceiling(norm * Q))
                        else:
                            dot = dot_high + norm_upper * angular_radius + EPSILON
                            norm = norm_squared - 2 * norm_upper * EPSILON
                            dots.append(ceiling(dot * Q))
                            norms.append((norm * Q).__floor__())
                    records.append((dots, norms))
                patches.append({
                    "index": (i, j, parity),
                    "area": area,
                    "jacobian_low": jacobian_low,
                    "jacobian_high": jacobian_high,
                    "source": records[0],
                    "target": records[1],
                })
    require(sum(patch["area"] for patch in patches) == 1, "two-chart parameter area")
    return patches


def root_proposal(threshold_s, record, source_lower):
    dots, norms = record
    terms = [(dot / Q, norm / (2 * Q)) for dot, norm in zip(dots, norms)]
    s = float(threshold_s)
    threshold = s * s / 2
    low, high = max(2.250001, s - 5), s + 4
    for _ in range(36):
        radius = (low + high) / 2
        value = sum(exp(threshold - radius * radius / 2 + radius * dot - norm)
                    for dot, norm in terms)
        if value > 16:
            low = radius
        else:
            high = radius
    if source_lower:
        return int(low * ROOT_Q) - 8
    return ceil(high * ROOT_Q) + 8


def check_root(threshold_s, record, root, source_lower):
    require(root > F(9, 4) * ROOT_Q, "radial endpoint below monotone region")
    dots, norms = record
    threshold_units = threshold_s * threshold_s / 2 * (1 << EXP_POWER)
    require(threshold_units.denominator == 1, "threshold scale")
    base = int(threshold_units) - root * root * (1 << (D - ROOT_BITS))
    total = 0
    for dot, norm in zip(dots, norms):
        exponent = base + 2 * root * dot - norm * (1 << ROOT_BITS)
        low, high = exp_signed_dyadic(exponent)
        total += low if source_lower else high
    slack = total - 16 * EXP_Q if source_lower else 16 * EXP_Q - total
    require(slack > 0, "proposed endpoint is not certified")
    return slack


def radial_band(n, step, start, stop):
    patches = make_patches(n)
    windows = int((stop - start) / step)
    require(start + windows * step == stop, "radial window coverage")
    stream = sha256()
    previous_source = None
    minimum_volume = minimum_s = minimum_slack = None
    for index in range(windows + 1):
        threshold_s = start + index * step
        source_roots, target_roots = [], []
        for patch in patches:
            source = root_proposal(threshold_s, patch["source"], True)
            target = root_proposal(threshold_s, patch["target"], False)
            source_slack = check_root(threshold_s, patch["source"], source, True)
            target_slack = check_root(threshold_s, patch["target"], target, False)
            for slack in (source_slack, target_slack):
                minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
            source_roots.append(source)
            target_roots.append(target)
            stream.update(f"{index}:{patch['index']}:{source}:{target}\n".encode())
        if previous_source is not None:
            volume = F(0)
            for patch, source, target in zip(patches, previous_source, target_roots):
                difference = F(source ** 3 - target ** 3, ROOT_Q ** 3)
                jacobian = (patch["jacobian_low"] if difference >= 0
                            else patch["jacobian_high"])
                volume += 8 * patch["area"] * jacobian * difference
            require(volume > F(1, 2), "signed radial-volume margin")
            if minimum_volume is None or volume < minimum_volume:
                minimum_volume, minimum_s = volume, threshold_s - step
        previous_source = source_roots
    return {
        "n": n,
        "start": str(start),
        "stop": str(stop),
        "step": str(step),
        "patches": len(patches),
        "windows": windows,
        "verified_roots": 2 * (windows + 1) * len(patches),
        "minimum_relative_slack_units": minimum_slack,
        "volume_lower": str(minimum_volume),
        "worst_S": str(minimum_s),
        "stream_sha256": stream.hexdigest(),
    }


def tetrahedral_images(point):
    images = set()
    for permutation in permutations(range(3)):
        for signs in product((-1, 1), repeat=3):
            if signs[0] * signs[1] * signs[2] == 1:
                images.add(tuple(signs[k] * point[permutation[k]] for k in range(3)))
    return images


def group_orbits(half_grid):
    """Construct each orbit from the 24 transformations themselves."""
    total = representatives = 0
    for i in range(half_grid + 1):
        for j in range(i, half_grid + 1):
            for k in range(j, half_grid + 1):
                local = {}
                for seed in ((i, j, k), (-i, j, k)):
                    orbit = tetrahedral_images(seed)
                    local[min(orbit)] = len(orbit)
                for representative, multiplicity in sorted(local.items()):
                    representatives += 1
                    total += multiplicity
                    yield representative, multiplicity
    require(total == (2 * half_grid + 1) ** 3, "explicit group-orbit coverage")


def middle_histograms(h, half_grid, bits):
    scale = 1 << bits
    denominator = 16 * scale * scale
    coordinates = sorted({coordinate for centre in X + Y for coordinate in centre})
    tables = {
        coordinate: [exp_neg_fraction((h * index - coordinate) ** 2 / 2, bits)
                     for index in range(-half_grid, half_grid + 1)]
        for coordinate in coordinates
    }
    source_atoms = [[tables[value] for value in centre] for centre in X]
    target_atoms = [[tables[value] for value in centre] for centre in Y]
    source, target = Counter(), Counter()
    stream = sha256()
    representatives = total = 0
    for point, multiplicity in group_orbits(half_grid):
        indices = tuple(value + half_grid for value in point)
        source_numerator = sum(atom[0][indices[0]][1]
                               * atom[1][indices[1]][1]
                               * atom[2][indices[2]][1]
                               for atom in source_atoms)
        target_numerator = sum(atom[0][indices[0]][0]
                               * atom[1][indices[1]][0]
                               * atom[2][indices[2]][0]
                               for atom in target_atoms)
        source_upper = ceiling(F(source_numerator, denominator))
        target_lower = target_numerator // denominator
        source[source_upper] += multiplicity
        target[target_lower] += multiplicity
        stream.update(
            f"{point}:{multiplicity}:{source_upper}:{target_lower}\n".encode()
        )
        representatives += 1
        total += multiplicity
    require(total == (2 * half_grid + 1) ** 3, "middle lattice coverage")
    return source, target, representatives, stream.hexdigest()


def direct_middle_histograms(h, half_grid, bits):
    """Definition-level unquotiented control for the group reconstruction."""
    scale = 1 << bits
    denominator = 16 * scale * scale
    coordinates = sorted({coordinate for centre in X + Y for coordinate in centre})
    tables = {
        coordinate: [exp_neg_fraction((h * index - coordinate) ** 2 / 2, bits)
                     for index in range(-half_grid, half_grid + 1)]
        for coordinate in coordinates
    }
    source_atoms = [[tables[value] for value in centre] for centre in X]
    target_atoms = [[tables[value] for value in centre] for centre in Y]
    source, target = Counter(), Counter()
    for point in product(range(-half_grid, half_grid + 1), repeat=3):
        indices = tuple(value + half_grid for value in point)
        source_numerator = sum(atom[0][indices[0]][1]
                               * atom[1][indices[1]][1]
                               * atom[2][indices[2]][1]
                               for atom in source_atoms)
        target_numerator = sum(atom[0][indices[0]][0]
                               * atom[1][indices[1]][0]
                               * atom[2][indices[2]][0]
                               for atom in target_atoms)
        source[ceiling(F(source_numerator, denominator))] += 1
        target[target_numerator // denominator] += 1
    return source, target


def suffix_window_max(source, target, left, right):
    require(sum(source.values()) == sum(target.values()), "histogram totals")
    candidates = sorted({left, right} | {
        value for value in source.keys() | target.keys() if left < value < right
    })
    source_items, target_items = sorted(source.items()), sorted(target.items())
    source_count = sum(source.values())
    source_sum = sum(value * count for value, count in source.items())
    target_count = sum(target.values())
    target_sum = sum(value * count for value, count in target.items())
    below_sc = below_ss = below_tc = below_ts = si = ti = 0
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
        hinge = ((source_sum - below_ss) - threshold * (source_count - below_sc)
                 - (target_sum - below_ts) + threshold * (target_count - below_tc))
        if best is None or hinge > best:
            best, argmax = hinge, threshold
    return best, argmax, len(candidates)


def middle_audit():
    control_h, control_m, control_bits = F(1, 3), 2, 40
    quotient_control = middle_histograms(control_h, control_m, control_bits)[:2]
    require(quotient_control == direct_middle_histograms(
        control_h, control_m, control_bits), "unquotiented middle control")
    h, half_grid, bits = F(1, 16), 120, 56
    scale = 1 << bits
    source, target, representatives, digest = middle_histograms(h, half_grid, bits)
    maximum, argmax, thresholds = suffix_window_max(
        source, target, F(scale, 512), F(9 * scale, 32))
    require(maximum < 0, "middle reference polygon sign")
    gaussian_low, gaussian_high = gaussian_constant_bounds(96)
    discrete = gaussian_low * h ** 3 * maximum / scale
    growth = 1 + h ** 2 / 8
    quadrature = h ** 2 * (1 + growth + growth ** 2) / 4
    tail = 3 * growth ** 2 * F(exp_neg_fraction(F(18), 80)[1], 1 << 80) / 6
    cell_upper = discrete + quadrature + tail + EPSILON
    require(cell_upper < -F(1, 128), "middle cell margin")
    grid_peak = F(max(source), scale)
    source_peak = grid_peak + F(61, 100) * (F(7, 128) + EPSILON)
    require(F(exp_neg_fraction(F(18), 80)[1], 1 << 80) < grid_peak,
            "outside-cube peak")
    require(source_peak < F(9, 32), "source peak")
    return {
        "precision_bits": bits,
        "sites": (2 * half_grid + 1) ** 3,
        "explicit_group_orbits": representatives,
        "orbit_stream_sha256": digest,
        "evaluated_thresholds": thresholds,
        "polygon_maximum_units": str(maximum),
        "argmax_over_C": str(argmax / scale),
        "gaussian_constant_lower": str(gaussian_low),
        "gaussian_constant_upper": str(gaussian_high),
        "discrete_adverse_upper": str(discrete),
        "quadrature_error": str(quadrature),
        "tail_error": str(tail),
        "cell_adverse_upper": str(cell_upper),
        "source_peak_upper": str(source_peak),
        "small_unquotiented_control_sites": (2 * control_m + 1) ** 3,
    }


def bareiss_determinant(matrix):
    values = [row[:] for row in matrix]
    sign, previous = 1, 1
    for k in range(len(values) - 1):
        pivot = next((row for row in range(k, len(values)) if values[row][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            values[k], values[pivot] = values[pivot], values[k]
            sign = -sign
        for i in range(k + 1, len(values)):
            for j in range(k + 1, len(values)):
                numerator = (values[i][j] * values[k][k]
                             - values[i][k] * values[k][j])
                require(numerator % previous == 0, "Bareiss divisibility")
                values[i][j] = numerator // previous
        previous = values[k][k]
    return sign * values[-1][-1]


def geometry_audit():
    require(len(X) == len(Y) == 16 and len(set(X)) == len(set(Y)) == 16,
            "sixteen distinct sites")
    losses, source_distances, target_distances = [], [], []
    for first, second in combinations(range(16), 2):
        source = sum((X[first][k] - X[second][k]) ** 2 for k in range(3))
        target = sum((Y[first][k] - Y[second][k]) ** 2 for k in range(3))
        source_distances.append(source)
        target_distances.append(target)
        losses.append(source - target)
    cell_floor = min(losses) - 4 * EPSILON * F(63, 8)
    require(min(losses) == F(127, 2048), "reference pair loss")
    require(cell_floor == F(1, 32), "cell pair-loss floor")
    labels = [1, 2, 3, 4, 7, 10]
    integer_rows = []
    for label in labels:
        row = [int(128 * (X[label][k] - X[0][k])) for k in range(3)]
        row += [int(128 * (Y[label][k] - Y[0][k])) for k in range(3)]
        integer_rows.append(row)
    determinant = F(bareiss_determinant(integer_rows), 128 ** 6)
    require(determinant == F(-250047, 4096), "paired determinant")
    return {
        "reference_pair_loss": str(min(losses)),
        "cell_pair_loss_floor": str(cell_floor),
        "minimum_source_squared_separation": str(min(source_distances)),
        "minimum_target_squared_separation": str(min(target_distances)),
        "paired_rank_six_determinant": str(determinant),
    }


def analytic_tail_audit():
    require(all(sum(centre[k] for centre in X) == 0 for k in range(3))
            and all(sum(centre[k] for centre in Y) == 0 for k in range(3)),
            "reference means")
    require(sum(sum(value * value for value in centre) for centre in X) / 16
            == F(15, 4), "source second moment")
    source_radius = max(sqrt_bounds(sum(value * value for value in centre), 80)[1]
                        for centre in X) + EPSILON
    target_radius = max(sqrt_bounds(sum(value * value for value in centre), 80)[1]
                        for centre in Y) + EPSILON
    require(source_radius < F(9, 4) and target_radius < F(27, 16),
            "cell support radii")
    inner = F(141, 32) + F(9, 2) * EPSILON + EPSILON ** 2 / 2
    require(inner < F(49, 8), "inner-ball threshold")
    require(F(exp_neg_fraction(F(49, 8), 80)[0], 1 << 80) > F(1, 512),
            "low-threshold overlap")

    midpoint_witnesses = []
    for target in Y:
        undamped = tuple(F(64, 63) * value for value in target)
        witness = next(((i, j) for i in range(16) for j in range(i, 16)
                        if tuple((X[i][k] + X[j][k]) / 2 for k in range(3))
                        == undamped), None)
        require(witness is not None, "target midpoint witness")
        midpoint_witnesses.append(witness)
    cross_witnesses = []
    for coordinate in range(3):
        for sign in (-1, 1):
            indices = [i for i, centre in enumerate(X)
                       if centre[coordinate] == sign * F(3, 2)]
            mean = tuple(sum(X[i][k] for i in indices) / len(indices) for k in range(3))
            expected = tuple(sign * F(3, 2) if k == coordinate else F(0)
                             for k in range(3))
            require(mean == expected, "source crosspolytope witness")
            cross_witnesses.append(indices)
    require(F(3, 4) > F(36, 49), "crosspolytope support lower bound")
    require(F(1, 12) > F(4, 49), "core-tetrahedron inradius lower bound")
    require(F(63, 64) * F(2, 7) - EPSILON > 0, "target origin interior")

    patches = make_patches(12)
    support_sum = F(0)
    for patch in patches:
        source_dots = patch["source"][0]
        target_dots = patch["target"][0]
        gap = max(0, max(source_dots) - max(target_dots))
        support_sum += patch["area"] * patch["jacobian_low"] * F(gap, Q)
    mean_support = F(21, 11) * support_sum
    require(mean_support > F(1, 4), "mean support gap")
    radius_x, radius_y = F(9, 4), F(27, 16)
    constant_a, constant_b = F(269, 25), F(277, 200)
    require(F(19, 4) + 2 * radius_x * EPSILON + EPSILON ** 2 + 6 < constant_a,
            "source far-tail constant")
    require(F(11, 4) * F(63, 64) ** 2 + 2 * radius_y * EPSILON
            + EPSILON ** 2 < 2 * constant_b, "target far-tail constant")
    error = (constant_a / 64 * (1 + radius_x / 64) ** 2
             + constant_b / 64 * (1 + radius_y / 64 + constant_b / 64 ** 2) ** 2)
    require(error < F(21, 100), "far-tail error")
    require(F(3, 224) - 2 * EPSILON > 0, "support inclusion")
    return {
        "inner_ball_exponent_upper": str(inner),
        "mean_support_lower": str(mean_support),
        "far_error_at_64": str(error),
        "support_gap_floor": str(F(3, 224) - 2 * EPSILON),
        "target_midpoint_witnesses": len(midpoint_witnesses),
        "source_crosspolytope_witnesses": len(cross_witnesses),
    }


def rejected_radial_mutations():
    patch = make_patches(12)[0]
    rejected = 0
    for record, source_lower, direction in (
        (patch["source"], True, 1),
        (patch["target"], False, -1),
    ):
        root = root_proposal(F(6), record, source_lower) + direction * ROOT_Q // 4
        try:
            check_root(F(6), record, root, source_lower)
        except AssertionError:
            rejected += 1
    require(rejected == 2, "radial mutation rejection")
    return rejected


def exponential_controls():
    checked = 0
    requests = [
        (0, 0), (1, 67), (1, 20), (1, 8), (1, 3),
        (1, 1), (1, 0), (3, 0), (10, 0), (20, 0),
        ((1 << 67) + 1, 67), (3 * (1 << 66) + 17, 67),
    ]
    for numerator, power in requests:
        low, high = exp_neg_dyadic_positive(numerator, power)
        reference_low, reference_high = exp_neg_fraction(
            F(numerator, 1 << power), EXP_BITS + 24)
        require(F(low, EXP_Q) <= F(reference_low, 1 << (EXP_BITS + 24))
                <= F(reference_high, 1 << (EXP_BITS + 24)) <= F(high, EXP_Q),
                "independent exponential control")
        checked += 1
    return checked


def audit():
    manifest = pins()
    cell = json.loads((TARGET / "CELL.json").read_text())
    require(cell["coordinate_radius"] == "1/2048"
            and cell["euclidean_radius_upper"] == "1/1024"
            and cell["coordinate_parameters"] == 96
            and cell["anchored_coordinate_parameters"] == 90
            and cell["frontier_level"] == 2,
            "cell parameters")
    require(cell["source_centers"] == [[str(value) for value in centre] for centre in X]
            and cell["target_centers"] == [[str(value) for value in centre] for centre in Y],
            "cell centres")
    controls = exponential_controls()
    rejected_mutations = rejected_radial_mutations()
    geometry = geometry_audit()
    analytic_tail = analytic_tail_audit()
    radial_bands = [
        radial_band(24, F(1, 16), F(7, 2), F(6)),
        radial_band(12, F(1, 8), F(6), F(64)),
    ]
    require(sum(row["verified_roots"] for row in radial_bands) == 194_280,
            "radial endpoint count")
    middle = middle_audit()
    return {
        "status": "INDEPENDENT_DEEP_FLAP_CELL_REVIEW_PASS",
        "target_commit": manifest["target_commit"],
        "target_graph_ref": manifest["target_graph_ref"],
        "pinned_files": len(manifest["files"]),
        "method": "positive-series reciprocal radial exponentials; tighter exact angular radii; explicit 24-transformation middle orbits",
        "fixed_point_parameters": {
            "angular_bits": D,
            "root_bits": ROOT_BITS,
            "radial_exponential_bits": EXP_BITS,
        },
        "positive_series_exponential_controls": controls,
        "rejected_radial_endpoint_mutations": rejected_mutations,
        "geometry": geometry,
        "analytic_tail": analytic_tail,
        "radial_bands": radial_bands,
        "total_verified_radial_endpoints": 194_280,
        "middle": middle,
        "verdict": "accept the stated fixed-variance all-threshold 96-coordinate cell; unrestricted majorisation and all-variance claims remain open",
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
