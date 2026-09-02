#!/usr/bin/env python3
"""Verify the exact reflection-to-rotation reduction for Parts's L/S gadgets.

This checker deliberately does not rerun a SAT solver.  It verifies the new
geometric bridge exactly and binds it to the committed rotation scan and its
criticality certificate.  The rotation theorem itself is checked by the
sibling contribution's independent checker.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ROTATION_DIR = ROOT / "hadwiger_nelson_parts509_rotation_scan"
CRITICALITY_DIR = ROOT / "hadwiger_nelson_parts509_criticality"
sys.path.insert(0, str(ROTATION_DIR))

from independent_check import O, decoded_field, parse_points  # noqa: E402


L_SIZE = 374
N = 509


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--points", type=Path, default=CRITICALITY_DIR / "parts509.vtx"
    )
    parser.add_argument(
        "--rotation-scan", type=Path, default=ROTATION_DIR / "rotation_certificate.json"
    )
    parser.add_argument(
        "--rotation-criticality",
        type=Path,
        default=ROTATION_DIR / "criticality_certificate.json",
    )
    args = parser.parse_args()

    points = parse_points(args.points)
    if len(points) != N:
        raise ValueError(f"expected {N} points")

    # J=diag(-1,1) preserves L pointwise as a set.  Reconstruct the exact
    # label permutation, rather than relying on approximate coordinates.
    lookup = {point: index for index, point in enumerate(points[:L_SIZE])}
    if len(lookup) != L_SIZE:
        raise ValueError("L contains duplicate points")
    permutation = []
    for x, y in points[:L_SIZE]:
        reflected = (-x, y)
        if reflected not in lookup:
            raise ValueError("L is not invariant under y-axis reflection")
        permutation.append(lookup[reflected])
    if sorted(permutation) != list(range(L_SIZE)):
        raise ValueError("reflection labels do not form a permutation")
    if any(permutation[permutation[i]] != i for i in range(L_SIZE)):
        raise ValueError("reflection permutation is not an involution")
    permutation_bytes = "".join(
        f"{i} {j}\n" for i, j in enumerate(permutation)
    ).encode()

    scan_bytes = args.rotation_scan.read_bytes()
    scan = json.loads(scan_bytes)
    criticality = json.loads(args.rotation_criticality.read_text())
    if scan.get("format") != "parts509-k-rational-rotation-scan-v1":
        raise ValueError("rotation scan format mismatch")
    if criticality.get("format") != "parts509-rotation-criticality-v1":
        raise ValueError("rotation criticality format mismatch")
    if criticality.get("scan_sha256") != hashlib.sha256(scan_bytes).hexdigest():
        raise ValueError("criticality certificate is not bound to the supplied scan")

    exceptional_indices = scan["counts"]["uncolorable_event_indices"]
    if len(exceptional_indices) != 6:
        raise ValueError("expected six exceptional rotations")
    exceptional_reflections = []
    for event_index in exceptional_indices:
        record = scan["events"][event_index]
        rotation_c = decoded_field(record["cos"])
        rotation_s = decoded_field(record["sin"])
        reflection_c, reflection_s = -rotation_c, rotation_s
        if reflection_c * reflection_c + reflection_s * reflection_s != O:
            raise ValueError("exceptional reflection is not orthogonal")

        # Check J F(c,s)q = R(-c,s)q on every S point.  Since c=-rotation_c,
        # this is J F(c,s)q = R(rotation_c,rotation_s)q.
        for qx, qy in points[L_SIZE:]:
            fx = reflection_c * qx + reflection_s * qy
            fy = reflection_s * qx - reflection_c * qy
            jfq = (-fx, fy)
            rq = (
                rotation_c * qx - rotation_s * qy,
                rotation_s * qx + rotation_c * qy,
            )
            if jfq != rq:
                raise ValueError("matrix bridge failed")
        exceptional_reflections.append(
            (reflection_c, reflection_s, record["distinct_points"])
        )

    if len(set((c, s) for c, s, _distinct in exceptional_reflections)) != 6:
        raise ValueError("exceptional reflection matrices are not distinct")
    if any(distinct != N for _c, _s, distinct in exceptional_reflections):
        raise ValueError("an exceptional placement has fewer than 509 points")
    classes = criticality.get("isomorphism_classes", [])
    if len(classes) != 3:
        raise ValueError("expected three exceptional isomorphism classes")
    covered = sorted(index for item in classes for index in item["event_indices"])
    if covered != sorted(exceptional_indices):
        raise ValueError("criticality classes do not cover the exceptional rotations")

    print(f"points_sha256={sha256(args.points)}")
    print(f"rotation_scan_sha256={sha256(args.rotation_scan)}")
    print(f"rotation_criticality_sha256={sha256(args.rotation_criticality)}")
    print(
        "L_y_axis_reflection_permutation_sha256="
        f"{hashlib.sha256(permutation_bytes).hexdigest()}"
    )
    print(
        "L_y_axis_reflection_fixed_points="
        f"{sum(i == j for i, j in enumerate(permutation))}"
    )
    print(f"exceptional_reflection_to_rotation_events={exceptional_indices}")
    print("exceptional_reflection_matrices=6")
    print("exceptional_full_orthogonal_matrices=12")
    print("exceptional_isomorphism_classes=3")
    print("all_exceptional_distinct_points=509")
    print("all_checks=true")


if __name__ == "__main__":
    main()
