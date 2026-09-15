#!/usr/bin/env python3
"""Negative controls for the independent Parts136 review checker."""

from __future__ import annotations

import argparse
from pathlib import Path
import tempfile

from verify_review import (
    canonical, read_points, read_relation, reconstruct, require,
    verify_binary_semantics,
)


def must_fail(action, label):
    try:
        action()
    except (AssertionError, ValueError):
        return
    raise AssertionError(f"negative control was accepted: {label}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--relation", required=True, type=Path)
    args = parser.parse_args()
    verify_binary_semantics()

    points = read_points(args.source / "points.tsv")
    damaged = list(points)
    row = list(damaged[0])
    row[0] += 1
    damaged[0] = tuple(row)
    must_fail(lambda: reconstruct(damaged), "one-coefficient geometry mutation")

    lines = args.relation.read_text().splitlines()
    require(len(lines) == 41025, "valid full relation supplied")
    with tempfile.TemporaryDirectory(prefix="parts136-review-controls-") as directory:
        directory = Path(directory)
        short = directory / "short.tsv"
        short.write_text("\n".join(lines[:-1]) + "\n")
        must_fail(lambda: read_relation(short), "deleted relation row")
        duplicate = directory / "duplicate.tsv"
        duplicate.write_text("\n".join([lines[0], lines[0], *lines[2:]]) + "\n")
        must_fail(lambda: read_relation(duplicate), "duplicate relation row")

    first_pattern = tuple(map(int, lines[0].split("\t", 1)[0]))
    require(first_pattern == canonical(first_pattern), "valid row canonical")
    bad_origin = (1,) + first_pattern[1:]
    require(not (bad_origin[0] == 0 and bad_origin == canonical(bad_origin)),
            "origin-normalization mutation rejected")
    print("all negative controls passed")


if __name__ == "__main__":
    main()
