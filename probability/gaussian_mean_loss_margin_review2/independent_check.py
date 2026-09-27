#!/usr/bin/env python3
"""Independent exact controls for the uniform mean-loss margin review.

This checker imports no target code.  It pins the reviewed source and uses
only integers and fractions to exercise the algebraic interfaces in the
compactness proof.  It does not turn the non-effective continuum argument
into a finite certificate.
"""

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_inputs():
    manifest = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    require(manifest["schema"] == 1, "target manifest schema")
    for relative, expected in manifest["files"].items():
        actual = sha256((HERE / relative).read_bytes()).hexdigest()
        require(actual == expected, f"changed target input: {relative}")
    return manifest


def dot(first, second):
    return sum((a * b for a, b in zip(first, second)), F(0))


def add(first, second):
    return tuple(a + b for a, b in zip(first, second))


def sub(first, second):
    return tuple(a - b for a, b in zip(first, second))


def scale(value, vector):
    return tuple(value * coordinate for coordinate in vector)


def norm2(vector):
    return dot(vector, vector)


def mean(points, weights):
    return tuple(sum((w * point[j] for w, point in zip(weights, points)), F(0))
                 for j in range(3))


def center(points, weights):
    average = mean(points, weights)
    return [sub(point, average) for point in points]


def matrix(rows, columns, weights):
    return [[sum((w * x[i] * y[j] for w, x, y in zip(weights, rows, columns)), F(0))
             for j in range(3)] for i in range(3)]


def determinant(values):
    if len(values) == 1:
        return values[0][0]
    return sum(((-1) ** j * values[0][j] * determinant(
        [[values[i][k] for k in range(len(values)) if k != j]
         for i in range(1, len(values))]) for j in range(len(values))), F(0))


def symmetric_psd(values):
    return (all(values[i][j] == values[j][i] for i in range(3) for j in range(3))
            and all(determinant([[values[i][j] for j in indices] for i in indices]) >= 0
                    for size in range(1, 4)
                    for indices in combinations(range(3), size)))


def subtract_diagonal(values, amount):
    return [[values[i][j] - (amount if i == j else 0) for j in range(3)]
            for i in range(3)]


def loss_matrix(source, target):
    return [[norm2(sub(x, xp)) - norm2(sub(y, yp))
             for xp, yp in zip(source, target)] for x, y in zip(source, target)]


def weighted_pair(values, weights, rows=None, columns=None):
    rows = range(len(weights)) if rows is None else rows
    columns = range(len(weights)) if columns is None else columns
    return sum((weights[i] * weights[j] * values[i][j]
                for i in rows for j in columns), F(0))


def validate_fold(source, target, weights, radius=F(3), kappa=F(3, 32)):
    require(len(source) == len(target) == len(weights) > 0, "matching inputs")
    require(all(weight > 0 for weight in weights) and sum(weights) == 1,
            "probability weights")
    require(mean(source, weights) == mean(target, weights) == (0, 0, 0),
            "centered inputs")
    require(all(norm2(x) <= radius * radius for x in source), "radius bound")
    covariance = matrix(source, source, weights)
    require(symmetric_psd(subtract_diagonal(covariance, kappa)), "covariance floor")
    cross = matrix(source, target, weights)
    require(symmetric_psd(cross), "identity Procrustes alignment")
    losses = loss_matrix(source, target)
    require(all(value >= 0 for row in losses for value in row), "pair contraction")
    return covariance, cross, losses


