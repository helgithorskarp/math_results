#!/usr/bin/env python3
"""Exact rational boundary of the two-color curved tetromino fixture."""

import json
from fractions import Fraction
from math import comb

from obstruction import solve


PROFILE = [Fraction(0), Fraction(0), Fraction(1), Fraction(-2), Fraction(1)]


def multiply(a, b):
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def derivative(a):
    return [i * a[i] for i in range(1, len(a))]


def integral(a):
    return sum((value / (i + 1) for i, value in enumerate(a)), Fraction(0))


def difference(a, b):
    return [(a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)
            for i in range(max(len(a), len(b)))]


def fixture():
    vertices = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1),
                (3, 1), (2, 1), (1, 1), (0, 1)]
    labels = ["a_plus"] * 3 + ["a_minus"] * 2 + ["b_plus"] * 2 + ["b_minus"] * 3
    amplitudes = {"a": Fraction(1, 100), "b": Fraction(1, 200)}
    counts = {label: labels.count(label) for label in sorted(set(labels))}
    area_by_green = Fraction(0)
    area_by_profiles = Fraction(4)
    arcs = []
    for i, (start, label) in enumerate(zip(vertices, labels)):
        end = vertices[(i + 1) % len(vertices)]
        e = (end[0] - start[0], end[1] - start[1])
        if e[0] ** 2 + e[1] ** 2 != 1:
            raise AssertionError("nonunit base edge")
        normal = (e[1], -e[0])
        color, sign = label.split("_")
        sigma = 1 if sign == "plus" else -1
        amplitude = amplitudes[color]
        coordinates = []
        for axis in range(2):
            poly = [sigma * amplitude * normal[axis] * x for x in PROFILE]
            poly[0] += start[axis]
            poly[1] += e[axis]
            coordinates.append(poly)
        x, y = coordinates
        area_by_green += integral(difference(multiply(x, derivative(y)),
                                             multiply(y, derivative(x)))) / 2
        area_by_profiles += sigma * amplitude * integral(PROFILE)
        arcs.append({"type": label, "start": list(start), "end": list(end),
                     "sigma": sigma, "amplitude": str(amplitude),
                     "x_coefficients": [str(t) for t in x],
                     "y_coefficients": [str(t) for t in y]})
    reversed_profile = [sum(PROFILE[j] * comb(j, i) * (-1) ** i
                            for j in range(i, len(PROFILE)))
                        for i in range(len(PROFILE))]
    if reversed_profile != PROFILE or integral(PROFILE) != Fraction(1, 30):
        raise AssertionError("quartic symmetry or area identity failed")
    if area_by_green != area_by_profiles or area_by_green != Fraction(24001, 6000):
        raise AssertionError("independent exact area calculation failed")
    diameter_upper = Fraction(5) + max(amplitudes.values()) / 8
    model = {"counts": counts,
             "pairs": [["a_plus", "a_minus"], ["b_plus", "b_minus"]],
             "area_lower": str(area_by_green),
             "diameter_squared_upper": str(diameter_upper ** 2)}
    return {"base": "4 by 1 rectangle with ten unit boundary edges",
            "profile_coefficients": [str(t) for t in PROFILE],
            "arcs": arcs, "area_exact": str(area_by_green),
            "area_checked_by_green_formula": True,
            "model": model, "charge_certificate": solve(model)}


if __name__ == "__main__":
    print(json.dumps(fixture(), indent=2, sort_keys=True))
