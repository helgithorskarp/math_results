#!/usr/bin/env python3
"""Exact full-union check for the frozen connector alignment with E457.

This is intentionally separate from the isolated-connector verifier.  It
works in Q(sqrt(3),sqrt(11),sqrt(47)), rebuilds every unit edge after exact
collision merging, and tests the published positive words on the actual
complete union.
"""

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, permutations
from json import dumps, loads
from math import gcd
from pathlib import Path


HERE = Path(__file__).resolve().parent
E457_CORE = HERE.parent / "hadwiger_nelson_e457_equal_pair_source" / "core.json"
E457_CORE_SHA256 = "d377e9526d13cc76aba6762ecd6a79bd04fe12d61e03a0b585a5ea38820d833b"
RADICANDS = (1, 3, 11, 33, 47, 141, 517, 1551)
RINDEX = {radicand: index for index, radicand in enumerate(RADICANDS)}
Scalar = tuple[Q, Q, Q, Q, Q, Q, Q, Q]
Point = tuple[Scalar, Scalar]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def basis(radicand=1, coefficient=1):
    values = [Q(0)] * 8
    values[RINDEX[radicand]] = Q(coefficient)
    return tuple(values)


ZERO = basis(coefficient=0)
ONE = basis()
SQRT3 = basis(3)
SQRT11 = basis(11)
SQRT33 = basis(33)
SQRT47 = basis(47)
SQRT141 = basis(141)


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def neg(value):
    return tuple(-coefficient for coefficient in value)


def sub(left, right):
    return add(left, neg(right))


def scale(value, coefficient):
    coefficient = Q(coefficient)
    return tuple(coefficient * entry for entry in value)


def mul(left, right):
    answer = [Q(0)] * 8
    for left_index, left_coefficient in enumerate(left):
        if not left_coefficient:
            continue
        for right_index, right_coefficient in enumerate(right):
            if not right_coefficient:
                continue
            common = gcd(RADICANDS[left_index], RADICANDS[right_index])
            radicand = RADICANDS[left_index] * RADICANDS[right_index] // (common * common)
            answer[RINDEX[radicand]] += common * left_coefficient * right_coefficient
    return tuple(answer)


def padd(left, right):
    return add(left[0], right[0]), add(left[1], right[1])


def pneg(value):
    return neg(value[0]), neg(value[1])


def psub(left, right):
    return padd(left, pneg(right))


def norm2(point):
    return add(mul(point[0], point[0]), mul(point[1], point[1]))


def rotate60(point):
    x, y = point
    return scale(sub(x, mul(SQRT3, y)), Q(1, 2)), scale(add(mul(SQRT3, x), y), Q(1, 2))


def connector_points_horizontal():
    origin = (ZERO, ZERO)
    terminal = (scale(ONE, Q(8, 3)), ZERO)
    left_seed = (scale(ONE, Q(23, 24)), scale(SQRT47, Q(1, 24)))
    right_seed = (
        add(scale(ONE, Q(-123, 144)), scale(SQRT141, Q(-1, 144))),
        add(scale(SQRT3, Q(-41, 144)), scale(SQRT47, Q(3, 144))),
    )
    points = [origin, terminal]
    left, right = left_seed, right_seed
    for _ in range(6):
        points.append(left)
        left = rotate60(left)
    for _ in range(6):
        points.append(padd(terminal, right))
        right = rotate60(right)
    require(left == left_seed and right == right_seed, "connector orbit closure")
    return tuple(points)


def connector_alignments():
    horizontal = connector_points_horizontal()
    return {
        "orientation_preserving_ccw": tuple((neg(y), x) for x, y in horizontal),
        "orientation_reversing": tuple((y, x) for x, y in horizontal),
    }


