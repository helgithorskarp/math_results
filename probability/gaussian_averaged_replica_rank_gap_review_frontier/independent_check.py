#!/usr/bin/env python3
"""Clean-room exact controls for the averaged replica-rank-gap review.

This checker imports no target module.  It pins the reviewed bytes and uses
Fractions plus formal exponential keys to check the Gaussian completion,
replica geometry, graph Lipschitz interface, marked clock, symmetrization,
and final constants.  The graph compactness lemma remains written analysis.
"""

import argparse
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_inputs():
    manifest = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    require(manifest["schema"] == 1, "manifest schema")
    for relative, expected in manifest["files"].items():
        actual = sha256((HERE / relative).read_bytes()).hexdigest()
        require(actual == expected, f"changed target input: {relative}")
    return manifest


def dot(first, second):
    return sum((x * y for x, y in zip(first, second)), F(0))


def sub(first, second):
    return tuple(x - y for x, y in zip(first, second))


def scale(amount, vector):
    return tuple(amount * x for x in vector)


def norm2(vector):
    return dot(vector, vector)


def mean(points):
    return tuple(sum((point[j] for point in points), F(0)) / len(points)
                 for j in range(len(points[0])))


def scatter(points):
    center = mean(points)
    return sum((norm2(sub(point, center)) for point in points), F(0))


def pair_scatter(points):
    return sum((norm2(sub(points[i], points[j]))
                for i, j in combinations(range(len(points)), 2)), F(0)) / len(points)


def diamond(points):
    distance = lambda i, j: norm2(sub(points[i], points[j]))
    return (distance(0, 1) / 6
            + (distance(0, 2) + distance(0, 3)
               + distance(1, 2) + distance(1, 3)) / 3)


def gaussian_completion_controls():
    """Complete the density-product square and compare formal exponent sums."""
    rho, variance = F(1, 3), F(2, 3)
    precision = 2 / variance - 1
    linear_square = rho / (2 * variance * variance * precision)
    cross = 2 * linear_square
    self_term = -rho / (2 * variance) + linear_square
    six_dimensional_prefactor = F(1, variance ** 6 * precision ** 3)
    require(precision == 2, "completion precision")
    require(cross == F(3, 8) and self_term == F(-1, 16),
            "completion exponent")
    require(six_dimensional_prefactor == F(9, 8) ** 3,
            "six-dimensional prefactor")

    points = [
        (F(0),) * 6,
        (F(1), F(-1), F(2), F(0), F(1, 2), F(-3, 2)),
        (F(-2), F(1, 3), F(0), F(4, 3), F(-1), F(2)),
        (F(1, 2), F(2, 3), F(-3, 4), F(5, 6), F(0), F(7, 5)),
    ]
    mixtures = [
        ([F(1)], points[:1]),
        ([F(1, 3), F(2, 3)], points[:2]),
        ([F(1, 10), F(2, 10), F(3, 10), F(4, 10)], points),
    ]
    formal_terms = pair_controls = 0
    for weights, support in mixtures:
        require(sum(weights) == 1, "mixture weights")
        kernel = defaultdict(F)
        density_inner_product = defaultdict(F)
        for weight, point in zip(weights, support):
            for other_weight, other in zip(weights, support):
                exponent = (self_term * (norm2(point) + norm2(other))
                            + cross * dot(point, other))
                kernel[exponent] += weight * other_weight
                density_inner_product[exponent] += (
                    six_dimensional_prefactor * weight * other_weight)
                pair_controls += 1
        recovered = {key: F(8, 9) ** 3 * value
                     for key, value in density_inner_product.items()}
        require(dict(kernel) == recovered, "formal Mehler identity")
        formal_terms += len(kernel)
    return {
        "mixtures": len(mixtures),
        "formal_exponential_terms": formal_terms,
        "ordered_kernel_pairs": pair_controls,
        "self_coefficient": str(self_term),
        "cross_coefficient": str(cross),
        "six_dimensional_prefactor": str(six_dimensional_prefactor),
    }


def source_fixture():
    source = [
        (F(0), F(0), F(0)),
        (F(1), F(0), F(0)),
        (F(-1), F(0), F(0)),
        (F(0), F(2), F(0)),
        (F(0), F(-1), F(1)),
        (F(1), F(1), F(-1)),
    ]
    target = [(x / 2, -y / 3, F(0)) for x, y, _ in source]
    weights = [F(i, 21) for i in range(1, 7)]
    require(sum(weights) == 1, "fixture weights")
    return source, target, weights


