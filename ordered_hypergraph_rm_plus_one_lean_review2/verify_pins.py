#!/usr/bin/env python3
"""Check the pinned source identity and optionally rebuild the Lean project."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


EXPECTED_COMMIT = "9e4c6dbaebab5f242bed49fe223c2cb2451a3ba5"
EXPECTED_SOURCE_SHA256 = (
    "c8fbee0c02f2bc6ca858fe2be7905ebed561f97f7a17dde52c52162b5b074a58"
)
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.33.1"
EXPECTED_MATHLIB_REV = "0df444a360eaa60ab8c11dca51a86af692955474"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
THEOREMS = (
    "card_copies_le_card_blocker_mul",
    "rm_add_one_le_card_blocker_of_bounded_multiplicity",
    "card_copies_le_card_blocker_of_pairwiseDisjoint",
    "rm_add_one_le_card_blocker_of_pairwiseDisjoint",
    "card_uniformEdges",
    "card_present_le_choose_sub",
    "boundary_upper_of_bounded_multiplicity",
    "boundary_upper_of_pairwiseDisjoint",
)


def checked_output(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> str:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ).stdout


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def audit_source(project: Path) -> None:
    source = project / "OrderedPatternBlocker.lean"
    manifest_path = project / "lake-manifest.json"

    commit = checked_output(
        ["git", "rev-parse", "HEAD"], cwd=project
    ).strip()
    require(commit == EXPECTED_COMMIT, f"unexpected commit: {commit}")
    require(
        sha256(source) == EXPECTED_SOURCE_SHA256,
        "OrderedPatternBlocker.lean hash mismatch",
    )
    require(
        (project / "lean-toolchain").read_text(encoding="utf-8").strip()
        == EXPECTED_TOOLCHAIN,
        "Lean toolchain pin mismatch",
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    mathlib = next(
        (package for package in manifest["packages"] if package["name"] == "mathlib"),
        None,
    )
    require(mathlib is not None, "Mathlib package missing from manifest")
    require(mathlib["rev"] == EXPECTED_MATHLIB_REV, "Mathlib revision mismatch")

    text = source.read_text(encoding="utf-8")
    banned = re.findall(r"\b(?:sorry|admit|native_decide|unsafe|axiom)\b", text)
    require(not banned, f"banned declarations/tokens found: {banned}")
    for theorem in THEOREMS:
        require(
            f"#print axioms {theorem}" in text,
            f"missing axiom audit for {theorem}",
        )

    print(f"commit={commit}")
    print(f"source_sha256={sha256(source)}")
    print(f"lean_toolchain={EXPECTED_TOOLCHAIN}")
    print(f"mathlib_rev={mathlib['rev']}")
    print("source_scan=PASS")


def audit_build(project: Path, lake: str) -> None:
    lake_resolved = shutil.which(lake)
    lake_path = Path(lake_resolved).resolve() if lake_resolved else Path(lake).resolve()
    require(lake_path.is_file(), f"Lake executable not found: {lake_path}")
    env = os.environ.copy()
    env["PATH"] = f"{lake_path.parent}{os.pathsep}{env.get('PATH', '')}"

    checked_output([str(lake_path), "clean", "ordered_pattern_blocker"], project, env)
    output = checked_output(
        [str(lake_path), "build", "OrderedPatternBlocker"], project, env
    )
    require(
        "Build completed successfully (758 jobs)." in output,
        "expected successful 758-job build line not found",
    )

    for theorem in THEOREMS:
        pattern = re.compile(
            rf"'OrderedPatternBlocker\.{re.escape(theorem)}' depends on axioms: "
            r"\[(.*?)\](?=\ninfo:|\nBuild completed)",
            re.DOTALL,
        )
        match = pattern.search(output)
        require(match is not None, f"axiom output missing for {theorem}")
        axioms = {item.strip() for item in match.group(1).split(",")}
        require(axioms == EXPECTED_AXIOMS, f"unexpected axioms for {theorem}: {axioms}")

    print("clean_build=PASS")
    print("axiom_audit=PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "project",
        type=Path,
        help="path to the checked-out ordered_pattern_blocker project",
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="also clean-build the project and verify #print axioms output",
    )
    parser.add_argument(
        "--lake",
        default="lake",
        help="Lake executable to use with --build (default: lake on PATH)",
    )
    args = parser.parse_args()

    project = args.project.resolve()
    require(project.is_dir(), f"project directory not found: {project}")
    audit_source(project)
    if args.build:
        audit_build(project, args.lake)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, subprocess.CalledProcessError, OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
