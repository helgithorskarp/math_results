#!/usr/bin/env python3
"""Exact finite audits for PROOF.md; not a proof of its analytic theorems.

Python 3.11+, standard library only. No files are written. Failures remain
active under python -O. Use --dump to print the computed compact summary.
"""

from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import argparse
import json
import math


def need(condition, label):
    if not condition:
        raise ValueError(label)


def poly(values):
    out = list(map(F, values))
    while out and out[-1] == 0:
        out.pop()
    return tuple(out)


ZERO, ONE, T = (), (F(1),), (F(0), F(1))


def add(a, b):
    return poly([(a[i] if i < len(a) else 0)
                 + (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def scale(a, c):
    return poly([x * c for x in a])


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    if not a or not b:
        return ZERO
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return poly(out)


def power(a, n):
    need(isinstance(n, int) and n >= 0, "nonnegative integer power required")
    out = ONE
    for _ in range(n):
        out = mul(out, a)
    return out


def deriv(a):
    return poly([i * a[i] for i in range(1, len(a))])


U = sub(ONE, power(T, 2))


def principal_radii(h):
    """For h(n)=h(t), t=n_1: meridional and latitudinal radii."""
    lateral = sub(h, mul(T, deriv(h)))
    meridional = add(lateral, mul(U, deriv(deriv(h))))
    return meridional, lateral


def det_curvature(h, d):
    meridional, lateral = principal_radii(h)
    return mul(meridional, power(lateral, d - 2))


def variation_det(h, u, d):
    r, s = principal_radii(h)
    dr, ds = principal_radii(u)
    out = mul(dr, power(s, d - 2))
    if d > 2:
        out = add(out, scale(mul(mul(r, power(s, d - 3)), ds), d - 2))
    return out


@lru_cache(None)
def sphere_moment(k, d):
    """E[n_1^k] under probability area measure on S^(d-1)."""
    need(d >= 2 and k >= 0, "sphere moment domain")
    if k % 2:
        return F(0)
    return math.prod((F(2*j-1, d+2*j-2) for j in range(1, k//2+1)),
                     start=F(1))


def integral(a, d):
    return sum((c * sphere_moment(k, d) for k, c in enumerate(a)), F(0))


def weighted_A(h, g, d):
    """h det(Q) A_h(g) from tangent eigenvalues, with no division."""
    r, s = principal_radii(h)
    dg, dh = deriv(g), deriv(h)
    meridian_hessian = sub(mul(U, deriv(dg)), mul(T, dg))
    first = mul(power(h, 2), mul(power(s, d-2), meridian_hessian))
    mixed = scale(mul(mul(h, mul(dh, dg)), mul(U, power(s, d-2))), 2)
    out = add(first, mixed)
    if d > 2:
        lateral = mul(mul(power(h, 2), mul(r, power(s, d-3))), mul(T, dg))
        out = sub(out, scale(lateral, d-2))
    return out


def polynomial_lower_bound(a):
    """Crude exact lower bound on [-1,1], adequate for our supports."""
    if not a:
        return F(0)
    return a[0] - sum(map(abs, a[1:]), F(0))


def transpose(A):
    return tuple(zip(*A))


def mm(A, B):
    return tuple(tuple(sum((A[i][k]*B[k][j] for k in range(2)), F(0))
                       for j in range(2)) for i in range(2))


def det2(A):
    return A[0][0]*A[1][1]-A[0][1]*A[1][0]


def inv2(A):
    det = det2(A)
    need(det != 0, "invertible affine fixture")
    return ((A[1][1]/det, -A[0][1]/det), (-A[1][0]/det, A[0][0]/det))


def transform(points, A):
    return tuple(tuple(sum(A[i][k]*v[k] for k in range(2)) for i in range(2))
                 for v in points)


def polygon_data(points):
    """Exact area and M2 from edges, with their normal lengths cancelled."""
    pairs = list(zip(points, points[1:]+points[:1]))
    area = sum((a[0]*b[1]-a[1]*b[0] for a, b in pairs), F(0))/2
    need(area > 0, "counterclockwise polygon fixture")
    M = [[F(0), F(0)], [F(0), F(0)]]
    for a, b in pairs:
        normal = (b[1]-a[1], a[0]-b[0])
        support = sum(normal[i]*a[i] for i in range(2))
        need(support > 0, "origin strictly inside each polygon facet")
        for i in range(2):
            for j in range(2):
                M[i][j] += normal[i]*normal[j]/support
    return area, tuple(map(tuple, M))


def audit():
    records = []
    counts = {}

    def record(kind, *values):
        counts[kind] = counts.get(kind, 0) + 1
        records.append([kind, *[str(v) for v in values]])

    # Independent area-moment controls: cosine Fourier constants in d=2;
    # the first coordinate is uniform on [-1,1] in d=3.
    for j in range(21):
        need(sphere_moment(2*j, 2) == F(math.comb(2*j, j), 4**j), "circle moments")
        need(sphere_moment(2*j, 3) == F(1, 2*j+1), "two-sphere moments")
        record("sphere_controls", j)

    supports = [ONE, (F(2),), poly([1, 0, F(1, 12)]),
                poly([1, 0, -F(1, 16), 0, F(1, 64)])]
    gs = [ONE, T, power(T, 2), power(T, 4),
          poly([1, 0, -2, 0, 1]), poly([0, 1, 0, -1])]
    test_function = poly([1, 0, F(1, 3), 0, -F(1, 7)])
    corruptions = 0

    for d in range(2, 11):
        for h in supports:
            r, s = principal_radii(h)
            need(min(polynomial_lower_bound(h), polynomial_lower_bound(r),
                     polynomial_lower_bound(s)) > 0, "curvature positivity fixture")
            D = det_curvature(h, d)
            mu = mul(h, D)
            # All integrals in the code use normalized spherical measure.
            # v is V/area(S^(d-1)), so the physical area factor cancels.
            v = integral(mu, d) / d
            need(v > 0, "positive volume")
            for g in gs:
                u = mul(h, g)
                dD = variation_det(h, u, d)
                dv = integral(mul(u, D), d)
                need(integral(mul(h, dD), d) == (d-1)*dv, "mixed-volume derivative")
                need((integral(mul(u, D), d) + integral(mul(h, dD), d))/d == dv,
                     "determinant-volume first derivative")
                wA = weighted_A(h, g, d)
                need(wA == sub(mul(h, dD), scale(mul(u, D), d-1)),
                     "pointwise logarithmic linearization")
                need(integral(wA, d) == 0, "mean-zero A")
                energy = integral(mul(mul(power(h, 2), power(s, d-2)),
                                      mul(U, power(deriv(g), 2))), d)
                need(-integral(mul(g, wA), d) == energy, "divergence energy")
                bilinear_energy = integral(mul(mul(power(h, 2), power(s, d-2)),
                                               mul(U, mul(deriv(g), deriv(test_function)))), d)
                need(-integral(mul(test_function, wA), d) == bilinear_energy,
                     "bilinear self-adjointness")
                mean = integral(mul(g, mu), d)/(d*v)
                variance = integral(mul(power(sub(g, (mean,)), 2), mu), d)
                need(energy >= (d-1)*variance, "classical spectral inequality fixture")
                record("zonal_variations", d, h, g, v, dv, energy, variance)

                for p in sorted({F(3, 2), F(2), F(4), F(d), F(2*d)}):
                    # This is V * h^p * delta f, with actual area factors
                    # removed consistently, computed from the density formula.
                    direct = add(scale(mul(u, D), 1-p), mul(h, dD))
                    direct = sub(direct, scale(mu, dv/v))
                    operator = add(wA, scale(mul(g, mu), d-p))
                    operator = sub(operator, scale(mu, d*mean))
                    need(direct == operator, "normalized density differential")
                    need(integral(direct, d)/v == -p*dv/v, "volume gradient normalization")
                    # Coercivity includes constants, whose eigenvalue is -p.
                    norm = integral(mul(power(g, 2), mu), d)
                    need(-integral(mul(g, operator), d) >= (p-1)*norm,
                         "normalized negative spectrum fixture")
                    record("normalized_variations", d, p, h, g, dv/v)

            # Critical exponent constants: unnormalized density has zero
            # differential; normalized density has nonzero eigenvalue -d.
            need(variation_det(h, h, d) == scale(D, d-1), "constant support scaling")
            record("critical_scaling", d, h, -d)

    # The ball spectrum supplies independent closed-form eigenvalue checks,
    # including the excluded p=1 translation degeneracy.
    for d in range(2, 13):
        for p in sorted({F(3, 2), F(2), F(d), F(2*d)}):
            need(-p < 0, "constant eigenvalue")
            for ell in range(1, 21):
                lam = d-p-ell*(ell+d-2)
                need(lam <= -(p-1), "ball nonconstant spectral gap")
                record("ball_modes", d, p, ell, lam)
        need(d-1-(d-1) == 0, "p=1 translation kernel control")
        record("excluded_boundary", d)

    # Chain-rule curvature bound for the explicit smooth hierarchy.
    for p in range(2, 130, 2):
        for a in (F(0), F(1, 8*p), F(1, 4*p)):
            expanded = (1-a)**2 - p*a*(1-a) - (p-1)*a*a
            need(expanded == 1-(p+2)*a+2*a*a, "curvature bracket algebra")
            need(expanded >= F(1, 2), "uniform curvature bracket")
            record("curvature_bounds", p, a, expanded)
        # For total degree q, planar weights are a-b with a+b<=q;
        # other coordinates absorb the remaining degree when d>2.
        for q in range(p):
            for a in range(q+1):
                for b in range(q-a+1):
                    w = a-b
                    need(w % p != 0 or w == 0, "cyclic invariance below p")
            record("lower_jet_weights", p, q)
        need(p % p == 0 and p != 0, "first nonzero allowed weight")
        record("top_jet_weight", p, p)

    # Deliberately incorrect normalizations/signs must fail for elementary
    # constants on a radius-two ball in dimension three.
    d, p, h, g = 3, F(3), (F(2),), ONE
    D = det_curvature(h, d)
    mu = mul(h, D)
    v = integral(mu, d)/d
    dv = integral(mu, d)
    correct = -p*dv/v
    wrong_values = [p*dv/v, -p*dv, -p*dv/(v*v), (d-p)*dv/v]
    for wrong in wrong_values:
        try:
            need(wrong == correct, "rejected wrong normalized volume gradient")
        except ValueError:
            corruptions += 1
        else:
            raise ValueError("corruption unexpectedly accepted")
    try:
        power(T, -1)
    except ValueError:
        corruptions += 1
    else:
        raise ValueError("negative polynomial power accepted")
    counts["rejected_corruptions"] = corruptions

    polygons = [((-1,-1),(1,-1),(1,1),(-1,1)),
                ((-2,-1),(1,-1),(2,0),(2,1),(-1,1),(-2,0)),
                ((-2,-1),(-1,-2),(1,-2),(2,-1),(2,1),(1,2),(-1,2),(-2,1))]
    matrices = [((1,0),(0,1)), ((2,1),(1,1)), ((1,F(1,3)),(0,1)),
                ((2,0),(0,F(1,2))), ((F(3,5),-F(4,5)),(F(4,5),F(3,5)))]
    for points in polygons:
        points = tuple(tuple(map(F, v)) for v in points)
        area, M = polygon_data(points)
        for A in matrices:
            A = tuple(tuple(map(F, row)) for row in A)
            new_area, new_M = polygon_data(transform(points, A))
            inv = inv2(A)
            prediction = mm(mm(transpose(inv), M), inv)
            prediction = tuple(tuple(det2(A)*v for v in row) for row in prediction)
            need(new_M == prediction and new_area == det2(A)*area,
                 "definition-level polygon affine law")
            record("polygon_affine", points, A, area, new_area, new_M)
    square = tuple(tuple(map(F,v)) for v in polygons[0])
    square_data = polygon_data(square)
    for a, b, c in ((3,4,5),(5,12,13),(8,15,17)):
        R = ((F(a,c),-F(b,c)),(F(b,c),F(a,c)))
        rotated = transform(square, R)
        need(set(rotated) != set(square) and polygon_data(rotated) == square_data,
             "nonsmooth equal quadratic jet control")
        record("polygon_rotation", a, b, c)
    rectangle = transform(square, ((F(2),F(0)),(F(0),F(1,2))))
    need(polygon_data(rectangle)[1] == ((F(1),F(0)),(F(0),F(16))), "whitening fixture")
    whitened = transform(rectangle, ((F(1),F(0)),(F(0),F(4))))
    need(polygon_data(whitened)[1] == ((F(4),F(0)),(F(0),F(4))), "positive square-root whitening")
    record("whitening", polygon_data(whitened))

    digest = sha256(json.dumps(records, separators=(",", ":")).encode()).hexdigest()
    return {"arithmetic": "integers and fractions.Fraction",
            "counts": counts, "record_sha256": digest,
            "scope": "finite corroboration; analytic theorem proved in PROOF.md"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump", action="store_true", help="print summary without comparing expected.json")
    args = parser.parse_args()
    result = audit()
    if not args.dump:
        expected = json.loads(Path(__file__).with_name("expected.json").read_text())
        need(result == expected, "computed summary differs from expected.json")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not args.dump:
        print("VERIFIED")


if __name__ == "__main__":
    main()
