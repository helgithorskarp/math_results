#!/usr/bin/env python3
"""Clean-room exact audit of the homogeneous four-power A5 pencil result.

This checker deliberately does not import the target package.  It rebuilds the
finite geometry, reverses the elimination coordinate, and reconstructs every
physical graph from label differences over exact quotient fields.
"""
import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
from functools import reduce
from itertools import combinations, product
from math import gcd
import hashlib
import json
from pathlib import Path

import sympy as sp
from flint import fmpq, fmpq_poly


T = ((0, 0), (1, 0), (0, 1))
UNITS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
DIGIT_DIFFERENCES = ((0, 0),) + UNITS
LABELS = tuple(product(range(3), repeat=5))
GF4_MUL = (
    (0, 0, 0, 0),
    (0, 1, 2, 3),
    (0, 2, 3, 1),
    (0, 3, 1, 2),
)
CIRCLE = ((0, 0, -1), (0, 2, 3), (2, 0, 1))
SCHEMA = "hn-four-power-no-binomial-pencils-v1"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def e_mul(left, right):
    """Multiply a+b*omega with omega^2=omega-1."""
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c + b * d


def canonical_row(row):
    return min(tuple(e_mul(unit, value) for value in row) for unit in UNITS)


def p_add(left, right, scale=1):
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, 0) + scale * coefficient
    return {m: c for m, c in out.items() if c}


def p_mul(left, right):
    out = {}
    for (i, j), a in left.items():
        for (k, ell), b in right.items():
            key = (i + k, j + ell)
            out[key] = out.get(key, 0) + a * b
    return {m: c for m, c in out.items() if c}


def p_scale(poly, scale):
    return {m: scale * c for m, c in poly.items() if scale * c}


