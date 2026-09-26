#!/usr/bin/env python3
"""Exact finite premises for GEOMETRIC_LIMIT.md, CPython >=3.11, stdlib.

The original square-cone order certificate is an explicit, hash-checked
dependency. This audit does not repeat its upper-set correlation proof.
"""
import argparse
import copy
from fractions import Fraction as Q
import hashlib
from itertools import permutations, product
import json
from math import comb
from pathlib import Path

A = ((1, 0, 1), (0, 1, 1), (-1, 0, 1), (0, -1, 1))
B = ((1, 1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1))
GROUP = tuple(product(permutations(range(3)), product((-1, 1), repeat=3)))
KEYS = tuple(product(range(3), range(5), range(7)))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(obj):
    return (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode()


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def basis(points):
    result = []
    for perm, signs in GROUP:
        columns = []
        for p in points:
            e = [0, 0, 0]
            for i in range(3):
                e[perm[i]] = signs[i] * p[i]
            powers = (1 + e[0], 2 + e[0] + e[1], 3 + sum(e))
            require(all(0 <= n <= bound for n, bound in zip(powers, (2, 4, 6))),
                    "invalid cleared exponent")
            columns.append(tuple(
                comb(powers[0], k[0]) * comb(powers[1], k[1]) * comb(powers[2], k[2])
                if all(j <= n for j, n in zip(k, powers)) else 0
                for k in KEYS))
        result.append(columns)
    return result


def selected_check(poly, order, rows):
    for row in rows:
        i, j = row["lower"], row["upper"]
        require(0 <= i < 48 and 0 <= j < 48 and (order[i] >> j) & 1,
                "coefficient comparison absent from source order")
        k = KEYS.index(tuple(row["monomial"]))
        require(row["gcd"] > 0 and len(row["d"]) == 4, "invalid primitive form")
        actual = tuple(poly[j][a][k] - poly[i][a][k] for a in range(4))
        expected = tuple(row["gcd"] * x for x in row["d"])
        require(actual == expected, "selected coefficient mismatch")


def all_forms(poly, order):
    for i, mask in enumerate(order):
        for j in range(48):
            if (mask >> j) & 1:
                for k in range(105):
                    yield tuple(poly[j][a][k] - poly[i][a][k] for a in range(4))


def member_audit(forms, q):
    require(len(q) == 4 and all(type(v) is int and v >= 0 for v in q),
            "invalid exact endpoint vector")
    values = [dot(d, q) for d in forms]
    require(all(v >= 0 for v in values), "endpoint outside coefficient cone")
    return {"vector": q, "coefficient_tests": len(values),
            "zero_coefficients": values.count(0),
            "least_positive_coefficient": min(v for v in values if v > 0)}


def linear_combination(rows, coefficients):
    return tuple(sum(c * rows[j][i] for j, c in coefficients)
                 for i in range(4))


def ratio_identities(selected):
    a = [r["d"] for r in selected["A"]]
    b = [r["d"] for r in selected["B"]]
    require(linear_combination(a, ((4, 1), (0, 3))) == (5, 0, 0, -1),
            "A first ratio certificate")
    require(linear_combination(a, ((5, 1), (1, 3))) == (0, 0, 5, -1),
            "A second ratio certificate")
    require(linear_combination(b, ((3, 1), (0, 1))) == (2, 0, -1, 0),
            "B first ratio certificate")
    require(linear_combination(b, ((4, 1), (3, 1), (0, 3))) == (4, 0, 0, -1),
            "B second ratio certificate")
    return 4


def geometry_audit():
    reflect = lambda p: (-p[0], p[1], p[2])
    swaps = [A.index(reflect(a)) for a in A]
    require(swaps == [2, 1, 0, 3], "wrong A radius relabelling")
    losses = {}
    for a in A:
        for b in B:
            # Coefficients of r^2,t^2 cancel; this is the coefficient of rt.
            require(dot(a, a) == dot(reflect(a), reflect(a)), "A norm")
            coefficient = 2*dot(a, b) + 2*dot(reflect(a), b)
            require(coefficient == 4*(1+a[1]*b[1]) >= 0, "cross polynomial")
            losses[coefficient] = losses.get(coefficient, 0) + 1
    for a in A:
        for b in A:
            require(dot(a, b) == dot(reflect(a), reflect(b)), "A radial isometry")
    # R maps a->S a and -b->b. S R preserves the first coordinate.
    for x, y in [(a, reflect(a)) for a in A] + [
            (tuple(-v for v in b), b) for b in B] + [((0, 0, 0), (0, 0, 0))]:
        require(reflect(y)[0] == x[0], "fixed coordinate after output isometry")
    require(losses == {0: 4, 4: 8, 8: 4}, "unexpected cross coefficients")
    return {"A_permutation": swaps, "cross_rt_coefficients": losses,
            "coordinate_relation_checked": True}


def hinge_normalization_audit():
    # Unit-volume cell controls, not Gaussian-contraction data.
    f = (Q(1, 6), Q(1, 3), Q(1, 2))
    g = (Q(1, 9), Q(2, 9), Q(2, 3))
    require(sum(f) == sum(g) == 1, "unequal masses")
    for a in (Q(1, 12), Q(1, 4), Q(3, 5), Q(1)):
        hg = sum(max(x-a, 0) for x in g)
        hf = sum(max(x-a, 0) for x in f)
        rhs = sum(min(x/a, 1) for x in f) - sum(min(x/a, 1) for x in g)
        require((hg-hf)/a == rhs, "wrong geometric defect normalization")
    return 4


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    raw = (here / "GEOMETRIC_CERTIFICATE.json").read_bytes()
    cert = json.loads(raw)
    source_raw = (here / cert["source_certificate"]).read_bytes()
    require(hashlib.sha256(source_raw).hexdigest() == cert["source_sha256"],
            "source certificate hash mismatch")
    source = json.loads(source_raw)
    require(source["group_size"] == len(GROUP) == 48, "wrong group size")
    reports = {}
    invalid = 0
    for label, points in (("A", A), ("B", B)):
        require(source["points_" + label] == [list(p) for p in points], "wrong geometry")
        poly = basis(points)
        order = source["orders"][label]["up"]
        selected_check(poly, order, cert["selected_forms"][label])
        forms = list(all_forms(poly, order))
        rows = [member_audit(forms, q) for q in cert["endpoint_vectors"][label]]
        reports[label] = {"retained_pairs": sum(x.bit_count() for x in order),
                          "selected_forms_checked": len(cert["selected_forms"][label]),
                          "endpoint_audits": rows}
        corrupted = copy.deepcopy(cert["selected_forms"][label])
        corrupted[0]["d"][0] += 1
        for call in (lambda: selected_check(poly, order, corrupted),
                     lambda: member_audit(forms, [1, 0, 0, 0])):
            try:
                call()
            except ValueError:
                invalid += 1
            else:
                raise RuntimeError("invalid control accepted")
    report = {"status": "GEOMETRIC_PROFILE_CLASSIFICATION_PASS",
              "certificate_sha256": hashlib.sha256(raw).hexdigest(),
              "source_certificate_sha256": cert["source_sha256"],
              "cone_audits": reports,
              "ratio_identities": ratio_identities(cert["selected_forms"]),
              "geometry": geometry_audit(),
              "hinge_normalization_controls": hinge_normalization_audit(),
              "invalid_controls_rejected": invalid,
              "scope": "Fixed coefficient cones: lambda0=lambda2=lambda3>=lambda1; extracted ball radii have an existing coordinate-preserving rematching."}
    output = encoded(report)
    if args.check:
        require(output == (here / "GEOMETRIC_EXPECTED.json").read_bytes(),
                "GEOMETRIC_EXPECTED.json mismatch")
        print(report["status"], hashlib.sha256(output).hexdigest())
    else:
        print(output.decode(), end="")


if __name__ == "__main__":
    main()
