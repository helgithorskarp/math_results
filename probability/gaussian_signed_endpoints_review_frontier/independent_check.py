#!/usr/bin/env python3
"""Independent exact audit of the uniform signed-endpoint certificate.

This checker does not evaluate Gaussian integrals.  It rebuilds the rational
frontier constants from the definitions, checks the two algebraic estimates
used around the analytic lemmas, and differentially tests the public instance
producer on exact fixtures.  The mean-width comparison and the low-tail lemma
remain written analytic proof obligations, as recorded in REVIEW.md.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from math import comb, isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TARGET = REPO / "probability" / "gaussian_prior_localization"
EXPECTED = HERE / "REVIEW_EXPECTED.json"

PINS = {
    "probability/gaussian_prior_localization/SIGNED_ENDPOINTS.md":
        "e14ecd00fb6bf302a95845792d2282a854e23df8a157e3abaf63e5f955cc4871",
    "probability/gaussian_prior_localization/signed_endpoints.py":
        "1664c27efcf80375c48b9d0acec702e64c819368a3986b3e17ac417eb1a98b99",
    "probability/gaussian_prior_localization/SIGNED_ENDPOINT_EXPECTED.json":
        "ab6428e599d05124b34d9dce8f5b5f390df8daf26bdb5bc08fd4e9e7207dd376",
    "probability/gaussian_prior_localization/CUBATURE_FRONTIER.md":
        "0dbcaf36263ee8ce2976d75d1073db4f878db908fd5c53161e55485c5da53632",
    "probability/gaussian_prior_localization/paired_cubature.py":
        "e533824e8e7260147a27ebe75607e7f4360aded6b23cb6d58080e7632bbe2b00",
    "probability/gaussian_majorisation_open_stability/PROOF.md":
        "ec382eca33145a0a7e487679d5205f31c42f94c290c2f98572c5e4a505b5e39b",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(obj: object) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def fraction(value: object) -> Q:
    if type(value) not in (int, str):
        raise ValueError("exact integer or rational string required")
    return Q(value)


def ceil_log2_integer(n: int) -> int:
    require(type(n) is int and n >= 1, "positive integer logarithm input")
    power, exponent = 1, 0
    while power < n:
        power *= 2
        exponent += 1
    require(power >= n and (exponent == 0 or power // 2 < n), "log bracket")
    return exponent


def ceil_fraction(x: Q) -> int:
    return -((-x.numerator) // x.denominator)


def independent_atom_budget(k: int) -> int:
    require(type(k) is int and k >= 1, "positive integer k")
    ell = ceil_log2_integer(k)
    h = isqrt(ell + 1)
    n = (k + h - 1) // h
    unweighted = k**3 * (2 * comb(2 * ell + 6, 3) - 1)
    weighted = n**3 * (2 * comb(4 * ell + 11, 3) - 1)
    return min(unweighted, weighted)


def independent_family(k: int) -> dict[str, object]:
    atoms = independent_atom_budget(k)
    weight_denominator = 4 * k * atoms
    log_bound = ceil_log2_integer(weight_denominator)
    pair_loss = Q(1, 256 * k**4)
    delta = pair_loss / (8 * 6 * k)
    radius = 3 * k
    tail_B = 6 * radius**2 + 2 * log_bound
    tail_radius = 4 * tail_B / delta
    require(tail_radius.denominator == 1, "integral uniform tail radius")
    tail_radius = tail_radius.numerator
    exponent = tail_radius**2
    peak = 1 - Q(1, weight_denominator**2 * (1024 * k**4 + 1))
    return {
        "status": "SIGNED_ENDPOINTS_ONLY",
        "scope": "every member of R^c_k with at least two positive weights",
        "k": k,
        "atoms": atoms,
        "coordinate_denominator": 256 * k**3,
        "weight_denominator": weight_denominator,
        "support_radius": radius,
        "minimum_squared_pair_loss": str(pair_loss),
        "minimum_positive_weight": str(Q(1, weight_denominator)),
        "log_inverse_weight_upper": log_bound,
        "mean_support_gap_lower": str(delta),
        "tail_B_upper": tail_B,
        "tail_radius_upper": str(tail_radius),
        "low_endpoint": {"base": 2, "negative_exponent": exponent},
        "relative_log_radius_upper": 2 * tail_radius,
        "low_adverse_relative_upper": str(-6 * delta * (exponent + 2)),
        "source_peak_upper": str(peak),
        "point_branch": "all thresholds have equal hinges",
        "middle_interval": "[low_endpoint,source_peak_upper] remains unsigned",
    }


def vector_sub(a: tuple[Q, ...], b: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(x - y for x, y in zip(a, b))


def squared_norm(a: tuple[Q, ...]) -> Q:
    return sum((x * x for x in a), Q(0))


def l1_norm(a: tuple[Q, ...]) -> Q:
    return sum((abs(x) for x in a), Q(0))


def independent_instance(obj: dict[str, object]) -> dict[str, object]:
    if set(obj) - {"source", "target", "weights", "variance"}:
        raise ValueError("unknown field")
    if fraction(obj.get("variance", 1)) != 1:
        raise ValueError("variance one required")
    try:
        xs = [tuple(fraction(a) for a in row) for row in obj["source"]]
        ys = [tuple(fraction(a) for a in row) for row in obj["target"]]
        ws = [fraction(w) for w in obj["weights"]]
    except (KeyError, TypeError) as error:
        raise ValueError("malformed instance") from error
    if not (len(xs) == len(ys) == len(ws) > 0):
        raise ValueError("label count")
    if any(len(row) != 3 for row in xs + ys):
        raise ValueError("dimension")
    if any(w < 0 for w in ws) or sum(ws, Q(0)) != 1:
        raise ValueError("probability weights")
    for i, j in combinations(range(len(ws)), 2):
        if squared_norm(vector_sub(ys[i], ys[j])) > squared_norm(vector_sub(xs[i], xs[j])):
            raise ValueError("expansion")

    merged: dict[tuple[tuple[Q, ...], tuple[Q, ...]], Q] = {}
    for x, y, w in zip(xs, ys, ws):
        if w:
            merged[x, y] = merged.get((x, y), Q(0)) + w
    records = sorted((x, y, w) for (x, y), w in merged.items())
    xs = [row[0] for row in records]
    ys = [row[1] for row in records]
    ws = [row[2] for row in records]
    if len(ws) == 1:
        return {"status": "POINT_EQUALITY_ALL_THRESHOLDS", "positive_source_sites": 1}

    pairs = list(combinations(range(len(ws)), 2))
    losses = [
        squared_norm(vector_sub(xs[i], xs[j])) - squared_norm(vector_sub(ys[i], ys[j]))
        for i, j in pairs
    ]
    pair_loss = min(losses)
    if pair_loss <= 0:
        raise ValueError("strict pair loss")

    source_mean = tuple(sum((w * x[t] for w, x in zip(ws, xs)), Q(0)) for t in range(3))
    target_mean = tuple(sum((w * y[t] for w, y in zip(ws, ys)), Q(0)) for t in range(3))
    xs = [vector_sub(x, source_mean) for x in xs]
    ys = [vector_sub(y, target_mean) for y in ys]
    radius = max(l1_norm(row) for row in xs + ys)
    diameter_bound = max(l1_norm(vector_sub(xs[i], xs[j])) for i, j in pairs)
    mass_floor = min(ws)
    delta = pair_loss / (8 * diameter_bound)
    log_bound = ceil_log2_integer(ceil_fraction(1 / mass_floor))
    # The preceding expression equals ceil(log2(1/m)) for all exact m used
    # here; verify its minimality directly, including non-reciprocal m.
    while log_bound and Q(2 ** (log_bound - 1)) >= 1 / mass_floor:
        log_bound -= 1
    while Q(2**log_bound) < 1 / mass_floor:
        log_bound += 1
    tail_B = 6 * radius**2 + 2 * log_bound
    tail_radius = 4 * tail_B / delta
    exponent = ceil_fraction(tail_radius**2)
    peak = 1 - mass_floor**2 * pair_loss / (4 + pair_loss)
    require(0 < peak < 1, "peak range")
    return {
        "status": "SIGNED_ENDPOINTS_ONLY",
        "positive_source_sites": len(ws),
        "support_radius": str(radius),
        "source_diameter_upper": str(diameter_bound),
        "minimum_squared_pair_loss": str(pair_loss),
        "minimum_positive_weight": str(mass_floor),
        "log_inverse_weight_upper": log_bound,
        "mean_support_gap_lower": str(delta),
        "tail_B_upper": str(tail_B),
        "tail_radius_upper": str(tail_radius),
        "low_endpoint": {"base": 2, "negative_exponent": exponent},
        "relative_log_radius_upper": 2 * ceil_fraction(tail_radius),
        "low_adverse_relative_upper": str(-6 * delta * (exponent + 2)),
        "source_peak_upper": str(peak),
        "middle_interval": "[low_endpoint,source_peak_upper] remains unsigned",
    }


def load_target_module():
    spec = importlib.util.spec_from_file_location("signed_endpoints_target", TARGET / "signed_endpoints.py")
    require(spec is not None and spec.loader is not None, "target import specification")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_pins() -> None:
    for name, wanted in PINS.items():
        got = sha256((REPO / name).read_bytes()).hexdigest()
        require(got == wanted, f"changed reviewed input: {name}")


def check_homothety_algebra() -> int:
    # If ell <= a <= d^2, then a-ell <= (1-ell/(2d^2))^2 a.
    # The difference is ell(1-a/d^2)+ell^2 a/(4d^4), termwise nonnegative.
    count = 0
    for d_index in range(1, 33):
        d_squared = Q(d_index, 3)
        for loss_index in range(1, 17):
            loss = d_squared * Q(loss_index, 16)
            lam = 1 - loss / (2 * d_squared)
            require(Q(1, 2) <= lam < 1, "homothety range")
            for pair_index in range(17):
                pair_squared = loss + (d_squared - loss) * Q(pair_index, 16)
                residual = loss * (1 - pair_squared / d_squared) + loss**2 * pair_squared / (4 * d_squared**2)
                require(lam**2 * pair_squared - (pair_squared - loss) == residual >= 0,
                        "homothety identity")
                count += 1
    return count


def check_segment_normalization() -> int:
    # For a centered segment of length d in R^3, normalized mean support is
    # d/4 because E_{S^2}|theta.e|=1/2.
    count = 0
    for d in range(1, 49):
        for numerator in range(32):
            target = Q(d * numerator, 32)
            loss = d * d - target * target
            actual_gap = Q(d, 4) - target / 4
            require(actual_gap >= loss / (8 * d), "segment mean-support lower bound")
            count += 1
    return count


def check_peak_algebra() -> int:
    # exp(-t) <= 1/(1+t) is the sole transcendental input.  These exact
    # checks cover the subsequent v and square-root relaxation.
    count = 0
    for denominator in range(2, 41):
        mass = Q(1, denominator)
        for numerator in range(1, 101):
            loss = Q(numerator, 5)
            v = mass**2 * loss / (4 + loss)
            require(0 < 2 * v <= 1, "square-root domain")
            require((1 - v) ** 2 >= 1 - 2 * v, "square-root relaxation")
            count += 1
    return count


def fixtures() -> list[dict[str, object]]:
    return [
        {
            "source": [[-1, 0, 0], [1, 0, 0]],
            "target": [[0, 0, 0], [0, 0, 0]],
            "weights": ["1/2", "1/2"],
        },
        {
            "source": [[2, 0, 0], [-2, 0, 0], [0, 3, 0], [0, 0, 1]],
            "target": [[2, -1, 3], [0, -1, 3], [1, "1/2", 3], [1, -1, "7/2"]],
            "weights": ["1/10", "1/5", "3/10", "2/5"],
            "variance": 1,
        },
        {
            "source": [[0, 0, 0], [3, 0, 0], [0, 4, 0]],
            "target": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
            "weights": ["2/7", "1/7", "4/7"],
        },
        {
            "source": [[2, 3, 4], [2, 3, 4], [8, 9, 10]],
            "target": [[-1, 5, 0], [-1, 5, 0], [-1, 5, 0]],
            "weights": ["1/3", "2/3", 0],
        },
    ]


def rejected_fixtures() -> list[dict[str, object]]:
    return [
        {"source": [[-1, 0, 0], [1, 0, 0]], "target": [[-2, 0, 0], [2, 0, 0]], "weights": ["1/2", "1/2"]},
        {"source": [[-1, 0, 0], [1, 0, 0]], "target": [[-1, 0, 0], [1, 0, 0]], "weights": ["1/2", "1/2"]},
        {"source": [[-1, 0, 0], [1, 0, 0]], "target": [[0, 0, 0], [0, 0, 0]], "weights": [1, 1]},
        {"source": [[-1, 0, 0], [1, 0, 0]], "target": [[0, 0, 0], [0, 0, 0]], "weights": [True, False]},
        {"source": [[-1, 0], [1, 0]], "target": [[0, 0], [0, 0]], "weights": ["1/2", "1/2"]},
        {"source": [[-1, 0, 0], [1, 0, 0]], "target": [[0, 0, 0], [0, 0, 0]], "weights": ["1/2", "1/2"], "variance": 2},
    ]


def run() -> dict[str, object]:
    check_pins()
    target_module = load_target_module()

    ks = list(range(1, 513)) + [997, 1000, 4096, 1_000_000]
    family_records = []
    for k in ks:
        independent = independent_family(k)
        require(independent == target_module.family_budget(k), f"family mismatch at k={k}")
        family_records.append(independent)

        # Verify the rational surrogates used to invoke the analytic lemma.
        radius = Q(3 * k)
        log_bound = independent["log_inverse_weight_upper"]
        delta = Q(independent["mean_support_gap_lower"])
        K_upper = radius**2 + 2 * log_bound
        B_upper = Q(independent["tail_B_upper"])
        tail_radius = Q(independent["tail_radius_upper"])
        require(B_upper == K_upper + 5 * radius**2, "B decomposition")
        require(tail_radius == 4 * B_upper / delta, "Q definition")
        require(tail_radius >= 4 * radius and tail_radius**2 >= 2 * K_upper,
                "low-tail side conditions")
        require(tail_radius >= K_upper / radius and delta <= 2 * radius,
                "remaining low-tail side conditions")
        exponent = independent["low_endpoint"]["negative_exponent"]
        require(exponent == tail_radius**2, "dyadic exponent")
        # ln(2)>1/2 and pi>3 turn the low-tail inequality into this exact
        # rational margin; no floating approximation is involved.
        require(-6 * delta * (exponent + 2) == Q(independent["low_adverse_relative_upper"]),
                "uniform low margin")

    public_expected = json.loads((TARGET / "SIGNED_ENDPOINT_EXPECTED.json").read_text())
    expected_by_k = {row["k"]: row for row in public_expected["family_certificates"]}
    for k in (1, 4, 64, 1000):
        require(independent_family(k) == expected_by_k[k], f"public record mismatch at k={k}")

    instance_records = []
    for fixture in fixtures():
        independent = independent_instance(fixture)
        require(independent == target_module.certify_instance(fixture), "instance mismatch")
        instance_records.append(independent)

    for fixture in rejected_fixtures():
        for implementation in (independent_instance, target_module.certify_instance):
            try:
                implementation(fixture)
            except (AssertionError, KeyError, TypeError, ValueError, ZeroDivisionError):
                pass
            else:
                raise AssertionError("malformed or ineligible fixture accepted")

    return {
        "status": "INDEPENDENT_SIGNED_ENDPOINTS_REVIEW_PASS",
        "reviewed_commit": "7bec0b3ac781fcc74a3d003a1e4d9fca2335c2b1",
        "source_pins": len(PINS),
        "homothety_identity_cases": check_homothety_algebra(),
        "segment_normalization_cases": check_segment_normalization(),
        "peak_relaxation_cases": check_peak_algebra(),
        "family_certificates_rebuilt": len(ks),
        "family_digest": digest(family_records),
        "public_family_records_matched": 4,
        "instance_certificates_rebuilt": len(instance_records),
        "instance_digest": digest(instance_records),
        "rejected_instances": len(rejected_fixtures()),
        "analytic_boundary": [
            "classical mean-width monotonicity",
            "R8 written low-threshold lemma",
            "elementary exp(-t)<=1/(1+t)",
        ],
        "scope": "endpoint ranges only; the middle interval and full frontier remain open",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = run()
    if args.check:
        wanted = json.loads(EXPECTED.read_text())
        require(result == wanted, "independent review record changed")
        print(result["status"])
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
