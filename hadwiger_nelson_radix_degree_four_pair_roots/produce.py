#!/usr/bin/env python3
"""Exact-component certificate producer for the A5 degree-four pair stratum.

It obtains the named source pairs from a regenerated h4195 residual, decomposes
their real intersection loci exactly over Q, determines every identically
active unit-event curve, and asks SAT for proper three- and four-colourings.
Satisfying assignments are checked directly before being written.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "hadwiger_nelson_complex_radix_architecture"
sys.path.insert(0, str(ARCH))
import geometry as geo  # noqa: E402
_ARCH_SPEC = importlib.util.spec_from_file_location("hn_radix_architecture_verify", ARCH / "verify.py")
require_arch = _ARCH_SPEC is not None and _ARCH_SPEC.loader is not None
if not require_arch:
    raise ImportError("cannot load complex-radix architecture verifier")
architecture = importlib.util.module_from_spec(_ARCH_SPEC)
_ARCH_SPEC.loader.exec_module(architecture)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def expression(sparse, x, y):
    return sum(coefficient * x**i * y**j for i, j, coefficient in sparse)


def primitive_univariate(poly, variable):
    poly = sp.Poly(poly, variable, domain=sp.QQ)
    _, primitive = poly.clear_denoms(convert=True)
    _, primitive = primitive.primitive()
    if primitive.LC() < 0:
        primitive = -primitive
    return sp.Poly(primitive, variable, domain=sp.QQ)


def rational_coefficients(poly, variable):
    poly = sp.Poly(poly, variable, domain=sp.QQ)
    if poly.is_zero:
        return ("0",)
    return tuple(str(poly.nth(i)) for i in range(poly.degree() + 1))


def reduce_substitution(poly, x_value, y_value, q, x, y, s):
    sparse = [
        (i, j, int(coefficient))
        for (i, j), coefficient in sp.Poly(poly, x, y, domain=sp.QQ).terms()
    ]
    xx = sp.Poly(x_value, s, domain=sp.QQ)
    yy = sp.Poly(y_value, s, domain=sp.QQ)
    return component_evaluator(q, xx, yy, s)(sparse)


def component_evaluator(q, xx, yy, s, maximum_degree=8):
    """Return a fast exact sparse-polynomial evaluator in Q[s]/(q)."""
    from flint import fmpq, fmpq_poly

    def convert(poly):
        if poly.is_zero:
            return fmpq_poly([])
        return fmpq_poly(
            [fmpq(int(poly.nth(i).p), int(poly.nth(i).q)) for i in range(poly.degree() + 1)]
        )

    modulus = convert(q)
    x_value = convert(xx)
    y_value = convert(yy)
    one = fmpq_poly([1])
    zero = fmpq_poly([])
    x_powers = [one]
    y_powers = [one]
    for _ in range(maximum_degree):
        x_powers.append(x_powers[-1] * x_value % modulus)
        y_powers.append(y_powers[-1] * y_value % modulus)
    monomials = {
        (i, j): x_powers[i] * y_powers[j] % modulus
        for i in range(maximum_degree + 1)
        for j in range(maximum_degree + 1 - i)
    }

    def evaluate(sparse):
        return sum(
            (int(coefficient) * monomials[i, j] for i, j, coefficient in sparse),
            zero,
        ) == zero

    return evaluate


def generic_components(f, g, x, y, s):
    basis = sp.groebner([f, g], y, x, order="lex", domain=sp.QQ)
    eliminants = [p.as_expr() for p in basis.polys if p.degree(y) == 0]
    require(len(eliminants) == 1, "expected one x eliminant")
    linear = [p.as_expr() for p in basis.polys if p.degree(y) == 1]

    if linear:
        require(len(linear) == 1, "expected one linear fibre equation")
        relation = linear[0]
        a = sp.Poly(sp.diff(relation, y), x, domain=sp.QQ)
        b = sp.Poly(relation.subs(y, 0), x, domain=sp.QQ)
        components = []
        for q0, _multiplicity in sp.factor_list(sp.Poly(eliminants[0], x))[1]:
            qx = primitive_univariate(q0, x)
            q = sp.Poly(qx.as_expr().subs(x, s), s, domain=sp.QQ)
            aa = sp.Poly(a.as_expr().subs(x, s), s, domain=sp.QQ).rem(q)
            bb = sp.Poly(b.as_expr().subs(x, s), s, domain=sp.QQ).rem(q)
            require(sp.gcd(aa, q).degree() == 0, "noninvertible linear fibre")
            inverse = sp.invert(aa, q)
            yy = sp.Poly(-bb.as_expr() * inverse.as_expr(), s, domain=sp.QQ).rem(q)
            xx = sp.Poly(s, s, domain=sp.QQ)
            require(reduce_substitution(f, xx.as_expr(), yy.as_expr(), q, x, y, s), "f component check")
            require(reduce_substitution(g, xx.as_expr(), yy.as_expr(), q, x, y, s), "g component check")
            components.append((q, xx, yy))
        return components

    # The only non-shape-position cases in this stratum are vertical rational
    # fibres.  Their common y-polynomial is factored exactly.
    qx_factors = sp.factor_list(sp.Poly(eliminants[0], x))[1]
    require(len(qx_factors) == 1 and qx_factors[0][0].degree() == 1, "unsupported non-linear fibre")
    qx = qx_factors[0][0]
    x0 = -qx.nth(0) / qx.nth(1)
    fy = sp.Poly(f.subs(x, x0), y, domain=sp.QQ)
    gy = sp.Poly(g.subs(x, x0), y, domain=sp.QQ)
    common = sp.gcd(fy, gy)
    require(common.degree() > 0, "empty vertical fibre")
    components = []
    for h, _multiplicity in sp.factor_list(common)[1]:
        q = primitive_univariate(h.as_expr().subs(y, s), s)
        xx = sp.Poly(x0, s, domain=sp.QQ)
        yy = sp.Poly(s, s, domain=sp.QQ)
        require(reduce_substitution(f, xx.as_expr(), yy.as_expr(), q, x, y, s), "vertical f check")
        require(reduce_substitution(g, xx.as_expr(), yy.as_expr(), q, x, y, s), "vertical g check")
        components.append((q, xx, yy))
    return components


def collision_parts(row):
    real, imaginary = {}, {}
    for (a, b), (left, right) in zip(row, geo.POWERS):
        real = geo.add(real, geo.add(geo.scale(left, 2 * a + b), geo.scale(right, -3 * b)))
        imaginary = geo.add(imaginary, geo.add(geo.scale(left, b), geo.scale(right, 2 * a + b)))
    return geo.primitive(real), geo.primitive(imaginary)


def colouring(vertices, edges, colours):
    from pysat.solvers import Solver

    def var(vertex, colour):
        return colours * vertex + colour + 1

    clauses = []
    for vertex in range(vertices):
        clauses.append([var(vertex, colour) for colour in range(colours)])
        for a in range(colours):
            for b in range(a):
                clauses.append([-var(vertex, a), -var(vertex, b)])
    for left, right in edges:
        for colour in range(colours):
            clauses.append([-var(left, colour), -var(right, colour)])
    # The universal triangle may be pinned by a global colour permutation.
    for vertex, colour in zip((0, 81, 162), (0, 1, 2)):
        clauses.append([var(vertex, colour)])
    with Solver(name="cadical153", bootstrap_with=clauses) as solver:
        if not solver.solve():
            return None
        model = set(literal for literal in solver.get_model() if literal > 0)
    word = []
    for vertex in range(vertices):
        selected = [colour for colour in range(colours) if var(vertex, colour) in model]
        require(len(selected) == 1, "SAT model does not encode one colour")
        word.append(selected[0])
    require(all(word[left] != word[right] for left, right in edges), "invalid SAT colouring")
    return word


def component_key(q, xx, yy, s):
    return (
        rational_coefficients(q, s),
        rational_coefficients(xx.rem(q), s),
        rational_coefficients(yy.rem(q), s),
    )


def run(residual_path):
    residual = json.loads(Path(residual_path).read_text())
    require(residual["schema"] == "hn-radix-complete-pair-propagation-v1", "residual schema")
    rows, _events, factors, factor_edges, base_edges, collisions, _simple, _circle = architecture.build()
    degrees = [architecture.degree(factor) for factor in factors]
    # In this exact residual, these are equivalently the systems of Bezout
    # allowance at most 16.  Select by the invariant used in the theorem.
    pairs = [
        row for row in residual["remaining_six"]
        if 4 in (degrees[row[0]], degrees[row[1]])
    ]
    require(
        len(pairs) == 160
        and all(
            row[2] == 1
            and degrees[row[0]] * degrees[row[1]] == 2 * row[3]
            and row[3] <= 16
            for row in pairs
        ),
        "pair stratum",
    )

    x, y, s = sp.symbols("x y s")
    factor_expressions = [expression(factor, x, y) for factor in factors]
    collision_sparse = list(map(collision_parts, collisions))
    pair_components = []
    component_sources = defaultdict(list)
    component_data = {}
    complex_components = 0
    for row in pairs:
        a, b = row[:2]
        components = generic_components(factor_expressions[a], factor_expressions[b], x, y, s)
        real_for_pair = []
        for q, xx, yy in components:
            real_roots = int(q.count_roots(-sp.oo, sp.oo))
            if not real_roots:
                complex_components += 1
                continue
            key = component_key(q, xx, yy, s)
            component_sources[key].append([a, b])
            component_data[key] = (q, xx, yy, real_roots)
            real_for_pair.append(key)
        pair_components.append({"pair": [a, b], "real_component_keys": [digest(key) for key in real_for_pair]})

    results = []
    active_histogram = Counter()
    chromatic_histogram = Counter()
    for key in sorted(component_data):
        q, xx, yy, real_roots = component_data[key]
        evaluates_to_zero = component_evaluator(q, xx, yy, s)
        active = [
            index
            for index, factor in enumerate(factors)
            if evaluates_to_zero(factor)
        ]
        require(len(active) >= 2, "source curves missing")
        collision_rows = []
        for index, (real, imaginary) in enumerate(collision_sparse):
            if evaluates_to_zero(real) and evaluates_to_zero(imaginary):
                collision_rows.append(index)
        if collision_rows:
            chromatic = 3
            colour4 = None
            colour3 = None
        else:
            edges = sorted(base_edges + [edge for curve in active for edge in factor_edges[curve]])
            require(len(edges) == len(set(edges)), "edge owner overlap")
            colour3 = colouring(243, edges, 3)
            colour4 = colouring(243, edges, 4)
            require(colour4 is not None, "NON_FOUR_COLOURABLE_CANDIDATE")
            chromatic = 3 if colour3 is not None else 4
        active_histogram[(len(active), sum(len(factor_edges[curve]) for curve in active))] += real_roots
        chromatic_histogram[chromatic] += real_roots
        results.append(
            {
                "component_key": digest(key),
                "source_pairs": sorted(component_sources[key]),
                "q": list(key[0]),
                "x": list(key[1]),
                "y": list(key[2]),
                "real_embeddings": real_roots,
                "active_curves": active,
                "collision_rows": collision_rows,
                "chromatic_number_upper_bound": chromatic,
                "three_colouring": colour3,
                "four_colouring": colour4,
            }
        )
    output = {
        "schema": "hn-radix-degree-four-pair-roots-v1",
        "source_residual_sha256": digest(residual),
        "curve_inventory_sha256": architecture.digest(factors),
        "pair_count": len(pairs),
        "maximum_bezout_allowance": max(row[3] for row in pairs),
        "total_bezout_allowance": sum(row[3] for row in pairs),
        "degree_pair_histogram": {
            f"{left}_{right}": count
            for (left, right), count in sorted(
                Counter((degrees[row[0]], degrees[row[1]]) for row in pairs).items()
            )
        },
        "pair_sha256": digest(pairs),
        "pair_components": pair_components,
        "distinct_real_components": len(results),
        "complex_only_irreducible_components": complex_components,
        "real_parameter_embeddings": sum(row["real_embeddings"] for row in results),
        "active_curve_edge_histogram_by_embedding": {
            f"{curves}_curves_{edges}_event_edges": count
            for (curves, edges), count in sorted(active_histogram.items())
        },
        "chromatic_upper_bound_histogram_by_embedding": {
            str(key): value for key, value in sorted(chromatic_histogram.items())
        },
        "components": results,
    }
    output["result_sha256_without_self"] = digest(output)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--residual", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = run(args.residual)
    if args.out:
        with args.out.open("x") as handle:
            json.dump(result, handle, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
    summary = {key: value for key, value in result.items() if key != "components" and key != "pair_components"}
    print(json.dumps(summary, indent=2, sort_keys=True))
