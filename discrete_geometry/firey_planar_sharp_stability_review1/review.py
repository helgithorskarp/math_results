#!/usr/bin/env python3
"""Independent audit of the sharp planar Firey area-stability theorem.

CPython 3.11+, standard library only.  The target package is not imported.
Exact rational polygon geometry is combined with a definition-level p=2
support-measure evaluation, exhaustive small zonotopes, analytic ellipse
controls, and an independent composite-Simpson audit of the scalar function.
The numerical layers corroborate the human proof; they are not interval
certificates for its universal analytic statements.
"""

from fractions import Fraction as F
from itertools import combinations, product
from math import atan, comb, gamma, pi, sqrt
from pathlib import Path
import hashlib
import json
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def scale(value, a):
    return value * a[0], value * a[1]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def cross(o, a, b):
    return det(sub(a, o), sub(b, o))


def hull(points):
    points = sorted(set((F(x), F(y)) for x, y in points))
    require(len(points) >= 3, "too few points for a polygon")
    lower = []
    for point in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper = []
    for point in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    polygon = lower[:-1] + upper[:-1]
    require(len(polygon) >= 3, "degenerate hull")
    return polygon


def polygon_area(polygon):
    return sum(det(a, b) for a, b in
               zip(polygon, polygon[1:] + polygon[:1])) / 2


def zonotope(generators):
    points = []
    for signs in product((-1, 1), repeat=len(generators)):
        point = (F(0), F(0))
        for sign, generator in zip(signs, generators):
            point = add(point, scale(F(sign, 2), generator))
        points.append(point)
    return hull(points)


def on_segment(point, a, b):
    if cross(a, b, point) != 0:
        return False
    return all(min(x, y) <= z <= max(x, y)
               for z, x, y in zip(point, a, b))


def polygon_data(polygon, translation):
    polygon = hull(polygon)
    translation = tuple(map(F, translation))
    require(set(polygon) == {scale(-1, v) for v in polygon},
            "polygon is not origin symmetric")
    facets = []
    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        edge = sub(b, a)
        normal = (edge[1], -edge[0])
        support_mass = dot(a, normal)
        signed_moment = dot(translation, normal)
        require(support_mass > 0, "origin is not interior")
        require(abs(signed_moment) <= support_mass,
                "translation lies outside centered body")
        facets.append((a, b, normal, support_mass,
                       signed_moment / support_mass))
    area = polygon_area(polygon)
    measure_moment = sum(abs(dot(translation, item[2]))
                         for item in facets) / 2
    twice_translation = scale(2, translation)
    determinant_moment = max(abs(det(vertex, twice_translation))
                             for vertex in polygon)
    require(measure_moment == determinant_moment <= area,
            "projection moment identity failed")

    maximizing_vertex = max(polygon,
                            key=lambda v: abs(det(v, twice_translation)))
    y = add(translation, maximizing_vertex)
    parallelogram = [
        (F(0), F(0)), y, twice_translation, sub(twice_translation, y)
    ]
    require(abs(det(y, twice_translation)) == determinant_moment,
            "anchored parallelogram has the wrong area")
    for point in parallelogram:
        centered = sub(point, translation)
        require(all(dot(centered, normal) <= support
                    for _, _, normal, support, _ in facets),
                "anchored parallelogram escaped the body")
    equality_signature = all(abs(item[4]) in (0, 1) for item in facets)
    return {
        "polygon": polygon,
        "translation": translation,
        "facets": facets,
        "area": area,
        "moment": measure_moment,
        "signature": equality_signature,
    }


