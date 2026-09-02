#!/usr/bin/env python3
"""Independent standard-library checker for the Haugland strict edge census.

This implementation reconstructs Q(zeta_84) as Q[x]/Phi_84(x) using tuples
of Fractions.  It does not import SymPy or the primary reconstruction code.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Iterable


DEGREE = 24
# Low-to-high coefficients of Phi_84(x).
MODULUS = (
    1, 0, 1, 0, 0, 0, -1, 0, -1, 0, 0, 0,
    1, 0, 0, 0, -1, 0, -1, 0, 0, 0, 1, 0, 1,
)
Element = tuple[Fraction, ...]
Point = tuple[Element, Element]
PairElement = tuple[Element, Element]
ExtendedPoint = tuple[PairElement, PairElement]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def edge_hash(edges: list[tuple[int, int]]) -> str:
    payload = "".join(f"{u} {v}\n" for u, v in edges).encode()
    return hashlib.sha256(payload).hexdigest()


def element_text(value: Element) -> str:
    return ",".join(
        str(coefficient.numerator)
        if coefficient.denominator == 1
        else f"{coefficient.numerator}/{coefficient.denominator}"
        for coefficient in value
    )


def coordinate_hash(
    points: list[Point] | list[ExtendedPoint], extended: bool
) -> str:
    digest = hashlib.sha256()
    for x, y in points:
        elements = (x[0], x[1], y[0], y[1]) if extended else (x, y)
        digest.update((";".join(element_text(value) for value in elements) + "\n").encode())
    return digest.hexdigest()


def pad(coefficients: Iterable[Fraction | int]) -> Element:
    result = tuple(Fraction(value) for value in coefficients)
    if len(result) > DEGREE:
        raise ValueError("element degree exceeds field degree")
    return result + (Fraction(0),) * (DEGREE - len(result))


ZERO = pad(())
ONE = pad((1,))
ZETA = pad((0, 1))


def add(left: Element, right: Element) -> Element:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def neg(value: Element) -> Element:
    return tuple(-coefficient for coefficient in value)


def sub(left: Element, right: Element) -> Element:
    return tuple(a - b for a, b in zip(left, right, strict=True))


def scale(value: Element, scalar: Fraction | int) -> Element:
    scalar = Fraction(scalar)
    return tuple(scalar * coefficient for coefficient in value)


def multiply(left: Element, right: Element) -> Element:
    product = [Fraction(0)] * (2 * DEGREE - 1)
    left_support = [(i, value) for i, value in enumerate(left) if value]
    right_support = [(i, value) for i, value in enumerate(right) if value]
    for i, a in left_support:
        for j, b in right_support:
            product[i + j] += a * b
    for exponent in range(2 * DEGREE - 2, DEGREE - 1, -1):
        leading = product[exponent]
        if not leading:
            continue
        product[exponent] = 0
        shift = exponent - DEGREE
        for i, coefficient in enumerate(MODULUS[:-1]):
            if coefficient:
                product[shift + i] -= leading * coefficient
    return tuple(product[:DEGREE])


def poly_trim(poly: list[Fraction]) -> list[Fraction]:
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def poly_sub(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    result = left[:] + [Fraction(0)] * max(0, len(right) - len(left))
    for i, value in enumerate(right):
        result[i] -= value
    return poly_trim(result)


def poly_multiply(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    if not left or not right:
        return []
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        if a:
            for j, b in enumerate(right):
                if b:
                    result[i + j] += a * b
    return poly_trim(result)


def poly_divmod(
    numerator: list[Fraction], denominator: list[Fraction]
) -> tuple[list[Fraction], list[Fraction]]:
    numerator = poly_trim(numerator[:])
    denominator = poly_trim(denominator[:])
    if not denominator:
        raise ZeroDivisionError
    if len(numerator) < len(denominator):
        return [], numerator
    quotient = [Fraction(0)] * (len(numerator) - len(denominator) + 1)
    while numerator and len(numerator) >= len(denominator):
        shift = len(numerator) - len(denominator)
        coefficient = numerator[-1] / denominator[-1]
        quotient[shift] = coefficient
        for i, value in enumerate(denominator):
            numerator[shift + i] -= coefficient * value
        poly_trim(numerator)
    return poly_trim(quotient), numerator


def inverse(value: Element) -> Element:
    if value == ZERO:
        raise ZeroDivisionError
    old_r = [Fraction(value) for value in MODULUS]
    r = poly_trim(list(value))
    old_t: list[Fraction] = []
    t = [Fraction(1)]
    while r:
        quotient, remainder = poly_divmod(old_r, r)
        old_r, r = r, remainder
        old_t, t = t, poly_sub(old_t, poly_multiply(quotient, t))
    if len(old_r) != 1:
        raise AssertionError("defining polynomial is not coprime to element")
    candidate = pad(coefficient / old_r[0] for coefficient in old_t)
    if multiply(value, candidate) != ONE:
        raise AssertionError("polynomial inverse check failed")
    return candidate


def power(value: Element, exponent: int) -> Element:
    if exponent < 0:
        return power(inverse(value), -exponent)
    result = ONE
    base = value
    while exponent:
        if exponent & 1:
            result = multiply(result, base)
        base = multiply(base, base)
        exponent >>= 1
    return result


def field_constants() -> tuple[Element, list[Point]]:
    imaginary = power(ZETA, 21)
    inverse_i = neg(imaginary)
    if multiply(imaginary, imaginary) != neg(ONE):
        raise AssertionError("zeta^21 is not a square root of -1")
    sqrt3 = multiply(sub(power(ZETA, 14), power(ZETA, -14)), inverse_i)
    if multiply(sqrt3, sqrt3) != scale(ONE, 3):
        raise AssertionError("sqrt(3) identity failed")

    def sine(exponent: int) -> Element:
        return scale(
            multiply(sub(power(ZETA, exponent), power(ZETA, -exponent)), inverse_i),
            Fraction(1, 2),
        )

    alpha = inverse(sine(12))
    beta = inverse(sine(24))
    base_x = scale(multiply(sqrt3, add(alpha, beta)), Fraction(1, 4))
    base_y = scale(sub(alpha, beta), Fraction(1, 4))
    vectors: list[Point] = []
    for j in range(42):
        rotation = power(ZETA, 2 * j)
        inverse_rotation = power(ZETA, -2 * j)
        cosine = scale(add(rotation, inverse_rotation), Fraction(1, 2))
        sine_value = scale(
            multiply(sub(rotation, inverse_rotation), inverse_i), Fraction(1, 2)
        )
        vectors.append((cosine, sine_value))
        vectors.append(
            (
                sub(multiply(base_x, cosine), multiply(base_y, sine_value)),
                add(multiply(base_x, sine_value), multiply(base_y, cosine)),
            )
        )
    if len(vectors) != 84:
        raise AssertionError("wrong vector count")
    for x, y in vectors:
        if add(multiply(x, x), multiply(y, y)) != ONE:
            raise AssertionError("a generating vector is not unit")
    for j in range(42):
        if vectors[j + 42] != (neg(vectors[j][0]), neg(vectors[j][1])):
            raise AssertionError("antipodal vector identity failed")
    return sqrt3, vectors


def insert_point(point: Point, index: dict[Point, int], points: list[Point]) -> None:
    if point not in index:
        index[point] = len(points)
        points.append(point)


def build_g1(paths: list[list[int]], sqrt3: Element, vectors: list[Point]) -> list[Point]:
    points: list[Point] = []
    index: dict[Point, int] = {}
    origin = (ZERO, ZERO)
    target = (ZERO, sqrt3)
    insert_point(origin, index, points)
    for path in paths:
        point = origin
        for step in path:
            if not 0 <= step < 84:
                raise AssertionError("path step is outside the vector table")
            point = (add(point[0], vectors[step][0]), add(point[1], vectors[step][1]))
            insert_point(point, index, points)
        if point != target:
            raise AssertionError("a path does not end at (0,sqrt(3))")
    return points


def build_g2(g1: list[Point], sqrt3: Element) -> list[Point]:
    points: list[Point] = []
    index: dict[Point, int] = {}
    for copy in (1, 2):
        for x, y in g1:
            if copy == 1:
                point = (
                    sub(scale(add(x, multiply(sqrt3, y)), Fraction(1, 2)), ONE),
                    scale(sub(y, multiply(sqrt3, x)), Fraction(1, 2)),
                )
            else:
                point = (
                    add(scale(sub(x, multiply(sqrt3, y)), Fraction(1, 2)), ONE),
                    scale(add(multiply(sqrt3, x), y), Fraction(1, 2)),
                )
            insert_point(point, index, points)
    return points


def pair_scale(value: PairElement, scalar: Fraction | int) -> PairElement:
    return scale(value[0], scalar), scale(value[1], scalar)


def pair_sub(left: PairElement, right: PairElement) -> PairElement:
    return sub(left[0], right[0]), sub(left[1], right[1])


def pair_square(value: PairElement) -> PairElement:
    a, b = value
    return add(multiply(a, a), scale(multiply(b, b), 5)), scale(multiply(a, b), 2)


def build_g3(g2: list[Point], sqrt3: Element) -> list[ExtendedPoint]:
    points: list[ExtendedPoint] = []
    index: dict[ExtendedPoint, int] = {}
    for copy in (0, 1):
        for x, y in g2:
            if copy == 0:
                point = ((x, ZERO), (y, ZERO))
            else:
                point = (
                    (
                        sub(scale(add(x, ONE), Fraction(7, 8)), ONE),
                        scale(multiply(sqrt3, y), Fraction(-1, 8)),
                    ),
                    (
                        scale(y, Fraction(7, 8)),
                        scale(multiply(sqrt3, add(x, ONE)), Fraction(1, 8)),
                    ),
                )
            if point not in index:
                index[point] = len(points)
                points.append(point)
    return points


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def evaluate(value: Element, prime: int, zeta_image: int) -> int:
    result = 0
    for coefficient in reversed(value):
        denominator = coefficient.denominator
        if denominator % prime == 0:
            raise AssertionError("specialization divides a denominator")
        result = (
            result * zeta_image
            + coefficient.numerator * pow(denominator, -1, prime)
        ) % prime
    return result


def check_specialization(parameters: dict[str, int]) -> None:
    prime = parameters["prime"]
    zeta_image = parameters["zeta_image"]
    sqrt5_image = parameters["sqrt5_image"]
    if not is_prime(prime):
        raise AssertionError("specialization modulus is not prime")
    if pow(zeta_image, 84, prime) != 1:
        raise AssertionError("zeta image is not an 84th root")
    for divisor in (2, 3, 7):
        if pow(zeta_image, 84 // divisor, prime) == 1:
            raise AssertionError("zeta image does not have order 84")
    modulus_value = 0
    for coefficient in reversed(MODULUS):
        modulus_value = (modulus_value * zeta_image + coefficient) % prime
    if modulus_value != 0:
        raise AssertionError("zeta image does not satisfy Phi_84")
    if sqrt5_image * sqrt5_image % prime != 5 % prime:
        raise AssertionError("sqrt(5) image has the wrong square")


def point_images(
    points: list[Point], parameters: dict[str, int]
) -> list[tuple[int, int]]:
    prime = parameters["prime"]
    zeta_image = parameters["zeta_image"]
    return [
        (evaluate(x, prime, zeta_image), evaluate(y, prime, zeta_image))
        for x, y in points
    ]


def extended_images(
    points: list[ExtendedPoint], parameters: dict[str, int]
) -> list[tuple[int, int]]:
    prime = parameters["prime"]
    zeta_image = parameters["zeta_image"]
    sqrt5_image = parameters["sqrt5_image"]

    def pair_image(value: PairElement) -> int:
        return (
            evaluate(value[0], prime, zeta_image)
            + sqrt5_image * evaluate(value[1], prime, zeta_image)
        ) % prime

    return [(pair_image(x), pair_image(y)) for x, y in points]


def sieve_intersection(
    image_tables: list[tuple[int, list[tuple[int, int]]]]
) -> list[tuple[int, int]]:
    vertex_count = len(image_tables[0][1])
    if any(len(images) != vertex_count for _, images in image_tables):
        raise AssertionError("specializations have different vertex counts")
    candidates: list[tuple[int, int]] = []
    for u, v in combinations(range(vertex_count), 2):
        survives = True
        for prime, images in image_tables:
            dx = images[u][0] - images[v][0]
            dy = images[u][1] - images[v][1]
            if (dx * dx + dy * dy - 1) % prime:
                survives = False
                break
        if survives:
            candidates.append((u, v))
    return candidates


def confirm_base(points: list[Point], candidates: list[tuple[int, int]]) -> list[tuple[int, int]]:
    edges: list[tuple[int, int]] = []
    for u, v in candidates:
        dx = sub(points[u][0], points[v][0])
        dy = sub(points[u][1], points[v][1])
        if add(multiply(dx, dx), multiply(dy, dy)) == ONE:
            edges.append((u, v))
    return edges


def confirm_extended(
    points: list[ExtendedPoint], candidates: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    edges: list[tuple[int, int]] = []
    for u, v in candidates:
        dx = pair_sub(points[u][0], points[v][0])
        dy = pair_sub(points[u][1], points[v][1])
        first_x, second_x = pair_square(dx)
        first_y, second_y = pair_square(dy)
        if add(first_x, first_y) == ONE and add(second_x, second_y) == ZERO:
            edges.append((u, v))
    return edges


def certify(
    name: str,
    points: list[Point] | list[ExtendedPoint],
    specializations: list[dict[str, int]],
    extended: bool,
) -> tuple[dict[str, int | str], list[tuple[int, int]]]:
    tables = []
    for parameters in specializations:
        images = (
            extended_images(points, parameters)  # type: ignore[arg-type]
            if extended
            else point_images(points, parameters)  # type: ignore[arg-type]
        )
        tables.append((parameters["prime"], images))
    candidates = sieve_intersection(tables)
    edges = (
        confirm_extended(points, candidates)  # type: ignore[arg-type]
        if extended
        else confirm_base(points, candidates)  # type: ignore[arg-type]
    )
    result: dict[str, int | str] = {
        "vertices": len(points),
        "pairs_checked": len(points) * (len(points) - 1) // 2,
        "sieve_survivors": len(candidates),
        "strict_unit_edges": len(edges),
        "edge_sha256": edge_hash(edges),
        "coordinate_sha256": coordinate_hash(points, extended),
    }
    return result, edges


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()

    certificate = json.loads(args.certificate.read_text())
    if sha256_file(args.graph) != certificate["input_graph_sha256"]:
        raise AssertionError("input graph hash mismatch")
    payload = json.loads(args.graph.read_text())
    paths = payload["paths"]
    if len(paths) != 231 or {len(path) for path in paths} != {5, 6}:
        raise AssertionError("unexpected path table shape")

    sqrt3, vectors = field_constants()
    g1 = build_g1(paths, sqrt3, vectors)
    g2 = build_g2(g1, sqrt3)
    g3 = build_g3(g2, sqrt3)
    if (len(g1), len(g2), len(g3)) != (740, 1066, 2131):
        raise AssertionError("exact point counts differ from the paper")

    specializations = certificate["independent_specializations"]
    for parameters in specializations:
        check_specialization(parameters)
    g1_result, g1_edges = certify("G1", g1, specializations, False)
    g2_result, _ = certify("G2", g2, specializations, False)
    g3_result, g3_edges = certify("G3", g3, specializations, True)
    results = {"G1": g1_result, "G2": g2_result, "G3": g3_result}
    if results != certificate["independent_results"]:
        raise AssertionError(
            "independent results differ from certificate:\n"
            + json.dumps(results, indent=2, sort_keys=True)
        )

    if g1_edges != [tuple(edge) for edge in payload["G1_edges"]]:
        raise AssertionError("independent G1 edge set differs from committed list")
    if g3_edges != [tuple(edge) for edge in payload["G3_edges"]]:
        raise AssertionError("independent G3 edge set differs from committed list")
    for name, result in results.items():
        if list(payload["graph_counts"][name]) != [
            result["vertices"], result["strict_unit_edges"]
        ]:
            raise AssertionError(f"{name} count mismatch")

    summaries = " ".join(
        f"{name}_pairs={result['pairs_checked']} "
        f"{name}_survivors={result['sieve_survivors']} "
        f"{name}_strict_edges={result['strict_unit_edges']} "
        f"{name}_edge_sha256={result['edge_sha256']} "
        f"{name}_coordinate_sha256={result['coordinate_sha256']}"
        for name, result in results.items()
    )
    primes = ",".join(str(item["prime"]) for item in specializations)
    print(f"independent_all_checks=true primes={primes} {summaries}")


if __name__ == "__main__":
    main()
