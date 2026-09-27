#!/usr/bin/env python3
"""Exact controls and symbolic budgets; no contact-volume/sign oracle."""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from math import isqrt, factorial
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent


def require(test, message):
    if not test:
        raise ValueError(message)


def rational(x, name):
    require(type(x) in (int, Q), name + " must be an exact integer/Fraction")
    return Q(x)


def positive(x, name):
    x = rational(x, name)
    require(x > 0, name + " must be positive")
    return x


def integer(x, name, lower=1):
    require(type(x) is int and x >= lower, name + " outside integer domain")
    return x


def ceilq(x):
    x = rational(x, "ceiling input")
    return -(-x.numerator // x.denominator)


def pow2(k):
    return Q(1 << k) if k >= 0 else Q(1, 1 << (-k))


def ceil_log2(x):
    x = positive(x, "logarithm input")
    k = x.numerator.bit_length() - x.denominator.bit_length()
    return k if x <= pow2(k) else k + 1


def ceil_sqrt(x):
    x = rational(x, "square root input")
    require(x >= 0, "negative square root")
    k = isqrt(x.numerator // x.denominator)
    return k if k * k == x else k + 1


def parameters(R, S, J):
    integer(R, "R")
    integer(J, "J")
    S = positive(S, "S")
    require(S >= 1, "normalize the minimum variance to one first")
    U = ceil_sqrt(2 * S * J)
    return S, U, R + U


def tightened_budget(R, S, J, eta, delta):
    """For an ALREADY tightened adverse gap delta; counts are expanded."""
    S, U, B = parameters(R, S, J)
    eta = positive(eta, "eta")
    delta = positive(delta, "delta")
    m = ceil_sqrt(Q(3 * R * R, 8) / eta)
    N = 2 * (2 * B * m + 1) ** 3
    E = max(0, ceil_log2(Q(N * (32 * U + 64)) / delta))
    return dict(U=U, B=B, m=m, atom_cap=N, variance_exponent=E)


def contact_budget(R, S, J, delta):
    """For an UNTIGHTENED adverse gap delta. All large powers symbolic.

    Nbar=2^n, eta=2^-t, m=2^v; see PROOF.md (14)--(18).
    Rational geometry needs the extra rational convex-hull presentation.
    """
    S, U, B = parameters(R, S, J)
    delta = positive(delta, "delta")
    B0 = 2 * R + ceil_sqrt(2 * (J + 1))
    r = 32 * B0 * B0 - 1
    C = 48 * S * S * B0 ** 3
    b0 = max(0, ceil_log2(4 * C / delta))
    t = max(1, J + 3 + r * b0)
    v = ceil_log2(R) + (t + 1) // 2
    n = 6 + 3 * ceil_log2(B) + 3 * v
    E = max(0, n + ceil_log2(Q(2 * (32 * U + 64)) / delta))
    ell = max(0, n + ceil_log2(Q(192 * U * U) / delta))
    M_exp = ell + ceil_log2(6 * R)
    ER = max(0, n + ceil_log2(Q(4 * (32 * U + 64)) / delta))
    # W = 2^(U^2 * 2^ER + addend). Never expand 2^ER or W.
    addend = 2 * n + 5 + max(0, ceil_log2(64 / delta))
    return dict(U=U, B=B, B0=B0, strip_exponent_denominator=r,
                C=str(C), strip_ratio_exponent=b0, eta_exponent=t,
                grid_denominator_exponent=v, atom_cap_exponent=n,
                variance_exponent=E, rational_error_exponent=ell,
                barycentric_denominator_exponent=M_exp,
                rational_variance_exponent=ER,
                prior_denominator_exponent=dict(
                    power_of_two_exponent=ER, multiplier=U * U,
                    addend=addend), adverse_datum_supplied=False)


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), Q(0))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def norm2(x):
    return dot(x, x)


def mean(points, weights):
    require(len(points) == len(weights), "support/weight mismatch")
    return tuple(sum((w * p[j] for p, w in zip(points, weights)), Q(0))
                 for j in range(3))


def round_simplex(weights, M):
    integer(M, "denominator")
    weights = tuple(rational(w, "weight") for w in weights)
    require(weights and min(weights) >= 0 and sum(weights) == 1,
            "weights must be a probability vector")
    first = tuple(Q((w * M).__floor__(), M) for w in weights[:-1])
    return first + (1 - sum(first),)


