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
CRITICALITY = ROOT / "hadwiger_nelson_parts509_criticality" / "certificate.json"
CENSUS = HERE / "census.cpp"
LIBRARY_GENERATOR = HERE / "make_colour_libraries.py"
LIBRARY = HERE / "colour_libraries.txt"
EXPECTED = HERE / "expected_census.txt"
THREE_SUMMARY = HERE / "expected_three_summary.txt"

from make_colour_libraries import library_bytes  # noqa: E402

sys.path.insert(0, str(PRIOR))
import verify as geometry  # noqa: E402

SOURCE_HASHES = {
    POINTS: "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50",
    POINTS_VTX: "770a585a6c1e1222355322707479cb826e9ada560279da904ef89c15c99ff0b5",
    PRIOR / "certificate.json": "7fddf99ef3de1e875ab5bc6b82d2f26dc751a27be54a85b03b75565990df5786",
    PRIOR / "verify.py": "10fa4c81d27c773c76f1a8645a9ff453cf846f17ed5140ec96538b8aa5ded788",
    AFFINE / "enumerate_overlaps.cpp": "97f63813d3058be87b2b6de32cb3a6b7c4e268eb7e1f49893e9f7cbd51c37b3e",
    FLEXIBILITY / "certificate.json": "718f0742acd6bbc8b4a809646a9a896912e2a593154906e2af04df62b9c3febb",
    FLEXIBILITY / "verify.py": "cfc83d15a14d34b7684576a162b602a18a3a0b2242112872f2670be498f0d9d9",
    CRITICALITY: "d354f9629c41639168b80fc1aa6feb6e4187dd37dee7efcb83b4ef6ebe68d16c",
    CENSUS: "167b9ae5a2fb101eed1fbd7abe897a3d76e216f0cccb403b19fec3dfec38c2b7",
    LIBRARY_GENERATOR: "ad23e21c17c48242ea2dcbb4a90bdad96da655c8c29f0ddadbfe86f4f5ab5660",
    LIBRARY: "91f5f39f1533e5780edfa30130f36bee3f90428bd7d442e788e8311d029b4169",
    EXPECTED: "4008074237712c7fe2064cb32c3a47db0f91cf293e1be11914bed232b95c497d",
    THREE_SUMMARY: "c82fc5b5b7da533686ddeb12273337e6a218e5a308be299218a4d7bccf14c559",
}

