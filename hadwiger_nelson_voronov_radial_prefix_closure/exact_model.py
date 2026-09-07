#!/usr/bin/env python3
"""Exact Q(sqrt(2),sqrt(3)) model for the VND radial-prefix closure."""

from collections import defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction
from functools import cmp_to_key
from itertools import combinations
from math import isqrt


Q = Fraction


@dataclass(frozen=True)
class K:
    # coefficients of 1, sqrt(2), sqrt(3), sqrt(6)
    c: tuple

    def __add__(self, other):
        return K(tuple(a + b for a, b in zip(self.c, other.c)))

    def __neg__(self):
        return K(tuple(-a for a in self.c))

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        out = [Q(0) for _ in range(4)]
        # index = exponent(sqrt(2)) + 2*exponent(sqrt(3)).
        for i, left in enumerate(self.c):
            for j, right in enumerate(other.c):
                a = (i & 1) + (j & 1)
                b = ((i >> 1) & 1) + ((j >> 1) & 1)
                factor = (2 if a >= 2 else 1) * (3 if b >= 2 else 1)
                out[(a & 1) + 2 * (b & 1)] += factor * left * right
        return K(tuple(out))

    def scale(self, value):
        value = Q(value)
        return K(tuple(value * x for x in self.c))


ZERO = K((Q(0), Q(0), Q(0), Q(0)))
ONE = K((Q(1), Q(0), Q(0), Q(0)))


def sign(value):
    """Rigorous sign using rational enclosing intervals for the radicals."""
    if all(x == 0 for x in value.c):
        return 0
    for digits in (12, 24, 48, 96, 192):
        scale = 10 ** digits
        intervals = [(Q(1), Q(1))]
        for radicand in (2, 3, 6):
            floor = isqrt(radicand * scale * scale)
            low = Q(floor, scale)
            high = Q(floor + 1, scale)
            intervals.append((low, high))
        low = Q(0)
        high = Q(0)
        for coefficient, (radical_low, radical_high) in zip(value.c, intervals):
            if coefficient >= 0:
                low += coefficient * radical_low
                high += coefficient * radical_high
            else:
                low += coefficient * radical_high
                high += coefficient * radical_low
        if low > 0:
            return 1
        if high < 0:
            return -1
    raise ArithmeticError(f"failed to separate sign of {value}")


