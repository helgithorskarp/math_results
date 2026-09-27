#!/usr/bin/env python3
"""Exact finite inputs and algebra controls; analytic proof is in PROOF.md."""
import copy
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rational(x):
    require(type(x) in (int, str), "Use integers or rational strings")
    return Q(x)


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), Q(0))


def minus(x, y):
    return tuple(a - b for a, b in zip(x, y))


def norm2(x):
    return dot(x, x)


def vector(x):
    require(isinstance(x, list) and len(x) == 3, "Expected a 3-vector")
    return tuple(map(rational, x))


def rank(rows):
    a = [list(row) for row in rows]
    if not a:
        return 0
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        v = a[row][col]
        a[row] = [x / v for x in a[row]]
        for i in range(len(a)):
            if i != row:
                v = a[i][col]
                a[i] = [x - v * y for x, y in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def loss_and_variance(p, q, w):
    """Independent ordered pair sum and centered second moments."""
    d = sum((w[i] * w[t] * (norm2(minus(p[i], p[t]))
             - norm2(minus(q[i], q[t])))
             for i in range(len(w)) for t in range(len(w))), Q(0))

    def var(points):
        mean = tuple(sum((wi * x[k] for wi, x in zip(w, points)), Q(0))
                     for k in range(3))
        return sum((wi * norm2(x) for wi, x in zip(w, points)), Q(0)) - norm2(mean)

    require(d == 2 * (var(p) - var(q)), "Pair/variance mismatch")
    return d


def parse(data):
    require(isinstance(data, dict), "Expected an object")
    require(set(data) == {"source", "target", "weights", "source_anchor",
                         "target_anchor", "variance", "R", "j", "k"},
            "Unexpected or missing field")
    require(all(isinstance(data[x], list) for x in ("source", "target", "weights")),
            "Expected lists")
    p, q = list(map(vector, data["source"])), list(map(vector, data["target"]))
    w = list(map(rational, data["weights"]))
    require(len(p) == len(q) == len(w) > 0, "Unequal or empty lists")
    require(all(x > 0 for x in w) and sum(w) == 1, "Invalid probability weights")
    a, b = vector(data["source_anchor"]), vector(data["target_anchor"])
    s = rational(data["variance"])
    require(s > 0, "Variance must be positive")
    R, j, k = (data[x] for x in ("R", "j", "k"))
    require(type(R) is int and R >= 1, "R must be a positive integer")
    require(type(j) is int and j >= 0 and type(k) is int and k >= 0,
            "j,k must be nonnegative integers")
    return [minus(x, a) for x in p], [minus(x, b) for x in q], w, s, R, j, k


def certify(data):
    p, q, w, s, R, j, k = parse(data)
    losses = [norm2(minus(p[i], p[t])) - norm2(minus(q[i], q[t]))
              for i in range(len(p)) for t in range(i)]
    if any(x < 0 for x in losses):
        return {"status": "UNRESOLVED", "reason": "pair expansion"}
    if any(norm2(x) != norm2(y) for x, y in zip(p, q)):
        return {"status": "UNRESOLVED", "reason": "anchor norm mismatch"}
    if any(norm2(x) > s * R * R for x in p):
        return {"status": "UNRESOLVED", "reason": "radius too small"}
    d = loss_and_variance(p, q, w)
    joined = [x + y for x, y in zip(p, q)]
    W = 2 * R + 2 ** (j + 1)
    exponent = 2 * W * W + W + 8 * R + 8 * k + 33
    lower, upper = Q(1, 2 ** j), Q(1, 2 ** (R * R)) - Q(1, 2 ** k)
    return {
        "status": "STRICT_NORM_PRESERVING_HINGES" if d else "ISOMETRY",
        "sites": len(w), "pairs": len(losses), "tight_pairs": losses.count(0),
        "paired_affine_rank": rank([minus(x, joined[0]) for x in joined[1:]]),
        "ordered_loss": str(d), "normalized_loss": str(d / s),
        "margin": {"prefactor": str(d / s), "power_of_two": -exponent},
        "conditional_band": {"h_over_C_lower": str(lower),
                             "distance_below_target_peak_over_C": str(Q(1, 2 ** k))},
        "explicit_band": {"lower": str(lower), "upper": str(upper),
                          "nonempty": lower <= upper},
        "scope": "Analytic Theorems 1/2 conditional on exact finite hypotheses; no peak oracle",
    }


def pins():
    records = json.loads((HERE / "DEPENDENCIES.json").read_text())
    for r in records:
        content = (HERE / r["path"]).read_bytes()
        require(hashlib.sha256(content).hexdigest() == r["sha256"], "Dependency pin mismatch")
    return len(records)


def controls(base):
    cert = certify(base)
    require(cert["status"] == "STRICT_NORM_PRESERVING_HINGES", "Calibration not strict")
    require(cert["paired_affine_rank"] == 6, "Calibration rank")
    p, q, w, _, _, _, _ = parse(base)
    # Independent endpoint orthogonal frames and translations retain the anchors.
    transformed = copy.deepcopy(base)
    for name, anchor, perm, signs in [
        ("source", [3, -2, 1], [1, 2, 0], [1, -1, 1]),
        ("target", [-4, 1, 2], [2, 0, 1], [-1, 1, -1]),
    ]:
        transformed[name] = [[str(signs[i] * rational(x[perm[i]]) + anchor[i])
                              for i in range(3)] for x in base[name]]
        transformed[name + "_anchor"] = anchor
    require(certify(transformed) == cert, "Endpoint frame invariance")
    # Spatial scaling and variance scaling keep the complete normalized record.
    scaled = copy.deepcopy(base)
    for name in ("source", "target"):
        scaled[name] = [[str(3 * rational(v)) for v in x] for x in base[name]]
    scaled["variance"] = 9
    result = certify(scaled)
    require(Q(result["ordered_loss"]) == 9 * Q(cert["ordered_loss"]), "Loss scaling")
    result["ordered_loss"] = cert["ordered_loss"]
    require(result == cert, "Variance normalization")
    iso = copy.deepcopy(base)
    iso["target"] = copy.deepcopy(iso["source"])
    require(certify(iso)["status"] == "ISOMETRY", "Isometry guard")
    singleton = copy.deepcopy(base)
    singleton.update(source=[[0, 0, 0]], target=[[0, 0, 0]], weights=[1])
    require(certify(singleton)["status"] == "ISOMETRY", "Singleton guard")

    # Posterior trace and likelihood-floor comparison in unrelated rational laws.
    posterior_cases = 0
    for n in range(1, 20):
        likelihood = [Q(1 + (n * (i + 3)) % 17, 18) for i in range(len(w))]
        z = sum(x * y for x, y in zip(w, likelihood))
        post = [x * y / z for x, y in zip(w, likelihood)]
        dp = loss_and_variance(p, q, post)
        beta = min(likelihood)  # z<=1, so dpost/dw>=beta.
        require(dp >= beta * beta * Q(cert["ordered_loss"]), "Posterior lower bound")
        posterior_cases += 1

    # Check the kernel exponent inequalities through exact rational vectors.
    directions = [(Q(1), Q(0), Q(0)), (Q(0), Q(1), Q(0)),
                  (Q(3, 5), Q(4, 5), Q(0)), (Q(0), Q(-3, 5), Q(4, 5))]
    kernel_cases = 0
    for theta in directions:
        for eta in directions:
            require(norm2(theta) == norm2(eta) == 1, "Not sphere directions")
            for u in (Q(0), Q(1, 7), Q(5, 6), Q(1)):
                for rho in (Q(1, 8), Q(1), Q(18)):
                    exponent = []
                    for x, y in zip(p, q):
                        m = (1-u) * dot(theta, x) + u * dot(eta, y)
                        e = -rho*rho/2 - norm2(x)/2 + rho*m
                        require(e <= 0 and abs(-rho+m) <= rho+1, "Kernel upper/derivative")
                        require(abs(dot(eta, y)-dot(theta, x)) <= 2, "u derivative")
                        exponent.append(e)
                    for i in range(len(p)):
                        for t in range(i):
                            require(exponent[i] + exponent[t] >= -(rho+1)**2,
                                    "Kernel pair lower bound")
                    kernel_cases += 1

    constant_cases = 0
    for R in range(1, 6):
        for j in range(5):
            for k in range(5):
                epsilon, B = Q(1, 2**k), R+1
                W = 2*R+2**(j+1)
                a, b = epsilon/(16*B*R), epsilon/(8*B*R)
                product = 4*(epsilon/4)**4*Q(1, 2)*(a*a/8)*(b*b/4)/W
                expected = epsilon**8/(2**26*B**4*R**4*W)
                require(product == expected, "Factor-of-two error")
                require(B**4*R**4 <= 2**(4+8*R) and W <= 2**W, "Dyadic estimate")
                # Exact integral of u(1-u) on the restricted interval.
                antiderivative = lambda v: v*v/2-v*v*v/3
                require(antiderivative(1-a/2)-antiderivative(1-a) >= a*a/8,
                        "Time interval integral")
                tau = Q(1, 2**j)
                require(tau*tau/(tau*tau+2) <= tau/2, "Tail endpoint algebra")
                constant_cases += 1

    # Universal two-site interval: p=(-t,1/2), q=(t,1/2), equal weights.
    # Compare polynomial coefficient arrays rather than relying on sampling.
    # (t+1/2)^2-(t-1/2)^2=2t; ordered weight factor is 1/2.
    squared_source, squared_target = [Q(1, 4), Q(1), Q(1)], [Q(1, 4), Q(-1), Q(1)]
    pair_polynomial = [x-y for x, y in zip(squared_source, squared_target)]
    require(pair_polynomial == [0, 2, 0], "Family polynomial")
    for t in (Q(0), Q(1, 1024), Q(1, 16)):
        example = copy.deepcopy(base)
        example.update(source=[[str(-t), 0, 0], ["1/2", 0, 0]],
                       target=[[str(t), 0, 0], ["1/2", 0, 0]], weights=["1/2", "1/2"])
        check = certify(example)
        require(Q(check["ordered_loss"]) == t and check["margin"]["power_of_two"] == -723,
                "Vanishing-loss control")
    family = {"parameter_interval": "0<=t<=1/16", "ordered_loss": "t",
              "margin": "t*2^-723", "explicit_h_over_C_band": ["1/8", "1/4"],
              "proof_check": "Exact quadratic coefficients; theorem uniform in t"}

    negatives = 0
    homothety = copy.deepcopy(base)
    homothety["target"] = [[str(rational(v)/2) for v in x] for x in base["source"]]
    require(certify(homothety)["reason"] == "anchor norm mismatch", "Anchor rejection")
    negatives += 1
    expansion = copy.deepcopy(base)
    expansion["target"] = [[str(2*rational(v)) for v in x] for x in base["source"]]
    require(certify(expansion)["reason"] == "pair expansion", "Expansion rejection")
    negatives += 1
    radius = copy.deepcopy(base)
    radius["variance"] = "1/100"
    require(certify(radius)["reason"] == "radius too small", "Radius rejection")
    negatives += 1
    for key, value in [("weights", [1]*7), ("variance", 0), ("R", True), ("R", 0),
                       ("j", -1), ("k", "2"), ("source_anchor", [0, 0]),
                       ("target", [[0, 0, 0]]), ("variance", 0.5)]:
        bad = copy.deepcopy(base)
        bad[key] = value
        try:
            certify(bad)
        except (ValueError, ZeroDivisionError):
            negatives += 1
        else:
            raise ValueError("Malformed input accepted: " + key)
    return {"status": "STRICT_NORM_HINGE_CONTROLS_PASS", "calibration": cert,
            "posterior_cases": posterior_cases, "kernel_cases": kernel_cases,
            "constant_cases": constant_cases, "negative_controls": negatives,
            "vanishing_loss_family": family, "content_pins": pins(),
            "trust_boundary": "Exact finite author checks, not formal or independent analytic verification"}


def main():
    if len(sys.argv) == 2:
        out = certify(json.loads(Path(sys.argv[1]).read_text()))
    elif len(sys.argv) == 1:
        out = controls(json.loads((HERE / "INPUT.json").read_text()))
        expected = HERE / "EXPECTED.json"
        require(out == json.loads(expected.read_text()), "Expected record mismatch")
    else:
        raise ValueError("Usage: verify.py [INPUT.json]")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
