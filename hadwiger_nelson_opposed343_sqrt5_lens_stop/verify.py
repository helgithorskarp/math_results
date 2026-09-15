#!/usr/bin/env python3
"""Exact replay for the squared-distance-16/9 lens layer on opposed S343."""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / "hadwiger_nelson_golomb_opposed_b214_stop"
SOURCE_FILES = {
    "verify.py": "3520b0e61bf1115c237d2c657dac06205eb194a97bd6975fa5c73847686bc00b",
    "certificate.json": "3f6a4a13ead37de71ceb3cd1818d21a9036ea0273e151461fc54d9df1a8c2e19",
    "excluded.rup": "e3f5c84e89d442d9d5ced2246681defdbccc9fa8cf4eeaebdbd78fec7b966e29",
}
RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
SCALE = 144
UNIT_SQUARED = (SCALE * SCALE,) + (0,) * 7
LENS_CENTRE_DISTANCE_SQUARED = (16 * SCALE * SCALE // 9,) + (0,) * 7


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_source():
    for name, expected in SOURCE_FILES.items():
        need(sha256(SOURCE / name) == expected, f"changed source dependency: {name}")
    spec = importlib.util.spec_from_file_location("opposed_b214_source_verify", SOURCE / "verify.py")
    need(spec is not None and spec.loader is not None, "cannot load source verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SOURCE_VERIFY = load_source()


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def subtract(a, b):
    return tuple(x - y for x, y in zip(a, b))


def divide_exact(a, divisor):
    need(divisor > 0 and all(x % divisor == 0 for x in a), "nonintegral exact division")
    return tuple(x // divisor for x in a)


def multiply_raw(a, b):
    """Multiply coefficient vectors; inputs each have implicit denominator SCALE."""
    out = [0] * 8
    for i, x in enumerate(a):
        if not x:
            continue
        for j, y in enumerate(b):
            if not y:
                continue
            common = math.gcd(RADICANDS[i], RADICANDS[j])
            radicand = RADICANDS[i] * RADICANDS[j] // (common * common)
            out[RADICANDS.index(radicand)] += x * y * common
    return tuple(out)


def squared_distance(p, q):
    dx = subtract(p[0], q[0])
    dy = subtract(p[1], q[1])
    xx, yy = multiply_raw(dx, dx), multiply_raw(dy, dy)
    # The raw product has denominator SCALE^2, matching UNIT_SQUARED.
    return add(xx, yy)


def lift_source_coefficient(a):
    """Embed scale-36 basis (1,sqrt3,sqrt11,sqrt33) at scale 144."""
    out = [0] * 8
    for old, new in enumerate((0, 1, 4, 5)):
        out[new] = 4 * a[old]
    return tuple(out)


def lift_source_point(point):
    return lift_source_coefficient(point[0]), lift_source_coefficient(point[1])


def strict_edges(points):
    return tuple((a, b) for a, b in combinations(range(len(points)), 2)
                 if squared_distance(points[a], points[b]) == UNIT_SQUARED)


def stream_hash(rows):
    return hashlib.sha256(("\n".join(rows) + "\n").encode()).hexdigest()


def point_hash(points):
    return stream_hash(" ".join(map(str, x + y)) for x, y in points)


def edge_hash(edges):
    return stream_hash(f"{a} {b}" for a, b in edges)


def pair_hash(pairs):
    return stream_hash(f"{a} {b}" for a, b in pairs)


def separation_counts(vertex_count, edges):
    adjacency = [set() for _ in range(vertex_count)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)

    def components(removed_vertex=None, removed_edge=None):
        seen = set()
        count = 0
        for start in range(vertex_count):
            if start == removed_vertex or start in seen:
                continue
            count += 1
            stack = [start]
            seen.add(start)
            while stack:
                vertex = stack.pop()
                for neighbour in adjacency[vertex]:
                    if neighbour == removed_vertex or neighbour in seen:
                        continue
                    if removed_edge is not None and tuple(sorted((vertex, neighbour))) == removed_edge:
                        continue
                    seen.add(neighbour)
                    stack.append(neighbour)
        return count

    need(components() == 1, "complete support is disconnected")
    articulations = sum(components(removed_vertex=v) > 1 for v in range(vertex_count))
    bridges = sum(components(removed_edge=edge) > 1 for edge in edges)
    return articulations, bridges


def build_source():
    source_b = SOURCE_VERIFY.read_parts(SOURCE_VERIFY.B_SOURCE, SOURCE_VERIFY.B_SHA256)
    golomb = SOURCE_VERIFY.golomb()
    source_points, _ = SOURCE_VERIFY.merge(
        golomb
        + SOURCE_VERIFY.shifted_b(source_b, 0)
        + SOURCE_VERIFY.shifted_b(source_b, 1)
    )
    source_edges = tuple(SOURCE_VERIFY.strict_edges(source_points))
    need((len(source_points), len(source_edges)) == (343, 1782), "wrong S343 source")
    return tuple(lift_source_point(point) for point in source_points), source_edges


def lens_point(p, q, sign):
    """A unit-circle intersection for |p-q|=4/3, sign in {-1,+1}."""
    need(sign in (-1, 1), "lens sign")
    midpoint_x = divide_exact(add(p[0], q[0]), 2)
    midpoint_y = divide_exact(add(p[1], q[1]), 2)
    dx, dy = subtract(q[0], p[0]), subtract(q[1], p[1])
    sqrt5 = (0, 0, SCALE, 0, 0, 0, 0, 0)
    # sqrt(1-(4/3)^2/4)/(4/3) = sqrt(5)/4.
    turn_x = divide_exact(multiply_raw(sqrt5, dy), 4 * SCALE)
    turn_y = divide_exact(multiply_raw(sqrt5, dx), 4 * SCALE)
    if sign == 1:
        return subtract(midpoint_x, turn_x), add(midpoint_y, turn_y)
    return add(midpoint_x, turn_x), subtract(midpoint_y, turn_y)


def build_geometry():
    old_points, old_edges = build_source()
    centre_pairs = tuple(
        (a, b) for a, b in combinations(range(len(old_points)), 2)
        if squared_distance(old_points[a], old_points[b]) == LENS_CENTRE_DISTANCE_SQUARED
    )
    need(len(centre_pairs) == 54, "wrong squared-distance-16/9 pair count")
    positive = tuple(lens_point(old_points[a], old_points[b], 1) for a, b in centre_pairs)
    negative = tuple(lens_point(old_points[a], old_points[b], -1) for a, b in centre_pairs)
    new_points = positive + negative
    need(len(set(new_points)) == 108, "lens collision")
    need(not (set(new_points) & set(old_points)), "lens point collides with S343")
    need(all(any(point[axis][mask] for axis in (0, 1) for mask in (2, 3, 6, 7))
             for point in new_points), "lens point did not leave the source field")

    for point, (a, b) in zip(positive, centre_pairs):
        need(squared_distance(point, old_points[a]) == UNIT_SQUARED, "positive lens edge a")
        need(squared_distance(point, old_points[b]) == UNIT_SQUARED, "positive lens edge b")
    for point, (a, b) in zip(negative, centre_pairs):
        need(squared_distance(point, old_points[a]) == UNIT_SQUARED, "negative lens edge a")
        need(squared_distance(point, old_points[b]) == UNIT_SQUARED, "negative lens edge b")

    points = old_points + new_points
    edges = strict_edges(points)
    need(tuple(edge for edge in edges if edge[1] < 343) == old_edges,
         "S343 induced edge set changed")
    cross_edges = tuple(edge for edge in edges if edge[0] < 343 <= edge[1])
    new_edges = tuple(edge for edge in edges if edge[0] >= 343)
    need((len(points), len(edges), len(cross_edges), len(new_edges)) == (451, 2170, 216, 172),
         "wrong complete support census")
    old_neighbours = {v: [] for v in range(343, 451)}
    for a, b in cross_edges:
        old_neighbours[b].append(a)
    need(all(len(old_neighbours[v]) == 2 for v in old_neighbours),
         "new point does not have exactly two old contacts")
    for offset, pair in enumerate(centre_pairs):
        need(tuple(sorted(old_neighbours[343 + offset])) == pair, "positive defining contacts")
        need(tuple(sorted(old_neighbours[397 + offset])) == pair, "negative defining contacts")

    degrees = [0] * len(points)
    for a, b in edges:
        degrees[a] += 1
        degrees[b] += 1
    articulation_count, bridge_count = separation_counts(len(points), edges)
    need((articulation_count, bridge_count) == (0, 0), "support is separable")
    return {
        "points": points,
        "edges": edges,
        "source_edges": old_edges,
        "centre_pairs": centre_pairs,
        "cross_edges": cross_edges,
        "new_edges": new_edges,
        "degrees": tuple(degrees),
        "articulations": articulation_count,
        "bridges": bridge_count,
    }


def proper(word, vertex_count, edges):
    return (isinstance(word, str) and len(word) == vertex_count
            and set(word) <= set("0123")
            and all(word[a] != word[b] for a, b in edges))


def verify_positive_certificate(certificate, geometry, source_patterns):
    need(certificate.get("schema") == "opposed343-sqrt5-lens-stop-v1", "certificate schema")
    words = certificate.get("words")
    need(isinstance(words, dict) and sorted(words) == source_patterns, "certificate pattern keys")
    digest = hashlib.sha256()
    for pattern in source_patterns:
        word = words[pattern]
        need(proper(word, 451, geometry["edges"]), f"improper word for {pattern}")
        need(word[:10] == pattern, f"wrong Golomb projection for {pattern}")
        digest.update((pattern + " " + word + "\n").encode())
    return len(words), digest.hexdigest()


def build_report(certificate_path=HERE / "certificate.json"):
    source_report = SOURCE_VERIFY.run(SOURCE / "certificate.json", SOURCE / "excluded.rup")
    need(source_report["opposed_b214_relation_patterns"] == 66, "source relation changed")
    source_certificate = json.loads((SOURCE / "certificate.json").read_text())
    source_patterns = source_certificate["surviving_patterns"]
    geometry = build_geometry()
    certificate = json.loads(certificate_path.read_text())
    positive_words, witness_hash = verify_positive_certificate(
        certificate, geometry, source_patterns)
    need(certificate.get("point_sha256") == point_hash(geometry["points"]), "point hash")
    need(certificate.get("edge_sha256") == edge_hash(geometry["edges"]), "edge hash")
    need(certificate.get("centre_pair_sha256") == pair_hash(geometry["centre_pairs"]),
         "centre-pair hash")

    new_degrees = Counter(geometry["degrees"][343:])
    report = {
        "verified": True,
        "status": "EXACT_UNCHANGED_66_PATTERN_RELATION_STOP",
        "record_candidate": False,
        "coordinate_basis": list(RADICANDS),
        "coordinate_scale": SCALE,
        "source_points": 343,
        "source_edges": 1782,
        "source_relation_patterns": 66,
        "lens_centre_distance_squared": "16/9",
        "lens_centre_pairs": len(geometry["centre_pairs"]),
        "new_points": 108,
        "outside_source_field_points": 108,
        "complete_points": len(geometry["points"]),
        "complete_edges": len(geometry["edges"]),
        "old_new_edges": len(geometry["cross_edges"]),
        "new_new_edges": len(geometry["new_edges"]),
        "new_point_degree_histogram": {
            str(degree): count for degree, count in sorted(new_degrees.items())
        },
        "articulation_vertices": geometry["articulations"],
        "bridges": geometry["bridges"],
        "positive_words_checked": positive_words,
        "complete_relation_patterns": positive_words,
        "relation_reduction": 0,
        "chromatic_number": 4,
        "point_sha256": point_hash(geometry["points"]),
        "edge_sha256": edge_hash(geometry["edges"]),
        "centre_pair_sha256": pair_hash(geometry["centre_pairs"]),
        "witness_stream_sha256": witness_hash,
        "source_rup_lemmas_replayed": source_report["rup_lemmas"],
    }
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    report = build_report(args.certificate)
    if args.check_expected:
        need(report == json.loads((HERE / "EXPECTED.json").read_text()),
             "result differs from EXPECTED.json")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