def fold_and_operator_controls():
    background = [(-1, 0, 0), (-2, 1, 0), (-2, 0, 1), (-2, -1, -1)]
    raw_source = [tuple(map(F, point)) for point in background + [(1, 0, 0)]]
    raw_target = [tuple(map(F, point)) for point in background + [(-1, 0, 0)]]
    alphas = [F(1, 2), F(1, 3), F(1, 5), F(1, 16), F(1, 256),
              F(1, 2**20), F(1, 2**60)]
    pair_identities = contraction_pairs = 0
    records = []
    for alpha in alphas:
        weights = [(1 - alpha) / 4] * 4 + [alpha]
        source, target = center(raw_source, weights), center(raw_target, weights)
        covariance, cross, losses = validate_fold(source, target, weights)
        displacement = [sub(y, x) for x, y in zip(source, target)]
        total = weighted_pair(losses, weights)
        second = weighted_pair([[value * value for value in row] for row in losses], weights)
        mean_square = sum((weight * norm2(h) for weight, h in zip(weights, displacement)), F(0))
        require(total == 14 * alpha * (1 - alpha), "fold mean loss")
        require(second == 104 * alpha * (1 - alpha), "fold second loss")
        require(second / total == F(52, 7), "nonvanishing loss ratio")
        require(mean_square == 4 * alpha * (1 - alpha), "fold mean square displacement")
        require(cross == [list(row) for row in zip(*cross)], "symmetric cross covariance")

        rows, rare = list(range(4)), [4]
        aa = weighted_pair(losses, weights, rows, rows)
        ab = weighted_pair(losses, weights, rows, rare)
        bb = weighted_pair(losses, weights, rare, rare)
        core_square = sum((weights[i] * norm2(displacement[i]) for i in rows), F(0))
        require(aa == bb == 0 and ab == 7 * alpha * (1 - alpha), "loss decomposition")
        require(total == aa + 2 * ab + bb, "retained pair multiplicity")
        require(core_square == 4 * alpha * alpha * (1 - alpha),
                "quadratic core displacement")

        trace_gap = sum((weight * (norm2(x) - norm2(y))
                         for weight, x, y in zip(weights, source, target)), F(0))
        require(total == 2 * trace_gap, "centered trace identity")
        row_means = [sum((weights[j] * losses[i][j] for j in range(5)), F(0))
                     for i in range(5)]
        for i, j in product(range(5), repeat=2):
            expected = (-F(1, 2) *
                        (losses[i][j] - row_means[i] - row_means[j] + total))
            require(dot(source[i], source[j]) - dot(target[i], target[j]) == expected,
                    "double-centered Gram identity")
            left = -2 * dot(sub(source[i], source[j]),
                            sub(displacement[i], displacement[j]))
            right = losses[i][j] + norm2(sub(displacement[i], displacement[j]))
            require(left == right, "symmetric first variation identity")
            require(losses[i][j] >= 0, "exact contraction pair")
            pair_identities += 2
            contraction_pairs += 1
        for i in range(5):
            q = norm2(source[i]) - norm2(target[i]) + total / 2
            require(q == row_means[i], "one-label mean loss")
            pair_identities += 1
        records.append({
            "alpha": str(alpha),
            "D": str(total),
            "Q_over_D": str(second / total),
            "M": str(mean_square),
            "M_core": str(core_square),
            "covariance_determinant": str(determinant(covariance)),
        })
    return {
        "rare_mass_scales": len(alphas),
        "exact_contraction_pairs": contraction_pairs,
        "pair_and_operator_identities": pair_identities,
        "records": records,
    }


def one_point_controls():
    background = [(-1, 0, 0), (-2, 1, 0), (-2, 0, 1), (-2, -1, -1)]
    weights = [F(1, 4)] * 4
    support = center([tuple(map(F, point)) for point in background], weights)
    covariance = matrix(support, support, weights)
    kappa, radius = F(3, 16), F(3)
    require(symmetric_psd(subtract_diagonal(covariance, kappa)),
            "background covariance floor")
    y = support[0]
    comparisons = posterior_floor_checks = 0
    cases = []
    for length in (F(1, 4), F(1, 2), F(1), F(2)):
        x = add(y, (length, F(0), F(0)))
        require(norm2(x) <= radius * radius, "one-point radius")
        h = sub(y, x)
        q = norm2(x) - norm2(y)
        losses = [norm2(sub(x, z)) - norm2(sub(y, z)) for z in support]
        require(all(value >= 0 for value in losses), "closer to every background center")
        require(q == sum((w * value for w, value in zip(weights, losses)), F(0)),
                "centered one-point loss average")
        require(q * radius >= 2 * kappa * length, "coercivity inequality")
        require(all(value == q + 2 * dot(z, h) for z, value in zip(support, losses)),
                "bisector half-space identity")
        comparisons += len(losses)

        # Exact discrete analogue of the posterior-density-floor step:
        # likelihood ratios average to one and stay above m.
        for floor in (F(1, 2), F(1, 4), F(1, 8)):
            for boosted in range(4):
                ratios = [floor] * 4
                ratios[boosted] = 4 - 3 * floor
                require(sum((w * ratio for w, ratio in zip(weights, ratios)), F(0)) == 1,
                        "posterior normalization")
                posterior_loss = sum((w * ratio * value
                                      for w, ratio, value in zip(weights, ratios, losses)), F(0))
                require(posterior_loss >= floor * q, "posterior floor retains mean loss")
                posterior_floor_checks += 1
        cases.append({"length": str(length), "q": str(q),
                      "minimum_center_loss": str(min(losses))})
    return {
        "one_point_cases": cases,
        "center_comparisons": comparisons,
        "posterior_floor_checks": posterior_floor_checks,
        "covariance_determinant": str(determinant(covariance)),
    }


