#!/usr/bin/env python3
"""Independent exact review of the capped UD9-3 equilateral closure.

No target code is imported.  Dense quadratic forms replace the target's
sparse polynomial engine; a row-weighted contraction bound replaces its
coarser product-norm bound; source colourings are canonical words rather than
DSATUR; and affine coordinate intervals are evaluated directly from their
five rational coefficients.
"""

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
from json import dumps, loads
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "hadwiger_nelson_ud93_equilateral_closure_stop"
TARGET_COMMIT = "9ac74f0c9858aa04d84a72e13f1b903f2dacb978"
TARGET_HASHES = {
    "EXPECTED.json": "b437ecd7250c0c26ac818fd5f58217361046feacf137552e57d4dda9f0df34f3",
    "PROOF.md": "c1db54f95a93d80ba2be798c28a7500f39d66acb77e5fc18c6746de01e89ad83",
    "README.md": "503e72d164ff67492d83b50da3280cca2caf07e6cf9c58a8c5c12075a212e9d1",
    "build_certificate.py": "37d245ecccf2afa044ff9096c0bb4efcf0c057f2961d168b22e8d6cf8f31a98e",
    "certificate.json": "cb6e06023fb334cf60d556df153dfd07c6b239a59214b2d1e6e27559eefec549",
    "controls.py": "9f037721a7d6e0bfeb535e9a2ec135b5d8df712878ce72aff6a7c04bcaf17cee",
    "verify.py": "e22d7cfbada440e5135b1412abe701c57744907c36311d1d6e402fbd826bf522",
}
SOURCE_EDGES = (
    (0, 1), (0, 2), (0, 4), (1, 3), (1, 8), (2, 4), (2, 6),
    (2, 7), (3, 5), (3, 6), (3, 7), (3, 8), (4, 5), (5, 8),
    (6, 7),
)
ROOTS = ((Q(1), Q(0)), (Q(0), Q(1)), (Q(-1), Q(1)),
         (Q(-1), Q(0)), (Q(0), Q(-1)), (Q(1), Q(-1)))
EXPECTED_COUNTS = ((9, 15), (24, 45), (50, 108), (91, 209),
                   (140, 333), (196, 486), (267, 677), (346, 891),
                   (432, 1134), (533, 1415))
QUADRATIC_INDICES = tuple(combinations_with_replacement(range(4), 2))
K = tuple[Q, Q]
Formal = tuple[K, K, K]
Affine = tuple[Q, tuple[Q, Q, Q, Q]]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def kadd(left, right):
    return left[0] + right[0], left[1] + right[1]


def kneg(value):
    return -value[0], -value[1]


def ksub(left, right):
    return kadd(left, kneg(right))


def kmul(left, right):
    # rho^2=rho-1.
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c + b * d


def fn_add(left, right):
    return tuple(kadd(a, b) for a, b in zip(left, right))


def fn_neg(value):
    return tuple(kneg(entry) for entry in value)


def fn_sub(left, right):
    return fn_add(left, fn_neg(right))


def fn_scale(value, scalar):
    return tuple(kmul(entry, scalar) for entry in value)


def formal_source():
    zero = ((Q(0), Q(0)),) * 3

    def basis(index):
        value = list(zero)
        value[index] = (Q(1), Q(0))
        return tuple(value)

    def combine(*terms):
        value = zero
        for coefficient, point in terms:
            value = fn_add(value, fn_scale(point, coefficient))
        return value

    one, z, w = (basis(index) for index in range(3))
    rho = (Q(0), Q(1))
    rhobar = (Q(1), Q(-1))
    alpha = (Q(1, 3), Q(1, 3))
    one_minus_alpha = (Q(2, 3), Q(-1, 3))
    p3 = combine(((Q(0), Q(-1)), one), ((Q(1), Q(1)), w))
    return (
        zero, one, z, w, fn_scale(z, rhobar), p3,
        combine((one_minus_alpha, z), (alpha, w)),
        combine((alpha, z), (one_minus_alpha, w)),
        combine((rhobar, w), (rho, p3)),
    )


