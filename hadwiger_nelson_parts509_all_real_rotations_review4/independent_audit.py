#!/usr/bin/env python3
"""Standard-library audit of the all-real Parts-509 rotation closure.

This checker uses the integer-basis ``points.tsv`` source rather than the
submitted expression parser.  Field inversion is by the product of Galois
conjugates, sign is decided recursively by exact relative norms, and event
line classes are regenerated without importing any submitted Python module.
"""

from __future__ import annotations

import base64
import hashlib
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path


RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
RADICAND_INDEX = {value: index for index, value in enumerate(RADICANDS)}
PRIMES = (3, 5, 11)
ZERO = (Fraction(0),) * 8
ONE = (Fraction(1),) + (Fraction(0),) * 7
N = 509
L_SIZE = 374
SCALE = 96

EXPECTED_POINTS_SHA256 = "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50"
EXPECTED_CERTIFICATE_SHA256 = "3f1a89021f43050341c828a3f8dbe9312c9a69f1595f3006d0b3839f88a35488"
EXPECTED_ROTATION_SHA256 = "f3d1ff76e031dc0bfe50153db43512428d073d25ea243173d26d5ebfaa8cdedf"
EXPECTED_BASE_EDGE_SHA256 = "5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c"
EXPECTED_NONK_LINE_SHA256 = "177f4d60807054ad5216dd19ae1467cf8fd4040a5995b11811975fbaa55865bf"


Element = tuple[Fraction, ...]
Point = tuple[Element, Element]
Line = tuple[Element, Element, Element]
Edge = tuple[int, int]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(left: Element, right: Element) -> Element:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def neg(value: Element) -> Element:
    return tuple(-coefficient for coefficient in value)


def scale(value: Element, multiplier: Fraction) -> Element:
    return tuple(multiplier * coefficient for coefficient in value)


def multiply(left: Element, right: Element) -> Element:
    result = [Fraction(0)] * 8
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if not b:
                continue
            common = math.gcd(RADICANDS[i], RADICANDS[j])
            reduced = RADICANDS[i] * RADICANDS[j] // (common * common)
            result[RADICAND_INDEX[reduced]] += a * b * common
    return tuple(result)


def conjugate(value: Element, sign_mask: int) -> Element:
    return tuple(
        -coefficient if (basis_mask & sign_mask).bit_count() % 2 else coefficient
        for basis_mask, coefficient in enumerate(value)
    )


def inverse(value: Element) -> Element:
    if value == ZERO:
        raise ZeroDivisionError
    numerator = ONE
    for sign_mask in range(1, 8):
        numerator = multiply(numerator, conjugate(value, sign_mask))
    denominator = multiply(value, numerator)
    if any(denominator[1:]) or not denominator[0]:
        raise AssertionError("Galois norm is not nonzero rational")
    result = scale(numerator, 1 / denominator[0])
    if multiply(value, result) != ONE:
        raise AssertionError("field inversion failed")
    return result


def tower_multiply(left: tuple[Fraction, ...], right: tuple[Fraction, ...], primes=PRIMES):
    if not primes:
        return (left[0] * right[0],)
    half = len(left) // 2
    a, b = left[:half], left[half:]
    c, d = right[:half], right[half:]
    lower = primes[:-1]
    rational = tuple(
        x + primes[-1] * y
        for x, y in zip(tower_multiply(a, c, lower), tower_multiply(b, d, lower), strict=True)
    )
    radical = tuple(
        x + y
        for x, y in zip(tower_multiply(a, d, lower), tower_multiply(b, c, lower), strict=True)
    )
    return rational + radical


def exact_sign(value: tuple[Fraction, ...], primes=PRIMES) -> int:
    """Sign in the positive real embedding, by recursive norm comparison."""
    if not primes:
        return (value[0] > 0) - (value[0] < 0)
    half = len(value) // 2
    a, b = value[:half], value[half:]
    sign_a = exact_sign(a, primes[:-1])
    sign_b = exact_sign(b, primes[:-1])
    if sign_b == 0:
        return sign_a
    if sign_a == 0 or sign_a == sign_b:
        return sign_b
    relative_norm = tuple(
        x - primes[-1] * y
        for x, y in zip(
            tower_multiply(a, a, primes[:-1]),
            tower_multiply(b, b, primes[:-1]),
            strict=True,
        )
    )
    norm_sign = exact_sign(relative_norm, primes[:-1])
    if norm_sign == 0:
        raise AssertionError("zero relative norm in a proper quadratic extension")
    return sign_a * norm_sign


