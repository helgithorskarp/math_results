#!/usr/bin/env python3
"""Independent exact audit for the dominating-unit-triangle theorem.

The universal continuum step is geometric and is documented in README.md.
This checker independently reconstructs the exceptional component, tests the
generic incidence template at several exact directions, exhausts the finite
colouring classifications, and audits the submitted compact certificate.  It
imports no executable from the reviewed package.
"""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations, product
import json
import os
from pathlib import Path
import sys


TARGET_COMMIT = "0c9e4cf4fd74b5bae3821c957e3b23186386e81d"
TARGET_HASHES = {
    ".gitignore": "862263fa1f46c20f0d1e4dac5ffcc75abd55c08211b2c3864c5f8764b9d87793",
    "README.md": "e02710308986ca6ffe58acc4b520e36527b9a71cf0847f8b9a40366a4ac7de8f",
    "build.py": "4e3334be1dcd18bb4ccae5bc09d2e5239d11fa4f2fdfabc3800e887f0b41ba85",
    "certificate.json": "f3e065d5907a96a41b9d0fe9ae4dfe5fc7ee141ac69030ea497082f1eb199e4c",
    "expected.json": "0d31e52c9457894a942e0c1a248e88535cc1053676cab7174f924f8cac946bc9",
    "validation.json": "9613234c1d7f13ccfa59b2004cdd2c1a48964673dfe48c5ae7a1db400c6d09fb",
    "verify.py": "a929bac6e7498aae5874ceeacac985053013521841def53d8eb0fb73cb5eee74",
}
TARGET_MANIFEST_HASH = "f13f11a465e1b8457e4ba70496969c1dd7e0f188f1b3733b9d081b5f3e691c3f"
CERTIFICATE_HASH = TARGET_HASHES["certificate.json"]
PATCH_EDGE_HASH = "bc4751ffd1cb921cee7b0804937907431e9fe9684b14c3e680116ab58d6a6ce3"
REPRESENTATIVE_EDGE_HASH = "755bd5a8a4dba576f173a972fc8da3505effd87a41c1d37a71c89ce4ab3cac22"


class ReviewFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewFailure(message)


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


# A quadratic number is a+b*sqrt(3).  A point is a pair of quadratic
# numbers.  This representation is deliberately separate from both submitted
# sparse-radicand arithmetic and its four-coefficient producer.
Quad = tuple[F, F]
Point = tuple[Quad, Quad]
ZERO: Quad = (F(0), F(0))
ONE: Quad = (F(1), F(0))


def qadd(left: Quad, right: Quad) -> Quad:
    return left[0] + right[0], left[1] + right[1]


def qneg(value: Quad) -> Quad:
    return -value[0], -value[1]


def qsub(left: Quad, right: Quad) -> Quad:
    return qadd(left, qneg(right))


def qmul(left: Quad, right: Quad) -> Quad:
    return left[0] * right[0] + 3 * left[1] * right[1], \
           left[0] * right[1] + left[1] * right[0]


def padd(left: Point, right: Point) -> Point:
    return qadd(left[0], right[0]), qadd(left[1], right[1])


def psub(left: Point, right: Point) -> Point:
    return qsub(left[0], right[0]), qsub(left[1], right[1])


def cmul(left: Point, right: Point) -> Point:
    return qsub(qmul(left[0], right[0]), qmul(left[1], right[1])), \
           qadd(qmul(left[0], right[1]), qmul(left[1], right[0]))


def squared(left: Point, right: Point) -> Quad:
    delta = psub(left, right)
    return qadd(qmul(delta[0], delta[0]), qmul(delta[1], delta[1]))


def lattice_point(label: tuple[int, int]) -> Point:
    a, b = label
    return ((F(a) + F(b, 2), F(0)), (F(0), F(b, 2)))


ROOT_LABELS = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
CENTRE_LABELS = [(0, 0), (1, 0), (0, 1)]
ROOTS = [lattice_point(label) for label in ROOT_LABELS]
CENTRES = [lattice_point(label) for label in CENTRE_LABELS]


def exact_edges(points: list[Point]) -> list[tuple[int, int]]:
    return [(left, right) for left, right in combinations(range(len(points)), 2)
            if squared(points[left], points[right]) == ONE]


def reconstruct_patch() -> tuple[list[tuple[int, int]], list[Point]]:
    labels = sorted({(a + u, b + v)
                     for a, b in CENTRE_LABELS for u, v in ROOT_LABELS})
    points = [lattice_point(label) for label in labels]
    require(len(labels) == len(set(points)) == 12, "twelve-point exceptional patch")
    require([points.index(centre) for centre in CENTRES] == [4, 8, 5],
            "canonical centre indices")
    return labels, points


