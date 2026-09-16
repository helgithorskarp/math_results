#!/usr/bin/env python3
"""Independent exact review of the 481-point opposed-core assembly.

No target executable is imported.  Geometry is rebuilt in the flat basis

    1, sqrt(3), sqrt(11), sqrt(33), t, sqrt(3)t, sqrt(11)t, sqrt(33)t,

where t^2=(2+2*sqrt(33))/3.  This differs from the target's K+Kt
implementation with separately normalized y coordinates.  A deterministic
DSATUR search produces a fresh proper four-colouring.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_opposed241_twenty_contact_stop"
SOURCE = ROOT / "hadwiger_nelson_opposed241_conditional_core"
B214 = ROOT / "hadwiger_nelson_nonmono159_214_lowden2" / "points214.tsv"
SOURCE_REVIEW = ROOT / "hadwiger_nelson_opposed241_conditional_core_review1"

REVIEWED_MATHEMATICAL_COMMIT = "3d0415fe410c7a0fa5b18aaacf71a7049014d382"
REVIEWED_PACKAGING_COMMIT = "e5deefabadbf4956986be5e6437d3248199e2838"

PINNED = {
    TARGET / "README.md":
        "131d357e81d3e3a45b791d25c95a3194224496fa88bae2b0268ecbc0969df0d5",
    TARGET / "PROOF.md":
        "59d15d4138f8e977b1f02357fc6ad3bc7993fc0417ae3dede31681f97d2d9d18",
    TARGET / "EXPECTED.json":
        "6a3ad778f3cb025137c77066714727df35ed00939fa6a62904668422014449dd",
    TARGET / "PUBLICATION.json":
        "1af13255a48a668b7f3bc30e02f90076a5934d8af2c4b946b236e1dd515a52cb",
    TARGET / "certificate.json":
        "79c26a35423f943120fafdae695e73f4764da5515bf9717d643fd254710e0b1a",
    TARGET / "verify.py":
        "d214bb5c4457dbf53eda248ba81c6834048f1d05a8b965dc2b8af97302be6b5a",
    TARGET / "controls.py":
        "bf829d41f107dfb52cdf2c214b5c561c5216895a03e7b89aaae1a9f60b115730",
    SOURCE / "certificate.json":
        "37e1397276f931ee1b9b63f4ca5c343a2ac129fa3b1c6d526e4c151031a750e4",
    B214:
        "97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f",
    SOURCE_REVIEW / "README.md":
        "e31e53a614713b00a8d05f4c48410c8bbbf76e45dccfc8c79613e54bb8d941bf",
    SOURCE_REVIEW / "EXPECTED.json":
        "b948ac102a499e4c8068a4f85ca0ab22a8e40435b8dd61124da118bb4700e230",
}

BASIS = 8
ZERO = (F(0),) * BASIS
ONE = (F(1),) + (F(0),) * (BASIS - 1)


class ReviewFailure(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise ReviewFailure(message)


def sha256(blob):
    return hashlib.sha256(blob).hexdigest()


def stream_hash(rows):
    return sha256(("\n".join(rows) + "\n").encode("ascii"))


def check_pins():
    for path, expected in PINNED.items():
        need(path.is_file(), f"missing pinned file: {path.relative_to(ROOT)}")
        need(sha256(path.read_bytes()) == expected,
             f"hash mismatch: {path.relative_to(ROOT)}")
    publication = json.loads((TARGET / "PUBLICATION.json").read_text())
    need(publication["source_commit"] == REVIEWED_MATHEMATICAL_COMMIT,
         "publication source commit")
    return len(PINNED)


def element(**terms):
    """Make an element; keys are e0,...,e7."""
    out = [F(0)] * BASIS
    for key, value in terms.items():
        need(key.startswith("e") and key[1:].isdigit(), "element key")
        index = int(key[1:])
        need(0 <= index < BASIS, "element basis index")
        out[index] = F(value)
    return tuple(out)


def add(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def neg(value):
    return tuple(-a for a in value)


def sub(left, right):
    return add(left, neg(right))


def scale(value, scalar):
    scalar = F(scalar)
    return tuple(scalar * a for a in value)


def monomial_product(first, second):
    """Return sparse expansion of two basis monomials.

    Basis index i+2*j+4*k denotes a^i b^j t^k, with a^2=3,
    b^2=11, and t^2=(2+2ab)/3.
    """
    ai = (first & 1) + (second & 1)
    bi = ((first >> 1) & 1) + ((second >> 1) & 1)
    ti = ((first >> 2) & 1) + ((second >> 2) & 1)
    terms = [(F(1), ai, bi, ti)]
    if ti == 2:
        terms = [(coefficient * F(2, 3), aa, bb, 0)
                 for coefficient, aa, bb, _ in terms] + [
                    (coefficient * F(2, 3), aa + 1, bb + 1, 0)
                    for coefficient, aa, bb, _ in terms
                 ]
    out = []
    for coefficient, aa, bb, tt in terms:
        while aa >= 2:
            coefficient *= 3
            aa -= 2
        while bb >= 2:
            coefficient *= 11
            bb -= 2
        out.append((coefficient, aa + 2 * bb + 4 * tt))
    return tuple(out)


PRODUCT_TABLE = tuple(
    tuple(monomial_product(first, second) for second in range(BASIS))
    for first in range(BASIS)
)


def multiply(left, right):
    out = [F(0)] * BASIS
    for first, a in enumerate(left):
        if not a:
            continue
        for second, b in enumerate(right):
            if not b:
                continue
            for coefficient, target in PRODUCT_TABLE[first][second]:
                out[target] += a * b * coefficient
    return tuple(out)


def square(value):
    out = [F(0)] * BASIS
    active = [(index, coefficient) for index, coefficient in enumerate(value)
              if coefficient]
    for position, (first, a) in enumerate(active):
        for second, b in active[position:]:
            symmetry = 1 if first == second else 2
            for coefficient, target in PRODUCT_TABLE[first][second]:
                out[target] += symmetry * a * b * coefficient
    return tuple(out)


A = element(e1=1)
B = element(e2=1)
C = element(e3=1)
T = add(scale(ONE, F(2, 3)), scale(C, F(2, 3)))
TROOT = element(e4=1)


def point(x=ZERO, y=ZERO):
    return (x, y)


def translate_x(p, amount):
    return (add(p[0], scale(ONE, amount)), p[1])


def reflect_vertical(p):
    return (neg(p[0]), p[1])


def squared_distance(first, second):
    return add(square(sub(first[0], second[0])),
               square(sub(first[1], second[1])))


def is_unit(first, second):
    return squared_distance(first, second) == ONE


def exact_edges(points):
    return [(first, second)
            for first, second in combinations(range(len(points)), 2)
            if is_unit(points[first], points[second])]


def merge_blocks(*blocks):
    points = []
    index = {}
    maps = []
    for block in blocks:
        image = []
        for value in block:
            if value not in index:
                index[value] = len(points)
                points.append(value)
            image.append(index[value])
        maps.append(image)
    return points, maps


def golomb_points():
    rows = (
        (0, 0, 0, 0), (36, 0, 0, 0), (18, 0, 18, 0),
        (-18, 0, 18, 0), (-36, 0, 0, 0), (-18, 0, -18, 0),
        (18, 0, -18, 0), (6, 0, 0, 6), (-3, -3, 3, -3),
        (-3, 3, -3, -3),
    )
    return [point(add(scale(ONE, F(a, 36)), scale(C, F(b, 36))),
                  add(scale(A, F(c, 36)), scale(B, F(d, 36))))
            for a, b, c, d in rows]


def b214_points():
    out = []
    for line in B214.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        need(len(row) == 16, "B214 coordinate arity")
        need(all(row[index] == 0 for index in range(16)
                 if index not in (0, 5, 9, 12)), "B214 subfield support")
        x = add(scale(ONE, F(row[0], 12)), scale(C, F(row[5], 12)))
        y = add(scale(A, F(row[9], 12)), scale(B, F(row[12], 12)))
        out.append(point(x, y))
    need(len(out) == len(set(out)) == 214, "B214 point order")
    return out


def source_points():
    bpoints = b214_points()
    left = [translate_x(value, F(-1, 2)) for value in bpoints]
    right = [translate_x(reflect_vertical(value), F(1, 2)) for value in bpoints]
    parent, _ = merge_blocks(golomb_points(), left, right)
    need(len(parent) == 343, "opposed parent order")
    certificate = json.loads((SOURCE / "certificate.json").read_text())
    labels = certificate["source_ids"]
    need(labels == sorted(set(labels)) and len(labels) == 241 and
         labels[:10] == list(range(10)), "conditional-core labels")
    source = [parent[label] for label in labels]
    need(len(source) == len(set(source)) == 241, "source point order")
    return source


def rational_string(value):
    return f"{value.numerator}/{value.denominator}"


def source_point_hash(points):
    """Match the prior review's 36-scaled E-coordinate stream."""
    rows = []
    for x, y in points:
        need(all(value.denominator == 1 for value in scale(x, 36) + scale(y, 36)),
             "source common denominator")
        # Prior basis order selected 1,a,b,c as old indices 0,1,4,5.
        values = (x[0], x[1], x[2], x[3], y[0], y[1], y[2], y[3])
        rows.append(" ".join(str(int(36 * value)) for value in values))
    return stream_hash(rows)


