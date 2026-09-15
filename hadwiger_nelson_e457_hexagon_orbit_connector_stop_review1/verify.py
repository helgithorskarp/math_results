#!/usr/bin/env python3
"""Independent exact review of the paired-hexagon E457 connector stop.

The target code is not imported.  Geometry uses a nested quadratic model
Q(sqrt(3))[sqrt(47)], and the universal colouring check uses an explicit
small witness bank rather than the target's general graph-colouring search.
"""

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from json import dumps
from math import isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "hadwiger_nelson_e457_hexagon_orbit_connector_stop"
TARGET_COMMIT = "a41aa85d3fed7c60a3065546b95ae7e9ca36f476"
TARGET_HASHES = {
    "DISCOVERY_BODY.md": "c54446a4204089e5fd78a7899c0d97dccd117a0fa4fb284faffe7682c3a3f388",
    "README.md": "1a4215aa93227c01ad890be99ccf90b281ae3458068a67abdb4f68d73069de2e",
    "SHA256SUMS": "b10aa93cc92e7e82e367a583c7bbb7629f006fc26834bace7ec7c7085aef0cc6",
    "VALIDATION.json": "3e44de8c2c7a5f3e25464f22c1056238f5552692707308fe653d60d28130056b",
    "controls.py": "1adc9d428d3db337f7805b9ba19174f097004af6a153e284f6a6cb8b89d92848",
    "expected.json": "b313421dc8b369ee0c377c8a3fbee0b30237d5d9cd988b1da2a9a60640b6a086",
    "verify.py": "fdc58ed2787fe6fc78937c26eaafc378181768227fbd807902e724666b1d4d40",
}

# A scalar is (x,y) with x,y in Q(sqrt(3)), representing x+y*sqrt(47).
# An inner pair (a,b) represents a+b*sqrt(3).  Flattening therefore gives
# the coefficient order 1,sqrt(3),sqrt(47),sqrt(141).
Inner = tuple[Q, Q]
Scalar = tuple[Inner, Inner]
Point = tuple[Scalar, Scalar]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def iadd(left, right):
    return left[0] + right[0], left[1] + right[1]


def ineg(value):
    return -value[0], -value[1]


def imul(left, right):
    return left[0] * right[0] + 3 * left[1] * right[1], left[0] * right[1] + left[1] * right[0]


IZERO = (Q(0), Q(0))


def scalar(rational=0):
    return ((Q(rational), Q(0)), IZERO)


ZERO = scalar()
ONE = scalar(1)
SQRT3 = ((Q(0), Q(1)), IZERO)
SQRT47 = (IZERO, (Q(1), Q(0)))
SQRT141 = (IZERO, (Q(0), Q(1)))


def add(left, right):
    return iadd(left[0], right[0]), iadd(left[1], right[1])


def neg(value):
    return ineg(value[0]), ineg(value[1])


def sub(left, right):
    return add(left, neg(right))


def mul(left, right):
    # (x+y*r47)(u+v*r47)=(xu+47yv)+(xv+yu)r47.
    return (
        iadd(imul(left[0], right[0]), tuple(47 * value for value in imul(left[1], right[1]))),
        iadd(imul(left[0], right[1]), imul(left[1], right[0])),
    )


def scale(value, rational):
    rational = Q(rational)
    return tuple(tuple(rational * coefficient for coefficient in inner) for inner in value)


def flatten(value):
    return value[0][0], value[0][1], value[1][0], value[1][1]


def padd(left, right):
    return add(left[0], right[0]), add(left[1], right[1])


def pneg(value):
    return neg(value[0]), neg(value[1])


def psub(left, right):
    return padd(left, pneg(right))


def pscale(point, value):
    return mul(point[0], value), mul(point[1], value)


def norm2(point):
    return add(mul(point[0], point[0]), mul(point[1], point[1]))


def rotate60(point):
    x, y = point
    return (
        scale(sub(x, mul(SQRT3, y)), Q(1, 2)),
        scale(add(mul(SQRT3, x), y), Q(1, 2)),
    )


def connector_points():
    origin = (ZERO, ZERO)
    terminal = (scale(ONE, Q(8, 3)), ZERO)
    left_seed = (scale(ONE, Q(23, 24)), scale(SQRT47, Q(1, 24)))
    right_seed = (
        add(scale(ONE, Q(-123, 144)), scale(SQRT141, Q(-1, 144))),
        add(scale(SQRT3, Q(-41, 144)), scale(SQRT47, Q(3, 144))),
    )
    left, right_vectors = [], []
    left_point, right_vector = left_seed, right_seed
    for _ in range(6):
        left.append(left_point)
        right_vectors.append(right_vector)
        left_point = rotate60(left_point)
        right_vector = rotate60(right_vector)
    require(left_point == left_seed and right_vector == right_seed, "orbit closure")
    return tuple((origin, terminal) + tuple(left) + tuple(padd(terminal, point) for point in right_vectors))


