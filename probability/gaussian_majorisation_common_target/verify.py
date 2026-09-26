#!/usr/bin/env python3
"""Exact supplementary audits for the common-target majorisation proof.

CPython 3.11+, standard library only. No Gaussian quadrature, solver, or
external mathematical code is used. Run with --check to compare EXPECTED.json.
Checks use explicit exceptions and remain active under python -O.
"""

from collections import deque
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import argparse
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def minus(x, y):
    return tuple(a - b for a, b in zip(x, y))


V = []
for i, j in combinations(range(3), 2):
    for a, b in product((-1, 1), repeat=2):
        v = [0, 0, 0]
        v[i], v[j] = a, b
        V.append(tuple(v))
Y = [tuple(a if k == i else 0 for k in range(3))
     for i in range(3) for a in (-1, 1)]
U = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]


def s_map(v):
    k = v.index(0)
    a, b = [i for i in range(3) if i != k]
    return tuple(v[a] * v[b] if i == k else 0 for i in range(3))


def r_map(v, i):
    j, k = (i + 1) % 3, (i + 2) % 3
    if v[i]:
        return tuple(v[i] if a == i else 0 for a in range(3))
    out = [F(0)] * 3
    out[j], out[k] = F(v[j] + v[k], 2), F(v[k] - v[j], 2)
    return tuple(out)


S = [Y.index(s_map(v)) for v in V]
R = [[Y.index(r_map(v, i)) for v in V] for i in range(3)]
P0 = [F(1, 12)] * 12
Z0 = [[F(1, 18) if v[i] == 0 else F(1, 72) for v in V]
      for i in range(3)]


def push(p, mapping):
    out = [F(0)] * 6
    for a, y in zip(p, mapping):
        out[y] += a
    return out


def check_split(p, z):
    require(len(p) == 12 and len(z) == 3, "wrong certificate dimensions")
    require(all(len(row) == 12 for row in z), "wrong row dimensions")
    require(sum(p) == 1 and min(p) >= 0, "invalid probability weights")
    require(all(a >= 0 for row in z for a in row), "negative split mass")
    require([sum(z[i][v] for i in range(3)) for v in range(12)] == p,
            "source reconstruction failed")
    q = push(p, S)
    for i in range(3):
        require(sum(z[i]) == F(1, 3), "component mass failed")
        require(push(z[i], R[i]) == [a / 3 for a in q],
                "component lacks the common target")


def make_tree():
    # Source nodes 0..11, target nodes 12+6*i+y. Edge (i,v).
    graph = [[] for _ in range(30)]
    for i in range(3):
        for v in range(12):
            t = 12 + 6 * i + R[i][v]
            graph[v].append((t, (i, v)))
            graph[t].append((v, (i, v)))
    parents = {0: None}
    parent_edges = {}
    order = []
    queue = deque([0])
    while queue:
        a = queue.popleft()
        order.append(a)
        for b, edge in sorted(graph[a]):
            if b not in parents:
                parents[b] = a
                parent_edges[b] = edge
                queue.append(b)
    require(len(order) == 30 and len(parent_edges) == 29,
            "incidence graph not connected")
    return parents, parent_edges, order


PARENTS, PARENT_EDGES, ORDER = make_tree()


def correction(delta):
    require(len(delta) == 12 and sum(delta) == 0, "not a zero-sum perturbation")
    dq = push(delta, S)
    b = list(delta) + [-a / 3 for _ in range(3) for a in dq]
    require(sum(b) == 0, "divergence conservation failed")
    subtree = list(b)
    flows = [[F(0)] * 12 for _ in range(3)]
    for child in reversed(ORDER[1:]):
        parent = PARENTS[child]
        i, v = PARENT_EDGES[child]
        flows[i][v] = subtree[child] if child < 12 else -subtree[child]
        subtree[parent] += subtree[child]
    require(subtree[0] == 0, "root residual")
    norm = sum(abs(a) for a in delta)
    require(all(abs(a) <= norm for row in flows for a in row),
            "tree-flow L1 estimate failed")
    require([sum(flows[i][v] for i in range(3)) for v in range(12)] == delta,
            "source divergence wrong")
    for i in range(3):
        require(push(flows[i], R[i]) == [a / 3 for a in dq],
                "target divergence wrong")
    return flows


def split(p):
    f = correction([a - b for a, b in zip(p, P0)])
    z = [[a + b for a, b in zip(row, fix)] for row, fix in zip(Z0, f)]
    check_split(p, z)
    return z


def second_moment_loss(p):
    out = [[F(0)] * 3 for _ in range(3)]
    for a, v in zip(p, V):
        w = s_map(v)
        for i, j in product(range(3), repeat=2):
            out[i][j] += a * (v[i] * v[j] - w[i] * w[j])
    return out


