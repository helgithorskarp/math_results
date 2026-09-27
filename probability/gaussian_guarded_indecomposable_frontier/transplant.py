#!/usr/bin/env python3
"""Exact finite geometry for PROOF.md Section 3; no Gaussian sign oracle."""
import json
import sys
from fractions import Fraction as F

VERTICES = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rational(value):
    require(type(value) in (int, str), "rational entries must be integers or strings")
    return F(value)


def points(value):
    require(isinstance(value, list) and value, "nonempty point list required")
    out = []
    for row in value:
        require(isinstance(row, list) and len(row) == 3, "three coordinates required")
        out.append(tuple(rational(x) for x in row))
    return out


def dist2(x, y):
    return sum((a - b) ** 2 for a, b in zip(x, y))


def make(data):
    require(isinstance(data, dict) and set(data) == {
        "source", "target", "weights", "radius", "budget_bits"
    }, "unexpected input fields")
    p, q = points(data["source"]), points(data["target"])
    require(len(p) == len(q) and len(set(p)) == len(p), "distinct matched source sites required")
    require(isinstance(data["weights"], list), "weight list required")
    w = [rational(x) for x in data["weights"]]
    require(len(w) == len(p) and all(x > 0 for x in w) and sum(w) == 1,
            "strictly positive probability weights required")
    r, k = data["radius"], data["budget_bits"]
    require(type(r) is int and r >= 1 and type(k) is int and k >= 1,
            "positive integer radius and budget_bits required")
    require(all(sum(t*t for t in x) <= r*r for x in p + q), "radius guard failed")
    require(all(dist2(q[i], q[j]) <= dist2(p[i], p[j])
                for i in range(len(p)) for j in range(i)), "input is not a contraction")
    ell = max(4*r, k)
    a = [tuple(F(t, 9) for t in row) for row in VERTICES]
    pp = a + [tuple((x[d] + (8*ell if d == 0 else 0))/(9*ell)
                    for d in range(3)) for x in p]
    qq = a + [tuple((x[d] + (6*ell if d == 0 else 0))/(9*ell)
                    for d in range(3)) for x in q]
    return {
        "status": "GEOMETRY_ONLY_TRANSPLANT",
        "source": [[str(t) for t in x] for x in pp],
        "target": [[str(t) for t in x] for x in qq],
        "weights": [str(x) for x in [F(1, 8)]*4 + [x/2 for x in w]],
        "L": ell,
        "variance": str(F(1, 81*ell*ell)),
        "threshold_multiplier": str(F((9*ell)**3, 2)),
        "support_radius_bound": "1",
        "covariance_floor": "1/162",
        "cross_squared_loss_floor": "14/81",
        "hinge_error_bound": {"base": 2, "exponent": -k},
        "conditional_adverse_input": "Requires an independently established original gap delta >= 4*2^(-budget_bits).",
        "adverse_input_verified": False,
        "indecomposability_verified": False,
        "localization_guards": {"R": 18*ell, "kappa": str(F(ell*ell, 2)), "alignment_factor": 2593},
    }


def main():
    require(len(sys.argv) == 2, "usage: transplant.py INPUT.json")
    with open(sys.argv[1], encoding="utf-8") as stream:
        data = json.load(stream)
    print(json.dumps(make(data), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
