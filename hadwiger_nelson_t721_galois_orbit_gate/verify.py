#!/usr/bin/env python3
"""Reconstruct with the other pinned parser; count closed-set orbits by Burnside."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RADICALS = (1, 2, 3, 6, 5, 10, 15, 30)
ACTIONS = tuple(itertools.product((1, -1), repeat=3))


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def action(point, signs):
    result = []
    for start in (0, 8):
        for i, radicand in enumerate(RADICALS):
            sign = 1
            for prime, choice in zip((2, 3, 5), signs):
                if radicand % prime == 0:
                    sign *= choice
            result.append(point[start + i] * sign)
    return tuple(result)


def burnside(points):
    closed = {action(p, g) for p in points for g in ACTIONS}
    fixed = []
    for g in ACTIONS:
        # Check closure, rather than assuming the generated set is invariant.
        image = {action(p, g) for p in closed}
        if image != closed:
            raise ValueError("not an invariant finite set")
        fixed.append(sum(action(p, g) == p for p in closed))
    if sum(fixed) % 8:
        raise ValueError("nonintegral orbit count")
    return closed, fixed, sum(fixed) // 8


def validate_count(actual, claimed):
    if actual != claimed:
        raise ValueError("orbit count mismatch")


def controls():
    def point(x=(), y=()):
        a = [0] * 16
        for i, v in x:
            a[i] = v
        for i, v in y:
            a[8 + i] = v
        return tuple(a)
    fixtures = [
        ([point()], 1),
        ([point([(0, 1)]), point([(0, -1)])], 2),
        ([point([(1, 1)]), point([(1, -1)])], 1),
        # A single field action must act consistently in both coordinates.
        ([point([(1, 1)], [(1, 1)]), point([(1, 1)], [(1, -1)])], 2),
        # The sign of sqrt(6) is the product of those of sqrt(2), sqrt(3).
        ([point([(1, 1), (2, 1), (3, 1)]),
          point([(1, 1), (2, 1), (3, -1)])], 2),
    ]
    for points, count in fixtures:
        closed, fixed, actual = burnside(points)
        validate_count(actual, count)
        # On small controls compare all pointwise assignments, with repetitions.
        choices = [set(action(p, g) for g in ACTIONS) for p in points]
        minimum = min(len(set(images)) for images in itertools.product(*choices))
        validate_count(minimum, count)
    rejected = 0
    for wrong in (0, 592, 594):
        try:
            validate_count(593, wrong)
        except ValueError:
            rejected += 1
    if rejected != 3:
        raise ValueError("corruption control")
    return {"finite_fixtures": len(fixtures), "false_counts_rejected": rejected}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    pins = json.loads((HERE / "provenance.json").read_text())
    if hashlib.sha256(args.input.read_bytes()).hexdigest() != pins["input_sha256"]:
        raise ValueError("coordinate input identity")
    path = HERE.parent / "hadwiger_nelson_t721_weighted_cover" / "exact.py"
    if hashlib.sha256(path.read_bytes()).hexdigest() != pins["inherited_files"]["exact.py"]:
        raise ValueError("inherited parser identity")
    spec = importlib.util.spec_from_file_location("t721_orbit_verifier_geometry", path)
    geometry = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(geometry)
    points, left, right = geometry.construct(args.input)
    expected = json.loads((HERE / "expected.json").read_text())
    if len(points) != 1441 or len(set(points)) != 1441:
        raise ValueError("distinct source count")
    if digest(points) != expected["source_points_sha256"]:
        raise ValueError("producer and checker source coordinates differ")
    closed, fixed, count = burnside(points)
    if len(closed) != expected["galois_closure_points"]:
        raise ValueError("closure count")
    if digest(sorted(closed)) != expected["galois_closure_sha256"]:
        raise ValueError("producer and checker closures differ")
    validate_count(count, expected["source_orbits"])
    validate_count(count, 593)
    result = {
        "source_points": len(points), "closure_points": len(closed),
        "fixed_point_counts": fixed, "sum_fixed_points": sum(fixed),
        "orbit_count": count, "image_lower_bound": count,
        "target_cap": 508, "cap_excluded": count > 508,
        "controls": controls(), "new_distance_census": False,
        "new_chromatic_certificate": False, "verified": True,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