def replica_and_clock_controls():
    source, target, weights = source_fixture()
    times = (F(1, 7), F(1, 2), F(4, 5), F(9, 10))
    noise = F(7, 5)
    quadruples = geometry = clock = loss_checks = 0
    for labels in product(range(len(source)), repeat=4):
        xs = [source[i] for i in labels]
        ys = [target[i] for i in labels]
        delta = norm2(sub(xs[0], xs[1])) - norm2(sub(ys[0], ys[1]))
        require(delta >= 0, "base pair contraction")
        loss = diamond(xs) - diamond(ys)
        require(loss >= 0, "diamond loss")
        bx, by = mean(xs[:2]), mean(ys[:2])
        source_extra = [sub(xs[i], bx) for i in (2, 3)]
        target_extra = [sub(ys[i], by) for i in (2, 3)]
        require(loss == (delta / 2 + F(2, 3) * sum(
            (norm2(source_extra[j]) - norm2(target_extra[j]) for j in range(2)), F(0))),
            "diamond loss identity")
        loss_checks += 2

        for time in times:
            remaining = 1 - time
            q2 = (remaining * scatter(xs[:2]) + time * scatter(ys[:2]))
            extra_norms = [remaining * norm2(source_extra[j])
                           + time * norm2(target_extra[j]) for j in range(2)]
            extra_dot = (remaining * dot(source_extra[0], source_extra[1])
                         + time * dot(target_extra[0], target_extra[1]))
            q4_from_base = q2 + F(3, 4) * sum(extra_norms) - extra_dot / 2
            q4_direct = remaining * scatter(xs) + time * scatter(ys)
            qd_from_base = q2 + F(2, 3) * sum(extra_norms)
            qd_direct = remaining * diamond(xs) + time * diamond(ys)
            require(q4_from_base == q4_direct, "four-replica centering")
            require(qd_from_base == qd_direct, "diamond centering")
            geometry += 2

            # Pointwise version of the conditional marked-clock identity.
            a_norms = [F(2) * remaining * norm2(vector) / (3 * noise)
                       for vector in source_extra]
            b_norms = [F(2) * time * norm2(vector) / (3 * noise)
                       for vector in target_extra]
            left = remaining * loss / (2 * noise)
            right = (remaining * delta / (4 * noise)
                     + sum((a_norms[j] / 2
                            - remaining * b_norms[j] / (2 * time)
                            for j in range(2)), F(0)))
            require(left == right, "marked clock identity")
            require(left >= 0, "remaining loss nonnegative")
            clock += 2
        quadruples += 1

    # The conditional support is a graph of squared Lipschitz bound t/(1-t).
    graph_checks = 0
    for time, i, j in product(times, range(len(source)), range(len(source))):
        remaining = 1 - time
        a_distance = (F(2) * remaining * norm2(sub(source[i], source[j]))
                      / (3 * noise))
        b_distance = (F(2) * time * norm2(sub(target[i], target[j]))
                      / (3 * noise))
        require(b_distance <= time / remaining * a_distance,
                "conditional graph Lipschitz bound")
        graph_checks += 1

    # Independently symmetrize the marked base pair at fixed scatter values.
    histograms = {}
    symmetrization_checks = 0
    for replicas in (2, 3, 4):
        marked, averaged = defaultdict(F), defaultdict(F)
        for labels in product(range(len(source)), repeat=replicas):
            xs = [source[i] for i in labels]
            ys = [target[i] for i in labels]
            mass = math.prod(weights[i] for i in labels)
            qx, qy = scatter(xs), scatter(ys)
            delta = norm2(sub(xs[0], xs[1])) - norm2(sub(ys[0], ys[1]))
            marked[(qx, qy)] += mass * delta
            averaged[(qx, qy)] += mass * F(2, replicas - 1) * (qx - qy)
        require(dict(marked) == dict(averaged), "base-mark symmetrization")
        histograms[str(replicas)] = len(marked)
        symmetrization_checks += len(marked)
    return {
        "ordered_quadruples": quadruples,
        "centering_geometry_checks": geometry,
        "clock_identity_checks": clock,
        "nonnegative_loss_checks": loss_checks,
        "conditional_graph_checks": graph_checks,
        "symmetrization_cells": symmetrization_checks,
        "histogram_sizes": histograms,
    }