def complete_edges(points):
    return tuple(
        (left, right)
        for left, right in combinations(range(len(points)), 2)
        if norm2(psub(points[left], points[right])) == ONE
    )


def proper(word, edges, colours):
    return (
        isinstance(word, str)
        and all(character in "0123456789" and int(character) < colours for character in word)
        and all(word[left] != word[right] for left, right in edges)
    )


def encode_scalar(value):
    return [[coefficient.numerator, coefficient.denominator] for coefficient in flatten(value)]


def digest_rows(rows):
    return sha256(("\n".join(rows) + "\n").encode()).hexdigest()


def point_hash(points):
    return digest_rows(
        dumps([encode_scalar(point[0]), encode_scalar(point[1])], separators=(",", ":"))
        for point in points
    )


def edge_hash(edges):
    return digest_rows(f"{left} {right}" for left, right in edges)


def triangle_count(order, edges):
    edge_set = set(edges)
    return sum(
        (left, middle) in edge_set and (left, right) in edge_set and (middle, right) in edge_set
        for left, middle, right in combinations(range(order), 3)
    )


def common_unit_neighbours(first, second):
    direction = psub(second, first)
    require(norm2(direction) == ONE, "common-neighbour input is not a unit pair")
    midpoint = pscale(padd(first, second), scale(ONE, Q(1, 2)))
    perpendicular = (neg(direction[1]), direction[0])
    offset = pscale(perpendicular, scale(SQRT3, Q(1, 2)))
    return padd(midpoint, offset), psub(midpoint, offset)


def canonical_three_cross_edge_distances():
    """Derive the two reflected nondegenerate K2,2-minus-edge configurations."""
    left_zero = (ZERO, ZERO)
    left_one = (ONE, ZERO)
    results = []
    for origin in common_unit_neighbours(left_zero, left_one):
        right_zero = next(point for point in common_unit_neighbours(left_zero, left_one) if point != origin)
        right_one_options = common_unit_neighbours(left_zero, right_zero)
        require(left_one in right_one_options, "missing degenerate third point")
        right_one = next(point for point in right_one_options if point != left_one)
        terminal_options = common_unit_neighbours(right_zero, right_one)
        require(left_zero in terminal_options, "missing degenerate right centre")
        terminal = next(point for point in terminal_options if point != left_zero)
        require(len({origin, left_zero, left_one, right_zero, right_one, terminal}) == 6,
                "canonical triple collision")
        results.append(norm2(psub(terminal, origin)))
    require(results == [scalar(7), scalar(7)], "three-edge terminal distance")
    return tuple(results)


def rim_edges():
    return {
        tuple(sorted((vertex, (vertex + 1) % 6))) for vertex in range(6)
    } | {
        tuple(sorted((6 + vertex, 6 + (vertex + 1) % 6))) for vertex in range(6)
    }


def colouring_bank():
    words = set()
    for left_phase in range(2):
        for right_phase in range(2):
            base = tuple((vertex + left_phase) % 2 for vertex in range(6)) + tuple(
                (vertex + right_phase) % 2 for vertex in range(6)
            )
            words.add("".join(map(str, base)))
            for vertex in range(12):
                recoloured = list(base)
                recoloured[vertex] = 2
                words.add("".join(map(str, recoloured)))
    return tuple(sorted(words))


def bipartite(order, edges):
    colours = [-1] * order
    for start in range(order):
        if colours[start] >= 0:
            continue
        colours[start] = 0
        stack = [start]
        while stack:
            vertex = stack.pop()
            for edge in edges:
                if vertex not in edge:
                    continue
                neighbour = edge[0] if edge[1] == vertex else edge[1]
                if colours[neighbour] < 0:
                    colours[neighbour] = 1 - colours[vertex]
                    stack.append(neighbour)
                elif colours[neighbour] == colours[vertex]:
                    return False
    return True


