#!/usr/bin/env python3
"""Independent exact audit of the near-collinear equal-ball theorem.

CPython 3.11+, standard library only.  This file does not import the target
checker.  It uses an axial-envelope derivation of the expanded-lens maximum,
exhaustive exact memberships on small rational grids, and asymmetric rational
sharpness witnesses.
"""

from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def theta(radius, left_gap, right_gap):
    if max(left_gap, right_gap) <= 2 * radius:
        return left_gap * right_gap / (4 * radius)
    return (left_gap + right_gap) / 2 - radius


def lens_envelope(radius, left_gap, right_gap, displacement):
    """Max ||x||^2 in the two expanded outer balls, or None if empty.

    At axial coordinate s, maximizing over perpendicular coordinates gives

      min(r^2-u^2-2us, r^2-v^2+2vs).

    The first affine function decreases and the second increases.  Their
    crossing therefore maximizes the lower envelope.
    """
    r = radius + displacement
    lo = right_gap - r
    hi = r - left_gap
    if lo > hi:
        return None
    crossing = (right_gap - left_gap) / 2
    require(lo <= crossing <= hi, "envelope crossing not in a nonempty lens")
    first = r * r - left_gap * left_gap - 2 * left_gap * crossing
    second = r * r - right_gap * right_gap + 2 * right_gap * crossing
    require(first == second == r * r - left_gap * right_gap,
            "axial-envelope formula failed")
    return first


def all_middle_balls_contain_lens(radius, left_gap, right_gap, displacement):
    maximum_squared = lens_envelope(radius, left_gap, right_gap, displacement)
    if maximum_squared is None:
        return True
    if displacement > radius:
        return False
    return maximum_squared <= (radius - displacement) ** 2


def audit_lens_thresholds():
    radii = [F(1), F(3, 2), F(2)]
    ratios = [F(1, 4), F(1, 2), F(1), F(3, 2), F(2), F(5, 2), F(3)]
    threshold_cases = 0
    envelope_samples = 0
    interfaces = 0
    for radius in radii:
        gaps = [radius * ratio for ratio in ratios]
        for left_gap in gaps:
            for right_gap in gaps:
                threshold = theta(radius, left_gap, right_gap)
                probes = [threshold / 2, threshold,
                          threshold + radius / 37]
                for index, displacement in enumerate(probes):
                    contained = all_middle_balls_contain_lens(
                        radius, left_gap, right_gap, displacement)
                    small = max(left_gap, right_gap) <= 2 * radius
                    expected = (index < 1) or (index == 1 and small)
                    require(contained == expected,
                            "wrong containment side of the proposed threshold")
                    maximum_squared = lens_envelope(
                        radius, left_gap, right_gap, displacement)
                    if maximum_squared is not None:
                        r = radius + displacement
                        lo, hi = right_gap - r, r - left_gap
                        for part in range(17):
                            s = lo + (hi - lo) * F(part, 16)
                            first = r * r - left_gap * left_gap - 2 * left_gap * s
                            second = r * r - right_gap * right_gap + 2 * right_gap * s
                            require(min(first, second) <= maximum_squared,
                                    "sample exceeded the lens envelope")
                            envelope_samples += 1
                    threshold_cases += 1
                if max(left_gap, right_gap) == 2 * radius:
                    interfaces += 1
    return threshold_cases, envelope_samples, interfaces


def audit_consecutive_reduction():
    radius = F(1)
    values = [F(1, 3), F(1), F(2), F(5, 2), F(4)]
    sequences = 0
    triples = 0
    for gap_count in range(2, 6):
        for gaps in product(values, repeat=gap_count):
            consecutive = min(theta(radius, gaps[j - 1], gaps[j])
                              for j in range(1, gap_count))
            every = []
            for i in range(gap_count - 1):
                for j in range(i + 1, gap_count):
                    left = sum(gaps[i:j])
                    for k in range(j + 1, gap_count + 1):
                        right = sum(gaps[j:k])
                        every.append(theta(radius, left, right))
                        triples += 1
            require(min(every) == consecutive,
                    "a nonconsecutive triple lowered the threshold")
            sequences += 1
    return sequences, triples


