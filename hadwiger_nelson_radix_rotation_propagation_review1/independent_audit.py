#!/usr/bin/env python3
"""Independent exact audit of Discovery Net h4193 and h4195.

The program imports only the previously reviewed h4163 displacement inventory.
It does not import either target's producer, verifier, or common module.
"""

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ROTATION = ROOT / "hadwiger_nelson_radix_rotation_pair_stratum"
PROPAGATION = ROOT / "hadwiger_nelson_radix_pair_exclusion_propagation"

CURVE_SHA = "85c286422c01bcb6ebb244186032bc607984471bc2b705ef7247084dd7c33db9"
H4193_INPUT_SHA = "8810828aa75a2d4a83cc18322d0312f58cb484b3683869eee38b63927d9246c1"
H4195_INPUT_SHA = "9da6cb1a32bbb5004b72bf2ac934dc05a44b5e2bf7705e7ec55498c3e7caabf9"
INCIDENCE_SHA = "c9cb33688915d282b9d410898eeeb22d4bd33e242b3d28b7703ca4fe2111c477"
H4195_EXPORT_SHA = "42132ed90f7696d9cf7c17e7b47588ca717bb71b633141e29412a1b55b55e97d"
PAIRS = ((318, 340, 7, 32, 10), (318, 341, 7, 32, 10),
         (319, 340, 7, 32, 10), (319, 341, 7, 32, 10))
GF4 = ((0, 0, 0, 0), (0, 1, 2, 3), (0, 2, 3, 1), (0, 3, 1, 2))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V = load_module(
    "reviewed_h4163_inventory",
    ROOT / "hadwiger_nelson_radix_four_active_closure_review1" / "independent_check.py",
)


def canonical(normal, constant):
    pivot = next(v for v in normal if v)
    inverse = next(v for v in (1, 2, 3) if GF4[v][pivot] == 1)
    return tuple(GF4[inverse][v] for v in normal), GF4[inverse][constant]


def affine_span(left, right):
    combinations = ((1, 0), (0, 1), (1, 1), (1, 2), (1, 3))
    sections = {
        canonical(
            tuple(GF4[a][u] ^ GF4[b][v] for u, v in zip(left[0], right[0])),
            GF4[a][left[1]] ^ GF4[b][right[1]],
        )
        for a, b in combinations
    }
    need(len(sections) == 5, "nonparallel signatures must span five sections")
    return tuple(sorted(sections))


def reconstruct_inventory():
    _, factors, circle, monomials, rowids = V.reconstruct_inventory()
    need(digest(factors) == CURVE_SHA, "reviewed h4163 curve inventory")
    signatures = {}
    buckets = defaultdict(list)
    for row, curve in rowids.items():
        values = tuple((a % 2) + 2 * (b % 2) for a, b in row)
        signature = canonical(values[1:], values[0])
        signatures[curve] = signature
        buckets[signature].append(curve)
    buckets = {s: tuple(sorted(cs)) for s, cs in buckets.items()}
    need(len(signatures) == 2796 and len(buckets) == 336, "complete noncircle inventory")
    return factors, circle, monomials, rowids, signatures, buckets


def all_pencils(buckets):
    """Generate pencils from pairs, unlike the target checker's RREF catalogue."""
    signatures = sorted(buckets)
    generated = {
        affine_span(s, t)
        for i, s in enumerate(signatures)
        for t in signatures[i + 1 :]
        if s[0] != t[0]
    }
    realized = sorted(p for p in generated if all(s in buckets for s in p))
    need(len(generated) == 5712 and len(realized) == 5382, "complete affine-pencil census")
    residual = []
    for pencil in realized:
        support = {i for normal, _ in pencil for i, value in enumerate(normal) if value}
        if len(support) <= 2:
            continue
        if any(normal == (1, 0, 0, 0) for normal, _ in pencil):
            continue
        residual.append(pencil)
    need(len(residual) == 5112, "h4185 residual pencil catalogue")
    return residual


