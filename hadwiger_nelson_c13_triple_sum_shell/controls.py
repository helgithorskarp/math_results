#!/usr/bin/env python3
"""Negative controls for the exact host and compact certificate."""
import copy
import json
from pathlib import Path

import verify


def rejects(call):
    try:
        call()
    except ValueError:
        return True
    raise ValueError("corrupt fixture was accepted")


def check_coordinate_receipt(certificate, points):
    if certificate["coordinate_sha256"] != verify.compact_hash(points):
        raise ValueError("coordinate receipt mismatch")


def main():
    path = Path(__file__).with_name("certificate.json")
    certificate = json.loads(path.read_text())
    _, _, base, shell, _, points = verify.reconstruct()
    edges = verify.strict_edges(points)
    controls = 0

    verify.proper(certificate["colouring"], edges, len(points))

    corrupt = copy.deepcopy(certificate)
    word = list(corrupt["colouring"])
    a, b = edges[0]
    word[b] = word[a]
    corrupt["colouring"] = "".join(word)
    controls += rejects(lambda: verify.proper(corrupt["colouring"], edges, len(points)))

    corrupt = copy.deepcopy(certificate)
    corrupt["colouring"] = corrupt["colouring"][:-1]
    controls += rejects(lambda: verify.proper(corrupt["colouring"], edges, len(points)))

    corrupt = copy.deepcopy(certificate)
    corrupt["coordinate_sha256"] = "0" * 64
    controls += rejects(lambda: check_coordinate_receipt(corrupt, points))

    _, _, _, stricter_shell, _, _ = verify.reconstruct(minimum_contacts=3)
    if len(stricter_shell) != 832 or len(base) != 403 or len(shell) != 2940:
        raise ValueError("threshold/cardinality control failed")

    # Squared norm 1+(4/9)sqrt(5): its rational coefficient alone is 1.
    if verify.unit_delta((64, 32, 0, 0, 0, 0, 0, 0)):
        raise ValueError("irrational norm false positive accepted")

    # Check the displayed Cartesian norm coefficients against quotient-ring
    # multiplication on a spanning set of quadratic inputs.
    basis = [tuple(int(i == j) for i in range(8)) for j in range(8)]
    for x in basis:
        for y in basis:
            z = tuple(a + 2*b for a, b in zip(x, y))
            a, b, c, d, e, f, g, h = z
            expected = (a*a + 5*b*b + 33*c*c + 165*d*d +
                        3*e*e + 15*f*f + 11*g*g + 55*h*h,
                        2*(a*b + 33*c*d + 3*e*f + 11*g*h),
                        0, 0, 0, 0,
                        -2*(a*c + 5*b*d + e*g + 5*f*h),
                        -2*(a*d + b*c + e*h + f*g))
            tensor = (a, b, e, f, g, h, -c, -d)
            if verify.multiply(tensor, verify.conjugate(tensor)) != expected:
                raise ValueError("Cartesian/tensor norm disagreement")

    print(json.dumps({"controls_passed": controls + 66,
                      "corrupt_certificates_rejected": controls,
                      "cartesian_tensor_norm_checks": 64,
                      "minimum_three_contact_shell": len(stricter_shell),
                      "rational_coefficient_false_positive_rejected": True},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
