#!/usr/bin/env python3
"""Independent exact checks for ray-boundary section universality.

This file imports no target code or data.  For N=3 it reconstructs the
original section directly as a rational polygon.  The identity

    sum_i (abs(x_i)-1)_+ <= R

is encoded by all 3^3 halfspaces

    sum_i s_i*x_i <= R + |supp(s)|,  s_i in {-1,0,1}.

After eliminating x_3 with the affine equation, every polygon vertex and
its area are computed over Q.  A separate series calculation derives and
checks the second (N^-2) coefficient, which is not printed in the target.
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from json import dumps
from math import comb, factorial


getcontext().prec = 90


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def intersect(
    first: tuple[F, F, F], second: tuple[F, F, F]
) -> tuple[F, F] | None:
    """Intersection of a*x+b*y=c for two boundary lines."""
    a, b, c = first
    d, e, f = second
    determinant = a * e - b * d
    if determinant == 0:
        return None
    return ((c * e - b * f) / determinant, (a * f - c * d) / determinant)


def cross(origin: tuple[F, F], a: tuple[F, F], b: tuple[F, F]) -> F:
    return ((a[0] - origin[0]) * (b[1] - origin[1])
            - (a[1] - origin[1]) * (b[0] - origin[0]))


def convex_hull(points: set[tuple[F, F]]) -> list[tuple[F, F]]:
    """Exact monotone-chain hull."""
    ordered = sorted(points)
    require(len(ordered) >= 3, "section polygon is degenerate")
    lower: list[tuple[F, F]] = []
    for point in ordered:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper: list[tuple[F, F]] = []
    for point in reversed(ordered):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def polygon_area(vertices: list[tuple[F, F]]) -> F:
    twice = sum(
        x1 * y2 - y1 * x2
        for (x1, y1), (x2, y2) in zip(vertices, vertices[1:] + vertices[:1])
    )
    return abs(twice) / 2


def direct_section_n3(theta: F, rho: F) -> tuple[F, int]:
    """Delta-normalized A_3(theta,rho), directly from its H-representation."""
    total = 3 * F(theta)
    radius = 3 * F(rho)
    inequalities: list[tuple[F, F, F]] = []
    for signs in product((-1, 0, 1), repeat=3):
        support = sum(sign != 0 for sign in signs)
        # x_3 = total-x_1-x_2.
        a = F(signs[0] - signs[2])
        b = F(signs[1] - signs[2])
        c = radius + support - signs[2] * total
        if a == b == 0:
            require(c >= 0, "empty section")
        else:
            inequalities.append((a, b, F(c)))

    vertices: set[tuple[F, F]] = set()
    for first, second in combinations(inequalities, 2):
        point = intersect(first, second)
        if point is None:
            continue
        x, y = point
        if all(a * x + b * y <= c for a, b, c in inequalities):
            vertices.add(point)
    hull = convex_hull(vertices)
    return polygon_area(hull), len(hull)


def falling(value: int, length: int) -> int:
    answer = 1
    for offset in range(length):
        answer *= value - offset
    return answer


def q_polynomial(size: int, z: F) -> F:
    """Evaluate the claimed Q_N from its displayed finite sum."""
    z = F(z)
    answer = F(1)
    for k in range(1, size):
        prefactor = F(
            falling(size, k) * falling(size - 1, k),
            factorial(k) * size ** (2 * k) * factorial(k - 1),
        )
        integral = sum(
            F(comb(size - k - 1, j), size ** (2 * j))
            * z ** (k + j) / (k + j)
            for j in range(size - k)
        )
        answer += prefactor * integral
    return answer


def decimal(value: F) -> Decimal:
    return Decimal(value.numerator) / Decimal(value.denominator)


def asymptotic_coefficients(z_value: int) -> tuple[Decimal, Decimal, Decimal]:
    """Independently sum Psi_0, Psi_1, and the derived Psi_2 series."""
    z = Decimal(z_value)
    psi0 = Decimal(0)
    psi1 = Decimal(0)
    psi2 = Decimal(0)
    for k in range(250):
        weight = z ** k / Decimal(factorial(k) ** 2)
        psi0 += weight
        if k:
            first = -Decimal(k * k) + Decimal(k) * z / Decimal(k + 1)
            second = (
                Decimal(3 * k**4 - 2 * k**3 - k) / Decimal(6)
                - Decimal(k) * z
                + Decimal(k) * z * z / Decimal(2 * (k + 2))
                - Decimal(k**3) * z / Decimal(k + 1)
            )
            psi1 += weight * first
            psi2 += weight * second
        if k > 60 and abs(weight) < Decimal("1e-100"):
            break
    else:
        raise RuntimeError("coefficient series did not converge")
    return psi0, psi1, psi2


def compact(value: Decimal) -> str:
    return f"{value:.24f}"


def main() -> None:
    geometric_cases = (
        (F(2), F(1)),
        (F(3), F(2)),
        (F(7, 4), F(5)),
        (F(-2), F(4)),
    )
    geometry = []
    for theta, z in geometric_cases:
        margin = abs(theta) - 1
        require(margin > 0 and margin * z / 3 < 2, "case outside gap")
        boundary, boundary_vertices = direct_section_n3(theta, margin)
        rho = margin * (1 + z / 9)
        section, vertices = direct_section_n3(theta, rho)
        predicted_boundary = (3 * margin) ** 2 / 2
        ratio = section / boundary
        predicted_ratio = q_polynomial(3, z)
        require(boundary == predicted_boundary, "boundary formula failed")
        require(ratio == predicted_ratio, "direct polygon/Q_3 mismatch")
        geometry.append({
            "theta": str(theta),
            "z": str(z),
            "slack": str(margin * z / 3),
            "boundary_A3": str(boundary),
            "section_A3": str(section),
            "ratio": str(ratio),
            "Q3": str(predicted_ratio),
            "boundary_vertices": boundary_vertices,
            "section_vertices": vertices,
        })

    # Crossing the first opposite-tail threshold must invalidate Q_3.
    outside_theta = F(2)
    outside_z = F(7)
    outside_margin = outside_theta - 1
    outside_boundary, _ = direct_section_n3(outside_theta, outside_margin)
    outside_section, _ = direct_section_n3(
        outside_theta, outside_margin * (1 + outside_z / 9)
    )
    outside_ratio = outside_section / outside_boundary
    require(outside_ratio != q_polynomial(3, outside_z), "gap control failed")

    # Check the prefactor's independently derived first two coefficients.
    for k in range(1, 13):
        polynomial = [F(1)]
        for root in list(range(k)) + list(range(1, k + 1)):
            updated = [F(0)] * (len(polynomial) + 1)
            for degree, coefficient in enumerate(polynomial):
                updated[degree] += coefficient
                updated[degree + 1] -= root * coefficient
            polynomial = updated
        require(polynomial[1] == -k * k, "first prefactor coefficient")
        expected_second = F(3 * k**4 - 2 * k**3 - k, 6)
        require(polynomial[2] == expected_second, "second prefactor coefficient")

    asymptotics = []
    for z in (1, 2, 4):
        psi0, psi1, psi2 = asymptotic_coefficients(z)
        rows = []
        previous_error: Decimal | None = None
        for size in (32, 64, 128, 256):
            q = decimal(q_polynomial(size, F(z)))
            scaled = Decimal(size * size) * (
                q - psi0 - psi1 / Decimal(size)
            )
            error = abs(scaled - psi2)
            if previous_error is not None:
                require(error < previous_error, "second-order convergence failed")
            previous_error = error
            rows.append({
                "N": size,
                "N2_scaled_residual": compact(scaled),
                "error_from_Psi2": compact(error),
            })
        require(previous_error is not None and previous_error < Decimal("0.35"),
                "second-order residual too large")
        asymptotics.append({
            "z": z,
            "Psi0": compact(psi0),
            "Psi1": compact(psi1),
            "Psi2_derived": compact(psi2),
            "finite_N": rows,
        })

    record = dumps({
        "status": "INDEPENDENT_RAY_BOUNDARY_REVIEW_PASSED",
        "method": "exact rational H-polytope sections plus independent Psi2 series",
        "exact_N3_cases": geometry,
        "outside_gap": {
            "theta": str(outside_theta),
            "z": str(outside_z),
            "slack": str(outside_margin * outside_z / 3),
            "direct_ratio": str(outside_ratio),
            "Q3": str(q_polynomial(3, outside_z)),
            "different": True,
        },
        "prefactor_coefficients_checked_through_k": 12,
        "second_order_asymptotics": asymptotics,
    }, indent=2, sort_keys=True)
    digest = sha256(record.encode()).hexdigest()
    print(record)
    print(dumps({"record_sha256": digest}, sort_keys=True))


if __name__ == "__main__":
    main()
