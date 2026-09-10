#!/usr/bin/env python3
"""Independent compact audit of the P84 global case decomposition."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from itertools import combinations_with_replacement
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "sidon_ramsey_8" / "p84_global_cases"
PROFILE = ROOT / "sidon_ramsey_8" / "p84_profiles"

EXPECTED = {
    "orbit_catalog.txt": "4cdac43dae88dfde56506152b01fce145bf2a7e878b486933f11b0c3dba4e3df",
    "global.csv": "5c3084d0b26ed3bef8bf23e0621881214e618f8d43f159a2ccb7dbdd65ef4050",
    "anchored.csv": "64fd0d4fa1f8b34f44de2136fa399600759a4da71ceee92ec9b6125fdeea1655",
    "selected_tuples.txt": "3b23e1fd08406e6fdb3e873c37fbc5b1b8116c292022201a818eb2a5cef49bcb",
    "residuals.txt": "3bf28565b32926508b84cbbf90c40827a1dca217b92b99f4b6e68c86d5f95f02",
    "cases.csv": "7c773d21b592e6bbab40dd1e6e67e5859b9a4394db2ca4f15e7a1bc5b6538e2b",
    "p84_difference.cnf": "72ee15dd60de4f6f100f649c45eeeb93a932c3d91e3297f3432efd511aba2411",
}
TRACE_HASHES = [
    "cb30ccd2f335bed55b95b473e827317e847454206aabc9e0ab26aa9a5a07df52",
    "084e13c7add522a96d5d6f24317ed5163e109c3da3124247064569fccbdb8d31",
    "e55fc82023c6957f093de5220d36d86d4d6e1020056225658febfc96f4f05495",
    "7dfb93ee6065d2cf8677587a3da71af1070c75ede89de43e53230a12e87ef702",
]
PROFILE_HASHES = {
    "sets84_11.txt": "e1541890c78cb206076fbcd6067b2da24884b044f902c1c03ffc0da7ccdc0720",
    "ordered84_11.txt": "af291053682c346304ed0f29fd1cfe9f9920b9220289151bd2b3ce488c920536",
    "packings84_five.txt": "e1a2ec3daa7a3ee49d346ce6877f80268a0b559b8fd5bb0638d1c8cb1cb5f41f",
    "unique_five_tuples.txt": "ff1a4b6024662a7a4e114da43e584277a5a9a18a11adb9e69454a6292ccae8c5",
    "other_packings.txt": "e1a2ec3daa7a3ee49d346ce6877f80268a0b559b8fd5bb0638d1c8cb1cb5f41f",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def rows(path: Path):
    return list(csv.DictReader(path.open()))


def case_ledger(path: Path):
    data = rows(path)
    assert len(data) == 1488
    data = [
        {name: value if name == "status" else int(value)
         for name, value in row.items()}
        for row in data
    ]
    assert [row["orbit"] for row in data] == list(range(1488))
    assert all(data[i]["weight"] >= data[i + 1]["weight"]
               for i in range(len(data) - 1))
    assert all(4 * row["weight"] >= 7685948 for row in data)
    assert all(row["global_packings"] == 2 * row["anchored_packings"]
               - row["both_orientations"] for row in data)
    for row in data:
        expected = ("packing_empty" if row["anchored_packings"] == 0 else
                    "cover_excluded" if row["anchored_packings"] <= 100 else
                    "unresolved")
        assert row["status"] == expected
    status = {name: sum(row["status"] == name for row in data)
              for name in ("packing_empty", "cover_excluded", "unresolved")}
    totals = {field: sum(row[field] for row in data)
              for field in ("global_packings", "anchored_packings",
                            "both_orientations", "reflection_fixed")}
    assert status == {"packing_empty": 64, "cover_excluded": 213,
                      "unresolved": 1211}
    assert totals == {"global_packings": 125576811,
                      "anchored_packings": 62861452,
                      "both_orientations": 146093,
                      "reflection_fixed": 2639}
    assert sum(row["anchored_packings"] for row in data
               if row["status"] == "cover_excluded") == 5959
    assert sum(row["anchored_packings"] for row in data
               if row["status"] == "unresolved") == 62855493
    return {"rows": len(data), "status": status, "totals": totals,
            "unresolved_anchored_packings": 62855493}


def static_audit():
    weights = list(map(int, (PROFILE / "weights.txt").read_text().split()))
    assert len(weights) == 84 and weights == weights[::-1]
    assert min(weights) >= 0 and sum(weights) == 15685948
    maximizer = [15, 20, 22, 30, 36, 47, 56, 59, 60, 78]
    sums = [a + b for a, b in combinations_with_replacement(maximizer, 2)]
    assert len(sums) == len(set(sums)) == 55
    assert sum(weights[x] for x in maximizer) == 1999990
    assert 15685948 - 4 * 2000000 == 7685948
    assert digest(TARGET / "cases.csv") == EXPECTED["cases.csv"]
    assert digest(PROFILE / "weights.txt") == "e5922593aed71d001e4d8b2af0731191008a1583dcf373c13d81a3933507acf3"
    return {
        "case_ledger": case_ledger(TARGET / "cases.csv"),
        "ten_cap_control": {"maximizer": maximizer,
                            "pair_sums": 55, "weight": 1999990},
        "threshold": 7685948,
    }


def global_run_audit(work: Path):
    for name, expected in EXPECTED.items():
        assert digest(work / name) == expected, name
    assert (work / "cases.csv").read_bytes() == (TARGET / "cases.csv").read_bytes()
    report = json.loads((work / "verification.json").read_text())
    assert report["verified"] and report["unresolved_cases"] == 1211
    assert report["catalog_10"]["sets"] == 35250764
    assert report["catalog_10"]["max_weight"] == 1999990
    assert report["catalog_11"]["sets"] == report["reference_catalog"]["sets"] == 30510
    assert report["orbits"]["eligible_orbits"] == 1488
    assert report["global"]["packings"] == 125576811
    assert report["anchored"]["packings"] == 62861452
    assert report["selected"]["packings"] == 5959
    assert report["residuals"]["distinct_residuals"] == 5959
    assert sum(x["methods"][0]["domains"] for x in report["completions"]) == 5959
    assert sum(x["methods"][0]["ten_sets"] for x in report["completions"]) == 999039
    for index, record in enumerate(report["completions"]):
        first, second = record["methods"]
        assert first["complete"] and second["complete"]
        assert first["found"] == second["found"] == 0
        assert first["domains"] == second["domains"]
        assert first["ten_sets"] == second["ten_sets"]
        assert digest(work / f"completion_{index}_0.bin") == TRACE_HASHES[index]
        assert (work / f"completion_{index}_0.bin").read_bytes() == \
               (work / f"completion_{index}_1.bin").read_bytes()
        assert (work / f"completion_{index}_0.jsonl").read_bytes() == \
               (work / f"completion_{index}_1.jsonl").read_bytes()
    case_ledger(work / "cases.csv")
    return {"canonical_hashes": len(EXPECTED), "residuals": 5959,
            "ten_set_occurrences": 999039, "unresolved_cases": 1211,
            "verified": True}


def profile_run_audit(work: Path):
    for name, expected in PROFILE_HASHES.items():
        assert digest(work / name) == expected, name
    report = json.loads((work / "verification.json").read_text())
    assert report["verified"]
    assert report["enumerate_10"]["sets"] == 35250764
    assert report["enumerate_11"]["sets"] == 30510
    assert report["enumerate_12"]["sets"] == 0
    assert report["packing"]["packings"] == 160244
    assert len(report["completions"]) == len(report["reference_completions"]) == 6
    for first, second in zip(report["completions"], report["reference_completions"]):
        assert not first["found"] and first["input_read_complete"]
        assert second["all_unsatisfiable"]
        assert first["unique_residuals"] == second["tested"]
        assert first["ten_sets"] == second["ten_sets"]
        assert first["eleven_sets"] == second["eleven_sets"] == 0
    assert sum(x["unique_residuals"] for x in report["completions"]) == 160242
    assert sum(x["ten_sets"] for x in report["completions"]) == 41022
    target_rows = {tuple(map(int, line.split()))
                   for line in (work / "sets84_11.txt").read_text().splitlines()}
    reference_rows = {tuple(map(int, line.split()))
                      for line in (work / "reference_sets.txt").read_text().splitlines()}
    assert len(target_rows) == len(reference_rows) == 30510
    assert target_rows == reference_rows
    assert (work / "packings84_five.txt").read_bytes() == \
           (work / "other_packings.txt").read_bytes()
    return {"distinct_residuals": 160242, "five_tuples": 160244,
            "independent_algorithms": True, "verified": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--global-run", type=Path)
    parser.add_argument("--profile-run", type=Path)
    args = parser.parse_args()
    result = static_audit()
    if args.global_run:
        result["global_run"] = global_run_audit(args.global_run.resolve())
    if args.profile_run:
        result["profile_run"] = profile_run_audit(args.profile_run.resolve())
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
