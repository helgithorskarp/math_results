#!/usr/bin/env python3
"""Definition-level controls for the hinge identity and colour extension."""
from itertools import product
import json
import geometry


def main():
    # Rational-coordinate control: v is one intersection of the unit circles
    # about a,b and q=a+b-v is the other. All coordinates use scale 2.
    zero = (0,)*16
    a = list(zero)
    b = list(zero)
    v = list(zero)
    a[0], b[0], v[0], v[9] = -1, 1, 0, 1
    q = tuple(a[i]+b[i]-v[i] for i in range(16))
    a, b, v = tuple(a), tuple(b), tuple(v)
    unit = (4,)+(0,)*7
    if not (geometry.norm_coefficients(a, v) == unit == geometry.norm_coefficients(b, v)
            and geometry.norm_coefficients(a, q) == unit == geometry.norm_coefficients(b, q)
            and q != v):
        raise ValueError("hinge identity control")

    # Exhaust every possible set of colours on up to three retained neighbours.
    low_degree_cases = 0
    for degree in range(4):
        for colours in product(range(4), repeat=degree):
            if not set(range(4))-set(colours):
                raise ValueError("low-degree extension control")
            low_degree_cases += 1

    # A wrong radical image and malformed coefficient vectors must fail.
    old = geometry.ROOTS
    rejected = []
    try:
        geometry.ROOTS = (0, 0, 0)
        try:
            geometry.modular_basis()
        except ValueError:
            rejected.append("wrong_radical_images")
        else:
            raise ValueError("wrong radical images accepted")
    finally:
        geometry.ROOTS = old
    try:
        geometry.norm_coefficients((0,)*15, (0,)*16)
    except Exception:
        rejected.append("wrong_coordinate_length")
    else:
        raise ValueError("wrong coordinate length accepted")
    print(json.dumps({"all_checks": True, "hinge_identity": True,
                      "low_degree_list_cases": low_degree_cases,
                      "malformed_inputs_rejected": rejected}, sort_keys=True))


if __name__ == "__main__":
    main()
