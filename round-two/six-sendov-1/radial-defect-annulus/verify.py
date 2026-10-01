#!/usr/bin/env python3
"""Exact finite algebra for the radial-defect / joint-channel annulus proof.

Python 3.10+, standard library. Default invocation only reads expected.json.
--emit explicitly regenerates that compact fixture. No floating point, solver,
campaign imports, or sampled universal claims are used.
"""
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import comb
from pathlib import Path
import argparse
import json


class CheckError(Exception):
    pass


def require(ok, message):
    if not ok:
        raise CheckError(message)


def add(p, q, scale=F(1)):
    out = p.copy()
    for key, value in q.items():
        out[key] = out.get(key, F(0)) + scale * value
        if not out[key]:
            del out[key]
    return out


def mul(p, q):
    out = {}
    for key, value in p.items():
        for other, weight in q.items():
            index = tuple(i + j for i, j in zip(key, other))
            out[index] = out.get(index, F(0)) + value * weight
    return {key: value for key, value in out.items() if value}


def power(p, n, dimension):
    out = {(0,) * dimension: F(1)}
    for _ in range(n):
        out = mul(out, p)
    return out


def to_bernstein(p, da, du):
    require(all(i <= da and j <= du for i, j in p), "power degrees")
    return [[sum(value * F(comb(i, ia), comb(da, ia))
                 * F(comb(j, ju), comb(du, ju))
                 for (ia, ju), value in p.items() if ia <= i and ju <= j)
             for j in range(du + 1)] for i in range(da + 1)]


def from_bernstein(matrix, da, du):
    out = {}
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if not value:
                continue
            for s in range(da - i + 1):
                for t in range(du - j + 1):
                    key = i + s, j + t
                    weight = (comb(da, i) * comb(da - i, s)
                              * comb(du, j) * comb(du - j, t)
                              * (-1) ** (s + t))
                    out[key] = out.get(key, F(0)) + value * weight
    return {key: value for key, value in out.items() if value}


def bmul(p, dp, q, dq):
    """Direct tensor Bernstein product, independent of power conversion."""
    degree = tuple(i + j for i, j in zip(dp, dq))
    out = {}
    for key, value in p.items():
        for other, weight in q.items():
            index = tuple(i + j for i, j in zip(key, other))
            ratio = F(1)
            for axis in range(len(degree)):
                ratio *= F(comb(dp[axis], key[axis])
                           * comb(dq[axis], other[axis]),
                           comb(degree[axis], index[axis]))
            out[index] = out.get(index, F(0)) + value * weight * ratio
    return {key: value for key, value in out.items() if value}, degree


def bpower(p, degree, n):
    out, total = {(0,) * len(degree): F(1)}, (0,) * len(degree)
    for _ in range(n):
        out, total = bmul(out, total, p, degree)
    return out, total


def elevate(p, degree, target):
    extra = tuple(i - j for i, j in zip(target, degree))
    require(min(extra) >= 0, "degree elevation")
    one = {key: F(1) for key in product(*(range(d + 1) for d in extra))}
    out, total = bmul(p, degree, one, extra)
    require(total == target, "elevated degree")
    return out


def profile_power(k, penalty=F(5)):
    m = 8 - k
    aa = {(0, 0, 0): F(1), (1, 0, 0): F(1), (1, 0, 1): F(-1)}
    bb = add(aa, {(2, 1, 1): F(-8, m)})
    integrand = mul(power(aa, k, 3), power(bb, m, 3))
    integral = {}
    for (i, j, t), value in integrand.items():
        integral[i, j] = integral.get((i, j), F(0)) + F(9, t + 1) * value
    radius_product = power({(0, 0): F(1), (1, 1): F(8, m)}, m, 2)
    defect = {(3, 2): F(64 * (m - 1), m),
              (3, 3): F(-256 * (m - 1) * (m - 2), 3 * m * m)}
    defect = {key: value for key, value in defect.items() if value}
    out = add(integral, radius_product, -1)
    out = add(out, {(0, 0): F(8), (9, 0): F(-8)}, -1)
    return add(out, defect, -penalty)


