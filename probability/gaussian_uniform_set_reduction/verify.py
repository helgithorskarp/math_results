#!/usr/bin/env python3
"""Exact whole-cube contraction controls; no Gaussian integration."""

import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def norm2(a):
    return sum(x * x for x in a)


def rank(rows):
    m = [[F(x) for x in r] for r in rows]
    p = 0
    for j in range(len(m[0])):
        i = next((i for i in range(p, len(m)) if m[i][j]), None)
        if i is None:
            continue
        m[p], m[i] = m[i], m[p]
        z = m[p][j]
        m[p] = [a / z for a in m[p]]
        for i in range(len(m)):
            if i != p:
                z = m[i][j]
                m[i] = [a - z * b for a, b in zip(m[i], m[p])]
        p += 1
        if p == len(m):
            break
    return p


CORNERS = tuple(product((-1, 1), repeat=3))  # Twice the actual Q corners.


def check_geometry(name, xs, ys, strict=True):
    require(len(xs) == len(ys) > 1, "label counts")
    require(all(len(x) == 3 and all(type(z) is int for z in x)
                for x in xs + ys), "integer centers")
    margins, source_sep, target_sep = [], [], []
    for i, j in combinations(range(len(xs)), 2):
        u, v = sub(xs[i], xs[j]), sub(ys[i], ys[j])
        source_sep.append(max(map(abs, u)))
        target_sep.append(max(map(abs, v)))
        margin = norm2(u) - norm2(v) - 2 * sum(map(abs, sub(u, v)))
        # Directly inspect every pair of cube corners. The squared norm
        # difference is affine in the offset difference; its minimum on
        # the whole box is attained at one of these corners (written proof).
        losses = []
        for a, b in product(CORNERS, repeat=2):
            h = sub(a, b)
            in_twice = tuple(2 * x + z for x, z in zip(u, h))
            out_twice = tuple(2 * y + z for y, z in zip(v, h))
            losses.append(F(norm2(in_twice) - norm2(out_twice), 4))
        require(min(losses) == margin, "corner/closed-form disagreement")
        require(margin > 0 if strict else margin >= 0, "whole-cube expansion")
        margins.append(margin)
    require(min(source_sep) >= 2 and min(target_sep) >= 2, "cubes not separated")
    return {"name": name, "N": len(xs), "pair_count": len(margins),
            "corner_pairs_checked": 64 * len(margins),
            "minimum_cube_margin": min(margins),
            "minimum_source_linf_separation": min(source_sep),
            "minimum_target_linf_separation": min(target_sep),
            "paired_affine_rank": rank([(1, *x, *y) for x, y in zip(xs, ys)]) - 1,
            "source_centers": xs, "target_centers": ys}


def report():
    xs = [tuple(64 * s for s in v) for v in CORNERS]
    ys = [(32 * a + b * c, 32 * b + a * c, 32 * c + a * b)
          for a, b, c in CORNERS]
    full = check_geometry("eight_cube_rank_six_control", xs, ys)
    require(full["paired_affine_rank"] == 6, "full paired rank")
    # The weights 1/3,2/3 become 3 equally weighted distinct labels.
    # Before dilation: source 0,3,31/10; target 0,-2,-39/20.
    # The two labels in the second cluster contract by exactly 1/2.
    clones_x = [(0, 0, 0), (3000, 0, 0), (3100, 0, 0)]
    clones_y = [(0, 0, 0), (-2000, 0, 0), (-1950, 0, 0)]
    clones = check_geometry("rational_equal_weight_splitting", clones_x, clones_y)
    require(norm2(sub(clones_y[1], clones_y[2])) * 4
            == norm2(sub(clones_x[1], clones_x[2])), "within-cluster ratio")
    require(F(1, 3) + F(2, 3) == 1, "uniform weight multiplicities")

    controls = []
    for dilation in (1, 2, 3):
        a = [(0, 0, 0), (3 * dilation, 0, 0)]
        b = [(0, 0, 0), (-2 * dilation, 0, 0)]
        u, v = sub(a[1], a[0]), sub(b[1], b[0])
        require(norm2(v) < norm2(u), "center contraction control")
        margin = 5 * dilation ** 2 - 10 * dilation
        try:
            check_geometry("dilation_control", a, b)
            rejected = False
        except ValueError as e:
            require(str(e) == "whole-cube expansion", "unexpected rejection")
            rejected = True
        require(rejected == (dilation < 3), "strict whole-cube rejection control")
        if dilation == 2:
            check_geometry("nonstrict_boundary", a, b, strict=False)
        controls.append({"dilation": dilation, "center_squared_loss": 5 * dilation ** 2,
                         "cube_margin": margin, "strict_checker_rejects": rejected})
    return {"status": "LATTICE_CUBE_CONTRACTION_CONTROLS_PASS",
            "scope": "Geometry and exact arithmetic only; no Gaussian hinge sign.",
            "positive_controls": [full, clones], "dilation_controls": controls,
            "thickening_error_upper_bound": "sqrt(3)/(q sqrt(2 pi)) < 1/q"}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--check", action="store_true")
    p.add_argument("--expected", type=Path, default=Path(__file__).with_name("EXPECTED.json"))
    args = p.parse_args()
    output = json.dumps(report(), sort_keys=True, indent=2) + "\n"
    if args.check:
        require(args.expected.read_text() == output, "expected output mismatch")
        print("LATTICE_CUBE_CONTRACTION_CONTROLS_PASS",
              hashlib.sha256(output.encode()).hexdigest())
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
