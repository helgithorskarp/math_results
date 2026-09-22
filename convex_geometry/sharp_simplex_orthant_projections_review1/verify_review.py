#!/usr/bin/env python3
"""Independent exact checks for the sharp simplex projection review.

This checker targets placement strictness and boundary completeness, rather
than duplicating the producer's explicit nine-dimensional lift.  It expands
the defining max inequality directly, enumerates vertices over Fraction, and
computes low-dimensional volumes from supporting facets.
"""

import json
from fractions import Fraction as F
from itertools import combinations, product
from math import factorial, gcd


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def solve(matrix, rhs):
    n = len(rhs)
    rows = [[F(x) for x in row] + [F(value)]
            for row, value in zip(matrix, rhs)]
    for column in range(n):
        pivot = next((row for row in range(column, n)
                      if rows[row][column]), None)
        if pivot is None:
            return None
        rows[column], rows[pivot] = rows[pivot], rows[column]
        scale = rows[column][column]
        rows[column] = [x / scale for x in rows[column]]
        for row in range(n):
            if row == column:
                continue
            scale = rows[row][column]
            rows[row] = [x - scale * y
                         for x, y in zip(rows[row], rows[column])]
    return tuple(row[-1] for row in rows)


def defining_inequalities(c):
    """Return sum_i max(|w_i|,c_i)<=2 in w_N=-sum_{i<N}w_i."""
    c = tuple(F(x) for x in c)
    require(len(c) >= 2 and min(c) >= 0 and sum(c) == 1,
            "invalid barycentric parameter")
    n = len(c) - 1
    inequalities = {}
    for choices in product((-1, 0, 1), repeat=n + 1):
        normal = tuple(choices[i] - choices[-1] for i in range(n))
        bound = F(2) - sum(c[i] for i, value in enumerate(choices)
                           if value == 0)
        divisor = 0
        for value in normal:
            divisor = gcd(divisor, abs(value))
        if divisor == 0:
            require(bound >= 0, "constant inequality is inconsistent")
            continue
        normal = tuple(value // divisor for value in normal)
        bound /= divisor
        inequalities[normal] = min(inequalities.get(normal, bound), bound)
    return sorted(inequalities.items())


def vertices(inequalities):
    n = len(inequalities[0][0])
    result = set()
    for active in combinations(inequalities, n):
        point = solve([item[0] for item in active],
                      [item[1] for item in active])
        if point is not None and all(dot(a, point) <= b
                                     for a, b in inequalities):
            result.add(point)
    require(result, "vertex enumeration returned an empty set")
    return sorted(result)


def cross(a, b, c):
    return ((b[0] - a[0]) * (c[1] - a[1])
            - (b[1] - a[1]) * (c[0] - a[0]))


def convex_hull_2(points):
    points = sorted(set(points))
    require(points, "empty planar point set")
    if len(points) <= 2:
        return points
    halves = []
    for sequence in (points, points[::-1]):
        half = []
        for point in sequence:
            while len(half) >= 2 and cross(half[-2], half[-1], point) <= 0:
                half.pop()
            half.append(point)
        halves.append(half[:-1])
    return halves[0] + halves[1]


def polygon_area(points):
    return abs(sum(a[0] * b[1] - a[1] * b[0]
                   for a, b in zip(points, points[1:] + points[:1]))) / 2


def determinant_3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def coordinate_volume(inequalities, points):
    n = len(points[0])
    if n == 1:
        return points[-1][0] - points[0][0]
    if n == 2:
        return polygon_area(convex_hull_2(points))
    require(n == 3, "review volume routine only covers dimensions at most 3")
    total = F(0)
    facet_keys = set()
    for normal, bound in inequalities:
        face = [point for point in points if dot(normal, point) == bound]
        if len(face) < 3:
            continue
        dropped = next(i for i, value in enumerate(normal) if value)
        kept = [i for i in range(3) if i != dropped]
        decode = {tuple(point[i] for i in kept): point for point in face}
        ring_2 = convex_hull_2(decode)
        if len(ring_2) < 3:
            continue
        ring = [decode[point] for point in ring_2]
        key = frozenset(ring)
        if key in facet_keys:
            continue
        facet_keys.add(key)
        anchor = ring[0]
        for i in range(1, len(ring) - 1):
            total += abs(determinant_3(anchor, ring[i], ring[i + 1])) / 6
    require(facet_keys, "no three-dimensional facets found")
    return total


def full_coordinates(point):
    return tuple(point) + (-sum(point, F(0)),)


def ratio_and_vertices(c):
    inequalities = defining_inequalities(c)
    points = vertices(inequalities)
    n = len(c) - 1
    ratio = F(factorial(n)) * coordinate_volume(inequalities, points)
    return ratio, points, inequalities


def face_vertex_audit(c, points):
    c = tuple(F(x) for x in c)
    expanded = [full_coordinates(point) for point in points]
    records = []
    for i in range(len(c)):
        face = {point for point in expanded if point[i] == 1}
        expected = set()
        other = [j for j in range(len(c)) if j != i]
        for chosen in other:
            point = []
            for j in range(len(c)):
                if j == i:
                    point.append(F(1))
                elif j == chosen:
                    point.append(-c[j] - c[i])
                else:
                    point.append(-c[j])
            expected.add(tuple(point))
        require(face == expected, "coordinate-one exposed face is incomplete")
        if c[i] > 0 and len(c) == 4:
            ring = list(face)
            base = ring[0]
            u = tuple(ring[1][j] - base[j] for j in range(4))
            v = tuple(ring[2][j] - base[j] for j in range(4))
            area_squared = (dot(u, u) * dot(v, v) - dot(u, v) ** 2) / 4
            require(area_squared == F(3, 4) * c[i] ** 4,
                    "exposed-face area formula failed")
        records.append({"coordinate": i, "c_i": text_fraction(c[i]),
                        "face_vertices": len(face)})
    return records


def satisfies(point, inequalities):
    return all(dot(normal, point) <= bound for normal, bound in inequalities)


def text_fraction(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def main():
    # This pair is related by a coordinate permutation, so its two volumes
    # agree. Strict concavity at their midpoint can therefore be checked by
    # an exact volume comparison, with no comparison of irrational cube roots.
    c = (F(1, 2), F(1, 4), F(1, 8), F(1, 8))
    d = (F(1, 4), F(1, 2), F(1, 8), F(1, 8))
    midpoint = tuple((x + y) / 2 for x, y in zip(c, d))
    ratio_c, points_c, inequalities_c = ratio_and_vertices(c)
    ratio_d, points_d, inequalities_d = ratio_and_vertices(d)
    ratio_mid, points_mid, inequalities_mid = ratio_and_vertices(midpoint)
    require(ratio_c == ratio_d, "permutation invariance failed")
    require(ratio_mid > ratio_c, "strict midpoint concavity was not detected")

    pair_checks = 0
    for left in points_c:
        for right in points_d:
            pair_checks += 1
            average = tuple((x + y) / 2 for x, y in zip(left, right))
            require(satisfies(average, inequalities_mid),
                    "Minkowski inclusion failed on a vertex pair")

    boundary = (F(1, 2), F(1, 4), F(1, 4), F(0))
    ratio_boundary, boundary_points, _ = ratio_and_vertices(boundary)
    barycenter_ratio, barycenter_points, _ = ratio_and_vertices(
        (F(1, 4), F(1, 4), F(1, 4), F(1, 4)))
    vertex_ratio, vertex_points, _ = ratio_and_vertices(
        (F(1), F(0), F(0), F(0)))
    edge_ratio, edge_points, _ = ratio_and_vertices(
        (F(1, 2), F(1, 2), F(0), F(0)))
    require(vertex_ratio == 8, "dimension-three vertex minimum is not 2^3")
    require(barycenter_ratio == F(127, 8),
            "independent dimension-three barycenter volume is not 127/8")
    require(edge_ratio > vertex_ratio and ratio_boundary > vertex_ratio,
            "a nonvertex boundary placement failed strictness")

    planar_records = []
    for planar_c in ((F(1, 7), F(2, 7), F(4, 7)),
                     (F(0), F(2, 5), F(3, 5)),
                     (F(1), F(0), F(0))):
        ratio, points, _ = ratio_and_vertices(planar_c)
        expected = F(6) - 2 * sum(x * x for x in planar_c)
        require(ratio == expected, "off-grid planar formula failed")
        planar_records.append({
            "c": [text_fraction(x) for x in planar_c],
            "ratio": text_fraction(ratio),
            "vertices": len(points),
        })

    one_dimensional = []
    for interval_c in ((F(0), F(1)), (F(2, 7), F(5, 7)), (F(1), F(0))):
        ratio, points, _ = ratio_and_vertices(interval_c)
        require(ratio == 2, "one-dimensional exceptional case is not constant")
        one_dimensional.append({
            "c": [text_fraction(x) for x in interval_c],
            "ratio": text_fraction(ratio),
            "vertices": len(points),
        })

    rejected = 0
    for invalid in ((F(1), F(1), F(0)), (F(-1), F(1), F(1))):
        try:
            defining_inequalities(invalid)
        except RuntimeError:
            rejected += 1
            continue
        raise RuntimeError("invalid barycentric parameter was accepted")

    report = {
        "arithmetic": "fractions.Fraction; direct max-inequality expansion",
        "strict_concavity_fixture": {
            "c": [text_fraction(x) for x in c],
            "permuted_c": [text_fraction(x) for x in d],
            "midpoint": [text_fraction(x) for x in midpoint],
            "endpoint_ratio": text_fraction(ratio_c),
            "midpoint_ratio": text_fraction(ratio_mid),
            "endpoint_vertices": len(points_c),
            "midpoint_vertices": len(points_mid),
            "minkowski_vertex_pair_checks": pair_checks,
        },
        "boundary_dimension_three": {
            "barycenter_ratio": text_fraction(barycenter_ratio),
            "barycenter_vertices": len(barycenter_points),
            "vertex_ratio": text_fraction(vertex_ratio),
            "edge_midpoint_ratio": text_fraction(edge_ratio),
            "other_boundary_ratio": text_fraction(ratio_boundary),
            "vertex_counts": [len(vertex_points), len(edge_points),
                              len(boundary_points)],
            "exposed_faces": face_vertex_audit(boundary, boundary_points),
        },
        "off_grid_planar_formula": planar_records,
        "one_dimensional_exception": one_dimensional,
        "rejected_invalid_parameters": rejected,
        "scope": (
            "Exact low-dimensional audit of placement and boundary reductions; "
            "the universal realization and asymptotic remain human-checked."
        ),
        "status": "INDEPENDENT_PLACEMENT_CHECKS_PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