def sparse_primitive(poly):
    poly = {m: c for m, c in poly.items() if c}
    if not poly:
        return ()
    content = reduce(gcd, poly.values(), 0)
    if poly[max(poly)] < 0:
        content = -content
    return tuple((i, j, c // content) for (i, j), c in sorted(poly.items()))


def norm_event(row):
    """Expand |sum row[k] z^k|^2-1 after clearing the factor 1/4."""
    one, zero = {(0, 0): 1}, {}
    powers = []
    real, imag = one, zero
    for _ in range(5):
        powers.append((real, imag))
        real, imag = (
            p_add(p_mul(real, {(1, 0): 1}), p_mul(imag, {(0, 1): 1}), -3),
            p_add(p_mul(real, {(0, 1): 1}), p_mul(imag, {(1, 0): 1})),
        )
    a_part, b_part = {}, {}
    for (a, b), (real, imag) in zip(row, powers):
        a_part = p_add(a_part, p_add(p_scale(real, 2 * a + b), p_scale(imag, -3 * b)))
        b_part = p_add(b_part, p_add(p_scale(real, b), p_scale(imag, 2 * a + b)))
    squared = p_add(p_mul(a_part, a_part), p_mul(b_part, b_part), 3)
    return sparse_primitive(p_add(squared, {(0, 0): 4}, -1))


def build_geometry():
    rows = tuple(sorted({
        canonical_row(row)
        for row in product(DIGIT_DIFFERENCES, repeat=5)
        if any(value != (0, 0) for value in row)
    }))
    need(len(rows) == 2801, "canonical displacement-row count")
    row_id = {row: index for index, row in enumerate(rows)}
    row_edges = [[] for _ in rows]
    for upper, left in enumerate(LABELS):
        for lower in range(upper):
            right = LABELS[lower]
            row = canonical_row(tuple(
                (T[a][0] - T[b][0], T[a][1] - T[b][1])
                for a, b in zip(left, right)
            ))
            row_edges[row_id[row]].append((lower, upper))
    need(sum(map(len, row_edges)) == 29403 and all(row_edges), "label-pair partition")

    events = []
    for row in rows:
        support = [k for k, value in enumerate(row) if value != (0, 0)]
        if len(support) == 1:
            events.append(() if support[0] == 0 else CIRCLE)
        else:
            events.append(norm_event(row))
    factors = tuple(sorted(set(events) - {()}))
    need(len(factors) == 2797, "active curve count")
    factor_id = {factor: index for index, factor in enumerate(factors)}
    factor_edges = [[] for _ in factors]
    universal_edges = []
    for event, edges in zip(events, row_edges):
        if event:
            factor_edges[factor_id[event]].extend(edges)
        else:
            universal_edges.extend(edges)
    need(len(universal_edges) == 243, "universal unit-edge count")
    return rows, events, factors, factor_edges, sorted(universal_edges)


def gf4_normalize(vector):
    pivot = next(value for value in vector if value)
    inverse = next(value for value in (1, 2, 3) if GF4_MUL[value][pivot] == 1)
    return tuple(GF4_MUL[inverse][value] for value in vector)


def gf4_affine(row, constant):
    pivot = next(value for value in row if value)
    inverse = next(value for value in (1, 2, 3) if GF4_MUL[value][pivot] == 1)
    return gf4_normalize(row), GF4_MUL[inverse][constant]


def gf4_add_scaled(left, right, a, b):
    return tuple(GF4_MUL[a][u] ^ GF4_MUL[b][v] for u, v in zip(left, right))


def classify_pencils(pencil_path, rows, events, factors):
    directions = sorted({
        gf4_normalize(vector)
        for vector in product(range(4), repeat=4)
        if any(vector)
    })
    need(len(directions) == 85, "PG(3,4) direction count")
    spaces = set()
    for left, right in combinations(directions, 2):
        span = tuple(sorted({
            gf4_normalize(gf4_add_scaled(left, right, a, b))
            for a, b in product(range(4), repeat=2)
            if a or b
        }))
        if len(span) == 5:
            spaces.add(span)
    need(len(spaces) == 357, "Grassmannian row-space count")
    selected = sorted(
        tuple((direction, 0) for direction in space)
        for space in spaces
        if min(sum(bool(value) for value in direction) for direction in space) >= 3
    )
    need(len(selected) == 54, "no-monomial/no-binomial pencil count")
    need(all(sorted(sum(bool(v) for v in row) for row, _ in pencil) == [3, 3, 3, 3, 4]
             for pencil in selected), "selected support profile")

    supplied_raw = json.loads(pencil_path.read_text())
    supplied = [tuple((tuple(row), constant) for row, constant in pencil)
                for _, pencil in supplied_raw]
    need(len(set(supplied)) == len(supplied) == 54 and sorted(supplied) == selected,
         "literal pencil list equals independent classification")

    lookup = {factor: index for index, factor in enumerate(factors)}
    buckets = {}
    for row, event in zip(rows, events):
        if not event or sum(value != (0, 0) for value in row) == 1:
            continue
        residue = lambda value: (value[0] % 2) + 2 * (value[1] % 2)
        normal = tuple(residue(value) for value in row[1:])
        constant = residue(row[0])
        signature = gf4_affine(normal, constant)
        buckets.setdefault(signature, []).append(lookup[event])
    for signature in buckets:
        buckets[signature].sort()
    need(len(buckets) == 336, "nonradial affine signature count")

    selected_records, all_pairs = [], set()
    for (residual_index, _), pencil in zip(supplied_raw, supplied):
        domains = sorted((buckets[signature] for signature in pencil), key=lambda d: (len(d), d))
        need(sorted(map(len, domains)) == [4, 4, 4, 4, 8], "unit-lift bucket profile")
        pairs = sorted({tuple(sorted(pair)) for pair in product(*domains[:2])})
        all_pairs.update(pairs)
        selected_records.append((residual_index, domains, pairs))
    all_pairs = sorted(all_pairs)
    need(len(all_pairs) == 864, "anchor envelope")
    return selected, selected_records, all_pairs, buckets


def expression(sparse, x, y):
    return sum(coefficient * x**i * y**j for i, j, coefficient in sparse)


def primitive_univariate(poly, variable):
    poly = sp.Poly(poly, variable, domain=sp.QQ)
    _, poly = poly.clear_denoms(convert=True)
    _, poly = poly.primitive()
    if poly.LC() < 0:
        poly = -poly
    return sp.Poly(poly, variable, domain=sp.QQ)


def sympy_coefficients(poly):
    return [str(poly.nth(k)) for k in range(poly.degree() + 1)]


def flint_poly(values):
    return fmpq_poly([fmpq(str(value)) for value in values])


def outer_trim(poly):
    while poly and not poly[-1]:
        poly.pop()
    return poly


def quotient_inverse(value, modulus):
    common, coefficient, _ = value.xgcd(modulus)
    need(common.degree() == 0, "irreducible quotient inverse")
    return (coefficient / common[0]) % modulus


def outer_gcd(left, right, modulus):
    left, right = outer_trim(left), outer_trim(right)
    while right:
        inverse = quotient_inverse(right[-1], modulus)
        while left and len(left) >= len(right):
            shift = len(left) - len(right)
            scale = left[-1] * inverse % modulus
            for k, coefficient in enumerate(right):
                left[k + shift] = (left[k + shift] - scale * coefficient) % modulus
            outer_trim(left)
        left, right = right, left
    if left:
        inverse = quotient_inverse(left[-1], modulus)
        left = [coefficient * inverse % modulus for coefficient in left]
    return left


def x_fibre(sparse, modulus):
    output = [fmpq_poly([]) for _ in range(1 + max(i for i, _, _ in sparse))]
    for i, j, coefficient in sparse:
        output[i] += fmpq_poly([0] * j + [coefficient])
    return [coefficient % modulus for coefficient in output]


def flint_coefficients(poly):
    return [str(value) for value in poly.coeffs()]


def reverse_components(pair_factors):
    """Eliminate x (the target routes both eliminate y), then use fibre gcds."""
    left, right = pair_factors
    x, y = sp.symbols("x y")
    f, g = expression(left, x, y), expression(right, x, y)
    resultant = sp.Poly(sp.resultant(f, g, x), y, domain=sp.QQ)
    need(not resultant.is_zero, "nonzero reverse resultant")
    output = []
    for factor, _ in sp.factor_list(resultant)[1]:
        qy = primitive_univariate(factor, y)
        modulus = flint_poly(sympy_coefficients(qy))
        common = outer_gcd(x_fibre(left, modulus), x_fibre(right, modulus), modulus)
        need(common, "unsupported common horizontal component")
        if len(common) == 1:
            continue
        if qy.degree() > 1:
            need(len(common) == 2 and common[1] == fmpq_poly([1]),
                 "reverse nonlinear fibre is not linear in x")
            output.append({
                "q": sympy_coefficients(qy),
                "x": flint_coefficients((-common[0]) % modulus),
                "y": ["0", "1"],
                "generator": "y",
            })
            continue
        y0 = -qy.nth(0) / qy.nth(1)
        hx = sp.Poly(sum(sp.Rational(str(coefficient[0])) * x**k
                         for k, coefficient in enumerate(common)), x, domain=sp.QQ)
        for xfactor, _ in sp.factor_list(hx)[1]:
            qx = primitive_univariate(xfactor, x)
            if qx.degree() == 1:
                x0 = -qx.nth(0) / qx.nth(1)
                output.append({
                    "q": ["0", "1"], "x": [str(x0)], "y": [str(y0)],
                    "generator": "constant",
                })
            else:
                output.append({
                    "q": sympy_coefficients(qx), "x": ["0", "1"],
                    "y": [str(y0)], "generator": "x",
                })
    output.sort(key=digest)
    return output


def evaluate_univariate(values, element, modulus):
    result = fmpq_poly([])
    for value in reversed(values):
        result = (result * element + fmpq_poly([fmpq(str(value))])) % modulus
    return result


def target_field(record):
    return tuple(flint_poly(record[name]) for name in ("q", "x", "y"))


def reverse_matches_target(reverse, target):
    modulus, x_value, y_value = target_field(target)
    if len(reverse["q"]) - 1 != len(target["q"]) - 1:
        return False
    if reverse["generator"] == "constant":
        generator = fmpq_poly([])
    elif reverse["generator"] == "x":
        generator = x_value
    else:
        generator = y_value
    zero = fmpq_poly([])
    return (
        evaluate_univariate(reverse["q"], generator, modulus) == zero
        and evaluate_univariate(reverse["x"], generator, modulus) == x_value
        and evaluate_univariate(reverse["y"], generator, modulus) == y_value
    )


def fraction_trim(poly):
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def fraction_remainder(left, right):
    left = list(left)
    fraction_trim(left)
    while len(left) >= len(right):
        scale = left[-1] / right[-1]
        shift = len(left) - len(right)
        for k, coefficient in enumerate(right):
            left[k + shift] -= scale * coefficient
        fraction_trim(left)
    return left


def sturm_real_roots(values):
    """Count distinct real roots by a standard-library exact Sturm chain."""
    poly = fraction_trim([Fraction(value) for value in values])
    derivative = [Fraction(k) * poly[k] for k in range(1, len(poly))]
    chain = [poly, fraction_trim(derivative)]
    while chain[-1]:
        remainder = fraction_remainder(chain[-2], chain[-1])
        chain.append([-value for value in remainder])
    chain.pop()
    need(chain and len(chain[-1]) == 1, "certificate component polynomial is squarefree")

    def variations(positive):
        signs = []
        for member in chain:
            sign = 1 if member[-1] > 0 else -1
            if not positive and (len(member) - 1) % 2:
                sign = -sign
            signs.append(sign)
        return sum(a != b for a, b in zip(signs, signs[1:]))

    return variations(False) - variations(True)


def sparse_evaluator(record):
    modulus, x_value, y_value = target_field(record)
    zero, one = fmpq_poly([]), fmpq_poly([1])
    x_powers, y_powers = [one], [one]
    for _ in range(8):
        x_powers.append(x_powers[-1] * x_value % modulus)
        y_powers.append(y_powers[-1] * y_value % modulus)

    def vanishes(sparse):
        total = zero
        for i, j, coefficient in sparse:
            total += coefficient * (x_powers[i] * y_powers[j] % modulus)
        return total % modulus == zero

    return vanishes


def quotient_coordinates(record):
    modulus, x_value, y_value = target_field(record)
    zero, one = fmpq_poly([]), fmpq_poly([1])

    def c_add(left, right):
        return left[0] + right[0], left[1] + right[1]

    def c_mul(left, right):
        return ((left[0] * right[0] - 3 * left[1] * right[1]) % modulus,
                (left[0] * right[1] + left[1] * right[0]) % modulus)

    powers = [(one, zero)]
    for _ in range(4):
        powers.append(c_mul(powers[-1], (x_value, y_value)))
    half = fmpq_poly([fmpq(1, 2)])
    digits = ((zero, zero), (one, zero), (half, half))
    terms = [[c_mul(digit, power) for digit in digits] for power in powers]
    points, lookup, label_map = [], {}, []
    for label in LABELS:
        point = (zero, zero)
        for k, digit in enumerate(label):
            point = c_add(point, terms[k][digit])
        key = tuple(tuple(str(value) for value in coordinate.coeffs()) for coordinate in point)
        if key not in lookup:
            lookup[key] = len(points)
            points.append(point)
        label_map.append(lookup[key])
    return points, label_map


def physical_graph(record, active, factor_edges, universal_edges):
    points, label_map = quotient_coordinates(record)
    label_edges = list(universal_edges)
    for factor in active:
        label_edges.extend(factor_edges[factor])
    edges = sorted({tuple(sorted((label_map[a], label_map[b])))
                    for a, b in label_edges if label_map[a] != label_map[b]})
    triangle = [label_map[index] for index in (0, 81, 162)]
    need(len(set(triangle)) == 3, "universal triangle survives the collision quotient")
    need(all(tuple(sorted((a, b))) in edges for a, b in combinations(triangle, 2)),
         "universal triangle edges")
    return points, label_map, [list(edge) for edge in edges]


def check_colouring(weights, label_map, point_count, edges):
    need(len(weights) == 5 and all(type(value) is int and value in (0, 1, 2) for value in weights),
         "ternary linear-colour weights")
    word = [None] * point_count
    for label, point in zip(LABELS, label_map):
        colour = sum(weight * digit for weight, digit in zip(weights, label)) % 3
        need(word[point] is None or word[point] == colour, "colour descends through collisions")
        word[point] = colour
    need(None not in word and all(word[a] != word[b] for a, b in edges),
         "proper three-colouring of complete physical graph")
    return word


WORKER_FACTORS = None
WORKER_FACTOR_EDGES = None
WORKER_UNIVERSAL_EDGES = None


def initialize_field_workers(factors, factor_edges, universal_edges):
    global WORKER_FACTORS, WORKER_FACTOR_EDGES, WORKER_UNIVERSAL_EDGES
    WORKER_FACTORS = factors
    WORKER_FACTOR_EDGES = factor_edges
    WORKER_UNIVERSAL_EDGES = universal_edges


def audit_field(record):
    """Recheck one component; suitable for deterministic ordered pool.map."""
    key = record["key"]
    field = {name: record[name] for name in ("q", "x", "y")}
    need(key == digest(field), "component key recomputation")
    nreal = sturm_real_roots(record["q"])
    need(nreal == record["real_embeddings"], "independent Sturm real-root count")
    evaluator = sparse_evaluator(record)
    active = [index for index, factor in enumerate(WORKER_FACTORS) if evaluator(factor)]
    need(active == record["active_curves"], "complete active-curve recomputation")
    item = {"key": key, "nreal": nreal, "degree": len(record["q"]) - 1,
            "active": len(active)}
    if not nreal:
        return item

    points, label_map, edges = physical_graph(
        record, active, WORKER_FACTOR_EDGES, WORKER_UNIVERSAL_EDGES
    )
    need(len(points) == record["point_count"] and len(edges) == record["edge_count"],
         "physical graph order and size")
    need(digest(label_map) == record["label_map_sha256"], "collision quotient hash")
    need(digest(edges) == record["edge_sha256"], "complete physical unit-edge hash")
    word = check_colouring(record["colour_weights"], label_map, len(points), edges)
    corrupted = list(word)
    corrupted[edges[0][1]] = corrupted[edges[0][0]]
    need(any(corrupted[a] == corrupted[b] for a, b in edges), "colour corruption control")
    item.update({"vertices": len(points), "edges": len(edges),
                 "weights": record["colour_weights"], "unit_circle": evaluator(CIRCLE)})
    return item


def audit(certificate_path, pencil_path, jobs):
    certificate = json.loads(certificate_path.read_text())
    need(certificate["schema"] == SCHEMA, "target certificate schema")
    rows, events, factors, factor_edges, universal_edges = build_geometry()
    need(certificate["curve_inventory_sha256"] == digest(factors), "curve inventory hash")
    pencils, selected, pairs, _ = classify_pencils(pencil_path, rows, events, factors)
    need(certificate["pencil_interface_sha256"] == digest([
        [index, [[list(row), constant] for row, constant in pencil]]
        for (index, _), pencil in zip(json.loads(pencil_path.read_text()), pencils)
    ]), "pencil interface hash")
    need(len(certificate["pairs"]) == len(pairs), "anchor-pair certificate length")
    claimed_by_key = {record["key"]: record for record in certificate["components"]}
    need(len(claimed_by_key) == len(certificate["components"]) == 907, "distinct claimed components")
    claimed_pair_rows = {tuple(row["pair"]): row["components"] for row in certificate["pairs"]}
    need(list(claimed_pair_rows) == pairs, "ordered complete anchor interface")

    reverse_transcript = []
    with ProcessPoolExecutor(max_workers=jobs) as pool:
        inputs = ((factors[a], factors[b]) for a, b in pairs)
        for pair, reverse_list in zip(pairs, pool.map(reverse_components, inputs, chunksize=1)):
            claimed_keys = claimed_pair_rows[pair]
            unmatched = set(claimed_keys)
            matches = []
            for reverse in reverse_list:
                candidates = [key for key in unmatched
                              if reverse_matches_target(reverse, claimed_by_key[key])]
                need(len(candidates) == 1, "unique reverse-elimination component match")
                key = candidates[0]
                unmatched.remove(key)
                matches.append(key)
            need(not unmatched and sorted(matches) == claimed_keys,
                 "reverse resultant/fibre coverage equals claimed pair components")
            reverse_transcript.append([list(pair), sorted(matches)])

    ordered_records = [claimed_by_key[key] for key in sorted(claimed_by_key)]
    with ProcessPoolExecutor(
        max_workers=jobs,
        initializer=initialize_field_workers,
        initargs=(factors, factor_edges, universal_edges),
    ) as pool:
        results = list(pool.map(audit_field, ordered_records, chunksize=1))

    graph_histogram, active_histogram = Counter(), Counter()
    degree_histogram, weight_histogram = Counter(), Counter()
    real_components = real_parameters = 0
    for item in results:
        nreal = item["nreal"]
        if nreal:
            real_components += 1
            real_parameters += nreal
            graph_histogram[f"{item['vertices']}v_{item['edges']}e"] += nreal
            active_histogram[str(item["active"])] += nreal
            degree_histogram[str(item["degree"])] += nreal
            weight_histogram["".join(map(str, item["weights"]))] += nreal

    concurrence_rows = []
    for residual_index, domains, pencil_pairs in selected:
        for pair in pencil_pairs:
            for key in claimed_pair_rows[pair]:
                active = set(claimed_by_key[key]["active_curves"])
                sections = [[factor for factor in domain if factor in active] for domain in domains]
                need(not all(sections), "full five-section complex concurrence")
                concurrence_rows.append([residual_index, list(pair), key, sections])

    # Three deliberately false microclaims must be rejected by local predicates.
    need(sturm_real_roots([1, 0, 1]) == 0 and sturm_real_roots([-1, 0, 1]) == 2,
         "Sturm negative controls")
    result = {
        "status": "PASS",
        "independent_route": "reverse_resultant_eliminate_x_plus_exact_quotient_fibre_gcd",
        "pencils": len(pencils),
        "raw_lifts": 54 * 4 * 4 * 4 * 4 * 8,
        "anchor_pairs": len(pairs),
        "distinct_complex_components": len(claimed_by_key),
        "components_with_pair_incidence": sum(len(row["components"]) for row in certificate["pairs"]),
        "components_with_pencil_pair_incidence": len(concurrence_rows),
        "complex_concurrences": 0,
        "real_components": real_components,
        "distinct_real_parameters": real_parameters,
        "all_physical_chromatic_numbers": 3,
        "physical_graph_histogram_by_parameter": dict(sorted(graph_histogram.items())),
        "active_curve_histogram_by_parameter": dict(sorted(active_histogram.items())),
        "degree_histogram_by_parameter": dict(sorted(degree_histogram.items())),
        "linear_colour_weight_histogram_by_parameter": dict(sorted(weight_histogram.items())),
        "concurrency_transcript_sha256": digest(concurrence_rows),
        "physical_transcript_sha256": digest(results),
        "reverse_coverage_transcript_sha256": digest(reverse_transcript),
        "curve_inventory_sha256": digest(factors),
        "certificate_sha256": hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
        "negative_controls": 3,
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--pencils", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--check-expected", type=Path)
    args = parser.parse_args()
    need(1 <= args.jobs <= 8, "bounded worker count")
    result = audit(args.certificate, args.pencils, args.jobs)
    if args.check_expected:
        need(result == json.loads(args.check_expected.read_text()), "expected audit transcript")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
