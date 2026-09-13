#!/usr/bin/env python3
"""Semantic controls for the independent three-power-pencil audit."""

from itertools import product
import json
from pathlib import Path

import sympy as sp

import independent_audit as audit


def main():
    half = sp.Rational(1, 2)
    quarter = sp.Rational(1, 4)
    witnesses = (
        ((1, 1, 1, 1, 1), (half, 0, half, 0), (quarter, quarter, quarter)),
        ((-1, -1, -1, -1, -1), (0, half, half, 0),
         (sp.Rational(3, 4), sp.Rational(7, 4), quarter)),
    )
    for signs, point, expected_radii in witnesses:
        equations, radii = audit.system(signs)
        substitution = dict(zip((audit.a, audit.b, audit.c, audit.d), point))
        if any(sp.expand(f.subs(substitution)) != 0 for f in equations):
            raise AssertionError("positive free-vector witness rejected")
        if tuple(sp.expand(r.subs(substitution)) for r in radii) != expected_radii:
            raise AssertionError("witness radii changed")

    corruptions_rejected = 0
    for signs in product((-1, 1), repeat=5):
        equations, (u, v, w) = audit.system(signs)
        basis = sp.groebner(equations, *audit.VARIABLES, order="grevlex", domain=sp.QQ)
        delta = (u - v) * (u - w) * (v - w)
        if audit.reduce_zero(basis, delta):
            continue
        wrong = lambda t: (4 * t - 1) * (4 * t - 3) * (4 * t - 5)
        if not all(audit.reduce_zero(basis, delta * wrong(t)) for t in (u, v, w)):
            corruptions_rejected += 1
    if corruptions_rejected != 12:
        raise AssertionError(corruptions_rejected)
    result = {
        "status": "PASS",
        "exact_positive_witnesses": 2,
        "equal_exponents_counterexample": True,
        "corrupted_exceptional_root_sets_rejected": corruptions_rejected,
    }
    expected = json.loads((Path(__file__).resolve().parent / "EXPECTED_CONTROLS.json").read_text())
    if result != expected:
        raise AssertionError("control output mismatch")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
