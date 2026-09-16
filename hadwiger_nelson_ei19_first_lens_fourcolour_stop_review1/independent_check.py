#!/usr/bin/env python3
"""Independent exact review of the EI19 first lens four-colour stop.

This checker imports no executable from the reviewed target or its EI19
source.  It replays the rational contraction argument, encloses the lens
formula with Fraction endpoints and an independently rounded square root,
checks the submitted word, and exhausts source three-colourings.
"""

import argparse
import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from math import isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_ei19_first_lens_fourcolour_stop"
SOURCE = ROOT / "hadwiger_nelson_ei19_terminal_boundary"
SOURCE_CERT = SOURCE / "geometry_certificate.json"
SQRT_SCALE = 1 << 192
REVIEWED_TARGET_COMMIT = "bada7569ddcfb515e608d6b043a0558416def00b"

PINNED = {
    TARGET / "README.md": "a210d2bb5150b0b5b044062021d14aa12a5e6d0b37a88b64615345d7b463e9d9",
    TARGET / "PROOF.md": "fb8cb1cbd0cf9905d52ec944525ba6900709041d82607d87f287aed6477ec088",
    TARGET / "PROVENANCE.md": "20ffb00339f1f58a727ee8d608383404db1047e1711b5537fd0150ac425c90d7",
    TARGET / "ARCHITECTURE.md": "5514ecc7932243cb72672a97fc203cd81874fbe29e00f52f651c72ca416cba8e",
    TARGET / "EXPECTED.json": "27dee6013880b82ee13cf221540848413f16df20cd6cbe94c001e3f3ca726c4d",
    TARGET / "four_word.txt": "b0a68784ba59e81066f46615d85b3953c38b70bbca0da91ffb69cfd34ce4bf60",
    TARGET / "intervals.py": "f14059557f64b690f6b60a9e5bfc2a42c45cf9870f0fddac12a6bbe97eef676f",
    TARGET / "verify.py": "3f40dea2118aa033d72e522509568716529b4d43016c6bc7c37025a3355aabdf",
    TARGET / "controls.py": "b4518cc3a2d9c6e054e4f4f5a495d72717fb1061b08bd1c04f395f81f02d75ee",
    SOURCE / "README.md": "ae0c57653224d62f4eafb912b7386a3aa25b1e9fd751670219902026c37632d0",
    SOURCE_CERT: "59e5ead5664daebcc2a68d83c14320976723b69eac7a566a5b4256946ae66fc4",
    SOURCE / "geometry.py": "de149b5ae8d09bdd9115f6d844e2532503923e2761cf6eb5532a7f0a1f50b6a2",
}


