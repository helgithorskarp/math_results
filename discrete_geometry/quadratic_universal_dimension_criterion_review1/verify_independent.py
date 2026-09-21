#!/usr/bin/env python3
"""Independent exact audit of the quadratic coefficient criterion.

CPython 3.11+, standard library only.  This imports no target code or target
output.  It checks the coefficient partition through Hessian geometry,
constructs rational certificates for both failure mechanisms, audits all
coordinate permutations, checks a level-three no-carry Cantor identity, and
tests the strict dimension-parameter choice used at the Ren--Wang interface.
The Ren--Wang theorem and Hausdorff-dimension arguments remain human inputs.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product
import argparse
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def normalize(coefficients):
    require(len(coefficients) == 9, "nine coefficients required")
    require(all(isinstance(value, (int, Fraction))
                and not isinstance(value, bool) for value in coefficients),
            "exact rational coefficients required")
    return tuple(Fraction(value) for value in coefficients)


def hessian_and_linear(coefficients):
    a, b, c, d, e, f, g, h, i = normalize(coefficients)
    return (
        ((2 * a, d, e), (d, 2 * b, f), (e, f, 2 * c)),
        (g, h, i),
    )


def evaluate(coefficients, point):
    a, b, c, d, e, f, g, h, i = normalize(coefficients)
    x, y, z = map(Fraction, point)
    return (a*x*x + b*y*y + c*z*z + d*x*y + e*x*z + f*y*z
            + g*x + h*y + i*z)


def line_condition_axis(matrix, linear, axis):
    if matrix[axis][axis]:
        return True
    others = [index for index in range(3) if index != axis]
    return (all(not matrix[axis][index] for index in others)
            and bool(linear[axis]))


def line_condition(coefficients):
    matrix, linear = hessian_and_linear(coefficients)
    return all(line_condition_axis(matrix, linear, axis)
               for axis in range(3))


def constant_line_certificate(coefficients, axis):
    matrix, linear = hessian_and_linear(coefficients)
    require(not line_condition_axis(matrix, linear, axis),
            "axis has no constant line")
    require(not matrix[axis][axis], "quadratic restriction cannot be constant")
    fixed = [Fraction(0)] * 3
    other = next((index for index in range(3)
                  if index != axis and matrix[axis][index]), None)
    if other is None:
        require(not linear[axis], "constant nonzero slope")
    else:
        fixed[other] = -linear[axis] / matrix[axis][other]
    values = []
    for parameter in (-3, -1, 0, 2, 5):
        point = fixed[:]
        point[axis] = Fraction(parameter)
        values.append(evaluate(coefficients, point))
    require(len(set(values)) == 1, "constant-line certificate failed")
    return tuple(fixed)


def coefficient_map_jacobian(coefficients, pin):
    """Coefficients of det D(L_pin,R_pin), derived from Hessian rows."""
    matrix, linear = hessian_and_linear(coefficients)
    free = [index for index in range(3) if index != pin]
    first, second = free
    # L = M[pin,first]*x_first + M[pin,second]*x_second + linear[pin]
    # grad R in the free variables uses the corresponding Hessian block.
    coefficient_first = (matrix[pin][first] * matrix[second][first]
                         - matrix[pin][second] * matrix[first][first])
    coefficient_second = (matrix[pin][first] * matrix[second][second]
                          - matrix[pin][second] * matrix[first][second])
    constant = (matrix[pin][first] * linear[second]
                - matrix[pin][second] * linear[first])
    return coefficient_first, coefficient_second, constant


def rank_condition(coefficients):
    return any(any(coefficient_map_jacobian(coefficients, pin))
               for pin in range(3))


def raw_conditions(coefficients):
    """Fast integer version for the exhaustive grid."""
    a, b, c, d, e, f, g, h, i = coefficients
    matrix = ((2*a, d, e), (d, 2*b, f), (e, f, 2*c))
    linear = (g, h, i)
    condition_l = all(
        matrix[axis][axis]
        or (all(not matrix[axis][other] for other in range(3)
                if other != axis) and linear[axis])
        for axis in range(3)
    )
    condition_r = False
    for pin in range(3):
        first, second = [axis for axis in range(3) if axis != pin]
        jacobian = (
            matrix[pin][first] * matrix[second][first]
            - matrix[pin][second] * matrix[first][first],
            matrix[pin][first] * matrix[second][second]
            - matrix[pin][second] * matrix[first][second],
            matrix[pin][first] * linear[second]
            - matrix[pin][second] * linear[first],
        )
        condition_r = condition_r or any(jacobian)
    return bool(condition_l), bool(condition_r)


def additive_certificate(coefficients):
    """Certify the R-failure alternatives under the line condition."""
    coefficients = normalize(coefficients)
    require(line_condition(coefficients) and not rank_condition(coefficients),
            "additive certificate requested outside L and not-R")
    a, b, c, d, e, f, g, h, i = coefficients
    mixed = (d, e, f)
    if not any(mixed):
        # G is the identity and the three summands are the coordinate pieces.
        return {
            "type": "separated_sum",
            "pieces": ((a, g), (b, h), (c, i)),
        }
    require(all(mixed), "zero Jacobians plus L forbid one or two mixed terms")
    scale = d * e / (2 * f)
    vector = (Fraction(1), f / e, f / d)
    require((a, b, c) == tuple(scale * value * value for value in vector),
            "rank-one quadratic coefficients do not factor")
    require((d, e, f) == (2*scale*vector[0]*vector[1],
                           2*scale*vector[0]*vector[2],
                           2*scale*vector[1]*vector[2]),
            "rank-one mixed coefficients do not factor")
    require((g, h, i) == tuple(g * value for value in vector),
            "linear term is not aligned with rank-one direction")
    return {
        "type": "quadratic_of_linear_form",
        "scale": scale,
        "vector": vector,
        "linear": g,
    }


def evaluate_additive_certificate(certificate, point):
    x, y, z = map(Fraction, point)
    if certificate["type"] == "separated_sum":
        return sum(q*t*t + l*t for (q, l), t
                   in zip(certificate["pieces"], (x, y, z)))
    vector = certificate["vector"]
    total = sum(value * coordinate for value, coordinate
                in zip(vector, (x, y, z)))
    return certificate["scale"] * total * total + certificate["linear"] * total


def coefficient_grid_audit():
    values = (-2, -1, 0, 1)
    counts = {
        "vectors": 0,
        "line_failure": 0,
        "line_and_rank": 0,
        "line_and_additive": 0,
        "separated_additive": 0,
        "rank_one_additive": 0,
        "constant_line_certificates": 0,
        "constant_line_evaluations": 0,
        "additive_identity_evaluations": 0,
    }
    digest = sha256()
    test_points = ((0, 0, 0), (1, -1, 2), (-2, 3, 1))
    certified_axes = set()
    for serial, raw in enumerate(product(values, repeat=9)):
        counts["vectors"] += 1
        condition_l, condition_r = raw_conditions(raw)
        if not condition_l:
            counts["line_failure"] += 1
            a, b, c, d, e, f, g, h, i = raw
            matrix = ((2*a, d, e), (d, 2*b, f), (e, f, 2*c))
            linear = (g, h, i)
            failing_axes = []
            for axis in range(3):
                if line_condition_axis(matrix, linear, axis):
                    continue
                failing_axes.append(axis)
            require(failing_axes, "line failure lacks a failing axis")
            chosen = next((axis for axis in failing_axes
                           if axis not in certified_axes), failing_axes[0])
            if serial % 127 == 0 or chosen not in certified_axes:
                constant_line_certificate(raw, chosen)
                certified_axes.add(chosen)
                counts["constant_line_certificates"] += 1
                counts["constant_line_evaluations"] += 5
            kind = "L0"
        elif condition_r:
            counts["line_and_rank"] += 1
            kind = "LR"
        else:
            counts["line_and_additive"] += 1
            certificate = additive_certificate(raw)
            key = ("separated_additive" if certificate["type"] == "separated_sum"
                   else "rank_one_additive")
            counts[key] += 1
            for point in test_points:
                require(evaluate(raw, point)
                        == evaluate_additive_certificate(certificate, point),
                        ("additive identity failed", raw, point))
                counts["additive_identity_evaluations"] += 1
            kind = "AS" if key == "separated_additive" else "AR"
        digest.update((kind + ":" + ",".join(map(str, raw)) + "\n").encode())
    require(sum(counts[key] for key in
                ("line_failure", "line_and_rank", "line_and_additive"))
            == counts["vectors"], "coefficient partition incomplete")
    require(counts["line_and_additive"] ==
            counts["separated_additive"] + counts["rank_one_additive"],
            "additive subtype partition incomplete")
    return counts, digest.hexdigest()


def permute_coefficients(coefficients, permutation):
    matrix, linear = hessian_and_linear(coefficients)
    permuted_matrix = tuple(tuple(matrix[permutation[row]][permutation[col]]
                                  for col in range(3)) for row in range(3))
    permuted_linear = tuple(linear[permutation[row]] for row in range(3))
    return (
        permuted_matrix[0][0] / 2,
        permuted_matrix[1][1] / 2,
        permuted_matrix[2][2] / 2,
        permuted_matrix[0][1],
        permuted_matrix[0][2],
        permuted_matrix[1][2],
        *permuted_linear,
    )


def permutation_audit():
    fixtures = (
        (0, 0, 0, 1, 1, 0, 0, 0, 0),       # line failure, rank passes
        (1, 1, 1, 0, 0, 0, 0, 0, 0),       # separated additive
        (1, 1, 1, 2, 2, 2, 3, 3, 3),       # quadratic of one linear form
        (1, 1, 1, 1, 0, 0, 0, 0, 0),       # both conditions
        (2, -1, 1, 1, -2, 1, 3, -1, 2),    # generic
    )
    checked = 0
    for fixture in fixtures:
        baseline = line_condition(fixture), rank_condition(fixture)
        for permutation in permutations(range(3)):
            moved = permute_coefficients(fixture, permutation)
            require((line_condition(moved), rank_condition(moved)) == baseline,
                    ("coordinate permutation changed criterion", fixture,
                     permutation))
            checked += 1
    return checked


def cantor_level_three_audit():
    base = 27
    digits = range(9)
    prefixes = {u * base * base + v * base + w
                for u in digits for v in digits for w in digits}
    pair_sums = {left + right for left in prefixes for right in prefixes}
    triple_sums = {pair + right for pair in pair_sums for right in prefixes}
    expected = {u * base * base + v * base + w
                for u in range(25) for v in range(25) for w in range(25)}
    require(triple_sums == expected, "level-three no-carry identity failed")
    require(len(prefixes) == 9**3 and len(pair_sums) == 17**3
            and len(triple_sums) == 25**3, "Cantor prefix counts failed")
    require(9**3 == 27**2 and 25 < 27,
            "Cantor dimension comparison failed")
    return {
        "base": base,
        "levels": 3,
        "input_prefixes": len(prefixes),
        "pair_sum_prefixes": len(pair_sums),
        "triple_sum_prefixes": len(triple_sums),
    }


def projection_parameter_audit():
    """Audit the strict alpha', beta' choice on an exact rational grid."""
    checked = 0
    for alpha_n, beta_n, gamma_n in product(range(1, 9), repeat=3):
        alpha = Fraction(alpha_n, 8)
        beta = Fraction(beta_n, 8)
        gamma = Fraction(gamma_n, 8)
        total = alpha + beta + gamma
        if total > 2 or gamma >= total / 2:
            continue
        for u_n in range(1, 33):
            u = Fraction(u_n, 32)
            if u >= total / 2:
                continue
            margin = min(alpha, beta, alpha + beta - u, total - 2*u)
            require(margin > 0, "strict margin unexpectedly absent")
            delta = margin / 4
            alpha_prime = alpha - delta
            beta_prime = beta - delta
            s_value = alpha_prime + beta_prime
            require(alpha_prime > 0 and beta_prime > 0 and s_value > u
                    and s_value + gamma > 2*u,
                    "Frostman exponent choice failed")
            exceptional_bound = max(2*u - s_value, Fraction(0))
            require(exceptional_bound < gamma,
                    "exceptional direction bound not strict")
            checked += 1
    return checked


def malformed_controls():
    rejected = 0
    for bad in ((0,) * 8, (0,) * 8 + (0.0,), (0,) * 8 + (True,)):
        try:
            normalize(bad)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("malformed coefficient vector accepted")
    try:
        constant_line_certificate((1,) + (0,) * 8, 0)
    except ValueError:
        rejected += 1
    else:
        raise ValueError("nonconstant axis accepted as constant")
    return rejected


def run():
    grid, grid_digest = coefficient_grid_audit()
    result = {
        "schema": 1,
        "status": "PASS",
        "coefficient_domain": [-2, -1, 0, 1],
        "coefficient_grid": grid,
        "coefficient_partition_sha256": grid_digest,
        "permutation_checks": permutation_audit(),
        "cantor_level_three": cantor_level_three_audit(),
        "projection_parameter_cases": projection_parameter_audit(),
        "malformed_controls_rejected": malformed_controls(),
        "trust_boundary": (
            "Exact finite corroboration of the algebraic partition, Cantor "
            "digits, and strict-exponent interface. The universal Hausdorff-"
            "dimension theorem still rests on the reviewed human proof, "
            "Frostman theory, and Ren--Wang Theorem 1.2."),
    }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true")
    arguments = parser.parse_args()
    result = run()
    if arguments.emit:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    expected_path = Path(__file__).with_name("expected.json")
    expected = json.loads(expected_path.read_text())
    require(result == expected, "frozen expected output mismatch")
    print(json.dumps({
        "status": result["status"],
        "coefficient_vectors": result["coefficient_grid"]["vectors"],
        "projection_parameter_cases": result["projection_parameter_cases"],
        "expected_sha256": sha256(expected_path.read_bytes()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
