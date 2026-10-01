#!/usr/bin/env python3
"""Exact algebra evidence for the written eight-coordinate stability proof.

Stdlib only. This does not formalize the analytic minimizer/equality bridges
or import/replay the separately cited radial and phase theorems.
"""
import argparse
from copy import deepcopy
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import sys


class CheckError(Exception):
    pass


def require(ok, message):
    if not ok:
        raise CheckError(message)


def c(q, n):
    return {} if not q else {(0,) * n: F(q)}


def var(i, n):
    exponent = [0] * n
    exponent[i] = 1
    return {tuple(exponent): F(1)}


def add(*polys):
    result = {}
    for poly in polys:
        for exponent, value in poly.items():
            result[exponent] = result.get(exponent, F(0)) + value
    return {e: v for e, v in result.items() if v}


def scale(poly, q):
    return {e: v * q for e, v in poly.items() if v * q}


def mul(*polys):
    require(bool(polys), "multiplication needs a dimensioned factor")
    # All callers have a nonzero first factor.
    require(bool(polys[0]), "first factor must supply a dimension")
    n = len(next(iter(polys[0])))
    result = c(1, n)
    for poly in polys:
        terms = {}
        for e, x in result.items():
            for f, y in poly.items():
                require(len(e) == len(f), "polynomial dimension mismatch")
                ef = tuple(a + b for a, b in zip(e, f))
                terms[ef] = terms.get(ef, F(0)) + x * y
        result = {e: v for e, v in terms.items() if v}
    return result


def pw(poly, k):
    require(k >= 1, "positive exponent required")
    return mul(*([poly] * k))


def g(poly):
    return add(scale(pw(poly, 2), 6), scale(pw(poly, 3), -1))


def gv(x):
    return 6 * x * x - x ** 3


def entries(poly):
    return [[list(e), str(v)] for e, v in sorted(poly.items())]


def elementary(values, k):
    return sum((product(xs) for xs in itertools.combinations(values, k)), F(0))


def product(values):
    answer = F(1)
    for x in values:
        answer *= x
    return answer


def moments(values):
    p2 = sum(x ** 2 for x in values)
    p3 = sum(x ** 3 for x in values)
    e2, e3 = elementary(values, 2), elementary(values, 3)
    require(sum(values) == 8 and min(values) >= 0, "moment-control domain")
    defect = 2 * e2 - e3
    require(defect == (9 * p2 - p3 - 64) / 3, "direct Newton control")
    u, e = p2 - 8, p2 + 64 - 16 * max(values)
    require(e - u == 72 - 16 * max(values), "nearest-family switch")
    return defect, min(u, e), u, e


def origin(a, radii):
    coefficients = [F(1)]
    for r in radii:
        nxt = [F(0)] * (len(coefficients) + 1)
        for i, value in enumerate(coefficients):
            nxt[i] += value
            nxt[i + 1] -= a * r * value
        coefficients = nxt
    return 9 * sum(value / F(i + 1) for i, value in enumerate(coefficients))


