#!/usr/bin/env python3
"""Colored induced-deck relaxations at a root of a hypothetical good45.

Vertices are colored H (the neighbours of the root) or X (its nonneighbours).
Edges are edges of G on both colors; Q is the complement of G[X].  Every
colored graph type through the requested order is retained, with exact
one-vertex-deletion marginals and all K5/I5/root-forbidden types removed.
The default 24+20 model also places the pure H four-deck in the exact convex
hull of the complete dense order-24 tail.  ``--order22-direct`` instead uses
22+22 colors and only the certified extremal edge intervals.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations
from math import comb
from pathlib import Path
import json

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, vstack


HERE = Path(__file__).resolve().parent
P4 = ("i4", "k2ii", "2k2", "p3i", "k3i", "k13", "p4", "c4", "t31", "t32")
REP_LOOKUP: dict[tuple[int, int], dict[int, int]] = {}


@lru_cache(maxsize=None)
def pairs(n: int) -> tuple[tuple[int, int], ...]:
    return tuple((i, j) for j in range(1, n) for i in range(j))


def adjacent(mask: int, n: int, i: int, j: int) -> int:
    if i > j:
        i, j = j, i
    return (mask >> pairs(n).index((i, j))) & 1


def subset_edges(mask: int, n: int, vertices: tuple[int, ...]) -> int:
    return sum(adjacent(mask, n, i, j) for i, j in combinations(vertices, 2))


def valid(mask: int, n: int, a: int) -> bool:
    h = tuple(range(a))
    x = tuple(range(a, n))
    # The root is adjacent precisely to H, so H cannot contain K4 and X
    # cannot contain I4.  The colored set itself cannot contain K5 or I5.
    if any(subset_edges(mask, n, s) == 6 for s in combinations(h, 4)):
        return False
    if any(subset_edges(mask, n, s) == 0 for s in combinations(x, 4)):
        return False
    if any(subset_edges(mask, n, s) in (0, 10) for s in combinations(range(n), 5)):
        return False
    return True


@lru_cache(maxsize=None)
def canonical(mask: int, n: int, a: int) -> int:
    best = None
    for hp in permutations(range(a)):
        for xp0 in permutations(range(n - a)):
            order = hp + tuple(a + i for i in xp0)
            image = 0
            for bit, (i, j) in enumerate(pairs(n)):
                if adjacent(mask, n, order[i], order[j]):
                    image |= 1 << bit
            if best is None or image < best:
                best = image
    assert best is not None
    return best


@lru_cache(maxsize=None)
def colored_types(n: int, a: int) -> tuple[int, ...]:
    """Orbit representatives under permutations preserving H and X."""
    seen = set()
    representatives = []
    group = tuple(
        hp + tuple(a + i for i in xp0)
        for hp in permutations(range(a))
        for xp0 in permutations(range(n - a))
    )
    for mask in range(1 << comb(n, 2)):
        if mask in seen:
            continue
        orbit = set()
        for order in group:
            image = 0
            for bit, (i, j) in enumerate(pairs(n)):
                if adjacent(mask, n, order[i], order[j]):
                    image |= 1 << bit
            orbit.add(image)
        seen.update(orbit)
        representative = min(orbit)
        if valid(representative, n, a):
            representatives.append(representative)
    return tuple(representatives)


def delete_vertex(mask: int, n: int, a: int, removed: int) -> tuple[int, int, int]:
    keep = tuple(i for i in range(n) if i != removed)
    na = a - (removed < a)
    image = 0
    for bit, (i, j) in enumerate(pairs(n - 1)):
        if adjacent(mask, n, keep[i], keep[j]):
            image |= 1 << bit
    representative = REP_LOOKUP.get((n - 1, na), {}).get(image)
    if representative is None:
        representative = canonical(image, n - 1, na)
    return n - 1, na, representative


def class4(mask: int) -> str:
    degree = [0] * 4
    e = 0
    for i, j in pairs(4):
        if adjacent(mask, 4, i, j):
            degree[i] += 1
            degree[j] += 1
            e += 1
    d = tuple(sorted(degree))
    if e == 0: return "i4"
    if e == 1: return "k2ii"
    if e == 2 and d == (1, 1, 1, 1): return "2k2"
    if e == 2: return "p3i"
    if e == 3 and d == (0, 2, 2, 2): return "k3i"
    if e == 3 and d == (1, 1, 1, 3): return "k13"
    if e == 3: return "p4"
    if e == 4 and d == (2, 2, 2, 2): return "c4"
    if e == 4: return "t31"
    if e == 5: return "t32"
    raise ValueError("K4 is not an allowed pure-H class")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, choices=(5, 6, 7), default=5)
    parser.add_argument("--types-file", type=Path)
    parser.add_argument("--fixed-232-degree-moments", action="store_true")
    parser.add_argument("--normalized", action="store_true")
    parser.add_argument("--top-a", type=int)
    parser.add_argument("--top-as", type=str)
    parser.add_argument("--zero-objective", action="store_true")
    parser.add_argument("--export-lp", type=Path)
    parser.add_argument("--order22-direct", action="store_true")
    parser.add_argument("--root-cut-codegrees", action="store_true")
    parser.add_argument("--degree-support-moments", action="store_true")
    parser.add_argument("--turan-neighborhood-cuts", action="store_true")
    parser.add_argument("--extremal-neighborhood-cuts", action="store_true")
    parser.add_argument("--edge-layer-degree-support", action="store_true")
    parser.add_argument("--triple-trace-cuts", action="store_true")
    parser.add_argument("--paired-lower", type=int)
    parser.add_argument("--fixed-eh", type=int)
    parser.add_argument("--fixed-eq", type=int)
    parser.add_argument("--method", choices=("highs", "highs-ds", "highs-ipm"), default="highs")
    parser.add_argument("--time-limit", type=float, default=900.0)
    parser.add_argument("--dual-ray", type=Path)
    parser.add_argument("--explicit-dual", type=Path)
    parser.add_argument("--bounded-dual", type=Path)
    parser.add_argument(
        "--explicit-dual-method", choices=("highs-ds", "highs-ipm"), default="highs-ipm"
    )
    parser.add_argument("--presolve", choices=("off", "on"), default="off")
    args = parser.parse_args()
    if args.order22_direct and not args.normalized:
        raise SystemExit("--order22-direct requires --normalized")
    if args.root_cut_codegrees and not args.order22_direct:
        raise SystemExit("--root-cut-codegrees is implemented for --order22-direct")
    if args.degree_support_moments and not args.order22_direct:
        raise SystemExit("--degree-support-moments is implemented for --order22-direct")
    if args.turan_neighborhood_cuts and not args.degree_support_moments:
        raise SystemExit("--turan-neighborhood-cuts requires --degree-support-moments")
    if args.extremal_neighborhood_cuts and not args.degree_support_moments:
        raise SystemExit("--extremal-neighborhood-cuts requires --degree-support-moments")
    if args.edge_layer_degree_support and not args.degree_support_moments:
        raise SystemExit("--edge-layer-degree-support requires --degree-support-moments")
    if args.triple_trace_cuts and not args.order22_direct:
        raise SystemExit("--triple-trace-cuts is implemented for --order22-direct")
    if args.paired_lower is not None and not args.order22_direct:
        raise SystemExit("--paired-lower is implemented for --order22-direct")
    h_size = 22 if args.order22_direct else 24
    x_size = 22 if args.order22_direct else 20
    if args.normalized and args.fixed_232_degree_moments:
        raise SystemExit("--normalized is not implemented with degree-moment auxiliaries")
    if args.top_a is not None and not (0 <= args.top_a <= args.order):
        raise SystemExit("--top-a must lie between zero and --order")
    if args.top_a is not None and args.top_as is not None:
        raise SystemExit("use at most one of --top-a and --top-as")
    selected_top = None
    if args.top_a is not None:
        selected_top = {args.top_a}
    elif args.top_as is not None:
        selected_top = {int(value) for value in args.top_as.split(",")}
        if not selected_top or not all(0 <= value <= args.order for value in selected_top):
            raise SystemExit("--top-as entries must lie between zero and --order")
    fixed_eh = 132 if args.fixed_232_degree_moments else args.fixed_eh
    fixed_eq = 100 if args.fixed_232_degree_moments else args.fixed_eq
    types: dict[tuple[int, int], tuple[int, ...]] = {}
    if args.types_file:
        loaded = defaultdict(list)
        for line in args.types_file.read_text().splitlines():
            n, a, mask = map(int, line.split())
            if n <= args.order:
                loaded[n, a].append(mask)
        for n in range(1, args.order + 1):
            for a in range(n + 1):
                types[n, a] = tuple(loaded[n, a])
                assert types[n, a] and all(valid(mask, n, a) for mask in types[n, a])
                if n <= 5:
                    assert types[n, a] == colored_types(n, a)
    else:
        if args.order == 7:
            raise SystemExit("--order 7 requires --types-file from colored_types.cpp")
        for n in range(1, args.order + 1):
            for a in range(n + 1):
                types[n, a] = colored_types(n, a)

    # Expand each retained lower-order representative over its colored orbit,
    # making every order-seven deletion a constant-time canonical lookup.
    REP_LOOKUP.clear()
    for n in range(1, args.order):
        for a in range(n + 1):
            lookup = {}
            group = tuple(
                hp + tuple(a + i for i in xp0)
                for hp in permutations(range(a))
                for xp0 in permutations(range(n-a))
            )
            for representative in types[n, a]:
                for order in group:
                    image = 0
                    for bit, (i, j) in enumerate(pairs(n)):
                        if adjacent(representative, n, order[i], order[j]):
                            image |= 1 << bit
                    lookup[image] = representative
            REP_LOOKUP[n, a] = lookup

    tail_rows = []
    if not args.order22_direct:
        for line in (HERE / "scan24e126plus.tsv").read_text().splitlines():
            v = list(map(int, line.split()))
            assert v[0] == 24 and 126 <= v[1] <= 132 and v[16] == 0
            tail_rows.append((v[1], tuple(v[6:16]), v[17]))
        assert len(tail_rows) == 10009 and sum(x[2] for x in tail_rows) == 15913
        if fixed_eh is not None:
            tail_rows = [row for row in tail_rows if row[0] == fixed_eh]
            assert tail_rows
    elif fixed_eh is not None or fixed_eq is not None:
        raise SystemExit("fixed-edge options are not used by --order22-direct")

    variables = [
        ("z", n, a, mask)
        for n in range(1, args.order + 1) for a in range(n + 1) for mask in types[n, a]
        if n < args.order or selected_top is None or a in selected_top
    ]
    variables += [("s", i) for i in range(len(tail_rows))]
    h_degree_pairs = [
        (j, c)
        for j in range(4, 14)
        for c in range(max(0, 19-j), min(17, 23-j)+1)
    ] if args.degree_support_moments else []
    x_degree_pairs = [
        (y, k)
        for y in range(8, 18)
        for k in range(max(5, 20-y), min(22, 24-y)+1)
    ] if args.degree_support_moments else []
    variables += [("dh22", j, c) for j, c in h_degree_pairs]
    variables += [("dx22", y, k) for y, k in x_degree_pairs]
    h_edge_layers = range(110, 115) if args.edge_layer_degree_support else range(0)
    q_edge_layers = range(88, 115) if args.edge_layer_degree_support else range(0)
    h_layer_degree_pairs = [
        (e, j, c) for e in h_edge_layers for j, c in h_degree_pairs
        if 77 <= e-j <= 107
    ]
    q_layer_degree_pairs = [
        (e, y, k) for e in q_edge_layers for y, k in x_degree_pairs
        if 77 <= e-(21-y) <= 107
    ]
    variables += [("she", e) for e in h_edge_layers]
    variables += [("sqe", e) for e in q_edge_layers]
    variables += [("ldh22", e, j, c) for e, j, c in h_layer_degree_pairs]
    variables += [("ldx22", e, y, k) for e, y, k in q_layer_degree_pairs]
    if args.fixed_232_degree_moments:
        # At e(H)=132 both complete-tail graphs are 11-regular.  At e(Q)=100
        # the unique complete extremal graph has Q-degree histogram
        # 9^2 10^16 11^2, hence Y-degree histogram 10^2 9^16 8^2.
        variables += [("dh", c) for c in range(8, 13)]
        variables += [
            ("dx", y, k)
            for y in (8, 9, 10) for k in range(20-y, 25-y) if k >= 9
        ]
    where = {v: i for i, v in enumerate(variables)}
    eq: list[tuple[str, dict[int, Fraction], Fraction]] = []

    def add_eq(name, items, rhs=0):
        row = defaultdict(Fraction)
        for variable, coefficient in items:
            if coefficient:
                row[where[variable]] += Fraction(coefficient)
        eq.append((name, dict(row), Fraction(rhs)))

    # One-vertex colored decks.
    add_eq("H_vertices", [(('z', 1, 1, types[1, 1][0]), 1)], 1 if args.normalized else h_size)
    add_eq("X_vertices", [(('z', 1, 0, types[1, 0][0]), 1)], 1 if args.normalized else x_size)
    for n in range(2, args.order + 1):
        for a in range(n + 1):
            if n == args.order and selected_top is not None and a not in selected_top:
                continue
            b = n - a
            if a:
                lower = (n - 1, a - 1)
                deletion_counts = defaultdict(list)
                for mask in types[n, a]:
                    counts = defaultdict(int)
                    for r in range(a):
                        counts[delete_vertex(mask, n, a, r)[2]] += 1
                    for target, count in counts.items():
                        deletion_counts[target].append((mask, count))
                for target in types[lower]:
                    items = [(('z', n, a, mask), Fraction(count, a) if args.normalized else count)
                             for mask, count in deletion_counts[target]]
                    items.append((('z', *lower, target), -1 if args.normalized else -(h_size - (a - 1))))
                    add_eq(f"delH_n{n}_a{a}_t{target}", items)
            if b:
                lower = (n - 1, a)
                deletion_counts = defaultdict(list)
                for mask in types[n, a]:
                    counts = defaultdict(int)
                    for r in range(a, n):
                        counts[delete_vertex(mask, n, a, r)[2]] += 1
                    for target, count in counts.items():
                        deletion_counts[target].append((mask, count))
                for target in types[lower]:
                    items = [(('z', n, a, mask), Fraction(count, b) if args.normalized else count)
                             for mask, count in deletion_counts[target]]
                    items.append((('z', *lower, target), -1 if args.normalized else -(x_size - (b - 1))))
                    add_eq(f"delX_n{n}_a{a}_t{target}", items)

    # Exact convex hull of the complete dense H four-decks.
    if tail_rows:
        add_eq("tail_mass", [(('s', i), 1) for i in range(len(tail_rows))], 1)
        h4_by_name = {class4(mask): mask for mask in types[4, 4]}
        assert set(h4_by_name) == set(P4)
        for j, name in enumerate(P4):
            add_eq(
                f"tail_{name}",
                [(('z', 4, 4, h4_by_name[name]), 1)]
                + [
                    (('s', i), -Fraction(row[1][j], comb(h_size, 4)) if args.normalized else -row[1][j])
                    for i, row in enumerate(tail_rows)
                ],
            )

    h_edge = canonical(1, 2, 2)
    x_edge = canonical(1, 2, 0)
    if fixed_eh is not None:
        add_eq(
            "fixed_eH", [(('z', 2, 2, h_edge), 1)],
            Fraction(fixed_eh, comb(24, 2)) if args.normalized else fixed_eh,
        )
    if fixed_eq is not None:
        add_eq(
            "fixed_eQ", [(('z', 2, 0, x_edge), 1)],
            Fraction(190-fixed_eq, comb(20, 2)) if args.normalized else 190-fixed_eq,
        )
    if args.fixed_232_degree_moments:
        add_eq("H_degree_vertices", [(('dh', c), 1) for c in range(8, 13)], 24)
        for y, count in ((8, 2), (9, 16), (10, 2)):
            add_eq(
                f"X_internal_degree_{y}",
                [(('dx', y, k), 1) for k in range(20-y, 25-y) if k >= 9],
                count,
            )

        # Full bivariate factorial moments of the internal/cross degrees are
        # exactly the counts of colored centered stars in the induced deck.
        for r in range(args.order):
            for s in range(args.order-r):
                n = 1 + r + s
                hitems = [(('dh', c), comb(11, r)*comb(c, s)) for c in range(8, 13)]
                for mask in types[n, r+1]:
                    centers = sum(
                        all(adjacent(mask, n, center, leaf) for leaf in range(n) if leaf != center)
                        for center in range(r+1)
                    )
                    hitems.append((('z', n, r+1, mask), -centers))
                add_eq(f"H_star_r{r}_s{s}", hitems)

                xitems = [
                    (('dx', y, k), comb(k, r)*comb(y, s))
                    for y in (8, 9, 10) for k in range(20-y, 25-y) if k >= 9
                ]
                for mask in types[n, r]:
                    centers = sum(
                        all(adjacent(mask, n, center, leaf) for leaf in range(n) if leaf != center)
                        for center in range(r, n)
                    )
                    xitems.append((('z', n, r, mask), -centers))
                add_eq(f"X_star_r{r}_s{s}", xitems)

    if args.degree_support_moments:
        # Continuous degree-distribution variables are probabilities on the
        # complete support forced by 20 <= deg_G(v) <= 24 and by
        # R(3,5)=14, R(4,4)=18 inside an order-22 (4,5)-graph.  Their full
        # bivariate factorial moments through the retained deck order equal
        # the corresponding colored centered-star densities.
        add_eq("H22_degree_mass", [(('dh22', j, c), 1) for j, c in h_degree_pairs], 1)
        add_eq("X22_degree_mass", [(('dx22', y, k), 1) for y, k in x_degree_pairs], 1)
        for r in range(args.order):
            for s in range(args.order-r):
                n = 1 + r + s
                hitems = [
                    (('dh22', j, c), comb(j, r)*comb(c, s))
                    for j, c in h_degree_pairs
                ]
                hfactor = Fraction(comb(h_size, r+1)*comb(x_size, s), h_size)
                for mask in types[n, r+1]:
                    centers = sum(
                        all(adjacent(mask, n, center, leaf)
                            for leaf in range(n) if leaf != center)
                        for center in range(r+1)
                    )
                    hitems.append((('z', n, r+1, mask), -hfactor*centers))
                add_eq(f"H22_star_r{r}_s{s}", hitems)

                xitems = [
                    (('dx22', y, k), comb(k, r)*comb(y, s))
                    for y, k in x_degree_pairs
                ]
                xfactor = Fraction(comb(h_size, r)*comb(x_size, s+1), x_size)
                for mask in types[n, r]:
                    centers = sum(
                        all(adjacent(mask, n, center, leaf)
                            for leaf in range(n) if leaf != center)
                        for center in range(r, n)
                    )
                    xitems.append((('z', n, r, mask), -xfactor*centers))
                add_eq(f"X22_star_r{r}_s{s}", xitems)

    if args.edge_layer_degree_support:
        # Convex-hull lift over every integral target edge layer.  Within an
        # e-edge (4,5,22)-graph the average internal degree is e/11, and
        # deletion of a vertex of internal degree t leaves an order-21 graph
        # with 77 <= e-t <= 107 edges.  These rows retain that correlation,
        # which is lost by a single averaged degree distribution.
        add_eq("H_edge_layer_mass", [(('she', e), 1) for e in h_edge_layers], 1)
        add_eq("Q_edge_layer_mass", [(('sqe', e), 1) for e in q_edge_layers], 1)
        for j, c in h_degree_pairs:
            add_eq(
                f"H_edge_layer_project_j{j}_c{c}",
                [(('dh22', j, c), 1)] + [
                    (('ldh22', e, j, c), -1) for e in h_edge_layers
                    if (e, j, c) in h_layer_degree_pairs
                ],
            )
        for y, k in x_degree_pairs:
            add_eq(
                f"Q_edge_layer_project_y{y}_k{k}",
                [(('dx22', y, k), 1)] + [
                    (('ldx22', e, y, k), -1) for e in q_edge_layers
                    if (e, y, k) in q_layer_degree_pairs
                ],
            )
        for e in h_edge_layers:
            members = [(j, c) for ee, j, c in h_layer_degree_pairs if ee == e]
            add_eq(
                f"H_edge_layer_{e}_mass",
                [(('ldh22', e, j, c), 1) for j, c in members] + [(('she', e), -1)],
            )
            add_eq(
                f"H_edge_layer_{e}_degree_sum",
                [(('ldh22', e, j, c), j) for j, c in members]
                + [(('she', e), Fraction(-e, 11))],
            )
        for e in q_edge_layers:
            members = [(y, k) for ee, y, k in q_layer_degree_pairs if ee == e]
            add_eq(
                f"Q_edge_layer_{e}_mass",
                [(('ldx22', e, y, k), 1) for y, k in members] + [(('sqe', e), -1)],
            )
            add_eq(
                f"Q_edge_layer_{e}_degree_sum",
                [(('ldx22', e, y, k), 21-y) for y, k in members]
                + [(('sqe', e), Fraction(-e, 11))],
            )
        add_eq(
            "H_edge_layer_edge_density",
            [(('z', 2, 2, h_edge), 1)]
            + [(('she', e), Fraction(-e, comb(22, 2))) for e in h_edge_layers],
        )
        add_eq(
            "Q_edge_layer_edge_density",
            [(('z', 2, 0, x_edge), 1)]
            + [(('sqe', e), Fraction(e, comb(22, 2))) for e in q_edge_layers],
            1,
        )

    def matrix(rows):
        rr, cc, vv, rhs = [], [], [], []
        for i, (_name, row, value) in enumerate(rows):
            for j, coefficient in row.items():
                rr.append(i); cc.append(j); vv.append(float(coefficient))
            rhs.append(float(value))
        return coo_matrix((vv, (rr, cc)), shape=(len(rows), len(variables))).tocsr(), np.array(rhs)

    aeq, beq = matrix(eq)
    objective = np.zeros(len(variables))
    objective[where[('z', 2, 2, h_edge)]] = -comb(h_size, 2) if args.normalized else -1
    objective[where[('z', 2, 0, x_edge)]] = comb(x_size, 2) if args.normalized else 1
    if args.zero_objective:
        objective[:] = 0
    if args.order22_direct:
        # H is a (4,5,22)-graph with the candidate dense range 110..114.
        # Y=G[X] is the complement of a (4,5,22)-graph Q with 88..114
        # edges, hence e(Y) lies in 117..143.
        denominator = comb(22, 2)
        ub_specs = [
            ("eH_lower_110", {where[('z', 2, 2, h_edge)]: Fraction(-1)}, Fraction(-110, denominator)),
            ("eH_upper_114", {where[('z', 2, 2, h_edge)]: Fraction(1)}, Fraction(114, denominator)),
            ("eY_lower_117", {where[('z', 2, 0, x_edge)]: Fraction(-1)}, Fraction(-117, denominator)),
            ("eY_upper_143", {where[('z', 2, 0, x_edge)]: Fraction(1)}, Fraction(143, denominator)),
        ]
        if args.paired_lower is not None:
            ub_specs.append((
                f"paired_sum_lower_{args.paired_lower}",
                {
                    where[('z', 2, 2, h_edge)]: Fraction(-1),
                    where[('z', 2, 0, x_edge)]: Fraction(1),
                },
                Fraction(1) - Fraction(args.paired_lower, denominator),
            ))
        if args.root_cut_codegrees:
            # Exact degree-22 specializations of the two root-cut codegree
            # inequalities.  A normalized z(3,a,type) is the probability of
            # the indicated induced type on a uniformly chosen colored set.
            # Multiplying by 22*C(22,2) therefore recovers the corresponding
            # unlabelled triple counts.
            triple_sets = 22 * comb(22, 2)

            c22_row: dict[int, Fraction] = {}
            for mask in types[3, 1]:
                cross = adjacent(mask, 3, 0, 1) + adjacent(mask, 3, 0, 2)
                y_edge = adjacent(mask, 3, 1, 2)
                coefficient = (
                    triple_sets * ((cross == 2) - (1-y_edge)*cross)
                    + 27 * comb(22, 2) * (1-y_edge)
                )
                if coefficient:
                    c22_row[where[('z', 3, 1, mask)]] = Fraction(coefficient)
            ub_specs.append(("C22_root_cut", c22_row, Fraction(3003)))

            r22_row: dict[int, Fraction] = {}
            for mask in types[3, 2]:
                cross = adjacent(mask, 3, 2, 0) + adjacent(mask, 3, 2, 1)
                h_edge_present = adjacent(mask, 3, 0, 1)
                coefficient = (
                    triple_sets * ((cross == 2) - (1-h_edge_present)*cross)
                    - 17 * comb(22, 2) * h_edge_present
                )
                if coefficient:
                    r22_row[where[('z', 3, 2, mask)]] = Fraction(coefficient)
            ub_specs.append(("R22_root_cut", r22_row, Fraction(-2079)))
        if args.triple_trace_cuts:
            # Four color-dual trace inequalities.  For example, the X
            # vertices avoiding an independent H-triple form a clique (or an
            # independent H-triple together with an X-nonedge gives I5), and
            # that clique has order at most four (or it gives K5).  Swap
            # clique/independent and H/X for the other three rows.
            mixed_sets = comb(22, 3) * 22
            pure_sets = comb(22, 3)
            trace_rows = {
                "H_i3_X_avoids": defaultdict(Fraction),
                "H_k3_X_common": defaultdict(Fraction),
                "X_i3_H_avoids": defaultdict(Fraction),
                "X_k3_H_common": defaultdict(Fraction),
            }
            for mask in types[4, 3]:
                h_edges = sum(adjacent(mask, 4, i, j) for i, j in combinations(range(3), 2))
                cross = sum(adjacent(mask, 4, i, 3) for i in range(3))
                if h_edges == 0 and cross == 0:
                    trace_rows["H_i3_X_avoids"][where[('z', 4, 3, mask)]] += mixed_sets
                if h_edges == 3 and cross == 3:
                    trace_rows["H_k3_X_common"][where[('z', 4, 3, mask)]] += mixed_sets
            for mask in types[4, 1]:
                x_edges = sum(adjacent(mask, 4, i, j) for i, j in combinations(range(1, 4), 2))
                cross = sum(adjacent(mask, 4, 0, i) for i in range(1, 4))
                if x_edges == 0 and cross == 0:
                    trace_rows["X_i3_H_avoids"][where[('z', 4, 1, mask)]] += mixed_sets
                if x_edges == 3 and cross == 3:
                    trace_rows["X_k3_H_common"][where[('z', 4, 1, mask)]] += mixed_sets
            trace_rows["H_i3_X_avoids"][where[('z', 3, 3, canonical(0, 3, 3))]] -= 4*pure_sets
            # In the next two orientations the trace set together with the
            # campaign root would itself form I5 or K5 at size four.
            trace_rows["H_k3_X_common"][where[('z', 3, 3, canonical(7, 3, 3))]] -= 3*pure_sets
            trace_rows["X_i3_H_avoids"][where[('z', 3, 0, canonical(0, 3, 0))]] -= 3*pure_sets
            trace_rows["X_k3_H_common"][where[('z', 3, 0, canonical(7, 3, 0))]] -= 4*pure_sets
            ub_specs.extend((name, dict(row), Fraction(0)) for name, row in trace_rows.items())
        if args.turan_neighborhood_cuts:
            # For every vertex v of a good graph, G[N(v)] is K4-free and the
            # complement induced by the nonneighbours of v is also K4-free.
            # Turan's theorem bounds both relevant pair counts by floor(t^2/3).
            # Summing separately over H- and X-centres gives four exact linear
            # inequalities.  The root contributes 2e(H) to the H-neighbour
            # sum and 2e(Q) to the X-nonneighbour sum.
            h_neighbour_row = defaultdict(Fraction)
            h_nonneighbour_row = defaultdict(Fraction)
            x_neighbour_row = defaultdict(Fraction)
            x_nonneighbour_row = defaultdict(Fraction)

            h_neighbour_row[where[('z', 2, 2, h_edge)]] += 2 * comb(22, 2)
            x_nonneighbour_row[where[('z', 2, 0, x_edge)]] -= 2 * comb(22, 2)
            # 2e(Q)=2*C(22,2)*(1-p_Y); move the variable term to the row and
            # leave the constant on the right-hand side below.
            x_nonneighbour_constant = 2 * comb(22, 2)

            for a in range(4):
                subset_count = comb(22, a) * comb(22, 3-a)
                for mask in types[3, a]:
                    edge_count = sum(adjacent(mask, 3, i, j) for i, j in pairs(3))
                    variable = where[('z', 3, a, mask)]
                    if edge_count == 3:
                        h_neighbour_row[variable] += subset_count * a
                        x_neighbour_row[variable] += subset_count * (3-a)
                    if edge_count == 0:
                        h_nonneighbour_row[variable] += subset_count * a
                        x_nonneighbour_row[variable] += subset_count * (3-a)

            for j, c in h_degree_pairs:
                h_neighbour_row[where[('dh22', j, c)]] -= 22 * ((1+j+c)**2 // 3)
                h_nonneighbour_row[where[('dh22', j, c)]] -= 22 * ((43-j-c)**2 // 3)
            for y, k in x_degree_pairs:
                x_neighbour_row[where[('dx22', y, k)]] -= 22 * ((y+k)**2 // 3)
                x_nonneighbour_row[where[('dx22', y, k)]] -= 22 * ((44-y-k)**2 // 3)

            ub_specs.extend([
                ("H_neighbour_Turan", dict(h_neighbour_row), Fraction(0)),
                ("H_nonneighbour_Turan", dict(h_nonneighbour_row), Fraction(0)),
                ("X_neighbour_Turan", dict(x_neighbour_row), Fraction(0)),
                ("X_nonneighbour_Turan", dict(x_nonneighbour_row), Fraction(-x_nonneighbour_constant)),
            ])
        if args.extremal_neighborhood_cuts:
            # Complete-catalogue extrema for (4,5,m), 20 <= m <= 24.
            # For every vertex v, G[N(v)] is a (4,5,d(v))-graph.  The
            # complement on its nonneighbours is a (4,5,44-d(v))-graph.
            # We impose both endpoint bounds after summing over each root
            # color.  Catalogue completeness is an explicit imported trust
            # boundary, not established by this program.
            alpha = {19: 57, 20: 68, 21: 77, 22: 88, 23: 101, 24: 116}
            beta = {19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}
            base_hn = defaultdict(Fraction)
            base_hq = defaultdict(Fraction)
            base_xn = defaultdict(Fraction)
            base_xq = defaultdict(Fraction)
            base_hn[where[('z', 2, 2, h_edge)]] += 2 * comb(22, 2)
            base_xq[where[('z', 2, 0, x_edge)]] -= 2 * comb(22, 2)
            xq_constant = 2 * comb(22, 2)
            for a in range(4):
                subset_count = comb(22, a) * comb(22, 3-a)
                for mask in types[3, a]:
                    edge_count = sum(adjacent(mask, 3, i, j) for i, j in pairs(3))
                    variable = where[('z', 3, a, mask)]
                    if edge_count == 3:
                        base_hn[variable] += subset_count * a
                        base_xn[variable] += subset_count * (3-a)
                    if edge_count == 0:
                        base_hq[variable] += subset_count * a
                        base_xq[variable] += subset_count * (3-a)

            def add_extreme_pair(name, base, constant, degree_terms):
                upper = defaultdict(Fraction, base)
                lower = defaultdict(Fraction, {i: -c for i, c in base.items()})
                for variable, degree in degree_terms:
                    upper[where[variable]] -= 22 * beta[degree]
                    lower[where[variable]] += 22 * alpha[degree]
                ub_specs.append((f"{name}_upper", dict(upper), Fraction(-constant)))
                ub_specs.append((f"{name}_lower", dict(lower), Fraction(constant)))

            add_extreme_pair(
                "H_neighbour_extreme", base_hn, 0,
                [(('dh22', j, c), 1+j+c) for j, c in h_degree_pairs],
            )
            add_extreme_pair(
                "H_nonneighbour_extreme", base_hq, 0,
                [(('dh22', j, c), 43-j-c) for j, c in h_degree_pairs],
            )
            add_extreme_pair(
                "X_neighbour_extreme", base_xn, 0,
                [(('dx22', y, k), y+k) for y, k in x_degree_pairs],
            )
            add_extreme_pair(
                "X_nonneighbour_extreme", base_xq, xq_constant,
                [(('dx22', y, k), 44-y-k) for y, k in x_degree_pairs],
            )

            # Two of those local (4,5)-graphs contain the campaign root as a
            # distinguished vertex.  Deleting it leaves a (4,5,d-1)-graph,
            # so e(F)-deg_F(root) obeys the order-(d-1) extrema as well.
            # Intersecting the two intervals gives conditional endpoint cuts.
            hn_upper = defaultdict(Fraction, base_hn)
            hn_lower = defaultdict(Fraction, {i: -c for i, c in base_hn.items()})
            for j, c in h_degree_pairs:
                d = 1+j+c
                upper = min(beta[d], beta[d-1]+j)
                lower = max(alpha[d], alpha[d-1]+j)
                hn_upper[where[('dh22', j, c)]] -= 22 * upper
                hn_lower[where[('dh22', j, c)]] += 22 * lower
            ub_specs.append(("H_neighbour_root_conditional_upper", dict(hn_upper), Fraction(0)))
            ub_specs.append(("H_neighbour_root_conditional_lower", dict(hn_lower), Fraction(0)))

            xq_upper = defaultdict(Fraction, base_xq)
            xq_lower = defaultdict(Fraction, {i: -c for i, c in base_xq.items()})
            for y, k in x_degree_pairs:
                m = 44-y-k
                root_degree = 21-y
                upper = min(beta[m], beta[m-1]+root_degree)
                lower = max(alpha[m], alpha[m-1]+root_degree)
                xq_upper[where[('dx22', y, k)]] -= 22 * upper
                xq_lower[where[('dx22', y, k)]] += 22 * lower
            ub_specs.append(("X_nonneighbour_root_conditional_upper", dict(xq_upper), Fraction(-xq_constant)))
            ub_specs.append(("X_nonneighbour_root_conditional_lower", dict(xq_lower), Fraction(xq_constant)))
    else:
        ex_lower = Fraction(90, 190) if args.normalized else Fraction(90)
        ex_upper = Fraction(122, 190) if args.normalized else Fraction(122)
        ub_specs = [
            ("eX_lower_90", {where[('z', 2, 0, x_edge)]: Fraction(-1)}, -ex_lower),
            ("eX_upper_122", {where[('z', 2, 0, x_edge)]: Fraction(1)}, ex_upper),
        ]
    bounds_ub = np.zeros((len(ub_specs), len(variables)))
    for row_index, (_name, row, _rhs) in enumerate(ub_specs):
        for column, coefficient in row.items():
            bounds_ub[row_index, column] = float(coefficient)
    bounds_rhs = np.array([float(rhs) for _name, _row, rhs in ub_specs])
    print("type_counts", {f"{n}:{a}": len(v) for (n, a), v in sorted(types.items())}, flush=True)
    print("variables", len(variables), "equalities", len(eq), "inequalities", len(ub_specs), flush=True)
    if args.export_lp:
        def qtext(value: Fraction) -> str:
            return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"

        def write_expression(handle, row: dict[int, Fraction]) -> None:
            width = 0
            for index, coefficient in sorted(row.items()):
                sign = "+" if coefficient > 0 else "-"
                term = f" {sign} {qtext(abs(coefficient))} x{index}"
                if width and width + len(term) > 120:
                    handle.write("\n   ")
                    width = 3
                handle.write(term)
                width += len(term)

        with args.export_lp.open("w") as handle:
            handle.write("Minimize\n obj: 0\nSubject To\n")
            for index, (_name, row, rhs) in enumerate(eq):
                handle.write(f" c{index}:")
                write_expression(handle, row)
                handle.write(f" = {qtext(rhs)}\n")
            for name, row, rhs in ub_specs:
                handle.write(f" {name}:")
                write_expression(handle, row)
                handle.write(f" <= {qtext(rhs)}\n")
            handle.write("End\n")
        print("exported_lp", args.export_lp, flush=True)
        return
    if args.bounded_dual:
        matrix_all = vstack((aeq, coo_matrix(bounds_ub)), format="csr")
        rhs_all = np.concatenate((beq, bounds_rhs))
        dual = linprog(
            -rhs_all,
            A_ub=matrix_all.transpose().tocsr(),
            b_ub=np.zeros(len(variables)),
            bounds=[(-1.0, 1.0)] * len(eq) + [(-1.0, 0.0)] * len(ub_specs),
            method=args.explicit_dual_method,
            options={"time_limit": args.time_limit, "presolve": True},
        )
        print("bounded_dual_status", dual.status, dual.message, flush=True)
        if not dual.success:
            raise SystemExit(1)
        names = [name for name, _row, _rhs in eq] + [name for name, _row, _rhs in ub_specs]
        payload = {
            "model_status": dual.message,
            "rhs_value": float(rhs_all @ dual.x),
            "max_column": float(np.max(matrix_all.transpose() @ dual.x)),
            "rows": [
                {"index": i, "name": names[i], "multiplier": float(value)}
                for i, value in enumerate(dual.x) if abs(value) > 1e-12
            ],
        }
        args.bounded_dual.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        return
    if args.explicit_dual:
        # Solve the Farkas system directly.  Equality-row multipliers are
        # free, while the two <= row multipliers are nonpositive.  The
        # normalization b^T y = 1 turns a nonzero infeasibility ray into a
        # feasibility problem.
        matrix_all = vstack((aeq, coo_matrix(bounds_ub)), format="csr")
        rhs_all = np.concatenate((beq, bounds_rhs))
        dual = linprog(
            np.zeros(len(rhs_all)),
            A_ub=matrix_all.transpose().tocsr(),
            b_ub=np.zeros(len(variables)),
            A_eq=rhs_all.reshape(1, -1),
            b_eq=np.array([1.0]),
            bounds=[(None, None)] * len(eq) + [(None, 0.0)] * len(ub_specs),
            method=args.explicit_dual_method,
            options={"time_limit": args.time_limit, "presolve": True},
        )
        print("explicit_dual_status", dual.status, dual.message, flush=True)
        if not dual.success:
            raise SystemExit(1)
        names = [name for name, _row, _rhs in eq] + [name for name, _row, _rhs in ub_specs]
        payload = {
            "model_status": dual.message,
            "normalization": float(rhs_all @ dual.x),
            "max_column": float(np.max(matrix_all.transpose() @ dual.x)),
            "rows": [
                {"index": i, "name": names[i], "multiplier": float(value)}
                for i, value in enumerate(dual.x) if abs(value) > 1e-12
            ],
        }
        args.explicit_dual.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        return
    if args.dual_ray:
        import highspy
        matrix_all = vstack((aeq, coo_matrix(bounds_ub)), format="csr")
        lower = np.concatenate((beq, np.full(len(ub_specs), -np.inf)))
        upper = np.concatenate((beq, bounds_rhs))
        highs = highspy.Highs()
        highs.setOptionValue("presolve", args.presolve)
        highs.setOptionValue("solver", "simplex")
        highs.setOptionValue("time_limit", args.time_limit)
        highs.addVars(
            len(variables), np.zeros(len(variables)), np.full(len(variables), np.inf)
        )
        highs.addRows(
            len(lower), lower, upper, matrix_all.nnz,
            matrix_all.indptr.astype(np.int32), matrix_all.indices.astype(np.int32),
            matrix_all.data.astype(float),
        )
        highs.run()
        ray_status, exists, ray = highs.getDualRay()
        print("highspy_status", highs.modelStatusToString(highs.getModelStatus()), flush=True)
        print("dual_ray", ray_status, exists,
              "nonzero", int(np.count_nonzero(np.abs(ray) > 1e-12)), flush=True)
        if not exists:
            raise SystemExit(1)
        names = [name for name, _row, _rhs in eq] + [name for name, _row, _rhs in ub_specs]
        payload = {
            "model_status": highs.modelStatusToString(highs.getModelStatus()),
            "rows": [
                {"index": i, "name": names[i], "multiplier": float(value)}
                for i, value in enumerate(ray) if abs(value) > 1e-12
            ],
        }
        args.dual_ray.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        return
    result = linprog(
        objective,
        A_ub=bounds_ub,
        b_ub=bounds_rhs,
        A_eq=aeq,
        b_eq=beq,
        bounds=(0, None),
        method=args.method,
        options={"time_limit": args.time_limit, "presolve": True},
    )
    print("status", result.status, result.message)
    if result.success:
        eh = result.x[where[('z', 2, 2, h_edge)]] * (comb(h_size, 2) if args.normalized else 1)
        ex = result.x[where[('z', 2, 0, x_edge)]] * (comb(x_size, 2) if args.normalized else 1)
        q_edges = comb(x_size, 2) - ex
        print("eH", eh, "eX", ex, "eQ", q_edges, "paired_sum", eh+q_edges)
        print("positive", int(np.count_nonzero(result.x > 1e-9)))
        selected = [(i, x) for i, x in enumerate(result.x) if variables[i][0] == "s" and x > 1e-9]
        for i, x in selected[:10]:
            row = tail_rows[variables[i][1]]
            print("tail_selector", variables[i][1], "mass", x, "e", row[0])


if __name__ == "__main__":
    main()
