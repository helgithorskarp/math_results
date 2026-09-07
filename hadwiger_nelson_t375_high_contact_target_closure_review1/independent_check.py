#!/usr/bin/env python3
"""Independent exact audit of the T375 high-contact completion cover.

No submitted module is imported.  The implementation deliberately uses a
full four-variable direction scan, representation-count completion degrees,
translated-neighbour edge construction, and bit-mask colouring checks.
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, deque
from itertools import combinations
from math import comb, isqrt
from pathlib import Path


class ReviewFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewFailure(message)


def load_json(path: Path):
    return json.loads(path.read_text())


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def object_sha256(value) -> str:
    raw = json.dumps(value, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def add(left, right):
    return tuple(x + y for x, y in zip(left, right))


def negate(point):
    return tuple(-x for x in point)


def rotate_120(point):
    """Exact 120-degree rotation in the integral lattice coordinates."""
    a, b, c, d = point
    numerators = (-a - c, -b - 3 * d, 3 * a - c, b - d)
    require(all(value % 2 == 0 for value in numerators),
            f"rotation leaves the integral lattice at {point}")
    return tuple(value // 2 for value in numerators)


def reflect(point):
    a, b, c, d = point
    return (-a, -b, c, d)


def symmetry_orbit(seed):
    """Generate the orbit by group closure, rather than a fixed six-row loop."""
    seen = {seed}
    queue = deque([seed])
    while queue:
        point = queue.popleft()
        for image in (rotate_120(point), reflect(point)):
            if image not in seen:
                seen.add(image)
                queue.append(image)
    return seen


def is_unit_difference(delta) -> bool:
    a, b, c, d = delta
    rational = 3 * a * a + 11 * b * b + c * c + 33 * d * d
    irrational_coefficient = a * b + c * d
    return rational == 1296 and irrational_coefficient == 0


def reconstruct_base(parent_dir: Path):
    appendix_path = parent_dir / "appendix.json"
    parent_certificate_path = parent_dir / "certificate.json"
    require(file_sha256(appendix_path) ==
            "dd74c3ef0bb3e9cc1c9c32f7ecc703c1d85cacaca6fca97834d162e8c05997fa",
            "parent appendix bytes differ from the reviewed source")
    require(file_sha256(parent_certificate_path) ==
            "282fd209157b0c327e02451c32a3d2f2dbb40c4ec31e6531bdd3b8316854b28e",
            "parent certificate bytes differ from the reviewed source")
    appendix = load_json(appendix_path)
    require(type(appendix) is list and len(appendix) == 109,
            "parent appendix does not have 109 seed rows")
    require(all(type(row) is list and len(row) == 4
                and all(type(value) is int for value in row)
                for row in appendix), "malformed parent appendix")

    orbit = set()
    orbit_sizes = Counter()
    for row in appendix:
        local = symmetry_orbit(tuple(row))
        orbit_sizes[len(local)] += 1
        orbit.update(local)
    terminals = [(0, 0, 12, 0), (-6, 0, -6, 0), (6, 0, -6, 0)]
    require(len(orbit) == 627 and set(terminals) <= orbit,
            "wrong parent source orbit")
    reference = terminals + sorted(orbit - set(terminals))

    parent_certificate = load_json(parent_certificate_path)
    retained = parent_certificate.get("retained_reference_indices")
    require(type(retained) is list and len(retained) == 375,
            "wrong retained-index count")
    require(all(type(index) is int and 0 <= index < len(reference)
                for index in retained), "invalid retained index")
    require(retained == sorted(set(retained)) and retained[:3] == [0, 1, 2],
            "retained indices are not canonical")
    base = [reference[index] for index in retained]
    require(len(set(base)) == 375, "duplicate base point")
    require(object_sha256(base) ==
            "0bf15083801eb6fa982b04e820aca6c5a16c9b75b2d85b3efd00c53716edb1fe",
            "parent point hash mismatch")
    return base, orbit_sizes, parent_certificate


def enumerate_directions_full_scan():
    """Exhaust the coefficient box forced by the positive quadratic form."""
    bounds = (isqrt(1296 // 3), isqrt(1296 // 11),
              isqrt(1296), isqrt(1296 // 33))
    directions = []
    tested = 0
    for a in range(-bounds[0], bounds[0] + 1):
        for b in range(-bounds[1], bounds[1] + 1):
            for c in range(-bounds[2], bounds[2] + 1):
                for d in range(-bounds[3], bounds[3] + 1):
                    tested += 1
                    delta = (a, b, c, d)
                    if is_unit_difference(delta):
                        directions.append(delta)
    directions.sort()
    require(len(directions) == len(set(directions)) == 54,
            f"found {len(directions)} rather than 54 directions")
    require(set(map(negate, directions)) == set(directions),
            "direction set is not closed under negation")
    return directions, tested


def reconstruct_support(base, directions):
    # Each representation q=p+d is in bijection with one T-neighbour p of q.
    landing_multiplicity = Counter(add(point, delta)
                                   for point in base for delta in directions)
    for point in base:
        landing_multiplicity.pop(point, None)
    completion = sorted(landing_multiplicity)
    degree_histogram = Counter(landing_multiplicity.values())
    require(len(completion) == 12184, "wrong completion-set order")
    require(degree_histogram == Counter({1: 9615, 2: 1482, 3: 529,
                                        4: 286, 5: 141, 6: 71, 7: 21,
                                        8: 16, 9: 18, 10: 5}),
            f"wrong completion incidence histogram {degree_histogram}")

    core_extra = [point for point in completion
                  if landing_multiplicity[point] >= 6]
    optional = [point for point in completion
                if landing_multiplicity[point] == 5]
    points = list(base) + core_extra + optional
    core_order = len(base) + len(core_extra)
    require((len(core_extra), len(optional), core_order, len(points)) ==
            (131, 141, 506, 647), "wrong support band orders")
    require(len(set(points)) == len(points), "duplicate support point")

    # Generate edges through translated-neighbour lookup, not all point pairs.
    index = {point: i for i, point in enumerate(points)}
    edge_set = set()
    for left, point in enumerate(points):
        for delta in directions:
            right = index.get(add(point, delta))
            if right is not None and left < right:
                edge_set.add((left, right))
    edges = sorted(edge_set)
    require(all(is_unit_difference(tuple(points[right][k] - points[left][k]
                                         for k in range(4)))
                for left, right in edges), "nonunit support edge")
    core_edges = [(left, right) for left, right in edges if right < core_order]
    base_edges = [(left, right) for left, right in edges if right < len(base)]
    optional_core = [set() for _ in optional]
    optional_edges = set()
    for left, right in edges:
        if left < core_order <= right:
            optional_core[right - core_order].add(left)
        elif core_order <= left:
            optional_edges.add((left - core_order, right - core_order))
    require(len(base_edges) == 1661, "wrong base edge count")
    require(len(core_edges) == 2677, "wrong core edge count")
    require(sum(map(len, optional_core)) == 868,
            "wrong optional-to-core edge count")
    require(len(optional_edges) == 81, "wrong optional-band edge count")
    require(len(edges) == 3626, "wrong support edge count")
    require(object_sha256(base_edges) ==
            "0e3d04cf0e0df94e9a7a9adda6677d92db162faf3ab29947dde8e0f52c287660",
            "parent edge hash mismatch")
    return {
        "completion": completion,
        "degree_histogram": degree_histogram,
        "points": points,
        "core_order": core_order,
        "edges": edges,
        "base_edges": base_edges,
        "core_edges": core_edges,
        "optional_core": optional_core,
        "optional_edges": optional_edges,
    }


def first_colour(mask: int) -> int:
    require(mask != 0, "cannot choose from an empty colour mask")
    return (mask & -mask).bit_length() - 1


def choose_pair(left_mask: int, right_mask: int, adjacent: bool):
    for left_colour in range(4):
        if not (left_mask >> left_colour) & 1:
            continue
        for right_colour in range(4):
            if (right_mask >> right_colour) & 1 and (
                    not adjacent or left_colour != right_colour):
                return left_colour, right_colour
    raise ReviewFailure("claimed covered optional pair has no colour choice")


def verify_certificate(package: Path, directions, direction_box_size,
                       base, orbit_sizes, parent_certificate, support):
    certificate_path = package / "certificate.json"
    require(file_sha256(certificate_path) ==
            "3431c8ffa3223e7c2efd26f43a41a1ad7ebeff3ddddfda220fedfe24dff2844f",
            "target certificate bytes differ from reviewed source")
    certificate = load_json(certificate_path)
    require(certificate.get("schema") ==
            "t375-high-contact-two-point-cover-v1", "wrong schema")
    require(certificate.get("target_found") is False,
            "certificate does not record a negative target search")

    histogram = {str(key): value for key, value in
                 sorted(support["degree_histogram"].items())}
    pair_edge_counts = []
    for left, right in combinations(range(141), 2):
        pair_edge_counts.append(
            len(support["core_edges"])
            + len(support["optional_core"][left])
            + len(support["optional_core"][right])
            + ((left, right) in support["optional_edges"])
        )
    edge_count_histogram = Counter(pair_edge_counts)
    expected_construction = {
        "base_vertices": 375,
        "base_edges": 1661,
        "unit_directions": 54,
        "completion_vertices": 12184,
        "base_degree_histogram": histogram,
        "core_minimum_base_degree": 6,
        "core_vertices": 506,
        "core_edges": 2677,
        "optional_base_degree": 5,
        "optional_vertices": 141,
        "optional_core_edges": 868,
        "optional_internal_edges": 81,
        "support_vertices": 647,
        "support_edges": 3626,
        "pair_members": comb(141, 2),
        "total_members_through_two_optional_points": 1 + 141 + comb(141, 2),
        "target_vertices": 508,
        "target_edge_range": [min(pair_edge_counts), max(pair_edge_counts)],
        "triangle_pin": [0, 34, 36],
    }
    require(certificate.get("construction") == expected_construction,
            "certificate construction metadata mismatch")

    hashes = {
        "unit_directions_sha256": object_sha256(directions),
        "completion_points_sha256": object_sha256(support["completion"]),
        "support_points_sha256": object_sha256(support["points"]),
        "support_edges_sha256": object_sha256(support["edges"]),
        "core_points_sha256": object_sha256(
            support["points"][:support["core_order"]]),
        "core_edges_sha256": object_sha256(support["core_edges"]),
    }
    published_hashes = certificate.get("hashes")
    require(type(published_hashes) is dict, "certificate hashes missing")
    for name, value in hashes.items():
        require(published_hashes.get(name) == value,
                f"certificate hash mismatch: {name}")

    edge_set = set(support["edges"])
    require(all(tuple(sorted(edge)) in edge_set
                for edge in combinations((0, 34, 36), 2)),
            "the colour-normalization pin is not a triangle")
    library = certificate.get("library")
    require(type(library) is list and len(library) == 8,
            "certificate does not have eight colouring rows")
    pair_list = list(combinations(range(141), 2))
    pair_to_index = {pair: index for index, pair in enumerate(pair_list)}
    full_pair_mask = (1 << len(pair_list)) - 1
    cover_masks = []
    availability_rows = []
    running_cover = 0
    coverage_counts = []
    new_counts = []

    for row_index, row in enumerate(library):
        require(type(row) is dict and set(row) == {
            "trigger_pair", "core_colouring", "coverage_count",
            "new_coverage_count"}, f"malformed library row {row_index}")
        text = row["core_colouring"]
        require(type(text) is str and len(text) == 506
                and set(text) <= set("0123"),
                f"invalid core-colouring word {row_index}")
        colours = [ord(character) - 48 for character in text]
        require([colours[index] for index in (0, 34, 36)] == [0, 1, 2],
                f"triangle normalization fails in row {row_index}")
        require(all(colours[left] != colours[right]
                    for left, right in support["core_edges"]),
                f"monochromatic core edge in row {row_index}")

        availability = []
        for neighbours in support["optional_core"]:
            forbidden = 0
            for neighbour in neighbours:
                forbidden |= 1 << colours[neighbour]
            availability.append(0b1111 ^ forbidden)
        coverage = 0
        for pair_index, (left, right) in enumerate(pair_list):
            left_mask, right_mask = availability[left], availability[right]
            covered = left_mask != 0 and right_mask != 0
            if covered and (left, right) in support["optional_edges"]:
                # An adjacent pair fails precisely when both masks are the
                # same singleton.  Otherwise two distinct choices exist.
                same_singleton = (left_mask == right_mask
                                  and left_mask.bit_count() == 1)
                covered = not same_singleton
            if covered:
                coverage |= 1 << pair_index
        trigger = row["trigger_pair"]
        require(type(trigger) is list and len(trigger) == 2
                and tuple(trigger) in pair_to_index,
                f"invalid trigger in row {row_index}")
        require((coverage >> pair_to_index[tuple(trigger)]) & 1,
                f"row {row_index} does not cover its trigger")
        count = coverage.bit_count()
        new_count = (coverage & ~running_cover).bit_count()
        require(row["coverage_count"] == count,
                f"coverage count mismatch in row {row_index}")
        require(row["new_coverage_count"] == new_count,
                f"new-coverage count mismatch in row {row_index}")
        coverage_counts.append(count)
        new_counts.append(new_count)
        running_cover |= coverage
        cover_masks.append(coverage)
        availability_rows.append(availability)

    require(coverage_counts == [9179, 9315, 9452, 9590,
                                9729, 9729, 9452, 9044],
            "unexpected row coverage counts")
    require(new_counts == [9179, 136, 137, 138, 139, 139, 1, 1],
            "unexpected successive new-coverage counts")
    require(running_cover == full_pair_mask,
            "the colouring library does not cover all optional pairs")

    # Explicitly choose colours and check every optional incidence for every
    # one of the 9,870 target-sized physical graphs.
    first_cover_rows = []
    coverage_multiplicity = Counter()
    for pair_index, (left, right) in enumerate(pair_list):
        rows = [row_index for row_index, mask in enumerate(cover_masks)
                if (mask >> pair_index) & 1]
        require(rows, f"uncovered pair {(left, right)}")
        coverage_multiplicity[len(rows)] += 1
        row_index = rows[0]
        first_cover_rows.append(row_index)
        colours = [ord(character) - 48
                   for character in library[row_index]["core_colouring"]]
        left_colour, right_colour = choose_pair(
            availability_rows[row_index][left],
            availability_rows[row_index][right],
            (left, right) in support["optional_edges"],
        )
        require(all(colours[vertex] != left_colour
                    for vertex in support["optional_core"][left]),
                f"left optional conflict for pair {(left, right)}")
        require(all(colours[vertex] != right_colour
                    for vertex in support["optional_core"][right]),
                f"right optional conflict for pair {(left, right)}")
        require((left, right) not in support["optional_edges"]
                or left_colour != right_colour,
                f"optional-pair conflict for {(left, right)}")
    first_cover_hash = hashlib.sha256(bytes(first_cover_rows)).hexdigest()
    require(first_cover_hash == published_hashes.get(
            "first_cover_rows_sha256"), "first-cover-row hash mismatch")

    # Empty and singleton members are checked separately, without inferring
    # them merely from the count of covered pairs.
    require(library, "empty core-colouring library")
    for optional_index in range(141):
        row_index = next((row for row, availability in
                          enumerate(availability_rows)
                          if availability[optional_index]), None)
        require(row_index is not None,
                f"optional singleton {optional_index} cannot be extended")
        colour = first_colour(availability_rows[row_index][optional_index])
        core_colours = [ord(character) - 48 for character in
                        library[row_index]["core_colouring"]]
        require(all(core_colours[vertex] != colour for vertex in
                    support["optional_core"][optional_index]),
                f"singleton {optional_index} has a colour conflict")

    return {
        "status": "VERIFIED_INDEPENDENT_T375_HIGH_CONTACT_CLOSURE",
        "certificate_sha256": file_sha256(certificate_path),
        "parent_vertices": len(base),
        "parent_edges": len(support["base_edges"]),
        "source_orbit_vertices": 627,
        "source_seed_orbit_size_histogram": {
            str(key): value for key, value in sorted(orbit_sizes.items())},
        "direction_box_tuples_tested": direction_box_size,
        "unit_directions": len(directions),
        "completion_vertices": len(support["completion"]),
        "completion_degree_histogram": histogram,
        "core_vertices": support["core_order"],
        "core_edges": len(support["core_edges"]),
        "optional_vertices": len(support["optional_core"]),
        "optional_internal_edges": len(support["optional_edges"]),
        "target_pair_members": len(pair_list),
        "target_edge_count_histogram": {
            str(key): value for key, value in sorted(edge_count_histogram.items())},
        "colouring_rows": len(library),
        "coverage_counts": coverage_counts,
        "new_coverage_counts": new_counts,
        "coverage_multiplicity_histogram": {
            str(key): value for key, value in
            sorted(coverage_multiplicity.items())},
        "first_cover_rows_sha256": first_cover_hash,
        "all_members_through_two_optional_points_four_colourable": True,
        "target_found": False,
        "parent_certificate_target_found": parent_certificate.get(
            "target_found"),
    }


def main() -> None:
    require(len(sys.argv) == 2,
            "usage: independent_check.py PATH/TO/math_results_checkout")
    source_root = Path(sys.argv[1]).resolve()
    package = source_root / "hadwiger_nelson_t375_high_contact_target_closure"
    parent_dir = source_root / "hadwiger_nelson_small_triangle_forcer375"
    require(package.is_dir() and parent_dir.is_dir(),
            "source root does not contain the required packages")
    base, orbit_sizes, parent_certificate = reconstruct_base(parent_dir)
    directions, direction_box_size = enumerate_directions_full_scan()
    support = reconstruct_support(base, directions)
    result = verify_certificate(
        package, directions, direction_box_size, base, orbit_sizes,
        parent_certificate, support,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