# Low-first exact rational polynomial arithmetic for an independent Sturm audit.
def qtrim(poly):
    poly = [Fraction(v) for v in poly]
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def qdivmod(left, right):
    left, right = qtrim(left), qtrim(right)
    need(right, "nonzero rational divisor")
    quotient = [Fraction(0)] * max(0, len(left) - len(right) + 1)
    while len(left) >= len(right):
        shift = len(left) - len(right)
        coefficient = left[-1] / right[-1]
        quotient[shift] = coefficient
        for i, value in enumerate(right):
            left[i + shift] -= coefficient * value
        left = qtrim(left)
    return qtrim(quotient), left


def qgcd(left, right):
    left, right = qtrim(left), qtrim(right)
    while right:
        _, remainder = qdivmod(left, right)
        left, right = right, remainder
    if not left:
        return []
    return [v / left[-1] for v in left]


def qderivative(poly):
    return [i * poly[i] for i in range(1, len(poly))]


def qeval(poly, value):
    result = Fraction(0)
    for coefficient in reversed(poly):
        result = result * value + coefficient
    return result


def sign(value):
    return (value > 0) - (value < 0)


def variations(signs):
    signs = [s for s in signs if s]
    return sum(a != b for a, b in zip(signs, signs[1:]))


def sturm(poly):
    sequence = [qtrim(poly), qtrim(qderivative(poly))]
    need(len(qgcd(*sequence)) == 1, "squarefree chart parameter")
    while sequence[-1]:
        _, remainder = qdivmod(sequence[-2], sequence[-1])
        if not remainder:
            break
        sequence.append([-v for v in remainder])
    return sequence


def roots_between(sequence, left, right):
    at_left = variations(sign(qeval(p, left)) for p in sequence)
    at_right = variations(sign(qeval(p, right)) for p in sequence)
    return at_left - at_right


def roots_total(sequence):
    minus = variations(sign(p[-1]) * (-1 if (len(p) - 1) % 2 else 1) for p in sequence)
    plus = variations(sign(p[-1]) for p in sequence)
    return minus - plus


def primitive_sympy(poly, *variables):
    poly = sp.Poly(poly, *variables, domain=sp.QQ)
    return poly.monic()


def norm_equation(row, x, y):
    """Derive |sum (a+b*omega) z^j|^2-1 in Cartesian coordinates."""
    real, imag = sp.Integer(0), sp.Integer(0)
    power_real, power_imag = sp.Integer(1), sp.Integer(0)
    for a, b in row:
        cr, ci = sp.Rational(2 * a + b, 2), sp.Rational(b, 2)
        real += cr * power_real - 3 * ci * power_imag
        imag += cr * power_imag + ci * power_real
        power_real, power_imag = (
            sp.expand(power_real * x - 3 * power_imag * y),
            sp.expand(power_real * y + power_imag * x),
        )
    return sp.expand(real * real + 3 * imag * imag - 1)


def substitute_factor_mod_q(factor, xpoly, qpoly, y):
    """Evaluate a sparse bivariate polynomial while reducing after each product."""
    maximum = max(i for i, _, _ in factor)
    powers = [sp.Poly(1, y, domain=sp.QQ)]
    for _ in range(maximum):
        powers.append(sp.rem(powers[-1] * xpoly, qpoly))
    value = sp.Poly(0, y, domain=sp.QQ)
    for i, j, coefficient in factor:
        term = powers[i] * sp.Poly(coefficient * y**j, y, domain=sp.QQ)
        value = sp.rem(value + term, qpoly)
    return value


# Low-first polynomial arithmetic over F_p, always reduced modulo a chart q.
def mtrim(poly, prime):
    poly = [v % prime for v in poly]
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def mdivmod(left, right, prime):
    left, right = mtrim(left, prime), mtrim(right, prime)
    need(right, "nonzero finite-field divisor")
    quotient = [0] * max(0, len(left) - len(right) + 1)
    inverse = pow(right[-1], -1, prime)
    while len(left) >= len(right):
        shift = len(left) - len(right)
        coefficient = left[-1] * inverse % prime
        quotient[shift] = coefficient
        for i, value in enumerate(right):
            left[i + shift] = (left[i + shift] - coefficient * value) % prime
        left = mtrim(left, prime)
    return mtrim(quotient, prime), left


