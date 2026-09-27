#!/usr/bin/env python3
"""Clean-room exact audit of the finite-symmetry reduction fixture.

No code from the reviewed packet is imported.  Signed permutation matrices
are represented as (permutation, sign-vector) pairs, and every geometry,
group-action, covariance, interaction, and scaling check is recomputed from
the published rational input.
"""

from fractions import Fraction as F
from itertools import permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "gaussian_finite_symmetry_reduction"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def q(x):
    require(type(x) is int or isinstance(x, str), "non-rational input")
    return F(x)


def point(row):
    require(isinstance(row, list) and len(row) == 3, "point dimension")
    return tuple(q(x) for x in row)


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def scale(c, x):
    return tuple(c * a for a in x)


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def d2(x, y):
    return dot(sub(x, y), sub(x, y))


def group():
    return tuple((perm, signs)
                 for perm in permutations(range(3))
                 for signs in product((-1, 1), repeat=3))


def act(g, x):
    perm, signs = g
    return tuple(signs[i] * x[perm[i]] for i in range(3))


def compose(g, h):
    """Return g after h in the independent (perm, signs) representation."""
    pg, sg = g
    ph, sh = h
    return (tuple(ph[pg[i]] for i in range(3)),
            tuple(sg[i] * sh[pg[i]] for i in range(3)))


def hinge(value, level):
    return max(value - level, F(0))


def moments(points, weights):
    mean = tuple(sum((w * x[j] for w, x in zip(weights, points)), F(0))
                 for j in range(3))
    covariance = tuple(
        tuple(sum((w * (x[i] - mean[i]) * (x[j] - mean[j])
                   for w, x in zip(weights, points)), F(0))
              for j in range(3))
        for i in range(3)
    )
    return mean, covariance


def scalar_covariance(covariance):
    value = covariance[0][0]
    require(value > 0, "degenerate covariance")
    expected = tuple(tuple(value if i == j else F(0) for j in range(3))
                     for i in range(3))
    require(covariance == expected, "covariance is not scalar")
    return value


def interaction_checks():
    values = (F(0), F(1, 3), F(2, 3), F(1), F(5, 3))
    checked = 0
    for u in product(values, repeat=4):
        pair_bound = sum((min(u[i], u[j])
                          for i in range(4) for j in range(i)), F(0))
        knots = sorted(set((F(0), sum(u, F(0)), sum(u, F(0)) + 1) + u))
        levels = knots + [(a + b) / 2 for a, b in zip(knots, knots[1:])]
        for h in levels:
            interaction = hinge(sum(u, F(0)), h) - sum(
                (hinge(x, h) for x in u), F(0)
            )
            require(0 <= interaction <= pair_bound, "interaction bound failed")
            checked += 1
    return checked


def copy_normalization_checks():
    checked = 0
    samples = (
        ((F(1, 5), F(4, 5)), (F(2, 5), F(3, 5))),
        ((F(1, 7), F(2, 7), F(4, 7)),
         (F(1, 6), F(1, 3), F(1, 2))),
    )
    for source, target in samples:
        knots = sorted(set((F(0), F(1)) + source + target))
        levels = knots + [(a + b) / 2 for a, b in zip(knots, knots[1:])]
        for h in levels:
            old = sum((hinge(x, h) for x in source), F(0)) - sum(
                (hinge(x, h) for x in target), F(0)
            )
            copied = 48 * (
                sum((hinge(x / 48, h / 48) for x in source), F(0))
                - sum((hinge(x / 48, h / 48) for x in target), F(0))
            )
            require(copied == old, "48-copy hinge normalization failed")
            checked += 1
    return checked


