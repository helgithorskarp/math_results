#!/usr/bin/env python3
"""Exact premise/schedule producer and arithmetic audit for PROOF.md.

Python 3.11+, standard library only. No Gaussian integral is evaluated.
With no argument, audit constants and finite controls. With one JSON path,
check that input and print its sufficient theorem certificate.
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


def mass_bits(p):
    require(0 < p <= 1, "Invalid probability floor")
    b = max(0, p.denominator.bit_length() - p.numerator.bit_length())
    while F(1, 2**b) > p:
        b += 1
    while b > 0 and F(1, 2**(b-1)) <= p:
        b -= 1
    return b


def certify(data):
    require(isinstance(data, dict), "Expected a JSON object")
    points = []
    for key in ("source", "target"):
        rows = data[key]
        require(isinstance(rows, list) and len(rows) >= 2, "Need at least two sites")
        require(all(isinstance(row, list) and len(row) == 3 for row in rows),
                "Sites must be three-dimensional lists")
        points.append([tuple(rational(x) for x in row) for row in rows])
    x, y = points
    require(len(x) == len(y), "Endpoint sizes differ")
    n = len(x)
    w = [rational(t) for t in data["weights"]]
    require(len(w) == n and all(t > 0 for t in w) and sum(w) == 1,
            "Weights must be positive and sum to one")
    s = rational(data["variance"])
    ell = rational(data["log_threshold"])
    require(s > 0 and ell >= 0, "Variance must be positive; log threshold nonnegative")
    target_distances = []
    loss = F(0)
    for i in range(n):
        for j in range(i):
            dx, dy = distance2(x[i], x[j]), distance2(y[i], y[j])
            require(dx > 0, "Combine repeated source sites before using this producer")
            require(dy <= dx, "The supplied map is not a contraction")
            target_distances.append(dy)
            loss += 2*w[i]*w[j]*(dx-dy)
    if loss == 0:
        return {"status": "EQUALITY", "scope": "all thresholds and variances"}
    d2 = min(target_distances)
    if d2 == 0:
        return {"status": "NOT_COVERED", "reason": "target collision"}
    b = mass_bits(min(w))
    a2 = d2/s
    required_a2 = 65536 + 8*b
    ell_max = a2/512
    result = {
        "status": "NOT_COVERED",
        "target_separation_squared": str(d2),
        "weight_floor_bits": b,
        "a_squared": str(a2),
        "required_a_squared": required_a2,
        "max_log_threshold": str(ell_max),
        "ordered_loss_over_variance": str(loss/s),
    }
    if a2 < required_a2:
        result["reason"] = "variance exceeds this sufficient budget"
    elif ell > ell_max:
        result["reason"] = "threshold is below this signed window"
    else:
        result["status"] = "NONNEGATIVE"
        result["strictness"] = "strict if exp(-log_threshold)<max(g)/C_s"
    return result


def rank(rows):
    a = [[F(v) for v in row] for row in rows]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        pivot = next((j for j in range(r, len(a)) if a[j][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
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
    a = F(256)
    eps = a**(-3)
    eta = eps/(2*a)
    require(a*a == 65536 and eps < F(1, 64), "Separation guard")
    require(a*a-9*a-72 > 0 and 2*a-9 > 0, "Exponential domination polynomial")
    require(eta <= F(1, 4), "Square-root series domain")
    sums = [sum(stirling(n, k)*factorial(k-1) for k in range(1, n+1))
            for n in range(1, 6)]
    require(sums == [1, 2, 6, 26, 150] and max(sums) < 256, "Log derivatives")
    q = F(1, 4)
    require((1+4*q+q*q)/(1-q)**4 < 8, "Matrix-square-root majorant")
    for k in (1, 2, 3):
        require(8*(a/8+k) <= 2*a, "Direct chart derivative")
    require(a/12+eps/2 < a/8, "Inverse chart inclusion")
    require(16+96*eps <= 18, "Third inverse derivative")
    require(216+1536*eps <= 256, "Log-Jacobian Hessian")
    require(97+a/2 <= a and 266+2*a <= 4*a, "Tilt derivatives")
    require(48+4*a <= 5*a, "Midpoint linear coefficient")
    require(25/a**4+24/a**2 <= 49/a**2, "Completed square")
    require(F(49, 256) < 1, "Spherical comparison domain")
    require(4-F(1, 6)/F(11, 12) == F(42, 11), "Spherical derivative margin")
    print("PASS: exact chart, midpoint and spherical constants")

    # The floor producer uses log(1/p)<=b*log(2)<b.
    for b in range(1, 257):
        require(mass_bits(F(1, 2**b)) == b, "Exact dyadic floor")
        require(mass_bits(F(3, 2**(b+2))) == b+1, "Nondyadic floor")
    print("PASS: 512 exact weight-floor schedules")

    # Complete example accepted by the optional JSON interface.
    example = {
        "source": [[0, 0, 0], [2, 0, 0]],
        "target": [[0, 0, 0], [1, 0, 0]],
        "weights": ["1/2", "1/2"],
        "variance": "1/65544",
        "log_threshold": "8193/64",
    }
    out = certify(example)
    require(out["status"] == "NONNEGATIVE", "Exact noise/threshold boundary")
    require(out["max_log_threshold"] == "8193/64", "Boundary normalization")
    changed = deepcopy(example)
    changed["variance"] = "1/65543"
    require(certify(changed)["status"] == "NOT_COVERED", "Outside noise budget")
    changed = deepcopy(example)
    changed["log_threshold"] = str(F(8193, 64)+F(1, 1000))
    require(certify(changed)["status"] == "NOT_COVERED", "Below threshold window")
    changed = deepcopy(example)
    changed["target"] = deepcopy(changed["source"])
    changed["variance"] = 10
    require(certify(changed)["status"] == "EQUALITY", "Isometric case")
    changed = deepcopy(example)
    changed["target"][1] = [0, 0, 0]
    require(certify(changed)["reason"] == "target collision", "Collision scope")
    changed = deepcopy(example)
    changed["weights"] = [str(F(1, 2**80)), str(1-F(1, 2**80))]
    changed["variance"] = str(F(1, 65536+8*80))
    changed["log_threshold"] = 1
    require(certify(changed)["status"] == "NONNEGATIVE", "Rare atom control")
    print("PASS: six exact boundary, equality and scope controls")

    # A rational seven-site control. Paired rank is checked directly;
    # no full all-variance sign or new geometric class is claimed for it.
    m = 2**20
    x = [[i, i*i, i**3] for i in range(7)]
    y = [[F(i**k, m) for k in (4, 5, 6)] for i in range(7)]
    require(rank([x[i]+y[i] for i in range(1, 7)]) == 6, "Paired affine rank")
    d2 = min(distance2(y[i], y[j]) for i in range(7) for j in range(i))
    data = {
        "source": x,
        "target": [[str(v) for v in row] for row in y],
        "weights": ["1/7"]*7,
        "variance": str(d2/(65536+24)),
        "log_threshold": str(F(65536+24, 512)),
    }
    require(certify(data)["status"] == "NONNEGATIVE", "Paired-rank-six control")
    # Every lifted separation is bounded below by the target separation:
    # its square is an affine combination of the endpoint squares.
    for i in range(7):
        for j in range(i):
            require(distance2(x[i], x[j]) >= distance2(y[i], y[j]) >= d2,
                    "Uniform separation along the orthogonal lift")
    print("PASS: paired-rank-six control and all 21 lifted pair bounds")

    malformed = []
    z = deepcopy(example); z["weights"] = ["1/2", "1/3"]; malformed.append(z)
    z = deepcopy(example); z["weights"] = [0, 1]; malformed.append(z)
    z = deepcopy(example); z["variance"] = 0; malformed.append(z)
    z = deepcopy(example); z["variance"] = 0.5; malformed.append(z)
    z = deepcopy(example); z["log_threshold"] = -1; malformed.append(z)
    z = deepcopy(example); z["target"][1] = [3, 0, 0]; malformed.append(z)
    z = deepcopy(example); z["source"][1] = [0, 0, 0]; malformed.append(z)
    z = deepcopy(example); z["source"][0] = [0, 0]; malformed.append(z)
    for data in malformed:
        try:
            certify(data)
        except (ValueError, TypeError):
            continue
        raise ValueError("Malformed input was accepted")
    print("PASS: eight malformed inputs rejected")
    print("SEPARATED_HINGE_WINDOW_AUDIT_PASS")


if __name__ == "__main__":
    require(len(sys.argv) <= 2, "Usage: audit.py [input.json]")
    if len(sys.argv) == 2:
        print(json.dumps(certify(json.loads(Path(sys.argv[1]).read_text())), indent=2))
    else:
        audit()
