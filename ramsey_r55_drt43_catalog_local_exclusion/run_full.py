#!/usr/bin/env python3
"""Compile and run the complete transient-DRAT certification."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

from merge_results import merge

RECORDS = 2178


def ranges(jobs: int) -> list[tuple[int, int]]:
    quotient, remainder = divmod(RECORDS, jobs)
    answer = []
    first = 0
    for shard in range(jobs):
        count = quotient + (shard < remainder)
        answer.append((first, count))
        first += count
    assert first == RECORDS
    return answer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--cadical-dir", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=10)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--work", type=Path)
    args = parser.parse_args()
    if not 1 <= args.jobs <= RECORDS:
        raise ValueError("jobs must lie between 1 and 2178")

    package = Path(__file__).resolve().parent
    work = args.work or Path(tempfile.mkdtemp(prefix="drt43-local-cert-"))
    work.mkdir(parents=True, exist_ok=True)
    binary = work / "certify"
    compile_command = [
        "g++", "-O3", "-std=c++20", "-Wall", "-Wextra", "-Werror", "-pedantic",
        f"-I{args.cadical_dir / 'src'}", str(package / "certify.cpp"),
        str(args.cadical_dir / "build" / "libcadical.a"), "-lpthread", "-o", str(binary),
    ]
    subprocess.run(compile_command, check=True)

    processes: list[tuple[subprocess.Popen[bytes], object, object, Path]] = []
    summaries: list[Path] = []
    for first, count in ranges(args.jobs):
        shard = work / str(first)
        temporary = shard / "tmp"
        temporary.mkdir(parents=True, exist_ok=True)
        summary = shard / "summary.tsv"
        stdout = (shard / "stdout.txt").open("wb")
        stderr = (shard / "stderr.txt").open("wb")
        command = [
            str(binary), "--certify", str(args.catalog.resolve()), str(first), str(count), "43",
            str(args.drat_trim.resolve()), str(temporary), str(summary),
        ]
        processes.append((subprocess.Popen(command, stdout=stdout, stderr=stderr), stdout, stderr, shard))
        summaries.append(summary)

    failures = []
    for process, stdout, stderr, shard in processes:
        status = process.wait()
        stdout.close()
        stderr.close()
        if status != 0:
            failures.append((shard, status))
    if failures:
        raise RuntimeError(f"certification shard failures (artifacts retained in {work}): {failures}")

    merge(summaries, args.output)
    subprocess.run(
        ["python3", "-B", str(package / "audit.py"), "--catalog", str(args.catalog),
         "--result", str(args.output)],
        check=True,
    )
    print(f"CERTIFIED_COMPLETE_DRT43_PARTIAL_CATALOG output={args.output} work={work}")


if __name__ == "__main__":
    main()
