"""Produce a uniform all-threshold cloud-family certificate with exact arithmetic.

The analytic meaning and trust boundaries are in PROOF.md. No huge dyadic
denominator is expanded: perturbation budgets are encoded by their exponents.
"""
import argparse
from fractions import Fraction as F
import json
from math import isqrt


def require(ok, message):
    if not ok:
        raise ValueError(message)


def rational(x):
    require(type(x) in (int, str), "exact integer or rational string required")
    return F(x)


def integer(x, lower, label):
    require(type(x) is int and x >= lower, "invalid " + label)
    return x


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def sub(x, y):
    return [a-b for a, b in zip(x, y)]


def vector(x):
    require(isinstance(x, list) and len(x) == 3, "three coordinates required")
    return list(map(rational, x))


def ceil_rational(x):
    return -(-x.numerator // x.denominator)


def ceil_sqrt(x):
    require(x >= 0, "negative square root")
    t = isqrt(x.numerator // x.denominator)
    return t if t*t == x else t+1


def dyadic_below(x):
    require(x > 0, "positive dyadic bound required")
    b = max(0, x.denominator.bit_length()-x.numerator.bit_length())
    if (x.numerator << b) < x.denominator:
        b += 1
    return b


def produce(data):
    require(data["schema"] == "anchored-cloud-family-input-v1", "wrong input schema")
    p, q = [[vector(v) for v in data[k]] for k in ("source", "target")]
    require(len(p) == len(q) and len(p) >= 2, "matching label lists required")
    anchors = [vector(v) for v in data["anchors"]]
    require(len(anchors) == 2, "two anchors required")
    p, q = [[sub(v, z) for v in rows] for rows, z in zip((p, q), anchors)]
    R = integer(data["radius"], 1, "radius")
    ell = integer(data["mass_exponent"], 0, "mass exponent")
    S = rational(data["variance_ratio"])
    require(S >= 1, "variance ratio must be at least one")
    m = F(1, 1 << ell)
    require(len(p)*m <= 1, "empty prior region")
    require(all(dot(x, x) == dot(y, y) <= R*R for x, y in zip(p, q)),
            "anchor equality or radius failed")
    losses = []
    for i in range(len(p)):
        for j in range(i):
            dx, dy = sub(p[i], p[j]), sub(q[i], q[j])
            loss = dot(dx, dx)-dot(dy, dy)
            require(loss >= 0, "reference pair expands")
            losses.append(loss)
    d0 = 2*m*m*sum(losses)
    require(d0 > 0, "zero uniform loss floor")

    wc = data["width_witness"]
    require(wc["kind"] == "nested-hulls-rational-cap-v1", "unsupported width witness")
    coeff = [[rational(t) for t in row] for row in wc["target_in_source_hull"]]
    require(len(coeff) == len(q), "wrong containment row count")
    for y, row in zip(q, coeff):
        require(len(row) == len(p) and min(row) >= 0 and sum(row) == 1,
                "invalid barycentric row")
        require([sum(row[i]*p[i][k] for i in range(len(p))) for k in range(3)] == y,
                "target is not in certified source hull")
    n = vector(wc["cap_axis"])
    c, r = rational(wc["cap_cosine"]), rational(wc["cap_sine_upper"])
    star = integer(wc["source_witness"], 0, "source cap witness")
    bits = integer(wc.get("perpendicular_bits", 16), 0, "perpendicular precision")
    scale = 1 << bits
    require(star < len(p) and dot(n, n) == 1 and 0 <= c < 1 and r >= 0
            and r*r >= 1-c*c, "invalid cap geometry")
    axial, perp = [], []
    for y in q:
        z = sub(p[star], y)
        A = dot(n, z)
        require(A >= 0, "cap axial coefficient is negative")
        axial.append(A)
        perp.append(F(ceil_sqrt((dot(z, z)-A*A)*scale*scale), scale))
    gamma = min(c*A-r*b for A, b in zip(axial, perp))
    require(gamma > 0, "cap has no certified support gap")
    w = (1-c)*gamma/2
    require(w <= 2*R, "inconsistent width bound")

    a = dyadic_below(d0/S)
    A = 6*(R+1)**2+2*S*(ell+1)
    Q0 = 8*A/w
    j = ceil_rational(Q0*Q0)
    k = a+9*R*R+4
    N = 40*R*R+9*R+38+3*j+8*k
    M = a+N
    bw = dyadic_below(w/2)
    B = max(M+1, k, ell+1, 1, bw)
    return {
        "schema": "anchored-cloud-family-certificate-v1",
        "status": "CERTIFIED_UNIFORM_ALL_THRESHOLD_FAMILY",
        "labels": len(p),
        "unordered_pairs": len(losses),
        "strict_pairs": sum(t > 0 for t in losses),
        "uniform_loss_floor": str(d0),
        "normalized_loss_exponent": a,
        "width": {"lower": str(w), "cap_gap_lower": str(gamma),
                  "perpendicular_upper": list(map(str, perp))},
        "schedule": {"tail_A": str(A), "tail_Q": str(Q0), "j": j,
                     "k": k, "N": N, "M": M, "width_exponent": bw,
                     "budget_exponent": B},
        "conclusion": {
            "variance_interval": ["1", str(S)],
            "threshold_interval": "[0,infinity)",
            "prior_region": "v_i >= 2^-mass_exponent; sum v_i=1",
            "error_guard": "2*cloud_radius + l1(u-v) + l1(z-v) <= 2^-budget_exponent",
            "middle_gap_exponent": M+1,
            "actual_contraction_required": False,
            "diffuse_clouds_allowed": True,
            "independent_review": "PENDING",
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    args = parser.parse_args()
    with open(args.input) as f:
        record = produce(json.load(f))
    print(json.dumps(record, sort_keys=True, indent=2))
