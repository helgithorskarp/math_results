#!/usr/bin/env python3
"""Independent exact checker for the common-target majorisation theorem.

The implementation imports none of the reviewed source.  It uses a different
depth-first spanning tree to construct the signed flow certificate, checks all
vertices of the zero-sum L1 ball, and audits the finite geometry directly.
Universal analytic steps are reviewed separately in README.md.
"""

import argparse
import hashlib
import json
from fractions import Fraction as Q
from itertools import combinations, permutations, product
from pathlib import Path


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def minus(x, y):
    return tuple(a - b for a, b in zip(x, y))


def norm2(x):
    return dot(x, x)


def original_map(v):
    zero = v.index(0)
    nonzero = [j for j in range(3) if j != zero]
    return tuple(v[nonzero[0]] * v[nonzero[1]] if j == zero else 0
                 for j in range(3))


def component_map(v, coordinate):
    j = (coordinate + 1) % 3
    k = (coordinate + 2) % 3
    if v[coordinate]:
        return tuple(v[coordinate] if ell == coordinate else 0
                     for ell in range(3))
    out = [Q(0), Q(0), Q(0)]
    out[j] = Q(v[j] + v[k], 2)
    out[k] = Q(v[k] - v[j], 2)
    return tuple(out)


def push(weights, mapping, targets):
    result = {y: Q(0) for y in targets}
    for weight, image in zip(weights, mapping):
        result[image] += weight
    return result


def build_depth_first_tree(directions, component_maps):
    # Edge (i,v) is directed from source vertex ("s",v) to target
    # vertex ("t",i,R_i(v)).  Descending traversal order deliberately
    # differs from the submitted breadth-first construction.
    graph = {}
    for v in range(len(directions)):
        graph[("s", v)] = []
    for i in range(3):
        for y in sorted(set(component_maps[i])):
            graph[("t", i, y)] = []
    for i in range(3):
        for v, y in enumerate(component_maps[i]):
            edge = (i, v)
            source, target = ("s", v), ("t", i, y)
            graph[source].append((target, edge))
            graph[target].append((source, edge))

    root = ("s", len(directions) - 1)
    parent = {root: None}
    parent_edge = {}
    order = []
    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node)
        neighbors = sorted(graph[node], key=repr)
        for neighbor, edge in neighbors:
            if neighbor not in parent:
                parent[neighbor] = node
                parent_edge[neighbor] = edge
                stack.append(neighbor)
    require(len(parent) == 30 and len(parent_edge) == 29,
            "incidence graph is not connected")
    return root, parent, parent_edge, order


def correction(delta, directions, targets, original, component_maps, tree):
    require(sum(delta) == 0, "perturbation is not zero-sum")
    root, parent, parent_edge, order = tree
    delta_target = push(delta, original, targets)
    divergence = {("s", v): delta[v] for v in range(12)}
    for i in range(3):
        for y in targets:
            divergence[("t", i, y)] = -delta_target[y] / 3
    require(sum(divergence.values()) == 0, "total divergence is nonzero")

    subtree = dict(divergence)
    flow = {(i, v): Q(0) for i in range(3) for v in range(12)}
    for child in reversed(order[1:]):
        edge = parent_edge[child]
        # The fixed orientation is source -> target.
        flow[edge] = subtree[child] if child[0] == "s" else -subtree[child]
        subtree[parent[child]] += subtree[child]
    require(subtree[root] == 0, "tree correction leaves root divergence")

    source_divergence = [sum(flow[(i, v)] for i in range(3))
                         for v in range(12)]
    require(source_divergence == delta, "source correction mismatch")
    for i in range(3):
        pushed = push([flow[(i, v)] for v in range(12)],
                      component_maps[i], targets)
        require(pushed == {y: delta_target[y] / 3 for y in targets},
                "target correction mismatch")
    total_variation = sum(abs(x) for x in delta)
    require(max(abs(x) for x in flow.values()) <= total_variation,
            "tree-flow bound failed")
    return flow


