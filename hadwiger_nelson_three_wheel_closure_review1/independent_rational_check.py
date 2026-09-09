#!/usr/bin/env python3
"""Reviewer-1 exact-Q audit of the h4085 three-wheel closure certificate.

This deliberately does not use the target verifier's resultant, quotient,
finite-field, multiplication-matrix, or norm implementations.  SymPy derives
the elimination and triangular relations.  A small local polynomial engine
then checks every claimed colour action directly over Q, so the certificate's
277,244 modular unit witnesses are not trusted.

The geometric input reconstruction is imported from the pinned h4085 input
adapter.  The accompanying review records that interface as an explicit trust
boundary and separately replays its h4065/h4071 dependencies.
"""

from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import sys

import sympy as s


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "hadwiger_nelson_three_wheel_closure"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def trim(poly):
    poly = list(poly)
    while poly and not poly[-1]:
        poly.pop()
    return tuple(poly)


def add(left, right, sign=1):
    return trim(
        (left[i] if i < len(left) else F(0))
        + sign * (right[i] if i < len(right) else F(0))
        for i in range(max(len(left), len(right)))
    )


def mul(left, right):
    if not left or not right:
        return ()
    out = [F(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return trim(out)


def monic(poly):
    poly = trim(map(F, poly))
    need(poly, "zero polynomial cannot be monic")
    return tuple(c / poly[-1] for c in poly)


def divmod_poly(dividend, divisor):
    divisor = trim(divisor)
    need(divisor, "polynomial division by zero")
    remainder = list(trim(dividend))
    quotient = [F(0)] * max(0, len(remainder) - len(divisor) + 1)
    while len(remainder) >= len(divisor):
        shift = len(remainder) - len(divisor)
        coefficient = remainder[-1] / divisor[-1]
        quotient[shift] += coefficient
        for j, value in enumerate(divisor):
            remainder[shift + j] -= coefficient * value
        remainder = list(trim(remainder))
    return trim(quotient), trim(remainder)


def rem(poly, modulus):
    return divmod_poly(poly, modulus)[1]


def gcd_poly(left, right):
    left, right = trim(left), trim(right)
    while right:
        left, right = right, rem(left, right)
    return monic(left) if left else ()


def quotient_add(left, right, modulus, sign=1):
    return rem(add(left, right, sign), modulus)


def quotient_mul(left, right, modulus):
    return rem(mul(left, right), modulus)


def sympy_coefficients(expression, variable):
    polynomial = s.Poly(expression, variable, domain=s.QQ)
    if polynomial.is_zero:
        return ()
    return trim(
        F(int(polynomial.nth(i).p), int(polynomial.nth(i).q))
        for i in range(polynomial.degree() + 1)
    )


def decode_h(encoded):
    return tuple(trim(F(value) for value in coefficient) for coefficient in encoded)


def multiply_y(left, right, modulus):
    out = [()] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] = quotient_add(out[i + j], quotient_mul(a, b, modulus), modulus)
    while out and not out[-1]:
        out.pop()
    return tuple(out)


def factor_is_unit(coefficients, h, modulus):
    # coefficient[3*i+j] is the coefficient of x^i y^j.
    c, b, a = [
        trim(F(coefficients[3 * i + j]) for i in range(3))
        for j in range(3)
    ]
    if len(h) == 2:
        root = tuple(-value for value in h[0])
        value = quotient_add(
            quotient_mul(quotient_add(quotient_mul(a, root, modulus), b, modulus), root, modulus),
            c,
            modulus,
        )
    else:
        need(len(h) == 3, "colour action has unsupported y degree")
        v, u = h[:2]
        c = quotient_add(c, quotient_mul(a, v, modulus), modulus, -1)
        b = quotient_add(b, quotient_mul(a, u, modulus), modulus, -1)
        # determinant of multiplication by c+b*y in
        # (Q[x]/r)[y]/(y^2+u*y+v)
        value = quotient_add(
            quotient_add(
                quotient_mul(c, c, modulus),
                quotient_mul(u, quotient_mul(b, c, modulus), modulus),
                modulus,
                -1,
            ),
            quotient_mul(v, quotient_mul(b, b, modulus), modulus),
            modulus,
        )
    return gcd_poly(modulus, value) == (F(1),)


def triangular_relation(f, g, r_expression, x, y):
    basis = s.groebner([f, g, r_expression], y, x, domain=s.QQ)
    expressions = [polynomial.as_expr() for polynomial in basis.polys]
    if expressions == [1]:
        return ((F(1),),)
    with_y = [expression for expression in expressions if expression.has(y)]
    need(len(with_y) == 1, "Groebner basis does not have one triangular y relation")
    hp = s.Poly(with_y[0], y)
    need(hp.LC() == 1, "triangular relation is not monic in y")
    return tuple(sympy_coefficients(hp.nth(j), x) for j in range(hp.degree() + 1))


def run(certificate_path):
    sys.path.insert(0, str(TARGET))
    import inputs  # pylint: disable=import-error,import-outside-toplevel

    certificate_bytes = certificate_path.read_bytes()
    certificate = json.loads(certificate_bytes)
    need(certificate.get("version") == 1, "certificate version")
    _, coefficients, pairs, allowed, base_edges, inventory = inputs.load()
    need(len(pairs) == len(certificate["systems"]) == 800, "800-system interface")

    words = certificate["words"]
    need(len(words) == len(set(words)) == 62, "62 distinct colour words")
    bad_words = []
    for word in words:
        need(type(word) is str and len(word) == 343 and set(word) <= set("0123"), "colour word encoding")
        need(all(word[a] != word[b] for a, b in base_edges), "Cartesian edge is monochromatic")
        bad = set()
        for a, b, factor_ids in inventory:
            if word[a] == word[b]:
                bad.update(factor_ids)
        bad_words.append(bad & allowed)

    x, y = s.symbols("x y")
    factor_expressions = [
        sum(row[3 * i + j] * x**i * y**j for i in range(3) for j in range(3))
        for row in coefficients
    ]
    r_factors = [tuple(map(F, row)) for row in certificate["rfactors"]]
    need(len(r_factors) == len(set(r_factors)) == 687, "projection factor inventory")
    actions = certificate["actions"]

    cache = {}
    action_counts = Counter()
    resultant_degrees = Counter()
    rational_unit_checks = 0
    branch_count = 0
    relation_hash = hashlib.sha256()
    unit_hash = hashlib.sha256()

    def classify(r, h, action):
        nonlocal rational_unit_checks
        modulus = monic(r)
        key = (r, h)
        action_tag = json.dumps(action, sort_keys=True, separators=(",", ":"))
        if key in cache:
            need(cache[key] == action_tag, "inconsistent action for repeated quotient block")
            return
        if action == {"empty": True}:
            need(h == ((F(1),),), "false empty action")
            kind = "empty"
        elif action == {"no_real_x": True}:
            need(len(r) == 3 and r[1] * r[1] - 4 * r[0] * r[2] < 0, "false no-real-x action")
            kind = "no_real_x"
        elif action == {"no_real_y": True}:
            need(len(h) == 3 and all(len(coefficient) <= 1 for coefficient in h), "nonconstant no-real-y relation")
            b = h[1][0] if h[1] else F(0)
            c = h[0][0] if h[0] else F(0)
            need(b * b - 4 * c < 0, "false no-real-y action")
            kind = "no_real_y"
        elif set(action) == {"split"}:
            children = [(decode_h(child["h"]), child["action"]) for child in action["split"]]
            need(len(children) >= 2, "trivial split")
            product = ((F(1),),)
            for child_h, _ in children:
                need(1 < len(child_h) < len(h) and child_h[-1] == (F(1),), "invalid split child")
                product = multiply_y(product, child_h, modulus)
            need(product == h, "false split identity")
            for child_h, child_action in children:
                classify(r, child_h, child_action)
            kind = "split"
        elif set(action) == {"colour", "primes"}:
            word_index = action["colour"]
            need(type(word_index) is int and 0 <= word_index < len(words), "colour action index")
            # The listed primes are intentionally ignored: every unit is
            # established directly over Q below.
            for factor_id in sorted(bad_words[word_index]):
                need(factor_is_unit(coefficients[factor_id], h, modulus), f"nonunit bad factor {factor_id}")
                rational_unit_checks += 1
                unit_hash.update(f"{r!r},{h!r},{factor_id}\n".encode())
            kind = "colour"
        else:
            raise ValueError("unproved certificate action")
        cache[key] = action_tag
        action_counts[kind] += 1

    for system_index, ((a, b), rows) in enumerate(zip(pairs, certificate["systems"])):
        f, g = factor_expressions[a], factor_expressions[b]
        resultant = s.resultant(f, g, y)
        need(resultant != 0, "zero elimination resultant")
        product = s.Integer(1)
        seen = set()
        for r_index, multiplicity, _ in rows:
            need(type(r_index) is int and r_index not in seen and 0 <= r_index < len(r_factors), "projection index")
            need(type(multiplicity) is int and 1 <= multiplicity <= 8, "projection multiplicity")
            seen.add(r_index)
            r_expression = sum(value * x**i for i, value in enumerate(r_factors[r_index]))
            product *= r_expression**multiplicity
        resultant_poly = s.Poly(resultant, x, domain=s.QQ)
        product_poly = s.Poly(product, x, domain=s.QQ)
        need(resultant_poly.monic() == product_poly.monic(), "incomplete resultant factorization")
        resultant_degrees[resultant_poly.degree()] += 1

        for r_index, _, action_index in rows:
            need(type(action_index) is int and 0 <= action_index < len(actions), "action index")
            r = r_factors[r_index]
            r_expression = sum(value * x**i for i, value in enumerate(r))
            h = triangular_relation(f, g, r_expression, x, y)
            relation_hash.update(f"{system_index},{r!r},{h!r}\n".encode())
            classify(r, h, actions[action_index])
            branch_count += 1

    return {
        "status": "INDEPENDENT_EXACT_Q_CLOSURE_CHECK_PASSED",
        "target_certificate_sha256": hashlib.sha256(certificate_bytes).hexdigest(),
        "systems": len(pairs),
        "projection_branches": branch_count,
        "unique_quotient_blocks": len(cache),
        "action_counts": dict(sorted(action_counts.items())),
        "resultant_degree_histogram": {str(key): value for key, value in sorted(resultant_degrees.items())},
        "rational_unit_checks": rational_unit_checks,
        "relation_stream_sha256": relation_hash.hexdigest(),
        "rational_unit_stream_sha256": unit_hash.hexdigest(),
        "sympy": s.__version__,
        "modular_witnesses_trusted": False,
        "solver_calls": 0,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=TARGET / "certificate.json")
    parser.add_argument("--expected", type=Path)
    args = parser.parse_args()
    result = run(args.certificate)
    if args.expected:
        need(result == json.loads(args.expected.read_text()), "expected result mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))
