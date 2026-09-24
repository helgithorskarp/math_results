#!/usr/bin/env python3
"""Standard-library verifier excluding non-isolated double-pole cancellations."""

from __future__ import annotations

from hashlib import sha256
from json import dumps, loads
from math import comb, factorial
from pathlib import Path

import verify as v


ZERO = v.poly([0])
ONE = v.poly([1])


def degree(polynomial: v.Poly) -> int:
    return len(polynomial) - 1


def open_root_count(polynomial: v.Poly) -> int:
    return v.root_count(v.strip_endpoint_roots(polynomial), v.F(0), v.F(1))


def row_coefficients_general(
    supplier: v.Rat,
    remaining: list[v.Rat],
    tails: list[v.Rat],
    boundary: v.Rat,
) -> dict[int, v.Rat]:
    """Rebuild all q=5 jets for a residual pole of multiplicity one or two."""
    size = len(remaining)
    multiplicity = remaining.count(supplier)
    v.require(multiplicity in (1, 2), "unexpected residual multiplicity")
    other = v.remove_n(remaining, supplier, multiplicity)
    t0 = v.reduce_rat(-(1 - supplier) / supplier)
    regularized_denominator = v.reduce_rat(
        (1 - t0) ** size
        * v.rat_product(remaining)
        * supplier**multiplicity
        * v.rat_product(1 - weight + weight * t0 for weight in other)
    )
    highest = v.reduce_rat(1 / regularized_denominator)
    principal_parts = [(multiplicity, highest)]
    if multiplicity == 2:
        logarithmic_derivative = v.reduce_rat(
            size / (1 - t0)
            - sum(
                (
                    v.reduce_rat(weight / (1 - weight + weight * t0))
                    for weight in other
                ),
                v.Rat.constant(0),
            )
        )
        principal_parts.append(
            (1, v.reduce_rat(highest * logarithmic_derivative))
        )

    states = []
    for order, coefficient in principal_parts:
        states.append(
            (
                v.reduce_rat(
                    coefficient
                    / (factorial(order - 1) * factorial(size - order))
                ),
                order - 1,
                v.Rat.constant(0),
                size - order,
            )
        )

    lam = (1 - supplier) / supplier
    for weight in tails:
        updated = []
        for coefficient, b_power, shift, slack_power in states:
            for moment in range(b_power + 1):
                eta = v.reduce_rat(
                    weight**moment / (1 + weight + lam * weight) ** (
                        moment + 1
                    )
                    - 1 / (weight * (1 + lam) ** (moment + 1))
                )
                beta_factor = v.F(
                    comb(b_power, moment)
                    * factorial(moment)
                    * factorial(slack_power),
                    factorial(moment + slack_power + 1),
                )
                updated.append(
                    (
                        v.reduce_rat(coefficient * eta * beta_factor),
                        b_power - moment,
                        v.reduce_rat(shift + 2 * weight),
                        slack_power + moment + 1,
                    )
                )
        states = updated

    answer: dict[int, v.Rat] = {}
    for coefficient, b_power, shift, slack_power in states:
        value = v.reduce_rat(coefficient * (boundary + shift) ** b_power)
        answer[slack_power] = v.reduce_rat(
            answer.get(slack_power, v.Rat.constant(0)) + value
        )
    expected = {3, 4} if multiplicity == 2 else {4}
    v.require(set(answer) == expected, "unexpected hinge support")
    return answer


