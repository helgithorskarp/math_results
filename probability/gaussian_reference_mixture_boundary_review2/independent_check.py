#!/usr/bin/env python3
"""Independent exact audit of the isometric-reference mixture obstruction.

This checker imports no submitted code or expected output.  It uses only
integer and Fraction arithmetic.  The analytic steps involving Gaussian
convolution, analyticity of level sets, and Popoviciu's inequality are written
out in REVIEW.md; the finite checks here exercise their constants and all
discrete/algebraic interfaces by a representation separate from the source.
"""

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import itertools
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def cross_cube_grid_audit(max_denominator):
    """Check exact distance loss and motion derivative on a rational grid."""
    loss_checks = 0
    motion_checks = 0
    stream = sha256()
    for denominator in range(1, max_denominator + 1):
        for numerator in range(-denominator, denominator + 1):
            h = Q(numerator, denominator)
            loss = (16 + h) ** 2 - (8 + h) ** 2
            require(loss == 192 + 16 * h >= 176, "cross-cube distance loss")
            loss_checks += 1
            stream.update(f"L:{denominator}:{numerator}:{loss}\n".encode())
            for time_numerator in range(denominator + 1):
                time = Q(time_numerator, denominator)
                derivative = -16 * (16 - 8 * time + h)
                require(derivative <= -112, "continuous-contraction derivative")
                motion_checks += 1
                stream.update(
                    f"M:{denominator}:{numerator}:{time_numerator}:{derivative}\n".encode()
                )
    return loss_checks, motion_checks, stream.hexdigest()


def matrix_for_quadratic(signs):
    """Matrix of 3|b|_2^2-(sum |b_i|)^2 in a fixed sign orthant."""
    return tuple(
        tuple((3 if i == j else 0) - signs[i] * signs[j] for j in range(3))
        for i in range(3)
    )