def pythagorean_seed(parameter: F) -> Point:
    denominator = 1 + parameter * parameter
    return ((1 - parameter * parameter) / denominator, F(0)), \
           (2 * parameter / denominator, F(0))


def generic_points(seed: Point) -> list[Point]:
    directions = [cmul(seed, root) for root in ROOTS]
    require(all(squared(direction, ((ZERO), (ZERO))) == ONE for direction in directions),
            "six exact unit directions")
    return [padd(centre, direction) for centre in CENTRES for direction in directions]


def predicted_generic_edges(offset: int = 0, cycle_length: int = 6) -> set[tuple[int, int]]:
    edges = set()
    for owner in range(3):
        for position in range(cycle_length):
            left = offset + cycle_length * owner + position
            right = offset + cycle_length * owner + (position + 1) % cycle_length
            edges.add(tuple(sorted((left, right))))
    for position in range(cycle_length):
        for left_owner, right_owner in combinations(range(3), 2):
            edges.add((offset + cycle_length * left_owner + position,
                       offset + cycle_length * right_owner + position))
    return edges


def graph_for_seed(seed: Point, patch_points: list[Point]) -> dict[str, object]:
    generic = generic_points(seed)
    points = patch_points + generic
    require(len(set(points)) == 30, "generic points distinct from each other and patch")
    edges = exact_edges(points)
    patch_edges = {(a, b) for a, b in edges if b < 12}
    generic_edges = {(a, b) for a, b in edges if a >= 12}
    cross_edges = set(edges) - patch_edges - generic_edges
    centre_indices = [patch_points.index(centre) for centre in CENTRES]
    spokes = {(centre_indices[owner], 12 + 6 * owner + position)
              for owner in range(3) for position in range(6)}
    require(len(patch_edges) == 24, "exceptional patch has 24 edges")
    require(generic_edges == predicted_generic_edges(12), "generic K3 Cartesian C6")
    require(cross_edges == spokes, "only owner-centre patch/generic spokes")
    require(len(edges) == 78, "complete representative edge count")
    edge_stream = "".join(f"{a},{b}\n" for a, b in edges).encode("ascii")
    return {"points": points, "edges": edges, "edge_sha256": sha256(edge_stream).hexdigest()}


def proper(row, edges) -> bool:
    return all(row[left] != row[right] for left, right in edges)


def patch_colourings(labels, patch_points) -> tuple[list[int], list[list[int]], int]:
    edges = exact_edges(patch_points)
    centres = [patch_points.index(centre) for centre in CENTRES]
    outside = [vertex for vertex in range(12) if vertex not in centres]
    solutions = []
    examined = 0
    for word in product(range(3), repeat=len(outside)):
        row = [-1] * 12
        for colour, vertex in enumerate(centres):
            row[vertex] = colour
        for vertex, colour in zip(outside, word):
            row[vertex] = colour
        examined += 1
        if proper(row, edges):
            solutions.append(row)
    lattice_row = [(a + 2 * b) % 3 for a, b in labels]
    require(examined == 3 ** 9 and solutions == [lattice_row],
            "unique pinned exceptional colouring")
    rim = set(outside)
    rim_edges = [(a, b) for a, b in edges if a in rim and b in rim]
    require(len(rim_edges) == 9 and all(sum(vertex in edge for edge in rim_edges) == 2
                                        for vertex in rim), "residual C9 degrees")
    reached = {min(rim)}
    while True:
        expanded = reached | {vertex for edge in rim_edges if reached.intersection(edge)
                              for vertex in edge}
        if expanded == reached:
            break
        reached = expanded
    require(reached == rim, "residual C9 connectivity")
    return lattice_row, solutions, examined


def generic_colourings(cycle_length: int = 6) -> tuple[list[list[int]], int]:
    edges = predicted_generic_edges(0, cycle_length)
    domains = [[colour for colour in range(3) if colour != owner]
               for owner in range(3) for _ in range(cycle_length)]
    solutions = []
    examined = 0
    for word in product(*domains):
        examined += 1
        if proper(word, edges):
            solutions.append(list(word))
    return solutions, examined


def formula_generic(sign: int) -> list[int]:
    return [(owner + sign * (-1) ** position) % 3
            for owner in range(3) for position in range(6)]


def encode_scale10(point: Point) -> list[int]:
    values = [point[0][0], point[0][1], point[1][0], point[1][1]]
    require(all((10 * value).denominator == 1 for value in values),
            "scale-ten certificate transcription")
    return [int(10 * value) for value in values]


