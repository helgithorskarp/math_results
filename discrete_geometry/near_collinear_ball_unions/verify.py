#!/usr/bin/env python3
"""Exact finite audits for PROOF.md; not a proof of its universal theorem.

Standard library only. All geometric predicates and integrations use integers
or fractions. Run with --write-expected only to regenerate the compact fixture.
"""

from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import comb
from pathlib import Path
import argparse
import json


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def sqdist(a, b):
    check(len(a) == len(b), "coordinate dimension mismatch")
    return sum((x - y) ** 2 for x, y in zip(a, b))


def runs(bits):
    return sum(x and (i == 0 or not bits[i - 1])
               for i, x in enumerate(bits))


def theta(R, u, v):
    R, u, v = map(F, (R, u, v))
    check(R > 0 and u > 0 and v > 0, "positive radius and gaps required")
    return u * v / (4 * R) if max(u, v) <= 2 * R else (u + v) / 2 - R


def containment_from_lens(R, u, v, epsilon):
    """Evaluate the direct expanded-lens maximum, without calling theta."""
    r = R + epsilon
    a, m = (u + v) / 2, (v - u) / 2
    if r < a:
        return True
    # Maximal squared middle distance: bisector coordinate m, height^2 r^2-a^2.
    M2 = m * m + r * r - a * a
    return epsilon <= R and M2 <= (R - epsilon) ** 2


def audit_masks():
    total = connected = 0
    for n in range(1, 13):
        for mask in range(1 << n):
            bits = [(mask >> i) & 1 for i in range(n)]
            vertex_edge = sum(bits) - sum(bits[i] * bits[i + 1]
                                         for i in range(n - 1))
            r = runs(bits)
            check(vertex_edge == r, "run identity")
            check(vertex_edge >= bool(mask), "universal path upper bound")
            check((vertex_edge == bool(mask)) == (r <= 1), "equality condition")
            connected += bool(mask) and r == 1
            total += 1
    return {"all_masks": total, "nonempty_interval_masks": connected}


def audit_radius():
    total = boundary_failures = 0
    R = F(1)
    for U, V in product(range(1, 17), repeat=2):
        u, v = F(U, 4), F(V, 4)
        t = theta(R, u, v)
        for factor in (F(0), F(1, 2), F(1), F(3, 2), F(2)):
            e = factor * t
            actual = containment_from_lens(R, u, v, e)
            expected = e < t or (e == t and max(u, v) <= 2 * R)
            check(actual == expected, "sharp radius/lens comparison")
            if e == t and not actual:
                boundary_failures += 1
            total += 1
        for du, dv in ((F(1, 7), 0), (0, F(1, 7)), (F(1, 7), F(2, 7))):
            check(theta(R, u + du, v + dv) >= t, "gap monotonicity")
    # Exact pointwise identity underlying the simpler sufficient bound.
    identities = 0
    for d in (2, 3, 5):
        for u, v in product((F(1, 3), F(1), F(5, 2)), repeat=2):
            lam = u / (u + v)
            left = (-u,) + (F(0),) * (d - 1)
            right = (v,) + (F(0),) * (d - 1)
            mid = (F(0),) * d
            for shift in range(-4, 5):
                x = tuple(F(shift + j, j + 2) for j in range(d))
                check(sqdist(x, mid) == (1 - lam) * sqdist(x, left)
                      + lam * sqdist(x, right) - u * v,
                      "squared-norm interpolation")
                identities += 1
    return {"lens_threshold_cases": total,
            "closed_boundary_pointwise_failures": boundary_failures,
            "interpolation_identities": identities}


def symmetric_witness(gamma, rational_parameter):
    """R=1. Rational parametrization r^2-h^2=gamma^2."""
    t = F(rational_parameter)
    gamma = F(gamma)
    r = gamma * (1 / t + t) / 2
    h = gamma * (1 / t - t) / 2
    eta = r - 1
    c = [(-gamma, F(0)), (F(0), F(0)), (gamma, F(0))]
    x = (F(0), h)
    p = [tuple(z + eta / r * (w - z) for z, w in zip(c[0], x)),
         (F(0), -eta),
         tuple(z + eta / r * (w - z) for z, w in zip(c[2], x))]
    check(r > 0 and h > 0 and eta > 0, "witness parameters")
    check(all(sqdist(p[i], c[i]) == eta ** 2 for i in range(3)),
          "witness displacement")
    check(sqdist(x, p[0]) == sqdist(x, p[2]) == 1,
          "witness outer boundaries")
    check(sqdist(x, p[1]) == (h + eta) ** 2, "middle distance")
    return eta, c, p, x