def audit_equality_classification(data):
    """Check the exact polygonal consequence of the a.e. equality condition."""
    x = data["translation"]
    if x == (0, 0):
        require(data["signature"], "centered body must have equality signature")
        return "centered"
    if not data["signature"]:
        return "strict"

    facets = data["facets"]
    polygon = data["polygon"]
    require(len(facets) <= 6, "equality signature has more than six sides")
    boundary_hits = 0
    for a, b, normal, support, ratio in facets:
        signed = dot(x, normal)
        if signed == 0:
            require(det(sub(b, a), x) == 0,
                    "zero-ratio side is not parallel to the center vector")
        else:
            point = x if signed > 0 else scale(-1, x)
            require(abs(ratio) == 1 and on_segment(point, a, b),
                    "nonparallel equality side misses both distinguished points")
            boundary_hits += 1
    require(boundary_hits >= 2, "distinguished boundary points were not exposed")

    # Construct the proof's normalization without assuming its answer.
    # u=det(c,x)/D gives horizontal width two and v0=<c,x>/<x,x>
    # sends x to (0,1).  A shear centers the rightmost vertical face.
    determinant_width = max(abs(det(vertex, x)) for vertex in polygon)
    require(determinant_width > 0, "normalizing width vanished")
    norm_x = dot(x, x)
    first_coordinates = [det(vertex, x) / determinant_width
                         for vertex in polygon]
    raw_seconds = [dot(vertex, x) / norm_x for vertex in polygon]
    right_seconds = [v for u, v in zip(first_coordinates, raw_seconds)
                     if u == 1]
    require(right_seconds, "right support face missing")
    center = (min(right_seconds) + max(right_seconds)) / 2
    tau = (max(right_seconds) - min(right_seconds)) / 2
    normalized = hull((u, v - center * u)
                      for u, v in zip(first_coordinates, raw_seconds))
    expected = hull([(0, 1), (0, -1)]
                    + [(u, v) for u in (-1, 1) for v in (-tau, tau)])
    require(normalized == expected, "equality polygon is not a normalized T_tau")
    require(0 <= tau <= 1, "normalized face parameter lies outside [0,1]")
    return "anchored_family"


def psi_two(value):
    value = abs(float(value))
    return 2 + 2 * value * atan(value)


def firey_area_two(data):
    # For a polygon, dS_C has one atom per side.  With the unnormalized
    # outward normal used here, h_C dS_C is exactly support_mass.
    return sum(float(support) * psi_two(ratio)
               for _, _, _, support, ratio in data["facets"]) / 2


def audit_small_zonotopes():
    directions = [(1, 0), (0, 1), (1, 1), (1, -1), (2, 1), (1, 2)]
    scale_patterns = (
        lambda count: [1] * count,
        lambda count: [1 + (index % 2) for index in range(count)],
        lambda count: [1 + ((2 * index + 1) % 3) for index in range(count)],
    )
    bodies = translations = equality_cases = strict_cases = 0
    minimum_strict_gap = None
    for count in range(2, 5):
        for selected in combinations(directions, count):
            for make_scales in scale_patterns:
                scales = make_scales(count)
                generators = [scale(F(factor), vector)
                              for factor, vector in zip(scales, selected)]
                polygon = zonotope(generators)
                candidates = set()
                for coefficients in product((F(-1, 2), F(0), F(1, 2)),
                                            repeat=count):
                    point = (F(0), F(0))
                    for coefficient, generator in zip(coefficients, generators):
                        point = add(point, scale(coefficient, generator))
                    candidates.add(point)
                for translation in sorted(candidates):
                    data = polygon_data(polygon, translation)
                    classification = audit_equality_classification(data)
                    area_two = firey_area_two(data)
                    bound = 2 * float(data["area"]) + (pi / 2) * float(data["moment"])
                    gap = bound - area_two
                    require(gap >= -2e-12, "p=2 stability inequality failed")
                    if data["signature"]:
                        require(abs(gap) < 2e-12,
                                "equality signature did not give equality")
                        require(classification in ("centered", "anchored_family"),
                                "unclassified equality case")
                        equality_cases += 1
                    else:
                        require(gap > 1e-10, "strict polygon case lost its gap")
                        minimum_strict_gap = (gap if minimum_strict_gap is None
                                              else min(minimum_strict_gap, gap))
                        strict_cases += 1
                    translations += 1
                bodies += 1
    require(equality_cases > 0 and strict_cases > 0,
            "zonotope audit missed an equality or strict stratum")
    return bodies, translations, equality_cases, strict_cases, minimum_strict_gap


