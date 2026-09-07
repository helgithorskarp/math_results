#!/usr/bin/env python3
"""Independent exact checker for the T375 high-contact target family."""

from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter
from itertools import combinations
from math import isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "hadwiger_nelson_small_triangle_forcer375"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read(path: Path):
    return json.loads(path.read_text())


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rotate(p: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    a, b, c, d = p
    doubled = (-a - c, -b - 3 * d, 3 * a - c, b - d)
    require(all(x % 2 == 0 for x in doubled), "nonintegral orbit")
    return tuple(x // 2 for x in doubled)


def is_unit(p, q) -> bool:
    a, b, c, d = (x - y for x, y in zip(p, q))
    return 3 * a * a + 11 * b * b + c * c + 33 * d * d == 1296 and a * b + c * d == 0


def reconstruct_base():
    appendix = read(PARENT / "appendix.json")
    require(
        type(appendix) is list
        and len(appendix) == 109
        and all(type(row) is list and len(row) == 4 and all(type(x) is int for x in row) for row in appendix),
        "malformed appendix",
    )
    orbit = set()
    for row in appendix:
        p = tuple(row)
        for _ in range(3):
            orbit.add(p)
            a, b, c, d = p
            orbit.add((-a, -b, c, d))
            p = rotate(p)
    first = [(0, 0, 12, 0), (-6, 0, -6, 0), (6, 0, -6, 0)]
    require(len(orbit) == 627 and set(first) <= orbit, "wrong source orbit")
    reference = first + sorted(orbit - set(first))
    parent = read(PARENT / "certificate.json")
    keep = parent.get("retained_reference_indices")
    require(
        type(keep) is list
        and keep == sorted(set(keep))
        and len(keep) == 375
        and keep[:3] == [0, 1, 2],
        "bad retained set",
    )
    points = [reference[i] for i in keep]
    edges = [[u, v] for u, v in combinations(range(len(points)), 2) if is_unit(points[u], points[v])]
    require(len(set(points)) == 375 and len(edges) == 1661, "wrong base graph")
    require(digest(points) == parent.get("point_sha256"), "parent point hash mismatch")
    require(digest(edges) == parent.get("edge_sha256"), "parent edge hash mismatch")
    return points, edges, parent


def enumerate_unit_directions():
    out = []
    bound = 1296
    for a in range(-isqrt(bound // 3), isqrt(bound // 3) + 1):
        after_a = bound - 3 * a * a
        for b in range(-isqrt(after_a // 11), isqrt(after_a // 11) + 1):
            after_b = after_a - 11 * b * b
            for d in range(-isqrt(after_b // 33), isqrt(after_b // 33) + 1):
                square = after_b - 33 * d * d
                c = isqrt(square)
                if c * c != square:
                    continue
                for signed_c in sorted({c, -c}):
                    if a * b + signed_c * d == 0:
                        out.append((a, b, signed_c, d))
    out.sort()
    require(len(out) == len(set(out)) == 54, "wrong unit-direction count")
    require(set(out) == {tuple(-x for x in row) for row in out}, "directions not closed under negation")
    require(all(is_unit((0, 0, 0, 0), row) for row in out), "nonunit direction")
    return out


def reconstruct_support(base_points):
    directions = enumerate_unit_directions()
    base_set = set(base_points)
    completion = sorted(
        {
            tuple(x + y for x, y in zip(point, displacement))
            for point in base_points
            for displacement in directions
        }
        - base_set
    )
    base_degree = [
        sum(tuple(x - y for x, y in zip(point, displacement)) in base_set for displacement in directions)
        for point in completion
    ]
    core_additions = [point for point, degree in zip(completion, base_degree) if degree >= 6]
    optional = [point for point, degree in zip(completion, base_degree) if degree == 5]
    points = base_points + core_additions + optional
    core_n = len(base_points) + len(core_additions)
    edges = [[u, v] for u, v in combinations(range(len(points)), 2) if is_unit(points[u], points[v])]
    core_edges = [(u, v) for u, v in edges if v < core_n]
    optional_core = [set() for _ in optional]
    optional_edges = set()
    for u, v in edges:
        if u < core_n <= v:
            optional_core[v - core_n].add(u)
        elif core_n <= u:
            optional_edges.add((u - core_n, v - core_n))
    require(len(completion) == 12184, "wrong completion size")
    require(core_n == 506 and len(optional) == 141, "wrong band sizes")
    require(len(core_edges) == 2677, "wrong core edge count")
    require(sum(map(len, optional_core)) == 868 and len(optional_edges) == 81, "wrong boundary edges")
    pair_edge_counts = [
        len(core_edges) + len(optional_core[i]) + len(optional_core[j]) + ((i, j) in optional_edges)
        for i, j in combinations(range(len(optional)), 2)
    ]
    return {
        "directions": directions,
        "completion": completion,
        "base_degree": base_degree,
        "points": points,
        "edges": edges,
        "core_n": core_n,
        "core_edges": core_edges,
        "optional_core": optional_core,
        "optional_edges": optional_edges,
        "target_edge_range": [min(pair_edge_counts), max(pair_edge_counts)],
    }


def validate_certificate(cert, support):
    require(cert.get("schema") == "t375-high-contact-two-point-cover-v1", "wrong schema")
    require(cert.get("target_found") is False, "wrong target status")
    construction = cert.get("construction")
    expected_construction = {
        "base_vertices": 375,
        "base_edges": 1661,
        "unit_directions": 54,
        "completion_vertices": 12184,
        "base_degree_histogram": {str(k): v for k, v in sorted(Counter(support["base_degree"]).items())},
        "core_minimum_base_degree": 6,
        "core_vertices": 506,
        "core_edges": 2677,
        "optional_base_degree": 5,
        "optional_vertices": 141,
        "optional_core_edges": 868,
        "optional_internal_edges": 81,
        "support_vertices": 647,
        "support_edges": 3626,
        "pair_members": 9870,
        "total_members_through_two_optional_points": 10012,
        "target_vertices": 508,
        "target_edge_range": support["target_edge_range"],
        "triangle_pin": [0, 34, 36],
    }
    require(construction == expected_construction, "construction metadata mismatch")
    edge_set = {tuple(edge) for edge in support["edges"]}
    require(all(tuple(sorted(pair)) in edge_set for pair in combinations((0, 34, 36), 2)), "pin is not a unit triangle")
    hashes = {
        "unit_directions_sha256": digest(support["directions"]),
        "completion_points_sha256": digest(support["completion"]),
        "support_points_sha256": digest(support["points"]),
        "support_edges_sha256": digest(support["edges"]),
        "core_points_sha256": digest(support["points"][: support["core_n"]]),
        "core_edges_sha256": digest(support["core_edges"]),
    }
    claimed_hashes = cert.get("hashes")
    require(type(claimed_hashes) is dict, "missing hashes")
    for key, value in hashes.items():
        require(claimed_hashes.get(key) == value, f"hash mismatch: {key}")

    library = cert.get("library")
    require(type(library) is list and len(library) == 8, "wrong library size")
    core_edges = support["core_edges"]
    optional_core = support["optional_core"]
    optional_edges = support["optional_edges"]
    pairs = list(combinations(range(141), 2))
    coverages = []
    available_rows = []
    seen = set()
    for row_index, row in enumerate(library):
        require(type(row) is dict and set(row) == {"trigger_pair", "core_colouring", "coverage_count", "new_coverage_count"}, "bad library row")
        word_text = row["core_colouring"]
        require(type(word_text) is str and len(word_text) == 506 and set(word_text) <= set("0123"), "bad core word")
        word = [ord(c) - ord("0") for c in word_text]
        require([word[v] for v in (0, 34, 36)] == [0, 1, 2], "triangle pin mismatch")
        require(all(word[u] != word[v] for u, v in core_edges), "improper core colouring")
        available = []
        for neighbours in optional_core:
            forbidden = {word[v] for v in neighbours}
            available.append(tuple(c for c in range(4) if c not in forbidden))
        covered = set()
        for pair_index, (i, j) in enumerate(pairs):
            if not available[i] or not available[j]:
                continue
            if (i, j) not in optional_edges or any(a != b for a in available[i] for b in available[j]):
                covered.add(pair_index)
        trigger = row["trigger_pair"]
        require(type(trigger) is list and len(trigger) == 2 and tuple(trigger) in pairs, "bad trigger")
        trigger_index = pairs.index(tuple(trigger))
        require(trigger_index in covered, "trigger not covered")
        require(row["coverage_count"] == len(covered), "wrong coverage count")
        require(row["new_coverage_count"] == len(covered - seen), "wrong new coverage count")
        seen |= covered
        coverages.append(covered)
        available_rows.append(available)
    require(seen == set(range(len(pairs))), "pair family not completely covered")

    first_cover = []
    for pair_index, (i, j) in enumerate(pairs):
        row_index = next(r for r, covered in enumerate(coverages) if pair_index in covered)
        first_cover.append(row_index)
        available = available_rows[row_index]
        ci = available[i][0]
        cj = next(c for c in available[j] if (i, j) not in optional_edges or c != ci)
        require(ci in available[i] and cj in available[j], "invalid extension colour")
        require((i, j) not in optional_edges or ci != cj, "optional edge conflict")
    require(claimed_hashes.get("first_cover_rows_sha256") == hashlib.sha256(bytes(first_cover)).hexdigest(), "first-cover hash mismatch")
    require(all(any(row[i] for row in available_rows) for i in range(141)), "singleton not covered")
    return hashes | {"first_cover_rows_sha256": hashlib.sha256(bytes(first_cover)).hexdigest()}


def malformed_controls(cert, support) -> int:
    cases = []
    bad = copy.deepcopy(cert)
    bad["library"] = bad["library"][:-1]
    cases.append(bad)
    bad = copy.deepcopy(cert)
    bad["library"][0]["core_colouring"] = "x" + bad["library"][0]["core_colouring"][1:]
    cases.append(bad)
    bad = copy.deepcopy(cert)
    bad["library"][0]["core_colouring"] = "0" * 506
    cases.append(bad)
    bad = copy.deepcopy(cert)
    bad["library"][-1] = copy.deepcopy(bad["library"][0])
    cases.append(bad)
    bad = copy.deepcopy(cert)
    bad["hashes"]["support_edges_sha256"] = "0" * 64
    cases.append(bad)
    bad = copy.deepcopy(cert)
    bad["construction"]["optional_vertices"] = 140
    cases.append(bad)
    bad = copy.deepcopy(cert)
    bad["target_found"] = True
    cases.append(bad)
    for candidate in cases:
        try:
            validate_certificate(candidate, support)
        except ValueError:
            continue
        raise RuntimeError("malformed certificate accepted")
    return len(cases)


def main() -> None:
    provenance = read(HERE / "provenance.json")
    require(provenance["parent_appendix_sha256"] == file_digest(PARENT / "appendix.json"), "appendix provenance mismatch")
    require(provenance["parent_certificate_sha256"] == file_digest(PARENT / "certificate.json"), "parent provenance mismatch")
    base_points, base_edges, parent = reconstruct_base()
    support = reconstruct_support(base_points)
    certificate = read(HERE / "certificate.json")
    hashes = validate_certificate(certificate, support)
    controls = malformed_controls(certificate, support)
    result = {
        "verified": True,
        "base_vertices": len(base_points),
        "base_edges": len(base_edges),
        "unit_directions": len(support["directions"]),
        "completion_vertices": len(support["completion"]),
        "base_degree_histogram": {str(k): v for k, v in sorted(Counter(support["base_degree"]).items())},
        "core_vertices": support["core_n"],
        "core_edges": len(support["core_edges"]),
        "optional_vertices": len(support["optional_core"]),
        "optional_core_edges": sum(map(len, support["optional_core"])),
        "optional_internal_edges": len(support["optional_edges"]),
        "support_vertices": len(support["points"]),
        "support_edges": len(support["edges"]),
        "family_members": 10012,
        "pair_members": 9870,
        "orders": [506, 507, 508],
        "target_edge_range": support["target_edge_range"],
        "colouring_library_rows": len(certificate["library"]),
        "all_members_four_colourable": True,
        "hashes": hashes,
        "parent_point_sha256": parent["point_sha256"],
        "parent_edge_sha256": parent["edge_sha256"],
        "malformed_controls_rejected": controls,
        "target_found": False,
    }
    require(result == read(HERE / "expected.json"), "expected output mismatch")
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
