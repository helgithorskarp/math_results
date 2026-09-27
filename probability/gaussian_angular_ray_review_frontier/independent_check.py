#!/usr/bin/env python3
"""Independent exact controls for the homogeneous angular-ray review.

This checker imports no target code.  It verifies the rational-function
identity by degree-bounded tensor-grid interpolation and evaluates the
motion in explicit coordinates, rather than using the target checker's
sparse-polynomial representation and inner-product-only fixtures.
"""

from fractions import Fraction as Q
import hashlib
import itertools
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "probability" / "gaussian_angular_ray_contractions"
PINS = {
    "PROOF.md": "27ef47567f6be6608af2ed09ec7f2c9e604707e80a5f5853862b8c55b00eaa44",
    "SOURCES.md": "55be6ec66184b5fdca2e93d7678c1ab05d0108f72727a355f0ff42c15c11b1e5",
    "check.py": "595b0d57a425f14581a5a802b8ed26700ea97782d05e3b6017333eacc30d2bbc",
    "EXPECTED.json": "31ed346da9fb5403c85cad9a337e2660a502b5b3bad1b0b80c1a70ea059ec359",
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def prod(values):
    answer = Q(1)
    for value in values:
        answer *= value
    return answer


def dot(x, y):
    need(len(x) == len(y), "dot dimension")
    return sum((a * b for a, b in zip(x, y)), Q(0))


def scale(c, x):
    return tuple(Q(c) * a for a in x)


def dist2(x, y):
    return sum(((a - b) ** 2 for a, b in zip(x, y)), Q(0))


def determinant(rows):
    matrix = [[Q(value) for value in row] for row in rows]
    n = len(matrix)
    need(all(len(row) == n for row in matrix), "nonsquare determinant")
    value = Q(1)
    for column in range(n):
        pivot = next((row for row in range(column, n)
                      if matrix[row][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            matrix[pivot], matrix[column] = matrix[column], matrix[pivot]
            value = -value
        diagonal = matrix[column][column]
        value *= diagonal
        for row in range(column + 1, n):
            ratio = matrix[row][column] / diagonal
            for j in range(column + 1, n):
                matrix[row][j] -= ratio * matrix[column][j]
            matrix[row][column] = 0
    return value


def pin_sources():
    for name, wanted in PINS.items():
        actual = hashlib.sha256((TARGET / name).read_bytes()).hexdigest()
        need(actual == wanted, f"source pin mismatch: {name}")


def cleared_derivative_residual(a, b, c, d, tau, mutated=False):
    """Cleared quotient-rule derivative minus the claimed factorization."""
    numerator = c * (a * b + (a + b) * tau + tau * tau) + d * (1 - tau * tau)
    numerator_prime = c * (a + b + 2 * tau) - 2 * d * tau
    denominator = 1 + (a + b) * tau + a * b * tau * tau
    denominator_prime = a + b + 2 * a * b * tau
    actual = numerator_prime * denominator - numerator * denominator_prime
    multiplier = (a + b) * (1 + tau * tau) + 2 * tau * (1 + a * b)
    bracket = c * (1 - a * b) + (d if mutated else -d)
    return actual - multiplier * bracket


def interpolation_identity():
    # After clearing denominators, the residual has degrees at most
    # (2,2,1,1,3) in (a,b,c,d,tau).  Vanishing on the tensor product of
    # degree+1 distinct field points therefore proves the polynomial zero.
    grids = (
        (Q(-1), Q(0), Q(2)),
        (Q(-2), Q(0), Q(1)),
        (Q(-3), Q(4)),
        (Q(-5), Q(7)),
        (Q(-2), Q(-1), Q(1), Q(3)),
    )
    evaluations = 0
    for values in itertools.product(*grids):
        need(cleared_derivative_residual(*values) == 0,
             "interpolated derivative identity")
        evaluations += 1
    need(evaluations == 144, "interpolation grid coverage")
    need(cleared_derivative_residual(0, 0, 0, 1, 1, mutated=True) == -4,
         "mutated derivative was not rejected")

    for a, tau in itertools.product(
        (Q(-2), Q(-1), Q(0), Q(1), Q(3)),
        (Q(-3), Q(-1), Q(0), Q(2)),
    ):
        need((a + tau) ** 2 + (1 - a * a) * (1 - tau * tau)
             == (1 + a * tau) ** 2, "norm identity")


FACTORS = (
    (Q(0), Q(1)),
    (Q(3, 5), Q(4, 5)),
    (Q(4, 5), Q(3, 5)),
    (Q(5, 13), Q(12, 13)),
    (Q(1), Q(0)),
)


COSINES = (
    (Q(-1), Q(0)),
    (Q(-3, 5), Q(4, 5)),
    (Q(0), Q(1)),
    (Q(3, 5), Q(4, 5)),
    (Q(1), Q(0)),
)


def loss(a, b, c, r, q):
    return ((1 - a * a) * r * r + (1 - b * b) * q * q
            - 2 * c * (1 - a * b) * r * q)


def copositive_controls():
    accepted = rejected = 0
    radii = (Q(0), Q(1, 3), Q(1), Q(7, 4), Q(5))
    for (a, sa), (b, sb), (c, _) in itertools.product(FACTORS, FACTORS, COSINES):
        need(a * a + sa * sa == 1 and b * b + sb * sb == 1,
             "factor complement")
        cross = c * (1 - a * b)
        admissible = cross <= sa * sb
        if admissible:
            accepted += 1
            need(all(loss(a, b, c, r, q) >= 0
                     for r, q in itertools.product(radii, repeat=2)),
                 "admissible sampled loss")
            if cross > 0:
                need(sa > 0 and cross * cross <= sa * sa * sb * sb,
                     "positive-cross copositivity")
                minimizing_r = cross / (sa * sa)
                need(loss(a, b, c, minimizing_r, Q(1))
                     == sb * sb - cross * cross / (sa * sa) >= 0,
                     "copositive minimum")
            else:
                need(all(term >= 0 for term in
                         (sa * sa, sb * sb, -2 * cross)),
                     "nonpositive-cross decomposition")
        else:
            rejected += 1
            need(cross > 0, "invalid boundary classification")
            if sa > 0:
                minimizing_r = cross / (sa * sa)
                need(loss(a, b, c, minimizing_r, Q(1)) < 0,
                     "invalid cone lacks exact witness")
            else:
                witness_r = (sb * sb + 1) / (2 * cross)
                need(loss(a, b, c, witness_r, Q(1)) == -1,
                     "zero-diagonal cone lacks exact witness")
    need((accepted, rejected) == (97, 28), "cone fixture counts")

    # A rational-direction example where unit representatives contract but
    # a different radial ratio fails the whole-cone condition.
    a, b, c = Q(0), Q(4, 5), Q(65, 97)
    need(loss(a, b, c, 1, 1) > 0, "unit representatives should contract")
    cross = c * (1 - a * b)
    minimizing_r = cross / (1 - a * a)
    need(loss(a, b, c, minimizing_r, 1) < 0,
         "whole-cone counter-control")


def stereographic_angles():
    # p=tan(theta/2), so theta increases with p and all coordinates are exact.
    result = []
    for p in (Q(0), Q(1, 5), Q(1, 3), Q(1, 2), Q(3, 4), Q(1)):
        denominator = 1 + p * p
        result.append(((1 - p * p) / denominator, 2 * p / denominator))
    need(all(c * c + s * s == 1 for c, s in result), "angle normalization")
    need(all(result[i][0] >= result[i + 1][0]
             for i in range(len(result) - 1)), "angle ordering")
    return tuple(result)


def raised_point(radius, direction, factor, complement, tau, sine):
    horizontal = (factor + tau) / (1 + factor * tau)
    vertical = complement * sine / (1 + factor * tau)
    point = tuple(radius * horizontal * x for x in direction) + (radius * vertical,)
    need(dot(point, point) == radius * radius, "raised norm")
    return point


def lowered_point(radius, direction, factor, complement, t):
    return tuple(radius * factor * x for x in direction) + (
        (1 - t) * radius * complement,
    )


def direct_motion_controls():
    angles = stereographic_angles()
    radii = (Q(7, 5), Q(11, 6))
    accepted = 0
    for (a, sa), (b, sb), (c, sc) in itertools.product(FACTORS, FACTORS, COSINES):
        if c * (1 - a * b) > sa * sb:
            continue
        u, v = (Q(1), Q(0)), (c, sc)
        raised_distances = []
        for tau, sine in angles:
            x = raised_point(radii[0], u, a, sa, tau, sine)
            y = raised_point(radii[1], v, b, sb, tau, sine)
            raised_distances.append(dist2(x, y))
        need(all(x >= y for x, y in zip(raised_distances, raised_distances[1:])),
             "direct raised-coordinate monotonicity")

        lowered_distances = []
        for t in (Q(0), Q(1, 3), Q(2, 3), Q(1)):
            x = lowered_point(radii[0], u, a, sa, t)
            y = lowered_point(radii[1], v, b, sb, t)
            lowered_distances.append(dist2(x, y))
        need(raised_distances[-1] == lowered_distances[0], "stage join")
        need(all(x >= y for x, y in zip(lowered_distances, lowered_distances[1:])),
             "direct lowering monotonicity")
        need(raised_distances[0] == dist2(scale(radii[0], u), scale(radii[1], v)),
             "source endpoint")
        need(lowered_distances[-1]
             == dist2(scale(radii[0] * a, u), scale(radii[1] * b, v)),
             "target endpoint")
        accepted += 1
    need(accepted == 97, "direct motion case count")

    # On an inadmissible pair, the same coordinate construction detects the
    # required late-stage distance increase.
    a, sa = Q(0), Q(1)
    b, sb = Q(4, 5), Q(3, 5)
    c, sc = Q(65, 97), Q(72, 97)
    bad = []
    for tau, sine in angles:
        bad.append(dist2(
            raised_point(1, (Q(1), Q(0)), a, sa, tau, sine),
            raised_point(1, (c, sc), b, sb, tau, sine),
        ))
    need(any(x < y for x, y in zip(bad, bad[1:])),
         "inadmissible raise was not rejected")


def shear_norm_control(alpha_squared, gradient_squared, q):
    leading = q * q - alpha_squared
    determinant_minor = leading * (leading - gradient_squared) \
        - alpha_squared * gradient_squared
    need(determinant_minor == leading * leading - q * q * gradient_squared,
         "shear determinant identity")
    return leading >= 0 and determinant_minor >= 0


def global_example_controls():
    # Exact barycentric grid checks supplement the written AM-GM and
    # sum-of-squares bounds; they do not replace their continuum proof.
    grid_points = 0
    for denominator in (6, 9, 12, 18):
        for i in range(denominator + 1):
            for j in range(denominator - i + 1):
                z = (Q(i, denominator), Q(j, denominator),
                     Q(denominator - i - j, denominator))
                pair_sum = z[0] * z[1] + z[0] * z[2] + z[1] * z[2]
                triple = prod(z)
                sos = sum(((z[i] - z[j]) ** 2
                           for i, j in ((0, 1), (0, 2), (1, 2))), Q(0)) / 2
                need(1 - 3 * pair_sum == sos >= 0, "pair-sum SOS")
                need(triple <= Q(1, 27), "AM-GM grid control")
                gradient_squared = pair_sum - 9 * triple
                need(0 <= gradient_squared <= Q(1, 3), "sphere-gradient bound")
                need(shear_norm_control(triple, gradient_squared, Q(2, 3)),
                     "grid shear control")
                # The extremal envelope used in the proof has
                # alpha^2=1/27 and |grad|^2=1/3.
                grid_points += 1
    need(grid_points == 364, "barycentric grid coverage")
    need((Q(2, 3) - Q(1, 27) / Q(2, 3)) ** 2 - Q(1, 3)
         == Q(13, 324), "global Lipschitz reserve")
    need(shear_norm_control(Q(1, 27), Q(1, 3), Q(2, 3)),
         "shear envelope boundary")

    sites = [
        (Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0)),
        (Q(0), Q(0), Q(1)),
        (Q(1, 3), Q(2, 3), Q(2, 3)),
        (Q(2, 3), Q(1, 3), Q(2, 3)),
        (Q(2, 3), Q(2, 3), Q(1, 3)),
    ]
    targets = [scale(abs(prod(x)), x) for x in sites]
    need(all(dist2(targets[i], targets[j]) <= dist2(sites[i], sites[j])
             for i in range(len(sites)) for j in range(i)),
         "global example finite contraction")
    paired_rows = [x + y for x, y in zip(sites, targets)]
    need(determinant(paired_rows) == Q(320, 531441), "paired rank determinant")

    # The two one-sided scalar-defect expressions force each component of
    # the proposed first axis to vanish.
    h = Q(12, 25)
    f = (Q(1, 3), Q(2, 3), Q(2, 3))
    need(dot(f, f) == 1, "scalar-defect test axis")
    coordinate_axes = ((Q(1), Q(0), Q(0)), (Q(0), Q(1), Q(0)),
                       (Q(0), Q(0), Q(1)))
    plane_points = ((Q(0), Q(3, 5), Q(4, 5)),
                    (Q(3, 5), Q(0), Q(4, 5)),
                    (Q(3, 5), Q(4, 5), Q(0)))
    for normal, u in zip(coordinate_axes, plane_points):
        F = dot(f, u)
        for e in coordinate_axes:
            E = dot(e, normal)
            plus = 1 - h * h * E * E - (1 - h * F * E) ** 2
            minus = 1 - h * h * E * E - (1 + h * F * E) ** 2
            need(plus + minus == -2 * h * h * E * E * (1 + F * F),
                 "opposite scalar-defect identity")


def perturbation_controls():
    # Convex interpolation with the identity keeps every sampled loss
    # nonnegative and makes all angular factors strictly positive.
    directions = ((Q(1), Q(0)), (Q(3, 5), Q(4, 5)),
                  (Q(-3, 5), Q(4, 5)))
    factors = (Q(0), Q(3, 5), Q(4, 5))
    for epsilon in (Q(1, 7), Q(1, 3), Q(3, 4)):
        moved = tuple((1 - epsilon) * a + epsilon for a in factors)
        need(all(a > 0 for a in moved), "perturbed factor positivity")
        for i in range(3):
            for j in range(i):
                c = dot(directions[i], directions[j])
                for r, q in ((Q(1), Q(2)), (Q(3, 5), Q(7, 4))):
                    source = dist2(scale(r, directions[i]), scale(q, directions[j]))
                    target = dist2(scale(r * moved[i], directions[i]),
                                   scale(q * moved[j], directions[j]))
                    need(target <= source, "perturbed endpoint contraction")


def main():
    pin_sources()
    interpolation_identity()
    copositive_controls()
    direct_motion_controls()
    global_example_controls()
    perturbation_controls()
    print("ANGULAR_RAY_INDEPENDENT_ACCEPT")
    print("arithmetic=fractions.Fraction target_imports=none")
    print("interpolation_evaluations=144 cone_cases=125 motion_cases=97")
    print("universal_motion_transfers_and_Lipschitz_scope=written_review")


if __name__ == "__main__":
    main()