def target_point_hash(points):
    """Independently translate the flat physical basis to the target stream."""
    rows = []
    for x, y in points:
        need(all(x[index] == 0 for index in (1, 2, 5, 6)),
             "x outside K+Kt")
        need(all(y[index] == 0 for index in (0, 3, 4, 7)),
             "y outside sqrt(3)(K+Kt)")
        # Divide the physical y by a=sqrt(3): b/a=ab/3.
        values = (x[0], x[3], x[4], x[7],
                  y[1], y[2] / 3, y[5], y[6] / 3)
        rows.append(" ".join(rational_string(value) for value in values))
    return stream_hash(rows)


def native_point_hash(points):
    return stream_hash(
        " ".join(rational_string(value) for value in x + y)
        for x, y in points
    )


def edge_hash(edges):
    return stream_hash(f"{first} {second}" for first, second in edges)


def rotation():
    co = add(add(scale(ONE, F(1, 4)), scale(C, F(1, 12))),
             multiply(add(scale(ONE, F(-5, 16)), scale(C, F(1, 16))),
                      TROOT))
    sy = add(add(scale(ONE, F(-5, 12)), scale(C, F(1, 12))),
             multiply(add(scale(ONE, F(-1, 16)), scale(C, F(-1, 48))),
                      TROOT))
    sine = multiply(A, sy)
    need(add(square(co), square(sine)) == ONE, "rotation unit norm")
    return co, sine