def source_directions(source):
    return {
        fn_scale(fn_sub(source[right], source[left]), root)
        for left, right in SOURCE_EDGES for root in ROOTS
    }


def build_closure(last_round=9):
    source = formal_source()
    directions = source_directions(source)
    points = set(source)
    rounds = []
    graphs = {}
    for round_index in range(last_round + 1):
        ordered = tuple(sorted(points))
        edges = tuple(
            (left, right)
            for right in range(len(ordered))
            for left in range(right)
            if fn_sub(ordered[right], ordered[left]) in directions
        )
        entry = {
            "round": round_index,
            "points": len(ordered),
            "complete_unit_edges": len(edges),
        }
        graphs[round_index] = (ordered, edges)
        if round_index < last_round:
            generated = Counter()
            for left, right in edges:
                delta = fn_sub(ordered[right], ordered[left])
                generated[fn_add(ordered[left], fn_scale(delta, ROOTS[1]))] += 1
                generated[fn_add(ordered[left], fn_scale(delta, ROOTS[5]))] += 1
            enlarged = points | set(generated)
            entry.update({
                "raw_completion_attempts": 2 * len(edges),
                "distinct_generated_points": len(generated),
                "new_points": len(enlarged) - len(points),
                "completion_collision_excess": 2 * len(edges) - (len(enlarged) - len(points)),
                "maximum_generated_multiplicity": max(generated.values()),
            })
            points = enlarged
        rounds.append(entry)
    require(tuple((row["points"], row["complete_unit_edges"]) for row in rounds) == EXPECTED_COUNTS,
            "round census")
    return source, directions, tuple(rounds), graphs


# Each equation is N(A,B)-rhs with A and B affine in (x,y,u,v).
EQUATION_DATA = (
    ((Q(0), (Q(1), Q(0), Q(0), Q(0))),
     (Q(0), (Q(0), Q(1), Q(0), Q(0))), Q(1)),
    ((Q(-1), (Q(0), Q(0), Q(1), Q(0))),
     (Q(0), (Q(0), Q(0), Q(0), Q(1))), Q(1)),
    ((Q(0), (Q(-1), Q(0), Q(1), Q(0))),
     (Q(0), (Q(0), Q(-1), Q(0), Q(1))), Q(3)),
    ((Q(0), (Q(-1), Q(-1), Q(1), Q(-1))),
     (Q(-1), (Q(1), Q(0), Q(1), Q(2))), Q(1)),
)


def affine_eval(affine, point):
    constant, coefficients = affine
    return constant + sum(coefficient * value for coefficient, value in zip(coefficients, point))


def equation_value(data, point):
    first, second, right_side = data
    a = affine_eval(first, point)
    b = affine_eval(second, point)
    return a * a + a * b + b * b - right_side


def equation_gradient(data, point):
    first, second, _ = data
    a = affine_eval(first, point)
    b = affine_eval(second, point)
    return tuple((2 * a + b) * first[1][index] + (a + 2 * b) * second[1][index]
                 for index in range(4))


def equation_hessian(data):
    first, second, _ = data
    a = first[1]
    b = second[1]
    return tuple(tuple(2 * a[row] * a[column] + a[row] * b[column]
                       + b[row] * a[column] + 2 * b[row] * b[column]
                       for column in range(4)) for row in range(4))


def dense_norm_polynomial(first, second, right_side=0):
    a0, a = first
    b0, b = second
    values = [a0 * a0 + a0 * b0 + b0 * b0 - Q(right_side)]
    values.extend((2 * a0 + b0) * a[index] + (a0 + 2 * b0) * b[index]
                  for index in range(4))
    for left, right in QUADRATIC_INDICES:
        if left == right:
            values.append(a[left] * a[left] + a[left] * b[left] + b[left] * b[left])
        else:
            values.append(2 * a[left] * a[right] + a[left] * b[right]
                          + a[right] * b[left] + 2 * b[left] * b[right])
    return tuple(values)