def e457_points_and_word():
    require(sha256(E457_CORE.read_bytes()).hexdigest() == E457_CORE_SHA256, "E457 core hash")
    data = loads(E457_CORE.read_text())
    require(data["schema"] == "hn-e457-equal-pair-v1", "E457 schema")
    points = []
    for a, b, c, d in data["points"]:
        x = add(scale(SQRT3, Q(a, 36)), scale(SQRT11, Q(b, 36)))
        y = add(scale(ONE, Q(c, 36)), scale(SQRT33, Q(d, 36)))
        points.append((x, y))
    word = tuple(data["equal_four_colouring"])
    require(len(points) == len(set(points)) == len(word) == 457, "E457 input census")
    return tuple(points), word


def merged_union(first, second):
    points = []
    index = {}
    maps = []
    for source in (first, second):
        source_map = []
        for point in source:
            if point not in index:
                index[point] = len(points)
                points.append(point)
            source_map.append(index[point])
        maps.append(tuple(source_map))
    return tuple(points), tuple(maps)


def complete_edges(points):
    return tuple(
        (left, right)
        for left, right in combinations(range(len(points)), 2)
        if norm2(psub(points[left], points[right])) == ONE
    )


def mapped_edges(points, mapping):
    return {
        tuple(sorted((mapping[left], mapping[right])))
        for left, right in complete_edges(points)
    }


def coordinate_hash(points):
    rows = []
    for x, y in points:
        rows.append(" ".join(f"{value.numerator}/{value.denominator}" for value in x + y))
    return sha256(("\n".join(rows) + "\n").encode()).hexdigest()


def edge_hash(edges):
    return sha256(("".join(f"{left} {right}\n" for left, right in edges)).encode()).hexdigest()


def verify():
    e457, source_word = e457_points_and_word()
    connector_word = tuple(map(int, "33010101121212"))
    alignments = {}
    for name, connector in connector_alignments().items():
        points, (source_map, connector_map) = merged_union(e457, connector)
        overlaps = tuple(
            (left, right)
            for left in range(len(e457))
            for right in range(len(connector))
            if source_map[left] == connector_map[right]
        )
        require(overlaps == ((0, 0), (1, 1)), "unexpected overlap census")
        edges = complete_edges(points)
        source_edges = mapped_edges(e457, source_map)
        connector_edges = mapped_edges(connector, connector_map)
        require(len(source_edges) == 2329 and len(connector_edges) == 26, "inherited edge census")
        incidental = tuple(sorted(set(edges) - source_edges - connector_edges))

        successful_words = []
        successful_permutations = []
        for permutation in permutations(range(3)):
            recoloured = tuple(3 if colour == 3 else permutation[colour] for colour in connector_word)
            colours = [-1] * len(points)
            valid = True
            for old, physical in enumerate(source_map):
                colours[physical] = source_word[old]
            for old, physical in enumerate(connector_map):
                if colours[physical] not in (-1, recoloured[old]):
                    valid = False
                    break
                colours[physical] = recoloured[old]
            if valid and all(colours[left] != colours[right] for left, right in edges):
                successful_words.append(tuple(colours))
                successful_permutations.append(permutation)
        require(len(successful_words) == len(successful_permutations) == 6,
                "not every connector colour permutation extends")
        alignments[name] = {
            "overlap_pairs": [list(pair) for pair in overlaps],
            "union_points": len(points),
            "complete_unit_edges": len(edges),
            "source_unit_edges": len(source_edges),
            "connector_unit_edges": len(connector_edges),
            "incidental_cross_edges": len(incidental),
            "incidental_cross_edge_list": [list(edge) for edge in incidental],
            "pinned_e457_word_extending_connector_permutations": len(successful_permutations),
            "first_four_colour_word_sha256": sha256("".join(map(str, successful_words[0])).encode()).hexdigest(),
            "coordinate_sha256": coordinate_hash(points),
            "edge_sha256": edge_hash(edges),
        }
    return {
        "checker": "independent full-union exact multiquadratic reconstruction",
        "e457_points": len(e457),
        "connector_points": 14,
        "ordered_terminal_isometries_checked": len(alignments),
        "alignments": alignments,
        "record_candidate": False,
    }


def main():
    print(dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
