#!/usr/bin/env python3
"""Exact controls and optional finite-input consumer for PROOF.md.

CPython 3.11+, standard library. This audits arithmetic and premises,
not Gaussian integrals or the continuum proof. No assert-based checks.
"""

from copy import deepcopy
from fractions import Fraction as F
import json
from math import factorial
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rational(value):
    require(type(value) in (int, str), "Use integers or exact rational strings")
    return F(value)


def distance2(x, y):
    return sum((a-b)**2 for a, b in zip(x, y))


def certify(data):
    require(isinstance(data, dict), "Expected a JSON object")
    clouds = []
    for key in ("source", "target"):
        rows = data[key]
        require(isinstance(rows, list) and rows, "Need a nonempty site list")
        require(all(isinstance(row, list) and len(row) == 3 for row in rows),
                "Sites must be three-dimensional lists")
        clouds.append([tuple(rational(v) for v in row) for row in rows])
    x, y = clouds
    require(len(x) == len(y), "Endpoint sizes differ")
    n = len(x)
    weights = data["weights"]
    require(isinstance(weights, list), "Weights must be a list")
    w = [rational(v) for v in weights]
    require(len(w) == n and all(v > 0 for v in w) and sum(w) == 1,
            "Weights must be positive and sum to one")
    s, ell = rational(data["variance"]), rational(data["log_threshold"])
    require(s > 0 and ell >= 0, "Invalid variance or logarithmic threshold")
    positive_distances, loss = [], F(0)
    for i in range(n):
        for j in range(i):
            dx, dy = distance2(x[i], x[j]), distance2(y[i], y[j])
            require(dx > 0, "Combine repeated source sites first")
            require(dy <= dx, "Input is not a contraction")
            positive_distances.append(dx)
            if dy:
                positive_distances.append(dy)
            loss += 2*w[i]*w[j]*(dx-dy)
    if not loss:
        return {"status": "EQUALITY", "scope": "all thresholds and variances"}
    d2 = min(positive_distances)
    ratio = d2/s
    result = {
        "status": "NOT_COVERED",
        "minimum_positive_endpoint_distance_squared": str(d2),
        "separation_over_variance": str(ratio),
        "required_separation_over_variance": 131072,
        "max_log_threshold": str(ratio/1024),
        "ordered_loss_over_variance": str(loss/s),
        "source_site_count": n,
        "distinct_target_count": len(set(y)),
        "minimum_weight_used": False,
    }
    if ratio < 131072:
        result["reason"] = "variance exceeds this sufficient budget"
    elif ell > ratio/1024:
        result["reason"] = "threshold is below this signed window"
    else:
        result["status"] = "NONNEGATIVE"
        result["strictness"] = "strict if exp(-log_threshold)<max(g)/C_s"
    return result


