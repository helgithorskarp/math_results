#!/usr/bin/env python3
"""QQ[r] identities and full QQ spectral projections; no search or numerics.

The continuous minimizer/IFT/Hessian argument is in PROOF.md, not certified
by this program. All checks raise exceptions and survive Python -O.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def poly(values):
    out = tuple(F(x) for x in values)
    while len(out) > 1 and out[-1] == 0:
        out = out[:-1]
    return out or (F(0),)


def add(a, b):
    return poly([(a[i] if i < len(a) else 0) +
                 (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def scale(a, c):
    return poly([F(c)*v for v in a])


def mul(a, b):
    out = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return poly(out)


def power(a, n):
    out = poly([1])
    for _ in range(n):
        out = mul(out, a)
    return out


def derivative(a):
    return poly([i*a[i] for i in range(1, len(a))])


def at(a, x):
    out = F(0)
    for c in reversed(a):
        out = out*F(x)+c
    return out


def coefficients(a):
    return [str(c) for c in a]


def identity(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def matrix_add(a, b):
    return [[x+y for x, y in zip(aa, bb)] for aa, bb in zip(a, b)]


def matrix_scale(a, c):
    return [[F(c)*x for x in row] for row in a]


def matrix_mul(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def matrix_vector(a, b):
    return [sum((x*y for x, y in zip(row, b)), F(0)) for row in a]


def matrix_record(a):
    return [[str(x) for x in row] for row in a]


def case_record(n, k, damage=None):
    m = n-1-k
    r = poly([0, 1])
    middle = poly([m, -k])
    cubic = add(add(poly([-m]), power(middle, 3)), scale(power(r, 3), k))
    if damage == "cube_coefficient" and (n, k) == (8, 3):
        cubic = add(cubic, power(r, 3))
    lo, hi = F(m, k+1), F(m+1, k)
    require(lo < hi, "empty ordered-level interval")
    record = {"n": n, "m": m, "k": k,
              "interval": [str(lo), str(hi)],
              "middle": coefficients(middle), "cubic": coefficients(cubic)}
    if k == 1:
        center, factor, remainder = (F(5, 2), 15, F(105, 4)) if n == 7 else (F(3), 18, F(48))
        square = add(scale(power(poly([-center, 1]), 2), factor), poly([remainder]))
        require(cubic == square and remainder > 0 and factor > 0, "positive-square certificate")
        record["certificate"] = {"route": "positive_square", "center": str(center),
                                 "factor": str(factor), "remainder": str(remainder),
                                 "square_identity": coefficients(square)}
    elif k == 2:
        f = poly([-10, 16, -8, 1]) if n == 7 else poly([-20, 25, -10, 1])
        outer = F(4) if n == 7 else F(5)
        factored_derivative = scale(mul(poly([-lo, 1]), poly([-outer, 1])), 3)
        expected_endpoint = F(-14, 27) if n == 7 else F(-40, 27)
        require(cubic == scale(f, -6), "negative-six factor identity")
        require(derivative(f) == factored_derivative, "whole derivative factor identity")
        require(lo < hi < outer, "derivative sign on entire interval")
        require(at(f, lo) == expected_endpoint < 0, "negative starting endpoint")
        record["certificate"] = {"route": "decreasing_negative_cubic",
                                 "factor": coefficients(f),
                                 "derivative": coefficients(derivative(f)),
                                 "outer_derivative_root": str(outer),
                                 "left_value": str(at(f, lo))}
    elif n == 7:
        q = poly([8, -19, 8])
        factored = scale(mul(poly([-1, 1]), q), -3)
        ends = [at(q, lo), at(q, hi)]
        require(cubic == factored and q[2] > 0, "middle-zero factor and convexity")
        require(ends == [F(-7, 4), F(-28, 9)] and max(ends) < 0,
                "negative entire closed quadratic interval")
        require(lo < 1 < hi and at(middle, 1) == 0 and at(cubic, 1) == 0,
                "sole interior root removes middle support")
        record["certificate"] = {"route": "only_zero_middle_root",
                                 "quadratic": coefficients(q),
                                 "quadratic_endpoint_values": [str(x) for x in ends],
                                 "interior_root": "1", "middle_at_root": "0"}
    else:
        factored = scale(mul(power(poly([-1, 1]), 2), poly([-5, 2])), -12)
        require(cubic == factored, "whole endpoint-square factor identity")
        require(lo == 1 and hi < F(5, 2), "strict positivity throughout open interval")
        record["certificate"] = {"route": "positive_endpoint_square",
                                 "double_root": "1", "remaining_factor": ["-5", "2"],
                                 "remaining_factor_at_right": str(2*hi-5)}
    return record


def build_record(damage=None):
    cases = [case_record(n, k, damage) for n in (7, 8) for k in (1, 2, 3)]
    require([(row["n"], row["m"], row["k"]) for row in cases] ==
            [(7, 5, 1), (7, 4, 2), (7, 3, 3), (8, 6, 1), (8, 5, 2), (8, 4, 3)],
            "complete multiplicity classification")
    v = [F(x) for x in (1, 1, 1, -1, -1, -1, 0, 0)]
    if damage == "equality_profile":
        v[-1] = F(1)
    moments = [sum((x**j for x in v), F(0)) for j in range(1, 7)]
    require(moments == [F(0), F(6), F(0), F(6), F(0), F(6)], "equality moments")
    norm = moments[1]
    eye = identity(8)
    p = [[F(i == j)-F(1, 8) for j in range(8)] for i in range(8)]
    diag = [[v[i] if i == j else F(0) for j in range(8)] for i in range(8)]
    h = matrix_mul(matrix_mul(p, diag), p)
    require(matrix_vector(h, [F(1)]*8) == [F(0)]*8, "ambient zero direction")
    nodes = [F(-1), F(-1, 2), F(0), F(1, 2), F(1)]
    if damage == "projector_node":
        nodes[3] = F(2, 3)
    projections, spectral_records = [], []
    char = poly([1])
    for lam in nodes:
        proj = eye
        for other in nodes:
            if other != lam:
                factor = matrix_scale(matrix_add(h, matrix_scale(eye, -other)), F(1)/(lam-other))
                proj = matrix_mul(proj, factor)
        require(matrix_mul(proj, proj) == proj, "whole projector idempotence")
        require(matrix_mul(h, proj) == matrix_scale(proj, lam), "whole projector eigenvalue equation")
        require(proj == [list(row) for row in zip(*proj)], "self-adjoint full projector")
        rank = sum((proj[i][i] for i in range(8)), F(0))
        require(rank.denominator == 1 and rank > 0, "projector rank")
        image = matrix_vector(proj, v)
        mass = sum((x*x for x in image), F(0))
        require(mass == sum((x*y for x, y in zip(v, image)), F(0)), "full projection mass")
        spectral_records.append({"eigenvalue": str(lam), "rank": int(rank),
                                 "matrix": matrix_record(proj), "image": [str(x) for x in image],
                                 "raw_full_mass": str(mass), "normalized_full_mass": str(mass/norm)})
        projections.append(proj)
        char = mul(char, power(poly([-lam, 1]), int(rank)))
    zero = matrix_scale(eye, 0)
    for i, a in enumerate(projections):
        for b in projections[i+1:]:
            require(matrix_mul(a, b) == zero, "whole projector orthogonality")
    total = zero
    for proj in projections:
        total = matrix_add(total, proj)
    require(total == eye, "complete full eigenspace decomposition")
    require([row["rank"] for row in spectral_records] == [2, 1, 2, 1, 2], "all ranks, including ambient zero")
    masses = [F(row["raw_full_mass"]) for row in spectral_records]
    require(masses == [0, 3, 0, 3, 0] and sum(masses) == norm, "all grouped equality masses")
    f = poly([1])
    for x in v:
        f = mul(f, poly([-x, 1]))
    critical = scale(derivative(f), F(1, 8))
    require(char == mul(poly([0, 1]), critical), "full characteristic versus original derivative")
    eta = sum((m*m for m in masses), F(0))/(norm*norm)
    normalized_x = moments[3]/(norm*norm)
    d = normalized_x-F(1, 8)
    c = (1-eta)/d
    require(normalized_x == F(1, 6) and eta == F(1, 2) and d == F(1, 24) and c == 12,
            "actual angular equality control")
    bounds = [{"r": r, "upper": str(F(24*(r-2), r-1))} for r in range(2, 9)]
    require(F(bounds[-1]["upper"]) == F(144, 7) < F(49, 2), "high-value sign restriction")
    return {"cases": cases,
            "small_support": [{"n": n, "cauchy_lower": str(F(1, n))} for n in range(1, 7)],
            "equality": {"profile": [str(x) for x in v], "moments_1_to_6": [str(x) for x in moments],
                         "original_polynomial": coefficients(f), "critical_polynomial": coefficients(critical),
                         "ambient_characteristic": coefficients(char), "ambient_H": matrix_record(h),
                         "full_projectors": spectral_records, "X": str(normalized_x),
                         "eta": str(eta), "D": str(d), "C": str(c)},
            "angular": {"level_bounds": bounds, "strict_universal_upper": "144/7",
                        "gap_to_49_over_2": str(F(49, 2)-F(144, 7))}}


def record_bytes(record):
    return (json.dumps(record, sort_keys=True, indent=2, ensure_ascii=False)+"\n").encode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=Path(__file__).with_name("expected.json"))
    parser.add_argument("--emit-record", type=Path, help="generate a record after all algebra checks; bootstrap only")
    parser.add_argument("--self-test", action="store_true", help="also reject three semantic mathematical damages")
    args = parser.parse_args()
    record = build_record()
    raw = record_bytes(record)
    if args.emit_record:
        args.emit_record.write_bytes(raw)
        print(json.dumps({"status": "record_generated", "bytes": len(raw),
                          "sha256": hashlib.sha256(raw).hexdigest()}))
        return
    require(args.fixture.read_bytes() == raw, "entire canonical fixture differs (content/keys/types/format)")
    rejected = 0
    if args.self_test:
        for damage in ("cube_coefficient", "equality_profile", "projector_node"):
            try:
                build_record(damage)
            except ValueError:
                rejected += 1
            else:
                raise ValueError("semantic mathematical damage accepted: "+damage)
    print(json.dumps({"status": "verified", "complete_cases": 6, "full_projectors": 5,
                      "record_bytes": len(raw), "record_sha256": hashlib.sha256(raw).hexdigest(),
                      "semantic_damages_rejected": rejected}))


if __name__ == "__main__":
    main()
