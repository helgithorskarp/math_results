#!/usr/bin/env python3
"""Exact profile/matching checks; the geometric proof remains a trust boundary."""

import argparse
from fractions import Fraction as Q
import json
from math import comb


F = (Q(0), Q(0), Q(1), Q(-2), Q(1), Q(0))
G = (Q(0), Q(0), Q(-1), Q(4), Q(-5), Q(2))


def trim(p):
    p = list(p)
    while len(p) > 1 and not p[-1]:
        p.pop()
    return p


def add(p, q):
    return trim([(p[i] if i < len(p) else Q(0)) +
                 (q[i] if i < len(q) else Q(0))
                 for i in range(max(len(p), len(q)))])


def scale(p, value):
    return trim([value * x for x in p])


def mul(p, q):
    out = [Q(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return trim(out)


def derivative(p):
    return trim([i * p[i] for i in range(1, len(p))])


def integral(p):
    return sum((x / (i + 1) for i, x in enumerate(p)), Q(0))


def at(p, x):
    value = Q(0)
    for c in reversed(p):
        value = value * x + c
    return value


def reverse(p):
    return trim([sum((p[j] * comb(j, i) * (-1) ** i
                     for j in range(i, len(p))), Q(0))
                 for i in range(len(p))])


def profile(a, b):
    return add(scale(F, a), scale(G, b))


def check_basis_identities():
    # Each expression is linear in A,B, so both coefficient bases suffice.
    assert mul(F, [Q(-1), Q(2)]) == trim(G)
    assert reverse(F) == trim(F)
    assert reverse(G) == scale(G, -1)
    endpoint_cases = diagonal_cases = derivative_cases = 0
    for A, B in [(Q(1), Q(0)), (Q(0), Q(1))]:
        p = profile(A, B)
        assert at(p, Q(0)) == at(p, Q(1)) == Q(0)
        assert at(derivative(p), Q(0)) == at(derivative(p), Q(1)) == Q(0)
        endpoint_cases += 1
        expected = scale(mul([Q(0), Q(1), Q(-1)],
                             [4*A-4*B, 20*B-8*A, -20*B]), Q(1, 2))
        assert derivative(p) == expected
        assert integral(p) == A / 30
        derivative_cases += 1
        for a in (-1, 1):
            for b in (-1, 1):
                transformed = profile(b*A, a*b*B)
                if a == -1:
                    transformed = reverse(transformed)
                assert transformed == scale(p, b)
                diagonal_cases += 1
    return {"coefficient_bases": 2, "endpoint_basis_checks": endpoint_cases,
            "derivative_and_integral_basis_checks": derivative_cases,
            "diagonal_isometry_basis_checks": diagonal_cases}


def green_fixture(epsilon, eta):
    vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
    labels = [(1, 1), (2, 0), (3, -1), (4, 1)]
    area = Q(0)
    profile_integrals = Q(0)
    for i, ((x0, y0), (color, state)) in enumerate(zip(vertices, labels)):
        x1, y1 = vertices[(i + 1) % 4]
        ex, ey = x1 - x0, y1 - y0
        p = profile(state * epsilon, color * eta)
        x = add([Q(x0), Q(ex)], scale(p, ey))
        y = add([Q(y0), Q(ey)], scale(p, -ex))
        integrand = add(mul(x, derivative(y)), scale(mul(y, derivative(x)), -1))
        area += integral(integrand) / 2
        profile_integrals += integral(p)
    expected = Q(1) + epsilon * sum(s for c, s in labels) / 30
    assert area == expected == Q(1) + profile_integrals
    return {"base": "unit square; colors 1,2,3,4; states 1,0,-1,1",
            "area_from_green": str(area), "area_from_profile_formula": str(expected),
            "heesch_lower_witness": "none; this fixture checks area only"}


def check_palette(colors=5):
    if type(colors) is not int or not 1 <= colors <= 32:
        raise ValueError("1<=colors<=32 is the bounded check domain")
    eta, epsilon = Q(1, 100 * colors), Q(1, 1000 * colors)
    labels = [(c, s, s * epsilon, c * eta)
              for c in range(1, colors + 1) for s in (-1, 0, 1)]
    root_sign_cases = 0
    for c, s, A, B in labels:
        assert B > 0 and abs(A) < B
        r = A / B
        quadratic = [Q(-1), 4*r, Q(5)]
        assert at(quadratic, Q(-1)) == 4*(1-r) > 0
        assert at(quadratic, Q(0)) == -1
        assert at(quadratic, Q(1)) == 4*(1+r) > 0
        root_sign_cases += 1
    counts = {"matched": 0, "wrong_direction_lens": 0,
              "wrong_direction_overlap": 0, "different_color_overlap": 0,
              "opposite_handedness_overlap": 0}
    for c, s, A, B in labels:
        for d, t, Aprime, Bprime in labels:
            for same_hand in (False, True):
                difference = profile(A + Aprime, B - Bprime if same_hand else B + Bprime)
                values = [at(difference, Q(1, 4)), at(difference, Q(3, 4))]
                if not same_hand:
                    assert min(values) < 0 < max(values)
                    counts["opposite_handedness_overlap"] += 1
                elif c != d:
                    assert min(values) < 0 < max(values)
                    counts["different_color_overlap"] += 1
                elif s == -t:
                    assert difference == [Q(0)]
                    # Independent coordinate reversal, not the difference rule.
                    assert add(profile(A, B), reverse(profile(Aprime, Bprime))) == [Q(0)]
                    counts["matched"] += 1
                elif A + Aprime < 0:
                    assert max(values) < 0
                    counts["wrong_direction_lens"] += 1
                else:
                    assert min(values) > 0
                    counts["wrong_direction_overlap"] += 1
    mirror_values = [str(at(profile(Q(0), 2*eta), x)) for x in (Q(1, 4), Q(3, 4))]
    alpha = Q(1, 100) + epsilon
    result = {"agent": "six-heesch-3", "role": "researcher",
              "arithmetic": "Python standard library integers and Fraction",
              "profile": "t^2*(1-t)^2*(A+B*(2*t-1))",
              "universal_linear_identities": check_basis_identities(),
              "palette": {"colors": colors, "eta": str(eta), "epsilon": str(epsilon),
                          "labels": len(labels), "critical_quadratic_sign_checks": root_sign_cases,
                          "ordered_pair_and_handedness_checks": sum(counts.values()),
                          "cases": counts},
              "pure_color_reflection_difference_at_quarters": mirror_values,
              "displacement_bound": str(alpha / 16),
              "endpoint_ratio_bound": str(4*alpha / 27),
              "diameter_increase_bound": str(alpha / 8),
              "trust_boundary": "Atomicity, local filled-contact grid locking and topology are written proofs, not formalized by this checker.",
              "record_construction": "none"}
    if colors >= 4:
        result["green_area_fixture"] = green_fixture(epsilon, eta)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--colors", type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(check_palette(args.colors), indent=2, sort_keys=True))
