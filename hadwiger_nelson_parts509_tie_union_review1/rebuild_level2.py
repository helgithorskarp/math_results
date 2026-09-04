#!/usr/bin/env python3
"""Single-process exact rebuild of the P25, P44, and pruned level-2 pools.

The implementation is independent of the contribution's level2_points.py.  It
uses the defining circle-intersection construction and exact arithmetic in the
eight-dimensional multiquadratic basis.  In particular it does not use a float
screen, multiprocessing, ambient edge files, or unpublished scratch data.
"""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path


RADICANDS = (3, 5, 11)
ZERO = (Fraction(0),) * 8
ONE = (Fraction(1),) + (Fraction(0),) * 7
FOUR = (Fraction(4),) + (Fraction(0),) * 7


def add(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(a + b for a, b in zip(left, right))


def sub(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(a - b for a, b in zip(left, right))


def neg(value: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(-coefficient for coefficient in value)


def scale(value: tuple[Fraction, ...], scalar: Fraction | int) -> tuple[Fraction, ...]:
    scalar = Fraction(scalar)
    return tuple(scalar * coefficient for coefficient in value)


def mul(left: tuple[Fraction, ...], right: tuple[Fraction, ...], depth: int = 3) -> tuple[Fraction, ...]:
    answer = [Fraction(0)] * (1 << depth)
    for left_mask, a in enumerate(left):
        if not a:
            continue
        for right_mask, b in enumerate(right):
            if not b:
                continue
            factor = 1
            for bit, radicand in enumerate(RADICANDS[:depth]):
                if (left_mask & right_mask) & (1 << bit):
                    factor *= radicand
            answer[left_mask ^ right_mask] += a * b * factor
    return tuple(answer)


def inverse(value: tuple[Fraction, ...], depth: int = 3) -> tuple[Fraction, ...]:
    if not any(value):
        raise ZeroDivisionError
    if depth == 0:
        return (Fraction(1, 1) / value[0],)
    half = 1 << (depth - 1)
    rational, radical = value[:half], value[half:]
    if not any(radical):
        return inverse(rational, depth - 1) + (Fraction(0),) * half
    norm = sub(
        mul(rational, rational, depth - 1),
        scale(mul(radical, radical, depth - 1), RADICANDS[depth - 1]),
    )
    norm_inverse = inverse(norm, depth - 1)
    conjugate = rational + neg(radical)
    return mul(conjugate, norm_inverse + (Fraction(0),) * half, depth)


def rational_sqrt(value: Fraction) -> Fraction | None:
    from math import isqrt

    if value < 0:
        return None
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if numerator * numerator == value.numerator and denominator * denominator == value.denominator:
        return Fraction(numerator, denominator)
    return None


def field_sqrt(value: tuple[Fraction, ...], depth: int = 3) -> tuple[Fraction, ...] | None:
    """Exact recursive square-root test in a tower of quadratic extensions."""

    if depth == 0:
        root = rational_sqrt(value[0])
        return None if root is None else (root,)
    half = 1 << (depth - 1)
    rational, radical = value[:half], value[half:]
    if not any(radical):
        root = field_sqrt(rational, depth - 1)
        if root is not None:
            return root + (Fraction(0),) * half
        root = field_sqrt(scale(rational, Fraction(1, RADICANDS[depth - 1])), depth - 1)
        return None if root is None else (Fraction(0),) * half + root

    norm = sub(
        mul(rational, rational, depth - 1),
        scale(mul(radical, radical, depth - 1), RADICANDS[depth - 1]),
    )
    norm_root = field_sqrt(norm, depth - 1)
    if norm_root is None:
        return None
    for sign in (1, -1):
        candidate_square = scale(add(rational, scale(norm_root, sign)), Fraction(1, 2))
        if not any(candidate_square):
            continue
        first = field_sqrt(candidate_square, depth - 1)
        if first is None:
            continue
        second = mul(radical, inverse(scale(first, 2), depth - 1), depth - 1)
        root = first + second
        if mul(root, root, depth) == value:
            return root
    return None


def parse_field(values: list[str]) -> tuple[Fraction, ...]:
    return tuple(Fraction(value) for value in values)


def parse_point(row: dict) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    return parse_field(row["x"]), parse_field(row["y"])


def distance_squared(left: tuple, right: tuple) -> tuple[Fraction, ...]:
    dx = sub(left[0], right[0])
    dy = sub(left[1], right[1])
    return add(mul(dx, dx), mul(dy, dy))


def intersections(left: tuple, right: tuple) -> list[tuple]:
    distance = distance_squared(left, right)
    if not any(distance):
        return []
    rho_squared = mul(sub(FOUR, distance), inverse(scale(distance, 4)))
    rho = field_sqrt(rho_squared)
    if rho is None:
        return []
    dx = sub(left[0], right[0])
    dy = sub(left[1], right[1])
    midpoint_x = scale(add(left[0], right[0]), Fraction(1, 2))
    midpoint_y = scale(add(left[1], right[1]), Fraction(1, 2))
    offset_x = mul(rho, neg(dy))
    offset_y = mul(rho, dx)
    return [
        (add(midpoint_x, scale(offset_x, sign)), add(midpoint_y, scale(offset_y, sign)))
        for sign in (1, -1)
    ]


def load_certificate(path: Path) -> dict:
    return json.loads(path.read_text())


def main() -> None:
    parser = argparse.ArgumentParser()
    repo = Path(__file__).resolve().parent.parent
    parser.add_argument("--repo", type=Path, default=repo)
    args = parser.parse_args()
    started = time.monotonic()

    source = args.repo / "hadwiger_nelson_parts509_tie_union_minimum"
    p25_cert = load_certificate(source / "certificate_P25.json")
    p44_cert = load_certificate(source / "certificate_P44.json")
    level2_cert = load_certificate(source / "certificate_L2.json")
    completion = json.loads(
        (args.repo / "hadwiger_nelson_parts509_swap_closure" / "completion_points.json").read_text()
    )["points"]
    swaps = json.loads((args.repo / "hadwiger_nelson_parts509_pair_closure" / "swaps.json").read_text())
    pairs = json.loads(
        (args.repo / "hadwiger_nelson_parts509_pair_replacement_classification" / "certificate.json").read_text()
    )["records"]
    triples = json.loads((source / "tie_results.json").read_text())["results"]

    certified_pairs = [row for row in pairs if row["status"].startswith("certified-not-4-colorable")]
    certified_triples = [
        row for row in triples if row["status"] == "UNSAT" and row.get("drat_trim_verified") is True
    ]
    assert (len(swaps), len(certified_pairs), len(certified_triples)) == (11, 60, 79)
    p25_indices = {509 + row[0] for row in swaps}
    p25_indices.update(509 + q for row in certified_pairs for q in row["A"])
    p25_indices.update(509 + q for row in certified_triples for q in row["A"])
    p44_indices = {509 + row[0] for row in swaps}
    p44_indices.update(509 + q for row in pairs for q in row["A"])
    p44_indices.update(509 + q for row in triples for q in row["A"])
    assert sorted(p25_indices) == p25_cert["pool"] and len(p25_indices) == 25
    assert sorted(p44_indices) == p44_cert["pool"] and len(p44_indices) == 44

    def cert_point(cert: dict, vertex: int) -> tuple:
        x, y = cert["coordinates"][str(vertex)]
        return parse_field(x), parse_field(y)

    for vertex in p44_indices:
        assert cert_point(p44_cert, vertex) == parse_point(completion[vertex - 509])
    print("tie_pools: swaps=11 pairs=60 triples=79 P25=25 P44=44")

    base_labels = list(range(509)) + sorted(p44_indices)
    base = {vertex: cert_point(p44_cert, vertex) for vertex in base_labels}
    all_known = set(base[vertex] for vertex in range(509)) | {parse_point(row) for row in completion}
    assert len(all_known) == 509 + 1158

    generated: dict[tuple, set[int]] = {}
    for anchor in sorted(p44_indices):
        for other in base_labels:
            if other == anchor:
                continue
            for point in intersections(base[anchor], base[other]):
                generated.setdefault(point, set()).update((anchor, other))
    new = {point: neighbours for point, neighbours in generated.items() if point not in all_known}
    raw_level2 = {point for point, neighbours in new.items() if len(neighbours) >= 3}
    histogram = Counter(len(neighbours) for neighbours in new.values())
    assert len(raw_level2) == 141
    print(
        f"level2_generation: generated_new={len(new)} histogram={dict(sorted(histogram.items()))} "
        f"raw_degree_at_least_3={len(raw_level2)} seconds={time.monotonic()-started:.3f}"
    )

    universe = set(base.values()) | raw_level2
    adjacency = {point: set() for point in universe}
    ordered = sorted(universe)
    for index, left in enumerate(ordered):
        for right in ordered[index + 1 :]:
            if distance_squared(left, right) == ONE:
                adjacency[left].add(right)
                adjacency[right].add(left)

    live = set(universe)
    removed = []
    while True:
        low_degree = next((point for point in sorted(live) if len(adjacency[point] & live) <= 3), None)
        if low_degree is None:
            break
        live.remove(low_degree)
        removed.append(low_degree)
    certified_live = {cert_point(level2_cert, vertex) for vertex in level2_cert["vertices"]}
    assert live == certified_live
    assert len(live) == 648 and len(removed) == 46
    assert all(point in raw_level2 for point in removed)
    print(
        f"exact_pruning: initial={len(universe)} removed={len(removed)} surviving={len(live)} "
        f"matches_certificate=true seconds={time.monotonic()-started:.3f}"
    )
    print("all_checks=true")


if __name__ == "__main__":
    main()
