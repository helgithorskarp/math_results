#!/usr/bin/env python3
"""Independent direct audit of the five new BHR path seeds."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

LENGTHS = (1, 2, 11)


def distance(x: int, y: int, order: int) -> int:
    forward = (y - x) % order
    backward = (x - y) % order
    return min(forward, backward)


def image(x: int, width: int, cut: int) -> int:
    return x + width if x > cut else x


def grow(path: list[int], width: int, cut: int) -> tuple[list[int], list[tuple[int, int]]]:
    order = len(path)
    critical = set(range(cut - width + 1, cut + 1))
    changed = []
    output = [image(path[0], width, cut)]
    for left, right in zip(path, path[1:]):
        old = distance(left, right, order)
        new_left = image(left, width, cut)
        new_right = image(right, width, cut)
        new = distance(new_left, new_right, order + width)
        if new > old:
            incident = [vertex for vertex in (left, right) if vertex in critical]
            if len(incident) != 1:
                raise AssertionError(("changed edge", width, cut, left, right, incident))
            changed.append((left, right))
            output.append(incident[0] + width)
        output.append(new_right)
    incidence = Counter(v for edge in changed for v in edge if v in critical)
    if incidence != Counter({v: 1 for v in critical}):
        raise AssertionError(("growth incidence", width, cut, incidence))
    return output, changed


def counts(path: list[int]) -> tuple[int, int, int]:
    order = len(path)
    values = Counter(distance(x, y, order) for x, y in zip(path, path[1:]))
    if set(values) - set(LENGTHS):
        raise AssertionError(("foreign length", values))
    return tuple(values[length] for length in LENGTHS)


def shifted(cut: int, inserted_cut: int, width: int) -> int:
    return cut if cut <= inserted_cut else cut + width


def main() -> None:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "certificate.json")
    raw = path.read_bytes()
    data = json.loads(raw)
    records = []
    if len(data["seeds"]) != 5:
        raise AssertionError("seed count")
    for seed in data["seeds"]:
        vertex_path = seed["path"]
        target = tuple(seed["counts"])
        cuts = {int(key): value for key, value in seed["growth"].items()}
        if sorted(vertex_path) != list(range(sum(target) + 1)):
            raise AssertionError(("permutation", target))
        if counts(vertex_path) != target:
            raise AssertionError(("counts", target, counts(vertex_path)))

        after2, edges2 = grow(vertex_path, 2, cuts[2])
        cut11_after2 = shifted(cuts[11], cuts[2], 2)
        end_2_11, edges11_after2 = grow(after2, 11, cut11_after2)
        after11, edges11 = grow(vertex_path, 11, cuts[11])
        cut2_after11 = shifted(cuts[2], cuts[11], 11)
        end_11_2, edges2_after11 = grow(after11, 2, cut2_after11)
        if end_2_11 != end_11_2:
            raise AssertionError(("noncommuting source square", target))
        expected = (target[0], target[1] + 2, target[2] + 11)
        if counts(end_2_11) != expected:
            raise AssertionError(("endpoint", target, counts(end_2_11)))
        intervals = {
            width: set(range(cuts[width] - width + 1, cuts[width] + 1))
            for width in (2, 11)
        }
        if not intervals[2].isdisjoint(intervals[11]):
            raise AssertionError(("critical intervals", target))
        if len(vertex_path) < 35:
            raise AssertionError(("safe margin", target))
        records.append(
            {
                "counts": target,
                "changed_2": edges2,
                "changed_11": edges11,
                "changed_11_after_2": edges11_after2,
                "changed_2_after_11": edges2_after11,
                "endpoint_sha256": hashlib.sha256(
                    json.dumps(end_2_11, separators=(",", ":")).encode()
                ).hexdigest(),
            }
        )
    digest = hashlib.sha256(json.dumps(records, separators=(",", ":"), sort_keys=True).encode()).hexdigest()
    print(f"certificate_sha256={hashlib.sha256(raw).hexdigest()}")
    print("seeds=5")
    print("definition_level_growth_checks=20")
    print("commuting_source_squares=5")
    print(f"independent_record_sha256={digest}")
    print("INDEPENDENT_CHECK=PASS")


if __name__ == "__main__":
    main()