def determinant(matrix):
    if not matrix:
        return F(1)
    return sum(((-1) ** j) * matrix[0][j] * determinant(
        [[row[k] for k in range(len(matrix)) if k != j] for row in matrix[1:]])
        for j in range(len(matrix)))


def check_moment_bound(p):
    m = second_moment_loss(p)
    for i in range(3):
        m[i][i] -= F(11, 36)
    for size in range(1, 4):
        for indices in combinations(range(3), size):
            require(determinant([[m[i][j] for j in indices] for i in indices]) >= 0,
                    "second-moment lower bound failed")


def rejection_control():
    bad = [row[:] for row in Z0]
    # Preserve column sums and row sums while destroying a target marginal.
    eps = F(1, 1000)
    bad[0][0] += eps
    bad[0][1] -= eps
    bad[1][0] -= eps
    bad[1][1] += eps
    try:
        check_split(P0, bad)
    except ValueError as err:
        require(str(err) == "component lacks the common target", "wrong rejection")
        return True
    raise ValueError("incorrect target certificate was accepted")


def audit():
    # Independently transcribed incidence table; definition-level code above
    # must reproduce it exactly, including the cyclic orientation in (8).
    require(S == [5, 4, 4, 5, 3, 2, 2, 3, 1, 0, 0, 1], "S incidence mismatch")
    require(R == [
        [0, 0, 1, 1, 0, 0, 1, 1, 2, 5, 4, 3],
        [2, 3, 2, 3, 4, 0, 1, 5, 2, 2, 3, 3],
        [0, 3, 2, 1, 4, 5, 4, 5, 4, 5, 4, 5]], "R incidence mismatch")
    pair_records = []
    core_checks = 0
    maps = [S] + R
    for a_index, mapping in enumerate(maps):
        require(set(mapping) == set(range(6)), "map is not onto axis set")
        for v_index, v in enumerate(V):
            av = Y[mapping[v_index]]
            require(dot(v, v) == 2 and dot(av, av) == 1, "norm identity failed")
            if a_index:
                i = a_index - 1
                require(av[i] == v[i], "coordinate not preserved")
            for w_index, w in enumerate(V):
                aw = Y[mapping[w_index]]
                d = dot(v, w) - dot(av, aw)
                require(d <= 1, "negative ray contraction deficit")
                pair_records.append([a_index, v_index, w_index, d])
            # Linear core inequality is checked at all four extreme points.
            for u in U:
                require(dot(u, minus(v, av)) <= 1, "core inequality failed")
                core_checks += 1
    require(len(pair_records) == 576, "incomplete pair audit")
    check_split(P0, Z0)
    require(all(push(P0, R[i]) != push(P0, S) for i in range(3)),
            "control: original uniform input unexpectedly has the target")
    q = push(P0, S)
    require(q == [F(1, 6)] * 6, "uniform target wrong")
    require(second_moment_loss(P0) ==
            [[F(int(i == j), 3) for j in range(3)] for i in range(3)],
            "uniform matrix identity failed")

    # Check the correction's exact linear identities on a basis; the written
    # proof supplies the bound for arbitrary real, not just rational, data.
    basis_records = []
    for k in range(1, 12):
        d = [F(0)] * 12
        d[k], d[0] = F(1), F(-1)
        f = correction(d)
        basis_records.append([[str(a) for a in row] for row in f])

    boundary_min = F(1)
    boundary_count = 0
    # Vertices of {sum delta=0, ||delta||_1 <= 1/72}.
    for a, b in product(range(12), repeat=2):
        if a == b:
            continue
        p = P0[:]
        p[a] += F(1, 144)
        p[b] -= F(1, 144)
        require(sum(abs(x - y) for x, y in zip(p, P0)) == F(1, 72),
                "boundary vector has wrong norm")
        z = split(p)
        boundary_min = min(boundary_min, min(x for row in z for x in row))
        check_moment_bound(p)
        boundary_count += 1

    # Vary the weights with radius; verify pushforwards before any Gaussian
    # convolution. The asymmetric core has four positive anchor atoms.
    shell_specs = [(F(2), F(2, 7), 0, 7), (F(5, 2), F(5, 7), 4, 10)]
    alpha = F(5, 8)
    core_weights = [F(1, 10), F(2, 10), F(3, 10), F(4, 10)]
    mu, nu = {}, {}
    components = [{}, {}, {}]
    targets = [{}, {}, {}]

    def add(law, point, mass):
        law[point] = law.get(point, F(0)) + mass

    for u, w in zip(U, core_weights):
        for law in [mu, nu] + components + targets:
            add(law, tuple(map(F, u)), (1 - alpha) * w)
    for r, shell_mass, a, b in shell_specs:
        p = P0[:]
        p[a] += F(1, 144)
        p[b] -= F(1, 144)
        z = split(p)
        for v_index, v in enumerate(V):
            point = tuple(r * x for x in v)
            target = tuple(r * x for x in s_map(v))
            add(mu, point, alpha * shell_mass * p[v_index])
            add(nu, target, alpha * shell_mass * p[v_index])
            for i in range(3):
                w = 3 * alpha * shell_mass * z[i][v_index]
                add(components[i], point, w)
                add(targets[i], tuple(r * x for x in r_map(v, i)), w)
    require(all(sum(law.values()) == 1 for law in [mu, nu] + components + targets),
            "radial normalization failed")
    require(all(target == nu for target in targets), "radial common output failed")
    require({x: sum(law.get(x, 0) for law in components) / 3 for x in mu} == mu,
            "radial source reconstruction failed")

    # Point-mass impossibility for these maps is not failure of majorisation.
    require(all(R[i][v] != S[v] for i in range(3) for v in range(12)),
            "point-mass obstruction control failed")
    rejection_control()

    # Exact equal-cardinality controls for Theorem B. The nonliftability
    # theorem for these nine labels is an external, explicitly cited proof.
    fixed = [(1, 0, 1), (0, 1, 1), (-1, 0, 1), (0, -1, 1)]
    moving = [(1, 1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1)]
    nine_x = [(0, 0, 0)] + fixed + [tuple(-a for a in b) for b in moving]
    nine_y = [(0, 0, 0)] + fixed + moving
    require(len(set(nine_x)) == len(set(nine_y)) == 9, "site collision")
    for i, j in combinations(range(9), 2):
        dx, dy = minus(nine_x[i], nine_x[j]), minus(nine_y[i], nine_y[j])
        require(dot(dx, dx) >= dot(dy, dy), "nine-point map not a contraction")
    weights = [F(2 ** j, 511) for j in range(9)]
    require(sum(weights) == 1 and len(set(weights)) == 9, "weights not distinct")
    rotated = weights[1:] + weights[:1]
    c = F(1, 3)
    mean = [c * a + (1 - c) * b for a, b in zip(weights, rotated)]
    variance = c * dot(minus(weights, mean), minus(weights, mean))
    variance += (1 - c) * dot(minus(rotated, mean), minus(rotated, mean))
    require(variance == dot(weights, weights) - dot(mean, mean) > 0,
            "strict permutation-mixture control failed")
    require(mean != weights, "nontrivial permutation mixture retained source")
    tree_record = [[child, PARENTS[child], list(PARENT_EDGES[child])]
                   for child in ORDER[1:]]
    compact_hash = lambda record: sha256(json.dumps(record, separators=(",", ":"),
                                                  sort_keys=True).encode()).hexdigest()
    return {
        "status": "EXACT_COMMON_TARGET_AUDIT_PASSED",
        "scope": "Supplementary finite identities; the universal proof is analytic.",
        "source_directions": [list(v) for v in V],
        "target_directions": [list(y) for y in Y],
        "original_incidence": S,
        "coordinate_preserving_incidence": R,
        "ray_pair_polynomial_checks": len(pair_records),
        "ray_pair_record_sha256": compact_hash(pair_records),
        "core_vertex_checks": core_checks,
        "uniform_split_weights": {"zero_coordinate": "1/18", "other": "1/72"},
        "graph": {"vertices": 30, "edges": 36, "tree_edges": len(tree_record),
                  "incidence_rank": 29, "tree_sha256": compact_hash(tree_record)},
        "zero_sum_basis_checks": len(basis_records),
        "basis_corrections_sha256": compact_hash(basis_records),
        "l1_radius": "1/72",
        "l1_ball_extreme_point_checks": boundary_count,
        "minimum_split_mass_on_audited_extreme_points": str(boundary_min),
        "second_moment_lower_bound": "11/36",
        "radial_shells": len(shell_specs),
        "asymmetric_core_atoms": len(core_weights),
        "original_uniform_input_control": "three outputs differ from the required target",
        "incorrect_common_target_certificate": "rejected",
        "point_mass_control": "certificate impossible; Gaussian laws are translates",
        "injective_target_control": {
            "distinct_source_sites": 9, "distinct_target_sites": 9,
            "distinct_weights": 9, "pair_contraction_checks": 36,
            "weight_squared_norm": str(dot(weights, weights)),
            "nontrivial_permutation_mixture_variance": str(variance),
            "nonliftability": "cited teammate proof, not reverified by this checker"
        },
        "external_code_dependencies": []
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = (json.dumps(audit(), indent=2, sort_keys=True) + "\n").encode()
    if args.check:
        expected = Path(__file__).with_name("EXPECTED.json").read_bytes()
        require(output == expected, "EXPECTED.json mismatch")
        print("PASS " + sha256(output).hexdigest())
    else:
        print(output.decode(), end="")


if __name__ == "__main__":
    main()
