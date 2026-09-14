#!/usr/bin/env python3
"""Exact verifier for four concurrent P36 triangular patches.

The program uses only integers, Fractions, and sparse squarefree radicals.
It enumerates every relative rotation at which two patches gain a proper
contact, reduces possible parity obstructions to simple cycles, and checks an
explicit four-colouring on every normalized triangle and four-cycle row.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from math import gcd, isqrt
from pathlib import Path


LIMIT = 36


def require(condition, message):
    if not condition:
        raise ValueError(message)


def norm(z):
    a, b = z
    return a * a + a * b + b * b


def multiply(z, w):
    a, b = z
    c, d = w
    return a * c - b * d, a * d + b * c + b * d


def conjugate(z):
    return z[0] + z[1], -z[1]


def primitive(u, v, k):
    divisor = gcd(gcd(u, v), k)
    require(divisor != 0, "zero contact equation")
    row = u // divisor, v // divisor, k // divisor
    return max(row, tuple(-x for x in row))


def squarefree_root(n):
    require(n > 0, "nonpositive radicand")
    square, radical, left, p = 1, 1, n, 2
    while p * p <= left:
        exponent = 0
        while left % p == 0:
            left //= p
            exponent += 1
        square *= p ** (exponent // 2)
        if exponent % 2:
            radical *= p
        p += 1
    radical *= left
    return square, radical


def rad(value=0):
    value = F(value)
    return {} if value == 0 else {1: value}


def rad_add(left, right):
    answer = dict(left)
    for basis, coefficient in right.items():
        answer[basis] = answer.get(basis, F(0)) + coefficient
        if answer[basis] == 0:
            del answer[basis]
    return answer


def rad_neg(value):
    return {basis: -coefficient for basis, coefficient in value.items()}


def rad_scale(value, scalar):
    scalar = F(scalar)
    return {basis: coefficient * scalar for basis, coefficient in value.items()
            if coefficient * scalar}


def rad_mul(left, right):
    answer = {}
    for a, x in left.items():
        for b, y in right.items():
            common = gcd(a, b)
            basis = (a // common) * (b // common)
            answer[basis] = answer.get(basis, F(0)) + x * y * common
    return {basis: coefficient for basis, coefficient in answer.items() if coefficient}


def rad_key(value):
    return tuple((basis, coefficient.numerator, coefficient.denominator)
                 for basis, coefficient in sorted(value.items()))


def phase_key(phase):
    return rad_key(phase[0]), rad_key(phase[1])


def phase_from_key(key):
    return tuple({basis: F(numerator, denominator)
                  for basis, numerator, denominator in coordinate}
                 for coordinate in key)


def phase_conjugate(phase):
    return phase[0], rad_neg(phase[1])


def phase_multiply(left, right):
    # (x+i*sqrt(3)y)(u+i*sqrt(3)v)
    x, y = left
    u, v = right
    return (rad_add(rad_mul(x, u), rad_scale(rad_mul(y, v), -3)),
            rad_add(rad_mul(x, v), rad_mul(y, u)))


def rational_phase(x, y):
    return rad(F(x)), rad(F(y))


def is_rational_key(key):
    return all(basis == 1 for coordinate in key for basis, _, _ in coordinate)


def line_roots(line):
    u, v, k = line
    scale = 3 * u * u + v * v
    discriminant = scale - 3 * k * k
    require(discriminant >= 0, "nonintersecting contact line")
    root = isqrt(discriminant)
    if root * root == discriminant:
        signs = (1,) if discriminant == 0 else (-1, 1)
        return [rational_phase(F(3 * u * k + sign * v * root, scale),
                               F(v * k - sign * u * root, scale))
                for sign in signs]
    factor, basis = squarefree_root(discriminant)
    roots = []
    for sign in (-1, 1):
        x = rad_add(rad(F(3 * u * k, scale)),
                    {basis: F(sign * v * factor, scale)})
        y = rad_add(rad(F(v * k, scale)),
                    {basis: F(-sign * u * factor, scale)})
        roots.append((x, y))
    return roots


def rotate_cartesian(phase, z):
    # Eisenstein z=a+b*omega has Cartesian form x+i*sqrt(3)y.
    x, y = phase
    u, v = F(2 * z[0] + z[1], 2), F(z[1], 2)
    return rad_add(rad_scale(x, u), rad_scale(y, -3 * v)), \
        rad_add(rad_scale(y, u), rad_scale(x, v))


def squared_distance(z, phase, w):
    moved_x, moved_y = rotate_cartesian(phase, w)
    zx, zy = F(2 * z[0] + z[1], 2), F(z[1], 2)
    dx = rad_add(rad(zx), rad_neg(moved_x))
    dy = rad_add(rad(zy), rad_neg(moved_y))
    return rad_add(rad_mul(dx, dx), rad_scale(rad_mul(dy, dy), 3))


class DSU:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, value):
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left, right):
        left, right = self.find(left), self.find(right)
        if left != right:
            self.parent[right] = left


def build_inventory():
    bound = isqrt(4 * LIMIT // 3)
    points = sorted((a, b) for a in range(-bound, bound + 1)
                    for b in range(-bound, bound + 1) if norm((a, b)) <= LIMIT)
    origin = points.index((0, 0))
    residues = [(a - b) % 3 for a, b in points]
    seed_edges = [(i, j) for i, z in enumerate(points)
                  for j, w in enumerate(points[:i])
                  if norm((z[0] - w[0], z[1] - w[1])) == 1]
    require(all(residues[i] != residues[j] for i, j in seed_edges),
            "residue colouring fails internally")

    lines = defaultdict(set)
    universal = set()
    for i, z in enumerate(points):
        for j, w in enumerate(points):
            k = norm(z) + norm(w) - 1
            if i == origin or j == origin:
                if k == 0:
                    universal.add((i, j))
                continue
            a, b = multiply(w, conjugate(z))
            u, v = 2 * a + b, -3 * b
            if 3 * k * k <= 3 * u * u + v * v:
                lines[primitive(u, v, k)].add((i, j))

    events = {}
    for line, contacts in sorted(lines.items()):
        for phase in line_roots(line):
            key = phase_key(phase)
            events.setdefault(key, set()).update(contacts)

    coincidences = defaultdict(set)
    for i, z in enumerate(points):
        if i == origin:
            continue
        for j, w in enumerate(points):
            denominator = norm(w)
            if denominator and norm(z) == denominator:
                a, b = multiply(z, conjugate(w))
                phase = rational_phase(F(2 * a + b, 2 * denominator),
                                       F(b, 2 * denominator))
                coincidences[phase_key(phase)].add((i, j))
    require(set(coincidences) <= set(events), "coincidence-only phase omitted")

    # Check every stored geometric assertion independently in Cartesian form.
    for key, contacts in events.items():
        phase = phase_from_key(key)
        require(phase_key(phase_multiply(phase, phase_conjugate(phase))) ==
                phase_key(rational_phase(1, 0)), "event phase is not unit")
        for i, j in contacts:
            require(squared_distance(points[i], phase, points[j]) == rad(1),
                    "declared contact is not a unit edge")
    for key, pairs in coincidences.items():
        phase = phase_from_key(key)
        for i, j in pairs:
            require(rotate_cartesian(phase, points[j]) ==
                    (rad(F(2 * points[i][0] + points[i][1], 2)),
                     rad(F(points[i][1], 2))), "declared coincidence is false")

    return {
        "points": points,
        "origin": origin,
        "residues": residues,
        "seed_edges": seed_edges,
        "universal": universal,
        "lines": lines,
        "events": events,
        "coincidences": coincidences,
    }


UNITS = [rational_phase(*xy) for xy in (
    (F(1), F(0)), (F(1, 2), F(1, 2)), (F(-1, 2), F(1, 2)),
    (F(-1), F(0)), (F(-1, 2), F(-1, 2)), (F(1, 2), F(-1, 2)),
)]


def canonical_phase(phase):
    return min(phase_key(phase_multiply(phase, unit)) for unit in UNITS)


def pair_constraints(delta, inventory):
    """Return optional XOR bits for sign palettes and zero palettes."""
    key = phase_key(delta)
    residues = inventory["residues"]
    sign_products, zero_bits = set(), set()
    for i, j in inventory["events"].get(key, ()):
        ri, rj = residues[i], residues[j]
        if ri and rj:
            sign_products.add(2 * ri * rj % 3)  # s_i*s_j=-ri*rj
        elif ri == rj == 0:
            zero_bits.add(1)
    for i, j in inventory["coincidences"].get(key, ()):
        ri, rj = residues[i], residues[j]
        require((ri == 0) == (rj == 0), "coincidence changes residue type")
        if ri:
            sign_products.add(ri * rj % 3)  # equal physical colours
        else:
            zero_bits.add(0)
    require(len(sign_products) <= 1, "inconsistent pair sign requirements")
    require(len(zero_bits) <= 1, "inconsistent pair zero requirements")
    sign_bit = None
    if sign_products:
        sign_bit = 0 if next(iter(sign_products)) == 1 else 1
    zero_bit = None if not zero_bits else next(iter(zero_bits))
    return sign_bit, zero_bit


def solve_xor(order, constraints):
    for word in product(range(2), repeat=order):
        if all((word[i] ^ word[j]) == bit for i, j, bit in constraints):
            return word
    return None


def check_placement(phases, inventory):
    order = len(phases)
    points = inventory["points"]
    patch_order = len(points)
    origin = inventory["origin"]
    sign_constraints, zero_constraints = [], []
    pair_keys = {}
    rational_interfaces = active_interfaces = 0
    for left, right in combinations(range(order), 2):
        delta = phase_multiply(phase_conjugate(phases[left]), phases[right])
        key = phase_key(delta)
        pair_keys[left, right] = key
        sign_bit, zero_bit = pair_constraints(delta, inventory)
        if sign_bit is not None:
            sign_constraints.append((left, right, sign_bit))
        if zero_bit is not None:
            zero_constraints.append((left, right, zero_bit))
        if key in inventory["events"]:
            active_interfaces += 1
            rational_interfaces += int(is_rational_key(key))
    sign_word = solve_xor(order, sign_constraints)
    zero_word = solve_xor(order, zero_constraints)
    require(sign_word is not None, "inconsistent sign cycle")
    require(zero_word is not None, "inconsistent zero cycle")

    dsu = DSU(order * patch_order)
    for layer in range(1, order):
        dsu.union(origin, layer * patch_order + origin)
    for (left, right), key in pair_keys.items():
        for i, j in inventory["coincidences"].get(key, ()):
            dsu.union(left * patch_order + i, right * patch_order + j)
    roots = sorted({dsu.find(v) for v in range(order * patch_order)})
    quotient = {root: i for i, root in enumerate(roots)}
    image = [quotient[dsu.find(v)] for v in range(order * patch_order)]

    raw_colours = []
    for layer in range(order):
        multiplier = 1 if sign_word[layer] == 0 else 2
        for vertex, residue in enumerate(inventory["residues"]):
            if vertex == origin:
                raw_colours.append(0)
            elif residue == 0:
                raw_colours.append(zero_word[layer])
            else:
                raw_colours.append(2 if multiplier * residue % 3 == 1 else 3)
    colours = [None] * len(roots)
    for formal, physical in enumerate(image):
        if colours[physical] is None:
            colours[physical] = raw_colours[formal]
        else:
            require(colours[physical] == raw_colours[formal],
                    "coincident labels receive different colours")

    edges = set()
    for layer in range(order):
        for i, j in inventory["seed_edges"]:
            u, w = image[layer * patch_order + i], image[layer * patch_order + j]
            require(u != w, "internal unit edge collapsed")
            edges.add(tuple(sorted((u, w))))
    for (left, right), key in pair_keys.items():
        contacts = set(inventory["universal"])
        contacts.update(inventory["events"].get(key, ()))
        for i, j in contacts:
            u = image[left * patch_order + i]
            w = image[right * patch_order + j]
            require(u != w, "cross unit edge collapsed")
            edges.add(tuple(sorted((u, w))))
    require(all(colours[u] != colours[w] for u, w in edges),
            "explicit physical four-colouring is improper")
    return {
        "order": len(roots),
        "edges": len(edges),
        "active": active_interfaces,
        "rational": rational_interfaces,
        "sign_constraints": len(sign_constraints),
        "zero_constraints": len(zero_constraints),
        "edge_rows": tuple(sorted(edges)),
        "colours": tuple(colours),
    }


def update_hash(digest, value):
    digest.update(repr(value).encode("ascii"))
    digest.update(b"\n")


def certify():
    inventory = build_inventory()
    events = inventory["events"]
    event_classes = sorted({canonical_phase(phase_from_key(key)) for key in events})
    identity = canonical_phase(rational_phase(1, 0))
    nonidentity = [key for key in event_classes if key != identity]
    phases = {key: phase_from_key(key) for key in event_classes}
    phases[identity] = phase_from_key(identity)
    require(all(key in events for key in event_classes),
            "canonical unit representative missing from events")

    inventory_digest = hashlib.sha256()
    for key in sorted(events):
        update_hash(inventory_digest, (key, tuple(sorted(events[key])),
                                       tuple(sorted(inventory["coincidences"].get(key, ())))))

    triangle_count = 0
    triangle_stats = Counter()
    triangle_digest = hashlib.sha256()
    for offset, alpha_key in enumerate(nonidentity):
        for beta_key in nonidentity[offset + 1:]:
            relative = phase_multiply(phase_conjugate(phases[alpha_key]),
                                      phases[beta_key])
            if phase_key(relative) not in events:
                continue
            placement = (rational_phase(1, 0), phases[alpha_key], phases[beta_key])
            row = check_placement(placement, inventory)
            triangle_count += 1
            triangle_stats[(row["order"], row["edges"], row["rational"],
                            row["sign_constraints"], row["zero_constraints"])] += 1
            update_hash(triangle_digest, (alpha_key, beta_key, row["edge_rows"],
                                          row["colours"]))

    # If 1--a--t--c--1 is an active four-cycle, then t belongs both to
    # a*E and c*E modulo multiplication by a sixth root of unity.
    neighbours = defaultdict(set)
    for alpha_key in nonidentity:
        for step_key in nonidentity:
            target = canonical_phase(phase_multiply(phases[alpha_key],
                                                    phases[step_key]))
            neighbours[target].add(alpha_key)
            phases.setdefault(target, phase_from_key(target))

    four_cycle_count = 0
    cycle_stats = Counter()
    order_histogram, edge_histogram = Counter(), Counter()
    cycle_digest = hashlib.sha256()
    for target_key in sorted(neighbours):
        if target_key == identity:
            continue
        adjacent = sorted(neighbours[target_key])
        for offset, alpha_key in enumerate(adjacent):
            for gamma_key in adjacent[offset + 1:]:
                if len({identity, alpha_key, target_key, gamma_key}) < 4:
                    continue
                placement = (rational_phase(1, 0), phases[alpha_key],
                             phases[target_key], phases[gamma_key])
                row = check_placement(placement, inventory)
                four_cycle_count += 1
                cycle_stats[(row["active"], row["rational"],
                             row["sign_constraints"], row["zero_constraints"])] += 1
                order_histogram[row["order"]] += 1
                edge_histogram[row["edges"]] += 1
                update_hash(cycle_digest, (alpha_key, target_key, gamma_key,
                                           row["edge_rows"], row["colours"]))

    require(triangle_count > 0 and four_cycle_count > 0, "empty cycle census")
    require(max(key[0] for key in cycle_stats) == 6,
            "fully active four-patch controls missing")

    rational_events = sum(is_rational_key(key) for key in events)
    rational_classes = sum(is_rational_key(key) for key in event_classes)
    return {
        "verified": True,
        "arithmetic": "exact integers, Fractions, sparse squarefree radicals",
        "norm_limit": LIMIT,
        "patch_vertices": len(inventory["points"]),
        "patch_edges": len(inventory["seed_edges"]),
        "maximum_union_vertices": 4 * len(inventory["points"]) - 3,
        "primitive_contact_lines": len(inventory["lines"]),
        "event_phases": len(events),
        "rational_event_phases": rational_events,
        "irrational_event_phases": len(events) - rational_events,
        "event_classes_mod_units": len(event_classes),
        "rational_event_classes_mod_units": rational_classes,
        "irrational_event_classes_mod_units": len(event_classes) - rational_classes,
        "coincidence_phases": len(inventory["coincidences"]),
        "normalized_active_triangles": triangle_count,
        "triangle_stat_rows": len(triangle_stats),
        "normalized_four_cycles": four_cycle_count,
        "four_cycle_target_classes": len(neighbours),
        "four_cycle_stat_rows": len(cycle_stats),
        "four_cycle_active_interface_histogram": {
            str(active): sum(count for row, count in cycle_stats.items() if row[0] == active)
            for active in sorted({row[0] for row in cycle_stats})
        },
        "four_cycle_order_range": [min(order_histogram), max(order_histogram)],
        "four_cycle_edge_range": [min(edge_histogram), max(edge_histogram)],
        "inventory_sha256": inventory_digest.hexdigest(),
        "triangle_certificate_sha256": triangle_digest.hexdigest(),
        "four_cycle_certificate_sha256": cycle_digest.hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    report = certify()
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.check_expected:
        expected = Path(__file__).with_name("EXPECTED.json").read_text()
        require(text == expected, "output differs from EXPECTED.json")
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