def read_points(path: Path) -> list[Point]:
    if file_sha256(path) != EXPECTED_POINTS_SHA256:
        raise ValueError("unexpected integer-basis point source")
    result = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        if len(row) != 16:
            raise ValueError("point row does not have sixteen coefficients")
        result.append((
            tuple(Fraction(value, SCALE) for value in row[:8]),
            tuple(Fraction(value, SCALE) for value in row[8:]),
        ))
    if len(result) != N or len(set(result)) != N:
        raise AssertionError("unexpected point census")
    return result


def norm2(point: Point) -> Element:
    return add(multiply(point[0], point[0]), multiply(point[1], point[1]))


def line_for(points: list[Point], radii: list[Element], u: int, v: int) -> Line:
    p_x, p_y = points[u]
    q_x, q_y = points[v]
    a = add(multiply(p_x, q_x), multiply(p_y, q_y))
    b = add(multiply(p_y, q_x), neg(multiply(p_x, q_y)))
    rhs = scale(add(add(radii[u], radii[v]), neg(ONE)), Fraction(1, 2))
    lead = a if a != ZERO else b
    if lead == ZERO:
        raise AssertionError("non-origin pair has no event line")
    reciprocal = inverse(lead)
    return tuple(multiply(coefficient, reciprocal) for coefficient in (a, b, rhs))  # type: ignore[return-value]


def enumerate_lines(points: list[Point]):
    radii = [norm2(point) for point in points]
    radius_sign: dict[tuple[Element, Element], int] = {}
    lines: dict[Line, list[Edge]] = defaultdict(list)
    discriminants: dict[Line, Element] = {}
    invariant = []
    admissible = tangencies = 0
    for u in range(L_SIZE):
        for v in range(L_SIZE, N):
            if points[u] == (ZERO, ZERO):
                if radii[v] == ONE:
                    invariant.append((u, v))
                continue
            rr = multiply(radii[u], radii[v])
            if rr == ZERO:
                raise AssertionError("zero-radius S point")
            rhs = scale(add(add(radii[u], radii[v]), neg(ONE)), Fraction(1, 2))
            delta = add(rr, neg(multiply(rhs, rhs)))
            radius_key = radii[u], radii[v]
            if radius_key not in radius_sign:
                radius_sign[radius_key] = exact_sign(delta)
            sign = radius_sign[radius_key]
            if sign < 0:
                continue
            admissible += 1
            tangencies += int(sign == 0)
            key = line_for(points, radii, u, v)
            lines[key].append((u, v))
            discriminants.setdefault(key, delta)
    return (
        {key: sorted(value) for key, value in lines.items()},
        discriminants,
        sorted(invariant),
        radii,
        {
            "radius_classes": len(radius_sign),
            "admissible_radius_classes": sum(sign >= 0 for sign in radius_sign.values()),
            "admissible_pairs": admissible,
            "tangent_pairs": tangencies,
        },
    )


