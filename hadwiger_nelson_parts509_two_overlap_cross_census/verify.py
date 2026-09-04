#!/usr/bin/env python3
"""Verify the exact two-overlap cross-edge census and its inherited inputs."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
POINTS = ROOT / "hadwiger_nelson_parts509_completion_census_degree9" / "points.tsv"
POINTS_VTX = ROOT / "hadwiger_nelson_parts509_criticality" / "parts509.vtx"
PRIOR = ROOT / "hadwiger_nelson_parts509_two_overlap_reduction"
FLEXIBILITY = ROOT / "hadwiger_nelson_parts509_splus_single_cross_flexibility"
AFFINE = ROOT / "hadwiger_nelson_parts509_affine_overlap_scan"
CENSUS = HERE / "census.cpp"
EXPECTED = HERE / "expected_census.txt"

SOURCE_HASHES = {
    POINTS: "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50",
    POINTS_VTX: "770a585a6c1e1222355322707479cb826e9ada560279da904ef89c15c99ff0b5",
    PRIOR / "certificate.json": "7fddf99ef3de1e875ab5bc6b82d2f26dc751a27be54a85b03b75565990df5786",
    PRIOR / "verify.py": "10fa4c81d27c773c76f1a8645a9ff453cf846f17ed5140ec96538b8aa5ded788",
    AFFINE / "enumerate_overlaps.cpp": "97f63813d3058be87b2b6de32cb3a6b7c4e268eb7e1f49893e9f7cbd51c37b3e",
    FLEXIBILITY / "certificate.json": "718f0742acd6bbc8b4a809646a9a896912e2a593154906e2af04df62b9c3febb",
    FLEXIBILITY / "verify.py": "cfc83d15a14d34b7684576a162b602a18a3a0b2242112872f2670be498f0d9d9",
    CENSUS: "a31533704faf903214c3729748b44a0739b4c5cbae13f8a4b7dc7a633db1df44",
    EXPECTED: "b2364ee34f0442436524111dd147507574e3125761caf648d2b8908fdd51bcc6",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_output(path: Path):
    rows, scalars, flags = [], {}, set()
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("orientation="):
            encoded = dict(item.split("=", 1) for item in line.split(";"))
            if set(encoded) != {
                "orientation", "reflected", "denominator", "exactly_two",
                "with_cross", "with_genuine", "genuine_zero", "genuine_one",
                "genuine_two_plus", "interval_candidates", "exact_checks",
            }:
                raise ValueError("bad per-orientation fields")
            rows.append({key: int(value) for key, value in encoded.items()})
        elif "=" in line:
            key, value = line.split("=", 1)
            if value.isdigit():
                if key in scalars:
                    raise ValueError(f"duplicate scalar: {key}")
                scalars[key] = int(value)
            elif value == "true":
                flags.add(key)
            else:
                raise ValueError(f"bad census line: {line}")
        else:
            raise ValueError(f"bad census line: {line}")
    return rows, scalars, flags


def verify_radical_bounds() -> None:
    scale = 10**12
    radicands = (1, 3, 5, 15, 11, 33, 55, 165)
    floors = (
        10**12, 1732050807568, 2236067977499, 3872983346207,
        3316624790355, 5744562646538, 7416198487095, 12845232578665,
    )
    for radicand, lower in zip(radicands[1:], floors[1:], strict=True):
        if not lower * lower < radicand * scale * scale < (lower + 1) ** 2:
            raise ValueError("invalid rational radical bound")
    # The C++ guard is safe for both-coordinate interval-square sums.
    if not 2 * (6 * 10**18) ** 2 < 2**127:
        raise ValueError("signed-int128 safety inequality failed")


def verify_prior_reduction() -> None:
    result = subprocess.run(
        [sys.executable, str(PRIOR / "verify.py"), str(PRIOR / "certificate.json")],
        cwd=PRIOR,
        check=True,
        capture_output=True,
        text=True,
    )
    expected = (PRIOR / "expected_verify.txt").read_text(encoding="utf-8")
    if result.stdout != expected:
        raise ValueError("prior two-overlap verifier output mismatch")


def verify_single_cross_flexibility() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(FLEXIBILITY / "verify.py"),
            str(FLEXIBILITY / "certificate.json"),
        ],
        cwd=FLEXIBILITY,
        check=True,
        capture_output=True,
        text=True,
    )
    expected = (FLEXIBILITY / "expected_verify.txt").read_text(encoding="utf-8")
    if result.stdout != expected:
        raise ValueError("single-cross-edge flexibility verifier output mismatch")


def verify() -> None:
    for path, expected in SOURCE_HASHES.items():
        if sha256(path) != expected:
            raise ValueError(f"source hash mismatch: {path.relative_to(ROOT)}")
    verify_radical_bounds()
    verify_prior_reduction()
    verify_single_cross_flexibility()

    rows, scalars, flags = parse_output(EXPECTED)
    if len(rows) != 2840 or [row["orientation"] for row in rows] != list(range(2840)):
        raise ValueError("orientation rows are incomplete or noncontiguous")
    if any(row["reflected"] != (index >= 1420) for index, row in enumerate(rows)):
        raise ValueError("rotation/reflection row partition mismatch")
    if any(row["denominator"] <= 0 for row in rows):
        raise ValueError("nonpositive orientation denominator")
    if min(row["denominator"] for row in rows) != 8 or max(row["denominator"] for row in rows) != 40416:
        raise ValueError("orientation denominator range mismatch")
    if any(row["with_cross"] != row["exactly_two"] for row in rows):
        raise ValueError("an exactly-two placement lacks a cross-unit label pair")
    if any(not 0 <= row["with_genuine"] <= row["with_cross"] for row in rows):
        raise ValueError("bad genuine-cross-edge count")
    if any(
        row["genuine_zero"] + row["genuine_one"] + row["genuine_two_plus"]
        != row["exactly_two"]
        for row in rows
    ):
        raise ValueError("genuine-edge categories do not partition placements")
    if any(
        row["genuine_one"] + row["genuine_two_plus"] != row["with_genuine"]
        for row in rows
    ):
        raise ValueError("positive genuine-edge categories disagree")
    if any(row["interval_candidates"] != row["exact_checks"] for row in rows):
        raise ValueError("exact-check accounting mismatch")

    expected_scalars = {
        "overlap_induced_rotations": 1420,
        "overlap_induced_reflections": 1420,
        "distinct_nonzero_L_vectors": 11650,
        "distinct_nonzero_S_vectors": 1666,
        "internal_L_edges": 1860,
        "internal_Splus_edges": 564,
        "affine_placements_with_at_least_two_overlaps": 2992078,
        "recovered_pair_certificates": 17658256,
        "exactly_two_overlap_placements": 2373802,
        "with_any_cross_unit_label_pair": 2373802,
        "with_genuinely_new_cross_edge": 2194728,
        "with_zero_genuinely_new_cross_edges": 179074,
        "with_exactly_one_genuinely_new_cross_edge": 189738,
        "with_at_least_two_genuinely_new_cross_edges": 2004990,
        "closed_by_single_cross_edge_absorption": 368812,
        "interval_candidates": 30525682,
        "exact_distance_checks": 30525682,
    }
    if scalars != expected_scalars:
        raise ValueError("global scalar summary mismatch")
    if flags != {"exact_two_overlap_cross_census"}:
        raise ValueError("exact-census trailer mismatch")
    mapping = {
        "exactly_two": "exactly_two_overlap_placements",
        "with_cross": "with_any_cross_unit_label_pair",
        "with_genuine": "with_genuinely_new_cross_edge",
        "genuine_zero": "with_zero_genuinely_new_cross_edges",
        "genuine_one": "with_exactly_one_genuinely_new_cross_edge",
        "genuine_two_plus": "with_at_least_two_genuinely_new_cross_edges",
        "interval_candidates": "interval_candidates",
        "exact_checks": "exact_distance_checks",
    }
    for local, global_name in mapping.items():
        if sum(row[local] for row in rows) != scalars[global_name]:
            raise ValueError(f"per-orientation sum mismatch: {local}")
    rotations, reflections = rows[:1420], rows[1420:]
    for key in (
        "exactly_two", "with_cross", "with_genuine", "genuine_zero",
        "genuine_one", "genuine_two_plus",
    ):
        if sum(row[key] for row in rotations) != sum(row[key] for row in reflections):
            raise ValueError(f"rotation/reflection aggregate mismatch: {key}")
    if scalars["closed_by_single_cross_edge_absorption"] != (
        scalars["with_zero_genuinely_new_cross_edges"]
        + scalars["with_exactly_one_genuinely_new_cross_edge"]
    ):
        raise ValueError("gluing-lemma subtraction mismatch")

    print("orientations=2840 rotations=1420 reflections=1420")
    print("affine_placements_with_at_least_two_overlaps=2992078")
    print("recovered_pair_certificates=17658256")
    print("exactly_two_overlap_placements=2373802")
    print("all_exactly_two_have_cross_unit_label_pair=true")
    print("with_genuinely_new_cross_edge=2194728")
    print("with_zero_genuinely_new_cross_edges=179074")
    print("with_exactly_one_genuinely_new_cross_edge=189738")
    print("with_at_least_two_genuinely_new_cross_edges=2004990")
    print("closed_by_single_cross_edge_absorption=368812")
    print("rotation_reflection_classification_totals_match=true")
    print("prior_two_overlap_reduction_verified=true")
    print("single_cross_edge_flexibility_verified=true")
    print("solver_free_census_checks=true")


if __name__ == "__main__":
    verify()
