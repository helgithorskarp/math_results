#!/usr/bin/env python3
"""Compare a downloaded arXiv v4 TeX source with the committed path input."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from exact_cayley_core import canonical_json_hash, sha256_file


def parse_paths(tex: str) -> list[list[int]]:
    try:
        appendix = tex.split("Appendix A:", 1)[1]
    except IndexError as error:
        raise ValueError("Appendix A marker not found") from error
    rows = re.findall(r"(?m)^\s*((?:\d+\s*&\s*){4,5}\d+)\s*\\\\", appendix)
    paths = [[int(value) for value in re.findall(r"\d+", row)] for row in rows]
    if len(paths) != 231 or not {len(path) for path in paths} <= {5, 6}:
        raise ValueError("unexpected Appendix A path table")
    return paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("tex", type=Path)
    parser.add_argument("graph", type=Path)
    parser.add_argument("certificate", type=Path)
    arguments = parser.parse_args()
    payload = json.loads(arguments.graph.read_text())
    certificate = json.loads(arguments.certificate.read_text())
    source = certificate["source"]
    if sha256_file(arguments.tex) != source["tex_sha256"]:
        raise AssertionError("TeX hash differs from the certified arXiv v4 source")
    paths = parse_paths(arguments.tex.read_text())
    if paths != payload["paths"]:
        raise AssertionError("arXiv v4 paths differ from graph.json")
    if canonical_json_hash(paths) != source["appendix_paths_sha256"]:
        raise AssertionError("canonical path hash mismatch")
    print(
        "source_check=true arxiv_version="
        f"{source['arxiv_version']} paths={len(paths)} "
        f"path_sha256={source['appendix_paths_sha256']}"
    )


if __name__ == "__main__":
    main()