def main():
    data = json.loads((TARGET / "INPUT.json").read_text())
    source = tuple(point(x) for x in data["source"])
    target = tuple(point(x) for x in data["target"])
    weights = tuple(q(x) for x in data["weights"])
    radius = q(data["radius"])
    variance = q(data["variance"])
    length = data["length"]
    bits = data["bits"]
    require(len(source) == len(target) == len(weights), "input lengths")
    require(sum(weights, F(0)) == 1 and all(w > 0 for w in weights), "weights")
    require(all(d2(target[i], target[j]) <= d2(source[i], source[j])
                for i in range(len(source)) for j in range(i)), "base contraction")

    gs = group()
    gset = set(gs)
    require(len(gs) == 48, "group order")
    require(all(compose(g, h) in gset for g in gs for h in gs), "group closure")
    v = (F(1), F(2), F(3))
    orbit = tuple(act(g, v) for g in gs)
    require(len(set(orbit)) == 48, "orbit is not free")
    orbit_minimum = min(d2(orbit[i], orbit[j])
                        for i in range(48) for j in range(i))
    require(orbit_minimum == 2, "orbit separation")

    copied_source, copied_target, copied_weights, block = [], [], [], []
    for block_index, g in enumerate(gs):
        for p, r, w in zip(source, target, weights):
            copied_source.append(act(g, add(scale(length, v), p)))
            copied_target.append(act(g, add(scale(F(length, 2), v), r)))
            copied_weights.append(w / 48)
            block.append(block_index)
    copied_source = tuple(copied_source)
    copied_target = tuple(copied_target)
    copied_weights = tuple(copied_weights)
    require(len(set(copied_source)) == len(copied_source), "copied source collision")

    within_tight = within_strict = cross_strict = 0
    minimum_cross_loss = None
    for i in range(len(copied_source)):
        for j in range(i):
            loss = d2(copied_source[i], copied_source[j]) - d2(
                copied_target[i], copied_target[j]
            )
            require(loss >= 0, "copied map expands")
            if block[i] != block[j]:
                require(loss > 0, "cross-block pair is not strict")
                cross_strict += 1
                minimum_cross_loss = (loss if minimum_cross_loss is None
                                      else min(minimum_cross_loss, loss))
            elif loss:
                within_strict += 1
            else:
                within_tight += 1

    table = {p: (r, w) for p, r, w in
             zip(copied_source, copied_target, copied_weights)}
    action_checks = 0
    for p, r, w in zip(copied_source, copied_target, copied_weights):
        for g in gs:
            require(table[act(g, p)] == (act(g, r), w), "equivariance failed")
            action_checks += 1

    mean_source, cov_source = moments(copied_source, copied_weights)
    mean_target, cov_target = moments(copied_target, copied_weights)
    require(mean_source == mean_target == (0, 0, 0), "mean is not zero")
    lambda_source = scalar_covariance(cov_source)
    lambda_target = scalar_covariance(cov_target)
    require(lambda_source > lambda_target > 0, "covariance ordering")
    radius_source_squared = max(dot(x, x) for x in copied_source)
    radius_target_squared = max(dot(x, x) for x in copied_target)

    upper_coefficient = F(14) + 1 + F(1, 64)
    lower_coefficient = F(13, 3)
    universal_ratio = upper_coefficient / lower_coefficient
    require(universal_ratio == F(2883, 832) < 4, "universal radius ratio")
    require(radius_source_squared / lambda_source < 4, "source radius ratio")
    require(radius_target_squared / lambda_target < 4, "target radius ratio")

    overlap_pair_factor = F(48 * 47, 2) * F(2, 48)
    require(overlap_pair_factor == 47, "overlap factor")
    require(length >= 16 * radius, "cross-block schedule")
    require((length - 4 * radius) ** 2 >= 32 * variance * bits,
            "Gaussian tail schedule")
    dyadic_error = F(47, 2**bits)
    require(dyadic_error <= q(data["requested_error"]), "dyadic error budget")

    result = {
        "status": "INDEPENDENT_FINITE_SYMMETRY_AUDIT_PASS",
        "arithmetic": "fractions.Fraction and definition-level group action",
        "imports_reviewed_code": False,
        "group_order": len(gs),
        "group_products_checked": len(gs) ** 2,
        "orbit_size": len(set(orbit)),
        "minimum_orbit_squared_separation": str(orbit_minimum),
        "constructed_labels": len(copied_source),
        "pair_checks": len(copied_source) * (len(copied_source) - 1) // 2,
        "within_tight": within_tight,
        "within_strict": within_strict,
        "cross_strict": cross_strict,
        "minimum_cross_squared_loss": str(minimum_cross_loss),
        "group_action_checks": action_checks,
        "source_covariance_scalar": str(lambda_source),
        "target_covariance_scalar": str(lambda_target),
        "source_radius_squared_over_covariance": str(
            radius_source_squared / lambda_source
        ),
        "target_radius_squared_over_covariance": str(
            radius_target_squared / lambda_target
        ),
        "universal_radius_squared_over_covariance_bound": str(universal_ratio),
        "separated_overlap_pair_factor": str(overlap_pair_factor),
        "certified_dyadic_error_upper_bound": str(dyadic_error),
        "scalar_interaction_checks": interaction_checks(),
        "copy_normalization_checks": copy_normalization_checks(),
        "gaussian_integrals_evaluated": False,
        "kirszbraun_extension_formalized": False,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
