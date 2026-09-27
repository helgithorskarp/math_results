"""Exact all-threshold high-variance guard with a factored martingale witness.

The Gaussian endpoint theorem remains an analytic dependency. The nine-entry
matrix encodes a coupling; no matrix of n^2 masses need be stored.
"""
from fractions import Fraction as F
import argparse
import json


def rational(v):
    if type(v) not in (int, str):
        raise ValueError("integers or rational strings required")
    return F(v)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def inverse(m):
    a = [[F(v) for v in row]+[F(i == j) for j in range(3)] for i, row in enumerate(m)]
    for j in range(3):
        k = next((k for k in range(j, 3) if a[k][j]), None)
        if k is None:
            return None
        a[j], a[k] = a[k], a[j]
        scale = a[j][j]
        a[j] = [v/scale for v in a[j]]
        for i in range(3):
            if i != j:
                scale = a[i][j]
                a[i] = [v-scale*w for v, w in zip(a[i], a[j])]
    return [row[3:] for row in a]


def produce(data):
    x = [[rational(v) for v in row] for row in data["sources"]]
    y = [[rational(v) for v in row] for row in data["targets"]]
    p = [rational(v) for v in data["weights"]]
    s = rational(data.get("variance", 1))
    dilation = rational(data.get("dilation", 2))
    if not p or len(x) != len(y) or len(x) != len(p) or any(len(v) != 3 for v in x+y):
        raise ValueError("matching nonempty three-dimensional lists required")
    if s <= 0 or dilation <= 1 or any(w < 0 for w in p) or sum(p) != 1:
        raise ValueError("variance, dilation or probability weights")
    keep = [i for i, w in enumerate(p) if w]
    x, y, p = [[z[i] for i in keep] for z in (x, y, p)]
    for i in range(len(p)):
        for j in range(i):
            if sum((a-b)**2 for a, b in zip(y[i], y[j])) > sum((a-b)**2 for a, b in zip(x[i], x[j])):
                raise ValueError("expanding original pair")
    clouds = []
    for z in (x, y):
        mean = [sum(w*row[k] for w, row in zip(p, z)) for k in range(3)]
        clouds.append([[row[k]-mean[k] for k in range(3)] for row in z])
    x, y = clouds
    V, W = [sum(w*dot(z, z) for w, z in zip(p, cloud)) for cloud in clouds]
    D = 2*(V-W)
    B = max(dot(z, z) for z in x)
    record = {"schema":"dilated-martingale-v1", "active_sites":len(p),
              "source_radius_squared":str(B), "source_scatter":str(V),
              "pair_loss":str(D), "variance":str(s), "dilation":str(dilation)}
    if D == 0:
        return dict(record, status="ISOMETRIC_ZERO")
    if D < 0:
        raise RuntimeError("validated contraction has negative loss")
    cov = [[sum(w*z[i]*z[j] for w, z in zip(p, x)) for j in range(3)] for i in range(3)]
    inv = inverse(cov)
    if inv is None:
        return dict(record, status="UNRESOLVED", reason="singular source covariance")
    matrix = [[dilation*v for v in row] for row in inv]
    minimum = min(1+dot(z, [dot(row, w) for row in matrix]) for z in x for w in y)
    if minimum < 0:
        return dict(record, status="UNRESOLVED", reason="negative coupling density",
                    minimum_kernel=str(minimum))
    gap = (dilation-1)*V/(96*dilation*B)
    cutoff = 44*B/gap
    loss_floor = 2*(1-1/dilation**2)*V
    if D < loss_floor or cutoff < 8*B:
        raise RuntimeError("coupling budget inconsistency")
    return dict(record,
                status="SIGNED_ALL_THRESHOLDS" if s >= cutoff else "UNRESOLVED_AT_REQUESTED_VARIANCE",
                matrix=[[str(v) for v in row] for row in matrix],
                minimum_kernel=str(minimum), spherical_gap=str(gap),
                variance_cutoff=str(cutoff), pair_loss_floor=str(loss_floor),
                certified_variances="[variance_cutoff,infinity)",
                certified_thresholds="[0,infinity)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    args = parser.parse_args()
    with open(args.input) as f:
        record = produce(json.load(f))
    print(json.dumps(record, sort_keys=True, indent=2))
