#!/usr/bin/env python3
"""Reproduce the pinned h3947 package and its independent review."""

from __future__ import annotations

import argparse
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import subprocess
import sys
import tarfile


HERE = Path(__file__).resolve().parent
SOURCE_COMMIT = "bd9db0fdcb30ec1dc6013c31174114d5a3791749"
SOURCE_DIRECTORY = "ramsey_r55_pentagon_product_extension_obstruction"
ARCHIVE_PATHS = (
    SOURCE_DIRECTORY,
    "ramsey_r55_path_complement_core_exclusion/WITNESSES.json",
)


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def run(command, cwd):
    completed = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, check=False)
    if completed.returncode:
        sys.stderr.buffer.write(completed.stderr)
        raise RuntimeError(f"command failed ({completed.returncode}): {command}")
    need(not completed.stderr, f"unexpected stderr: {command}")
    return completed.stdout


def extract_snapshot(repo, work):
    work.mkdir(parents=True)
    resolved = run(["git", "rev-parse", "--verify", f"{SOURCE_COMMIT}^{{commit}}"], repo)
    need(resolved.decode().strip() == SOURCE_COMMIT, "source commit identity")
    archive = run(["git", "archive", SOURCE_COMMIT, *ARCHIVE_PATHS], repo)
    destination = work.resolve()
    with tarfile.open(fileobj=BytesIO(archive), mode="r:") as stream:
        members = stream.getmembers()
        for member in members:
            target = (work / member.name).resolve()
            need(target == destination or destination in target.parents,
                 "unsafe archive member")
            need(member.isfile() or member.isdir(), "unexpected archive member")
        stream.extractall(work, members=members)


def verify_review_manifest():
    entries = []
    for line in (HERE / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split("  ", 1)
        need(Path(name).name == name and name not in entries,
             "review manifest path")
        need(sha256((HERE / name).read_bytes()).hexdigest() == digest,
             "review manifest hash " + name)
        entries.append(name)
    need(set(entries) == {path.name for path in HERE.iterdir()
                          if path.is_file()} - {"SHA256SUMS"},
         "review manifest file set")
    return entries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", type=Path)
    parser.add_argument("work", type=Path)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    work = args.work.resolve()
    need((repo / ".git").exists(), "repo_root is not a Git worktree")
    need(not work.exists(), "work path must not exist")
    work.mkdir(parents=True)
    entries = verify_review_manifest()
    extract_snapshot(repo, work / "snapshot")
    snapshot = work / "snapshot"

    source_receipt = json.loads(run(
        [sys.executable, "-B", str(snapshot / SOURCE_DIRECTORY / "reproduce.py")],
        snapshot,
    ))
    need(source_receipt["status"] ==
         "REPRODUCED_COMPLETE_PENTAGON_PRODUCT_EXTENSION_EXCLUSION",
         "reviewed source status")

    receipts = []
    for label, optimized in (("normal", False), ("optimized", True)):
        command = [sys.executable]
        if optimized:
            command.append("-O")
        command.extend([
            "-B", str(HERE / "independent_check.py"), str(snapshot),
            str(work / ("independent-" + label)),
        ])
        receipts.append(json.loads(run(command, HERE)))
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    need(receipts[0] == receipts[1] == expected,
         "independent modes or expected receipt")

    print(json.dumps({
        "attachment_words_covered": expected["attachment_words_covered"],
        "h3931_equality_witness_matches": True,
        "independent_modes_equal": True,
        "mark_avoiding_assignments": expected["mark_avoiding_assignments"],
        "review_manifest_entries": len(entries),
        "reviewed_source_commit": SOURCE_COMMIT,
        "source_modes_equal": source_receipt["replay_modes"] ==
                              ["normal", "assertions_disabled"],
        "status": "REPRODUCED_ACCEPT_REVIEW_H3947",
        "target_result_established": False,
        "target_solver_calls": 0,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
