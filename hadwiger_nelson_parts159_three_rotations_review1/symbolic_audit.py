#!/usr/bin/env python3
"""Small SymPy audit of the algebraic reductions used by the continuum proof."""

import json
from pathlib import Path
import sympy as sp


def main() -> None:
    px, py, qx, qy, co, si = sp.symbols("px py qx qy co si")
    pnorm = px**2 + py**2
    qnorm = qx**2 + qy**2
    dot = px * qx + py * qy
    cross = py * qx - px * qy
    rotated_distance = (
        (px - (co * qx - si * qy)) ** 2
        + (py - (si * qx + co * qy)) ** 2
        - 1
    )
    contact_line = pnorm + qnorm - 1 - 2 * (co * dot + si * cross)
    remainder = sp.rem(
        sp.Poly(sp.expand(rotated_distance - contact_line), co),
        sp.Poly(co**2 + si**2 - 1, co),
    )
    if sp.expand(remainder.as_expr()) != 0:
        raise AssertionError("contact-line identity")

    S, np, nq = sp.symbols("S np nq")
    Delta = 4 * np * nq - S**2
    if sp.expand(S**2 + Delta - 4 * np * nq) != 0:
        raise AssertionError("unit-root norm identity")

    x, a, b, d = sp.symbols("x a b d")
    q = sp.symbols("q")
    root_product = sp.expand((x - (a + b * q)) * (x - (a - b * q)))
    root_reduced = sp.rem(sp.Poly(root_product, q), sp.Poly(q**2 - d, q)).as_expr()
    if sp.expand(root_reduced - (x**2 - 2 * a * x + a**2 - b**2 * d)) != 0:
        raise AssertionError("quadratic minimal-polynomial identity")

    # In a biquadratic compositum, conjugate(u)*v has all four basis
    # coefficients nonzero when both traces and both radical coefficients are
    # nonzero.  The three flip differences expose the exact coefficients that
    # would have to vanish for a nonidentity automorphism to fix the quotient.
    A, B, C, D, q1, q2 = sp.symbols("A B C D q1 q2", nonzero=True)
    relative = sp.expand((A + B * q1) * (C + D * q2))
    flips = {
        "first": relative.xreplace({q1: -q1}),
        "second": relative.xreplace({q2: -q2}),
        "both": relative.xreplace({q1: -q1, q2: -q2}),
    }
    expected = {
        "first": 2 * B * q1 * (C + D * q2),
        "second": 2 * D * q2 * (A + B * q1),
        "both": 2 * (B * C * q1 + A * D * q2),
    }
    for name, image in flips.items():
        if sp.expand(relative - image - expected[name]) != 0:
            raise AssertionError(f"biquadratic flip: {name}")

    result = {
        "all_symbolic_checks": True,
        "biquadratic_nonidentity_flips": 3,
        "contact_line_identity": True,
        "minimal_polynomial_identity": True,
        "sympy": sp.__version__,
        "unit_root_norm_identity": True,
    }
    expected = json.loads((Path(__file__).resolve().parent / "EXPECTED_SYMBOLIC.json").read_text())
    if result != expected:
        raise AssertionError("expected symbolic result mismatch")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
