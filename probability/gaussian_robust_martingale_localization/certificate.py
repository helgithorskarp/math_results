"""Exact finite reference witness and uniform all-threshold cloud budget.

The conclusion is for actual contraction pairs in the described family.
It does not infer contraction inside clouds or compare unknown diffuse laws.
"""
from fractions import Fraction as F
import argparse
import json


def rational(value):
    if type(value) not in (int, str):
        raise ValueError("rational strings or integers required")
    return F(value)


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), F(0))


def fail_unless(condition, message):
    if not condition:
        raise ValueError(message)


def produce(data):
    ref = data["reference"]
    x = [[rational(z) for z in row] for row in ref["sources"]]
    y = [[rational(z) for z in row] for row in ref["targets"]]
    p = [rational(z) for z in ref["weights"]]
    fail_unless(p and len(x) == len(y) == len(p) and
                all(len(v) == 3 for v in x+y), "matching 3D clouds required")
    fail_unless(all(w >= 0 for w in p) and sum(p) == 1, "probability weights")
    keep = [i for i, w in enumerate(p) if w]
    x, y, p = [[z[i] for i in keep] for z in (x, y, p)]
    n = len(p)
    for i in range(n):
        for j in range(i):
            dx = [u-v for u, v in zip(x[i], x[j])]
            dy = [u-v for u, v in zip(y[i], y[j])]
            fail_unless(dot(dy, dy) <= dot(dx, dx), "expanding reference pair")
    centers = []
    for cloud in (x, y):
        mean = [sum(w*z[k] for w, z in zip(p, cloud)) for k in range(3)]
        centers.append([[z[k]-mean[k] for k in range(3)] for z in cloud])
    x, y = centers
    V = sum(w*dot(z, z) for w, z in zip(p, x))
    B = rational(data["radius_squared"])
    s = rational(data["variance"])
    witness = data["witness"]
    a = rational(witness["dilation"])
    ax, ay, rx, ry = [rational(data[k]) for k in (
        "source_relative_radius", "target_relative_radius",
        "source_relative_weight_error", "target_relative_weight_error")]
    fail_unless(B > 0 and s > 0 and a > 1, "positive radius, variance, dilation")
    fail_unless(all(dot(z, z) <= B for z in x), "invalid reference radius")
    fail_unless(ax >= 0 and ay >= 0 and 0 <= rx <= F(1, 2) and
                0 <= ry <= F(1, 2), "invalid neighborhood errors")

    kind = witness["kind"]
    if kind == "diagonal":
        fail_unless(all(u == a*v for xx, yy in zip(x, y)
                        for u, v in zip(xx, yy)), "invalid diagonal barycenter")
    elif kind == "affine_density":
        matrix = [[rational(z) for z in row] for row in witness["matrix"]]
        fail_unless(len(matrix) == 3 and all(len(row) == 3 for row in matrix),
                    "3x3 witness required")
        rows, cols = [F(0)]*n, [F(0)]*n
        moments = [[F(0)]*3 for _ in p]
        for i in range(n):
            for j in range(n):
                kernel = 1+dot(x[i], [dot(row, y[j]) for row in matrix])
                mass = p[i]*p[j]*kernel
                fail_unless(mass >= 0, "negative coupling mass")
                rows[i] += mass
                cols[j] += mass
                for k in range(3):
                    moments[j][k] += mass*x[i][k]
        fail_unless(rows == p and cols == p, "wrong coupling marginals")
        fail_unless(all(moments[j][k] == a*p[j]*y[j][k]
                        for j in range(n) for k in range(3)),
                    "wrong conditional first moments")
    else:
        raise ValueError("unknown witness kind")

    e, t = 1-1/a, 1+ax
    perturbation = ax+ay+4*t*(rx+ry)
    margin = e*V/(48*B*t)-perturbation
    # Exact cross-label check: sqrt(dx2)-sqrt(dy2)>=2 sqrt(E2).
    E2 = B*(ax+ay)**2
    cross = True
    for i in range(n):
        for j in range(i):
            dx = [u-v for u, v in zip(x[i], x[j])]
            dy = [u-v for u, v in zip(y[i], y[j])]
            A2, C2 = dot(dx, dx), dot(dy, dy)
            difference = A2-C2-4*E2
            cross = cross and difference >= 0 and difference**2 >= 16*E2*C2
    record = {
        "schema": "robust-martingale-localization-v1",
        "active_reference_sites": n,
        "witness": kind,
        "reference_radius_squared": str(B),
        "reference_scatter": str(V),
        "dilation": str(a),
        "radius_factor": str(t),
        "perturbation_slope_cost": str(perturbation),
        "remaining_dimensionless_slope": str(margin),
        "source_cloud_radius_squared": str(B*ax**2),
        "target_cloud_radius_squared": str(B*ay**2),
        "source_relative_weight_error": str(rx),
        "target_relative_weight_error": str(ry),
        "variance": str(s),
        "uniform_cross_label_condition": bool(cross),
        "actual_contraction_required": True,
        "within_cloud_contraction_is_not_inferred": True,
    }
    if margin <= 0:
        return dict(record, status="UNRESOLVED", reason="no positive spherical reserve")
    eta = margin/(2*t)
    cutoff = 44*B*t*t/eta
    fail_unless(cutoff == 88*B*t**3/margin and cutoff > 8*B*t*t,
                "inconsistent endpoint budget")
    return dict(
        record,
        status=("SIGNED_CONTRACTIVE_CLOUD_FAMILY" if s >= cutoff else
                "CERTIFIED_ONLY_FOR_LARGER_VARIANCES"),
        spherical_gap=str(eta), variance_cutoff=str(cutoff),
        certified_variances="[variance_cutoff,infinity)",
        certified_thresholds="[0,infinity)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    args = parser.parse_args()
    with open(args.input) as handle:
        result = produce(json.load(handle))
    print(json.dumps(result, sort_keys=True, indent=2))
