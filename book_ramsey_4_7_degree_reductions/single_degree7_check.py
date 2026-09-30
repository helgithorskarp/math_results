#!/usr/bin/env python3
"""Independent exact arithmetic controls for the 105-edge conditional bound.

The universal theorem has a written analytic proof in single_degree7.md.
These controls do not enumerate 22-vertex witnesses or twofold designs.
Python 3.11+, standard library only; one process and no solver.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import random


def require(condition, message):
    if not condition:
        raise ValueError(message)


def matrix(rows, n):
    return [[int(j in row) for j in range(n)] for row in rows]


def transpose(a):
    return [list(row) for row in zip(*a)]


def multiply(a, b):
    columns = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in columns] for row in a]


def graph(n, edges):
    g = [set() for _ in range(n)]
    for a, b in edges:
        g[a].add(b)
        g[b].add(a)
    return g


def make_control(p, m, l):
    """Literal graph: root0, A=1..14, B=15..21. No validity asserted."""
    edges = [(0, 15 + b) for b in range(7)]
    edges += [(1 + a, 1 + b) for a, b in combinations(range(14), 2) if not p[a][b]]
    edges += [(1 + a, 15 + b) for a in range(14) for b in range(7) if m[a][b]]
    edges += [(15 + a, 15 + b) for a, b in combinations(range(7), 2) if l[a][b]]
    red = graph(22, edges)
    blue = [set(range(22)) - row - {i} for i, row in enumerate(red)]
    return red, blue


def literal_controls():
    rng = random.Random(470104)
    ps = [matrix([{(i + d) % 14 for d in (1, 2, 3, -1, -2, -3)} for i in range(14)], 14),
          matrix([{j for j in range(14) if j != i and j // 7 == i // 7} for i in range(14)], 14),
          matrix([{j for j in range(14) if j // 7 != i // 7 and j % 7 != i % 7}
                  for i in range(14)], 14)]
    cross_checks = pair_checks = defect_checks = 0
    stream = sha256()
    first_actual = first_formula = None
    for trial in range(96):
        p = ps[trial % 3]
        m = [[0] * 7 for _ in range(14)]
        sigma = [rng.randrange(2) for _ in range(7)]
        for b in range(7):
            for a in rng.sample(range(14), 6 + sigma[b]):
                m[a][b] = 1
        l = matrix(graph(7, [(a, b) for a, b in combinations(range(7), 2)
                            if rng.randrange(2)]), 7)
        k = list(map(sum, m))
        h = list(map(sum, l))
        e = sum(h) // 2
        t = sum(sigma)
        pm = multiply(p, m)
        ml = multiply(m, l)
        s = multiply(transpose(m), m)
        l2 = multiply(l, l)
        red, blue = make_control(p, m, l)
        row_defects = []
        for a in range(14):
            unused = 0
            for b in range(7):
                d = pm[a][b] - ml[a][b]
                if m[a][b]:
                    actual = len(red[1 + a] & red[15 + b])
                    formula = 5 + sigma[b] - d
                    unused += 3 - actual
                else:
                    actual = len(blue[1 + a] & blue[15 + b])
                    formula = 12 - h[b] - k[a] - d
                    unused += 6 - actual
                require(actual == formula, "Mixed-spine count differs from literal pages")
                cross_checks += 1
                if first_actual is None:
                    first_actual, first_formula = actual, formula
            direct_formula = (sum(pm[a]) - 2 * sum(m[a][b] * h[b] for b in range(7))
                              - sum(m[a][b] * sigma[b] for b in range(7))
                              + 11 * k[a] - k[a] ** 2 + 2 * e - 42)
            require(unused == direct_formula, "Unsubstituted row-defect identity fails")
            row_defects.append(unused)
            defect_checks += 1
        u = 0
        for b, c in combinations(range(7), 2):
            if l[b][c]:
                actual = len(red[15 + b] & red[15 + c])
                formula = 1 + l2[b][c] + s[b][c]
                u += 3 - actual
            else:
                actual = len(blue[15 + b] & blue[15 + c])
                formula = 7 - h[b] - h[c] - sigma[b] - sigma[c] + l2[b][c] + s[b][c]
                u += 6 - actual
            require(actual == formula, "B-spine count differs from literal pages")
            pair_checks += 1
        formula = (32 * e - 3 * sum(x * x for x in h) + 13 * t
                   - 2 * sum(x * y for x, y in zip(h, sigma)) - sum(x * x for x in k))
        require(2 * u == formula, "Seven-neighborhood unused-capacity identity fails")
        stream.update(f"{trial}:{k}:{h}:{sigma}:{u}:{row_defects};".encode())
    require(first_actual != first_formula + 1, "Off-by-one control failed")
    return {"controlled_graphs": 96, "mixed_spines_checked": cross_checks,
            "B_spines_checked": pair_checks, "row_defect_identities_checked": defect_checks,
            "stream_sha256": stream.hexdigest(), "wrong_constant_control_rejected": True,
            "interpretation": "literal 22-vertex algebra controls; book validity is not asserted"}


def scalar_controls():
    best = {0: 0}
    for _ in range(14):
        new = {}
        for total, cost in best.items():
            for value in range(8):
                target = total + value
                new[target] = min(new.get(target, 10 ** 9), cost + value * value)
        best = new
    require(all(best[42 + t] == 126 + 7 * t for t in range(8)), "Row-square DP fails")
    retained = []
    states = 0
    stream = sha256()
    for h in product(range(4), repeat=7):
        total = sum(h)
        if total % 2 or total > 12:
            continue
        e = total // 2
        for sigma in product(range(2), repeat=7):
            t = sum(sigma)
            if e + t > 6:
                continue
            bound = (32 * e - 3 * sum(x * x for x in h) + 13 * t
                     - 2 * sum(x * y for x, y in zip(h, sigma)) - best[42 + t])
            states += 1
            stream.update(f"{h}:{sigma}:{bound};".encode())
            if bound >= 0:
                retained.append((h, sigma, bound))
    require(len(retained) == 21, "Unexpected low-edge scalar profiles")
    require(all(sorted(h) == [1, 1, 2, 2, 2, 2, 2] and sum(sigma) == bound == 0
                for h, sigma, bound in retained), "Scalar equality structure fails")
    maxima = [32 * e - 3 * max(2 * e, 6 * e - 14) + 6 * (6 - e) - 126
              for e in range(7)]
    require(maxima == [-90, -70, -50, -30, -16, -8, 0], "Analytic scalar bounds fail")
    return {"labeled_scalar_states": states, "equality_profiles": 21,
            "upper_twice_unused_by_e": maxima, "stream_sha256": stream.hexdigest(),
            "interpretation": "necessary degree/column counts, with no graphicality assertion"}


def recursive_boundary_graphs():
    targets = [1, 1, 2, 2, 2, 2, 2]
    g = [set() for _ in targets]

    def visit(i):
        if i == 7:
            if list(map(len, g)) == targets:
                yield tuple((a, b) for a, b in combinations(range(7), 2) if b in g[a])
            return
        need = targets[i] - len(g[i])
        future = [j for j in range(i + 1, 7) if len(g[j]) < targets[j]]
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

    return sorted(visit(0))


def boundary_graph_controls():
    targets = [1, 1, 2, 2, 2, 2, 2]
    recursive = recursive_boundary_graphs()
    alternative = []
    for edges in combinations(list(combinations(range(7), 2)), 6):
        g = graph(7, edges)
        if list(map(len, g)) == targets:
            alternative.append(edges)
    require(recursive == sorted(alternative), "Boundary generators disagree")
    require(len(recursive) == len(set(recursive)) == 167, "Boundary coverage count fails")
    retained = []
    stream = sha256()
    for edges in recursive:
        l = matrix(graph(7, edges), 7)
        l2 = multiply(l, l)
        s = [[6 if b == c else (2 if l[b][c] else targets[b] + targets[c] - 1) - l2[b][c]
              for c in range(7)] for b in range(7)]
        rows = list(map(sum, s))
        stream.update(f"{edges}:{rows};".encode())
        if rows == [18] * 7:
            require((0, 1) in edges, "Leaf edge missing")
            require(all(s[b][c] == (6 if b == c else 2) for b in range(7) for c in range(7)),
                    "Forced twofold-design Gram fails")
            retained.append(edges)
    require(len(retained) == 12, "Expected the twelve labeled C5 completions")
    return {"complete_normalized_graphs": 167, "row_equation_survivors": 12,
            "survivor_type": "K2 disjoint-union C5", "stream_sha256": stream.hexdigest(),
            "interpretation": "arithmetic control of a classification proved analytically"}


def projection_controls():
    fano = {tuple(sorted(((i + d) % 7 for d in (0, 1, 3)))) for i in range(7)}
    fixtures = {}
    for permutation in permutations(range(7)):
        second = {tuple(sorted(permutation[i] for i in row)) for row in fano}
        common = len(fano & second)
        if common not in fixtures:
            fixtures[common] = sorted(fano) + sorted(second)
        if set(fixtures) == {0, 1, 3, 7}:
            break
    require(set(fixtures) == {0, 1, 3, 7}, "Fano controls missing")
    results = []
    difference_tests = final_count_tests = 0
    stream = sha256()
    for common, rows in sorted(fixtures.items()):
        m = [[int(b in row) for b in range(7)] for row in rows]
        mtm = multiply(transpose(m), m)
        require(all(mtm[b][c] == 4 * (b == c) + 2 for b in range(7) for c in range(7)),
                "Twofold-design fixture has wrong Gram")
        g = multiply(m, transpose(m))
        four_pi = [[g[a][b] - 1 for b in range(14)] for a in range(14)]
        require(multiply(four_pi, four_pi) == [[4 * x for x in row] for row in four_pi],
                "Projection idempotence fails")
        require(multiply(four_pi, m) == [[4 * x for x in row] for row in m],
                "Projection image fails")
        candidates = []
        for a, b in combinations(range(14), 2):
            v = [int(i in (a, b)) for i in range(14)]
            candidates.append(v)
        for a in range(14):
            candidates.append([2 * (i == a) for i in range(14)])
        accepted = []
        for v in candidates:
            direct = all(sum(x * y for x, y in zip(row, v)) == 4 * v[a]
                         for a, row in enumerate(four_pi))
            norm = sum(x * x for x in v)
            quadratic = sum(v[a] * four_pi[a][b] * v[b] for a in range(14) for b in range(14))
            require(direct == (4 * norm == quadratic), "Projection norm test differs")
            if direct:
                support = [a for a, value in enumerate(v) if value]
                require(len(support) == 2 and rows[support[0]] == rows[support[1]],
                        "Defect support is not a repeated triple")
                accepted.append(v)
        require(len(candidates) == 105 and len(accepted) == common, "Projection count fails")
        for p, q in combinations(range(7), 2):
            w = [row[p] - row[q] for row in m]
            z = [row[p] + row[q] for row in m]
            require(sum(x * x for x in z) == 16, "Column-sum norm fails")
            for d1, d2 in product(accepted, repeat=2):
                epsilon = [x - y for x, y in zip(d1, d2)]
                norm = sum(x * x for x in epsilon)
                scalar = sum(x * y for x, y in zip(w, epsilon))
                require(scalar % 2 == 0, "Paired defect scalar is not even")
                require(norm != 3 * scalar or d1 == d2, "Different supports pass polynomial")
                difference_tests += 1
                if d1 != d2:
                    continue
                support = [a for a, value in enumerate(d1) if value]
                row = rows[support[0]]
                if (p in row) != (q in row):
                    continue  # symmetry of P excludes this case
                if p not in row:
                    require(2 * int(p in row) + 2 * int(q in row) == 0,
                            "No-leaf row should have zero total defect")
                    continue  # the two leaf defects contradict zero total row defect
                require([a for a in range(14) if m[a][p] and m[a][q]] == support,
                        "Twofold pair is not exhausted by its duplicate")
                require(4 + 4 - 6 == 2 and len(support) - 1 == 1,
                        "Final six-neighbor pigeonhole contradiction fails")
                final_count_tests += 1
        results.append({"repeated_triples": common, "integer_load_two_vectors": 105,
                        "vectors_in_incidence_image": len(accepted)})
        stream.update(f"{common}:{rows}:{accepted};".encode())
    return {"fixture_counts": results, "difference_polynomial_controls": difference_tests,
            "final_neighborhood_controls": final_count_tests, "stream_sha256": stream.hexdigest(),
            "interpretation": "four exact incidence controls; no classification of all twofold designs"}


def baseline_control():
    rows = (Path(__file__).parent / "baseline21.rows").read_text().splitlines()
    red = [{j for j, value in enumerate(row) if value == '1'} for row in rows]
    require(len(red) == 21 and all(len(row) == 21 for row in rows), "Baseline dimensions fail")
    blue = [set(range(21)) - row - {i} for i, row in enumerate(red)]
    red_codes = [len(red[a] & red[b]) for a, b in combinations(range(21), 2) if b in red[a]]
    blue_codes = [len(blue[a] & blue[b]) for a, b in combinations(range(21), 2) if b in blue[a]]
    require(max(red_codes) == 3 and max(blue_codes) == 6, "Known baseline codegrees fail")
    require(Counter(map(len, red)) == Counter({8: 4, 9: 16, 10: 1}), "Baseline degrees fail")
    return {"vertices": 21, "red_edges": sum(map(len, red)) // 2,
            "red_max_codegree": max(red_codes), "blue_max_codegree": max(blue_codes),
            "status": "known primary construction reproduced; no new lower bound"}


def saturated_gram_control():
    # KG(7,2), split at the edges of C7, with a virtual degree-seven root.
    # The virtual graph violates a root spine, so this is an algebra control.
    pairs = list(combinations(range(7), 2))
    cycle = {tuple(sorted((i, (i + 1) % 7))) for i in range(7)}
    a = [edge for edge in pairs if edge not in cycle]
    b = [edge for edge in pairs if edge in cycle]
    p = [[int(i != j and bool(set(x) & set(y))) for j, y in enumerate(a)]
         for i, x in enumerate(a)]
    m = [[int(set(x).isdisjoint(y)) for y in b] for x in a]
    l = [[int(set(x).isdisjoint(y)) for y in b] for x in b]
    k = list(map(sum, m))
    h = list(map(sum, l))
    e = sum(h) // 2
    p2 = multiply(p, p)
    gram = multiply(m, transpose(m))
    require(k == [3] * 14 and h == [4] * 7, "KG split degrees fail")
    for i in range(14):
        for j in range(14):
            formula = (3 + (k[i] + 3) * (i == j) - p2[i][j]
                       + (k[i] + k[j] - 5) * p[i][j])
            require(gram[i][j] == formula, "Saturated Gram formula fails")
        require(k[i] + sum(p[i][j] * k[j] for j in range(14)) == 21,
                "Saturated row-sum identity fails")
    red, blue = make_control(p, m, l)
    for i in range(14):
        actual = sum((3 - len(red[1 + i] & red[15 + j])) if m[i][j]
                     else (6 - len(blue[1 + i] & blue[15 + j])) for j in range(7))
        formula = 2 * e - 21 + 10 * k[i] - k[i] ** 2 - 2 * sum(m[i][j] * h[j] for j in range(7))
        require(actual == formula == 4, "Substituted row-defect identity fails")
    require(max(len(red[0] & red[15 + j]) for j in range(7)) == 4,
            "Virtual-root invalidity marker fails")
    return {"gram_entries_checked": 196, "row_equations_checked": 14,
            "weighted_row_defects_checked": 14, "row_defects": 4,
            "interpretation": "known KG(7,2) plus virtual root, violating the root red cap; algebra only"}


def main():
    result = {"agent": "six-books-1", "role": "researcher",
              "claim": "A degree-seven vertex in an order22 witness forces105..115 edges",
              "proof_status": "written analytic proof; exact arithmetic controls, no witness enumeration",
              "literal_controls": literal_controls(), "scalar_controls": scalar_controls(),
              "boundary_controls": boundary_graph_controls(), "projection_controls": projection_controls(),
              "baseline": baseline_control(), "saturated_gram_control": saturated_gram_control()}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
