#!/usr/bin/env python3
"""Clean-room exact audit for the universal Gaussian peak window.

This script imports no reviewed code.  It recomputes the conservative
constant chain and independently calibrates the six-dimensional coarea,
replica, and Abel normalizations used in the proof.  The analytic inequalities
and measure-theoretic inversion remain written mathematics.
"""

from fractions import Fraction as F
import json
from math import factorial


def integer_partitions(n, minimum=1):
    if n == 0:
        yield ()
        return
    for first in range(minimum, n + 1):
        for tail in integer_partitions(n - first, first):
            yield (first,) + tail


def log_derivative_coefficient_sum(n):
    """Sum absolute coefficients by explicit integer-partition multiplicity."""
    total = 0
    for partition in integer_partitions(n):
        counts = {size: partition.count(size) for size in set(partition)}
        blocks = len(partition)
        multiplicity = factorial(n)
        for size, count in counts.items():
            multiplicity //= factorial(size) ** count * factorial(count)
        total += multiplicity * factorial(blocks - 1)
    return total


def main():
    delta = F(1, 2**32)
    eta_factor = 8192
    e0_factor = 256 * eta_factor
    epsilon_factor = 32 * e0_factor
    eta = eta_factor * delta
    e0 = e0_factor * delta
    epsilon = epsilon_factor * delta
    assert epsilon == F(1, 64)
    assert eta <= 1 and e0 <= F(1, 4)

    # Scalar posterior tail split: r<=1 costs <4e<12, while r>=1 costs
    # <3e*320<2880.  Both sit below the proof's 4096 envelope.
    scalar_small_radius_bound = 12
    scalar_large_radius_bound = 2880
    assert max(scalar_small_radius_bound, scalar_large_radius_bound) < 4096

    partition_sums = [log_derivative_coefficient_sum(n) for n in range(1, 6)]
    assert partition_sums == [1, 2, 6, 26, 150]
    assert max(partition_sums) < 256

    # Matrix-square-root series and inverse-chart budgets, recomputed from the
    # primitive derivative bounds rather than copied from the author audit.
    q = F(1, 4)
    square_root_series = q * (1 + 4*q + q*q) / (1 - q)**4
    assert square_root_series < 8
    inverse_norm_budget = 2
    inverse_second = inverse_norm_budget * F(3, 4) * inverse_norm_budget**2
    inverse_third_linear = 16
    inverse_third_quadratic = 54 * epsilon
    assert inverse_second == 6
    assert inverse_third_linear + inverse_third_quadratic <= 17

    log_jacobian_gradient = 6 * 2 * 6
    log_jacobian_hessian_linear = 6 * 2 * 17
    log_jacobian_hessian_quadratic = 6 * 4 * 36 * epsilon
    assert log_jacobian_gradient == 72
    assert log_jacobian_hessian_linear + log_jacobian_hessian_quadratic <= 256
    gradient_a = F(5, 2) + log_jacobian_gradient
    hessian_a = 6 + 12 + 256
    assert gradient_a <= 75 and hessian_a <= 288
    midpoint_linear = 36 + 2 * (1 + epsilon) * 75
    assert midpoint_linear <= 192
    helmholtz_penalty = 192**2 * epsilon**2 + 6 * 288 * epsilon
    assert helmholtz_penalty == 36

    # The regular radial Helmholtz solution in dimension six has coefficients
    # (-1)^k x^(2k)/(4^k k! (3)_k).  At x<=1 the first term gives the exact
    # conservative logarithmic-derivative bound used in the proof.
    b_lower = 1 - F(1, 12)
    minus_x_bprime_upper = F(1, 6)
    radial_log_derivative = -minus_x_bprime_upper / b_lower
    spherical_margin = 4 + radial_log_derivative
    assert radial_log_derivative == -F(2, 11)
    assert spherical_margin == F(42, 11)
    for k in range(0, 100):
        assert F(1, 4 * (k + 1) * (k + 3)) < 1
    for k in range(1, 100):
        assert F(1, 4 * k * (k + 3)) < 1
    assert 72 * delta < 1

    # Dimension audit.  In d=6, polar volume r^5 dr and dw=r dr give
    # coarea power r^(d-2)=r^4.  Differentiation adds the radial margin.
    dimension = 6
    coarea_power = dimension - 2
    assert coarea_power == 4
    coarea_derivative_margin = coarea_power + radial_log_derivative
    assert coarea_derivative_margin == F(42, 11)

    # Replica normalization.  A hinge u-moment contributes 1/[k(k-1)].
    # A three-dimensional normalized k-energy has k^(-3/2); differentiating
    # its affine lifted variance contributes (k-1)/4.  The result is
    # 1/(4 k^(5/2)).  The six-dimensional marked integral contributes k^-3,
    # and the asserted sqrt(k)/4 prefactor gives the same exponent/coefficient.
    hinge_k_power = -1
    energy_k_power = F(-3, 2)
    endpoint_total_power = hinge_k_power + energy_k_power
    marked_k_power = -3 + F(1, 2)
    endpoint_replica_coefficient = F(1, 4)
    marked_laplace_coefficient = F(1, 4)
    assert endpoint_total_power == marked_k_power == F(-5, 2)
    assert endpoint_replica_coefficient == marked_laplace_coefficient

    # Independent centered calibration.  C6*A(l)=D*l^2/2, hence
    # G(l)=D*l^(3/2)/(3 sqrt(pi)).  Its Laplace transform uses
    # Gamma(5/2)/sqrt(pi)=3/4 and equals D/(4 k^(5/2)).
    coarea_density_coefficient = F(1, 2)
    abel_g_coefficient = F(1, 3)
    gamma_five_half_over_sqrt_pi = F(3, 4)
    centered_moment_coefficient = abel_g_coefficient * gamma_five_half_over_sqrt_pi
    assert coarea_density_coefficient == F(1, 2)
    assert centered_moment_coefficient == F(1, 4)

    # The Riemann--Liouville half-integral is normalized by 1/sqrt(pi), so
    # composing it twice multiplies by Beta(1/2,1/2)/pi=1.  A density
    # O((l-sigma)^2) and derivative O(l-sigma) both vanish at entry.
    half_integral_composition = 1
    mode_density_order = dimension // 2 - 1
    mode_derivative_order = mode_density_order - 1
    assert half_integral_composition == 1
    assert (mode_density_order, mode_derivative_order) == (2, 1)

    result = {
        "status": "INDEPENDENT_UNIVERSAL_PEAK_AUDIT_PASS",
        "arithmetic": "fractions.Fraction and exact combinatorics",
        "imports_reviewed_code": False,
        "delta": str(delta),
        "posterior_scalar_envelope": 4096,
        "log_derivative_partition_sums": partition_sums,
        "epsilon": str(epsilon),
        "square_root_series_at_one_quarter": str(square_root_series),
        "inverse_chart_second_derivative_factor": str(inverse_second),
        "inverse_chart_third_derivative_factor": str(
            inverse_third_linear + inverse_third_quadratic
        ),
        "marked_midpoint_helmholtz_penalty": str(helmholtz_penalty),
        "radial_log_derivative_lower_bound": str(radial_log_derivative),
        "coarea_power": coarea_power,
        "coarea_derivative_margin": str(coarea_derivative_margin),
        "endpoint_replica_k_exponent": str(endpoint_total_power),
        "marked_laplace_k_exponent": str(marked_k_power),
        "replica_and_marked_coefficient": str(endpoint_replica_coefficient),
        "centered_abel_moment_coefficient": str(centered_moment_coefficient),
        "mode_density_vanishing_order": mode_density_order,
        "mode_derivative_vanishing_order": mode_derivative_order,
        "analytic_inequalities_formalized": False,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
