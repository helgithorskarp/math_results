#!/usr/bin/env python3
"""Independent exact checks for the prime-index Ehrhart Fourier formula.

The target inverts cyclotomic elements by solving a dense linear system and
tests one-bad-face simplex products.  Here

    1/(1-zeta^a) = -(1/p) sum_{r=1}^{p-1} r zeta^(a r)

provides every reciprocal without field inversion, and shifted slack-box
parallelograms exercise four simultaneously bad faces with different
normalized characters.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import product


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def zero(p: int) -> tuple[Fraction, ...]:
    return (Fraction(0),) * (p - 1)


def one(p: int) -> tuple[Fraction, ...]:
    return (Fraction(1),) + (Fraction(0),) * (p - 2)


def add(
    left: tuple[Fraction, ...], right: tuple[Fraction, ...]
) -> tuple[Fraction, ...]:
    return tuple(a + b for a, b in zip(left, right))


def scale(
    scalar: Fraction, value: tuple[Fraction, ...]
) -> tuple[Fraction, ...]:
    return tuple(scalar * coefficient for coefficient in value)


def reduce_cyclotomic(coefficients: list[Fraction], p: int) -> tuple[Fraction, ...]:
    """Reduce modulo zeta^p=1 and 1+zeta+...+zeta^(p-1)=0."""
    cyclic = [Fraction(0)] * p
    for exponent, coefficient in enumerate(coefficients):
        cyclic[exponent % p] += coefficient
    top = cyclic[-1]
    return tuple(cyclic[index] - top for index in range(p - 1))


def zeta_power(exponent: int, p: int) -> tuple[Fraction, ...]:
    coefficients = [Fraction(0)] * (exponent % p + 1)
    coefficients[exponent % p] = 1
    return reduce_cyclotomic(coefficients, p)


def multiply(
    left: tuple[Fraction, ...], right: tuple[Fraction, ...], p: int
) -> tuple[Fraction, ...]:
    raw = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            raw[i + j] += a * b
    return reduce_cyclotomic(raw, p)


def reciprocal_one_minus(exponent: int, p: int) -> tuple[Fraction, ...]:
    """Return (1-zeta^exponent)^(-1) from a finite differentiated sum."""
    require(exponent % p != 0, "the reciprocal requires a nonzero exponent")
    answer = zero(p)
    for r in range(1, p):
        answer = add(answer, scale(Fraction(-r, p), zeta_power(exponent * r, p)))
    return answer


def profile_factor(
    profile: tuple[int, ...], h: int, p: int
) -> tuple[Fraction, ...]:
    answer = one(p)
    for entry in profile:
        answer = multiply(answer, reciprocal_one_minus(h * entry, p), p)
    return answer


def dft(
    values: list[Fraction], h: int, p: int
) -> tuple[Fraction, ...]:
    answer = zero(p)
    for residue, value in enumerate(values):
        answer = add(answer, scale(value, zeta_power(h * residue, p)))
    return scale(Fraction(1, p), answer)


def dft_cyclotomic(
    values: list[tuple[Fraction, ...]], h: int, p: int
) -> tuple[Fraction, ...]:
    answer = zero(p)
    for residue, value in enumerate(values):
        answer = add(answer, multiply(value, zeta_power(h * residue, p), p))
    return scale(Fraction(1, p), answer)


def polynomial_multiply(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def interpolate_quadratic(points: list[tuple[int, int]]) -> list[Fraction]:
    """Quadratic Lagrange interpolation, independent of a Vandermonde solve."""
    require(len(points) == 3, "three points are required")
    result = [Fraction(0), Fraction(0), Fraction(0)]
    for i, (x_i, y_i) in enumerate(points):
        basis = [Fraction(1)]
        denominator = 1
        for j, (x_j, _) in enumerate(points):
            if i == j:
                continue
            basis = polynomial_multiply(basis, [Fraction(-x_j), Fraction(1)])
            denominator *= x_i - x_j
        for degree, coefficient in enumerate(basis):
            result[degree] += Fraction(y_i, denominator) * coefficient
    return result


def shifted_box_count(p: int, a: int, lower: int, b: int, n: int) -> int:
    """Count (u,v) in [0,an] x [lower*n,(lower+b)*n], v=u mod p."""
    return sum(
        1
        for u in range(a * n + 1)
        for v in range(lower * n, (lower + b) * n + 1)
        if (v - u) % p == 0
    )


def corner_profiles(p: int, a: int, lower: int, b: int) -> list[tuple[int, int]]:
    """Normalized active characters for the four shifted-box corners."""
    # Each pair is (sign on u-row, sign on v-row, rhs_u, rhs_v).
    corners = [
        (-1, -1, 0, -lower),
        (-1, 1, 0, lower + b),
        (1, -1, a, -lower),
        (1, 1, a, lower + b),
    ]
    profiles = []
    for sign_u, sign_v, rhs_u, rhs_v in corners:
        epsilon = (sign_v % p, (-sign_u) % p)
        c = (epsilon[0] * rhs_u + epsilon[1] * rhs_v) % p
        require(c != 0, f"integral corner encountered for {(p, a, lower, b)}")
        c_inverse = pow(c, -1, p)
        eta = tuple(c_inverse * entry % p for entry in epsilon)
        require(all(eta), "normalized profile lost full support")
        # Scaling the annihilator cannot change eta.
        for scalar in range(1, p):
            scaled_c = scalar * c % p
            scaled = tuple(
                pow(scaled_c, -1, p) * scalar * entry % p
                for entry in epsilon
            )
            require(scaled == eta, "profile is not scalar invariant")
        profiles.append(eta)
    return profiles


def check_reciprocals() -> int:
    checks = 0
    for p in (2, 3, 5, 7, 11):
        for a in range(1, p):
            factor = add(one(p), scale(Fraction(-1), zeta_power(a, p)))
            require(
                multiply(factor, reciprocal_one_minus(a, p), p) == one(p),
                f"finite reciprocal identity failed for {(p, a)}",
            )
            checks += 1
    return checks


def check_local_filter() -> int:
    """Exhaust the normalized local DFT through p=7 and codimension four."""
    checks = 0
    for p in (2, 3, 5, 7):
        for g in range(1, 5):
            for tail in product(range(1, p), repeat=g - 1):
                epsilon = (1,) + tail
                q_by_a = {
                    scalar: profile_factor(
                        tuple(scalar * entry % p for entry in epsilon), 1, p
                    )
                    for scalar in range(1, p)
                }
                for c in range(1, p):
                    local_values = []
                    for n in range(p):
                        value = zero(p)
                        for scalar, q_value in q_by_a.items():
                            phase = zeta_power(-scalar * n * c, p)
                            value = add(value, multiply(phase, q_value, p))
                        local_values.append(scale(Fraction(1, p), value))
                    for h in range(1, p):
                        selected = h * pow(c, -1, p) % p
                        predicted = scale(Fraction(1, p), q_by_a[selected])
                        require(
                            dft_cyclotomic(local_values, h, p) == predicted,
                            f"local character selection failed for {(p, g, epsilon, c, h)}",
                        )
                        checks += 1
    return checks


def check_shifted_boxes() -> tuple[int, int, int, dict[str, list[list[int]]]]:
    fixtures = (
        (3, 3, 1, 3),
        (5, 2, 1, 2),
        (7, 2, 1, 3),
        (11, 3, 2, 4),
    )
    residue_polynomials = 0
    mode_checks = 0
    holdouts = 0
    recorded_profiles: dict[str, list[list[int]]] = {}
    for p, a, lower, b in fixtures:
        profiles = corner_profiles(p, a, lower, b)
        recorded_profiles[str(p)] = [list(profile) for profile in profiles]
        coefficients: list[list[Fraction]] = []
        for residue in range(p):
            points = [
                (n, shifted_box_count(p, a, lower, b, n))
                for n in (residue, residue + p, residue + 2 * p)
            ]
            polynomial = interpolate_quadratic(points)
            n = residue + 3 * p
            reconstructed = sum(
                polynomial[degree] * n**degree for degree in range(3)
            )
            require(
                reconstructed == shifted_box_count(p, a, lower, b, n),
                f"shifted-box holdout failed for {(p, residue)}",
            )
            require(polynomial[2] == Fraction(a * b, p), "area coefficient mismatch")
            coefficients.append(polynomial)
            residue_polynomials += 1
            holdouts += 1
        require(
            len({polynomial[1] for polynomial in coefficients}) == 1,
            f"an integral-affine edge produced a varying linear coefficient at p={p}",
        )
        constant_terms = [polynomial[0] for polynomial in coefficients]
        for h in range(1, p):
            predicted = zero(p)
            for profile in profiles:
                predicted = add(predicted, profile_factor(profile, h, p))
            predicted = scale(Fraction(1, p), predicted)
            require(
                dft(constant_terms, h, p) == predicted,
                f"four-face Fourier formula failed for {(p, h)}",
            )
            mode_checks += 1
    return residue_polynomials, mode_checks, holdouts, recorded_profiles


def check_diagonal_profile_sum() -> tuple[int, dict[str, str]]:
    """Prove computationally the exact sum used by the codimension-two refinement."""
    checks = 0
    values: dict[str, str] = {}
    for p in (2, 3, 5, 7, 11):
        total = zero(p)
        for a in range(1, p):
            total = add(total, profile_factor((a, a), 1, p))
        scalar = Fraction((p - 1) * (5 - p), 12)
        require(total == scale(scalar, one(p)), f"diagonal sum failed at p={p}")
        values[str(p)] = str(scalar)
        checks += 1
    require(values["5"] == "0", "the p=5 codimension-two cancellation vanished")
    return checks, values


def verify() -> dict[str, object]:
    reciprocal_checks = check_reciprocals()
    local_filter_checks = check_local_filter()
    residue_polynomials, box_modes, holdouts, profiles = check_shifted_boxes()
    diagonal_checks, diagonal_values = check_diagonal_profile_sum()
    record: dict[str, object] = {
        "arithmetic": "exact Fraction arithmetic in Q[zeta_p]",
        "cyclotomic_reciprocal_checks": reciprocal_checks,
        "local_filter_mode_checks": local_filter_checks,
        "shifted_box": {
            "fixtures": 4,
            "residue_polynomials": residue_polynomials,
            "unused_count_values": holdouts,
            "four_face_mode_checks": box_modes,
            "profiles": profiles,
        },
        "diagonal_profile_sum": {
            "checks": diagonal_checks,
            "values": diagonal_values,
            "p5_g2_cancellation": True,
        },
    }
    payload = json.dumps(record, sort_keys=True, separators=(",", ":"))
    record["record_sha256"] = hashlib.sha256(payload.encode()).hexdigest()
    return record


def main() -> None:
    print(json.dumps(verify(), sort_keys=True, separators=(",", ":")))
    print("VERIFIED independent prime-index Fourier audit")


if __name__ == "__main__":
    main()
