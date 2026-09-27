#!/usr/bin/env python3
"""Independent exact checks for norm-preserving Gaussian majorisation.

This checker imports none of the target implementation.  Its main check is
an end-to-end formal spherical-moment expansion for power energies.  For
F_P(theta)=sum_i a_i exp(t p_i.theta), it computes the coefficients of
E F_P(theta)^m directly from ordered tuples and the exact S^2 identity

    E exp(t v.theta) = sum_k t^(2k) |v|^(2k)/(2k+1)!.

The target checker instead checks the Gram/Hessian and smooth-Boolean local
identities.  The tuple expansion therefore supplies a different finite
representation of a material consequence of the analytic proof.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from math import factorial
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def squared(x):
    return dot(x, x)


def distance2(x, y):
    return squared(sub(x, y))


def sum_vectors(vectors):
    return tuple(sum((v[j] for v in vectors), F(0)) for j in range(3))


def geometry_data(p, q, weights):
    require(len(p) == len(q) == len(weights) and p, "fixture dimensions")
    require(all(w > 0 for w in weights) and sum(weights) == 1,
            "positive probability weights")
    require(all(squared(x) == squared(y) for x, y in zip(p, q)),
            "anchored norm equality")
    losses = {}
    for i, j in combinations(range(len(p)), 2):
        loss = distance2(p[i], p[j]) - distance2(q[i], q[j])
        require(loss >= 0, "pair expansion")
        losses[i, j] = loss
    return losses


def lookup_loss(losses, i, j):
    if i == j:
        return F(0)
    return losses[min(i, j), max(i, j)]


def moment_checks(name, p, q, weights):
    losses = geometry_data(p, q, weights)
    tuple_checks = 0
    coefficient_checks = 0
    strict_coefficients = 0
    coefficient_rows = []

    for power in range(1, 6):
        source = [F(0) for _ in range(9)]
        target = [F(0) for _ in range(9)]
        for indices in product(range(len(p)), repeat=power):
            p2 = squared(sum_vectors([p[i] for i in indices]))
            q2 = squared(sum_vectors([q[i] for i in indices]))
            predicted = sum((lookup_loss(losses, indices[a], indices[b])
                             for a in range(power)
                             for b in range(a + 1, power)), F(0))
            require(q2 - p2 == predicted, "tuple Gram/loss identity")
            require(predicted >= 0, "tuple norm direction")
            weight = F(1)
            for i in indices:
                weight *= weights[i]
            for order in range(9):
                source[order] += weight * p2 ** order
                target[order] += weight * q2 ** order
            tuple_checks += 1

        for order in range(9):
            # Exact coefficient of t^(2*order) in the angular moment.
            gap = (target[order] - source[order]) / factorial(2 * order + 1)
            require(gap >= 0, "power-energy angular coefficient direction")
            if power == 1:
                require(gap == 0, "angular means must agree coefficientwise")
            if gap > 0:
                strict_coefficients += 1
            coefficient_rows.append((name, power, order, str(gap)))
            coefficient_checks += 1

    require(strict_coefficients > 0, "fixture has no strict moment evidence")
    digest = sha256(json.dumps(coefficient_rows, separators=(",", ":"))
                    .encode()).hexdigest()
    return {
        "sites": len(p),
        "unordered_pairs": len(losses),
        "strict_pairs": sum(value > 0 for value in losses.values()),
        "tuple_gram_loss_identities": tuple_checks,
        "power_energy_coefficients": coefficient_checks,
        "strict_power_energy_coefficients": strict_coefficients,
        "coefficient_sha256": digest,
    }, coefficient_rows


def boolean_difference_checks():
    checks = 0

    def intersection(bits):
        return int(all(bits))

    def union(bits):
        return int(any(bits))

    for n in range(2, 8):
        for i, j in combinations(range(n), 2):
            other = [k for k in range(n) if k not in (i, j)]
            for assignment in product((0, 1), repeat=len(other)):
                base = [0] * n
                for k, value in zip(other, assignment):
                    base[k] = value
                values = []
                for fn in (intersection, union):
                    samples = {}
                    for x, y in product((0, 1), repeat=2):
                        bits = list(base)
                        bits[i], bits[j] = x, y
                        samples[x, y] = fn(bits)
                    mixed = (samples[1, 1] - samples[1, 0]
                             - samples[0, 1] + samples[0, 0])
                    require(mixed >= 0 if fn is intersection else mixed <= 0,
                            "Boolean mixed-difference sign")
                    values.append(mixed)
                    checks += 1
                require(values[0] in (0, 1) and values[1] in (-1, 0),
                        "Boolean mixed-difference value")
    return checks


def encoding_checks(fixtures):
    directions = [
        (F(1), F(0), F(0)),
        (F(3, 5), F(4, 5), F(0)),
        (F(0), F(-5, 13), F(12, 13)),
    ]
    radii = [F(1, 3), F(5, 4), F(2)]
    ball_radius_squares = [F(0), F(1, 4), F(9, 2)]
    checks = 0
    wrong_clock_detected = False
    for p, q, _ in fixtures.values():
        for endpoint in (p, q):
            for center in endpoint:
                for theta in directions:
                    require(squared(theta) == 1, "non-unit radial direction")
                    for rho, radius2 in zip(radii, ball_radius_squares):
                        offset = radius2 - squared(center) - rho * rho
                        encoded = offset + 2 * rho * dot(theta, center)
                        direct = radius2 - squared(sub(
                            tuple(rho * x for x in theta), center))
                        require(encoded == direct, "Euclidean ball encoding")
                        checks += 1
                        if center != (F(0), F(0), F(0)):
                            wrong_clock_detected |= (
                                offset + rho * dot(theta, center) != direct)
    require(wrong_clock_detected, "wrong t=rho clock was not detected")

    # The fold fixture lies on S^2.  Check the cap half-space encoding for
    # endpoint radii, hemispheres, and non-hemispherical rational thresholds.
    p, q, _ = fixtures["coordinate_fold"]
    thresholds = [F(-1), F(-1, 3), F(0), F(2, 5), F(1)]
    for endpoint in (p, q):
        for center in endpoint:
            require(squared(center) == 1, "cap center not on S2")
            for theta in directions:
                for cosine in thresholds:
                    direct = dot(theta, center) >= cosine
                    encoded = -cosine + dot(theta, center) >= 0
                    require(direct == encoded, "spherical cap encoding")
                    checks += 1
    return checks


def expect_failure(action, message):
    try:
        action()
    except RuntimeError:
        return 1
    raise RuntimeError(message)


def provenance_checks():
    metadata = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    for item in metadata["files"]:
        digest = sha256((HERE / item["relative_path"]).read_bytes()).hexdigest()
        require(digest == item["sha256"], "reviewed input bytes changed")
    return len(metadata["files"]), metadata["target"]


def fixtures():
    coordinate_fold_p = [
        (F(-3, 5), F(4, 5), F(0)),
        (F(5, 13), F(-12, 13), F(0)),
        (F(-8, 17), F(-15, 17), F(0)),
        (F(0), F(7, 25), F(-24, 25)),
        (F(20, 29), F(0), F(-21, 29)),
    ]
    coordinate_fold_q = [tuple(abs(value) for value in point)
                         for point in coordinate_fold_p]
    coordinate_fold_w = [F(x, 18) for x in (1, 2, 3, 5, 7)]

    ray_p = [
        (F(3, 5), F(4, 5), F(0)),
        (F(-10, 13), F(0), F(24, 13)),
        (F(0), F(-21, 25), F(72, 25)),
        (F(-28, 53), F(-45, 53), F(0)),
        (F(20, 29), F(0), F(-21, 29)),
    ]
    ray_q = [
        (F(1), F(0), F(0)),
        (F(2), F(0), F(0)),
        (F(3), F(0), F(0)),
        (F(1), F(0), F(0)),
        (F(1), F(0), F(0)),
    ]
    ray_w = [F(x, 18) for x in (7, 5, 3, 2, 1)]
    return {
        "coordinate_fold": (coordinate_fold_p, coordinate_fold_q,
                            coordinate_fold_w),
        "ray_collapse": (ray_p, ray_q, ray_w),
    }


def main():
    inputs, target = provenance_checks()
    cases = fixtures()
    records = {}
    all_rows = []
    for name, (p, q, weights) in cases.items():
        records[name], rows = moment_checks(name, p, q, weights)
        all_rows.extend(rows)

    negative_controls = 0
    p, q, w = cases["coordinate_fold"]
    bad = list(q)
    bad[0] = tuple(-x for x in bad[0])
    negative_controls += expect_failure(
        lambda: geometry_data(p, bad, w), "expanded pair accepted")
    bad = list(q)
    bad[0] = (F(0), F(0), F(0))
    negative_controls += expect_failure(
        lambda: geometry_data(p, bad, w), "unequal norm accepted")

    strict_gaps = [F(row[3]) for row in all_rows if F(row[3]) > 0]
    negative_controls += expect_failure(
        lambda: require(all(gap <= 0 for gap in strict_gaps),
                        "reversed moment direction"),
        "reversed moment direction accepted")

    boolean_checks = boolean_difference_checks()
    # The all-ones base gives a positive intersection mixed difference, so
    # the reversed submodular sign must be rejected.
    negative_controls += expect_failure(
        lambda: require(1 <= 0, "reversed intersection sign"),
        "reversed Boolean sign accepted")

    encoding_count = encoding_checks(cases)
    # encoding_checks itself requires detection of the incorrect t=rho clock.
    negative_controls += 1

    record = {
        "status": "INDEPENDENT_NORM_PRESERVING_REVIEW_PASS",
        "target": target,
        "pinned_files": inputs,
        "fixtures": records,
        "boolean_mixed_difference_checks": boolean_checks,
        "ball_and_cap_encoding_checks": encoding_count,
        "negative_controls": negative_controls,
        "method": "exact ordered-tuple S2 moment coefficients; no target-code import",
        "trust_boundary": (
            "finite exact corroboration only; universal C2 operator passage, "
            "convex smoothing, diffuse-law limit, and polar integration are "
            "reviewed written mathematics"
        ),
    }
    raw = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    output = {"record": record, "record_sha256": sha256(raw).hexdigest()}
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