def audit_witnesses():
    eta, _, p, x = symmetric_witness(1, F(1, 2))
    check(eta == F(1, 4) and sqdist(x, p[1]) == 1,
          "short-gap sharp boundary")
    witnesses = []
    for gamma, t in ((F(1), F(12, 25)), (F(1), F(1, 3)),
                     (F(3), F(1, 2)), (F(3), F(2, 3))):
        eta, _, p, x = symmetric_witness(gamma, t)
        check(eta > theta(1, gamma, gamma), "outside the proved tube")
        check(sqdist(x, p[1]) > 1, "missing middle at witness")
        # Find a strictly interior rational point. This finite check supports
        # the proof's open-set argument, rather than testing only a boundary.
        for exponent in range(2, 30):
            z = (x[0], x[1] - F(1, 2 ** exponent))
            if sqdist(z, p[0]) < 1 and sqdist(z, p[2]) < 1 and sqdist(z, p[1]) > 1:
                break
        else:
            raise RuntimeError("strict witness not found")
        witnesses.append({"gamma": str(gamma), "displacement": str(eta),
                          "threshold": str(theta(1, gamma, gamma)),
                          "strict_point": list(map(str, z)),
                          "squared_distances": [str(sqdist(z, q)) for q in p]})
    # At the long-gap boundary, the label hole has zero volume: outer tangency.
    c = [(-F(1), F(0)), (F(0), F(0)), (F(3), F(0))]
    p = [(F(0), F(0)), (-F(1), F(0)), (F(2), F(0))]
    x = (F(1), F(0))
    check(theta(1, 1, 3) == 1, "long-gap threshold")
    check(all(sqdist(c[i], p[i]) == 1 for i in range(3)), "boundary norm")
    check([sqdist(x, q) for q in p] == [1, 4, 1], "boundary label hole")
    return {"strict_rational_witnesses": witnesses,
            "pointwise_boundary_controls": 2}


def cross_section_primitive(k, R, x):
    """Integral_0^x (R^2-t^2)^k dt, normalized by kappa_(2k)."""
    return sum(F((-1) ** j * comb(k, j), 2 * j + 1)
               * R ** (2 * (k - j)) * x ** (2 * j + 1)
               for j in range(k + 1))


def ball_volume(k, R):
    return 2 * cross_section_primitive(k, R, R)


def phi(k, R, s):
    s = min(F(s), 2 * R)
    return sum(F((-1) ** j * comb(k, j), 4 ** j * (2 * j + 1))
               * R ** (2 * (k - j)) * s ** (2 * j + 1)
               for j in range(k + 1))


def collinear_volume(k, R, coords):
    """Independent direct axial integration on nearest-center cells."""
    coords = sorted(set(map(F, coords)))
    total = F(0)
    for i, c in enumerate(coords):
        lo = -R if i == 0 else max(-R, (coords[i - 1] - c) / 2)
        hi = R if i == len(coords) - 1 else min(R, (coords[i + 1] - c) / 2)
        check(lo <= hi, "nearest-center interval")
        total += cross_section_primitive(k, R, hi) - cross_section_primitive(k, R, lo)
    return total


def generalized_binomial(a, n):
    value = F(1)
    for j in range(n):
        value *= (a - j) / (j + 1)
    return value


