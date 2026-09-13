#!/usr/bin/env python3
"""Independent finite audit and exact geometric controls for the theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, deque
from fractions import Fraction
from itertools import product
from pathlib import Path


PAIR4 = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PAIR3 = ((0, 1), (0, 2), (1, 2))
RADICANDS = (2, 3, 11)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def mask_edges(mask, pairs):
    return {p for k, p in enumerate(pairs) if mask >> k & 1}


def is_complete_bipartite_union(mask: int, n: int, pairs) -> bool:
    """Recognize parity-conflict graphs without enumerating partitions."""
    edges = mask_edges(mask, pairs)
    neighbours = [set() for _ in range(n)]
    for i, j in edges:
        neighbours[i].add(j)
        neighbours[j].add(i)
    unseen = set(range(n))
    while unseen:
        root = min(unseen)
        color = {root: 0}
        queue = deque([root])
        component = set()
        while queue:
            u = queue.popleft()
            component.add(u)
            for v in neighbours[u]:
                if v not in color:
                    color[v] = 1 - color[u]
                    queue.append(v)
                elif color[v] == color[u]:
                    return False
        unseen -= component
        left = {v for v in component if color[v] == 0}
        right = component - left
        if any((min(u, v), max(u, v)) not in edges for u in left for v in right):
            return False
    return True


def count_allocations(n, a_mask, c_mask, pairs, forced_a=()):
    answers = []
    ea = mask_edges(a_mask, pairs)
    ec = mask_edges(c_mask, pairs)
    for word in product((0, 1), repeat=n):
        if any(word[v] != 1 for v in forced_a):
            continue
        if any(word[i] == word[j] == 1 for i, j in ea):
            continue
        if any(word[i] == word[j] == 0 for i, j in ec):
            continue
        answers.append(word)
    return answers


class MQ:
    """Q(sqrt(2),sqrt(3),sqrt(11)) in its eight-element product basis."""

    __slots__ = ("c",)

    def __init__(self, *coeffs):
        values = list(coeffs) + [0] * (8 - len(coeffs))
        require(len(values) == 8, "bad multiquadratic length")
        self.c = tuple(Fraction(v) for v in values)

    @staticmethod
    def rational(value):
        return MQ(value)

    def __add__(self, other):
        other = as_mq(other)
        return MQ(*(a + b for a, b in zip(self.c, other.c)))

    __radd__ = __add__

    def __neg__(self):
        return MQ(*(-a for a in self.c))

    def __sub__(self, other):
        return self + (-as_mq(other))

    def __rsub__(self, other):
        return as_mq(other) - self

    def __mul__(self, other):
        other = as_mq(other)
        out = [Fraction(0) for _ in range(8)]
        for m, a in enumerate(self.c):
            if not a:
                continue
            for n, b in enumerate(other.c):
                if not b:
                    continue
                factor = 1
                common = m & n
                for bit, radicand in enumerate(RADICANDS):
                    if common >> bit & 1:
                        factor *= radicand
                out[m ^ n] += a * b * factor
        return MQ(*out)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Fraction(other)
        return MQ(*(a / other for a in self.c))

    def __eq__(self, other):
        return self.c == as_mq(other).c

    def __hash__(self):
        return hash(self.c)

    def key(self):
        return tuple((x.numerator, x.denominator) for x in self.c)


def as_mq(value):
    return value if isinstance(value, MQ) else MQ.rational(value)


class Point:
    __slots__ = ("x", "y")

    def __init__(self, x=0, y=0):
        self.x, self.y = as_mq(x), as_mq(y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __sub__(self, other):
        return self + (-other)

    def scale(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def key(self):
        return (self.x.key(), self.y.key())


ONE = MQ(1)
S2 = MQ(0, 1)
S3 = MQ(0, 0, 1)
S6 = MQ(0, 0, 0, 1)
S11 = MQ(0, 0, 0, 0, 1)
S33 = MQ(0, 0, 0, 0, 0, 0, 1)
OMEGA = Point(Fraction(1, 2), S3 / 2)


def norm2(point):
    return point.x * point.x + point.y * point.y


def rotate_omega(point):
    return Point(point.x / 2 - point.y * S3 / 2, point.x * S3 / 2 + point.y / 2)


def orbit_with_exponents(direction):
    values = []
    current = direction
    for k in range(6):
        values.append((current, k))
        current = rotate_omega(current)
    require(current == direction, "omega does not have order six")
    require(len({p for p, _ in values}) == 6, "unit orbit collapsed")
    return values


def canonical_orbit(direction):
    values = orbit_with_exponents(direction)
    key_point, key_exponent = min(values, key=lambda item: item[0].key())
    # direction rotated by -key_exponent is the canonical point, so the
    # exponent taking the canonical point back to direction is key_exponent.
    return key_point, (-key_exponent) % 6


def relation_exponent(first, second):
    current = first
    for k in range(6):
        if current == second:
            return k
        current = rotate_omega(current)
    return None


def make_samples():
    zero = Point()
    one = Point(1, 0)
    # Both centre separations are sqrt(3).
    c_double = Point(Fraction(1, 2), S11 / 2)
    double_points = [
        (frozenset((0,)), Point(Fraction(1, 4) - S33 / 12, S11 / 4 + S3 / 12)),
        (frozenset((0,)), Point(Fraction(1, 4) + S33 / 12, S11 / 4 - S3 / 12)),
        (frozenset((1,)), Point(Fraction(3, 4) - S33 / 12, S11 / 4 - S3 / 12)),
        (frozenset((1,)), Point(Fraction(3, 4) + S33 / 12, S11 / 4 + S3 / 12)),
    ]

    # Exactly the 0-pair is at separation sqrt(3); the 1-pair is at sqrt(2).
    c_one = Point(1, S2)
    one_points = [
        (frozenset((0,)), Point(Fraction(1, 2) - S6 / 6, S2 / 2 + S3 / 6)),
        (frozenset((0,)), Point(Fraction(1, 2) + S6 / 6, S2 / 2 - S3 / 6)),
        (frozenset((1,)), Point(1 - S2 / 2, S2 / 2)),
        (frozenset((1,)), Point(1 + S2 / 2, S2 / 2)),
    ]

    # omega is triple-owned; the other intersections are i and 1+i.
    c_triple = Point(Fraction(1, 2), 1 + S3 / 2)
    triple_points = [
        (frozenset((0, 1)), OMEGA),
        (frozenset((0,)), Point(0, 1)),
        (frozenset((1,)), Point(1, 1)),
    ]
    return [
        ("double_bad", (zero, one, c_double), double_points),
        ("one_bad", (zero, one, c_one), one_points),
        ("one_triple", (zero, one, c_triple), triple_points),
    ]


def conflict_masks(centres, mixed):
    c = centres[2]
    a_mask = c_mask = 0
    pairs = tuple((i, j) for i in range(len(mixed)) for j in range(i + 1, len(mixed)))
    for bit, (r, s) in enumerate(pairs):
        owners_r, p = mixed[r]
        owners_s, q = mixed[s]
        i, j = min(owners_r), min(owners_s)
        ka = relation_exponent(p - centres[i], q - centres[j])
        if ka is not None and ((j - i + ka) & 1):
            a_mask |= 1 << bit
        if len(owners_r) == len(owners_s) == 1:
            kc = relation_exponent(p - c, q - c)
            if kc is not None and ((j - i + kc) & 1):
                c_mask |= 1 << bit
    return pairs, a_mask, c_mask


def verify_mixed_points(centres, mixed):
    zero, one, c = centres
    for owners, p in mixed:
        require(norm2(p - c) == ONE, "mixed point misses third circle")
        actual = frozenset(i for i, a in enumerate((zero, one)) if norm2(p - a) == ONE)
        require(actual == owners, "wrong A ownership")
    # Completeness is elementary: each listed centre pair has two incidences,
    # counted with a triple point twice.
    require(sum(len(owners) for owners, _ in mixed) == 4, "wrong intersection incidence count")


def allocation_for_sample(centres, mixed):
    pairs, a_mask, c_mask = conflict_masks(centres, mixed)
    forced = tuple(i for i, (owners, _) in enumerate(mixed) if len(owners) == 2)
    answers = count_allocations(len(mixed), a_mask, c_mask, pairs, forced)
    require(answers, "sample palette system is unsatisfiable")
    return pairs, a_mask, c_mask, answers[0], len(answers)


def patch_audit(centres, mixed, allocation):
    a_centres = centres[:2]
    c = centres[2]
    phase_a = {}
    phase_c = {}

    def impose(table, key, value):
        if key in table:
            require(table[key] == value, "incompatible phase prescription")
        table[key] = value

    for index, ((owners, point), use_a) in enumerate(zip(mixed, allocation)):
        i = min(owners)
        if use_a:
            key, exponent = canonical_orbit(point - a_centres[i])
            impose(phase_a, key, (1 - i - exponent) & 1)
        else:
            require(len(owners) == 1, "triple-owned point assigned C")
            key, exponent = canonical_orbit(point - c)
            impose(phase_c, key, (1 - i - exponent) & 1)

    directions_a = set()
    directions_c = set()
    for owners, point in mixed:
        for i in owners:
            directions_a.update(p for p, _ in orbit_with_exponents(point - a_centres[i]))
        directions_c.update(p for p, _ in orbit_with_exponents(point - c))
    points = set(centres)
    for a in a_centres:
        points.update(a + d for d in directions_a)
    points.update(c + d for d in directions_c)
    ordered = sorted(points, key=Point.key)
    mixed_index = {point: k for k, (_, point) in enumerate(mixed)}

    colors = {}
    for point in ordered:
        if point == a_centres[0]:
            colors[point] = 2
            continue
        if point == a_centres[1]:
            colors[point] = 3
            continue
        if point == c:
            colors[point] = 0
            continue
        owners_a = [i for i, a in enumerate(a_centres) if norm2(point - a) == ONE]
        owner_c = norm2(point - c) == ONE
        require(owners_a or owner_c, "patch point has no owner")
        if owners_a and owner_c:
            require(point in mixed_index, "mixed-point list is incomplete")
            use_a = allocation[mixed_index[point]]
        else:
            use_a = bool(owners_a)
        if use_a:
            i = min(owners_a)
            key, exponent = canonical_orbit(point - a_centres[i])
            colors[point] = (phase_a.get(key, 0) + i + exponent) & 1
        else:
            key, exponent = canonical_orbit(point - c)
            colors[point] = 2 + ((phase_c.get(key, 0) + exponent) & 1)

    edges = []
    for i, p in enumerate(ordered):
        for j in range(i + 1, len(ordered)):
            q = ordered[j]
            if norm2(p - q) == ONE:
                require(colors[p] != colors[q], "monochromatic exact patch edge")
                edges.append((i, j))
    stream = "".join(f"{i},{j}\n" for i, j in edges).encode()
    word = "".join(str(colors[p]) for p in ordered)
    return {
        "vertices": len(ordered),
        "edges": len(edges),
        "colors_sha256": hashlib.sha256((word + "\n").encode()).hexdigest(),
        "edges_sha256": hashlib.sha256(stream).hexdigest(),
    }


def independent_combinatorial_audit(certificate):
    parity = [mask for mask in range(64) if is_complete_bipartite_union(mask, 4, PAIR4)]
    require(len(parity) == certificate["distinct_parity_conflict_graphs_4"], "parity graph count")
    histogram = Counter()
    unsat = []
    admissible = 0
    for a_mask in parity:
        for c_mask in parity:
            if bool(a_mask & 1) != bool(c_mask & 1) or bool(a_mask & 32) != bool(c_mask & 32):
                continue
            admissible += 1
            answers = count_allocations(4, a_mask, c_mask, PAIR4)
            histogram[len(answers)] += 1
            if not answers:
                unsat.append({"a_mask": a_mask, "c_mask": c_mask})
    require(admissible == certificate["admissible_no_triple_graph_pairs"], "admissible pair count")
    require({str(k): histogram[k] for k in sorted(histogram)} == certificate["allocation_count_histogram"], "histogram")
    require(unsat == certificate["unsat_no_triple"], "no-triple exceptions")

    triple_histogram = Counter()
    triple_unsat = []
    for a_mask in range(8):
        for c_mask in (0, 4):
            answers = count_allocations(3, a_mask, c_mask, PAIR3, forced_a=(0,))
            triple_histogram[len(answers)] += 1
            if not answers:
                triple_unsat.append({"a_mask": a_mask, "c_mask": c_mask})
    require({str(k): triple_histogram[k] for k in sorted(triple_histogram)} == certificate["triple_allocation_count_histogram"], "triple histogram")
    require(triple_unsat == certificate["unsat_one_triple"], "triple exceptions")
    return parity, admissible, histogram, triple_histogram


def exact_exception_audit():
    # If both intersection pairs have odd internal phase, both centre
    # separations have square 3.  Subtraction gives x=1/2 and y^2=11/4.
    x = Fraction(1, 2)
    y2 = Fraction(11, 4)
    require(x * x + y2 == 3 and (x - 1) ** 2 + y2 == 3, "double-bad locus")
    cos_delta = Fraction(5, 6)
    require(Fraction(1, 2) < cos_delta < 1, "exceptional angle interval")
    # Cross owner-relative and third-circle direction differences are delta,
    # delta+pi/3, or delta-pi/3.  Their cosines cannot be 1 or -1/2,
    # the even sixth-root values.  Pairs are encoded as a+b*sqrt(33).
    cross_cosines = ((Fraction(5, 6), 0), (Fraction(5, 12), Fraction(1, 12)), (Fraction(5, 12), Fraction(-1, 12)))
    for rational, radical in cross_cosines:
        for target in (Fraction(1), Fraction(-1, 2)):
            require(radical != 0 or rational != target, "cross even rotation")
    # A prospective triple point is one of (1/2,+/-sqrt(3)/2).
    # Its square distance from either double-bad centre is (7+/-sqrt(33))/2,
    # never one because sqrt(33) is irrational.
    triple_distances = ((Fraction(7, 2), Fraction(1, 2)), (Fraction(7, 2), Fraction(-1, 2)))
    for rational, radical in triple_distances:
        require(radical != 0 or rational != 1, "triple at double-bad locus")
    return {
        "double_bad_x": "1/2",
        "double_bad_y_squared": "11/4",
        "cos_delta": "5/6",
        "cross_cosines_Qsqrt33": [[str(a), str(b)] for a, b in cross_cosines],
        "triple_distance_squares_Qsqrt33": [[str(a), str(b)] for a, b in triple_distances],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", default="certificate.json")
    args = parser.parse_args()
    certificate = json.loads(Path(args.certificate).read_text())
    require(certificate["schema"] == "unit-edge-dominating-triples-parity-v1", "schema")
    parity, admissible, histogram, triple_histogram = independent_combinatorial_audit(certificate)
    exception = exact_exception_audit()
    samples = {}
    for name, centres, mixed in make_samples():
        verify_mixed_points(centres, mixed)
        pairs, a_mask, c_mask, allocation, allocation_count = allocation_for_sample(centres, mixed)
        patch = patch_audit(centres, mixed, allocation)
        samples[name] = {
            "mixed_points": len(mixed),
            "a_conflict_mask": a_mask,
            "c_conflict_mask": c_mask,
            "allocation": "".join(str(x) for x in allocation),
            "allocation_count": allocation_count,
            **patch,
        }
    report = {
        "schema": certificate["schema"],
        "parity_graphs": len(parity),
        "admissible_no_triple_pairs": admissible,
        "no_triple_unsat": len(certificate["unsat_no_triple"]),
        "one_triple_unsat": len(certificate["unsat_one_triple"]),
        "exception": exception,
        "samples": samples,
    }
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
