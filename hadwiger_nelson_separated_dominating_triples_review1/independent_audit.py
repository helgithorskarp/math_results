#!/usr/bin/env python3
"""Independent exact audit of the separated-dominating-triple theorem.

No target certificate or target module is read.  The finite palette cases are
tested by full C6 colour words, and the sharpness witness is reconstructed from
its mathematical formula in Q(sqrt(3),sqrt(11)).
"""

from fractions import Fraction as Q
from itertools import combinations, product
import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ZERO = (Q(0), Q(0), Q(0), Q(0))
ONE = (Q(1), Q(0), Q(0), Q(0))


def fadd(x, y):
    return tuple(a + b for a, b in zip(x, y))


def fneg(x):
    return tuple(-a for a in x)


def fmul(x, y):
    # Basis index is a bit mask: 0=1, 1=sqrt(3), 2=sqrt(11), 3=sqrt(33).
    out = [Q(0)] * 4
    for i, a in enumerate(x):
        for j, b in enumerate(y):
            factor = (3 if i & j & 1 else 1) * (11 if i & j & 2 else 1)
            out[i ^ j] += factor * a * b
    return tuple(out)


def rational(x):
    return (Q(x), Q(0), Q(0), Q(0))


def complex_add(x, y):
    return fadd(x[0], y[0]), fadd(x[1], y[1])


def complex_neg(x):
    return fneg(x[0]), fneg(x[1])


def complex_multiply(x, y):
    return (
        fadd(fmul(x[0], y[0]), fneg(fmul(x[1], y[1]))),
        fadd(fmul(x[0], y[1]), fmul(x[1], y[0])),
    )


def complex_number(real=0, imag=0):
    return rational(real), rational(imag)


def squared_distance(x, y):
    delta = complex_add(x, complex_neg(y))
    return fadd(fmul(delta[0], delta[0]), fmul(delta[1], delta[1]))


def circle_audit():
    omega = (rational(Q(1, 2)), (Q(0), Q(1, 2), Q(0), Q(0)))
    roots = [complex_number(1)]
    for _ in range(5):
        roots.append(complex_multiply(roots[-1], omega))
    if complex_multiply(roots[-1], omega) != roots[0] or len(set(roots)) != 6:
        raise AssertionError("sixth-root orbit")
    chords = []
    for point in roots:
        value = squared_distance(roots[0], point)
        if value[1:] != ZERO[1:]:
            raise AssertionError(value)
        chords.append(int(value[0]))
    if chords != [0, 1, 3, 4, 3, 1]:
        raise AssertionError(chords)

    edges = {(i, (i + 1) % 6) for i in range(6)}
    proper = []
    for word in product((0, 1), repeat=6):
        if all(word[i] != word[j] for i, j in edges):
            proper.append(word)
    if proper != [(0, 1, 0, 1, 0, 1), (1, 0, 1, 0, 1, 0)]:
        raise AssertionError(proper)

    # At two-circle centre distance d, the intersection chord has square 4-d^2.
    # Same-colour prescriptions fail only at odd C6 steps.  The step-three
    # option gives d=0 and is excluded by distinct centres.
    exceptional = sorted({4 - chords[k] for k in range(1, 6)
                          if k % 2 and 4 - chords[k] > 0})
    if exceptional != [3]:
        raise AssertionError(exceptional)
    return proper, {
        "circle_orbit_points": 6,
        "binary_words_checked": 64,
        "proper_binary_words": len(proper),
        "positive_distinct_centre_exception_squared": exceptional,
    }


