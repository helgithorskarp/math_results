#!/usr/bin/env python3
"""Independent arithmetic checks for the nonmono-gadget field obstruction."""

from __future__ import annotations

import hashlib
import itertools
import sys
from fractions import Fraction
from math import lcm
from pathlib import Path


F = Fraction
ZERO = (F(0),) * 4
ONE = (F(1), F(0), F(0), F(0))


def add(first, second):
    return tuple(a + b for a, b in zip(first, second, strict=True))


def neg(value):
    return tuple(-coefficient for coefficient in value)


def conj(value):
    return value[0], value[1], -value[2], -value[3]


def mul(first, second):
    a, b, c, d = first
    A, B, C, D = second
    return (
        a * A + 33 * b * B - 3 * c * C - 11 * d * D,
        a * B + b * A - c * D - d * C,
        a * C + c * A + 11 * (b * D + d * B),
        a * D + d * A + 3 * (b * C + c * B),
    )


def inverse(value):
    real = mul(value, conj(value))
    if real[2:] != (0, 0):
        raise AssertionError("conjugate product is not real")
    a, b = real[:2]
    denominator = a * a - 33 * b * b
    if not denominator:
        raise ZeroDivisionError
    return mul(conj(value), (a / denominator, -b / denominator, F(0), F(0)))


def norm(value):
    return mul(value, conj(value))


def lift_root33(bits):
    """Lift the unique root t=0 mod 2 of 4t^2+t-2; return 1+8t."""
    if bits < 1:
        raise ValueError
    t = 0
    for precision in range(1, max(1, bits - 2)):
        modulus = 1 << (precision + 1)
        if (4 * t * t + t - 2) % modulus:
            t += 1 << precision
        if (4 * t * t + t - 2) % modulus:
            raise AssertionError("root lift failed")
    return (1 + 8 * t) % (1 << bits)


def color_from_integer_representation(numerators, denominator):
    if denominator <= 0:
        raise ValueError
    a, b, c, d = numerators
    exponent = (denominator & -denominator).bit_length() - 1
    modulus = 1 << (exponent + 1)
    r = lift_root33(exponent + 1)
    odd_inverse = pow(3 * (denominator >> exponent), -1, modulus)
    first = ((3 * a + 3 * b * r + 3 * c + d * r) * odd_inverse) % modulus
    second = ((6 * c + 2 * d * r) * odd_inverse) % modulus
    return (first >> exponent) | (2 * (second >> exponent))


def color(value):
    denominator = lcm(*(entry.denominator for entry in value))
    numerators = tuple(int(entry * denominator) for entry in value)
    return color_from_integer_representation(numerators, denominator)


def edge_set(vertices):
    return {
        (low, high)
        for high, first in enumerate(vertices)
        for low, second in enumerate(vertices[:high])
        if norm(add(first, neg(second))) == ONE
    }


def parse_gadget(path):
    rows = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        raw = tuple(map(int, line.split()))
        if len(raw) != 16:
            raise AssertionError("bad point row")
        if any(raw[index] for index in range(16) if index not in (0, 5, 9, 12)):
            raise AssertionError("coordinate outside claimed field")
        rows.append(tuple(F(raw[index], 12) for index in (0, 5, 9, 12)))
    if len(rows) != len(set(rows)):
        raise AssertionError("duplicate gadget point")
    return rows


def color_digest(vertices):
    encoded = "".join(str(color(vertex)) for vertex in vertices).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def is_k_colorable(vertex_count, edges, colour_count):
    neighbours = [set() for _ in range(vertex_count)]
    for first, second in edges:
        neighbours[first].add(second)
        neighbours[second].add(first)
    colors = [-1] * vertex_count

    def extend(colored):
        if colored == vertex_count:
            return True
        uncolored = [index for index, value in enumerate(colors) if value < 0]
        vertex = max(
            uncolored,
            key=lambda item: (len({colors[n] for n in neighbours[item] if colors[n] >= 0}),
                              len(neighbours[item])),
        )
        forbidden = {colors[n] for n in neighbours[vertex] if colors[n] >= 0}
        for value in range(colour_count):
            if value in forbidden:
                continue
            colors[vertex] = value
            if extend(colored + 1):
                return True
        colors[vertex] = -1
        return False

    return extend(0)


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: independent_check.py POINTS159.tsv POINTS214.tsv")

    for bits in range(1, 129):
        root = lift_root33(bits)
        if (root * root - 33) % (1 << bits):
            raise AssertionError("bad sqrt(33) residue")
        if bits >= 3 and root % 8 != 1:
            raise AssertionError("wrong sqrt(33) branch")

    residues = {
        (a, b): (a * a - a * b + b * b) % 2
        for a, b in itertools.product(range(2), repeat=2)
        if (a, b) != (0, 0)
    }
    if set(residues.values()) != {1}:
        raise AssertionError("binary residue norm is isotropic")

    representations = 0
    translations = 0
    coefficient_rows = list(itertools.product(range(-2, 3), repeat=4))
    denominators = (1, 2, 3, 4, 5, 8, 12, 16)
    for index, coefficients in enumerate(coefficient_rows):
        denominator = denominators[index % len(denominators)]
        value = tuple(F(entry, denominator) for entry in coefficients)
        base_color = color(value)
        for scale in (2, 3, 7, 16):
            scaled = tuple(entry * scale for entry in coefficients)
            if color_from_integer_representation(scaled, denominator * scale) != base_color:
                raise AssertionError("representation-dependent color")
            representations += 1

        q = F((index % 19) - 9, (index % 11) + 1)
        w = (F(0), F(0), q, F((index % 7) - 3, (index % 13) + 1))
        unit = mul(add(ONE, w), inverse(add(ONE, neg(w))))
        if norm(unit) != ONE or color(value) == color(add(value, unit)):
            raise AssertionError("unit translation is monochromatic")
        translations += 1

    gadget159 = parse_gadget(Path(sys.argv[1]))
    gadget214 = parse_gadget(Path(sys.argv[2]))
    edges159, edges214 = edge_set(gadget159), edge_set(gadget214)
    if (len(gadget159), len(edges159), len(gadget214), len(edges214)) != (159, 646, 214, 977):
        raise AssertionError("gadget census mismatch")
    for vertices, edges in ((gadget159, edges159), (gadget214, edges214)):
        colors = list(map(color, vertices))
        if any(colors[first] == colors[second] for first, second in edges):
            raise AssertionError("monochromatic gadget edge")

    spindle = [tuple(F(entry, 12) for entry in row) for row in (
        (0, 0, 0, 0), (12, 0, 0, 0), (6, 0, 6, 0), (18, 0, 6, 0),
        (10, 0, 0, 2), (5, -1, 5, 1), (15, -1, 5, 3),
    )]
    spindle_edges = edge_set(spindle)
    if len(spindle_edges) != 11:
        raise AssertionError("wrong spindle edge count")
    if is_k_colorable(7, spindle_edges, 3) or not is_k_colorable(7, spindle_edges, 4):
        raise AssertionError("wrong spindle chromatic number")

    print("sqrt33_precisions=128")
    print("nonzero_binary_norm_residues=3")
    print(f"representation_checks={representations}")
    print(f"unit_translation_checks={translations}")
    print(f"gadget159=159,646,{color_digest(gadget159)}")
    print(f"gadget214=214,977,{color_digest(gadget214)}")
    print("moser_spindle=7,11,4")
    print("independent_field_checks=true")


if __name__ == "__main__":
    main()
