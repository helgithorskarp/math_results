#!/usr/bin/env python3
"""Independent exact audit of homogeneous angular-ray contractions.

The checker imports no target code.  It uses univariate coefficient lists and
complete interpolation grids for the lift identities, then separately checks
whole-cone witnesses, rational motions, and a large exact control for the
nonsmooth global example.
"""

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def trim(poly):
    values = list(poly)
    while values and not values[-1]:
        values.pop()
    return values


def add(first, second):
    out = [F(0)] * max(len(first), len(second))
    for index, value in enumerate(first):
        out[index] += value
    for index, value in enumerate(second):
        out[index] += value
    return trim(out)


def scale_poly(value, poly):
    return trim([F(value) * coefficient for coefficient in poly])


def multiply(first, second):
    if not first or not second:
        return []
    out = [F(0)] * (len(first) + len(second) - 1)
    for i, value in enumerate(first):
        for j, other in enumerate(second):
            out[i + j] += value * other
    return trim(out)


def derivative(poly):
    return trim([index * poly[index] for index in range(1, len(poly))])


def subtract(first, second):
    return add(first, scale_poly(-1, second))


def pin_inputs():
    manifest = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    require(manifest["schema"] == 1, "manifest schema")
    for relative, expected in manifest["files"].items():
        actual = sha256((HERE / relative).read_bytes()).hexdigest()
        require(actual == expected, f"changed target input: {relative}")
    return manifest


def interpolation_identities():
    # For fixed a,b,c,d, numerator and denominator are polynomials in tau.
    # The cleared derivative identity has degrees <=(2,2,1,1) in a,b,c,d.
    # Three-by-three-by-two-by-two distinct values therefore certify every
    # coefficient by tensor-product interpolation.
    grids = ((F(-2), F(0), F(3)), (F(-3), F(1), F(2)),
             (F(-1), F(2)), (F(-2), F(1)))
    checked = 0
    wrong_rejected = 0
    for a, b, c, d in product(*grids):
        numerator = add(scale_poly(c, [a * b, a + b, 1]), [d, 0, -d])
        denominator = [1, a + b, a * b]
        left = subtract(multiply(derivative(numerator), denominator),
                        multiply(numerator, derivative(denominator)))
        factor = [a + b, 2 * (1 + a * b), a + b]
        bracket = c * (1 - a * b) - d
        right = scale_poly(bracket, factor)
        require(left == right, "cleared lift derivative identity")
        wrong = scale_poly(c * (1 - a * b) + d, factor)
        if left != wrong:
            wrong_rejected += 1
        checked += 1
    require(checked == 36 and wrong_rejected > 0, "interpolation grid coverage")

    norm_checks = 0
    factors = pythagorean_factors()
    angles = pythagorean_angles()
    for a, sa in factors:
        for tau, sine in angles:
            first = (a + tau) / (1 + a * tau)
            last = sa * sine / (1 + a * tau)
            require(first * first + last * last == 1, "norm-preserving raise")
            norm_checks += 1
    return {
        "complete_parameter_grid_tuples": checked,
        "parameter_degree_bounds": [2, 2, 1, 1],
        "maximum_tau_degree": 3,
        "wrong_sign_grid_rejections": wrong_rejected,
        "independent_norm_checks": norm_checks,
    }


def pythagorean_factors():
    return [(F(0), F(1)), (F(5, 13), F(12, 13)),
            (F(3, 5), F(4, 5)), (F(4, 5), F(3, 5)),
            (F(12, 13), F(5, 13)), (F(1), F(0))]


def pythagorean_angles():
    return [(F(1), F(0)), (F(12, 13), F(5, 13)),
            (F(4, 5), F(3, 5)), (F(3, 5), F(4, 5)),
            (F(5, 13), F(12, 13)), (F(0), F(1))]