def abstract_census():
    rims = rim_edges()
    cross_edges = tuple((left, 6 + right) for left in range(6) for right in range(6))
    bank = colouring_bank()
    cases = 0
    bipartite_cases = 0
    three_colour_cases = 0
    rows = []
    size_histogram = Counter()
    for size in range(3):
        for selected in combinations(cross_edges, size):
            cases += 1
            edges = tuple(sorted(rims | set(selected)))
            is_bipartite = bipartite(12, edges)
            eligible = (word for word in bank if ("2" not in word) == is_bipartite)
            witness = next((word for word in eligible if proper(word, edges, 3)), None)
            require(witness is not None, "witness bank missed a cross-edge pattern")
            require(("2" not in witness) == is_bipartite, "witness/bipartite mismatch")
            bipartite_cases += is_bipartite
            three_colour_cases += not is_bipartite
            size_histogram[size] += 1
            encoded_edges = ",".join(f"{left}-{right}" for left, right in selected) or "-"
            rows.append(f"{size} {encoded_edges} {int(is_bipartite)} {witness}")
    require(cases == 667 and bipartite_cases == 343 and three_colour_cases == 324,
            "abstract census totals")
    return {
        "cases": cases,
        "bipartite_cases": bipartite_cases,
        "strictly_three_chromatic_cases": three_colour_cases,
        "case_size_histogram": {str(size): size_histogram[size] for size in sorted(size_histogram)},
        "witness_bank_size": len(bank),
        "census_sha256": digest_rows(rows),
    }


def rational_square(value):
    value = Q(value)
    return isqrt(value.numerator) ** 2 == value.numerator and isqrt(value.denominator) ** 2 == value.denominator


def verify():
    for name, expected in TARGET_HASHES.items():
        require(sha256((TARGET / name).read_bytes()).hexdigest() == expected, "target hash: " + name)

    points = connector_points()
    require(len(points) == len(set(points)) == 14, "fixed point census")
    edges = complete_edges(points)
    require(len(edges) == 26, "fixed edge census")

    spokes = {(0, vertex) for vertex in range(2, 8)} | {(1, vertex) for vertex in range(8, 14)}
    left_rim = {tuple(sorted((2 + vertex, 2 + (vertex + 1) % 6))) for vertex in range(6)}
    right_rim = {tuple(sorted((8 + vertex, 8 + (vertex + 1) % 6))) for vertex in range(6)}
    cross = tuple(sorted(set(edges) - spokes - left_rim - right_rim))
    require(cross == ((2, 8), (2, 13)), "fixed cross contacts")
    require(norm2(psub(points[0], points[1])) == scale(ONE, Q(64, 9)), "terminal distance")

    equal_word = "33010101121212"
    three_word = "01121212020202"
    require(len(equal_word) == len(three_word) == 14, "word length")
    require(proper(equal_word, edges, 4) and equal_word[0] == equal_word[1], "equal word")
    require(proper(three_word, edges, 3) and three_word[0] != three_word[1], "three word")
    triangles = triangle_count(14, edges)
    require(triangles > 0, "fixed graph has no triangle")

    quarter_turn_seed = (neg(points[2][1]), points[2][0])
    require(quarter_turn_seed == (scale(SQRT47, Q(-1, 24)), scale(ONE, Q(23, 24))),
            "quarter-turn witness")
    require(not rational_square(Q(47, 3)) and not rational_square(Q(47, 11)),
            "sqrt(47) outside-field test")

    forced_distances = canonical_three_cross_edge_distances()
    abstract = abstract_census()
    degrees = Counter()
    for left, right in edges:
        degrees[left] += 1
        degrees[right] += 1

    return {
        "checker": "independent nested-quadratic geometry and explicit colouring-witness bank",
        "target_code_imported": False,
        "target_mathematical_commit": TARGET_COMMIT,
        "fixed_connector": {
            "points": len(points),
            "complete_unit_edges": len(edges),
            "cross_edges": [list(edge) for edge in cross],
            "triangles": triangles,
            "degree_histogram": {str(degree): count for degree, count in sorted(Counter(degrees.values()).items())},
            "chromatic_number": 3,
            "equal_terminal_four_word_sha256": sha256(equal_word.encode()).hexdigest(),
            "different_terminal_three_word_sha256": sha256(three_word.encode()).hexdigest(),
            "point_sha256": point_hash(points),
            "edge_sha256": edge_hash(edges),
            "terminal_squared_distance": "64/9",
            "raw_two_overlap_e457_budget": 469,
        },
        "universal_geometry": {
            "projection_threshold": "2/3",
            "candidate_cross_support": "adjacent K2,2",
            "three_edge_patterns_up_to_labelled_missing_edge": 4,
            "nondegenerate_reflection_cases_checked": len(forced_distances),
            "forced_three_edge_terminal_squared_distance": "7",
            "target_terminal_squared_distance": "64/9",
            "maximum_cross_edges": 2,
        },
        "abstract_relation": abstract,
        "outside_e457_support": {
            "quarter_turn_witness": "(-sqrt(47)/24,23/24)",
            "sqrt47_in_Qsqrt3_plus_Qsqrt11": False,
        },
        "verdict": "ACCEPT_SCOPED_ARCHITECTURE_STOP",
        "record_candidate": False,
        "scope": "one unit-radius six-point orbit at each of two terminals at distance 8/3, plus one exact maximal-contact realization",
    }


def main():
    print(dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
