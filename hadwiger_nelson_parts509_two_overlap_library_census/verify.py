#!/usr/bin/env python3
"""Check source pins, complete census accounting, and the compact residual seeds.

This verifies a regenerated production transcript. It does not independently
re-enumerate the complete geometric family.
"""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PRIOR = ROOT / "hadwiger_nelson_parts509_two_overlap_cross_census"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def histogram(rows):
    result = {}
    for item in rows:
        if (len(item) != 3 or any(type(x) is not int for x in item)
                or item[0] < 0 or item[1] <= 0 or not 0 <= item[2] <= item[1]):
            raise ValueError("invalid histogram cell")
        k, count, covered = item
        if k in result:
            raise ValueError("duplicate histogram cell")
        result[k] = (count, covered)
    if list(result) != sorted(result):
        raise ValueError("unsorted histogram")
    return result


def legacy_rows(path):
    return [{k: int(v) for k, v in (field.split("=") for field in line.split(";"))}
            for line in path.read_text().splitlines() if line.startswith("orientation=")]


def verify(transcript, residual, prior_seven=None):
    manifest = json.loads((HERE / "manifest.json").read_text())
    for relative, expected in manifest["files"].items():
        if digest(ROOT / relative) != expected:
            raise ValueError(f"source/evidence digest mismatch: {relative}")
    if digest(transcript) != manifest["transcript_sha256"]:
        raise ValueError("full transcript digest mismatch")
    if digest(residual) != manifest["residual_sha256"]:
        raise ValueError("full residual digest mismatch")
    if prior_seven is not None and digest(prior_seven) != (
        "f1c9791ed5aa4b33179534dce6715edf52352c5bada066339dea2fcb7528c971"
    ):
        raise ValueError("prior seven-edge transcript digest mismatch")
    records = [json.loads(line) for line in transcript.read_text().splitlines()]
    header, *rows, final = records
    if header != {"type": "header", "first": 0, "end": 2840, "orientations": 2840,
                  "left_colourings": 135, "small_colourings": 194,
                  "expanded_small_colourings": 4656}:
        raise ValueError("full-run header mismatch")
    if len(rows) != 2840:
        raise ValueError("incomplete orientation range")
    if final != json.loads((HERE / "expected_summary.json").read_text()):
        raise ValueError("global summary mismatch")
    if final["type"] != "complete" or (final["first"], final["end"]) != (0, 2840):
        raise ValueError("missing full completion marker")
    totals, covered = Counter(), Counter()
    legacy = legacy_rows(PRIOR / "expected_census.txt")
    extended = legacy_rows(prior_seven) if prior_seven else None
    keys = {"type", "orientation", "reflected", "multi", "pairs", "two", "checks",
            "coloured", "unresolved", "dense_checks", "histogram"}
    for index, row in enumerate(rows):
        if set(row) != keys or row["type"] != "orientation" or row["orientation"] != index:
            raise ValueError("bad orientation record")
        if type(row["reflected"]) is not bool or row["reflected"] != (index >= 1420):
            raise ValueError("bad orientation parity")
        for field in keys - {"type", "reflected", "histogram"}:
            if type(row[field]) is not int or row[field] < 0:
                raise ValueError("invalid counter")
        cells = histogram(row["histogram"])
        if (sum(n for n, c in cells.values()) != row["two"]
                or sum(c for n, c in cells.values()) != row["coloured"]
                or row["two"] != row["coloured"] + row["unresolved"]):
            raise ValueError("per-orientation count mismatch")
        if row["dense_checks"] != int(index % 137 == 0 and row["two"] > 0):
            raise ValueError("direct sample coverage mismatch")
        old = legacy[index]
        if row["two"] != old["exactly_two"]:
            raise ValueError("legacy translation census mismatch")
        for k, name in enumerate(("zero", "one", "two")):
            if cells.get(k, (0, 0))[0] != old["genuine_" + name]:
                raise ValueError("legacy per-orientation edge census mismatch")
        if extended is not None:
            if len(extended) != 2840:
                raise ValueError("incomplete prior seven-edge transcript")
            for k, name in enumerate(("zero", "one", "two", "three", "four", "five", "six", "seven")):
                if cells.get(k, (0, 0))[0] != extended[index]["genuine_" + name]:
                    raise ValueError("prior seven-edge per-orientation mismatch")
        for k, (n, c) in cells.items():
            totals[k] += n
            covered[k] += c
    for field in ("multi", "pairs", "two", "checks", "coloured", "unresolved", "dense_checks"):
        if sum(row[field] for row in rows) != final[field]:
            raise ValueError(f"global accounting mismatch: {field}")
    if [(k, totals[k], covered[k]) for k in sorted(totals)] != [
        tuple(cell) for cell in final["histogram"]
    ]:
        raise ValueError("global histogram mismatch")
    if (final["multi"], final["pairs"], final["two"]) != (2992078, 17658256, 2373802):
        raise ValueError("known complete geometry census mismatch")
    prior_counts = (179074, 189738, 194946, 180216, 180234, 173230, 153368, 137192)
    if any((totals[k], covered[k]) != (n, n) for k, n in enumerate(prior_counts)):
        raise ValueError("prior zero-through-seven closure mismatch")
    # Geometry is reflection-symmetric; library coverage need not be.
    for k in totals:
        halves = [sum(histogram(r["histogram"]).get(k, (0, 0))[0] for r in half)
                  for half in (rows[:1420], rows[1420:])]
        if halves[0] != halves[1]:
            raise ValueError("geometric reflection subtotal mismatch")
    cases = [json.loads(line) for line in residual.read_text().splitlines()]
    if len(cases) != final["unresolved"]:
        raise ValueError("residual count mismatch")
    seeds, residual_counts = [], Counter()
    previous = None
    for case in cases:
        if set(case) != {"orientation", "denominator", "x", "y", "overlaps", "edges"}:
            raise ValueError("bad residual fields")
        index = case["orientation"]
        if not 0 <= index < 2840 or case["denominator"] <= 0:
            raise ValueError("bad residual orientation")
        if any(len(case[k]) != 8 or any(type(v) is not int for v in case[k]) for k in ("x", "y")):
            raise ValueError("bad residual translation")
        if len(case["overlaps"]) != 2 or not all(0 <= v < 374 * 136 for v in case["overlaps"]):
            raise ValueError("bad overlap seed")
        a, b = case["overlaps"]
        if a >= b or a // 136 == b // 136 or a % 136 == b % 136:
            raise ValueError("degenerate overlap seed")
        if case["edges"] != sorted(set(case["edges"])) or any(
            not (0 <= e // 510 < 374 and 374 <= e % 510 < 510) for e in case["edges"]
        ):
            raise ValueError("bad residual edge list")
        key = (index, tuple(case["x"]), tuple(case["y"]))
        if previous is not None and key <= previous:
            raise ValueError("unordered or repeated residual")
        previous = key
        seeds.append((index, a, b))
        residual_counts[index, len(case["edges"])] += 1
    if len(seeds) != len(set(seeds)):
        raise ValueError("duplicate residual isometry seed")
    published_seeds = [tuple(map(int, line.split())) for line in
                       (HERE / "residual_seeds.tsv").read_text().splitlines()
                       if not line.startswith("#")]
    if seeds != published_seeds:
        raise ValueError("compact residual seeds mismatch")
    for row in rows:
        for k, (n, c) in histogram(row["histogram"]).items():
            if residual_counts[row["orientation"], k] != n - c:
                raise ValueError("residual histogram mismatch")
    minimum = min((k for k in totals if totals[k] != covered[k]), default=None)
    print(f"exactly_two_overlap_placements={final['two']}")
    print(f"library_coloured_placements={final['coloured']}")
    print(f"residual_placements={final['unresolved']}")
    print(f"minimum_residual_new_edges={minimum}")
    print(f"maximum_new_edges={max(totals)}")
    print(f"exact_distance_checks={final['checks']}")
    print(f"dense_geometry_samples={final['dense_checks']}")
    print("full_census_and_residual_transcripts_verified=true")
    print("legacy_per_orientation_counts_match=true")
    if extended is not None:
        print("prior_seven_edge_per_orientation_counts_match=true")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("transcript", type=Path)
    parser.add_argument("residual", type=Path)
    parser.add_argument("--prior-seven", type=Path)
    arguments = parser.parse_args()
    verify(arguments.transcript, arguments.residual, arguments.prior_seven)
