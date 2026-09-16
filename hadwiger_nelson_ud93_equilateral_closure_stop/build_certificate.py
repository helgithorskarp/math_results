#!/usr/bin/env python3
"""Produce the untrusted certificate for the frozen UD9-3 closure."""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
from pathlib import Path

import mpmath as mp
from pysat.solvers import Solver


HERE = Path(__file__).resolve().parent


SOURCE_EDGES = (
    (0, 1), (0, 2), (0, 4), (1, 3), (1, 8), (2, 4), (2, 6),
    (2, 7), (3, 5), (3, 6), (3, 7), (3, 8), (4, 5), (5, 8),
    (6, 7),
)
ROOTS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))


def kadd(x, y):
    return x[0] + y[0], x[1] + y[1]


def kmul(x, y):
    a, b = x
    c, d = y
    return a * c - b * d, a * d + b * c + b * d


def vadd(x, y):
    return tuple(kadd(a, b) for a, b in zip(x, y))


def vsub(x, y):
    return tuple((a[0] - b[0], a[1] - b[1]) for a, b in zip(x, y))


def vscale(x, scalar):
    return tuple(kmul(scalar, a) for a in x)


def formal_source():
    zero = ((Q(0), Q(0)),) * 3

    def basis(i):
        row = list(zero)
        row[i] = (Q(1), Q(0))
        return tuple(row)

    def combination(*terms):
        value = zero
        for scalar, vector in terms:
            value = vadd(value, vscale(vector, scalar))
        return value

    one, z, w = (basis(i) for i in range(3))
    rho = (Q(0), Q(1))
    rhobar = (Q(1), Q(-1))
    alpha = (Q(1, 3), Q(1, 3))
    one_minus_alpha = (Q(2, 3), Q(-1, 3))
    p3 = combination(((Q(0), Q(-1)), one),
                     ((Q(1), Q(1)), w))
    return (
        zero,
        one,
        z,
        w,
        vscale(z, rhobar),
        p3,
        combination((one_minus_alpha, z), (alpha, w)),
        combination((alpha, z), (one_minus_alpha, w)),
        combination((rhobar, w), (rho, p3)),
    )


def closure_graph(round_index=8):
    source = formal_source()
    unit_differences = {
        vscale(vsub(source[b], source[a]), root)
        for a, b in SOURCE_EDGES for root in ROOTS
    }
    points = set(source)
    rows = []
    last_edges = None
    for current_round in range(round_index + 2):
        ordered = sorted(points)
        edges = [
            (left, right)
            for right in range(len(ordered))
            for left in range(right)
            if vsub(ordered[right], ordered[left]) in unit_differences
        ]
        rows.append((len(ordered), len(edges)))
        if current_round == round_index:
            target = ordered, edges
        if current_round == round_index + 1:
            last_edges = edges
            break
        enlarged = set(points)
        for left, right in edges:
            delta = vsub(ordered[right], ordered[left])
            enlarged.add(vadd(ordered[left], vscale(delta, ROOTS[1])))
            enlarged.add(vadd(ordered[left], vscale(delta, ROOTS[5])))
        points = enlarged
    assert last_edges is not None
    return target[0], target[1], rows


def nearest_integer(value):
    if value >= 0:
        return int(mp.floor(value + mp.mpf("0.5")))
    return -int(mp.floor(-value + mp.mpf("0.5")))


def four_colour(vertex_count, edges):
    with Solver(name="cadical153") as solver:
        for vertex in range(vertex_count):
            solver.add_clause([4 * vertex + colour + 1 for colour in range(4)])
        for left, right in edges:
            for colour in range(4):
                solver.add_clause(
                    [-4 * left - colour - 1, -4 * right - colour - 1]
                )
        if not solver.solve():
            raise RuntimeError("unexpected four-colour UNSAT")
        model = set(solver.get_model())
    word = tuple(
        next(colour for colour in range(4)
             if 4 * vertex + colour + 1 in model)
        for vertex in range(vertex_count)
    )
    assert all(word[a] != word[b] for a, b in edges)
    return "".join(map(str, word))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", type=Path,
                        default=HERE / "certificate.json")
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)

    mp.mp.dps = 180
    def norm(pair):
        a, b = pair
        return a * a + a * b + b * b

    def mul(left, right):
        a, b = left
        c, d = right
        return a * c - b * d, a * d + b * c + b * d

    def equations(x, y, u, v):
        z = (x, y)
        w = (u, v)
        one = (mp.mpf(1), mp.mpf(0))
        rho = (mp.mpf(0), mp.mpf(1))
        p2 = mul((mp.mpf(1), mp.mpf(-1)), z)
        q = tuple(a - b for a, b in zip(mul((mp.mpf(1), mp.mpf(1)), w), rho))
        return (
            norm(z) - 1,
            norm((u - 1, v)) - 1,
            norm((u - x, v - y)) - 3,
            norm(tuple(a - b for a, b in zip(q, p2))) - 1,
        )

    initial = tuple(map(mp.mpf, (
        "-0.85700264790477040343114695914305277253641975921354",
        "1.09869521090836087270261614929513351014040182834790",
        "0.90085117372248520325522227528981281659948260353611",
        "1.04588115942016414367045763470965566988737076131727",
    )))
    root = mp.findroot(equations, initial,
                       tol=mp.mpf("1e-160"), verify=True, maxsteps=100)
    if max(abs(value) for value in equations(*root)) > mp.mpf("1e-150"):
        raise RuntimeError("source residual")
    jacobian = mp.matrix(4, 4)
    for row in range(4):
        for column in range(4):
            def one_variable(value, row=row, column=column):
                trial = list(root)
                trial[column] = value
                return equations(*trial)[row]
            jacobian[row, column] = mp.diff(one_variable, root[column])
    inverse = jacobian ** -1

    midpoint_denominator = 10**90
    inverse_denominator = 10**65
    radius_denominator = 10**35
    points, edges, rows = closure_graph(8)
    certificate = {
        "schema": "ud93-maximal-capped-equilateral-closure-v1",
        "provenance": {
            "repository": "https://github.com/Parcly-Taxel/Shibuya",
            "commit": "218097c9971db2b60ab94a0b8dae20d76741cc43",
            "source_path": "shibuya/graphs/pegg.py",
        },
        "midpoint_denominator": midpoint_denominator,
        "midpoint_numerators": [
            nearest_integer(value * midpoint_denominator) for value in root
        ],
        "inverse_denominator": inverse_denominator,
        "inverse_numerators": [
            [nearest_integer(inverse[i, j] * inverse_denominator)
             for j in range(4)]
            for i in range(4)
        ],
        "radius_denominator": radius_denominator,
        "source_parameter_approximation":
            "1.88352388367344957721527779410884306903392824098114780948504063332870842503693535289648306381005851",
        "round_vertex_edge_counts": [list(row) for row in rows],
        "completed_round": 8,
        "four_colour_word": four_colour(len(points), edges),
    }
    args.output.write_text(json.dumps(certificate, separators=(",", ":")) + "\n")
    print(json.dumps({
        "output": str(args.output),
        "bytes": args.output.stat().st_size,
        "rounds": rows,
        "word_length": len(certificate["four_colour_word"]),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