def regenerate(damage=None):
    identities = {}

    def identity(name, lhs, rhs):
        require(lhs == rhs, "full polynomial identity: " + name)
        identities[name] = entries(lhs)

    x, z = var(0, 2), var(1, 2)
    s = add(x, z)
    pair_constant = -13 if damage == "pair" else -12
    pair_rhs = add(scale(pw(s, 2), 6), scale(pw(s, 3), -1),
                   mul(add(scale(s, 3), c(pair_constant, 2)), x, z))
    identity("fixed_pair", add(g(x), g(z)), pair_rhs)

    m = var(0, 1)
    identity("lower_profile_cleared", add(c(-512, 1), scale(m, 384), scale(pw(m, 2), -40)),
             scale(mul(add(c(8, 1), scale(m, -1)), add(scale(m, 5), c(-8, 1))), 8))
    identity("ceiling_profile_cleared", add(c(-343, 1), scale(m, 588), scale(pw(m, 2), -77)),
             scale(mul(add(c(7, 1), scale(m, -1)), add(scale(m, 11), c(-7, 1))), 7))
    ell = var(0, 1)
    heavy = add(c(8, 1), scale(ell, -1))
    upper_lhs = add(g(heavy), scale(g(scale(ell, F(1, 7))), 7), c(-256, 1), scale(heavy, 48))
    upper_endpoint = 15 if damage == "upper" else 14
    upper_rhs = scale(mul(ell, add(c(F(7, 2), 1), scale(ell, -1)),
                          add(c(upper_endpoint, 1), scale(ell, -1))), F(48, 49))
    identity("upper_factor", upper_lhs, upper_rhs)

    # Definition-level products versus Newton moments, on the entire sum plane.
    variables = [var(i, 7) for i in range(7)]
    variables.append(add(c(8, 7), scale(add(*variables), -1)))
    e2 = add(*(mul(*xs) for xs in itertools.combinations(variables, 2)))
    e3 = add(*(mul(*xs) for xs in itertools.combinations(variables, 3)))
    p2 = add(*(pw(v, 2) for v in variables))
    p3 = add(*(pw(v, 3) for v in variables))
    newton_constant = -65 if damage == "newton" else -64
    identity("newton_full", add(scale(e2, 2), scale(e3, -1)),
             scale(add(scale(p2, 9), scale(p3, -1), c(newton_constant, 7)), F(1, 3)))
    identity("uniform_distance", add(*(pw(add(v, c(-1, 7)), 2) for v in variables)),
             add(p2, c(-8, 7)))
    identity("spike_distance", add(*(pw(add(v, c(-8 if i == 0 else 0, 7)), 2)
                                      for i, v in enumerate(variables))),
             add(p2, c(64, 7), scale(variables[0], -16)))

    # Same full plane, now interpreted as radii; affine image is y=2r-1.
    image = [add(scale(v, 2), c(-1, 7)) for v in variables]
    image_p2 = add(*(pw(v, 2) for v in image))
    identity("origin_uniform_scale", scale(add(image_p2, c(-8, 7)), F(1, 4)),
             add(p2, c(-8, 7)))
    metric_constant = 15 if damage == "metric" else 14
    origin_distance = add(*(pw(add(v, c(-F(9, 2) if i == 0 else -F(1, 2), 7)), 2)
                             for i, v in enumerate(variables)))
    identity("origin_coalesced_distance", origin_distance,
             add(p2, c(metric_constant, 7), scale(variables[0], -8)))
    identity("origin_spike_scale", scale(add(image_p2, c(64, 7), scale(image[0], -16)), F(1, 4)),
             origin_distance)

    a, t, e2w, e3w = [var(i, 4) for i in range(4)]
    at = mul(a, t)
    weighted_lhs = add(scale(mul(a, pw(at, 2), e2w), 2), scale(mul(pw(at, 3), e3w), -1))
    weighted_rhs = add(mul(pw(a, 3), pw(t, 2), add(scale(e2w, 2), scale(e3w, -1))),
                       mul(pw(a, 3), pw(t, 2), add(c(1, 4), scale(t, -1)), e3w))
    identity("weighted_mass", weighted_lhs, weighted_rhs)

    # Independent count enumeration of every floor/ceiling/free-count candidate.
    profiles, candidates, endpoint_feasible = [], 0, 0
    for ceilings in range(9):
        for free_count in range(9 - ceilings):
            candidates += 1
            remaining = 8 - ceilings * F(9, 2)
            if free_count == 0:
                endpoint_feasible += int(remaining == 0)
                continue
            free = remaining / free_count
            if not 0 < free < F(9, 2):
                continue
            if damage == "omit_profile" and (ceilings, free_count) == (0, 2):
                continue
            excess = ceilings * gv(F(9, 2)) + free_count * gv(free) - 40
            if ceilings == 0:
                factored = F(8 * (8 - free_count) * (5 * free_count - 8), free_count ** 2)
            else:
                require(ceilings == 1, "unexpected feasible ceiling count")
                factored = F(7 * (7 - free_count) * (11 * free_count - 7), 8 * free_count ** 2)
            require(excess == factored and excess >= 0, "profile factor/sign")
            require((excess == 0) == ((ceilings, free_count) in [(0, 8), (1, 7)]), "profile zero")
            profiles.append({"ceilings": ceilings, "free_count": free_count,
                             "free_value": str(free), "excess": str(excess)})
    require(candidates == 45 and endpoint_feasible == 0 and len(profiles) == 14,
            "complete finite-profile count")

    shapes = {"uniform": [F(1)] * 8, "spike": [F(8)] + [F(0)] * 7,
              "midpoint": [F(9, 2)] + [F(1, 2)] * 7}
    controls = {}
    radial_controls = []
    for name, w in shapes.items():
        defect, distance, u, e = moments(w)
        require(defect == distance, "equality-orbit control")
        controls[name] = {"D": str(defect), "distance_squared": str(distance), "U": str(u), "E": str(e)}
        for a in [F(1, 4), F(1, 2), F(1)]:
            radii = [(1 + a * v) / (1 + a) for v in w]
            y = [(1 + a) * r - 1 for r in radii]
            da = 2 * a * elementary(y, 2) - elementary(y, 3)
            h2 = a * a * distance / ((1 + a) ** 2)
            require(da == a * ((1 + a) ** 2) * h2, "normalized sharp defect scale")
            pr, oa = product(radii), origin(a, radii)
            bound = (8 * (1 - a ** 9) + 5 * da) / ((1 + a) ** 8)
            require(pr <= 1 and oa - pr >= bound, "inherited radial rational control")
            radial_controls.append({"shape": name, "a": str(a), "O": str(oa), "product": str(pr),
                                    "D_a": str(da), "distance_squared": str(h2), "gap_lower": str(bound)})
    require(controls["midpoint"]["D"] == controls["midpoint"]["U"] == controls["midpoint"]["E"] == "14",
            "sharp coefficient witness")
    require(radial_controls[2]["O"] == radial_controls[2]["product"], "uniform origin equality")
    require(radial_controls[5]["O"] == radial_controls[5]["product"], "coalesced origin equality")

    mass_controls = []
    for name, w in shapes.items():
        for a in [F(1, 2), F(1)]:
            for t in [F(1, 3), F(1)]:
                y = [a * t * v for v in w]
                sigma = sum(y)
                da = 2 * a * elementary(y, 2) - elementary(y, 3)
                distance = (a * t) ** 2 * moments(w)[1]
                correction = (8 * a - sigma) * elementary(y, 3) / sigma
                require(da == a * distance + correction, "weighted equality control")
                mass_controls.append({"shape": name, "a": str(a), "t": str(t),
                                      "sigma": str(sigma), "D_a": str(da), "correction": str(correction)})
    require(F(570801247, 1647086) < 350, "inherited phase constant comparison")
    return {"format_version": 1, "polynomial_identities": identities,
            "candidate_counts": {"total": candidates, "feasible": len(profiles), "endpoint_feasible": endpoint_feasible},
            "profiles": profiles, "equality_controls": controls, "radial_rational_controls": radial_controls,
            "weighted_mass_controls": mass_controls,
            "scope": "Exact algebra evidence; written analytic bridges and cited radial/phase theorems remain outside this checker."}


