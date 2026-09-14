#!/usr/bin/env python3
"""Independent audit of the Parts quadratic-switching retraction theorem.

The reviewed module is never imported.  Exact coordinates are represented as
a three-stage quadratic tower Q(sqrt(3))(sqrt(11))(sqrt(5)), rather than the
target's XOR-indexed multiquadratic product.  The checker reconstructs every
host distance, decodes every deletion word, checks the retraction, and emits a
symmetry-free exactly-one four-colour CNF for the 509-point base graph.
"""

import argparse
import base64
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
TARGET = REPOSITORY / "hadwiger_nelson_parts_quadratic_switching_gate"
POINTS_FILE = (REPOSITORY /
               "hadwiger_nelson_parts509_completion_census_degree9/points.tsv")
CRITICALITY = REPOSITORY / "hadwiger_nelson_parts509_criticality"
DENOMINATOR = 96

TARGET_HASHES = {
    "README.md": "eb3956ebffa0e6dfcbb130dc485a09ba3f8e40496e0400d07e42ce54dc4a13b6",
    "SHA256SUMS": "2d9ea05d70e782a2624a392f0eac0d54b354dd7e6bca01c7c7f167346ab16390",
    "expected.json": "9d8f358805d3b6f962b3147af399a70127b78afd6b54657061e0581b4bb8e068",
    "manifest.json": "9e76bd2f21060b2248cab52c5c176ea5bbb4a7c9ab8a5ea8f22c55aef10fea64",
    "validation.json": "99e798f4793cacd27245378e4d032300f6d550f978e3a8a58ad065eb23928329",
    "verify.py": "41e679d010b39b5a9b5863b9e358612796bb72b54e7b99b787429f6a4dd58694",
}
INPUT_HASHES = {
    POINTS_FILE:
        "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50",
    CRITICALITY / "certificate.json":
        "d354f9629c41639168b80fc1aa6feb6e4187dd37dee7efcb83b4ef6ebe68d16c",
    CRITICALITY / "parts509.vtx":
        "770a585a6c1e1222355322707479cb826e9ada560279da904ef89c15c99ff0b5",
}


class AuditError(RuntimeError):
    pass


def require(condition, detail):
    if not condition:
        raise AuditError(detail)


def file_digest(path):
    return sha256(path.read_bytes()).hexdigest()


# Q(sqrt(3)); an element is a+b*sqrt(3).
def q3_add(left, right):
    return left[0] + right[0], left[1] + right[1]


def q3_neg(value):
    return -value[0], -value[1]


def q3_scale(value, scalar):
    return value[0] * scalar, value[1] * scalar


def q3_mul(left, right):
    a, b = left
    c, d = right
    return a * c + 3 * b * d, a * d + b * c


# Q(sqrt(3),sqrt(11)); an element is a+b*sqrt(11), with a,b in Q(sqrt(3)).
def q311_add(left, right):
    return q3_add(left[0], right[0]), q3_add(left[1], right[1])


def q311_neg(value):
    return q3_neg(value[0]), q3_neg(value[1])


def q311_scale(value, scalar):
    return q3_scale(value[0], scalar), q3_scale(value[1], scalar)


def q311_mul(left, right):
    a, b = left
    c, d = right
    return (q3_add(q3_mul(a, c), q3_scale(q3_mul(b, d), 11)),
            q3_add(q3_mul(a, d), q3_mul(b, c)))


# Full field: A+B*sqrt(5), with A,B in Q(sqrt(3),sqrt(11)).
def field_add(left, right):
    return q311_add(left[0], right[0]), q311_add(left[1], right[1])


def field_neg(value):
    return q311_neg(value[0]), q311_neg(value[1])


def field_sub(left, right):
    return field_add(left, field_neg(right))


def field_mul(left, right):
    a, b = left
    c, d = right
    return (q311_add(q311_mul(a, c), q311_scale(q311_mul(b, d), 5)),
            q311_add(q311_mul(a, d), q311_mul(b, c)))


