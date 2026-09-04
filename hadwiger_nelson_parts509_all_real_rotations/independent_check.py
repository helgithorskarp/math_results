#!/usr/bin/env python3
"""Independent SymPy-field replay of the all-real rotation certificate."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ROTATION_DIR = ROOT / "hadwiger_nelson_parts509_rotation_scan"
CRITICALITY_DIR = ROOT / "hadwiger_nelson_parts509_criticality"
POINTS = CRITICALITY_DIR / "parts509.vtx"
GRAPH_CERTIFICATE = CRITICALITY_DIR / "certificate.json"
ROTATION_CERTIFICATE = ROTATION_DIR / "rotation_certificate.json"
CRITICALITY_CERTIFICATE = ROTATION_DIR / "criticality_certificate.json"
FORMAT = "parts509-all-real-rotations-v1"
N = 509
L_SIZE = 374

sys.path.insert(0, str(ROTATION_DIR))
import independent_check as prior  # noqa: E402
sys.path.insert(0, str(CRITICALITY_DIR))
import parts509 as base_geometry  # noqa: E402


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def encode_fraction(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def encode_line(key) -> list[list[str]]:
    return [[encode_fraction(value) for value in element] for element in key]


def line_digest(keys) -> str:
    digest = hashlib.sha256()
    for key in sorted(keys):
        digest.update(json.dumps(encode_line(key), separators=(",", ":")).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


@lru_cache(maxsize=None)
def mq_inverse(value):
    return prior.mq_inv(value)


def normalized_line(points, radii, u, v):
    px, py = points[u]
    qx, qy = points[v]
    a = px * qx + py * qy
    b = py * qx - px * qy
    rhs = (radii[u] + radii[v] - prior.O) / 2
    zero = (Fraction(0),) * 8
    raw = tuple(prior.anp_to_multiquadratic(value) for value in (a, b, rhs))
    lead = raw[0] if raw[0] != zero else raw[1]
    if lead == zero:
        raise ValueError("rotation-invariant pair has no event line")
    inverse = mq_inverse(lead)
    return tuple(prior.mq_mul(value, inverse) for value in raw)


def enumerate_classes(points):
    radii = [prior.norm2(point) for point in points]
    classes = defaultdict(list)
    square_by_line = {}
    radius_cache = {}
    invariant = []
    admissible_pairs = tangent_pairs = 0
    for u in range(L_SIZE):
        px, py = points[u]
        for v in range(L_SIZE, N):
            if px == prior.Z and py == prior.Z:
                if radii[v] == prior.O:
                    invariant.append((u, v))
                continue
            rhs = (radii[u] + radii[v] - prior.O) / 2
            discriminant = radii[u] * radii[v] - rhs * rhs
            radius_key = radii[u], radii[v]
            if radius_key not in radius_cache:
                sign = prior.sign(discriminant)
                root = prior.nonnegative_sqrt_in_k(discriminant) if sign >= 0 else None
                radius_cache[radius_key] = sign, root
            sign, root = radius_cache[radius_key]
            if sign < 0:
                continue
            admissible_pairs += 1
            tangent_pairs += int(sign == 0)
            key = normalized_line(points, radii, u, v)
            classes[key].append((u, v))
            square = root is not None
            if key in square_by_line and square_by_line[key] != square:
                raise ValueError("one line has incompatible square classifications")
            square_by_line[key] = square
    stats = {
        "vertices_labeled": N,
        "L_vertices": L_SIZE,
        "S_vertices": N - L_SIZE,
        "cross_radius_pair_classes": len(radius_cache),
        "admissible_radius_pair_classes": sum(sign >= 0 for sign, _root in radius_cache.values()),
        "admissible_cross_pairs": admissible_pairs,
        "tangent_cross_pairs": tangent_pairs,
        "invariant_cross_edges": len(invariant),
        "line_classes": len(classes),
    }
    return {key: sorted(edges) for key, edges in classes.items()}, square_by_line, sorted(invariant), stats


def unpack_coloring(text: str):
    raw = base64.b64decode(text, validate=True)
    if len(raw) != (N + 3) // 4 or raw[-1] >> 2:
        raise ValueError("bad packed colouring")
    return [(raw[index // 4] >> (2 * (index % 4))) & 3 for index in range(N)]


def coloring_ok(colors, edges):
    return all(colors[u] != colors[v] for u, v in edges)


def histogram(classes):
    return {str(size): count for size, count in sorted(Counter(map(len, classes.values())).items())}


def check(path: Path) -> None:
    certificate = json.loads(path.read_text())
    if certificate.get("format") != FORMAT:
        raise ValueError("certificate format mismatch")
    for name, source in (
        ("parts509.vtx", POINTS),
        ("parts509_certificate.json", GRAPH_CERTIFICATE),
        ("rotation_certificate.json", ROTATION_CERTIFICATE),
        ("criticality_certificate.json", CRITICALITY_CERTIFICATE),
    ):
        if certificate["source_sha256"].get(name) != file_sha256(source):
            raise ValueError(f"source hash mismatch: {name}")

    points = prior.parse_points(POINTS)
    classes, square_by_line, invariant, stats = enumerate_classes(points)
    k_lines = {key for key, square in square_by_line.items() if square}
    nonk = {key: classes[key] for key, square in square_by_line.items() if not square}
    rotation = json.loads(ROTATION_CERTIFICATE.read_text())
    observed = {
        **stats,
        "L_edges": 1860,
        "S_edges": 552,
        "k_intersection_line_classes": len(k_lines),
        "nonk_line_classes": len(nonk),
        "nonk_event_rotations": 2 * len(nonk),
        "all_real_event_rotations": rotation["counts"]["event_rotations"] + 2 * len(nonk),
        "nonk_cross_edge_histogram": histogram(nonk),
    }
    for key, value in observed.items():
        if certificate["counts"].get(key) != value:
            raise ValueError(f"independent count mismatch for {key}: {value}")
    if line_digest(nonk) != certificate["nonk_line_key_sha256"]:
        raise ValueError("independent non-K line digest mismatch")

    graph_certificate = json.loads(GRAPH_CERTIFICATE.read_text())
    if graph_certificate.get("coordinate_sha256") != file_sha256(POINTS):
        raise ValueError("prior graph certificate is bound to different coordinates")
    base_points = base_geometry.parse_points(POINTS)
    strict_edges = base_geometry.build_edges(base_points)
    if len(strict_edges) != graph_certificate["edges"]:
        raise ValueError("prior strict-edge count mismatch")
    if base_geometry.edge_sha256(strict_edges) != graph_certificate["edge_sha256"]:
        raise ValueError("prior strict-edge digest mismatch")
    internal = [edge for edge in strict_edges if edge[1] < L_SIZE or edge[0] >= L_SIZE]
    if sum(v < L_SIZE for _u, v in internal) != 1860:
        raise ValueError("L-edge count mismatch")
    if sum(u >= L_SIZE for u, _v in internal) != 552:
        raise ValueError("S-edge count mismatch")
    base = internal + invariant
    witnesses = [unpack_coloring(text) for text in certificate["witnesses"]]
    assignments = certificate["assignments"]
    ordered = sorted(nonk)
    if len(assignments) != len(ordered):
        raise ValueError("assignment count mismatch")
    usage = [0] * len(witnesses)
    for index, colors in enumerate(witnesses):
        if not coloring_ok(colors, base):
            raise ValueError(f"witness {index} fails on the common graph")
    for key, witness_index in zip(ordered, assignments):
        if not isinstance(witness_index, int) or not 0 <= witness_index < len(witnesses):
            raise ValueError("bad witness assignment")
        if not coloring_ok(witnesses[witness_index], nonk[key]):
            raise ValueError("independently reconstructed event edge is monochromatic")
        usage[witness_index] += 1
    if any(value == 0 for value in usage):
        raise ValueError("unused witness")

    # Every L/S coincidence rotation is K-rational by the explicit dot/determinant formula.
    overlaps = prior.enumerate_overlaps(points)

    print(f"independent_line_classes={len(classes)}")
    print(f"independent_nonk_line_classes={len(nonk)}")
    print(f"independent_all_real_event_rotations={observed['all_real_event_rotations']}")
    print(f"independent_coloring_witnesses={len(witnesses)}")
    print(f"independent_coincidence_rotations={len(overlaps)}")
    print("independent_all_checks=true")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path, default=Path("certificate.json"))
    args = parser.parse_args()
    check(args.certificate)


if __name__ == "__main__":
    main()