def mreduce(poly, modulus, prime):
    return mdivmod(poly, modulus, prime)[1]


def madd(left, right, modulus, prime, scale=1):
    out = [0] * max(len(left), len(right))
    for i, value in enumerate(left):
        out[i] += value
    for i, value in enumerate(right):
        out[i] += scale * value
    return mreduce(out, modulus, prime)


def mmul(left, right, modulus, prime):
    if not left or not right:
        return []
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] = (out[i + j] + a * b) % prime
    return mreduce(out, modulus, prime)


def mgcd(left, right, prime):
    left, right = mtrim(left, prime), mtrim(right, prime)
    while right:
        _, remainder = mdivmod(left, right, prime)
        left, right = right, remainder
    if not left:
        return []
    inverse = pow(left[-1], -1, prime)
    return [(v * inverse) % prime for v in left]


def fraction_mod(value, prime):
    value = Fraction(value)
    need(value.denominator % prime, "rational denominator survives proof prime")
    return value.numerator * pow(value.denominator, -1, prime) % prime


def complex_multiply(left, right, modulus, prime):
    a, b = left
    c, d = right
    return (
        madd(mmul(a, c, modulus, prime), mmul(b, d, modulus, prime), modulus, prime, -3),
        madd(mmul(a, d, modulus, prime), mmul(b, c, modulus, prime), modulus, prime),
    )


def modular_norms(rowids, xpoly, qpoly, prime):
    one, ypoly = [1], [0, 1]
    powers = [(one, [])]
    for _ in range(4):
        powers.append(complex_multiply(powers[-1], (xpoly, ypoly), qpoly, prime))
    inverse_two = pow(2, -1, prime)
    norms = {}
    for row, curve in rowids.items():
        value = ([], [])
        for (a, b), power in zip(row, powers):
            coefficient = ([(2 * a + b) * inverse_two % prime], [b * inverse_two % prime])
            term = complex_multiply(coefficient, power, qpoly, prime)
            value = (
                madd(value[0], term[0], qpoly, prime),
                madd(value[1], term[1], qpoly, prime),
            )
        norms[curve] = madd(
            mmul(value[0], value[0], qpoly, prime),
            mmul(value[1], value[1], qpoly, prime),
            qpoly,
            prime,
            3,
        )
    return norms


def d3_group(factors, rowids):
    identity = tuple(range(len(factors)))
    lookup = {row: curve for row, curve in rowids.items()}
    rotation, conjugation = list(identity), list(identity)
    for row, curve in rowids.items():
        power = (1, 0)
        rotated = []
        for coefficient in row:
            rotated.append(V.e_mul(coefficient, power))
            power = V.e_mul(power, (-1, 1))
        rotation[curve] = lookup[V.canonical_row(tuple(rotated))]
        conjugated = tuple((a + b, -b) for a, b in row)
        conjugation[curve] = lookup[V.canonical_row(conjugated)]
    compose = lambda a, b: tuple(a[b[i]] for i in range(len(a)))
    rotation, conjugation = tuple(rotation), tuple(conjugation)
    rotation2 = compose(rotation, rotation)
    group = (identity, rotation, rotation2, conjugation,
             compose(rotation, conjugation), compose(rotation2, conjugation))
    need(len(set(group)) == 6, "six distinct D3 actions")
    need(all(compose(a, b) in group for a in group for b in group), "D3 closure")
    return group


