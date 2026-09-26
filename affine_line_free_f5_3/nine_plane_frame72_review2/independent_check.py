#!/usr/bin/env python3
"""Independent exact audit of the nine-plane-frame dual and frame lemma.

This checker imports no target code.  It reads only the published spectrum list
and dual certificate, rebuilds the 61-by-463 incidence system in a sparse
representation, and checks the projective frame argument exhaustively.
"""

from collections import Counter
from itertools import combinations, combinations_with_replacement, product
import json
from math import comb
from pathlib import Path


TARGET_COMMIT = "2e42f83c5bf9005239e1272b5a1c27eb4bb137eb"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def determinant(a, b, c):
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    ) % 5


def is_frame(points):
    return len(points) == 4 and all(determinant(*triple) for triple in combinations(points, 3))


def projective_audit():
    vectors = tuple(product(range(5), repeat=3))
    points = tuple(v for v in vectors if any(v) and next(x for x in v if x) == 1)
    require(len(points) == 31, "PG(2,5) point count")
    lines = {
        frozenset(v for v in points if determinant(a, b, v) == 0)
        for a, b in combinations(points, 2)
    }
    require(len(lines) == 31 and {len(line) for line in lines} == {6},
            "PG(2,5) line structure")

    triangles = 0
    containment_checks = 0
    frames = sum(is_frame(four) for four in combinations(points, 4))
    for a, b, c in combinations(points, 3):
        if determinant(a, b, c) == 0:
            continue
        triangles += 1
        line_ab = frozenset(v for v in points if determinant(a, b, v) == 0)
        for p in line_ab - {a, b}:
            for q in points:
                if q in line_ab or q == c:
                    continue
                five = (a, b, c, p, q)
                require(any(is_frame(four) for four in combinations(five, 4)),
                        "five-point containment step has no frame")
                containment_checks += 1

    require(triangles == 3875, "noncollinear triangle count")
    require(containment_checks == 372000, "frame-containment case count")
    # If a frame-free set is noncollinear, take a triangle.  Every fourth point
    # lies on a side.  After choosing P on AB, the audit above forces the whole
    # set into the six-point line AB plus C.  Collinear sets have at most six.
    return {
        "projective_points": len(points),
        "projective_lines": len(lines),
        "projective_frames": frames,
        "projective_triangles": triangles,
        "frame_containment_checks": containment_checks,
        "certified_frame_free_upper_bound": 7,
        "normalized_nonzero_coefficient_planes": 4 * 4 * 5,
    }


def spectrum_rows(path):
    rows = []
    for line in path.read_text().splitlines():
        values = tuple(map(int, line.split()))
        require(len(values) == 7 and values[-1] > 0, "bad spectrum row")
        spectrum = values[:6]
        m, counts = spectrum[0], spectrum[1:]
        require(sum(counts) == 30, "a plane must have 30 affine lines")
        require(sum(k * counts[k] for k in range(5)) == 6 * m,
                "point-line incidence identity failed")
        require(sum(comb(k, 2) * counts[k] for k in range(5)) == comb(m, 2),
                "pair-line incidence identity failed")
        require(not (m <= 11 and counts[4]), "small spectrum has a four-point line")
        rows.append(spectrum)
    require(len(rows) == 70 and len(set(rows)) == 70, "spectrum catalogue size")
    return tuple(rows)


def add(column, name, value):
    if value:
        column[name] = column.get(name, 0) + value


def incidence_columns(spectra):
    columns = []

    for spectrum in spectra:
        m, counts = spectrum[0], spectrum[1:]
        column = {}
        add(column, "planes", 1)
        add(column, "plane_points", m)
        add(column, "plane_pairs", comb(m, 2))
        add(column, f"parallel_size_{m}", 1)
        for k, count in enumerate(counts):
            add(column, f"pencil_{k}_size_{m}", count)
        objective = 3 if m == 8 else 1 if m == 9 else 0
        columns.append(("spectrum", spectrum, column, objective))

    parallel_profiles = tuple(
        profile for profile in combinations_with_replacement(range(8, 17), 5)
        if sum(profile) == 72
    )
    require(len(parallel_profiles) == 18, "parallel-profile count")
    for profile in parallel_profiles:
        column = {"parallel_classes": 1}
        for m, count in Counter(profile).items():
            add(column, f"parallel_size_{m}", -count)
        columns.append(("parallel", profile, column, 0))

    pencil_profiles = []
    for k in range(5):
        for profile in combinations_with_replacement(range(max(8, 5 * k - 8), 17), 6):
            if sum(profile) != 72 + 5 * k:
                continue
            pencil_profiles.append((k, profile))
            column = {"lines": 1, "line_points": k, "line_pairs": comb(k, 2)}
            for m, count in Counter(profile).items():
                add(column, f"pencil_{k}_size_{m}", -count)
            columns.append(("pencil", (k, profile), column, 0))
    require(len(pencil_profiles) == 375, "pencil-profile count")
    require(len(columns) == 463, "incidence-column count")
    return columns


def dual_audit(source):
    spectra = spectrum_rows(source / "low_planes72" / "spectra_expected.txt")
    certificate_path = source / "nine_plane_frame72" / "certificate.json"
    certificate = json.loads(certificate_path.read_text())
    row_names = tuple(certificate["row_names"])
    multipliers = tuple(certificate["multipliers"])
    denominator = certificate["denominator"]
    require(len(row_names) == len(multipliers) == 61, "dual row count")
    require(len(set(row_names)) == 61, "duplicate dual row")
    z = dict(zip(row_names, multipliers))
    expected_names = (
        "planes", "plane_points", "plane_pairs", "parallel_classes",
        *(f"parallel_size_{m}" for m in range(8, 17)),
        *(f"pencil_{k}_size_{m}" for k in range(5) for m in range(8, 17)),
        "lines", "line_points", "line_pairs",
    )
    require(row_names == expected_names, "certificate row order/names")

    columns = incidence_columns(spectra)
    slacks = []
    for kind, identity, column, objective in columns:
        unknown = set(column) - set(z)
        require(not unknown, f"unknown rows in {kind} {identity}: {unknown}")
        lhs = sum(z[name] * value for name, value in column.items())
        slacks.append(denominator * objective - lhs)
    require(min(slacks) >= 0, "dual column inequality failed")

    rhs = {
        "planes": 155,
        "plane_points": 72 * 31,
        "plane_pairs": comb(72, 2) * 6,
        "parallel_classes": 31,
        "lines": 775,
        "line_points": 72 * 31,
        "line_pairs": comb(72, 2),
    }
    numerator = sum(z[name] * value for name, value in rhs.items())
    require(numerator == certificate["bound_numerator"], "dual numerator mismatch")
    require(numerator > 10 * denominator and numerator <= 11 * denominator,
            "wrong integer consequence")
    require(min(slacks) == certificate["minimum_slack"], "minimum slack mismatch")
    return {
        "spectra": len(spectra),
        "spectra_incidence_identities": len(spectra),
        "incidence_rows": len(row_names),
        "incidence_columns": len(columns),
        "minimum_dual_slack": min(slacks),
        "zero_slack_columns": sum(slack == 0 for slack in slacks),
        "bound_numerator": numerator,
        "bound_denominator": denominator,
        "weighted_integer_lower_bound": 11,
    }


def main():
    here = Path(__file__).resolve().parent
    source = here.parent
    result = {
        "target_commit": TARGET_COMMIT,
        **dual_audit(source),
        **projective_audit(),
        "status": "PASS",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