def audit():
    anchors = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    directions = sorted(set(permutations((0, 1, 1))) |
                        set(permutations((0, 1, -1))) |
                        set(permutations((0, -1, -1))))
    # The set construction above includes exactly the 12 signed two-coordinate
    # directions, without depending on the reviewed ordering.
    require(len(directions) == 12, "wrong source direction count")
    targets = sorted({tuple(sign if j == i else 0 for j in range(3))
                      for i in range(3) for sign in (-1, 1)})
    original = [original_map(v) for v in directions]
    component_maps = [[component_map(v, i) for v in directions]
                      for i in range(3)]

    # Geometry of S,R_1,R_2,R_3.  The inner-product maximum proves all
    # unequal-radius ray comparisons through the identity in the proof.
    pair_checks = 0
    core_checks = 0
    maximum_defect = {}
    for name, mapping in [("S", original)] + [
            (f"R{i + 1}", component_maps[i]) for i in range(3)]:
        defects = []
        require(set(mapping) == set(targets), f"{name} is not onto")
        for index, (v, image) in enumerate(zip(directions, mapping)):
            require(norm2(v) == 2 and norm2(image) == 1, "norm mismatch")
            if name.startswith("R"):
                coordinate = int(name[1:]) - 1
                require(v[coordinate] == image[coordinate],
                        "component does not preserve its coordinate")
            for w, image_w in zip(directions, mapping):
                defect = dot(v, w) - dot(image, image_w)
                require(defect <= 1, "ray contraction fails")
                defects.append(defect)
                pair_checks += 1
            for u in anchors:
                require(dot(u, minus(v, image)) <= 1,
                        "core-ray contraction fails at an extreme point")
                core_checks += 1
        maximum_defect[name] = max(defects)

    # Uniform common target and source reconstruction.
    uniform = [Q(1, 12)] * 12
    q_uniform = push(uniform, original, targets)
    require(q_uniform == {y: Q(1, 6) for y in targets}, "uniform target")
    components = []
    for i in range(3):
        weights = [Q(1, 6) if v[i] == 0 else Q(1, 24)
                   for v in directions]
        require(sum(weights) == 1, "component normalization")
        require(push(weights, component_maps[i], targets) == q_uniform,
                "component lacks common target")
        components.append(weights)
    require([sum(row[v] for row in components) / 3 for v in range(12)] == uniform,
            "uniform source reconstruction")

    # A different DFS spanning tree gives a second explicit linear splitting.
    tree = build_depth_first_tree(directions, component_maps)
    base = [[Q(1, 18) if v[i] == 0 else Q(1, 72)
             for v in directions] for i in range(3)]
    rho = Q(1, 72)
    minimum_mass = Q(1)
    boundary_records = []
    for positive, negative in product(range(12), repeat=2):
        if positive == negative:
            continue
        delta = [Q(0)] * 12
        delta[positive] = rho / 2
        delta[negative] = -rho / 2
        require(sum(abs(x) for x in delta) == rho, "L1 vertex radius")
        flow = correction(delta, directions, targets, original,
                          component_maps, tree)
        z = [[base[i][v] + flow[(i, v)] for v in range(12)]
             for i in range(3)]
        minimum_mass = min(minimum_mass, *(x for row in z for x in row))
        require(minimum_mass >= 0, "negative split at an L1-ball vertex")
        p = [uniform[v] + delta[v] for v in range(12)]
        require([sum(z[i][v] for i in range(3)) for v in range(12)] == p,
                "perturbed source reconstruction")
        q = push(p, original, targets)
        for i in range(3):
            require(push(z[i], component_maps[i], targets) ==
                    {y: q[y] / 3 for y in targets},
                    "perturbed common target")
        boundary_records.append([
            positive, negative,
            [str(flow[(i, v)]) for i in range(3) for v in range(12)]
        ])
    require(len(boundary_records) == 132, "incomplete L1 boundary audit")

    # The second-moment obstruction: direct matrix average and the spectrum
    # of every summand in its natural orthogonal basis {v,S(v),third axis}.
    average = [[Q(0) for _ in range(3)] for _ in range(3)]
    summand_spectra = set()
    for v, image in zip(directions, original):
        matrix = [[v[i] * v[j] - image[i] * image[j]
                   for j in range(3)] for i in range(3)]
        for i, j in product(range(3), repeat=2):
            average[i][j] += Q(matrix[i][j], 12)
        require(dot(v, image) == 0, "loss basis is not orthogonal")
        summand_spectra.add((norm2(v), -norm2(image), 0))
    require(average == [[Q(int(i == j), 3) for j in range(3)]
                        for i in range(3)], "uniform moment loss")
    require(summand_spectra == {(2, -1, 0)}, "summand spectrum")

    # Concrete check of the equal-cardinality premise used by Theorem B.
    # The strict convexity identity itself is analytic and recorded in README.
    weights = [Q(2 ** j, 511) for j in range(9)]
    require(sum(weights) == 1 and len(set(weights)) == 9,
            "binary weights are not distinct probabilities")
    nonidentity = weights[1:] + weights[:1]
    midpoint = [(a + b) / 2 for a, b in zip(weights, nonidentity)]
    strict_loss = (sum(a * a for a in weights) -
                   sum(a * a for a in midpoint))
    require(strict_loss > 0, "strict convexity control")

    encoded_boundary = json.dumps(boundary_records, separators=(",", ":"))
    return {
        "status": "INDEPENDENT_COMMON_TARGET_AUDIT_PASSED",
        "scope": "exact finite geometry and a distinct DFS flow certificate",
        "source_directions": len(directions),
        "target_directions": len(targets),
        "ordered_ray_pair_checks": pair_checks,
        "core_extreme_point_checks": core_checks,
        "maximum_inner_product_defect": {
            name: str(value) for name, value in maximum_defect.items()
        },
        "uniform_component_masses": [str(sum(row)) for row in components],
        "incidence_tree_edges": len(tree[2]),
        "l1_radius": str(rho),
        "l1_ball_vertex_checks": len(boundary_records),
        "minimum_split_mass": str(minimum_mass),
        "dfs_boundary_certificate_sha256": hashlib.sha256(
            encoded_boundary.encode()).hexdigest(),
        "uniform_second_moment_loss": [[str(x) for x in row] for row in average],
        "summand_spectrum": [2, 0, -1],
        "injective_target_distinct_weight_control": str(strict_loss),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    encoded = json.dumps(audit(), indent=2, sort_keys=True) + "\n"
    if args.check:
        expected = Path(__file__).with_name("EXPECTED.json").read_text()
        require(encoded == expected, "EXPECTED.json mismatch")
        print("PASS " + hashlib.sha256(encoded.encode()).hexdigest())
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
