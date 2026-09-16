#!/usr/bin/env python3
"""Independent exact review of the frozen 462-point Haugland two-frame patch.

No executable target or dependency module is imported.  Geometry is rebuilt
in Cartesian coordinates over Q(zeta_84,sqrt(5)), rather than in the target's
complex Q(zeta_42,sqrt(5)) representation.  Two new finite-field images sieve
all unordered pairs; every survivor is confirmed by exact integer polynomial
arithmetic.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET_NAME = "hadwiger_nelson_haugland_two_frame_address_patch"
TARGET_COMMIT = "d5892b6c006bbd3fb007631b502bf8d5311ce8b1"
TARGET_HASHES = {
    "README.md": "d8a7c8bb2ec29ecb4c91f526a07e1425410d3f8d04732bf4ec5223a23f80f2ad",
    "DEPENDENCIES.json": "a6aef1936439a57d425e71e8b0a6703844e7abd80b03e792b243582f579a17a4",
    "certificate.json": "78c94dd56761fe3a435060895dc3608566fd94b9d915ccd94a5c76505fff3ff9",
    "model.py": "0ad70c258cf6e1074dc15c0fa96b6244dfc5e96306ca6f490ca407a8e33034db",
    "verify.py": "868880ef061b9c0d26d2b54fc9712cb55555c6ffe4eae2ce4467d3eecb97dd58",
}
PARENT_GRAPH = "hadwiger_nelson_haugland2131_exact_reproduction/graph.json"
PARENT_GRAPH_SHA256 = "201196679760fc329fff548346b843a821646ce5ffc326a91cc24598effc299d"

DEGREE = 24
# Low-to-high coefficients of Phi_84.
MODULUS = (
    1, 0, 1, 0, 0, 0, -1, 0, -1, 0, 0, 0,
    1, 0, 0, 0, -1, 0, -1, 0, 0, 0, 1, 0, 1,
)
SIEVES = (
    # (prime, primitive 84th root, square root of 5)
    (1429, 1274, 336),
    (2269, 1840, 158),
)
EXPECTED_CROSS = ((56, 461), (83, 461), (123, 461), (193, 461), (197, 461))


class ReviewFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewFailure(message)


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pad(values=()):
    result = tuple(Fraction(value) for value in values)
    need(len(result) <= DEGREE, "field element degree")
    return result + (Fraction(0),) * (DEGREE - len(result))


ZERO = pad()
ONE = pad((1,))
ZETA = pad((0, 1))


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def neg(value):
    return tuple(-coefficient for coefficient in value)


def sub(left, right):
    return add(left, neg(right))


def scale(value, scalar):
    scalar = Fraction(scalar)
    return tuple(scalar * coefficient for coefficient in value)


def multiply(left, right):
    product = [Fraction(0)] * (2 * DEGREE - 1)
    for i, a in enumerate(left):
        if a:
            for j, b in enumerate(right):
                if b:
                    product[i + j] += a * b
    for exponent in range(2 * DEGREE - 2, DEGREE - 1, -1):
        leading = product[exponent]
        if not leading:
            continue
        shift = exponent - DEGREE
        for i, coefficient in enumerate(MODULUS[:-1]):
            if coefficient:
                product[shift + i] -= leading * coefficient
    return tuple(product[:DEGREE])


def poly_trim(poly):
    while poly and not poly[-1]:
        poly.pop()
    return poly


def poly_sub(left, right):
    result = left[:] + [Fraction(0)] * max(0, len(right) - len(left))
    for i, value in enumerate(right):
        result[i] -= value
    return poly_trim(result)


def poly_multiply(left, right):
    if not left or not right:
        return []
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        if a:
            for j, b in enumerate(right):
                if b:
                    result[i + j] += a * b
    return poly_trim(result)


def poly_divmod(numerator, denominator):
    numerator = poly_trim(numerator[:])
    denominator = poly_trim(denominator[:])
    need(bool(denominator), "zero polynomial divisor")
    if len(numerator) < len(denominator):
        return [], numerator
    quotient = [Fraction(0)] * (len(numerator) - len(denominator) + 1)
    while numerator and len(numerator) >= len(denominator):
        shift = len(numerator) - len(denominator)
        coefficient = numerator[-1] / denominator[-1]
        quotient[shift] = coefficient
        for i, value in enumerate(denominator):
            numerator[shift + i] -= coefficient * value
        poly_trim(numerator)
    return poly_trim(quotient), numerator


def inverse(value):
    need(value != ZERO, "zero inverse")
    old_r, r = [Fraction(value) for value in MODULUS], poly_trim(list(value))
    old_t, t = [], [Fraction(1)]
    while r:
        quotient, remainder = poly_divmod(old_r, r)
        old_r, r = r, remainder
        old_t, t = t, poly_sub(old_t, poly_multiply(quotient, t))
    need(len(old_r) == 1, "noninvertible quotient element")
    candidate = pad(coefficient / old_r[0] for coefficient in old_t)
    need(multiply(value, candidate) == ONE, "inverse check")
    return candidate


def power(value, exponent):
    need(exponent >= 0, "negative generic exponent")
    result, base = ONE, value
    while exponent:
        if exponent & 1:
            result = multiply(result, base)
        base = multiply(base, base)
        exponent >>= 1
    return result


def zeta_power(exponent):
    return power(ZETA, exponent % 84)


def conjugate(value):
    result = ZERO
    for exponent, coefficient in enumerate(value):
        if coefficient:
            result = add(result, scale(zeta_power(-exponent), coefficient))
    return result


def eadd(left, right):
    return add(left[0], right[0]), add(left[1], right[1])


def eneg(value):
    return neg(value[0]), neg(value[1])


def esub(left, right):
    return eadd(left, eneg(right))


def escale(value, scalar):
    return scale(value[0], scalar), scale(value[1], scalar)


def emultiply(left, right):
    return (
        add(multiply(left[0], right[0]), scale(multiply(left[1], right[1]), 5)),
        add(multiply(left[0], right[1]), multiply(left[1], right[0])),
    )


E_ZERO = (ZERO, ZERO)
E_ONE = (ONE, ZERO)
I = zeta_power(21)
MINUS_I = neg(I)


def complex_to_cartesian(value):
    value_bar = conjugate(value)
    x = scale(add(value, value_bar), Fraction(1, 2))
    y = scale(multiply(sub(value, value_bar), MINUS_I), Fraction(1, 2))
    need(conjugate(x) == x and conjugate(y) == y, "Cartesian reality")
    return x, y


def construct_support():
    """Rebuild H, its two-address patch, and the frozen Cartesian union."""

    need(power(ZETA, 84) == ONE and power(ZETA, 42) == neg(ONE), "zeta order")
    t = lambda exponent: zeta_power(2 * exponent)
    first = inverse(sub(t(24), t(-24)))
    second = neg(multiply(t(-7), inverse(sub(t(6), t(-6)))))
    third = neg(multiply(t(7), inverse(sub(t(12), t(-12)))))
    host = [multiply(seed, t(6 * j)) for seed in (first, second, third) for j in range(7)]
    normalized = [sub(value, host[0]) for value in host]
    patch = sorted({add(left, right) for left in normalized for right in normalized})
    need(len(host) == 21 and len(patch) == 231 and ZERO in patch, "host/patch orders")

    patch_xy = [complex_to_cartesian(value) for value in patch]
    frame_a = [((x, ZERO), (y, ZERO)) for x, y in patch_xy]
    i_sqrt3 = sub(scale(t(7), 2), ONE)
    sqrt3 = multiply(i_sqrt3, MINUS_I)
    need(multiply(sqrt3, sqrt3) == scale(ONE, 3) and conjugate(sqrt3) == sqrt3,
         "sqrt3 identity")
    cosine = (scale(ONE, Fraction(7, 8)), ZERO)
    sine = (ZERO, scale(sqrt3, Fraction(1, 8)))

    def rotate(point):
        x, y = point
        return (esub(emultiply(cosine, x), emultiply(sine, y)),
                eadd(emultiply(sine, x), emultiply(cosine, y)))

    rotated_anchor = rotate(frame_a[230])
    translation = (esub(esub(frame_a[197][0], rotated_anchor[0]), E_ONE),
                   esub(frame_a[197][1], rotated_anchor[1]))
    frame_b = []
    for point in frame_a:
        image = rotate(point)
        frame_b.append((eadd(image[0], translation[0]), eadd(image[1], translation[1])))
    points = frame_a + frame_b
    need(len(points) == len(set(points)) == 462 and not (set(frame_a) & set(frame_b)),
         "physical point order")
    return host, normalized, patch, sqrt3, points


def target_coordinate_hash(points):
    """Recover the target's complex zeta_42 stream from Cartesian zeta_84 data."""

    digest = hashlib.sha256()
    for x, y in points:
        fields = []
        for root_part in range(2):
            complex_value = add(x[root_part], multiply(I, y[root_part]))
            need(all(not coefficient for index, coefficient in enumerate(complex_value) if index % 2),
                 "point left zeta_42 subfield")
            coefficients = tuple(complex_value[2 * index] for index in range(12))
            fields.append(",".join(
                f"{coefficient.numerator}/{coefficient.denominator}"
                for coefficient in coefficients
            ))
        digest.update((";".join(fields) + "\n").encode("ascii"))
    return digest.hexdigest()


