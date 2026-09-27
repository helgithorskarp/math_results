#!/usr/bin/env python3
"""Exact structured controls, not a formal proof or arbitrary-law oracle.

CPython 3.11, standard library only. No denominator 2**B is constructed.
Failures raise explicit exceptions; correctness does not depend on assert.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(a, t):
    return tuple(t * x for x in a)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def norm2(a):
    return dot(a, a)


def mean(points, weights):
    return tuple(sum((p * x[a] for p, x in zip(weights, points)), F(0))
                 for a in range(3))


def covariance(points, weights):
    center = mean(points, weights)
    q = [sub(x, center) for x in points]
    return [[sum((p * x[a] * x[b] for p, x in zip(weights, q)), F(0))
             for b in range(3)] for a in range(3)]


def scalar_matrix(c):
    return [[c if a == b else F(0) for b in range(3)] for a in range(3)]


def rank(rows):
    a = [list(map(F, row)) for row in rows]
    if not a:
        return 0
    r = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        c = a[r][col]
        a[r] = [v / c for v in a[r]]
        for i in range(len(a)):
            if i != r and a[i][col]:
                c = a[i][col]
                a[i] = [v - c * w for v, w in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def schedule(R, j, k):
    require(type(R) is int and R >= 1, "R must be a positive integer")
    require(type(j) is int and j >= 0, "j must be a nonnegative integer")
    require(type(k) is int and k >= 0, "k must be a nonnegative integer")
    A = (R + 1)**2 + j + 2 * R + 4
    S = 8 * R * (1 << (j + k)) * A
    m = (S + R + 1)**2
    ell = j + k + 6 * R**2 + 3
    Q = (2 * R + 1)**2
    B = m + j + k + 3 * ell + Q + 13
    require(B + 1 >= ell + 1, "peak error reserve")
    require(B + 1 >= j + k + 3 + R, "tail slope reserve")
    require(B + 1 >= j + k + 4 + 2 * R, "variance reserve")
    require(R <= 1 << R, "elementary integer bound")
    return dict(R=R, j=j, k=k, A=A, S=S, m=m, ell=ell, Q=Q, B=B)


def parse_input(raw):
    fields = {"schema", "R", "j", "k", "c", "walsh_t", "cloud_exponent_offset"}
    require(type(raw) is dict and set(raw) == fields, "input fields mismatch")
    require(raw["schema"] == "fixed-variance-neighborhood-v1", "unknown schema")
    s = schedule(raw["R"], raw["j"], raw["k"])
    require(type(raw["c"]) is str and type(raw["walsh_t"]) is str,
            "rational parameters must be strings")
    c, t = F(raw["c"]), F(raw["walsh_t"])
    require(0 < c <= 1 - F(1, 1 << s["k"]), "homothety reserve missing")
    require(0 < t <= F(1, 128), "reference Walsh interval failed")
    require(F(1, 1 << s["j"]) <= F(1, 16), "reference covariance floor failed")
    offset = raw["cloud_exponent_offset"]
    require(type(offset) is int and 0 <= offset <= 64, "invalid exponent offset")
    # 4 epsilon <= 2^(-B-1) iff 4*2^-offset <= 1/2.
    require(F(4, 1 << offset) <= F(1, 2), "cloud error exceeds budget")
    return s, c, t, offset


def check_coupling(pi, weights, source, target):
    n = len(weights)
    require(len(pi) == n and all(len(row) == n for row in pi), "coupling shape")
    require(all(v >= 0 for row in pi for v in row), "negative coupling mass")
    for i in range(n):
        require(sum(pi[i]) == weights[i], "source marginal mismatch")
        require(sum(pi[j][i] for j in range(n)) == weights[i],
                "target marginal mismatch")
        for a in range(3):
            require(sum(pi[j][i] * source[j][a] for j in range(n))
                    == weights[i] * target[i][a], "conditional moment mismatch")


def balanced_guard(source, target, floor):
    """Reconstruct scatter by pair differences and Gram error by distances."""
    n = len(source)
    loss = [[norm2(sub(source[i], source[j])) - norm2(sub(target[i], target[j]))
             for j in range(n)] for i in range(n)]
    delta = min(loss[i][j] for i, j in combinations(range(n), 2))
    scatter = [[sum((sub(source[i], source[j])[a] * sub(source[i], source[j])[b]
                     for i in range(n) for j in range(n)), F(0)) / (2 * n)
                for b in range(3)] for a in range(3)]
    # Our structured input has scalar scatter, so no spectral oracle is needed.
    require(scatter == scalar_matrix(floor), "reference scalar scatter failed")
    avg = [sum(row) / n for row in loss]
    grand = sum(avg) / n
    gram_error = sum(((loss[i][j] - avg[i] - avg[j] + grand)**2 / 4
                      for i in range(n) for j in range(n)), F(0))
    margin = floor * delta - 4 * gram_error
    return delta, gram_error, margin


def affine_value(coeff, epsilon):
    return coeff[0] + epsilon * coeff[1]


def check_affine_sign(coeff, right, strict=False):
    values = (affine_value(coeff, F(0)), affine_value(coeff, right))
    require(min(values) > 0 if strict else min(values) >= 0,
            "affine interval sign failed")
    return min(values)


def structured_control(raw):
    s, c, t, offset = parse_input(raw)
    signs = list(product((-1, 1), repeat=3))
    parity = [u * v * w for u, v, w in signs]
    weights = [F(3, 16) if chi == 1 else F(1, 16) for chi in parity]
    x = [scale(i, F(1, 4)) for i in signs]
    z = [(F(v * w, 8), F(u * w, 8), F(u * v, 8)) for u, v, w in signs]
    U = [scale(v, c) for v in x]
    Y = [scale(add(scale(a, 1 - t), scale(b, t)), c) for a, b in zip(x, z)]
    require(sum(weights) == 1 and min(weights) > 0, "probability weights")
    require(mean(x, weights) == mean(Y, weights) == (0, 0, 0), "centering")
    require(covariance(x, weights) == scalar_matrix(F(1, 16)), "source covariance")
    require(max(map(norm2, x)) == F(3, 16), "source radius")
    a0, b0 = (1 - t) / 4, t / 8
    target_cov = c*c * (a0*a0 + b0*b0 + a0*b0)
    require(covariance(Y, weights) == scalar_matrix(target_cov), "target covariance")
    require(max(map(norm2, Y)) <= s["R"]**2, "target radius")

    pi = [[F(0) for _ in signs] for _ in signs]
    for i, chi in enumerate(parity):
        a = t / 4 if chi == 1 else 3 * t / 4
        pi[i][i] = weights[i] * (1 - 3 * a)
        for j in range(8):
            if sum(u != v for u, v in zip(signs[i], signs[j])) == 1:
                pi[j][i] = weights[i] * a
    check_coupling(pi, weights, U, Y)
    require(all(pi[i][j] == pi[j][i] for i in range(8) for j in range(8)),
            "coupling reversibility")

    delta, gram, margin = balanced_guard(U, Y, c*c / 2)
    require(delta == c*c * t * (4 - 3*t) / 8, "reference minimum-loss formula")
    require(gram == c**4 * (F(27, 8)*t*t - F(15, 4)*t**3 + F(75, 64)*t**4),
            "reference Gram formula")
    require(margin > 0, "accepted reference guard failed")
    paired_rank = rank([sub(x[i], x[0]) + sub(Y[i], Y[0]) for i in range(1, 8)])
    require(paired_rank == 6, "paired affine rank")
    require(len({sub(a, b) for a, b in zip(x, Y)}) > 1, "anchor obstruction missing")

    # The full cloud interval is proved analytically for c<=1/2. The default
    # record also checks every endpoint using the actual rational coordinates.
    right = F(1, 128)
    labels = list(product(range(8), range(8)))
    tight, strict, straight, coefficients = 0, 0, [], []
    for (i, v), (j, w) in combinations(labels, 2):
        a, b, q = sub(x[i], x[j]), sub(Y[i], Y[j]), sub(signs[v], signs[w])
        ab = sub(a, b)
        loss = (norm2(a) - norm2(b), 2 * dot(q, ab))
        if i == j:
            require(loss == (0, 0), "within-cloud distance not preserved")
            tight += 1
        else:
            check_affine_sign(loss, right, strict=True)
            strict += 1
        # d/dt |(1-t)Pdiff+t Qdiff|^2 at 1 = -2(Qdiff).(Pdiff-Qdiff).
        endpoint = (dot(b, ab), dot(q, ab))
        straight.append(check_affine_sign(endpoint, right))
        coefficients.append([i, v, j, w, str(loss[0]), str(loss[1])])
    require((tight, strict) == (224, 1792), "cloud pair partition")
    require(s["B"] + offset >= 7, "cloud outside geometric interval")
    require(norm2((1, 1, 1)) < 4, "spatial error multiplier")
    # A zero Gram discrepancy forces every distance loss to vanish. The
    # tight/strict partition therefore rejects the full all-pairs guard.
    require(tight > 0 and strict > 0, "balanced guard exclusion missing")

    # Quantities polynomial in epsilon are not evaluated at its huge exponent.
    ordered_loss = sum((weights[i] * weights[j]
                        * (norm2(sub(x[i], x[j])) - norm2(sub(Y[i], Y[j])))
                        for i in range(8) for j in range(8)), F(0))
    require(ordered_loss == 6 * (F(1, 16) - target_cov), "mean loss identity")
    require(ordered_loss >= 3 * F(1, 1 << (s["j"] + s["k"])), "positive loss")
    old_cutoff = F(4224) * F(3, 16) / (1 - c)
    result = {
        "schedule": s,
        "error_budget": {"at_most": "2^(-B-1)",
                         "cloud_epsilon_exponent": s["B"] + offset,
                         "bound_4epsilon_divided_by_2power_minusB": str(F(4, 1 << offset)),
                         "uniform_hinge_margin_exponent": s["B"] + 1},
        "reference": {"sites": 8, "c": str(c), "t": str(t),
                      "source_covariance_scalar": "1/16",
                      "target_covariance_scalar": str(target_cov),
                      "radius_squared": "3/16", "paired_affine_rank": paired_rank,
                      "martingale_positive_entries": sum(v > 0 for row in pi for v in row),
                      "martingale_scalar_moments": 24,
                      "minimum_loss_U_to_Y": str(delta),
                      "gram_error_U_to_Y": str(gram),
                      "balanced_guard_margin": str(margin),
                      "ordered_loss_X_to_Y": str(ordered_loss),
                      "credited_R3_zero_error_cutoff": str(old_cutoff)},
        "cloud_interval": {"epsilon": "0 < epsilon <= 1/128", "sites": 64,
                           "tight_unordered_pairs": tight,
                           "strict_unordered_pairs": strict,
                           "affine_loss_sha256": sha256(canonical(coefficients)).hexdigest(),
                           "straight_motion_endpoint_checks": len(straight),
                           "no_anchored_norm_equality": True,
                           "all_pairs_balanced_guard_rejected": True},
    }
    return result, (pi, weights, U, Y)


def audit_inputs():
    spec = json.loads((ROOT / "INPUTS.json").read_text())
    require(spec["schema"] == "content-pins-v1", "content pin schema")
    for row in spec["files"]:
        path = (ROOT / row["path"]).resolve()
        require(path.is_relative_to(ROOT.parent.resolve()), "pin outside probability tree")
        require(sha256(path.read_bytes()).hexdigest() == row["sha256"],
                "dependency content pin changed: " + row["path"])
    return len(spec["files"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "INPUT.json")
    args = parser.parse_args()
    raw = json.loads(args.input.read_text())
    control, coupling = structured_control(raw)
    audit = []
    for R, j, k in product((1, 2, 4, 10), (0, 4, 10), (0, 1, 4)):
        audit.append(schedule(R, j, k))

    rejected = []

    def reject(label, fn):
        try:
            fn()
        except (ValueError, ZeroDivisionError, TypeError):
            rejected.append(label)
        else:
            raise ValueError("negative control accepted: " + label)

    for label, update in [
        ("zero_radius", {"R": 0}),
        ("boolean_exponent", {"j": True}),
        ("negative_exponent", {"k": -1}),
        ("unsupported_covariance", {"j": 3}),
        ("no_homothety_reserve", {"c": "1"}),
        ("outside_reference_interval", {"walsh_t": "1/64"}),
        ("cloud_budget_exceeded", {"cloud_exponent_offset": 2}),
        ("non_rational_input", {"c": 0.5}),
        ("unknown_schema", {"schema": "unknown"}),
    ]:
        damaged = dict(raw, **update)
        reject(label, lambda damaged=damaged: parse_input(damaged))
    pi, weights, U, Y = coupling
    damaged_pi = [row[:] for row in pi]
    damaged_pi[0][0] += F(1, 10000)
    reject("damaged_coupling_mass", lambda: check_coupling(damaged_pi, weights, U, Y))
    damaged_Y = list(Y)
    damaged_Y[0] = add(Y[0], (F(1, 10000), F(0), F(0)))
    reject("damaged_conditional_mean", lambda: check_coupling(pi, weights, U, damaged_Y))
    reject("expanding_pair", lambda: check_affine_sign((F(-3), F(0)), F(1, 128)))
    reject("endpoint_only_sign_change", lambda: check_affine_sign((F(1), F(-256)), F(1, 128)))
    boundary = dict(raw, cloud_exponent_offset=3)
    parse_input(boundary)
    require(F(4, 1 << 3) == F(1, 2), "exact budget boundary")

    body = {"status": "FIXED_VARIANCE_NEIGHBORHOOD_CONTROLS_PASS",
            "arithmetic": "CPython 3.11 / fractions.Fraction / arbitrary integers",
            "control": control, "schedule_controls": len(audit),
            "schedule_controls_sha256": sha256(canonical(audit)).hexdigest(),
            "negative_controls": rejected,
            "exact_budget_boundary_passed": True, "dependency_pins": audit_inputs(),
            "trust_boundary": "Finite guards only; universal analytic proof is PROOF.md."}
    digest = sha256(canonical(body)).hexdigest()
    print(json.dumps(dict(body, record_sha256=digest), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
