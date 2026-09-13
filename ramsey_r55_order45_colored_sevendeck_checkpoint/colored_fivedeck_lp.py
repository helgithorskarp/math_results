#!/usr/bin/env python3
"""Colored induced-five-deck relaxation at a degree-24 good45 root.

Vertices are colored H (the 24 neighbours of the root) or X (its 20
nonneighbours).  Edges are edges of G on both colors; Q is the complement of
G[X].  Every colored graph type through order five is retained, with exact
one-vertex-deletion marginals and all K5/I5/root-forbidden types removed.
The pure H four-deck is in the exact convex hull of the complete dense tail.
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
    for line in (HERE / "scan24e126plus.tsv").read_text().splitlines():
        v = list(map(int, line.split()))
        assert v[0] == 24 and 126 <= v[1] <= 132 and v[16] == 0
        tail_rows.append((v[1], tuple(v[6:16]), v[17]))
    assert len(tail_rows) == 10009 and sum(x[2] for x in tail_rows) == 15913
    if fixed_eh is not None:
        tail_rows = [row for row in tail_rows if row[0] == fixed_eh]
        assert tail_rows

    variables = [
        ("z", n, a, mask)
        for n in range(1, args.order + 1) for a in range(n + 1) for mask in types[n, a]
        if n < args.order or selected_top is None or a in selected_top
    ]
    variables += [("s", i) for i in range(len(tail_rows))]
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
    add_eq("H_vertices", [(('z', 1, 1, types[1, 1][0]), 1)], 1 if args.normalized else 24)
    add_eq("X_vertices", [(('z', 1, 0, types[1, 0][0]), 1)], 1 if args.normalized else 20)
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
                    items.append((('z', *lower, target), -1 if args.normalized else -(24 - (a - 1))))
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
                    items.append((('z', *lower, target), -1 if args.normalized else -(20 - (b - 1))))
                    add_eq(f"delX_n{n}_a{a}_t{target}", items)

    # Exact convex hull of the complete dense H four-decks.
    add_eq("tail_mass", [(('s', i), 1) for i in range(len(tail_rows))], 1)
    h4_by_name = {class4(mask): mask for mask in types[4, 4]}
    assert set(h4_by_name) == set(P4)
    for j, name in enumerate(P4):
        add_eq(
            f"tail_{name}",
            [(('z', 4, 4, h4_by_name[name]), 1)]
            + [
                (('s', i), -Fraction(row[1][j], comb(24, 4)) if args.normalized else -row[1][j])
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

    def matrix(rows):
        rr, cc, vv, rhs = [], [], [], []
        for i, (_name, row, value) in enumerate(rows):
            for j, coefficient in row.items():
                rr.append(i); cc.append(j); vv.append(float(coefficient))
            rhs.append(float(value))
        return coo_matrix((vv, (rr, cc)), shape=(len(rows), len(variables))).tocsr(), np.array(rhs)

    aeq, beq = matrix(eq)
    objective = np.zeros(len(variables))
    objective[where[('z', 2, 2, h_edge)]] = -comb(24, 2) if args.normalized else -1
    objective[where[('z', 2, 0, x_edge)]] = comb(20, 2) if args.normalized else 1
    if args.zero_objective:
        objective[:] = 0
    # 68 <= e(Q)=190-e(X) <= 100.
    bounds_ub = np.zeros((2, len(variables)))
    bounds_ub[0, where[('z', 2, 0, x_edge)]] = -1
    bounds_ub[1, where[('z', 2, 0, x_edge)]] = 1
    ex_lower = Fraction(90, 190) if args.normalized else Fraction(90)
    ex_upper = Fraction(122, 190) if args.normalized else Fraction(122)
    print("type_counts", {f"{n}:{a}": len(v) for (n, a), v in sorted(types.items())}, flush=True)
    print("variables", len(variables), "equalities", len(eq), "inequalities", 2, flush=True)
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
            lower_row = {where[('z', 2, 0, x_edge)]: Fraction(-1)}
            upper_row = {where[('z', 2, 0, x_edge)]: Fraction(1)}
            handle.write(f" lower_ex:")
            write_expression(handle, lower_row)
            handle.write(f" <= {qtext(-ex_lower)}\n")
            handle.write(f" upper_ex:")
            write_expression(handle, upper_row)
            handle.write(f" <= {qtext(ex_upper)}\n")
            handle.write("End\n")
        print("exported_lp", args.export_lp, flush=True)
        return
    if args.bounded_dual:
        matrix_all = vstack((aeq, coo_matrix(bounds_ub)), format="csr")
        rhs_all = np.concatenate((beq, np.array([-float(ex_lower), float(ex_upper)])))
        dual = linprog(
            -rhs_all,
            A_ub=matrix_all.transpose().tocsr(),
            b_ub=np.zeros(len(variables)),
            bounds=[(-1.0, 1.0)] * len(eq) + [(-1.0, 0.0), (-1.0, 0.0)],
            method=args.explicit_dual_method,
            options={"time_limit": args.time_limit, "presolve": True},
        )
        print("bounded_dual_status", dual.status, dual.message, flush=True)
        if not dual.success:
            raise SystemExit(1)
        names = [name for name, _row, _rhs in eq] + ["eX_lower_90", "eX_upper_122"]
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
        rhs_all = np.concatenate((beq, np.array([-float(ex_lower), float(ex_upper)])))
        dual = linprog(
            np.zeros(len(rhs_all)),
            A_ub=matrix_all.transpose().tocsr(),
            b_ub=np.zeros(len(variables)),
            A_eq=rhs_all.reshape(1, -1),
            b_eq=np.array([1.0]),
            bounds=[(None, None)] * len(eq) + [(None, 0.0), (None, 0.0)],
            method=args.explicit_dual_method,
            options={"time_limit": args.time_limit, "presolve": True},
        )
        print("explicit_dual_status", dual.status, dual.message, flush=True)
        if not dual.success:
            raise SystemExit(1)
        names = [name for name, _row, _rhs in eq] + ["eX_lower_90", "eX_upper_122"]
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
        lower = np.concatenate((beq, np.full(2, -np.inf)))
        upper = np.concatenate((beq, np.array([-float(ex_lower), float(ex_upper)])))
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
        names = [name for name, _row, _rhs in eq] + ["eX_lower_90", "eX_upper_122"]
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
        b_ub=np.array([-float(ex_lower), float(ex_upper)]),
        A_eq=aeq,
        b_eq=beq,
        bounds=(0, None),
        method=args.method,
        options={"time_limit": args.time_limit, "presolve": True},
    )
    print("status", result.status, result.message)
    if result.success:
        eh = result.x[where[('z', 2, 2, h_edge)]] * (comb(24, 2) if args.normalized else 1)
        ex = result.x[where[('z', 2, 0, x_edge)]] * (comb(20, 2) if args.normalized else 1)
        print("eH", eh, "eX", ex, "eQ", 190-ex, "paired_sum", eh+190-ex)
        print("positive", int(np.count_nonzero(result.x > 1e-9)))
        selected = [(i, x) for i, x in enumerate(result.x) if variables[i][0] == "s" and x > 1e-9]
        for i, x in selected[:10]:
            row = tail_rows[variables[i][1]]
            print("tail_selector", variables[i][1], "mass", x, "e", row[0])


if __name__ == "__main__":
    main()
