#!/usr/bin/env python3
"""Supplementary exact checks for ANCHOR_REDUCTION.md; CPython >=3.11.

Finite-cell controls are not Gaussian-contraction counterexamples.
The universal overlap, tail and entropy arguments are written proofs.
"""
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def positive(x):
    return max(x, 0)


def hinge(p, a):
    return sum(positive(x-a) for x in p)


def defect(f, g):
    # Equal unit-volume cells; maxima of this piecewise-linear function
    # occur at zero or at a density value.
    require(sum(f) == sum(g), "unequal cell masses")
    return max([Q(0)] + [hinge(f, a)-hinge(g, a)
                         for a in set(f+g+(Q(0),))])


def interaction_audit():
    grid = tuple(map(Q, (0, 1, 2, 3, 5))) + (Q(1, 7), Q(1, 3), Q(1, 2), Q(3, 2))
    cases = [0]*5
    for u, v, a in product(grid, repeat=3):
        value = positive(u+v-a)-positive(u-a)-positive(v-a)
        independent = positive(min(a, u, v, u+v-a))
        require(value == independent, "interaction formula mismatch")
        require(0 <= value <= min(u, v), "overlap bound failed")
        if u >= a and v >= a:
            k, expected = 0, a
        elif u >= a:
            k, expected = 1, v
        elif v >= a:
            k, expected = 2, u
        elif u+v <= a:
            k, expected = 3, Q(0)
        else:
            k, expected = 4, u+v-a
        require(value == expected, "piecewise interaction mismatch")
        cases[k] += 1
    return {"rational_triples": len(grid)**3, "five_case_counts": cases}


def disjoint_audit():
    bad_source, bad_target = (Q(1), Q(0)), (Q(1, 2), Q(1, 2))
    require(defect(bad_source, bad_target) == Q(1, 2), "negative control lost")
    require(defect(bad_target, bad_source) == 0, "positive control failed")
    rows = []
    for eps in (Q(1, 2), Q(1, 3), Q(1, 100)):
        for f, g in ((bad_source, bad_target), (bad_target, bad_source)):
            F = tuple(eps*x for x in f) + (1-eps,)
            G = tuple(eps*x for x in g) + (1-eps,)
            require(defect(F, G) == eps*defect(f, g), "wrong defect scale")
            for a in set(F+G+(Q(0),)):
                require(hinge(G, a)-hinge(F, a)
                        == eps*(hinge(g, a/eps)-hinge(f, a/eps)),
                        "wrong disjoint hinge scale")
            rows.append({"epsilon": str(eps), "base_defect": str(defect(f, g)),
                         "diluted_defect": str(defect(F, G))})
    return {"scope": "non-Gaussian finite-cell normalization controls", "rows": rows}


def overlap_audit():
    laws = ((Q(1), Q(0), Q(0)), (Q(0), Q(1, 2), Q(1, 2)),
            (Q(1, 4), Q(1, 4), Q(1, 2)))
    cases = knots = 0
    for f, g, b, eps in product(laws, laws, laws, (Q(1, 4), Q(1, 2), Q(3, 4))):
        h = tuple((1-eps)*x for x in b)
        ef, eg = tuple(eps*x for x in f), tuple(eps*x for x in g)
        F, G = tuple(x+y for x, y in zip(h, ef)), tuple(x+y for x, y in zip(h, eg))
        of = sum(min(x, y) for x, y in zip(h, ef))
        og = sum(min(x, y) for x, y in zip(h, eg))
        for a in set(h+ef+eg+F+G+(Q(0),)):
            xf = hinge(F, a)-hinge(h, a)-hinge(ef, a)
            xg = hinge(G, a)-hinge(h, a)-hinge(eg, a)
            require(0 <= xf <= of and 0 <= xg <= og, "interaction mass failed")
            error = hinge(G, a)-hinge(F, a)-eps*(hinge(g, a/eps)-hinge(f, a/eps))
            require(error == xg-xf and abs(error) <= max(of, og),
                    "one-overlap error bound failed")
            knots += 1
        require(abs(defect(F, G)-eps*defect(f, g)) <= max(of, og),
                "defect perturbation bound failed")
        cases += 1
    return {"mixture_pairs": cases, "all_piecewise_linear_knots_checked": knots}


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def norm2(x):
    return sum(t*t for t in x)


