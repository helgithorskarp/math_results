#!/usr/bin/env python3
"""Independent exact checks for the paired-cubature Gaussian frontier.

This standard-library checker imports no submitted producer or expected
record.  It uses a separately written exact affine-dependence eliminator,
checks both marginal moment systems from their definitions, and audits the
tail, atom, rounding, and error constants with ``Fraction`` arithmetic.
The finite checks are implementation evidence; the universal analytic proof
is recorded separately in REVIEW.md.
"""

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from math import comb, factorial, isqrt
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(t, a):
    return tuple(t * x for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm2(a):
    return dot(a, a)


def powers_through(degree):
    return [(a, b, total - a - b)
            for total in range(degree + 1)
            for a in range(total + 1)
            for b in range(total - a + 1)]


def monomial(point, alpha):
    value = Q(1)
    for coordinate, exponent in zip(point, alpha):
        value *= coordinate ** exponent
    return value


def feature(point, image, degree):
    nonconstant = powers_through(degree)[1:]
    return ((Q(1),)
            + tuple(monomial(point, a) for a in nonconstant)
            + tuple(monomial(image, a) for a in nonconstant))


def rightmost_kernel(matrix):
    """One exact kernel vector, pivoting bottom-up and choosing the last free column."""
    rows = [list(map(Q, row)) for row in matrix]
    height = len(rows)
    width = len(rows[0])
    pivot_rows = []
    pivot_columns = []
    row = height - 1
    for column in range(width - 1, -1, -1):
        pivot = next((r for r in range(row, -1, -1) if rows[r][column]), None)
        if pivot is None:
            continue
        rows[row], rows[pivot] = rows[pivot], rows[row]
        divisor = rows[row][column]
        rows[row] = [x / divisor for x in rows[row]]
        for r in range(height):
            if r != row and rows[r][column]:
                multiple = rows[r][column]
                rows[r] = [x - multiple * y for x, y in zip(rows[r], rows[row])]
        pivot_rows.append(row)
        pivot_columns.append(column)
        row -= 1
        if row < 0:
            break
    free = next((c for c in range(width) if c not in pivot_columns), None)
    require(free is not None, "matrix unexpectedly has full column rank")
    vector = [Q(0)] * width
    vector[free] = Q(1)
    for r, c in zip(pivot_rows, pivot_columns):
        vector[c] = -rows[r][free]
    require(any(vector), "zero kernel vector")
    require(all(sum(matrix[r][c] * vector[c] for c in range(width)) == 0
                for r in range(height)), "invalid exact kernel vector")
    return vector


def compress(points, images, weights, degree):
    require(len(points) == len(images) == len(weights) > 0, "input lengths")
    weights = list(map(Q, weights))
    require(all(w >= 0 for w in weights) and sum(weights) == 1, "input weights")
    require(all(norm2(sub(images[i], images[j])) <= norm2(sub(points[i], points[j]))
                for i in range(len(points)) for j in range(i)), "not a contraction")
    columns = [feature(x, y, degree) for x, y in zip(points, images)]
    cap = 2 * comb(degree + 3, 3) - 1
    require(len(columns[0]) == cap, "feature count")
    active = [i for i, w in enumerate(weights) if w]
    eliminations = 0
    while len(active) > cap:
        labels = active[-(cap + 1):]
        matrix = [[columns[c][r] for c in labels] for r in range(cap)]
        direction = rightmost_kernel(matrix)
        # The constant row makes the nonzero direction sum to zero.
        require(any(t > 0 for t in direction) and any(t < 0 for t in direction),
                "affine dependence lacks both signs")
        step = min(weights[i] / t for i, t in zip(labels, direction) if t > 0)
        for i, t in zip(labels, direction):
            weights[i] -= step * t
            require(weights[i] >= 0, "negative output weight")
        newer = [i for i in active if weights[i] > 0]
        require(len(newer) < len(active), "no support elimination")
        active = newer
        eliminations += 1
    return active, [weights[i] for i in active], eliminations


def moment(point, alpha, center=None):
    return monomial(point if center is None else sub(point, center), alpha)


def verify_cubature(points, images, weights, ids, output_weights, degree):
    require(len(ids) == len(output_weights) <= 2 * comb(degree + 3, 3) - 1,
            "support cap")
    require(len(set(ids)) == len(ids), "duplicate retained label")
    require(all(w > 0 for w in output_weights) and sum(output_weights) == 1,
            "output probability")
    raw_checks = 0
    centered_checks = 0
    centers = ((Q(2, 7), Q(-1, 5), Q(3, 11)),
               (Q(-1, 9), Q(4, 13), Q(2, 5)))
    for sites, center in zip((points, images), centers):
        for alpha in powers_through(degree):
            before = sum(w * moment(x, alpha) for w, x in zip(weights, sites))
            after = sum(w * moment(sites[i], alpha)
                        for i, w in zip(ids, output_weights))
            require(before == after, "raw marginal moment mismatch")
            raw_checks += 1
            before_c = sum(w * moment(x, alpha, center) for w, x in zip(weights, sites))
            after_c = sum(w * moment(sites[i], alpha, center)
                          for i, w in zip(ids, output_weights))
            require(before_c == after_c, "translated marginal moment mismatch")
            centered_checks += 1
    return raw_checks, centered_checks


def ordered_pair_loss(points, images, weights):
    return sum(weights[i] * weights[j]
               * (norm2(sub(points[i], points[j])) - norm2(sub(images[i], images[j])))
               for i in range(len(points)) for j in range(len(points)))


def kernel_cancellations(points, images, weights, ids, output_weights, degree):
    signed = [-w for w in weights]
    for i, w in zip(ids, output_weights):
        signed[i] += w
    checks = 0
    for sites in (points, images):
        for power in range(degree + 1):
            coefficient = sum(signed[i] * signed[j] * dot(sites[i], sites[j]) ** power
                              for i in range(len(sites)) for j in range(len(sites)))
            require(coefficient == 0, "Gaussian kernel coefficient did not cancel")
            checks += 1
    return checks


def exponential_tail_upper(a, degree):
    a = Q(a)
    require(0 <= a < degree + 2, "tail ratio")
    return a ** (degree + 1) / factorial(degree + 1) / (1 - a / (degree + 2))


def budget(k):
    require(type(k) is int and k >= 1, "positive k")
    ell = (k - 1).bit_length()
    unit_degree = 2 * ell + 3
    unit_atoms = k ** 3 * (2 * comb(unit_degree + 3, 3) - 1)
    width = isqrt(ell + 1)
    cells = (k + width - 1) // width
    wide_degree = 4 * ell + 8
    wide_atoms = cells ** 3 * (2 * comb(wide_degree + 3, 3) - 1)
    atoms = min(unit_atoms, wide_atoms)
    return ell, width, unit_degree, wide_degree, unit_atoms, wide_atoms, atoms


def nearest_integer(value):
    lower = value.numerator // value.denominator
    return lower if value - lower < Q(1, 2) else lower + 1


def round_instance(k, points, images, weights):
    """Independent implementation of the updated finite rational handoff."""
    ell, width, pu, pw, unit, wide, cap = budget(k)
    del ell, width, pu, pw, unit, wide
    require(len(points) <= cap and points[0] == images[0] == (Q(0),) * 3,
            "compact input contract")
    require(all(norm2(x) <= 4 * k * k for x in points + images), "compact radius")
    merge_radius = Q(1, 4 * k)
    representatives = [0]
    for i in range(1, len(points)):
        if all(norm2(sub(points[i], points[j])) > merge_radius ** 2
               for j in representatives):
            representatives.append(i)
    merged_weights = [Q(0)] * len(representatives)
    for i, w in enumerate(weights):
        slot = next(s for s, j in enumerate(representatives)
                    if norm2(sub(points[i], points[j])) <= merge_radius ** 2)
        j = representatives[slot]
        require(norm2(sub(images[i], images[j])) <= merge_radius ** 2,
                "target merge displacement")
        merged_weights[slot] += w
    coordinate_denominator = 256 * k ** 3
    weight_denominator = 4 * k * cap
    expansion = 1 + Q(1, 8 * k * k)
    xx = [tuple(nearest_integer(coordinate_denominator * expansion * a)
                for a in points[i]) for i in representatives]
    yy = [tuple(nearest_integer(coordinate_denominator * a)
                for a in images[i]) for i in representatives]
    nn = [(weight_denominator * w).numerator // (weight_denominator * w).denominator
          for w in merged_weights]
    missing = weight_denominator - sum(nn)
    remainders = [weight_denominator * w - n for w, n in zip(merged_weights, nn)]
    order = sorted(range(len(nn)), key=lambda i: (-remainders[i], i))
    require(0 <= missing < len(nn), "largest-remainder allocation")
    for i in order[:missing]:
        nn[i] += 1
    require(sum(nn) == weight_denominator and all(n >= 0 for n in nn), "integer weights")
    weight_error = sum(abs(w - Q(n, weight_denominator))
                       for w, n in zip(merged_weights, nn))
    require(weight_error <= Q(len(nn), weight_denominator) <= Q(1, 4 * k),
            "weight error")
    losses = [norm2(sub(xx[i], xx[j])) - norm2(sub(yy[i], yy[j]))
              for i in range(len(xx)) for j in range(i)]
    require(all(loss >= 256 * k * k for loss in losses), "integer pair margin")
    expected_loss = sum(Q(nn[i] * nn[j], weight_denominator ** 2 * coordinate_denominator ** 2)
                        * (norm2(sub(xx[i], xx[j])) - norm2(sub(yy[i], yy[j])))
                        for i in range(len(xx)) for j in range(len(xx)))
    if sum(n > 0 for n in nn) >= 2:
        require(expected_loss >= Q(1, 2048 * k ** 6 * cap ** 2), "pair-loss floor")
    else:
        require(expected_loss == 0, "point-law equality")
    return {
        "representatives": len(representatives),
        "minimum_integer_margin": min(losses) if losses else None,
        "weight_l1_error": str(weight_error),
        "positive_output_weights": sum(n > 0 for n in nn),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    # A nonlinear coordinate fold on a non-symmetric rational grid.
    values = tuple(Q(x, 16) for x in (-7, -1, 3, 5))
    points = list(product(values, repeat=3))
    images = [(abs(x) / 2, abs(y) / 3, z / 4) for x, y, z in points]
    denominator = sum((i + 1) ** 2 for i in range(len(points)))
    weights = [Q((i + 1) ** 2, denominator) for i in range(len(points))]
    original_loss = ordered_pair_loss(points, images, weights)

    support_sizes = []
    elimination_counts = []
    raw_moment_checks = 0
    centered_moment_checks = 0
    cancellation_checks = 0
    pair_loss_checks = 0
    rounding = []
    cubature_stream = sha256()
    for degree in (1, 2, 3):
        ids, output_weights, eliminations = compress(points, images, weights, degree)
        raw, centered = verify_cubature(
            points, images, weights, ids, output_weights, degree)
        cancellation_checks += kernel_cancellations(
            points, images, weights, ids, output_weights, degree)
        if degree >= 2:
            compressed_loss = ordered_pair_loss(
                [points[i] for i in ids], [images[i] for i in ids], output_weights)
            require(compressed_loss == original_loss, "ordered pair loss changed")
            pair_loss_checks += 1
        anchor_x, anchor_y = points[ids[0]], images[ids[0]]
        shifted_x = [sub(points[i], anchor_x) for i in ids]
        shifted_y = [sub(images[i], anchor_y) for i in ids]
        rounding.append(round_instance(1, shifted_x, shifted_y, output_weights))
        support_sizes.append(len(ids))
        elimination_counts.append(eliminations)
        raw_moment_checks += raw
        centered_moment_checks += centered
        cubature_stream.update((json.dumps({
            "degree": degree,
            "indices": ids,
            "weights": list(map(str, output_weights)),
        }, sort_keys=True, separators=(",", ":")) + "\n").encode())

    # Exact proof constants and a dense transition audit for the schedules.
    require(exponential_tail_upper(Q(3, 4), 3) == Q(135, 8704) < Q(1, 64),
            "unit schedule base")
    require(Q(16, 13) * Q(9, 16) ** 9 < Q(1, 64), "wide schedule base")
    require(Q(9, 16) ** 4 < Q(1, 4), "wide schedule ratio")
    require(Q(11, 4) + Q(2, 3) + Q(161, 256) == Q(3107, 768),
            "frontier error composition")
    require(Q(1, 2) + Q(3107, 768 * 9) == Q(6563, 6912) < 1,
            "epsilon handoff")

    schedule_stream = sha256()
    unit_winners = 0
    wide_winners = 0
    atom_improvements = 0
    maximum_k = 8192
    for k in range(1, maximum_k + 1):
        ell, width, pu, pw, unit, wide, atoms = budget(k)
        unit_tail = exponential_tail_upper(Q(3, 4), pu)
        wide_tail = exponential_tail_upper(Q(3 * width * width, 4), pw)
        require(unit_tail < Q(1, 64 * k * k), "unit tail schedule")
        require(wide_tail < Q(1, 64 * k * k), "wide tail schedule")
        require(4 * width * width >= ell + 1, "width lower bound")
        require((k + width - 1) // width <= Q(2 * k, width), "cell-count bound")
        require(4 * ell + 11 <= 11 * (ell + 1), "degree linearization")
        require((3 * atoms) ** 2 <= 85184 ** 2 * k ** 6 * (ell + 1) ** 3,
                "near-cubic asymptotic envelope")
        unit_winners += unit <= wide
        wide_winners += wide < unit
        atom_improvements += atoms < k ** 6
        schedule_stream.update((f"{k}:{ell}:{width}:{pu}:{pw}:{unit}:{wide}:{atoms}:"
                                f"{unit_tail}:{wide_tail}\n").encode())

    result = {
        "status": "INDEPENDENT_PAIRED_CUBATURE_REVIEW_PASS",
        "imports_submitted_code_or_expected_output": False,
        "input_atoms": len(points),
        "support_sizes_degrees_1_2_3": support_sizes,
        "elimination_counts": elimination_counts,
        "raw_moment_equalities": raw_moment_checks,
        "translated_moment_equalities": centered_moment_checks,
        "kernel_coefficient_cancellations": cancellation_checks,
        "pair_loss_equalities": pair_loss_checks,
        "rounding_controls": rounding,
        "cubature_stream_sha256": cubature_stream.hexdigest(),
        "schedule_k_range": [1, maximum_k],
        "unit_schedule_winners": unit_winners,
        "wide_schedule_winners": wide_winners,
        "atom_budget_improvements_over_k6": atom_improvements,
        "schedule_stream_sha256": schedule_stream.hexdigest(),
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check:
        expected = Path(__file__).with_name("EXPECTED.json").read_text()
        require(encoded == expected, "review expected-output mismatch")
    print(encoded, end="")


if __name__ == "__main__":
    main()
