"""Exact finite controls; the analytic time integral is proved in PROOF.md."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import argparse
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def dist2(a, b):
    z = sub(a, b)
    return dot(z, z)


def rank(rows):
    a = [list(map(F, row)) for row in rows]
    r = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][col]
        a[r] = [v / scale for v in a[r]]
        for i in range(len(a)):
            if i != r and a[i][col]:
                scale = a[i][col]
                a[i] = [u - scale * v for u, v in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def fixture(lam):
    b = (F(3),) * 3
    x = [b]
    labels = ["anchor"]
    for axis in range(3):
        p = list(b)
        p[axis] += 1
        x.append(tuple(p))
        labels.append("positive_" + str(axis))
    for axis in range(3):
        for depth in (4, 5):
            p = list(b)
            p[axis] -= depth
            x.append(tuple(p))
            labels.append("negative_" + str(axis) + "_" + str(depth))
    y = [tuple(3 + lam * (abs(v) - 3) for v in p) for p in x]
    return labels, x, y


def covariance(a, b):
    n = len(a)
    ma = [sum(p[k] for p in a) / n for k in range(3)]
    mb = [sum(p[k] for p in b) / n for k in range(3)]
    return [[sum((p[i] - ma[i]) * (q[j] - mb[j])
                 for p, q in zip(a, b)) / n
             for j in range(3)] for i in range(3)]


def data_for_pair(x, y, i, j):
    d0 = dist2(x[i], x[j])
    loss = d0 - dist2(y[i], y[j])
    hi = sub(y[i], x[i])
    hj = sub(y[j], x[j])
    speed = dist2(hi, hj)
    linear = 2 * dot(sub(x[i], x[j]), sub(hi, hj))
    require(linear == -loss - speed, "wrong straight-path coefficients")
    return d0, loss, speed


def verify():
    lam = F(9999, 10000)
    labels, x, y = fixture(lam)
    n = len(x)
    require(n == 10 and len(set(x)) == n and len(set(y)) == n,
            "endpoint labels must be distinct")
    pairs = list(combinations(range(n), 2))
    losses = []
    for i, j in pairs:
        d0, loss, speed = data_for_pair(x, y, i, j)
        require(loss > 0, "not a strict endpoint contraction")
        require(dist2(y[i], y[j]) <= lam * lam * d0,
                "claimed Lipschitz constant fails")
        losses.append(loss)
    z = [p + q for p, q in zip(x, y)]
    paired_rank = rank([sub(v, z[0]) for v in z[1:]])
    require(paired_rank == 6, "paired rank must be six")

    cross = covariance(x, y)
    expected_cross = [[lam * (F(7, 5) * (i == j) - F(4, 25))
                       for j in range(3)] for i in range(3)]
    require(cross == expected_cross, "Procrustes cross covariance mismatch")
    eigenvalues = [lam * F(23, 25), lam * F(7, 5), lam * F(7, 5)]
    require(all(v > 0 for v in eigenvalues), "alignment is not unique")
    expected_source_covariance = [[F(21, 5) * (i == j) - F(16, 25)
                                   for j in range(3)] for i in range(3)]
    require(covariance(x, x) == expected_source_covariance,
            "source covariance mismatch")

    # The distinguished labels are the two negative sites on the first axis.
    i, j = 4, 5
    d0, loss, speed = data_for_pair(x, y, i, j)
    require(d0 == 1 and loss == 1 - lam * lam
            and speed == (1 + lam) ** 2, "distinguished edge mismatch")
    require(loss < F(1, 5000) and speed > 3, "edge budget fails")
    triples = []
    for k in range(n):
        edges = ((i, j), (i, k), (j, k))
        s0 = sum(dist2(x[a], x[b]) for a, b in edges)
        sq = sum(dist2(y[a], y[b]) for a, b in edges)
        ltot = s0 - sq
        vtot = sum(dist2(sub(y[a], x[a]), sub(y[b], x[b]))
                   for a, b in edges)
        require(ltot >= 0 and vtot >= 0, "invalid triple sign")
        triples.append({"label": labels[k], "source_sum": str(s0),
                        "loss_sum": str(ltot), "speed_sum": str(vtot)})
    require(F(triples[0]["source_sum"]) == 42, "anchor exponent mismatch")
    require(F(triples[0]["loss_sum"]) == 42 - 6 * lam * lam >= 36,
            "anchor loss reserve fails")

    # e <= 1+1+1/2+1/6+1/24 + (1/120)/(1-1/6) < 11/4.
    exp_upper = sum(F(1, d) for d in (1, 1, 2, 6, 24)) + F(1, 100)
    require(exp_upper == F(1631, 600) < F(11, 4), "exponential bound fails")
    margin = F(3, 10) * F(4, 11) ** 7 - F(1, 5000)
    require(margin == F(5088829, 97435855000) > 0, "negative-action margin fails")

    # Independently count the ordered-triple derivative and unordered-edge
    # stress expansions, retaining each monomial and each differentiated pair.
    direct = Counter()
    for a, b, c in product(range(n), repeat=3):
        key = tuple(sorted((a, b, c)))
        for u, v in ((a, b), (a, c), (b, c)):
            if u != v:
                direct[(key, tuple(sorted((u, v))))] += 1
    stress = Counter()
    for a, b in pairs:
        for c in range(n):
            stress[(tuple(sorted((a, b, c))), (a, b))] += 6
    require(direct == stress, "cubic derivative normalization mismatch")

    # Time-reflection controls and two deliberately inapplicable geometries.
    _, x1, y1 = fixture(F(1))
    require(data_for_pair(x1, y1, i, j)[1:] == (0, 4),
            "tight-edge boundary control fails")
    _, xc, yc = fixture(F(0))
    for a, b in pairs:
        d, l, v = data_for_pair(xc, yc, a, b)
        require(l == v == d, "collapse must give d(t)=(1-t)^2 d(0)")
    require(all(data_for_pair(x, x, a, b)[1:] == (0, 0)
                for a, b in pairs), "identity equality control fails")
    _, xb, yb = fixture(F(10001, 10000))
    require(data_for_pair(xb, yb, i, j)[1] < 0,
            "expansive damaged parameter was not detected")

    # Reuse the accepted reduction's positive seven-site fixture, without
    # replaying or extending its eight-state interval classification.
    px = [tuple(map(F, p)) for p in (
        (0, 0, 0), (-1, -1, 0), (-1, 0, 1), (0, -1, 1),
        (1, -2, 5), (-2, -5, -1), (-5, 1, 2))]
    normals = ((1, 1, 1), (1, -1, -1), (-1, 1, -1))
    py = px[:4] + [tuple(a - F(8, 3) * b for a, b in zip(p, v))
                   for p, v in zip(px[4:], normals)]
    tight = []
    for a, b in combinations(range(7), 2):
        _, l, _ = data_for_pair(px, py, a, b)
        require(l >= 0, "known positive control contracts")
        if l == 0:
            tight.append((a, b))
    reached = {0}
    for _ in range(7):
        for a, b in tight:
            if a in reached or b in reached:
                reached.update((a, b))
    require(len(reached) == 7, "common tight graph is not connected")
    require(rank([sub(v, px[0]) for v in px[1:4]]) == 3,
            "root tetrahedron is degenerate")
    zp = [a + b for a, b in zip(px, py)]
    require(rank([sub(v, zp[0]) for v in zp[1:]]) == 6,
            "positive fixture paired rank mismatch")
    _, pl, pv = data_for_pair(px, py, 0, 4)
    ps = sum(dist2(px[a], px[b]) for a, b in ((0, 4), (0, 1), (4, 1)))
    pL = sum(data_for_pair(px, py, a, b)[1]
             for a, b in ((0, 4), (0, 1), (4, 1)))
    require((pl, pv, ps, pL) == (0, F(64, 3), 62, F(32, 3)),
            "known positive fixture adverse-edge data mismatch")
    coefficient = F(1, 7) ** 3 * pv * pL / 36
    require(coefficient == F(512, 27783), "adverse-edge coefficient mismatch")

    return {
        "status": "STRICT_ALIGNED_PAIR_ACTION_OBSTRUCTION_PASS",
        "dimension": 3, "labels": labels,
        "source": [[str(v) for v in p] for p in x],
        "target": [[str(v) for v in p] for p in y],
        "uniform_weight": "1/10", "variance": 1,
        "lambda": str(lam), "strict_pairs": len(pairs),
        "minimum_squared_loss": str(min(losses)),
        "paired_affine_rank": paired_rank,
        "cross_covariance": [[str(v) for v in row] for row in cross],
        "cross_covariance_eigenvalues": list(map(str, eigenvalues)),
        "distinguished_labels": [labels[i], labels[j]],
        "edge_source_squared_distance": str(d0),
        "edge_squared_loss": str(loss), "edge_relative_speed_squared": str(speed),
        "triple_data": triples,
        "ordered_triples_checked": n ** 3,
        "derivative_coefficient_entries_checked": len(direct),
        "exp_one_upper_bound": str(exp_upper),
        "positive_margin": str(margin),
        "cubic_edge_action_over_C3_upper_bound": str(-margin / 100),
        "some_hinge_pair_action_times_3sqrt3_upper_bound": str(-margin / 300),
        "known_positive_indecomposable_control": {
            "source": [[str(v) for v in p] for p in px],
            "target": [[str(v) for v in p] for p in py],
            "paired_affine_rank": 6, "tight_pairs": len(tight),
            "tight_graph_connected": True,
            "edge": [0, 4], "strict_loss_third_label": 1,
            "edge_squared_loss": str(pl), "relative_speed_squared": str(pv),
            "triple_source_sum": str(ps), "triple_loss_sum": str(pL),
            "negative_coefficient_over_C3": str(coefficient),
            "negative_exponential_factor": "exp(-31/(3s))/s^2",
            "interval_classification_replayed": False
        },
        "controls": ["undamped tight pair", "point collapse", "identity",
                     "expansive parameter rejected"],
        "analytic_integrals_evaluated": False,
        "negative_hinge_threshold_located": False,
        "gaussian_majorisation_counterexample": False
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true",
                        help="write canonical expected JSON to stdout")
    args = parser.parse_args()
    result = verify()
    if args.emit:
        print(json.dumps(result, indent=2))
    else:
        expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
        require(result == expected, "expected record mismatch")
        print(result["status"])


if __name__ == "__main__":
    main()
