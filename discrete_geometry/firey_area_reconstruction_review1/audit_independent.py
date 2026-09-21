"""Independent exact audit for the local Firey-area reconstruction theorem.

This checker deliberately does not import the target's reconstruction code.
It enumerates a complete bounded catalogue of centrally symmetric lattice
polygons, derives the polar moment data directly from oriented edges, and
tests the proof reductions through exact rational identities and collisions.
"""

import hashlib
import json
from fractions import Fraction as F
from itertools import combinations
from math import factorial, gcd, lcm


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def subtract(a, b):
    return a[0] - b[0], a[1] - b[1]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def hull(points):
    """Strict counterclockwise hull, beginning at its lexicographic minimum."""
    points = sorted(set((F(x), F(y)) for x, y in points))
    require(len(points) >= 3, "too few distinct points")

    def half(sequence):
        output = []
        for point in sequence:
            while len(output) >= 2 and cross(
                subtract(output[-1], output[-2]),
                subtract(point, output[-1]),
            ) <= 0:
                output.pop()
            output.append(point)
        return output

    polygon = tuple(half(points)[:-1] + half(reversed(points))[:-1])
    require(len(polygon) >= 3, "points are collinear")
    return polygon


def transform(polygon, matrix):
    a, b, c, d = map(F, matrix)
    require(a * d - b * c != 0, "singular affine map")
    return hull((a * x + b * y, c * x + d * y) for x, y in polygon)


def polar_atoms(polygon):
    """Return (polar endpoint, h*dS mass) directly from CCW edges."""
    require(len(polygon) >= 4 and len(polygon) % 2 == 0, "bad symmetric polygon")
    require(set(polygon) == {(-x, -y) for x, y in polygon}, "not origin symmetric")
    atoms = []
    twice_area = F(0)
    for start, end in zip(polygon, polygon[1:] + polygon[:1]):
        edge = subtract(end, start)
        normal = edge[1], -edge[0]
        support_mass = dot(normal, start)
        require(support_mass > 0, "origin not strictly inside or orientation reversed")
        atoms.append(((normal[0] / support_mass, normal[1] / support_mass), support_mass))
        twice_area += cross(start, end)
    require(sum(weight for _, weight in atoms) == twice_area, "cone-area identity failed")
    return tuple(atoms)


def moment(atoms, degree):
    """Moment vector indexed by the exponent of x."""
    return tuple(
        sum(weight * u[0] ** exponent * u[1] ** (degree - exponent)
            for u, weight in atoms)
        for exponent in range(degree + 1)
    )


def matrix_rank(matrix):
    data = [[F(value) for value in row] for row in matrix]
    if not data:
        return 0
    row = 0
    for column in range(len(data[0])):
        pivot = next((index for index in range(row, len(data)) if data[index][column]), None)
        if pivot is None:
            continue
        data[row], data[pivot] = data[pivot], data[row]
        scale = data[row][column]
        data[row] = [value / scale for value in data[row]]
        for index in range(row + 1, len(data)):
            if data[index][column]:
                scale = data[index][column]
                data[index] = [left - scale * right
                               for left, right in zip(data[index], data[row])]
        row += 1
        if row == len(data):
            break
    return row


def gram(moment_vector, degree):
    require(len(moment_vector) == 2 * degree + 1, "wrong moment degree")
    return [[moment_vector[i + j] for j in range(degree + 1)]
            for i in range(degree + 1)]