def structural_rows(beta: v.Rat, boundary: v.Rat):
    a = v.Rat.variable()
    one = v.Rat.constant(1)
    original = [one, one, a, a, beta]
    rows = []

    for k in range(2):
        for ell in range(3):
            for h in range(2):
                tails = [one] * k + [a] * ell + [beta] * h
                remaining = v.remove_n(original, one, k)
                remaining = v.remove_n(remaining, a, ell)
                remaining = v.remove_n(remaining, beta, h)
                coefficients = row_coefficients_general(one, remaining, tails, boundary)
                multiplicity = comb(2, k) * comb(2, ell)
                rows.append(
                    (
                        f"U({k},{ell},{h})",
                        2 * (k + ell * a + h * beta),
                        {key: multiplicity * value for key, value in coefficients.items()},
                    )
                )

    for i in range(3):
        for j in range(2):
            for g in range(2):
                tails = [one] * i + [a] * j + [beta] * g
                remaining = v.remove_n(original, one, i)
                remaining = v.remove_n(remaining, a, j)
                remaining = v.remove_n(remaining, beta, g)
                coefficients = row_coefficients_general(a, remaining, tails, boundary)
                multiplicity = comb(2, i) * comb(2, j)
                rows.append(
                    (
                        f"A({i},{j},{g})",
                        (1 - a) * boundary / a
                        + 2 * (i + j * a + g * beta) / a,
                        {key: multiplicity * value for key, value in coefficients.items()},
                    )
                )

    for i in range(3):
        for ell in range(3):
            tails = [one] * i + [a] * ell
            remaining = v.remove_n(original, one, i)
            remaining = v.remove_n(remaining, a, ell)
            coefficients = row_coefficients_general(beta, remaining, tails, boundary)
            multiplicity = comb(2, i) * comb(2, ell)
            rows.append(
                (
                    f"b({i},{ell})",
                    (1 - beta) * boundary / beta + 2 * (i + ell * a) / beta,
                    {key: multiplicity * value for key, value in coefficients.items()},
                )
            )

    v.require(len(rows) == 33 and len({row[0] for row in rows}) == 33, "row census")
    return rows


def divide_out(dividend: v.Poly, divisor: v.Poly) -> v.Poly:
    answer = dividend
    while degree(answer) >= degree(divisor):
        quotient, remainder = v.pdivmod(answer, divisor)
        if remainder != ZERO:
            break
        answer = quotient
    return answer