def canonical(record):
    return json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode()


def compare_fixture(record, expected):
    require(canonical(record) == canonical(expected), "full regenerated fixture mismatch")


def self_checks(record):
    mathematical = ["pair", "upper", "newton", "metric", "omit_profile"]
    for damage in mathematical:
        try:
            regenerate(damage)
        except CheckError:
            continue
        raise CheckError("mathematical damage accepted: " + damage)
    bad = []
    for mode in range(4):
        x = deepcopy(record)
        if mode == 0:
            x["profiles"].pop()
        elif mode == 1:
            x["polynomial_identities"]["newton_full"][0][1] = "1/999999999"
        elif mode == 2:
            x["equality_controls"]["midpoint"]["D"] = "15"
        else:
            x["format_version"] = 2
        bad.append(x)
    for x in bad:
        try:
            compare_fixture(record, x)
        except CheckError:
            continue
        raise CheckError("fixture damage accepted")
    return len(mathematical), len(bad)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=Path(__file__).with_name("expected.json"))
    parser.add_argument("--emit-fixture", type=Path, help="explicit regeneration output; default verification never writes")
    args = parser.parse_args()
    try:
        record = regenerate()
        mathematical, fixtures = self_checks(record)
        if args.emit_fixture is not None:
            args.emit_fixture.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        else:
            expected = json.loads(args.fixture.read_text(encoding="utf-8"))
            compare_fixture(record, expected)
        print(json.dumps({"status": "PASS", "polynomial_identities": len(record["polynomial_identities"]),
                          "newton_monomials": len(record["polynomial_identities"]["newton_full"]),
                          "finite_profiles": len(record["profiles"]), "radial_controls": len(record["radial_rational_controls"]),
                          "mass_controls": len(record["weighted_mass_controls"]), "mathematical_damages_rejected": mathematical,
                          "fixture_damages_rejected": fixtures, "record_sha256": hashlib.sha256(canonical(record)).hexdigest()}, sort_keys=True))
    except (CheckError, OSError, ValueError) as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