def profile_direct(k):
    m, target = 8 - k, (16 - k, 8 - k)
    aa = {(i, 0, s): F(1 + i * (1 - s))
          for i in range(2) for s in range(2)}
    bb = {(i, j, s): F(1) + F(i, 2) * (1 - s)
          - F(8, m) * (i == 2) * j * s
          for i in range(3) for j in range(2) for s in range(2)}
    p, dp = bpower(aa, (1, 0, 1), k)
    q, dq = bpower(bb, (2, 1, 1), m)
    integrand, total = bmul(p, dp, q, dq)
    require(total == (*target, 8), "integrand degree")
    out = {}
    # Nine times integral B_s^8 equals one: sum all t layers.
    for (i, j, _), value in integrand.items():
        out[i, j] = out.get((i, j), F(0)) + value
    factor = {(i, j): F(1) + F(8, m) * i * j
              for i in range(2) for j in range(2)}
    rp, degree = bpower(factor, (1, 1), m)
    out = add(out, elevate(rp, degree, target), -1)
    gap = {(i, 0): F(8 if i < 9 else 0) for i in range(10)}
    out = add(out, elevate(gap, (9, 0), target), -1)
    if m > 1:
        d2 = elevate({(3, 2): F(64 * (m - 1), m)}, (3, 2), target)
        out = add(out, d2, -5)
    if m > 2:
        d3 = elevate({(3, 3): F(-256 * (m - 1) * (m - 2), 3 * m * m)},
                     (3, 3), target)
        out = add(out, d3, -5)
    return [[out.get((i, j), F(0)) for j in range(target[1] + 1)]
            for i in range(target[0] + 1)]


def h_coefficients():
    factor = {(0, 0): F(1), (1, 0): F(-1),
              (1, 1): F(2), (2, 1): F(-1)}
    h = [F(0)] * 17
    for (d, t), value in power(factor, 8, 2).items():
        h[d] += value / (t + 1)
    independent = [F(0)] * 17
    for k in range(9):
        for i in range(9 - k):
            for j in range(k + 1):
                independent[k + i + j] += (
                    F(comb(8, k), k + 1) * comb(8 - k, i) * (-1) ** i
                    * comb(k, j) * 2 ** (k - j) * (-1) ** j)
    require(h == independent, "full H coefficient identity")
    require(h[:3] == [F(1), F(0), F(16, 3)], "H low coefficients")
    return h


def finite_constants(h):
    gamma, delta = F(1, 10**6), F(1, 10**10)
    k1 = 9 * sum(F(comb(7, i), i + 2) * F(8, 7) ** i for i in range(8))
    k2 = 9 * sum(F(comb(6, i), i + 3) * F(4, 3) ** i for i in range(7))
    tail = sum(abs(h[k]) * F(1, 100) ** (k - 3) for k in range(3, 17))
    variance_cap = (1 + 24 * gamma + 37500 * gamma**2) / (1 - 30 * gamma)
    e2_floor = 28 * (1 - 3 * gamma)**2 - 18
    spread_slack = F(1, 2048) - (72 + F(1, 1024)) * delta - F(1, 2560)
    bridge_slack = F(5, 983040) - 44800 * delta
    inequalities = {
        "H_tail": tail < 128,
        "A_upper": F(101, 100)**8 < 2,
        "E_upper": 16 / F(99, 100)**2 < 17,
        "variance_remainder": F(3 * 180625, 16) < 37500,
        "variance_cap": variance_cap < F(9, 8),
        "e2_floor": e2_floor > F(28, 3),
        "K1_value": k1 == F(570801247, 1647086),
        "K2_value": k2 == F(1199851, 5103),
        "phase_K1": k1 < 350,
        "phase_K2": k2 < 2 * k1,
        "tube_collar": 1 - delta >= F(511, 512),
        "variance_collar": delta <= gamma,
        "spread_slack": spread_slack > 0,
        "origin_phase_slack": bridge_slack > 0,
        "origin_phase_value": bridge_slack == F(46561, 76800000000),
    }
    for name, ok in inequalities.items():
        require(ok, "finite comparison: " + name)
    return {
        "H_tail_bound_at_1_over_100": str(tail),
        "K1": str(k1), "K2": str(k2),
        "variance_cap_at_1e_minus_6": str(variance_cap),
        "e2_floor_at_1e_minus_6": str(e2_floor),
        "spread_slack_at_1e_minus_10": str(spread_slack),
        "origin_phase_slack_at_1e_minus_10": str(bridge_slack),
        "strict_comparisons": len(inequalities),
    }