def audit_h4193(factors, circle, monomials, rowids, group, certificate_path=None):
    certificate_path = certificate_path or ROTATION / "certificate.json"
    certificate = json.loads(Path(certificate_path).read_text())
    need(certificate["pair_rows"] == [list(row) for row in PAIRS], "four h4193 rows")
    need(certificate["source_frontier_sha256"] == H4193_INPUT_SHA, "h4193 source frontier")
    images = {
        tuple(sorted((action[a], action[b])))
        for a, b, *_ in PAIRS
        for action in group
    }
    need(len(images) == 8, "eight D3-expanded h4193 exclusions")
    need(certificate["expanded_pair_exclusions"] == [list(p) for p in sorted(images)],
         "h4193 expanded-pair list")

    inverse_rows = {curve: row for row, curve in rowids.items()}
    expected_rows = {
        318: ((0, 0), (-1, 0), (0, 0), (0, 0), (-1, 1)),
        319: ((0, 0), (-1, 0), (0, 0), (0, 0), (0, 1)),
        340: ((0, 0), (-1, 0), (0, 0), (0, 0), (-1, 0)),
        341: ((0, 0), (-1, 0), (0, 0), (0, 0), (1, 0)),
    }
    need({c: inverse_rows[c] for c in expected_rows} == expected_rows,
         "the four stated displacement polynomials")

    x, y = sp.symbols("x y")
    equations = {curve: norm_equation(row, x, y) for curve, row in expected_rows.items()}
    # Independently connect the stated displacement rows to the reviewed norm inventory.
    for curve, expression in equations.items():
        submitted = sum(coefficient * x**i * y**j for i, j, coefficient in factors[curve])
        need(primitive_sympy(expression, x, y) == primitive_sympy(submitted, x, y),
             f"independent norm expansion for curve {curve}")

    prime = certificate["modular_prime"]
    need(prime == 1_000_003 and sp.isprime(prime), "h4193 proof prime")
    off_charts = []
    real_slots = circle_slots = event_checks = label_checks = 0
    edge_hashes = set()
    for a, b, *_ in PAIRS:
        f, g = equations[a], equations[b]
        result = sp.resultant(f, g, x)
        submitted_charts = [chart for chart in certificate["charts"] if chart["pair"] == [a, b]]
        product = sp.Integer(1)
        for chart in submitted_charts:
            qexpr = sum(coefficient * y**i for i, coefficient in enumerate(chart["q"]))
            product *= qexpr
        need(primitive_sympy(result, y) == primitive_sympy(product, y),
             f"complete resultant factor product for pair {(a, b)}")

        for chart in submitted_charts:
            q = [Fraction(v) for v in chart["q"]]
            qexpr = sum(sp.Rational(v.numerator, v.denominator) * y**i for i, v in enumerate(q))
            xcoeff = [Fraction(v) for v in chart["x"]]
            xexpr = sum(sp.Rational(v.numerator, v.denominator) * y**i
                        for i, v in enumerate(xcoeff))
            qsym = sp.Poly(qexpr, y, domain=sp.QQ)
            need(substitute_factor_mod_q(factors[a], sp.Poly(xexpr, y, domain=sp.QQ), qsym, y).is_zero,
                 "h4193 chart satisfies first norm equation")
            need(substitute_factor_mod_q(factors[b], sp.Poly(xexpr, y, domain=sp.QQ), qsym, y).is_zero,
                 "h4193 chart satisfies second norm equation")

            sequence = sturm(q)
            intervals = [(Fraction(left), Fraction(right))
                         for left, right in chart["isolating_intervals"]]
            need(all(left < right for left, right in intervals), "proper isolating intervals")
            need(all(intervals[i][1] < intervals[i + 1][0]
                     for i in range(len(intervals) - 1)), "ordered disjoint intervals")
            need(all(qeval(q, left) and qeval(q, right) and
                     roots_between(sequence, left, right) == 1
                     for left, right in intervals), "one exact real root per interval")
            need(roots_total(sequence) == len(intervals), "all chart real roots isolated")

            radius = sp.Poly(sp.expand(xexpr * xexpr + 3 * y * y), y, domain=sp.QQ)
            radius_remainder = sp.rem(radius, qsym)
            if chart["closed_unit_circle"]:
                need(radius_remainder == sp.Poly(1, y, domain=sp.QQ), "unit-circle chart")
                circle_slots += len(intervals)
                continue
            need(sp.gcd(radius_remainder - sp.Poly(1, y, domain=sp.QQ), qsym).degree() == 0,
                 "off-circle chart is disjoint from the unit circle")
            off_charts.append((chart, qsym, sp.Poly(xexpr, y, domain=sp.QQ)))
            real_slots += len(intervals)

            qmod = [v % prime for v in chart["q"]]
            xmod = [fraction_mod(v, prime) for v in xcoeff]
            norms = modular_norms(rowids, xmod, qmod, prime)
            active = set()
            for curve, norm in norms.items():
                need(len(mgcd(norm, qmod, prime)) == 1, "no label collision on any chart root")
                unit = madd(norm, [1], qmod, prime, -1)
                if not unit:
                    active.add(curve)
                else:
                    need(len(mgcd(unit, qmod, prime)) == 1,
                         "absent unit event excluded at every chart root")
                event_checks += 1
            radius_mod = madd(mmul(xmod, xmod, qmod, prime),
                               mmul([0, 1], [0, 1], qmod, prime), qmod, prime, 3)
            need(len(mgcd(radius_mod, qmod, prime)) == 1, "nonzero radix parameter")
            need(circle not in active and active == set(chart["active_curves"]) == {a, b},
                 "exactly the submitted pair is active")

            word = chart["colour_word"]
            colours = [sum(u * v for u, v in zip(word, label)) % 3 for label in V.LABELS]
            edges = []
            for i, j in itertools.combinations(range(243), 2):
                raw = tuple((V.DIGITS[u][0] - V.DIGITS[v][0],
                             V.DIGITS[u][1] - V.DIGITS[v][1])
                            for u, v in zip(V.LABELS[i], V.LABELS[j]))
                owner = V.edge_owner(i, j, monomials, rowids, circle)
                is_edge = owner == "base" or owner in active
                if is_edge:
                    need(colours[i] != colours[j], "independent h4193 proper 3-colouring")
                    edges.append([i, j])
                label_checks += 1
            need(len(edges) == chart["unit_edges"] == 405, "h4193 strict edge count")
            need(digest(edges) == chart["edge_sha256"], "h4193 strict edge hash")
            need(all(edge in edges for edge in ([0, 81], [0, 162], [81, 162])),
                 "permanent unit triangle")
            edge_hashes.add(chart["edge_sha256"])

    # The theorem says 18 distinct off-circle parameters, not merely 18 slots.
    for i, (_, q1, x1) in enumerate(off_charts):
        for _, q2, x2 in off_charts[i + 1 :]:
            common_y = sp.gcd(q1, q2)
            if common_y.degree() > 0:
                need(sp.gcd(common_y, x1 - x2).degree() == 0,
                     "off-circle charts have no common parameter")
    need(real_slots == 18 and circle_slots == 6 and len(edge_hashes) == 4,
         "h4193 real-slot and strict-graph totals")
    return {
        "pair_systems": 4,
        "expanded_pair_exclusions": 8,
        "charts": 6,
        "off_circle_distinct_parameters": real_slots,
        "unit_circle_parameter_slots": circle_slots,
        "modular_event_checks": event_checks,
        "label_pair_checks": label_checks,
        "strict_graphs": len(edge_hashes),
        "every_physical_member_chromatic_number": 3,
    }


