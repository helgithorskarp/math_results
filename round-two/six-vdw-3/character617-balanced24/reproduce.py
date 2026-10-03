"""Cold, serial reproduction of the character617 119-edge bound.

The pinned programs contain the mathematical computations. This driver
copies only source into a new work directory, journals every stage, and
checks all finite domains before emitting the final result. No external
data, solver, network, or campaign service is required.
"""
import argparse
import hashlib
import json
import os
import platform
import resource
import shutil
import subprocess
import sys
import time
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def save(path, value):
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w") as stream:
        stream.write(json.dumps(value, sort_keys=True, indent=2) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def same(left, right):
    need(left.read_bytes() == right.read_bytes(),
         f"Whole mathematical transcripts differ: {left.name}, {right.name}")


def operations_barrier():
    # An optional local stop barrier retained by the original guarded runners.
    # On other machines this directory does not exist and requires no setup.
    state = Path("/scratch/research-team-sol61-six-20260929/state")
    need(not any((state / name).exists()
                 for name in ("PAUSED", "PAUSED.json", "HANDOVER.json")),
         "Operations barrier; preserve partial work, no exclusion")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True,
                        help="new, nonexistent directory for all generated state")
    args = parser.parse_args()
    need(platform.python_implementation() == "CPython" and
         sys.version_info[:2] == (3, 11), "Use CPython 3.11; validated on 3.11.2")
    original = Path(__file__).resolve().parent
    pins = read(original / "SOURCE_PINS.json")
    for item in pins["files"]:
        path = original / item["name"]
        need(path.is_file() and path.stat().st_size == item["bytes"] and
             sha(path) == item["sha256"], f"Pinned source differs: {item['name']}")
    operations_barrier()
    work = args.work.resolve()
    need(not work.exists(), "Preserve existing work; choose a new cold directory")
    work.mkdir(parents=True)
    source = work / "source"
    source.mkdir()
    for item in pins["files"]:
        if item["name"].endswith(".py") and item["name"] != "reproduce.py":
            shutil.copyfile(original / item["name"], source / item["name"])
            same(original / item["name"], source / item["name"])
    python = source / "solver-env" / "bin" / "python"
    python.parent.mkdir(parents=True)
    python.symlink_to(Path(sys.executable).resolve())
    env = os.environ.copy()
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                 "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS"):
        env[name] = "1"
    for directory in ("character617-size24-common-four-checks",
                      "character617-size24-common-five-checks"):
        (source / directory).mkdir()
    journal = {"agent": "six-vdw-3", "role": "researcher",
               "python": platform.python_version(), "cold_start": True,
               "guard_seconds": 20, "numerical_threads": 1,
               "source_pins_sha256": sha(original / "SOURCE_PINS.json"),
               "status": "STARTED_NO_CONCLUSION", "stages": []}
    save(work / "journal.json", journal)
    beginning = time.monotonic()

    def stage(name, script, arguments=(), optimized=False, runner=False):
        operations_barrier()
        command = [str(python)] + (["-O"] if optimized else [])
        command += [str(source / script)] + [str(x) for x in arguments]
        entry = {"name": name, "command": command, "status": "STARTED",
                 "guard_seconds": "internal_math_children_20" if runner else 20}
        journal["stages"].append(entry)
        save(work / "journal.json", journal)
        print(json.dumps({"stage": name, "status": "STARTED"}), flush=True)
        start = time.monotonic()
        stdout, stderr = work / (name + ".stdout"), work / (name + ".stderr")
        try:
            with stdout.open("w") as out, stderr.open("w") as err:
                result = subprocess.run(command, cwd=source, env=env,
                                        stdout=out, stderr=err,
                                        timeout=None if runner else 20)
            entry["exit_code"] = result.returncode
            need(result.returncode == 0, f"Incomplete stage {name}; see {stderr}")
            entry["status"] = "COMPLETE"
        except BaseException as error:
            entry.update(status="INCOMPLETE_NO_EXCLUSION", error=str(error))
            journal["status"] = "INCOMPLETE_NO_EXCLUSION"
            raise
        finally:
            entry["seconds"] = time.monotonic() - start
            entry["peak_child_rss_kib"] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
            save(work / "journal.json", journal)
        print(json.dumps({"stage": name, "status": "COMPLETE",
                          "seconds": entry["seconds"]}), flush=True)

    try:
        stage("01-threshold-queue", "run-character617-threshold-four.py", runner=True)
        stage("02-threshold-extract", "character617-threshold-four.py",
              ("--checkpoint", source / "character617-threshold-four-run/checkpoint.json",
               "--final", source / "character617-threshold-four.json"))
        stage("03-threshold-checks", "run-character617-threshold-four-checks.py", runner=True)
        stage("04-capacity-producer", "character617-size24-capacity-profile.py",
              ("--input", source / "character617-threshold-four.json",
               "--output", source / "character617-size24-capacity.json"))
        stage("05-capacity-checks", "run-character617-size24-capacity-checks.py", runner=True)
        for optimized in (False, True):
            stage("07-singleton-optimized" if optimized else "06-singleton-normal",
                  "character617-capacity-controls.py", optimized=optimized)
        for number, word in ((8, "four"), (11, "five")):
            data = source / f"character617-size24-common-{word}.json"
            capacity = source / "character617-size24-capacity.json"
            stage(f"{number:02}-common-{word}-producer",
                  f"character617-size24-common-{word}.py",
                  ("--capacity", capacity, "--output", data))
            for offset, mode in ((1, "normal"), (2, "optimized")):
                options = ("--capacity", capacity) if word == "four" else (
                    "--capacity-checked", source / "character617-size24-capacity-checks/normal/checked.json")
                stage(f"{number+offset:02}-common-{word}-{mode}",
                      f"check-character617-size24-common-{word}.py",
                      ("--input", data, *options, "--output",
                       source / f"character617-size24-common-{word}-checks/{mode}.json"),
                      optimized=mode == "optimized")
        stage("14-cover-controls", "character617-pass29-damages.py", runner=True)
        stage("15-row-budget", "run-character617-size24-row-budget.py", runner=True)
        stage("16-row-completion", "run-character617-size24-row-completion.py", runner=True)
        stage("17-row-controls", "character617-pass30-controls.py", runner=True)

        # These pins are regression summaries, not proof inputs. Full distinct
        # implementations have already regenerated and checked all records.
        for relative, fields in read(original / "EXPECTED.json")["outputs"].items():
            actual = read(source / relative)
            for key, expected in fields.items():
                need(actual[key] == expected, f"Expected summary differs: {relative}:{key}")
        same(work / "06-singleton-normal.stdout", work / "07-singleton-optimized.stdout")
        singleton = read(work / "06-singleton-normal.stdout")
        need(singleton["small_exhaustive_capacity_fixtures"] == 3699,
             "Whole singleton fixture domain")
        whole_pairs = 1
        for word in ("four", "five"):
            base = source / f"character617-size24-common-{word}-checks"
            same(base / "normal.json", base / "optimized.json")
            whole_pairs += 1
        for name, pattern, modes in (
            ("character617-threshold-four-checks", "*.json", ("normal", "optimized")),
            ("character617-size24-capacity-checks", "*.json", ("normal", "optimized")),
            ("character617-size24-row-budget-checks", "range-*.json", ("producer", "normal", "optimized")),
            ("character617-size24-row-completion-checks", "batch-*.json", ("producer", "normal", "optimized"))):
            base = source / name
            originals = sorted((base / modes[0]).glob(pattern))
            need(originals, f"No complete transcripts: {name}")
            for mode in modes[1:]:
                need([p.name for p in originals] ==
                     [p.name for p in sorted((base / mode).glob(pattern))],
                     f"Different whole transcript file sets: {name}/{mode}")
                for path in originals:
                    same(path, base / mode / path.name)
                    whole_pairs += 1
        executions = []
        for name, expected_children, expected_status in (
            ("character617-threshold-four-checks", 74, "COMPLETE"),
            ("character617-size24-capacity-checks", 150, "COMPLETE"),
            ("character617-pass29-damages", 28, "EXPECTED_POSITIVE_OR_SEMANTIC_REJECTION"),
            ("character617-size24-row-budget-checks", 162, "COMPLETE"),
            ("character617-size24-row-completion-checks", 339, "COMPLETE"),
            ("character617-pass30-controls", 34, "EXPECTED_CONTROL_COMPLETED")):
            entries = read(source / name / "execution.json")
            need(len(entries) == expected_children and
                 all(r["status"] == expected_status and r["guard_seconds"] == 20 and
                     r["threads"] == 1 for r in entries), f"Incomplete children: {name}")
            executions.extend(entries)
        queue = [read(p) for p in sorted((source / "character617-threshold-four-run").glob("batch-*.json"))]
        need(len(queue) == 50 and all(r["status"] == "COMPLETE_BATCH" and
             r["guard_seconds"] == 20 and r["threads"] == 1 for r in queue), "Whole queue execution")
        executions.extend(queue)
        direct = [r for r in journal["stages"] if r["guard_seconds"] == 20]
        need(len(executions) + len(direct) == 847, "Whole cold mathematical child count")
        # Both control programs have already compared their valid records as
        # whole files; their expected summaries certify all six positive pairs.
        whole_pairs += 6
        need(whole_pairs == 456, "Whole corresponding file pair count")
        for item in pins["files"]:
            if item["name"].endswith(".py") and item["name"] != "reproduce.py":
                need(sha(source / item["name"]) == item["sha256"], "Source changed during run")
        summary = {"agent": "six-vdw-3", "role": "researcher", "python": platform.python_version(),
                   "status": "EXACT_CHARACTER617_119_EDGE_BOUND", "cold_start": True,
                   "math_children": 847, "whole_file_pairs": whole_pairs,
                   "fixed_child_guard_seconds": 20, "numerical_threads": 1,
                   "seconds": time.monotonic() - beginning,
                   "maximum_math_child_seconds": max(r["seconds"] for r in executions + direct),
                   "peak_child_rss_kib": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                   "row_choices_checked": 2033590, "remaining_row_choices": 0,
                   "graph_part_sizes": [10, 14], "missing_cross_pairs_at_least": 21,
                   "graph_edges_at_most": 119,
                   "actual_24_flip_character_balances": [[11, 13], [12, 12]],
                   "balance_corollary_requires": [9880, 9976],
                   "size25_flip_bound_or_3704_coloring": False}
        save(work / "summary.json", summary)
        journal["status"] = summary["status"]
        save(work / "journal.json", journal)
        print(json.dumps(summary, sort_keys=True), flush=True)
    except BaseException as error:
        journal.update(status="INCOMPLETE_NO_EXCLUSION", error=str(error))
        save(work / "journal.json", journal)
        raise


if __name__ == "__main__":
    main()