def compare_certificate(data, labels, target_graph, patch_row, generic_solutions) -> None:
    require(data.get("coordinate_scale") == 10, "certificate scale")
    require(data.get("coordinate_map")
            == "(a,b,c,d)/10 -> ((a+b*sqrt3)/10,(c+d*sqrt3)/10)",
            "certificate coordinate map")
    require(data.get("patch_lattice") == [list(label) for label in labels],
            "certificate patch labels")
    require(data.get("vertices") == [encode_scale10(point) for point in target_graph["points"]],
            "certificate points")
    require(data.get("centres") == [4, 8, 5], "certificate centres")
    require(data.get("generic_labels") == [[owner, position]
                                             for owner in range(3) for position in range(6)],
            "certificate generic labels")
    require(data.get("edges") == [list(edge) for edge in target_graph["edges"]],
            "certificate edge list")
    roots_squared = [squared(ROOTS[0], root) for root in ROOTS]
    require(all(value[1] == 0 and value[0].denominator == 1 for value in roots_squared),
            "integral root chord squares")
    require(data.get("rotation_chord_squared") == [int(value[0]) for value in roots_squared]
            == [0, 1, 3, 4, 3, 1], "certificate root chords")
    derangements = [list(word) for word in permutations(range(3))
                    if all(word[index] != index for index in range(3))]
    require(data.get("generic_column_derangements") == derangements
            == [[1, 2, 0], [2, 0, 1]], "certificate column derangements")
    expected_rows = [patch_row + formula_generic(sign) for sign in (1, -1)]
    require(sorted(generic_solutions) == sorted([formula_generic(1), formula_generic(-1)]),
            "generic solutions equal formulas")
    require(data.get("pinned_colourings") == expected_rows,
            "certificate pinned colourings")