LEGACY_ROW_FIELDS = {
    "orientation", "reflected", "denominator", "exactly_two",
    "with_cross", "with_genuine", "genuine_zero", "genuine_one",
    "genuine_two", "genuine_three_plus", "two_share_left",
    "two_share_small", "two_disjoint", "disjoint_adj00",
    "disjoint_adj01", "disjoint_adj10", "disjoint_adj11",
    "two_library_absorbed", "absorbed_share_left",
    "absorbed_share_small", "absorbed_disjoint",
    "interval_candidates", "exact_checks",
}
THREE_ROW_FIELDS = (LEGACY_ROW_FIELDS - {"genuine_three_plus"}) | {
    "genuine_three", "genuine_four_plus", "three_L1_S3", "three_L3_S1",
    "three_L2_S2", "three_L2_S3", "three_L3_S2", "three_L3_S3",
    "three_library_absorbed", "absorbed_three_L1_S3",
    "absorbed_three_L3_S1", "absorbed_three_L2_S2",
    "absorbed_three_L2_S3", "absorbed_three_L3_S2",
    "absorbed_three_L3_S3",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_output(path: Path, row_fields=None):
    rows, scalars, flags = [], {}, set()
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("orientation="):
            encoded = dict(item.split("=", 1) for item in line.split(";"))
            if row_fields is None or set(encoded) != row_fields:
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


def verify_colour_libraries() -> None:
    if library_bytes() != LIBRARY.read_bytes():
        raise ValueError("colour library does not match its source certificates")
    left, small = [], []
    for line in LIBRARY.read_text(encoding="ascii").splitlines():
        if line.startswith("L:") and len(line) == 376:
            left.append(tuple(map(int, line[2:])))
        elif line.startswith("S:") and len(line) == 138:
            small.append(tuple(map(int, line[2:])))
        else:
            raise ValueError("bad colour-library row")
    if len(left) != 135 or len(small) != 194:
        raise ValueError("colour-library row-count mismatch")
    if any(not set(colours) <= {0, 1, 2, 3} for colours in left + small):
        raise ValueError("bad colour-library value")
    points = geometry.read_points(POINTS)
    left_edges = geometry.build_edges(points[:374])
    small_edges = geometry.build_edges([points[0]] + points[374:])
    if len(left_edges) != 1860 or len(small_edges) != 564:
        raise ValueError("strict internal-edge census mismatch")
    if any(
        colours[u] == colours[v]
        for colours in left
        for u, v in left_edges
    ):
        raise ValueError("improper L colour-library witness")
    if any(
        colours[u] == colours[v]
        for colours in small
        for u, v in small_edges
    ):
        raise ValueError("improper S+ colour-library witness")


def verify_three_edge_summary():
    rows, scalars, flags = parse_output(THREE_SUMMARY)
    if rows:
        raise ValueError("compact three-edge summary contains orientation rows")
    expected = {
        "affine_placements_with_at_least_two_overlaps": 2992078,
        "recovered_pair_certificates": 17658256,
        "exactly_two_overlap_placements": 2373802,
        "with_any_cross_unit_label_pair": 2373802,
        "with_genuinely_new_cross_edge": 2194728,
        "with_zero_genuinely_new_cross_edges": 179074,
        "with_exactly_one_genuinely_new_cross_edge": 189738,
        "with_exactly_two_genuinely_new_cross_edges": 194946,
        "with_exactly_three_genuinely_new_cross_edges": 180216,
        "with_at_least_four_genuinely_new_cross_edges": 1629828,
        "two_new_edges_share_left_endpoint": 21432,
        "two_new_edges_share_small_endpoint": 37900,
        "two_new_edges_vertex_disjoint": 135614,
        "disjoint_two_edges_left_nonedge_small_nonedge": 122630,
        "disjoint_two_edges_left_nonedge_small_edge": 12124,
        "disjoint_two_edges_left_edge_small_nonedge": 520,
        "disjoint_two_edges_left_edge_small_edge": 340,
        "two_new_edges_absorbed_by_explicit_libraries": 194946,
        "absorbed_two_edges_share_left_endpoint": 21432,
        "absorbed_two_edges_share_small_endpoint": 37900,
        "absorbed_two_edges_vertex_disjoint": 135614,
        "two_new_edges_unresolved_by_explicit_libraries": 0,
        "three_new_edges_L1_S3": 7402,
        "three_new_edges_L3_S1": 15236,
        "three_new_edges_L2_S2": 154,
        "three_new_edges_L2_S3": 31788,
        "three_new_edges_L3_S2": 37302,
        "three_new_edges_L3_S3": 88334,
        "three_new_edges_absorbed_by_explicit_libraries": 180216,
        "absorbed_three_new_edges_L1_S3": 7402,
        "absorbed_three_new_edges_L3_S1": 15236,
        "absorbed_three_new_edges_L2_S2": 154,
        "absorbed_three_new_edges_L2_S3": 31788,
        "absorbed_three_new_edges_L3_S2": 37302,
        "absorbed_three_new_edges_L3_S3": 88334,
        "three_new_edges_unresolved_by_explicit_libraries": 0,
        "closed_by_single_cross_edge_absorption": 368812,
        "interval_candidates": 45942172,
        "exact_distance_checks": 45942172,
    }
    if scalars != expected:
        raise ValueError("three-edge global summary mismatch")
    if flags != {"exact_two_overlap_cross_census"}:
        raise ValueError("three-edge census trailer mismatch")
    if sum(
        scalars[name]
        for name in (
            "with_zero_genuinely_new_cross_edges",
            "with_exactly_one_genuinely_new_cross_edge",
            "with_exactly_two_genuinely_new_cross_edges",
            "with_exactly_three_genuinely_new_cross_edges",
            "with_at_least_four_genuinely_new_cross_edges",
        )
    ) != scalars["exactly_two_overlap_placements"]:
        raise ValueError("three-edge categories do not partition placements")
    topology_suffixes = ("L1_S3", "L3_S1", "L2_S2", "L2_S3", "L3_S2", "L3_S3")
    if sum(scalars[f"three_new_edges_{suffix}"] for suffix in topology_suffixes) != (
        scalars["with_exactly_three_genuinely_new_cross_edges"]
    ):
        raise ValueError("three-edge topologies do not partition placements")
    if any(
        scalars[f"absorbed_three_new_edges_{suffix}"]
        != scalars[f"three_new_edges_{suffix}"]
        for suffix in topology_suffixes
    ):
        raise ValueError("a three-edge topology lacks an explicit colouring")
    if scalars["three_new_edges_absorbed_by_explicit_libraries"] != (
        scalars["with_exactly_three_genuinely_new_cross_edges"]
    ) or scalars["three_new_edges_unresolved_by_explicit_libraries"] != 0:
        raise ValueError("three-edge explicit-colouring closure mismatch")
    if scalars["interval_candidates"] != scalars["exact_distance_checks"]:
        raise ValueError("three-edge exact-check accounting mismatch")
    return scalars


def verify_extended_transcript(path: Path, expected_scalars) -> None:
    if sha256(path) != "6a1903a823aa4712ffc76107b038e2ab2f78a844651bcdc4c47264ed94513f2c":
        raise ValueError("extended transcript hash mismatch")
    rows, scalars, flags = parse_output(path, THREE_ROW_FIELDS)
    headers = {
        "overlap_induced_rotations": 1420,
        "overlap_induced_reflections": 1420,
        "distinct_nonzero_L_vectors": 11650,
        "distinct_nonzero_S_vectors": 1666,
        "internal_L_edges": 1860,
        "internal_Splus_edges": 564,
        "explicit_L_colourings": 135,
        "explicit_Splus_colourings": 194,
    }
    if scalars != headers | expected_scalars:
        raise ValueError("extended transcript scalar mismatch")
    if flags != {"exact_two_overlap_cross_census"}:
        raise ValueError("extended transcript trailer mismatch")
    if len(rows) != 2840 or [row["orientation"] for row in rows] != list(range(2840)):
        raise ValueError("extended orientation rows are incomplete or noncontiguous")
    if any(row["reflected"] != (index >= 1420) for index, row in enumerate(rows)):
        raise ValueError("extended rotation/reflection partition mismatch")
    if any(
        row["genuine_zero"] + row["genuine_one"] + row["genuine_two"]
        + row["genuine_three"] + row["genuine_four_plus"] != row["exactly_two"]
        for row in rows
    ):
        raise ValueError("extended genuine-edge categories do not partition placements")
    topology_suffixes = ("L1_S3", "L3_S1", "L2_S2", "L2_S3", "L3_S2", "L3_S3")
    if any(
        sum(row[f"three_{suffix}"] for suffix in topology_suffixes)
        != row["genuine_three"]
        for row in rows
    ):
        raise ValueError("extended three-edge topologies do not partition placements")
    if any(
        row["three_library_absorbed"] != row["genuine_three"]
        or any(
            row[f"absorbed_three_{suffix}"] != row[f"three_{suffix}"]
            for suffix in topology_suffixes
        )
        for row in rows
    ):
        raise ValueError("extended row lacks an explicit three-edge colouring")
    if any(row["interval_candidates"] != row["exact_checks"] for row in rows):
        raise ValueError("extended exact-check accounting mismatch")
    mapping = {
        "exactly_two": "exactly_two_overlap_placements",
        "with_cross": "with_any_cross_unit_label_pair",
        "with_genuine": "with_genuinely_new_cross_edge",
        "genuine_zero": "with_zero_genuinely_new_cross_edges",
        "genuine_one": "with_exactly_one_genuinely_new_cross_edge",
        "genuine_two": "with_exactly_two_genuinely_new_cross_edges",
        "genuine_three": "with_exactly_three_genuinely_new_cross_edges",
        "genuine_four_plus": "with_at_least_four_genuinely_new_cross_edges",
        "three_library_absorbed": "three_new_edges_absorbed_by_explicit_libraries",
        "interval_candidates": "interval_candidates",
        "exact_checks": "exact_distance_checks",
    }
    mapping.update({f"three_{suffix}": f"three_new_edges_{suffix}" for suffix in topology_suffixes})
    mapping.update({
        f"absorbed_three_{suffix}": f"absorbed_three_new_edges_{suffix}"
        for suffix in topology_suffixes
    })
    for local, global_name in mapping.items():
        if sum(row[local] for row in rows) != scalars[global_name]:
            raise ValueError(f"extended per-orientation sum mismatch: {local}")
    rotations, reflections = rows[:1420], rows[1420:]
    symmetry_fields = tuple(
        key for key in mapping if key not in {"interval_candidates", "exact_checks"}
    )
    for key in symmetry_fields:
        if sum(row[key] for row in rotations) != sum(row[key] for row in reflections):
            raise ValueError(f"extended rotation/reflection mismatch: {key}")


def verify() -> None:
    for path, expected in SOURCE_HASHES.items():
        if sha256(path) != expected:
            raise ValueError(f"source hash mismatch: {path.relative_to(ROOT)}")
    verify_radical_bounds()
    verify_prior_reduction()
    verify_single_cross_flexibility()
    verify_colour_libraries()
    three_scalars = verify_three_edge_summary()

    rows, scalars, flags = parse_output(EXPECTED, LEGACY_ROW_FIELDS)
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
        row["genuine_zero"] + row["genuine_one"] + row["genuine_two"]
        + row["genuine_three_plus"]
        != row["exactly_two"]
        for row in rows
    ):
        raise ValueError("genuine-edge categories do not partition placements")
    if any(
        row["genuine_one"] + row["genuine_two"] + row["genuine_three_plus"]
        != row["with_genuine"]
        for row in rows
    ):
        raise ValueError("positive genuine-edge categories disagree")
    if any(
        row["two_share_left"] + row["two_share_small"] + row["two_disjoint"]
        != row["genuine_two"]
        for row in rows
    ):
        raise ValueError("two-edge topologies do not partition placements")
    if any(
        row["disjoint_adj00"] + row["disjoint_adj01"]
        + row["disjoint_adj10"] + row["disjoint_adj11"]
        != row["two_disjoint"]
        for row in rows
    ):
        raise ValueError("disjoint adjacency types do not partition placements")
    if any(
        row["two_library_absorbed"] != row["genuine_two"]
        or row["absorbed_share_left"] != row["two_share_left"]
        or row["absorbed_share_small"] != row["two_share_small"]
        or row["absorbed_disjoint"] != row["two_disjoint"]
        for row in rows
    ):
        raise ValueError("an exactly-two-new-edge placement lacks an explicit colouring")
    if any(row["interval_candidates"] != row["exact_checks"] for row in rows):
        raise ValueError("exact-check accounting mismatch")

    expected_scalars = {
        "overlap_induced_rotations": 1420,
        "overlap_induced_reflections": 1420,
        "distinct_nonzero_L_vectors": 11650,
        "distinct_nonzero_S_vectors": 1666,
        "internal_L_edges": 1860,
        "internal_Splus_edges": 564,
        "explicit_L_colourings": 135,
        "explicit_Splus_colourings": 194,
        "affine_placements_with_at_least_two_overlaps": 2992078,
        "recovered_pair_certificates": 17658256,
        "exactly_two_overlap_placements": 2373802,
        "with_any_cross_unit_label_pair": 2373802,
        "with_genuinely_new_cross_edge": 2194728,
        "with_zero_genuinely_new_cross_edges": 179074,
        "with_exactly_one_genuinely_new_cross_edge": 189738,
        "with_exactly_two_genuinely_new_cross_edges": 194946,
        "with_at_least_three_genuinely_new_cross_edges": 1810044,
        "two_new_edges_share_left_endpoint": 21432,
        "two_new_edges_share_small_endpoint": 37900,
        "two_new_edges_vertex_disjoint": 135614,
        "disjoint_two_edges_left_nonedge_small_nonedge": 122630,
        "disjoint_two_edges_left_nonedge_small_edge": 12124,
        "disjoint_two_edges_left_edge_small_nonedge": 520,
        "disjoint_two_edges_left_edge_small_edge": 340,
        "two_new_edges_absorbed_by_explicit_libraries": 194946,
        "absorbed_two_edges_share_left_endpoint": 21432,
        "absorbed_two_edges_share_small_endpoint": 37900,
        "absorbed_two_edges_vertex_disjoint": 135614,
        "two_new_edges_unresolved_by_explicit_libraries": 0,
        "closed_by_single_cross_edge_absorption": 368812,
        "interval_candidates": 39179441,
        "exact_distance_checks": 39179441,
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
        "genuine_two": "with_exactly_two_genuinely_new_cross_edges",
        "genuine_three_plus": "with_at_least_three_genuinely_new_cross_edges",
        "two_share_left": "two_new_edges_share_left_endpoint",
        "two_share_small": "two_new_edges_share_small_endpoint",
        "two_disjoint": "two_new_edges_vertex_disjoint",
        "disjoint_adj00": "disjoint_two_edges_left_nonedge_small_nonedge",
        "disjoint_adj01": "disjoint_two_edges_left_nonedge_small_edge",
        "disjoint_adj10": "disjoint_two_edges_left_edge_small_nonedge",
        "disjoint_adj11": "disjoint_two_edges_left_edge_small_edge",
        "two_library_absorbed": "two_new_edges_absorbed_by_explicit_libraries",
        "absorbed_share_left": "absorbed_two_edges_share_left_endpoint",
        "absorbed_share_small": "absorbed_two_edges_share_small_endpoint",
        "absorbed_disjoint": "absorbed_two_edges_vertex_disjoint",
        "interval_candidates": "interval_candidates",
        "exact_checks": "exact_distance_checks",
    }
    for local, global_name in mapping.items():
        if sum(row[local] for row in rows) != scalars[global_name]:
            raise ValueError(f"per-orientation sum mismatch: {local}")
    rotations, reflections = rows[:1420], rows[1420:]
    for key in (
        "exactly_two", "with_cross", "with_genuine", "genuine_zero",
        "genuine_one", "genuine_two", "genuine_three_plus",
        "two_share_left", "two_share_small", "two_disjoint",
        "disjoint_adj00", "disjoint_adj01", "disjoint_adj10", "disjoint_adj11",
        "two_library_absorbed", "absorbed_share_left", "absorbed_share_small",
        "absorbed_disjoint",
    ):
        if sum(row[key] for row in rotations) != sum(row[key] for row in reflections):
            raise ValueError(f"rotation/reflection aggregate mismatch: {key}")
    if scalars["closed_by_single_cross_edge_absorption"] != (
        scalars["with_zero_genuinely_new_cross_edges"]
        + scalars["with_exactly_one_genuinely_new_cross_edge"]
    ):
        raise ValueError("gluing-lemma subtraction mismatch")
    if scalars["two_new_edges_absorbed_by_explicit_libraries"] != (
        scalars["with_exactly_two_genuinely_new_cross_edges"]
    ) or scalars["two_new_edges_unresolved_by_explicit_libraries"] != 0:
        raise ValueError("two-edge explicit-colouring closure mismatch")

    print("orientations=2840 rotations=1420 reflections=1420")
    print("affine_placements_with_at_least_two_overlaps=2992078")
    print("recovered_pair_certificates=17658256")
    print("exactly_two_overlap_placements=2373802")
    print("all_exactly_two_have_cross_unit_label_pair=true")
    print("with_genuinely_new_cross_edge=2194728")
    print("with_zero_genuinely_new_cross_edges=179074")
    print("with_exactly_one_genuinely_new_cross_edge=189738")
    print("with_exactly_two_genuinely_new_cross_edges=194946")
    print("with_exactly_three_genuinely_new_cross_edges=180216")
    print("with_at_least_four_genuinely_new_cross_edges=1629828")
    print("two_edge_topologies=share_L:21432 share_Splus:37900 disjoint:135614")
    print("two_new_edges_absorbed_by_explicit_libraries=194946")
    print("two_new_edges_unresolved_by_explicit_libraries=0")
    print("three_edge_topologies=L1_S3:7402 L3_S1:15236 L2_S2:154 L2_S3:31788 L3_S2:37302 L3_S3:88334")
    print("three_new_edges_absorbed_by_explicit_libraries=180216")
    print("three_new_edges_unresolved_by_explicit_libraries=0")
    print("closed_by_single_cross_edge_absorption=368812")
    print("closed_by_at_most_two_edge_certificates=563758")
    closed_through_three = (
        three_scalars["closed_by_single_cross_edge_absorption"]
        + three_scalars["two_new_edges_absorbed_by_explicit_libraries"]
        + three_scalars["three_new_edges_absorbed_by_explicit_libraries"]
    )
    print(f"closed_by_at_most_three_edge_certificates={closed_through_three}")
    print("rotation_reflection_classification_totals_match=true")
    print("prior_two_overlap_reduction_verified=true")
    print("single_cross_edge_flexibility_verified=true")
    print("explicit_colour_libraries_verified=true")
    print("solver_free_census_checks=true")

    if len(sys.argv) > 2:
        raise ValueError("usage: verify.py [EXTENDED_TRANSCRIPT]")
    if len(sys.argv) == 2:
        verify_extended_transcript(Path(sys.argv[1]), three_scalars)


if __name__ == "__main__":
    verify()
