#!/usr/bin/env python3
"""Independent check of h3999's exterior census and colouring cover.

No Python or C++ module from the reviewed package is imported.  The only
generated author data used are the untrusted centre rows from a fresh full
replay; exact incidences and exhaustive coverage are reconstructed here.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import comb, lcm
from pathlib import Path
import subprocess


EXPECTED_HASHES = {
    "hadwiger_nelson_h516_degree4_surgeries/SOURCE.json":
        "3f60fe94c7cd3d9c70b7cc52124fa185d4b46d54bb59b21bca0c45d2b181fd51",
    "hadwiger_nelson_heule516_all_plane_onepoint_closure/certificate.json":
        "8713d2af4f8e02bbd873bdb01f671a4630c3b946e5f65e810b2361a4a6dd06cb",
    "hadwiger_nelson_heule516_single_point_h632_closure/certificate.json":
        "2afa90a5e96af79d0c2855db41a7d17fb8e34fee2c30bb81e3dfd9cc26da6335",
    "hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json":
        "bc8e0f5f5ec7fa5f2376cc77ba0e65f6023b340cf48990370d5eda575d30ae79",
    "hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json":
        "89345930e1bea184ce2457b0e14a015bcd9a2901cfc609a6468cf050234a8317",
    "hadwiger_nelson_heule632_minimize/certificate.json":
        "3a22660e40329c0aef34e108b91747f529adb046cf687df5b05b3531ca17e35b",
    "hadwiger_nelson_heule560_target508_review1/result.json":
        "9b2661d57b32ce6a1d03586ed0fe3451cfe97119e728cd7596d6a8663483f425",
}
REVIEWED_REF = "bafkreidrpgz7n2d5c4z7o4cifdreb7cchzft2ae7sbgkbgnlqlocr7cr7u"
REVIEWED_COMMIT = "4241a558b4f1279e2a8741202cc2bd2c93b3048c"
H560_REVIEW_REF = "bafkreifbln2uuz67wbkaz3ae54j3jv5kfsqyh2wzinztiaxj7zrupmjb7e"
RADICAL_FACTOR = (1, 3, 5, 15, 11, 33, 55, 165)
ZERO = (0,) * 8


def need(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def parse_point(row: list[list[str | int]]) -> tuple[tuple[Fraction, ...], ...]:
    need(len(row) == 2 and all(len(axis) == 8 for axis in row), "point shape")
    return tuple(tuple(Fraction(value) for value in axis) for axis in row)


def multiply(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    """Product in the squarefree basis indexed by subsets of {3,5,11}."""
    result = [0] * 8
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(b):
            if y:
                result[i ^ j] += x * y * RADICAL_FACTOR[i & j]
    return tuple(result)


def squared_distance(a: tuple[tuple[int, ...], ...],
                     b: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    dx = tuple(x - y for x, y in zip(a[0], b[0]))
    dy = tuple(x - y for x, y in zip(a[1], b[1]))
    return tuple(x + y for x, y in zip(multiply(dx, dx), multiply(dy, dy)))


def scale_point(point: tuple[tuple[Fraction, ...], ...], denominator: int
                ) -> tuple[tuple[int, ...], ...]:
    result = []
    for axis in point:
        scaled = [value * denominator for value in axis]
        need(all(value.denominator == 1 for value in scaled), "point scaling")
        result.append(tuple(value.numerator for value in scaled))
    return tuple(result)


def unpack(encoded: str, length: int) -> list[int]:
    raw = base64.b64decode(encoded, validate=True)
    need(len(raw) == (length + 3) // 4, "packed colouring length")
    need(base64.b64encode(raw).decode("ascii") == encoded, "noncanonical base64")
    values = [(raw[i // 4] >> (2 * (i % 4))) & 3 for i in range(length)]
    need(all(((raw[i // 4] >> (2 * (i % 4))) & 3) == 0
             for i in range(length, 4 * len(raw))), "nonzero packed padding")
    return values


def load_inputs(repository: Path):
    for relative, expected in EXPECTED_HASHES.items():
        need(digest(repository / relative) == expected, "input hash: " + relative)

    source = json.loads((repository /
        "hadwiger_nelson_h516_degree4_surgeries/SOURCE.json").read_text())
    union = json.loads((repository /
        "hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json").read_text())
    fresh = json.loads((repository /
        "hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json").read_text())
    heule_labels = [v for v in sorted(map(int, union["coordinates"]))
                    if "510" in union["provenance"][v]]
    host = [parse_point(union["coordinates"][str(v)]) for v in heule_labels]
    host += [parse_point(row["coordinates"]) for row in fresh]
    need(len(host) == len(set(host)) == 632, "H632 point reconstruction")

    labels = source["labels"]
    base = [parse_point([[Fraction(c, 96) for c in axis] for axis in point])
            for point in source["coordinates"]]
    need(labels == sorted(set(labels)) and len(labels) == len(base) == 516,
         "base labels")
    need([host[label] for label in labels] == base, "base/H632 coordinate alignment")
    return source, host, labels, base


def exact_graph(host, labels, base, source):
    denominator = lcm(*(value.denominator for point in host for axis in point for value in axis))
    need(denominator == 96, "unexpected H632 denominator")
    scaled_host = [scale_point(point, denominator) for point in host]
    unit = (denominator * denominator,) + ZERO[1:]
    edges = []
    adjacency = [set() for _ in host]
    for left, right in combinations(range(632), 2):
        if squared_distance(scaled_host[left], scaled_host[right]) == unit:
            edges.append((left, right))
            adjacency[left].add(right)
            adjacency[right].add(left)
    need(len(edges) == 3112, "H632 edge count")
    base_set = set(labels)
    base_edges = [(u, v) for u, v in edges if u in base_set and v in base_set]
    need(base_edges == [tuple(edge) for edge in source["edges"]], "complete base edge stream")
    need(len(base_edges) == 2538, "base edge count")
    return adjacency, base_edges


def decode_deletion_rows(rows, labels, base_edges, require_all_removed=True):
    need(rows == sorted(rows, key=lambda row: (row["removed"], row["colours"])),
         "deletion row order")
    need(len({(row["removed"], row["colours"]) for row in rows}) == len(rows),
         "duplicate deletion row")
    decoded = []
    removed_seen = set()
    edge_checks = 0
    label_set = set(labels)
    for row in rows:
        need(set(row) == {"removed", "colours"}, "deletion row fields")
        removed = row["removed"]
        need(type(removed) is int and removed in label_set, "removed label")
        order = [v for v in labels if v != removed]
        colouring = dict(zip(order, unpack(row["colours"], len(order))))
        for u, v in base_edges:
            if removed not in (u, v):
                need(colouring[u] != colouring[v], "monochromatic base edge")
                edge_checks += 1
        removed_seen.add(removed)
        decoded.append((removed, colouring))
    if require_all_removed:
        need(removed_seen == label_set, "missing base-deletion witness")
    return decoded, edge_checks


def check_centres(base, labels, host_set, author_work: Path, third_filter: Path,
                  scratch: Path):
    need(digest(author_work / "centres.json") ==
         "2d33a4c3c78026573f777b98f097de09a30b1071b84a0142956f4e38aadba0cc",
         "fresh centres hash")
    need(digest(author_work / "exterior.json") ==
         "0f6c7c84cb1a27fa90b7d14f5c2669bee0cffebb85e7fadedb51a89b790cdee4",
         "fresh exterior hash")
    rows = json.loads((author_work / "centres.json").read_text())
    centres = [parse_point(row["coordinates"]) for row in rows]
    need(centres == sorted(set(centres)) and len(centres) == 1726,
         "centre canonical order")

    scaled_base = {}
    triple_cover = set()
    exterior = []
    degree_histogram = Counter()
    denominator_histogram = Counter()
    for index, (point, row) in enumerate(zip(centres, rows)):
        denominator = lcm(96, *(value.denominator for axis in point for value in axis))
        denominator_histogram[denominator] += 1
        if denominator not in scaled_base:
            scaled_base[denominator] = [scale_point(p, denominator) for p in base]
        scaled_point = scale_point(point, denominator)
        unit = (denominator * denominator,) + ZERO[1:]
        neighbours = [i for i, base_point in enumerate(scaled_base[denominator])
                      if squared_distance(scaled_point, base_point) == unit]
        need(neighbours == row["neighbors"] and len(neighbours) >= 3,
             "centre incidence row")
        witness = row["witness"]
        need(witness == sorted(set(witness)) and len(witness) == 3
             and set(witness) <= set(neighbours), "centre witness")
        for triple in combinations(neighbours, 3):
            need(triple not in triple_cover, "triple assigned to two centres")
            triple_cover.add(triple)
        if len(neighbours) >= 4 and point not in host_set:
            exterior.append({"centre_index": index, **row})
            degree_histogram[len(neighbours)] += 1
    need(denominator_histogram == Counter({96: 1714, 288: 12}), "centre denominators")
    need(exterior == json.loads((author_work / "exterior.json").read_text()),
         "exterior set")

    scratch.mkdir(parents=True, exist_ok=True)
    points_path = scratch / "review_points.txt"
    survivor_path = scratch / "third_survivors.tsv"
    points_path.write_text("516 96\n" + "".join(
        " ".join(str(value) for axis in point for value in axis) + "\n"
        for point in [scale_point(p, 96) for p in base]))
    run = subprocess.run([str(third_filter.resolve()), str(points_path), str(survivor_path)],
                         text=True, capture_output=True, check=True)
    filter_receipt = json.loads(run.stdout)
    need(filter_receipt["triples"] == comb(516, 3), "independent triple count")
    survivors = [tuple(map(int, line.split()))
                 for line in survivor_path.read_text().splitlines()]
    need(survivors == sorted(triple_cover), "independent survivor stream versus exact centres")
    need(digest(survivor_path) ==
         "23f9790bff3809086d28d7ef983b56bb8cb7944c25d4e1fd9a7a6157414baa11",
         "independent survivor hash")
    return rows, exterior, degree_histogram, denominator_histogram, filter_receipt


def exterior_cover(repository, source, labels, base_edges, exterior):
    boundary = json.loads((repository /
        "hadwiger_nelson_heule516_single_point_h632_closure/certificate.json").read_text())
    target = json.loads((repository /
        "hadwiger_nelson_heule516_all_plane_onepoint_closure/certificate.json").read_text())
    need(target["source_sha256"] == EXPECTED_HASHES[
        "hadwiger_nelson_h516_degree4_surgeries/SOURCE.json"], "target source link")
    need(target["target_order"] == 508 and target["outside_H632_points"] == 558,
         "target metadata")
    inherited_decoded, inherited_edge_checks = decode_deletion_rows(
        boundary["deletion_rows"], labels, base_edges)
    additional_decoded, additional_edge_checks = decode_deletion_rows(
        target["additional_deletion_rows"], labels, base_edges,
        require_all_removed=False)
    all_rows = boundary["deletion_rows"] + target["additional_deletion_rows"]
    need(len({(row["removed"], row["colours"]) for row in all_rows}) == len(all_rows),
         "duplicate colouring across inherited and additional rows")
    decoded = inherited_decoded + additional_decoded
    edge_checks = inherited_edge_checks + additional_edge_checks
    counts = []
    extension_tests = 0
    for centre in exterior:
        adjacent = {labels[i] for i in centre["neighbors"]}
        covered = set()
        for removed, colouring in decoded:
            extension_tests += 1
            if len({colouring[v] for v in adjacent if v != removed}) < 4:
                covered.add(removed)
        counts.append(len(covered))
    need(min(counts) == 508 and len(counts) == 558, "exterior deletion coverage")
    return {
        "points": len(counts),
        "inherited_rows": len(boundary["deletion_rows"]),
        "additional_rows": len(target["additional_deletion_rows"]),
        "base_edge_checks": edge_checks,
        "extension_tests": extension_tests,
        "minimum_covered_deletions": min(counts),
        "maximum_covered_deletions": max(counts),
        "coverage_histogram": dict(sorted(Counter(counts).items())),
    }


def boundary_cover(repository, labels, adjacency, base_edges):
    certificate = json.loads((repository /
        "hadwiger_nelson_heule516_single_point_h632_closure/certificate.json").read_text())
    h560 = set(json.loads((repository /
        "hadwiger_nelson_heule632_minimize/certificate.json").read_text())["retained"])
    label_set = set(labels)
    outside = set(range(632)) - h560
    need(certificate["base_vertices"] == labels and
         certificate["outside_points"] == sorted(outside), "h3991 exact family")
    need(len(h560 - label_set) == 44 and len(outside) == 72, "H632 partition")
    decoded, deletion_edge_checks = decode_deletion_rows(
        certificate["deletion_rows"], labels, base_edges)
    coverage = {point: set() for point in outside}
    for point in outside:
        adjacent = adjacency[point] & label_set
        for removed, colouring in decoded:
            if len({colouring[v] for v in adjacent if v != removed}) < 4:
                coverage[point].add(removed)

    host_edges = [(u, v) for u in range(632) for v in adjacency[u] if u < v]
    direct_checks = 0
    direct_rows = certificate["direct_rows"]
    need(direct_rows == sorted(direct_rows, key=lambda row: (row["point"], row["removed"])),
         "direct row order")
    need(len({(row["point"], row["removed"]) for row in direct_rows}) == len(direct_rows),
         "duplicate direct row")
    for row in direct_rows:
        point, removed = row["point"], row["removed"]
        need(point in outside and removed in label_set, "direct row domain")
        order = sorted((label_set - {removed}) | {point})
        colouring = dict(zip(order, unpack(row["colours"], len(order))))
        for u, v in host_edges:
            if u in colouring and v in colouring:
                need(colouring[u] != colouring[v], "monochromatic direct edge")
                direct_checks += 1
        coverage[point].add(removed)
    counts = [len(coverage[q]) for q in sorted(outside)]
    need(min(counts) == 508, "h3991 boundary coverage")
    prior = json.loads((repository /
        "hadwiger_nelson_heule560_target508_review1/result.json").read_text())
    need(prior["all_checks_passed"] is True and prior["verdict"] == "accept"
         and prior["reviewed_artifact_ref"] ==
         "bafkreiapqqcgluwkxod6r667racxwqhrhqpy2bkoy46vlc75abt5esdezi"
         and prior["uncovered"] == 0, "accepted H560 review receipt")
    return {
        "outside_H560_points_directly_checked": 72,
        "inside_H560_points_imported_from_accepted_closure": 44,
        "minimum_covered_deletions_outside_H560": min(counts),
        "maximum_covered_deletions_outside_H560": max(counts),
        "coverage_histogram_outside_H560": dict(sorted(Counter(counts).items())),
        "deletion_rows": len(certificate["deletion_rows"]),
        "direct_rows": len(direct_rows),
        "deletion_edge_checks": deletion_edge_checks,
        "direct_edge_checks": direct_checks,
        "imported_H560_review_ref": H560_REVIEW_REF,
        "imported_H560_review_result_sha256": EXPECTED_HASHES[
            "hadwiger_nelson_heule560_target508_review1/result.json"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--author-work", type=Path, required=True)
    parser.add_argument("--third-filter", type=Path, required=True)
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    repository = args.repository.resolve()
    source, host, labels, base = load_inputs(repository)
    adjacency, base_edges = exact_graph(host, labels, base, source)
    rows, exterior, degree_histogram, denominator_histogram, filter_receipt = check_centres(
        base, labels, set(host), args.author_work.resolve(), args.third_filter,
        args.scratch.resolve())
    exterior_result = exterior_cover(repository, source, labels, base_edges, exterior)
    boundary_result = boundary_cover(repository, labels, adjacency, base_edges)
    result = {
        "status": "INDEPENDENT_ACCEPT_CHECK_PASSED",
        "reviewed_artifact_ref": REVIEWED_REF,
        "reviewed_commit": REVIEWED_COMMIT,
        "scope": "fixed Heule 516-point placement plus one arbitrary plane point, through order 508",
        "record_improvement": False,
        "geometry": {
            "base_vertices": 516,
            "base_edges": len(base_edges),
            "base_pairs_checked": comb(516, 2),
            "base_triples_enumerated_by_independent_filter": filter_receipt["triples"],
            "independent_filter": filter_receipt,
            "exact_centres": len(rows),
            "exact_centre_base_incidence_checks": len(rows) * 516,
            "centre_denominator_histogram": dict(sorted(denominator_histogram.items())),
            "exterior_degree_histogram": dict(sorted(degree_histogram.items())),
            "independent_survivor_sha256":
                "23f9790bff3809086d28d7ef983b56bb8cb7944c25d4e1fd9a7a6157414baa11",
        },
        "exterior_cover": exterior_result,
        "H632_boundary": boundary_result,
        "logical_implication": {
            "low_degree_case": "at most three neighbours leaves an available fourth colour",
            "high_degree_completeness": "three distinct unit neighbours determine the unique circumcentre; every exact triple survives both new ring evaluations",
            "pigeonhole_case": "a 508-vertex target containing q omits at least nine base vertices while at most eight are uncovered",
        },
        "trust_boundary": "pinned published coordinates and witness bytes; exact CPython integer/Fraction and Base64 semantics; independently compiled C++20 exhaustive loop; compiler, OS, and hardware; prior accepted fixed-H560 closure for 44 boundary points",
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