def field_square(value):
    return field_mul(value, value)


def from_flat(values):
    require(len(values) == 8, "flat field width")
    return (((values[0], values[1]), (values[4], values[5])),
            ((values[2], values[3]), (values[6], values[7])))


def to_flat(value):
    return (value[0][0][0], value[0][0][1],
            value[1][0][0], value[1][0][1],
            value[0][1][0], value[0][1][1],
            value[1][1][0], value[1][1][1])


ZERO = from_flat((0,) * 8)
UNIT_SQUARED = from_flat((DENOMINATOR * DENOMINATOR,) + (0,) * 7)


def conjugate_field(value):
    """Negate sqrt(5), fixing sqrt(3) and sqrt(11)."""
    return value[0], q311_neg(value[1])


def conjugate_point(point):
    return conjugate_field(point[0]), conjugate_field(point[1])


def squared_distance(left, right):
    dx = field_sub(left[0], right[0])
    dy = field_sub(left[1], right[1])
    return field_add(field_square(dx), field_square(dy))


def read_points():
    lines = POINTS_FILE.read_text().splitlines()
    require(lines[0] ==
            "# basis=1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165 scale=96",
            "point header")
    points = []
    for line in lines[1:]:
        if not line:
            continue
        words = tuple(map(int, line.split()))
        require(len(words) == 16, "point width")
        points.append((from_flat(words[:8]), from_flat(words[8:])))
    require(len(points) == 509 and len(set(points)) == 509,
            "base point census")
    return tuple(points)


def build_edges(points):
    return tuple(
        (first, second)
        for first, second in combinations(range(len(points)), 2)
        if squared_distance(points[first], points[second]) == UNIT_SQUARED
    )


def edge_digest(edges, separator):
    return sha256("".join(f"{a}{separator}{b}\n" for a, b in edges).encode()).hexdigest()


def check_word(edges, colours, missing=None):
    for first, second in edges:
        if first == missing or second == missing:
            continue
        require(colours[first] != colours[second],
                ("monochromatic edge", first, second, colours[first]))


