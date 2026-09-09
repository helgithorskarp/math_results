#!/usr/bin/env python3
"""Independent exact audit of the h4105 complex-radix obstruction.

This does not import the target implementation or read its certificate.  It
uses a different displacement normalization (the first nonzero coefficient is
made 1), SymPy's exact QQ(sqrt(-3)) polynomial arithmetic, and independently
reconstructs the event curves, edge groups, colour covers, collision inventory,
and Bezout union bound.
"""

import argparse
from collections import Counter, defaultdict
from functools import reduce
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd, lcm
from pathlib import Path

import sympy
from sympy import Poly, QQ, expand, sqrt, symbols
from sympy.polys.polytools import gcd as polynomial_gcd


ZERO = (0, 0)
ONE = (1, 0)
TRIANGLE = (ZERO, ONE, (0, 1))
UNITS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
DIFFERENCES = (ZERO,) + UNITS
LABELS = tuple(product(range(3), repeat=5))

x, y, z = symbols("x y z")
s = sqrt(-3)
omega = (1 + s) / 2
omega_bar = (1 - s) / 2
Z = x + s * y
V = x - s * y


def need(condition, message):
    if not condition:
        raise ValueError(message)


def emul(left, right):
    """Multiplication in Z[omega], where omega^2 = omega - 1."""
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c + b * d


def econj(value):
    """Complex conjugation: conjugate(omega) = 1 - omega."""
    a, b = value
    return a + b, -b


def esub(left, right):
    return left[0] - right[0], left[1] - right[1]


def epow(value, exponent):
    result = ONE
    for _ in range(exponent):
        result = emul(result, value)
    return result


def normalize_displacement(row):
    """Quotient unit multiples by making the first nonzero coefficient 1."""
    first = next(coefficient for coefficient in row if coefficient != ZERO)
    inverse = econj(first)
    need(emul(first, inverse) == ONE, "difference coefficient is not a unit")
    return tuple(emul(inverse, coefficient) for coefficient in row)