def rank(rows):
    a = [[F(v) for v in row] for row in rows]
    r = 0
    for c in range(len(a[0])):
        p = next((j for j in range(r, len(a)) if a[j][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        p = a[r][c]
        a[r] = [v/p for v in a[r]]
        for j in range(r+1, len(a)):
            p = a[j][c]
            a[j] = [v-p*t for v, t in zip(a[j], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def stirling(n, k):
    if n == k == 0:
        return 1
    if k == 0 or k > n:
        return 0
    return k*stirling(n-1, k) + stirling(n-1, k-1)


def audit():
    a, L = F(256), F(128)
    eps = a**(-3)
    require(a*a/512 == L and 2*a*a == 131072, "Threshold normalization")
    require(225*L >= L+1, "Active amplitude floor")
    require(a*a-9*a-72 > 0 and 2*a-9 > 0,
            "Logarithmic domination polynomial and its derivative")
    require(1+a*a/512 <= a*a/8, "Self-supplied mass bound")
    sums = [sum(stirling(n, k)*factorial(k-1) for k in range(1, n+1))
            for n in range(1, 6)]
    require(sums == [1, 2, 6, 26, 150], "Log partition derivatives")
    q = F(1, 4)
    require((1+4*q+q*q)/(1-q)**4 < 8, "Matrix square-root majorant")
    require(eps <= F(1, 64), "Chart perturbation")
    for k in (1, 2, 3):
        require(8*(a/8+k) <= 2*a, "Chart derivative scale")
    require(a/12+eps/2 < a/8, "Inverse chart domain")
    require(16+96*eps <= 18 and 216+1536*eps <= 256, "Inverse/Jacobian bounds")
    require(97+a/2 <= a and 266+2*a <= 4*a, "Tilt bounds")
    require(48+4*a <= 5*a, "Midpoint linear coefficient")
    require(25/a**4+24/a**2 <= 49/a**2, "Midpoint square completion")
    require(F(7, 16) < 1 and 1-F(1, 3)/F(5, 6) == F(3, 5),
            "Three-dimensional spherical margin")
    # Terms of -x b'(x) decrease for 0<=x<=1; polynomial factors
    # below are its exact coefficient ratios at x=1.
    for k in range(1, 20):
        ratio = F((k+1), k*(2*k+2)*(2*k+3))
        require(0 < ratio < 1, "Alternating derivative-series ratio")
    require(F(1, 3)-F(1, 30) > 0, "Lower derivative-series bound")
    print("PASS: active-well, chart, midpoint and S2 spectral constants")

    example = {
        "source": [[0, 0, 0], [2, 0, 0]],
        "target": [[0, 0, 0], [1, 0, 0]],
        "weights": ["1/2", "1/2"],
        "variance": "1/131072", "log_threshold": 128,
    }
    out = certify(example)
    require(out["status"] == "NONNEGATIVE" and out["max_log_threshold"] == "128",
            "Exact closed noise/threshold boundary")
    z = deepcopy(example); z["variance"] = "1/131071"
    require(certify(z)["status"] == "NOT_COVERED", "Outside noise guard")
    z = deepcopy(example); z["log_threshold"] = "128001/1000"
    require(certify(z)["status"] == "NOT_COVERED", "Below signed threshold")
    z = deepcopy(example); z["target"] = deepcopy(z["source"]); z["variance"] = 10
    require(certify(z)["status"] == "EQUALITY", "Isometry")
    single = {"source": [[1, 2, 3]], "target": [[9, 8, 7]], "weights": [1],
              "variance": 10, "log_threshold": 1000}
    require(certify(single)["status"] == "EQUALITY", "Single source")
    z = deepcopy(example); z["target"] = [[0, 0, 0]]*2; z["variance"] = "1/32768"
    out = certify(z)
    require(out["status"] == "NONNEGATIVE" and out["distinct_target_count"] == 1,
            "Complete target merger")
    # Scaling all coordinates by three and variance by nine preserves
    # the two dimensionless quantities used in the certificate.
    z = deepcopy(example)
    for name in ("source", "target"):
        z[name] = [[3*v+7 for v in row] for row in z[name]]
    z["variance"] = "9/131072"
    out = certify(z)
    require(out["status"] == "NONNEGATIVE" and out["max_log_threshold"] == "128",
            "Common scaling and translations")
    print("PASS: seven boundary, equality, merger and normalization controls")

    # Credited geometric control from the prior collision theorem6386.
    # Coordinatewise absolute value is a known positive map; it is not
    # presented as a new Gaussian class or a counterexample candidate.
    x = [[0, 0, 0], [-1, 0, 0], [1, 0, 0], [0, -2, 0],
         [0, 2, 0], [0, 0, -3], [0, 0, 3]]
    y = [[abs(v) for v in row] for row in x]
    require(rank([x[i]+y[i] for i in range(1, 7)]) == 6, "Paired rank six")
    groups = {tuple(row) for row in y}
    require(len(groups) == 4, "Exact coincidence quotient")
    for bits in (8, 64, 256, 1024, 2048):
        e = F(1, 2**bits)
        w = [e*2**i for i in range(6)]+[1-63*e]
        data = {"source": x, "target": y, "weights": [str(v) for v in w],
                "variance": "1/131072", "log_threshold": 128}
        out = certify(data)
        require(out["status"] == "NONNEGATIVE" and out["max_log_threshold"] == "128"
                and not out["minimum_weight_used"], "Prior-uniform window")
        # An exact algebraic control for the conditional grouping identity.
        conditional_factors = [F(i+1, 8) for i in range(7)]
        amplitudes = {g: sum(w[i]*conditional_factors[i] for i in range(7)
                            if tuple(y[i]) == g) for g in groups}
        require(sum(amplitudes.values()) == sum(w[i]*conditional_factors[i]
                                               for i in range(7)) <= 1,
                "Conditional amplitudes preserve total mass bound")
    for i in range(7):
        for j in range(i):
            dx, dy = distance2(x[i], x[j]), distance2(y[i], y[j])
            require(dx >= dy and dx >= 1, "Source half: all 21 separated pairs")
            if dy:
                require(dy >= 1, "Target half: all distinct groups separated")
            # At t=1/2 the squared normal separations are dx/2 or dy/2;
            # their affine factors increase toward the corresponding end.
    print("PASS: rank-six collision control; five priors down to 2^-2048")
    print("PASS: all 21 contraction pairs and both conditional group splittings")

    bad = []
    z = deepcopy(example); z["weights"] = ["1/2", "1/3"]; bad.append(z)
    z = deepcopy(example); z["weights"] = [0, 1]; bad.append(z)
    z = deepcopy(example); z["weights"] = [True, 0]; bad.append(z)
    z = deepcopy(example); z["variance"] = 0; bad.append(z)
    z = deepcopy(example); z["variance"] = 0.5; bad.append(z)
    z = deepcopy(example); z["log_threshold"] = -1; bad.append(z)
    z = deepcopy(example); z["target"][1] = [3, 0, 0]; bad.append(z)
    z = deepcopy(example); z["source"][1] = [0, 0, 0]; bad.append(z)
    z = deepcopy(example); z["target"][1] = [1, 0]; bad.append(z)
    z = deepcopy(example); z["target"].pop(); bad.append(z)
    for data in bad:
        try:
            certify(data)
        except (ValueError, TypeError):
            continue
        raise ValueError("Malformed input was accepted")
    print("PASS: ten malformed inputs rejected")
    print("ATOMIC_HINGE_WINDOW_AUDIT_PASS")


if __name__ == "__main__":
    require(len(sys.argv) <= 2, "Usage: audit.py [input.json]")
    if len(sys.argv) == 2:
        print(json.dumps(certify(json.loads(Path(sys.argv[1]).read_text())), indent=2))
    else:
        audit()
