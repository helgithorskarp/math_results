#!/usr/bin/env python3
"""Exact finite corroboration of PROOF.md; CPython 3.11+, standard library.

The geometric model uses (x_1,...,x_n,z). The independent graph calculation
uses hubs 0,1, leaves 2,...,n+1 and centered generator segments.
All checks remain active under -O. No solver, floats, randomness or data.
"""
import argparse
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def signs(n):
    return product((-1, 1), repeat=n)


def sign_product(eta):
    return (-1) ** sum(x == -1 for x in eta)


def directions(n):
    require(n >= 1, "n must be positive")
    return [eta + ((n - 1) * sign_product(eta),) for eta in signs(n)] + [
        (0,) * n + (1,), (0,) * n + (-1,)]


def vertices(n):
    result = set()
    for x in product((-1, 0, 1), repeat=n):
        height = n - sum(abs(a) for a in x)
        for delta in (-1, 1):
            result.add(x + (delta * height,))
    return result


def inequalities(n):
    rows = []
    for i in range(n):
        for s in (-1, 1):
            row = [0] * (n + 1)
            row[i] = s
            rows.append((tuple(row), 1))
    rows.extend((row, n) for row in signs(n + 1))
    return rows


def choose_direction(point):
    n = len(point) - 1
    x, z = point[:-1], point[-1]
    if not any(x):
        return (0,) * n + (-1 if z > 0 else 1,)
    eta = [-v if v else 1 for v in x]
    if z:
        wanted = -1 if z > 0 else 1
        if sign_product(eta) != wanted:
            eta[x.index(0)] *= -1
    return tuple(eta) + ((n - 1) * sign_product(eta),)


def to_graph(h):
    x, z = h[:-1], h[-1]
    return (z - sum(x), -z - sum(x)) + tuple(2 * v for v in x)


def to_model(y):
    return tuple(Fraction(v, 2) for v in y[2:]) + (Fraction(y[0] - y[1], 2),)


def is_acyclic(vertex_count, arcs):
    # Definition-level topological sorting, independent of the three leaf types.
    remaining = set(range(vertex_count))
    while remaining:
        sources = {v for v in remaining
                   if not any(t == v and s in remaining for s, t in arcs)}
        if not sources:
            return False
        remaining -= sources
    return True


def graph_vertex(n, edge_signs, weights):
    require(len(weights) == 2 * n and all(w > 0 for w in weights),
            "every edge must have positive weight")
    edges = [(hub, i + 2) for hub in (0, 1) for i in range(n)]
    y = [0] * (n + 2)
    for (hub, leaf), s, w in zip(edges, edge_signs, weights):
        y[hub] += s * w
        y[leaf] -= s * w
    return tuple(y)


def active_cuts(n, y, weights):
    """Direct support function on ALL proper nonempty coordinate cuts."""
    edges = [(hub, i + 2) for hub in (0, 1) for i in range(n)]
    active = set()
    for mask in range(1, (1 << (n + 2)) - 1):
        cut = tuple((mask >> i) & 1 for i in range(n + 2))
        support = sum(w * abs(cut[a] - cut[b]) for (a, b), w in zip(edges, weights))
        value = dot(cut, y)
        require(value <= support, "generator sum violates support bound")
        if value == support:
            active.add(mask)
    return active


def is_antipodal_point(point):
    return all(point[:-1]) or not any(point[:-1])


