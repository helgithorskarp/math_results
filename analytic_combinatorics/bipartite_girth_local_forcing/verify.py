#!/usr/bin/env python3
"""Exact normalization audits; the infinite theorem is proved in PROOF.md.

Python 3.11+, standard library. No assertions or floating point are used.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, lcm
from pathlib import Path
import argparse
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def normalize(edges):
    edges = tuple(sorted(tuple(sorted(e)) for e in edges))
    require(all(a != b for a, b in edges), "loop")
    require(len(set(edges)) == len(edges), "duplicate edge")
    vertices = sorted({v for e in edges for v in e})
    labels = {v: i for i, v in enumerate(vertices)}
    return tuple((labels[a], labels[b]) for a, b in edges)


def parameters(edges):
    edges = normalize(edges)
    n = 1 + max(v for e in edges for v in e)
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    colors = {}
    for root in range(n):
        if root in colors:
            continue
        colors[root] = 0
        queue = [root]
        for v in queue:
            for w in adj[v]:
                if w not in colors:
                    colors[w] = 1 - colors[v]
                    queue.append(w)
                require(colors[w] != colors[v], "not bipartite")
    cycles = Counter()
    for root in range(n):
        def visit(path):
            for nxt in adj[path[-1]]:
                if nxt == root:
                    if len(path) >= 3 and path[1] < path[-1]:
                        cycles[len(path)] += 1
                elif nxt > root and nxt not in path:
                    visit(path + [nxt])
        visit([root])
    require(bool(cycles), "acyclic graph")
    g = min(cycles)
    return n, len(edges), g, cycles[g], sum(comb(len(a), 2) for a in adj)


def check_kernel(matrix, weights):
    k = len(weights)
    require(k > 0 and all(w > 0 for w in weights) and sum(weights) == 1,
            "invalid atom weights")
    require(len(matrix) == k and all(len(row) == k for row in matrix),
            "matrix dimensions")
    require(all(matrix[i][j] == matrix[j][i] for i in range(k) for j in range(k)),
            "kernel is not symmetric")


def density(edges, matrix, weights):
    """Definition-level vertex-assignment sum, scaled to integer arithmetic."""
    check_kernel(matrix, weights)
    edges = normalize(edges)
    if not edges:
        return Q(1)
    n = 1 + max(v for e in edges for v in e)
    k = len(weights)
    den = lcm(*(x.denominator for row in matrix for x in row))
    mass_den = lcm(*(w.denominator for w in weights))
    entries = [[int(x * den) for x in row] for row in matrix]
    masses = [int(w * mass_den) for w in weights]
    total = 0
    for assignment in product(range(k), repeat=n):
        term = 1
        for i in assignment:
            term *= masses[i]
        for a, b in edges:
            term *= entries[assignment[a]][assignment[b]]
            if term == 0:
                break
        total += term
    return Q(total, den ** len(edges) * mass_den ** n)


def matmul(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def cycle_moment(matrix, weights, length):
    """Operator trace; independent of vertex-assignment enumeration."""
    check_kernel(matrix, weights)
    k = len(weights)
    operator = [[matrix[i][j] * weights[j] for j in range(k)] for i in range(k)]
    power = [[Q(i == j) for j in range(k)] for i in range(k)]
    for _ in range(length):
        power = matmul(power, operator)
    return sum(power[i][i] for i in range(k))


def cut_norm(matrix, weights):
    """Exact: optimize the second set after enumerating the first set."""
    k = len(weights)
    answer = Q(0)
    for mask in range(1 << k):
        columns = [weights[j] * sum(weights[i] * matrix[i][j]
                    for i in range(k) if mask >> i & 1) for j in range(k)]
        answer = max(answer, sum(x for x in columns if x > 0),
                     -sum(x for x in columns if x < 0))
    return answer


def center(matrix, weights):
    degrees = [sum(x * w for x, w in zip(row, weights)) for row in matrix]
    mean = sum(x * w for x, w in zip(degrees, weights))
    a = [x - mean for x in degrees]
    u = [[matrix[i][j] - mean - a[i] - a[j] for j in range(len(weights))]
         for i in range(len(weights))]
    require(all(sum(x * w for x, w in zip(row, weights)) == 0 for row in u),
            "centering failed")
    return mean, a, u


def polynomial_density(edges, p, u, b, weights, g):
    """Direct assignments for p + eps*u + eps**(g/2)*(b_i+b_j), through degree g."""
    edges = normalize(edges)
    n = 1 + max(v for e in edges for v in e)
    k = len(weights)
    d = [[b[i] + b[j] for j in range(k)] for i in range(k)]
    den = lcm(p.denominator, *(x.denominator for row in u for x in row),
              *(x.denominator for row in d for x in row))
    mass_den = lcm(*(w.denominator for w in weights))
    masses = [int(w * mass_den) for w in weights]
    terms = [[((0, int(p * den)), (1, int(u[i][j] * den)),
               (g // 2, int(d[i][j] * den))) for j in range(k)] for i in range(k)]
    total = [0] * (g + 1)
    for assignment in product(range(k), repeat=n):
        coeff = [1] + [0] * g
        for i, j in edges:
            nxt = [0] * (g + 1)
            for shift, value in terms[assignment[i]][assignment[j]]:
                if value:
                    for z in range(g + 1 - shift):
                        nxt[z + shift] += coeff[z] * value
            coeff = nxt
        mass = 1
        for i in assignment:
            mass *= masses[i]
        for z in range(g + 1):
            total[z] += mass * coeff[z]
    denom = den ** len(edges) * mass_den ** n
    return [Q(x, denom) for x in total]


def cycle(n, offset=0):
    return [(offset + i, offset + (i + 1) % n) for i in range(n)]


def theta(lengths):
    edges, nxt = [], 2
    for length in lengths:
        path = [0] + list(range(nxt, nxt + length - 1)) + [1]
        nxt += length - 1
        edges.extend(zip(path, path[1:]))
    return edges


def fixtures():
    cube = [(i, i ^ (1 << b)) for i in range(8) for b in range(3) if i < (i ^ (1 << b))]
    subk4 = []
    for v, (a, b) in enumerate(combinations(range(4), 2), 4):
        subk4.extend([(a, v), (v, b)])
    return [
        ("C4", cycle(4), 4, 1), ("C6", cycle(6), 6, 1),
        ("C8", cycle(8), 8, 1), ("C10", cycle(10), 10, 1),
        ("K23", theta([2, 2, 2]), 4, 3),
        ("K33", [(i, j) for i in range(3) for j in range(3, 6)], 4, 9),
        ("theta333", theta([3, 3, 3]), 6, 3),
        ("theta244", theta([2, 4, 4]), 6, 2),
        ("C6_leaf", cycle(6) + [(0, 6)], 6, 1),
        ("C6_edge", cycle(6) + [(6, 7)], 6, 1),
        ("two_C6_bridge", cycle(6) + cycle(6, 6) + [(0, 6)], 6, 2),
        ("cube", cube, 4, 6), ("subdivision_K4", subk4, 6, 4),
    ]


def run():
    records = []
    counts = Counter()
    raw_kernels = [
        ([[Q(-1), Q(1)], [Q(1), Q(-1)]], [Q(1, 2)] * 2),
        ([[Q(1), Q(-1, 2)], [Q(-1, 2), Q(1, 3)]], [Q(1, 3), Q(2, 3)]),
        ([[Q(-1), Q(0), Q(1, 2)], [Q(0), Q(1), Q(-1, 3)],
          [Q(1, 2), Q(-1, 3), Q(0)]], [Q(1, 4), Q(1, 4), Q(1, 2)]),
        ([[Q(-1), Q(-1)], [Q(-1), Q(-1)]], [Q(1, 2)] * 2),
    ]
    # Complete edge-subset audit on a labelled 3-by-3 bipartite host.
    host = [(i, j) for i in range(3) for j in range(3, 6)]
    for mask in range(1, 1 << len(host)):
        edges = [edge for i, edge in enumerate(host) if mask >> i & 1]
        degrees = Counter(v for e in edges for v in e)
        if min(degrees.values()) < 2:
            continue
        n, m, g, c, wedges = parameters(edges)
        counts["leafless_graphs"] += 1
        for index, (u, weights) in enumerate(raw_kernels):
            h = max(abs(x) for row in u for x in row)
            z = cycle_moment(u, weights, g)
            value = density(edges, u, weights)
            require(abs(value) <= h ** (m - g) * z, "signed-density domination")
            records.append(["domination", mask, index, str(value), str(z)])
            counts["signed_density_checks"] += 1
    regular_data = []
    for raw, weights in raw_kernels[:3]:
        _, b, u = center(raw, weights)
        regular_data.append((u, b, weights))
        for g in [4, 6, 8, 10]:
            z = cycle_moment(u, weights, g)
            require(z == density(cycle(g), u, weights), "cycle normalization")
            require((4 * cut_norm(u, weights)) ** g <= z, "centered cut inequality")
            counts["trace_and_cut_checks"] += 1
    for name, edges, expected_g, expected_c in fixtures():
        n, m, g, c, wedges = parameters(edges)
        require((g, c) == (expected_g, expected_c), "fixture cycle count: " + name)
        require(wedges > 0, "missing wedges")
        records.append(["graph", name, n, m, g, c, wedges])
        counts["named_graphs"] += 1
        for index, (u, b, weights) in enumerate(regular_data):
            if n > 8 and len(weights) > 2:
                continue
            p = Q(2, 5)
            z = cycle_moment(u, weights, g)
            for degree_scale in [0, 1]:
                bb = [degree_scale * t for t in b]
                coeff = polynomial_density(edges, p, u, bb, weights, g)
                expected = wedges * p ** (m - 2) * sum(w * t * t for w, t in zip(weights, bb))
                expected += c * p ** (m - g) * z
                require(coeff[0] == p ** m, "constant coefficient")
                require(all(x == 0 for x in coeff[1:g]), "unexpected lower-order term")
                require(coeff[g] == expected, "two-scale leading coefficient")
                records.append(["polynomial", name, index, degree_scale, str(coeff[g])])
                counts["two_scale_polynomials"] += 1
            # The finite-radius estimate is checked at two rational radii.
            for radius in [Q(1, 100), Q(1, 1000)]:
                w = [[p + radius * (u[i][j] + b[i] + b[j])
                      for j in range(len(weights))] for i in range(len(weights))]
                mean, a, regular = center(w, weights)
                require(mean == p and all(0 <= x <= 1 for row in w for x in row),
                        "invalid graphon fixture")
                v = sum(t * t * mass for t, mass in zip(a, weights))
                zg = cycle_moment(regular, weights, g)
                h = max(*(abs(t) for t in a), *(abs(t) for row in regular for t in row))
                x = h / p
                require(x <= 1, "radius hypothesis")
                delta = density(edges, w, weights) - p ** m
                xx, yy = p ** (m - 2) * v, p ** (m - g) * zg
                mixed = m * 2 ** (m - 1) * x ** (g // 2)
                ev, eg = 6 ** m * x + mixed, 2 ** m * x * x + mixed
                require(abs(delta - wedges * xx - c * yy) <= ev * xx + eg * yy,
                        "two-component remainder")
                records.append(["remainder", name, index, str(radius), str(delta)])
                counts["finite_radius_checks"] += 1
    # Exact rank-one sharpness polynomial: surviving subsets are Eulerian.
    for name, edges, g, c in fixtures():
        counts_by_size = Counter()
        for mask in range(1 << len(edges)):
            degree = Counter(v for i, edge in enumerate(edges) if mask >> i & 1 for v in edge)
            if all(d % 2 == 0 for d in degree.values()):
                counts_by_size[mask.bit_count()] += 1
        require(counts_by_size[0] == 1 and counts_by_size[g] == c, "Eulerian leading term")
        require(all(k == 0 or (k >= g and k % 2 == 0) for k in counts_by_size),
                "Eulerian support")
        direct = polynomial_density(edges, Q(2, 5), [[Q(1), Q(-1)], [Q(-1), Q(1)]],
                                    [Q(0), Q(0)], [Q(1, 2), Q(1, 2)], g)
        require(direct[g] == c * Q(2, 5) ** (len(edges) - g), "rank-one direct comparison")
        records.append(["rank_one", name, sorted(counts_by_size.items())])
        counts["rank_one_checks"] += 1
    # Malformed hypotheses must be rejected.
    bad = [lambda: normalize([(0, 0)]), lambda: normalize([(0, 1), (1, 0)]),
           lambda: parameters(cycle(3)), lambda: parameters([(0, 1), (1, 2)]),
           lambda: check_kernel([[Q(0), Q(1)], [Q(0), Q(0)]], [Q(1, 2)] * 2),
           lambda: check_kernel([[Q(0)]], [Q(2)])]
    for task in bad:
        try:
            task()
        except ValueError:
            counts["rejected_invalid_inputs"] += 1
        else:
            raise ValueError("invalid input was accepted")
    encoded = json.dumps(records, separators=(",", ":"), sort_keys=True).encode()
    return {"status": "PASS", "scope": "exact finite audits; analytic proof is external to computation",
            "counts": dict(sorted(counts.items())), "record_sha256": hashlib.sha256(encoded).hexdigest()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="print regenerated compact evidence without comparison")
    args = parser.parse_args()
    result = run()
    if not args.emit:
        saved = json.loads(Path(__file__).with_name("expected.json").read_text())
        require(result == saved, "saved evidence does not match")
    print(json.dumps(result, indent=2, sort_keys=True))