def require_contraction(xs, ys):
    require(len(xs) == len(ys), "label count mismatch")
    for i in range(len(xs)):
        for j in range(i):
            require(norm2(sub(ys[i], ys[j])) <= norm2(sub(xs[i], xs[j])),
                    "noncontractive labelled pair")


def parameters(eps, R, M):
    require(0 < eps < 1 and R > max(M, 0), "invalid anchor parameters")


def geometry_audit():
    xs = tuple(tuple(map(Q, p)) for p in
               ((-2, -1, 0), (1, -3, 2), (0, 0, 0), (-1, 2, -2), (2, 1, 3)))
    original = tuple((abs(x[0])/2, abs(x[1])/2, x[2]/2) for x in xs)
    require_contraction(xs, original)
    L = 1+max(Q(0), max(x[0]-y[0] for x, y in zip(xs, original)))
    ys = tuple((y[0]+L, y[1], y[2]) for y in original)
    eta = min(y[0]-x[0] for x, y in zip(xs, ys))
    D = max(norm2(y)-norm2(x) for x, y in zip(xs, ys))
    M = max(p[0] for p in xs+ys)
    K = max(sum(abs(t) for t in p) for p in xs+ys)
    displacement = max(sum(abs(t) for t in sub(y, x)) for x, y in zip(xs, ys))
    rows = []
    for R in map(Q, (10, 100, 1000)):
        parameters(Q(1, 100), R, M)
        require(2*R*eta > D, "anchor margin absent")
        z = (R, Q(0), Q(0))
        require_contraction(xs+(z,), ys+(z,))
        losses = []
        for x, y in zip(xs, ys):
            loss = norm2(sub(z, x))-norm2(sub(z, y))
            require(loss == 2*R*(y[0]-x[0])-(norm2(y)-norm2(x)),
                    "anchor identity sign error")
            require(loss >= 2*R*eta-D > 0, "anchor lower bound failed")
            losses.append(loss)
        scale = R+K
        X = tuple(tuple(t/scale for t in sub(x, z)) for x in xs+(z,))
        Y = tuple(tuple(t/scale for t in sub(y, z)) for y in ys+(z,))
        require(all(norm2(p) <= 1 for p in X+Y), "unit-ball normalization failed")
        require_contraction(X, Y)
        require(all(norm2(sub(y, x)) <= (displacement/scale)**2
                    for x, y in zip(X, Y)), "displacement estimate failed")
        rows.append({"R": str(R), "minimum_anchor_loss": str(min(losses)),
                     "unit_ball_scale": str(scale),
                     "displacement_upper_bound": str(displacement/scale)})
    invalid = 0
    calls = [lambda: require_contraction(xs+((Q(10), Q(0), Q(0)),),
                                        original+((Q(10), Q(0), Q(0)),)),
             lambda: parameters(Q(0), Q(10), M),
             lambda: parameters(Q(1), Q(10), M),
             lambda: parameters(Q(1, 2), M, M)]
    for call in calls:
        try:
            call()
        except ValueError:
            invalid += 1
        else:
            raise RuntimeError("invalid extension/control accepted")
    return {"translation_L": str(L), "forward_margin_eta": str(eta),
            "squared_norm_difference_bound_D": str(D), "projection_bound_M": str(M),
            "rational_extensions": rows, "invalid_controls_rejected": invalid}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    report = {"status": "FIXED_ATOM_REDUCTION_EXACT_AUDITS_PASS",
              "interaction": interaction_audit(), "disjoint_mixtures": disjoint_audit(),
              "overlapping_mixtures": overlap_audit(), "anchor_extension": geometry_audit(),
              "trust_boundary": "Supplementary rational controls. The universal Gaussian and entropy proofs are analytic; no counterexample is asserted."}
    encoded = (json.dumps(report, indent=2, sort_keys=True)+"\n").encode()
    if args.check:
        require(encoded == Path(__file__).with_name("ANCHOR_EXPECTED.json").read_bytes(),
                "ANCHOR_EXPECTED.json mismatch")
        print(report["status"], hashlib.sha256(encoded).hexdigest())
    else:
        print(encoded.decode(), end="")


if __name__ == "__main__":
    main()
