#!/usr/bin/env python3
"""Independent exact audit of the odd-valuation projection theorem.

The reviewed package is never imported.  Exact base-field arithmetic is
loaded from the already accepted independent review of the three-Moser
collision theorem and pinned by digest.  The A159 coordinate file is data.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
from itertools import product
import json
from math import lcm
from pathlib import Path

ARITHMETIC_SHA256 = "b9a8dcb5cd672318614916345222230e675a34eddede4a190a3d3ff0f6b28fd4"
POINTS_SHA256 = "4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02"


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def digest(value) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def load_arithmetic(path: Path):
    need(file_sha(path) == ARITHMETIC_SHA256, "independent arithmetic digest")
    spec = importlib.util.spec_from_file_location("accepted_independent_arithmetic", path)
    need(spec is not None and spec.loader is not None, "cannot load arithmetic")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def e_from_flat(A, values):
    a, b, c, d = map(F, values)
    return ((a, b), (c, d / 3))


def xadd(A, left, right):
    return (A.ea(left[0], right[0]), A.ea(left[1], right[1]))


def xsub(A, left, right):
    return (A.es(left[0], right[0]), A.es(left[1], right[1]))


def xneg(A, value):
    return (A.ec(value[0], -1), A.ec(value[1], -1))


def xinverse(A, value, D):
    denominator = A.es(A.em(value[0], value[0]), A.em((D, A.Q0), A.em(value[1], value[1])))
    inverse = A.ei(denominator)
    return (A.em(value[0], inverse), A.ec(A.em(value[1], inverse), -1))


def q_digit_zero(A, value, sign):
    """Coefficient of 2^0 after the selected Q(sqrt(33))->Q_2 embedding."""
    need(sign in (-1, 1), "embedding sign")
    denominator = lcm(value[0].denominator, value[1].denominator)
    left, right = int(value[0] * denominator), int(value[1] * denominator)
    exponent = (denominator & -denominator).bit_length() - 1
    bits = max(3, exponent + 1)
    modulus = 1 << bits
    root = sign * A.root33(bits)
    numerator = (left + right * root) * pow(denominator >> exponent, -1, modulus)
    return ((numerator % modulus) >> exponent) & 1


def color_e(A, value, sign=1):
    """Two zeroth digits in the basis omega=(-1+alpha)/2."""
    x, y = value
    first = A.qa(x, y)
    second = A.qc(y, 2)
    return q_digit_zero(A, first, sign) + 2 * q_digit_zero(A, second, sign)


def color_x(A, value, sign=1):
    return color_e(A, value[0], sign)


def qvaluation(A, value, sign=1):
    need(value != A.Q0 and sign in (-1, 1), "valuation input")
    return A.q2_data((value[0], sign * value[1]))[0]


def local_square(A, value, sign):
    transformed = (value[0], sign * value[1])
    valuation, odd_unit = A.q2_data(transformed, 3)
    return valuation % 2 == 0 and odd_unit == 1


def source_points(A, path: Path):
    need(file_sha(path) == POINTS_SHA256, "A159 coordinate digest")
    points = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        need(len(row) == 16, "bad A159 row")
        need(all(row[index] == 0 for index in range(16) if index not in (0, 5, 9, 12)),
             "A159 point outside E")
        points.append(e_from_flat(A, (F(row[index], 12) for index in (0, 5, 9, 12))))
    need(len(points) == len(set(points)) == 159 and points[0] == A.E0, "A159 census")
    return points


def rt_mul(A, left, right, D):
    """Multiply in Q(sqrt(33))[t]/(t^2-D), independently of E arithmetic."""
    return (
        A.qa(A.qm(left[0], right[0]), A.qm(D, A.qm(left[1], right[1]))),
        A.qa(A.qm(left[0], right[1]), A.qm(left[1], right[0])),
    )


def cartesian_unit(A, value, D):
    z0, z1 = value
    real_coordinate = (z0[0], z1[0])
    imag_over_sqrt3 = (z0[1], z1[1])
    real_square = rt_mul(A, real_coordinate, real_coordinate, D)
    imag_square = rt_mul(A, imag_over_sqrt3, imag_over_sqrt3, D)
    total = (A.qa(real_square[0], A.qc(imag_square[0], 3)),
             A.qa(real_square[1], A.qc(imag_square[1], 3)))
    return total == (A.Q1, A.Q0)


def build_physical(A, source):
    D = (F(330), F(-42))
    u = (
        e_from_flat(A, (F(-3, 32), F(3, 32), F(-1, 32), F(3, 32))),
        e_from_flat(A, (F(-1, 64), F(-1, 192), F(1, 64), F(1, 64))),
    )
    T = e_from_flat(A, (F(-3, 16), F(3, 16), F(-1, 16), F(3, 16)))
    V = e_from_flat(A, (F(1, 2), 0, F(1, 2), 0))
    need(A.xmul(u, A.xconj(u), D) == (A.E1, A.E0), "named phase is not unit")
    u2 = A.xmul(u, u, D)
    Tu = A.xm_e(u, T)
    need((A.ea(A.es(u2[0], Tu[0]), V), A.es(u2[1], Tu[1])) == (A.E0, A.E0),
         "named quadratic identity")

    base = [(point, A.E0) for point in source]
    base.extend(A.xm_e(u, point) for point in source[1:])
    need(len(base) == len(set(base)) == 317, "base collision census")
    source_edges = [(i, j) for i in range(159) for j in range(i + 1, 159)
                    if A.enorm(A.es(source[i], source[j])) == A.Q1]
    cross_bridges = []
    # The 29 edges from the shared origin to uA reproduce source edges and are
    # not bridges between two nonzero endpoints.  The placement theorem uses
    # precisely the latter class, matching the target's 0 < left filter.
    for i in range(1, 159):
        for j in range(1, 159):
            difference = xsub(A, base[i], base[158 + j])
            if A.xmul(difference, A.xconj(difference), D) == (A.E1, A.E0):
                cross_bridges.append((i, j))
    need(len(source_edges) == 646 and len(cross_bridges) == 16,
         f"source-edge or bridge census: {len(source_edges)}, {len(cross_bridges)}")
    need(all(i != 0 and j != 0 for i, j in cross_bridges),
         "bridge endpoint needed by overlap proof is zero")
    target_edge = xsub(A, base[158 + 113], base[18])
    source_edge = A.econj(A.es(source[28], source[13]))
    need(A.enorm(source_edge) == A.Q1, "selected source pair is not an edge")
    need(A.xmul(target_edge, A.xconj(target_edge), D) == (A.E1, A.E0),
         "selected bridge is not an edge")
    third = [
        xadd(A, base[18], A.xm_e(target_edge, A.em(source_edge, A.es(point, source[13]))))
        for point in source
    ]
    need(len(third) == len(set(third)) == 159, "third copy collision")
    need(set(base) & set(third) == {base[18], base[158 + 113]}, "unexpected overlap")
    points = list(dict.fromkeys(base + third))
    need(len(points) == 474, "physical support size")
    return D, points, source_edges, cross_bridges


def physical_census(A, source):
    D, points, source_edges, cross_bridges = build_physical(A, source)
    values = [coefficient for point in points for part in point for coefficient in A.flat(part)]
    denominator = lcm(*(value.denominator for value in values))
    integer_points = [tuple(int(value * denominator) for part in point for value in A.flat(part))
                      for point in points]
    point_bytes = ("\n".join(" ".join(map(str, row)) for row in integer_points) + "\n").encode()
    colors = [color_x(A, point, 1) for point in points]
    edges = []
    metric_agreements = 0
    for high, point in enumerate(points):
        for low, other in enumerate(points[:high]):
            difference = xsub(A, point, other)
            field_metric = A.xmul(difference, A.xconj(difference), D) == (A.E1, A.E0)
            direct_metric = cartesian_unit(A, difference, D)
            need(field_metric == direct_metric, "physical metric disagreement")
            metric_agreements += 1
            if field_metric:
                edges.append((low, high))
    need(all(colors[left] != colors[right] for left, right in edges),
         "projection word has a monochromatic unit edge")
    base_edges = [(left, right) for left, right in edges if right < 317]
    cross_edges = sorted((left, right - 158) for left, right in base_edges
                         if 0 < left < 159 <= right)
    edge_bytes = ("\n".join(f"{left} {right}" for left, right in edges) + "\n").encode()
    word = "".join(map(str, colors))
    return {
        "vertices": len(points),
        "edges": len(edges),
        "pair_checks": len(points) * (len(points) - 1) // 2,
        "independent_metric_agreements": metric_agreements,
        "denominator": denominator,
        "max_coefficient": max(abs(value) for row in integer_points for value in row),
        "base_vertices": 317,
        "base_edges": len(base_edges),
        "source_edges": len(source_edges),
        "base_cross_edges": len(cross_bridges),
        "covered_raw_oriented_chiral_placements": len(cross_bridges) * len(source_edges) * 4,
        "cross_edges": [list(edge) for edge in cross_edges],
        "point_sha256": sha256(point_bytes).hexdigest(),
        "edge_sha256": sha256(edge_bytes).hexdigest(),
        "word_sha256": sha256(word.encode()).hexdigest(),
        "D_valuation_plus": qvaluation(A, D, 1),
    }


def theorem_controls(A):
    cases = [
        ((F(6), F(0)), 1),
        ((F(2), F(0)), 1),
        ((F(18), F(0)), 1),
        ((F(1, 2), F(0)), 1),
        ((F(330), F(-42)), 1),
        ((F(330), F(42)), -1),
    ]
    expected_valuations = [1, 1, 1, -1, 7, 7]
    shifts = [
        (A.E0, A.E0),
        (e_from_flat(A, (F(1, 8), F(1, 16), F(-3, 32), F(5, 64))),
         e_from_flat(A, (F(1, 2), F(-1, 4), F(1, 8), F(-1, 16)))),
        (e_from_flat(A, (F(-7, 256), F(13, 128), F(5, 32), F(-3, 16))),
         e_from_flat(A, (F(5, 64), F(3, 16), F(-1, 4), F(3, 2)))),
    ]
    unit_vectors = translated_checks = nonzero_radical = 0
    valuations = []
    norm_projection_checks = 0
    for (D, sign), expected in zip(cases, expected_valuations):
        valuation = qvaluation(A, D, sign)
        need(valuation == expected and valuation % 2, "control radicand valuation")
        valuations.append(valuation)
        made = 0
        candidate = 0
        while made < 75:
            candidate += 1
            den = (1, 2, 4, 8)[candidate % 4]
            x = e_from_flat(A, (F(candidate % 7 - 3, den), F(candidate % 5 - 2, den),
                                F(candidate % 11 - 5, den), F(candidate % 13 - 6, den)))
            y = e_from_flat(A, (F(candidate % 3 - 1, den), F(candidate % 17 - 8, 2 * den),
                                F(candidate % 19 - 9, den), F(candidate % 23 - 11, 2 * den)))
            q = (x, y)
            conjugate = A.xconj(q)
            try:
                unit = A.xmul(q, xinverse(A, conjugate, D), D)
            except (ZeroDivisionError, ValueError):
                continue
            need(A.xmul(unit, A.xconj(unit), D) == (A.E1, A.E0), "Hilbert-90 unit")
            projected_norm = A.enorm(unit[0])
            radical_norm = A.enorm(unit[1])
            need(A.qa(projected_norm, A.qm(D, radical_norm)) == A.Q1,
                 "constant coefficient of unit norm")
            need(qvaluation(A, projected_norm, sign) == 0, "projection norm valuation")
            norm_projection_checks += 1
            for shift in shifts:
                need(color_x(A, shift, sign) != color_x(A, xadd(A, shift, unit), sign),
                     "translated unit edge is monochromatic")
                translated_checks += 1
            unit_vectors += 1
            nonzero_radical += unit[1] != A.E0
            made += 1

    # D=5 has even valuation and the unguarded projection rule fails.
    D5 = (F(5), F(0))
    bad = (e_from_flat(A, (F(7, 8), 0, 0, 0)),
           e_from_flat(A, (0, 0, F(1, 8), 0)))
    need(A.xmul(bad, A.xconj(bad), D5) == (A.E1, A.E0), "D=5 counterexample norm")
    need(color_x(A, bad) == color_x(A, (A.E0, A.E0)), "D=5 projection counterexample")
    need(qvaluation(A, (F(1 << 601), F(0))) == 601, "large positive valuation")
    need(qvaluation(A, (F(1, 1 << 601), F(0))) == -601, "large negative valuation")
    return {
        "fields": len(cases),
        "valuations": valuations,
        "unit_vectors": unit_vectors,
        "nonzero_radical_vectors": nonzero_radical,
        "translated_colour_checks": translated_checks,
        "norm_projection_checks": norm_projection_checks,
        "D5_projection_counterexample": True,
        "extreme_valuations": [601, -601],
    }


def frontier_census(A, source):
    norms = [A.enorm(point) for point in source]
    inverses = [None] + [A.ei(A.econj(point)) for point in source[1:]]
    groups = defaultdict(list)
    direction_counts = Counter()
    for i in range(1, 159):
        for j in range(1, 159):
            S = A.qs(A.qa(norms[i], norms[j]), A.Q1)
            delta = A.qs(A.qc(A.qm(norms[i], norms[j]), 4), A.qm(S, S))
            if A.qsign(delta) < 0:
                direction_counts["no_unit_roots"] += 1
                continue
            radicand = A.qc(delta, F(1, 3))
            if A.qsqrt(radicand) is not None:
                direction_counts["roots_in_E"] += 1
                continue
            need(A.qsign(delta) > 0, "unhandled double root")
            invc = A.em(inverses[i], A.ei(source[j]))
            T = A.em((S, A.Q0), invc)
            V = A.em(A.em(source[i], A.econj(source[j])), invc)
            groups[(T, V)].append((i, j))
            direction_counts["outside_E_pairs"] += 1
    need(len(groups) == 1490, "origin-pencil class census")

    rows = []
    new_by_radicand = Counter()
    odd_total = prior_total = additional = 0
    remaining = []
    for (T, V), directions in groups.items():
        i, j = directions[0]
        S = A.qs(A.qa(norms[i], norms[j]), A.Q1)
        radicand = A.qc(A.qs(A.qc(A.qm(norms[i], norms[j]), 4), A.qm(S, S)), F(1, 3))
        vp, vm = qvaluation(A, radicand, 1), qvaluation(A, radicand, -1)
        square_plus = local_square(A, radicand, 1)
        square_minus = local_square(A, radicand, -1)
        prior = square_plus or square_minus
        odd = bool(vp % 2 or vm % 2)
        odd_total += odd
        prior_total += prior
        if odd and not prior:
            additional += 1
            new_by_radicand[radicand] += 1
        if not odd and not prior:
            remaining.append((radicand, len(directions)))
        rows.append({
            "trace": A.ser_e(T),
            "norm": A.ser_e(V),
            "edges": len(directions),
            "D": [str(value) for value in radicand],
            "valuation_plus": vp,
            "valuation_minus": vm,
            "embeds_plus": square_plus,
            "embeds_minus": square_minus,
        })

    expected_new = [
        ((F(32, 27), F(0)), 42),
        ((F(55, 54), F(-7, 54)), 50),
        ((F(55, 54), F(7, 54)), 30),
        ((F(40, 81), F(8, 81)), 24),
    ]
    additional_fields = []
    additional_covered = 0
    for representative, wanted_count in expected_new:
        count = sum(multiplicity for radicand, multiplicity in new_by_radicand.items()
                    if A.qsqrt(A.qm(radicand, A.qi(representative))) is not None)
        need(count == wanted_count, "additional square-class distribution")
        additional_covered += count
        additional_fields.append({"D": [str(value) for value in representative],
                                  "classes": count})
    need(additional_covered == additional, "additional square-class coverage")
    representatives = [
        ((F(13, 9), F(0)), 36, 10),
        ((F(101, 162), F(-11, 162)), 24, 8),
        ((F(101, 162), F(11, 162)), 24, 8),
    ]
    unresolved_fields = []
    covered = 0
    for representative, wanted_count, wanted_max in representatives:
        members = [edges for radicand, edges in remaining
                   if A.qsqrt(A.qm(radicand, A.qi(representative))) is not None]
        need((len(members), max(members)) == (wanted_count, wanted_max),
             "unresolved square-class census")
        covered += len(members)
        unresolved_fields.append({
            "D": [str(value) for value in representative],
            "classes": len(members),
            "max_edges": max(members),
        })
    need((prior_total, odd_total, additional, len(remaining), covered) == (1260, 218, 146, 84, 84),
         "frontier filter census")
    rows.sort(key=lambda row: (row["trace"], row["norm"], row["D"], row["edges"]))
    return {
        "classes": len(groups),
        "direction_counts": dict(direction_counts),
        "previous_square_embedding_exclusions": prior_total,
        "odd_valuation_classes": odd_total,
        "additional_projection_exclusions": additional,
        "total_whole_field_exclusions": len(groups) - len(remaining),
        "unresolved_classes": len(remaining),
        "unresolved_fields": unresolved_fields,
        "remaining_max_contacts": max(edges for _, edges in remaining),
        "additional_fields": additional_fields,
        "complete_class_inventory_sha256": digest(rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arithmetic", type=Path, required=True)
    parser.add_argument("--points", type=Path, required=True)
    parser.add_argument("--target-expected", type=Path, required=True)
    args = parser.parse_args()
    A = load_arithmetic(args.arithmetic)
    source = source_points(A, args.points)
    target = json.loads(args.target_expected.read_text())

    physical = physical_census(A, source)
    for key in ("vertices", "edges", "pair_checks", "denominator", "max_coefficient",
                "base_vertices", "base_edges", "cross_edges", "point_sha256", "edge_sha256",
                "word_sha256", "D_valuation_plus"):
        need(physical[key] == target["physical"][key], f"physical target mismatch: {key}")
    controls = theorem_controls(A)
    frontier = frontier_census(A, source)
    for key in ("classes", "previous_square_embedding_exclusions", "odd_valuation_classes",
                "additional_projection_exclusions", "total_whole_field_exclusions",
                "unresolved_classes", "unresolved_fields", "remaining_max_contacts"):
        need(frontier[key] == target["frontier"][key], f"frontier target mismatch: {key}")

    result = {
        "status": "PASS",
        "imports_target_code": False,
        "independent_arithmetic_sha256": file_sha(args.arithmetic),
        "source_points_sha256": file_sha(args.points),
        "physical": physical,
        "theorem_controls": controls,
        "frontier": frontier,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