def multiply(left, right):
    output = [F(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            output[i + j] += a * b
    return tuple(output)


def integrate_form(coefficients, moment_vector):
    require(len(coefficients) == len(moment_vector), "form/moment degree mismatch")
    return sum(a * b for a, b in zip(coefficients, moment_vector))


def projective_key(vector):
    denominators = [coordinate.denominator for coordinate in vector]
    scale = lcm(*denominators)
    integers = [int(coordinate * scale) for coordinate in vector]
    divisor = gcd(abs(integers[0]), abs(integers[1]))
    require(divisor > 0, "zero projective vector")
    integers = [value // divisor for value in integers]
    if integers[0] < 0 or (integers[0] == 0 and integers[1] < 0):
        integers = [-value for value in integers]
    return tuple(integers)


def positive_endpoint(vector):
    key = projective_key(vector)
    if (vector[0] > 0) or (vector[0] == 0 and vector[1] > 0):
        return vector, key
    return (-vector[0], -vector[1]), key


def radial_ratio_audit(atoms):
    """Check the two-adjacent-degree radius formula with rescaled line data."""
    representatives = {}
    for endpoint, _ in atoms:
        positive, key = positive_endpoint(endpoint)
        representatives[key] = positive
    r = len(representatives)
    require(2 * r == len(atoms), "wrong antipodal pairing")
    ordered = sorted(representatives.items())
    lines = [(F(3 * key[0]), F(3 * key[1])) for key, _ in ordered]
    factors = [(-line[0], line[1]) for line in lines]
    low = moment(atoms, 2 * r - 2)
    high = moment(atoms, 2 * r)
    checks = 0
    for j, ((_, endpoint), line) in enumerate(zip(ordered, lines)):
        quotient = (F(1),)
        for i, factor in enumerate(factors):
            if i != j:
                quotient = multiply(quotient, factor)
        if line[1]:
            isolator = (F(1, 1) / line[1], F(0))  # y / line_y
            alpha = endpoint[1] / line[1]
        else:
            isolator = (F(0), F(1, 1) / line[0])  # x / line_x
            alpha = endpoint[0] / line[0]
        require(alpha > 0, "inconsistent line orientation")
        square_quotient = multiply(quotient, quotient)
        numerator_form = multiply(multiply(isolator, isolator), square_quotient)
        denominator = integrate_form(square_quotient, low)
        numerator = integrate_form(numerator_form, high)
        require(denominator > 0 and numerator / denominator == alpha * alpha,
                "two-degree radial ratio failed")
        checks += 1
    return checks


def halfplane_vertices(polar_points):
    """Intersect all pairs of supporting lines and retain feasible vertices."""
    output = set()
    for first, second in combinations(polar_points, 2):
        determinant = cross(first, second)
        if determinant == 0:
            continue
        point = ((second[1] - first[1]) / determinant,
                 (first[0] - second[0]) / determinant)
        if all(dot(point, normal) <= 1 for normal in polar_points):
            output.add(point)
    return output


def enumerate_lattice_polygons():
    """All hulls from antipodal subsets of the nonzero [-2,2]^2 lattice."""
    representatives = [
        (x, y)
        for x in range(-2, 3)
        for y in range(-2, 3)
        if (x > 0 or (x == 0 and y > 0))
    ]
    require(len(representatives) == 12, "unexpected lattice representative count")
    polygons = set()
    for mask in range(1, 1 << len(representatives)):
        points = []
        for index, point in enumerate(representatives):
            if mask & (1 << index):
                points.extend((point, (-point[0], -point[1])))
        try:
            polygon = hull(points)
        except RuntimeError:
            continue
        if len(polygon) >= 4:
            polygons.add(polygon)
    require(len(polygons) == 165, "bounded catalogue is incomplete")
    return tuple(sorted(polygons))


def disk_moment(degree):
    """Moments of uniform circle measure divided by pi (total mass two)."""
    require(degree % 2 == 0, "disk audit uses even moments")
    m = degree // 2
    output = []
    for exponent in range(degree + 1):
        if exponent % 2:
            output.append(F(0))
            continue
        a = exponent // 2
        b = m - a
        output.append(F(2 * factorial(2 * a) * factorial(2 * b),
                        4 ** m * factorial(a) * factorial(b) * factorial(m)))
    return tuple(output)


def expect_failure(function):
    try:
        function()
    except RuntimeError:
        return
    raise RuntimeError("negative control was accepted")


def main():
    base = enumerate_lattice_polygons()
    matrices = (
        (1, 0, 0, 1),
        (1, 1, 0, 1),
        (F(3, 5), F(-4, 5), F(4, 5), F(3, 5)),
    )
    catalogue = tuple(sorted({transform(polygon, matrix)
                              for polygon in base for matrix in matrices}))
    require(len(catalogue) == 419, "unexpected transformed-catalogue size")

    counts = {
        "affine_images": len(catalogue),
        "base_lattice_polygons": len(base),
        "catalogue_jet_uniqueness_checks": 0,
        "catalogue_top_term_uniqueness_checks": 0,
        "directional_moment_sandwiches": 0,
        "disk_positive_gram_checks": 0,
        "fourier_mode_checks": 0,
        "gram_rank_checks": 0,
        "negative_controls": 0,
        "polar_hull_checks": 0,
        "radial_ratio_checks": 0,
    }
    facet_counts = {}
    records = []
    cache = {}
    for polygon in catalogue:
        atoms = polar_atoms(polygon)
        r = len(polygon) // 2
        facet_counts[len(polygon)] = facet_counts.get(len(polygon), 0) + 1
        polar = tuple(endpoint for endpoint, _ in atoms)
        require(halfplane_vertices(polar) == set(polygon), "supported polar hull lost C")
        counts["polar_hull_checks"] += 1
        counts["radial_ratio_checks"] += radial_ratio_audit(atoms)
        moments = {degree: moment(atoms, degree) for degree in range(0, 2 * r + 5, 2)}
        cache[polygon] = moments
        for k in range(1, r + 3):
            require(matrix_rank(gram(moments[2 * k], k)) == min(k + 1, r),
                    "facet detector rank failed")
            counts["gram_rank_checks"] += 1
        total_mass = moments[0][0]
        for direction in ((1, 0), (0, 1), (1, 1), (2, -1)):
            maximum = max(abs(dot(direction, endpoint)) for endpoint in polar)
            extremal_mass = sum(weight for endpoint, weight in atoms
                                if abs(dot(direction, endpoint)) == maximum)
            require(maximum > 0 and extremal_mass > 0, "gauge support not attained")
            for degree in (2, 4, 6, 8):
                value = sum(weight * dot(direction, endpoint) ** degree
                            for endpoint, weight in atoms)
                require(extremal_mass * maximum ** degree <= value
                        <= total_mass * maximum ** degree,
                        "directional moment root sandwich failed")
                counts["directional_moment_sandwiches"] += 1
        record = [len(polygon)]
        for degree in range(0, 2 * r + 1, 2):
            record.extend(map(str, moments[degree]))
        records.append(record)

    # The target polygon's top term, and hence also its full jet, is collision
    # free in this complete bounded catalogue even against other facet counts.
    for polygon in catalogue:
        r = len(polygon) // 2
        top = cache[polygon][2 * r]
        same_top = [candidate for candidate in catalogue
                    if cache[candidate].get(2 * r) == top]
        require(same_top == [polygon], "top homogeneous term collision")
        counts["catalogue_top_term_uniqueness_checks"] += 1
        jet = tuple(cache[polygon][degree] for degree in range(0, 2 * r + 1, 2))
        same_jet = [candidate for candidate in catalogue
                    if all(cache[candidate].get(degree) == value
                           for degree, value in zip(range(0, 2 * r + 1, 2), jet))]
        require(same_jet == [polygon], "finite jet collision")
        counts["catalogue_jet_uniqueness_checks"] += 1

    # Smooth infinite-support boundary case: every finite disk Gram matrix is
    # positive definite. This adversarially separates smooth bodies from the
    # finite-facet singularity criterion.
    for k in range(1, 13):
        require(matrix_rank(gram(disk_moment(2 * k), k)) == k + 1,
                "smooth disk produced a singular Gram matrix")
        counts["disk_positive_gram_checks"] += 1

    # Exact sharpness at r=2: a rational non-symmetry rotation of the square
    # has the same constant and quadratic terms but a different fourth term.
    square = hull(((-1, -1), (-1, 1), (1, -1), (1, 1)))
    rotated = transform(square, matrices[2])
    square_atoms, rotated_atoms = polar_atoms(square), polar_atoms(rotated)
    require(moment(square_atoms, 0) == moment(rotated_atoms, 0), "areas changed")
    require(moment(square_atoms, 2) == moment(rotated_atoms, 2), "low square jet changed")
    require(moment(square_atoms, 4) != moment(rotated_atoms, 4), "sharp term vanished")
    require(square != rotated, "sharpness bodies coincide")

    # For every regular 2r-gon, a degree d<2r circle polynomial has frequency
    # d-2j; no nonzero such frequency is divisible by 2r. Hence rotation only
    # changes the first potentially aliased term at degree 2r.
    for r in range(2, 21):
        for degree in range(0, 2 * r):
            for j in range(degree + 1):
                frequency = degree - 2 * j
                require(frequency == 0 or frequency % (2 * r) != 0,
                        "premature regular-polygon Fourier alias")
                counts["fourier_mode_checks"] += 1

    # Negative controls exercise the geometric preconditions, not a decoder.
    expect_failure(lambda: hull(((0, 0), (1, 0), (2, 0))))
    counts["negative_controls"] += 1
    expect_failure(lambda: polar_atoms(tuple(reversed(square))))
    counts["negative_controls"] += 1
    expect_failure(lambda: transform(square, (1, 2, 2, 4)))
    counts["negative_controls"] += 1
    expect_failure(lambda: polar_atoms(hull(((0, 0), (1, 0), (0, 1), (-1, 0)))))
    counts["negative_controls"] += 1

    digest = hashlib.sha256()
    for record in records:
        digest.update((json.dumps(record, separators=(",", ":")) + "\n").encode())
    result = {
        "arithmetic": "fractions.Fraction; no floating point",
        "catalogue_facet_counts": {str(key): facet_counts[key] for key in sorted(facet_counts)},
        "counts": counts,
        "entrywise_sha256": digest.hexdigest(),
        "status": "pass",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
