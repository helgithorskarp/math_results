#!/usr/bin/env python3
"""Independent exact controls for the two-rigid-body transfer theorem.

This checker imports no target code.  It pins the reviewed commit, verifies
the barycentric contraction through the pair-energy decomposition, exhausts
independent posterior-grid roundings, checks the scalar interaction and
clipping orientations, and rederives the rational small-variance budget.
It does not assert that an adverse joint-level contact has been found.
"""

from fractions import Fraction as Q
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TARGET_COMMIT = "036e7355fd2481a562ece50be4cbab5889f41c25"
TARGET_DIR = "probability/gaussian_two_body_contact_transfer"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def git_bytes(commit, path):
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout


def pin_sources():
    records = json.loads((HERE / "TARGET_SOURCES.json").read_text())
    for record in records:
        raw = git_bytes(record["commit"], record["path"])
        require(hashlib.sha256(raw).hexdigest() == record["sha256"],
                f"reviewed source drift: {record['path']}")
    return records


def compositions(total, parts, positive=False):
    if parts == 1:
        if total >= (1 if positive else 0):
            yield (total,)
        return
    start = 1 if positive else 0
    reserve = parts - 1 if positive else 0
    for first in range(start, total - reserve + 1):
        for tail in compositions(total - first, parts - 1, positive):
            yield (first,) + tail


def simplex_points(parts, max_denominator):
    points = set()
    for denominator in range(1, max_denominator + 1):
        for counts in compositions(denominator, parts):
            points.add(tuple(Q(value, denominator) for value in counts))
    return sorted(points)


def point(raw):
    return tuple(Q(coordinate) for coordinate in raw)


def squared_distance(left, right):
    return sum((a - b) ** 2 for a, b in zip(left, right))


def barycentre(points, weights):
    require(len(points) == len(weights) and sum(weights) == 1,
            "invalid barycentre data")
    return tuple(sum(weight * p[coordinate]
                     for weight, p in zip(weights, points))
                 for coordinate in range(3))


def pair_variance(points, weights):
    return sum(weights[i] * weights[j] * squared_distance(points[i], points[j])
               for i in range(len(points)) for j in range(len(points))) / 2


def cross_energy(left, right, left_weights, right_weights):
    return sum(left_weights[i] * right_weights[j]
               * squared_distance(left[i], right[j])
               for i in range(len(left)) for j in range(len(right)))


def geometry_controls(source_data):
    source_a = [point(row) for row in source_data["source_A"]]
    source_b = [point(row) for row in source_data["source_B"]]
    target_a = [point(row) for row in source_data["target_A"]]
    target_b = [point(row) for row in source_data["target_B"]]

    for source, target in ((source_a, target_a), (source_b, target_b)):
        for i in range(len(source)):
            for j in range(len(source)):
                require(squared_distance(source[i], source[j])
                        == squared_distance(target[i], target[j]),
                        "component is not rigid")

    losses = [[squared_distance(a, b) - squared_distance(qa, qb)
               for b, qb in zip(source_b, target_b)]
              for a, qa in zip(source_a, target_a)]
    require(all(loss >= 0 for row in losses for loss in row),
            "fixture is not a contraction")

    weights_a = simplex_points(len(source_a), 4)
    weights_b = simplex_points(len(source_b), 5)
    variance_checks = 0
    for points, targets, weights_list in (
            (source_a, target_a, weights_a),
            (source_b, target_b, weights_b)):
        for weights in weights_list:
            centre = barycentre(points, weights)
            direct = sum(weight * squared_distance(p, centre)
                         for weight, p in zip(weights, points))
            pairwise = pair_variance(points, weights)
            require(direct == pairwise == pair_variance(targets, weights),
                    "rigid barycentric variance identity")
            variance_checks += 1

    cross_checks = 0
    for left_weights in weights_a:
        source_left_variance = pair_variance(source_a, left_weights)
        target_left_variance = pair_variance(target_a, left_weights)
        for right_weights in weights_b:
            source_right_variance = pair_variance(source_b, right_weights)
            target_right_variance = pair_variance(target_b, right_weights)
            source_distance = squared_distance(
                barycentre(source_a, left_weights),
                barycentre(source_b, right_weights))
            target_distance = squared_distance(
                barycentre(target_a, left_weights),
                barycentre(target_b, right_weights))
            # E|A-B|^2 = |EA-EB|^2 + Var(A) + Var(B).
            require(cross_energy(source_a, source_b, left_weights, right_weights)
                    == source_distance + source_left_variance + source_right_variance,
                    "source pair-energy decomposition")
            require(cross_energy(target_a, target_b, left_weights, right_weights)
                    == target_distance + target_left_variance + target_right_variance,
                    "target pair-energy decomposition")
            weighted_loss = sum(left_weights[i] * right_weights[j] * losses[i][j]
                                for i in range(4) for j in range(4))
            require(source_distance - target_distance == weighted_loss >= 0,
                    "barycentric cross-loss identity")
            cross_checks += 1

    return {
        "component_a_simplex_labels": len(weights_a),
        "component_b_simplex_labels": len(weights_b),
        "rigid_variance_checks": variance_checks,
        "barycentric_cross_checks": cross_checks,
        "strict_original_cross_pairs": sum(loss > 0 for row in losses for loss in row),
    }


def positive_part(value):
    return max(value, Q(0))


