"""Exact checks for ray-boundary universality and its Bessel crossover."""

from decimal import Decimal as D, getcontext
from fractions import Fraction as F
from importlib.util import module_from_spec, spec_from_file_location
from json import dumps
from math import comb, factorial
from pathlib import Path


getcontext().prec = 80
ONE = D(1)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def falling(value, length):
    answer = 1
    for offset in range(length):
        answer *= value - offset
    return answer


def universal_ratio(size, z):
    """The polynomial Q_N(z), evaluated exactly for rational z."""
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
    require(margin > 0 and margin * z / size < 2,
            "parameters outside the one-ray gap")
    boundary_radius = margin * size
    radius = boundary_radius + margin * z / size
    boundary = module.section(size, boundary_radius, theta * size)
    predicted_boundary = boundary_radius ** (size - 1) / factorial(size - 1)
    require(boundary == predicted_boundary, "ray-boundary normalization")
    return module.section(size, radius, theta * size) / boundary


def as_decimal(value):
    return D(value.numerator) / D(value.denominator)


def bessel_data(z):
    """Phi and Psi from their independent entire series."""
    z = D(z)
    phi = D(0)
    psi_closed = D(0)
    psi_strata = D(0)
    for order in range(300):
        weight = z ** order / D(factorial(order) ** 2)
        phi += weight
        if order:
            psi_closed -= (
                z ** order
                / D(factorial(order - 1) * factorial(order))
            )
        psi_strata += weight * (
            -D(order ** 2) + D(order) * z / D(order + 1)
        )
        if order > 50 and abs(weight) < D("1e-90"):
            require(abs(psi_closed - psi_strata) < D("1e-72"),
                    "closed and stratum first corrections")
            return phi, psi_closed
    raise ArithmeticError("Bessel series did not terminate")


def text(value, digits=18):
    return f"{value:.{digits}f}"


def main():
    exact = load_exact_section()

    # These cases contain distinct offsets with z=1, a reflected offset,
    # and two further z values.  Equality is exact, not a tolerance check.
    exact_parameters = (
        (F(2), F(1)),
        (F(3), F(1)),
        (F(-2), F(1)),
        (F(3, 2), F(2)),
        (F(2), F(4)),
    )
    exact_check_count = 0
    for size in (3, 4, 6, 8):
        for theta, z in exact_parameters:
            direct = affine_ratio(exact, size, theta, z)
            universal = universal_ratio(size, z)
            require(direct == universal, "finite-N universality identity")
            exact_check_count += 1

    require(universal_ratio(8, 0) == 1, "zero-thickness identity")
    require(
        affine_ratio(exact, 8, F(2), F(1))
        == affine_ratio(exact, 8, F(3), F(1))
        == affine_ratio(exact, 8, F(-2), F(1)),
        "offset and reflection collapse",
    )

    # Beyond slack two a minus-tail stratum enters; the one-ray polynomial
    # must no longer be mistaken for the full section.
    outside_size, outside_z = 3, F(7)
    outside_boundary = exact.section(outside_size, 3, 6)
    outside_ratio = (
        exact.section(outside_size, F(16, 3), 6) / outside_boundary
    )
    require(outside_ratio != universal_ratio(outside_size, outside_z),
            "opposite-tail threshold negative control")

    asymptotic_samples = []
    for z in (1, 2, 4):
        phi, psi = bessel_data(z)
        rows = []
        for size in (4, 8, 16, 32, 64):
            ratio = as_decimal(universal_ratio(size, F(z)))
            scaled = D(size) * (ratio - phi)
            rows.append({
                "N": size,
                "Q_N": text(ratio),
                "N_times_leading_residual": text(scaled),
                "first_correction_residual": text(scaled - psi),
            })
        require(abs(D(rows[-1]["Q_N"]) - phi)
                < abs(D(rows[0]["Q_N"]) - phi),
                "Bessel leading convergence")
        require(abs(D(rows[-1]["first_correction_residual"])) < D("0.4"),
                "first-correction corroboration outside tolerance")
        asymptotic_samples.append({
            "z": z,
            "Phi_I0": text(phi),
            "Psi_minus_sqrt_z_I1": text(psi),
            "finite_universal_polynomials": rows,
        })

    output = {
        "status": "RAY_BOUNDARY_UNIVERSALITY_VERIFIED",
        "exact_affine_engine_checks": exact_check_count,
        "exact_engine_sizes": [3, 4, 6, 8],
        "exact_parameter_pairs_theta_z": [
            [str(theta), str(z)] for theta, z in exact_parameters
        ],
        "exact_offset_reflection_collapse": True,
        "outside_gap_negative_control": True,
        "zero_thickness_Q_N": "1",
        "series_agreement_bound": "1e-72",
        "asymptotic_samples": asymptotic_samples,
        "scope": (
            "Exact rational comparison with the independent affine-stratum "
            "engine, plus independent 80-digit Bessel and correction series; "
            "PROOF.md establishes the identity and all-orders expansion."
        ),
    }
    print(dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
