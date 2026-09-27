#!/usr/bin/env python3
"""Exact finite controls for PROOF.md; not a continuum proof or quadrature."""

from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), Q(0))


def sub(x, y):
    return [a - b for a, b in zip(x, y)]


def squared_distance(x, y):
    z = sub(x, y)
    return dot(z, z)


def rank(rows):
    rows = [[Q(x) for x in row] for row in rows]
    if not rows:
        return 0
    pivot = 0
    for j in range(len(rows[0])):
        candidates = [i for i in range(pivot, len(rows)) if rows[i][j]]
        if not candidates:
            continue
        i = candidates[0]
        rows[pivot], rows[i] = rows[i], rows[pivot]
        divisor = rows[pivot][j]
        rows[pivot] = [x / divisor for x in rows[pivot]]
        for i in range(len(rows)):
            if i != pivot:
                multiplier = rows[i][j]
                rows[i] = [x - multiplier * y
                           for x, y in zip(rows[i], rows[pivot])]
        pivot += 1
        if pivot == len(rows):
            break
    return pivot


def affine_rank(points):
    return rank([sub(p, points[0]) for p in points[1:]])


def geometry():
    record = json.loads((ROOT / "INPUTS.json").read_text())
    a, b, qa, qb = [
        [[Q(x) for x in row] for row in record[key]]
        for key in ("source_A", "source_B", "target_A", "target_B")
    ]
    require([len(a), len(b), len(qa), len(qb)] == [4, 4, 4, 4],
            "Fixture block sizes changed")
    require(a == qa, "A isometry must be the identity")
    require(qb == [[-y, x, z + 1] for x, y, z in b],
            "B isometry must be the fixed-point-free screw")
    require(affine_rank(a) == affine_rank(b) == 3,
            "Both blocks must contain an affine basis")
    p, q = a + b, qa + qb
    n = len(p)
    offsets = [dot(x, x) - dot(y, y) for x, y in zip(p, q)]
    delta = [[squared_distance(p[i], p[j])
              - squared_distance(q[i], q[j]) for j in range(n)]
             for i in range(n)]
    within = [(i, j) for i, j in combinations(range(n), 2)
              if (i < 4) == (j < 4)]
    cross = [(i, j) for i in range(4) for j in range(4, n)]
    require(all(delta[i][j] == 0 for i, j in within),
            "Internal distances changed")
    require(all(delta[i][j] >= 0 for i, j in cross),
            "Cross distance expanded")
    require(any(delta[i][j] > 0 for i, j in cross),
            "Fixture must include a strict cross contraction")
    expected_cross = [[10, 2, 4, 2], [0, 16, 2, 8],
                      [9, 1, 5, 5], [1, 17, 5, 13]]
    require([[delta[i][j] for j in range(4, n)] for i in range(4)]
            == expected_cross, "Cross loss table changed")
    require(offsets == [0, 0, 0, 0, 3, 3, 1, 3],
            "Norm offsets changed")
    paired_rank = affine_rank([x + y for x, y in zip(p, q)])
    require(paired_rank == 6, "Paired affine rank must be six")
    # The fixed-point equation (I-R)c=h has a zero third row and RHS 1.
    identity_minus_rotation = [[1, 1, 0], [-1, 1, 0], [0, 0, 0]]
    augmented = [row + [rhs] for row, rhs in
                 zip(identity_minus_rotation, [0, 0, 1])]
    require(rank(augmented) > rank(identity_minus_rotation),
            "The screw unexpectedly has a fixed point")
    return p, q, offsets, delta, {
        "within_block_pairs": len(within),
        "cross_block_pairs": len(cross),
        "strict_cross_pairs": sum(delta[i][j] > 0 for i, j in cross),
        "paired_affine_rank": paired_rank,
        "block_affine_ranks": [affine_rank(a), affine_rank(b)],
        "norm_offsets": [str(x) for x in offsets],
        "common_equal_norm_anchors_excluded": True,
    }


def cancellation(p, q, offsets, delta):
    """Check a linear identity on a basis of all symmetric Hessians."""
    n = len(p)
    gram_difference = [[dot(q[i], q[j]) - dot(p[i], p[j])
                        for j in range(n)] for i in range(n)]
    checks = 0
    rejected_drift_omissions = 0
    for i in range(n):
        for j in range(i, n):
            hessian = [[Q(0) for _ in range(n)] for _ in range(n)]
            hessian[i][j] = hessian[j][i] = Q(1)
            # The logarithmic Euler identity makes the gradient H * 1.
            gradient = [sum(row) for row in hessian]
            mean_term = sum(offsets[k] * gradient[k] for k in range(n)) / 2
            covariance_term = sum(gram_difference[k][l] * hessian[k][l]
                                  for k in range(n) for l in range(n)) / 2
            cross_term = sum(delta[k][l] * hessian[k][l]
                             for k, l in combinations(range(n), 2)) / 2
            require(mean_term + covariance_term == cross_term,
                    "Norm cancellation or unordered-pair factor failed")
            checks += 1
            if mean_term:
                require(covariance_term != cross_term,
                        "The negative drift-omission control failed")
                rejected_drift_omissions += 1
    require(rejected_drift_omissions > 0, "No active norm drift tested")
    return checks, rejected_drift_omissions