class ReviewFailure(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise ReviewFailure(message)


def digest(blob):
    return hashlib.sha256(blob).hexdigest()


def check_pins():
    for path, expected in PINNED.items():
        need(path.is_file(), f"missing pinned file: {path.relative_to(ROOT)}")
        actual = digest(path.read_bytes())
        need(actual == expected, f"hash mismatch: {path.relative_to(ROOT)}")
    return len(PINNED)


def fraction_text(value):
    return str(value)


def audit_source(certificate):
    """Replay the exact contraction and pair-separation argument."""
    need(certificate.get("schema") == "EI19-isolated-unit-equations-v1", "source schema")
    h = certificate.get("point_denominator")
    ad = certificate.get("inverse_denominator")
    rd = certificate.get("radius_denominator")
    need(all(type(value) is int and value > 0 for value in (h, ad, rd)),
         "source denominators")
    radius = Fraction(1, rd)
    centres = certificate.get("centre_numerators")
    inverse = certificate.get("inverse_numerators")
    raw_edges = certificate.get("edge_equations")
    need(isinstance(centres, list) and len(centres) == 19, "source point count")
    need(all(isinstance(row, list) and len(row) == 2 and
             all(type(value) is int for value in row) for row in centres),
         "source point rows")
    need(centres[0] == [0, 0] and centres[1] == [h, 0], "source anchors")
    need(isinstance(inverse, list) and len(inverse) == 34 and
         all(isinstance(row, list) and len(row) == 34 and
             all(type(value) is int for value in row) for row in inverse),
         "inverse matrix dimensions")
    need(isinstance(raw_edges, list), "source edge list")
    edges = [tuple(row) for row in raw_edges]
    need(len(edges) == 35 and edges == sorted(set(edges)) and (0, 1) in edges and
         all(len(edge) == 2 and all(type(value) is int for value in edge) and
             0 <= edge[0] < edge[1] < 19 for edge in edges),
         "source edge equations")

    equations = [edge for edge in edges if edge != (0, 1)]
    jacobian_numerators = [[0] * 34 for _ in range(34)]
    residual_numerators = []
    for equation, (left, right) in enumerate(equations):
        delta = [centres[left][axis] - centres[right][axis] for axis in range(2)]
        residual_numerators.append(sum(value * value for value in delta) - h * h)
        for axis in range(2):
            if left >= 2:
                jacobian_numerators[equation][2 * (left - 2) + axis] = 2 * delta[axis]
            if right >= 2:
                jacobian_numerators[equation][2 * (right - 2) + axis] = -2 * delta[axis]

    defect_numerators = [
        [
            (ad * h if row == column else 0) -
            sum(inverse[row][middle] * jacobian_numerators[middle][column]
                for middle in range(34))
            for column in range(34)
        ]
        for row in range(34)
    ]
    beta = Fraction(
        max(sum(abs(value) for value in row) for row in defect_numerators),
        ad * h,
    )
    inverse_norm = Fraction(
        max(sum(abs(value) for value in row) for row in inverse), ad
    )
    displacement_at_centre = Fraction(
        max(abs(sum(inverse[row][column] * residual_numerators[column]
                    for column in range(34))) for row in range(34)),
        ad * h * h,
    )

    # Each quadratic edge row changes by at most 16*r in row-sum norm
    # throughout the infinity-radius-r box.  This includes the worst case in
    # which both endpoints are variables.
    contraction = beta + 16 * radius * inverse_norm
    self_map = displacement_at_centre + contraction * radius
    need(beta < 1, "A J(midpoint) is not certified invertible")
    need(contraction < 1, "source map is not a contraction")
    need(self_map < radius, "source map is not a strict self-map")

    edge_set = set(edges)
    separation = None
    nonedge_unit_gap = None
    nonedges = 0
    for left, right in combinations(range(19), 2):
        delta = [Fraction(centres[left][axis] - centres[right][axis], h)
                 for axis in range(2)]
        midpoint_d2 = sum(value * value for value in delta)
        error = 4 * radius * sum(abs(value) for value in delta) + 8 * radius * radius
        lower = midpoint_d2 - error
        need(lower > 0, f"source points {left},{right} not separated")
        separation = lower if separation is None else min(separation, lower)
        if (left, right) not in edge_set:
            gap = abs(midpoint_d2 - 1) - error
            need(gap > 0, f"unlisted source pair {left},{right} could be unit")
            nonedge_unit_gap = gap if nonedge_unit_gap is None else min(nonedge_unit_gap, gap)
            nonedges += 1

    return {
        "all_source_pairs": 171,
        "contraction_norm_upper": fraction_text(contraction),
        "fixed_point_displacement_bound": fraction_text(self_map),
        "inverse_norm_upper": fraction_text(inverse_norm),
        "midpoint_defect_norm_upper": fraction_text(beta),
        "nonedge_squared_unit_gap_lower": fraction_text(nonedge_unit_gap),
        "nonedges_excluded": nonedges,
        "radius": fraction_text(radius),
        "root_variables": 34,
        "source_squared_separation_lower": fraction_text(separation),
    }, centres, edges, radius, h


@dataclass(frozen=True)
class Interval:
    lo: Fraction
    hi: Fraction

    def __post_init__(self):
        need(isinstance(self.lo, Fraction) and isinstance(self.hi, Fraction),
             "non-rational interval endpoint")
        need(self.lo <= self.hi, "reversed interval")

    @staticmethod
    def point(value):
        value = Fraction(value)
        return Interval(value, value)

    def __add__(self, other):
        other = as_interval(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-as_interval(other))

    def __rsub__(self, other):
        return as_interval(other) - self

    def __mul__(self, other):
        other = as_interval(other)
        products = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return Interval(min(products), max(products))

    __rmul__ = __mul__

    def reciprocal(self):
        need(not (self.lo <= 0 <= self.hi), "reciprocal interval crosses zero")
        return Interval(1 / self.hi, 1 / self.lo)

    def __truediv__(self, other):
        return self * as_interval(other).reciprocal()

    def square(self):
        if self.lo <= 0 <= self.hi:
            return Interval(Fraction(0), max(self.lo * self.lo, self.hi * self.hi))
        values = self.lo * self.lo, self.hi * self.hi
        return Interval(min(values), max(values))

    def sqrt(self):
        need(self.lo >= 0, "square root of negative interval")
        return Interval(sqrt_lower(self.lo), sqrt_upper(self.hi))


def as_interval(value):
    return value if isinstance(value, Interval) else Interval.point(value)


def sqrt_grid_floor(value):
    """floor(SQRT_SCALE*sqrt(value)) using integer arithmetic only."""
    need(value >= 0, "negative square-root argument")
    return isqrt((value.numerator * SQRT_SCALE * SQRT_SCALE) // value.denominator)


def sqrt_lower(value):
    return Fraction(sqrt_grid_floor(value), SQRT_SCALE)


def sqrt_upper(value):
    k = sqrt_grid_floor(value)
    if k * k * value.denominator == value.numerator * SQRT_SCALE * SQRT_SCALE:
        return Fraction(k, SQRT_SCALE)
    return Fraction(k + 1, SQRT_SCALE)


def norm2(vector):
    return sum((coordinate.square() for coordinate in vector), Interval.point(0))


def source_boxes(centres, radius, denominator):
    boxes = []
    for vertex, row in enumerate(centres):
        uncertainty = Fraction(0) if vertex in (0, 1) else radius
        boxes.append(tuple(
            Interval(Fraction(value, denominator) - uncertainty,
                     Fraction(value, denominator) + uncertainty)
            for value in row
        ))
    return boxes


def first_lens_closure(source_points):
    points = list(source_points)
    included = []
    excluded = []
    for left, right in combinations(range(19), 2):
        a, b = source_points[left], source_points[right]
        delta = b[0] - a[0], b[1] - a[1]
        d2 = norm2(delta)
        need(d2.lo > 0, f"unresolved duplicate source pair {left},{right}")
        need(not (d2.lo <= 4 <= d2.hi),
             f"unresolved tangent source pair {left},{right}")
        if d2.lo > 4:
            excluded.append((left, right))
            continue
        need(d2.hi < 4, f"unresolved circle-intersection pair {left},{right}")
        factor = (d2.reciprocal() - Fraction(1, 4)).sqrt()
        midpoint = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        for sign in (-1, 1):
            points.append((
                midpoint[0] - sign * delta[1] * factor,
                midpoint[1] + sign * delta[0] * factor,
            ))
        included.append((left, right))
    return points, included, excluded


def interval_stream_hash(points):
    rows = []
    for point in points:
        values = []
        for coordinate in point:
            values.extend((coordinate.lo.numerator, coordinate.lo.denominator,
                           coordinate.hi.numerator, coordinate.hi.denominator))
        rows.append(" ".join(map(str, values)) + "\n")
    return digest("".join(rows).encode("ascii"))


def validate_word(points, word):
    need(isinstance(word, str) and len(word) == len(points), "word length")
    need(set(word) <= set("0123"), "word alphabet")
    same = 0
    different = 0
    same_gap = None
    different_gap = None
    for left, right in combinations(range(len(points)), 2):
        if word[left] != word[right]:
            gaps = []
            for first, second in zip(points[left], points[right]):
                gaps.extend((second.lo - first.hi, first.lo - second.hi))
            gap = max(gaps)
            need(gap > 0, f"different-colour boxes overlap: {left},{right}")
            different_gap = gap if different_gap is None else min(different_gap, gap)
            different += 1
        else:
            delta = tuple(first - second
                          for first, second in zip(points[left], points[right]))
            d2 = norm2(delta)
            if d2.hi < 1:
                gap = 1 - d2.hi
            elif d2.lo > 1:
                gap = d2.lo - 1
            else:
                raise ReviewFailure(f"same-colour pair could be unit: {left},{right}")
            same_gap = gap if same_gap is None else min(same_gap, gap)
            same += 1
    return {
        "all_label_pairs": same + different,
        "different_colour_coordinate_gap_lower": fraction_text(different_gap),
        "different_colour_pairs": different,
        "same_colour_pairs": same,
        "same_colour_squared_unit_gap_lower": fraction_text(same_gap),
    }


def boxes_overlap(first, second):
    return all(a.lo <= b.hi and b.lo <= a.hi for a, b in zip(first, second))


def overlap_components(points):
    parent = list(range(len(points)))

    def find(item):
        while parent[item] != item:
            parent[item] = parent[parent[item]]
            item = parent[item]
        return item

    def join(left, right):
        left = find(left)
        right = find(right)
        if left != right:
            parent[right] = left

    overlaps = 0
    for left, right in combinations(range(len(points)), 2):
        if boxes_overlap(points[left], points[right]):
            overlaps += 1
            join(left, right)
    sizes = {}
    for item in range(len(points)):
        root = find(item)
        sizes[root] = sizes.get(root, 0) + 1
    histogram = {}
    for size in sizes.values():
        histogram[size] = histogram.get(size, 0) + 1
    return overlaps, len(sizes), {str(size): histogram[size] for size in sorted(histogram)}


def adjacency(edges, omitted=None):
    graph = [set() for _ in range(19)]
    for left, right in edges:
        if left != omitted and right != omitted:
            graph[left].add(right)
            graph[right].add(left)
    return graph


def three_colour(edges, omitted=None):
    """Complete deterministic DSATUR search, with edge colour symmetry fixed."""
    graph = adjacency(edges, omitted)
    active = [vertex for vertex in range(19) if vertex != omitted]
    first_edge = next((edge for edge in edges if omitted not in edge), None)
    need(first_edge is not None, "no normalization edge")
    colours = [-1] * 19
    colours[first_edge[0]] = 0
    colours[first_edge[1]] = 1
    nodes = 0

    def visit():
        nonlocal nodes
        nodes += 1
        left = [vertex for vertex in active if colours[vertex] < 0]
        if not left:
            return True
        forbidden = {
            vertex: {colours[other] for other in graph[vertex] if colours[other] >= 0}
            for vertex in left
        }
        vertex = max(left, key=lambda item: (
            len(forbidden[item]), len(graph[item]), -item
        ))
        for colour in range(3):
            if colour not in forbidden[vertex]:
                colours[vertex] = colour
                if visit():
                    return True
        colours[vertex] = -1
        return False

    satisfiable = visit()
    word = "".join("-" if vertex == omitted else str(colours[vertex])
                   for vertex in range(19)) if satisfiable else None
    return satisfiable, word, nodes


def check_graph_word(word, edges, omitted=None):
    need(isinstance(word, str) and len(word) == 19, "source word length")
    need(all(character in "012" or (character == "-" and index == omitted)
             for index, character in enumerate(word)), "source word alphabet")
    for left, right in edges:
        if omitted not in (left, right):
            need(word[left] != word[right], f"improper source word on {left},{right}")


def source_criticality(edges):
    satisfiable, word, nodes = three_colour(edges)
    need(not satisfiable and word is None, "EI19 source unexpectedly three-colourable")
    deletion_words = []
    deletion_nodes = []
    for omitted in range(19):
        satisfiable, word, count = three_colour(edges, omitted)
        need(satisfiable, f"source minus vertex {omitted} is not three-colourable")
        check_graph_word(word, edges, omitted)
        deletion_words.append(word)
        deletion_nodes.append(count)
    stream = "".join(f"{vertex} {word}\n" for vertex, word in enumerate(deletion_words))
    return {
        "full_three_colour_exhaustion_nodes": nodes,
        "vertex_critical": True,
        "deletion_search_nodes": deletion_nodes,
        "deletion_words": deletion_words,
        "deletion_word_stream_sha256": digest(stream.encode("ascii")),
    }


def verify():
    pinned_files = check_pins()
    certificate = json.loads(SOURCE_CERT.read_text())
    source_report, centres, edges, radius, denominator = audit_source(certificate)
    source_points = source_boxes(centres, radius, denominator)
    points, included, excluded = first_lens_closure(source_points)
    need(len(included) == 165 and len(excluded) == 6, "lens pair census")
    need(len(points) == 349, "formal closure order")
    word = (TARGET / "four_word.txt").read_text().strip()
    colouring = validate_word(points, word)
    need(all(word[left] != word[right] for left, right in edges),
         "submitted word is improper on the EI19 source")
    overlaps, components, histogram = overlap_components(points)
    criticality = source_criticality(edges)
    return {
        "status": "ACCEPT_AND_STRENGTHEN_EI19_FIRST_LENS_FOUR_COLOUR_STOP",
        "reviewed_target_commit": REVIEWED_TARGET_COMMIT,
        "pinned_public_files": pinned_files,
        "source_vertices": 19,
        "source_unit_edges": 35,
        "source_chromatic_number": 4,
        "source_vertex_critical": criticality,
        "source_geometry": source_report,
        "eligible_source_pairs": len(included),
        "ineligible_source_pairs": len(excluded),
        "formal_lens_labels": 2 * len(included),
        "formal_labels": len(points),
        "physical_vertices_lower_bound": components,
        "physical_vertices_upper_bound": len(points),
        "rectangle_overlap_pairs": overlaps,
        "rectangle_overlap_component_histogram": histogram,
        "independent_sqrt_grid_bits": 192,
        "independent_rectangle_stream_sha256": interval_stream_hash(points),
        "colouring": colouring,
        "word_sha256": digest((word + "\n").encode()),
        "scope": "one fixed isolated EI19 realization and its first two-circle-intersection closure",
        "record_candidate": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    arguments = parser.parse_args()
    result = verify()
    if arguments.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        need(result == expected, "expected output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))
