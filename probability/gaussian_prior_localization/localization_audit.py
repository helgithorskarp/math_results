#!/usr/bin/env python3
"""Exact compact controls for DEFECT_LOCALIZATION.md; not Gaussian quadrature."""

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def positive(x):
    return max(F(0), x)


def hinge(row, a):
    return sum((positive(x - a) for x in row), F(0))


def total(rows):
    return [sum(column, F(0)) for column in zip(*rows)]


def fraction(x):
    return str(F(x))


def audit_partition(name, source, target, labels):
    """Unit-volume observation cells; every row has its labelled mass."""
    source = [[F(x) for x in row] for row in source]
    target = [[F(x) for x in row] for row in target]
    require(len(source) == len(target) > 0, "row counts")
    require(all(len(row) == len(labels) for row in source + target), "columns")
    require(all(x >= 0 for row in source + target for x in row), "negative mass")
    require(all(isinstance(i, int) and 0 <= i < len(source) for i in labels),
            "invalid observation label")
    masses = [sum(row, F(0)) for row in source]
    require(all(p > 0 for p in masses) and sum(masses) == 1, "probability masses")
    require(masses == [sum(row, F(0)) for row in target], "unmatched mass")
    f, g = total(source), total(target)
    leak = sum((source[i][j] for i in range(len(source))
                for j, label in enumerate(labels) if label != i), F(0))
    # These include every breakpoint of each piecewise-linear expression.
    knots = sorted({F(0), *f, *g,
                    *(x for row in source + target for x in row)})
    component_defects = [max(hinge(a, t) - hinge(b, t) for t in knots) / p
                         for a, b, p in zip(source, target, masses)]
    gaps = []
    rescaling_is_essential = False
    interactions = []
    for a in knots:
        gap = hinge(f, a) - hinge(g, a)
        row_gap = sum((hinge(fi, a) - hinge(gi, a)
                       for fi, gi in zip(source, target)), F(0))
        scaled = sum((p * (hinge([x / p for x in fi], a / p)
                          - hinge([x / p for x in gi], a / p))
                      for fi, gi, p in zip(source, target, masses)), F(0))
        unscaled = sum((p * (hinge([x / p for x in fi], a)
                            - hinge([x / p for x in gi], a))
                        for fi, gi, p in zip(source, target, masses)), F(0))
        rescaling_is_essential |= unscaled != row_gap
        fi = hinge(f, a) - sum((hinge(row, a) for row in source), F(0))
        gi = hinge(g, a) - sum((hinge(row, a) for row in target), F(0))
        require(0 <= fi <= leak and gi >= 0, "interaction bound")
        require(row_gap == scaled, "incorrect mass/threshold normalization")
        require(gap == row_gap + fi - gi, "interaction decomposition")
        require(gap <= row_gap + leak, "partition inequality")
        require(gap <= sum(p * d for p, d in zip(masses, component_defects)) + leak,
                "normalized defect inequality")
        gaps.append(gap)
        interactions.append((fi, gi))
    return {
        "name": name, "model": "finite cells; not Gaussian contraction data",
        "masses": list(map(fraction, masses)), "knots": list(map(fraction, knots)),
        "source_leakage": fraction(leak), "global_defect": fraction(max(gaps)),
        "component_defects": list(map(fraction, component_defects)),
        "source_interaction_max": fraction(max(a for a, b in interactions)),
        "target_interaction_max": fraction(max(b for a, b in interactions)),
        "unscaled_threshold_changes_value": rescaling_is_essential,
    }


def crossing_by_intervals(x, z, ell):
    """Integrate the indicator over shifts, without using the min formula."""
    require(ell > 0, "positive grid side required")
    cuts = sorted({F(0), ell, x % ell, (x + z) % ell})
    length = F(0)
    for left, right in zip(cuts, cuts[1:]):
        u = (left + right) / 2
        if (x - u) // ell != (x + z - u) // ell:
            length += right - left
    return length / ell


