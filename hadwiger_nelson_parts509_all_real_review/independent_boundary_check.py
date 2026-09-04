#!/usr/bin/env python3
"""Independent boundary audit for the all-real Parts-509 rotation closure.

This checker deliberately uses SymPy's generic number-field embedding test,
not the target verifier's recursive multiquadratic square-root routine.  It
reuses the target's exact event-line enumerator, so it audits the field-
membership boundary rather than independently reconstructing the coordinates
or event lines.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

import sympy
from sympy.polys.polyerrors import IsomorphismFailed


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
TARGET = REPOSITORY / "hadwiger_nelson_parts509_all_real_rotations"
ROTATIONS = REPOSITORY / "hadwiger_nelson_parts509_rotation_scan"

sys.path.insert(0, str(TARGET))
import common  # noqa: E402


RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
THETA = sympy.sqrt(3) + sympy.sqrt(5) + sympy.sqrt(11)


def as_sympy(value: tuple[Fraction, ...]) -> sympy.Expr:
    """Convert the target's fixed basis to a generic SymPy expression."""
    return sum(
        sympy.Rational(coefficient.numerator, coefficient.denominator)
        * sympy.sqrt(radical)
        for coefficient, radical in zip(value, RADICANDS)
        if coefficient
    )


def generic_square_in_k(value: tuple[Fraction, ...]) -> bool:
    """Decide whether sqrt(value) lies in K using a generic embedding test."""
    try:
        root = sympy.to_number_field(sympy.sqrt(as_sympy(value)), THETA)
    except IsomorphismFailed:
        return False
    difference = sympy.to_number_field(root.as_expr() ** 2 - as_sympy(value), THETA)
    # AlgebraicNumber.is_zero is intentionally tri-valued and returns None for
    # this exact zero representation in SymPy 1.14.  Inspect the exact ANP
    # coefficients instead.
    return all(coefficient == 0 for coefficient in difference.native_coeffs())


def coincidence_rotations(points, radii):
    """Enumerate exact rotations at which an L label equals an S label."""
    rotations = set()
    for p in range(common.L_SIZE):
        px, py = points[p]
        for q in range(common.L_SIZE, common.N):
            if radii[p] != radii[q] or radii[q] == common.ZERO:
                continue
            qx, qy = points[q]
            c = common.f_div(
                common.f_add(common.f_mul(px, qx), common.f_mul(py, qy)),
                radii[q],
            )
            s = common.f_div(
                common.f_sub(common.f_mul(py, qx), common.f_mul(px, qy)),
                radii[q],
            )
            if common.f_add(common.f_sq(c), common.f_sq(s)) != common.ONE:
                raise AssertionError("coincidence candidate is not a rotation")
            if (
                common.f_sub(common.f_mul(c, qx), common.f_mul(s, qy)),
                common.f_add(common.f_mul(s, qx), common.f_mul(c, qy)),
            ) != (px, py):
                raise AssertionError("coincidence formula failed")
            rotations.add((c, s))
    return rotations


def reflection_fixed_points(points) -> int:
    """Check J(L)=L for J=diag(-1,1) and return the number fixed by J."""
    large = set(points[: common.L_SIZE])
    reflected = {(tuple(-x for x in px), py) for px, py in large}
    if reflected != large:
        raise AssertionError("the large gadget is not reflection-invariant")
    return sum(px == common.ZERO for px, _py in large)


def main() -> None:
    certificate = json.loads((TARGET / "certificate.json").read_text())
    points = common.parse_points(common.POINTS)
    classes, discriminants, _invariant, _stats, radii = common.enumerate_line_classes(points)

    distinct_discriminants = sorted(set(discriminants.values()))
    membership = {
        value: generic_square_in_k(value) for value in distinct_discriminants
    }
    generic_k_lines = {
        key for key, value in discriminants.items() if membership[value]
    }

    rotation_certificate = json.loads(common.ROTATION_CERTIFICATE.read_text())
    prior_k_lines = {
        common.normalized_line(points, radii, u, v)
        for event in rotation_certificate["events"]
        for u, v in event["event_cross_edges"]
    }
    if generic_k_lines != prior_k_lines:
        raise AssertionError("generic field-membership split disagrees entry-by-entry")

    non_k_lines = set(classes) - generic_k_lines
    if common.line_digest(non_k_lines) != certificate["nonk_line_key_sha256"]:
        raise AssertionError("non-K line digest mismatch")
    if any(discriminants[key] == common.ZERO for key in non_k_lines):
        raise AssertionError("a non-K line was tangent to the unit circle")

    coincidences = coincidence_rotations(points, radii)
    fixed = reflection_fixed_points(points)

    print(f"unique_admissible_discriminants={len(distinct_discriminants)}")
    print(f"generic_k_discriminants={sum(membership.values())}")
    print(f"generic_nonk_discriminants={len(membership) - sum(membership.values())}")
    print(f"generic_k_line_classes={len(generic_k_lines)}")
    print(f"generic_nonk_line_classes={len(non_k_lines)}")
    print(f"coincidence_rotations={len(coincidences)}")
    print(f"reflection_fixed_L_points={fixed}")
    print("entrywise_classifier_match=true")
    print("independent_boundary_checks=true")


if __name__ == "__main__":
    main()
