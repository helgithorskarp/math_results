#!/usr/bin/env python3
"""Recompute the nonzero transition and target union through radius six."""

import argparse


def read_map(path: str) -> tuple[int, set[tuple[str, int]]]:
    transitions = 0
    targets = set()
    summary = None
    with open(path, encoding="ascii") as source:
        header = source.readline().rstrip("\n").split("\t")
        if header[-2:] != ["target_kind", "target_index"]:
            raise RuntimeError(f"unexpected map header: {path}")
        for line in source:
            if line.startswith("# SUMMARY "):
                summary = dict(field.split("=", 1) for field in line.split()[2:])
                break
            fields = line.rstrip("\n").split("\t")
            kind = fields[-2]
            index = int(fields[-1])
            if kind not in {"base", "complement"} or not 0 <= index < 328:
                raise RuntimeError(f"bad target in {path}")
            transitions += 1
            targets.add((kind, index))
    if summary is None:
        raise RuntimeError(f"missing summary: {path}")
    if "transitions" in summary:
        summarized_transitions = int(summary["transitions"])
    elif "radius1" in summary and "radius2" in summary:
        summarized_transitions = int(summary["radius1"]) + int(summary["radius2"])
    else:
        raise RuntimeError(f"unrecognized summary: {path}")
    if summarized_transitions != transitions:
        raise RuntimeError(f"summary mismatch: {path}")
    return transitions, targets


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("radius2_map")
    parser.add_argument("radius3_map")
    parser.add_argument("radius4_map")
    parser.add_argument("radius5_map")
    parser.add_argument("radius6_map")
    args = parser.parse_args()

    maps = [
        args.radius2_map,
        args.radius3_map,
        args.radius4_map,
        args.radius5_map,
        args.radius6_map,
    ]
    transitions = 0
    targets = set()
    for path in maps[:-1]:
        count, map_targets = read_map(path)
        transitions += count
        targets.update(map_targets)
    prior_targets = set(targets)
    count, radius6_targets = read_map(maps[-1])
    transitions += count
    targets.update(radius6_targets)
    new_targets = targets - prior_targets

    values = {
        "radius_at_most_6_nonzero_transitions": transitions,
        "distinct_targets": len(targets),
        "base_targets": sum(kind == "base" for kind, _ in targets),
        "complement_targets": sum(
            kind == "complement" for kind, _ in targets
        ),
        "new_radius6_targets": len(new_targets),
        "new_base_targets": sum(kind == "base" for kind, _ in new_targets),
        "new_complement_targets": sum(
            kind == "complement" for kind, _ in new_targets
        ),
    }
    expected = {
        "radius_at_most_6_nonzero_transitions": 37256,
        "distinct_targets": 552,
        "base_targets": 328,
        "complement_targets": 224,
        "new_radius6_targets": 12,
        "new_base_targets": 2,
        "new_complement_targets": 10,
    }
    if values != expected:
        raise RuntimeError(f"aggregate mismatch: {values}")
    print(" ".join(f"{key}={value}" for key, value in values.items()))


if __name__ == "__main__":
    main()