def generate():
    profiles, entries, power_counts = [], [], []
    for k in range(8):
        da, du = 16 - k, 8 - k
        p = profile_power(k)
        matrix = to_bernstein(p, da, du)
        require(matrix == profile_direct(k), "two full routes at k=" + str(k))
        require(from_bernstein(matrix, da, du) == p, "full inverse at k=" + str(k))
        require(min(min(row) for row in matrix) >= 0, "negative Bernstein entry")
        # Both real boundary equality profiles must have zero residual.
        if k in (0, 7):
            require(matrix[-1][-1] == 0, "boundary equality corner")
        entries.extend(value for row in matrix for value in row)
        power_counts.append(len(p))
        profiles.append({"k": k, "degrees": [da, du],
                         "coefficients": [[str(x) for x in row] for row in matrix]})
    require(len(entries) == 636, "coefficient count")
    require(sum(x == 0 for x in entries) == 46, "zero count")
    require(min(x for x in entries if x) == F(7, 4), "positive coefficient minimum")
    h = h_coefficients()
    constants = finite_constants(h)
    matrices = [item["coefficients"] for item in profiles]
    digest = sha256(json.dumps(matrices, separators=(",", ":")).encode()).hexdigest()
    power_digest = sha256(json.dumps([
        [[i, j, str(value)] for (i, j), value in sorted(profile_power(k).items())]
        for k in range(8)], separators=(",", ":")).encode()).hexdigest()
    # The selected coefficient certificate rejects penalty six; no optimal
    # mathematical penalty and no nonexistence theorem are inferred from this.
    six = to_bernstein(profile_power(6, F(6)), 10, 2)
    require(six[8][2] < 0, "unsupported penalty not detected")
    return {
        "schema": "radial-defect-annulus-v1", "penalty": "5",
        "profiles": profiles, "H_delta_coefficients": [str(x) for x in h],
        "constants": constants,
        "summary": {"bernstein_coefficients": len(entries),
                    "positive": sum(x > 0 for x in entries), "zero": 46,
                    "minimum_positive": "7/4", "full_routes": 2,
                    "full_inverse_checks": 8, "power_term_counts": power_counts,
                    "coefficient_sha256": digest, "power_sha256": power_digest,
                    "penalty_six_negative_control": str(six[8][2])},
    }


def check_fixture(fixture, generated):
    require(fixture == generated, "fixture differs from full exact regeneration")


def damage_controls(generated):
    controls = []
    altered = deepcopy(generated)
    altered["profiles"][0]["coefficients"][0][0] = "1"
    controls.append(altered)
    altered = deepcopy(generated)
    altered["profiles"].pop()
    controls.append(altered)
    altered = deepcopy(generated)
    altered["profiles"][1]["degrees"][0] -= 1
    controls.append(altered)
    altered = deepcopy(generated)
    altered["profiles"][2]["coefficients"][1].pop()
    controls.append(altered)
    altered = deepcopy(generated)
    altered["H_delta_coefficients"][2] = "5"
    controls.append(altered)
    altered = deepcopy(generated)
    altered["constants"]["K1"] = "350"
    controls.append(altered)
    for altered in controls:
        try:
            check_fixture(altered, generated)
        except CheckError:
            continue
        raise CheckError("corruption accepted")
    return len(controls)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="explicitly regenerate expected.json")
    args = parser.parse_args()
    path = Path(__file__).with_name("expected.json")
    generated = generate()
    if args.emit:
        path.write_text(json.dumps(generated, indent=2) + "\n", encoding="utf-8")
    try:
        fixture = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise CheckError("missing or malformed expected.json") from exc
    check_fixture(fixture, generated)
    rejected = damage_controls(generated)
    print(json.dumps({"status": "PASS", **generated["summary"],
                      "H_coefficients": len(generated["H_delta_coefficients"]),
                      "finite_comparisons": generated["constants"]["strict_comparisons"],
                      "rejected_corruptions": rejected}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except CheckError as exc:
        raise SystemExit("FAIL: " + str(exc))