def cartesian_coordinate_hash(points):
    digest = hashlib.sha256()
    for point in points:
        for extended in point:
            for value in extended:
                digest.update((",".join(
                    f"{coefficient.numerator}/{coefficient.denominator}"
                    for coefficient in value
                ) + ";").encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def integerize(points):
    denominator = 1
    for point in points:
        for extended in point:
            for value in extended:
                for coefficient in value:
                    denominator = math.lcm(denominator, coefficient.denominator)
    integers = []
    for point in points:
        flattened = []
        for extended in point:
            for value in extended:
                row = tuple(int(coefficient * denominator) for coefficient in value)
                need(all(Fraction(number, denominator) == coefficient
                         for number, coefficient in zip(row, value)), "integerization")
                flattened.append(row)
        integers.append(tuple(flattened))
    return denominator, integers


def multiply_integer(left, right):
    product = [0] * (2 * DEGREE - 1)
    for i, a in enumerate(left):
        if a:
            for j, b in enumerate(right):
                if b:
                    product[i + j] += a * b
    for exponent in range(2 * DEGREE - 2, DEGREE - 1, -1):
        leading = product[exponent]
        if not leading:
            continue
        shift = exponent - DEGREE
        for i, coefficient in enumerate(MODULUS[:-1]):
            if coefficient:
                product[shift + i] -= leading * coefficient
    return tuple(product[:DEGREE])


def vector_add(*values):
    return tuple(sum(parts) for parts in zip(*values))


def vector_scale(value, scalar):
    return tuple(scalar * coefficient for coefficient in value)


def exact_unit(left, right, denominator):
    differences = [tuple(a - b for a, b in zip(x, y)) for x, y in zip(left, right)]
    xa, xb, ya, yb = differences
    rational = vector_add(
        multiply_integer(xa, xa), vector_scale(multiply_integer(xb, xb), 5),
        multiply_integer(ya, ya), vector_scale(multiply_integer(yb, yb), 5),
    )
    radical = vector_scale(vector_add(
        multiply_integer(xa, xb), multiply_integer(ya, yb)
    ), 2)
    return rational == (denominator * denominator,) + (0,) * 23 and radical == (0,) * 24


def is_prime(value):
    if value < 2:
        return False
    for divisor in range(2, math.isqrt(value) + 1):
        if value % divisor == 0:
            return False
    return True


def validate_sieve(prime, zeta, sqrt5):
    need(is_prime(prime), "nonprime sieve modulus")
    need(pow(zeta, 84, prime) == 1, "zeta power")
    need(all(pow(zeta, 84 // factor, prime) != 1 for factor in (2, 3, 7)),
         "zeta not primitive")
    need(sqrt5 * sqrt5 % prime == 5, "sqrt5 image")


def evaluate(value, prime, zeta):
    result = 0
    for coefficient in reversed(value):
        need(coefficient.denominator % prime != 0, "sieve divides denominator")
        result = (result * zeta + coefficient.numerator *
                  pow(coefficient.denominator, -1, prime)) % prime
    return result


def modular_points(points, parameters):
    prime, zeta, sqrt5 = parameters
    validate_sieve(*parameters)
    result = []
    for x, y in points:
        result.append((
            (evaluate(x[0], prime, zeta) + sqrt5 * evaluate(x[1], prime, zeta)) % prime,
            (evaluate(y[0], prime, zeta) + sqrt5 * evaluate(y[1], prime, zeta)) % prime,
        ))
    return result


def complete_edges(points):
    """Screen every physical pair under two homomorphisms, then confirm exactly."""

    images = [(parameters[0], modular_points(points, parameters)) for parameters in SIEVES]
    active = None
    counts = []
    for prime, values in images:
        survivors = {
            (left, right)
            for left in range(len(points))
            for right in range(left + 1, len(points))
            if ((values[left][0] - values[right][0]) ** 2 +
                (values[left][1] - values[right][1]) ** 2 - 1) % prime == 0
        }
        counts.append(len(survivors))
        active = survivors if active is None else active & survivors
    denominator, integer_points = integerize(points)
    candidates = sorted(active)
    edges = [pair for pair in candidates
             if exact_unit(integer_points[pair[0]], integer_points[pair[1]], denominator)]
    need(len(edges) == len(candidates), "surviving modular false positive")
    return edges, counts, denominator


def edge_hash(edges):
    payload = "".join(f"{left} {right}\n" for left, right in edges).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def source_pattern_edges():
    edges = set()
    for index in range(7):
        for left, right in ((index, 7 + index), (index, 14 + index), (7 + index, 14 + index)):
            edges.add(tuple(sorted((left, right))))
    for offset, step in ((0, 1), (7, 2), (14, 3)):
        for index in range(7):
            edges.add(tuple(sorted((offset + index, offset + (index + step) % 7))))
    need(len(edges) == 42, "source pattern size")
    return tuple(sorted(edges))


def normalized_triangle_colourings(edges):
    """Fix the first vertical triangle by global colour symmetry and enumerate."""

    permutations = tuple(itertools.permutations(range(3)))
    count = 0
    for tail in itertools.product(permutations, repeat=6):
        columns = ((0, 1, 2),) + tail
        word = [-1] * 21
        for index, column in enumerate(columns):
            word[index], word[7 + index], word[14 + index] = column
        if all(word[left] != word[right] for left, right in edges):
            count += 1
    return count


def check_source(host, normalized, patch, points, union_edges):
    source_indices = [patch.index(value) for value in normalized]
    source_index_set = set(source_indices)
    actual = []
    for left, right in union_edges:
        if left in source_index_set and right in source_index_set:
            actual.append(tuple(sorted((source_indices.index(left), source_indices.index(right)))))
    actual = tuple(sorted(actual))
    expected = source_pattern_edges()
    need(actual == expected, "embedded 21-point source graph")
    need(normalized_triangle_colourings(expected) == 0, "source three-colouring")
    return source_indices, expected


def check_word(word, order, edges):
    need(type(word) is str and len(word) == order and set(word) <= set("0123"),
         "four-word format")
    need(all(word[left] != word[right] for left, right in edges), "monochromatic unit edge")


def components(order, edges, removed=frozenset()):
    selected = set(range(order)) - set(removed)
    adjacency = {vertex: set() for vertex in selected}
    for left, right in edges:
        if left in selected and right in selected:
            adjacency[left].add(right)
            adjacency[right].add(left)
    blocks = []
    while selected:
        root = min(selected)
        selected.remove(root)
        stack, block = [root], []
        while stack:
            vertex = stack.pop()
            block.append(vertex)
            found = adjacency[vertex] & selected
            selected.difference_update(found)
            stack.extend(found)
        blocks.append(sorted(block))
    return sorted(blocks, key=lambda block: (-len(block), block))


def articulation_data(order, edges):
    adjacency = [set() for _ in range(order)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    entered = [-1] * order
    low = [0] * order
    parent = [-1] * order
    articulations, bridges = set(), set()
    clock = 0

    def visit(vertex):
        nonlocal clock
        entered[vertex] = low[vertex] = clock
        clock += 1
        children = 0
        for neighbour in sorted(adjacency[vertex]):
            if entered[neighbour] < 0:
                parent[neighbour] = vertex
                children += 1
                visit(neighbour)
                low[vertex] = min(low[vertex], low[neighbour])
                if parent[vertex] < 0 and children > 1:
                    articulations.add(vertex)
                if parent[vertex] >= 0 and low[neighbour] >= entered[vertex]:
                    articulations.add(vertex)
                if low[neighbour] > entered[vertex]:
                    bridges.add((vertex, neighbour))
            elif neighbour != parent[vertex]:
                low[vertex] = min(low[vertex], entered[neighbour])

    visit(0)
    need(all(value >= 0 for value in entered), "union disconnected")
    return sorted(articulations), sorted(tuple(sorted(edge)) for edge in bridges)


def field_constants():
    sqrt3 = multiply(sub(zeta_power(14), zeta_power(-14)), MINUS_I)
    need(multiply(sqrt3, sqrt3) == scale(ONE, 3), "parent sqrt3")

    def sine(exponent):
        return scale(multiply(sub(zeta_power(exponent), zeta_power(-exponent)), MINUS_I),
                     Fraction(1, 2))

    alpha = inverse(sine(12))
    beta = inverse(sine(24))
    base_x = scale(multiply(sqrt3, add(alpha, beta)), Fraction(1, 4))
    base_y = scale(sub(alpha, beta), Fraction(1, 4))
    vectors = []
    for index in range(42):
        rotation, reverse = zeta_power(2 * index), zeta_power(-2 * index)
        cosine = scale(add(rotation, reverse), Fraction(1, 2))
        sine_value = scale(multiply(sub(rotation, reverse), MINUS_I), Fraction(1, 2))
        vectors.append((cosine, sine_value))
        vectors.append((sub(multiply(base_x, cosine), multiply(base_y, sine_value)),
                        add(multiply(base_x, sine_value), multiply(base_y, cosine))))
    need(len(vectors) == 84, "parent direction count")
    return sqrt3, tuple(vectors)


def scope_check(repository, points):
    graph_path = repository / PARENT_GRAPH
    need(file_digest(graph_path) == PARENT_GRAPH_SHA256, "changed parent path data")
    paths = json.loads(graph_path.read_text())["paths"]
    sqrt3, vectors = field_constants()
    origin = (ZERO, ZERO)
    g1 = {origin}
    for path in paths:
        point = origin
        for step in path:
            need(type(step) is int and 0 <= step < 84, "parent path step")
            point = (add(point[0], vectors[step][0]), add(point[1], vectors[step][1]))
            g1.add(point)
        need(point == (ZERO, sqrt3), "parent path endpoint")
    need(len(g1) == 740, "G1 order")

    g2 = set()
    for x, y in g1:
        g2.add((sub(scale(add(x, multiply(sqrt3, y)), Fraction(1, 2)), ONE),
                scale(sub(y, multiply(sqrt3, x)), Fraction(1, 2))))
        g2.add((add(scale(sub(x, multiply(sqrt3, y)), Fraction(1, 2)), ONE),
                scale(add(multiply(sqrt3, x), y), Fraction(1, 2))))
    need(len(g2) == 1066, "G2 order")

    parent = set()
    for x, y in g2:
        parent.add(((x, ZERO), (y, ZERO)))
        parent.add((
            (sub(scale(add(x, ONE), Fraction(7, 8)), ONE),
             scale(multiply(sqrt3, y), Fraction(-1, 8))),
            (scale(y, Fraction(7, 8)),
             scale(multiply(sqrt3, add(x, ONE)), Fraction(1, 8))),
        ))
    need(len(parent) == 2131, "parent order")
    frame_a_hits = [index for index, point in enumerate(points[:231]) if point in parent]
    frame_b_hits = [index + 231 for index, point in enumerate(points[231:]) if point in parent]
    base_field_b = [index + 231 for index, point in enumerate(points[231:])
                    if point[0][1] == ZERO and point[1][1] == ZERO]
    need(frame_a_hits == [40, 43, 55, 58, 59, 110, 112], "frame A parent hits")
    need(frame_b_hits == [] and base_field_b == [461], "frame B parent exclusion")
    return {
        "parent_points": len(parent),
        "frame_a_parent_indices": frame_a_hits,
        "frame_b_parent_indices": frame_b_hits,
        "frame_b_base_field_indices": base_field_b,
        "support_not_parent_subset": True,
    }


def validate_certificate(certificate, points, edges):
    need(certificate.get("version") == 1 and certificate.get("anchors") == [197, 230],
         "target certificate header")
    target_hash = target_coordinate_hash(points)
    need(target_hash == certificate.get("coordinate_sha256"), "target coordinate hash")
    need(len(edges) == 1853 and edge_hash(edges) == certificate.get("edge_sha256"),
         "complete edge stream")
    word = certificate.get("four_word")
    check_word(word, 462, edges)
    return word, target_hash


def review(repository: Path, with_scope=False):
    target = repository / TARGET_NAME
    for name, expected in TARGET_HASHES.items():
        need(file_digest(target / name) == expected, "changed target file: " + name)
    certificate = json.loads((target / "certificate.json").read_text())

    host, normalized, patch, sqrt3, points = construct_support()
    edges, sieve_counts, denominator = complete_edges(points)
    word, target_hash = validate_certificate(certificate, points, edges)

    source_indices, source_edges = check_source(host, normalized, patch, points, edges)
    edge_set = set(edges)
    need(all(tuple(sorted((left + 231, right + 231))) in edge_set
             for left, right in ((source_indices[a], source_indices[b]) for a, b in source_edges)),
         "second embedded source")
    frame_a_edges = [(left, right) for left, right in edges if right < 231]
    frame_b_edges = [(left, right) for left, right in edges if left >= 231]
    cross = [(left, right) for left, right in edges if left < 231 <= right]
    need(len(frame_a_edges) == len(frame_b_edges) == 924 and tuple(cross) == EXPECTED_CROSS,
         "frame/cross edge census")
    check_word(word[:231], 231, frame_a_edges)
    check_word(word[231:], 231, [(left - 231, right - 231) for left, right in frame_b_edges])

    blocks = components(462, edges, {461})
    articulations, bridges = articulation_data(462, edges)
    need(list(map(len, blocks)) == [231, 230], "contact-vertex components")
    need(articulations == [461] and bridges == [], "unique articulation/no bridges")
    class_sizes = [word.count(str(colour)) for colour in range(4)]
    cross_neighbour_colours = [int(word[index]) for index, _ in cross]
    need(set(cross_neighbour_colours) == {0, 2, 3} and word[461] == "1",
         "cross-cut word")

    result = {
        "status": "ACCEPT_AND_STRENGTHEN",
        "target_commit": TARGET_COMMIT,
        "vertices": len(points),
        "unit_edges": len(edges),
        "unordered_pairs_screened": len(points) * (len(points) - 1) // 2,
        "sieve_primes": [parameters[0] for parameters in SIEVES],
        "single_sieve_candidate_counts": sieve_counts,
        "joint_sieve_candidates": len(edges),
        "exact_survivors_confirmed": len(edges),
        "cartesian_common_denominator": denominator,
        "target_coordinate_sha256": target_hash,
        "cartesian_coordinate_sha256": cartesian_coordinate_hash(points),
        "edge_sha256": edge_hash(edges),
        "patch_vertices_each": 231,
        "patch_unit_edges_each": 924,
        "cross_edges": [list(edge) for edge in cross],
        "unique_articulation_vertices": articulations,
        "bridges": bridges,
        "components_after_461_deletion": list(map(len, blocks)),
        "source_vertices_each": len(source_indices),
        "source_edges_each": len(source_edges),
        "normalized_source_triangle_assignments_tested": 6 ** 6,
        "proper_source_three_colourings": 0,
        "frame_chromatic_numbers": [4, 4],
        "union_chromatic_number": 4,
        "union_colour_class_sizes": class_sizes,
        "cross_neighbour_colours": cross_neighbour_colours,
        "contact_vertex_colour": int(word[461]),
        "record_candidate": False,
    }
    if with_scope:
        result["scope"] = scope_check(repository, points)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", nargs="?", type=Path, default=HERE.parent)
    parser.add_argument("--scope", action="store_true")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = review(args.repository.resolve(), args.scope)
    if args.check_expected:
        expected = "SCOPE_EXPECTED.json" if args.scope else "EXPECTED.json"
        need(result == json.loads((HERE / expected).read_text()), "expected review result")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