def interaction_controls():
    values = [Q(value, 4) for value in range(13)]
    checks = 0
    for u, v, h in itertools.product(values, repeat=3):
        left = (positive_part(u + v - h)
                - positive_part(u - h) - positive_part(v - h))
        # Length of {0<t<h: t<u and h-t<v}.
        right = positive_part(min(h, u) - max(Q(0), h - v))
        require(left == right, "two-component hinge interaction orientation")
        checks += 1
    return checks


def posterior_grid_controls():
    checks = 0
    worst_scaled_l1 = Q(0)
    worst_scaled_chi = Q(0)
    for parts in range(2, 6):
        for denominator in range(parts, 14):
            for counts in compositions(denominator, parts, positive=True):
                posterior = tuple(Q(value, denominator) for value in counts)
                tau = min(posterior)
                for grid_denominator in (3, 7, 13, 23):
                    floors = []
                    for value in posterior[:-1]:
                        scaled = value * grid_denominator
                        floors.append(scaled.numerator // scaled.denominator)
                    rounded = tuple(Q(value, grid_denominator) for value in
                                    floors + [grid_denominator - sum(floors)])
                    require(min(rounded) >= 0 and sum(rounded) == 1,
                            "simplex rounding left the simplex")
                    l1 = sum(abs(a - b) for a, b in zip(rounded, posterior))
                    chi = sum((a - b) ** 2 / b
                              for a, b in zip(rounded, posterior))
                    require(l1 <= Q(2 * parts, grid_denominator),
                            "posterior L1 grid bound")
                    require(chi <= l1 * l1 / tau
                            <= Q(4 * parts * parts,
                                 grid_denominator * grid_denominator) / tau,
                            "posterior chi-square/KL majorant")
                    worst_scaled_l1 = max(
                        worst_scaled_l1,
                        l1 * grid_denominator / (2 * parts))
                    worst_scaled_chi = max(
                        worst_scaled_chi,
                        chi * grid_denominator * grid_denominator * tau
                        / (4 * parts * parts))
                    checks += 1
    return checks, worst_scaled_l1, worst_scaled_chi


def clipping_controls():
    # Exact finite-space version of H_g(h)-H_f(h)=h(M_f-M_g).
    checks = 0
    for cells in (2, 3, 4):
        for total in range(1, 7):
            profiles = list(compositions(total, cells))
            for raw_f in profiles:
                f = tuple(map(Q, raw_f))
                for raw_g in profiles:
                    g = tuple(map(Q, raw_g))
                    for h in (Q(1, 3), Q(1), Q(5, 2)):
                        hinge_difference = sum(positive_part(value - h) for value in g)
                        hinge_difference -= sum(positive_part(value - h) for value in f)
                        clipped_f = sum(min(value / h, 1) for value in f)
                        clipped_g = sum(min(value / h, 1) for value in g)
                        require(hinge_difference == h * (clipped_f - clipped_g),
                                "clipped-integral hinge orientation")
                        checks += 1
    return checks


def tail_budget_controls():
    checks = 0
    state = []
    for delta in (Q(1, 4096), Q(2, 9), Q(5), Q(1000)):
        for radii in ((Q(0),), (Q(1, 7), Q(11, 5)),
                      (Q(2), Q(3, 2), Q(9, 4), Q(5))):
            number = len(radii)
            total = sum(radii)
            epsilon = min(Q(1), delta / (32 * total + 64 * number))
            rational_majorant = 16 * epsilon * total + 32 * number * epsilon
            require(0 < epsilon <= 1 and rational_majorant <= delta / 2,
                    "small-variance source-tail budget")
            state.append((str(delta), tuple(map(str, radii)), str(epsilon),
                          str(rational_majorant)))
            checks += 1
    return checks, state


def audit():
    records = pin_sources()
    raw_inputs = git_bytes(TARGET_COMMIT, f"{TARGET_DIR}/INPUTS.json")
    geometry = geometry_controls(json.loads(raw_inputs))
    interaction_checks = interaction_controls()
    grid_checks, worst_l1, worst_chi = posterior_grid_controls()
    clip_checks = clipping_controls()
    tail_checks, tail_state = tail_budget_controls()

    state = {
        "geometry": geometry,
        "interaction_checks": interaction_checks,
        "posterior_grid_checks": grid_checks,
        "worst_scaled_l1": str(worst_l1),
        "worst_scaled_chi": str(worst_chi),
        "clipping_checks": clip_checks,
        "tail_state": tail_state,
    }
    state_hash = hashlib.sha256(
        json.dumps(state, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "status": "INDEPENDENT_TWO_BODY_TRANSFER_REVIEW_PASS",
        "target_artifact": "bafkreid62eenvh4wovui3x5dujdjcpynmv7pv4kgi7d5b3hfkv66t624da",
        "target_commit": TARGET_COMMIT,
        "source_pins": len(records),
        **geometry,
        "hinge_interaction_checks": interaction_checks,
        "posterior_grid_checks": grid_checks,
        "clipped_hinge_checks": clip_checks,
        "conditional_tail_budget_checks": tail_checks,
        "worst_normalized_l1_bound": str(worst_l1),
        "worst_normalized_chi_bound": str(worst_chi),
        "adverse_contact_supplied": False,
        "gaussian_counterexample_certified": False,
        "exact_state_sha256": state_hash,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true",
                        help="emit a fresh record without checking EXPECTED.json")
    args = parser.parse_args()
    result = audit()
    if not args.emit:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        require(result == expected, "expected independent record mismatch")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
