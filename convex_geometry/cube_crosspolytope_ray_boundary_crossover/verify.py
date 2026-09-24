"""Exact checks for the ray-boundary Legendre law and Bessel bounds."""

from decimal import Decimal as D, getcontext
from fractions import Fraction as F
from importlib.util import module_from_spec, spec_from_file_location
from json import dumps
from math import comb, factorial
from pathlib import Path


getcontext().prec = 80


def require(condition, message):
    if not condition:
        raise ValueError(message)


def falling(value, length):
    answer = 1
    for offset in range(length):
        answer *= value - offset
    return answer


def rising(value, length):
    answer = 1
    for offset in range(length):
        answer *= value + offset
    return answer


def simplex_ratio(size, z):
    """The pre-collapse simplex-integral formula, in exact arithmetic."""
    z = F(z)
    answer = F(1)
    for inactive in range(1, size):
        prefactor = F(
            falling(size, inactive) * falling(size - 1, inactive),
            factorial(inactive) * size ** (2 * inactive),
        )
        integral = sum(
            F(comb(size - inactive - 1, power), size ** (2 * power))
            * z ** (inactive + power)
            / F(factorial(inactive - 1) * (inactive + power))
            for power in range(size - inactive)
        )
        answer += prefactor * integral
    return answer


def simplex_coefficient(size, degree):
    """Coefficient extracted directly from the nested sum above."""
    if degree == 0:
        return F(1)
    return sum(
        F(
            falling(size, inactive) * falling(size - 1, inactive),
            factorial(inactive)
            * size ** (2 * inactive)
            * factorial(inactive - 1),
        )
        * F(comb(size - inactive - 1, degree - inactive),
            size ** (2 * (degree - inactive)) * degree)
        for inactive in range(1, degree + 1)
    )


def legendre_coefficients(size):
    """Coefficients of 2F1(1-N,N;1;-z/N^2)."""
    return [
        F(
            falling(size - 1, degree) * rising(size, degree),
            factorial(degree) ** 2 * size ** (2 * degree),
        )
        for degree in range(size)
    ]


def evaluate(coefficients, value):
    value = F(value)
    answer = F(0)
    for coefficient in reversed(coefficients):
        answer = answer * value + coefficient
    return answer


def legendre_value(degree, value):
    """Three-term Legendre recurrence, evaluated exactly."""
    value = F(value)
    previous = F(1)
    if degree == 0:
        return previous
    current = value
    for order in range(1, degree):
        previous, current = (
            current,
            F(2 * order + 1, order + 1) * value * current
            - F(order, order + 1) * previous,
        )
    return current


def check_differential_equation(size, coefficients):
    """Check the transformed Legendre ODE coefficient by coefficient."""
    extended = coefficients + [F(0)]
    for degree in range(size):
        residual = (
            (degree + 1) ** 2 * extended[degree + 1]
            + F(degree * (degree + 1), size ** 2) * extended[degree]
            - F(size - 1, size) * extended[degree]
        )
        require(residual == 0, "transformed Legendre differential equation")


def load_exact_section():
    path = (Path(__file__).resolve().parent.parent
            / "affine_cube_crosspolytope_sections" / "exact_section.py")
    specification = spec_from_file_location("ray_exact_section", path)
    require(specification is not None and specification.loader is not None,
            "exact-section import")
    module = module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def affine_ratio(module, size, theta, z):
    """Ratio from the independent all-strata affine section engine."""
    theta, z = F(theta), F(z)
    margin = abs(theta) - 1
    require(margin > 0 and margin * z / size <= 2,
            "parameters outside the first ray segment")
    boundary_radius = margin * size
    radius = boundary_radius + margin * z / size
    boundary = module.section(size, boundary_radius, theta * size)
    predicted_boundary = boundary_radius ** (size - 1) / factorial(size - 1)
    require(boundary == predicted_boundary, "ray-boundary normalization")
    return module.section(size, radius, theta * size) / boundary


def as_decimal(value):
    return D(value.numerator) / D(value.denominator)


def bessel_data(z):
    """F, KF, (K^3-K)F, Psi_1, and Psi_2 from entire series."""
    z = D(z)
    phi = D(0)
    k_phi = D(0)
    k3_minus_k = D(0)
    psi2_direct = D(0)
    for order in range(300):
        weight = z ** order / D(factorial(order) ** 2)
        phi += weight
        k_phi += D(order) * weight
        k3_minus_k += D(order ** 3 - order) * weight
        psi2_direct -= (
            D(order * (order - 1) * (2 * order - 1)) * weight / D(6)
        )
        if order > 50 and abs(weight) < D("1e-90"):
            psi1 = -k_phi
            psi2_closed = (z * phi - (D(2) * z + D(1)) * k_phi) / D(6)
            require(abs(psi2_direct - psi2_closed) < D("1e-72"),
                    "direct and closed second corrections")
            return phi, k_phi, k3_minus_k, psi1, psi2_closed
    raise ArithmeticError("Bessel series did not terminate")


def text(value, digits=18):
    return f"{value:.{digits}f}"


