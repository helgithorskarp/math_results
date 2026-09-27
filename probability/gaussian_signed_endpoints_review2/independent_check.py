#!/usr/bin/env python3
"""Independent exact audit of the uniform signed-endpoint certificate."""

import argparse
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
from math import isqrt
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "gaussian_prior_localization"

PINNED = {
    "SIGNED_ENDPOINTS.md":
        "e14ecd00fb6bf302a95845792d2282a854e23df8a157e3abaf63e5f955cc4871",
    "SIGNED_ENDPOINT_EXPECTED.json":
        "ab6428e599d05124b34d9dce8f5b5f390df8daf26bdb5bc08fd4e9e7207dd376",
    "SIGNED_ENDPOINT_INPUTS.json":
        "8c463f2d49557c05f309b851466b5f54220d9ab5892de3b350e805cbe5a0d897",
    "signed_endpoints.py":
        "1664c27efcf80375c48b9d0acec702e64c819368a3986b3e17ac417eb1a98b99",
}


def require(test, message):
    if not test:
        raise ValueError(message)


def frac(value):
    return Q(value)


def n_choose_3(n):
    return n * (n - 1) * (n - 2) // 6


def atom_budget(k):
    # CUBATURE_FRONTIER.md has M(p)=2 binom(p+3,3)-1,
    # p_u=2 ell+3, p_w=4 ell+8 and n=ceil(k/floor(sqrt(ell+1))).
    ell = (k - 1).bit_length()
    h = isqrt(ell + 1)
    n = (k + h - 1) // h
    first = k**3 * (2 * n_choose_3(2 * ell + 6) - 1)
    second = n**3 * (2 * n_choose_3(4 * ell + 11) - 1)
    return min(first, second)


def uniform_certificate(k):
    atoms = atom_budget(k)
    coordinate_denominator = 256 * k**3
    weight_denominator = 4 * k * atoms
    log_weight = (weight_denominator - 1).bit_length()
    pair_loss = Q(1, 256 * k**4)
    delta = pair_loss / (48 * k)
    tail_b = 54 * k**2 + 2 * log_weight
    tail_q = 4 * tail_b / delta
    require(tail_q.denominator == 1, "uniform tail radius should be integral")
    tail_q = tail_q.numerator
    exponent = tail_q**2
    peak = 1 - pair_loss / (weight_denominator**2 * (4 + pair_loss))
    return {
        "status": "SIGNED_ENDPOINTS_ONLY",
        "scope": "every member of R^c_k with at least two positive weights",
        "k": k,
        "atoms": atoms,
        "coordinate_denominator": coordinate_denominator,
        "weight_denominator": weight_denominator,
        "support_radius": 3 * k,
        "minimum_squared_pair_loss": str(pair_loss),
        "minimum_positive_weight": str(Q(1, weight_denominator)),
        "log_inverse_weight_upper": log_weight,
        "mean_support_gap_lower": str(delta),
        "tail_B_upper": tail_b,
        "tail_radius_upper": str(tail_q),
        "low_endpoint": {"base": 2, "negative_exponent": exponent},
        "relative_log_radius_upper": 2 * tail_q,
        "low_adverse_relative_upper": str(-6 * delta * (exponent + 2)),
        "source_peak_upper": str(peak),
        "point_branch": "all thresholds have equal hinges",
        "middle_interval": "[low_endpoint,source_peak_upper] remains unsigned",
    }


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def norm1(a):
    return sum(abs(x) for x in a)


def norm2(a):
    return sum(x * x for x in a)


def ceil_fraction(x):
    return (x.numerator + x.denominator - 1) // x.denominator


def ceil_log2_fraction(x):
    p = 0
    power = Q(1)
    while power < x:
        power *= 2
        p += 1
    return p


def instance_certificate(source, target, weights):
    require(len(source) == len(target) == len(weights) >= 2, "fixture size")
    require(sum(weights) == 1 and min(weights) > 0, "fixture weights")
    pairs = [(i, j) for i in range(len(weights)) for j in range(i + 1, len(weights))]
    losses = [norm2(sub(source[i], source[j])) -
              norm2(sub(target[i], target[j])) for i, j in pairs]
    pair_loss = min(losses)
    require(pair_loss > 0, "fixture must be strictly contracting")

    source_mean = tuple(sum(w * x[t] for w, x in zip(weights, source))
                        for t in range(3))
    target_mean = tuple(sum(w * y[t] for w, y in zip(weights, target))
                        for t in range(3))
    source0 = [sub(x, source_mean) for x in source]
    target0 = [sub(y, target_mean) for y in target]
    radius = max(norm1(v) for v in source0 + target0)
    diameter = max(norm1(sub(source0[i], source0[j])) for i, j in pairs)
    mass = min(weights)
    delta = pair_loss / (8 * diameter)
    log_mass = ceil_log2_fraction(1 / mass)
    tail_b = 6 * radius**2 + 2 * log_mass
    tail_q = 4 * tail_b / delta
    exponent = ceil_fraction(tail_q**2)
    peak = 1 - mass**2 * pair_loss / (4 + pair_loss)
    return {
        "status": "SIGNED_ENDPOINTS_ONLY",
        "positive_source_sites": len(weights),
        "support_radius": str(radius),
        "source_diameter_upper": str(diameter),
        "minimum_squared_pair_loss": str(pair_loss),
        "minimum_positive_weight": str(mass),
        "log_inverse_weight_upper": log_mass,
        "mean_support_gap_lower": str(delta),
        "tail_B_upper": str(tail_b),
        "tail_radius_upper": str(tail_q),
        "low_endpoint": {"base": 2, "negative_exponent": exponent},
        "relative_log_radius_upper": 2 * ceil_fraction(tail_q),
        "low_adverse_relative_upper": str(-6 * delta * (exponent + 2)),
        "source_peak_upper": str(peak),
        "middle_interval": "[low_endpoint,source_peak_upper] remains unsigned",
    }


