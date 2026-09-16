#!/usr/bin/env python3
"""Exact Q(zeta_66) model and colouring routines for the C11 spindle round."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256


# Phi_66(x), ascending coefficient order.  All arithmetic below is reduced
# modulo this monic polynomial, so no numerical root approximation is used.
PHI66 = (1, 1, 0, -1, -1, 0, 1, 1, 0, -1, -1,
         -1, 0, 1, 1, 0, -1, -1, 0, 1, 1)
DEGREE = 20


def _reduce(coefficients):
    a = [Fraction(x) for x in coefficients]
    if len(a) < DEGREE:
        a.extend([Fraction(0)] * (DEGREE - len(a)))
    for degree in range(len(a) - 1, DEGREE - 1, -1):
        leading = a[degree]
        if leading:
            shift = degree - DEGREE
            for j in range(DEGREE + 1):
                a[shift + j] -= leading * PHI66[j]
    return tuple(a[:DEGREE])


class C66:
    """An element of Q(q), q a primitive 66th root of unity."""

    __slots__ = ("c",)

    def __init__(self, coefficients=()):
        self.c = _reduce(coefficients)

    def __hash__(self):
        return hash(self.c)

    def __eq__(self, other):
        return self.c == as_c66(other).c

    def __add__(self, other):
        other = as_c66(other)
        return C66(a + b for a, b in zip(self.c, other.c))

    __radd__ = __add__

    def __neg__(self):
        return C66(-a for a in self.c)

    def __sub__(self, other):
        return self + (-as_c66(other))

    def __rsub__(self, other):
        return as_c66(other) - self

    def __mul__(self, other):
        other = as_c66(other)
        raw = [Fraction(0)] * (2 * DEGREE - 1)
        for i, a in enumerate(self.c):
            if not a:
                continue
            for j, b in enumerate(other.c):
                if b:
                    raw[i + j] += a * b
        return C66(raw)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        scalar = Fraction(scalar)
        return C66(a / scalar for a in self.c)

    def conjugate(self):
        result = ZERO
        for exponent, coefficient in enumerate(self.c):
            if coefficient:
                result += coefficient * qpower(-exponent)
        return result

    def key(self):
        return tuple((x.numerator, x.denominator) for x in self.c)


def as_c66(value):
    if isinstance(value, C66):
        return value
    return C66((Fraction(value),))


ZERO = C66()
ONE = C66((1,))
Q = C66((0, 1))
_QPOWERS = [ONE]
for _ in range(1, 66):
    _QPOWERS.append(_QPOWERS[-1] * Q)


def qpower(exponent):
    return _QPOWERS[exponent % 66]


def rotate_about(point, centre, multiplier):
    return centre + multiplier * (point - centre)


def construction():
    """Return collision-merged points, exact edges, labels, and source fibre.

    We work in a translated/rotated copy of the Shibuya realization.  Put
    zeta=q^6=exp(2*pi*i/11), and give the regular hendecagon unit sides via
    p_0=0, p_k=sum_{j<k} zeta^j.  The old circumcentre is then
    O=-sum(k*zeta^k)/11.  The rest exactly follows rigid_hendecagon(), except
    that all eleven rotations of its seven-point spindle are included.
    """
    zeta = qpower(6)
    omega = qpower(11)  # exp(pi*i/3)

    outer = [ZERO]
    step = ONE
    for _ in range(1, 11):
        outer.append(outer[-1] + step)
        step *= zeta

    centre = -sum((k * qpower(6 * k) for k in range(11)), ZERO) / 11
    z1i = outer[1] + outer[10] - outer[0]
    z2i = outer[2] + outer[10] - outer[0]
    z1 = rotate_about(z1i, centre, qpower(6 * 7))
    z2 = rotate_about(z2i, centre, qpower(6 * 7))
    z3 = outer[3] + outer[10] - outer[0]

    # Here |z1-z3|=|z2-z3|=sqrt(3).  Their left common unit
    # neighbour is a+alpha(b-a), alpha=(1+exp(pi*i/3))/3.
    alpha = (ONE + omega) / 3
    z13 = z1 + alpha * (z3 - z1)
    z31 = z3 + alpha * (z1 - z3)
    z23 = z2 + alpha * (z3 - z2)
    z32 = z3 + alpha * (z2 - z3)
    spindle = (z1, z2, z3, z13, z31, z23, z32)

    raw = []
    raw_labels = []
    for k, point in enumerate(outer):
        raw.append(point)
        raw_labels.append(("outer", k))
    raw.extend((z1i, z2i))
    raw_labels.extend((("inner", 1), ("inner", 2)))
    for k in range(11):
        multiplier = qpower(-24 * k)  # zeta^(-4k)
        for j, point in enumerate(spindle):
            raw.append(rotate_about(point, centre, multiplier))
            raw_labels.append(("spindle", k, j))

    points = []
    label_groups = []
    index = {}
    raw_to_point = []
    for point, label in zip(raw, raw_labels):
        if point not in index:
            index[point] = len(points)
            points.append(point)
            label_groups.append([])
        v = index[point]
        raw_to_point.append(v)
        label_groups[v].append(label)

    edges = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            difference = points[i] - points[j]
            if difference * difference.conjugate() == ONE:
                edges.append((i, j))

    source = tuple(raw_to_point[13:20])  # spindle rotation k=0
    return (tuple(points), tuple(edges), tuple(map(tuple, label_groups)), source)


def induced_edges(vertices, edges):
    position = {v: i for i, v in enumerate(vertices)}
    return tuple(
        (position[a], position[b])
        for a, b in edges
        if a in position and b in position
    )


def adjacency(vertex_count, edges):
    result = [set() for _ in range(vertex_count)]
    for a, b in edges:
        result[a].add(b)
        result[b].add(a)
    return tuple(map(frozenset, result))


def find_coloring(vertex_count, edges, color_count, pins=None):
    """Deterministic exhaustive DSATUR; return a word or None."""
    adj = adjacency(vertex_count, edges)
    colors = [-1] * vertex_count
    if pins:
        for vertex, color in sorted(pins.items()):
            if not (0 <= vertex < vertex_count and 0 <= color < color_count):
                return None
            if colors[vertex] not in (-1, color):
                return None
            colors[vertex] = color
        for a, b in edges:
            if colors[a] >= 0 and colors[a] == colors[b]:
                return None

    def visit(uncolored):
        if not uncolored:
            return True
        candidates = [v for v in range(vertex_count) if colors[v] < 0]
        vertex = max(
            candidates,
            key=lambda v: (
                len({colors[w] for w in adj[v] if colors[w] >= 0}),
                len(adj[v]),
                -v,
            ),
        )
        forbidden = {colors[w] for w in adj[vertex] if colors[w] >= 0}
        for color in range(color_count):
            if color not in forbidden:
                colors[vertex] = color
                if visit(uncolored - 1):
                    return True
        colors[vertex] = -1
        return False

    return tuple(colors) if visit(sum(c < 0 for c in colors)) else None


def canonical_colorings(vertex_count, edges, color_count):
    """Enumerate proper colourings up to global colour permutation."""
    adj = adjacency(vertex_count, edges)
    colors = [-1] * vertex_count
    result = []

    def visit(vertex, maximum):
        if vertex == vertex_count:
            result.append(tuple(colors))
            return
        forbidden = {colors[w] for w in adj[vertex] if w < vertex}
        for color in range(min(color_count - 1, maximum + 1) + 1):
            if color not in forbidden:
                colors[vertex] = color
                visit(vertex + 1, max(maximum, color))
        colors[vertex] = -1

    colors[0] = 0
    visit(1, 0)
    return tuple(result)


def check_word(word, vertex_count, edges, color_count=4):
    colors = tuple(int(x) for x in word)
    if len(colors) != vertex_count:
        raise ValueError("wrong colouring length")
    if any(not 0 <= x < color_count for x in colors):
        raise ValueError("colour outside range")
    if any(colors[a] == colors[b] for a, b in edges):
        raise ValueError("monochromatic edge")
    return colors


def _fraction_text(value):
    return f"{value.numerator}/{value.denominator}"


def coordinate_hash(points):
    lines = []
    for point in points:
        lines.append(",".join(_fraction_text(x) for x in point.c))
    return sha256(("\n".join(lines) + "\n").encode()).hexdigest()


def edge_hash(edges):
    text = "".join(f"{a} {b}\n" for a, b in edges)
    return sha256(text.encode()).hexdigest()


def word_hash(words):
    text = "".join("".join(map(str, word)) + "\n" for word in words)
    return sha256(text.encode()).hexdigest()
