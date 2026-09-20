#!/usr/bin/env python3
"""Independent exact checks for the graph-polytope odd-girth review.

This file deliberately imports no code from the reviewed package.  It counts
lattice points by recursive assignments, interpolates the two residue
polynomials over Q, enumerates shortest odd cycles, and obtains each face
volume from an independently counted even-dilate Ehrhart polynomial.
"""

from fractions import Fraction
from itertools import combinations, permutations
from math import comb, factorial
import hashlib
import json
from pathlib import Path


def normalized_edges(d, edges):
    answer = set()
    for u, v in edges:
        assert 0 <= u < d and 0 <= v < d and u != v
        answer.add((min(u, v), max(u, v)))
    return tuple(sorted(answer))


def components(d, edges):
    adjacency = [set() for _ in range(d)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    unseen = set(range(d))
    answer = []
    while unseen:
        root = min(unseen)
        stack = [root]
        unseen.remove(root)
        component = []
        while stack:
            u = stack.pop()
            component.append(u)
            for v in adjacency[u]:
                if v in unseen:
                    unseen.remove(v)
                    stack.append(v)
        answer.append(tuple(sorted(component)))
    return answer


def count_component(vertices, edges, rhs, caps):
    """Count assignments with 0<=x_v<=caps[v], x_u+x_v<=rhs."""
    vertex_set = set(vertices)
    local_edges = [edge for edge in edges if set(edge) <= vertex_set]
    degree = {v: 0 for v in vertices}
    for u, v in local_edges:
        degree[u] += 1
        degree[v] += 1
    # A fixed high-degree-first ordering makes the recursion small but does
    # not use the subset-transform algorithm in the reviewed checker.
    order = tuple(sorted(vertices, key=lambda v: (-degree[v], v)))
    earlier = []
    position = {v: i for i, v in enumerate(order)}
    adjacency = {v: set() for v in vertices}
    for u, v in local_edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    for i, v in enumerate(order):
        earlier.append(tuple(u for u in adjacency[v] if position[u] < i))

    assigned = {}

    def visit(i):
        if i == len(order):
            return 1
        v = order[i]
        upper = caps[v]
        for u in earlier[i]:
            upper = min(upper, rhs - assigned[u])
        total = 0
        for value in range(upper + 1):
            assigned[v] = value
            total += visit(i + 1)
        del assigned[v]
        return total

    return visit(0)


def count_polytope(d, edges, rhs, caps=None):
    edges = normalized_edges(d, edges)
    if caps is None:
        caps = tuple(rhs for _ in range(d))
    assert len(caps) == d and all(0 <= cap <= rhs for cap in caps)
    total = 1
    for component in components(d, edges):
        total *= count_component(component, edges, rhs, caps)
    return total


def add(p, q):
    out = [Fraction(0) for _ in range(max(len(p), len(q)))]
    for i, value in enumerate(p):
        out[i] += value
    for i, value in enumerate(q):
        out[i] += value
    return trim(out)


def scale(p, scalar):
    return trim([scalar * value for value in p])


def multiply(p, q):
    out = [Fraction(0) for _ in range(len(p) + len(q) - 1)]
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return trim(out)


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def interpolate(xs, ys):
    assert len(xs) == len(ys) and len(set(xs)) == len(xs)
    answer = [Fraction(0)]
    for i, (x_i, y_i) in enumerate(zip(xs, ys)):
        basis = [Fraction(1)]
        denominator = Fraction(1)
        for j, x_j in enumerate(xs):
            if i == j:
                continue
            basis = multiply(basis, [Fraction(-x_j), Fraction(1)])
            denominator *= x_i - x_j
        answer = add(answer, scale(basis, Fraction(y_i, 1) / denominator))
    return trim(answer)


def evaluate(p, x):
    answer = Fraction(0)
    for coefficient in reversed(p):
        answer = answer * x + coefficient
    return answer


def shortest_odd_cycles(d, edges):
    edges = set(normalized_edges(d, edges))

    def adjacent(u, v):
        return (min(u, v), max(u, v)) in edges

    for length in range(3, d + 1, 2):
        found = set()
        for subset in combinations(range(d), length):
            first = subset[0]
            for tail in permutations(subset[1:]):
                cycle = (first,) + tail
                if cycle[1] > cycle[-1]:
                    continue
                if all(adjacent(cycle[i], cycle[(i + 1) % length])
                       for i in range(length)):
                    found.add(cycle)
        if found:
            return length, tuple(sorted(found))
    return None, ()


def face_count(d, edges, cycle, dilation):
    """Count lattice points in dilation*F_C; dilation must be even."""
    assert dilation % 2 == 0
    cycle_set = set(cycle)
    outside = [v for v in range(d) if v not in cycle_set]
    index = {v: i for i, v in enumerate(outside)}
    outside_edges = []
    touches_cycle = [False] * len(outside)
    for u, v in normalized_edges(d, edges):
        if u in cycle_set and v not in cycle_set:
            touches_cycle[index[v]] = True
        elif v in cycle_set and u not in cycle_set:
            touches_cycle[index[u]] = True
        elif u not in cycle_set and v not in cycle_set:
            outside_edges.append((index[u], index[v]))
    caps = tuple(dilation // 2 if touches_cycle[i] else dilation
                 for i in range(len(outside)))
    return count_polytope(len(outside), outside_edges, dilation, caps)


def face_volume(d, edges, cycle):
    dimension = d - len(cycle)
    if dimension == 0:
        return Fraction(1)
    ms = list(range(dimension + 1))
    counts = [face_count(d, edges, cycle, 2 * m) for m in ms]
    polynomial_in_m = interpolate(ms, counts)
    # One independent holdout guards against an interpolation/index error.
    holdout_m = dimension + 1
    assert evaluate(polynomial_in_m, holdout_m) == face_count(
        d, edges, cycle, 2 * holdout_m
    )
    return polynomial_in_m[-1] / (2 ** dimension)


def numerator_coefficients(d, residue_polynomials):
    even, odd = residue_polynomials

    def lattice_count(n):
        if n < 0:
            return Fraction(0)
        return evaluate(even if n % 2 == 0 else odd, n)

    coefficients = []
    for j in range(2 * d + 2):
        value = Fraction(0)
        for r in range(min(d + 1, j // 2) + 1):
            value += (-1) ** r * comb(d + 1, r) * lattice_count(j - 2 * r)
        coefficients.append(value)
    # The next four recurrence values must vanish if the interpolation really
    # gives a period-two quasipolynomial of degree at most d.
    for j in range(2 * d + 2, 2 * d + 6):
        value = sum(
            Fraction((-1) ** r * comb(d + 1, r)) * lattice_count(j - 2 * r)
            for r in range(d + 2)
        )
        assert value == 0
    return trim(coefficients)


def root_multiplicity_and_residual_at_minus_one(polynomial):
    p = trim(polynomial)
    multiplicity = 0
    while evaluate(p, -1) == 0:
        assert len(p) > 1
        q = [Fraction(0) for _ in range(len(p) - 1)]
        q[-1] = p[-1]
        for i in range(len(p) - 2, 0, -1):
            q[i - 1] = p[i] - q[i]
        assert p[0] == q[0]
        p = trim(q)
        multiplicity += 1
    return multiplicity, evaluate(p, -1)


def fraction_text(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def review_fixture(name, d, raw_edges):
    edges = normalized_edges(d, raw_edges)
    girth, cycles = shortest_odd_cycles(d, edges)
    assert girth is not None

    even_xs = [2 * m for m in range(d + 1)]
    odd_xs = [2 * m + 1 for m in range(d + 1)]
    even_values = [count_polytope(d, edges, n) for n in even_xs]
    odd_values = [count_polytope(d, edges, n) for n in odd_xs]
    even_polynomial = interpolate(even_xs, even_values)
    odd_polynomial = interpolate(odd_xs, odd_values)

    # Definition-level holdouts not used for interpolation.
    even_holdout = 2 * d + 2
    odd_holdout = 2 * d + 3
    assert evaluate(even_polynomial, even_holdout) == count_polytope(
        d, edges, even_holdout
    )
    assert evaluate(odd_polynomial, odd_holdout) == count_polytope(
        d, edges, odd_holdout
    )

    parity_polynomial = scale(add(even_polynomial, scale(odd_polynomial, -1)),
                              Fraction(1, 2))
    volumes = [face_volume(d, edges, cycle) for cycle in cycles]
    volume_sum = sum(volumes, Fraction(0))
    expected_degree = d - girth
    expected_leading = Fraction(1, 2 ** (girth + 1)) * volume_sum
    assert len(parity_polynomial) - 1 == expected_degree
    assert parity_polynomial[-1] == expected_leading

    numerator = numerator_coefficients(d, (even_polynomial, odd_polynomial))
    root_order, residual = root_multiplicity_and_residual_at_minus_one(numerator)
    expected_residual = (2 ** expected_degree) * factorial(expected_degree) * volume_sum
    assert root_order == girth
    assert residual == expected_residual

    return {
        "name": name,
        "vertices": d,
        "edges": len(edges),
        "odd_girth": girth,
        "shortest_odd_cycles": len(cycles),
        "face_volumes": [fraction_text(x) for x in volumes],
        "degree_B": len(parity_polynomial) - 1,
        "leading_B": fraction_text(parity_polynomial[-1]),
        "H_root_order_at_minus_one": root_order,
        "H_residual_at_minus_one": fraction_text(residual),
        "definition_level_holdouts": 2,
    }


def cycle_edges(vertices):
    return [(vertices[i], vertices[(i + 1) % len(vertices)])
            for i in range(len(vertices))]


TRIANGLE = [(0, 1), (1, 2), (2, 0)]
FIXTURES = [
    ("triangle", 3, TRIANGLE),
    ("five_cycle", 5, cycle_edges(tuple(range(5)))),
    ("triangle_with_two_edge_tail", 5, TRIANGLE + [(2, 3), (3, 4)]),
    ("bow_tie_triangles", 5,
     TRIANGLE + [(2, 3), (3, 4), (4, 2)]),
    ("two_disjoint_triangles", 6,
     TRIANGLE + [(3, 4), (4, 5), (5, 3)]),
    ("two_bridged_triangles", 6,
     TRIANGLE + [(3, 4), (4, 5), (5, 3), (2, 3)]),
    ("triangle_plus_three_isolates", 6, TRIANGLE),
    ("triangle_disjoint_five_cycle", 8,
     TRIANGLE + cycle_edges((3, 4, 5, 6, 7))),
]


def main():
    records = [review_fixture(*fixture) for fixture in FIXTURES]
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    output = {
        "implementation": "independent recursive definition-level counter",
        "imports_reviewed_code": False,
        "fixtures": records,
        "record_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "status": "PASS",
    }
    expected = json.loads(Path(__file__).with_name("expected.json").read_text())
    if output != expected:
        raise SystemExit("computed record differs from expected.json")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