def matrix_for_pair_squares(signs):
    """Matrix of sum_{i<j}(s_i b_i-s_j b_j)^2."""
    matrix = [[0 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(i + 1, 3):
            matrix[i][i] += 1
            matrix[j][j] += 1
            matrix[i][j] -= signs[i] * signs[j]
            matrix[j][i] -= signs[i] * signs[j]
    return tuple(tuple(row) for row in matrix)


def strong_log_concavity_audit():
    """Verify all sign-orthant polynomial identities behind the width bound."""
    identities = 0
    for signs in itertools.product((-1, 1), repeat=3):
        require(matrix_for_quadratic(signs) == matrix_for_pair_squares(signs),
                "three-dimensional Cauchy identity")
        identities += 1
    range_variance_bound = Q(3, 4)
    hessian_upper_bound = -1 + range_variance_bound
    require(hessian_upper_bound == Q(-1, 4), "log-Hessian bound")
    return identities, range_variance_bound, hessian_upper_bound


def discrete_midpoint_model(max_cells):
    """Exhaust a finite analogue of the two-box midpoint obstruction.

    Each cell has two end points and their midpoint.  A candidate containing
    both end points must contain the midpoint.  Missing end points are the
    false-negative mass; chosen midpoints plus unrestricted exterior points
    supply equal false-positive mass.  The optimum is ceil(cells/2), matching
    the review's stronger joint-deficit argument.
    """
    local_states = tuple(
        (2 - left - right, middle)
        for left, right, middle in itertools.product((0, 1), repeat=3)
        if not (left and right and not middle)
    )
    reachable = {(0, 0)}
    stream = sha256()
    optima = []
    state_transitions = 0
    for cells in range(1, max_cells + 1):
        following = set()
        for missed, middle in reachable:
            for local_missed, local_middle in local_states:
                following.add((missed + local_missed, middle + local_middle))
                state_transitions += 1
        reachable = following
        # Exterior false positives can fill missed-middle when nonnegative.
        optimum = min(missed for missed, middle in reachable if middle <= missed)
        require(optimum == (cells + 1) // 2, "discrete midpoint optimum")
        optima.append(optimum)
        stream.update(f"{cells}:{optimum}:{len(reachable)}\n".encode())
    return optima, state_transitions, stream.hexdigest()


def mixture_and_energy_identities(weight_denominator):
    """Exhaust exact pointwise identities used for convex mixtures and energy."""
    mixture_checks = 0
    for a, first, second in itertools.product((0, 1), repeat=3):
        for numerator in range(weight_denominator + 1):
            weight = Q(numerator, weight_denominator)
            phi = weight * first + (1 - weight) * second
            require(abs(a - phi)
                    == weight * abs(a - first) + (1 - weight) * abs(a - second),
                    "indicator-mixture L1 identity")
            mixture_checks += 1

    energy_checks = 0
    for a in (0, 1):
        signed_levels = (range(-32, 1) if a == 0 else range(1, 33))
        for level_numerator in signed_levels:
            level = Q(level_numerator, 32)
            for numerator in range(weight_denominator + 1):
                phi = Q(numerator, weight_denominator)
                require((a - phi) * level == abs(a - phi) * abs(level),
                        "superlevel energy identity")
                energy_checks += 1
    return mixture_checks, energy_checks


def audit():
    loss_checks, motion_checks, motion_hash = cross_cube_grid_audit(64)
    orthant_checks, variance_bound, hessian_bound = strong_log_concavity_audit()

    # Exact rational consequences of the elementary Gaussian estimates.
    centered_kernel_lower = Q(7, 24)
    endpoint_density_lower = Q(1, 2) * Q(29, 32) * centered_kernel_lower ** 3
    middle_density_upper = Q(3, 8) ** 5
    require(endpoint_density_lower == Q(9947, 884736) > Q(1, 100),
            "endpoint boxes are above threshold")
    require(middle_density_upper == Q(243, 32768) < Q(1, 100),
            "middle box is below threshold")
    require(Q(841, 32) > 5, "middle Gaussian exponent comparison")

    optima, state_transitions, midpoint_hash = discrete_midpoint_model(96)
    box_volume = Q(1, 8)
    submitted_symmetric_difference = Q(1, 12)
    stronger_symmetric_difference = box_volume
    require(stronger_symmetric_difference > submitted_symmetric_difference,
            "joint-deficit strengthening")

    mixture_checks, energy_checks = mixture_and_energy_identities(64)
    shell_measure_cap = Q(1, 24)
    submitted_energy_coefficient = submitted_symmetric_difference - shell_measure_cap
    stronger_energy_coefficient = stronger_symmetric_difference - shell_measure_cap
    require(submitted_energy_coefficient == Q(1, 24), "submitted shell gap")
    require(stronger_energy_coefficient == Q(1, 12), "strengthened shell gap")

    return {
        "status": "INDEPENDENT_REFERENCE_MIXTURE_BOUNDARY_REVIEW_PASS",
        "imports_submitted_code_or_expected_output": False,
        "cross_cube_grid_denominators": [1, 64],
        "cross_cube_distance_checks": loss_checks,
        "continuous_motion_derivative_checks": motion_checks,
        "cross_cube_stream_sha256": motion_hash,
        "cauchy_orthant_polynomial_identities": orthant_checks,
        "posterior_variance_upper": str(variance_bound),
        "log_hessian_upper": str(hessian_bound),
        "endpoint_density_rational_lower": str(endpoint_density_lower),
        "middle_density_rational_upper": str(middle_density_upper),
        "midpoint_model_cell_range": [1, 96],
        "midpoint_model_last_optimum": optima[-1],
        "midpoint_model_state_transitions": state_transitions,
        "midpoint_model_stream_sha256": midpoint_hash,
        "indicator_mixture_identity_checks": mixture_checks,
        "superlevel_energy_identity_checks": energy_checks,
        "submitted_l1_lower_bound": str(submitted_symmetric_difference),
        "reviewer_strengthened_l1_lower_bound": str(stronger_symmetric_difference),
        "submitted_energy_gap_coefficient": str(submitted_energy_coefficient),
        "reviewer_strengthened_energy_gap_coefficient": str(stronger_energy_coefficient),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.check:
        expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
        require(result == expected, "result differs from EXPECTED.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