def audit_model(n):
    points, rows, ds = vertices(n), inequalities(n), directions(n)
    require(len(points) == 2 * 3 ** n - 2 ** n, "wrong model vertex count")
    require(len(set(ds)) == 2 ** n + 2 and all(any(d) for d in ds), "bad directions")
    active_count = 0
    normal_sets = {}
    for p in sorted(points):
        d = choose_direction(p)
        require(d in ds, "decoder left the stated direction set")
        require(all(dot(f, p) <= b for f, b in rows), "infeasible model vertex")
        active = {f for f, b in rows if dot(f, p) == b}
        require(active and all(dot(f, d) < 0 for f in active), "model cover failed")
        active_count += len(active)
        normal_sets[p] = active
    anti = sorted(p for p in points if is_antipodal_point(p))
    require(len(anti) == 2 ** n + 2, "wrong antipodal certificate size")
    # The pole normal need not be a facet normal, so include all three explicit
    # normal types from the proof and check support maxima on the actual vertices.
    for p, q in combinations(anti, 2):
        if all(p[:-1]) and all(q[:-1]):
            i = next(i for i in range(n) if p[i] != q[i])
            f = tuple(p[i] if j == i else 0 for j in range(n + 1))
        elif not any(p[:-1]) and not any(q[:-1]):
            f = (0,) * n + (1,)
        else:
            corner, pole = (p, q) if all(p[:-1]) else (q, p)
            f = tuple(-v for v in corner[:-1]) + (1 if pole[-1] > 0 else -1,)
        values = [dot(f, v) for v in points]
        require({dot(f, p), dot(f, q)} == {min(values), max(values)}
                and min(values) < max(values), "invalid antipodal support pair")
    return {"vertices": len(points), "directions": len(ds),
            "active_inequalities_checked": active_count,
            "antipodal_pairs": len(anti) * (len(anti) - 1) // 2}


def audit_graph(n):
    edges = [(hub, i + 2) for hub in (0, 1) for i in range(n)]
    configurations = [tuple(Fraction(1) for _ in edges),
                      tuple(Fraction(j + 1, 2 * j + 3) for j in range(2 * n)),
                      tuple(Fraction((j + 2) ** 2, j + 1) for j in range(2 * n))]
    orientation_count = support_checks = anti_checks = 0
    model_points = set()
    anti_sets = [dict() for _ in configurations]
    for ss in signs(2 * n):
        arcs = [(leaf, hub) if s == 1 else (hub, leaf)
                for (hub, leaf), s in zip(edges, ss)]
        if not is_acyclic(n + 2, arcs):
            continue
        orientation_count += 1
        base = graph_vertex(n, ss, configurations[0])
        model = to_model(base)
        require(model not in model_points, "two acyclic orientations share a vertex")
        model_points.add(model)
        d = to_graph(choose_direction(model))
        require(sum(d) == 0, "graph direction not in the sum-zero space")
        first_active = None
        for j, weights in enumerate(configurations):
            y = graph_vertex(n, ss, weights)
            active = active_cuts(n, y, weights)
            require(active, "no proper active supporting cut")
            if first_active is None:
                first_active = active
            require(active == first_active, "positive weights changed normal cuts")
            for mask in active:
                value = sum(d[i] for i in range(n + 2) if (mask >> i) & 1)
                require(value < 0, "weighted graphical cover failed")
                support_checks += 1
            if is_antipodal_point(model):
                anti_sets[j][ss] = active
    require(model_points == vertices(n), "graph/model vertex correspondence failed")
    complement = (1 << (n + 2)) - 1
    for data in anti_sets:
        require(len(data) == 2 ** n + 2, "weighted lower certificate incomplete")
        for a, b in combinations(data, 2):
            require(any((mask ^ complement) in data[b] for mask in data[a]),
                    "weighted antipodal cut pair missing")
            anti_checks += 1
    return {"orientations_tested": 4 ** n, "acyclic_orientations": orientation_count,
            "positive_weight_assignments": len(configurations),
            "strict_active_cut_checks": support_checks,
            "weighted_antipodal_pairs": anti_checks}


def run():
    model = {n: audit_model(n) for n in range(1, 7)}
    graphs = {n: audit_graph(n) for n in range(1, 6)}
    # A direction tangent to a supporting hyperplane does not illuminate.
    corner = (1, 1, 1, 0)
    tangent = (-1, -1, -1, 3)
    require(any(dot(f, corner) == b and dot(f, tangent) == 0
                for f, b in inequalities(3)), "missing tangency control")
    require(not all(dot(f, tangent) < 0 for f, b in inequalities(3)
                    if dot(f, corner) == b), "tangent direction accepted")
    # Delete the parity alternation: an upper nonpolar vertex is missed.
    bad = [eta + (2,) for eta in signs(3)] + [(0, 0, 0, 1), (0, 0, 0, -1)]
    witness = (1, 0, 0, 2)
    rows = inequalities(3)
    require(not any(all(dot(f, d) < 0 for f, b in rows if dot(f, witness) == b)
                    for d in bad), "constant-parity negative control failed")
    for weights in [(0, 1), (-1, 1)]:
        try:
            graph_vertex(1, (1, 1), weights)
        except ValueError:
            pass
        else:
            raise ValueError("nonpositive edge weight accepted")
    try:
        directions(0)
    except ValueError:
        pass
    else:
        raise ValueError("n=0 accepted")
    return {"status": "VERIFIED", "model_checks": model, "weighted_graph_checks": graphs,
            "negative_controls": ["tangent ray rejected", "constant parity misses vertex",
                                  "zero weight rejected", "negative weight rejected", "n=0 rejected"],
            "trust_boundary": "finite corroboration; the all-n theorem is the written proof"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="omit comparison to expected.json")
    result = run()
    encoded = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if not parser.parse_args().emit:
        expected = json.loads(Path(__file__).with_name('expected.json').read_text())
        require(json.loads(encoded) == expected, "expected output mismatch")
    print(encoded, end='')


if __name__ == '__main__':
    main()
