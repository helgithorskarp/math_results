#!/usr/bin/env python3
"""Independent exact controls for the midpoint-polarization review.

This imports no target code. It pins the reviewed bytes, rebuilds the
compressed schedules, and checks the reflection, repair, and loss-assembly
interfaces with fractions. Continuum Gaussian inequalities remain written
mathematics.
"""

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    return value


def pin_inputs():
    manifest = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    require(manifest["schema"] == 1, "manifest schema")
    for relative, expected in manifest["files"].items():
        actual = sha256((HERE / relative).read_bytes()).hexdigest()
        require(actual == expected, "changed target input: " + relative)
    return manifest


def ceiling(value):
    return -(-value.numerator // value.denominator)


def floor_log2(value):
    require(value > 0, "positive logarithm argument")
    exponent = value.numerator.bit_length() - value.denominator.bit_length()
    trial = F(2**exponent) if exponent >= 0 else F(1, 2**(-exponent))
    if trial > value:
        exponent -= 1
    require((F(2**exponent) if exponent >= 0 else F(1, 2**(-exponent))) <= value,
            "floor lower endpoint")
    return exponent


def ceil_log2(value):
    return -floor_log2(1 / value)


def power2(exponent):
    return F(2**exponent) if exponent >= 0 else F(1, 2**(-exponent))


def schedule(radius, kappa, volume_radius):
    R, k, r = map(F, (radius, kappa, volume_radius))
    require(R > 0 and k > 0 and r > 0 and 3 * k <= R**2,
            "admissible schedule")
    e0 = ceiling((r + R)**2 / 2 + (r + 3 * R)**2)
    eb = ceiling((r + R)**2 / 2 + (r + 4 * R)**2 + 2 * R**2)
    ep = ceiling((r + 6 * R)**2 / 2)
    eg = ceiling((r + 4 * R)**2 + (r + R)**2)
    ew = ceiling((r + R)**2)
    a0, ab = 6 + 2 * e0, 7 + 2 * eb
    k0 = ceil_log2(2 * R**2 / k)
    k1 = ceil_log2(16 * R / k)
    k2 = ceil_log2(2 * R) + 2 * ew
    ell = ceil_log2(96 * R**3 / k + 6 * R)
    A = max(1, -floor_log2(k / (8 * R**2)),
            2 * ep - floor_log2(k / (16 * R)),
            2 * eg - floor_log2(k / (48 * R**2)))
    h = max(a0, ab + 3)
    t2 = max(0, -floor_log2(R), h + 2 + k1)
    t1 = max(t2 + 1, 2 * t2 + ceil_log2(12 * R),
             2 * t2 - floor_log2(k / (576 * R**3)),
             ab + 2 * t2 - floor_log2(k / (48 * R**2)))
    j = 1 + max(-1, ceil_log2(12 * R**2) + k0 + 2 * t1)
    constraints = [ceil_log2(8 * R**4 / k**3), A + 2 * t1 + k0,
                   t2 + j - floor_log2(k / (16 * R)),
                   h + 4 * t2 + 3 + 2 * ell + 2 * k0,
                   2 * h + 4 * t2 + 6 + 2 * k2 + 3 * k0]
    return {"R": R, "k": k, "r": r, "a0": a0, "ab": ab,
            "k0": k0, "k1": k1, "k2": k2, "ell": ell, "A": A,
            "h": h, "t2": t2, "t1": t1, "j": j,
            "constraints": constraints, "N": max(0, *constraints),
            "margin": h + 1}


def expanded_budgets(row):
    R, k, r = row["R"], row["k"], row["r"]
    c0, b = power2(-row["a0"]), power2(-row["ab"])
    K0, K1, K2 = power2(row["k0"]), power2(row["k1"]), power2(row["k2"])
    L = power2(row["ell"])
    alpha, c = power2(-row["A"]), power2(-row["h"])
    d2, d1, D = power2(-row["t2"]), power2(-row["t1"]), power2(-row["N"])
    e0 = ceiling((r + R)**2 / 2 + (r + 3 * R)**2)
    eb = ceiling((r + R)**2 / 2 + (r + 4 * R)**2 + 2 * R**2)
    ep = ceiling((r + 6 * R)**2 / 2)
    eg = ceiling((r + 4 * R)**2 + (r + R)**2)
    ew = ceiling((r + R)**2)
    checks = [
        c0 <= F(1, 64) * power2(-2 * e0),
        b <= F(1, 128) * power2(-2 * eb),
        K0 >= 2 * R**2 / k, K1 >= 16 * R / k,
        K2 >= 2 * R * power2(2 * ew), L >= 96 * R**3 / k + 6 * R,
        alpha <= F(1, 2), alpha <= k / (8 * R**2),
        alpha <= k / (16 * R) * power2(-2 * ep),
        alpha <= k / (48 * R**2) * power2(-2 * eg),
        c <= c0, c <= b / 8,
        d2 <= 1, d2 <= R, d2 <= c / (4 * K1),
        d1 <= d2 / 2, d1 <= d2**2 / (12 * R),
        d1 <= k * d2**2 / (576 * R**3),
        d1 <= b * k * d2**2 / (48 * R**2),
        D <= k**3 / (8 * R**4), D <= alpha * d1**2 / K0,
        D <= k * d2 / (16 * R * (F(1, 2) + 12 * R**2 * K0 / d1**2)),
        D <= c * d2**4 / (8 * L**2 * K0**2),
        D <= c**2 * d2**4 / (64 * K2**2 * K0**3),
        power2(-row["margin"]) <= c / 2,
    ]
    require(all(checks), "expanded sufficient budget")
    return len(checks)


def schedule_controls():
    cases = [(F(1), F(1, 32), F(1)),
             (F(1, 2), F(1, 384), F(9, 2)),
             (F(3), F(3, 32), F(1))]
    rows, checks = [], 0
    for R, k, r in cases:
        row = schedule(R, k, r)
        checks += expanded_budgets(row)
        rows.append({"radius": R, "kappa": k, "volume_radius": r,
                     "cutoff_exponent": row["N"],
                     "margin_exponent": row["margin"],
                     "constraint_exponents": row["constraints"]})
    require([(row["cutoff_exponent"], row["margin_exponent"])
             for row in rows] == [(567, 69), (967, 123), (2900, 401)],
            "headline schedules")
    return {"expanded_budget_checks": checks, "rows": rows}


def dot(first, second):
    return sum((a * b for a, b in zip(first, second)), F(0))


def sub(first, second):
    return tuple(a - b for a, b in zip(first, second))


def add(first, second):
    return tuple(a + b for a, b in zip(first, second))


def scale(value, vector):
    return tuple(value * coordinate for coordinate in vector)


def norm2(vector):
    return dot(vector, vector)


def reflection_controls():
    checks = 0
    for ell, t, m, perpendicular in product(
            (F(1, 5), F(1), F(7, 2)),
            (F(1, 7), F(2, 3), F(4)),
            (F(-2), F(0), F(3, 5)),
            (F(0), F(5, 11))):
        x, y = (m + ell / 2, perpendicular), (m - ell / 2, perpendicular)
        z, reflected = (m - t, F(1, 3)), (m + t, F(1, 3))
        require(norm2(sub(z, x)) - norm2(sub(z, y)) == 2 * ell * t,
                "favorable kernel exponent")
        require(norm2(sub(reflected, y)) == norm2(sub(z, x)),
                "reflection pairing")
        checks += 1
    return {"midpoint_exponent_checks": checks}


def repair_controls():
    background = [tuple(map(F, point)) for point in
                  [(-1, 0, 0), (-2, 1, 0), (-2, 0, 1), (-2, -1, -1)]]
    x = (F(1), F(0), F(0))
    checks = damaged_rejections = 0
    for p, q in product(range(-6, 7), repeat=2):
        y = (F(0), F(p, 2), F(q, 2))
        ell2 = norm2(sub(x, y))
        eta = max(F(0), *(norm2(sub(y, a)) - norm2(sub(x, a))
                          for a in background))
        if not 0 < eta < ell2 / 2:
            continue
        t = eta / ell2
        repaired = add(scale(1 - t, y), scale(t, x))
        for a in background:
            exact = ((1 - t) * norm2(sub(y, a)) + t * norm2(sub(x, a))
                     - t * (1 - t) * ell2)
            require(norm2(sub(repaired, a)) == exact <= norm2(sub(x, a)),
                    "exact interpolation repair")
            checks += 1
        # The damaged choice t=eta/(2l^2) need not repair the worst center.
        bad_t = eta / (2 * ell2)
        damaged = add(scale(1 - bad_t, y), scale(bad_t, x))
        if any(norm2(sub(damaged, a)) > norm2(sub(x, a)) for a in background):
            damaged_rejections += 1
    require(checks > 0 and damaged_rejections * 4 == checks,
            "every repair witness rejects the half-strength interpolation")
    return {"center_repair_checks": checks,
            "damaged_interpolation_rejections": damaged_rejections}


def coefficient_controls():
    robust_cases = assembly_cases = 0
    # p is the favorable density envelope and ratio=w/w1. These are abstract
    # exact controls for the two exceptional-mass absorptions in Sections 3.1-3.2.
    for R, k, p, ratio in product((F(1, 2), F(1), F(3)),
                                  (F(1, 128), F(1, 16)),
                                  (F(1, 64), F(1, 8)),
                                  (F(1, 256), F(1, 32))):
        alpha = min(F(1, 2), k * p / (16 * R), k * ratio / (48 * R**2))
        bbar = k / (4 * R)
        require((1 - alpha) * p * bbar - alpha >= 0,
                "actual-set polarization survives exception")
        # Normalize w1=1 and w=ratio.
        require((1 - alpha) * ratio * bbar - 3 * R * alpha
                >= ratio * bbar / 4,
                "posterior midpoint retains a quarter bias")
        robust_cases += 1

    for c0, b, daa, dab, dbb in product(
            (F(1, 64), F(1, 16)), (F(1, 8), F(1, 2)),
            range(4), range(4), range(4)):
        cstar = min(c0, b / 8)
        favorable = c0 * daa + b / 4 * (dab + dbb)
        total = daa + 2 * dab + dbb
        require(favorable >= cstar * total, "mixed loss counted twice")
        assembly_cases += 1
    return {"robust_polarization_cases": robust_cases,
            "loss_assembly_cases": assembly_cases,
            "mixed_pair_multiplicity": 2}


def run():
    manifest = pin_inputs()
    return {
        "status": "INDEPENDENT_MIDPOINT_POLARIZATION_REVIEW_PASS",
        "verdict": ("accept the midpoint-polarization effective mean-loss theorem "
                    "and compressed schedule in their stated fixed-volume, "
                    "positive-covariance, sufficiently-small-loss scope"),
        "target_commit": manifest["target_commit"],
        "target_graph_ref": manifest["target_graph_ref"],
        "pinned_target_files": len(manifest["files"]),
        "schedules": schedule_controls(),
        "reflection": reflection_controls(),
        "repair": repair_controls(),
        "coefficients": coefficient_controls(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    record = (json.dumps(encode(run()), sort_keys=True, indent=2) + "\n").encode()
    if args.emit:
        print(record.decode(), end="")
        return
    require(record == (HERE / "REVIEW_EXPECTED.json").read_bytes(),
            "expected review record mismatch")
    print("INDEPENDENT_MIDPOINT_POLARIZATION_REVIEW_PASS")
    print("record_sha256=" + sha256(record).hexdigest())


if __name__ == "__main__":
    main()
