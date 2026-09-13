#!/usr/bin/env python3
"""Small exact and adversarial controls for the clean-room audit."""

from __future__ import annotations

import json
import tempfile
from fractions import Fraction as Q
from pathlib import Path

import independent_audit as audit


HERE = Path(__file__).resolve().parent


def reject(callable_, label):
    try:
        callable_()
    except (ValueError, json.JSONDecodeError):
        return
    raise ValueError(f"negative control unexpectedly passed: {label}")


def polynomial_controls():
    x, y = audit.pvar(0), audit.pvar(1)
    first = audit.padd(x, y, -1)
    second = audit.padd(x, y)
    basis, pairs = audit.buchberger([first, second])
    for target in (x, y):
        remainder, _ = audit.normal_form(target, basis)
        audit.need(not remainder, "linear ideal consequence")

    generators = [
        audit.padd(audit.pmul(x, x), y, -1),
        audit.padd(audit.pmul(x, y), audit.P_ONE, -1),
    ]
    basis, more_pairs = audit.buchberger(generators)
    cube_minus_one = audit.padd(audit.ppow(x, 3), audit.P_ONE, -1)
    remainder, _ = audit.normal_form(cube_minus_one, basis)
    audit.need(not remainder, "nonlinear ideal consequence")
    return pairs + more_pairs


def unit_controls():
    checks = 0
    for left in audit.UNITS:
        audit.need(audit.unorm(left) == 1, "unit norm")
        audit.need(
            audit.gf4_mul(audit.residue(left), audit.gf4_inverse(audit.residue(left))) == 1,
            "residue inverse",
        )
        for right in audit.UNITS:
            value = audit.umul(left, right)
            audit.need(value in audit.UNITS, "unit closure")
            audit.need(
                audit.residue(value)
                == audit.gf4_mul(audit.residue(left), audit.residue(right)),
                "residue homomorphism",
            )
            checks += 1
    return checks


def witness_controls():
    # Values use the audit monomial order (D,C,B,A).
    cases = (
        (
            (1, 1, 1, 1, 1),
            (Q(0), Q(1, 2), Q(0), Q(1, 2)),
            (Q(1, 4),) * 3,
        ),
        (
            (-1, -1, -1, -1, -1),
            (Q(0), Q(1, 2), Q(1, 2), Q(0)),
            (Q(3, 4), Q(7, 4), Q(1, 4)),
        ),
    )
    for signs, point, radii in cases:
        equations, norms = audit.equations(signs)
        audit.need(
            all(audit.peval(polynomial, point) == 0 for polynomial in equations),
            "free-vector witness",
        )
        audit.need(
            tuple(audit.peval(polynomial, point) for polynomial in norms) == radii,
            "witness radii",
        )
    return len(cases)


def residual_control(residual_path, pencils):
    data = json.loads(Path(residual_path).read_text())
    data["remaining_pencil_signatures"] = data["remaining_pencil_signatures"][:-1]
    with tempfile.NamedTemporaryFile("w", suffix=".json") as handle:
        json.dump(data, handle)
        handle.flush()
        reject(
            lambda: audit.a5_interface_audit(pencils, handle.name),
            "altered residual",
        )


def run(residual_path):
    normalization = audit.finite_normalization_audit()
    pencils = normalization.pop("pencils")
    residual_control(residual_path, pencils)
    result = {
        "status": "PASS",
        "buchberger_small_pair_checks": polynomial_controls(),
        "unit_ring_checks": unit_controls(),
        "free_vector_witnesses": witness_controls(),
        "altered_residuals_rejected": 1,
    }
    expected = json.loads(HERE.joinpath("EXPECTED_CONTROLS.json").read_text())
    audit.need(result == expected, "control output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--residual", type=Path, required=True)
    arguments = parser.parse_args()
    run(arguments.residual)