def audit_h4195(factors, rowids, signatures, buckets, group, frontier, incidence,
                certificate_path=None):
    source = json.loads(Path(frontier).read_text())
    constraints = json.loads(Path(incidence).read_text())
    need(digest(source) == H4195_INPUT_SHA, "fresh h4193 residual interface")
    need(digest(constraints) == INCIDENCE_SHA, "fresh h4167 incidence interface")
    certificate_path = certificate_path or PROPAGATION / "certificate.json"
    certificate = json.loads(Path(certificate_path).read_text())
    pencils = all_pencils(buckets)
    need(digest(pencils) == certificate["pencil_catalogue_sha256"], "entrywise pencil catalogue")
    pencil_ids = {pencil: i for i, pencil in enumerate(pencils)}
    section_pairs = {
        tuple(sorted((left, right))): i
        for i, pencil in enumerate(pencils)
        for left, right in itertools.combinations(pencil, 2)
    }
    need(len(section_pairs) == 10 * len(pencils), "every section pair determines one pencil")

    old_pairs = {tuple(pair) for pair in constraints["monic_degree_four_excluded_pairs"]}
    excluded = {tuple(row) for row in constraints["injectivity_excluded_sets"]}
    old_pairs |= {row for row in excluded if len(row) == 2}
    triples = {row for row in excluded if len(row) == 3}
    new_pairs = {tuple(pair) for pair in source["reflection_and_rotation_pair_exclusions"]}
    need(len(old_pairs) == 8376 and len(triples) == 176420 and len(new_pairs) == 6704,
         "complete pair/triple inventories")
    need(not (old_pairs & new_pairs), "old and new pairs are disjoint")

    affected = defaultdict(list)
    applicable = set()
    for a, b in new_pairs:
        left, right = signatures[a], signatures[b]
        if left[0] == right[0]:
            continue
        pencil = affine_span(left, right)
        if pencil in pencil_ids:
            affected[pencil_ids[pencil]].append((a, b))
            applicable.add((a, b))
    for a, b in old_pairs:
        left, right = signatures[a], signatures[b]
        if left[0] != right[0]:
            need(affine_span(left, right) not in pencil_ids,
                 "old pair exclusions cannot occur in a residual pencil")
    affected = {i: sorted(rows) for i, rows in affected.items()}
    need(len(affected) == 226 and len(applicable) == 5280, "affected-pencil assignment")
    assignment = [[i, affected[i]] for i in sorted(affected)]
    need(digest(assignment) == certificate["affected_pair_assignment_sha256"],
         "entrywise affected-pair assignment")

    cores = {index: tuple(positions) for index, positions in certificate["three_section_cores"]}
    need(set(cores) == set(affected), "one core for every affected pencil")
    core_transversals = 0
    changed = []
    for index in sorted(affected):
        pencil = pencils[index]
        positions = cores[index]
        need(len(set(positions)) == 3 and all(0 <= position < 5 for position in positions),
             "valid three-section core")
        for values in itertools.product(*(buckets[pencil[position]] for position in positions)):
            core_transversals += 1
            need(any(tuple(sorted(pair)) in new_pairs for pair in itertools.combinations(values, 2)),
                 "every certified core transversal contains a new forbidden pair")
        raw = before = 0
        for values in itertools.product(*(buckets[section] for section in pencil)):
            raw += 1
            ordered = tuple(sorted(values))
            if not any(triple in triples for triple in itertools.combinations(ordered, 3)):
                before += 1
        changed.append([index, raw, before])
    need(changed == certificate["closed_pencils_index_raw_before"],
         "entrywise changed-subset counts")
    need(core_transversals == 19504, "complete three-section core replay")
    need(sum(row[1] for row in changed) == 3481088 and
         sum(row[2] for row in changed) == 3064704, "h4195 changed-subset totals")

    all_pairs = old_pairs | new_pairs
    bucket_masks = {section: sum(1 << curve for curve in curves)
                    for section, curves in buckets.items()}
    moved, retained = [], []
    witness_hash = hashlib.sha256()
    witness_trials = 0
    for row in source["remaining_exact"]:
        a, b = row[:2]
        sections = tuple(sorted((signatures[a], signatures[b])))
        index = section_pairs[sections]
        if index in affected:
            moved.append(row)
            continue
        others = sorted((section for section in pencils[index] if section not in sections),
                        key=lambda section: (len(buckets[section]), bucket_masks[section]))
        need(len(others) == 3, "three remaining pencil sections")
        witness = None
        for choices in itertools.product(*(buckets[section] for section in others)):
            witness_trials += 1
            candidate = tuple(sorted((a, b) + choices))
            if any(pair in all_pairs for pair in itertools.combinations(candidate, 2)):
                continue
            if any(triple in triples for triple in itertools.combinations(candidate, 3)):
                continue
            witness = candidate
            break
        need(witness is not None, "every retained exact-five pair has a constraint witness")
        retained.append(row)
        line = json.dumps([row[:2], list(witness)], separators=(",", ":")).encode() + b"\n"
        witness_hash.update(line)

    moved = sorted(moved)
    remaining_six = sorted(source["remaining_six"] + moved)
    need(len(moved) == 2960 and sum(row[4] for row in moved) == 87728, "exact mode moves")
    need(len(retained) == 118520 and len(remaining_six) == 10176, "residual mode counts")
    need(witness_trials == 279443, "deterministic witness search transcript length")
    need(witness_hash.hexdigest() == certificate["witness_transcript_sha256"],
         "complete retained-witness transcript")

    # Reconstruct the exported interface and its canonical hash independently.
    output = {
        "schema": "hn-radix-complete-pair-propagation-v1",
        "source_frontier_sha256": H4195_INPUT_SHA,
        "incidence_interface_sha256": INCIDENCE_SHA,
        "curve_inventory_sha256": CURVE_SHA,
        "reflection_and_rotation_pair_exclusions": sorted(new_pairs),
        "new_closed_pencils": [pencils[i] for i in sorted(affected)],
        "remaining_pencil_signatures": [p for i, p in enumerate(pencils) if i not in affected],
        "moved": moved,
        "remaining_exact": retained,
        "remaining_six": remaining_six,
        "extension_witness_transcript_sha256": witness_hash.hexdigest(),
        "mode_note": "Exact-five feasibility updated through all h4167 and h4191/h4193 exclusions; compatibility does not establish physical realization.",
    }
    need(digest(output) == certificate["export_canonical_sha256"] == H4195_EXPORT_SHA,
         "independent residual-interface reconstruction")

    signature_actions = []
    for action in group:
        mapping = {}
        for curve, section in signatures.items():
            image = signatures[action[curve]]
            need(section not in mapping or mapping[section] == image,
                 "D3 action descends to affine signatures")
            mapping[section] = image
        signature_actions.append(mapping)
    closed = {pencils[i] for i in affected}
    for action, section_action in zip(group, signature_actions):
        need({tuple(sorted((action[a], action[b]))) for a, b in new_pairs} == new_pairs,
             "new exclusions are D3 invariant")
        need({tuple(sorted(section_action[s] for s in pencil)) for pencil in closed} == closed,
             "closed pencils are D3 invariant")
    for row in source["remaining_exact"] + source["remaining_six"]:
        a, b, mask = row[:3]
        orbit = [tuple(sorted((action[a], action[b]))) for action in group]
        actual_mask = sum(1 << i for i, pair in enumerate(orbit) if pair == (a, b))
        need((a, b) == min(orbit) and mask == actual_mask == 1,
             "post-h4193 representatives have trivial stabilizer")

    return {
        "baseline_pencils": 5112,
        "baseline_admissible_lifts_imported_from_reviewed_h4189": 128871936,
        "applicable_new_pairs": len(applicable),
        "closed_pencils": len(affected),
        "closed_raw_lifts": sum(row[1] for row in changed),
        "closed_previously_admissible_lifts": sum(row[2] for row in changed),
        "remaining_pencils": len(pencils) - len(affected),
        "remaining_admissible_lifts": 128871936 - sum(row[2] for row in changed),
        "moved_pairs": len(moved),
        "moved_allowance": sum(row[4] for row in moved),
        "remaining_exact_five_pairs": len(retained),
        "remaining_exact_five_allowance": sum(row[4] for row in retained),
        "remaining_at_least_six_pairs": len(remaining_six),
        "remaining_at_least_six_allowance": sum(row[4] for row in remaining_six),
        "global_pairs_unchanged": len(retained) + len(remaining_six),
        "global_allowance_unchanged": sum(row[4] for row in retained + remaining_six),
        "constraint_witnesses": len(retained),
        "D3_invariant": True,
        "export_canonical_sha256": digest(output),
    }


def run(frontier, incidence):
    factors, circle, monomials, rowids, signatures, buckets = reconstruct_inventory()
    group = d3_group(factors, rowids)
    rotation = audit_h4193(factors, circle, monomials, rowids, group)
    propagation = audit_h4195(factors, rowids, signatures, buckets, group, frontier, incidence)
    return {
        "verified": True,
        "h4193": rotation,
        "h4195": propagation,
        "record_improvement": False,
        "scope": "fixed A5 complex-radix architecture only",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--frontier", type=Path, required=True)
    parser.add_argument("--incidence", type=Path, required=True)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = run(args.frontier, args.incidence)
    if args.check_expected:
        need(result == json.loads((HERE / "EXPECTED.json").read_text()), "expected review result")
    print(json.dumps(result, indent=2, sort_keys=True))
