#!/usr/bin/env python3
"""Produce the exact 800-system real-viability certificate with SymPy."""
from itertools import product
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import platform
import sys
import time

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SYMMETRY = ROOT / "hadwiger_nelson_three_wheel_symmetry_frontier"
SYMMETRY_CERTIFICATE_SHA256 = "14e2a5e3fc00af36d4ef57b6a8fdd964450633b0ab76f0f2783094172ec69132"
x, y, t = sp.symbols("x y t")


def need(condition, message):
    if not condition:
        raise ValueError(message)


def load_symmetry_verifier():
    sys.path.insert(0, str(SYMMETRY))
    spec = importlib.util.spec_from_file_location("hn_three_wheel_symmetry_verify", SYMMETRY / "verify.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def primitive(poly):
    poly = sp.Poly(poly, t, domain=sp.QQ)
    _, integral = poly.clear_denoms(convert=True)
    _, integral = integral.primitive()
    if integral.LC() < 0:
        integral = -integral
    return integral


def integers(poly):
    poly = primitive(poly)
    return [int(poly.nth(i)) for i in range(poly.degree() + 1)]


def rationals(poly):
    poly = sp.Poly(poly, t, domain=sp.QQ)
    return [str(poly.nth(i)) for i in range(poly.degree() + 1)]


def encoded_intervals(poly):
    return [[str(left), str(right)] for left, right in poly.intervals(sqf=True)]


def factor_expression(factor):
    return sum(coefficient * x**i * y**j for (i, j), coefficient in factor.items())


def shape(expression_left, expression_right):
    for shear in range(3):
        generators = [sp.expand(expression.subs(x, t - shear * y))
                      for expression in (expression_left, expression_right)]
        basis = [sp.Poly(row, y, t, domain=sp.QQ)
                 for row in sp.groebner(generators, y, t, order="lex", domain=sp.QQ).polys]
        if len(basis) == 1 and basis[0].total_degree() == 0:
            return shear, basis
        if len(basis) != 2 or basis[0].degree(y) != 1 or basis[1].degree(y) != 0:
            continue
        relation = sp.Poly(basis[0].as_expr(), y)
        coefficient = sp.Poly(relation.coeff_monomial(y), t, domain=sp.QQ)
        projection = sp.Poly(basis[1].as_expr(), t, domain=sp.QQ).sqf_part()
        if sp.gcd(coefficient, projection).degree() == 0:
            return shear, basis
    raise ValueError("no shape shear among 0,1,2")


def quotient_value(factor, xpowers, ypowers, modulus):
    value = sp.Poly(0, t, domain=sp.QQ)
    for (i, j), coefficient in factor.items():
        value += coefficient * xpowers[i] * ypowers[j]
    return sp.rem(value, modulus)


def qconstant(value):
    return sp.Poly(sp.Rational(value), t, domain=sp.QQ)


def qadd(left, right, modulus):
    return sp.rem(left + right, modulus)


def qmul(left, right, modulus):
    return sp.rem(left * right, modulus)


def cmul(left, right, modulus):
    # r+i sqrt(3)s representation.
    real = qadd(qmul(left[0], right[0], modulus),
                -3 * qmul(left[1], right[1], modulus), modulus)
    imag = qadd(qmul(left[0], right[1], modulus),
                qmul(left[1], right[0], modulus), modulus)
    return real, imag


def cadd(left, right, modulus):
    return qadd(left[0], right[0], modulus), qadd(left[1], right[1], modulus)


def phi(value, modulus):
    denominator = qadd(qconstant(1), 3 * qmul(value, value, modulus), modulus)
    inverse = sp.invert(denominator, modulus)
    real = qmul(qadd(qconstant(1), -3 * qmul(value, value, modulus), modulus), inverse, modulus)
    imag = qmul(2 * value, inverse, modulus)
    return real, imag


def eisenstein(pair):
    a, b = pair
    return qconstant(sp.Rational(2 * a + b, 2)), qconstant(sp.Rational(b, 2))


def collision_witness(source, xvalue, yvalue, modulus):
    U, V = phi(xvalue, modulus), phi(yvalue, modulus)
    nonzero = [difference for difference in source.D if difference != (0, 0)]
    rows = sorted({source.canonical(row) for row in product(nonzero, repeat=3)})
    need(len(rows) == 972, "collision row count")
    for d, e, f in rows:
        total = cadd(eisenstein(d),
                     cadd(cmul(U, eisenstein(e), modulus),
                          cmul(V, eisenstein(f), modulus), modulus), modulus)
        if total[0].is_zero and total[1].is_zero:
            return [list(d), list(e), list(f)]
    return None


def produce():
    symmetry_bytes = (SYMMETRY / "certificate.json").read_bytes()
    need(hashlib.sha256(symmetry_bytes).hexdigest() == SYMMETRY_CERTIFICATE_SHA256,
         "symmetry certificate hash")
    symmetry_certificate = json.loads(symmetry_bytes)
    symmetry = load_symmetry_verifier()
    source, factors, active, words, cover = symmetry.source_state()
    alignment = symmetry.alignment_ids(factors)
    pairs = symmetry_certificate["pair_orbit_representatives"]
    need(len(pairs) == 800, "representative pair count")
    expressions = [factor_expression(factor) for factor in factors]

    pair_rows = []
    for pair_index, (left, right) in enumerate(pairs):
        shear, basis = shape(expressions[left], expressions[right])
        if len(basis) == 1:
            pair_rows.append({"pair": [left, right], "shear": shear, "components": []})
            continue

        relation = sp.Poly(basis[0].as_expr(), y)
        A = sp.Poly(relation.coeff_monomial(y), t, domain=sp.QQ)
        B = sp.Poly(relation.coeff_monomial(1), t, domain=sp.QQ)
        projection = sp.Poly(basis[1].as_expr(), t, domain=sp.QQ).sqf_part()
        projection_integral = primitive(projection)
        components = []
        for component, exponent in sp.factor_list(projection)[1]:
            need(exponent == 1, "squarefree factor exponent")
            component = primitive(component)
            intervals = encoded_intervals(component)
            row = {"polynomial": integers(component), "intervals": intervals}
            if not intervals:
                row["outcome"] = "no_real_roots"
                components.append(row)
                continue

            inverse_A = sp.invert(A, component)
            yvalue = sp.rem(-B * inverse_A, component)
            xvalue = sp.rem(sp.Poly(t, t) - shear * yvalue, component)
            xpowers = [sp.Poly(1, t), xvalue, sp.rem(xvalue * xvalue, component)]
            ypowers = [sp.Poly(1, t), yvalue, sp.rem(yvalue * yvalue, component)]
            cache = {}

            def value(factor_id):
                if factor_id not in cache:
                    cache[factor_id] = quotient_value(
                        factors[factor_id], xpowers, ypowers, component)
                return cache[factor_id]

            aligned = [factor_id for factor_id in sorted(alignment) if value(factor_id).is_zero]
            if aligned:
                row.update({"outcome": "alignment", "alignment_factor_id": aligned[0]})
                components.append(row)
                continue

            failure_witnesses = []
            proper_word = None
            for word_index, word in enumerate(words):
                witness = next((factor_id for factor_id in sorted(word["bad"])
                                if value(factor_id).is_zero), None)
                if witness is None:
                    proper_word = word_index
                    break
                failure_witnesses.append(witness)
            if proper_word is not None:
                row.update({"outcome": "proper_word", "proper_word_index": proper_word})
                components.append(row)
                continue

            collision = collision_witness(source, xvalue, yvalue, component)
            if collision is not None:
                row.update({"outcome": "collision", "collision_displacements": collision})
                components.append(row)
                continue

            zero = [factor_id for factor_id in range(len(factors)) if value(factor_id).is_zero]
            row.update({"outcome": "survivor", "zero_factor_ids": zero,
                        "failure_factor_ids": failure_witnesses})
            components.append(row)

        pair_rows.append({
            "pair": [left, right],
            "shear": shear,
            "relation_a": rationals(A),
            "relation_b": rationals(B),
            "squarefree_projection": integers(projection_integral),
            "components": components,
        })

    return {
        "schema": "hn-three-wheel-exact-viability-v1",
        "source_symmetry_certificate_sha256": SYMMETRY_CERTIFICATE_SHA256,
        "coordinate_convention": "t=x+shear*y; A(t)*y+B(t)=0",
        "pair_rows": pair_rows,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    certificate = produce()
    encoded = (json.dumps(certificate, separators=(",", ":"), sort_keys=True) + "\n").encode()
    (args.out / "certificate.json").write_bytes(encoded)
    outcomes = {}
    real_embeddings = 0
    survivor_embeddings = 0
    for pair in certificate["pair_rows"]:
        for component in pair["components"]:
            outcome = component["outcome"]
            outcomes[outcome] = outcomes.get(outcome, 0) + 1
            real_embeddings += len(component["intervals"])
            if outcome == "survivor":
                survivor_embeddings += len(component["intervals"])
    receipt = {
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "pair_systems": len(certificate["pair_rows"]),
        "component_outcomes": dict(sorted(outcomes.items())),
        "real_embeddings": real_embeddings,
        "survivor_embeddings": survivor_embeddings,
        "certificate_bytes": len(encoded),
        "certificate_sha256": hashlib.sha256(encoded).hexdigest(),
        "elapsed_seconds": time.monotonic() - start,
        "chromatic_solver_calls": 0,
    }
    (args.out / "GENERATION.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(receipt, indent=2, sort_keys=True))
