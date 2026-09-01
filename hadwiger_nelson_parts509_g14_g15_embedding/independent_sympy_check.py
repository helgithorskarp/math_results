#!/usr/bin/env python3
"""Independent exact embedding check using SymPy's AlgebraicField.

This imports none of verify_embedding.py or the sibling field implementations.
It reparses the published Parts coordinates and all cited completion points into
QQ(sqrt(3),sqrt(5),sqrt(11)), then compares complete distance matrices.
"""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

import sympy
from sympy import QQ, Rational, sqrt, sympify

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = ROOT / "hadwiger_nelson_parts509_criticality"
SWAP = ROOT / "hadwiger_nelson_parts509_swap_closure"
RADICALS = [sympy.Integer(1), sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165)]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def split_pair(body):
    expr = body.replace("Sqrt[", "sqrt(").replace("]", ")")
    depth = 0
    for i, char in enumerate(expr):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            return expr[:i], expr[i + 1:]
    raise ValueError(body)


def main():
    cert = json.loads((HERE / "embedding_certificate.json").read_text())
    assert sha256(BASE / "parts509.vtx") == cert["parts_coordinate_sha256"]
    assert sha256(SWAP / "completion_points.json") == cert["completion_points_sha256"]
    field = QQ.algebraic_field(sqrt(3), sqrt(5), sqrt(11))
    one = field.one
    basis = [field.from_sympy(r) for r in RADICALS]

    def expression_to_field(text):
        expr = sympy.expand(sympy.sqrtdenest(sympify(text)))
        result = field.zero
        for term, coefficient in expr.as_coefficients_dict().items():
            if term not in RADICALS or not coefficient.is_Rational:
                raise ValueError(f"unexpected denested term {term}: {coefficient}")
            value = Rational(coefficient)
            result += field.from_sympy(value) * basis[RADICALS.index(term)]
        return result

    parts = []
    for line in (BASE / "parts509.vtx").read_text().splitlines():
        if not line.strip():
            continue
        a, b = split_pair(line.strip()[1:-1])
        parts.append((expression_to_field(a), expression_to_field(b)))
    assert len(parts) == 509 and len(set(parts)) == 509

    completion_doc = json.loads((SWAP / "completion_points.json").read_text())

    def coeffs(values):
        expr = sum(Rational(Fraction(c).numerator, Fraction(c).denominator) * r
                   for c, r in zip(values, RADICALS))
        return field.from_sympy(expr)

    qids = {index for records in cert["g14"]["embeddings"] for kind, index in records if kind == "Q3"}
    completion = {i: (coeffs(completion_doc["points"][i]["x"]), coeffs(completion_doc["points"][i]["y"]))
                  for i in qids}
    assert not (set(parts) & set(completion.values()))

    def canonical(row):
        a, b, c, d = map(Fraction, row)
        x = Rational(a.numerator, a.denominator) + Rational(b.numerator, b.denominator) * sqrt(3)
        y = Rational(c.numerator, c.denominator) + Rational(d.numerator, d.denominator) * sqrt(3)
        return field.from_sympy(x), field.from_sympy(y)

    def d2(a, b):
        dx, dy = a[0] - b[0], a[1] - b[1]
        return dx * dx + dy * dy

    objects = {name: [canonical(row) for row in cert[name]["coordinates"]] for name in ("g14", "g15")}
    for mapping in cert["g15"]["parts_embeddings"]:
        g15_images = [parts[i] for i in mapping]
        for i in range(15):
            for j in range(i + 1, 15):
                assert d2(objects["g15"][i], objects["g15"][j]) == d2(g15_images[i], g15_images[j])

    for records in cert["g14"]["embeddings"]:
        images = []
        for kind, index in records:
            images.append(parts[index] if kind == "V" else completion[index])
        assert len(set(images)) == 14
        for i in range(14):
            for j in range(i + 1, 14):
                assert d2(objects["g14"][i], objects["g14"][j]) == d2(images[i], images[j])

    neighborhoods = {}
    for qi in sorted(qids):
        neighbors = [i for i, point in enumerate(parts) if d2(completion[qi], point) == one]
        assert neighbors == completion_doc["points"][qi]["neighbors"]
        neighborhoods[str(qi)] = neighbors

    print(json.dumps({
        "independent_sympy_check": True,
        "parts_vertices": len(parts),
        "g15_complete_distance_checks": 210,
        "g14_complete_distance_checks": 182,
        "completion_point_rescans": len(qids),
        "completion_neighborhoods": neighborhoods,
        "field": "SymPy AlgebraicField QQ(sqrt(3),sqrt(5),sqrt(11))"
    }, indent=2))


if __name__ == "__main__":
    main()
