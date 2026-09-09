#!/usr/bin/env python3
"""Exact standard-library verifier for the three-wheel symmetry quotient."""
from collections import Counter, deque
from fractions import Fraction
from functools import reduce
from itertools import combinations_with_replacement
from math import gcd, lcm
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_three_wheel_architecture"
SOURCE_CERTIFICATE_SHA256 = "7d3813350faffa9e6710cddc44d528a93ece7a1405db28c799974afd38c96e49"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def load_source():
    sys.path.insert(0, str(SOURCE))
    spec = importlib.util.spec_from_file_location("hn_three_wheel_source_verify", SOURCE / "verify.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def scale(polynomial, coefficient):
    return {monomial: coefficient * value for monomial, value in polynomial.items() if coefficient * value}


def multiply(left, right):
    result = {}
    for (i, j), a in left.items():
        for (k, l), b in right.items():
            monomial = (i + k, j + l)
            result[monomial] = result.get(monomial, 0) + a * b
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def power(polynomial, exponent):
    result = {(0, 0): 1}
    base = polynomial
    while exponent:
        if exponent & 1:
            result = multiply(result, base)
        base = multiply(base, base)
        exponent //= 2
    return result


def canonical(polynomial):
    need(polynomial, "zero polynomial has no projective normalization")
    denominator = reduce(lcm, (Fraction(value).denominator for value in polynomial.values()), 1)
    integral = {monomial: int(Fraction(value) * denominator) for monomial, value in polynomial.items()}
    common = reduce(gcd, (abs(value) for value in integral.values()))
    result = {monomial: value // common for monomial, value in integral.items()}
    if result[max(result)] < 0:
        result = scale(result, -1)
    return tuple(sorted(result.items()))


X = {(1, 0): 1}
Y = {(0, 1): 1}
ONE = {(0, 0): 1}


def transform(polynomial, name):
    if name == "swap":
        return {(j, i): coefficient for (i, j), coefficient in polynomial.items()}
    if name == "conjugate":
        return {
            (i, j): coefficient * (-1) ** (i + j)
            for (i, j), coefficient in polynomial.items()
        }
    if name == "rotate_x":
        degree = max(i for i, _ in polynomial)
        numerator = add(scale(X, 3), scale(ONE, -1))
        denominator = add(scale(X, 3), scale(ONE, 3))
        result = {}
        for (i, j), coefficient in polynomial.items():
            term = multiply(power(numerator, i), power(denominator, degree - i))
            term = multiply(term, power(Y, j))
            result = add(result, scale(term, coefficient))
        return result
    if name == "transpose_01":
        degree = max(j for _, j in polynomial)
        numerator_y = add(Y, scale(X, -1))
        denominator = add(ONE, {(1, 1): 3})
        result = {}
        for (i, j), coefficient in polynomial.items():
            term = multiply(power(scale(X, -1), i), power(numerator_y, j))
            term = multiply(term, power(denominator, degree - j))
            result = add(result, scale(term, coefficient))
        return result
    raise ValueError("unknown generator: " + name)


def compose(left, right):
    return tuple(left[right[i]] for i in range(len(right)))


def permutation_power(permutation, exponent):
    result = tuple(range(len(permutation)))
    for _ in range(exponent):
        result = compose(permutation, result)
    return result


def group_closure(generators):
    identity = tuple(range(len(generators[0])))
    seen = {identity}
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for generator in generators:
            candidate = compose(generator, current)
            if candidate not in seen:
                seen.add(candidate)
                queue.append(candidate)
    return seen


def sha256_json(value):
    encoded = json.dumps(value, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def source_state():
    source = load_source()
    certificate_bytes = (SOURCE / "certificate.json").read_bytes()
    need(hashlib.sha256(certificate_bytes).hexdigest() == SOURCE_CERTIFICATE_SHA256,
         "source certificate hash")
    certificate = json.loads(certificate_bytes)
    displacements, polynomials = source.input_polynomials()
    factors, decomposition = source.factor_check(certificate, polynomials)
    positive = {i for i, factor in enumerate(factors) if factor in (source.A.DX, source.A.DY)}
    need(len(positive) == 2, "source positive denominators")
    active = set(range(len(factors))) - positive
    base, pair_inventory = source.pair_inventory(displacements, decomposition)
    rows, cover = source.covering(factors, active, base, pair_inventory)
    expected = json.loads((SOURCE / "EXPECTED.json").read_text())
    need(cover == expected["finite_intersection_cover"], "source finite cover")
    need(source.A.audit_coprime(factors, sorted(active)) == expected["coprimality_audit"],
         "source coprimality audit")
    return source, factors, active, rows, cover


def alignment_ids(factors):
    lookup = {canonical(factor): i for i, factor in enumerate(factors)}
    thirds = (Fraction(0), Fraction(1, 3), Fraction(-1, 3), Fraction(1), Fraction(-1))
    polynomials = []
    for variable in (X, Y):
        for value in thirds:
            polynomials.append(add(variable, {(0, 0): -value}))
    for value in thirds:
        polynomials.append(add(Y, scale(X, -1), scale(add(ONE, {(1, 1): 3}), -value)))
    polynomials.append(add(ONE, {(1, 1): 3}))
    return {lookup[canonical(polynomial)] for polynomial in polynomials}


def generator_data(certificate, factors, domain_ids, safe_ids):
    factor_lookup = {factor_id: position for position, factor_id in enumerate(domain_ids)}
    permutations = []
    word_maps = {}
    for name in ("swap", "conjugate", "rotate_x", "transpose_01"):
        rows = certificate["generators"][name]["identities"]
        need(len(rows) == len(domain_ids), name + " identity count")
        targets = []
        for source_id, row in zip(domain_ids, rows):
            need(set(row) == {"target", "extras"}, name + " identity schema")
            target = row["target"]
            need(type(target) is int and target in factor_lookup, name + " target")
            extras = row["extras"]
            need(all(type(entry) is list and len(entry) == 2 and entry[0] in safe_ids
                     and type(entry[1]) is int and entry[1] > 0 for entry in extras),
                 name + " safe extras")
            right = factors[target]
            for extra_id, exponent in extras:
                right = multiply(right, power(factors[extra_id], exponent))
            need(canonical(transform(factors[source_id], name)) == canonical(right),
                 name + " polynomial identity")
            targets.append(factor_lookup[target])
        need(len(set(targets)) == len(domain_ids), name + " factor permutation")
        permutations.append(tuple(targets))
        word_map = certificate["generators"][name]["word_map"]
        need(sorted(word_map) == list(range(13)), name + " word permutation")
        word_maps[name] = word_map
    return permutations, word_maps


def pair_quotient(data, source_rows, cover, domain_ids, alignment, group):
    position = {factor_id: i for i, factor_id in enumerate(domain_ids)}
    primary = cover["primary_index"]
    protecting = {
        factor_id: min(
            (i for i, row in enumerate(source_rows) if factor_id not in row["bad"]),
            key=lambda i: (source_rows[i]["bad_degree_sum"], i),
        )
        for factor_id in sorted(source_rows[primary]["bad"])
    }
    selected_all = {
        tuple(sorted((factor_id, other)))
        for factor_id, word in protecting.items()
        for other in source_rows[word]["bad"]
    }
    need(len(selected_all) == cover["distinct_curve_pairs"], "source selected pairs")
    selected = {
        tuple(sorted((position[a], position[b])))
        for a, b in selected_all
        if a not in alignment and b not in alignment
    }
    orbit_by_key = {}
    for pair in selected:
        orbit = {
            tuple(sorted((permutation[pair[0]], permutation[pair[1]])))
            for permutation in group
        }
        orbit_by_key.setdefault(min(orbit), orbit)
    closure = set().union(*orbit_by_key.values())
    need(selected <= closure, "pair closure coverage")

    factors = data["factors"]
    bidegrees = [
        (max(i for i, _ in factors[factor_id]), max(j for _, j in factors[factor_id]))
        for factor_id in domain_ids
    ]
    total_degrees = [max(i + j for i, j in factors[factor_id]) for factor_id in domain_ids]

    def p1xp1_cost(pair):
        ax, ay = bidegrees[pair[0]]
        bx, by = bidegrees[pair[1]]
        return ax * by + ay * bx

    def total_cost(pair):
        return total_degrees[pair[0]] * total_degrees[pair[1]]

    representatives = []
    orbit_histogram = Counter()
    p1xp1_bound = 0
    total_bound = 0
    for orbit in orbit_by_key.values():
        orbit_histogram[len(orbit)] += 1
        representative = min(orbit, key=lambda pair: (p1xp1_cost(pair), total_cost(pair), pair))
        representatives.append(tuple(sorted((domain_ids[representative[0]], domain_ids[representative[1]]))))
        p1xp1_bound += p1xp1_cost(representative)
        total_bound += total_cost(representative)
    representatives.sort()
    certificate_representatives = [tuple(pair) for pair in data["pair_orbit_representatives"]]
    need(certificate_representatives == representatives, "pair orbit representatives")
    closure_absolute = sorted(
        tuple(sorted((domain_ids[a], domain_ids[b]))) for a, b in closure
    )
    return {
        "source_selected_pairs": len(selected_all),
        "selected_pairs_after_alignment_filter": len(selected),
        "symmetric_pair_closure": len(closure),
        "symmetric_pair_closure_sha256": sha256_json(closure_absolute),
        "symmetric_pair_orbits": len(orbit_by_key),
        "pair_orbit_size_histogram": {str(k): v for k, v in sorted(orbit_histogram.items())},
        "pair_orbit_representatives_sha256": sha256_json(representatives),
        "representative_p1xp1_bezout_bound": p1xp1_bound,
        "representative_total_degree_bezout_bound": total_bound,
    }


def qadd(left, right):
    return left[0] + right[0], left[1] + right[1]


def qneg(value):
    return -value[0], -value[1]


def qmul(left, right, radicand):
    return left[0] * right[0] + radicand * left[1] * right[1], left[0] * right[1] + left[1] * right[0]


def qinv(value, radicand):
    denominator = value[0] * value[0] - radicand * value[1] * value[1]
    need(denominator, "quadratic division by zero")
    return value[0] / denominator, -value[1] / denominator


def qdiv(left, right, radicand):
    return qmul(left, qinv(right, radicand), radicand)


def cmul(left, right, radicand):
    # A pair (r,s) encodes r + i sqrt(3) s, with r,s in Q(sqrt(radicand)).
    return (
        qadd(qmul(left[0], right[0], radicand), qneg((lambda z: (3*z[0], 3*z[1]))(qmul(left[1], right[1], radicand)))),
        qadd(qmul(left[0], right[1], radicand), qmul(left[1], right[0], radicand)),
    )


def cadd(left, right):
    return qadd(left[0], right[0]), qadd(left[1], right[1])


def phi(value, radicand):
    square = qmul(value, value, radicand)
    denominator = qadd((Fraction(1), Fraction(0)), (3 * square[0], 3 * square[1]))
    real = qdiv(qadd((Fraction(1), Fraction(0)), (-3 * square[0], -3 * square[1])), denominator, radicand)
    imag = qdiv((2 * value[0], 2 * value[1]), denominator, radicand)
    return real, imag


def phi_extended(value, radicand):
    if value is None:
        return ((Fraction(-1), Fraction(0)), (Fraction(0), Fraction(0)))
    return phi(value, radicand)


def eisenstein(pair):
    a, b = pair
    return ((Fraction(2 * a + b, 2), Fraction(0)), (Fraction(b, 2), Fraction(0)))


def evaluate_alignment(xvalue, yvalue, radicand):
    one = (Fraction(1), Fraction(0))
    three_xy = qmul(xvalue, yvalue, radicand)
    equations = []
    for value in (Fraction(0), Fraction(1, 3), Fraction(-1, 3), Fraction(1), Fraction(-1)):
        equations.extend((qadd(xvalue, (-value, Fraction(0))), qadd(yvalue, (-value, Fraction(0)))))
        equations.append(qadd(qadd(yvalue, qneg(xvalue)), qneg((value + 3 * value * three_xy[0], 3 * value * three_xy[1]))))
    equations.append(qadd(one, (3 * three_xy[0], 3 * three_xy[1])))
    return all(value != (0, 0) for value in equations)


def collision_check(certificate):
    representatives = certificate["collision_orbit_representatives"]
    need(len(representatives) == 4, "collision representative count")
    expected_norms = [(1, 3, 3), (1, 4, 4), (3, 3, 4), (3, 4, 4)]
    displacement = {1: (1, 0), 3: (1, 1), 4: (2, 0)}
    for row, norms in zip(representatives, expected_norms):
        need(tuple(row["squared_norms"]) == norms, "collision norm type")
        radicand = row["radicand"]
        need(type(radicand) is int and radicand > 1, "collision radicand")
        xvalue = tuple(map(Fraction, row["x_coefficients"]))
        yvalue = tuple(map(Fraction, row["y_coefficients"]))
        need(evaluate_alignment(xvalue, yvalue, radicand), "collision representative is nonalignment")
        d, e, f = (eisenstein(displacement[norm]) for norm in norms)
        total = cadd(d, cadd(cmul(phi(xvalue, radicand), e, radicand),
                             cmul(phi(yvalue, radicand), f, radicand)))
        need(total == (((0, 0), (0, 0))), "collision equation")
    types = list(combinations_with_replacement((1, 3, 4), 3))
    discriminants = {str(list(t)): 4*t[0]*t[1] - (t[2]-t[0]-t[1])**2 for t in types}
    need(all(value >= 0 for value in discriminants.values()), "collision triangle types")
    alignment_rows = certificate["alignment_collision_types"]
    expected_alignment = [(1, 1, 1), (1, 1, 3), (1, 1, 4), (1, 3, 4), (3, 3, 3), (4, 4, 4)]
    need([tuple(row["squared_norms"]) for row in alignment_rows] == expected_alignment,
         "alignment collision norm types")
    alignment_values = {Fraction(0), Fraction(1, 3), Fraction(-1, 3), Fraction(1), Fraction(-1)}
    for row, norms in zip(alignment_rows, expected_alignment):
        root_count = 2 if discriminants[str(list(norms))] > 0 else 1
        need(len(row["solutions"]) == root_count and len(set(map(tuple, row["solutions"]))) == root_count,
             "alignment collision root coverage")
        d, e, f = (eisenstein(displacement[norm]) for norm in norms)
        for xencoded, yencoded in row["solutions"]:
            xvalue = None if xencoded == "inf" else (Fraction(xencoded), Fraction(0))
            yvalue = None if yencoded == "inf" else (Fraction(yencoded), Fraction(0))
            need(xvalue is None or yvalue is None or xvalue[0] in alignment_values
                 or yvalue[0] in alignment_values, "listed collision alignment")
            total = cadd(d, cadd(cmul(phi_extended(xvalue, 1), e, 1),
                                 cmul(phi_extended(yvalue, 1), f, 1)))
            need(total == (((0, 0), (0, 0))), "alignment collision equation")
    need(set(types) == set(expected_norms) | set(expected_alignment), "complete collision type split")
    return {
        "squared_norm_types": len(types),
        "alignment_covered_types": len(alignment_rows),
        "nonalignment_collision_orbits": len(representatives),
        "nonalignment_squared_norm_types": [list(t) for t in expected_norms],
        "discriminants": discriminants,
    }


def run(certificate_path):
    certificate_bytes = certificate_path.read_bytes()
    certificate = json.loads(certificate_bytes)
    need(certificate["schema"] == "hn-three-wheel-symmetry-frontier-v1", "certificate schema")
    source, factors, active, source_rows, cover = source_state()
    alignment = alignment_ids(factors)
    need(sorted(alignment) == certificate["alignment_factor_ids"], "alignment factors")
    domain_ids = sorted(active - alignment)
    need(domain_ids == certificate["nonalignment_factor_ids"], "nonalignment factors")
    safe_ids = alignment | (set(range(len(factors))) - active)
    permutations, word_maps = generator_data(certificate, factors, domain_ids, safe_ids)

    for name, permutation in zip(("swap", "conjugate", "rotate_x", "transpose_01"), permutations):
        bad_sets = [set(row["bad"]) - alignment for row in source_rows]
        position = {factor_id: i for i, factor_id in enumerate(domain_ids)}
        for word, target_word in enumerate(word_maps[name]):
            image = {domain_ids[permutation[position[factor_id]]] for factor_id in bad_sets[word]}
            need(image == bad_sets[target_word], name + " word equivariance")

    group = group_closure(permutations)
    identity = tuple(range(len(domain_ids)))
    generator_orders = {
        name: next(exponent for exponent in range(1, 7) if permutation_power(permutation, exponent) == identity)
        for name, permutation in zip(("swap", "conjugate", "rotate_x", "transpose_01"), permutations)
    }
    factor_unseen = set(range(len(domain_ids)))
    factor_orbits = []
    while factor_unseen:
        seed = min(factor_unseen)
        orbit = {permutation[seed] for permutation in group}
        factor_orbits.append(orbit)
        factor_unseen -= orbit

    data = {"factors": factors, "pair_orbit_representatives": certificate["pair_orbit_representatives"]}
    pair_data = pair_quotient(data, source_rows, cover, domain_ids, alignment, group)
    collision_data = collision_check(certificate)
    result = {
        "status": "THREE_WHEEL_FRONTIER_QUOTIENTED_TO_5114_PHYSICAL_CLASSES",
        "record_improvement": False,
        "source_commit": "3e70f8f36be88fe8fdfd68dc2448b512a76e00c6",
        "source_contribution_height": 4065,
        "source_certificate_sha256": SOURCE_CERTIFICATE_SHA256,
        "certificate_sha256": hashlib.sha256(certificate_bytes).hexdigest(),
        "active_event_factors": len(active),
        "alignment_factors_removed": len(alignment),
        "nonalignment_factors": len(domain_ids),
        "generator_orders": generator_orders,
        "group_order_on_factors": len(group),
        "factor_orbits": len(factor_orbits),
        "factor_orbit_size_histogram": {str(k): v for k, v in sorted(Counter(map(len, factor_orbits)).items())},
        "word_permutations": word_maps,
        **pair_data,
        "collision_quotient": collision_data,
        "whole_frontier_physical_isomorphism_class_upper_bound": pair_data["representative_p1xp1_bezout_bound"] + collision_data["nonalignment_collision_orbits"],
        "new_chromatic_solver_calls": 0,
        "root_isolation_performed": False,
        "external_peer_review_claimed": False,
    }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    output = run(args.certificate)
    if args.check_expected:
        need(output == json.loads((HERE / "EXPECTED.json").read_text()), "expected output")
    print(json.dumps(output, indent=2, sort_keys=True))