def whole_cone_and_motion():
    factors = pythagorean_factors()
    cosines = [F(-1), F(-4, 5), F(-3, 5), F(0),
               F(3, 5), F(4, 5), F(1)]
    radii = [(F(1, 3), F(5, 2)), (F(1), F(1)), (F(0), F(2))]
    angles = pythagorean_angles()
    admissible = rejected = negative_witnesses = motion_paths = 0
    for (a, sa), (b, sb), c in product(factors, factors, cosines):
        cross = c * (1 - a * b)
        condition = cross <= sa * sb
        A, B = 1 - a * a, 1 - b * b
        if condition:
            admissible += 1
            for r, q in radii:
                losses = []
                raised = []
                for tau, sine in angles:
                    aa = (a + tau) / (1 + a * tau)
                    ba = sa * sine / (1 + a * tau)
                    ab = (b + tau) / (1 + b * tau)
                    bb = sb * sine / (1 + b * tau)
                    require(aa * aa + ba * ba == ab * ab + bb * bb == 1,
                            "raised norm")
                    inner = c * aa * ab + ba * bb
                    raised.append(r * r + q * q - 2 * r * q * inner)
                require(all(first >= second for first, second
                            in zip(raised, raised[1:])), "raising distance")
                target = ((a * r) ** 2 + (b * q) ** 2
                          - 2 * c * a * b * r * q)
                lowered = [target + (1 - t) ** 2 * (r * sa - q * sb) ** 2
                           for t in (F(0), F(1, 3), F(2, 3), F(1))]
                require(raised[-1] == lowered[0], "motion stage join")
                require(all(first >= second for first, second
                            in zip(lowered, lowered[1:])), "lowering distance")
                losses.append(A * r * r + B * q * q - 2 * cross * r * q)
                require(losses[-1] >= 0, "whole-cone sufficiency")
                motion_paths += 1
        else:
            rejected += 1
            require(cross > 0, "inadmissible cross sign")
            if A:
                r, q = cross, A
            elif B:
                q, r = cross, B
            else:
                raise AssertionError("both diagonal terms vanish but condition fails")
            loss = A * r * r + B * q * q - 2 * cross * r * q
            if loss >= 0:
                # One zero diagonal term needs a deliberately unbalanced pair.
                if not A:
                    q, r = F(1), (B + 1) / (2 * cross)
                else:
                    r, q = F(1), (A + 1) / (2 * cross)
                loss = A * r * r + B * q * q - 2 * cross * r * q
            require(loss < 0, "necessity witness")
            negative_witnesses += 1

    # Tight condition: every raised distance is constant for this pair.
    a, sa, b, sb, c, r, q = F(0), F(1), F(4, 5), F(3, 5), F(3, 5), F(3, 5), F(1)
    tight = []
    for tau, sine in angles:
        aa, ba = (a + tau) / (1 + a * tau), sa * sine / (1 + a * tau)
        ab, bb = (b + tau) / (1 + b * tau), sb * sine / (1 + b * tau)
        tight.append(r * r + q * q - 2 * r * q * (c * aa * ab + ba * bb))
    require(set(tight) == {F(16, 25)}, "tight pair constancy")
    return {
        "factor_pairs_times_cosines": len(factors) ** 2 * len(cosines),
        "admissible_conditions": admissible,
        "inadmissible_conditions": rejected,
        "exact_negative_necessity_witnesses": negative_witnesses,
        "checked_motion_paths": motion_paths,
        "tight_pair_distance_squared": "16/25",
        "tight_pair_raise_samples": len(tight),
    }


def dot(first, second):
    return sum((a * b for a, b in zip(first, second)), F(0))


def scale(value, vector):
    return tuple(value * coordinate for coordinate in vector)


def distance_squared(first, second):
    return sum((a - b) ** 2 for a, b in zip(first, second))


def rational_sphere_directions():
    values = [F(-2), F(-1), F(-1, 2), F(0), F(1, 2), F(1), F(2)]
    directions = set()
    for p, q in product(values, repeat=2):
        denominator = 1 + p * p + q * q
        directions.add((2 * p / denominator, 2 * q / denominator,
                        (1 - p * p - q * q) / denominator))
    directions.update(((F(1), F(0), F(0)), (F(0), F(1), F(0)),
                       (F(0), F(0), F(1))))
    require(all(dot(u, u) == 1 for u in directions), "rational sphere")
    return sorted(directions)


def leibniz_determinant(rows):
    size = len(rows)
    require(all(len(row) == size for row in rows), "square determinant")
    total = F(0)
    for permutation in permutations(range(size)):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(size) for j in range(i + 1, size))
        term = F(-1 if inversions % 2 else 1)
        for row, column in enumerate(permutation):
            term *= rows[row][column]
        total += term
    return total