def run_count(mask):
    return sum(bit and (index == 0 or not mask[index - 1])
               for index, bit in enumerate(mask))


def audit_pointwise_combinatorics():
    masks = 0
    forced_gaps = 0
    for length in range(1, 15):
        for integer in range(1 << length):
            mask = tuple(bool(integer & (1 << index))
                         for index in range(length))
            left = sum(mask) - sum(mask[i] and mask[i + 1]
                                   for i in range(length - 1))
            require(left == run_count(mask), "run-count identity failed")
            if any(mask[i] and not mask[j] and mask[k]
                   for i in range(length)
                   for j in range(i + 1, length)
                   for k in range(j + 1, length)):
                require(run_count(mask) >= 2,
                        "an omitted middle label was hidden by extra labels")
                forced_gaps += 1
            masks += 1
    return masks, forced_gaps


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def subtract(x, y):
    return tuple(a - b for a, b in zip(x, y))


def scale(value, x):
    return tuple(value * a for a in x)


def norm_squared(x):
    return sum(a * a for a in x)


def audit_asymmetric_witnesses():
    # (u,v,eta,h,M).  In each row R=1, eta>theta, and h,M are exact.
    fixtures = [
        (F(1, 7), F(13, 7), F(2, 15), F(8, 15), F(106, 105)),
        (F(1, 13), F(35, 13), F(19, 20), F(357, 260), F(493, 260)),
    ]
    reports = []
    for left_gap, right_gap, displacement, height, maximum in fixtures:
        radius = F(1)
        require(displacement > theta(radius, left_gap, right_gap),
                "witness is not beyond the threshold")
        r = radius + displacement
        a = (left_gap + right_gap) / 2
        m = (right_gap - left_gap) / 2
        require(height * height == r * r - a * a, "wrong witness height")
        require(maximum * maximum == r * r - left_gap * right_gap,
                "wrong witness norm")
        point = (m, height)
        require(norm_squared(point) == maximum * maximum,
                "witness point has wrong norm")
        c_left = (-left_gap, F(0))
        c_right = (right_gap, F(0))
        p_left = add(c_left, scale(displacement / r,
                                   subtract(point, c_left)))
        p_right = add(c_right, scale(displacement / r,
                                     subtract(point, c_right)))
        p_middle = scale(-displacement / maximum, point)
        for actual, reference in ((p_left, c_left),
                                  (p_middle, (F(0), F(0))),
                                  (p_right, c_right)):
            require(norm_squared(subtract(actual, reference))
                    == displacement * displacement,
                    "actual center has wrong displacement")
        require(norm_squared(subtract(point, p_left)) == radius * radius,
                "point is not on the left outer sphere")
        require(norm_squared(subtract(point, p_right)) == radius * radius,
                "point is not on the right outer sphere")
        require(norm_squared(subtract(point, p_middle)) > radius * radius,
                "middle ball did not miss the witness")

        interior_point = None
        chosen_delta = None
        for exponent in range(4, 40):
            delta = F(1, 2 ** exponent)
            candidate = (point[0], point[1] - delta)
            if (norm_squared(subtract(candidate, p_left)) < radius * radius
                    and norm_squared(subtract(candidate, p_right)) < radius * radius
                    and norm_squared(subtract(candidate, p_middle)) > radius * radius):
                interior_point = candidate
                chosen_delta = delta
                break
        require(interior_point is not None,
                "no exact open sharpness witness was found")
        reports.append({
            "gaps": [str(left_gap), str(right_gap)],
            "theta": str(theta(radius, left_gap, right_gap)),
            "eta": str(displacement),
            "interior_delta": str(chosen_delta),
        })
    return reports


