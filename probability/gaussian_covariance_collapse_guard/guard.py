"""Exact finite-input certificate for the covariance-collapse theorem.

No eigenvalue approximation, Gaussian integration or extension oracle is
used. The written projection proof is the analytic trust boundary.
"""
from fractions import Fraction as F
from functools import reduce
from math import gcd, lcm
import argparse
import json


def rational(value):
    if type(value) not in (int, str):
        raise ValueError("rational data must be integers or strings")
    return F(value)


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), F(0))


def minus(x, y):
    return [a-b for a, b in zip(x, y)]


def primitive(v):
    denominator = lcm(*(x.denominator for x in v))
    out = [int(x*denominator) for x in v]
    divisor = reduce(gcd, map(abs, out))
    if not divisor:
        raise ValueError("zero direction")
    out = [x//divisor for x in out]
    if next(x for x in out if x) < 0:
        out = [-x for x in out]
    return out


def nonpositive_direction(matrix):
    """Return v != 0 with v^T M v <= 0, or None exactly when M is SPD."""
    if len(matrix) != 3 or any(len(row) != 3 for row in matrix):
        raise ValueError("three by three matrix required")
    M = [[F(v) for v in row] for row in matrix]
    if any(M[i][j] != M[j][i] for i in range(3) for j in range(3)):
        raise ValueError("symmetric matrix required")
    basis = [[F(i == j) for i in range(3)] for j in range(3)]
    while basis:
        b = basis[0]
        Mb = [dot(row, b) for row in M]
        pivot = dot(b, Mb)
        if pivot <= 0:
            return primitive(b)
        basis = [[v[i]-dot(v, Mb)*b[i]/pivot for i in range(3)]
                 for v in basis[1:]]
    return None


def finite_guard(data):
    x = [[rational(v) for v in row] for row in data["sources"]]
    y = [[rational(v) for v in row] for row in data["targets"]]
    p = [rational(v) for v in data["weights"]]
    s = rational(data.get("variance", 1))
    if not p or len(x) != len(p) or len(y) != len(p):
        raise ValueError("matching nonempty lists required")
    if any(len(row) != 3 for row in x+y) or s <= 0:
        raise ValueError("dimension or variance")
    if any(v < 0 for v in p) or sum(p) != 1:
        raise ValueError("probability weights")
    active = [i for i, w in enumerate(p) if w]
    x, y, p = [[seq[i] for i in active] for seq in (x, y, p)]
    for i in range(len(p)):
        for j in range(i):
            dx, dy = minus(x[i], x[j]), minus(y[i], y[j])
            if dot(dy, dy) > dot(dx, dx):
                raise ValueError("expanding pair")
    means = [[sum(w*point[k] for w, point in zip(p, cloud)) for k in range(3)]
             for cloud in (x, y)]
    centered = [[minus(point, mean) for point in cloud]
                for cloud, mean in zip((x, y), means)]
    covs = [[[sum(w*point[j]*point[k] for w, point in zip(p, cloud))/s
              for k in range(3)] for j in range(3)] for cloud in centered]
    D = 2*sum(covs[0][j][j]-covs[1][j][j] for j in range(3))
    radius2 = max(dot(point, point)/s for point in centered[0])
    if D < 0:
        raise RuntimeError("contraction/loss inconsistency")
    result = {"schema": "covariance-collapse-v1", "D": str(D),
              "source_radius_squared": str(radius2), "active_sites": len(p)}
    if D == 0:
        return dict(result, status="ISOMETRIC_ZERO")
    if radius2 > F(1, 4):
        return dict(result, status="UNRESOLVED", reason="radius")
    threshold = D*D/F(2**86)
    for side, cov in zip(("source", "target"), covs):
        matrix = [[cov[i][j]-(threshold if i == j else 0) for j in range(3)]
                  for i in range(3)]
        direction = nonpositive_direction(matrix)
        if direction is not None:
            q = dot(direction, [dot(row, direction) for row in cov])/dot(direction, direction)
            if q > threshold:
                raise RuntimeError("Rayleigh witness mismatch")
            return dict(result, status="SIGNED_MIDDLE", side=side,
                        direction=direction, directional_variance=str(q),
                        variance_cutoff=str(threshold), middle_margin=str(D/F(2**42)),
                        signed_thresholds="[1/64,infinity)", margin_interval="[1/64,1/2]")
    return dict(result, status="UNRESOLVED", reason="both covariance matrices above cutoff")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    args = parser.parse_args()
    with open(args.input) as stream:
        record = finite_guard(json.load(stream))
    print(json.dumps(record, sort_keys=True, indent=2))