def displacement_inventory():
    all_classes = {
        normalize_displacement(row)
        for row in product(DIFFERENCES, repeat=5)
        if any(coefficient != ZERO for coefficient in row)
    }
    need(len(all_classes) == (7**5 - 1) // 6 == 2801, "displacement orbit count")

    edge_groups = defaultdict(list)
    for high, right in enumerate(LABELS):
        for low, left in enumerate(LABELS[:high]):
            row = tuple(
                esub(TRIANGLE[right_digit], TRIANGLE[left_digit])
                for left_digit, right_digit in zip(left, right)
            )
            edge_groups[normalize_displacement(row)].append((low, high))
    need(len(edge_groups) == 2801, "realized displacement class count")
    need(set(edge_groups) == all_classes, "label pairs do not realize the full displacement space")
    need(sum(map(len, edge_groups.values())) == len(LABELS) * (len(LABELS) - 1) // 2 == 29403, "label-pair census")
    return tuple(sorted(all_classes)), edge_groups


def qelement(coefficient):
    a, b = coefficient
    return a + b * omega


def qconjugate(coefficient):
    a, b = coefficient
    return a + b * omega_bar


def primitive_key(expression):
    """Canonical primitive integer coefficient stream for a QQ[x,y] polynomial."""
    polynomial = Poly(expand(expression), x, y, domain=QQ)
    entries = polynomial.as_dict()
    need(entries, "zero event polynomial")
    denominator = reduce(lcm, (coefficient.q for coefficient in entries.values()), 1)
    integers = {monomial: int(coefficient * denominator) for monomial, coefficient in entries.items()}
    content = reduce(gcd, integers.values(), 0)
    need(content != 0, "zero primitive content")
    integers = {monomial: coefficient // abs(content) for monomial, coefficient in integers.items()}
    if integers[max(integers)] < 0:
        integers = {monomial: -coefficient for monomial, coefficient in integers.items()}
    return tuple((i, j, integers[i, j]) for i, j in sorted(integers))


def event_polynomial(row):
    displacement = sum(qelement(coefficient) * Z**index for index, coefficient in enumerate(row))
    conjugate = sum(qconjugate(coefficient) * V**index for index, coefficient in enumerate(row))
    expression = expand(displacement * conjugate - 1)
    need(not expression.has(s), "norm expression did not descend to QQ[x,y]")
    return primitive_key(expression)


def total_degree(key):
    return max(i + j for i, j, _ in key)


def simple_root_degree(row):
    """Degree of the product of the multiplicity-one factors over QQ(sqrt(-3))."""
    polynomial = Poly(
        sum(qelement(coefficient) * z**index for index, coefficient in enumerate(row)),
        z,
        extension=s,
    )
    derivative = polynomial.diff()
    squarefree_support = polynomial.exquo(polynomial_gcd(polynomial, derivative))
    repeated_support = polynomial_gcd(squarefree_support, derivative)
    return squarefree_support.exquo(repeated_support).degree()


def build_geometry():
    rows, edge_groups = displacement_inventory()
    circle = primitive_key(x**2 + 3 * y**2 - 1)
    S = x**2 + 3 * y**2
    row_event = {}
    simple_histogram = Counter()
    nonmonomial_events = set()

    for row in rows:
        nonzero = [index for index, coefficient in enumerate(row) if coefficient != ZERO]
        if len(nonzero) == 1:
            index = nonzero[0]
            if index:
                need(event_polynomial(row) == primitive_key(S**index - 1), "radial monomial norm")
                need(expand((S - 1) * sum(S**j for j in range(index)) - (S**index - 1)) == 0, "radial factorization")
                row_event[row] = circle
            else:
                row_event[row] = None
            continue

        key = event_polynomial(row)
        nonmonomial_events.add(key)
        row_event[row] = key
        degree = simple_root_degree(row)
        need(degree > 0, "nonmonomial displacement has no simple root")
        simple_histogram[degree] += 1

    need(len(nonmonomial_events) == 2796, "distinct nonmonomial norm curves")
    need(circle not in nonmonomial_events, "circle duplicates a nonmonomial curve")
    curves = tuple(sorted(nonmonomial_events | {circle}))
    curve_ids = {curve: index for index, curve in enumerate(curves)}
    curve_edges = [[] for _ in curves]
    universal_edges = []
    for row in rows:
        key = row_event[row]
        if key is None:
            universal_edges.extend(edge_groups[row])
        else:
            curve_edges[curve_ids[key]].extend(edge_groups[row])

    need(len(universal_edges) == 243, "universal edge count")
    need(sum(map(len, curve_edges)) + len(universal_edges) == 29403, "event edge partition")
    degrees = tuple(map(total_degree, curves))
    return rows, curves, curve_edges, universal_edges, degrees, dict(sorted(simple_histogram.items())), circle


def f4_multiply(left, right):
    """Multiply a+b*t modulo t^2+t+1, encoded as a+2*b."""
    a, b = left & 1, left >> 1
    c, d = right & 1, right >> 1
    return (a * c ^ b * d) | ((a * d ^ b * c ^ b * d) << 1)


def finite_field_controls():
    need((2 * 2 - 2 + 1) % 3 == 0, "F3 image of omega violates its polynomial")
    for left, right, third in product(range(4), repeat=3):
        need(f4_multiply(left, right) == f4_multiply(right, left), "F4 multiplication is not commutative")
        need(
            f4_multiply(f4_multiply(left, right), third)
            == f4_multiply(left, f4_multiply(right, third)),
            "F4 multiplication is not associative",
        )
        need(
            f4_multiply(left, right ^ third)
            == (f4_multiply(left, right) ^ f4_multiply(left, third)),
            "F4 distributivity",
        )
    need(all(any(f4_multiply(value, inverse) == 1 for inverse in range(1, 4)) for value in range(1, 4)), "F4 inverse")
    return 64


def colour_word(field, weights):
    need(field in (3, 4) and len(weights) == 5 and weights[0] == 1, "colour specification")
    result = []
    for label in LABELS:
        if field == 3:
            result.append(sum(weight * (0, 1, 2)[digit] for weight, digit in zip(weights, label)) % 3)
        else:
            value = 0
            for weight, digit in zip(weights, label):
                value ^= f4_multiply(weight, (0, 1, 2)[digit])
            result.append(value)
    return result


def bad_curves(word, curve_edges, universal_edges):
    need(all(word[left] != word[right] for left, right in universal_edges), "word fails a universal triangle")
    return {
        curve
        for curve, edges in enumerate(curve_edges)
        if any(word[left] == word[right] for left, right in edges)
    }


def finite_colour_audit(rows, curves, curve_edges, universal_edges, degrees, circle):
    single_specs = [(3, (1, 0, 0, 0, 0))]
    single_specs.extend((3, tuple([1] + [int(index == selected) for index in range(4)])) for selected in range(4))
    single_specs.append((3, (1, 1, 1, 1, 1)))
    single_words = [colour_word(*specification) for specification in single_specs]
    assignments = []
    for edges in curve_edges:
        choices = [
            index
            for index, word in enumerate(single_words)
            if all(word[left] != word[right] for left, right in universal_edges + edges)
        ]
        need(choices, "single curve lacks a three-colouring")
        assignments.append(min(choices))

    cover_specs = [
        (3, (1, 0, 0, 0, 0)),
        (4, (1, 0, 1, 0, 1)),
        (4, (1, 1, 0, 0, 1)),
        (4, (1, 1, 0, 0, 2)),
        (4, (1, 1, 1, 1, 1)),
    ]
    cover_words = [colour_word(*specification) for specification in cover_specs]
    bad = [bad_curves(word, curve_edges, universal_edges) for word in cover_words]
    word_scores = [sum(degrees[curve] for curve in failures) for failures in bad]
    protectors = []
    for curve in sorted(bad[0]):
        choices = [index for index, failures in enumerate(bad) if curve not in failures]
        need(choices, "primary failure curve has no protector")
        protectors.append((curve, min(choices, key=lambda index: (word_scores[index], index))))
    pairs = {
        tuple(sorted((curve, other)))
        for curve, protector in protectors
        for other in bad[protector]
    }
    need(all(left != right for left, right in pairs), "pair system contains a repeated curve")

    # Definition-level verification of the affine-hyperplane counts behind the
    # >=4 simultaneous-curve obstruction.  Coefficients reduce in F4 because
    # omega satisfies t^2+t+1 modulo 2.
    tails = tuple(product(range(4), repeat=4))
    nonzero_tails = tuple(product((1, 2, 3), repeat=4))
    unrestricted_failures = Counter()
    nonzero_failures = Counter()
    for row in rows:
        if sum(coefficient != ZERO for coefficient in row) <= 1:
            continue
        coefficients = tuple((a & 1) | ((b & 1) << 1) for a, b in row)

        def fails(tail):
            weights = (1,) + tail
            value = 0
            for weight, coefficient in zip(weights, coefficients):
                value ^= f4_multiply(weight, coefficient)
            return value == 0

        unrestricted = sum(map(fails, tails))
        restricted = sum(map(fails, nonzero_tails))
        need(unrestricted == 64, "F4 affine hyperplane does not have 64 points")
        need(restricted <= 27, "F4 nonzero-tail failure bound")
        unrestricted_failures[unrestricted] += 1
        nonzero_failures[restricted] += 1

    circle_id = curves.index(circle)
    need(all(cover_words[-1][left] != cover_words[-1][right] for left, right in curve_edges[circle_id]), "all-ones word fails circle")
    bezout = sum(degrees[left] * degrees[right] for left, right in pairs)
    return {
        "single_curve_three_coloured": len(assignments),
        "single_assignment_sha256": sha256(json.dumps(assignments, separators=(",", ":")).encode()).hexdigest(),
        "primary_failure_curves": len(bad[0]),
        "primary_failure_degree_sum": sum(degrees[curve] for curve in bad[0]),
        "protector_word_histogram": dict(sorted(Counter(word for _, word in protectors).items())),
        "pair_systems": len(pairs),
        "bezout_sum": bezout,
        "maximum_pair_degree_product": max(degrees[left] * degrees[right] for left, right in pairs),
        "all_nonmonomial_F4_equations_have_64_solutions": unrestricted_failures == {64: 2796},
        "nonzero_tail_failure_histogram": dict(sorted(nonzero_failures.items())),
    }


def collision_inventory(rows):
    collisions = set()
    for row in rows:
        coefficients = list(row)
        while coefficients and coefficients[0] == ZERO:
            coefficients.pop(0)
        while coefficients and coefficients[-1] == ZERO:
            coefficients.pop()
        if len(coefficients) > 1:
            collisions.add(normalize_displacement(tuple(coefficients)))
    histogram = Counter(len(polynomial) - 1 for polynomial in collisions)
    need(histogram == {1: 6, 2: 42, 3: 294, 4: 2058}, "collision inventory")
    return collisions, dict(sorted(histogram.items())), sum(degree * count for degree, count in histogram.items())


def symmetry_controls():
    checks = 0
    omega_squared = emul((0, 1), (0, 1))
    shifts = (ZERO, (-1, 0), (0, -1))
    for index in range(5):
        unit = epow(omega_squared, index)
        left = {emul(unit, digit) for digit in TRIANGLE}
        shift = shifts[index % 3]
        right = {(digit[0] + shift[0], digit[1] + shift[1]) for digit in TRIANGLE}
        need(left == right, "rotation digit translation")
        checks += 1
    need({econj(digit) for digit in TRIANGLE} == {(1 - digit[0], -digit[1]) for digit in TRIANGLE}, "conjugation digit translation")
    return checks + 1


def digest_stream(values):
    return sha256(json.dumps(values, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def run():
    rows, curves, curve_edges, universal_edges, degrees, simple_histogram, circle = build_geometry()
    colour = finite_colour_audit(rows, curves, curve_edges, universal_edges, degrees, circle)
    collisions, collision_histogram, collision_bound = collision_inventory(rows)
    degree_histogram = dict(sorted(Counter(degrees).items()))
    need(degree_histogram == {2: 7, 4: 48, 6: 342, 8: 2400}, "curve degree histogram")
    need(simple_histogram == {1: 24, 2: 102, 3: 330, 4: 2340}, "simple-root histogram")
    need(colour["pair_systems"] == 264800 and colour["bezout_sum"] == 15513472, "finite pair cover")
    need(colour["maximum_pair_degree_product"] == 64, "point field-degree bound")
    need(collision_bound == 9204, "collision root bound")
    return {
        "status": "INDEPENDENT_COMPLEX_RADIX_OBSTRUCTION_VERIFIED",
        "implementation_imports_target": False,
        "target_certificate_read": False,
        "coefficient_domain": "QQ(sqrt(-3)); exact SymPy AlgebraicField",
        "sympy_version": sympy.__version__,
        "labels": len(LABELS),
        "label_pairs": sum(map(len, curve_edges)) + len(universal_edges),
        "canonical_displacements_first_nonzero_normalization": len(rows),
        "event_curve_count": len(curves),
        "event_curve_degree_histogram": degree_histogram,
        "event_curve_stream_sha256": digest_stream(curves),
        "nonmonomial_simple_root_degree_histogram": simple_histogram,
        "universal_edges": len(universal_edges),
        "single_curve_three_coloured": colour["single_curve_three_coloured"],
        "primary_failure_curves": colour["primary_failure_curves"],
        "primary_failure_degree_sum": colour["primary_failure_degree_sum"],
        "protector_word_histogram": colour["protector_word_histogram"],
        "factor_pair_systems": colour["pair_systems"],
        "injective_parameter_bezout_bound": colour["bezout_sum"],
        "maximum_pair_degree_product": colour["maximum_pair_degree_product"],
        "minimum_simultaneous_curves_for_injective_nonfour": 4,
        "all_nonmonomial_F4_equations_have_64_solutions": colour["all_nonmonomial_F4_equations_have_64_solutions"],
        "nonzero_tail_failure_histogram": colour["nonzero_tail_failure_histogram"],
        "collision_polynomials": len(collisions),
        "collision_degree_histogram": collision_histogram,
        "collision_parameter_upper_bound": collision_bound,
        "all_parameter_upper_bound": colour["bezout_sum"] + collision_bound,
        "finite_field_law_triples": finite_field_controls(),
        "parameter_symmetry_digit_checks": symmetry_controls(),
        "sympy_norm_expansions": 2800,
        "sympy_algebraic_gcd_checks": 2796,
        "solver_calls": 0,
        "record_improvement": False,
        "full_architecture_four_colour_closure": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected", type=Path)
    arguments = parser.parse_args()
    result = run()
    json_result = json.loads(json.dumps(result))
    if arguments.expected:
        need(json_result == json.loads(arguments.expected.read_text()), "expected result mismatch")
    print(json.dumps(json_result, indent=2, sort_keys=True))
