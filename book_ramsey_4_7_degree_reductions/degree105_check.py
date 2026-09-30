#!/usr/bin/env python3
"""Exact controls and complete template check for degree105.md.

Python 3.11+, standard library, one process. The external spectral
classification and written reductions are separate proof dependencies.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
from math import comb, factorial
from pathlib import Path
import json
import random
import sys


ROOT = Path(__file__).resolve().parent
PAIRS = list(combinations(range(7), 2))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def multiply(a, b):
    bt = list(zip(*b))
    return [[sum(x*y for x, y in zip(row, col)) for col in bt] for row in a]


def transpose(a):
    return [list(x) for x in zip(*a)]


def adjacency(n, edges):
    a = [[0]*n for _ in range(n)]
    for i, j in edges:
        a[i][j] = a[j][i] = 1
    return a


def neighbors(n, edges):
    a = [0]*n
    for i, j in edges:
        a[i] |= 1 << j
        a[j] |= 1 << i
    return a


def literal_graph(p, m, l):
    edges = [(0, 15+b) for b in range(7)]
    edges += [(1+a, 1+b) for a, b in combinations(range(14), 2) if not p[a][b]]
    edges += [(1+a, 15+b) for a in range(14) for b in range(7) if m[a][b]]
    edges += [(15+b, 15+c) for b, c in PAIRS if l[b][c]]
    red = neighbors(22, edges)
    blue = [((1 << 22)-1) ^ red[i] ^ (1 << i) for i in range(22)]
    return red, blue


def capacity(l, sigma):
    h = list(map(sum, l))
    e, t = sum(h)//2, sum(sigma)
    l2 = multiply(l, l)
    c = [[6+sigma[b] if b == z else
          (2 if l[b][z] else h[b]+h[z]+sigma[b]+sigma[z]-1)-l2[b][z]
          for z in range(7)] for b in range(7)]
    formula = [9*h[b]+2*e-h[b]**2-2*sum(l[b][z]*h[z] for z in range(7))
               +t+(6-h[b])*sigma[b]-sum(l[b][z]*sigma[z] for z in range(7))
               for b in range(7)]
    require(list(map(sum, c)) == formula, "Capacity matrix row sum fails")
    return c


def baseline():
    lines = (ROOT / "baseline21.rows").read_text().splitlines()
    red = [int(x[::-1], 2) for x in lines]
    n = len(red)
    require(n == 21 and all(len(x) == n for x in lines), "Primary fixture dimensions")
    require(all(not (red[i] >> i) & 1 for i in range(n)), "Primary fixture loop")
    require(all(((red[i] >> j) & 1) == ((red[j] >> i) & 1)
                for i, j in combinations(range(n), 2)), "Primary fixture asymmetry")
    blue = [((1 << n)-1) ^ red[i] ^ (1 << i) for i in range(n)]
    maximum = [max((g[i] & g[j]).bit_count() for i, j in combinations(range(n), 2)
                   if (g[i] >> j) & 1) for g in (red, blue)]
    hist = dict(sorted(Counter(x.bit_count() for x in red).items()))
    require(sum(map(int.bit_count, red))//2 == 93 and hist == {8: 4, 9: 16, 10: 1}
            and maximum == [3, 6], "Known primary witness differs")
    return {"vertices": n, "red_edges": 93, "red_degree_histogram": hist,
            "maximum_red_blue_codegrees": maximum, "status": "known baseline, not new research"}


def scalar_audit():
    counts = Counter()
    states = 0
    stream = sha256()
    for h in product(range(4), repeat=7):
        if sum(h) % 2:
            continue
        e = sum(h)//2
        t = 7-e
        if not 0 <= t <= 7:
            continue
        for selected in combinations(range(7), t):
            bound = 32*e-3*sum(x*x for x in h)+6*t-2*sum(h[b] for b in selected)-126
            states += 1
            stream.update(f"{h}:{selected}:{bound};".encode())
            if bound >= 0:
                counts[(tuple(sorted(h)), tuple(sorted(h[b] for b in selected)), bound)] += 1
    expected = {
        ((0, 2, 2, 2, 2, 2, 2), (0,), 0): 7,
        ((1, 1, 2, 2, 2, 2, 2), (1,), 4): 42,
        ((1, 1, 2, 2, 2, 2, 2), (2,), 2): 105,
        ((1, 1, 2, 2, 2, 3, 3), (), 2): 210,
        ((1, 2, 2, 2, 2, 2, 3), (), 8): 42,
        ((2, 2, 2, 2, 2, 2, 2), (), 14): 1}
    require(states == 143572 and counts == expected, "Scalar profile coverage differs")
    # Independent permutation weight, without replaying labeled h/sigma tuples.
    for (h, selected, bound), count in counts.items():
        weight = factorial(7)
        histogram = Counter(h)
        for v in histogram.values():
            weight //= factorial(v)
        for v, amount in Counter(selected).items():
            weight *= comb(histogram[v], amount)
        require(weight == count, "Independent profile weight differs")
    maxima = [32*e-3*max(2*e, 6*e-14)+6*(7-e)-126 for e in range(8)]
    require(maxima == [-84, -64, -44, -24, -10, -2, 6, 14], "Scalar branch bound")
    budgets = {}
    for a in range(3, 8):
        u = 7-a
        profiles = [d for d in combinations_with_replacement(range(u+1), 7)
                    if sum(d) == 2*u and sum((2-x)**2 for x in d) == 8*a]
        require(not profiles, "A j=0 irregular-row moment profile survived")
        budgets[str(a)] = len(profiles)
    return {"labeled_states": states, "retained_labeled_profiles": sum(counts.values()),
            "profiles": [{"h": h, "selected_h": s, "twice_unused_upper_bound": b,
                          "labeled_count": c} for (h, s, b), c in sorted(counts.items())],
            "independent_histogram_weights_agree": True, "branch_bounds": maxima,
            "j0_irregular_moment_survivors": budgets, "stream_sha256": stream.hexdigest()}


def algebra_controls():
    rng = random.Random(470105)
    ps = [adjacency(14, [(i, j) for i, j in combinations(range(14), 2)
                        if (j-i) % 14 in (1, 2, 3, 11, 12, 13)]),
          adjacency(14, [(i, j) for i, j in combinations(range(14), 2) if i//7 == j//7]),
          adjacency(14, [(i, j) for i, j in combinations(range(14), 2)
                         if i//7 != j//7 and i % 7 != j % 7])]
    stream = sha256()
    row_checks = pair_checks = polynomial_checks = 0
    wrong_parity_seen = False
    for trial in range(96):
        p = ps[trial % 3]
        sigma = [0]*7 if trial % 3 == 0 else [rng.randrange(2) for _ in range(7)]
        m = [[0]*7 for _ in range(14)]
        for b in range(7):
            for a in rng.sample(range(14), 6+sigma[b]):
                m[a][b] = 1
        l = adjacency(7, [(i, j) for i, j in PAIRS if rng.randrange(2)])
        c = capacity(l, sigma)
        s = multiply(transpose(m), m)
        red, blue = literal_graph(p, m, l)
        for b, z in PAIRS:
            g, limit = (red, 3) if l[b][z] else (blue, 6)
            actual = limit-(g[15+b] & g[15+z]).bit_count()
            require(c[b][z]-s[b][z] == actual, "B defect differs from literal pages")
            pair_checks += 1
        for b in range(7):
            actual = sum((3 if l[b][z] else 6)
                         -((red if l[b][z] else blue)[15+b]
                           & (red if l[b][z] else blue)[15+z]).bit_count()
                         for z in range(7) if b != z)
            require(sum(c[b])-sum(s[b]) == actual, "Incident B defect sum differs")
            row_checks += 1
        if not any(sigma):
            require(all(sum(row) % 2 == 0 for row in c), "t=0 capacity row parity")
        if any(sum(row) % 2 for row in c):
            wrong_parity_seen = True
        # Independently check polynomial expansions including the nonzero residual.
        for t in (0, 1):
            q = rng.randrange(1, 5)
            positions = rng.sample(range(14), 2*q+t)
            r = [0]*14
            for a in positions[:q+t]:
                r[a] = 1
            for a in positions[q+t:]:
                r[a] = -1
            if t == 0 and trial % 2:
                # A size-one row is needed to control the cubic term in (7).
                q = rng.randrange(4)
                positions = rng.sample(range(14), 2*q+3)
                r = [0]*14
                for a in positions[:q+2]:
                    r[a] = 1
                for a in positions[q+2:-1]:
                    r[a] = -1
                r[positions[-1]] = -2
            p2 = multiply(p, p)
            gram = [[3+(6+r[a] if a == b else 0)-p2[a][b]
                     +(1+r[a]+r[b])*p[a][b] for b in range(14)] for a in range(14)]
            lhs = sum(r[a]*gram[a][b]*r[b] for a in range(14) for b in range(14))
            pr = [sum(p[a][b]*r[b] for b in range(14)) for a in range(14)]
            if t == 0:
                w = [pr[a]+r[a] for a in range(14)]
                rhs = (4*sum(x*x for x in r)-sum(x**3 for x in r)
                       -sum(x*x for x in w)+3*sum(r[a]*w[a] for a in range(14))
                       +2*sum(r[a]**2*w[a] for a in range(14)))
            else:
                z = [0]*14
                for a in rng.sample(range(14), 7):
                    z[a] = 1
                delta = sum(x*y for x, y in zip(r, z))
                nz = sum(r[a] != 0 and z[a] for a in range(14))
                w = [pr[a]+r[a]-z[a] for a in range(14)]
                rhs = (4*(2*q+1)-5+3*delta+2*nz-sum(x*x for x in w)
                       -2*sum(z[a]*w[a] for a in range(14))
                       +3*sum(r[a]*w[a] for a in range(14))
                       +2*sum(r[a]**2*w[a] for a in range(14)))
            require(lhs == rhs, "Polynomial residual identity differs")
            polynomial_checks += 1
            stream.update(f"{trial}:{t}:{r}:{lhs}:{rhs};".encode())
    require(wrong_parity_seen, "Control incorrectly extends t=0 parity to arbitrary sigma")
    return {"controlled_graphs": 96, "literal_B_spines": pair_checks,
            "literal_capacity_row_sums": row_checks, "polynomial_residual_controls": polynomial_checks,
            "interpretation": "algebra controls; no book validity assumed",
            "wrong_sigma_parity_control_rejected": True, "stream_sha256": stream.hexdigest()}


def exceptional_rows():
    fours = [sum(1 << x for x in row) for row in combinations(range(7), 4)]
    twos = [sum(1 << x for x in row) for row in combinations(range(7), 2)]
    induced = []
    for bits in range(1 << 6):
        p = adjacency(4, [edge for i, edge in enumerate(combinations(range(4), 2))
                          if (bits >> i) & 1])
        r = [1, 1, -1, -1]
        if all(sum(p[a][b]*r[b] for b in range(4)) == -r[a] for a in range(4)):
            induced.append(tuple(map(sum, p)))
    require(Counter(induced) == Counter({(1, 1, 1, 1): 2, (3, 3, 3, 3): 1}),
            "Complete exceptional P domain differs")
    tested = 0
    for h1, h2 in combinations_with_replacement(fours, 2):
        hh = (h1 & h2).bit_count()
        for t1, t2 in combinations_with_replacement(twos, 2):
            tt = (t1 & t2).bit_count()
            cross = [(h1 & t1).bit_count(), (h1 & t2).bit_count(),
                     (h2 & t1).bit_count(), (h2 & t2).bit_count()]
            dot = [4+hh-cross[0]-cross[1], 4+hh-cross[2]-cross[3],
                   cross[0]+cross[2]-2-tt, cross[1]+cross[3]-2-tt]
            for degree in (1, 3):
                require(dot != [4+degree, 4+degree, -4+degree, -4+degree],
                        "Two size-two-row configuration survived")
                tested += 1
    return {"induced_blue_graphs_checked": 64, "induced_survivors": 3,
            "ordered_degree_patterns": induced, "normalized_row_tests": tested,
            "size_two_row_survivors": 0,
            "coverage": "all size-four/size-two row multisets, allowing repeated rows"}


def templates():
    return [("C7", sorted({tuple(sorted((i, (i+1) % 7))) for i in range(7)})),
            ("C3+C4", [(0, 1), (0, 2), (1, 2), (3, 4), (3, 6), (4, 5), (5, 6)])]


def inverse(a):
    n = len(a)
    aug = [[Fraction(x) for x in row]+[Fraction(i == j) for j in range(n)]
           for i, row in enumerate(a)]
    for i in range(n):
        pivot = next((j for j in range(i, n) if aug[j][i]), None)
        if pivot is None:
            return None
        aug[i], aug[pivot] = aug[pivot], aug[i]
        value = aug[i][i]
        aug[i] = [x/value for x in aug[i]]
        for j in range(n):
            if j != i:
                value = aug[j][i]
                aug[j] = [x-value*y for x, y in zip(aug[j], aug[i])]
    return [row[n:] for row in aug]


def line_control(q):
    edges = [edge for edge in PAIRS if edge not in q]
    p = [[int(i != j and bool(set(a) & set(b))) for j, b in enumerate(edges)]
         for i, a in enumerate(edges)]
    m = [[int(not (set(a) & set(b))) for b in q] for a in edges]
    require(all(sum(row) == 6 for row in p), "Line graph degree")
    require(list(map(sum, m)) == [3]*14 and list(map(sum, transpose(m))) == [6]*7,
            "Forced incidence counts")
    g = multiply(m, transpose(m))
    p2 = multiply(p, p)
    require(g == [[3+6*(a == b)+p[a][b]-p2[a][b] for b in range(14)] for a in range(14)],
            "Line incidence Gram fails")
    n = [[int(i in edge) for i in range(7)] for edge in edges]
    for chosen in combinations(range(14), 7):
        inv = inverse([n[i] for i in chosen])
        if inv is not None:
            break
    else:
        raise ValueError("No full-rank incidence minor")
    doubled = [[2*x for x in row] for row in inv]
    require(all(x.denominator == 1 for row in doubled for x in row), "Odd-cycle minor denominator")
    doubled = [[int(x) for x in row] for row in doubled]
    columns = []
    for row in combinations(range(14), 6):
        values = [int(i in row) for i in range(14)]
        x = [sum(doubled[i][j]*values[chosen[j]] for j in range(7)) for i in range(7)]
        if all(x[a]+x[b] == 2*values[j] for j, (a, b) in enumerate(edges)):
            require(sorted(x) == [-1, -1, 1, 1, 1, 1, 1], "Binary potential domain differs")
            columns.append(sum(1 << a for a in row))
    forced = [sum(m[a][b] << a for a in range(14)) for b in range(7)]
    require(sorted(columns) == sorted(forced) and len(set(columns)) == 7,
            "Complete weight-six incidence-image column domain differs")
    return p, m, {"H_edges": edges, "Q_edges": q, "binary_columns_tested": comb(14, 6),
                  "incidence_image_columns": len(columns), "column_masks": sorted(columns),
                  "Gram_entries_checked": 196}


def complete_check(name, q):
    p, m, control = line_control(q)
    gram = multiply(transpose(m), m)
    pm = multiply(p, m)
    counts = {"seven_edge_subsets": 0, "root_spines_pass": 0, "B_spines_pass": 0,
              "all_cross_spines_pass": 0}
    domain_masks = []
    records = []
    for edges in combinations(PAIRS, 7):
        counts["seven_edge_subsets"] += 1
        l = adjacency(7, edges)
        h = list(map(sum, l))
        if max(h) > 3:
            continue
        counts["root_spines_pass"] += 1
        mask = sum(1 << PAIRS.index(edge) for edge in edges)
        domain_masks.append(mask)
        ln = neighbors(7, edges)
        if any(gram[b][z] > (2 if l[b][z] else h[b]+h[z]-1)
               -(ln[b] & ln[z]).bit_count() for b, z in PAIRS):
            continue
        counts["B_spines_pass"] += 1
        ml = multiply(m, l)
        bad = [(a, b, pm[a][b]-ml[a][b]-2 if m[a][b]
                else pm[a][b]-ml[a][b]+h[b]-3)
               for a in range(14) for b in range(7)
               if (pm[a][b]-ml[a][b]-2 if m[a][b]
                   else pm[a][b]-ml[a][b]+h[b]-3) < 0]
        if not bad:
            counts["all_cross_spines_pass"] += 1
            raise ValueError("A valid template completion survived")
        require(len(bad) == 14 and all(not m[a][b] and delta == -1 for a, b, delta in bad),
                "Expected fourteen unit blue-cross violations")
        red, blue = literal_graph(p, m, l)
        require(all((red[1+a] & red[15+b]).bit_count() == 3-delta if m[a][b]
                    else (blue[1+a] & blue[15+b]).bit_count() == 6-delta
                    for a, b, delta in bad), "Literal book differs from matrix defect")
        a, b, delta = bad[0]
        pages = [i for i in range(22) if ((blue[1+a] & blue[15+b]) >> i) & 1]
        require(len(pages) == 7, "Literal B7 pages")
        records.append({"B_edge_mask": mask, "B_edges": edges, "B_degrees": h,
                        "violating_blue_cross_spines": len(bad),
                        "book": {"color": "blue", "spine": [1+a, 15+b], "pages": pages}})
    require(counts["seven_edge_subsets"] == 116280 and counts["root_spines_pass"] == 66090,
            "Complete seven-vertex coverage count differs")
    require(counts["B_spines_pass"] == (1 if name == "C7" else 24), "B-spine survivor count differs")
    require(len({r["B_edge_mask"] for r in records}) == len(records), "Duplicate completion record")
    stream = sha256()
    for mask in sorted(domain_masks):
        stream.update(f"{mask};".encode())
    return {"name": name, "control": control, "counts": counts,
            "root_domain_stream_sha256": stream.hexdigest(), "B_spine_survivors": records}


def run():
    return {"agent": "six-books-1", "role": "researcher",
            "claim": "A degree-seven vertex in an order22 witness forces106..115 edges",
            "proof_status": "written unformalized structural proof plus exact finite check",
            "external_dependency": "Bussemaker-Cvetkovic-Seidel 1976, Theorem1.12 and Proposition5.10; not re-enumerated",
            "baseline": baseline(), "scalar_audit": scalar_audit(),
            "algebra_controls": algebra_controls(), "exceptional_rows": exceptional_rows(),
            "templates": [complete_check(name, q) for name, q in templates()]}


if __name__ == "__main__":
    result = run()
    encoded = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if "--emit-only" not in sys.argv:
        require(json.loads(encoded) == json.loads((ROOT / "degree105_expected.json").read_text()),
                "Deterministic expected diagnostics differ")
    print(encoded, end="")
