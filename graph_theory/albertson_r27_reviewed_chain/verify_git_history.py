#!/usr/bin/env python3
"""Audit the manifest against immutable objects in the local Git history."""

from __future__ import annotations

from hashlib import sha256
from json import dumps, loads
from pathlib import Path, PurePosixPath
from re import fullmatch
from subprocess import PIPE, CalledProcessError, run


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[1]
COMMIT_PATTERN = r"[0-9a-f]{40}"
HASH_PATTERN = r"[0-9a-f]{64}"


def git(*arguments: str, check: bool = True) -> bytes:
    process = run(
        ["git", *arguments],
        cwd=REPOSITORY,
        check=False,
        stdout=PIPE,
        stderr=PIPE,
    )
    if check and process.returncode:
        message = process.stderr.decode("utf-8", errors="replace").strip()
        raise CalledProcessError(
            process.returncode,
            process.args,
            output=process.stdout,
            stderr=message,
        )
    return process.stdout


def safe_relative(value: object) -> str:
    path = PurePosixPath(str(value))
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise ValueError(f"unsafe repository path: {value!r}")
    return path.as_posix()


def load_manifest() -> dict[str, object]:
    manifest = loads((HERE / "dependency_manifest.json").read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise TypeError("dependency_manifest.json")
    return manifest


def audit_history(manifest: dict[str, object]) -> tuple[list[dict[str, object]], int]:
    repository_root = Path(git("rev-parse", "--show-toplevel").decode().strip()).resolve()
    if repository_root != REPOSITORY:
        raise AssertionError((repository_root, REPOSITORY))

    artifacts = manifest["artifacts"]
    if not isinstance(artifacts, list):
        raise TypeError("artifacts")
    records: list[dict[str, object]] = []
    review_links = 0
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            raise TypeError("artifact")
        artifact_id = str(artifact["id"])
        source_commit = str(artifact["source_commit"])
        if not fullmatch(COMMIT_PATTERN, source_commit):
            raise ValueError(f"invalid source commit for {artifact_id}")
        git("cat-file", "-e", f"{source_commit}^{{commit}}")
        directory = safe_relative(artifact["path"])
        files = artifact["files"]
        if not isinstance(files, dict) or not files:
            raise TypeError(f"files for {artifact_id}")

        checked_files: list[dict[str, str]] = []
        for relative_value, expected_value in sorted(files.items()):
            relative = safe_relative(relative_value)
            expected = str(expected_value)
            if not fullmatch(HASH_PATTERN, expected):
                raise ValueError(f"invalid hash for {artifact_id}/{relative}")
            object_path = f"{directory}/{relative}"
            historical = git("show", f"{source_commit}:{object_path}")
            historical_hash = sha256(historical).hexdigest()
            if historical_hash != expected:
                raise AssertionError(
                    (artifact_id, source_commit, object_path, historical_hash, expected)
                )
            current_hash = sha256((REPOSITORY / object_path).read_bytes()).hexdigest()
            if current_hash != expected:
                raise AssertionError(
                    (artifact_id, "current", object_path, current_hash, expected)
                )
            checked_files.append({"path": object_path, "sha256": expected})

        record: dict[str, object] = {
            "id": artifact_id,
            "source_commit": source_commit,
            "files": checked_files,
        }
        if "review_commit" in artifact:
            review_commit = str(artifact["review_commit"])
            if not fullmatch(COMMIT_PATTERN, review_commit):
                raise ValueError(f"invalid review commit for {artifact_id}")
            git("cat-file", "-e", f"{review_commit}^{{commit}}")
            ancestry = run(
                ["git", "merge-base", "--is-ancestor", source_commit, review_commit],
                cwd=REPOSITORY,
                check=False,
                stdout=PIPE,
                stderr=PIPE,
            )
            if ancestry.returncode:
                raise AssertionError((artifact_id, source_commit, review_commit))
            record["review_commit"] = review_commit
            review_links += 1
        records.append(record)
    return records, review_links


def main() -> None:
    records, review_links = audit_history(load_manifest())
    file_count = sum(len(record["files"]) for record in records)
    digest = sha256(dumps(records, sort_keys=True).encode("ascii")).hexdigest()
    print(f"PASS historical manifest: {len(records)} artifacts")
    print(f"PASS {file_count} files match their recorded Git objects and checkout")
    print(f"PASS {review_links} review commits descend from their source commits")
    print(f"history_certificate_sha256={digest}")


if __name__ == "__main__":
    main()