def decode_words(document):
    require(document["format"] == "parts509-vertex-criticality-v1",
            "certificate format")
    require(document["vertices"] == 509 and document["edges"] == 2442,
            "certificate graph domain")
    require(document["deletion_row_packing"] ==
            "four 2-bit colors, low bits first, vertices in increasing order with the deleted vertex omitted",
            "packing declaration")
    packed = base64.b64decode(document["deletion_colorings_base64"], validate=True)
    require(len(packed) == 509 * 127, "packed size")
    require(sha256(packed).hexdigest() ==
            "be5c4c0d333552334ae6d343d000f84456be50f8ef9e7f95d64ca92779390d36",
            "packed digest")
    words = []
    for missing in range(509):
        colours = []
        for vertex in range(509):
            if vertex == missing:
                colours.append(None)
                continue
            index = vertex - (vertex > missing)
            byte = packed[127 * missing + index // 4]
            colours.append((byte >> (2 * (index % 4))) & 3)
        words.append(tuple(colours))
    return tuple(words)


def projection_check(host_edges, base_edges, projection):
    base = set(base_edges)
    for first, second in host_edges:
        image = projection[first], projection[second]
        require(image[0] != image[1], ("edge collapsed", first, second))
        require(tuple(sorted(image)) in base,
                ("edge outside base image", first, second, image))


def variable(vertex, colour):
    return 4 * vertex + colour + 1


def colouring_clauses(order, edges):
    clauses = []
    for vertex in range(order):
        clauses.append(tuple(variable(vertex, colour) for colour in range(4)))
        for first, second in combinations(range(4), 2):
            clauses.append((-variable(vertex, first), -variable(vertex, second)))
    for left, right in edges:
        for colour in range(4):
            clauses.append((-variable(left, colour), -variable(right, colour)))
    return tuple(clauses)


def cnf_bytes(order, edges):
    clauses = colouring_clauses(order, edges)
    body = "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return clauses, f"p cnf {4 * order} {len(clauses)}\n{body}".encode()


def satisfies(clauses, truth):
    return all(any(truth[abs(literal) - 1] == (literal > 0)
                   for literal in clause)
               for clause in clauses)


def cnf_controls():
    checks = 0
    for order in range(4):
        possible_edges = tuple(combinations(range(order), 2))
        for graph_mask in range(1 << len(possible_edges)):
            edges = tuple(edge for index, edge in enumerate(possible_edges)
                          if graph_mask & (1 << index))
            clauses = colouring_clauses(order, edges)
            for truth_mask in range(1 << (4 * order)):
                truth = tuple(bool(truth_mask & (1 << index))
                              for index in range(4 * order))
                chosen = [tuple(colour for colour in range(4)
                                if truth[4 * vertex + colour])
                          for vertex in range(order)]
                direct = (all(len(row) == 1 for row in chosen) and
                          all(chosen[a][0] != chosen[b][0] for a, b in edges))
                require(satisfies(clauses, truth) == direct,
                        ("CNF control", order, graph_mask, truth_mask))
                checks += 1
    return checks


def arithmetic_controls():
    radicands = (3, 5, 11)
    checks = 0
    for first in range(8):
        for second in range(8):
            a = [0] * 8
            b = [0] * 8
            a[first] = 1
            b[second] = 1
            common = first & second
            coefficient = 1
            for bit, radicand in enumerate(radicands):
                if common & (1 << bit):
                    coefficient *= radicand
            expected = [0] * 8
            expected[first ^ second] = coefficient
            require(to_flat(field_mul(from_flat(a), from_flat(b))) == tuple(expected),
                    ("tower product", first, second))
            require(conjugate_field(field_mul(from_flat(a), from_flat(b))) ==
                    field_mul(conjugate_field(from_flat(a)),
                              conjugate_field(from_flat(b))),
                    ("conjugation product", first, second))
            checks += 1
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf-out", type=Path, required=True)
    args = parser.parse_args()

    for name, expected in TARGET_HASHES.items():
        require(file_digest(TARGET / name) == expected, ("target hash", name))
    for path, expected in INPUT_HASHES.items():
        require(file_digest(path) == expected, ("input hash", path.name))

    arithmetic_checks = arithmetic_controls()
    points = read_points()
    fixed = tuple(index for index, point in enumerate(points)
                  if conjugate_point(point) == point)
    require(fixed == tuple(range(374)), "fixed-label block")
    host = points + tuple(conjugate_point(point) for point in points[374:])
    require(len(host) == 644 and len(set(host)) == 644, "host point census")

    host_edges = build_edges(host)
    base_edges = tuple(edge for edge in host_edges if edge[1] < 509)
    require(len(base_edges) == 2442 and len(host_edges) == 3024,
            ("edge census", len(base_edges), len(host_edges)))
    projection = tuple(range(509)) + tuple(range(374, 509))
    cross_edges = tuple(edge for edge in host_edges
                        if 374 <= edge[0] < 509 <= edge[1])
    require(not cross_edges, ("cross-sheet edges", cross_edges[:1]))
    projection_check(host_edges, base_edges, projection)

    certificate = json.loads((CRITICALITY / "certificate.json").read_text())
    require(edge_digest(base_edges, " ") == certificate["edge_sha256"],
            "base edge digest differs from criticality certificate")
    words = decode_words(certificate)
    base_checks = 0
    neighbour_surjectivity = 0
    neighbours = [set() for _ in range(509)]
    for first, second in base_edges:
        neighbours[first].add(second)
        neighbours[second].add(first)
    for missing, colours in enumerate(words):
        check_word(base_edges, colours, missing)
        base_checks += sum(missing not in edge for edge in base_edges)
        require({colours[v] for v in neighbours[missing]} == {0, 1, 2, 3},
                ("neighbour palette", missing))
        neighbour_surjectivity += 1

    five = tuple(map(int, certificate["five_coloring"]))
    require(len(five) == 509 and set(five) <= set(range(5)), "five-colour domain")
    check_word(base_edges, five)
    host_five = tuple(five[label] for label in projection)
    check_word(host_edges, host_five)

    lifted_checks = 0
    fibre_orders = []
    for missing, colours in enumerate(words):
        for first, second in host_edges:
            a, b = projection[first], projection[second]
            if a == missing or b == missing:
                continue
            require(colours[a] != colours[b],
                    ("lifted monochromatic edge", missing, first, second))
            lifted_checks += 1
        fibre_orders.append(sum(label != missing for label in projection))
    require(fibre_orders.count(643) == 374 and fibre_orders.count(642) == 135,
            "whole-fibre support sizes")

    type_counts = {
        "large_large": sum(second < 374 for _, second in host_edges),
        "large_original_small": sum(first < 374 <= second < 509
                                    for first, second in host_edges),
        "original_small_original_small": sum(374 <= first < second < 509
                                             for first, second in host_edges),
        "large_conjugate_small": sum(first < 374 and second >= 509
                                     for first, second in host_edges),
        "original_small_conjugate_small": len(cross_edges),
        "conjugate_small_conjugate_small": sum(first >= 509
                                               for first, _ in host_edges),
    }
    require(sum(type_counts.values()) == len(host_edges), "edge-type partition")

    clauses, cnf = cnf_bytes(509, base_edges)
    args.cnf_out.parent.mkdir(parents=True, exist_ok=True)
    args.cnf_out.write_bytes(cnf)
    control_count = cnf_controls()

    result = {
        "status": "INDEPENDENT QUADRATIC-SWITCHING RETRACTION AUDIT PASSED; BASE FOUR-COLOUR CNF EMITTED",
        "base_points": 509,
        "base_edges": len(base_edges),
        "fixed_points": len(fixed),
        "nonfixed_points": 135,
        "host_points": len(host),
        "host_edges": len(host_edges),
        "complete_pair_checks": len(host) * (len(host) - 1) // 2,
        "mixed_pair_checks": 135 * 135,
        "mixed_unit_edges": len(cross_edges),
        "edge_type_counts": type_counts,
        "projection_failures": 0,
        "base_edge_sha256": edge_digest(base_edges, " "),
        "host_edge_sha256": edge_digest(host_edges, ","),
        "host_point_sha256": sha256(json.dumps(
            [[list(to_flat(axis)) for axis in point] for point in host],
            separators=(",", ":")).encode()).hexdigest(),
        "projection_sha256": sha256(json.dumps(
            projection, separators=(",", ":")).encode()).hexdigest(),
        "base_deletion_words_checked": len(words),
        "base_word_edge_checks": base_checks,
        "neighbour_surjectivity_checks": neighbour_surjectivity,
        "lifted_whole_fibre_words_checked": len(words),
        "lifted_word_edge_checks": lifted_checks,
        "whole_fibre_support_sizes": {"642": 135, "643": 374},
        "proper_base_five_colouring": True,
        "proper_host_five_colouring": True,
        "pigeonhole_source_cap": 508,
        "pigeonhole_target_order": 509,
        "all_at_most_508_host_subgraphs_four_colourable": True,
        "arithmetic_controls": arithmetic_checks,
        "cnf_semantics_controls": control_count,
        "base_four_colour_cnf_variables": 2036,
        "base_four_colour_cnf_clauses": len(clauses),
        "base_four_colour_cnf_bytes": len(cnf),
        "base_four_colour_cnf_sha256": sha256(cnf).hexdigest(),
        "base_non_four_colourability_requires_checked_external_proof": True,
        "physical_host_constructed": True,
        "record_improvement": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
