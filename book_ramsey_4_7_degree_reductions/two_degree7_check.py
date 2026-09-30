#!/usr/bin/env python3
"""Exact auxiliary coverage and arithmetic controls for the two-root theorem.

Standard library only. No enumeration of arbitrary 22-vertex graphs.
Every rejected cubic-eight graph has a directly checked integer negative
quadratic vector. The analytic bridges are written in two_degree7.md.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import gcd, lcm


def recursive_cubic(n):
    assert n in (6, 8)
    pairs = list(combinations(range(n), 2))
    position = {pair: i for i, pair in enumerate(pairs)}
    g = [set() for _ in range(n)]
    for j in (1, 2, 3):
        g[0].add(j)
        g[j].add(0)

    def visit(i):
        if i == n:
            if all(len(row) == 3 for row in g):
                yield sum(1 << position[(a, b)] for a, b in pairs if b in g[a])
            return
        need = 3 - len(g[i])
        future = [j for j in range(i + 1, n) if len(g[j]) < 3]
        if need < 0 or len(future) < need:
            return
        for chosen in combinations(future, need):
            for j in chosen:
                g[i].add(j)
                g[j].add(i)
            yield from visit(i + 1)
            for j in chosen:
                g[i].remove(j)
                g[j].remove(i)

    return sorted(visit(1))


def combination_cubic(n):
    assert n in (6, 8)
    pairs = list(combinations(range(n), 2))
    position = {pair: i for i, pair in enumerate(pairs)}
    remaining = list(combinations(range(1, n), 2))
    targets = [2 if i in (1, 2, 3) else 3 for i in range(1, n)]
    fixed = sum(1 << position[(0, j)] for j in (1, 2, 3))
    output = []
    for chosen in combinations(range(len(remaining)), 3 * n // 2 - 3):
        degrees = [0] * (n - 1)
        for index in chosen:
            a, b = remaining[index]
            degrees[a - 1] += 1
            degrees[b - 1] += 1
        if degrees == targets:
            output.append(fixed + sum(1 << position[remaining[index]] for index in chosen))
    return sorted(output)


def graph(n, mask):
    g = [set() for _ in range(n)]
    for bit, (a, b) in enumerate(combinations(range(n), 2)):
        if mask >> bit & 1:
            g[a].add(b)
            g[b].add(a)
    assert all(len(row) == 3 for row in g) and g[0] == {1, 2, 3}
    return g


def primitive(vector):
    scale = lcm(*(x.denominator for x in vector))
    integers = [int(x * scale) for x in vector]
    assert any(integers)
    divisor = gcd(*integers)
    integers = [x // divisor for x in integers]
    if next(x for x in integers if x) < 0:
        integers = [-x for x in integers]
    return integers


def generate_negative_vector(g):
    n = len(g)
    a = [[Fraction(2 * (i == j) + (j in g[i])) for j in range(n)] for i in range(n)]
    basis = [[Fraction(i == j) for i in range(n)] for j in range(n)]
    for k in range(n):
        if a[k][k] < 0:
            return primitive(basis[k])
        if a[k][k] == 0:
            others = [j for j in range(k + 1, n) if a[k][j]]
            if others:
                j = others[0]
                multiplier = -(a[j][j] + 1) / (2 * a[k][j])
                return primitive([multiplier * x + y for x, y in zip(basis[k], basis[j])])
            continue
        coefficients = [a[k][j] / a[k][k] for j in range(n)]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] -= coefficients[i] * coefficients[j] * a[k][k]
        for i in range(k + 1, n):
            basis[i] = [x - coefficients[i] * y for x, y in zip(basis[i], basis[k])]
    return None


def check_negative_vector(g, mask, vector):
    n = len(g)
    if len(vector) != n or not all(isinstance(x, int) for x in vector):
        raise ValueError("Expected an integer vector of the correct dimension")
    direct = 2 * sum(x * x for x in vector) + sum(
        vector[i] * vector[j] for i in range(n) for j in g[i])
    # Independent use of the edge mask, without the adjacency-set encoding.
    other = 2 * sum(x * x for x in vector) + 2 * sum(
        vector[i] * vector[j] for bit, (i, j) in enumerate(combinations(range(n), 2))
        if mask >> bit & 1)
    assert direct == other
    if direct >= 0:
        raise ValueError("The vector does not prove a negative quadratic value")
    return direct


def cubic_eight_classification():
    masks = recursive_cubic(8)
    alternative = combination_cubic(8)
    assert masks == alternative and len(masks) == len(set(masks)) == 553
    stream = sha256()
    retained = []
    for mask in masks:
        g = graph(8, mask)
        vector = generate_negative_vector(g)
        if vector is None:
            retained.append(mask)
        else:
            check_negative_vector(g, mask, vector)
        stream.update((str(mask) + ':' + str(vector) + ';').encode())
    assert retained == [264249735]
    g = graph(8, retained[0])
    assert all((j in g[i]) == (i // 4 == j // 4) for i, j in combinations(range(8), 2))
    # Its adjacency plus 2I is the block diagonal of E_4+I_4.
    try:
        check_negative_vector(g, retained[0], [1] + [0] * 7)
    except ValueError:
        malformed_rejected = True
    else:
        raise AssertionError("Nonnegative certificate unexpectedly accepted")
    assert masks[:-1] != alternative
    return {"normalized_graphs": 553, "explicit_negative_vectors": 552,
            "retained_mask": retained[0], "retained_graph": "K4 disjoint-union K4",
            "certificate_stream_sha256": stream.hexdigest(),
            "nonnegative_vector_control_rejected": malformed_rejected,
            "omitted_graph_control_rejected": True}


def determinant(matrix):
    # Bareiss fraction-free elimination, with row swaps.
    a = [row[:] for row in matrix]
    n = len(a)
    sign = 1
    previous = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot = next((i for i in range(k + 1, n) if a[i][k]), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[k][k] * a[i][j] - a[i][k] * a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator // previous
        previous = a[k][k]
    return sign * a[-1][-1] if n else 1


def cubic_six_positive_subspaces():
    masks = recursive_cubic(6)
    assert masks == combination_cubic(6) and len(masks) == 7
    counts = Counter()
    stream = sha256()
    for mask in masks:
        g = graph(6, mask)
        blue = [set(range(6)) - g[i] - {i} for i in range(6)]
        unseen = set(range(6))
        parts = []
        while unseen:
            stack = [min(unseen)]
            component = set()
            while stack:
                i = stack.pop()
                if i in component:
                    continue
                component.add(i)
                stack.extend(blue[i] - component)
            unseen -= component
            parts.append(sorted(component))
        parts.sort(key=len)
        assert sorted(map(len, parts)) in ([3, 3], [6])
        if len(parts) == 2:
            basis = []
            for part in parts:
                for i, j in zip(part, part[1:]):
                    v = [0] * 6
                    v[i], v[j] = 1, -1
                    basis.append(v)
            basis.append([1] * 6)
            kind = "K3,3"
        else:
            cycle = [0, min(blue[0])]
            while len(cycle) < 6:
                cycle.append(next(j for j in sorted(blue[cycle[-1]]) if j != cycle[-2]))
            assert cycle[0] in blue[cycle[-1]] and len(set(cycle)) == 6
            a, b = cycle[::2], cycle[1::2]
            basis = []
            for i in a:
                paired = sorted(g[i] & set(b))
                assert len(paired) == 1
                v = [0] * 6
                v[i] = v[paired[0]] = 1
                basis.append(v)
            basis.append([1 if i in a else -1 for i in range(6)])
            kind = "triangular prism"
        restriction = [[sum(x[i] * y[j] * ((i == j) + (j in g[i]))
                             for i in range(6) for j in range(6))
                        for y in basis] for x in basis]
        minors = [determinant([row[:k] for row in restriction[:k]])
                  for k in range(1, len(basis) + 1)]
        assert all(value > 0 for value in minors) and len(basis) >= 4
        counts[kind] += 1
        stream.update(f"{mask}:{kind}:{minors};".encode())
    return {"normalized_graphs": 7, "type_counts": dict(sorted(counts.items())),
            "minimum_positive_subspace_dimension": 4, "stream_sha256": stream.hexdigest()}


def minimum_squares(rows, maximum, total):
    best = {0: 0}
    for _ in range(rows):
        following = {}
        for s, cost in best.items():
            for value in range(maximum + 1):
                target = s + value
                following[target] = min(following.get(target, 10 ** 9), cost + value * value)
        best = following
    return best[total]


def two_root_scalar_controls():
    # Blue pair: the six common-blue vertices form a blue matching.
    assert minimum_squares(14, 6, 36) == 96
    blue_pair = {"outside_rows": 14, "total_red_incidences": 36,
                 "required_square_sum": 72, "minimum_square_sum": 96}
    red_pair = []
    for threes in range(9):
        degrees = [3] * threes + [1] * (8 - threes)
        s = sum(degrees)
        t = sum(h * h for h in degrees)
        moment = t + 12 * s - 168
        assert moment - 8 * (2 * s) + 16 * 12 == 0
        minimum = minimum_squares(12, 8, 2 * s)
        red_pair.append({"local_degree_three_count": threes, "degree_sum": s,
                         "required_square_sum": moment, "minimum_square_sum": minimum,
                         "possible": moment >= minimum})
    assert [r["local_degree_three_count"] for r in red_pair if r["possible"]] == [8]
    return {"blue_pair": blue_pair, "red_pair": red_pair}


def centered_incidence_control():
    pairs = list(combinations(range(4), 2))
    rows = [[int(i in pair) for i in range(4)] + [int(i in pair) for i in range(4)]
            for pair in pairs]
    rows += [[int(i in pair) for i in range(4)] + [int(i not in pair) for i in range(4)]
             for pair in pairs]
    assert len(rows) == 12 and all(sum(row) == 4 for row in rows)
    assert all(sum(row[i] for row in rows) == 6 for i in range(8))
    y = [[2 * x - 1 for x in row] for row in rows]
    gram = [[sum(row[i] * row[j] for row in y) for j in range(8)] for i in range(8)]
    for i in range(8):
        for j in range(8):
            assert gram[i][j] == (16 * (i == j) - 4 if i // 4 == j // 4 else 0)
    retained = [0, 1, 2, 4, 5, 6]
    minor = determinant([[gram[i][j] for j in retained] for i in retained])
    assert minor == 1048576
    assert all(sum(row[:4]) == sum(row[4:]) == 0 for row in y)
    return {"rank": 6, "integer_centered_gram_entries_checked": 64,
            "positive_six_by_six_minor": minor,
            "interpretation": "exact incidence-algebra control, not a valid22-vertex graph"}


def degree7_incidence_control():
    # The known KG(7,2) baseline, split into the edges/nonedges of C7.
    edges = list(combinations(range(7), 2))
    cycle = {tuple(sorted((i, (i + 1) % 7))) for i in range(7)}
    a = [edge for edge in edges if edge not in cycle]
    b = [edge for edge in edges if edge in cycle]
    p = [{j for j, other in enumerate(a) if i != j and set(edge) & set(other)}
         for i, edge in enumerate(a)]
    m = [[int(set(edge).isdisjoint(other)) for other in b] for edge in a]
    k = list(map(sum, m))
    assert len(a) == 14 and len(b) == 7
    assert k == [3] * 14 and all(len(row) == 6 for row in p)
    assert [sum(row[j] for row in m) for j in range(7)] == [6] * 7
    for i in range(14):
        for j in range(14):
            direct = sum(m[i][c] * m[j][c] for c in range(7))
            formula = 3 + (k[i] + 3) * (i == j) - len(p[i] & p[j]) + (k[i] + k[j] - 5) * (j in p[i])
            assert direct == formula
        assert k[i] + sum(k[j] for j in p[i]) == 21
    red = [{j for j, other in enumerate(edges) if set(edge).isdisjoint(other)} for edge in edges]
    blue = [set(range(21)) - row - {i} for i, row in enumerate(red)]
    red_codes = [len(red[i] & red[j]) for i, j in combinations(range(21), 2) if j in red[i]]
    blue_codes = [len(blue[i] & blue[j]) for i, j in combinations(range(21), 2) if j in blue[i]]
    assert all(len(row) == 10 for row in red)
    assert set(red_codes) == {3} and set(blue_codes) == {5}
    return {"known_baseline": "KG(7,2)", "vertices": 21, "red_edges": 105,
            "red_degrees": 10, "red_codegrees": 3, "blue_codegrees": 5,
            "gram_entries_checked": 196, "row_sum_equations_checked": 14,
            "interpretation": "known21-vertex baseline and algebra control; no22-vertex witness is asserted"}


def conditional_edge_control():
    points = [(t, e) for t in range(8) for e in range(11) if 2 * e + t >= 7]
    totals = [98 + t + e for t, e in points]
    assert len(points) == 72 and min(totals) == 102 and max(totals) == 115
    return {"scalar_points": len(points), "edge_range": [min(totals), max(totals)]}


def main():
    result = {"agent": "six-books-1", "role": "researcher",
              "claim": "Any hypothetical22-vertex witness has at most one degree-seven vertex",
              "status": "exact cubic-eight auxiliary classification with unformalized analytic bridges; Ramsey gap unresolved",
              "degree7_if_present_edge_range": [102, 115],
              "cubic8": cubic_eight_classification(),
              "cubic6": cubic_six_positive_subspaces(),
              "two_root_moments": two_root_scalar_controls(),
              "centered_incidence": centered_incidence_control(),
              "degree7_incidence": degree7_incidence_control(),
              "conditional_edges": conditional_edge_control()}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
