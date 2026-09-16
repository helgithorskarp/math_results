#!/usr/bin/env python3
"""Independent exact review of one frozen T375--G79--G49 construction.

No executable module from the target or its T375 dependency is imported.  The
review reconstructs the geometry from the four pinned JSON inputs, uses two
finite-field homomorphisms as a complete pair sieve, and exactly confirms every
surviving unit-distance candidate in Q(sqrt(3),sqrt(11),sqrt(247)).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from itertools import product
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE_NAME = "hadwiger_nelson_small_triangle_forcer375"
TARGET_NAME = "hadwiger_nelson_t375_g79_g49_complement_stop"
SOURCE_COMMIT = "f88d7ee5b1d0b5c640750dc287bda159b8775423"
TARGET_COMMIT = "fe8d17ab505eb283244bcacb5ff55e082615f006"
SOURCE_HASHES = {
    "appendix.json": "dd74c3ef0bb3e9cc1c9c32f7ecc703c1d85cacaca6fca97834d162e8c05997fa",
    "certificate.json": "282fd209157b0c327e02451c32a3d2f2dbb40c4ec31e6531bdd3b8316854b28e",
    "g40.json": "df1316f4351859dfe5751a56092ae73dbc5be73bea30813ce5133ebab140449f",
    "g49.json": "1dfb84f8fca02ada017c5d7fc22aa66ac81ba90fd031f4ff94beb002e9b6fdca",
}
TARGET_CERTIFICATE_SHA256 = "976685f3ce556cc1b7d0eb7ab3cc9f2e02e9078ec9fbe0c1c05257bcd7596d73"
TARGET_ARCHITECTURE_SHA256 = "f43e7591dbabaaa66836b8cb9ed91e1abf155a37d906a8d646f18bd5f92dbfde"
SCALE = 4608
RADICANDS = (3, 11, 247)
TERMINAL_ROWS = ((0, 0, 12, 0), (-6, 0, -6, 0), (6, 0, -6, 0))

# Each root is checked at runtime.  Both primes are 3 mod 4, but primality and
# the displayed square-root identities, rather than that derivation, are the
# premises used by the checker.
SIEVES = (
    (10007, (8530, 7439, 1123)),
    (10067, (6075, 2221, 4635)),
)

MOSER_VERTICES = (44, 40, 50, 45, 41, 51, 47)
MOSER_PATTERN_EDGES = (
    (0, 1), (0, 2), (0, 4), (0, 5), (1, 2), (1, 3),
    (2, 3), (3, 6), (4, 5), (4, 6), (5, 6),
)


class ReviewFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewFailure(message)


def read_json(path: Path):
    return json.loads(path.read_text())


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def object_digest(value) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def subtract(left, right):
    return tuple(a - b for a, b in zip(left, right))


def scalar_multiply(value, scalar: int):
    return tuple(scalar * x for x in value)


def basis_product(left, right):
    """Multiply in the square-root basis indexed by three-bit masks."""

    out = [0] * 8
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if not b:
                continue
            factor = 1
            common = i & j
            for bit, radicand in enumerate(RADICANDS):
                if common & (1 << bit):
                    factor *= radicand
            out[i ^ j] += factor * a * b
    return tuple(out)


def multiply_by_root(value, bit: int):
    out = [0] * 8
    for mask, coefficient in enumerate(value):
        if mask & (1 << bit):
            out[mask ^ (1 << bit)] += coefficient * RADICANDS[bit]
        else:
            out[mask | (1 << bit)] += coefficient
    return tuple(out)


def point_from_row(row):
    """Convert paper coordinates to coefficients with denominator SCALE."""

    a, b, c, d = row
    x = (0, 128 * a, 128 * b, 0, 0, 0, 0, 0)
    y = (128 * c, 0, 0, 128 * d, 0, 0, 0, 0)
    return x, y


def point_add(left, right):
    return add(left[0], right[0]), add(left[1], right[1])


def rotate_spindle(point):
    """Multiply x+iy by (119+3*i*sqrt(247))/128 exactly."""

    x, y = point
    new_x_num = subtract(scalar_multiply(x, 119), scalar_multiply(multiply_by_root(y, 2), 3))
    new_y_num = add(scalar_multiply(multiply_by_root(x, 2), 3), scalar_multiply(y, 119))
    need(all(value % 128 == 0 for value in new_x_num + new_y_num),
         "nonintegral spindle rotation")
    return (tuple(value // 128 for value in new_x_num),
            tuple(value // 128 for value in new_y_num))


def final_frame(point):
    """Apply the frozen reflection/translation (x,y) -> (x,2/3-y)."""

    x, y = point
    constant = (3072, 0, 0, 0, 0, 0, 0, 0)
    return x, subtract(constant, y)


def rotate_120(row):
    a, b, c, d = row
    doubled = (-a - c, -b - 3 * d, 3 * a - c, b - d)
    need(all(value % 2 == 0 for value in doubled), "rotation left integer row lattice")
    return tuple(value // 2 for value in doubled)


def reflect_y_axis(row):
    a, b, c, d = row
    return -a, -b, c, d


def reconstruct_host(source_dir: Path):
    for name, expected in SOURCE_HASHES.items():
        need(file_digest(source_dir / name) == expected, "changed source dependency: " + name)

    appendix = read_json(source_dir / "appendix.json")
    need(type(appendix) is list and len(appendix) == 109, "appendix row count")
    orbit = {tuple(row) for row in appendix}
    frontier = list(orbit)
    while frontier:
        row = frontier.pop()
        for image in (rotate_120(row), reflect_y_axis(row)):
            if image not in orbit:
                orbit.add(image)
                frontier.append(image)
    need(len(orbit) == 627 and set(TERMINAL_ROWS) <= orbit, "source orbit")

    reference = list(TERMINAL_ROWS) + sorted(orbit - set(TERMINAL_ROWS))
    source_certificate = read_json(source_dir / "certificate.json")
    retained = source_certificate.get("retained_reference_indices")
    need(type(retained) is list and len(retained) == 375, "retained-index count")
    need(retained == sorted(set(retained)) and retained[:3] == [0, 1, 2],
         "retained-index normalization")
    native_rows = [reference[index] for index in retained]
    need(object_digest(native_rows) == "0bf15083801eb6fa982b04e820aca6c5a16c9b75b2d85b3efd00c53716edb1fe",
         "T375 native-point hash")
    return [point_from_row(row) for row in native_rows], appendix


def reconstruct_geometry(source_dir: Path):
    host, appendix = reconstruct_host(source_dir)
    pins = host[:3]
    g40 = [point_from_row(row) for row in read_json(source_dir / "g40.json")]
    g49 = [point_from_row(row) for row in read_json(source_dir / "g49.json")]
    need(len(g40) == 40 and len(g49) == 49, "component orders")

    anchor = point_from_row((0, 0, 30, -6))
    other_anchor = point_from_row((0, 0, 30, 6))
    need(anchor in g40 and other_anchor in g40, "frozen G40 anchors")
    need(119 * 119 + 9 * 247 == 128 * 128, "unit spindle multiplier")
    rotated = {rotate_spindle(point) for point in g40}
    g79 = set(g40) | rotated
    need(len(g79) == 79 and len(set(g40) & rotated) == 1, "G79 collision count")

    moved49 = [final_frame(point_add(anchor, point)) for point in g49]
    moved79 = {final_frame(point) for point in g79}
    need([moved49[index] for index in (4, 2, 3)] == pins, "receiving pins")
    need(len(moved79 & set(moved49)) == 2, "component overlap")

    complement_set = moved79 | set(moved49)
    complement = pins + sorted(complement_set - set(pins))
    union = host + sorted(complement_set - set(host))
    need(len(complement) == len(set(complement)) == 126, "complement point count")
    need(len(union) == len(set(union)) == 466, "union point count")
    triangle_target = (SCALE * SCALE // 3,) + (0,) * 7
    need(all(exact_norm_coefficients(pins[left], pins[right]) == triangle_target
             for left in range(3) for right in range(left + 1, 3)),
         "marked equilateral triangle")
    return host, complement, union, appendix


def is_prime(number: int) -> bool:
    if number < 2:
        return False
    for divisor in range(2, math.isqrt(number) + 1):
        if number % divisor == 0:
            return False
    return True


def sieve_weights(prime: int, roots):
    need(is_prime(prime) and SCALE % prime, "invalid sieve prime")
    need(all((root * root - radicand) % prime == 0
             for root, radicand in zip(roots, RADICANDS)), "invalid modular square root")
    weights = []
    for mask in range(8):
        value = 1
        for bit, root in enumerate(roots):
            if mask & (1 << bit):
                value = value * root % prime
        weights.append(value)
    return tuple(weights)


def modular_value(coefficients, prime, weights):
    return sum(coefficient * weight for coefficient, weight in zip(coefficients, weights)) % prime


def exact_norm_coefficients(left, right):
    dx = subtract(left[0], right[0])
    dy = subtract(left[1], right[1])
    return add(basis_product(dx, dx), basis_product(dy, dy))


def complete_edges(points):
    """Sieve every unordered pair, then exactly confirm every survivor."""

    evaluations = []
    for prime, roots in SIEVES:
        weights = sieve_weights(prime, roots)
        evaluations.append((
            prime,
            [(modular_value(x, prime, weights), modular_value(y, prime, weights))
             for x, y in points],
        ))

    target = (SCALE * SCALE,) + (0,) * 7
    candidates = []
    for left in range(len(points)):
        for right in range(left + 1, len(points)):
            survives = True
            for prime, values in evaluations:
                dx = values[left][0] - values[right][0]
                dy = values[left][1] - values[right][1]
                if (dx * dx + dy * dy - SCALE * SCALE) % prime:
                    survives = False
                    break
            if survives:
                candidates.append((left, right))

    edges = [pair for pair in candidates if exact_norm_coefficients(points[pair[0]], points[pair[1]]) == target]
    need(len(edges) == len(candidates), "modular collision survived both sieves")
    return edges, len(candidates)


def check_colour_word(word, order, edges):
    need(type(word) is list and len(word) == order, "colour-word length")
    need(all(type(colour) is int and 0 <= colour < 4 for colour in word), "colour-word alphabet")
    need(all(word[left] != word[right] for left, right in edges), "monochromatic strict edge")


def proper_colourings(order, edges, colours):
    count = 0
    for word in product(range(colours), repeat=order):
        if all(word[left] != word[right] for left, right in edges):
            count += 1
    return count


def validate_moser(complement_edges):
    complete = set(complement_edges)
    induced = {
        tuple(sorted((MOSER_VERTICES[left], MOSER_VERTICES[right])))
        for left in range(7) for right in range(left + 1, 7)
        if tuple(sorted((MOSER_VERTICES[left], MOSER_VERTICES[right]))) in complete
    }
    expected = {
        tuple(sorted((MOSER_VERTICES[left], MOSER_VERTICES[right])))
        for left, right in MOSER_PATTERN_EDGES
    }
    need(induced == expected and len(induced) == 11, "induced Moser spindle")
    need(proper_colourings(7, MOSER_PATTERN_EDGES, 3) == 0, "Moser three-colour obstruction")
    need(proper_colourings(7, MOSER_PATTERN_EDGES, 4) > 0, "Moser four-colour witness")
    return sorted(map(list, induced))


def validate_certificate(certificate, host, complement, union, complement_edges, union_edges):
    need(certificate.get("schema") == "hn-t375-g79-g49-one-complement-v1", "certificate schema")
    need(certificate.get("scale") == SCALE, "coordinate scale")
    need(certificate.get("complement_points") == len(complement) == 126, "complement order")
    need(certificate.get("union_points") == len(union) == 466, "union order")
    need(certificate.get("complement_edges") == len(complement_edges) == 346, "complement size")
    need(certificate.get("union_edges") == len(union_edges) == 1966, "union size")

    need(certificate.get("complement_point_sha256") == object_digest(complement), "complement point hash")
    need(certificate.get("union_point_sha256") == object_digest(union), "union point hash")
    need(certificate.get("complement_edge_sha256") == object_digest(complement_edges), "complement edge hash")
    need(certificate.get("union_edge_sha256") == object_digest(union_edges), "union edge hash")

    union_index = {point: index for index, point in enumerate(union)}
    complement_map = [union_index[point] for point in complement]
    need(certificate.get("complement_to_union") == complement_map, "complement embedding")
    overlap_count = len(set(host) & set(complement))
    need(certificate.get("overlap_count") == overlap_count == 35, "host/complement overlap")

    host_edges = [edge for edge in union_edges if edge[1] < 375]
    need(len(host_edges) == 1661, "T375 complete edge count")
    need(object_digest(host_edges) == "0e3d04cf0e0df94e9a7a9adda6677d92db162faf3ab29947dde8e0f52c287660",
         "T375 edge hash")
    inherited = set(host_edges)
    inherited.update(tuple(sorted((complement_map[left], complement_map[right])))
                     for left, right in complement_edges)
    extra = [list(edge) for edge in union_edges if edge not in inherited]
    need(certificate.get("extra_cross_edges") == extra and len(extra) == 47,
         "incidental cross contacts")

    outside = [index for index, point in enumerate(complement)
               if any(point[axis][mask] for axis in (0, 1) for mask in range(4, 8))]
    need(certificate.get("outside_native_field_indices") == outside and len(outside) == 39,
         "native-field support")

    complement_word = certificate.get("complement_colour_word")
    union_word = certificate.get("union_colour_word")
    check_colour_word(complement_word, 126, complement_edges)
    check_colour_word(union_word, 466, union_edges)
    need([union_word[index] for index in complement_map] == complement_word,
         "restricted complement word")
    need(certificate.get("pins") == complement_word[:3] == [0, 0, 3], "pin colours")
    need(certificate.get("record_candidate") is False, "record scope")
    return complement_map, extra, outside


def review(repository: Path):
    source_dir = repository / SOURCE_NAME
    target_dir = repository / TARGET_NAME
    need(file_digest(target_dir / "certificate.json") == TARGET_CERTIFICATE_SHA256,
         "changed target certificate")
    need(file_digest(target_dir / "ARCHITECTURE.json") == TARGET_ARCHITECTURE_SHA256,
         "changed frozen architecture")

    host, complement, union, appendix = reconstruct_geometry(source_dir)
    complement_edges, complement_candidates = complete_edges(complement)
    union_edges, union_candidates = complete_edges(union)
    certificate = read_json(target_dir / "certificate.json")
    complement_map, extra, outside = validate_certificate(
        certificate, host, complement, union, complement_edges, union_edges
    )
    moser_edges = validate_moser(complement_edges)
    need(all(certificate["complement_colour_word"][left] !=
             certificate["complement_colour_word"][right]
             for left, right in map(tuple, moser_edges)), "Moser restriction word")

    return {
        "status": "ACCEPT_AND_STRENGTHEN",
        "source_commit": SOURCE_COMMIT,
        "target_commit": TARGET_COMMIT,
        "appendix_rows": len(appendix),
        "reference_points": 627,
        "host_points": len(host),
        "host_edges": 1661,
        "complement_points": len(complement),
        "complement_edges": len(complement_edges),
        "union_points": len(union),
        "union_edges": len(union_edges),
        "overlap_count": 35,
        "incidental_cross_edges": len(extra),
        "outside_native_field_points": len(outside),
        "modular_candidate_counts": [complement_candidates, union_candidates],
        "sieve_primes": [prime for prime, _ in SIEVES],
        "checked_pin_colours": certificate["pins"],
        "moser_complement_vertices": list(MOSER_VERTICES),
        "moser_induced_edges": len(moser_edges),
        "moser_proper_three_colourings": 0,
        "complement_chromatic_number": 4,
        "union_chromatic_number": 4,
        "record_candidate": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", nargs="?", type=Path, default=HERE.parent)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = review(args.repository.resolve())
    if args.check_expected:
        need(result == read_json(HERE / "EXPECTED.json"), "expected review result")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
