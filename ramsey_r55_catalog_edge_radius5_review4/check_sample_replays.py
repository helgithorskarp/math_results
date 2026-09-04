#!/usr/bin/env python3
"""Compare fresh enumerator output for selected parents with the saved map."""

from __future__ import annotations

import argparse
from pathlib import Path


def raw_key(fields: list[str]) -> tuple[int, tuple[str, ...]]:
    if len(fields) != 7:
        raise ValueError("fresh enumerator row must have seven fields")
    return int(fields[0]), tuple(fields[1:6])


def map_key(fields: list[str]) -> tuple[int, tuple[str, ...]]:
    if len(fields) != 8:
        raise ValueError("saved map row must have eight fields")
    return int(fields[0]), tuple(fields[1:6])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("saved_map", type=Path)
    parser.add_argument(
        "fresh",
        nargs="+",
        help="fresh replay as PARENT=PATH (an empty file certifies zero models)",
    )
    args = parser.parse_args()

    saved = set()
    for line in args.saved_map.read_text(encoding="ascii").splitlines()[1:]:
        if line.startswith("# SUMMARY "):
            break
        fields = line.split("\t")
        saved.add(map_key(fields))

    parents = set()
    fresh = set()
    for specification in args.fresh:
        parent_text, separator, path_text = specification.partition("=")
        if not separator:
            raise ValueError("fresh replay must be PARENT=PATH")
        expected_parent = int(parent_text)
        if not 0 <= expected_parent < 328 or expected_parent in parents:
            raise ValueError("bad or duplicate fresh parent")
        parents.add(expected_parent)
        path = Path(path_text)
        for line in path.read_text(encoding="ascii").splitlines():
            fields = line.split("\t")
            key = raw_key(fields)
            if key[0] != expected_parent:
                raise AssertionError(f"wrong parent in {path}")
            if key in fresh:
                raise AssertionError(f"duplicate fresh model {key}")
            fresh.add(key)
    expected = {key for key in saved if key[0] in parents}
    if fresh != expected:
        raise AssertionError(
            f"fresh/saved mismatch: missing={len(expected-fresh)} extra={len(fresh-expected)}"
        )
    print(
        f"sample_parents={','.join(map(str, sorted(parents)))} "
        f"sample_transitions={len(fresh)} exact_set_match=true"
    )


if __name__ == "__main__":
    main()