def rotate(value, cosine, sine):
    x, y = value
    return (sub(multiply(cosine, x), multiply(sine, y)),
            add(multiply(sine, x), multiply(cosine, y)))


def adjacency(vertices, edges):
    out = [set() for _ in range(vertices)]
    for first, second in edges:
        out[first].add(second)
        out[second].add(first)
    return out


def graph_structure(vertices, edges):
    graph = adjacency(vertices, edges)
    discovery = [-1] * vertices
    low = [0] * vertices
    timer = 0
    articulations = set()
    bridges = set()
    components = 0

    def visit(vertex, parent=-1):
        nonlocal timer
        discovery[vertex] = low[vertex] = timer
        timer += 1
        children = 0
        for other in sorted(graph[vertex]):
            if other == parent:
                continue
            if discovery[other] >= 0:
                low[vertex] = min(low[vertex], discovery[other])
            else:
                visit(other, vertex)
                children += 1
                low[vertex] = min(low[vertex], low[other])
                if low[other] > discovery[vertex]:
                    bridges.add((min(vertex, other), max(vertex, other)))
                if parent >= 0 and low[other] >= discovery[vertex]:
                    articulations.add(vertex)
        if parent < 0 and children > 1:
            articulations.add(vertex)

    for start in range(vertices):
        if discovery[start] < 0:
            components += 1
            visit(start)

    live = set(range(vertices))
    queue = [vertex for vertex in live if len(graph[vertex]) < 4]
    while queue:
        vertex = queue.pop()
        if vertex not in live:
            continue
        live.remove(vertex)
        for other in graph[vertex] & live:
            if len(graph[other] & live) < 4:
                queue.append(other)
    return graph, {
        "components": components,
        "articulation_vertices": len(articulations),
        "bridges": len(bridges),
        "four_core_vertices": len(live),
        "minimum_degree": min(map(len, graph)),
        "maximum_degree": max(map(len, graph)),
    }


