#!/usr/bin/env python3
"""Rigorous exact-sign audit of the Parts-509 K-rational rotation census."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
POINT_DIR = ROOT / "hadwiger_nelson_parts509_criticality"
TARGET_DIR = ROOT / "hadwiger_nelson_parts509_rotation_scan"
sys.path.insert(0, str(POINT_DIR))

from parts509 import ONE, ZERO, f_add, f_mul, f_sub, parse_points  # noqa: E402


PRIMES = (3, 5, 11)
L_SIZE = 374
N = 509
EXPECTED_POINTS_SHA256 = "770a585a6c1e1222355322707479cb826e9ada560279da904ef89c15c99ff0b5"
EXPECTED_SCAN_SHA256 = "f3d1ff76e031dc0bfe50153db43512428d073d25ea243173d26d5ebfaa8cdedf"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def neg(value):
    return tuple(-coefficient for coefficient in value)


def scale(value, scalar: Fraction):
    return tuple(scalar * coefficient for coefficient in value)


def mul(left, right, primes=PRIMES):
    """Multiply in the recursive tower Q(sqrt(primes[0]),...)."""
    if not primes:
        return (left[0] * right[0],)
    half = len(left) // 2
    a, b = left[:half], left[half:]
    c, d = right[:half], right[half:]
    lower = primes[:-1]
    real = add(mul(a, c, lower), scale(mul(b, d, lower), Fraction(primes[-1])))
    radical = add(mul(a, d, lower), mul(b, c, lower))
    return real + radical


def inverse(value, primes=PRIMES):
    if not primes:
        if not value[0]:
            raise ZeroDivisionError
        return (1 / value[0],)
    half = len(value) // 2
    a, b = value[:half], value[half:]
    lower = primes[:-1]
    denominator = add(
        mul(a, a, lower),
        scale(mul(b, b, lower), Fraction(-primes[-1])),
    )
    denominator_inverse = inverse(denominator, lower)
    return mul(a, denominator_inverse, lower) + neg(
        mul(b, denominator_inverse, lower)
    )


def divide(left, right, primes=PRIMES):
    return mul(left, inverse(right, primes), primes)


@lru_cache(maxsize=None)
def exact_sign(value, primes=PRIMES) -> int:
    """Return the sign using only exact rational field operations.

    For x=a+b*sqrt(d), equal signs of a and b settle the result.  With
    opposite signs, sign(x)=sign(a)*sign(a^2-d*b^2).  Recursing reaches Q.
    The radical tower has full degree eight, so the opposite-sign comparison
    cannot vanish unless the represented element is zero.
    """
    if not primes:
        return (value[0] > 0) - (value[0] < 0)
    half = len(value) // 2
    a, b = value[:half], value[half:]
    lower = primes[:-1]
    sign_a = exact_sign(a, lower)
    sign_b = exact_sign(b, lower)
    if sign_a == 0:
        return sign_b
    if sign_b == 0 or sign_a == sign_b:
        return sign_a
    comparison = add(
        mul(a, a, lower),
        scale(mul(b, b, lower), Fraction(-primes[-1])),
    )
    sign_comparison = exact_sign(comparison, lower)
    if sign_comparison == 0:
        raise ArithmeticError("unexpected square relation in radical tower")
    return sign_a * sign_comparison


def rational_sqrt(value: Fraction):
    if value < 0:
        return None
    numerator = math.isqrt(value.numerator)
    denominator = math.isqrt(value.denominator)
    if numerator * numerator != value.numerator or denominator * denominator != value.denominator:
        return None
    return Fraction(numerator, denominator)


@lru_cache(maxsize=None)
def square_root_in_tower(value, primes=PRIMES):
    """Return some exact square root in the tower, or None if none exists."""
    if not primes:
        root = rational_sqrt(value[0])
        return None if root is None else (root,)
    half = len(value) // 2
    a, b = value[:half], value[half:]
    lower = primes[:-1]
    zero = (Fraction(0),) * half
    if b == zero:
        root_a = square_root_in_tower(a, lower)
        if root_a is not None:
            candidate = root_a + zero
            if mul(candidate, candidate, primes) == value:
                return candidate
        root_b = square_root_in_tower(scale(a, Fraction(1, primes[-1])), lower)
        if root_b is not None:
            candidate = zero + root_b
            if mul(candidate, candidate, primes) == value:
                return candidate
        return None

    norm = add(
        mul(a, a, lower),
        scale(mul(b, b, lower), Fraction(-primes[-1])),
    )
    norm_root = square_root_in_tower(norm, lower)
    if norm_root is None:
        return None
    for signed_norm_root in (norm_root, neg(norm_root)):
        u_squared = scale(add(a, signed_norm_root), Fraction(1, 2))
        u = square_root_in_tower(u_squared, lower)
        if u is None or u == zero:
            continue
        v = divide(b, scale(u, Fraction(2)), lower)
        candidate = u + v
        if mul(candidate, candidate, primes) == value:
            return candidate
    return None


def nonnegative_square_root(value):
    sign = exact_sign(value)
    if sign < 0:
        return None
    if sign == 0:
        return ZERO
    root = square_root_in_tower(value)
    if root is None:
        return None
    if mul(root, root) != value:
        raise AssertionError("square-root membership returned a false root")
    return neg(root) if exact_sign(root) < 0 else root


def norm2(point):
    return add(mul(point[0], point[0]), mul(point[1], point[1]))


def decode(coefficients):
    if len(coefficients) != 8:
        raise ValueError("field element needs eight coefficients")
    return tuple(Fraction(text) for text in coefficients)


def encode(value):
    return ",".join(str(coefficient) for coefficient in value)


def main() -> None:
    points_path = POINT_DIR / "parts509.vtx"
    scan_path = TARGET_DIR / "rotation_certificate.json"
    if sha256(points_path) != EXPECTED_POINTS_SHA256:
        raise ValueError("unexpected point input")
    if sha256(scan_path) != EXPECTED_SCAN_SHA256:
        raise ValueError("unexpected rotation certificate")
    points = parse_points(points_path)
    if len(points) != N or len(set(points)) != N:
        raise ValueError("expected 509 distinct source points")
    if sum(point == (ZERO, ZERO) for point in points[:L_SIZE]) != 1:
        raise ValueError("expected one origin in L")
    if any(point == (ZERO, ZERO) for point in points[L_SIZE:]):
        raise ValueError("S unexpectedly contains the origin")

    radii = [norm2(point) for point in points]
    root_cache = {}
    events = defaultdict(set)
    invariant = []
    admissible_cross_pairs = 0
    k_rational_cross_pairs = 0
    tangent_cross_pairs = 0

    for u in range(L_SIZE):
        px, py = points[u]
        for v in range(L_SIZE, N):
            qx, qy = points[v]
            if (px, py) == (ZERO, ZERO):
                if radii[v] == ONE:
                    invariant.append((u, v))
                continue
            rp2, rq2 = radii[u], radii[v]
            rhs = scale(f_sub(f_add(rp2, rq2), ONE), Fraction(1, 2))
            rr = f_mul(rp2, rq2)
            discriminant = f_sub(rr, f_mul(rhs, rhs))
            key = (rp2, rq2)
            if key not in root_cache:
                sign = exact_sign(discriminant)
                root_cache[key] = (
                    sign >= 0,
                    nonnegative_square_root(discriminant) if sign >= 0 else None,
                )
            admissible, root = root_cache[key]
            if not admissible:
                continue
            admissible_cross_pairs += 1
            if root is None:
                continue
            k_rational_cross_pairs += 1
            if root == ZERO:
                tangent_cross_pairs += 1
            a = f_add(f_mul(px, qx), f_mul(py, qy))
            b = f_sub(f_mul(py, qx), f_mul(px, qy))
            for signed_root in (root,) if root == ZERO else (root, neg(root)):
                c = divide(f_sub(f_mul(rhs, a), f_mul(b, signed_root)), rr)
                s = divide(f_add(f_mul(rhs, b), f_mul(a, signed_root)), rr)
                if f_add(f_mul(c, c), f_mul(s, s)) != ONE:
                    raise AssertionError("enumerated parameter is not a rotation")
                if f_add(f_mul(a, c), f_mul(b, s)) != rhs:
                    raise AssertionError("enumerated parameter misses its edge equation")
                events[(c, s)].add((u, v))

    stats = {
        "radius_pair_classes": sum(admissible for admissible, _root in root_cache.values()),
        "admissible_cross_pairs": admissible_cross_pairs,
        "k_rational_cross_pairs": k_rational_cross_pairs,
        "tangent_cross_pairs": tangent_cross_pairs,
        "invariant_cross_edges": len(invariant),
        "event_rotations": len(events),
    }
    expected_stats = {
        "radius_pair_classes": 547,
        "admissible_cross_pairs": 37861,
        "k_rational_cross_pairs": 14512,
        "tangent_cross_pairs": 576,
        "invariant_cross_edges": 12,
        "event_rotations": 790,
    }
    if stats != expected_stats:
        raise ValueError(f"rigorous event counts differ: {stats}")

    scan = json.loads(scan_path.read_text())
    certificate_events = {}
    for index, record in enumerate(scan["events"]):
        rotation = (decode(record["cos"]), decode(record["sin"]))
        if rotation in certificate_events:
            raise ValueError("duplicate certificate rotation")
        certificate_events[rotation] = (index, record)
    if set(events) != set(certificate_events):
        raise ValueError("rigorous event set differs from the certificate")
    if sorted(invariant) != [tuple(edge) for edge in scan["invariant_cross_edges"]]:
        raise ValueError("invariant edge list differs")

    transcript = hashlib.sha256()
    for rotation in sorted(events):
        index, record = certificate_events[rotation]
        event_edges = sorted(events[rotation])
        if event_edges != [tuple(edge) for edge in record["event_cross_edges"]]:
            raise ValueError(f"cross-edge list differs at event {index}")
        transcript.update(f"{index}|{encode(rotation[0])}|{encode(rotation[1])}|".encode())
        transcript.update(",".join(f"{u}-{v}" for u, v in event_edges).encode())
        transcript.update(b"\n")

    print("PASS rigorous exact-sign Parts-509 rotation event audit")
    print("field_basis=1,r3,r5,r15,r11,r33,r55,r165")
    print("sign_method=recursive_exact_norm_comparison numerical_sign_calls=0")
    print("admissible_radius_pair_classes=547 admissible_cross_pairs=37861")
    print("k_rational_cross_pairs=14512 tangent_cross_pairs=576")
    print("invariant_cross_edges=12 exact_event_rotations=790")
    print(f"event_transcript_sha256={transcript.hexdigest()}")


if __name__ == "__main__":
    main()