def audit_explicit_family():
    taus = [F(0), F(1, 5), F(2, 3), F(1)]
    matrices = [((1, 0), (0, 1)), ((2, 1), (1, 3)), ((0, 2), (3, 1))]
    checks = 0
    for tau in taus:
        base = hull([(0, 1), (0, -1)]
                    + [(u, v) for u in (-1, 1) for v in (-tau, tau)])
        for matrix in matrices:
            determinant = abs(det(matrix[0], matrix[1]))
            transformed = [(dot(matrix[0], v), dot(matrix[1], v)) for v in base]
            x = (matrix[0][1], matrix[1][1])
            data = polygon_data(transformed, x)
            require(data["area"] == determinant * (2 + 2 * tau),
                    "T_tau area failed under GL(2)")
            require(data["moment"] == determinant * 2,
                    "T_tau moment failed under GL(2)")
            require(audit_equality_classification(data) == "anchored_family",
                    "T_tau was not recognized as an equality body")
            require(abs(firey_area_two(data)
                        - (2 * float(data["area"])
                           + pi / 2 * float(data["moment"]))) < 2e-12,
                    "T_tau p=2 area did not attain the bound")
            checks += 1
    return checks


def audit_hexagons():
    fixtures = [(F(1), F(1)), (F(1), F(3)), (F(2, 5), F(7, 3)),
                (F(5), F(1, 4))]
    checks = 0
    for a, b in fixtures:
        generators = [(F(1), F(0)), (a, b), (F(0), F(1))]
        centered = zonotope(generators)
        x = scale(F(1, 2), (1 + a, 1 + b))
        data = polygon_data(centered, x)
        require(data["area"] == 1 + a + b, "hexagon area formula failed")
        require(data["moment"] == 1 + max(a, b), "hexagon moment formula failed")
        ratio = abs(a - b) / (a + b)
        area_two = firey_area_two(data)
        deficit = (2 + pi / 2) * float(data["area"]) - area_two
        expected = float(a + b) / 2 * (psi_two(1) - psi_two(ratio))
        require(abs(deficit - expected) < 3e-12,
                "hexagon deficit formula failed")
        lower = pi / 2 * float(min(a, b))
        upper = (1 + pi / 2) * float(min(a, b))
        require(deficit + 2e-12 >= lower and deficit < upper,
                "sharp hexagon bounds failed")
        require((abs(deficit - lower) < 2e-12) == (a == b),
                "hexagon lower equality condition failed")
        checks += 1
    return checks


def audit_ellipses():
    # If h_C(n)^2=n^T Q n and p=2, then the Firey body has support
    # 2 n^T(Q+xx^T)n.  The determinant lemma gives the following areas.
    semiaxes = [(F(1), F(1)), (F(2), F(1)), (F(3, 2), F(5, 2))]
    normalized_points = [(F(0), F(0)), (F(1, 3), F(0)),
                         (F(1), F(0)), (F(3, 5), F(4, 5))]
    checks = 0
    for a, b in semiaxes:
        for u, v in normalized_points:
            z = u * u + v * v
            require(z <= 1, "ellipse translation left the body")
            area = pi * float(a * b)
            moment = 2 * float(a * b) * sqrt(float(z))
            firey_area = 2 * pi * float(a * b) * sqrt(1 + float(z))
            bound = 2 * area + (pi / 2) * moment
            require(firey_area <= bound + 2e-12,
                    "analytic ellipse control failed")
            require((abs(firey_area - bound) < 2e-12) == (z == 0),
                    "ellipse equality condition failed")
            checks += 1
    return checks