def proper(word, vertices, edges):
    return (isinstance(word, str) and len(word) == vertices and
            set(word) <= set("0123") and
            all(word[first] != word[second] for first, second in edges))


def golomb_audit(points):
    edges = exact_edges(points[:10])
    need(len(edges) == 18, "Golomb edge count")
    three_words = 0
    for tail in product(range(3), repeat=7):
        word = (0, 1, 2) + tail
        if all(word[first] != word[second] for first, second in edges):
            three_words += 1
    need(three_words == 0, "Golomb three-colouring")
    return edges, 3 ** 7


def fresh_four_colouring(vertices, edges):
    """Deterministic direct-assignment DSATUR, with only a triangle pinned."""
    graph = adjacency(vertices, edges)
    triangle = None
    for first in range(10):
        for second in sorted(graph[first]):
            if second >= 10:
                continue
            common = sorted((graph[first] & graph[second]) & set(range(10)))
            if common:
                triangle = tuple(sorted((first, second, common[0])))
                break
        if triangle is not None:
            break
    need(triangle == (0, 1, 2), "normalized Golomb triangle")
    colours = [-1] * vertices
    for vertex, colour in zip(triangle, range(3), strict=True):
        colours[vertex] = colour
    nodes = 0
    backtracks = 0

    def search(uncoloured):
        nonlocal nodes, backtracks
        nodes += 1
        if not uncoloured:
            return True
        selected = None
        available = None
        selected_key = None
        for vertex in uncoloured:
            used = {colours[other] for other in graph[vertex]
                    if colours[other] >= 0}
            choices = tuple(colour for colour in range(4) if colour not in used)
            key = (len(used), sum(other in uncoloured for other in graph[vertex]),
                   len(graph[vertex]), -vertex)
            if selected_key is None or key > selected_key:
                selected = vertex
                selected_key = key
                available = choices
        if not available:
            return False
        remainder = uncoloured - {selected}
        for colour in available:
            colours[selected] = colour
            if search(remainder):
                return True
        colours[selected] = -1
        backtracks += 1
        return False

    need(search(set(range(vertices)) - set(triangle)), "fresh four-colouring")
    word = "".join(map(str, colours))
    need(proper(word, vertices, edges), "fresh four-word verification")
    return word, triangle, nodes, backtracks


