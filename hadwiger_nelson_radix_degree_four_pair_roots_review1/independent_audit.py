#!/usr/bin/env python3
"""Independent exact audit of the A5 degree-four residual-pair closure.

The target producer/verifier is not imported.  The accepted h4105 architecture
is an explicit dependency.  Root coverage is reconstructed with resultants,
FLINT factorization, vertical-fibre gcds, and reviewer-written Sturm arithmetic,
instead of the target's lexicographic Groebner decomposition.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

import sympy as sp
from flint import fmpz_poly


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ARCHITECTURE = ROOT / "hadwiger_nelson_complex_radix_architecture"
TARGET = ROOT / "hadwiger_nelson_radix_degree_four_pair_roots"

RESIDUAL_SHA = "42132ed90f7696d9cf7c17e7b47588ca717bb71b633141e29412a1b55b55e97d"
CURVE_SHA = "85c286422c01bcb6ebb244186032bc607984471bc2b705ef7247084dd7c33db9"
CERTIFICATE_SHA = "3ddb773a2713302100d60cc512aee44782293f10e2fb66cb8c853b3e211e0fbf"
PROOF_PRIMES = (1_000_033, 1_000_037)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_architecture():
    sys.path.insert(0, str(ARCHITECTURE))
    spec = importlib.util.spec_from_file_location(
        "accepted_h4105_architecture", ARCHITECTURE / "verify.py"
    )
    need(spec is not None and spec.loader is not None, "load accepted h4105 architecture")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Low-first exact rational polynomial arithmetic.
def qtrim(poly):
    poly = [Fraction(value) for value in poly]
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def qadd(left, right, scale=1):
    result = [Fraction(0)] * max(len(left), len(right))
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += scale * value
    return qtrim(result)


def qdivmod(left, right):
    left, right = qtrim(left), qtrim(right)
    need(right, "nonzero rational divisor")
    quotient = [Fraction(0)] * max(0, len(left) - len(right) + 1)
    while len(left) >= len(right):
        shift = len(left) - len(right)
        coefficient = left[-1] / right[-1]
        quotient[shift] = coefficient
        for index, value in enumerate(right):
            left[index + shift] -= coefficient * value
        left = qtrim(left)
    return qtrim(quotient), left


def qreduce(poly, modulus):
    return qdivmod(poly, modulus)[1]


def qmul(left, right, modulus=None):
    if not left or not right:
        return []
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    result = qtrim(result)
    return qreduce(result, modulus) if modulus else result


def qgcd(left, right):
    left, right = qtrim(left), qtrim(right)
    while right:
        _, remainder = qdivmod(left, right)
        left, right = right, remainder
    if not left:
        return []
    return [value / left[-1] for value in left]


def qderivative(poly):
    return qtrim([index * value for index, value in enumerate(poly)][1:])


def qeval(poly, value):
    result = Fraction(0)
    for coefficient in reversed(poly):
        result = result * value + coefficient
    return result


def sign(value):
    return (value > 0) - (value < 0)


def variations(signs):
    signs = [value for value in signs if value]
    return sum(left != right for left, right in zip(signs, signs[1:]))


def sturm(poly):
    poly = qtrim(poly)
    derivative = qderivative(poly)
    need(len(qgcd(poly, derivative)) == 1, "squarefree component factor")
    sequence = [poly, derivative]
    while sequence[-1]:
        _, remainder = qdivmod(sequence[-2], sequence[-1])
        if not remainder:
            break
        sequence.append([-value for value in remainder])
    return sequence


def real_root_count(poly):
    sequence = sturm(poly)
    at_minus_infinity = variations(
        sign(row[-1]) * (-1 if (len(row) - 1) % 2 else 1) for row in sequence
    )
    at_plus_infinity = variations(sign(row[-1]) for row in sequence)
    return at_minus_infinity - at_plus_infinity


def primitive_integer_coefficients(poly):
    poly = qtrim(poly)
    need(poly, "nonzero polynomial for primitive normalization")
    common_denominator = math.lcm(*(value.denominator for value in poly))
    integers = [value.numerator * (common_denominator // value.denominator) for value in poly]
    content = math.gcd(*integers)
    integers = [value // abs(content) for value in integers]
    if integers[-1] < 0:
        integers = [-value for value in integers]
    return tuple(integers)


def flint_coefficients(poly):
    return tuple(int(poly[index]) for index in range(len(poly)))


def flint_factors(coefficients):
    _unit, factors = fmpz_poly(list(coefficients)).factor()
    result = []
    for factor, multiplicity in factors:
        normalized = primitive_integer_coefficients(flint_coefficients(factor))
        result.append((normalized, int(multiplicity)))
    return result


def parse_coefficients(values):
    return qtrim(Fraction(value) for value in values)


def expression(sparse, x, y):
    return sum(coefficient * x**i * y**j for i, j, coefficient in sparse)


def exact_evaluator(q, xx, yy, maximum_degree=8):
    one = [Fraction(1)]
    x_powers = [one]
    y_powers = [one]
    for _ in range(maximum_degree):
        x_powers.append(qmul(x_powers[-1], xx, q))
        y_powers.append(qmul(y_powers[-1], yy, q))
    monomials = {
        (i, j): qmul(x_powers[i], y_powers[j], q)
        for i in range(maximum_degree + 1)
        for j in range(maximum_degree + 1 - i)
    }

    def evaluate(sparse):
        result = []
        for i, j, coefficient in sparse:
            result = qadd(result, monomials[i, j], Fraction(coefficient))
        return qreduce(result, q)

    return evaluate


# Low-first finite-field quotient arithmetic.  A nonzero modular residue is an
# exact witness that the corresponding rational residue is not identically zero.
def mtrim(poly, prime):
    poly = [value % prime for value in poly]
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def mdivmod(left, right, prime):
    left, right = mtrim(left, prime), mtrim(right, prime)
    need(right, "nonzero modular divisor")
    quotient = [0] * max(0, len(left) - len(right) + 1)
    inverse = pow(right[-1], -1, prime)
    while len(left) >= len(right):
        shift = len(left) - len(right)
        coefficient = left[-1] * inverse % prime
        quotient[shift] = coefficient
        for index, value in enumerate(right):
            left[index + shift] = (left[index + shift] - coefficient * value) % prime
        left = mtrim(left, prime)
    return mtrim(quotient, prime), left


def mreduce(poly, modulus, prime):
    return mdivmod(poly, modulus, prime)[1]


def madd(left, right, modulus, prime, scale=1):
    result = [0] * max(len(left), len(right))
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += scale * value
    return mreduce(result, modulus, prime)


def mmul(left, right, modulus, prime):
    if not left or not right:
        return []
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = (result[i + j] + a * b) % prime
    return mreduce(result, modulus, prime)


def fraction_mod(value, prime):
    value = Fraction(value)
    need(value.denominator % prime, "proof prime divides a rational denominator")
    return value.numerator * pow(value.denominator, -1, prime) % prime


def modular_evaluator(q, xx, yy, prime, maximum_degree=8):
    modulus = [fraction_mod(value, prime) for value in q]
    need(len(modulus) == len(q) and modulus[-1], "component degree preserved modulo proof prime")
    x_value = [fraction_mod(value, prime) for value in xx]
    y_value = [fraction_mod(value, prime) for value in yy]
    one = [1]
    x_powers = [one]
    y_powers = [one]
    for _ in range(maximum_degree):
        x_powers.append(mmul(x_powers[-1], x_value, modulus, prime))
        y_powers.append(mmul(y_powers[-1], y_value, modulus, prime))
    monomials = {
        (i, j): mmul(x_powers[i], y_powers[j], modulus, prime)
        for i in range(maximum_degree + 1)
        for j in range(maximum_degree + 1 - i)
    }

    def evaluate(sparse):
        result = []
        for i, j, coefficient in sparse:
            result = madd(result, monomials[i, j], modulus, prime, coefficient)
        return result

    return evaluate


# Sparse integer Cartesian arithmetic for collision coordinates.  Here the
# architecture variables mean z=x+i*sqrt(3)*y; this corrects a notation slip in
# the target prose, which writes z=x+i*y despite using these equations.
def sparse_add(left, right, scale=1):
    result = dict(left)
    for key, value in right.items():
        result[key] = result.get(key, 0) + scale * value
        if result[key] == 0:
            del result[key]
    return result


def sparse_multiply(left, right):
    result = defaultdict(int)
    for (i, j), a in left.items():
        for (k, ell), b in right.items():
            result[i + k, j + ell] += a * b
    return {key: value for key, value in result.items() if value}


def sparse_scale(poly, scale):
    return {key: scale * value for key, value in poly.items() if scale * value}


def collision_coordinate_polynomials(rows):
    xpoly, ypoly = {(1, 0): 1}, {(0, 1): 1}
    powers = [({(0, 0): 1}, {})]
    for _ in range(4):
        real, imaginary = powers[-1]
        powers.append(
            (
                sparse_add(sparse_multiply(real, xpoly), sparse_multiply(imaginary, ypoly), -3),
                sparse_add(sparse_multiply(real, ypoly), sparse_multiply(imaginary, xpoly)),
            )
        )
    output = []
    for row in rows:
        real, imaginary = {}, {}
        for (a, b), (power_real, power_imaginary) in zip(row, powers):
            real = sparse_add(real, sparse_scale(power_real, 2 * a + b))
            real = sparse_add(real, sparse_scale(power_imaginary, b), -3)
            imaginary = sparse_add(imaginary, sparse_scale(power_real, b))
            imaginary = sparse_add(imaginary, sparse_scale(power_imaginary, 2 * a + b))
        encode = lambda value: tuple((i, j, coefficient) for (i, j), coefficient in sorted(value.items()))
        output.append((encode(real), encode(imaginary)))
    return output


def specialize_y_at_integer(sparse, value):
    degree = max(j for _, j, _ in sparse)
    coefficients = [0] * (degree + 1)
    for i, j, coefficient in sparse:
        coefficients[j] += coefficient * value**i
    return coefficients


def specialize_x_at_rational(sparse, value):
    degree = max(j for _, j, _ in sparse)
    coefficients = [Fraction(0)] * (degree + 1)
    for i, j, coefficient in sparse:
        coefficients[j] += coefficient * value**i
    return qtrim(coefficients)


def integer_sequence():
    yield 0
    for value in itertools.count(1):
        yield value
        yield -value


def independent_resultant(sparse_f, sparse_g, x, y):
    f = expression(sparse_f, x, y)
    g = expression(sparse_g, x, y)
    resultant = sp.Poly(sp.resultant(f, g, y), x, domain=sp.ZZ)
    need(not resultant.is_zero, "distinct source curves have a nonzero resultant")

    degree_x_f = max(i for i, _, _ in sparse_f)
    degree_y_f = max(j for _, j, _ in sparse_f)
    degree_x_g = max(i for i, _, _ in sparse_g)
    degree_y_g = max(j for _, j, _ in sparse_g)
    degree_bound = degree_x_f * degree_y_g + degree_x_g * degree_y_f
    need(resultant.degree() <= degree_bound, "resultant degree bound")

    interpolation_checks = 0
    for value in integer_sequence():
        f_coefficients = specialize_y_at_integer(sparse_f, value)
        g_coefficients = specialize_y_at_integer(sparse_g, value)
        if not f_coefficients[-1] or not g_coefficients[-1]:
            continue
        independent = fmpz_poly(f_coefficients).resultant(fmpz_poly(g_coefficients))
        need(int(independent) == int(resultant.eval(value)), "FLINT/SymPy resultant evaluation")
        interpolation_checks += 1
        if interpolation_checks == degree_bound + 1:
            break
    need(interpolation_checks == degree_bound + 1, "enough resultant interpolation checks")
    coefficients = [Fraction(resultant.nth(i)) for i in range(resultant.degree() + 1)]
    return flint_factors(primitive_integer_coefficients(coefficients)), interpolation_checks


def component_tuple(row):
    return tuple(row["q"]), tuple(row["x"]), tuple(row["y"])


def x_projection_factor(row):
    q = parse_coefficients(row["q"])
    xx = parse_coefficients(row["x"])
    if len(row["x"]) == 1:
        x0 = Fraction(row["x"][0])
        return primitive_integer_coefficients([-x0, Fraction(1)])
    need(xx == [Fraction(0), Fraction(1)], "supported exact x parametrization")
    return primitive_integer_coefficients(q)


def y_projection_factor_on_rational_x_fibre(row):
    q = parse_coefficients(row["q"])
    yy = parse_coefficients(row["y"])
    if len(row["y"]) == 1:
        y0 = Fraction(row["y"][0])
        return primitive_integer_coefficients([-y0, Fraction(1)])
    need(yy == [Fraction(0), Fraction(1)],
         f"supported vertical y parametrization for {row['component_key']}: {yy}")
    return primitive_integer_coefficients(q)


def audit_root_cover(pairs, factors, certificate):
    certified = {row["component_key"]: row for row in certificate["components"]}
    need(len(certified) == len(certificate["components"]), "unique certificate component keys")
    for key, row in certified.items():
        need(key == digest(component_tuple(row)), "component key binds exact coordinates")

    pair_entries = certificate["pair_components"]
    need([entry["pair"] for entry in pair_entries] == [list(row[:2]) for row in pairs],
         "pair-component rows bind the selected pair order")
    source_map = defaultdict(list)
    for entry in pair_entries:
        need(len(entry["real_component_keys"]) == len(set(entry["real_component_keys"])),
             "no duplicate component within a source pair")
        for key in entry["real_component_keys"]:
            need(key in certified, "pair cites a certified component")
            source_map[key].append(entry["pair"])
    need(set(source_map) == set(certified), "every certified component has a source pair")
    for key, row in certified.items():
        need(row["source_pairs"] == sorted(source_map[key]), "complete component source list")

    x, y = sp.symbols("x y")
    complex_instances = 0
    real_instances = 0
    resultant_factors = 0
    interpolation_checks = 0
    rational_x_fibre_instances = 0
    rational_x_real_instances = 0
    rational_x_resultant_multiplicity_excess = 0
    expected_roots = {}
    for pair, entry in zip(pairs, pair_entries):
        a, b = pair[:2]
        factorization, checks = independent_resultant(factors[a], factors[b], x, y)
        interpolation_checks += checks
        resultant_factors += len(factorization)
        target_rows = [certified[key] for key in entry["real_component_keys"]]
        targets_by_projection = defaultdict(list)
        for target_row in target_rows:
            targets_by_projection[x_projection_factor(target_row)].append(target_row)

        for qx, resultant_multiplicity in factorization:
            x_roots = real_root_count(qx)
            projected_targets = targets_by_projection.pop(qx, [])
            if len(qx) > 2 and not x_roots:
                need(not projected_targets, "no real certificate above a complex x projection")
                complex_instances += 1
                continue

            if len(qx) > 2:
                need(x_roots > 0 and resultant_multiplicity == 1,
                     "nonlinear real x projection is a simple branch")
                need(len(projected_targets) == 1,
                     "one certified branch above a simple real x projection")
                target_row = projected_targets[0]
                target_q = primitive_integer_coefficients(parse_coefficients(target_row["q"]))
                need(target_q == qx, "simple branch uses its exact x eliminant")
                roots = real_root_count(parse_coefficients(target_row["q"]))
                need(roots == x_roots, "simple branch preserves all real x roots")
                previous = expected_roots.setdefault(target_row["component_key"], roots)
                need(previous == roots, "consistent shared-component root count")
                real_instances += 1
                continue

            rational_x_fibre_instances += 1
            need(x_roots == 1, "linear x projection has one real root")
            x0 = -Fraction(qx[0], qx[1])
            need(all(parse_coefficients(row["x"]) == [x0] for row in projected_targets),
                 "certificate uses the independently recovered vertical coordinate")
            fy = primitive_integer_coefficients(specialize_x_at_rational(factors[a], x0))
            gy = primitive_integer_coefficients(specialize_x_at_rational(factors[b], x0))
            common = fmpz_poly(list(fy)).gcd(fmpz_poly(list(gy)))
            common_coefficients = primitive_integer_coefficients(flint_coefficients(common))
            fibre_factors = flint_factors(common_coefficients)
            fibre_degree = sum((len(q) - 1) * multiplicity
                               for q, multiplicity in fibre_factors)
            need(resultant_multiplicity >= fibre_degree,
                 "vertical resultant multiplicity dominates the affine common fibre")
            rational_x_resultant_multiplicity_excess += resultant_multiplicity - fibre_degree
            need(all(multiplicity == 1 for _, multiplicity in fibre_factors),
                 "vertical common fibre is squarefree")
            real_factors = []
            for q_coefficients, _multiplicity in fibre_factors:
                roots = real_root_count(q_coefficients)
                if roots:
                    real_factors.append(q_coefficients)
                else:
                    complex_instances += 1
            target_factors = [
                y_projection_factor_on_rational_x_fibre(row)
                for row in projected_targets
            ]
            need(Counter(real_factors) == Counter(target_factors),
                 "all and only real vertical-fibre factors are certified")
            for target_row in projected_targets:
                roots = real_root_count(parse_coefficients(target_row["q"]))
                previous = expected_roots.setdefault(target_row["component_key"], roots)
                need(previous == roots, "consistent shared vertical-component root count")
                real_instances += 1
                rational_x_real_instances += 1
        need(not targets_by_projection, "every certified x projection occurs in the resultant")

    need(complex_instances == certificate["complex_only_irreducible_components"] == 22,
         "complete complex-only component-instance count")
    need(real_instances == sum(len(row["real_component_keys"]) for row in pair_entries) == 266,
         "complete real component-instance count")
    need(len(expected_roots) == certificate["distinct_real_components"] == 169,
         "distinct real component-record count")
    return expected_roots, {
        "resultant_factor_instances": resultant_factors,
        "resultant_interpolation_checks": interpolation_checks,
        "rational_x_fibre_instances": rational_x_fibre_instances,
        "rational_x_real_component_instances": rational_x_real_instances,
        "rational_x_resultant_multiplicity_excess": rational_x_resultant_multiplicity_excess,
        "real_component_instances": real_instances,
        "complex_only_component_instances": complex_instances,
        "distinct_real_component_records": len(expected_roots),
    }


def audit_components(factors, factor_edges, base_edges, collisions, certificate, expected_roots):
    collision_polynomials = collision_coordinate_polynomials(collisions)
    triangle = {(0, 81), (0, 162), (81, 162)}
    need(triangle <= set(map(tuple, base_edges)), "permanent unit triangle")

    active_histogram = Counter()
    chromatic_histogram = Counter()
    event_decisions = collision_decisions = colour_edge_checks = exact_fallbacks = 0
    real_embeddings = 0
    collision_records = collision_embeddings = 0
    injective_records = injective_embeddings = 0
    for row in certificate["components"]:
        q = parse_coefficients(row["q"])
        xx = parse_coefficients(row["x"])
        yy = parse_coefficients(row["y"])
        factorization = flint_factors(primitive_integer_coefficients(q))
        need(len(factorization) == 1 and factorization[0][1] == 1 and
             factorization[0][0] == primitive_integer_coefficients(q),
             "FLINT independently verifies component irreducibility")
        roots = real_root_count(q)
        need(roots == expected_roots[row["component_key"]] == row["real_embeddings"],
             "reviewer Sturm count agrees with root-cover multiplicity")

        exact = exact_evaluator(q, xx, yy)
        modular = None
        for prime in PROOF_PRIMES:
            try:
                modular = modular_evaluator(q, xx, yy, prime)
                break
            except ValueError:
                continue
        need(modular is not None, "a reviewer proof prime preserves the component")

        claimed_active = set(row["active_curves"])
        actual_active = []
        for index, factor in enumerate(factors):
            if index in claimed_active:
                need(not exact(factor), "claimed active event is an exact identity")
                actual_active.append(index)
            elif not modular(factor):
                residue = exact(factor)
                exact_fallbacks += 1
                need(residue, "unlisted active event")
            event_decisions += 1
        need(actual_active == row["active_curves"], "complete ordered active-event set")
        need(all(left in claimed_active and right in claimed_active
                 for left, right in row["source_pairs"]),
             "every source pair is active on its certified component")

        claimed_collisions = set(row["collision_rows"])
        actual_collisions = []
        for index, (real, imaginary) in enumerate(collision_polynomials):
            if index in claimed_collisions:
                need(not exact(real) and not exact(imaginary), "claimed collision is exact")
                actual_collisions.append(index)
            elif not modular(real) and not modular(imaginary):
                real_residue, imaginary_residue = exact(real), exact(imaginary)
                exact_fallbacks += 1
                need(real_residue or imaginary_residue, "unlisted label collision")
            collision_decisions += 1
        need(actual_collisions == row["collision_rows"], "complete ordered collision set")

        if actual_collisions:
            need(row["chromatic_number_upper_bound"] == 3, "collision theorem upper bound")
            need(row["three_colouring"] is None and row["four_colouring"] is None,
                 "collision branch stores no invalid label colouring")
            collision_records += 1
            collision_embeddings += roots
        else:
            need(2 <= len(actual_active) <= 4,
                 "every injective component has two, three, or four active curves")
            edges = sorted(base_edges + [edge for curve in actual_active for edge in factor_edges[curve]])
            need(len(edges) == len(set(edges)), "unique event-edge ownership")
            word = row["three_colouring"]
            need(row["chromatic_number_upper_bound"] == 3, "injective component upper bound")
            need(isinstance(word, list) and len(word) == 243 and set(word) <= {0, 1, 2},
                 "properly encoded three-colour word")
            need(all(word[left] != word[right] for left, right in edges),
                 "independent strict-edge colouring replay")
            colour_edge_checks += len(edges)
            injective_records += 1
            injective_embeddings += roots

        active_histogram[(len(actual_active), sum(len(factor_edges[c]) for c in actual_active))] += roots
        chromatic_histogram[3] += roots
        real_embeddings += roots

    active_summary = {
        f"{curves}_curves_{edges}_event_edges": count
        for (curves, edges), count in sorted(active_histogram.items())
    }
    chromatic_summary = {str(key): value for key, value in sorted(chromatic_histogram.items())}
    need(active_summary == certificate["active_curve_edge_histogram_by_embedding"],
         "active-event histogram")
    need(chromatic_summary == certificate["chromatic_upper_bound_histogram_by_embedding"],
         "chromatic histogram")
    need(real_embeddings == certificate["real_parameter_embeddings"] == 415,
         "total real embeddings")
    need((collision_records, collision_embeddings) == (17, 25), "collision totals")
    need((injective_records, injective_embeddings) == (152, 390), "injective totals")
    return {
        "real_parameter_embeddings": real_embeddings,
        "collision_component_records": collision_records,
        "collision_embeddings": collision_embeddings,
        "injective_component_records": injective_records,
        "injective_embeddings": injective_embeddings,
        "event_identity_decisions": event_decisions,
        "collision_identity_decisions": collision_decisions,
        "colour_edge_checks": colour_edge_checks,
        "exact_nonzero_fallbacks_after_modular_screen": exact_fallbacks,
        "chromatic_number_of_every_physical_member": 3,
    }


def run(residual_path, certificate_path):
    residual = json.loads(Path(residual_path).read_text())
    certificate = json.loads(Path(certificate_path).read_text())
    need(digest(residual) == RESIDUAL_SHA == certificate["source_residual_sha256"],
         "independently reviewed h4195 residual")
    need(file_digest(certificate_path) == CERTIFICATE_SHA, "target certificate file digest")
    need(certificate["schema"] == "hn-radix-degree-four-pair-roots-v1", "certificate schema")

    architecture = load_architecture()
    _rows, _events, factors, factor_edges, base_edges, collisions, _simple, _circle = architecture.build()
    need(digest(factors) == CURVE_SHA == certificate["curve_inventory_sha256"],
         "accepted h4105 curve inventory")
    degrees = [architecture.degree(factor) for factor in factors]
    pairs = [
        row for row in residual["remaining_six"]
        if 4 in (degrees[row[0]], degrees[row[1]])
    ]
    need(len(pairs) == certificate["pair_count"] == 160, "complete degree-four pair stratum")
    need(all(row[2] == 1 and row[3] == row[4] and
             degrees[row[0]] * degrees[row[1]] == 2 * row[3]
             for row in pairs),
         "trivial stabilizers and equal Bezout/orbit allowances")
    pair_histogram = Counter((degrees[row[0]], degrees[row[1]]) for row in pairs)
    need(pair_histogram == Counter({(4, 4): 28, (4, 6): 32, (6, 4): 4, (4, 8): 96}),
         "ordered degree-pair histogram")
    need(digest(pairs) == certificate["pair_sha256"], "entrywise selected pair list")
    removed_allowance = sum(row[4] for row in pairs)
    need(removed_allowance == certificate["total_bezout_allowance"] == 2192,
         "removed orbit allowance")

    expected_roots, cover = audit_root_cover(pairs, factors, certificate)
    components = audit_components(
        factors, factor_edges, base_edges, collisions, certificate, expected_roots
    )

    remaining_exact = residual["remaining_exact"]
    selected = {tuple(row) for row in pairs}
    remaining_six = [row for row in residual["remaining_six"] if tuple(row) not in selected]
    residual_counts = {
        "remaining_exact_pairs": len(remaining_exact),
        "remaining_exact_allowance": sum(row[4] for row in remaining_exact),
        "remaining_at_least_six_pairs": len(remaining_six),
        "remaining_at_least_six_allowance": sum(row[4] for row in remaining_six),
        "total_pairs": len(remaining_exact) + len(remaining_six),
        "total_allowance": sum(row[4] for row in remaining_exact + remaining_six),
    }
    need(residual_counts == {
        "remaining_exact_pairs": 118_520,
        "remaining_exact_allowance": 3_503_032,
        "remaining_at_least_six_pairs": 10_016,
        "remaining_at_least_six_allowance": 308_208,
        "total_pairs": 128_536,
        "total_allowance": 3_811_240,
    }, "revised conditional residual arithmetic")

    without_self = dict(certificate)
    claimed = without_self.pop("result_sha256_without_self")
    need(claimed == digest(without_self), "target certificate self-excluding digest")
    return {
        "verified": True,
        "verdict": "ACCEPT_WITH_MINOR_DOCUMENTATION_CORRECTION",
        "scope": "160 explicit degree-four pairs in the fixed A5 complex-radix architecture",
        "record_improvement": False,
        "pair_count": len(pairs),
        "removed_orbit_allowance": removed_allowance,
        "degree_pair_histogram": {
            f"{left}_{right}": count for (left, right), count in sorted(pair_histogram.items())
        },
        "root_cover": cover,
        "components": components,
        "conditional_revised_residual": residual_counts,
        "documentation_correction": "The polynomial variables encode z=x+i*sqrt(3)*y, not z=x+i*y.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--residual", type=Path, required=True)
    parser.add_argument("--certificate", type=Path, default=TARGET / "certificate.json")
    parser.add_argument("--check-expected", action="store_true")
    arguments = parser.parse_args()
    result = run(arguments.residual, arguments.certificate)
    if arguments.check_expected:
        need(result == json.loads((HERE / "EXPECTED.json").read_text()), "expected reviewer output")
    print(json.dumps(result, indent=2, sort_keys=True))
