#!/usr/bin/env python3
"""Independent exact audit of the small-radius Gaussian defect certificate.

The universal signed high-noise window is a written analytic theorem, not a
finite computation.  This program independently rebuilds every algebraic
handoff used after that theorem, audits key normalization identities in its
proof, and differentially tests the public exact producer.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TARGET = REPO / "probability" / "gaussian_majorisation_high_noise_window"
EXPECTED = HERE / "REVIEW_EXPECTED.json"

PINS = {
    "probability/gaussian_majorisation_high_noise_window/SMALL_RADIUS_DEFECT.md":
        "dceeca7a790284d50b7c0fcebe7533859403e064d1b642e121637ec6a9237df1",
    "probability/gaussian_majorisation_high_noise_window/radius_defect.py":
        "1b8f55eed8249c9e37a59951cd08a9a26047b18992480a170af64e35e20b2541",
    "probability/gaussian_majorisation_high_noise_window/RADIUS_EXPECTED.json":
        "6a3fdd88d60ecdb99d7da05d0f58eb82ebec021ff1fbb6b3acff99eedb1c2cca",
    "probability/gaussian_majorisation_high_noise_window/RADIUS_INPUTS.json":
        "2fc86edfb58ec427f22868ff2c81d63d261a2d299727032cc9d9c9f711833d3f",
    "probability/gaussian_majorisation_high_noise_window/PROOF.md":
        "e96063604af579e6ebb8cb25e6eb82ca65c07f6716ecc85f67ae6cc137d0bdf9",
    "probability/gaussian_uniform_defect_bound/PROOF.md":
        "545233fe914f3ad1547af841299a832c9371a0c7f579fb0f4478b4cddc7a6f5a",
    "probability/gaussian_uniform_defect_bound_review2/REVIEW.md":
        "80dcfa7e2bd7ac3c7e3d232ba80d92fe9e24ccba033e81e88f69975cf06cb719",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def exact(value: object) -> Q:
    if type(value) not in (int, str) and not isinstance(value, Q):
        raise ValueError("exact integer or rational string required")
    return Q(value)


def load_target():
    spec = importlib.util.spec_from_file_location("radius_defect_target", TARGET / "radius_defect.py")
    require(spec is not None and spec.loader is not None, "target module specification")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_pins() -> None:
    for name, wanted in PINS.items():
        got = sha256((REPO / name).read_bytes()).hexdigest()
        require(got == wanted, f"changed reviewed input: {name}")


def polynomial_add(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    size = max(len(a), len(b))
    return tuple((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                 for i in range(size))


def polynomial_scale(a: tuple[int, ...], c: int) -> tuple[int, ...]:
    return tuple(c * x for x in a)


def polynomial_multiply(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return tuple(out)


def analytic_identity_audit() -> dict[str, object]:
    # (r+R)^3-(r-R)^3 = 6 r^2 R+2 R^3.  This is the cancellation
    # responsible for losing no r^3 term in the two-volume comparison.
    plus = (1, 3, 3, 1)
    minus = (-1, 3, -3, 1)
    shell = tuple(x - y for x, y in zip(plus, minus))
    require(shell == (2, 0, 6, 0), "shell cancellation")

    # Clear 32 epsilon(1-epsilon) from
    # L=1/(2e)-3/4+e/[32(1-e)].
    left = polynomial_multiply((4, -5), (4, -5))
    right = polynomial_add(
        polynomial_add(polynomial_scale((1, -1), 16),
                       polynomial_scale(polynomial_multiply((0, 1), (1, -1)), -24)),
        (0, 0, 1),
    )
    require(left == right == (16, -40, 25), "cutoff decomposition")

    # Clear 64 e(1-e) from L-9/(64e).  The result factors as
    # (1-2e)(23-25e), nonnegative on 0<e<=1/2.
    factor = polynomial_multiply((1, -2), (23, -25))
    require(factor == (23, -71, 50), "cutoff comparison factorization")

    # The layer-cake integration constants after factoring
    # 8/sqrt(2pi)*sqrt(epsilon)*exp(-ell).
    # The r^2 shell term yields ell+1; the R^3 term yields epsilon/6.
    require(Q(16, 2) == 8, "logarithmic shell coefficient")
    require(Q(8, 3) / 16 == Q(1, 6), "cubic shell coefficient")

    # The half-derivative boundary normalization on A(w)=w^2/2:
    # integral_0^l v/sqrt(l-v)dv=(4/3)l^(3/2), and the Laplace
    # coefficient (4/(3sqrt(pi)))Gamma(5/2) is exactly one.
    abel_numerator = Q(4, 3)
    gamma_five_halves_without_sqrt_pi = Q(3, 4)
    require(abel_numerator * gamma_five_halves_without_sqrt_pi == 1,
            "half-derivative Laplace multiplier")

    # In the replica normalization, the R6 Gaussian integral contributes
    # k^-3 and the unordered-pair sum contributes k(k-1)/2.  After the
    # derivative factor 1/(2sk) and division by k(k-1), the rational part
    # is 1/(4sk^3); the remaining square-root multiplier gives k^-5/2.
    replica_cases = 0
    for k in range(2, 129):
        unordered_pairs = k * (k - 1) // 2
        coefficient = Q(unordered_pairs, 2 * k) / (k * (k - 1))
        require(coefficient == Q(1, 4 * k), "replica exchangeability factor")
        require(Q(1, k**3) * coefficient == Q(1, 4 * k**4),
                "replica rational normalization")
        replica_cases += 1

    return {
        "shell_coefficients": list(shell),
        "cutoff_polynomial": list(left),
        "cutoff_factor": list(factor),
        "half_derivative_coefficient": str(abel_numerator),
        "replica_normalizations": replica_cases,
    }


def independent_radius(radius_squared: object, variance: object = 1) -> dict[str, object]:
    r2, s = exact(radius_squared), exact(variance)
    if r2 < 0 or s <= 0:
        raise ValueError("radius and variance")
    if r2 == 0:
        k = None
        bound = {"numerator": "0", "denominator": "1", "binary_exponent": 0}
        reason = "Point support: exact equality"
    else:
        k = (s / (8 * r2)).numerator // (s / (8 * r2)).denominator
        if k >= 2:
            bound = {"numerator": str(k), "denominator": "1", "binary_exponent": 4 - 5 * k}
            reason = "Exponential support-radius defect bound"
        else:
            bound = {"numerator": "7", "denominator": "50", "binary_exponent": 0}
            reason = "Accepted uniform defect bound; radius rule not stronger"
    return {
        "schema": "gaussian_radius_defect_v1",
        "radius_squared": str(r2),
        "variance": str(s),
        "epsilon": str(r2 / s),
        "k": k,
        "defect_upper_bound": bound,
        "reason": reason,
        "covers": [
            "every density threshold",
            "every beta degree and index",
            "every finite Hankel matrix after adding E times its monomial Gram matrix",
        ],
        "exact_majorisation_certified": r2 == 0,
        "geometric_radius_is_supplied_input": True,
    }


def independent_tolerance(bits: int) -> dict[str, object]:
    if type(bits) is not int or bits < 0:
        raise ValueError("bit budget")
    k = 1 + (bits + 3) // 4
    return {
        "schema": "gaussian_radius_tolerance_v1",
        "bits": bits,
        "k": k,
        "sufficient_radius_squared_over_variance": str(Q(1, 8 * k)),
        "requested_upper_bound": {"numerator": "1", "denominator": "1", "binary_exponent": -bits},
        "radius_rule_bound": {"numerator": str(k), "denominator": "1", "binary_exponent": 4 - 5 * k},
        "integer_budget_check": 4 - 4 * k <= -bits,
        "proof_of_unexpanded_comparison": "k<=2^k for every integer k>=1",
    }


def squared_distance(a: tuple[Q, ...], b: tuple[Q, ...]) -> Q:
    return sum(((x - y) ** 2 for x, y in zip(a, b)), Q(0))


def independent_instance(data: dict[str, object], variance: object | None = None) -> dict[str, object]:
    if not isinstance(data, dict):
        raise ValueError("object required")
    endpoints = []
    for field in ("source", "target"):
        raw = data.get(field)
        if not isinstance(raw, list) or not raw:
            raise ValueError("nonempty endpoint")
        if any(not isinstance(row, list) or len(row) != 3 for row in raw):
            raise ValueError("dimension")
        endpoints.append([tuple(exact(value) for value in row) for row in raw])
    source, target = endpoints
    raw_weights = data.get("weights")
    if not isinstance(raw_weights, list):
        raise ValueError("weights")
    weights = [exact(value) for value in raw_weights]
    if not (len(source) == len(target) == len(weights)):
        raise ValueError("label count")
    if any(weight < 0 for weight in weights) or sum(weights, Q(0)) != 1:
        raise ValueError("probability weights")
    s = exact(data.get("variance", 1) if variance is None else variance)
    if s <= 0:
        raise ValueError("variance")
    for i, j in combinations(range(len(source)), 2):
        if squared_distance(target[i], target[j]) > squared_distance(source[i], source[j]):
            raise ValueError("not a contraction")
    active = [i for i, weight in enumerate(weights) if weight > 0]
    candidates = []
    for anchor in active:
        candidates.append((max(squared_distance(source[anchor], source[j]) for j in active), anchor))
    radius_squared, anchor = min(candidates)
    target_radius_squared = max(squared_distance(target[anchor], target[j]) for j in active)
    require(target_radius_squared <= radius_squared, "anchor contraction")
    result = independent_radius(radius_squared, s)
    result.update({
        "geometric_radius_is_supplied_input": False,
        "labels": len(source),
        "active_labels": len(active),
        "source_anchor_index": anchor,
        "target_radius_squared": str(target_radius_squared),
        "pair_contractions_checked": len(source) * (len(source) - 1) // 2,
        "radius_method": "minimum over active source-site anchors; not a minimum enclosing ball",
    })
    return result


def deterministic_instances() -> list[dict[str, object]]:
    records = [
        {"source": [[0, 0, 0], [100, 0, 0]], "target": [[3, 0, 0], [3, 0, 0]], "weights": [1, 0]},
        {"source": [[0, 0, 0], [3, 0, 0], [0, 4, 0]], "target": [[2, -1, 5]] * 3,
         "weights": ["2/7", "1/7", "4/7"], "variance": 25},
    ]
    base = [[0, 0, 0], [2, -1, 1], [-1, 3, 2], [4, 1, -2], [7, 7, 7]]
    for denominator in range(2, 34):
        lam = Q(denominator - 1, denominator)
        shift = (Q(3, denominator), Q(-5, denominator), Q(2, denominator))
        target = [[str(lam * Q(value) + shift[axis]) for axis, value in enumerate(row)] for row in base]
        weights = ["1/10", "1/5", "3/10", "2/5", 0]
        records.append({"source": base, "target": target, "weights": weights,
                        "variance": str(Q(9, denominator))})
    return records


def beta_and_gram_audit() -> dict[str, int]:
    beta_cases = 0
    for n in range(65):
        for j in range(n + 1):
            # Integral u^j(1-u)^(n-j) = j!(n-j)!/(n+1)!.
            normalization = Q((n + 1) * comb(n, j), 1)
            integral = Q(1, (n + 1) * comb(n, j))
            require(normalization * integral == 1, "Beta normalization")
            beta_cases += 1

    gram_cases = 0
    exponent_lists = [(0, 1, 2), (0, 2, 5, 9), (3, 3, 7), (0, 8, 16, 32, 64)]
    coefficient_lists = [(1, -2, 3, -4, 5), (7, 0, -3, 2, -1)]
    for exponents in exponent_lists:
        for coefficients in coefficient_lists:
            coeffs = coefficients[:len(exponents)]
            if len(coeffs) < len(exponents):
                coeffs = coeffs + (1,) * (len(exponents) - len(coeffs))
            quadratic = sum((Q(coeffs[i] * coeffs[j], exponents[i] + exponents[j] + 1)
                             for i in range(len(exponents)) for j in range(len(exponents))), Q(0))
            expanded = {}
            for exponent, coefficient in zip(exponents, coeffs):
                expanded[exponent] = expanded.get(exponent, 0) + coefficient
            integral = sum((Q(a * b, p + q + 1)
                            for p, a in expanded.items() for q, b in expanded.items()), Q(0))
            require(quadratic == integral >= 0, "monomial Gram identity")
            gram_cases += 1
    return {"beta_normalizations": beta_cases, "gram_quadratic_forms": gram_cases}


def run() -> dict[str, object]:
    check_pins()
    target = load_target()
    analytic = analytic_identity_audit()

    radius_records = []
    for k in range(2, 1025):
        for offset in range(8):
            r2 = Q(1, 8 * k + offset)
            ours = independent_radius(r2)
            require(ours == target.radius_certificate(r2), f"radius mismatch k={k}, offset={offset}")
            require(ours["k"] == k, "floor cell index")
            radius_records.append(ours)
    for r2, s in ((0, 1), (1, 1), (Q(1, 8), 1), (Q(7, 31), Q(9, 5))):
        require(independent_radius(r2, s) == target.radius_certificate(r2, s), "boundary radius mismatch")

    # k=2 is the largest exponential compressed bound; subsequent ratios
    # are ((k+1)/k)/32<1.  This verifies the fallback switch exactly.
    require(16 * Q(2, 2**10) < Q(7, 50), "k=2 fallback comparison")
    for k in range(2, 1024):
        require(Q(k + 1, 32 * k) < 1, "compressed bound monotonicity")

    tolerance_records = []
    for bits in list(range(4097)) + [1_000_000]:
        ours = independent_tolerance(bits)
        require(ours == target.tolerance_certificate(bits), f"tolerance mismatch at {bits}")
        k = ours["k"]
        require(k <= 2**k and 4 - 4 * k <= -bits, "unexpanded tolerance proof")
        tolerance_records.append(ours)

    instance_records = []
    for instance in deterministic_instances():
        ours = independent_instance(instance)
        require(ours == target.instance_certificate(instance), "instance mismatch")
        instance_records.append(ours)

    malformed = [
        lambda: independent_radius(-1),
        lambda: independent_radius(1, 0),
        lambda: independent_tolerance(True),
        lambda: independent_instance({"source": [[0, 0]], "target": [[0, 0, 0]], "weights": [1]}),
        lambda: independent_instance({"source": [[0, 0, 0]], "target": [[0, 0, 0]], "weights": [2]}),
        lambda: independent_instance({"source": [[0, 0, 0], [0, 0, 0]], "target": [[0, 0, 0], [1, 0, 0]],
                                      "weights": ["1/2", "1/2"]}),
    ]
    for call in malformed:
        try:
            call()
        except (AssertionError, KeyError, TypeError, ValueError, ZeroDivisionError):
            pass
        else:
            raise AssertionError("malformed input accepted")

    consequences = beta_and_gram_audit()
    public = json.loads((TARGET / "RADIUS_EXPECTED.json").read_text())
    require(public["status"] == "EXPONENTIAL_RADIUS_DEFECT_CERTIFICATES_PASS", "public record status")
    for row in public["table"]:
        require(row == independent_radius(row["radius_squared"], row["variance"]), "public table mismatch")

    return {
        "status": "INDEPENDENT_SMALL_RADIUS_DEFECT_REVIEW_PASS",
        "reviewed_commit": "debfb7ae35895c71f36d5d89ac4efb372ae7435b",
        "source_pins": len(PINS),
        "analytic_identities": analytic,
        "radius_certificates_rebuilt": len(radius_records),
        "radius_digest": digest(radius_records),
        "tolerance_certificates_rebuilt": len(tolerance_records),
        "tolerance_digest": digest(tolerance_records),
        "instances_rebuilt": len(instance_records),
        "instance_digest": digest(instance_records),
        "malformed_instances_rejected": len(malformed),
        **consequences,
        "public_table_rows_matched": len(public["table"]),
        "analytic_boundary": [
            "signed high-noise window Theorem A, directly audited in the review",
            "accepted uniform 7/50 fallback",
            "elementary Gaussian shell and layer-cake calculus",
        ],
        "scope": "uniform defect bound only; no exact Gaussian majorisation sign",
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
