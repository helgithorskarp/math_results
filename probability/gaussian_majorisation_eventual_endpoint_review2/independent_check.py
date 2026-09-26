#!/usr/bin/env python3
"""Independent exact audit for the eventual Gaussian-majorisation endpoint.

This checker imports none of the reviewed implementation.  It checks the
stitching constants, the algebra used in both analytic dependencies, and the
finite tetrahedral application with integer and rational arithmetic only.
It does not turn the universal analytic arguments into a finite computation.
"""

import argparse
import hashlib
import json
from fractions import Fraction as Q
from itertools import product
from pathlib import Path


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def norm2(x):
    return dot(x, x)


def poly_add(*ps):
    out = {}
    for p in ps:
        for degree, coefficient in p.items():
            out[degree] = out.get(degree, Q(0)) + coefficient
    return {d: c for d, c in out.items() if c}


def poly_scale(p, scalar):
    return {d: scalar * c for d, c in p.items() if scalar * c}


def poly_mul(p, q):
    out = {}
    for i, a in p.items():
        for j, b in q.items():
            out[i + j] = out.get(i + j, Q(0)) + a * b
    return {d: c for d, c in out.items() if c}


def poly_shift(p, places):
    return {d + places: c for d, c in p.items()}


def audit_window_algebra():
    # With e=R^2/s, L=(4-5e)^2/[32e(1-e)].  Clear denominators
    # in the division formula and the 9/(64e) lower bound.
    e = {1: Q(1)}
    one = {0: Q(1)}
    four_minus_five_e = poly_add(poly_scale(one, 4), poly_scale(e, -5))
    numerator = poly_mul(four_minus_five_e, four_minus_five_e)

    # 32 e(1-e) * (1/(2e)-3/4+e/[32(1-e)])
    division_numerator = poly_add(
        poly_scale(poly_add(one, poly_scale(e, -1)), 16),
        poly_scale(poly_mul(e, poly_add(one, poly_scale(e, -1))), -24),
        poly_mul(e, e),
    )
    require(numerator == division_numerator, "high-noise division identity")

    # 64e(1-e)(L-9/(64e)) = 2(4-5e)^2-9(1-e).
    difference_numerator = poly_add(poly_scale(numerator, 2),
                                    poly_scale(poly_add(one, poly_scale(e, -1)), -9))
    stated_factor = poly_mul(poly_add(one, poly_scale(e, -2)),
                             poly_add(poly_scale(one, 23), poly_scale(e, -25)))
    require(difference_numerator == stated_factor,
            "high-noise cutoff factorization")

    # On 0<e<=1/2 both factors are nonnegative.  The simpler window
    # exponent 9/(64e) exceeds the mode bound e/2.
    for denominator in range(2, 202):
        for numerator_e in range(1, denominator // 2 + 1):
            epsilon = Q(numerator_e, denominator)
            require((1 - 2 * epsilon) * (23 - 25 * epsilon) >= 0,
                    "cutoff factor sign")
            require(Q(9, 64) / epsilon > epsilon / 2,
                    "cutoff exceeds possible mode")
    return {
        "division_coefficients": {str(k): str(v) for k, v in sorted(numerator.items())},
        "cutoff_factor_coefficients": {
            str(k): str(v) for k, v in sorted(stated_factor.items())
        },
    }


def audit_stitching():
    # Set R=1 by scaling.  For lambda>=1/2, the tail error coefficient
    # decreases termwise and is therefore bounded by its endpoint value.
    lam0 = Q(1, 2)
    tail_error = 8 + 6 / lam0 + 6 / (lam0 * lam0)
    require(tail_error == 44, "tail error endpoint")
    s0 = Q(8)
    require(lam0 * lam0 * s0 >= 1, "tail lambda^2 s regime")
    require(lam0 * s0 >= 4, "tail lambda s regime")

    tail_cutoff = lam0 * lam0 / 2
    window_cutoff = Q(9, 64)
    overlap = window_cutoff - tail_cutoff
    require(tail_cutoff == Q(1, 8), "tail cutoff")
    require(overlap == Q(1, 64) and overlap > 0, "window overlap")

    # The quantitative flap bound uses R^2=8r^2 and
    # kappa>=alpha/(150-99alpha).  Check the exact endpoint reduction
    # and that it dominates every analytic regime threshold.
    endpoint_rows = []
    for alpha in [Q(1, 1000), Q(1, 10), Q(1, 3), Q(1, 2), Q(9, 10), Q(1)]:
        q = alpha / (50 * (3 - 2 * alpha))
        kappa = q / (1 + q)
        require(kappa == alpha / (150 - 99 * alpha), "log lower-bound algebra")
        endpoint = 352 * (150 - 99 * alpha) / alpha
        require(endpoint == 44 * 8 / kappa, "flap variance endpoint")
        require(endpoint >= 64, "endpoint covers s>=8R^2")
        endpoint_rows.append([str(alpha), str(kappa), str(endpoint)])
    return {
        "uniform_tail_error": str(tail_error),
        "tail_exponent": str(tail_cutoff),
        "window_exponent": str(window_cutoff),
        "overlap": str(overlap),
        "endpoint_rows_alpha_kappa_s_over_r2": endpoint_rows,
    }


def audit_tetrahedral_application():
    anchors = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    labels = [(i, j) for i, j in product(range(4), repeat=2) if i != j]
    source = [sub(anchors[j], anchors[i]) for i, j in labels]
    image = [add(anchors[j], anchors[i]) for i, j in labels]
    require(len(set(source)) == 12 and len(set(image)) == 6, "support cardinalities")

    # Check every ordered pair, including equal labels; this directly
    # establishes contraction on the flap sites.
    flap_losses = {}
    for a in range(12):
        for b in range(12):
            i, j = labels[a]
            k, ell = labels[b]
            loss = norm2(sub(source[a], source[b])) - norm2(sub(image[a], image[b]))
            claimed = 16 * ((j == k) + (ell == i))
            require(loss == claimed and loss >= 0, "ordered flap loss")
            flap_losses[loss] = flap_losses.get(loss, 0) + 1

    # It suffices to check the affine flap-to-background loss at the four
    # extreme points of the tetrahedron.
    anchor_losses = {}
    for a, ((i, _), x, y) in enumerate(zip(labels, source, image)):
        for k, u in enumerate(anchors):
            loss = norm2(sub(x, u)) - norm2(sub(y, u))
            require(loss == 16 * (i == k), "flap-anchor affine endpoint")
            anchor_losses[loss] = anchor_losses.get(loss, 0) + 1

    # Independently construct a martingale kernel: condition on each of the
    # six axis images and average the four source sites sharing its nonzero
    # coordinate.  Check both marginals and conditional means.
    images = sorted(set(image))
    input_masses = [Q(0)] * 12
    conditional_sizes = []
    mean_squared_displacement = Q(0)
    for y in images:
        axis = next(k for k in range(3) if y[k])
        chosen = [a for a, x in enumerate(source) if x[axis] == y[axis]]
        require(len(chosen) == 4, "four-point conditional")
        mean = tuple(sum(Q(source[a][k], 4) for a in chosen) for k in range(3))
        require(mean == y, "martingale conditional mean")
        for a in chosen:
            input_masses[a] += Q(1, 24)
            mean_squared_displacement += Q(norm2(sub(source[a], y)), 24)
        conditional_sizes.append(len(chosen))
    require(input_masses == [Q(1, 12)] * 12, "martingale input marginal")
    require(mean_squared_displacement == 4, "martingale displacement")

    # The pointwise ratio estimate is purely algebraic in v_i>=0.
    # Verify its cleared numerator on a grid, including axes and the origin.
    ratio_samples = 0
    for v1, v2, v3 in product(range(8), repeat=3):
        V = Q(v1 + v2 + v3)
        P = Q(v1 * v2 + v1 * v3 + v2 * v3)
        e2 = 3 + 2 * V + P
        e1 = 3 + V
        lhs = (e2 - e1) * (3 + 2 * V) - V * e2
        require(lhs == (3 + V) * P >= 0, "ratio remainder")
        ratio_samples += 1

    # The Jensen certificate for B<=3F: represent each anchor with weights
    # 1/4 on three incoming differences and 1/24 on six differences avoiding
    # the anchor as either endpoint.
    for i, u in enumerate(anchors):
        weights = [Q(1, 4) if j == i else
                   Q(1, 24) if a != i and j != i else Q(0)
                   for a, j in labels]
        require(sum(weights) == 1 and max(weights) <= Q(1, 4), "Jensen weights")
        barycenter = tuple(sum(w * x[k] for w, x in zip(weights, source))
                           for k in range(3))
        require(barycenter == u, "Jensen barycenter")

    return {
        "ordered_flap_pairs": 144,
        "ordered_flap_loss_histogram": {
            str(k): v for k, v in sorted(flap_losses.items())
        },
        "flap_anchor_pairs": 48,
        "flap_anchor_loss_histogram": {
            str(k): v for k, v in sorted(anchor_losses.items())
        },
        "martingale_conditional_sizes": conditional_sizes,
        "martingale_mean_squared_displacement": str(mean_squared_displacement),
        "ratio_grid_samples": ratio_samples,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = {
        "status": "INDEPENDENT_EVENTUAL_ENDPOINT_AUDIT_PASSED",
        "scope": "exact algebra and finite geometry; universal analytic steps audited in README",
        "high_noise_window": audit_window_algebra(),
        "stitching": audit_stitching(),
        "tetrahedral_application": audit_tetrahedral_application(),
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check:
        expected = Path(__file__).with_name("EXPECTED.json").read_text()
        require(encoded == expected, "EXPECTED.json mismatch")
        print("PASS " + hashlib.sha256(encoded.encode()).hexdigest())
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
