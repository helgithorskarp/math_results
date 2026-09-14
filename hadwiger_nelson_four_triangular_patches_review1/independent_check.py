#!/usr/bin/env python3
"""Clean-room exact review of the four-P36 continuum theorem.

No code is imported from the reviewed package.  Surds are represented by
prime-support tuples, contact phases are generated directly from every ordered
point pair, coincidences are merged by exact Cartesian coordinate keys, and
XOR systems are solved by parity propagation.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from fractions import Fraction as Q
from functools import cache
import hashlib
from itertools import combinations
import json
from math import gcd, isqrt
from pathlib import Path


LIMIT = 36
HERE = Path(__file__).resolve().parent

# These are claims under review, not inputs used to generate the census.
TARGET = {
    "patch_vertices": 127,
    "patch_edges": 342,
    "maximum_union_vertices": 505,
    "primitive_contact_lines": 528,
    "event_phases": 594,
    "rational_event_phases": 162,
    "irrational_event_phases": 432,
    "event_classes_mod_units": 99,
    "rational_event_classes_mod_units": 27,
    "irrational_event_classes_mod_units": 72,
    "coincidence_phases": 54,
    "normalized_active_triangles": 186,
    "normalized_four_cycles": 8100,
    "four_cycle_target_classes": 4231,
    "inventory_sha256":
        "31285b4c110ec1cd5c06ee0c0a71f0d9014bcb91e8de6b59bddca28ddc8da34a",
    "triangle_certificate_sha256":
        "be221bdb1df2df0eca2b538058bdd97be6b087a4d52d501c0424cad2e0b1cea0",
    "four_cycle_certificate_sha256":
        "8915b9d8012d3e4653f3089feffe8c00aca6ea4d86fff6019a1a18420bfa8f8d",
}


def need(condition, message):
    if not condition:
        raise AssertionError(message)


@cache
def factor_sqrt(n):
    """Return c,S with sqrt(n)=c*product(sqrt(p) for p in S)."""
    need(n > 0, "square-root radicand must be positive")
    coefficient = 1
    support = []
    divisor = 2
    remaining = n
    while divisor * divisor <= remaining:
        exponent = 0
        while remaining % divisor == 0:
            exponent += 1
            remaining //= divisor
        coefficient *= divisor ** (exponent // 2)
        if exponent & 1:
            support.append(divisor)
        divisor += 1
    if remaining > 1:
        support.append(remaining)
    return coefficient, tuple(support)


# A surd is a dict {tuple_of_primes: rational_coefficient}.  The empty tuple
# is the rational basis.  Prime supports multiply by symmetric difference.
def scalar(value=0):
    value = Q(value)
    return {} if value == 0 else {(): value}


def add(left, right):
    answer = dict(left)
    for basis, value in right.items():
        answer[basis] = answer.get(basis, Q(0)) + value
        if answer[basis] == 0:
            del answer[basis]
    return answer


def neg(value):
    return {basis: -coefficient for basis, coefficient in value.items()}


def scale(value, multiplier):
    multiplier = Q(multiplier)
    return {basis: coefficient * multiplier
            for basis, coefficient in value.items() if coefficient * multiplier}


@cache
def basis_product(left, right):
    a, b = set(left), set(right)
    common = a & b
    coefficient = 1
    for prime in common:
        coefficient *= prime
    return coefficient, tuple(sorted(a ^ b))


def multiply(left, right):
    answer = {}
    for a, x in left.items():
        for b, y in right.items():
            coefficient, basis = basis_product(a, b)
            answer[basis] = answer.get(basis, Q(0)) + coefficient * x * y
    return {basis: value for basis, value in answer.items() if value}


def external_surd_key(value):
    rows = []
    for support, coefficient in value.items():
        radicand = 1
        for prime in support:
            radicand *= prime
        rows.append((radicand, coefficient.numerator, coefficient.denominator))
    return tuple(sorted(rows))


def surd_from_external(key):
    result = {}
    for radicand, numerator, denominator in key:
        coefficient, support = factor_sqrt(radicand)
        need(coefficient == 1, "external basis is not squarefree")
        result[support] = Q(numerator, denominator)
    return result


def phase_key(phase):
    return external_surd_key(phase[0]), external_surd_key(phase[1])


def phase_from_key(key):
    return surd_from_external(key[0]), surd_from_external(key[1])


def rational_phase(x, y):
    return scalar(Q(x)), scalar(Q(y))


def phase_conjugate(phase):
    return phase[0], neg(phase[1])


def phase_product(left, right):
    # (x+i sqrt(3)y)(u+i sqrt(3)v)
    return (
        add(multiply(left[0], right[0]), scale(multiply(left[1], right[1]), -3)),
        add(multiply(left[0], right[1]), multiply(left[1], right[0])),
    )


def is_rational_key(key):
    return all(radicand == 1 for coordinate in key
               for radicand, _, _ in coordinate)


UNITS = tuple(rational_phase(x, y) for x, y in (
    (Q(1), Q(0)), (Q(1, 2), Q(1, 2)), (Q(-1, 2), Q(1, 2)),
    (Q(-1), Q(0)), (Q(-1, 2), Q(-1, 2)), (Q(1, 2), Q(-1, 2)),
))
IDENTITY = rational_phase(1, 0)


def canonical_phase(phase):
    return min(phase_key(phase_product(phase, unit)) for unit in UNITS)


def ring_norm(z):
    a, b = z
    return a * a + a * b + b * b


def ring_conjugate(z):
    return z[0] + z[1], -z[1]


def ring_product(z, w):
    a, b = z
    c, d = w
    return a * c - b * d, a * d + b * c + b * d


def primitive_line(p, q, k):
    divisor = gcd(gcd(abs(p), abs(q)), abs(k))
    need(divisor, "zero line")
    row = p // divisor, q // divisor, k // divisor
    for value in row:
        if value:
            return row if value > 0 else tuple(-x for x in row)
    raise AssertionError("unreachable zero line")


def line_intersections(p, q, k):
    """Intersect p*x+q*y=k with x^2+3*y^2=1 exactly."""
    denominator = 3 * p * p + q * q
    discriminant = denominator - 3 * k * k
    need(discriminant >= 0, "requested nonintersecting line")
    if discriminant == 0:
        signs = (1,)
        root_scale, support = 0, ()
    else:
        signs = (-1, 1)
        root_scale, support = factor_sqrt(discriminant)
    roots = []
    for sign in signs:
        root = {} if not root_scale else {support: Q(sign * root_scale, denominator)}
        x = add(scalar(Q(3 * p * k, denominator)), scale(root, q))
        y = add(scalar(Q(q * k, denominator)), scale(root, -p))
        roots.append((x, y))
    return roots


def rotate(phase, z):
    x, y = phase
    u = Q(2 * z[0] + z[1], 2)
    v = Q(z[1], 2)
    return (
        add(scale(x, u), scale(y, -3 * v)),
        add(scale(y, u), scale(x, v)),
    )


def coordinate_key(point):
    return external_surd_key(point[0]), external_surd_key(point[1])


def distance_squared(left, right):
    dx = add(left[0], neg(right[0]))
    dy = add(left[1], neg(right[1]))
    return add(multiply(dx, dx), scale(multiply(dy, dy), 3))


def update_digest(digest, value):
    digest.update(repr(value).encode("ascii"))
    digest.update(b"\n")


def build_inventory():
    # The deliberately loose box is independent of the target's point bound.
    points = sorted((a, b) for a in range(-LIMIT, LIMIT + 1)
                    for b in range(-LIMIT, LIMIT + 1)
                    if ring_norm((a, b)) <= LIMIT)
    origin = points.index((0, 0))
    residue = tuple((a - b) % 3 for a, b in points)
    seed_edges = []
    for i, z in enumerate(points):
        for j in range(i):
            w = points[j]
            if ring_norm((z[0] - w[0], z[1] - w[1])) == 1:
                seed_edges.append((i, j))
    need(all(residue[i] != residue[j] for i, j in seed_edges),
         "residue colouring failed inside P36")

    lines = set()
    universal = set()
    events = defaultdict(set)
    # Generate roots from each ordered point pair, without first aggregating
    # primitive lines.  Set union later coalesces duplicate roots.
    for i, z in enumerate(points):
        for j, w in enumerate(points):
            k = ring_norm(z) + ring_norm(w) - 1
            if i == origin or j == origin:
                if k == 0:
                    universal.add((i, j))
                continue
            a, b = ring_product(w, ring_conjugate(z))
            p, q = 2 * a + b, -3 * b
            discriminant = 3 * p * p + q * q - 3 * k * k
            if discriminant < 0:
                continue
            lines.add(primitive_line(p, q, k))
            for phase in line_intersections(p, q, k):
                need(distance_squared(rotate(IDENTITY, z), rotate(phase, w)) == scalar(1),
                     "derived contact does not have unit length")
                events[phase_key(phase)].add((i, j))

    coincidences = defaultdict(set)
    for i, z in enumerate(points):
        if i == origin:
            continue
        for j, w in enumerate(points):
            denominator = ring_norm(w)
            if denominator and ring_norm(z) == denominator:
                a, b = ring_product(z, ring_conjugate(w))
                phase = rational_phase(Q(2 * a + b, 2 * denominator),
                                       Q(b, 2 * denominator))
                need(coordinate_key(rotate(phase, w)) == coordinate_key(rotate(IDENTITY, z)),
                     "ratio phase does not give the declared coincidence")
                coincidences[phase_key(phase)].add((i, j))
    need(set(coincidences) <= set(events), "coincidence-only phase found")

    for key in events:
        phase = phase_from_key(key)
        need(phase_key(phase_product(phase, phase_conjugate(phase))) == phase_key(IDENTITY),
             "non-unit event phase")

    digest = hashlib.sha256()
    for key in sorted(events):
        update_digest(digest, (key, tuple(sorted(events[key])),
                               tuple(sorted(coincidences.get(key, ())))))
    return {
        "points": tuple(points), "origin": origin, "residue": residue,
        "seed_edges": tuple(seed_edges), "universal": frozenset(universal),
        "lines": frozenset(lines), "events": dict(events),
        "coincidences": dict(coincidences), "inventory_sha256": digest.hexdigest(),
    }


def pair_requirements(delta, inventory):
    key = phase_key(delta)
    residue = inventory["residue"]
    sign_bits = set()
    zero_bits = set()
    for i, j in inventory["events"].get(key, ()):
        ri, rj = residue[i], residue[j]
        if ri and rj:
            # Unequal nonzero colours: xor=1 for ri*rj=1, else 0.
            sign_bits.add(int((ri * rj) % 3 == 1))
        elif ri == 0 and rj == 0:
            zero_bits.add(1)
    for i, j in inventory["coincidences"].get(key, ()):
        ri, rj = residue[i], residue[j]
        need((ri == 0) == (rj == 0), "coincidence changes residue type")
        if ri:
            # Equal nonzero colours: xor=1 for ri*rj=-1, else 0.
            sign_bits.add(int((ri * rj) % 3 == 2))
        else:
            zero_bits.add(0)
    need(len(sign_bits) <= 1, "conflicting sign requirements on one interface")
    need(len(zero_bits) <= 1, "conflicting zero requirements on one interface")
    return (next(iter(sign_bits)) if sign_bits else None,
            next(iter(zero_bits)) if zero_bits else None)


def propagate_parity(order, constraints):
    adjacency = [[] for _ in range(order)]
    for left, right, bit in constraints:
        adjacency[left].append((right, bit))
        adjacency[right].append((left, bit))
    values = [None] * order
    for start in range(order):
        if values[start] is not None:
            continue
        values[start] = 0  # makes the component word lexicographically minimal
        queue = deque([start])
        while queue:
            here = queue.popleft()
            for there, bit in adjacency[here]:
                expected = values[here] ^ bit
                if values[there] is None:
                    values[there] = expected
                    queue.append(there)
                elif values[there] != expected:
                    return None
    return tuple(values)


def placement(phases, inventory, direct_scan=False):
    order = len(phases)
    points = inventory["points"]
    patch_order = len(points)
    pair_keys = {}
    sign_constraints = []
    zero_constraints = []
    active = rational = 0
    for left, right in combinations(range(order), 2):
        delta = phase_product(phase_conjugate(phases[left]), phases[right])
        key = phase_key(delta)
        pair_keys[left, right] = key
        sign_bit, zero_bit = pair_requirements(delta, inventory)
        if sign_bit is not None:
            sign_constraints.append((left, right, sign_bit))
        if zero_bit is not None:
            zero_constraints.append((left, right, zero_bit))
        if key in inventory["events"]:
            active += 1
            rational += int(is_rational_key(key))
    signs = propagate_parity(order, sign_constraints)
    zeros = propagate_parity(order, zero_constraints)
    need(signs is not None, "inconsistent sign cycle")
    need(zeros is not None, "inconsistent zero cycle")

    # Merge equal labels from their exact Cartesian coordinates, not from the
    # target's pairwise coincidence DSU.
    physical_by_coordinate = {}
    image = []
    coordinates = []
    for phase in phases:
        for z in points:
            coordinate = rotate(phase, z)
            key = coordinate_key(coordinate)
            if key not in physical_by_coordinate:
                physical_by_coordinate[key] = len(coordinates)
                coordinates.append(coordinate)
            image.append(physical_by_coordinate[key])

    raw_colours = []
    for layer in range(order):
        multiplier = 1 if signs[layer] == 0 else 2
        for vertex, residue in enumerate(inventory["residue"]):
            if vertex == inventory["origin"]:
                raw_colours.append(0)
            elif residue == 0:
                raw_colours.append(zeros[layer])
            else:
                raw_colours.append(2 if (multiplier * residue) % 3 == 1 else 3)
    colours = [None] * len(coordinates)
    for formal, physical in enumerate(image):
        if colours[physical] is None:
            colours[physical] = raw_colours[formal]
        else:
            need(colours[physical] == raw_colours[formal],
                 "coincident labels have different colours")

    edges = set()
    for layer in range(order):
        for i, j in inventory["seed_edges"]:
            endpoints = image[layer * patch_order + i], image[layer * patch_order + j]
            need(endpoints[0] != endpoints[1], "internal unit edge collapsed")
            edges.add(tuple(sorted(endpoints)))
    for (left, right), key in pair_keys.items():
        contacts = set(inventory["universal"])
        contacts.update(inventory["events"].get(key, ()))
        for i, j in contacts:
            endpoints = image[left * patch_order + i], image[right * patch_order + j]
            need(endpoints[0] != endpoints[1], "cross unit edge collapsed")
            edges.add(tuple(sorted(endpoints)))
    need(all(colours[u] != colours[v] for u, v in edges),
         "constructed four-colouring is improper")

    scanned_pairs = 0
    if direct_scan:
        rebuilt = set()
        for right in range(len(coordinates)):
            for left in range(right):
                scanned_pairs += 1
                if distance_squared(coordinates[left], coordinates[right]) == scalar(1):
                    rebuilt.add((left, right))
        need(rebuilt == edges, "direct physical edge scan disagrees with inventory")

    return {
        "order": len(coordinates), "edges": len(edges), "active": active,
        "rational": rational, "sign_constraints": len(sign_constraints),
        "zero_constraints": len(zero_constraints), "edge_rows": tuple(sorted(edges)),
        "colours": tuple(colours), "direct_pairs": scanned_pairs,
    }


def certify():
    inventory = build_inventory()
    events = inventory["events"]
    classes = sorted({canonical_phase(phase_from_key(key)) for key in events})
    identity_key = canonical_phase(IDENTITY)
    need(all(key in events for key in classes), "canonical representative absent")
    nonidentity = [key for key in classes if key != identity_key]
    phases = {key: phase_from_key(key) for key in classes}

    # Pair consistency is a load-bearing two-cycle condition.  Audit every raw
    # event phase, including phases that never occur in a triangle.
    pair_histogram = Counter(pair_requirements(phase_from_key(key), inventory)
                             for key in events)
    need(pair_requirements(IDENTITY, inventory) == (0, 0),
         "identical patches do not impose palette equality")

    # Directly scan every physical pair for all 99 two-layer event classes.
    two_digest = hashlib.sha256()
    two_orders = Counter()
    two_edges = Counter()
    direct_pairs = 0
    for key in classes:
        row = placement((IDENTITY, phases[key]), inventory, direct_scan=True)
        direct_pairs += row["direct_pairs"]
        two_orders[row["order"]] += 1
        two_edges[row["edges"]] += 1
        update_digest(two_digest, (key, row["edge_rows"], row["colours"]))

    triangle_digest = hashlib.sha256()
    triangle_count = 0
    triangle_stats = Counter()
    for offset, alpha_key in enumerate(nonidentity):
        for beta_key in nonidentity[offset + 1:]:
            relative = phase_product(phase_conjugate(phases[alpha_key]),
                                     phases[beta_key])
            if phase_key(relative) not in events:
                continue
            row = placement((IDENTITY, phases[alpha_key], phases[beta_key]), inventory)
            triangle_count += 1
            triangle_stats[(row["order"], row["edges"], row["rational"],
                            row["sign_constraints"], row["zero_constraints"])] += 1
            update_digest(triangle_digest,
                          (alpha_key, beta_key, row["edge_rows"], row["colours"]))

    # Build the endpoint-incidence map for all normalized length-two walks.
    neighbours = defaultdict(set)
    for alpha_key in nonidentity:
        for step_key in nonidentity:
            target_key = canonical_phase(phase_product(phases[alpha_key],
                                                       phases[step_key]))
            neighbours[target_key].add(alpha_key)
            if target_key not in phases:
                phases[target_key] = phase_from_key(target_key)

    cycle_digest = hashlib.sha256()
    cycle_count = 0
    cycle_stats = Counter()
    cycle_orders = Counter()
    cycle_edges = Counter()
    for target_key in sorted(neighbours):
        if target_key == identity_key:
            continue
        adjacent = sorted(neighbours[target_key])
        for offset, alpha_key in enumerate(adjacent):
            for gamma_key in adjacent[offset + 1:]:
                if len({identity_key, alpha_key, target_key, gamma_key}) != 4:
                    continue
                row = placement((IDENTITY, phases[alpha_key], phases[target_key],
                                 phases[gamma_key]), inventory)
                cycle_count += 1
                cycle_stats[(row["active"], row["rational"],
                             row["sign_constraints"], row["zero_constraints"])] += 1
                cycle_orders[row["order"]] += 1
                cycle_edges[row["edges"]] += 1
                update_digest(cycle_digest, (alpha_key, target_key, gamma_key,
                                             row["edge_rows"], row["colours"]))

    report = {
        "verified": True,
        "review_arithmetic": "exact Fractions with prime-support surds",
        "patch_vertices": len(inventory["points"]),
        "patch_edges": len(inventory["seed_edges"]),
        "p37_vertices": sum(ring_norm((a, b)) <= 37 for a in range(-37, 38)
                            for b in range(-37, 38)),
        "maximum_union_vertices": 4 * len(inventory["points"]) - 3,
        "primitive_contact_lines": len(inventory["lines"]),
        "event_phases": len(events),
        "rational_event_phases": sum(is_rational_key(key) for key in events),
        "irrational_event_phases": sum(not is_rational_key(key) for key in events),
        "event_classes_mod_units": len(classes),
        "rational_event_classes_mod_units": sum(is_rational_key(key) for key in classes),
        "irrational_event_classes_mod_units": sum(not is_rational_key(key) for key in classes),
        "coincidence_phases": len(inventory["coincidences"]),
        "raw_pair_constraint_histogram": {
            f"sign={sign},zero={zero}": count
            for (sign, zero), count in sorted(pair_histogram.items(), key=lambda row: repr(row[0]))
        },
        "two_layer_representatives_directly_scanned": len(classes),
        "two_layer_direct_physical_pairs": direct_pairs,
        "two_layer_order_range": [min(two_orders), max(two_orders)],
        "two_layer_edge_range": [min(two_edges), max(two_edges)],
        "two_layer_certificate_sha256": two_digest.hexdigest(),
        "normalized_active_triangles": triangle_count,
        "triangle_stat_rows": len(triangle_stats),
        "normalized_four_cycles": cycle_count,
        "four_cycle_target_classes": len(neighbours),
        "four_cycle_stat_rows": len(cycle_stats),
        "four_cycle_active_interface_histogram": {
            str(active): sum(count for row, count in cycle_stats.items() if row[0] == active)
            for active in sorted({row[0] for row in cycle_stats})
        },
        "four_cycle_order_range": [min(cycle_orders), max(cycle_orders)],
        "four_cycle_edge_range": [min(cycle_edges), max(cycle_edges)],
        "inventory_sha256": inventory["inventory_sha256"],
        "triangle_certificate_sha256": triangle_digest.hexdigest(),
        "four_cycle_certificate_sha256": cycle_digest.hexdigest(),
    }
    for field, expected in TARGET.items():
        need(report[field] == expected,
             f"target disagreement for {field}: {report[field]!r} != {expected!r}")
    need(report["p37_vertices"] == 139, "P37 size check failed")
    need(report["four_cycle_active_interface_histogram"] ==
         {"4": 5304, "5": 2472, "6": 324}, "active-interface histogram mismatch")
    need(report["four_cycle_order_range"] == [451, 505], "order range mismatch")
    need(report["four_cycle_edge_range"] == [1368, 1446], "edge range mismatch")
    return report


def negative_controls():
    need(propagate_parity(3, ((0, 1, 0), (1, 2, 0), (0, 2, 1))) is None,
         "odd triangle accepted")
    need(propagate_parity(4, ((0, 1, 0), (1, 2, 0), (2, 3, 0), (0, 3, 1))) is None,
         "odd square accepted")
    need(propagate_parity(4, ((0, 1, 1), (1, 2, 0), (2, 3, 1))) is not None,
         "consistent forest rejected")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    negative_controls()
    report = certify()
    output = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.check_expected:
        expected = (HERE / "EXPECTED.json").read_text()
        need(output == expected, "output differs from review EXPECTED.json")
    print(output, end="")


if __name__ == "__main__":
    main()