def scalar_f(t, p):
    return ((1 + t) ** p + (1 - t) ** p) ** (1 / p)


def scalar_fp(t, p):
    value = scalar_f(t, p)
    return ((1 + t) ** (p - 1) - (1 - t) ** (p - 1)) / value ** (p - 1)


def composite_simpson(function, upper, panels):
    require(panels % 2 == 0, "Simpson panel count must be even")
    step = upper / panels
    value = function(0.0) + function(upper)
    value += 4 * sum(function((2 * index - 1) * step)
                     for index in range(1, panels // 2 + 1))
    value += 2 * sum(function(2 * index * step)
                     for index in range(1, panels // 2))
    return value * step / 3


def scalar_psi(t, p, panels):
    integral = composite_simpson(lambda value: scalar_fp(value, p) ** 2,
                                 t, panels)
    return scalar_f(t, p) ** 2 - t * integral


def audit_scalar_function():
    parameters = [1.05, 1.25, 1.5, 2.0, 3.0, 10.0, 50.0]
    points = [0.1, 0.25, 0.5, 0.75, 0.9]
    endpoint_checks = chord_checks = 0
    for p in parameters:
        q = p / (p - 1)
        c_q = 2 * gamma(1 + 1 / q) ** 2 / gamma(1 + 2 / q)
        base = 2 ** (2 / p)
        constant = 2 + c_q - base
        require(constant > 0, "stability constant is not positive")
        endpoint = scalar_psi(1.0, p, 262144)
        require(abs(endpoint - (2 + c_q)) < 2e-6,
                "independent endpoint integration missed the beta value")
        endpoint_checks += 1
        for t in points:
            value = scalar_psi(t, p, 8192)
            require(value < base + constant * t,
                    "strict scalar chord inequality failed")
            chord_checks += 1
    for t in [0.0, 0.1, 0.5, 0.9, 1.0]:
        value = scalar_psi(t, 2.0, 16384)
        require(abs(value - psi_two(t)) < 2e-12,
                "p=2 closed scalar formula failed")
    return endpoint_checks, chord_checks


def build_summary():
    bodies, translations, equality_cases, strict_cases, minimum_gap = (
        audit_small_zonotopes())
    family_checks = audit_explicit_family()
    hexagon_checks = audit_hexagons()
    ellipse_checks = audit_ellipses()
    endpoint_checks, chord_checks = audit_scalar_function()
    return {
        "ellipses": {"analytic_p2_controls": ellipse_checks},
        "explicit_family": {"exact_gl2_cases": family_checks},
        "hexagons": {"exact_geometry_and_p2_deficit_cases": hexagon_checks},
        "scalar": {
            "general_p_chord_checks": chord_checks,
            "general_p_endpoint_checks": endpoint_checks,
            "p2_closed_formula_checks": 5,
        },
        "zonotopes": {
            "bodies": bodies,
            "equality_cases": equality_cases,
            "strict_cases": strict_cases,
            "translations": translations,
            "strict_gap_positive": minimum_gap is not None and minimum_gap > 0,
        },
    }


def main():
    summary = build_summary()
    encoded = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode()
    if "--emit" in sys.argv:
        sys.stdout.write(encoded.decode())
        return
    expected_path = Path(__file__).with_name("EXPECTED.json")
    expected = json.loads(expected_path.read_text())
    require(summary == expected, "result differs from EXPECTED.json")
    print("PASS independent planar Firey stability review")
    print(hashlib.sha256(encoded).hexdigest())
    print(json.dumps({
        "exact_polygon_translations": summary["zonotopes"]["translations"],
        "general_p_scalar_checks": (summary["scalar"]["general_p_chord_checks"]
                                    + summary["scalar"]["general_p_endpoint_checks"]),
        "smooth_controls": summary["ellipses"]["analytic_p2_controls"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