# Tiny exact polynomial arithmetic in the variables a, b, epsilon.
# A dictionary maps an exponent triple to its rational coefficient.
def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            result[exponent] = result.get(exponent, Q(0)) + coefficient
    return {e: c for e, c in result.items() if c}


def scale(polynomial, scalar):
    return {e: Q(scalar) * c for e, c in polynomial.items() if scalar * c}


def multiply(left, right):
    terms = []
    for e, c in left.items():
        for f, d in right.items():
            terms.append({tuple(x + y for x, y in zip(e, f)): c * d})
    return add(*terms)


def derivative(polynomial, variable):
    result = {}
    for exponent, coefficient in polynomial.items():
        degree = exponent[variable]
        if degree:
            e = list(exponent)
            e[variable] -= 1
            result[tuple(e)] = coefficient * degree
    return result


def smooth_minimum():
    quadratic = {(2, 0, 0): Q(1), (0, 2, 0): Q(1),
                 (1, 1, 1): Q(1), (1, 1, 0): Q(-2)}
    qa, qb = derivative(quadratic, 0), derivative(quadratic, 1)
    qab = derivative(qa, 1)
    numerator = add(multiply(qa, qb),
                    scale(multiply(quadratic, qab), -2))
    require(numerator == {(1, 1, 1): Q(4), (1, 1, 2): Q(-1)},
            "Smooth overlap mixed-Hessian polynomial failed")
    # Also pin homogeneity and the two elementary bounding quadratics.
    a, b = {(1, 0, 0): Q(1)}, {(0, 1, 0): Q(1)}
    require(add(multiply(a, qa), multiply(b, qb)) == scale(quadratic, 2),
            "Quadratic homogeneity failed")
    minus_square = multiply(add(a, scale(b, -1)), add(a, scale(b, -1)))
    plus_square = multiply(add(a, b), add(a, b))
    require(add(quadratic, scale(minus_square, -1)) == {(1, 1, 1): Q(1)},
            "Lower quadratic bound failed")
    require(add(plus_square, scale(quadratic, -1))
            == {(1, 1, 0): Q(4), (1, 1, 1): Q(-1)},
            "Upper quadratic bound failed")
    return 4


def finite_kernel():
    """An exact two-state control of the direction of disintegration."""
    source_base = [Q(1, 2), Q(1, 2)]
    target_base = [Q(1, 3), Q(2, 3)]
    source_ratio = [Q(1, 4), Q(7, 4)]
    target_ratio = [Q(1, 2), Q(5, 4)]
    joint = [[Q(5, 18), Q(2, 9)], [Q(1, 18), Q(4, 9)]]
    require([sum(row) for row in joint] == source_base,
            "Source base marginal failed")
    require([sum(joint[i][j] for i in range(2)) for j in range(2)]
            == target_base, "Target base marginal failed")
    require([sum(source_ratio[i] * joint[i][j] for i in range(2))
             / target_base[j] for j in range(2)] == target_ratio,
            "Conditional-mean direction is wrong")
    kernel = [[joint[i][j] / source_base[i] for j in range(2)]
              for i in range(2)]
    require(all(sum(row) == 1 for row in kernel), "K is not Markov")
    source_a = [a * b for a, b in zip(source_base, source_ratio)]
    target_a = [a * b for a, b in zip(target_base, target_ratio)]
    require(sum(source_a) == sum(target_a) == 1, "A masses changed")
    for source, target in ((source_base, target_base), (source_a, target_a)):
        require([sum(source[i] * kernel[i][j] for i in range(2))
                 for j in range(2)] == target, "A common K marginal failed")
    require([sum(kernel[i][j] for i in range(2)) for j in range(2)]
            != [1, 1], "Control should not preserve counting measure")
    # This finite control is not a Gaussian fixture or a counterexample.
    return [[str(x) for x in row] for row in kernel]


def main():
    require(sys.version_info >= (3, 11), "Use Python 3.11 or later")
    p, q, offsets, delta, geometry_record = geometry()
    basis_checks, negative_controls = cancellation(p, q, offsets, delta)
    result = {
        "status": "EXACT_BINARY_COUPLING_CONTROLS_PASS",
        "geometry": geometry_record,
        "symmetric_hessian_basis_checks": basis_checks,
        "drift_omission_controls_rejected": negative_controls,
        "exact_polynomial_identities": smooth_minimum(),
        "finite_common_kernel": finite_kernel(),
        "finite_kernel_preserves_counting_measure": False,
        "continuum_kernel_computed": False,
        "majorisation_or_KP_certified_by_code": False,
    }
    expected = ROOT / "EXPECTED.json"
    require(result == json.loads(expected.read_text()),
            "Result differs from EXPECTED.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
