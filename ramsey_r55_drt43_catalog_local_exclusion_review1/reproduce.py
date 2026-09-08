#!/usr/bin/env python3
"""Reproduce the pinned h3989 source audit and full independent review."""

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
SOURCE_COMMIT = "93242be92b95d9918582152fdd754014b44010de"
SOURCE_DIRECTORY = "ramsey_r55_drt43_catalog_local_exclusion"
CADICAL_COMMIT = "c60730422e758ef1cebe7aeddf2dda31c996bf04"
KISSAT_COMMIT = "8af8e56f174b778aef3aa45af9f739b2a5f492c2"


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
    return completed.stdout


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def verify_manifest(directory, exclude):
    names = []
    for row in (directory / "SHA256SUMS").read_text().splitlines():
        expected, name = row.split("  ", 1)
        need(Path(name).name == name and name not in names,
             "manifest path")
        need(digest(directory / name) == expected,
             "manifest hash " + name)
        names.append(name)
    present = {path.name for path in directory.iterdir() if path.is_file()}
    need(set(names) == present - set(exclude), "manifest file set")
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


def check_git_commit(directory, expected):
    actual = run(["git", "rev-parse", "HEAD"], directory).decode().strip()
    need(actual == expected, f"dependency commit {directory}")


def compile_cpp(source, output, include, library, sanitizer=False):
    flags = ["-O3"] if not sanitizer else [
        "-O1", "-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer"
    ]
    run([
        "g++", *flags, "-std=c++20", "-Wall", "-Wextra", "-Werror",
        "-pedantic", f"-I{include}", str(source), str(library),
        "-lpthread", "-o", str(output),
    ], HERE)


def cross_solver_controls(binary, catalog, expected, environment):
    receipts = []
    for item in expected:
        output = run([
            str(binary), str(catalog), str(item["record"]), "1", "1",
            str(item["root"]),
        ], HERE, environment).decode().splitlines()
        need(len(output) == 1, "cross-solver stdout")
        fields = output[0].split()
        need(fields[:4] == ["FINAL", "1", "1", "0"] and len(fields) == 5,
             "cross-solver status")
        receipts.append({
            "base_clauses": int(fields[4]),
            "record": item["record"],
            "root": item["root"],
            "status": "UNSAT",
        })
    need(receipts == expected, "cross-solver controls")
    return receipts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", type=Path)
    parser.add_argument("work", type=Path)
    parser.add_argument("--cadical-dir", type=Path, required=True)
    parser.add_argument("--kissat-dir", type=Path, required=True)
    parser.add_argument("--catalog", type=Path)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    work = args.work.resolve()
    cadical = args.cadical_dir.resolve()
    kissat = args.kissat_dir.resolve()
    need((repo / ".git").is_dir(), "repo_root is not a Git worktree")
    need(not work.exists(), "work path must not exist")
    work.mkdir(parents=True)
    environment = os.environ.copy()
    environment["TMPDIR"] = str(work / "tmp")
    Path(environment["TMPDIR"]).mkdir()

    review_manifest = verify_manifest(HERE, {"SHA256SUMS"})
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    snapshot = work / "snapshot"
    extract_source(repo, snapshot)
    source = snapshot / SOURCE_DIRECTORY
    source_manifest = verify_manifest(source, {".gitignore", "SHA256SUMS"})

    if args.catalog is None:
        catalog = work / "drtourn43some.txt"
        run([sys.executable, "-B", str(source / "fetch_catalog.py"),
             str(catalog)], source, environment)
    else:
        catalog = args.catalog.resolve()
    source_outputs = []
    for optimized in (False, True):
        command = [sys.executable]
        if optimized:
            command.append("-O")
        command.extend(["-B", str(source / "audit.py"),
                        "--catalog", str(catalog),
                        "--result", str(source / "RESULT.tsv")])
        source_outputs.append(run(command, source, environment).decode().strip())
    need(source_outputs == ["AUDITED_DRT43_CATALOG_LOCAL_EXCLUSION"] * 2,
         "source audit modes")

    check_git_commit(cadical, CADICAL_COMMIT)
    need(run([str(cadical / "build" / "cadical"), "--version"], HERE)
         .decode().strip() == "3.0.1", "CaDiCaL version")
    checker = work / "independent_check"
    compile_cpp(HERE / "independent_check.cpp", checker,
                cadical / "src", cadical / "build" / "libcadical.a")
    result = work / "INDEPENDENT_RESULT.tsv"
    full_stdout = run([
        str(checker), str(catalog), str(source / "RESULT.tsv"), str(result)
    ], HERE, environment).decode().strip()
    need(full_stdout == expected["full_checker_stdout"], "full checker stdout")
    need(digest(result) == expected["audit"]["independent_result_sha256"],
         "full independent result hash")

    audits = []
    for optimized in (False, True):
        command = [sys.executable]
        if optimized:
            command.append("-O")
        command.extend(["-B", str(HERE / "audit_receipt.py"),
                        str(catalog), str(source / "RESULT.tsv"), str(result)])
        audits.append(json.loads(run(command, HERE, environment)))
    need(audits == [expected["audit"]] * 2, "review audit modes")

    sanitized = work / "independent_check_sanitized"
    compile_cpp(HERE / "independent_check.cpp", sanitized,
                cadical / "src", cadical / "build" / "libcadical.a", True)
    sanitizer_environment = environment.copy()
    sanitizer_environment["ASAN_OPTIONS"] = "detect_leaks=1"
    sanitizer_environment["UBSAN_OPTIONS"] = "halt_on_error=1"
    sanitizer_result = work / "sanitizer-control.tsv"
    sanitizer_stdout = run([
        str(sanitized), str(catalog), str(source / "RESULT.tsv"),
        str(sanitizer_result), "1",
    ], HERE, sanitizer_environment).decode().strip()
    need(sanitizer_stdout.startswith("PARTIAL_DRT43_CATALOG_CHECK records=1 "),
         "sanitizer control")

    check_git_commit(kissat, KISSAT_COMMIT)
    need(run([str(kissat / "build" / "kissat"), "--version"], HERE)
         .decode().strip() == "4.0.4", "Kissat version")
    cross = work / "kissat_cross_check"
    run([
        "g++", "-O3", "-std=c++20", "-Wall", "-Wextra", "-Werror",
        "-pedantic", f"-I{kissat / 'src'}",
        str(HERE / "kissat_cross_check.cpp"),
        str(kissat / "build" / "libkissat.a"), "-lm", "-o", str(cross),
    ], HERE)
    controls = cross_solver_controls(cross, catalog,
                                     expected["cross_solver_controls"],
                                     environment)

    print(json.dumps({
        "catalog_scope": "the 2178 supplied records, not all DRT(43)s",
        "cross_solver_controls": len(controls),
        "first_position_branches_unsat":
            expected["audit"]["first_position_branches_unsat"],
        "full_independent_result_sha256": digest(result),
        "review_manifest_entries": len(review_manifest),
        "reviewed_source_commit": SOURCE_COMMIT,
        "root_formulas_unsat": expected["audit"]["root_formulas_unsat"],
        "sanitizer_control": True,
        "source_manifest_entries": len(source_manifest),
        "status": "REPRODUCED_ACCEPT_REVIEW_H3989",
        "target_good43_found": False,
        "transient_author_drat_replayed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
