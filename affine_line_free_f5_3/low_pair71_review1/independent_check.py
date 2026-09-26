#!/usr/bin/env python3
"""Independent exact audit of the 71-point two-low-plane theorem.

No reviewed Python or C++ module is imported.  The planar census uses a new
Gray-code implementation, the incidence system is reconstructed sparsely by
row name, and every published Farkas inequality is checked with Python
integers.  Moment types and the 15-profile cover are regenerated separately.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
import hashlib
from itertools import combinations_with_replacement, product
import json
from math import comb
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "low_pair71"
N = 71
SPECTRUM_SHA256 = "8e65bcf9fab9c6a75a83368e3bef7339f9411f58f0231f4a3cbb10209be94bc9"
CERTIFICATE_SHA256 = "c1c05da8548ddb40f35db3d6cf86f9d353f468b2fd63412b18b27bc3d26833cb"
FORM_COUNTS = {
    "zero": (31, 0, 0),
    "rank1_square": (6, 25, 0),
    "rank1_nonsquare": (6, 0, 25),
    "rank2_split": (11, 10, 10),
    "rank2_anisotropic": (1, 15, 15),
    "rank3_square": (6, 15, 10),
    "rank3_nonsquare": (6, 10, 15),
}
EXPECTED_INTEGER_BOUNDS = {
    "zero": (2, 4),
    "rank1_square": (3, 3),
    "rank1_nonsquare": (2, 2),
    "rank2_split": (2, 2),
    "rank2_anisotropic": (3, 3),
    "rank3_square": (2, 2),
    "rank3_nonsquare": (2, 2),
}
LOW_REPRESENTATIVES = (
    (7, 16, 16, 16, 16),
    (8, 15, 16, 16, 16),
    (9, 14, 16, 16, 16),
    (9, 15, 15, 16, 16),
    (9, 15, 16, 16, 15),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def weak_compositions(total: int, length: int):
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, length - 1):
            yield (first,) + tail


def character(value: int) -> int:
    value %= 5
    return 0 if value == 0 else 1 if value in (1, 4) else -1


def projective_points(dimension: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        vector for vector in product(range(5), repeat=dimension)
        if any(vector) and next(value for value in vector if value) == 1
    )


def run_gray_census(out: Path, cxx: str, sanitize: bool) -> list[tuple[int, ...]]:
    executable = out / "gray_spectra"
    flags = ["-std=c++20", "-Wall", "-Wextra", "-Wpedantic", "-Wconversion"]
    flags += (["-O1", "-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer"]
              if sanitize else ["-O3"])
    subprocess.run([cxx, *flags, str(HERE / "gray_spectra.cpp"), "-o", str(executable)],
                   check=True)
    census = subprocess.check_output([str(executable)])
    require(digest(census) == SPECTRUM_SHA256, "independent spectrum hash mismatch")
    require(census == (TARGET / "spectra_expected.txt").read_bytes(),
            "independent spectrum bytes mismatch")
    records = [tuple(map(int, line.split())) for line in census.decode().splitlines()]
    require(len(records) == 91 and all(len(record) == 7 for record in records),
            "incorrect spectrum records")
    for size, *tail in records:
        counts, multiplicity = tail[:5], tail[5]
        require(multiplicity > 0 and sum(counts) == 30, "bad spectrum multiplicity/count")
        require(sum(k * counts[k] for k in range(5)) == 6 * size,
                "spectrum point-line identity")
        require(sum(comb(k, 2) * counts[k] for k in range(5)) == comb(size, 2),
                "spectrum pair-line identity")
        require(size > 10 or counts[4] == 0, "small spectrum has a four-point line")
    return records


def audit_profiles() -> tuple[list[tuple[tuple[int, ...], int]], dict[str, object]]:
    ordered: set[tuple[tuple[int, ...], int]] = set()
    low_at_zero: set[tuple[int, ...]] = set()
    centered_all: set[tuple[tuple[int, ...], int]] = set()
    for deficits in weak_compositions(9, 5):
        profile = tuple(16 - deficit for deficit in deficits)
        if profile[0] <= 9:
            low_at_zero.add(profile)
        if sum(label * profile[label] for label in range(5)) % 5:
            continue
        q = sum(label * label * profile[label] for label in range(5)) % 5
        centered_all.add((profile, q))
        if q in (0, 1, 2):
            ordered.add((profile, q))
    require(len(ordered) == 85, "incorrect ordered-profile count")
    require(Counter(q for _, q in ordered) == Counter({0: 27, 1: 29, 2: 29}),
            "incorrect ordered-profile character counts")

    # Every centered profile can be put in canonical character 0, 1 or 2 by
    # multiplying its normal by a nonzero field element.
    for profile, q in centered_all:
        images = set()
        for scale in range(1, 5):
            inverse = pow(scale, -1, 5)
            image = tuple(profile[(inverse * label) % 5] for label in range(5))
            image_q = sum(label * label * image[label] for label in range(5)) % 5
            require(image_q == scale * scale * q % 5, "normal-scaling law failed")
            images.add((image, image_q))
        require(images & ordered, "canonical normal scaling is incomplete")

    covered: set[tuple[int, ...]] = set()
    orbit_sizes = []
    for representative in LOW_REPRESENTATIVES:
        orbit = {
            tuple(representative[(pow(scale, -1, 5) * label) % 5]
                  for label in range(5))
            for scale in range(1, 5)
        }
        require(not (covered & orbit), "low-profile scaling orbits overlap")
        covered |= orbit
        orbit_sizes.append(len(orbit))
    require(covered == low_at_zero, "five low-profile representatives are incomplete")

    barycenters = tuple(sum(label * profile[label] for label in range(5)) % 5
                        for profile in LOW_REPRESENTATIVES)
    variances = tuple(
        (sum(label * label * profile[label] for label in range(5)) - mean * mean) % 5
        for profile, mean in zip(LOW_REPRESENTATIVES, barycenters, strict=True)
    )
    require(barycenters == (0, 4, 3, 2, 0), "low-profile barycenters disagree")
    require(variances == (0, 3, 4, 1, 3), "low-profile variances disagree")

    ranges = []
    for first, second in combinations_with_replacement(range(5), 2):
        m = LOW_REPRESENTATIVES[first][0]
        n = LOW_REPRESENTATIVES[second][0]
        fiber_cap = (m + n - 7) // 5
        lower = m + n - 7 - fiber_cap
        upper = m + n - 7
        require(fiber_cap in (1, 2) and upper <= 11, "pair deficit range failed")
        for total in range(lower, upper + 1):
            origin_deficit = 11 - m - n + total
            require(4 - fiber_cap <= origin_deficit <= 4,
                    "origin-deficit reconstruction failed")
        ranges.append(
            f"{first}/{second}: common_fiber_cap={fiber_cap}, T={lower}..{upper}"
        )
    require(len(ranges) == 15, "incorrect normalized pair count")

    # Enumerate quotient lines independently and verify that no line has more
    # than four positions in the 4-by-4 interior, proving the gauge frame.
    interior = set(product(range(1, 5), repeat=2))
    line_intersections = []
    for c in range(5):
        line_intersections.append(sum((c, y) in interior for y in range(5)))
    for slope in range(5):
        for offset in range(5):
            line_intersections.append(sum((x, (slope * x + offset) % 5) in interior
                                          for x in range(5)))
    require(len(line_intersections) == 30 and max(line_intersections) == 4,
            "interior affine-line bound failed")
    return sorted(ordered), {
        "ordered_profiles": len(ordered),
        "ordered_q_counts": {str(q): sum(value == q for _, value in ordered)
                             for q in (0, 1, 2)},
        "low_profiles_at_zero": len(low_at_zero),
        "low_orbit_sizes": orbit_sizes,
        "normalized_pair_types": len(ranges),
        "pair_ranges": ranges,
        "maximum_interior_line_positions": max(line_intersections),
    }


def audit_quadratic_forms() -> dict[str, int]:
    normals = projective_points(3)
    require(len(normals) == 31, "incorrect projective normal count")
    evaluation = tuple((x*x, y*y, z*z, 2*x*y, 2*x*z, 2*y*z)
                       for x, y, z in normals)
    expected = set(FORM_COUNTS.values())
    frequencies: Counter[tuple[int, int, int]] = Counter()
    for coefficients in product(range(5), repeat=6):
        counts = Counter(character(sum(a * b for a, b in zip(coefficients, row, strict=True)))
                         for row in evaluation)
        distribution = tuple(counts[value] for value in (0, 1, -1))
        require(distribution in expected, "unclassified symmetric quadratic form")
        frequencies[distribution] += 1
    require(sum(frequencies.values()) == 5**6 and len(frequencies) == 7,
            "quadratic-form census incomplete")
    result = {name: frequencies[counts] for name, counts in FORM_COUNTS.items()}
    require(result == {
        "zero": 1,
        "rank1_square": 62,
        "rank1_nonsquare": 62,
        "rank2_split": 1860,
        "rank2_anisotropic": 1240,
        "rank3_square": 6200,
        "rank3_nonsquare": 6200,
    }, "quadratic-form frequencies disagree")
    return result


def row_names() -> tuple[str, ...]:
    return (
        "planes", "plane_points", "plane_pairs", "parallel_classes",
        *(f"parallel_{size}" for size in range(7, 17)),
        *(f"pencil_{k}_{size}" for k in range(5) for size in range(7, 17)),
        "lines", "line_points", "line_pairs", "barycenter_star",
        "quadratic_0", "quadratic_1", "quadratic_2",
    )


def add(column: dict[str, int], name: str, value: int) -> None:
    if value:
        column[name] = column.get(name, 0) + value


def sparse_columns(
    spectra: list[tuple[int, ...]],
    profiles: list[tuple[tuple[int, ...], int]],
) -> tuple[list[tuple[dict[str, int], int]], dict[str, int]]:
    columns: list[tuple[dict[str, int], int]] = []
    counts = {"spectra": 0, "profiles": 0, "pencils": 0}
    for record in spectra:
        size, *tail = record
        intersections = tail[:5]
        column: dict[str, int] = {}
        add(column, "planes", 1)
        add(column, "plane_points", size)
        add(column, "plane_pairs", comb(size, 2))
        add(column, f"parallel_{size}", 1)
        for k, number in enumerate(intersections):
            add(column, f"pencil_{k}_{size}", number)
        columns.append((column, int(size <= 9)))
        counts["spectra"] += 1
    for profile, q in profiles:
        column = {"parallel_classes": 1, "barycenter_star": profile[0],
                  f"quadratic_{q}": 1}
        for size, number in Counter(profile).items():
            add(column, f"parallel_{size}", -number)
        columns.append((column, 0))
        counts["profiles"] += 1
    for k in range(5):
        minimum = max(7, 5 * k - 9)
        for pencil in combinations_with_replacement(range(minimum, 17), 6):
            if sum(pencil) != N + 5 * k:
                continue
            column = {"lines": 1}
            add(column, "line_points", k)
            add(column, "line_pairs", comb(k, 2))
            for size, number in Counter(pencil).items():
                add(column, f"pencil_{k}_{size}", -number)
            columns.append((column, 0))
            counts["pencils"] += 1
    require(counts == {"spectra": 91, "profiles": 85, "pencils": 522},
            "sparse column family counts disagree")
    require(len(columns) == 698, "incorrect sparse column total")
    return columns, counts


def rhs(form: str, mu_in_set: int) -> dict[str, int]:
    require(form in FORM_COUNTS and mu_in_set in (0, 1), "invalid certificate case")
    answer = {
        "planes": 155,
        "plane_points": 31 * N,
        "plane_pairs": 6 * comb(N, 2),
        "parallel_classes": 31,
        "lines": 775,
        "line_points": 31 * N,
        "line_pairs": comb(N, 2),
        "barycenter_star": 6 * N + 25 * mu_in_set,
    }
    for q, value in enumerate(FORM_COUNTS[form]):
        answer[f"quadratic_{q}"] = value
    return answer


def verify_certificate_data(
    data: dict[str, object],
    columns: list[tuple[dict[str, int], int]],
) -> tuple[list[dict[str, object]], str]:
    names = row_names()
    require(data.get("schema") == 1 and data.get("row_names") == list(names),
            "certificate schema or rows disagree")
    index = {name: position for position, name in enumerate(names)}
    cases = data.get("cases")
    require(isinstance(cases, list), "certificate cases are not a list")
    expected_cases = {(form, bit) for form in FORM_COUNTS for bit in (0, 1)}
    seen: set[tuple[str, int]] = set()
    records = []
    all_slacks = hashlib.sha256()
    for case in cases:
        require(isinstance(case, dict), "malformed certificate case")
        form, bit = case.get("form"), case.get("mu_in_set")
        require(type(form) is str and type(bit) is int, "bad certificate identifier")
        key = (form, bit)
        require(key in expected_cases and key not in seen, "missing/duplicate/unknown case")
        seen.add(key)
        denominator = case.get("denominator")
        multipliers = case.get("multipliers")
        require(type(denominator) is int and denominator > 0, "nonpositive denominator")
        require(isinstance(multipliers, list) and len(multipliers) == len(names)
                and all(type(value) is int for value in multipliers), "bad multipliers")
        slacks = []
        for column, objective in columns:
            lhs = sum(multipliers[index[name]] * value for name, value in column.items())
            slack = denominator * objective - lhs
            require(slack >= 0, f"dual inequality failed for {form}/{bit}")
            slacks.append(slack)
        right = rhs(form, bit)
        numerator = sum(multipliers[index[name]] * value for name, value in right.items())
        require(type(case.get("numerator")) is int and numerator == case["numerator"],
                "certificate numerator mismatch")
        lower_bound = (numerator + denominator - 1) // denominator
        require(lower_bound == case.get("lower_bound")
                == EXPECTED_INTEGER_BOUNDS[form][bit], "integer lower bound mismatch")
        encoded = json.dumps([form, bit, slacks], separators=(",", ":")).encode("ascii")
        all_slacks.update(len(encoded).to_bytes(4, "big"))
        all_slacks.update(encoded)
        records.append({
            "case": f"{form}/{bit}",
            "rational_bound": str(Fraction(numerator, denominator)),
            "integer_bound": lower_bound,
            "minimum_slack": min(slacks),
            "tight_columns": sum(slack == 0 for slack in slacks),
        })
    require(seen == expected_cases, "incomplete fourteen-case family")
    records.sort(key=lambda record: record["case"])
    return records, all_slacks.hexdigest()


def mutation_controls(
    data: dict[str, object],
    columns: list[tuple[dict[str, int], int]],
) -> dict[str, bool]:
    controls = {}
    changed = deepcopy(data)
    changed["cases"][0]["multipliers"][0] += 1
    missing = deepcopy(data)
    missing["cases"].pop()
    negative = deepcopy(data)
    negative["cases"][0]["denominator"] = -1
    for name, candidate in (("changed_multiplier", changed),
                            ("missing_case", missing),
                            ("negative_denominator", negative)):
        try:
            verify_certificate_data(candidate, columns)
        except RuntimeError:
            controls[name] = True
        else:
            controls[name] = False
    require(all(controls.values()), "a malformed certificate control was accepted")
    return controls


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--cxx", default="g++")
    parser.add_argument("--sanitize", action="store_true")
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)

    spectra = run_gray_census(out, args.cxx, args.sanitize)
    profiles, profile_audit = audit_profiles()
    form_audit = audit_quadratic_forms()
    columns, column_counts = sparse_columns(spectra, profiles)
    certificate_bytes = (TARGET / "certificates.json").read_bytes()
    require(digest(certificate_bytes) == CERTIFICATE_SHA256, "certificate hash mismatch")
    certificate_data = json.loads(certificate_bytes)
    case_records, slack_hash = verify_certificate_data(certificate_data, columns)
    controls = mutation_controls(certificate_data, columns)
    weakest = min(Fraction(record["rational_bound"]) for record in case_records)
    require(weakest == Fraction(117641713, 100000000) and weakest > 1,
            "weakest bound does not force two low planes")

    result = {
        "status": "INDEPENDENT_LOW_PAIR71_CHECK_PASSED",
        "spectrum_census": {
            "algorithm": "Gray-code incremental line occupancies",
            "spectra": len(spectra),
            "sha256": SPECTRUM_SHA256,
        },
        "profile_audit": profile_audit,
        "quadratic_form_frequencies": form_audit,
        "incidence_columns": column_counts,
        "incidence_rows": len(row_names()),
        "incidence_columns_total": len(columns),
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_cases": case_records,
        "certificate_slacks_sha256": slack_hash,
        "weakest_rational_bound": str(weakest),
        "forced_integer_low_planes": 2,
        "mutation_controls": controls,
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (out / "result.json").write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