def controls():
    counts = {}
    logs = 0
    for d in range(1, 38):
        for n in range(1, 43):
            x = Q(n, d)
            k = ceil_log2(x)
            require(pow2(k - 1) < x <= pow2(k), "log ceiling")
            h = ceil_sqrt(x)
            require((h - 1) ** 2 < x <= h * h, "sqrt ceiling")
            logs += 1
    counts["exact_log_sqrt_pairs"] = logs

    grids = 0
    for B, m in ((2, 1), (3, 2), (6, 3), (9, 7)):
        # Include exterior faces, half-cell ties and their neighboring points.
        coords = {Q(-B), Q(B), Q(0)}
        coords.update(Q(i, 2 * m) for i in range(-2 * B * m, 2 * B * m + 1))
        coords.update(Q(i, 3 * m) for i in range(-3 * m, 3 * m + 1))
        for x in sorted(coords):
            z = Q((x * m + Q(1, 2)).__floor__(), m)
            require(-B <= z <= B and (x - z) ** 2 <= Q(1, 4 * m * m),
                    "nearest spatial grid point")
            grids += 1
        # Three simultaneous ties attain the exact Euclidean squared error.
        x = (Q(1, 2 * m),) * 3
        z = (Q(1, m),) * 3
        require(norm2(sub(x, z)) == Q(3, 4 * m * m), "3D grid constant")
    counts["grid_coordinates"] = grids

    points = [(Q(1), Q(0), Q(0)), (Q(-1), Q(0), Q(0)),
              (Q(0), Q(1), Q(0)), (Q(0), Q(0), Q(0))]
    weights = [(Q(1, 4),) * 4, (Q(1), Q(0), Q(0), Q(0)),
               (Q(1, 2), Q(1, 2), Q(0), Q(0)),
               (Q(1, 2**200), Q(0), Q(0), 1-Q(1, 2**200))]
    cov = 0
    for w in weights:
        c = mean(points, w)
        for vec in product((Q(-2), Q(0), Q(3)), repeat=3):
            var = sum(wi * dot(vec, sub(p, c)) ** 2 for p, wi in zip(points, w))
            second = sum(wi * dot(vec, p) ** 2 for p, wi in zip(points, w))
            pair = sum(wi * wj * dot(vec, sub(p, q)) ** 2
                       for p, wi in zip(points, w) for q, wj in zip(points, w)) / 2
            require(var == second-dot(vec, c)**2 == pair, "covariance identity")
            require(0 <= var <= norm2(vec), "posterior covariance cap")
            cov += 1
    counts["posterior_covariance_controls"] = cov

    A = [(Q(-3), Q(0), Q(0)), (Q(-2), Q(0), Q(0)),
         (Q(-3), Q(1), Q(0)), (Q(-3), Q(0), Q(1))]
    B = [tuple(-x for x in p) for p in A]
    IA = [tuple(p[j] + (1 if j == 0 else 0) for j in range(3)) for p in A]
    IB = [tuple(p[j] - (1 if j == 0 else 0) for j in range(3)) for p in B]
    for P, QP in ((A, IA), (B, IB)):
        require(all(norm2(sub(p, q)) == norm2(sub(u, v))
                    for p, u in zip(P, QP) for q, v in zip(P, QP)), "block rigidity")
    losses = [[norm2(sub(p, q))-norm2(sub(u, v))
               for q, v in zip(B, IB)] for p, u in zip(A, IA)]
    require(min(min(row) for row in losses) > 0, "cross contraction control")
    bary = 0
    for w, v in product(weights, repeat=2):
        lhs = norm2(sub(mean(A, w), mean(B, v)))-norm2(sub(mean(IA, w), mean(IB, v)))
        rhs = sum(wi * vj * losses[i][j] for i, wi in enumerate(w) for j, vj in enumerate(v))
        require(lhs == rhs and lhs >= 0, "whole-hull barycentric identity")
        bary += 1
    counts["barycentric_contractions"] = bary

    rounded = 0
    for M in (1, 7, 137, 888):
        for w in weights + [(Q(17, 137), Q(31, 137), Q(42, 137), Q(47, 137))]:
            wp = round_simplex(w, M)
            tv = sum(abs(u-v) for u, v in zip(w, wp))
            error = sub(mean(A, w), mean(A, wp))
            image_error = sub(mean(IA, w), mean(IA, wp))
            require(tv <= Q(6, M), "four-vertex rounding")
            require(norm2(error) <= Q(24, M)**2, "radius-four centre error")
            require(norm2(error) == norm2(image_error), "rigid rounding error")
            rounded += 1
    counts["rational_barycentre_roundings"] = rounded

    shells = 0
    for e in (Q(1, 100), Q(1, 7), Q(1), Q(5)):
        for radius in (Q(0), e, 2*e, Q(5, 2)*e, 3*e, 4*e, 17*e, Q(10)):
            rp = Q(0) if radius <= 2*e else e*((radius/e).__floor__()-1)
            if rp:
                require(radius-2*e <= rp <= radius-e, "rational inner radius")
            require(radius**3-max(Q(0), radius-3*e)**3 <= 9*radius**2*e,
                    "shell-volume polynomial bound")
            shells += 1
    counts["shell_and_radius_controls"] = shells

    strip = 0
    for R, J in ((1, 1), (1, 3), (2, 1), (2, 5)):
        B0 = 2*R + ceil_sqrt(2*(J+1))
        m0 = 16*B0*B0
        # Definition-level factorial remainder; independent of the loose estimate.
        require(Q((2*B0*B0)**m0, factorial(m0)) <= pow2(-J-2), "strip remainder")
        strip += 1
    counts["direct_strip_remainders"] = strip

    schedules = []
    for R, S, J, delta in ((1, Q(4), 3, Q(1,100)), (2, Q(1), 1, Q(1,16)),
                           (1, Q(3,2), 4, Q(1,2**200)), (8, Q(16), 10, Q(1,256)),
                           (1, Q(1), 1, Q(2**30))):
        d = contact_budget(R, S, J, delta)
        b0, r, t, v, n = (d[k] for k in ("strip_ratio_exponent", "strip_exponent_denominator",
                            "eta_exponent", "grid_denominator_exponent", "atom_cap_exponent"))
        C = Q(d["C"])
        require(C*pow2(-b0) <= delta/4 and t >= J+3+r*b0, "source strip allowance")
        require(2*v >= t+2*ceil_log2(R), "posterior cover allowance")
        require(n >= 6+3*ceil_log2(d["B"])+3*v, "atom-count allowance")
        U = d["U"]
        require(pow2(d["variance_exponent"]-n) >= 2*(32*U+64)/delta, "variance allowance")
        require(pow2(d["rational_error_exponent"]-n) >= 192*U*U/delta, "shell allowance")
        require(pow2(d["barycentric_denominator_exponent"]-d["rational_error_exponent"]) >= 6*R,
                "centre allowance")
        require(pow2(d["rational_variance_exponent"]-n) >= 4*(32*U+64)/delta,
                "rounded variance allowance")
        add = d["prior_denominator_exponent"]["addend"]-2*n-5
        require(pow2(add) >= 64/delta, "prior allowance")
        schedules.append(dict(R=R, S=str(S), J=J, delta=str(delta), **d))

    tb = tightened_budget(1, Q(4), 3, Q(1,16), Q(1,100))
    require((tb["U"], tb["B"], tb["m"], tb["atom_cap"]) == (5,6,3,101306),
            "small tightened illustrative count")
    w = (Q(1,3), Q(1,7), Q(11,21))
    h_lower, delta = Q(1,16), Q(1,10)
    W = ceilq(64*len(w)/(h_lower*delta))
    wp = round_simplex(w, W)
    tv = sum(abs(x-y) for x, y in zip(w, wp))
    require(2*tv <= Q(4*len(w), W) <= h_lower*delta/16, "rational prior hinge allowance")

    invalid = [lambda: contact_budget(True, 1, 1, Q(1)),
               lambda: contact_budget(0, 1, 1, Q(1)),
               lambda: contact_budget(1, Q(1,2), 1, Q(1)),
               lambda: contact_budget(1, 1, 0, Q(1)),
               lambda: contact_budget(1, 1, True, Q(1)),
               lambda: contact_budget(1, 1, 1, Q(0)),
               lambda: contact_budget(1, 1, 1, -1),
               lambda: contact_budget(1, 1.0, 1, Q(1)),
               lambda: contact_budget(1, 1, 1, 0.1),
               lambda: tightened_budget(1, 1, 1, 0, 1),
               lambda: round_simplex((Q(1,2),), 7),
               lambda: round_simplex((Q(-1),Q(2)), 7),
               lambda: round_simplex((Q(1),), 0)]
    for bad in invalid:
        try:
            bad()
        except ValueError:
            pass
        else:
            raise RuntimeError("invalid input accepted")
    counts["rejected_inputs"] = len(invalid)

    pins = json.loads((HERE/"INPUTS.json").read_text())
    for pin in pins:
        require(sha256((HERE/pin["path"]).read_bytes()).hexdigest() == pin["sha256"],
                "dependency pin: "+pin["path"])
    return dict(status="SPATIAL_CONTACT_LOCALIZATION_CONTROLS_PASS", counts=counts,
                source_pins=len(pins), tightened_example=tb, untightened_schedules=schedules,
                adverse_contact_certified=False, universal_analysis_formalized=False,
                output_powers_expanded=False)


if __name__ == "__main__":
    require(sys.version_info >= (3,11), "CPython 3.11 or later required")
    require(sys.argv[1:] in ([], ["--emit"]), "usage: verify.py [--emit]")
    output = json.dumps(controls(), indent=2, sort_keys=True)+"\n"
    if not sys.argv[1:]:
        require(output == (HERE/"EXPECTED.json").read_text(), "expected controls mismatch")
    print(output, end="")
