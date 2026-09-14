#!/usr/bin/env python3
"""Exact solver-free verifier for the three-triangular-patch contact gate."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations
import json
from math import gcd, isqrt


LIMIT = 48


def require(test, message):
    if not test:
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
    """Return q,d with sqrt(n)=q*sqrt(d) and d squarefree."""
    require(n > 0, "positive radicand")
    square, radical = 1, 1
    p = 2
    left = n
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


def line_roots(line):
    u, v, k = line
    scale = 3 * u * u + v * v
    discriminant = scale - 3 * k * k
    require(discriminant >= 0, "nonintersecting line")
    root = isqrt(discriminant)
    if root * root == discriminant:
        signs = (1,) if discriminant == 0 else (-1, 1)
        return [(rational_phase(F(3 * u * k + sign * v * root, scale),
                                F(v * k - sign * u * root, scale)), True)
                for sign in signs]
    factor, basis = squarefree_root(discriminant)
    roots = []
    for sign in (-1, 1):
        x = rad(F(3 * u * k, scale))
        x = rad_add(x, {basis: F(sign * v * factor, scale)})
        y = rad(F(v * k, scale))
        y = rad_add(y, {basis: F(-sign * u * factor, scale)})
        roots.append(((x, y), False))
    return roots


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


def reduce_mod_three(value):
    value = F(value)
    require(value.denominator % 3 != 0, "denominator divisible by three")
    return value.numerator * pow(value.denominator, -1, 3) % 3


def build_inventory():
    bound = isqrt(4 * LIMIT // 3)
    points = sorted((a, b) for a in range(-bound, bound + 1)
                    for b in range(-bound, bound + 1) if norm((a, b)) <= LIMIT)
    origin = points.index((0, 0))
    residues = [(a - b) % 3 for a, b in points]
    seed_edges = [(i, j) for i, z in enumerate(points)
                  for j, w in enumerate(points[:i])
                  if norm((z[0] - w[0], z[1] - w[1])) == 1]
    lines = defaultdict(list)
    universal = []
    for i, z in enumerate(points):
        for j, w in enumerate(points):
            k = norm(z) + norm(w) - 1
            if i == origin or j == origin:
                if k == 0:
                    universal.append((i, j))
                continue
            a, b = multiply(w, conjugate(z))
            u, v = 2 * a + b, -3 * b
            if 3 * k * k <= 3 * u * u + v * v:
                lines[primitive(u, v, k)].append((i, j))

    events = {}
    four_phases = []
    four_lines = 0
    for line, contacts in sorted(lines.items()):
        zero_zero = any(residues[i] == residues[j] == 0 for i, j in contacts)
        nonzero_nonzero = any(residues[i] and residues[j] for i, j in contacts)
        roots = line_roots(line)
        if zero_zero:
            require(not nonzero_nonzero,
                    "four-phase line also has a nonzero-to-nonzero contact")
            require(all(not rational for _phase, rational in roots),
                    "rational zero-to-zero contact phase")
            four_lines += 1
        for phase, rational in roots:
            key = phase_key(phase)
            if rational:
                row = events.setdefault(key, {"rational": True, "contacts": set()})
                require(row["rational"], "rational/irrational phase collision")
                row["contacts"].update(contacts)
            else:
                require(key not in events, "duplicate irrational contact phase")
                events[key] = {"rational": False, "contacts": set(contacts)}
            if zero_zero:
                four_phases.append(phase)

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
    require(len(four_phases) == len({phase_key(x) for x in four_phases}),
            "duplicate four-chromatic phase")
    return points, residues, seed_edges, universal, events, coincidences, four_phases, four_lines


def exact_family_check(points, residues, seed_edges, universal, events,
                       coincidences, four_phases):
    patch_order = len(points)
    origin = points.index((0, 0))
    order_histogram = Counter()
    edge_histogram = Counter()
    relative_kind = Counter()
    candidate_count = 0

    for alpha, beta in combinations(four_phases, 2):
        candidate_count += 1
        relative = phase_multiply(phase_conjugate(alpha), beta)
        relative_key = phase_key(relative)
        relative_event = events.get(relative_key)
        if relative_event is None:
            relative_kind["generic"] += 1
        else:
            require(relative_event["rational"],
                    "relative irrational contact between four-phases")
            relative_kind["rational"] += 1

        phases = [rational_phase(1, 0), alpha, beta]
        dsu = DSU(3 * patch_order)
        dsu.union(origin, patch_order + origin)
        dsu.union(origin, 2 * patch_order + origin)
        pair_data = {}
        for left, right in combinations(range(3), 2):
            delta = phase_multiply(phase_conjugate(phases[left]), phases[right])
            delta_key = phase_key(delta)
            event = events.get(delta_key)
            pair_data[left, right] = event
            for i, j in coincidences.get(delta_key, ()):
                dsu.union(left * patch_order + i, right * patch_order + j)

        roots = sorted({dsu.find(v) for v in range(3 * patch_order)})
        quotient = {root: i for i, root in enumerate(roots)}
        image = [quotient[dsu.find(v)] for v in range(3 * patch_order)]
        edges = set()
        for layer in range(3):
            for i, j in seed_edges:
                u, v = image[layer * patch_order + i], image[layer * patch_order + j]
                require(u != v, "unit edge collapsed")
                edges.add(tuple(sorted((u, v))))
        for left, right in combinations(range(3), 2):
            contacts = list(universal)
            if pair_data[left, right] is not None:
                contacts += list(pair_data[left, right]["contacts"])
            for i, j in contacts:
                u = image[left * patch_order + i]
                v = image[right * patch_order + j]
                require(u != v, "cross unit edge collapsed")
                edges.add(tuple(sorted((u, v))))

        # Construct the four-colouring.  The base zero class is A; the two
        # moved zero classes are B.  Their base contacts contain no pair of
        # nonzero residues.  If their relative phase is rational, use its
        # extended F_3 residue on both moved patches; otherwise there are no
        # nonuniversal contacts between them.
        relative_residue = 1
        if relative_event is not None:
            x_terms, y_terms = relative
            require(set(x_terms) <= {1} and set(y_terms) <= {1},
                    "rational event has radical coefficients")
            x = x_terms.get(1, F(0))
            y = y_terms.get(1, F(0))
            relative_residue = reduce_mod_three(x - 3 * y)
            require(relative_residue in (1, 2), "zero rational phase residue")
        raw_colours = []
        raw_colours.extend(0 if residue == 0 else residue + 1 for residue in residues)
        for layer_factor in (1, relative_residue):
            for vertex, residue in enumerate(residues):
                if vertex == origin:
                    raw_colours.append(0)
                elif residue == 0:
                    raw_colours.append(1)
                else:
                    raw_colours.append((layer_factor * residue) % 3 + 1)
        colours = [None] * len(roots)
        for formal, vertex in enumerate(image):
            if colours[vertex] is None:
                colours[vertex] = raw_colours[formal]
            else:
                require(colours[vertex] == raw_colours[formal],
                        "coincident labels receive different colours")
        require(all(colours[u] != colours[v] for u, v in edges),
                "improper explicit four-colouring")
        order_histogram[len(roots)] += 1
        edge_histogram[len(edges)] += 1

    return {
        "candidate_count": candidate_count,
        "relative_kind_histogram": dict(sorted(relative_kind.items())),
        "order_histogram": dict(sorted(order_histogram.items())),
        "edge_histogram": dict(sorted(edge_histogram.items())),
    }


def certify():
    (points, residues, seed_edges, universal, events, coincidences,
     four_phases, four_lines) = build_inventory()
    family = exact_family_check(points, residues, seed_edges, universal,
                                events, coincidences, four_phases)
    report = {
        "verified": True,
        "arithmetic": "exact integers, Fractions, and sparse squarefree radicals",
        "norm_limit": LIMIT,
        "patch_vertices": len(points),
        "patch_edges": len(seed_edges),
        "maximum_support_vertices": 3 * len(points) - 2,
        "contact_lines": len({}),
        "four_phase_lines": four_lines,
        "four_phase_orientations": len(four_phases),
        **family,
    }
    # The contact-line count is computed without retaining a second copy in
    # the family checker.  Rebuild only this inexpensive scalar.
    lines = set()
    origin = points.index((0, 0))
    for i, z in enumerate(points):
        for j, w in enumerate(points):
            if i == origin or j == origin:
                continue
            k = norm(z) + norm(w) - 1
            a, b = multiply(w, conjugate(z))
            u, v = 2 * a + b, -3 * b
            if 3 * k * k <= 3 * u * u + v * v:
                lines.add(primitive(u, v, k))
    report["contact_lines"] = len(lines)
    return report


if __name__ == "__main__":
    print(json.dumps(certify(), indent=2, sort_keys=True))