def verify_target_files(target: Path) -> dict[str, dict[str, int | str]]:
    records = {}
    for name, expected in TARGET_HASHES.items():
        raw = (target / name).read_bytes()
        actual = sha256(raw).hexdigest()
        require(actual == expected, "reviewed target source identity: " + name)
        records[name] = {"bytes": len(raw), "sha256": actual}
    manifest_raw = (target / "SHA256SUMS").read_bytes()
    require(sha256(manifest_raw).hexdigest() == TARGET_MANIFEST_HASH,
            "reviewed target manifest identity")
    records["SHA256SUMS"] = {"bytes": len(manifest_raw), "sha256": TARGET_MANIFEST_HASH}
    manifest = {}
    for line in manifest_raw.decode("ascii").splitlines():
        digest, name = line.split(maxsplit=1)
        manifest[name] = digest
    require(manifest == TARGET_HASHES, "published SHA256SUMS matches pinned target")
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--target", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    repository = args.repository.resolve()
    target = (args.target or repository / "hadwiger_nelson_dominating_triangle").resolve()

    target_files = verify_target_files(target)
    raw_certificate = (target / "certificate.json").read_bytes()
    require(sha256(raw_certificate).hexdigest() == CERTIFICATE_HASH,
            "published certificate identity")
    certificate = json.loads(raw_certificate)

    labels, patch = reconstruct_patch()
    patch_row, patch_solutions, patch_examined = patch_colourings(labels, patch)
    generic_solutions, generic_examined = generic_colourings(6)
    require(generic_examined == 2 ** 18 and len(generic_solutions) == 2,
            "complete pinned generic colouring census")

    # Three rational unit directions strictly inside the fundamental
    # 60-degree sector.  The last one is the contributor's certificate
    # direction; the other two are reviewer-selected exact controls.
    parameters = [F(1, 7), F(1, 3), F(1, 2)]
    seed_records = []
    graphs = []
    for parameter in parameters:
        seed = pythagorean_seed(parameter)
        require(squared(seed, ((ZERO), (ZERO))) == ONE, "Pythagorean unit seed")
        require(seed not in ROOTS, "nonexceptional seed")
        graph = graph_for_seed(seed, patch)
        graphs.append(graph)
        require(graph["edge_sha256"] == REPRESENTATIVE_EDGE_HASH,
                "canonical representative edge stream")
        seed_records.append({
            "half_angle_parameter": f"{parameter.numerator}/{parameter.denominator}",
            "unit_direction": [str(seed[0][0]), str(seed[1][0])],
            "vertices": len(graph["points"]),
            "edges": len(graph["edges"]),
            "edge_sha256": graph["edge_sha256"],
        })
    # parameter 1/2 gives direction (3/5,4/5), the published representative.
    compare_certificate(certificate, labels, graphs[2], patch_row, generic_solutions)

    # Directly check that all six pinned centre prescriptions extend on the
    # representative graph by permuting the independently found base rows.
    complete_rows = [patch_row + row for row in generic_solutions]
    centre_indices = [4, 8, 5]
    centre_words = set()
    edge_checks = 0
    for colour_permutation in permutations(range(3)):
        for row in complete_rows:
            permuted = [colour_permutation[colour] for colour in row]
            require(proper(permuted, graphs[2]["edges"]), "permuted positive row")
            edge_checks += len(graphs[2]["edges"])
            centre_words.add(tuple(permuted[index] for index in centre_indices))
    require(len(centre_words) == 6 and edge_checks == 936,
            "all proper centre prescriptions")

    # Column-state parity controls isolate why C6 works and an odd cycle does
    # not.  These are exact definition-level enumerations.
    cycle4_solutions, cycle4_examined = generic_colourings(4)
    cycle5_solutions, cycle5_examined = generic_colourings(5)
    require((cycle4_examined, len(cycle4_solutions)) == (2 ** 12, 2),
            "even column-cycle control")
    require((cycle5_examined, len(cycle5_solutions)) == (2 ** 15, 0),
            "odd column-cycle control")

    # The certificate comparison is total over every field.  Mutations in
    # independent data classes must be rejected without rerunning discovery.
    mutants = []
    bad = copy.deepcopy(certificate); bad["vertices"][12][0] += 1; mutants.append(bad)
    bad = copy.deepcopy(certificate); bad["edges"].pop(); mutants.append(bad)
    bad = copy.deepcopy(certificate); bad["pinned_colourings"][0][12] = 0; mutants.append(bad)
    bad = copy.deepcopy(certificate); bad["patch_lattice"][0][0] -= 1; mutants.append(bad)
    bad = copy.deepcopy(certificate); bad["rotation_chord_squared"][1] = 3; mutants.append(bad)
    rejected = 0
    for mutant in mutants:
        try:
            compare_certificate(mutant, labels, graphs[2], patch_row, generic_solutions)
        except ReviewFailure:
            rejected += 1
        else:
            raise ReviewFailure("malformed certificate accepted")
    require(rejected == 5, "all malformed controls rejected")

    patch_edge_stream = "".join(f"{a},{b}\n" for a, b in exact_edges(patch)).encode("ascii")
    require(sha256(patch_edge_stream).hexdigest() == PATCH_EDGE_HASH,
            "canonical exceptional edge stream")
    result = {
        "all_checks_passed": True,
        "reviewed_source_commit": TARGET_COMMIT,
        "reviewed_source": target_files,
        "scope": "full strict unit graph on three unit circles centred at a unit equilateral triangle; dominating-clique corollary",
        "exceptional_patch": {
            "vertices": 12,
            "edges": 24,
            "residual_component": "C9",
            "pair_distances_checked": 66,
            "pinned_assignments_examined": patch_examined,
            "pinned_colourings": len(patch_solutions),
            "edge_sha256": sha256(patch_edge_stream).hexdigest(),
        },
        "generic_template": {
            "vertices": 18,
            "internal_edges": 36,
            "centre_spokes": 18,
            "structure_after_deleting_centres": "K3 Cartesian C6",
            "pair_distances_checked_per_exact_control": 435,
            "pair_distances_checked_total": 1305,
            "pinned_assignments_examined": generic_examined,
            "pinned_colourings": len(generic_solutions),
            "reviewer_exact_direction_controls": seed_records,
        },
        "definition_level_controls": {
            "C4_assignments_examined": cycle4_examined,
            "C4_colourings": len(cycle4_solutions),
            "C5_assignments_examined": cycle5_examined,
            "C5_colourings": len(cycle5_solutions),
            "malformed_certificates_rejected": rejected,
        },
        "colouring": {
            "proper_centre_prescriptions": len(centre_words),
            "permuted_representative_edge_checks": edge_checks,
            "exceptional_extension_unique": True,
            "generic_extension_choices_per_orbit": 2,
        },
        "logical_audit": {
            "continuum_coverage_from_finite_sampling": False,
            "continuum_coverage_from_unit_rhombus_and_rotation_orbit_proof": True,
            "same_circle_unit_chords_are_sixth_rotation_neighbours": True,
            "noncentre_cross_circle_edges_preserve_unit_direction": True,
            "multiple_circle_membership_is_exceptional": True,
            "dominating_clique_sizes_reduced": [1, 2, 3],
            "record_improvement": False,
        },
        "trust_boundary": [
            "elementary Euclidean two-circle intersection and unit-chord arguments used for the continuum reduction",
            "the standard irrationality of sqrt(3) in the exact quadratic representation",
            "ordinary CPython Fraction/integer arithmetic, JSON decoding, and exhaustive-loop execution",
            "SHA-256 collision resistance for the reviewed source identity",
        ],
        "python": sys.version.split()[0],
    }
    atomic_json(args.report.resolve(), result)
    print(json.dumps({
        "all_checks_passed": True,
        "patch_colourings": len(patch_solutions),
        "generic_colourings": len(generic_solutions),
        "exact_generic_directions": len(seed_records),
        "dominating_clique_bound": 3,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
