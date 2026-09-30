#!/usr/bin/env python3
"""Exact controls for the analytic neighborhood-capacity proof.

No solver or floating point; no enumeration of arbitrary 22-vertex graphs.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


def choose2(k):
    return k * (k - 1) // 2


def complement(g):
    vertices = set(range(len(g)))
    return [vertices - row - {i} for i, row in enumerate(g)]


def capacity_direct(g, r, s):
    blue = complement(g)
    return sum(
        r - 1 - len(g[i] & g[j]) if j in g[i]
        else s - len(blue[i] & blue[j])
        for i, j in combinations(range(len(g)), 2)
    )


def capacity_formula(g, r, s):
    d = len(g)
    numerator = sum((3 * d + r - s - 4) * len(row) - 3 * len(row) ** 2
                    for row in g) + 2 * (s - d + 2) * choose2(d)
    assert numerator % 2 == 0
    return numerator // 2


def subset_cost_direct(g, red_set):
    z = set(range(len(g))) - red_set
    return sum(j in g[i] for i, j in combinations(red_set, 2)) + sum(
        j not in g[i] for i, j in combinations(z, 2))


def subset_cost_formula(g, red_set):
    z = set(range(len(g))) - red_set
    return sum(map(len, g)) // 2 - sum(len(g[i]) for i in z) + choose2(len(z))


def exhaustive_small_controls():
    graphs = subsets = 0
    stream = sha256()
    for d in range(6):
        edges = list(combinations(range(d), 2))
        for mask in range(1 << len(edges)):
            g = [set() for _ in range(d)]
            for bit, (i, j) in enumerate(edges):
                if mask >> bit & 1:
                    g[i].add(j)
                    g[j].add(i)
            for r, s in ((3, 6), (6, 3), (2, 1)):
                direct = capacity_direct(g, r, s)
                assert direct == capacity_formula(g, r, s)
                stream.update(f"{d},{mask},{r},{s},{direct};".encode())
            for bits in range(1 << d):
                red_set = {i for i in range(d) if bits >> i & 1}
                direct = subset_cost_direct(g, red_set)
                assert direct == subset_cost_formula(g, red_set)
                stream.update(f"{d},{mask},{bits},{direct};".encode())
                subsets += 1
            graphs += 1
    return {"graphs": graphs, "subsets": subsets, "sha256": stream.hexdigest()}


def scalar_bound(n, r, s, d):
    q = n - 1 - d
    coefficient = 3 * d + r - s - 4 - q
    scores = [coefficient * h - 3 * h * h for h in range(r + 1)]
    twice_bound = d * max(scores) + 2 * (s - d + 2) * choose2(d) + q * r * (r + 1)
    # Independent evaluation through the capacities of a uniform degree list.
    capacities_twice = [d * ((3 * d + r - s - 4) * h - 3 * h * h)
                        + 2 * (s - d + 2) * choose2(d) for h in range(r + 1)]
    direct_bounds = [c - q * (d * h - r * (r + 1))
                     for h, c in enumerate(capacities_twice)]
    assert max(direct_bounds) == twice_bound
    return {"neighborhood_degree": d, "twice_budget_upper": twice_bound,
            "maximizing_local_degrees": [h for h, score in enumerate(scores) if score == max(scores)]}


def scalar_histograms():
    initial = []
    for n0, n1, n2 in product(range(12), repeat=3):
        n3 = 11 - n0 - n1 - n2
        if n3 < 0:
            continue
        degrees = [0] * n0 + [1] * n1 + [2] * n2 + [3] * n3
        if sum(degrees) % 2:
            continue
        twice_budget = 21 - 21 * n0 - 8 * n1 - n2
        degrees.sort(reverse=True)
        best_row = min(6 + choose2(z) - sum(degrees[:z]) for z in range(12))
        # Independently minimize by choosing counts from each degree class.
        best_row2 = min(6 + choose2(k0 + k1 + k2 + k3) - k1 - 2 * k2 - 3 * k3
                        for k0 in range(n0 + 1) for k1 in range(n1 + 1)
                        for k2 in range(n2 + 1) for k3 in range(n3 + 1))
        assert best_row == best_row2
        if twice_budget >= 20 * best_row:
            assert twice_budget % 2 == 0
            initial.append({"counts_0_1_2_3": [n0, n1, n2, n3],
                            "budget": twice_budget // 2, "minimum_row_cost": best_row})
    assert len(initial) == 12
    final = [row for row in initial if row["counts_0_1_2_3"][0] == 0
             and row["counts_0_1_2_3"][1] <= 1]
    expected_counts = [[0, n1, n2, 11 - n1 - n2] for n1 in (0, 1) for n2 in (1, 3, 5, 7)]
    assert [row["counts_0_1_2_3"] for row in final] == expected_counts
    return {"scalar_survivors": initial, "after_analytic_exclusions": final}


def induced(g, vertices):
    return [{j for j, v in enumerate(vertices) if v in g[u]} for u in vertices]


def baseline_controls(path):
    rows = path.read_text().splitlines()
    n = len(rows)
    assert n == 21 and all(len(row) == n and set(row) <= {"0", "1"} for row in rows)
    red = [{j for j, bit in enumerate(row) if bit == "1"} for row in rows]
    assert all(i not in red[i] for i in range(n))
    assert all((j in red[i]) == (i in red[j]) for i, j in combinations(range(n), 2))
    output = []
    for g, r, s, label in ((red, 3, 6, "red"), (complement(red), 6, 3, "blue")):
        other = complement(g)
        assert all(len(g[i] & g[j]) <= r for i, j in combinations(range(n), 2) if j in g[i])
        assert all(len(other[i] & other[j]) <= s for i, j in combinations(range(n), 2) if j in other[i])
        for v in range(n):
            a = sorted(g[v])
            b = sorted(other[v])
            jgraph = induced(g, a)
            c = capacity_direct(jgraph, r, s)
            assert c == capacity_formula(jgraph, r, s)
            costs = [subset_cost_direct(jgraph, {i for i, u in enumerate(a) if u in g[w]})
                     for w in b]
            unused = sum(r - len(g[i] & g[j]) if j in g[i]
                         else s - len(other[i] & other[j]) for i, j in combinations(a, 2))
            assert c - sum(costs) == unused >= 0
            delta = [choose2(r + 1) + choose2(sum(u not in g[w] for u in a))
                     - sum(len(jgraph[i]) for i, u in enumerate(a) if u not in g[w]) for w in b]
            assert all(value >= 0 for value in delta)
            d = len(a)
            budget_twice = sum((3 * d + r - s - 4 - len(b)) * len(row) - 3 * len(row) ** 2
                               for row in jgraph) + 2 * (s - d + 2) * choose2(d) + len(b) * r * (r + 1)
            assert budget_twice == 2 * (unused + sum(delta))
            output.append({"color": label, "root": v, "degree": d,
                           "unused": unused, "row_cost_total": sum(delta), "budget": budget_twice // 2})
    assert sum(map(len, red)) // 2 == 93
    assert Counter(map(len, red)) == {8: 4, 9: 16, 10: 1}
    return output


def gram_control():
    # KG(5,2), used solely to control the isolated-case exact matrix algebra.
    vertices = list(combinations(range(5), 2))
    p = [{j for j, other in enumerate(vertices) if set(pair).isdisjoint(other)} for pair in vertices]
    assert all(len(row) == 3 for row in p)
    assert all(len(p[i] & p[j]) == (0 if j in p[i] else 1)
               for i, j in combinations(range(10), 2))
    # Two copies of each of the five four-element stars.
    m = [[int(point in pair) for pair in vertices] for point in range(5) for _ in range(2)]
    assert all(sum(row) == 4 for row in m)
    assert all(sum(row[i] for row in m) == 4 for i in range(10))
    for i in range(10):
        for j in range(10):
            gram = sum(row[i] * row[j] for row in m)
            formula = 4 * (i == j) + 3 - 3 * (j in p[i]) - len(p[i] & p[j])
            assert gram == formula
    independent = [set(c) for c in combinations(range(10), 4)
                   if all(j not in p[i] for i, j in combinations(c, 2))]
    assert len(independent) == 5
    assert all(s & t for s, t in combinations(independent, 2))
    assert all(sum(u in p[w] for u in s) == 2 for s in independent for w in set(range(10)) - s)
    return {"independent_four_sets": [sorted(s) for s in independent],
            "gram_entries_checked": 100, "interpretation": "arithmetic control, not a cubic-graph classification"}


def main():
    directory = Path(__file__).resolve().parent
    upper = [scalar_bound(22, 3, 6, d) for d in range(12, 22)]
    lower = [scalar_bound(22, 6, 3, d) for d in range(15, 22)]
    assert all(row["twice_budget_upper"] < 0 for row in upper + lower)
    equality = scalar_bound(22, 6, 3, 14)
    assert equality["twice_budget_upper"] == 0 and equality["maximizing_local_degrees"] == [6]
    result = {"agent": "six-books-1", "role": "researcher",
              "status": "analytic necessary conditions; Ramsey gap 22..23 remains unresolved",
              "degree_range22": [7, 11], "edge_range22": [97, 121],
              "small_controls": exhaustive_small_controls(),
              "upper_degree_scalar_bounds": upper, "lower_degree_scalar_bounds": lower,
              "degree7_equality": equality, "degree11_histograms": scalar_histograms(),
              "baseline21_root_controls": baseline_controls(directory / "baseline21.rows"),
              "isolated_case_gram_control": gram_control()}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
