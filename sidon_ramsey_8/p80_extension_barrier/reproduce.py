#!/usr/bin/env python3
"""Regenerate and verify the P80 seed extension obstruction using only stdlib and GCC."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import filecmp
import hashlib
import itertools
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def check_partition(partition, points, classes):
    require(len(partition) == classes, "wrong number of classes")
    require(sorted(x for row in partition for x in row) == points, "wrong coverage")
    for row in partition:
        sums = [a + b for a, b in itertools.combinations_with_replacement(row, 2)]
        require(len(set(sums)) == len(sums), "repeated unordered pair sum")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--independent", action="store_true")
    args = parser.parse_args()
    require(__debug__, "run without Python -O")
    require(args.jobs > 0, "jobs must be positive")
    source = Path(__file__).resolve().parent
    work = args.work.resolve()
    repository = source.parents[1]
    require(work != repository and repository not in work.parents, "work must be outside repository")
    work.mkdir(parents=True, exist_ok=True)
    expected = json.loads((source / "expected.json").read_text())
    base = [list(map(int, line.split())) for line in (source / "partition80.txt").read_text().splitlines()]
    check_partition(base, list(range(1, 81)), 8)
    require(all(len(row) == 10 for row in base), "seed sizes")
    start = time.monotonic()
    compiler = os.environ.get("CXX", "g++")
    flags = ["-O3", "-std=c++20", "-Wall", "-Wextra", "-Wconversion", "-Werror"]
    binary = work / "verify"
    subprocess.run([compiler, *flags, str(source / "verify.cpp"), "-o", str(binary)], check=True)
    methods = [0, 1] if args.independent else [0]

    def run_case(case):
        shift, method = case
        stem = work / f"shift{shift}_method{method}"
        trace = stem.with_suffix(".bin")
        command = [str(binary), str(source / "partition80.txt"), str(shift), str(method), str(trace)]
        with stem.with_suffix(".log").open("w") as log:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=log, text=True, check=True)
        record = json.loads(result.stdout)
        stem.with_suffix(".json").write_text(json.dumps(record, indent=2) + "\n")
        require(record["shift"] == shift and record["method"] == method, "case identity")
        for key, value in expected["runs"][str(shift)].items():
            require(record.get(key) == value, f"case {case}: mismatch at {key}")
        trace_record = {"bytes": trace.stat().st_size, "sha256": digest(trace)}
        require(trace_record == expected["traces"][str(shift)], "catalog trace mismatch")
        print(json.dumps({"shift": shift, "method": method, "verified": True}), flush=True)
        return record

    cases = [(shift, method) for shift in [0, 1] for method in methods]
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        runs = list(pool.map(run_case, cases))
    if args.independent:
        for shift in [0, 1]:
            require(filecmp.cmp(work / f"shift{shift}_method0.bin", work / f"shift{shift}_method1.bin", shallow=False), "catalogs differ entrywise")
    controls = []
    fixtures = json.loads((source / "positive_controls.json").read_text())
    for i, fixture in enumerate(fixtures):
        points = fixture["points"]
        require(len(points) == fixture["size"] and points == sorted(set(points)), "fixture domain")
        if "known_partition" in fixture:
            check_partition(fixture["known_partition"], points, len(fixture["witness_sizes"]))
        input_path = work / f"positive{i}.txt"
        input_path.write_text(" ".join(map(str, points)) + "\n")
        for method in methods:
            output = subprocess.check_output([str(binary), "--residual", str(method), str(input_path), str(work / f"positive{i}_{method}.bin")], text=True)
            result = json.loads(output)
            require(result["found"], "missed positive control")
            check_partition(result["partition"], points, len(fixture["witness_sizes"]))
            controls.append({"fixture": i, "method": method, "returned_sizes": sorted(map(len, result["partition"]))})
    report = {
        "claim": "No P81 partition retains three seed classes, for either seed shift.",
        "complete": True,
        "independent_methods": args.independent,
        "runs": runs,
        "traces": expected["traces"],
        "entrywise_equal": args.independent,
        "positive_controls": controls,
        "compiler": subprocess.check_output([compiler, "--version"], text=True).splitlines()[0],
        "flags": flags,
        "python": platform.python_version(),
        "machine": platform.machine(),
        "jobs": args.jobs,
        "wall_seconds": time.monotonic() - start,
        "max_child_rss_kb_linux": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        "source_sha256": digest(source / "verify.cpp"),
    }
    (work / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"complete": True, "independent": args.independent, "wall_seconds": report["wall_seconds"]}), flush=True)


if __name__ == "__main__":
    main()
