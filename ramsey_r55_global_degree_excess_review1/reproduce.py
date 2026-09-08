#!/usr/bin/env python3
"""Reproduce the pinned h4009 source and independent review."""

from __future__ import annotations

import argparse
from hashlib import sha256
from io import BytesIO
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile


HERE = Path(__file__).resolve().parent
SOURCE_COMMIT = "d1c2e7026b09696a72c72e1921b6f09500c21c29"
SOURCE_DIRECTORY = "ramsey_r55_global_degree_excess"
PARENT_DIRECTORY = "ramsey_r55_regular18_overlap_exclusion"


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def run(command, cwd, environment=None):
    completed = subprocess.run(
        command, cwd=cwd, env=environment,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if completed.returncode:
        sys.stderr.buffer.write(completed.stderr)
        raise RuntimeError(f"command failed ({completed.returncode}): {command}")
    need(not completed.stderr, f"unexpected stderr: {command}")
    return completed.stdout


def verify_review_manifest():
    names = []
    for line in (HERE / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split("  ", 1)
        need(Path(name).name == name and name not in names,
             "review manifest path")
        need(sha256((HERE / name).read_bytes()).hexdigest() == digest,
             "review manifest hash " + name)
        names.append(name)
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    need(set(names) == actual - {"SHA256SUMS"}, "review manifest file set")
    return names


def extract_source(repo, destination):
    destination.mkdir(parents=True)
    resolved = run(
        ["git", "rev-parse", "--verify", f"{SOURCE_COMMIT}^{{commit}}"], repo
    )
    need(resolved.decode().strip() == SOURCE_COMMIT, "source commit identity")
    archive = run(
        ["git", "archive", SOURCE_COMMIT, SOURCE_DIRECTORY, PARENT_DIRECTORY], repo
    )
    root = destination.resolve()
    with tarfile.open(fileobj=BytesIO(archive), mode="r:") as stream:
        members = stream.getmembers()
        for member in members:
            target = (destination / member.name).resolve()
            need(target == root or root in target.parents, "unsafe archive member")
            need(member.isfile() or member.isdir(), "unexpected archive member")
        stream.extractall(destination, members=members)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", type=Path)
    parser.add_argument("catalog", type=Path)
    parser.add_argument("work", type=Path)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    catalog = args.catalog.resolve()
    work = args.work.resolve()
    need((repo / ".git").exists(), "repo_root is not a Git worktree")
    need(catalog.is_file(), "catalog input")
    need(not work.exists(), "work path must not exist")
    work.mkdir(parents=True)
    review_manifest = verify_review_manifest()

    snapshot = work / "snapshot"
    extract_source(repo, snapshot)
    source_tmp = work / "source-tmp"
    source_tmp.mkdir()
    environment = os.environ.copy()
    environment["TMPDIR"] = str(source_tmp)
    source_receipt = json.loads(run([
        sys.executable, "-B", str(snapshot / SOURCE_DIRECTORY / "reproduce.py"),
        "--catalog", str(catalog),
    ], snapshot, environment))
    need(source_receipt == {
        "certificate_sha256":
            "d030ea15e9529f3dcf6fdefb03f3f64e8eff75cf23aa9359152cce23338c06fe",
        "edge_window": [390, 513],
        "normal_and_optimized_agree": True,
        "status": "REPRODUCED_GLOBAL_GOOD43_EDGE_WINDOW",
        "target_found": False,
    }, "reviewed source receipt")

    receipts = []
    for optimized in (False, True):
        command = [sys.executable]
        if optimized:
            command.append("-O")
        command.extend([
            "-B", str(HERE / "independent_check.py"),
            str(snapshot), str(catalog),
        ])
        receipts.append(json.loads(run(command, HERE, environment)))
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    need(receipts[0] == receipts[1] == expected,
         "independent modes or expected receipt")

    print(json.dumps({
        "catalog_records": expected["catalog_records"],
        "edge_window": expected["edge_window"],
        "independent_modes_equal": True,
        "profile_pairs": expected["profile_pairs"],
        "review_manifest_entries": len(review_manifest),
        "reviewed_source_commit": SOURCE_COMMIT,
        "source_modes_equal": source_receipt["normal_and_optimized_agree"],
        "status": "REPRODUCED_ACCEPT_REVIEW_H4009",
        "surviving_profile_pairs": expected["surviving_profile_pairs"],
        "target_result_established": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
