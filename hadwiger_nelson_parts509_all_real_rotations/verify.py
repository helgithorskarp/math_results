#!/usr/bin/env python3
"""Solver-free exact verifier for the all-real Parts-509 rotation closure."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

from common import (
    CRITICALITY_CERTIFICATE,
    FORMAT,
    GRAPH_CERTIFICATE,
    POINTS,
    ROTATION_CERTIFICATE,
    ZERO,
    coloring_ok,
    edge_size_histogram,
    enumerate_line_classes,
    f_add,
    f_div,
    f_mul,
    f_scale,
    f_sq,
    file_sha256,
    internal_edges,
    line_digest,
    normalized_line,
    parse_points,
    unpack_coloring,
)


def mq_neg(x):
    return tuple(-a for a in x)


def mq_scale(x, scalar):
    return tuple(scalar * a for a in x)


def mq_mul(x, y, primes=(3, 5, 11)):
    """Recursive multiplication in a multiquadratic tower."""
    if not primes:
        return (x[0] * y[0],)
    half = len(x) // 2
    xa, xb, ya, yb = x[:half], x[half:], y[:half], y[half:]
    lower = primes[:-1]
    real = tuple(
        a + Fraction(primes[-1]) * b
        for a, b in zip(mq_mul(xa, ya, lower), mq_mul(xb, yb, lower))
    )
    radical = tuple(
        a + b for a, b in zip(mq_mul(xa, yb, lower), mq_mul(xb, ya, lower))
    )
    return real + radical


def mq_inv(x, primes=(3, 5, 11)):
    if not primes:
        if not x[0]:
            raise ZeroDivisionError
        return (1 / x[0],)
    half = len(x) // 2
    a, b = x[:half], x[half:]
    lower = primes[:-1]
    denominator = tuple(
        p - Fraction(primes[-1]) * q
        for p, q in zip(mq_mul(a, a, lower), mq_mul(b, b, lower))
    )
    inverse = mq_inv(denominator, lower)
    return mq_mul(a, inverse, lower) + mq_neg(mq_mul(b, inverse, lower))


def rational_sqrt(value: Fraction):
    if value < 0:
        return None
    import math

    numerator = math.isqrt(value.numerator)
    denominator = math.isqrt(value.denominator)
    if numerator * numerator != value.numerator or denominator * denominator != value.denominator:
        return None
    return Fraction(numerator, denominator)


def mq_sqrt(x, primes=(3, 5, 11)):
    """Return some square root in the tower, or None; all checks are exact."""
    if not primes:
        root = rational_sqrt(x[0])
        return None if root is None else (root,)
    half = len(x) // 2
    a, b = x[:half], x[half:]
    lower = primes[:-1]
    zero = (Fraction(0),) * half
    if b == zero:
        root_a = mq_sqrt(a, lower)
        if root_a is not None:
            candidate = root_a + zero
            if mq_mul(candidate, candidate, primes) == x:
                return candidate
        root_b = mq_sqrt(mq_scale(a, Fraction(1, primes[-1])), lower)
        if root_b is not None:
            candidate = zero + root_b
            if mq_mul(candidate, candidate, primes) == x:
                return candidate
        return None
    norm = tuple(
        p - Fraction(primes[-1]) * q
        for p, q in zip(mq_mul(a, a, lower), mq_mul(b, b, lower))
    )
    norm_root = mq_sqrt(norm, lower)
    if norm_root is None:
        return None
    for signed in (norm_root, mq_neg(norm_root)):
        u_squared = tuple((p + q) / 2 for p, q in zip(a, signed))
        u = mq_sqrt(u_squared, lower)
        if u is None or u == zero:
            continue
        two_u_inverse = mq_inv(tuple(2 * value for value in u), lower)
        v = mq_mul(b, two_u_inverse, lower)
        candidate = u + v
        if mq_mul(candidate, candidate, primes) == x:
            return candidate
    return None


def verify(certificate_path: Path) -> None:
    certificate = json.loads(certificate_path.read_text())
    if certificate.get("format") != FORMAT:
        raise ValueError("certificate format mismatch")
    expected_hashes = certificate["source_sha256"]
    for name, path in (
        ("parts509.vtx", POINTS),
        ("parts509_certificate.json", GRAPH_CERTIFICATE),
        ("rotation_certificate.json", ROTATION_CERTIFICATE),
        ("criticality_certificate.json", CRITICALITY_CERTIFICATE),
    ):
        if file_sha256(path) != expected_hashes[name]:
            raise ValueError(f"source hash mismatch: {name}")

    points = parse_points(POINTS)
    classes, discriminants, invariant, stats, radii = enumerate_line_classes(points)
    rotation = json.loads(ROTATION_CERTIFICATE.read_text())
    k_lines_from_prior = set()
    for event in rotation["events"]:
        for u, v in event["event_cross_edges"]:
            k_lines_from_prior.add(normalized_line(points, radii, u, v))

    # Independently classify line-circle intersections by exact square membership.
    square_cache = {}
    k_lines = set()
    nonk = {}
    for key, edges in classes.items():
        discriminant = discriminants[key]
        if discriminant not in square_cache:
            square_cache[discriminant] = mq_sqrt(discriminant) is not None
        if square_cache[discriminant]:
            k_lines.add(key)
        else:
            nonk[key] = edges
    if k_lines != k_lines_from_prior:
        raise ValueError("exact square test disagrees with the prior K-event line set")

    counts = certificate["counts"]
    base_internal = internal_edges(points)
    observed = {
        **stats,
        "L_edges": len([edge for edge in base_internal if edge[1] < 374]),
        "S_edges": len([edge for edge in base_internal if edge[0] >= 374]),
        "k_intersection_line_classes": len(k_lines),
        "nonk_line_classes": len(nonk),
        "nonk_event_rotations": 2 * len(nonk),
        "all_real_event_rotations": rotation["counts"]["event_rotations"] + 2 * len(nonk),
        "nonk_cross_edge_histogram": edge_size_histogram(nonk),
    }
    for key, value in observed.items():
        if counts.get(key) != value:
            raise ValueError(f"count mismatch for {key}: observed {value}")
    if line_digest(nonk) != certificate["nonk_line_key_sha256"]:
        raise ValueError("non-K line-class digest mismatch")

    witnesses = [unpack_coloring(text) for text in certificate["witnesses"]]
    if counts["witnesses"] != len(witnesses):
        raise ValueError("witness count mismatch")
    assignments = certificate["assignments"]
    ordered = sorted(nonk)
    if len(assignments) != len(ordered):
        raise ValueError("assignment count mismatch")
    base = base_internal + invariant
    for index, colors in enumerate(witnesses):
        if not coloring_ok(colors, base):
            raise ValueError(f"witness {index} fails on the rotation-invariant graph")
    usage = [0] * len(witnesses)
    for key, witness_index in zip(ordered, assignments):
        if not isinstance(witness_index, int) or not 0 <= witness_index < len(witnesses):
            raise ValueError("invalid witness assignment")
        if not coloring_ok(witnesses[witness_index], nonk[key]):
            raise ValueError("assigned witness has a monochromatic event edge")
        usage[witness_index] += 1
    if any(count == 0 for count in usage):
        raise ValueError("certificate contains an unused witness")

    print(f"exact_line_classes={len(classes)}")
    print(f"k_intersection_line_classes={len(k_lines)}")
    print(f"nonk_line_classes={len(nonk)}")
    print(f"all_real_event_rotations={observed['all_real_event_rotations']}")
    print(f"nonk_coloring_witnesses={len(witnesses)}")
    print(f"witness_usage_min={min(usage)} witness_usage_max={max(usage)}")
    print("solver_free_all_checks=true")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path, default=Path("certificate.json"))
    args = parser.parse_args()
    verify(args.certificate)


if __name__ == "__main__":
    main()