def global_example():
    directions = rational_sphere_directions()
    qbound = F(2, 3)
    differentiable = differential_checks = cone_pairs = 0
    max_alpha_squared = max_gradient_squared = F(0)
    factors = []
    for u in directions:
        signed = u[0] * u[1] * u[2]
        alpha = abs(signed)
        factors.append(alpha)
        if signed:
            sign = 1 if signed > 0 else -1
            euclidean = (sign * u[1] * u[2], sign * u[0] * u[2],
                         sign * u[0] * u[1])
            gradient = tuple(value - 3 * alpha * coordinate
                             for value, coordinate in zip(euclidean, u))
            gradient_squared = dot(gradient, gradient)
            require(alpha * alpha <= F(1, 27), "alpha AM-GM bound")
            require(gradient_squared <= F(1, 3), "spherical gradient bound")
            right = qbound - alpha * alpha / qbound
            require(right >= 0 and gradient_squared <= right * right,
                    "two-thirds shear bound")
            max_alpha_squared = max(max_alpha_squared, alpha * alpha)
            max_gradient_squared = max(max_gradient_squared, gradient_squared)
            differentiable += 1
            differential_checks += 3

    for i, j in combinations(range(len(directions)), 2):
        c, a, b = dot(directions[i], directions[j]), factors[i], factors[j]
        if c > 0:
            require(c * c * (1 - a * b) ** 2
                    <= (1 - a * a) * (1 - b * b), "global full-cone condition")
        cone_pairs += 1

    sites = [(F(0), F(0), F(0))]
    for direction in directions:
        sites.extend(scale(radius, direction) for radius in (F(1, 3), F(1), F(5, 2)))

    def image(x):
        radius_squared = dot(x, x)
        if not radius_squared:
            return x
        # All generated sites have a known rational radius.
        radius = next(radius for radius in (F(1, 3), F(1), F(5, 2))
                      if radius * radius == radius_squared)
        u = scale(1 / radius, x)
        return scale(abs(u[0] * u[1] * u[2]), x)

    images = [image(site) for site in sites]
    pair_checks = 0
    for i, j in combinations(range(len(sites)), 2):
        source = distance_squared(sites[i], sites[j])
        target = distance_squared(images[i], images[j])
        require(target <= F(4, 9) * source, "global exact Lipschitz control")
        pair_checks += 1

    axes = [(F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1))]
    oblique = [tuple(F(value, 3) for value in row)
               for row in ((1, 2, 2), (2, 1, 2), (2, 2, 1))]
    fixture = axes + oblique
    paired_rows = [list(x) + list(image(x)) for x in fixture]
    determinant = leibniz_determinant(paired_rows)
    require(determinant == F(320, 531441), "paired-rank determinant")

    # Positive regularization is injective on this exact multi-radius control.
    epsilon = F(1, 7)
    regularized = []
    for site in sites:
        radius_squared = dot(site, site)
        if not radius_squared:
            regularized.append(site)
            continue
        radius = next(radius for radius in (F(1, 3), F(1), F(5, 2))
                      if radius * radius == radius_squared)
        u = scale(1 / radius, site)
        alpha = abs(u[0] * u[1] * u[2])
        regularized.append(scale(epsilon + (1 - epsilon) * alpha, site))
    require(len(set(regularized)) == len(regularized), "positive-factor injection")
    return {
        "rational_directions": len(directions),
        "differentiable_direction_controls": differentiable,
        "differential_inequalities": differential_checks,
        "full_cone_direction_pairs": cone_pairs,
        "multi_radius_sites": len(sites),
        "exact_two_thirds_lipschitz_pairs": pair_checks,
        "observed_maximum_alpha_squared": str(max_alpha_squared),
        "observed_maximum_gradient_squared": str(max_gradient_squared),
        "paired_rank_determinant": str(determinant),
        "epsilon_regularized_injective_sites": len(regularized),
    }


def transfer_and_scope_controls():
    hinge_controls = 0
    for density in [F(k, 7) for k in range(15)]:
        for threshold in [F(k, 11) for k in range(17)]:
            conditional = density * max(1 - threshold / density, 0) if density else F(0)
            require(conditional == max(density - threshold, 0),
                    "two-dimensional Gaussian cancellation algebra")
            hinge_controls += 1

    # The older norm-displacement lift decreases and then increases here.
    r, q, a, b, c = F(3, 5), F(1), F(0), F(4, 5), F(3, 5)
    source = r * r + q * q - 2 * r * q * c
    target = (a * r) ** 2 + (b * q) ** 2 - 2 * a * b * r * q * c
    midpoint = ((r * (1 + a) / 2) ** 2 + (q * (1 + b) / 2) ** 2
                - 2 * c * r * (1 + a) / 2 * q * (1 + b) / 2
                + (r * (1 - a) - q * (1 - b)) ** 2 / 4)
    require(source == target == F(16, 25) and midpoint == F(77, 125),
            "classical lift comparison")
    return {
        "gaussian_cancellation_controls": hinge_controls,
        "classical_source_and_target_distance_squared": str(source),
        "classical_midpoint_distance_squared": str(midpoint),
        "external_transfer_inputs": [
            "Aishwarya-Li Theorem 1.4(i)(a): sampled-density order",
            "Bezdek-Connelly Theorem 1: n+2 piecewise-smooth expansion",
        ],
    }


def audit():
    manifest = pin_inputs()
    return {
        "status": "INDEPENDENT_ANGULAR_RAY_CONTRACTIONS_REVIEW_PASS",
        "target_commit": manifest["target_commit"],
        "target_graph_ref": manifest["target_graph_ref"],
        "pinned_target_files": len(manifest["files"]),
        "identity_interpolation": interpolation_identities(),
        "whole_cone_and_motion": whole_cone_and_motion(),
        "global_example": global_example(),
        "transfer_and_scope": transfer_and_scope_controls(),
        "verdict": ("accept the homogeneous nonnegative ray class; external transfer "
                    "theorems and historical novelty remain explicit trust boundaries"),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected", type=Path, default=HERE / "REVIEW_EXPECTED.json")
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    result = audit()
    raw = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.emit:
        args.expected.write_text(raw)
    else:
        require(result == json.loads(args.expected.read_text()), "review record differs")
    print(result["status"])
    print("record_sha256", sha256(raw.encode()).hexdigest())


if __name__ == "__main__":
    main()
