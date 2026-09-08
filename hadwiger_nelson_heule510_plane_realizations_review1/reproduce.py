#!/usr/bin/env python3
"""Reproduce the exact h3945 source checks and independent review."""

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
SOURCE_COMMIT = "70bd2363ee5505770eb54d3fd089a640d2c6a653"
PACKAGE = "hadwiger_nelson_heule510_plane_realizations"
SIBLING = "hadwiger_nelson_parts509_heule_union_minimum"
ARCHIVE_PATHS = (
    PACKAGE,
    f"{SIBLING}/aligned_510.json",
    f"{SIBLING}/union_510.json",
)


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def run(command, cwd):
    completed = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, check=False)
    if completed.returncode:
        sys.stderr.buffer.write(completed.stderr)
        raise RuntimeError(f"command failed ({completed.returncode}): {command}")
    return completed.stdout


def extract_snapshot(repo: Path, work: Path):
    resolved = run(["git", "rev-parse", "--verify", f"{SOURCE_COMMIT}^{{commit}}"], repo)
    require(resolved.decode().strip() == SOURCE_COMMIT, "source commit identity")
    archive = run(["git", "archive", SOURCE_COMMIT, *ARCHIVE_PATHS], repo)
    destination = work.resolve()
    with tarfile.open(fileobj=BytesIO(archive), mode="r:") as stream:
        members = stream.getmembers()
        for member in members:
            target = (work / member.name).resolve()
            require(target == destination or destination in target.parents, "unsafe archive member")
            require(member.isfile() or member.isdir(), "unexpected archive member type")
        stream.extractall(work, members=members)


def verify_manifest(package: Path):
    listed = []
    for line in (package / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split(None, 1)
        path = package / name
        require(path.is_file(), f"missing manifest file: {name}")
        require(sha256(path.read_bytes()).hexdigest() == digest, f"manifest mismatch: {name}")
        listed.append(name)
    require(len(listed) == 9 and len(set(listed)) == 9, "source manifest cardinality")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", type=Path)
    parser.add_argument("work", type=Path)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    work = args.work.resolve()
    require((repo / ".git").exists(), "repo_root is not a Git worktree")
    require(not work.exists(), "work path must not exist")
    work.mkdir(parents=True)
    extract_snapshot(repo, work)

    package = work / PACKAGE
    verify_manifest(package)
    python = sys.executable
    source_verify = run([python, "-B", "verify.py"], package)
    source_verify_o = run([python, "-O", "-B", "verify.py"], package)
    require(source_verify == source_verify_o == (package / "expected.json").read_bytes(),
            "source verifier output")
    source_controls = run([python, "-B", "controls.py"], package)
    source_controls_o = run([python, "-O", "-B", "controls.py"], package)
    require(source_controls == source_controls_o == (package / "controls_expected.json").read_bytes(),
            "source control output")

    generated = work / "generated"
    run([python, "-B", "generate.py", "--out", str(generated)], package)
    require((generated / "certificate.json").read_bytes() == (package / "certificate.json").read_bytes(),
            "deterministic source certificate replay")

    controls = run([python, "-B", str(HERE / "reviewer_controls.py")], HERE)
    controls_o = run([python, "-O", "-B", str(HERE / "reviewer_controls.py")], HERE)
    require(controls == controls_o == (HERE / "CONTROLS_EXPECTED.json").read_bytes(),
            "reviewer controls")

    audit = run([python, "-B", str(HERE / "independent_audit.py"), str(work)], HERE)
    audit_o = run([python, "-O", "-B", str(HERE / "independent_audit.py"), str(work)], HERE)
    require(audit == audit_o == (HERE / "EXPECTED.json").read_bytes(), "independent audit output")

    report = {
        "independent_audit_sha256": sha256(audit).hexdigest(),
        "reviewed_source_commit": SOURCE_COMMIT,
        "source_certificate_sha256": sha256((package / "certificate.json").read_bytes()).hexdigest(),
        "status": "REPRODUCED_ACCEPT_REVIEW_H3945",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
