#!/usr/bin/env python3
"""Exact hypotheses and finite algebra; analytic author proof is unformalized."""
from __future__ import annotations

import argparse
import copy
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent


def require(test, message):
    if not test:
        raise ValueError(message)


def rational(x):
    require(type(x) is int or (type(x) is str and
            re.fullmatch(r"[+-]?\d+(?:/[+-]?\d+)?", x) is not None),
            "coordinates and weights must be integer or rational strings")
    return F(x)


def vector(x):
    require(type(x) is list and len(x) == 3, "expected a vector in R3")
    return tuple(map(rational, x))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def distance2(x, y):
    d = sub(x, y)
    return dot(d, d)


def rank(rows):
    a = [list(row) for row in rows]
    if not a:
        return 0
    r = 0
    for j in range(len(a[0])):
        k = next((k for k in range(r, len(a)) if a[k][j]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        pivot = a[r][j]
        a[r] = [v / pivot for v in a[r]]
        for k in range(len(a)):
            if k != r:
                factor = a[k][j]
                a[k] = [v - factor * u for v, u in zip(a[k], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def affine_rank(rows):
    return rank([sub(row, rows[0]) for row in rows[1:]])


def decode(obj):
    require(type(obj) is dict and set(obj) == {
        "source", "target", "source_anchor", "target_anchor", "weights"
    }, "wrong input fields")
    require(type(obj["source"]) is list and type(obj["target"]) is list,
            "site lists required")
    n = len(obj["source"])
    require(n > 0 and len(obj["target"]) == n, "site counts disagree")
    a, b = vector(obj["source_anchor"]), vector(obj["target_anchor"])
    p = [sub(vector(x), a) for x in obj["source"]]
    q = [sub(vector(x), b) for x in obj["target"]]
    require(type(obj["weights"]) is list and len(obj["weights"]) == n,
            "weight count disagrees")
    w = list(map(rational, obj["weights"]))
    require(min(w) >= 0 and sum(w) == 1, "invalid probability weights")
    return p, q, w


def guard(obj):
    p, q, w = decode(obj)
    n = len(p)
    require(all(dot(x, x) == dot(y, y) for x, y in zip(p, q)),
            "anchored norms are unequal: guard unresolved")
    losses = {(i, j): distance2(p[i], p[j]) - distance2(q[i], q[j])
              for i in range(n) for j in range(i + 1, n)}
    require(all(d >= 0 for d in losses.values()), "expanding pair")
    # Compute the same geometric data independently through Gram entries.
    for i in range(n):
        for j in range(n):
            gram = dot(p[i], p[j]) - dot(q[i], q[j])
            loss = distance2(p[i], p[j]) - distance2(q[i], q[j])
            require(2 * gram == -loss, "Gram/distance normalization mismatch")
    return {
        "status": "EXACT_GUARD_ACCEPTS_AUTHOR_THEOREM",
        "sites": n,
        "source_affine_rank": affine_rank(p),
        "target_affine_rank": affine_rank(q),
        "paired_affine_rank": affine_rank([x + y for x, y in zip(p, q)]),
        "unordered_pairs": len(losses),
        "equal_pairs": sum(d == 0 for d in losses.values()),
        "strict_pairs": sum(d > 0 for d in losses.values()),
        "radius_squared": str(max(dot(x, x) for x in p)),
        "mean_ordered_loss": str(2 * sum(w[i] * w[j] * d
                                         for (i, j), d in losses.items())),
        "all_sites_on_unit_sphere_about_anchors": all(dot(x, x) == 1 for x in p),
        "scope": "all s>0 and h>=0, conditional on PROOF.md; no numerical hinge evaluation",
    }


def encode(p, q, w, a=(0, 0, 0), b=(0, 0, 0)):
    return {"source": [[str(z) for z in x] for x in p],
            "target": [[str(z) for z in x] for x in q],
            "source_anchor": list(map(str, a)),
            "target_anchor": list(map(str, b)), "weights": list(map(str, w))}


def rotated(x):
    return (F(3, 5) * x[0] - F(4, 5) * x[1],
            F(4, 5) * x[0] + F(3, 5) * x[1], -x[2])


def hessian_checks(cases):
    checks = 0
    for obj in cases:
        p, q, _ = decode(obj)
        n = len(p)
        k = [[dot(x, y) - dot(q[i], q[j])
              for j, y in enumerate(p)] for i, x in enumerate(p)]
        for a, b in itertools.product([F(-3), F(0), F(5, 7)],
                                      [F(0), F(1, 3), F(2)]):
            v = [F(i + 1, n + 1) for i in range(n)]
            # Hessian of U(sum exp) from directional differentiation.
            h = [[b * v[i] * v[j] + (a * v[i] if i == j else 0)
                  for j in range(n)] for i in range(n)]
            trace = sum(k[i][j] * h[i][j] for i in range(n) for j in range(n))
            pair = sum((distance2(p[i], p[j]) - distance2(q[i], q[j]))
                       * b * v[i] * v[j]
                       for i in range(n) for j in range(i + 1, n))
            require(trace == -pair and pair >= 0, "mixed-Hessian sign failure")
            checks += 1
    return checks


def boolean_checks():
    checks = 0
    for n in range(2, 9):
        full = (1 << n) - 1
        # Expand AND and OR as independent multiaffine polynomials.
        for is_union in [False, True]:
            poly = ({m: F((-1) ** (m.bit_count() + 1))
                     for m in range(1, 1 << n)} if is_union else {full: F(1)})
            for values in [[F(i + 1, n + 1) for i in range(n)],
                           [F(i % 2) for i in range(n)]]:
                for i in range(n):
                    for j in range(i + 1, n):
                        answer = F(0)
                        for mask, coeff in poly.items():
                            if mask & (1 << i) and mask & (1 << j):
                                term = coeff
                                for k in range(n):
                                    if k not in [i, j] and mask & (1 << k):
                                        term *= values[k]
                                answer += term
                        product = F(-1 if is_union else 1)
                        for k in range(n):
                            if k not in [i, j]:
                                product *= (1 - values[k]) if is_union else values[k]
                        require(answer == product, "Boolean mixed derivative mismatch")
                        require(answer <= 0 if is_union else answer >= 0,
                                "Boolean sign mismatch")
                        checks += 1
    return checks


def rejection_checks(base):
    bad = []
    z = copy.deepcopy(base); z["target"][0] = ["0", "0", "0"]
    bad.append(z)  # Loss of anchored norm, irrespective of other guards.
    z = copy.deepcopy(base); z["target"][0] = ["-1", "0", "0"]
    bad.append(z)  # Keeps norms but expands relative to the extra unit vector.
    z = copy.deepcopy(base); z["weights"][0] = "-1/28"; bad.append(z)
    z = copy.deepcopy(base); z["weights"][0] = "1/14"; bad.append(z)
    z = copy.deepcopy(base); z["source"][0].append("0"); bad.append(z)
    z = copy.deepcopy(base); z["source"][0][0] = 1.0; bad.append(z)
    z = copy.deepcopy(base); z["target_anchor"] = ["1", "0", "0"]; bad.append(z)
    z = copy.deepcopy(base); z["target"].pop(); bad.append(z)
    z = copy.deepcopy(base); z["unused"] = 1; bad.append(z)
    for obj in bad:
        try:
            guard(obj)
        except (ValueError, ZeroDivisionError):
            continue
        raise ValueError("invalid input accepted")
    return len(bad)


def run_suite():
    inp = json.loads((HERE / "INPUT.json").read_text())
    p, q, w = decode(inp)
    a, b = (F(2), F(-3), F(4)), (F(-1), F(5), F(-2))
    translated = encode([tuple(xi + ai for xi, ai in zip(x, a)) for x in p],
                        [tuple(yi + bi for yi, bi in zip(rotated(y), b)) for y in q],
                        w, a, b)
    radii = [F(1), F(2), F(3), F(1, 2), F(1, 3), F(5, 4), F(7, 5)]
    scaled = encode([tuple(r * z for z in x) for r, x in zip(radii, p)],
                    [tuple(r * z for z in x) for r, x in zip(radii, q)], w)
    origin = encode([(F(0),) * 3] + p, [(F(0),) * 3] + q,
                    [F(1, 2)] + [v / 2 for v in w])
    congruent = encode(p, [rotated(x) for x in p], w)
    point = encode([(F(0),) * 3], [(F(0),) * 3], [F(1)])
    cases = [inp, translated, scaled, origin, congruent, point]
    names = ["unit_sphere", "independent_isometries", "unequal_radial_scales",
             "fixed_anchor_in_support", "congruent", "single_point"]
    result = {name: guard(obj) for name, obj in zip(names, cases)}
    require(result["unit_sphere"]["paired_affine_rank"] == 6, "rank-six calibration")
    require(result["fixed_anchor_in_support"]["paired_affine_rank"] == 6,
            "rank-six anchored calibration")
    require(result["congruent"]["strict_pairs"] == 0, "congruent boundary")
    require(result["unit_sphere"]["equal_pairs"] > 0, "tight-pair boundary")
    pins = json.loads((HERE / "INPUTS.json").read_text())
    for dependency in pins["files"]:
        data = (HERE / dependency["relative_path"]).read_bytes()
        require(hashlib.sha256(data).hexdigest() == dependency["sha256"],
                "dependency bytes changed")
    record = {"status": "EXACT_NORM_PRESERVING_CHECKS_PASSED", "cases": result,
              "hessian_identities": hessian_checks(cases),
              "boolean_derivative_identities": boolean_checks(),
              "rejected_inputs": rejection_checks(inp),
              "analytic_dependency": pins,
              "trust_boundary": "finite rational algebra only; PROOF.md and R1 Lemma 1 are unformalized author proofs"}
    raw = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    return {"record": record, "record_sha256": hashlib.sha256(raw).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="check supplied rational finite geometry")
    parser.add_argument("--record-only", action="store_true", help="emit suite record without expected-record comparison")
    args = parser.parse_args()
    if args.input:
        require(not args.record_only, "input and record-only modes are distinct")
        output = guard(json.loads(args.input.read_text()))
    else:
        output = run_suite()
        if not args.record_only:
            require(output == json.loads((HERE / "EXPECTED.json").read_text()),
                    "expected record mismatch")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, ZeroDivisionError, KeyError, TypeError) as exc:
        print("CHECK FAILED: " + str(exc), file=sys.stderr)
        sys.exit(2)
