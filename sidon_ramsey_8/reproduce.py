#!/usr/bin/env python3
"""Recompute the integer certificate and the complete P85 exclusion."""
import argparse
import concurrent.futures
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import time

SOURCE = Path(__file__).resolve().parent
EXPECTED = {
    "sets85_11.txt": "41bc844293638556ad1896f5ad3593a3181c24e1edba7aea8d73c1aeca4051ab",
    "ordered_sets.txt": "29f50fe15a092b6b1a8270dcbe7c6f4714b6e21cd3d9ea3fe71831af8d96f907",
    "packings.txt": "3ac309d39a65e7853042b50a8d11d4203821ed19ba13a952a107befc369d7122",
}


def run(args):
    result = subprocess.run(list(map(str, args)), check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def check_hash(path, name=None):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest == EXPECTED[name or path.name], (path, digest)


def sidon(row):
    sums = [x + y for x, y in itertools.combinations_with_replacement(row, 2)]
    return len(sums) == len(set(sums))


def read_sets(path):
    rows = [tuple(map(int, line.split())) for line in path.read_text().splitlines()]
    assert len(rows) == len(set(rows)) == 56110
    for row in rows:
        assert len(row) == 11 and tuple(sorted(set(row))) == row
        assert 0 <= row[0] <= row[-1] < 85 and sidon(row)
    return rows


def main():
    if not __debug__:
        raise SystemExit("Run without -O or PYTHONOPTIMIZE: proof checks use assertions.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--independent", action="store_true")
    args = parser.parse_args()
    work = args.work.resolve()
    assert 1 <= args.jobs <= 64
    assert work != SOURCE and SOURCE not in work.parents, "Use a work directory outside the source."
    work.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    programs = ["enumerate", "reference", "packing_reference", "complete"]
    if args.independent:
        programs += ["packing_weighted", "residual_reference"]
    for name in programs:
        subprocess.run([
            "g++", "-std=c++20", "-O3", "-Wall", "-Wextra", "-Wconversion", "-Wshadow",
            "-Werror", str(SOURCE / (name + ".cpp")), "-o", str(work / name),
        ], check=True)

    weights = list(map(int, (SOURCE / "weights.txt").read_text().split()))
    assert len(weights) == 85 and min(weights) >= 0 and max(weights) <= 111111
    assert sum(weights) == 7899969
    reports = {}
    for k in (10, 11, 12):
        output = work / "sets85_11.txt" if k == 11 else "-"
        command = [work / "enumerate", 85, k, "all", output]
        if k != 12:
            command += [SOURCE / "weights.txt"]
        report = run(command)
        assert report["complete"] and report["sets"] == {10: 49479804, 11: 56110, 12: 0}[k]
        if k != 12:
            assert report["max_weight"] == {10: 999996, 11: 999995}[k]
        reports[f"enumerate_{k}"] = report
        print(json.dumps(report), flush=True)
    check_hash(work / "sets85_11.txt")
    rows = read_sets(work / "sets85_11.txt")
    rows.sort(key=lambda a: (-sum(weights[x] for x in a), sum(1 << x for x in a)))
    (work / "ordered_sets.txt").write_text("".join(" ".join(map(str, a)) + "\n" for a in rows))
    check_hash(work / "ordered_sets.txt")
    packing = run([work / "packing_reference", work / "ordered_sets.txt", SOURCE / "weights.txt", work / "packings.txt"])
    assert packing["complete"] and packing["packings"] == 130780
    check_hash(work / "packings.txt")
    reports["packing"] = packing
    print(json.dumps(packing), flush=True)

    tuples = [tuple(map(int, line.split())) for line in (work / "packings.txt").read_text().splitlines()]
    assert len(tuples) == len(set(tuples)) == 130780
    masks = [sum(1 << x for x in row) for row in rows]
    residual_masks = set()
    for ids in tuples:
        assert len(ids) == 5 and tuple(sorted(set(ids))) == ids
        union = 0
        for i in ids:
            assert 0 <= i < len(rows) and not union & masks[i]
            union |= masks[i]
        residual_masks.add(((1 << 85) - 1) ^ union)
        assert sum(sum(weights[x] for x in rows[i]) for i in ids) >= 4899969
    assert len(residual_masks) == 130780

    # Positive controls for every possible sorted size profile of a 30-point remainder.
    for sizes in ((10, 10, 10), (11, 10, 9), (11, 11, 8)):
        residual = sorted(x for i, size in zip(tuples[0][:3], sizes) for x in rows[i][:size])
        assert len(residual) == len(set(residual)) == 30
        path = work / ("positive_" + "_".join(map(str, sizes)) + ".txt")
        path.write_text(" ".join(map(str, residual)) + "\n")
        result = run([work / "complete", "--residual", path])
        assert result["found"]
        decoded = [[x - 1 for x in part] for part in result["partition"]]
        assert sorted(x for part in decoded for x in part) == residual
        assert all(sidon(part) for part in decoded)
        if args.independent:
            assert run([work / "residual_reference", "--residual", path])["found"]

    for i in range(args.jobs):
        (work / f"chunk_{i}.txt").write_text("".join(" ".join(map(str, ids)) + "\n" for ids in tuples[i::args.jobs]))

    def complete_part(i):
        result = run([work / "complete", 85, work / "ordered_sets.txt", work / f"chunk_{i}.txt"])
        assert not result["found"] and result["input_read_complete"]
        assert result["tuples"] == len(tuples[i::args.jobs])
        (work / f"completion_{i}.json").write_text(json.dumps(result) + "\n")
        return result

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        reports["completions"] = list(pool.map(complete_part, range(args.jobs)))
    assert sum(r["tuples"] for r in reports["completions"]) == 130780
    assert sum(r["ten_sets"] for r in reports["completions"]) == 1487970
    assert sum(r["eleven_sets"] for r in reports["completions"]) == 26

    if args.independent:
        reference = run([work / "reference", 85, 11, work / "reference_sets.txt"])
        assert reference["complete"] and reference["sets"] == 56110
        assert set(read_sets(work / "reference_sets.txt")) == set(rows)
        assert run([work / "reference", 85, 12])["sets"] == 0
        other = run([work / "packing_weighted", 85, 11, 5, work / "sets85_11.txt", SOURCE / "weights.txt", work / "other_packings.txt"])
        assert other["complete"] and other["packings"] == 130780
        check_hash(work / "other_packings.txt", "packings.txt")
        check_hash(work / "other_packings.txt.sets", "ordered_sets.txt")

        def reference_part(i):
            result = run([work / "residual_reference", work / "ordered_sets.txt", work / f"chunk_{i}.txt"])
            expected = reports["completions"][i]
            assert result["all_unsatisfiable"] and result["tested"] == expected["tuples"]
            assert result["ten_sets"] == expected["ten_sets"] and result["eleven_sets"] == expected["eleven_sets"]
            (work / f"reference_completion_{i}.json").write_text(json.dumps(result) + "\n")
            return result

        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            reports["reference_completions"] = list(pool.map(reference_part, range(args.jobs)))
    reports["seconds"] = time.monotonic() - started
    reports["conclusion"] = "SR(8) <= 85"
    (work / "verification.json").write_text(json.dumps(reports, indent=2) + "\n")
    print(json.dumps({"verified": True, "bound": "SR(8) <= 85", "independent": args.independent, "seconds": reports["seconds"]}))


if __name__ == "__main__":
    main()
