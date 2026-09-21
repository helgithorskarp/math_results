"""Independent exact audit of the maximum-gap square-localization witness.

The target solves for a center/radius or branch-adapted square parameter and
intersects general halfspaces.  This checker instead assigns four cyclically
ordered square vertices to edges, parametrizes each edge by lambda in [0,1],
and intersects the resulting affine square equations with the four-cube by
enumerating cube faces.  It imports no target module or fixture.
"""

import hashlib
import json
from fractions import Fraction as F
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add(first, second):
    return first[0] + second[0], first[1] + second[1]


def subtract(first, second):
    return first[0] - second[0], first[1] - second[1]


def scale(value, vector):
    return value * vector[0], value * vector[1]


def dot(first, second):
    return sum(a * b for a, b in zip(first, second))


def squared_norm(vector):
    return dot(vector, vector)


def affine_solution(rows, right, variables):
    """Return (particular, nullspace basis), or None if inconsistent."""
    matrix = [[F(value) for value in row] + [F(value)]
              for row, value in zip(rows, right)]
    pivot_columns = []
    pivot_row = 0
    for column in range(variables):
        pivot = next((row for row in range(pivot_row, len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        divisor = matrix[pivot_row][column]
        matrix[pivot_row] = [value / divisor for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row != pivot_row and matrix[row][column]:
                multiplier = matrix[row][column]
                matrix[row] = [left - multiplier * right_value
                               for left, right_value in zip(matrix[row], matrix[pivot_row])]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    if any(not any(row[:variables]) and row[variables] for row in matrix):
        return None
    free_columns = [column for column in range(variables)
                    if column not in pivot_columns]
    particular = [F(0)] * variables
    for row, column in enumerate(pivot_columns):
        particular[column] = matrix[row][variables]
    basis = []
    for free in free_columns:
        vector = [F(0)] * variables
        vector[free] = F(1)
        for row, column in enumerate(pivot_columns):
            vector[column] = -matrix[row][free]
        basis.append(tuple(vector))
    return tuple(particular), tuple(basis)


def cube_section_vertices(rows, right):
    """Vertices of {lambda in [0,1]^4: rows*lambda=right}."""
    solution = affine_solution(rows, right, 4)
    if solution is None:
        return (), None
    particular, basis = solution
    dimension = len(basis)
    vertices = set()
    for fixed_coordinates in combinations(range(4), dimension):
        for endpoint_values in product((F(0), F(1)), repeat=dimension):
            augmented_rows = list(rows)
            augmented_right = list(right)
            for coordinate, value in zip(fixed_coordinates, endpoint_values):
                row = [F(0)] * 4
                row[coordinate] = F(1)
                augmented_rows.append(tuple(row))
                augmented_right.append(value)
            candidate = affine_solution(augmented_rows, augmented_right, 4)
            if candidate is None or candidate[1]:
                continue
            point = candidate[0]
            if all(0 <= value <= 1 for value in point):
                vertices.add(point)
    # In dimension zero, the empty fixed-coordinate choice is already used.
    return tuple(sorted(vertices)), dimension


def point_on_edge(edge, parameter):
    start, end = edge
    return add(start, scale(parameter, subtract(end, start)))


def square_equations(edges):
    """Affine equations for p0,p1,p2,p3=c+v,c+Jv,c-v,c-Jv."""
    starts = [edge[0] for edge in edges]
    directions = [subtract(edge[1], edge[0]) for edge in edges]
    # Each item gives coefficients of the x and y coordinates of p_i.
    equations = (
        ((1, 0), (-1, 0), (1, 0), (-1, 0)),
        ((0, 1), (0, -1), (0, 1), (0, -1)),
        ((0, 1), (1, 0), (0, -1), (-1, 0)),
        ((-1, 0), (0, 1), (1, 0), (0, -1)),
    )
    rows, right = [], []
    for equation in equations:
        row = tuple(dot(coefficient, direction)
                    for coefficient, direction in zip(equation, directions))
        constant = sum(dot(coefficient, start)
                       for coefficient, start in zip(equation, starts))
        rows.append(row)
        right.append(-constant)
    return tuple(rows), tuple(right)


def ordered_square(edges, parameters):
    return tuple(point_on_edge(edge, parameter)
                 for edge, parameter in zip(edges, parameters))


def validate_square(points):
    center_twice = add(points[0], points[2])
    require(center_twice == add(points[1], points[3]), "diagonals do not bisect")
    sides = [subtract(points[(index + 1) % 4], points[index]) for index in range(4)]
    side_square = squared_norm(sides[0])
    require(all(squared_norm(side) == side_square for side in sides), "unequal sides")
    require(all(dot(sides[index], sides[(index + 1) % 4]) == 0
                for index in range(4)), "non-right angle")
    return side_square


def canonical(points):
    return tuple(sorted(points))


def enumerate_squares(edges):
    squares = set()
    statistics = {
        "affine_dimension_0": 0,
        "affine_dimension_1": 0,
        "assignments": 0,
        "feasible_assignments": 0,
        "inconsistent_equations": 0,
        "positive_square_singular_assignments": 0,
        "singular_feasible_assignments": 0,
    }
    trace = hashlib.sha256()
    for assignment in product(range(len(edges)), repeat=4):
        assigned = tuple(edges[index] for index in assignment)
        rows, right = square_equations(assigned)
        vertices, dimension = cube_section_vertices(rows, right)
        statistics["assignments"] += 1
        if dimension is None:
            statistics["inconsistent_equations"] += 1
            trace.update((json.dumps([assignment, None, []]) + "\n").encode())
            continue
        statistics[f"affine_dimension_{dimension}"] = (
            statistics.get(f"affine_dimension_{dimension}", 0) + 1
        )
        if vertices:
            statistics["feasible_assignments"] += 1
            if dimension:
                statistics["singular_feasible_assignments"] += 1
        positive = False
        trace_vertices = []
        for parameters in vertices:
            points = ordered_square(assigned, parameters)
            side_square = validate_square(points)
            trace_vertices.append([[str(x), str(y)] for x, y in points])
            if side_square:
                positive = True
                squares.add(canonical(points))
        if dimension and positive:
            statistics["positive_square_singular_assignments"] += 1
        # A bounded cube section is the convex hull of its vertices. If every
        # vertex has zero diagonal, every point of that section is degenerate.
        if dimension and vertices and not positive:
            require(all(points[0] == points[2]
                        for points in (ordered_square(assigned, vertex)
                                       for vertex in vertices)),
                    "zero-side singular family was not linear-degenerate")
        trace.update((json.dumps([assignment, dimension, trace_vertices],
                                 separators=(",", ":")) + "\n").encode())
    return squares, dict(sorted(statistics.items())), trace.hexdigest()


def interpolate(xs, values, x):
    for index, (left, right) in enumerate(zip(xs, xs[1:])):
        if left <= x <= right:
            parameter = (x - left) / (right - left)
            return values[index] + parameter * (values[index + 1] - values[index])
    raise RuntimeError("point outside interpolation interval")


def gap_value(xs, lower, upper, x):
    return interpolate(xs, upper, x) - interpolate(xs, lower, x)


def expect_failure(function):
    try:
        function()
    except RuntimeError:
        return
    raise RuntimeError("negative control was accepted")


def main():
    xs = tuple(map(F, (0, 4, 6, 8, 10)))
    lower = tuple(map(F, (0, F(-9, 5), F(-18, 5), F(-93, 50), 0)))
    upper = tuple(map(F, (0, F(9, 5), 0, F(9, 5), 0)))
    lower_slopes = tuple((b - a) / (right - left)
                         for a, b, left, right in zip(lower, lower[1:], xs, xs[1:]))
    upper_slopes = tuple((b - a) / (right - left)
                         for a, b, left, right in zip(upper, upper[1:], xs, xs[1:]))
    require(max(map(abs, lower_slopes + upper_slopes)) == F(93, 100),
            "wrong strict Lipschitz constant")
    gaps = tuple(b - a for a, b in zip(lower, upper))
    require(gaps[3] == F(183, 50)
            and all(value < gaps[3] for index, value in enumerate(gaps) if index != 3),
            "peak is not unique")
    lower_points = tuple(zip(xs, lower))
    upper_points = tuple(zip(xs, upper))
    edges = tuple(zip(lower_points, lower_points[1:])) + tuple(zip(upper_points, upper_points[1:]))

    squares, statistics, trace_digest = enumerate_squares(edges)
    require(statistics["assignments"] == 4096, "assignment space incomplete")
    require(statistics["positive_square_singular_assignments"] == 0,
            "nonzero singular square family found")
    require(len(squares) == 3, "witness does not have exactly three squares")

    expected_parameters = (
        (F(1016, 497), F(-2286, 2485), F(1206, 497), F(-648, 497)),
        (F(104, 49), F(-234, 245), F(18, 7), F(-72, 49)),
        (F(44202, 10439), F(-104958, 52195), F(37872, 10439), F(324, 10439)),
    )
    expected = set()
    for t, y, a, b in expected_parameters:
        expected.add(canonical(((t, y), (t + a - b, y + a + b),
                                (t + a, y + b), (t - b, y + a))))
    require(squares == expected, "independent square list differs from certificate")

    rightmost = max(x for square in squares for x, _ in square)
    require(rightmost == F(82074, 10439), "wrong rightmost square point")
    require(F(8) - rightmost == F(1438, 10439), "wrong peak separation")
    maximum_side_square = max(
        min(squared_norm(subtract(first, second))
            for first, second in combinations(square, 2))
        for square in squares
    )
    require(maximum_side_square == F(1434393360, 108972721), "wrong largest square")

    # The gap is affine between knots. Hence extrema on the complement of the
    # open band occur at knots or band endpoints.
    band = (F(63, 8), F(65, 8))
    candidates = tuple(x for x in xs if x <= band[0] or x >= band[1]) + band
    outside_maximum = max(gap_value(xs, lower, upper, x) for x in candidates)
    require(outside_maximum == F(117, 32)
            and gaps[3] - outside_maximum == F(3, 800),
            "wrong robust peak margin")
    require(rightmost < band[0], "a square reaches the protected band")
    require(4 * F(3, 3200) == F(3, 800), "perturbation margin arithmetic failed")

    # Definition-level checks of the projection envelope for every exact
    # square. Maxima of the piecewise-affine gap on a projection occur at its
    # endpoints or at original knots.
    envelope_checks = 0
    for t, y, a, b in expected_parameters:
        projection = (min(t, t + a, t - b, t + a - b),
                      max(t, t + a, t - b, t + a - b))
        critical = [projection[0], projection[1]]
        critical.extend(x for x in xs if projection[0] <= x <= projection[1])
        require(max(gap_value(xs, lower, upper, x) for x in critical) <= 2 * a,
                "whole-projection envelope failed")
        require(a * a <= a * a + b * b, "side comparison failed")
        envelope_checks += len(critical)

    # Bernstein premises are exact at coefficient level: positive interior
    # sampled gaps and difference quotients bounded by 0.93. The stability
    # lemma, not these finite samples, supplies the eventual counterexamples.
    bernstein_checks = 0
    for degree in range(2, 81):
        sampled_lower = tuple(interpolate(xs, lower, F(10 * k, degree))
                              for k in range(degree + 1))
        sampled_upper = tuple(interpolate(xs, upper, F(10 * k, degree))
                              for k in range(degree + 1))
        require(all(sampled_lower[k] < sampled_upper[k] for k in range(1, degree)),
                "nonpositive interior Bernstein coefficient")
        for samples in (sampled_lower, sampled_upper):
            derivative_controls = tuple(F(degree, 10) * (b - a)
                                        for a, b in zip(samples, samples[1:]))
            require(max(map(abs, derivative_controls)) <= F(93, 100),
                    "Bernstein Lipschitz preservation failed")
            bernstein_checks += len(derivative_controls)

    # A rectangle supplies an independent positive-dimensional control. Some
    # cube sections must contain nondegenerate squares, so singular families
    # are not silently discarded by the face enumeration.
    rectangle = ((F(0), F(0)), (F(2), F(0)), (F(2), F(1)), (F(0), F(1)))
    rectangle_edges = tuple(zip(rectangle, rectangle[1:] + rectangle[:1]))
    _, rectangle_stats, _ = enumerate_squares(rectangle_edges)
    require(rectangle_stats["assignments"] == 256
            and rectangle_stats["positive_square_singular_assignments"] > 0,
            "positive-dimensional rectangle control failed")

    expect_failure(lambda: require(F(1) < F(1), "strictness lost"))
    expect_failure(lambda: interpolate(xs, lower, F(11)))

    result = {
        "arithmetic": "fractions.Fraction; no floating point",
        "bernstein_difference_quotient_checks": bernstein_checks,
        "envelope_critical_point_checks": envelope_checks,
        "full_assignment_stats": statistics,
        "independent_trace_sha256": trace_digest,
        "maximum_gap": str(gaps[3]),
        "maximum_side_squared": str(maximum_side_square),
        "nondegenerate_squares": [
            [[str(x), str(y)] for x, y in square] for square in sorted(squares)
        ],
        "outside_band_gap_maximum": str(outside_maximum),
        "peak_separation": str(F(8) - rightmost),
        "rectangle_control_stats": rectangle_stats,
        "status": "pass",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