def polynomial_add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def polynomial_scale(poly, coefficient):
    return tuple(Q(coefficient) * value for value in poly)


ONE_POLYNOMIAL = (Q(1),) + (Q(0),) * 14
EQUATION_POLYNOMIALS = tuple(dense_norm_polynomial(a, b, rhs) for a, b, rhs in EQUATION_DATA)


def formal_affines(point):
    constant, z_coefficient, w_coefficient = point
    a0, b0 = constant
    p, q = z_coefficient
    r, s = w_coefficient
    first = (a0, (p, -q, r, -s))
    second = (b0, (q, p + q, s, r + s))
    return first, second


def formal_norm_polynomial(point):
    return dense_norm_polynomial(*formal_affines(point))


def determinant(matrix):
    work = [list(row) for row in matrix]
    answer = Q(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        require(pivot is not None, "singular matrix")
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        value = work[column][column]
        answer *= value
        for row in range(column + 1, len(work)):
            factor = work[row][column] / value
            for index in range(column, len(work)):
                work[row][index] -= factor * work[column][index]
    return answer


def root_certificate(certificate):
    require(certificate.get("schema") == "ud93-maximal-capped-equilateral-closure-v1",
            "certificate schema")
    h = certificate["midpoint_denominator"]
    d = certificate["inverse_denominator"]
    rden = certificate["radius_denominator"]
    require(all(type(value) is int and value > 0 for value in (h, d, rden)), "denominators")
    numerators = certificate["midpoint_numerators"]
    inverse_numerators = certificate["inverse_numerators"]
    require(len(numerators) == 4 and all(type(value) is int for value in numerators), "midpoint")
    require(len(inverse_numerators) == 4 and all(len(row) == 4 for row in inverse_numerators)
            and all(type(value) is int for row in inverse_numerators for value in row), "inverse")
    midpoint = tuple(Q(value, h) for value in numerators)
    inverse = tuple(tuple(Q(value, d) for value in row) for row in inverse_numerators)
    radius = Q(1, rden)
    jacobian = tuple(equation_gradient(data, midpoint) for data in EQUATION_DATA)
    residual = tuple(equation_value(data, midpoint) for data in EQUATION_DATA)
    defect = tuple(tuple(Q(row == column) - sum(inverse[row][inner] * jacobian[inner][column]
                                                   for inner in range(4))
                         for column in range(4)) for row in range(4))
    beta = max(sum(abs(value) for value in row) for row in defect)
    hessians = tuple(equation_hessian(data) for data in EQUATION_DATA)
    hessian_weights = tuple(sum(abs(value) for row in hessian for value in row)
                            for hessian in hessians)
    variation = radius * max(sum(abs(inverse[row][equation]) * hessian_weights[equation]
                                 for equation in range(4)) for row in range(4))
    contraction = beta + variation
    residual_image = max(abs(sum(inverse[row][equation] * residual[equation]
                                 for equation in range(4))) for row in range(4))
    displacement = residual_image + contraction * radius
    inverse_determinant = determinant(inverse)
    require(inverse_determinant and contraction < 1 and displacement < radius,
            "independent contraction certificate")
    require(beta < Q(1, 10**64), "inverse-defect threshold")
    require(variation < Q(1, 10**33) and contraction < Q(1, 10**33),
            "contraction-factor threshold")
    require(displacement < Q(1, 10**68), "self-map displacement threshold")
    digest = sha256("".join(f"{value.numerator}/{value.denominator}\n"
                             for value in (beta, variation, contraction, residual_image,
                                           displacement, inverse_determinant)).encode()).hexdigest()
    return midpoint, radius, {
        "inverse_determinant_nonzero": True,
        "beta_lt_1e64_inverse": beta < Q(1, 10**64),
        "row_weighted_variation_lt_1e33_inverse": variation < Q(1, 10**33),
        "contraction_factor_lt_1e33_inverse": contraction < Q(1, 10**33),
        "self_map_displacement_lt_1e68_inverse": displacement < Q(1, 10**68),
        "exact_bound_tuple_sha256": digest,
    }


def interval_product(left, right):
    products = tuple(a * b for a in left for b in right)
    return min(products), max(products)


def interval_add(left, right):
    return left[0] + right[0], left[1] + right[1]


def norm_interval(first, first_error, second, second_error):
    a = (first - first_error, first + first_error)
    b = (second - second_error, second + second_error)
    return interval_add(interval_add(interval_product(a, a), interval_product(a, b)),
                        interval_product(b, b))


def physical_audit(points, edges, midpoint, radius):
    affines = tuple(formal_affines(point) for point in points)
    values = tuple(tuple(affine_eval(coordinate, midpoint) for coordinate in pair) for pair in affines)
    errors = tuple(tuple(radius * sum(abs(value) for value in coordinate[1]) for coordinate in pair)
                   for pair in affines)
    edge_set = set(edges)
    separation = None
    separation_pair = None
    nonedge_gap = None
    nonedge_pair = None
    pair_checks = 0
    for right in range(len(points)):
        for left in range(right):
            pair_checks += 1
            first = values[right][0] - values[left][0]
            second = values[right][1] - values[left][1]
            first_error = errors[right][0] + errors[left][0]
            second_error = errors[right][1] + errors[left][1]
            lower, upper = norm_interval(first, first_error, second, second_error)
            require(lower > 0, "unresolved collision")
            if separation is None or lower < separation:
                separation, separation_pair = lower, (left, right)
            if (left, right) in edge_set:
                require(lower <= 1 <= upper, "declared edge interval")
            else:
                require(upper < 1 or lower > 1, "unresolved nonedge")
                gap = min(abs(lower - 1), abs(upper - 1))
                if nonedge_gap is None or gap < nonedge_gap:
                    nonedge_gap, nonedge_pair = gap, (left, right)
    return {
        "pair_checks": pair_checks,
        "separation_gt_1e4_inverse": separation > Q(1, 10000),
        "separation_argmin_pair": list(separation_pair),
        "nonedge_unit_gap_gt_1e3_inverse": nonedge_gap > Q(1, 1000),
        "nonedge_unit_gap_argmin_pair": list(nonedge_pair),
    }


def canonical_colourings(order, edges, colours):
    earlier = [[] for _ in range(order)]
    for left, right in edges:
        earlier[right].append(left)
    word = [-1] * order
    word[0] = 0
    output = []

    def visit(vertex, maximum):
        if vertex == order:
            output.append("".join(map(str, word)))
            return
        for colour in range(min(colours - 1, maximum + 1) + 1):
            if all(word[neighbour] != colour for neighbour in earlier[vertex]):
                word[vertex] = colour
                visit(vertex + 1, max(maximum, colour))
        word[vertex] = -1

    visit(1, 0)
    return tuple(output)


def proper(word, order, edges, colours=4):
    return (isinstance(word, str) and len(word) == order
            and set(word) <= set(map(str, range(colours)))
            and all(word[left] != word[right] for left, right in edges))


def formal_point_hash(points):
    stream = "".join(
        f"{index}:" + ";".join(f"{a.numerator}/{a.denominator},{b.numerator}/{b.denominator}"
                                for a, b in point) + "\n"
        for index, point in enumerate(points)
    )
    return sha256(stream.encode()).hexdigest()


def edge_hash(edges):
    return sha256("".join(f"{left} {right}\n" for left, right in edges).encode()).hexdigest()


def verify(certificate_path=None):
    for name, expected in TARGET_HASHES.items():
        require(file_hash(TARGET / name) == expected, "target input hash: " + name)
    certificate_path = Path(certificate_path) if certificate_path else TARGET / "certificate.json"
    certificate = loads(certificate_path.read_text())
    midpoint, radius, contraction = root_certificate(certificate)
    source, directions, rounds, graphs = build_closure()
    require(len(source) == 9 and len(directions) == 30, "source/direction census")

    allowed_norms = {
        ONE_POLYNOMIAL,
        polynomial_add(ONE_POLYNOMIAL, EQUATION_POLYNOMIALS[0]),
        polynomial_add(ONE_POLYNOMIAL, EQUATION_POLYNOMIALS[1]),
        polynomial_add(ONE_POLYNOMIAL,
                       polynomial_scale(EQUATION_POLYNOMIALS[2], Q(1, 3))),
        polynomial_add(ONE_POLYNOMIAL, EQUATION_POLYNOMIALS[3]),
    }
    source_norms = {formal_norm_polynomial(fn_sub(source[right], source[left]))
                    for left, right in SOURCE_EDGES}
    require(source_norms == allowed_norms and len(source_norms) == 5, "five source direction classes")
    require(all(formal_norm_polynomial(direction) in allowed_norms for direction in directions),
            "rotated direction norm proof")

    points, edges = graphs[8]
    next_points, next_edges = graphs[9]
    audit = physical_audit(points, edges, midpoint, radius)
    next_audit = physical_audit(next_points, next_edges, midpoint, radius)
    require(audit["pair_checks"] + next_audit["pair_checks"] == 234874, "pair audit count")
    require(audit["separation_gt_1e4_inverse"] and next_audit["separation_gt_1e4_inverse"],
            "separation margin")
    require(audit["nonedge_unit_gap_gt_1e3_inverse"] and
            next_audit["nonedge_unit_gap_gt_1e3_inverse"], "nonedge margin")

    three_words = canonical_colourings(9, SOURCE_EDGES, 3)
    four_words = canonical_colourings(9, SOURCE_EDGES, 4)
    require(not three_words and four_words, "source chromatic census")
    word = certificate["four_colour_word"]
    require(proper(word, len(points), edges), "round-eight four-colour word")
    source_positions = {point: index for index, point in enumerate(points)}
    require(len(source_positions) == len(points) and all(point in source_positions for point in source),
            "source embedding")

    expected = loads((TARGET / "EXPECTED.json").read_text())
    point_sha = formal_point_hash(points)
    edge_sha = edge_hash(edges)
    next_point_sha = formal_point_hash(next_points)
    next_edge_sha = edge_hash(next_edges)
    require(point_sha == expected["point_stream_sha256"] and edge_sha == expected["edge_stream_sha256"]
            and next_point_sha == expected["next_point_stream_sha256"]
            and next_edge_sha == expected["next_edge_stream_sha256"], "target stream hashes")

    return {
        "checker": "independent dense-quadratic contraction and affine-interval closure audit",
        "target_code_imported": False,
        "target_mathematical_commit": TARGET_COMMIT,
        "root_certificate": contraction,
        "source": {
            "points": 9,
            "complete_unit_edges": 15,
            "direction_classes": len(source_norms),
            "oriented_unit_directions": len(directions),
            "canonical_three_colourings": len(three_words),
            "canonical_four_colourings": len(four_words),
            "chromatic_number": 4,
        },
        "round_census": list(rounds),
        "round_eight": {
            "points": len(points),
            "complete_unit_edges": len(edges),
            "chromatic_number": 4,
            "proper_literal_four_word": True,
            "point_stream_sha256": point_sha,
            "edge_stream_sha256": edge_sha,
            "physical_audit": audit,
        },
        "round_nine": {
            "points": len(next_points),
            "complete_unit_edges": len(next_edges),
            "point_stream_sha256": next_point_sha,
            "edge_stream_sha256": next_edge_sha,
            "physical_audit": next_audit,
        },
        "certificate_sha256": file_hash(certificate_path),
        "verdict": "ACCEPT_COMPLETE_ROUND_STOP",
        "record_candidate": False,
        "scope": "one exact UD9-3 realization and its complete equilateral closure rounds zero through nine",
    }


def main():
    print(dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
