#!/usr/bin/env python3
"""Reproduce the pinned h3981 source and an independent exact audit."""

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
SOURCE_COMMIT = "9b5f0b989aebbec953d20846d58150e1a0449405"
OBSTRUCTION_DIRECTORY = "hadwiger_nelson_301_repair_plane_obstruction"
GRAPH_DIRECTORY = "hadwiger_nelson_h516_k23free_edge_repair"
ARCHIVE_PATHS = (
    OBSTRUCTION_DIRECTORY,
    f"{GRAPH_DIRECTORY}/graph.json",
    f"{GRAPH_DIRECTORY}/five_colouring.json",
    f"{GRAPH_DIRECTORY}/four_colour.cnf",
    f"{GRAPH_DIRECTORY}/vertex_deletion_colours.json",
)


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
    archive = run(["git", "archive", SOURCE_COMMIT, *ARCHIVE_PATHS], repo)
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


def verify_source_manifest(source):
    names = []
    for row in (source / "SHA256SUMS").read_text().splitlines():
        expected, name = row.split("  ", 1)
        need(Path(name).name == name and name not in names,
             "source manifest path")
        need(sha256((source / name).read_bytes()).hexdigest() == expected,
             "source manifest hash " + name)
        names.append(name)
    present = {path.name for path in source.iterdir() if path.is_file()}
    need(set(names) == present - {"SHA256SUMS"},
         "source manifest file set")
    return names


def source_receipt(source, optimized, environment):
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(source / "verify.py"),
                    "--controls", "--positive"])
    return json.loads(run(command, source, environment))


def independent_receipt(snapshot, optimized, environment):
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([
        "-B", str(HERE / "independent_check.py"),
        str(snapshot / GRAPH_DIRECTORY / "graph.json"),
        str(snapshot / OBSTRUCTION_DIRECTORY / "certificate.json"),
    ])
    return json.loads(run(command, HERE, environment))


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

    review_manifest = verify_review_manifest()
    snapshot = work / "snapshot"
    extract_source(repo, snapshot)
    source = snapshot / OBSTRUCTION_DIRECTORY
    source_manifest = verify_source_manifest(source)
    source_expected = json.loads((source / "EXPECTED.json").read_text())
    source_normal = source_receipt(source, False, environment)
    source_optimized = source_receipt(source, True, environment)
    need(source_normal == source_optimized == source_expected,
         "source modes or source expected receipt")

    expected = json.loads((HERE / "EXPECTED.json").read_text())
    normal = independent_receipt(snapshot, False, environment)
    optimized = independent_receipt(snapshot, True, environment)
    need(normal == optimized == expected,
         "independent modes or expected receipt")
    print(json.dumps({
        "certificate_sha256": expected["certificate_sha256"],
        "independent_modes_equal": True,
        "maps_excluded": expected["maps_excluded"],
        "review_manifest_entries": len(review_manifest),
        "reviewed_source_commit": SOURCE_COMMIT,
        "source_manifest_entries": len(source_manifest),
        "source_modes_equal": True,
        "status": "REPRODUCED_ACCEPT_REVIEW_H3981",
        "target_unit_distance_graph_established": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