def assembly_and_error_controls():
    coefficient_checks = 0
    for c0, beta in product((F(1, 11), F(2, 7), F(3, 5)),
                            (F(1, 13), F(1, 3), F(4, 5))):
        common = min(c0, beta / 4)
        for daa, dab, dbb in product((F(0), F(1, 9), F(2, 3), F(5)), repeat=3):
            core_rare = c0 * daa + beta / 2 * (dab + dbb)
            total = daa + 2 * dab + dbb
            require(core_rare >= common * total, "retained-loss coefficient assembly")
            coefficient_checks += 1

    # With alpha <= K D/delta^2 and M <= K D, the squared normalized
    # cross-error is bounded by K^3 D/delta^4.  These exact scales exercise
    # the sequential little-o calculation without using square roots.
    K, delta = F(7), F(1, 5)
    error_scales = []
    previous = None
    for exponent in (8, 16, 32, 64):
        loss = F(1, 2**exponent)
        alpha = K * loss / (delta * delta)
        mean_square = K * loss
        alpha_square_ratio = alpha * alpha / loss
        cross_ratio_squared = alpha * alpha * mean_square / (loss * loss)
        require(alpha_square_ratio == K * K * loss / delta**4,
                "quadratic rare-mass error rate")
        require(cross_ratio_squared == K**3 * loss / delta**4,
                "core-rare error rate")
        if previous is not None:
            require(cross_ratio_squared < previous, "strict error decay")
        previous = cross_ratio_squared
        error_scales.append({"D": str(loss),
                             "alpha_squared_over_D": str(alpha_square_ratio),
                             "squared_alpha_sqrtM_over_D": str(cross_ratio_squared)})
    return {"coefficient_checks": coefficient_checks, "error_scales": error_scales}


def rejected_controls():
    background = [(-1, 0, 0), (-2, 1, 0), (-2, 0, 1), (-2, -1, -1)]
    raw_source = [tuple(map(F, point)) for point in background + [(1, 0, 0)]]
    raw_target = [tuple(map(F, point)) for point in background + [(-1, 0, 0)]]
    alpha = F(1, 4)
    weights = [(1 - alpha) / 4] * 4 + [alpha]
    source, target = center(raw_source, weights), center(raw_target, weights)
    attempts = [
        (source, [scale(F(2), point) for point in source], weights, F(3), F(3, 32)),
        (source, target, [F(-1)] + weights[1:], F(3), F(3, 32)),
        (source[:-1], target, weights, F(3), F(3, 32)),
        (source, target, weights, F(1, 10), F(3, 32)),
        (source, target, weights, F(3), F(100)),
    ]
    rejected = 0
    for args in attempts:
        try:
            validate_fold(*args)
        except (AssertionError, IndexError):
            rejected += 1
        else:
            raise AssertionError("malformed or adverse input accepted")
    return rejected


def audit():
    manifest = pin_inputs()
    return {
        "status": "INDEPENDENT_MEAN_LOSS_MARGIN_REVIEW_PASS",
        "target_commit": manifest["target_commit"],
        "target_graph_ref": manifest["target_graph_ref"],
        "pinned_target_files": len(manifest["files"]),
        "fold_and_operator": fold_and_operator_controls(),
        "one_point": one_point_controls(),
        "assembly_and_errors": assembly_and_error_controls(),
        "damaged_or_adverse_rejections": rejected_controls(),
        "verdict": ("accept the fixed-radius, fixed-covariance-floor, bounded-volume "
                    "small-mean-loss theorem; the compactness cutoff is non-effective "
                    "and unrestricted dimension-three majorisation remains open"),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected", type=Path, default=HERE / "REVIEW_EXPECTED.json")
    parser.add_argument("--print-record", action="store_true")
    args = parser.parse_args()
    result = audit()
    raw = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.print_record:
        print(raw, end="")
        return
    require(result == json.loads(args.expected.read_text()), "review record differs")
    print(result["status"])
    print("record_sha256", sha256(raw.encode()).hexdigest())


if __name__ == "__main__":
    main()
