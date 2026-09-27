"""Exact finite guard for uniform eventual Gaussian majorisation.

The proof uses spherical symmetrization, not a martingale witness.
Standard-library fractions only; no numerical spherical integration.
"""
from fractions import Fraction as F
import argparse
import json


def rational(v):
    if type(v) not in (int, str):
        raise ValueError("integers or rational strings required")
    return F(v)


def distance(a, b):
    return sum((u-v)**2 for u, v in zip(a, b))


def produce(data):
    x, y = [[[rational(v) for v in row] for row in data[k]]
            for k in ("sources", "targets")]
    p = [rational(v) for v in data["weights"]]
    s = rational(data.get("variance", 1))
    requested_q = rational(data["factor"]) if "factor" in data else None
    if not p or len(x) != len(y) or len(x) != len(p) or any(len(v) != 3 for v in x+y):
        raise ValueError("matching nonempty three-dimensional lists required")
    if s <= 0 or min(p) < 0 or sum(p) != 1:
        raise ValueError("variance or probability weights")
    if requested_q is not None and not 0 < requested_q < 1:
        raise ValueError("factor must lie strictly between zero and one")
    keep = [i for i, w in enumerate(p) if w]
    x, y, p = [[v[i] for i in keep] for v in (x, y, p)]
    beta = F(0)
    for i in range(len(p)):
        for j in range(i):
            a, b = distance(x[i], x[j]), distance(y[i], y[j])
            if b > a:
                raise ValueError("expanding original pair")
            if a:
                beta = max(beta, b/a)
    mean = [sum(w*z[k] for w, z in zip(p, x)) for k in range(3)]
    norms = [distance(z, mean) for z in x]
    V = sum(w*v for w, v in zip(p, norms))
    B = max(norms)
    record = {"schema":"uniform-lipschitz-v1", "active_sites":len(p),
              "variance":str(s), "squared_lipschitz":str(beta),
              "source_radius_squared":str(B), "source_scatter":str(V)}
    if not V or beta == 1 and all(distance(x[i], x[j]) == distance(y[i], y[j])
                                 for i in range(len(p)) for j in range(i)):
        return dict(record, status="ISOMETRIC_ZERO")
    if beta == 0:
        return dict(record, status="POINT_TARGET_ALL_VARIANCES")
    if beta >= F(1, 27):
        return dict(record, status="UNRESOLVED", reason="uniform contraction bound fails")
    q = requested_q if requested_q is not None else (1+27*beta)/2
    if q*q < 27*beta:
        return dict(record, status="UNRESOLVED", reason="supplied factor is too small")
    eta = (1-q)*V/(96*B)
    cutoff = 44*B/eta
    return dict(record, status="SIGNED_ALL_THRESHOLDS" if s >= cutoff else
                "UNRESOLVED_AT_REQUESTED_VARIANCE", factor=str(q),
                spherical_gap=str(eta), variance_cutoff=str(cutoff),
                pair_loss_floor=str(2*(1-beta)*V),
                certified_variances="[variance_cutoff,infinity)",
                certified_thresholds="[0,infinity)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    args = parser.parse_args()
    with open(args.input) as f:
        result = produce(json.load(f))
    print(json.dumps(result, sort_keys=True, indent=2))