@dataclass(frozen=True)
class P:
    x: K
    y: K

    def __add__(self, other):
        return P(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return P(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return P(self.x * other.x - self.y * other.y,
                 self.x * other.y + self.y * other.x)

    def conjugate(self):
        return P(self.x, -self.y)

    def norm2(self):
        return self.x * self.x + self.y * self.y

    def power(self, exponent):
        if exponent < 0:
            return self.conjugate().power(-exponent)
        result = P(ONE, ZERO)
        base = self
        while exponent:
            if exponent & 1:
                result = result * base
            base = base * base
            exponent >>= 1
        return result


ORIGIN = P(ZERO, ZERO)
PHI0 = P(K((Q(0), Q(1, 4), Q(0), Q(1, 4))),
         K((Q(0), Q(-1, 4), Q(0), Q(1, 4))))
PHI1 = P(K((Q(0), Q(0), Q(0), Q(1, 3))),
         K((Q(0), Q(0), Q(1, 3), Q(0))))


def point_key(point):
    values = point.x.c + point.y.c
    return tuple(item for value in values
                 for item in (value.numerator, value.denominator))


def field_json(value):
    return [[coefficient.numerator, coefficient.denominator]
            for coefficient in value.c]


def cmp_field(left, right):
    return sign(left - right)


def source_sets():
    assert PHI0.power(24) == P(ONE, ZERO)
    assert PHI0.norm2() == ONE and PHI1.norm2() == ONE
    m1 = {ORIGIN}
    for a in range(24):
        for b in (-1, 0, 1):
            m1.add(PHI0.power(a) * PHI1.power(b))
    assert len(m1) == 73
    m2 = {left + right for left in m1 for right in m1
          if sign((left + right).norm2() - ONE) <= 0}
    assert len(m2) == 865
    return tuple(sorted(m1, key=point_key)), tuple(sorted(m2, key=point_key))


def shell_prefixes(m2):
    shells = defaultdict(list)
    for point in m2:
        shells[point.norm2()].append(point)
    radii2 = sorted(shells, key=cmp_to_key(cmp_field))
    accumulated = []
    rows = []
    for radius2 in radii2:
        accumulated.extend(shells[radius2])
        rows.append((radius2, tuple(sorted(accumulated, key=point_key))))
    return rows


def maximal_pairs(prefixes):
    usable = [(radius2, points) for radius2, points in prefixes
              if len(points) <= 508]
    valid = []
    for left in usable:
        for right in usable:
            nl, nr = len(left[1]), len(right[1])
            if nl >= nr and nl + nr - 1 <= 508:
                valid.append((left, right))
    return [pair for pair in valid if not any(
        len(other[0][1]) >= len(pair[0][1]) and
        len(other[1][1]) >= len(pair[1][1]) and
        (len(other[0][1]) > len(pair[0][1]) or
         len(other[1][1]) > len(pair[1][1]))
        for other in valid)]


def radius_sum_margins(left2, right2):
    # sqrt(left2)+sqrt(right2)<1 iff both returned quantities are >0.
    linear = ONE - left2 - right2
    squared = linear * linear - (left2 * right2).scale(4)
    assert sign(linear) > 0 and sign(squared) > 0
    return linear, squared


def unit_edges(points):
    return tuple((i, j) for i, j in combinations(range(len(points)), 2)
                 if (points[i] - points[j]).norm2() == ONE)


def bipartition(order, edges):
    adjacency = [[] for _ in range(order)]
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    colours = [-1] * order
    for root in range(order):
        if colours[root] >= 0:
            continue
        colours[root] = 0
        queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for neighbour in adjacency[vertex]:
                if colours[neighbour] < 0:
                    colours[neighbour] = 1 - colours[vertex]
                    queue.append(neighbour)
                elif colours[neighbour] == colours[vertex]:
                    raise AssertionError("odd cycle")
    return tuple(colours)


def exact_certificate():
    m1, m2 = source_sets()
    prefixes = shell_prefixes(m2)
    shell_rows = [{
        "radius_squared": field_json(radius2),
        "cumulative_vertices": len(points),
    } for radius2, points in prefixes]
    pairs = maximal_pairs(prefixes)
    expected = [(241, 241), (289, 217), (361, 145),
                (433, 73), (457, 25), (505, 1)]
    sizes = sorted((len(left[1]), len(right[1])) for left, right in pairs)
    assert sizes == expected

    pair_rows = []
    for (left2, left), (right2, right) in sorted(
            pairs, key=lambda pair: (len(pair[0][1]), len(pair[1][1]))):
        linear, squared = radius_sum_margins(left2, right2)
        pair_rows.append({
            "left_vertices": len(left),
            "right_vertices": len(right),
            "nominal_union_vertices": len(left) + len(right) - 1,
            "left_radius_squared": field_json(left2),
            "right_radius_squared": field_json(right2),
            "one_minus_radius_squares": field_json(linear),
            "squared_radius_sum_margin": field_json(squared),
        })

    k505 = next(points for _, points in prefixes if len(points) == 505)
    edges = unit_edges(k505)
    colours = bipartition(len(k505), edges)
    assert len(edges) == 216
    assert all(colours[left] != colours[right] for left, right in edges)
    return {
        "schema": "hn-vnd-radial-prefix-closure-v1",
        "arithmetic": "Q(sqrt(2),sqrt(3)); basis 1,sqrt(2),sqrt(3),sqrt(6)",
        "m1_vertices": len(m1),
        "m2_vertices": len(m2),
        "shells": shell_rows,
        "maximal_budget_pairs": pair_rows,
        "largest_relevant_prefix_vertices": len(k505),
        "largest_relevant_prefix_unit_edges": [list(edge) for edge in edges],
        "largest_relevant_prefix_bipartition": "".join(map(str, colours)),
        "conclusion": "Every union K_r union rho(K_s) with |K_r|+|K_s|-1 <= 508 is four-colourable for every origin-centred rotation rho.",
    }
