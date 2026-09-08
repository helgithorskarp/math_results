#!/usr/bin/env python3
"""Reproduce the pinned h3975 source and independent review."""

from hashlib import sha256
from io import BytesIO
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile


HERE = Path(__file__).resolve().parent
SOURCE_COMMIT = "379a6369935a0ca0ee5ec61f8503ef64cee6fd1f"
SOURCE_DIRECTORY = "ramsey_r55_orbit_dense_deletion"


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def run(command, cwd, environment=None):
    completed = subprocess.run(command, cwd=cwd, env=environment,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, check=False)
    if completed.returncode:
        sys.stderr.buffer.write(completed.stderr)
        raise RuntimeError(f"command failed ({completed.returncode}): {command}")
    need(not completed.stderr, f"unexpected stderr: {command}")
    return completed.stdout


def verify_review_manifest():
    names = []
    for row in (HERE / "SHA256SUMS").read_text().splitlines():
        expected, name = row.split("  ", 1)
        need(Path(name).name == name and name not in names,
             "review manifest path")
        need(sha256((HERE / name).read_bytes()).hexdigest() == expected,
             "review manifest hash " + name)
        names.append(name)
    present = {path.name for path in HERE.iterdir() if path.is_file()}
    need(set(names) == present - {"SHA256SUMS"},
         "review manifest file set")
    return names


def extract_source(repo, destination):
    destination.mkdir()
    resolved = run(["git", "rev-parse", "--verify",
                    f"{SOURCE_COMMIT}^{{commit}}"], repo)
    need(resolved.decode().strip() == SOURCE_COMMIT, "source commit identity")
    archive = run(["git", "archive", SOURCE_COMMIT, SOURCE_DIRECTORY], repo)
    root = destination.resolve()
    with tarfile.open(fileobj=BytesIO(archive), mode="r:") as stream:
        members = stream.getmembers()
        for member in members:
            target = (destination / member.name).resolve()
            need(target == root or root in target.parents,
                 "unsafe archive member")
            need(member.isfile() or member.isdir(),
                 "unexpected archive member")
        stream.extractall(destination, members=members)


def independent_receipt(source, work, optimized):
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(HERE / "independent_check.py"),
                    str(source), str(work)])
    return json.loads(run(command, HERE))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", type=Path)
    parser.add_argument("work", type=Path)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    work = args.work.resolve()
    need((repo / ".git").is_dir(), "repo_root is not a Git worktree")
    need(not work.exists(), "work path must not exist")
    work.mkdir(parents=True)
    environment = os.environ.copy()
    environment["TMPDIR"] = str(work / "tmp")
    Path(environment["TMPDIR"]).mkdir()

    manifest = verify_review_manifest()
    snapshot = work / "snapshot"
    extract_source(repo, snapshot)
    source = snapshot / SOURCE_DIRECTORY
    source_receipt = json.loads(run(
        [sys.executable, "-B", str(source / "reproduce.py")],
        source, environment))
    need(source_receipt.pop("elapsed_seconds") > 0,
         "source elapsed time")
    need(source_receipt.pop("max_child_rss_kib") > 0,
         "source resource usage")
    need(source_receipt == {
        "status": "REPRODUCED_COMPLETE_ORBIT_DENSE_DELETION_CERTIFICATES",
        "modes": ["normal", "assertions_disabled"],
        "physical_fixtures_per_mode": 7,
        "literal_physical_pairs_per_mode": 70,
        "paley_physical_jobs_excluded": 19499099620,
        "two_orbit_physical_parameter_jobs_excluded":
            77948453671476024416665600,
        "new_solver_calls": 0,
        "target43_found": False,
    }, "reviewed source receipt")

    normal = independent_receipt(source, work / "independent-normal", False)
    optimized = independent_receipt(source, work / "independent-optimized", True)
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    need(normal == optimized == expected,
         "independent modes or expected receipt")
    print(json.dumps({
        "independent_modes_equal": True,
        "paley_physical_jobs_excluded":
            expected["paley53"]["physical_subset_jobs_excluded"],
        "review_manifest_entries": len(manifest),
        "reviewed_source_commit": SOURCE_COMMIT,
        "source_reproduced": True,
        "status": "REPRODUCED_ACCEPT_REVIEW_H3975",
        "target43_found": False,
        "two_orbit_physical_parameter_jobs_excluded":
            expected["two_cycle_template53"]
                    ["physical_parameter_jobs_excluded"],
        "upper_bound_imported": True,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