def main() -> None:
    directory = Path(__file__).resolve().parent
    certificate_bytes = (directory / "COLLISION_CERTIFICATE.json").read_bytes()
    certificate = loads(certificate_bytes)
    canonical = dumps(certificate, sort_keys=True, separators=(",", ":"))
    certificate_hash = sha256(canonical.encode()).hexdigest()
    v.require(
        certificate["format"]
        == "q5-double-pole-nonisolated-collision-certificate-v1",
        "certificate format",
    )
    v.require(certificate["coefficient_order"] == "ascending", "coefficient order")
    v.require(certificate["parameter_interval"] == "0<a<1", "parameter interval")

    a = v.Rat.variable()
    d1 = a**6 - a**5 + a**4 - a**3 + a**2 - a + 1
    n1 = -a * (a - 1) * (a**2 - a + 1) * (a**2 + a + 1)
    d2 = a**8 + a**7 + 2 * a - 2
    n2 = a * (a**7 + a**6 + 2 * a - 2)
    d3 = a**9 + 2 * a**8 + a**7 + a**2 - 2 * a + 1
    n3 = a * (a**2 + 1) * (a**2 + a - 1) * (a**4 + a**3 - a + 1)
    d4 = 2 * a**8 + 2 * a**7 - a + 1
    n4 = a * (2 * a**7 + 2 * a**6 + a - 1)
    branch_data = {
        "B01": ((0, 1, 0, 0), n1 / d1),
        "B10": ((1, 0, 0, 0), n2 / d2),
        "B11": ((1, 1, 0, 1), -n2 / d2),
        "B20": ((2, 0, 0, 1), n3 / d3),
        "B201": ((2, 0, 1, 1), n4 / d4),
        "B21": ((2, 1, 0, 0), -n3 / d3),
        "B211": ((2, 1, 1, 0), -n4 / d4),
        "B212": ((2, 1, 2, 0), n1 / d1),
    }
    v.require(len(certificate["branches"]) == len(branch_data) == 8, "branch count")

    branch_counts = {}
    all_factor_count = 0
    all_root_count = 0
    maximum_degree = 0
    checked_differences = 0

    for record in certificate["branches"]:
        name = record["name"]
        v.require(name in branch_data, f"unknown branch {name}")
        pattern, beta = branch_data[name]
        v.require(record["pattern"] == list(pattern), f"pattern {name}")
        ell, h, i, g = pattern
        boundary = 2 * (a * (ell * a + h * beta) - (i + g * beta)) / (1 - a)
        target = 2 * (ell * a + h * beta)
        rows = structural_rows(beta, boundary)
        row_map = {label: coefficients for label, _wall, coefficients in rows}
        differences = {
            label: v.reduce_rat(wall - target) for label, wall, _coefficients in rows
        }
        generic = sorted(label for label, difference in differences.items() if difference.is_zero())
        expected_generic = sorted([f"U(0,{ell},{h})", f"A({i},0,{g})"])
        v.require(generic == expected_generic == record["generic_rows"], f"generic {name}")
        checked_differences += len(rows) - len(generic)

        leading = sum(
            (row_map[label][3] for label in generic), v.Rat.constant(0)
        )
        v.require(leading.is_zero(), f"leading cancellation {name}")

        factors = [v.poly(item["polynomial"]) for item in record["factors"]]
        for left_index, left in enumerate(factors):
            v.require(v.peval(left, v.F(0)) != 0 and v.peval(left, v.F(1)) != 0, "endpoint factor")
            v.require(v.pgcd(left, v.pderivative(left)) == ONE, "nonsquarefree factor")
            for right in factors[left_index + 1 :]:
                v.require(v.pgcd(left, right) == ONE, "overlapping collision factors")

        for item, polynomial in zip(record["factors"], factors):
            roots = open_root_count(polynomial)
            v.require(degree(polynomial) == item["degree"], f"factor degree {name}")
            v.require(roots == item["open_unit_roots"] > 0, f"factor roots {name}")
            colliding = []
            for label, difference in differences.items():
                if difference.is_zero():
                    colliding.append(label)
                    continue
                common = v.pgcd(polynomial, difference.numerator)
                if common != ONE:
                    v.require(
                        v.pmonic(common) == v.pmonic(polynomial),
                        f"partial factor overlap {name} {label}",
                    )
                    colliding.append(label)
            colliding.sort()
            v.require(colliding == item["colliding_rows"], f"colliding rows {name}")

            aggregate = v.reduce_rat(
                sum(
                    (row_map[label][4] for label in colliding),
                    v.Rat.constant(0),
                )
            )
            common = v.pgcd(polynomial, aggregate.numerator)
            v.require(common == ONE, f"aggregate cancellation {name}")
            v.require(
                degree(aggregate.numerator) == item["aggregate_numerator_degree"],
                f"aggregate degree {name}",
            )
            v.require(item["aggregate_gcd_degree"] == 0, "certificate gcd claim")

        # Coverage: after recorded factors are divided out, no wall difference
        # numerator has a root in the open unit interval.
        for label, difference in differences.items():
            if difference.is_zero():
                continue
            residual = difference.numerator
            for polynomial in factors:
                residual = divide_out(residual, polynomial)
            v.require(open_root_count(residual) == 0, f"uncovered collision {name} {label}")

        factor_count = len(factors)
        root_total = sum(item["open_unit_roots"] for item in record["factors"])
        v.require(factor_count == record["collision_factor_count"], f"count {name}")
        v.require(root_total == record["collision_root_count"], f"roots {name}")
        branch_counts[name] = {
            "collision_factors": factor_count,
            "open_unit_roots": root_total,
        }
        all_factor_count += factor_count
        all_root_count += root_total
        maximum_degree = max(
            [maximum_degree] + [item["degree"] for item in record["factors"]]
        )

    payload = {
        "status": "Q5_NONISOLATED_DOUBLE_POLE_WALLS_EXCLUSION_VERIFIED",
        "structural_rows": certificate["structural_rows"],
        "leading_branches": len(branch_data),
        "row_differences_checked": checked_differences,
        "branch_counts": branch_counts,
        "collision_factors": all_factor_count,
        "open_unit_collision_roots": all_root_count,
        "maximum_factor_degree": maximum_degree,
        "aggregate_cancellation_factors": 0,
        "certificate_sha256": certificate_hash,
    }
    print(dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