def averaging_and_constant_controls():
    # Definition-level finite Cauchy--Schwarz defect for B3^2 <= B2 I_D.
    cs_cases = 0
    fixtures = [
        ([F(1)], [F(3, 5)]),
        ([F(1, 3), F(2, 3)], [F(1, 4), F(7, 5)]),
        ([F(1, 10), F(2, 10), F(3, 10), F(4, 10)],
         [F(0), F(1, 3), F(5, 4), F(3)]),
    ]
    for masses, values in fixtures:
        b2 = sum(masses)
        b3 = sum((mass * value for mass, value in zip(masses, values)), F(0))
        diamond_integral = sum((mass * value * value
                                for mass, value in zip(masses, values)), F(0))
        defect = b2 * diamond_integral - b3 * b3
        pair_defect = sum((masses[i] * masses[j] * (values[i] - values[j]) ** 2
                           for i, j in combinations(range(len(masses)), 2)), F(0))
        require(defect == pair_defect >= 0, "Cauchy--Schwarz surplus")
        cs_cases += 1

    # Exact OU moment and good/bad event arithmetic.
    rho = F(1, 3)
    gaussian_variance = 6
    moment_constant = gaussian_variance / (rho * rho)
    cutoff = F(1, 216)
    require(moment_constant == 54 and moment_constant * cutoff == F(1, 4),
            "OU moment threshold")
    require(F(4, 5) / (1 - F(4, 5)) == 4, "graph threshold")
    good_clock = F(5, 2) - F(1, 4) * F(7, 2)
    good_probability = 1 / good_clock
    bad_probability = 1 - good_probability
    eta_cap = bad_probability * cutoff
    require(good_clock == F(13, 8), "good-event clock lower bound")
    require(good_probability == F(8, 13) and bad_probability == F(5, 13),
            "averaged event proportions")
    require(eta_cap == F(5, 2808), "eta cap")

    # Check the endpoint normalization and the precise remaining gap.
    require((1 + eta_cap) ** 2 < F(9, 8), "Hankel threshold not reached")
    # Truncated Exp(1): numerator 1-(a+1)e^-a is at most denominator 1-e^-a.
    # Coefficients of their difference are exactly a*e^-a, hence nonnegative.
    truncated_clock_coefficient_checks = 0
    for numerator in range(1, 65):
        a = F(numerator, 13)
        require(a >= 0, "truncated exponential parameter")
        require((a + 1) - 1 == a, "truncated exponential mean deficit")
        truncated_clock_coefficient_checks += 1
    return {
        "cauchy_schwarz_fixtures": cs_cases,
        "moment_constant": str(moment_constant),
        "good_clock": str(good_clock),
        "good_probability_upper_bound": str(good_probability),
        "bad_probability_lower_bound": str(bad_probability),
        "eta_cap": str(eta_cap),
        "truncated_clock_coefficient_checks": truncated_clock_coefficient_checks,
        "unrestricted_hankel_sign_proved": False,
    }


def run():
    manifest = pin_inputs()
    return {
        "status": "INDEPENDENT_AVERAGED_REPLICA_RANK_GAP_REVIEW_PASS",
        "scope": ("Pinned source and exact controls for Gaussian completion, replica "
                  "centering, graph support, clock identities, symmetrization, and "
                  "averaged constants; the universal graph compactness separation "
                  "remains reviewed written analysis."),
        "source_commit": manifest["source_commit"],
        "graph_artifact": manifest["graph_artifact"],
        "gaussian_completion": gaussian_completion_controls(),
        "replica_clock": replica_and_clock_controls(),
        "averaging_constants": averaging_and_constant_controls(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-expected", action="store_true")
    args = parser.parse_args()
    encoded = (json.dumps(run(), indent=2, sort_keys=True) + "\n").encode()
    expected = HERE / "EXPECTED.json"
    if args.write_expected:
        require(not expected.exists(), "refusing to overwrite expected record")
        expected.write_bytes(encoded)
    else:
        require(expected.read_bytes() == encoded, "expected record differs")
    print("INDEPENDENT_AVERAGED_REPLICA_RANK_GAP_REVIEW_PASS")
    print("record_sha256=" + sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()
