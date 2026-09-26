#!/usr/bin/env python3
"""Exact finite controls for the analytic three-cap reflection theorem.

Only Python's standard library is used. This checks one rational seven-site
example and two deliberately insufficient shortcuts. The all-measures theorem
is proved in PROOF.md, not by sampling or by this finite calculation.
"""

from fractions import Fraction as F
from itertools import combinations, permutations, product
import argparse
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def vector(values):
    return tuple(map(F, values))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def scale(c, x):
    return tuple(c * a for a in x)


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def norm2(x):
    return dot(x, x)


def rank(rows):
    if not rows:
        return 0
    a = [list(map(F, row)) for row in rows]
    pivot = 0
    for col in range(len(a[0])):
        selected = next((j for j in range(pivot, len(a)) if a[j][col]), None)
        if selected is None:
            continue
        a[pivot], a[selected] = a[selected], a[pivot]
        divisor = a[pivot][col]
        a[pivot] = [value / divisor for value in a[pivot]]
        for j in range(pivot + 1, len(a)):
            factor = a[j][col]
            if factor:
                a[j] = [u - factor * v for u, v in zip(a[j], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


V = tuple(map(vector, ((1, 1, 1), (1, -1, -1), (-1, 1, -1))))
U = tuple(map(vector, ((1, 0), (0, 1), (-1, 0))))
LABELS = ("c0", "c1", "c2", "c3", "x0", "x1", "x2")
P = tuple(map(vector, (
    (0, 0, 0), (-1, -1, 0), (-1, 0, 1), (0, -1, 1),
    (1, -2, 5), (-2, -5, -1), (-5, 1, 2),
)))


def cap_index(x):
    positive = [i for i, v in enumerate(V) if dot(v, x) > 0]
    require(len(positive) <= 1, "overlapping caps at a source site")
    return positive[0] if positive else None


def half_displacement(x):
    i = cap_index(x)
    return vector((0, 0, 0)) if i is None else scale(dot(V[i], x) / 3, V[i])


def image(x):
    return sub(x, scale(2, half_displacement(x)))


def auxiliary_dot(x, y, directions):
    i, j = cap_index(x), cap_index(y)
    if i is None or j is None:
        return F(0)
    # a_i(x) = (v_i . x)/sqrt(3); the radicals cancel in this dot product.
    return dot(V[i], x) * dot(V[j], y) * dot(directions[i], directions[j]) / 3


def coefficients(x, y, directions):
    d = sub(x, y)
    v = sub(half_displacement(x), half_displacement(y))
    e = dot(d, v) - norm2(v)
    aux2 = (auxiliary_dot(x, x, directions) + auxiliary_dot(y, y, directions)
            - 2 * auxiliary_dot(x, y, directions))
    delta = aux2 - norm2(v)
    return e, delta


def fold(x, i):
    t = dot(V[i], x)
    return sub(x, scale(F(2, 3) * t, V[i])) if t > 0 else x


def rigidity_rank(points, edges):
    rows = []
    for i, j in edges:
        d = sub(points[i], points[j])
        row = [F(0)] * (3 * len(points))
        row[3 * i:3 * i + 3] = d
        row[3 * j:3 * j + 3] = scale(-1, d)
        rows.append(row)
    return rank(rows)


def check():
    q = tuple(map(image, P))
    require(len(set(P)) == len(P) == len(set(q)) == 7, "distinct-site count")
    require(rank(V) == 3, "normal independence")
    require(rank([sub(x, P[0]) for x in P[1:4]]) == 3, "core affine span")
    normal_coordinates = [[dot(v, x) for v in V] for x in P]
    for ts in normal_coordinates:
        for i in range(3):
            require(ts[i] + 2 * ts[(i + 1) % 3] <= 0, "cap-separation certificate")
    # These linear inequalities hold on conv(P). Each pair of its caps cannot
    # be simultaneously positive because one of the displayed sums forbids it.
    require([cap_index(x) for x in P] == [None] * 4 + [0, 1, 2], "cap membership")
    for i, j in combinations(range(3), 2):
        n = dot(V[i], V[j]) / 3
        require(dot(U[i], U[j]) <= 1 + 2 * n, "auxiliary Gram condition")

    pairs, tight, strict = [], [], []
    for i, j in combinations(range(7), 2):
        d0, d1 = norm2(sub(P[i], P[j])), norm2(sub(q[i], q[j]))
        e, delta = coefficients(P[i], P[j], U)
        require(d0 - 4 * e == d1, "endpoint polynomial identity")
        require(e >= abs(delta), "full-time derivative bound")
        require(d1 <= d0, "endpoint contraction")
        (tight if d0 == d1 else strict).append((i, j))
        pairs.append({"labels": [LABELS[i], LABELS[j]], "initial_squared": d0,
                      "final_squared": d1, "E": e, "Delta": delta,
                      "derivative_at_0": -4 * (e - delta),
                      "derivative_at_1": -4 * (e + delta)})

    require(len(tight) == 15 and len(strict) == 6, "tight/strict pair counts")
    endpoint_ranks = [rigidity_rank(points, tight) for points in (P, q)]
    require(endpoint_ranks == [15, 15], "rigid endpoint ranks")
    paired = [p + z for p, z in zip(P, q)]
    paired_rank = rank([sub(x, paired[0]) for x in paired[1:]])
    require(paired_rank == 6, "paired affine rank")

    faces = []
    for i, v in enumerate(V):
        face = [j for j in range(4) if dot(v, P[j]) == 0]
        require(len(face) == 3, "three core anchors in a reflecting plane")
        require(rank([sub(P[j], P[face[0]]) for j in face[1:]]) == 2, "face rank")
        require(all((j, 4 + i) in tight for j in face), "tight face attachments")
        faces.append([LABELS[j] for j in face])
    require(all(dot(V[i], V[j]) != 0 for i, j in combinations(range(3), 2)),
            "nonorthogonal normals for the strong-contraction obstruction")

    # Tight core/face distances force every aligned intermediate 3D
    # configuration into these eight states. The analytic argument in
    # PROOF.md shows that a strong step changes at most one bit.
    states = {
        bits: P[:4] + tuple(q[4 + i] if bits[i] else P[4 + i] for i in range(3))
        for bits in product((0, 1), repeat=3)
    }
    state_distances = {
        bits: [norm2(sub(points[i], points[j])) for i, j in combinations(range(7), 2)]
        for bits, points in states.items()
    }
    interval_states = [
        bits for bits in states
        if all(lower <= middle <= upper for lower, middle, upper in zip(
            state_distances[(1, 1, 1)], state_distances[bits], state_distances[(0, 0, 0)]))
    ]
    require(interval_states == [(0, 0, 0), (1, 1, 1)],
            "only endpoint states lie in the endpoint distance interval")
    cyclic_distances = []
    for i, j in ((0, 1), (1, 2), (2, 0)):
        values = [norm2(sub(q[4 + i] if a else P[4 + i],
                            q[4 + j] if b else P[4 + j]))
                  for a, b in ((0, 0), (1, 0), (0, 1), (1, 1))]
        require(values == [F(54), F(34, 3), F(130, 3), F(134, 9)],
                "cyclic pair distance table")
        cyclic_distances.append({"labels": [LABELS[4 + i], LABELS[4 + j]],
                                 "00_10_01_11": values})
    state_edges = []
    for initial in states:
        for final in states:
            if sum(a != b for a, b in zip(initial, final)) != 1:
                continue
            if all(b <= a for a, b in zip(state_distances[initial], state_distances[final])):
                state_edges.append((initial, final))
    expected_edges = [((0, 0, 0), (0, 0, 1)), ((0, 0, 0), (0, 1, 0)),
                      ((0, 0, 0), (1, 0, 0)), ((0, 0, 1), (0, 1, 1)),
                      ((0, 1, 0), (1, 1, 0)), ((1, 0, 0), (1, 0, 1))]
    require(state_edges == expected_edges, "complete one-bit transition graph")
    reached = {(0, 0, 0)}
    while True:
        enlarged = reached | {b for a, b in state_edges if a in reached}
        if enlarged == reached:
            break
        reached = enlarged
    require(len(reached) == 7 and (1, 1, 1) not in reached,
            "strong-contraction chain obstruction")

    orders = []
    for order in permutations(range(3)):
        output = []
        for point in P:
            for i in order:
                point = fold(point, i)
            output.append(point)
        failed = [LABELS[j] for j in range(7) if output[j] != q[j]]
        require(bool(failed), "one-use fold-order negative control unexpectedly passed")
        orders.append({"order": list(order), "mismatched_labels": failed,
                       "images": output})

    bad = (vector((1, 0)),) * 3
    bad_derivatives = []
    for i, j in combinations(range(4, 7), 2):
        e, delta = coefficients(P[i], P[j], bad)
        derivative = -4 * (e + delta)
        require(derivative == F(160, 9) > 0, "wrong-auxiliary negative control")
        bad_derivatives.append({"labels": [LABELS[i], LABELS[j]],
                                "derivative_at_1": derivative})

    return {"scope": "Exact finite controls; the all-measures proof is in PROOF.md.",
            "labels": LABELS, "source": P, "target": q,
            "unnormalized_normals": V, "auxiliary_directions": U,
            "source_normal_coordinates": normal_coordinates,
            "separation_inequalities": ["t0 + 2*t1 <= 0", "t1 + 2*t2 <= 0", "t2 + 2*t0 <= 0"],
            "pairs": pairs, "tight_pair_count": len(tight), "strict_pair_count": len(strict),
            "endpoint_rigidity_ranks": endpoint_ranks, "paired_affine_rank": paired_rank,
            "core_face_anchors": faces, "prescribed_fold_orders": orders,
            "one_bit_contraction_edges": state_edges,
            "reachable_states_from_000": sorted(reached),
            "states_in_endpoint_distance_interval": interval_states,
            "cyclic_pair_distance_table": cyclic_distances,
            "wrong_auxiliary_positive_derivatives": bad_derivatives}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="write canonical expected JSON to stdout")
    args = parser.parse_args()
    result = check()
    canonical = json.dumps(result, default=lambda x: str(x) if isinstance(x, F) else x,
                           indent=2, sort_keys=True) + "\n"
    if args.emit:
        print(canonical, end="")
        return
    expected = Path(__file__).with_name("EXPECTED.json").read_text()
    require(canonical == expected, "canonical output differs from EXPECTED.json")
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    print("PASS: 21 pair polynomials; 15 tight / 6 strict; rigidity 15,15; paired rank 6")
    print("PASS: 8 reflection states; 6 one-bit contraction edges; target unreachable")
    print("PASS: only 000 and 111 lie in the endpoint distance interval")
    print("PASS: all 6 prescribed fold orders fail; common auxiliary direction fails")
    print("EXPECTED.json sha256 " + digest)


if __name__ == "__main__":
    main()
