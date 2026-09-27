#!/usr/bin/env python3
"""Deterministic exact controls; not independent analytic peer review."""

from copy import deepcopy
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

from certificate import (ceil_log2_positive, finite_guard, le_negative_power,
                         psd_three, rational, schedule)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rejected(call, name):
    try:
        call()
    except (ValueError, ZeroDivisionError):
        return name
    raise RuntimeError("malformed input was accepted: " + name)


def main():
    budgets = 0
    for R in [1, 2, 3, 5, 8]:
        for j in [0, 1, 2, 5, 9, 16]:
            c = schedule(R, j)
            Z, S, m, B = (c[key] for key in ["Z", "S", "m", "B"])
            kappa, zeta = Q(1, 1 << j), Q(1, 1 << Z)
            a = kappa / (4 * R)
            require(a * S == R * R + 2 * (j + 2 + 2 * R * R), "tail exponent")
            require(zeta <= kappa / (4 * (1 + R * R)), "peak floor")
            require(zeta * zeta / 8 < 3 * zeta, "strict ball inclusion")
            require(1 - zeta * zeta / 8 >= Q(1, 2), "posterior floor")
            require(m == (S + R) ** 2, "common threshold floor")
            require(B == m + j + 5 * Z + R * R + 14, "hinge exponent")
            require(R * R <= 1 << (R * R), "power budget for radius")
            require(B + 1 >= j + 3 + ceil_log2_positive(Q(R)), "target fits directional ball")
            require(c["target_radius_negative_exponent"] == B + 1, "error uses half the gap")
            require(Q(3) / 48 / 16 / 8 == Q(1, 2048), "homothety coefficient")
            budgets += 1

    # Compare the logarithmic guard with actual powers on both sides of each boundary.
    log_controls = 0
    for k in range(-80, 81):
        power = Q(1 << k) if k >= 0 else Q(1, 1 << -k)
        for multiplier in [Q(1, 2), Q(3, 4), Q(1), Q(5, 4), Q(2)]:
            q = power * multiplier
            e = ceil_log2_positive(q)
            lo = Q(1 << (e - 1)) if e >= 1 else Q(1, 1 << (1 - e))
            hi = Q(1 << e) if e >= 0 else Q(1, 1 << -e)
            require(lo < q <= hi, "ceil-log boundary")
            for n in [0, 17, 80]:
                require(le_negative_power(q, n) == (q <= Q(1, 1 << n)), "dyadic comparison")
            log_controls += 1
    require(le_negative_power(Q(0), 10**100), "zero target must not allocate huge powers")

    c = schedule(1, 2)
    require([c[k] for k in ["S", "m", "Z", "B"]] == [208, 43681, 6, 43728], "published example")
    b = Q(1, 1 << (c["B"] + 1))
    source = {"points": [[Q(a, 2), Q(d, 2), Q(e, 2)] for a, d, e in
                         [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]],
              "weights": [Q(1, 4)] * 4}
    target = {"points": [[0, 0, 0]] + [[sign * b if k == axis else 0 for k in range(3)]
                                     for axis in range(3) for sign in [-1, 1]],
              "weights": [Q(1, 7)] * 7}
    cases = {}

    def record(name, x, y, want="CERTIFIED", **kwargs):
        answer = finite_guard(x, y, **kwargs)
        require(answer["status"] == want, name)
        cases[name] = {k: answer[k] for k in ["status", "guards", "positive_source_atoms", "positive_target_atoms"]}
        return answer

    record("independent_4_and_7_atom_laws_at_cap", source, target)
    zero = {"points": [[0, 0, 0]], "weights": [1]}
    record("point_target", source, zero)

    def affine(law, scale=1, shift=(0, 0, 0), rotate=False):
        points = []
        for p in law["points"]:
            q = [-p[1], p[0], p[2]] if rotate else p
            points.append([scale * q[k] + shift[k] for k in range(3)])
        return {"points": points, "weights": law["weights"][:]}

    record("separate_translations", affine(source, shift=(17, -5, 9)),
           affine(target, shift=(-3, 11, 2)))
    record("joint_orthogonal_rotation", affine(source, rotate=True), affine(target, rotate=True))
    record("variance_rescaling", affine(source, scale=2), affine(target, scale=2), variance=4)
    answer = record("twice_the_target_cap", source, affine(target, scale=2), "UNRESOLVED")
    require(not answer["guards"]["target_radius"], "target boundary must be enforced")
    answer = record("too_small_source_covariance", affine(source, scale=Q(1, 2)), target, "UNRESOLVED")
    require(not answer["guards"]["source_covariance"], "covariance floor must be enforced")
    answer = record("source_outside_radius", affine(source, scale=2), target, "UNRESOLVED")
    require(not answer["guards"]["source_radius"], "radius must be enforced")
    flat = {"points": [[-1, 0, 0], [1, 0, 0]], "weights": [Q(1, 2), Q(1, 2)]}
    record("rank_deficient_source", flat, target, "UNRESOLVED")
    with_zero = deepcopy(source)
    with_zero["points"].append([10**6, -10**6, 0])
    with_zero["weights"].append(0)
    record("zero_mass_outlier_ignored", with_zero, target)
    dyadic_target = {"points": [[0, 0, 0]] + [
        [{"numerator": sign, "negative_exponent": c["B"] + 1} if k == axis else 0 for k in range(3)]
        for axis in range(3) for sign in [-1, 1]], "weights": ["1/7"] * 7}
    record("compact_dyadic_json", source, json.loads(json.dumps(dyadic_target)))

    # All diagonal entries and leading principal minors alone are insufficient for PSD.
    require(not psd_three([[0, 0, 0], [0, 1, 2], [0, 2, 1]]), "nonleading minor")
    require(psd_three([[0, 0, 0], [0, 1, 1], [0, 1, 1]]), "singular PSD boundary")
    require(not psd_three([[1, Q(3, 4), Q(3, 4)], [Q(3, 4), 1, -Q(3, 4)],
                           [Q(3, 4), -Q(3, 4), 1]]), "full determinant")
    invalid = []
    for bad in [0.5, True, {"numerator": 1, "negative_exponent": -1},
                {"numerator": 1.0, "negative_exponent": 4}]:
        invalid.append(rejected(lambda bad=bad: rational(bad), "rational_" + str(len(invalid))))
    invalid.append(rejected(lambda: schedule(0, 2), "zero_radius"))
    invalid.append(rejected(lambda: schedule(1, -1), "negative_covariance_bits"))
    invalid.append(rejected(lambda: finite_guard(source, target, variance=0), "zero_variance"))
    bad = deepcopy(source)
    bad["weights"][0] = Q(1, 3)
    invalid.append(rejected(lambda: finite_guard(bad, target), "incorrect_total_mass"))
    bad2 = {"points": [[0, 0, 0], [1, 0, 0]], "weights": [-1, 2]}
    invalid.append(rejected(lambda: finite_guard(bad2, target), "negative_mass"))
    invalid.append(rejected(lambda: finite_guard({"points": [[0, 0]], "weights": [1]}, target), "wrong_dimension"))

    record_data = {
        "claim_status": "complete author proof pending independent review",
        "example_schedule": c,
        "exact_scalar_schedules": budgets,
        "exact_log_boundary_controls": log_controls,
        "finite_law_cases": cases,
        "malformed_rejections": invalid,
        "trust_boundary": "The controls do not prove the analytic identities or the diffuse-law theorem.",
    }
    canonical = json.dumps(record_data, sort_keys=True, separators=(",", ":")).encode()
    record_data["record_sha256"] = hashlib.sha256(canonical).hexdigest()
    expected = Path(__file__).with_name("EXPECTED.json")
    if expected.exists():
        require(json.loads(expected.read_text()) == record_data, "expected record mismatch")
    print(json.dumps(record_data, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