def cross_structure(cross_edges, first_vertices, second_vertices):
    participants = set(vertex for edge in cross_edges for vertex in edge)
    graph = {vertex: set() for vertex in participants}
    for first, second in cross_edges:
        graph[first].add(second)
        graph[second].add(first)
    seen = set()
    shapes = []
    for start in sorted(participants):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        block = set()
        edge_twice = 0
        while stack:
            vertex = stack.pop()
            block.add(vertex)
            edge_twice += len(graph[vertex])
            for other in graph[vertex]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        shapes.append((len(block), edge_twice // 2))
    shapes.sort()
    need(all((len(graph[vertex]) <= 2) for vertex in participants),
         "cross maximum degree")
    need(all(edges == vertices - 1 for vertices, edges in shapes),
         "cross contact forest")

    # Exact bipartite maximum matching by augmenting paths.
    left = sorted(participants & set(first_vertices))
    right_set = participants & set(second_vertices)
    match = {}

    def augment(vertex, visited):
        for other in sorted(graph[vertex] & right_set):
            if other in visited:
                continue
            visited.add(other)
            if other not in match or augment(match[other], visited):
                match[other] = vertex
                return True
        return False

    matching = sum(augment(vertex, set()) for vertex in left)
    return {
        "participating_vertices": len(participants),
        "first_copy_vertices": len(participants & set(first_vertices)),
        "second_copy_vertices": len(participants & set(second_vertices)),
        "components": len(shapes),
        "isolated_edges": shapes.count((2, 1)),
        "length_two_paths": shapes.count((3, 2)),
        "cycles": 0,
        "maximum_cross_degree": max(map(len, graph.values())),
        "maximum_matching": matching,
    }


def validate_submitted_certificate(certificate, data):
    need(certificate["schema"] == "opposed241-twenty-contact-stop-v1", "schema")
    need(certificate["rotation_contact_source_indices"] == [45, 65],
         "rotation source indices")
    need(certificate["rotation_branch"] == "positive_t", "rotation branch")
    need([tuple(edge) for edge in certificate["cross_edges"]] == data["cross_edges"],
         "submitted cross-edge list")
    need(certificate["point_sha256"] == data["point_sha256"],
         "submitted point hash")
    need(certificate["edge_sha256"] == data["edge_sha256"],
         "submitted edge hash")
    need(proper(certificate["proper4"], 481, data["edges"]),
         "submitted four-word")


def reconstruct():
    need(multiply(A, A) == scale(ONE, 3), "sqrt(3) relation")
    need(multiply(B, B) == scale(ONE, 11), "sqrt(11) relation")
    need(multiply(A, B) == C, "sqrt(33) relation")
    need(multiply(TROOT, TROOT) == T, "t relation")
    norm_t_squared = F(2, 3) ** 2 - 33 * F(2, 3) ** 2
    need(norm_t_squared == F(-128, 9), "negative quadratic norm")
    norm_t_squared_over_three = F(2, 9) ** 2 - 33 * F(2, 9) ** 2
    need(norm_t_squared_over_three == F(-128, 81),
         "negative norm after adjoining sqrt(3)")

    source = source_points()
    source_edges = exact_edges(source)
    need(len(source_edges) == 991, "source edge count")
    source_ph = source_point_hash(source)
    source_eh = edge_hash(source_edges)
    source_expected = json.loads((SOURCE_REVIEW / "EXPECTED.json").read_text())
    need(source_expected["status"] == "ACCEPTED_INDEPENDENT_CONDITIONAL_CORE_REVIEW" and
         source_expected["points"] == 241 and
         source_expected["complete_unit_edges"] == 991 and
         source_expected["point_hash"] == source_ph and
         source_expected["edge_hash"] == source_eh,
         "prior independent source-review alignment")

    cosine, sine = rotation()
    first = source
    second = [rotate(value, cosine, sine) for value in source]
    need(is_unit(first[45], second[65]), "defining private contact")
    points, maps = merge_blocks(first, second)
    overlap = set(maps[0]) & set(maps[1])
    need(len(points) == 481 and overlap == {0}, "collision quotient")

    edges = exact_edges(points)
    first_set, second_set = set(maps[0]), set(maps[1])
    inherited = [edge for edge in edges
                 if set(edge) <= first_set or set(edge) <= second_set]
    cross = [edge for edge in edges if edge not in set(inherited)]
    need(len(edges) == 2002 and len(inherited) == 1982 and len(cross) == 20,
         "complete edge partition")
    need(sum(set(edge) <= first_set for edge in inherited) == 991 and
         sum(set(edge) <= second_set for edge in inherited) == 991,
         "copy edge counts")

    point_sha = target_point_hash(points)
    edge_sha = edge_hash(edges)
    need(point_sha == "9ac902c4f179dbe1c1a3a2c76dab6225f77c7969041e9feef18d5455082adff6",
         "target point identity")
    need(edge_sha == "57296047b72d08a553b2a84b22db353ad5a6af29369314e3bf74fa01ac4a287f",
         "target edge identity")

    graph, structure = graph_structure(481, edges)
    need(structure == {
        "components": 1,
        "articulation_vertices": 0,
        "bridges": 0,
        "four_core_vertices": 481,
        "minimum_degree": 4,
        "maximum_degree": 48,
    }, "full graph structure")
    golomb_edges, three_assignments = golomb_audit(source)
    fresh_word, triangle, nodes, backtracks = fresh_four_colouring(481, edges)
    cross_audit = cross_structure(cross, first_set, second_set)
    need(cross_audit == {
        "participating_vertices": 33,
        "first_copy_vertices": 17,
        "second_copy_vertices": 16,
        "components": 13,
        "isolated_edges": 6,
        "length_two_paths": 7,
        "cycles": 0,
        "maximum_cross_degree": 2,
        "maximum_matching": 13,
    }, "cross-contact structure")

    return {
        "source": source,
        "source_edges": source_edges,
        "source_point_sha256": source_ph,
        "source_edge_sha256": source_eh,
        "points": points,
        "edges": edges,
        "maps": maps,
        "cross_edges": cross,
        "point_sha256": point_sha,
        "edge_sha256": edge_sha,
        "native_point_sha256": native_point_hash(points),
        "structure": structure,
        "golomb_edges": golomb_edges,
        "three_assignments": three_assignments,
        "fresh_word": fresh_word,
        "fresh_triangle": triangle,
        "fresh_nodes": nodes,
        "fresh_backtracks": backtracks,
        "cross_structure": cross_audit,
        "norm_t_squared": norm_t_squared,
        "norm_t_squared_over_three": norm_t_squared_over_three,
    }


def verify():
    pinned = check_pins()
    data = reconstruct()
    certificate = json.loads((TARGET / "certificate.json").read_text())
    validate_submitted_certificate(certificate, data)
    fresh_hash = sha256((data["fresh_word"] + "\n").encode("ascii"))
    submitted_hash = sha256((certificate["proper4"] + "\n").encode("ascii"))
    distance = sum(first != second for first, second in
                   zip(data["fresh_word"], certificate["proper4"], strict=True))
    need(fresh_hash == "0f0714865d39e756ea43a13f9998f8c1054d5427b9062a47246901cbe94d2b43",
         "fresh four-word identity")
    need(data["fresh_nodes"] == 7054 and data["fresh_backtracks"] == 6279,
         "fresh DSATUR deterministic census")
    need(distance == 304 and fresh_hash != submitted_hash,
         "fresh colouring independence")

    return {
        "status": "ACCEPT_AND_STRENGTHEN_OPPOSED241_TWENTY_CONTACT_STOP",
        "reviewed_mathematical_commit": REVIEWED_MATHEMATICAL_COMMIT,
        "reviewed_packaging_commit": REVIEWED_PACKAGING_COMMIT,
        "pinned_public_files": pinned,
        "exact_field": {
            "basis": ["1", "sqrt3", "sqrt11", "sqrt33", "t",
                      "sqrt3*t", "sqrt11*t", "sqrt33*t"],
            "t_squared": "(2+2*sqrt33)/3",
            "norm_of_t_squared": str(data["norm_t_squared"]),
            "norm_of_t_squared_over_three":
                str(data["norm_t_squared_over_three"]),
            "faithful_basis_reason":
                "T and T/3 have negative K/Q norm, so T is not a square in K(sqrt3)",
        },
        "source_alignment": {
            "points": 241,
            "complete_unit_edges": len(data["source_edges"]),
            "all_pairs": 241 * 240 // 2,
            "point_sha256": data["source_point_sha256"],
            "edge_sha256": data["source_edge_sha256"],
            "prior_independent_review_aligned": True,
        },
        "construction": {
            "source_copies": 2,
            "points": len(data["points"]),
            "all_pairs": 481 * 480 // 2,
            "complete_unit_edges": len(data["edges"]),
            "inherited_edges": 1982,
            "private_cross_edges": len(data["cross_edges"]),
            "shared_points": 1,
            "point_sha256": data["point_sha256"],
            "edge_sha256": data["edge_sha256"],
            "independent_flat_basis_point_sha256": data["native_point_sha256"],
            **data["structure"],
        },
        "chromatic_certificate": {
            "chromatic_number": 4,
            "golomb_edges": len(data["golomb_edges"]),
            "normalized_three_colour_assignments_exhausted": data["three_assignments"],
            "submitted_four_word_checked": True,
            "submitted_four_word_sha256": submitted_hash,
            "fresh_four_word_sha256": fresh_hash,
            "fresh_word_differs_at_vertices": distance,
            "fresh_dsat_triangle": list(data["fresh_triangle"]),
            "fresh_dsat_nodes": data["fresh_nodes"],
            "fresh_dsat_backtracks": data["fresh_backtracks"],
        },
        "structural_strengthening": {
            "cross_contact_graph": data["cross_structure"],
            "interpretation": "linear forest: six K2 components and seven P3 components",
        },
        "record_candidate": False,
        "scope": "one frozen shared-origin rotation of two 241-point opposed cores",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        need(result == expected, "EXPECTED.json mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
