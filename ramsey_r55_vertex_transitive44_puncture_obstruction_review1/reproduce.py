#!/usr/bin/env python3
"""Reproduce the pinned h3963 source and its independent review."""

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
SOURCE_COMMIT = "b64588fddf2267c4261b2520e40841dc3c1bab89"
TARGET_DIRECTORY = "ramsey_r55_vertex_transitive44_puncture_obstruction"
CAYLEY_DIRECTORY = "ramsey_r55_cayley44_puncture_obstruction"


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
    archive = run(["git", "archive", SOURCE_COMMIT,
                   TARGET_DIRECTORY, CAYLEY_DIRECTORY], repo)
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


def independent_receipt(snapshot, optimized):
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([
        "-B", str(HERE / "independent_check.py"),
        "--catalog", str(snapshot / TARGET_DIRECTORY / "catalog.txt"),
        "--certificates",
        str(snapshot / TARGET_DIRECTORY / "certificates.json"),
        "--cayley", str(snapshot / CAYLEY_DIRECTORY),
    ])
    receipt = json.loads(run(command, HERE))
    elapsed = receipt.pop("elapsed_seconds")
    need(isinstance(elapsed, (int, float)) and elapsed > 0,
         "independent elapsed time")
    return receipt


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
    source_output = run([
        sys.executable, "-B",
        str(snapshot / TARGET_DIRECTORY / "reproduce.py"),
    ], snapshot / TARGET_DIRECTORY, environment).decode().strip()
    need(source_output ==
         "REPRODUCED_COMPLETE_VERTEX_TRANSITIVE44_PUNCTURE_EXCLUSION",
         "reviewed source status")

    normal = independent_receipt(snapshot, False)
    optimized = independent_receipt(snapshot, True)
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    need(normal == optimized == expected,
         "independent modes or expected receipt")
    print(json.dumps({
        "catalog_actions": expected["catalog_actions"],
        "independent_modes_equal": True,
        "physical_core_partitions": expected["physical_cores"]["partitions"],
        "regular_actions_direct": len(expected["regular_actions_direct"]),
        "review_manifest_entries": len(manifest),
        "reviewed_source_commit": SOURCE_COMMIT,
        "source_reproduced": True,
        "status": "REPRODUCED_ACCEPT_REVIEW_H3963",
        "target_result_established": False,
        "transgrp_completeness_imported": True
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
