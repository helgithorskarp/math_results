#!/usr/bin/env python3
"""Independent exact review of the fixed-H560 order-508 closure.

This checker imports no executable from the reviewed contribution.  It
reconstructs the 632-point host with recursive quadratic-tower arithmetic,
assembles and checks all 42 full-H560 positive colour witnesses, independently
enumerates the exact 508-vertex necessary family, and checks coverage entry by
entry.  It uses no SAT solver and trusts no negative search result.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys


REVIEWED_REF = "bafkreiapqqcgluwkxod6r667racxwqhrhqpy2bkoy46vlc75abt5esdezi"
REVIEWED_COMMIT = "d857e528601d5c9fba166290af5185cc2e5ef9f9"
TARGET = "hadwiger_nelson_heule560_target508"
TARGET_MANIFEST_SHA256 = "534edc9783415f22c8d91b56c14b345fabb47214cd48855c8b84f1e4e239bda5"
TARGET_HASHES = {
    ".gitignore": "862263fa1f46c20f0d1e4dac5ffcc75abd55c08211b2c3864c5f8764b9d87793",
    "README.md": "cda09c63360f9963b368bd91cf1c10a15bff726cadb894303453938c567da6ad",
    "build.py": "a5ccd26fa0df648efe743426f78c8bdb488a01fc1ec5c8aadc8a255c7a856367",
    "certificate.json": "687311aea18740f55257eaccd571d526fc20ee0c118cadf5a7b85cffcd423813",
    "expected.json": "8264904a882351daeb4ab595004d94910f077e55cd8707c5ea83989214908062",
    "plan.json": "24c6d3c3dee0cc9d22308e39872647a753789f29b7e6042b6e49864a69ff5dcf",
    "run_summary.json": "b4fc3cebb0fd2811a2a6197429aab56d31d7a9dc11ff760d0dc2901b1d2b4fae",
    "validation.json": "ca9c717aa5d7b14ecb482914fc32ca8d0405c9de7b4b3debc20a26fdd84cf850",
    "verify.py": "bdacc328f7b4716db57d18ec0f5f17f5126a3f9413523881daf0633c0d60394b",
}
OLD_INPUT = "hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json"
FRESH_INPUT = "hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json"
EXPECTED_HOST_EDGE_SHA256 = "8dd36c195b3e252ec2be150ea6a029375707293fec70b63da9fc157eed4140f0"
SCALE = 96
UNIT = (SCALE * SCALE,) + (0,) * 7


class ReviewFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewFailure(message)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def file_record(path: Path) -> dict[str, int | str]:
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": digest(raw)}


def source_identity(repository: Path) -> dict[str, object]:
    target = repository / TARGET
    manifest_raw = (target / "SHA256SUMS").read_bytes()
    require(digest(manifest_raw) == TARGET_MANIFEST_SHA256, "target manifest identity")
    manifest = {}
    for line in manifest_raw.decode("ascii").splitlines():
        value, name = line.split(maxsplit=1)
        manifest[name] = value
    require(manifest == TARGET_HASHES, "target manifest entries")
    target_records = {}
    for name, expected in TARGET_HASHES.items():
        record = file_record(target / name)
        require(record["sha256"] == expected, "target source identity: " + name)
        target_records[name] = record

    plan = read_json(target / "plan.json")
    input_records = {}
    for name, expected in plan["input_files"].items():
        record = file_record(repository / name)
        require(record["sha256"] == expected, "pinned input identity: " + name)
        input_records[name] = record
    return {
        "reviewed_artifact_ref": REVIEWED_REF,
        "reviewed_source_commit": REVIEWED_COMMIT,
        "target_files": target_records,
        "pinned_inputs": input_records,
    }


# An element of Q(sqrt(3))(sqrt(5))(sqrt(11)) is an eight-entry vector.  The
# outermost split is A+B sqrt(p).  This representation and recursive product
# differ from the target's sparse-radicand and XOR-convolution implementations.
def add(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a + b for a, b in zip(left, right))


def scale(value: tuple[int, ...], factor: int) -> tuple[int, ...]:
    return tuple(factor * entry for entry in value)


def tower_product(left: tuple[int, ...], right: tuple[int, ...],
                  primes: tuple[int, ...] = (11, 5, 3)) -> tuple[int, ...]:
    require(len(left) == len(right) == 2 ** len(primes), "tower element shape")
    if not primes:
        return (left[0] * right[0],)
    half = len(left) // 2
    a, b = left[:half], left[half:]
    c, d = right[:half], right[half:]
    rest = primes[1:]
    low = add(tower_product(a, c, rest),
              scale(tower_product(b, d, rest), primes[0]))
    high = add(tower_product(a, d, rest), tower_product(b, c, rest))
    return low + high


def scaled_axis(raw) -> tuple[int, ...]:
    values = [SCALE * Fraction(value) for value in raw]
    require(len(values) == 8 and all(value.denominator == 1 for value in values),
            "scaled coordinate coefficients")
    return tuple(int(value) for value in values)


def scaled_point(raw):
    require(isinstance(raw, list) and len(raw) == 2, "point shape")
    return scaled_axis(raw[0]), scaled_axis(raw[1])


def squared_distance(left, right) -> tuple[int, ...]:
    answer = (0,) * 8
    for axis in range(2):
        delta = tuple(a - b for a, b in zip(left[axis], right[axis]))
        answer = add(answer, tower_product(delta, delta))
    return answer


def reconstruct_geometry(repository: Path) -> dict[str, object]:
    old = read_json(repository / OLD_INPUT)
    old_labels = [index for index, provenance in enumerate(old["provenance"])
                  if "510" in provenance]
    require(old_labels == sorted(set(old_labels)) and len(old_labels) == 510,
            "canonical old labels")
    fresh = read_json(repository / FRESH_INPUT)
    fresh_ids = [row["centre_index"] for row in fresh]
    require(fresh_ids == sorted(set(fresh_ids)) and len(fresh_ids) == 122,
            "canonical fresh labels")
    points = [scaled_point(old["coordinates"][str(label)]) for label in old_labels]
    points.extend(scaled_point(row["coordinates"]) for row in fresh)
    require(len(points) == len(set(points)) == 632, "632 distinct exact points")
    edges = [(u, v) for u, v in combinations(range(632), 2)
             if squared_distance(points[u], points[v]) == UNIT]
    edge_raw = "".join(f"{u},{v}\n" for u, v in edges).encode("ascii")
    require(len(edges) == 3112 and digest(edge_raw) == EXPECTED_HOST_EDGE_SHA256,
            "complete exact H632 edge set")
    return {
        "points": points,
        "edges": edges,
        "exact_pairs_checked": 199396,
        "edge_sha256": digest(edge_raw),
    }


def check_full_colouring(word: str, active: set[int], edges: list[tuple[int, int]]) -> int:
    require(isinstance(word, str) and len(word) == 632, "colour word length")
    require(set(word) <= set(".0123"), "colour word alphabet")
    domain = {vertex for vertex, colour in enumerate(word) if colour != "."}
    require(domain == active, "colour word exact domain")
    checked = 0
    for left, right in edges:
        if left in active and right in active:
            require(word[left] != word[right], "monochromatic exact unit edge")
            checked += 1
    return checked


def assemble_right_word(right_word: str, active: set[int], right: list[int],
                        separator: list[int], left: list[int],
                        full_table: dict[str, str], absent310_table: dict[str, str],
                        edges: list[tuple[int, int]]) -> tuple[str, int]:
    require(len(right_word) == len(right) and set(right_word) <= set(".0123"),
            "right word shape")
    right_colours = {vertex: colour for vertex, colour in zip(right, right_word)
                     if colour != "."}
    require(set(right_colours) == active & set(right), "right word exact domain")
    state = "".join(right_colours[vertex] for vertex in separator)
    table = full_table if 310 in active else absent310_table
    require(state in table, "explicit matching left state")
    left_word = table[state]
    require(len(left_word) == len(left) and set(left_word) <= set(".0123"),
            "left word shape")
    colours = {vertex: colour for vertex, colour in zip(left, left_word)
               if vertex in active}
    require(all(colours[vertex] == right_colours[vertex] for vertex in separator),
            "left and right separator agreement")
    colours.update(right_colours)
    require(set(colours) == active, "assembled full support")
    word = "".join(colours.get(vertex, ".") for vertex in range(632))
    return word, check_full_colouring(word, active, edges)


def collect_colourings(repository: Path, edges: list[tuple[int, int]],
                        retained: set[int], m492: set[int]):
    global_certificate = read_json(
        repository / "hadwiger_nelson_heule560_global_decision/certificate.json")
    separator_certificate = read_json(
        repository / "hadwiger_nelson_heule560_separator/certificate.json")
    relation_certificate = read_json(
        repository / "hadwiger_nelson_heule560_left_relation/certificate.json")
    cylinder_certificate = read_json(
        repository / "hadwiger_nelson_heule560_cylinder508/certificate.json")

    right = global_certificate["right_vertices"]
    separator = separator_certificate["separator"]
    left = separator_certificate["blocks"]["full"]["vertices"]
    require(right == sorted(set(right)) and left == sorted(set(left)), "block label order")
    require(set(left) | set(right) == retained and set(left) & set(right) == set(separator),
            "left/right decomposition")
    full_table = {row["state"]: row["colouring"]
                  for row in separator_certificate["blocks"]["full"]["states"]}
    require(len(full_table) == 20, "twenty explicit full-left states")
    absent310_table = dict(full_table)
    for row in relation_certificate["rows"]:
        if row["inherited_full"]:
            continue
        matches = [cover["colouring"] for cover in row["positive_covers"]
                   if cover["mask"] == 510]
        require(len(matches) == 1, "unique 310-absent left witness")
        absent310_table[row["state"]] = matches[0]

    words = []
    edge_checks = 0
    optional_order = global_certificate["optional_order"]
    require(len(optional_order) == 60, "global optional mask width")
    for row in global_certificate["positive_covers"]:
        omitted = {vertex for index, vertex in enumerate(optional_order)
                   if not (row["mask"] >> index) & 1}
        active = retained - omitted
        word, checked = assemble_right_word(
            row["colouring"], active, right, separator, left,
            full_table, absent310_table, edges)
        words.append(word)
        edge_checks += checked
    require(len(words) == 35, "thirty-five global positive witnesses")

    erased = {510, 512, 513, 520, 521, 523, 524, 535}
    for row in cylinder_certificate["covers"]:
        partial = row["colouring"]
        require(len(partial) == 632 and set(partial) <= set(".0123"),
                "cylinder word shape")
        active = ({vertex for vertex, colour in enumerate(partial) if colour != "."}
                  | erased)
        require(active <= retained and not active & (set(range(632)) - retained),
                "lifted cylinder support")
        right_word = "".join(partial[vertex] for vertex in right)
        word, checked = assemble_right_word(
            right_word, active, right, separator, left,
            full_table, absent310_table, edges)
        words.append(word)
        edge_checks += checked
    require(len(words) == 40, "forty inherited full-H560 witnesses")

    omission_sets = [retained - {vertex for vertex, colour in enumerate(word)
                                 if colour != "."} for word in words]
    require(all(not omitted & m492 for omitted in omission_sets),
            "inherited omissions avoid M492")
    return words, omission_sets, edge_checks


def polynomial_product(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def necessary_family(optional: list[int], pairs: list[tuple[int, int]]):
    pair_vertices = set().union(*(set(pair) for pair in pairs))
    outside = sorted(set(optional) - pair_vertices)
    require(len(pairs) == 9 and len(pair_vertices) == 18 and len(outside) == 44,
            "nine disjoint pairs plus forty-four outside vertices")
    rows = []

    # Case A: one endpoint from every pair, plus one outside vertex.
    for choices in product((0, 1), repeat=len(pairs)):
        endpoints = [pairs[index][choice] for index, choice in enumerate(choices)]
        for extra in outside:
            rows.append(tuple(sorted(endpoints + [extra])))

    # Case B: both endpoints of one pair and one from every other pair.
    for doubled in range(len(pairs)):
        other_indices = [index for index in range(len(pairs)) if index != doubled]
        for choices in product((0, 1), repeat=len(other_indices)):
            selected = list(pairs[doubled])
            selected.extend(pairs[index][choice]
                            for index, choice in zip(other_indices, choices))
            rows.append(tuple(sorted(selected)))

    rows.sort()
    require(len(rows) == len(set(rows)) == 24832, "complete distinct necessary family")
    require(all(len(row) == 10 and set(row) <= set(optional)
                and all(set(row) & set(pair) for pair in pairs) for row in rows),
            "literal necessary-family members")

    # Independent coefficient count: [x^10] (2x+x^2)^9 (1+x)^44.
    polynomial = [1]
    for _ in pairs:
        polynomial = polynomial_product(polynomial, [0, 2, 1])
    for _ in outside:
        polynomial = polynomial_product(polynomial, [1, 1])
    require(polynomial[10] == len(rows), "generating-function family count")
    return rows, outside, polynomial[10]


def cover_family(rows: list[tuple[int, ...]], base: set[int], words: list[str]):
    active_sets = [{vertex for vertex, colour in enumerate(word) if colour != "."}
                   for word in words]
    counts = Counter()
    uncovered = []
    assignment = bytearray()
    residual_after_inherited = []
    for index, row in enumerate(rows):
        support = base | set(row)
        require(len(support) == 508, "exact target support order")
        first = next((cover for cover, active in enumerate(active_sets)
                      if support <= active), None)
        if first is None:
            uncovered.append(index)
            continue
        if first >= 40:
            residual_after_inherited.append(index)
        counts[first] += 1
        assignment.extend(first.to_bytes(2, "little"))
    return counts, uncovered, residual_after_inherited, bytes(assignment)


def small_controls() -> dict[str, int]:
    cases = 0
    members = 0
    for pair_count in range(5):
        pairs = [(2 * index, 2 * index + 1) for index in range(pair_count)]
        for outside_count in range(5):
            universe = list(range(2 * pair_count + outside_count))
            for size in range(len(universe) + 1):
                brute = [choice for choice in combinations(universe, size)
                         if all(set(choice) & set(pair) for pair in pairs)]
                polynomial = [1]
                for _ in pairs:
                    polynomial = polynomial_product(polynomial, [0, 2, 1])
                for _ in range(outside_count):
                    polynomial = polynomial_product(polynomial, [1, 1])
                coefficient = polynomial[size] if size < len(polynomial) else 0
                require(coefficient == len(brute), "small generating-function control")
                cases += 1
                members += len(brute)
    return {"small_family_cases": cases, "small_family_members": members}


def expect_failure(callback, message: str) -> None:
    try:
        callback()
    except ReviewFailure:
        return
    raise ReviewFailure(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    repository = args.repository.resolve()
    target = repository / TARGET
    identity = source_identity(repository)
    geometry = reconstruct_geometry(repository)
    seed = read_json(repository / "hadwiger_nelson_heule632_minimize/certificate.json")
    boundary = read_json(repository / "hadwiger_nelson_heule632_minimize/boundary.json")
    certificate = read_json(target / "certificate.json")
    run_summary = read_json(target / "run_summary.json")

    retained = set(seed["retained"])
    m492 = set(boundary["mandatory_vertices"])
    require(len(retained) == 560 and len(m492) == 492, "H560 and M492 orders")
    require(retained == m492 | set(boundary["optional_vertices"])
            and not m492 & set(boundary["optional_vertices"]), "M492/U68 partition")
    h560_edges = [(left, right) for left, right in geometry["edges"]
                  if left in retained and right in retained]
    require(len(h560_edges) == 2758, "exact H560 edge set")

    additions = certificate["mandatory_additions"]
    pairs = [tuple(pair) for pair in certificate["disjoint_pairs"]]
    require(additions == [310, 393, 454, 539, 578, 615], "six fixed additions")
    require(len(set(additions)) == 6 and not set(additions) & m492, "new mandatory labels")
    require(all(len(pair) == 2 for pair in pairs), "pair sizes")
    require(len(set().union(*(set(pair) for pair in pairs))) == 18, "pair disjointness")
    base = m492 | set(additions)
    optional = sorted(retained - base)
    require(len(base) == 498 and len(optional) == 62, "M498/optional62 partition")
    require(set().union(*(set(pair) for pair in pairs)) <= set(optional),
            "pairs outside M498")

    inherited, inherited_omissions, inherited_checks = collect_colourings(
        repository, geometry["edges"], retained, m492)
    necessary_omissions = [{vertex} for vertex in additions] + [set(pair) for pair in pairs]
    necessity_indices = []
    for omitted in necessary_omissions:
        require(omitted in inherited_omissions, "explicit complement colouring for necessity")
        necessity_indices.append(inherited_omissions.index(omitted))

    new_words = certificate["new_H560_colourings"]
    require(len(new_words) == 2 and len(set(new_words)) == 2, "two distinct new witnesses")
    new_active = []
    new_checks = 0
    for word in new_words:
        active = {vertex for vertex, colour in enumerate(word) if colour != "."}
        require(base <= active <= retained, "new witness contains M498 inside H560")
        new_checks += check_full_colouring(word, active, geometry["edges"])
        new_active.append(active)
    new_omissions = [sorted(retained - active) for active in new_active]
    require(new_omissions == [[500, 609], [440, 607, 612]], "new omission sets")

    rows, outside, coefficient = necessary_family(optional, pairs)
    family_raw = "".join(",".join(map(str, row)) + "\n" for row in rows).encode("ascii")
    counts, uncovered, residual, assignment = cover_family(
        rows, base, inherited + new_words)
    require(not uncovered, "every necessary exact-508 support is covered")
    require(len(residual) == 72 and counts[40] == 64 and counts[41] == 8,
            "two new witnesses close the inherited residual")
    require(digest(family_raw) == run_summary["family_sha256"], "canonical family identity")
    require(digest(assignment) == run_summary["coverage_sha256"],
            "entrywise first-cover identity")
    require({str(index): count for index, count in counts.items()}
            == run_summary["first_cover_counts"], "first-cover multiplicities")

    # Failure controls exercise the claims carried by the compact certificate.
    bad_word = list(new_words[0])
    edge = next((edge for edge in h560_edges if all(bad_word[v] != "." for v in edge)))
    bad_word[edge[1]] = bad_word[edge[0]]
    expect_failure(lambda: check_full_colouring("".join(bad_word), new_active[0],
                                                geometry["edges"]),
                   "monochromatic new witness accepted")
    shortened = new_words[0][:-1]
    expect_failure(lambda: check_full_colouring(shortened, new_active[0], geometry["edges"]),
                   "short new witness accepted")
    _, missing_without_second, _, _ = cover_family(rows, base, inherited + [new_words[0]])
    require(len(missing_without_second) == 8, "second new witness is necessary for eight rows")
    _, missing_without_new, _, _ = cover_family(rows, base, inherited)
    require(len(missing_without_new) == 72, "inherited residual is exactly 72 rows")
    controls = small_controls()

    report = {
        "all_checks_passed": True,
        "verdict": "accept",
        "accepted_scope": (
            "Every subgraph on at most 508 vertices of the fixed exact H560 support "
            "is four-colourable; this is not a sub-509 construction or a statement "
            "about other Euclidean supports."
        ),
        "source_identity": identity,
        "exact_geometry": {
            "host_vertices": 632,
            "distinct_points": 632,
            "exact_pairs_checked": geometry["exact_pairs_checked"],
            "host_edges": len(geometry["edges"]),
            "host_edge_sha256": geometry["edge_sha256"],
            "h560_vertices": len(retained),
            "h560_edges": len(h560_edges),
        },
        "imported_premise": {
            "statement": "The previously accepted M492 singleton-deletion theorem.",
            "mandatory_vertices": len(m492),
            "optional_vertices": len(boundary["optional_vertices"]),
        },
        "direct_positive_checks": {
            "inherited_full_h560_colourings": len(inherited),
            "inherited_unit_edge_checks": inherited_checks,
            "new_full_h560_colourings": len(new_words),
            "new_unit_edge_checks": new_checks,
            "new_orders": [len(active) for active in new_active],
            "new_omission_sets": new_omissions,
            "necessity_witness_indices": necessity_indices,
        },
        "finite_reduction": {
            "mandatory_vertices": len(base),
            "optional_vertices": len(optional),
            "disjoint_pairs": len(pairs),
            "outside_pair_vertices": len(outside),
            "selected_optional_vertices_at_order_508": 10,
            "family_members": len(rows),
            "generating_function_coefficient_x10": coefficient,
            "family_sha256": digest(family_raw),
        },
        "entrywise_coverage": {
            "inherited_residual": len(residual),
            "new_first_cover_counts": [counts[40], counts[41]],
            "uncovered": len(uncovered),
            "coverage_sha256": digest(assignment),
            "first_cover_counts": dict(sorted(counts.items())),
        },
        "negative_controls": {
            "monochromatic_new_witness_rejected": True,
            "short_new_witness_rejected": True,
            "rows_uncovered_without_second_new_witness": len(missing_without_second),
            "rows_uncovered_without_both_new_witnesses": len(missing_without_new),
            **controls,
        },
        "scope": {
            "fixed_h560_through_508_closed": True,
            "record_improvement": False,
            "sub509_five_chromatic_graph_established": False,
            "general_h632_subgraphs_closed": False,
            "other_euclidean_supports_closed": False,
            "sat_solver_needed": False,
            "negative_search_result_needed": False,
        },
        "trust_boundary": [
            "the previously accepted M492 singleton-deletion theorem",
            "SHA-256-pinned coordinate and certificate inputs",
            "linear independence of the eight squarefree-radical basis elements",
            "ordinary CPython integer/Fraction execution and exhaustive finite enumeration",
            "author-published positive colour words and left/right gluing data, all checked definitionally here",
            "SHA-256 collision resistance for byte identities",
        ],
        "python": sys.version.split()[0],
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "all_checks_passed": True,
        "h560_vertices": len(retained),
        "h560_edges": len(h560_edges),
        "necessary_supports": len(rows),
        "inherited_residual": len(residual),
        "new_cover_counts": [counts[40], counts[41]],
        "uncovered": len(uncovered),
        "family_sha256": digest(family_raw),
        "coverage_sha256": digest(assignment),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
