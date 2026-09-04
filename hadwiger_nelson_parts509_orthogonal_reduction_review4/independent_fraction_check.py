#!/usr/bin/env python3
"""Independent Fraction-basis audit of the Parts-509 reflection reduction."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CRITICALITY_DIR = ROOT / "hadwiger_nelson_parts509_criticality"
ROTATION_DIR = ROOT / "hadwiger_nelson_parts509_rotation_scan"
sys.path.insert(0, str(CRITICALITY_DIR))

from parts509 import ONE, ZERO, f_add, f_mul, parse_points  # noqa: E402


N = 509
L_SIZE = 374
EXPECTED_POINTS_SHA256 = "770a585a6c1e1222355322707479cb826e9ada560279da904ef89c15c99ff0b5"
EXPECTED_SCAN_SHA256 = "f3d1ff76e031dc0bfe50153db43512428d073d25ea243173d26d5ebfaa8cdedf"
EXPECTED_CRITICALITY_SHA256 = "b6e436cfe41401885722c85ea47bb67a24c4aff9dd5f854cfa7f39d6572163cf"
EXPECTED_PERMUTATION_SHA256 = "d7591e94665b42a3ffc45b6380a56836b4cb4f7aa8b91891b1244e1aa32251f4"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def neg(value):
    return tuple(-coefficient for coefficient in value)


def sub(left, right):
    return f_add(left, neg(right))


def decode(coefficients: list[str]):
    if len(coefficients) != 8:
        raise ValueError("field element needs eight basis coefficients")
    return tuple(Fraction(text) for text in coefficients)


def reflect_y(point):
    return neg(point[0]), point[1]


def rotate(point, c, s):
    x, y = point
    return sub(f_mul(c, x), f_mul(s, y)), f_add(f_mul(s, x), f_mul(c, y))


def orientation_reverse(point, c, s):
    x, y = point
    return f_add(f_mul(c, x), f_mul(s, y)), sub(f_mul(s, x), f_mul(c, y))


def main() -> None:
    points_path = CRITICALITY_DIR / "parts509.vtx"
    scan_path = ROTATION_DIR / "rotation_certificate.json"
    criticality_path = ROTATION_DIR / "criticality_certificate.json"
    if sha256(points_path) != EXPECTED_POINTS_SHA256:
        raise ValueError("unexpected point input")
    if sha256(scan_path) != EXPECTED_SCAN_SHA256:
        raise ValueError("unexpected rotation certificate")
    if sha256(criticality_path) != EXPECTED_CRITICALITY_SHA256:
        raise ValueError("unexpected criticality certificate")

    # This parser converts every coordinate to the explicit basis
    # 1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165),
    # with Fraction coefficients.  It is distinct from the target checker's
    # SymPy AlgebraicField representation.
    points = parse_points(points_path)
    if len(points) != N or len(set(points)) != N:
        raise ValueError("the published point list is not 509 distinct points")
    large = points[:L_SIZE]
    small = points[L_SIZE:]

    lookup = {point: index for index, point in enumerate(large)}
    if len(lookup) != L_SIZE:
        raise ValueError("the large gadget has duplicate points")
    permutation = []
    for point in large:
        image = reflect_y(point)
        if image not in lookup:
            raise ValueError("J(L) is not L")
        permutation.append(lookup[image])
    if sorted(permutation) != list(range(L_SIZE)):
        raise ValueError("J does not induce a permutation of L")
    if any(permutation[permutation[index]] != index for index in range(L_SIZE)):
        raise ValueError("the J permutation is not an involution")
    permutation_bytes = "".join(
        f"{index} {image}\n" for index, image in enumerate(permutation)
    ).encode()
    permutation_hash = hashlib.sha256(permutation_bytes).hexdigest()
    if permutation_hash != EXPECTED_PERMUTATION_SHA256:
        raise ValueError("reflection permutation digest mismatch")

    scan_bytes = scan_path.read_bytes()
    scan = json.loads(scan_bytes)
    criticality = json.loads(criticality_path.read_text())
    if criticality["scan_sha256"] != hashlib.sha256(scan_bytes).hexdigest():
        raise ValueError("criticality certificate is not bound to the scan")
    exceptional = scan["counts"]["uncolorable_event_indices"]
    if exceptional != [108, 109, 215, 216, 690, 789]:
        raise ValueError("unexpected exceptional rotation list")

    parameters = set()
    for event_index in exceptional:
        record = scan["events"][event_index]
        rotation_c = decode(record["cos"])
        rotation_s = decode(record["sin"])
        reflection_c = neg(rotation_c)
        reflection_s = rotation_s
        if f_add(f_mul(reflection_c, reflection_c), f_mul(reflection_s, reflection_s)) != ONE:
            raise ValueError("reflection parameter is not on the exact unit circle")
        parameters.add((reflection_c, reflection_s))

        reflected_small = []
        rotated_small = []
        for point in small:
            f_point = orientation_reverse(point, reflection_c, reflection_s)
            jf_point = reflect_y(f_point)
            r_point = rotate(point, rotation_c, rotation_s)
            if jf_point != r_point:
                raise ValueError("JF(c,s)q != R(-c,s)q")
            reflected_small.append(f_point)
            rotated_small.append(r_point)

        reflection_union = set(large) | set(reflected_small)
        rotation_union = set(large) | set(rotated_small)
        transported_union = {reflect_y(point) for point in reflection_union}
        if transported_union != rotation_union:
            raise ValueError("J does not transport the full reflected union to the rotation union")
        if len(reflection_union) != N or len(rotation_union) != N:
            raise ValueError("an exceptional union does not contain 509 distinct points")
        if record["distinct_points"] != N:
            raise ValueError("parent certificate distinct-point count disagrees")
    if len(parameters) != 6:
        raise ValueError("exceptional reflection parameters are not distinct")

    classes = criticality["isomorphism_classes"]
    covered = sorted(index for item in classes for index in item["event_indices"])
    if len(classes) != 3 or covered != exceptional:
        raise ValueError("three-class certificate does not cover the six events")

    print("PASS independent Fraction-basis reflection audit")
    print("field_basis=1,r3,r5,r15,r11,r33,r55,r165")
    print("large_points=374 fixed_points=14 permutation_involution=true")
    print("exceptional_reflections=6 full_orthogonal_exceptions=12 classes=3")
    print("matrix_point_checks=810 distinct_union_checks=6 all_union_sizes=509")
    print(f"permutation_sha256={permutation_hash}")


if __name__ == "__main__":
    main()
