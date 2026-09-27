"""Rational support-cover certificate for a uniform eventual Gaussian sign.

The actual cloud pair must be a contraction. The spherical sign theorem is
a written dependency; this program checks finite data and quantitative guards.
"""
import argparse
from fractions import Fraction as F
import json
from math import lcm


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rational(value):
    require(type(value) in (int, str), "integer or rational string required")
    return F(value)


def norm2(v):
    return sum(z*z for z in v)


def centered(points):
    mean = [sum(v[k] for v in points)/len(points) for k in range(3)]
    return [[v[k]-mean[k] for k in range(3)] for v in points]


def width_enclosure(x, y, radius, mesh, bits):
    """Six cube faces cover S2. All cell contributions are rounded down."""
    normalized = [[v/radius for v in row] for row in x+y]
    den = lcm(*(v.denominator for row in normalized for v in row))
    integer = [[int(v*den) for v in row] for row in normalized]
    xx, yy = integer[:len(x)], integer[len(x):]
    scale, total = 1 << bits, 0
    for axis in range(3):
        other = [k for k in range(3) if k != axis]
        for sign in (-1, 1):
            for a in range(1-mesh, mesh, 2):
                for b in range(1-mesh, mesh, 2):
                    v = [0, 0, 0]
                    v[axis], v[other[0]], v[other[1]] = sign*mesh, a, b
                    gap = max(sum(z*w for z, w in zip(row, v)) for row in xx)
                    gap -= max(sum(z*w for z, w in zip(row, v)) for row in yy)
                    q = mesh*mesh+a*a+b*b
                    total += (scale*4*mesh*gap)//(den*q*q)
    integral_lower = F(total, scale)-F(480, mesh)
    # Division by 16 uses pi<4 and is valid here only for a positive numerator.
    delta = radius*integral_lower/16 if integral_lower > 0 else None
    return dict(mesh=mesh, rounding_bits=bits, face_cells=6*mesh*mesh,
                normalized_floor_sum=total, normalized_integral_lower=str(integral_lower),
                reference_width_lower=None if delta is None else str(delta))


def produce(data):
    x = [[rational(v) for v in row] for row in data["sources"]]
    y = [[rational(v) for v in row] for row in data["targets"]]
    p = list(map(rational, data["weights"]))
    require(p and len(x) == len(y) == len(p) and all(len(v) == 3 for v in x+y),
            "matching nonempty three-dimensional lists required")
    require(all(w >= 0 for w in p) and sum(p) == 1, "probability weights required")
    keep = [i for i, w in enumerate(p) if w > 0]
    x, y, p = [[a[i] for i in keep] for a in (x, y, p)]
    x, y = centered(x), centered(y)
    R0, r, rho = [rational(data[k]) for k in
                   ("reference_radius", "cloud_radius", "relative_weight_error")]
    require(R0 > 0 and r >= 0 and 0 <= rho <= F(1, 2), "invalid radius/prior range")
    require(all(norm2(v) <= R0*R0 for v in x+y), "invalid reference support radius")
    mesh = data["mesh"]
    require(type(mesh) is int and mesh >= 1, "positive integer mesh required")
    bits = data.get("rounding_bits", max(32, 4*mesh.bit_length()))
    require(type(bits) is int and bits >= 1, "positive integer rounding precision required")
    D0 = F(0)
    for i in range(len(p)):
        for j in range(i):
            loss = norm2([a-b for a, b in zip(x[i], x[j])])
            loss -= norm2([a-b for a, b in zip(y[i], y[j])])
            require(loss >= 0, "reference pair expands")
            D0 += 2*p[i]*p[j]*loss
    width = width_enclosure(x, y, R0, mesh, bits)
    R = R0+r
    d = (1-rho)**2*D0-16*R0*r-8*r*r
    q = (1-rho)*min(p)
    k = max(0, q.denominator.bit_length()-q.numerator.bit_length())
    if (q.numerator << k) < q.denominator:
        k += 1
    out = dict(schema="support-cap-localization-v1", active_sites=len(p),
               width=width, reference_radius=str(R0), reference_loss=str(D0),
               cloud_radius=str(r), relative_weight_error=str(rho),
               actual_radius=str(R), actual_loss_lower=str(d),
               aggregate_mass_lower=str(q), mass_exponent=k,
               actual_cloud_contraction_required=True,
               common_label_weights_required=True,
               analytical_premise="universal spherical comparison6494 and endpoint6032/6048")
    if width["reference_width_lower"] is None:
        return dict(out, status="UNRESOLVED", reason="width not certified at this mesh")
    b = F(width["reference_width_lower"])-2*r
    out["tail_slope_lower"] = str(b)
    if b <= 0 or d <= 0:
        return dict(out, status="UNRESOLVED", reason="nonpositive width or loss reserve")
    value = R*(k+1)/b
    N = max(1, -(-value.numerator//value.denominator))
    prefactor = 2112*R**4/d
    require(d <= 4*R*R and N*b >= R*(k+1), "inconsistent endpoint schedule")
    return dict(out, status="CERTIFIED_UNIFORM_EVENTUAL_FAMILY", tail_join=N,
                variance_cutoff=dict(prefactor=str(prefactor), power_of_two=8*N),
                certified_thresholds="[0,infinity)",
                certified_variances="[prefactor*2^power_of_two,infinity)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    args = parser.parse_args()
    with open(args.input) as stream:
        record = produce(json.load(stream))
    print(json.dumps(record, sort_keys=True, indent=2))