def audit_grid():
    cases = []
    for ell in [F(1), F(3, 2)]:
        for x in [F(-7, 3), F(0), F(5, 7)]:
            for z in [F(-5), F(-2, 3), F(0), F(1, 7), ell, F(11, 4)]:
                p = crossing_by_intervals(x, z, ell)
                require(p == min(F(1), abs(z) / ell), "one-dimensional grid crossing")
                cases.append((x, z, ell, p))
    # Product cells use independent coordinate shifts; check the union bound.
    triples = [(1, 3, 8), (3, 9, 15), (2, 8, 14), (19, 21, 26), (18, 24, 30)]
    three = []
    for ids in triples:
        ps = [cases[i][3] for i in ids]
        same = F(1)
        for p in ps:
            same *= 1 - p
        require(1 - same <= sum(ps), "coordinate union bound")
        three.append({"crossing": fraction(1 - same),
                      "union_bound": fraction(sum(ps))})
    return {"interval_cases": len(cases), "three_coordinate_controls": three}


def audit_rounding_warning():
    # A one-dimensional isometry embedded in R3. Separate nearest-integer
    # rounding collapses its input pair but splits its output pair.
    x = [F(1, 10), F(1, 5)]
    y = [F(49, 100), F(59, 100)]
    require(y[0] - x[0] == y[1] - x[1], "original translation")
    rounded_x = [int((v + F(1, 2)) // 1) for v in x]
    rounded_y = [int((v + F(1, 2)) // 1) for v in y]
    require(abs(y[1] - y[0]) == abs(x[1] - x[0]), "original isometry")
    require(abs(rounded_y[1] - rounded_y[0]) > abs(rounded_x[1] - rounded_x[0]),
            "control must break independent endpoint rounding")
    return {"input": list(map(fraction, x)), "output": list(map(fraction, y)),
            "rounded_input": rounded_x, "rounded_output": rounded_y}


def report():
    fixtures = [
        audit_partition("source overlap requires its error",
                        [[F(1, 2), 0], [F(1, 2), 0]],
                        [[F(1, 2), 0], [0, F(1, 2)]], [0, 1]),
        audit_partition("target merging is favorable",
                        [[F(1, 2), 0], [0, F(1, 2)]],
                        [[F(1, 2), 0], [F(1, 2), 0]], [0, 1]),
        audit_partition("unequal component masses change thresholds",
                        [[F(1, 4), 0, 0], [0, F(3, 4), 0]],
                        [[F(1, 8), F(1, 8), 0], [0, F(3, 8), F(3, 8)]],
                        [0, 1, 1]),
    ]
    require(fixtures[0]["global_defect"] == "1/2", "source-overlap control")
    require(fixtures[0]["component_defects"] == ["0", "0"], "component equality")
    require(fixtures[1]["global_defect"] == "0", "target merging control")
    require(fixtures[2]["unscaled_threshold_changes_value"], "threshold control")
    # pi>3 is a standard analytic input. All subsequent comparisons are exact.
    require(F(7, 4) ** 2 > 3, "sqrt(3) bound")
    coefficient_square_upper = F(19, 4) ** 2 * F(2, 3)
    require(coefficient_square_upper == F(361, 24) < 16, "4/k coefficient")
    return {
        "scope": "finite exact controls; universal theorem is the written proof",
        "partition_controls": fixtures, "grid_controls": audit_grid(),
        "invalid_rounding_control": audit_rounding_warning(),
        "constant_square_upper_using_pi_gt_3": fraction(coefficient_square_upper),
        "symbolic_frontiers_not_enumerated": [
            {"k": k, "atom_bound": k ** 6, "radius_bound": 2 * k,
             "defect_error_bound": fraction(F(4, k))} for k in [1, 2, 8, 80]
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--expected", type=Path,
                        default=Path(__file__).with_name("LOCALIZATION_EXPECTED.json"))
    args = parser.parse_args()
    actual = report()
    encoded = (json.dumps(actual, indent=2, sort_keys=True) + "\n").encode()
    if args.check:
        expected = json.loads(args.expected.read_text())
        require(expected == actual, "expected report differs")
        print("GAUSSIAN_DEFECT_LOCALIZATION_EXACT_CONTROLS_PASS",
              hashlib.sha256(encoded).hexdigest())
    else:
        print(encoded.decode(), end="")


if __name__ == "__main__":
    main()
