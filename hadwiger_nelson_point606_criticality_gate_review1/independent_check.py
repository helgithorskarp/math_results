#!/usr/bin/env python3
"""Independent exact audit of the point606 530-vertex critical core.

This checker imports no Python module from the reviewed contribution.  It
reconstructs the complete unit-distance graph over Q(sqrt(3),sqrt(5),sqrt(11)),
checks the five-colouring and every vertex-deletion four-colouring directly,
and emits a different four-colour CNF: exactly one colour per vertex and no
symmetry-breaking clauses.
"""

import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import lcm
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
TARGET = REPOSITORY / "hadwiger_nelson_point606_criticality_gate"
PRIMES = (3, 5, 11)
TARGET_HASHES = {
    "README.md": "c086afcfb754f414ef12af103c32157d5e635c8ac1cf6027c5b5a9e2405c5321",
    "certificate.json": "be652a44cb9e070c77a6404ee7cfc45a6956e94f600a0b486ec1d21ed6bfdb20",
    "manifest.json": "3dcf587ec8223671012e2bf6571c5db70f83c5d56a6bebaefac7dff2efb43004",
    "run_native.py": "67bcfd9b3bc5dd96c2a733a0015b0f0b5c1a32b2ae2bea4c199c2149e56f5eb9",
    "validation.json": "73e15fac3767bc83f40ed2ce9089e01c89dc28eefc6cd76ce130d1e6eab09ff6",
    "verify.py": "6cba8df63b34c7feea5d3b22fe301cde91b9e3fb62c43490b85763f09c3936a2",
}
INPUT_HASHES = {
    "hadwiger_nelson_parts509_completion_census_degree9/points.tsv":
        "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50",
    "hadwiger_nelson_parts509_swap_closure/completion_points.json":
        "b82909c48ce088deb89b555f4c8fa554bba44030570fdaaf0b9b607e9552a5a6",
    "hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json":
        "41a47be8d0568be7e1497f16a45c17d433e31e01fb62877856189fbf1ad53729",
    "hadwiger_nelson_parts509_degree6_lift_family/catalogue.json":
        "0282698f8bfb3b7df241c3d60af0dfef82f6f0535f114af71bf0db11807d0a4f",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    answer = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            answer.update(block)
    return answer.hexdigest()


def multiply(left, right):
    """Multiply coefficient vectors in the square-free bit-mask basis."""
    answer = [0] * 8
    for first, a in enumerate(left):
        for second, b in enumerate(right):
            coefficient = a * b
            for bit, prime in enumerate(PRIMES):
                if (first & second) & (1 << bit):
                    coefficient *= prime
            answer[first ^ second] += coefficient
    return tuple(answer)


def squared_distance(first, second):
    dx = tuple(a - b for a, b in zip(first[0], second[0], strict=True))
    dy = tuple(a - b for a, b in zip(first[1], second[1], strict=True))
    return tuple(a + b for a, b in zip(multiply(dx, dx), multiply(dy, dy), strict=True))


def read_geometry():
    for name, expected in INPUT_HASHES.items():
        require(digest(REPOSITORY / name) == expected, ("input hash", name))
    for name, expected in TARGET_HASHES.items():
        require(digest(TARGET / name) == expected, ("target hash", name))

    original_path = (REPOSITORY /
                     "hadwiger_nelson_parts509_completion_census_degree9/points.tsv")
    originals = []
    for line in original_path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        require(len(row) == 16, ("original width", len(originals)))
        originals.append((row[:8], row[8:]))
    require(len(originals) == 509, ("original count", len(originals)))

    completion_path = (REPOSITORY /
                       "hadwiger_nelson_parts509_swap_closure/completion_points.json")
    raw_completion = json.loads(completion_path.read_text())
    completion = []
    denominator = 96
    for record in raw_completion["points"]:
        point = (tuple(Fraction(value) for value in record["x"]),
                 tuple(Fraction(value) for value in record["y"]))
        require(len(point[0]) == len(point[1]) == 8, "completion width")
        for coefficient in point[0] + point[1]:
            denominator = lcm(denominator, coefficient.denominator)
        completion.append(point)
    require(len(completion) == 1158, ("completion count", len(completion)))
    require(denominator == 288, ("common denominator", denominator))

    points = [
        (tuple((denominator // 96) * x for x in point[0]),
         tuple((denominator // 96) * y for y in point[1]))
        for point in originals
    ]
    points.extend(
        (tuple(int(denominator * x) for x in point[0]),
         tuple(int(denominator * y) for y in point[1]))
        for point in completion
    )

    expected_q = ((-48, 0, 0, 0, 0, -48, 0, 0),
                  (0, 48, 0, 0, 48, 0, 0, 0))
    require(points[606] == expected_q, "q606 coordinate formula")
    host = tuple(range(585)) + (606,)
    require(len(set(host)) == len(host), "host label collision")
    require(len({points[v] for v in host}) == len(host), "host coordinate collision")
    target_distance = (denominator * denominator,) + (0,) * 7
    edges = tuple(
        (first, second)
        for first, second in combinations(host, 2)
        if squared_distance(points[first], points[second]) == target_distance
    )
    require(len(edges) == 3090, ("host edge count", len(edges)))
    require(sum(second < 509 for first, second in edges) == 2442,
            "Parts induced edge count")
    q_neighbors = tuple(first if second == 606 else second
                        for first, second in edges if 606 in (first, second))
    require(q_neighbors == (37, 51, 69, 142, 180, 198, 530),
            ("q606 neighbours", q_neighbors))
    return denominator, points, host, edges


def proper(labels, edges, word, palette):
    require(len(word) == len(labels), ("colouring length", len(labels), len(word)))
    require(set(word) <= set(palette), ("colouring palette", sorted(set(word))))
    colours = dict(zip(labels, word, strict=True))
    checks = 0
    for first, second in edges:
        if first in colours and second in colours:
            checks += 1
            require(colours[first] != colours[second],
                    ("monochromatic edge", first, second))
    return colours, checks


def read_library():
    old_path = (REPOSITORY /
                "hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json")
    catalogue_path = (REPOSITORY /
                      "hadwiger_nelson_parts509_degree6_lift_family/catalogue.json")
    old = json.loads(old_path.read_text())
    require(old["vertices"] == list(range(585)), "old ambient labels")
    require(old["pool"] == list(range(509, 585)), "old pool labels")
    require(len(old["forced"]) == 451, ("forced count", len(old["forced"])))
    library = {}
    for vertex in old["forced"]:
        witness = old["forced_witness"][str(vertex)]
        require(len(witness) == 584 and set(witness) <= set("0123"),
                ("base witness", vertex))
        library[vertex] = [witness]
    for record in json.loads(catalogue_path.read_text()):
        if record["kind"] != "forced":
            continue
        vertex = record["key"]
        require(vertex in library, ("catalogue key", vertex))
        require(record["index"] == len(library[vertex]),
                ("catalogue index", vertex, record["index"]))
        witness = record["witness"]
        require(len(witness) == 584 and set(witness) <= set("0123"),
                ("catalogue witness", vertex, record["index"]))
        library[vertex].append(witness)
    return old, library


def check_certificate(points, host, host_edges):
    certificate = json.loads((TARGET / "certificate.json").read_text())
    require(set(certificate) == {"deleted_labels", "original_deletion_references",
                                 "new_deletion_words", "five_colouring"},
            "certificate fields")
    deleted = certificate["deleted_labels"]
    require(deleted == sorted(set(deleted)), "canonical deletion labels")
    require(len(deleted) == 56 and 122 in deleted and set(deleted) < set(host),
            ("deletion set", len(deleted)))
    keep = tuple(vertex for vertex in host if vertex not in set(deleted))
    selected = set(keep)
    edges = tuple(edge for edge in host_edges if set(edge) <= selected)
    require(len(keep) == 530 and len(edges) == 2648,
            ("core dimensions", len(keep), len(edges)))
    point_hash = sha256(json.dumps([points[v] for v in keep],
                                   separators=(",", ":")).encode()).hexdigest()
    edge_hash = sha256("".join(f"{a},{b}\n" for a, b in edges).encode("ascii")).hexdigest()
    require(point_hash == "6acc2b7e08a3d623da9524bebd36f61edef5678543f119bf722b2cdc4dc02cbb",
            ("core point hash", point_hash))
    require(edge_hash == "bd9e7354233ea4d83fe36beea419de7e3006323367a4d1be3f12fd45f4b64514",
            ("core edge hash", edge_hash))

    _, five_checks = proper(keep, edges, certificate["five_colouring"], "01234")
    require(five_checks == len(edges), "five-colouring edge coverage")
    old, library = read_library()
    deletion_words = {}
    deletion_edge_checks = 0
    for row in certificate["original_deletion_references"]:
        require(type(row) is list and len(row) == 3, "reference width")
        vertex, index, appended = row
        require(vertex in selected and vertex not in deletion_words,
                ("reference vertex", vertex))
        if vertex == 606:
            require(index == "original122" and appended is None,
                    "q606 deletion reference")
            ambient = tuple(v for v in old["vertices"] if v != 122)
            source = library[122][0]
            colour_map = dict(zip(ambient, source, strict=True))
        else:
            require(type(index) is int and 0 <= index < len(library[vertex]),
                    ("library index", vertex, index))
            require(appended in "0123", ("q colour", vertex, appended))
            ambient = tuple(v for v in old["vertices"] if v != vertex)
            colour_map = dict(zip(ambient, library[vertex][index], strict=True))
            colour_map[606] = appended
        labels = tuple(v for v in keep if v != vertex)
        word = "".join(colour_map[v] for v in labels)
        _, checks = proper(labels, edges, word, "0123")
        deletion_words[vertex] = word
        deletion_edge_checks += checks

    require(type(certificate["new_deletion_words"]) is dict, "literal word map")
    for key, word in certificate["new_deletion_words"].items():
        vertex = int(key)
        require(str(vertex) == key and vertex in selected and vertex not in deletion_words,
                ("literal vertex", key))
        labels = tuple(v for v in keep if v != vertex)
        _, checks = proper(labels, edges, word, "0123")
        deletion_words[vertex] = word
        deletion_edge_checks += checks
    require(set(deletion_words) == selected,
            ("deletion witness coverage", len(deletion_words), len(selected)))
    require(len(certificate["original_deletion_references"]) == 451,
            "reference witness count")
    require(len(certificate["new_deletion_words"]) == 79,
            "literal witness count")
    require(deletion_edge_checks == 1_398_144,
            ("deletion edge checks", deletion_edge_checks))

    # Four independent rejection controls for the direct witness checker.
    rejections = 0
    first, second = edges[0]
    bad_five = list(certificate["five_colouring"])
    bad_five[keep.index(second)] = bad_five[keep.index(first)]
    controls = [
        (keep, "".join(bad_five), "01234"),
        (keep, certificate["five_colouring"][:-1], "01234"),
        (keep, "x" + certificate["five_colouring"][1:], "01234"),
    ]
    control_vertex = keep[0]
    labels = tuple(v for v in keep if v != control_vertex)
    control_edge = next(edge for edge in edges if control_vertex not in edge)
    bad_delete = list(deletion_words[control_vertex])
    bad_delete[labels.index(control_edge[1])] = bad_delete[labels.index(control_edge[0])]
    controls.append((labels, "".join(bad_delete), "0123"))
    for labels, word, palette in controls:
        try:
            proper(labels, edges, word, palette)
        except RuntimeError:
            rejections += 1
        else:
            raise RuntimeError("corrupted colouring accepted")
    require(rejections == 4, "colouring rejection controls")
    return keep, edges, deletion_edge_checks, rejections


def exact_one_cnf(vertices, edges):
    position = {vertex: index for index, vertex in enumerate(vertices)}
    clauses = []
    for vertex in vertices:
        variables = tuple(4 * position[vertex] + colour + 1 for colour in range(4))
        clauses.append(variables)
        clauses.extend((-first, -second) for first, second in combinations(variables, 2))
    for first, second in edges:
        for colour in range(4):
            clauses.append((-(4 * position[first] + colour + 1),
                            -(4 * position[second] + colour + 1)))
    return 4 * len(vertices), tuple(clauses)


def formula_true(clauses, assignment):
    return all(any(assignment[abs(literal)] == (literal > 0) for literal in clause)
               for clause in clauses)


def small_encoding_controls():
    checks = 0
    for order in range(4):
        possible_edges = tuple(combinations(range(order), 2))
        for graph_mask in range(1 << len(possible_edges)):
            edges = tuple(edge for index, edge in enumerate(possible_edges)
                          if graph_mask & (1 << index))
            variables, clauses = exact_one_cnf(tuple(range(order)), edges)
            for assignment_mask in range(1 << variables):
                assignment = {variable: bool(assignment_mask & (1 << (variable - 1)))
                              for variable in range(1, variables + 1)}
                one_hot = all(sum(assignment[4 * vertex + colour + 1]
                                  for colour in range(4)) == 1
                              for vertex in range(order))
                separated = all(not any(assignment[4 * first + colour + 1] and
                                        assignment[4 * second + colour + 1]
                                        for colour in range(4))
                                for first, second in edges)
                require(formula_true(clauses, assignment) == (one_hot and separated),
                        ("small CNF control", order, graph_mask, assignment_mask))
                checks += 1
    require(checks == 33_297, ("small CNF checks", checks))
    return checks


def dimacs(variables, clauses):
    return (f"p cnf {variables} {len(clauses)}\n" +
            "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)).encode("ascii")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf-out", type=Path, required=True)
    parser.add_argument("--result-out", type=Path)
    args = parser.parse_args()

    controls = small_encoding_controls()
    denominator, points, host, host_edges = read_geometry()
    keep, edges, deletion_checks, rejections = check_certificate(points, host, host_edges)
    variables, clauses = exact_one_cnf(keep, edges)
    encoded = dimacs(variables, clauses)
    args.cnf_out.parent.mkdir(parents=True, exist_ok=True)
    args.cnf_out.write_bytes(encoded)
    result = {
        "status": "POSITIVE CERTIFICATES AND EXACT GEOMETRY VERIFIED; ALTERNATIVE CNF EMITTED",
        "host_points": len(host),
        "host_unit_edges": len(host_edges),
        "host_pair_distances": len(host) * (len(host) - 1) // 2,
        "core_points": len(keep),
        "core_unit_edges": len(edges),
        "denominator": denominator,
        "five_colouring_edge_checks": len(edges),
        "vertex_deletion_words": len(keep),
        "vertex_deletion_edge_checks": deletion_checks,
        "colouring_corruptions_rejected": rejections,
        "small_cnf_assignment_checks": controls,
        "alternative_cnf_variables": variables,
        "alternative_cnf_clauses": len(clauses),
        "alternative_cnf_sha256": sha256(encoded).hexdigest(),
        "alternative_encoding": "exactly-one pairwise, no symmetry breaking",
    }
    if args.result_out:
        args.result_out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
