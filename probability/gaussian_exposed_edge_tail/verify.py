#!/usr/bin/env python3
"""Exact supplied-certificate checks; no hull solver or numerical integration.

The universal inequalities are proved in PROOF.md, not inferred by this code.
CPython >=3.11; standard library only. All coordinates and budgets are rational.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from fractions import Fraction as F
import hashlib
import itertools
import json
from math import factorial, lcm
from pathlib import Path


@dataclass(frozen=True)
class Certificate:
    name: str
    x: tuple[tuple[F, ...], ...]
    y: tuple[tuple[F, ...], ...]
    weights: tuple[F, ...]
    radius: F
    variance: F
    pair: tuple[int, int]
    normal: tuple[F, ...]
    eta: F


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def dot(a: tuple[F, ...], b: tuple[F, ...]) -> F:
    require(len(a) == len(b), "dimension mismatch")
    return sum((u * v for u, v in zip(a, b)), F(0))


def sub(a: tuple[F, ...], b: tuple[F, ...]) -> tuple[F, ...]:
    require(len(a) == len(b), "dimension mismatch")
    return tuple(u - v for u, v in zip(a, b))


def norm2(a: tuple[F, ...]) -> F:
    return dot(a, a)


def on_segment(w: tuple[F, ...], a: tuple[F, ...], b: tuple[F, ...]) -> bool:
    direction = sub(b, a)
    delta = sub(w, a)
    pivots = [k for k, value in enumerate(direction) if value]
    if not pivots:
        return w == a
    k = pivots[0]
    t = delta[k] / direction[k]
    return 0 <= t <= 1 and all(v == t * u for v, u in zip(delta, direction))


def ceil_fraction(q: F) -> int:
    return -(-q.numerator // q.denominator)


def mass_log_budget(m: F) -> int:
    """ceil(log2(1/m)) using integers; no floating-point logarithm."""
    require(0 < m <= 1, "invalid mass floor")
    q = 1 / m
    ell = max(0, q.numerator.bit_length() - q.denominator.bit_length())
    if q.denominator * (1 << ell) < q.numerator:
        ell += 1
    require(q.denominator * (1 << ell) >= q.numerator, "log budget too small")
    require(ell == 0 or q.denominator * (1 << (ell - 1)) < q.numerator,
            "log budget not minimal")
    return ell


def endpoints(delta: F, radius: F, variance: F, mass: F, source_d2: F) -> dict:
    require(delta > 0 and radius > 0 and variance > 0, "nonpositive endpoint data")
    ell = mass_log_budget(mass)
    big_b = 6 * radius**2 + 2 * variance * ell
    big_q = 4 * big_b / delta
    exponent = ceil_fraction(big_q**2 / variance)
    upper = 1 - mass * source_d2 / (8 * variance + source_d2)
    require(exponent > 0 and 0 < upper < 1, "invalid endpoint window")
    return {
        "ell": ell,
        "B0": str(big_b),
        "Q": str(big_q),
        "dyadic_tail_exponent": str(exponent),
        "exponent_bit_length": exponent.bit_length(),
        "upper_window": str(upper),
    }


def check_certificate(c: Certificate) -> dict:
    n = len(c.x)
    require(n >= 2 and len(c.y) == n and len(c.weights) == n, "label count mismatch")
    require(all(len(p) == 3 for p in c.x + c.y), "endpoint must be in R3")
    require(len(c.normal) == 6, "normal must be in R6")
    rationals = [v for p in c.x + c.y for v in p]
    rationals += list(c.normal) + list(c.weights) + [c.radius, c.variance, c.eta]
    require(all(isinstance(v, F) for v in rationals), "non-rational input")
    require(c.radius > 0 and c.variance > 0, "invalid radius or variance")
    require(all(v > 0 for v in c.weights) and sum(c.weights) == 1,
            "weights must form a positive probability vector")
    require(all(norm2(p) <= c.radius**2 for p in c.x + c.y), "support radius violated")
    i, j = c.pair
    require(0 <= i < n and 0 <= j < n and i != j, "invalid selected pair")
    losses = {}
    for a, b in itertools.combinations(range(n), 2):
        value = norm2(sub(c.x[a], c.x[b])) - norm2(sub(c.y[a], c.y[b]))
        require(value >= 0, "map is not a contraction")
        losses[a, b] = value
    d = losses[tuple(sorted((i, j)))]
    require(d > 0, "selected edge is not strictly shortened")
    require(sum(abs(v) for v in c.normal) <= 1, "normal L1 bound violated")
    require(0 < c.eta <= c.radius, "invalid exposing margin")
    paired = tuple(x + y for x, y in zip(c.x, c.y))
    require(dot(c.normal, sub(paired[i], paired[j])) == 0, "edge is not exposed equally")
    segment, off_segment_gaps = [], {}
    for k, w in enumerate(paired):
        if on_segment(w, paired[i], paired[j]):
            segment.append(k)
        else:
            gap = dot(c.normal, sub(paired[i], w))
            require(gap >= c.eta, "off-segment gap violated")
            off_segment_gaps[str(k)] = str(gap)
    delta = d * c.eta**5 / (2**40 * n**2 * c.radius**6)
    source_d2 = norm2(sub(c.x[i], c.x[j]))
    explicit_window = endpoints(delta, c.radius, c.variance, min(c.weights), source_d2)

    # Input-size bound: its validity is the proof's polytope/Cramer argument.
    # Here compute its parameters and compare the two algebraic expressions.
    denominator = lcm(*(v.denominator for p in paired for v in p))
    integers = [denominator * v for p in paired for v in p]
    require(all(v.denominator == 1 for v in integers), "denominator reconstruction failed")
    size = max(abs(v.numerator) for v in integers)
    require(size >= 1, "noncongruent map has zero input size")
    uniform_radius = max(F(1), c.radius)
    eta0 = F(1, 6 * denominator * factorial(7) * (2 * size)**6)
    delta0 = F(1, 2**40 * n**2 * denominator**7 *
               (6 * factorial(7))**5 * (2 * size)**30) / uniform_radius**6
    require(delta0 == F(1, denominator**2) * eta0**5 /
            (2**40 * n**2 * uniform_radius**6), "input-size formula mismatch")
    uniform_window = endpoints(delta0, uniform_radius, c.variance, min(c.weights), source_d2)
    return {
        "name": c.name,
        "x": [[str(v) for v in p] for p in c.x],
        "y": [[str(v) for v in p] for p in c.y],
        "weights": [str(v) for v in c.weights],
        "radius": str(c.radius), "variance": str(c.variance),
        "pair": list(c.pair), "normal": [str(v) for v in c.normal], "eta": str(c.eta),
        "normal_l1": str(sum(abs(v) for v in c.normal)),
        "pair_source_distance_squared": str(source_d2),
        "pair_target_distance_squared": str(source_d2 - d),
        "pair_loss": str(d),
        "tight_pairs": sum(v == 0 for v in losses.values()),
        "strict_pairs": sum(v > 0 for v in losses.values()),
        "segment_labels": segment,
        "off_segment_gaps": off_segment_gaps,
        "mean_support_lower_bound": str(delta),
        "certificate_endpoints": explicit_window,
        "input_size_bound": {
            "D": denominator, "M": size, "radius": str(uniform_radius),
            "eta0": str(eta0), "mean_support_lower_bound": str(delta0),
            "endpoints": uniform_window,
        },
    }


def fixtures() -> list[Certificate]:
    # Already published positive indecomposable control; no new map family.
    p = tuple(tuple(map(F, row)) for row in [
        (0, 0, 0), (-1, -1, 0), (-1, 0, 1), (0, -1, 1),
        (1, -2, 5), (-2, -5, -1), (-5, 1, 2)])
    normals = ((1, 1, 1), (1, -1, -1), (-1, 1, -1))
    q = p[:4] + tuple(tuple(v - F(8, 3) * u for v, u in zip(row, normal))
                     for row, normal in zip(p[4:], normals))
    normal = tuple(map(F, ["-1/4", "-1/22", "7/44", "3/44", "-3/22", "-15/44"]))
    base = Certificate("published_seven_site_positive_control", p, q, (F(1, 7),) * 7,
                       F(6), F(1), (1, 4), normal, F(4, 11))
    scaled = replace(base, name="same_control_scaled_by_one_half",
                     x=tuple(tuple(v / 2 for v in row) for row in p),
                     y=tuple(tuple(v / 2 for v in row) for row in q),
                     radius=F(3), variance=F(1, 4), eta=F(2, 11))
    line = tuple(tuple(map(F, row)) for row in [(-1, 0, 0), (1, 0, 0), (0, 0, 0)])
    segment = Certificate("segment_interior_label_collapsed_target", line,
                          ((F(0),) * 3,) * 3, (F(1, 3),) * 3,
                          F(1), F(1), (0, 1), (F(0),) * 6, F(1))
    return [base, scaled, segment]


def evidence() -> dict:
    supplied = fixtures()
    records = [check_certificate(c) for c in supplied]
    base, scaled, segment = records
    require(base["tight_pairs"] == 15 and base["strict_pairs"] == 6, "old pair counts changed")
    require(F(base["mean_support_lower_bound"]) == F(1, 37062793887769165824),
            "independently simplified seven-site margin disagrees")
    require(base["certificate_endpoints"]["dyadic_tail_exponent"] ==
            "1083184010300377825938618225621159364414930944", "seven-site exponent disagrees")
    require(F(scaled["mean_support_lower_bound"]) == F(base["mean_support_lower_bound"]) / 2,
            "mean-width scaling failed")
    for key in ("dyadic_tail_exponent", "upper_window"):
        require(base["certificate_endpoints"][key] == scaled["certificate_endpoints"][key],
                "variance-adjusted endpoint scaling failed")
    require(segment["segment_labels"] == [0, 1, 2] and not segment["off_segment_gaps"],
            "segment-interior control failed")
    require(F(segment["mean_support_lower_bound"]) == F(1, 9 * 2**38),
            "segment margin disagrees")
    c = supplied[0]
    broken_y = list(c.y)
    broken_y[0] = (F(100), F(0), F(0))
    damaged = [
        ("tight_selected_pair", replace(c, pair=(0, 1)), "selected edge is not strictly shortened"),
        ("reversed_normal", replace(c, normal=tuple(-v for v in c.normal)), "off-segment gap violated"),
        ("inflated_margin", replace(c, eta=F(1)), "off-segment gap violated"),
        ("wrong_edge_normal", replace(c, normal=(F(1),) + (F(0),) * 5), "edge is not exposed equally"),
        ("unnormalized_normal", replace(c, normal=tuple(2 * v for v in c.normal)), "normal L1 bound violated"),
        ("noncontraction", replace(c, y=tuple(broken_y), radius=F(101)), "map is not a contraction"),
        ("zero_mass", replace(c, weights=(F(0),) + (F(1, 6),) * 6),
         "weights must form a positive probability vector"),
        ("insufficient_radius", replace(c, radius=F(1)), "support radius violated"),
    ]
    rejected = []
    for name, bad, expected_message in damaged:
        try:
            check_certificate(bad)
        except ValueError as exc:
            require(str(exc) == expected_message, "wrong rejection for " + name + ": " + str(exc))
            rejected.append({"name": name, "reason": str(exc)})
        else:
            raise ValueError("malformed certificate was accepted: " + name)
    return {
        "status": "EXPOSED_EDGE_TAIL_CERTIFICATES_PASS",
        "scope": "Exact finite controls only; universal author proof is in PROOF.md.",
        "certificates": records,
        "scaling_control": "margin scales by 1/2; variance-adjusted cutoff exponent and peak bound unchanged",
        "damaged_certificates_rejected": rejected,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--record", action="store_true")
    modes.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = evidence()
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    path = Path(__file__).with_name("EXPECTED.json")
    if args.record:
        path.write_text(serialized, encoding="utf-8")
    else:
        require(path.read_text(encoding="utf-8") == serialized, "EXPECTED.json mismatch")
    print(result["status"])
    print("3 supplied controls; 8 malformed certificates rejected; no Gaussian integration")
    print("EXPECTED.json sha256=" + hashlib.sha256(serialized.encode()).hexdigest())


if __name__ == "__main__":
    main()