def main():
    exact = load_exact_section()

    coefficient_checks = 0
    ode_checks = 0
    for size in range(2, 17):
        coefficients = legendre_coefficients(size)
        for degree, coefficient in enumerate(coefficients):
            require(simplex_coefficient(size, degree) == coefficient,
                    "Vandermonde coefficient collapse")
            coefficient_checks += 1
        check_differential_equation(size, coefficients)
        ode_checks += 1

    # Distinct offsets, reflection, and several scaled radii.
    exact_parameters = (
        (F(2), F(1)),
        (F(3), F(1)),
        (F(-2), F(1)),
        (F(3, 2), F(2)),
        (F(2), F(4)),
    )
    exact_checks = 0
    for size in (3, 4, 6, 8):
        for theta, z in exact_parameters:
            coefficients = legendre_coefficients(size)
            hypergeometric = evaluate(coefficients, z)
            legendre = legendre_value(
                size - 1, F(1) + F(2) * z / size ** 2
            )
            require(simplex_ratio(size, z) == hypergeometric == legendre,
                    "simplex, hypergeometric, and Legendre identity")
            require(affine_ratio(exact, size, theta, z) == legendre,
                    "affine section and Legendre identity")
            exact_checks += 1

    endpoint_checks = 0
    for size in (3, 4, 6, 8):
        for theta in (F(3, 2), F(2), F(3), F(-2)):
            margin = abs(theta) - 1
            z = F(2 * size, margin)
            expected = legendre_value(
                size - 1, F(1) + F(2) * z / size ** 2
            )
            require(affine_ratio(exact, size, theta, z) == expected,
                    "closed first-segment endpoint")
            endpoint_checks += 1

    require(evaluate(legendre_coefficients(8), 0) == 1,
            "zero-thickness identity")
    require(
        affine_ratio(exact, 8, F(2), F(1))
        == affine_ratio(exact, 8, F(3), F(1))
        == affine_ratio(exact, 8, F(-2), F(1)),
        "offset and reflection collapse",
    )

    # Just beyond total slack two, a minus-tail stratum has positive measure.
    outside_size, outside_z = 3, F(7)
    outside_boundary = exact.section(outside_size, 3, 6)
    outside_ratio = exact.section(outside_size, F(16, 3), 6) / outside_boundary
    require(outside_ratio != evaluate(
        legendre_coefficients(outside_size), outside_z
    ), "opposite-tail threshold negative control")

    monotonicity_checks = 0
    for size in range(2, 24):
        current = legendre_coefficients(size)
        following = legendre_coefficients(size + 1)
        for degree in range(size):
            require(current[degree] <= following[degree],
                    "coefficientwise dimension monotonicity")
            monotonicity_checks += 1
        require(following[size] > 0, "new positive terminal coefficient")

    bound_checks = 0
    asymptotic_samples = []
    for z in (1, 2, 4):
        phi, k_phi, k3_minus_k, psi1, psi2 = bessel_data(z)
        rows = []
        previous = F(0)
        for size in (8, 16, 32, 64, 128):
            ratio_exact = evaluate(legendre_coefficients(size), F(z))
            require(ratio_exact > previous, "strict numerical monotonicity")
            previous = ratio_exact
            ratio = as_decimal(ratio_exact)
            upper = bessel_data(D(z) * D(size - 1) / D(size))[0]
            lower = (
                phi - k_phi / D(size)
                - k3_minus_k / (D(3) * D(size ** 2))
            )
            require(lower <= ratio <= upper <= phi,
                    "finite-N global Bessel bounds")
            bound_checks += 1
            scaled = D(size ** 2) * (
                ratio - phi - psi1 / D(size)
            )
            rows.append({
                "N": size,
                "Q_N": text(ratio),
                "N2_times_two_term_residual": text(scaled),
                "second_correction_residual": text(scaled - psi2),
            })
        require(abs(D(rows[-1]["second_correction_residual"]))
                < abs(D(rows[0]["second_correction_residual"])),
                "second-correction convergence")
        asymptotic_samples.append({
            "z": z,
            "Phi_I0": text(phi),
            "Psi1_minus_sqrt_z_I1": text(psi1),
            "Psi2": text(psi2),
            "finite_legendre_polynomials": rows,
        })

    output = {
        "status": "RAY_BOUNDARY_LEGENDRE_VERIFIED",
        "vandermonde_coefficient_checks": coefficient_checks,
        "exact_differential_equation_polynomials": ode_checks,
        "exact_affine_engine_checks": exact_checks,
        "closed_endpoint_checks": endpoint_checks,
        "coefficient_monotonicity_checks": monotonicity_checks,
        "global_bessel_bound_checks": bound_checks,
        "exact_offset_reflection_collapse": True,
        "outside_segment_negative_control": True,
        "zero_thickness_Q_N": "1",
        "series_agreement_bound": "1e-72",
        "asymptotic_samples": asymptotic_samples,
        "scope": (
            "Independent exact simplex, hypergeometric, Legendre-recurrence, "
            "differential-equation, and affine-stratum checks, plus 80-digit "
            "global bounds and two correction terms; PROOF.md is universal."
        ),
    }
    print(dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
