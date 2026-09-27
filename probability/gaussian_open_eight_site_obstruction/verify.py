#!/usr/bin/env python3
"""Exact supporting checks; the universal path argument is in PROOF.md."""
import argparse
from fractions import Fraction as F
import itertools
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c * x for x in a)


def norm2(a):
    return dot(a, a)


def distance(a, b):
    return norm2(sub(a, b))


def rank(rows):
    a = [[F(x) for x in row] for row in rows]
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        t = a[row][col]
        a[row] = [x / t for x in a[row]]
        for i in range(len(a)):
            if i != row:
                t = a[i][col]
                a[i] = [x - t * y for x, y in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def xi(points):
    return sum(distance(points[4 + i], points[j])
               for i in range(4) for j in range(4)) - 4 * sum(
                   distance(points[4 + i], points[i]) for i in range(4))


def margin_certificate(r, e):
    """These inequalities are sufficient conditions, not necessity tests."""
    c = r - F(2, 3)
    delta = 3 * e / 8
    require(delta < F(1, 100), "core conditioning bound")
    require(17 * e / 16 <= 2 * e, "face error bound")
    require(3 * delta + 7 * e + e <= 10 * e, "norm error bound")
    bsum_bound = 32 * r - F(64, 3) + 166 * e
    require(bsum_bound < 621, "barycentre bound")
    require(F(101, 100) * 621 < F(251, 10) ** 2, "square-root bound")
    require(F(251, 10) + 8 * e < 26, "physical coefficient bound")
    projection_bound = F(100, 99) * (3 * 169 + 4 * (2 * e) ** 2)
    require(projection_bound < 513, "projection trace bound")
    loss_range = 8 * (r * r - c * c)
    full_gram_bound = 4 * r * r - loss_range - 2 * e
    require(full_gram_bound > 1390, "outer centred Gram bound")
    require(1390 - 513 == 877, "residual bound")
    return {
        "core_metric_error": str(delta),
        "barycentre_squared_bound": str(bsum_bound),
        "projection_trace_upper_bound": str(projection_bound),
        "outer_gram_lower_bound": str(full_gram_bound),
        "residual_gram_lower_bound": 877,
    }


def verify():
    v = [tuple(map(F, x)) for x in
         [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]]
    r, c, e = F(20), F(58, 3), F(1, 100)
    eta, h = F(1, 2**20), F(1, 2**28)
    lam = 1 - eta
    p = v + [scale(-r, x) for x in v]
    q = v + [scale(c, x) for x in v]
    qhat = [scale(lam, x) for x in q]
    require(all(sum(x[j] for x in v) == 0 for j in range(3)), "centering")
    for i, j in itertools.product(range(4), repeat=2):
        require(dot(v[i], v[j]) == (3 if i == j else -1), "tetra Gram")
    for i, j in itertools.product(range(3), repeat=2):
        require(sum(x[i] * x[j] for x in v) == (4 if i == j else 0),
                "tetra tight frame")
    for i in range(4):
        edges = [sub(v[j], v[k]) for j, k in itertools.combinations(
            [j for j in range(4) if j != i], 2)]
        for j, k in itertools.product(range(3), repeat=2):
            target = (12 if j == k else 0) - 4 * v[i][j] * v[i][k]
            require(sum(x[j] * x[k] for x in edges) == target, "face frame")

    pairs = list(itertools.combinations(range(8), 2))
    pd = {(i, j): distance(p[i], p[j]) for i, j in pairs}
    qd = {(i, j): distance(q[i], q[j]) for i, j in pairs}
    tight = strict = 0
    for i, j in pairs:
        require(pd[i, j] >= qd[i, j], "endpoint contraction")
        tight += pd[i, j] == qd[i, j]
        strict += pd[i, j] > qd[i, j]
        if j < 4:
            target = (F(8), F(8))
        elif i >= 4:
            target = (F(3200), F(26912, 9))
        elif i == j - 4:
            target = (F(1323), F(3025, 3))
        else:
            target = (F(1163), F(1163))
        require((pd[i, j], qd[i, j]) == target, "distance table")
    require((tight, strict) == (18, 10), "pair count")
    require(min(qd.values()) == 8, "minimum target separation")
    require(max(qd.values()) < 3200, "maximum target distance")
    require((xi(p), xi(q)) == (-1920, 1856), "separator endpoints")
    require(xi(p) + 24 * e < 0 < xi(q) - 24 * e, "robust endpoint signs")

    # The positive/negative coefficient estimate in (12) uses these three cuts.
    cut_bounds = [F(k * (4 - k), 4) for k in range(1, 4)]
    require(all(x <= 1 for x in cut_bounds), "zero-sum cut bound")
    margins = margin_certificate(r, e)

    coordinate_error = 480 * h + 12 * h * h
    require(coordinate_error <= 481 * h, "coordinate perturbation bound")
    template_error = 6400 * eta + 481 * h
    require(template_error < e, "template proximity")
    loss_floor = 8 * eta - 962 * h
    require(loss_floor > F(1, 2**18), "strict box loss floor")
    central_losses = [pd[i, j] - distance(qhat[i], qhat[j]) for i, j in pairs]
    require(min(central_losses) == 8 * (2 * eta - eta * eta), "central reserve")
    require(min(central_losses) > 8 * eta, "central lower bound")
    paired = [p[i] + qhat[i] for i in range(8)]
    paired_rank = rank([sub(x, paired[0]) for x in paired[1:]])
    require(paired_rank == 6, "paired affine rank")

    # Genuine six-dimensional separator control, stored as its exact Gram.
    # Core vectors are (v_i,0), outer vectors (0,b v_i), b^2=1160/3.
    b2 = F(1160, 3)
    gram = [[F(0) for _ in range(8)] for _ in range(8)]
    for i, j in itertools.product(range(4), repeat=2):
        gram[i][j] = dot(v[i], v[j])
        gram[4 + i][4 + j] = b2 * dot(v[i], v[j])
    gd = {(i, j): gram[i][i] + gram[j][j] - 2 * gram[i][j]
          for i, j in pairs}
    require(all(qd[k] <= gd[k] <= pd[k] for k in pairs), "six-dimensional box")
    control_xi = sum(gram[4+i][4+i] + gram[j][j] - 2*gram[4+i][j]
                     for i in range(4) for j in range(4)) - 4 * sum(
                         gram[4+i][4+i] + gram[i][i] - 2*gram[4+i][i]
                         for i in range(4))
    require(control_xi == 0, "six-dimensional separator")
    require(rank(gram) == 6, "six-dimensional joint rank")
    require(rank([row[4:] for row in gram[4:]]) == 3, "residual rank control")

    # Binary masses rule out alternate deterministic matchings, not couplings.
    masses = [2**i for i in range(8)]
    for i in range(8):
        matches = [mask for mask in range(256)
                   if sum(masses[j] for j in range(8) if mask & (1 << j)) == masses[i]]
        require(matches == [1 << i], "unique binary subset")

    rejected = []
    for name, rr, ee in [("shallow_radius_not_certified", F(1), e),
                         ("wide_error_not_certified", r, F(1))]:
        try:
            margin_certificate(rr, ee)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("invalid parameter control was accepted")
    bad = list(q)
    bad[4] = scale(100, v[0])
    require(any(distance(bad[i], bad[j]) > pd[i, j] for i, j in pairs),
            "invalid endpoint rejected")
    rejected.append("expanded_endpoint")
    return {
        "status": "OPEN_EIGHT_SITE_INTERVAL_OBSTRUCTION_PASS",
        "arithmetic": "Python standard-library Fraction; no floating point",
        "sites": 8,
        "template_pairs": {"total": 28, "tight": tight, "strict": strict},
        "separator_endpoints": [str(xi(p)), str(xi(q))],
        "squared_distance_tolerance": str(e),
        "margin_certificate": margins,
        "coordinate_box": {
            "coordinates": 48, "half_width": str(h), "target_scale": str(lam),
            "template_error_upper_bound": str(template_error),
            "squared_distance_loss_lower_bound": str(loss_floor),
            "claimed_loss_floor": str(F(1, 2**18)),
        },
        "paired_affine_rank": paired_rank,
        "six_dimensional_control": {"separator": str(control_xi),
                                    "joint_rank": 6, "residual_rank": 3},
        "binary_total_mass": sum(masses),
        "rejected_controls": rejected,
        "scope": "Finite exact controls; universal rank/path proof is in PROOF.md; no Gaussian sign",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare with EXPECTED.json")
    args = parser.parse_args()
    result = verify()
    if args.check:
        expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
        require(result == expected, "EXPECTED.json mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