def encode_fraction(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def line_digest(keys) -> str:
    result = hashlib.sha256()
    for key in sorted(keys):
        encoded = [[encode_fraction(value) for value in coefficient] for coefficient in key]
        result.update(json.dumps(encoded, separators=(",", ":")).encode("ascii"))
        result.update(b"\n")
    return result.hexdigest()


def unit_edges(points: list[Point]) -> list[Edge]:
    result = []
    for u in range(N):
        for v in range(u + 1, N):
            dx = add(points[u][0], neg(points[v][0]))
            dy = add(points[u][1], neg(points[v][1]))
            if add(multiply(dx, dx), multiply(dy, dy)) == ONE:
                result.append((u, v))
    return result


def edge_digest(edge_list: list[Edge]) -> str:
    raw = "".join(f"{u} {v}\n" for u, v in edge_list).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def unpack_coloring(text: str) -> list[int]:
    raw = base64.b64decode(text, validate=True)
    if len(raw) != (N + 3) // 4 or raw[-1] >> 2:
        raise ValueError("malformed packed coloring")
    return [(raw[i // 4] >> (2 * (i % 4))) & 3 for i in range(N)]


def self_tests() -> None:
    value = (Fraction(2), Fraction(1), Fraction(-1, 3)) + (Fraction(0),) * 5
    if multiply(value, inverse(value)) != ONE:
        raise AssertionError("inverse self-test failed")
    sqrt3_minus_17_over_10 = (Fraction(-17, 10), Fraction(1)) + (Fraction(0),) * 6
    if exact_sign(sqrt3_minus_17_over_10) != 1:
        raise AssertionError("sign self-test failed")
    raw = (value, ONE, add(value, ONE))
    scalar = add(ONE, (Fraction(0), Fraction(0), Fraction(1)) + (Fraction(0),) * 5)
    scaled = tuple(multiply(coefficient, scalar) for coefficient in raw)
    def normalize(line: Line) -> Line:
        lead = next(coefficient for coefficient in line if coefficient != ZERO)
        reciprocal = inverse(lead)
        return tuple(multiply(coefficient, reciprocal) for coefficient in line)  # type: ignore[return-value]
    if normalize(raw) != normalize(scaled):
        raise AssertionError("projective normalization self-test failed")


def main() -> None:
    self_tests()
    here = Path(__file__).resolve().parent
    root = here.parent
    points_path = root / "hadwiger_nelson_parts509_completion_census_degree9" / "points.tsv"
    certificate_path = root / "hadwiger_nelson_parts509_all_real_rotations" / "certificate.json"
    rotation_path = root / "hadwiger_nelson_parts509_rotation_scan" / "rotation_certificate.json"
    if file_sha256(certificate_path) != EXPECTED_CERTIFICATE_SHA256:
        raise ValueError("unexpected all-real certificate")
    if file_sha256(rotation_path) != EXPECTED_ROTATION_SHA256:
        raise ValueError("unexpected K-rotation certificate")
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    rotation = json.loads(rotation_path.read_text(encoding="utf-8"))
    points = read_points(points_path)
    lines, discriminants, invariant, radii, stats = enumerate_lines(points)

    k_lines = set()
    for event in rotation["events"]:
        for u, v in event["event_cross_edges"]:
            key = line_for(points, radii, u, v)
            if (u, v) not in lines[key]:
                raise AssertionError("K-event edge is absent from the all-real census")
            k_lines.add(key)
    if len(k_lines) != 2167 or not k_lines <= set(lines):
        raise AssertionError("unexpected K-intersection line set")
    nonk = {key: value for key, value in lines.items() if key not in k_lines}
    if any(exact_sign(discriminants[key]) <= 0 for key in nonk):
        raise AssertionError("a non-K line is tangent or has no real intersection")
    if len(lines) != 9024 or len(nonk) != 6857:
        raise AssertionError("unexpected line-class split")
    if line_digest(nonk) != EXPECTED_NONK_LINE_SHA256:
        raise AssertionError("non-K line transcript mismatch")

    strict = unit_edges(points)
    if len(strict) != 2442 or edge_digest(strict) != EXPECTED_BASE_EDGE_SHA256:
        raise AssertionError("unexpected strict Parts graph")
    internal = [edge for edge in strict if edge[1] < L_SIZE or edge[0] >= L_SIZE]
    if len(internal) != 2412 or len(invariant) != 12:
        raise AssertionError("unexpected rotation-invariant edge set")
    base = internal + invariant

    witnesses = [unpack_coloring(text) for text in certificate["witnesses"]]
    assignments = certificate["assignments"]
    ordered = sorted(nonk)
    if len(witnesses) != 55 or len(assignments) != len(ordered):
        raise AssertionError("unexpected witness library")
    checks = 0
    for colors in witnesses:
        for u, v in base:
            if colors[u] == colors[v]:
                raise AssertionError("witness fails on an invariant edge")
            checks += 1
    usage = [0] * len(witnesses)
    for key, assignment in zip(ordered, assignments, strict=True):
        if not isinstance(assignment, int) or not 0 <= assignment < len(witnesses):
            raise AssertionError("invalid witness assignment")
        colors = witnesses[assignment]
        for u, v in nonk[key]:
            if colors[u] == colors[v]:
                raise AssertionError("witness fails on its event line")
            checks += 1
        usage[assignment] += 1
    if any(count == 0 for count in usage):
        raise AssertionError("unused witness")

    l_points = set(points[:L_SIZE])
    reflected = {(neg(x), y) for x, y in points[:L_SIZE]}
    if reflected != l_points:
        raise AssertionError("L is not invariant under y-axis reflection")
    fixed = sum(x == ZERO for x, _y in points[:L_SIZE])
    histogram = {str(size): count for size, count in sorted(Counter(map(len, nonk.values())).items())}
    if histogram != certificate["counts"]["nonk_cross_edge_histogram"]:
        raise AssertionError("non-K line-size histogram mismatch")

    summary = {
        "admissible_cross_pairs": stats["admissible_pairs"],
        "all_checks": True,
        "all_real_event_rotations": rotation["counts"]["event_rotations"] + 2 * len(nonk),
        "base_edge_sha256": edge_digest(strict),
        "coloring_edge_checks": checks,
        "k_intersection_line_classes": len(k_lines),
        "line_classes": len(lines),
        "nonk_line_key_sha256": line_digest(nonk),
        "nonk_line_classes": len(nonk),
        "reflection_fixed_L_points": fixed,
        "self_tests": True,
        "tangent_cross_pairs": stats["tangent_pairs"],
        "witness_usage_min": min(usage),
        "witness_usage_max": max(usage),
        "witnesses": len(witnesses),
    }
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
