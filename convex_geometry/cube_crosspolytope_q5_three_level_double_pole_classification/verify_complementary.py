#!/usr/bin/env python3
"""Standard-library verifier for 0<a<b<1 double-pole exclusion."""

from __future__ import annotations

from hashlib import sha256
from json import dumps, loads
from pathlib import Path

import verify as v
from verify_nonisolated import (
    ZERO,
    degree,
    divide_out,
    open_root_count,
    structural_rows,
)


def polynomial(entries) -> v.Poly:
    return v.poly(entries)


def polynomial_degree(value: v.Poly) -> int:
    return -1 if value == ZERO else degree(value)


def branch_data(a: v.Rat):
    d2 = a**8 + a**7 + 2 * a - 2
    d3 = a**9 + 2 * a**8 + a**7 + a**2 - 2 * a + 1
    d4 = 2 * a**8 + 2 * a**7 - a + 1
    s6 = sum((a**index for index in range(7)), v.Rat.constant(0))
    p2 = polynomial([4, -8, 4, 0, 0, 0, -6, -2, 2, 6, 0, 0, 0, 1, 2, 1])
    p3 = polynomial([-1, 4, -5, 0, 4, 0, -1, 1, -1, 1, 0, -4, 0, 5, 4, 1])
    return {
        "C1100": (
            (1, 1, 0, 0),
            -a * (a**7 + a**6 - 2 * a + 2) / d2,
            polynomial([-4, 8, -4, 0, 0, 0, -6, -6, -6, -6, 0, 0, 0, 1, 2, 1]),
            "no_open_unit_root",
            [],
        ),
        "C1101": (
            (1, 1, 0, 1),
            -a * (a**7 + a**6 + 2 * a - 2) / d2,
            p2,
            "beta_negative",
            [(v.F(27, 40), v.F(677, 1000)), (v.F(9, 10), v.F(901, 1000))],
        ),
        "C1110": (
            (1, 1, 1, 0),
            -a * (a**2 + 1) * (a**4 - a**2 + 1) / ((a - 1) * s6),
            polynomial([1, 0, -2, -1, 2, 2, 2, -1, -2, 0, 1]),
            "no_open_unit_root",
            [],
        ),
        "C2000": (
            (2, 0, 0, 0),
            a * (a**8 + 2 * a**7 + a**6 + a**2 - 2 * a + 1) / d3,
            polynomial([1, -4, 6, -4, 1, 0, 3, -1, -2, -2, -1, 3, 0, 1, 4, 6, 4, 1]),
            "no_open_unit_root",
            [],
        ),
        "C2001": (
            (2, 0, 0, 1),
            a * (a**2 + 1) * (a**2 + a - 1) * (a**4 + a**3 - a + 1) / d3,
            p3,
            "beta_negative",
            [(v.F(64, 125), v.F(513, 1000))],
        ),
        "C2010": (
            (2, 0, 1, 0),
            a * (2 * a**7 + 2 * a**6 - a + 1) / d4,
            polynomial([1, -2, 1, 0, 0, 0, 6, -6, 6, -6, 0, 0, 0, 4, 8, 4]),
            "no_open_unit_root",
            [],
        ),
    }


def candidate_patterns() -> set[tuple[int, int, int, int]]:
    answer = set()
    for ell in range(3):
        for h in range(2):
            for i in range(3):
                for g in range(2):
                    if ell + h == 0:
                        potentially_positive = False
                    elif (ell, h) in ((1, 1), (2, 0)):
                        potentially_positive = i <= 1 and not (i == 1 and g == 1)
                    else:
                        potentially_positive = False
                    if (ell + h) % 2 == 0 and potentially_positive:
                        answer.add((ell, h, i, g))
    return answer


def strip_branch_poles(quotient: v.Poly, denominator: v.Poly) -> v.Poly:
    answer = quotient
    while answer != ZERO:
        common = v.pgcd(answer, denominator)
        if degree(common) == 0:
            break
        answer, remainder = v.pdivmod(answer, common)
        v.require(remainder == ZERO, "branch-pole division")
    return answer