def central_prescription_audit(proper):
    cases = []
    endpoint_choices = 0
    # fixed means d_i=1 and anchor a_i is fixed on C(b); edge means
    # d_i=sqrt(3) and either endpoint of M_i may be selected.
    for kind0, kind1 in product(("fixed", "edge"), repeat=2):
        if kind0 == kind1 == "fixed":
            continue  # two fixed anchors imply |a0-a1|<=2.
        candidates0 = (0,) if kind0 == "fixed" else (0, 1)
        colour0 = 0 if kind0 == "fixed" else 1
        for base in range(6):
            candidates1 = (base,) if kind1 == "fixed" else (base, (base + 1) % 6)
            colour1 = 1 if kind1 == "fixed" else 0
            if set(candidates0) & set(candidates1):
                continue  # the two anchor objects are geometrically disjoint.
            valid = []
            for x, y in product(candidates0, candidates1):
                if any(word[x] == colour0 and word[y] == colour1 for word in proper):
                    valid.append((x, y))
            if not valid:
                raise AssertionError((kind0, kind1, base))
            cases.append((kind0, kind1, base, tuple(valid)))
            endpoint_choices += len(valid)
    if len(cases) != 11 or endpoint_choices != 14:
        raise AssertionError((len(cases), endpoint_choices))
    digest = hashlib.sha256(json.dumps(cases, separators=(",", ":")).encode()).hexdigest()
    return {
        "same_orbit_two_anchor_cases": len(cases),
        "valid_endpoint_pairs": endpoint_choices,
        "central_case_sha256": digest,
        "fixed_fixed_excluded_by_far_leaf_distance": True,
        "different_orbit_phases_independent": True,
    }


def colouring_number(vertices, edges):
    tested_three = 0
    for word in product(range(3), repeat=len(vertices)):
        tested_three += 1
        if all(word[i] != word[j] for i, j in edges):
            raise AssertionError("unexpected three-colouring")
    four = next(word for word in product(range(4), repeat=len(vertices))
                if all(word[i] != word[j] for i, j in edges))
    return tested_three, four


def sharpness_audit():
    zero = complex_number()
    u = complex_number(1)
    v = (rational(Q(1, 2)), (Q(0), Q(1, 2), Q(0), Q(0)))
    rho = (rational(Q(5, 6)), (Q(0), Q(0), Q(1, 6), Q(0)))
    u_plus_v = complex_add(u, v)
    vertices = (zero, u, v, u_plus_v, complex_multiply(rho, u),
                complex_multiply(rho, v), complex_multiply(rho, u_plus_v))
    if len(set(vertices)) != 7:
        raise AssertionError("Moser collision")
    edges = tuple(pair for pair in combinations(range(7), 2)
                  if squared_distance(vertices[pair[0]], vertices[pair[1]]) == ONE)
    if len(edges) != 11:
        raise AssertionError(edges)
    dominating = (0, 3)
    if any(k not in dominating and not any(k in edge and (edge[0] in dominating or edge[1] in dominating)
                                           for edge in edges) for k in range(7)):
        raise AssertionError("pair does not dominate")
    tested_three, four = colouring_number(vertices, edges)
    third = complex_number(4)
    centres = (vertices[0], vertices[3], third)
    if len(set(centres)) != 3 or squared_distance(centres[0], centres[2]) != rational(16):
        raise AssertionError("separated centres")
    for point in vertices:
        if point not in centres and not any(squared_distance(point, c) == ONE for c in centres):
            raise AssertionError("spindle not in three-circle support")
    return {
        "sharpness_vertices": len(vertices),
        "sharpness_pair_distances": 21,
        "sharpness_strict_edges": len(edges),
        "three_colour_assignments_refuted": tested_three,
        "proper_four_colouring": list(four),
        "dominating_pair": list(dominating),
        "far_pair_squared_distance": 16,
        "spindle_contained_in_support": True,
    }


def boundary_audit():
    # At the excluded boundary |a0-a1|=3, equality in the triangle inequality
    # gives the unique cross-leaf unit edge 0--1--2--3.
    a0, x, y, a1 = map(complex_number, (0, 1, 2, 3))
    if not (squared_distance(a0, x) == squared_distance(x, y) ==
            squared_distance(y, a1) == ONE and squared_distance(a0, a1) == rational(9)):
        raise AssertionError("distance-three boundary witness")
    return {
        "distance_three_cross_leaf_edge_witness": True,
        "distance_three_not_claimed": True,
    }


def audit():
    proper, circle = circle_audit()
    return {"status": "PASS", **circle, **central_prescription_audit(proper),
            **sharpness_audit(), **boundary_audit()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.check_expected and result != json.loads((HERE / "EXPECTED.json").read_text()):
        raise AssertionError("expected output mismatch")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
