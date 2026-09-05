#!/usr/bin/env python3
"""Independent compact audit for the ten-cycle minority-matching lemma.

This checker intentionally imports no code from the contribution under review.
With --sweep it also validates a freshly generated serial SAT/DRAT run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path


EXPECTED_PARENT_SHA256 = (
    "f01c990a1dae17fb7bc1cd633d785cd819ba9f4d1a1eeacd69b4034663af104e"
)
EXPECTED_OPEN = [64, 65, 67, 69]
EXPECTED_SURVIVORS = [
    [1, 2, 2, 1, 1, 1, 1, 2, 2],
    [1, 2, 2, 1, 1, 1, 2, 2, 2],
    [1, 2, 2, 1, 1, 2, 2, 2, 2],
    [1, 2, 2, 1, 2, 2, 2, 2, 2],
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_info(path: Path) -> dict[str, object]:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            digest.update(block)
    return {"bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def multiplicity(row: tuple[int, ...]) -> int:
    result = math.factorial(len(row))
    for count in Counter(row).values():
        result //= math.factorial(count)
    return result


def enumerate_profiles() -> tuple[list[list[int]], int]:
    """Use sorted multisets and orbit multiplicities, not a 4^9 scan."""
    profiles: list[list[int]] = []
    labeled = 0
    for red in combinations_with_replacement(range(3), 3):
        for blue in combinations_with_replacement(range(4), 6):
            row = red + blue
            complete = row.count(3)
            feasible = any(
                a + 3 * complete <= 4 and 18 <= 2 + a + sum(row) <= 24
                for a in range(14)
            )
            if feasible:
                profiles.append(list(row))
                labeled += multiplicity(red) * multiplicity(blue)
    return profiles, labeled


def edge_orbits() -> dict[tuple[int, int], int]:
    """Construct actual unordered-pair C3 orbits and submitted variable order."""
    sigma = tuple(3 * (v // 3) + (v + 1) % 3 if v < 30 else v for v in range(43))
    unseen = set(combinations(range(43), 2))
    orbits: list[tuple[tuple[int, int], ...]] = []
    while unseen:
        start = min(unseen)
        orbit = set()
        edge = start
        while edge not in orbit:
            orbit.add(edge)
            edge = tuple(sorted((sigma[edge[0]], sigma[edge[1]])))
        unseen -= orbit
        orbits.append(tuple(sorted(orbit)))
    cross = sorted(
        (o for o in orbits if o[0][1] < 30 and o[0][0] // 3 != o[0][1] // 3),
        key=lambda o: o[0],
    )
    fixed = sorted((o for o in orbits if o[0][0] >= 30), key=lambda o: o[0])
    links = sorted(
        (o for o in orbits if o[0][0] < 30 <= o[0][1]),
        key=lambda o: (o[0][1], o[0][0]),
    )
    require((len(orbits), len(cross), len(fixed), len(links)) == (353, 135, 78, 130),
            "unexpected C3 edge-orbit counts")
    result: dict[tuple[int, int], int] = {}
    for variable, orbit in enumerate(cross + fixed + links, 1):
        for edge in orbit:
            result[edge] = variable
    return result


def cube_units(weights: list[int], variables: dict[tuple[int, int], int]) -> bytes:
    literals = []
    for block, weight in enumerate(weights, 1):
        for offset in range(3):
            variable = variables[(0, 3 * block + offset)]
            literals.append(variable if offset < weight else -variable)
    require(len(literals) == len(set(map(abs, literals))) == 27, "bad cube unit support")
    return "".join(f"{literal} 0\n" for literal in literals).encode()


def check_matching_consequence() -> int:
    """Exhaust all symmetric weights on four red triangles."""
    pairs = list(combinations(range(4), 2))
    accepted = 0
    for values in product((1, 2), repeat=len(pairs)):
        weights = dict(zip(pairs, values))
        rows = []
        for vertex in range(4):
            row = sorted(
                weights[tuple(sorted((vertex, other)))]
                for other in range(4) if other != vertex
            )
            rows.append(row)
        if rows != [[1, 2, 2]] * 4:
            continue
        accepted += 1
        one_edges = [edge for edge, value in weights.items() if value == 1]
        require(len(one_edges) == 2, "one-edges do not have matching size")
        require(sorted(v for edge in one_edges for v in edge) == list(range(4)),
                "one-edges are not a perfect matching")
    require(accepted == 3, "unexpected number of labeled perfect matchings")
    return accepted


def check_public(source: Path) -> dict[str, object]:
    parent = source.parent / "ramsey_r55_order3_ten_cycle_obstruction"
    manifest = json.loads((source / "parent_manifest.json").read_text())
    for name, digest in manifest["files"].items():
        require(file_info(parent / name)["sha256"] == digest, f"parent source changed: {name}")
    stored = json.loads((parent / "anchor_r4.json").read_text())["weights"]
    profiles, labeled = enumerate_profiles()
    require(profiles == stored, "independent profile list disagrees with parent list")
    require((len(profiles), labeled) == (98, 5599), "wrong profile counts")

    result = json.loads((source / "result.json").read_text())
    excluded = result["excluded_indices"]
    require(result["open_indices"] == EXPECTED_OPEN, "wrong public open indices")
    require([stored[index] for index in EXPECTED_OPEN] == EXPECTED_SURVIVORS,
            "wrong public survivor rows")
    require(sorted(excluded + EXPECTED_OPEN) == list(range(98)) and len(excluded) == 94,
            "public result does not partition all profiles")
    require([row["index"] for row in result["cases"]] == excluded,
            "public certificate rows disagree with excluded indices")
    require(not result["all_98_cubes_excluded"] and not result["target_graph_found"],
            "public scope flags overclaim")
    require(result["base"]["sha256"] == EXPECTED_PARENT_SHA256, "wrong public parent hash")

    degree_ranges = {}
    for p in range(1, 5):
        possible = [a for a in range(14) if a <= 4 and 18 <= 19 - p + a <= 24]
        require(possible == list(range(max(0, p - 1), 5)), "degree-range derivation failed")
        degree_ranges[str(p)] = [possible[0], possible[-1]]
    return {
        "normalized_profiles": len(profiles),
        "labeled_profiles_by_orbit_multiplicity": labeled,
        "open_indices": EXPECTED_OPEN,
        "matching_weight_matrices": check_matching_consequence(),
        "fixed_red_neighbor_ranges_by_p": degree_ranges,
        "total_pair_orbits": 353,
        "primary_variable_orbits": len(set(edge_orbits().values())),
    }


def check_sweep(source: Path, sweep: Path) -> dict[str, object]:
    report = json.loads((sweep / "sweep.json").read_text())
    public = json.loads((source / "result.json").read_text())
    require(report["complete_bounded_sweep"], "fresh sweep is incomplete")
    require(report["open_indices"] == EXPECTED_OPEN, "fresh open indices differ")
    require(report["excluded_indices"] == public["excluded_indices"],
            "fresh excluded indices differ")
    require(not report["all_98_cubes_excluded"] and not report["target_graph_found"],
            "fresh scope flags differ")
    base = sweep / "base.cnf"
    require(file_info(base)["sha256"] == EXPECTED_PARENT_SHA256, "fresh parent hash differs")
    with base.open("rb") as stream:
        base_header = stream.readline()
        base_body = stream.read()
    require(base_header == b"p cnf 28950 927000\n", "bad fresh parent header")

    weights = json.loads(
        (source.parent / "ramsey_r55_order3_ten_cycle_obstruction" / "anchor_r4.json").read_text()
    )["weights"]
    variables = edge_orbits()
    public_rows = {row["index"]: row for row in public["cases"]}
    formula_reference_matches = 0
    proof_reference_matches = 0
    replay_logs_verified = 0
    for row in report["cases"]:
        index = row["index"]
        cube = sweep / f"cube_{index:02}.cnf"
        with cube.open("rb") as stream:
            require(stream.readline() == b"p cnf 28950 927027\n", f"bad cube header {index}")
            body = stream.read()
        units = cube_units(weights[index], variables)
        require(body == base_body + units, f"cube {index} is not exact parent plus units")
        require(file_info(cube) == row["formula"], f"cube checkpoint hash differs {index}")
        if index in public_rows:
            if row["formula"] == public_rows[index]["full_formula"]:
                formula_reference_matches += 1
            proof = sweep / f"cube_{index:02}.drat"
            require(file_info(proof) == row["proof"], f"proof checkpoint hash differs {index}")
            if row["proof"] == public_rows[index]["full_proof"]:
                proof_reference_matches += 1
            log = (sweep / f"cube_{index:02}.replay.log").read_text()
            require("s VERIFIED" in log and row.get("replay_code") == 0,
                    f"proof replay not verified {index}")
            replay_logs_verified += 1
        else:
            require(row["status"] == "open" and row.get("solver_code") == 0,
                    f"open case has unexpected status {index}")
    require(replay_logs_verified == 94, "wrong replay count")
    return {
        "fresh_exclusions_replayed": replay_logs_verified,
        "fresh_open_indices": EXPECTED_OPEN,
        "formula_reference_hash_matches": formula_reference_matches,
        "proof_reference_hash_matches": proof_reference_matches,
        "workers": report["contract"]["workers"],
        "solver_seconds_per_cube": report["contract"]["solver_seconds_per_cube"],
        "fresh_elapsed_seconds": report["elapsed_seconds"],
        "largest_child_maxrss_kib": report["largest_child_maxrss_kib"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--sweep", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    report = {"public": check_public(source)}
    if args.sweep:
        report["fresh_sweep"] = check_sweep(source, args.sweep.resolve())
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