def audit_closed_boundary():
    # R=1, gaps 1 and 3.  The long-gap threshold is eta=1.  The two
    # outer actual balls are tangent at x=(1,0), while the adversarial
    # middle ball misses x.  Scaling displacements by alpha<1 separates
    # the outer balls, so this pointwise defect has zero volume.
    radius = F(1)
    left_gap, right_gap = F(1), F(3)
    boundary = theta(radius, left_gap, right_gap)
    require(boundary == 1, "unexpected long-gap boundary")
    point = (F(1), F(0))
    actual = [(F(0), F(0)), (F(-1), F(0)), (F(2), F(0))]
    membership = tuple(norm_squared(subtract(point, center)) <= 1
                       for center in actual)
    require(membership == (True, False, True),
            "boundary point does not exhibit the 101 defect")
    scaled = 0
    for numerator in range(10):
        alpha = F(numerator, 10)
        left = (F(-1) + alpha, F(0))
        right = (F(3) - alpha, F(0))
        require(norm_squared(subtract(left, right)) > 4,
                "outer balls met before the closed boundary")
        scaled += 1
    return membership, scaled


def audit_small_membership_grids():
    fixtures = [
        (F(1), [F(0), F(1), F(5, 2)]),
        (F(1), [F(0), F(1, 2), F(2), F(9, 2)]),
    ]
    configurations = 0
    point_tests = 0
    nonempty_tests = 0
    for radius, axial in fixtures:
        gaps = [axial[i + 1] - axial[i] for i in range(len(axial) - 1)]
        tube = min(theta(radius, gaps[i - 1], gaps[i])
                   for i in range(1, len(gaps)))
        step = tube / 2
        moves = [(F(0), F(0)), (step, F(0)), (-step, F(0)),
                 (F(0), step), (F(0), -step)]
        x_lo = axial[0] - radius
        x_hi = axial[-1] + radius
        x_values = [x_lo + (x_hi - x_lo) * F(i, 20) for i in range(21)]
        y_values = [F(-1) + F(i, 10) for i in range(21)]
        for displacements in product(moves, repeat=len(axial)):
            centers = [add((x, F(0)), move)
                       for x, move in zip(axial, displacements)]
            for x in x_values:
                for y in y_values:
                    mask = tuple(norm_squared(subtract((x, y), center))
                                 <= radius * radius for center in centers)
                    require(not any(mask[i] and not mask[j] and mask[k]
                                    for i in range(len(mask))
                                    for j in range(i + 1, len(mask))
                                    for k in range(j + 1, len(mask))),
                            "strict-tube grid found noninterval membership")
                    point_tests += 1
                    nonempty_tests += bool(any(mask))
            configurations += 1
    return configurations, point_tests, nonempty_tests


def integral_power(radius, exponent, upper):
    """Integral_0^upper (R^2-t^2)^exponent dt, exactly."""
    return sum(F(comb(exponent, k) * (-1) ** k, 2 * k + 1)
               * radius ** (2 * (exponent - k)) * upper ** (2 * k + 1)
               for k in range(exponent + 1))


def phi_unscaled(radius, exponent, distance):
    clipped = min(distance, 2 * radius)
    # Substitution t=2z in the stated Phi integral.
    return 2 * integral_power(radius, exponent, clipped / 2)


