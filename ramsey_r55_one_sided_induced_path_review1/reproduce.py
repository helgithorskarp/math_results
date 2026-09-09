#!/usr/bin/env python3
"""Reproduce the pinned h4015 source and independent review."""

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
SOURCE_COMMIT = "687178a20b787b5b53fba3ba90380b8e94063bee"
SOURCE_DIRECTORY = "ramsey_r55_one_sided_induced_path"


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
    archive = run(["git", "archive", SOURCE_COMMIT, SOURCE_DIRECTORY], repo)
    root = destination.resolve()
    with tarfile.open(fileobj=BytesIO(archive), mode="r:") as stream:
        members = stream.getmembers()
        for member in members:
            target = (destination / member.name).resolve()
            need(target == root or root in target.parents, "unsafe archive member")
            need(member.isfile() or member.isdir(), "unexpected archive member")
        stream.extractall(destination, members=members)


def source_expected():
    return {
        "all_formula_audits_and_proofs": "PASS",
        "complete_18_vertex_families": {
            "G1": {"clauses": 57596, "rup_additions": 275,
                   "variables": 75, "verified": True},
            "G2": {"clauses": 34197, "rup_additions": 77,
                   "variables": 62, "verified": True},
        },
        "imported_classification":
            "Cameron et al., arXiv:2005.03441v1, Theorem 7 (not reproduced)",
    }


def controls_expected():
    return {
        "corruptions_rejected": [
            "missing physical constraint", "unjustified empty clause"
        ],
        "status": "PASS",
        "two_variable_rup_soundness_checks": 4608,
    }


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
    review_manifest = verify_review_manifest()

    snapshot = work / "snapshot"
    extract_source(repo, snapshot)
    environment = os.environ.copy()
    environment["TMPDIR"] = str(work / "tmp")
    Path(environment["TMPDIR"]).mkdir()
    source_receipts = []
    control_receipts = []
    independent_receipts = []
    for label, optimized in (("normal", False), ("optimized", True)):
        interpreter = [sys.executable]
        if optimized:
            interpreter.append("-O")
        source_receipts.append(json.loads(run(
            interpreter + [
                "-B", str(snapshot / SOURCE_DIRECTORY / "reproduce.py"),
                "--out", str(work / ("source-" + label)),
            ], snapshot, environment
        )))
        control_receipts.append(json.loads(run(
            interpreter + [
                "-B", str(snapshot / SOURCE_DIRECTORY / "controls.py"),
                "--out", str(work / ("controls-" + label)),
            ], snapshot, environment
        )))
        independent_receipts.append(json.loads(run(
            interpreter + [
                "-B", str(HERE / "independent_check.py"), str(snapshot),
            ], HERE, environment
        )))

    expected = json.loads((HERE / "EXPECTED.json").read_text())
    need(source_receipts[0] == source_receipts[1] == source_expected(),
         "source modes or expected source receipt")
    need(control_receipts[0] == control_receipts[1] == controls_expected(),
         "control modes or expected control receipt")
    need(independent_receipts[0] == independent_receipts[1] == expected,
         "independent modes or expected receipt")

    print(json.dumps({
        "complete_extension_families": 2,
        "independent_modes_equal": True,
        "review_manifest_entries": len(review_manifest),
        "reviewed_source_commit": SOURCE_COMMIT,
        "source_and_control_modes_equal": True,
        "status": "REPRODUCED_ACCEPT_REVIEW_H4015",
        "surviving_extension_families":
            expected["surviving_extension_families"],
        "target_good43_constructed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