def audit_caps_and_hessian():
    caps = hessians = slices = 0
    for k, R in product(range(1, 5), (F(1), F(3, 2), F(3))):
        for j in range(25):
            s = R * F(j, 8)
            overlap = (2 * (cross_section_primitive(k, R, R)
                           - cross_section_primitive(k, R, s / 2))) if s <= 2 * R else F(0)
            check(phi(k, R, s) == ball_volume(k, R) - overlap, "two-cap formula")
            caps += 1
        for j in range(1, 16):
            g = R * F(j, 8)
            # Expand Phi(sqrt(g^2+q)) directly by generalized binomials.
            coefficient = sum(F((-1) ** z * comb(k, z), 4 ** z * (2 * z + 1))
                              * R ** (2 * (k - z)) * g ** (2 * z - 1)
                              * generalized_binomial(F(2 * z + 1, 2), 1)
                              for z in range(k + 1))
            predicted = (R * R - g * g / 4) ** k / (2 * g)
            check(coefficient == predicted, "transverse quadratic coefficient")
            hessians += 1
        for coords in ((0,), (0, 0), (0, 1, 2, 3), (-4, -1, 0, 2, 7),
                       (0, R, 3 * R, 6 * R), (0, R / 3, R / 2, R)):
            sorted_coords = sorted(map(F, coords))
            predicted = ball_volume(k, R) + sum(phi(k, R, b - a)
                                                for a, b in zip(sorted_coords, sorted_coords[1:]))
            check(collinear_volume(k, R, coords) == predicted, "direct axial integration")
            slices += 1
    # A direct volume failure beyond the long-gap radius. Here center order
    # has changed; the direct integration re-sorts, the tested path does not.
    k, R = 1, F(1)
    coords = [F(1, 2), -F(3, 2), F(3, 2)]
    actual = collinear_volume(k, R, coords)
    path = ball_volume(k, R) + sum(phi(k, R, abs(b - a))
                                  for a, b in zip(coords, coords[1:]))
    check(path - actual == F(5, 12), "strict volume counterexample to enlarged tube")
    # At the closed long-gap radius, the same integration gives equality.
    coords_boundary = [F(0), -F(1), F(2)]
    path_boundary = ball_volume(k, R) + sum(phi(k, R, abs(b - a))
                                           for a, b in zip(coords_boundary, coords_boundary[1:]))
    check(path_boundary == collinear_volume(k, R, coords_boundary), "closed volume boundary")
    return {"two_cap_identities": caps, "hessian_coefficients": hessians,
            "direct_axial_integrations": slices,
            "long_gap_failure_volume_over_pi": str(path - actual),
            "long_gap_closed_boundary_volume_over_pi": str(path_boundary)}


def audit_point_memberships():
    outputs = []
    for d in (2, 3):
        R = 32
        centers = []
        for i in range(5):
            # Displacements have norm at most sqrt(3)<2=tau.
            centers.append((16 * i + (-1) ** i,)
                           + tuple((-1) ** (i + j) for j in range(1, d)))
        check(theta(R, 16, 16) == 2, "grid tube")
        hist = Counter()
        points = product(range(-34, 101, 2), *([range(-34, 35, 2)] * (d - 1)))
        count = 0
        for point in points:
            bits = [sqdist(point, center) <= R * R for center in centers]
            check(runs(bits) <= 1, "noninterval membership in exact grid")
            mask = sum(int(b) << i for i, b in enumerate(bits))
            hist[mask] += 1
            count += 1
        check(any(mask.bit_count() >= 3 for mask in hist), "multiple-overlap control")
        outputs.append({"dimension": d, "grid_points": count,
                        "membership_histogram": {str(k): hist[k] for k in sorted(hist)}})
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-expected", action="store_true")
    args = parser.parse_args()
    result = {"status": "PASS", "arithmetic": "exact integers and fractions",
              "scope": "finite audits; universal theorem is the written proof",
              "masks": audit_masks(), "radius": audit_radius(),
              "witnesses": audit_witnesses(), "caps": audit_caps_and_hessian(),
              "point_memberships": audit_point_memberships()}
    encoded = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    expected = Path(__file__).with_name("EXPECTED.json")
    if args.write_expected:
        expected.write_bytes(encoded)
    else:
        check(encoded == expected.read_bytes(), "EXPECTED.json mismatch")
    print("PASS: masks, sharp radius, rational witnesses, caps, Hessian, exact memberships")
    print("EXPECTED.json SHA256:", sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()