def audit_two_ball_and_hessian():
    cap_checks = 0
    hessian_checks = 0
    contraction_checks = 0
    radii = [F(1), F(3, 2), F(2)]
    for exponent in range(1, 5):  # dimensions 3,5,7,9
        for radius in radii:
            ball = 2 * integral_power(radius, exponent, radius)
            distances = [F(0), radius / 3, radius, 3 * radius / 2,
                         2 * radius, 5 * radius / 2]
            for distance in distances:
                overlap = (2 * (integral_power(radius, exponent, radius)
                                - integral_power(radius, exponent,
                                                 distance / 2))
                           if distance <= 2 * radius else F(0))
                require(ball - overlap
                        == phi_unscaled(radius, exponent, distance),
                        "cap identity disagrees with Phi")
                cap_checks += 1
            for gap in [radius / 3, radius, 3 * radius / 2]:
                rho_squared = radius * radius - gap * gap / 4
                # d Phi(sqrt(g^2+Q))/dQ at Q=0, computed by the
                # fundamental theorem and 2s ds/dQ=1.
                chain_coefficient = rho_squared ** exponent / (2 * gap)
                hessian = 2 * chain_coefficient
                require(hessian == rho_squared ** exponent / gap,
                        "transverse Hessian coefficient failed")
                hessian_checks += 1
            samples = [F(0), radius / 2, radius, 3 * radius / 2,
                       2 * radius, 5 * radius / 2]
            for before in samples:
                for after in samples:
                    if after > before:
                        continue
                    delta = (phi_unscaled(radius, exponent, before)
                             - phi_unscaled(radius, exponent, after))
                    equal_clipped = (min(before, 2 * radius)
                                     == min(after, 2 * radius))
                    require((delta == 0) == equal_clipped,
                            "contraction equality criterion failed")
                    require(delta >= 0, "Phi was not monotone")
                    contraction_checks += 1

    # The weighted path kernel is exactly constancy on every component of
    # strict-overlap edges.  Exhaust a small disconnected example.
    weights = [F(3, 2), F(0), F(5, 7), F(11, 9)]
    kernel_vectors = 0
    for vector in product(range(-1, 2), repeat=5):
        quadratic = sum(weight * (vector[i + 1] - vector[i]) ** 2
                        for i, weight in enumerate(weights))
        expected_zero = all(weight == 0 or vector[i + 1] == vector[i]
                            for i, weight in enumerate(weights))
        require((quadratic == 0) == expected_zero,
                "weighted path kernel was misstated")
        kernel_vectors += 1
    return cap_checks, hessian_checks, contraction_checks, kernel_vectors


def build_summary():
    threshold_cases, envelope_samples, interfaces = audit_lens_thresholds()
    sequences, triples = audit_consecutive_reduction()
    masks, forced_gaps = audit_pointwise_combinatorics()
    witnesses = audit_asymmetric_witnesses()
    membership, scaled = audit_closed_boundary()
    configurations, point_tests, nonempty_tests = audit_small_membership_grids()
    cap_checks, hessian_checks, contraction_checks, kernel_vectors = (
        audit_two_ball_and_hessian())
    return {
        "boundary": {
            "membership": [int(value) for value in membership],
            "strict_scaled_configurations": scaled,
        },
        "combinatorics": {
            "forced_gap_masks": forced_gaps,
            "masks": masks,
        },
        "consecutive_reduction": {
            "sequences": sequences,
            "triples": triples,
        },
        "lens": {
            "envelope_samples": envelope_samples,
            "interface_pairs": interfaces,
            "threshold_cases": threshold_cases,
        },
        "path_formula": {
            "cap_checks": cap_checks,
            "contraction_checks": contraction_checks,
            "hessian_checks": hessian_checks,
            "kernel_vectors": kernel_vectors,
        },
        "strict_tube_grid": {
            "configurations": configurations,
            "nonempty_memberships": nonempty_tests,
            "point_tests": point_tests,
        },
        "witnesses": witnesses,
    }


def main():
    summary = build_summary()
    encoded = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode()
    if "--emit" in sys.argv:
        sys.stdout.write(encoded.decode())
        return
    expected_path = Path(__file__).with_name("EXPECTED.json")
    expected = json.loads(expected_path.read_text())
    require(summary == expected, "result differs from EXPECTED.json")
    print("PASS independent near-collinear ball-union review")
    print(hashlib.sha256(encoded).hexdigest())
    print(json.dumps({
        "asymmetric_witnesses": len(summary["witnesses"]),
        "exact_membership_tests": summary["strict_tube_grid"]["point_tests"],
        "lens_envelope_samples": summary["lens"]["envelope_samples"],
        "run_masks": summary["combinatorics"]["masks"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