def main() -> None:
    directory = Path(__file__).resolve().parent
    certificate_bytes = (directory / "COMPLEMENTARY_CERTIFICATE.json").read_bytes()
    certificate = loads(certificate_bytes)
    canonical = dumps(certificate, sort_keys=True, separators=(",", ":"))
    certificate_hash = sha256(canonical.encode()).hexdigest()
    v.require(
        certificate["format"] == "q5-complementary-double-pole-exclusion-v1",
        "certificate format",
    )
    v.require(certificate["coefficient_order"] == "ascending", "coefficient order")
    v.require(certificate["parameter_domain"] == "0<a<b<1 and B>0", "domain")
    v.require(certificate["structural_rows"] == 33, "row count")
    v.require(certificate["pair_patterns_examined"] == 36, "pair count")

    candidates = candidate_patterns()
    v.require(len(candidates) == certificate["candidate_patterns"] == 6, "candidate count")
    a = v.Rat.variable()
    branches = branch_data(a)
    v.require(len(branches) == len(certificate["branches"]) == 6, "branch count")

    # Exceptional same-unit-supplier collision.  In the physical stratum
    # b=2a one has a<1/2; proving no H3 root on (0,1) is stronger.
    beta = 2 * a
    boundary = 4 * a**2 / (1 - a)
    rows = structural_rows(beta, boundary)
    target = 4 * a
    differences = {
        label: v.reduce_rat(wall - target) for label, wall, _coefficients in rows
    }
    triple_labels = sorted(label for label, difference in differences.items() if difference.is_zero())
    triple_record = certificate["exceptional_triple"]
    v.require(triple_record["condition"] == "b=2a", "triple condition")
    v.require(triple_labels == triple_record["rows"], "triple rows")
    row_map = {label: coefficients for label, _wall, coefficients in rows}
    triple_h3 = v.reduce_rat(
        sum((row_map[label].get(3, v.Rat.constant(0)) for label in triple_labels), v.Rat.constant(0))
    )
    triple_polynomial = polynomial(triple_record["H3_numerator"])
    v.require(
        v.pmonic(triple_h3.numerator) == v.pmonic(triple_polynomial),
        "triple H3 polynomial",
    )
    v.require(
        open_root_count(triple_polynomial) == triple_record["open_unit_roots"] == 0,
        "triple H3 roots",
    )

    all_factor_count = 0
    all_root_count = 0
    checked_differences = 0
    both_jet_cancellations = 0
    aggregate_h4_cancellations = 0
    maximum_degree = 0
    generic_root_total = 0
    branch_counts = {}

    for record in certificate["branches"]:
        name = record["name"]
        v.require(name in branches, f"unknown branch {name}")
        pattern, beta, eliminant, obstruction, intervals = branches[name]
        v.require(pattern in candidates and record["pattern"] == list(pattern), f"pattern {name}")
        v.require(
            v.pmonic(polynomial(record["generic_eliminant"])) == v.pmonic(eliminant),
            f"eliminant {name}",
        )
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
        v.require(generic == expected_generic == record["generic_rows"], f"generic rows {name}")
        checked_differences += len(rows) - len(generic)

        generic_h3 = v.reduce_rat(
            sum((row_map[label].get(3, v.Rat.constant(0)) for label in generic), v.Rat.constant(0))
        )
        v.require(generic_h3.is_zero(), f"generic H3 {name}")
        generic_h4 = v.reduce_rat(
            sum((row_map[label].get(4, v.Rat.constant(0)) for label in generic), v.Rat.constant(0))
        )
        quotient, remainder = v.pdivmod(generic_h4.numerator, eliminant)
        v.require(remainder == ZERO, f"generic H4 eliminant {name}")
        residual = strip_branch_poles(quotient, beta.denominator)
        v.require(open_root_count(residual) == 0, f"extra generic H4 root {name}")
        roots = open_root_count(eliminant)
        v.require(roots == record["generic_eliminant_roots"], f"generic roots {name}")
        v.require(obstruction == record["generic_root_obstruction"], f"obstruction {name}")
        if obstruction == "no_open_unit_root":
            v.require(roots == 0 and not intervals, f"root-free eliminant {name}")
        else:
            v.require(roots == len(intervals), f"isolating interval count {name}")
            for left, right in intervals:
                v.require(v.root_count(eliminant, left, right) == 1, f"root interval {name}")
                v.require(v.sign_at_root(beta, eliminant, left, right) < 0, f"negative beta {name}")
        generic_root_total += roots

        factors = [polynomial(item["polynomial"]) for item in record["factors"]]
        for left_index, left in enumerate(factors):
            v.require(v.peval(left, v.F(0)) != 0 and v.peval(left, v.F(1)) != 0, "factor endpoint")
            v.require(v.pgcd(left, v.pderivative(left)) == polynomial([1]), "factor squarefree")
            for right in factors[left_index + 1 :]:
                v.require(v.pgcd(left, right) == polynomial([1]), "overlapping factors")

        for item, factor in zip(record["factors"], factors):
            factor_roots = open_root_count(factor)
            v.require(degree(factor) == item["degree"], f"factor degree {name}")
            v.require(factor_roots == item["open_unit_roots"] > 0, f"factor roots {name}")
            colliding = []
            for label, difference in differences.items():
                if difference.is_zero():
                    colliding.append(label)
                    continue
                common = v.pgcd(factor, difference.numerator)
                if common != polynomial([1]):
                    v.require(v.pmonic(common) == v.pmonic(factor), f"partial overlap {name} {label}")
                    colliding.append(label)
            colliding.sort()
            v.require(colliding == item["colliding_rows"], f"colliding rows {name}")

            gcd_degrees = {}
            for jet in (3, 4):
                aggregate = v.reduce_rat(
                    sum(
                        (row_map[label].get(jet, v.Rat.constant(0)) for label in colliding),
                        v.Rat.constant(0),
                    )
                )
                common = v.pgcd(factor, aggregate.numerator)
                gcd_degrees[jet] = degree(common)
                v.require(
                    polynomial_degree(aggregate.numerator) == item[f"H{jet}_numerator_degree"],
                    f"aggregate degree H{jet} {name}",
                )
                v.require(
                    gcd_degrees[jet] == item[f"H{jet}_gcd_degree"],
                    f"aggregate gcd H{jet} {name}",
                )
            v.require(not (gcd_degrees[3] > 0 and gcd_degrees[4] > 0), f"both jets cancel {name}")
            both_jet_cancellations += int(gcd_degrees[3] > 0 and gcd_degrees[4] > 0)
            aggregate_h4_cancellations += int(gcd_degrees[4] > 0)

        for label, difference in differences.items():
            if difference.is_zero():
                continue
            residual = difference.numerator
            for factor in factors:
                residual = divide_out(residual, factor)
            v.require(open_root_count(residual) == 0, f"uncovered collision {name} {label}")

        factor_count = len(factors)
        root_count = sum(item["open_unit_roots"] for item in record["factors"])
        v.require(factor_count == record["collision_factor_count"], f"factor count {name}")
        v.require(root_count == record["collision_root_count"], f"collision roots {name}")
        branch_counts[name] = {
            "collision_factors": factor_count,
            "open_unit_roots": root_count,
        }
        all_factor_count += factor_count
        all_root_count += root_count
        maximum_degree = max([maximum_degree] + [item["degree"] for item in record["factors"]])

    payload = {
        "status": "Q5_COMPLEMENTARY_DOUBLE_POLE_WALLS_EXCLUSION_VERIFIED",
        "structural_rows": certificate["structural_rows"],
        "pair_patterns_examined": certificate["pair_patterns_examined"],
        "candidate_patterns": len(candidates),
        "leading_branches": len(branches),
        "generic_eliminant_roots": generic_root_total,
        "exceptional_triple_H3_roots": triple_record["open_unit_roots"],
        "row_differences_checked": checked_differences,
        "branch_counts": branch_counts,
        "collision_factors": all_factor_count,
        "open_unit_collision_roots": all_root_count,
        "aggregate_H4_cancellation_factors": aggregate_h4_cancellations,
        "factors_canceling_both_jets": both_jet_cancellations,
        "maximum_factor_degree": maximum_degree,
        "certificate_sha256": certificate_hash,
    }
    print(dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