def rank_six_fixture():
    source = [(Q(0), Q(0), Q(0))]
    target = [(Q(0), Q(0), Q(0))]
    for axis in range(3):
        for sign in (-1, 1):
            x = [Q(0), Q(0), Q(0)]
            y = [Q(0), Q(0), Q(0)]
            x[axis] = Q(sign, 2)
            y[axis] = Q(1, 4)
            source.append(tuple(x))
            target.append(tuple(y))
    weights = [Q(2, 13)] + [Q(11, 78)] * 6
    return source, target, weights


def collapsed_fixture():
    return ([(-Q(1), Q(0), Q(0)), (Q(1), Q(0), Q(0))],
            [(Q(0), Q(0), Q(0)), (Q(0), Q(0), Q(0))],
            [Q(1, 2), Q(1, 2)])


def analytic_identity_controls():
    homothety = 0
    for d2_num in range(1, 14):
        d2 = Q(d2_num, 3)
        for loss_index in range(1, 10):
            ell = d2 * Q(loss_index, 10)
            lam = 1 - ell / (2 * d2)
            # The universal comparison is the exact identity below.
            require(lam**2 - (1 - ell / d2) == ell**2 / (4 * d2**2),
                    "homothety identity")
            for distance_index in range(loss_index, 11):
                a = d2 * Q(distance_index, 10)
                require(0 <= a - ell <= lam**2 * a, "homothety domination")
                homothety += 1

    peak = 0
    for mass_denominator in range(2, 31):
        mass = Q(1, mass_denominator)
        for loss_num in range(1, 18):
            ell = Q(loss_num, 5)
            v = mass**2 * ell / (4 + ell)
            require(0 < 2 * v < 1, "peak range")
            require((1 - v)**2 >= 1 - 2 * v, "square-root majorant")
            peak += 1
    return homothety, peak


def check_record(record):
    require(record["status"] == "SIGNED_FRONTIER_ENDPOINTS_PASS", "author status")
    regenerated = [uniform_certificate(k) for k in (1, 4, 64, 1000)]
    require(record["family_certificates"] == regenerated, "uniform certificate mismatch")

    fixture = rank_six_fixture()
    require(record["rank_six_instance"] == instance_certificate(*fixture),
            "rank-six certificate mismatch")
    collapsed = collapsed_fixture()
    require(record["collapsed_target"] == instance_certificate(*collapsed),
            "collapsed-target certificate mismatch")
    require(record["point"] == {
        "status": "POINT_EQUALITY_ALL_THRESHOLDS", "positive_source_sites": 1,
    }, "point branch")

    # The dyadic cutoff is safe because ln(2)>1/2: for every regenerated
    # record, 2^(-E)<exp(-E/2), and E=Q^2.  The rational consequences needed
    # by the consumer are checked here without evaluating either exponential.
    for item in regenerated:
        radius = int(item["tail_radius_upper"])
        exponent = item["low_endpoint"]["negative_exponent"]
        delta = frac(item["mean_support_gap_lower"])
        require(exponent == radius**2, "dyadic exponent")
        require(item["relative_log_radius_upper"] == 2 * radius,
                "relative radius")
        require(frac(item["low_adverse_relative_upper"]) ==
                -6 * delta * (exponent + 2), "low-tail rational margin")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    for name, digest in PINNED.items():
        require(sha256((TARGET / name).read_bytes()).hexdigest() == digest,
                "target source changed: " + name)
    record = json.loads((TARGET / "SIGNED_ENDPOINT_EXPECTED.json").read_text())
    check_record(record)
    homothety, peak = analytic_identity_controls()

    damaged = deepcopy(record)
    damaged["family_certificates"][0]["low_endpoint"]["negative_exponent"] -= 1
    try:
        check_record(damaged)
    except ValueError:
        corruption_rejected = True
    else:
        corruption_rejected = False
    require(corruption_rejected, "damaged cutoff was accepted")

    result = {
        "status": "INDEPENDENT_SIGNED_ENDPOINT_REVIEW_PASS",
        "pinned_target_files": len(PINNED),
        "uniform_certificates": len(record["family_certificates"]),
        "homothety_identity_checks": homothety,
        "peak_majorant_checks": peak,
        "rank_six_positive_sites": record["rank_six_instance"]["positive_source_sites"],
        "collapsed_target_peak": record["collapsed_target"]["source_peak_upper"],
        "corruption_rejected": corruption_rejected,
    }
    if args.check:
        print(result["status"])
        print("uniform/rank-six/collapsed certificates:",
              result["uniform_certificates"],
              result["rank_six_positive_sites"],
              result["collapsed_target_peak"])
        print("homothety/peak exact controls:", homothety, peak)
        print("corruption rejected:", corruption_rejected)
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
