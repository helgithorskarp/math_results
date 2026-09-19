#!/usr/bin/env python3
"""Reproduce all ternary G8 profiles by exact adjacent-swap exchange."""

from __future__ import annotations

import argparse
import itertools
import re
from collections import deque
from hashlib import sha256
from pathlib import Path

from verify import (
    EDGE_INDEX,
    G8_ARCS,
    G8_MISSING,
    HEADER,
    PAIRS,
    order_masks,
    predicts_arc,
)

CORNER_HEADER = "CERTIFICATE stable_transitivity_g8_pair_corners_v1 n=8 targets=256"


def read_corners(path: Path) -> dict[tuple[int, ...], tuple[int, ...]]:
    text = path.read_text(encoding="ascii")
    lines = text.splitlines()
    if not lines or lines[0] != CORNER_HEADER:
        raise ValueError("wrong corner-profile header")
    row = re.compile(r"TARGET (?P<target>[02]{8}) profile=(?P<profile>[0-9,]+)")
    records = {}
    for line in lines[1:]:
        if not line or line.startswith("#"):
            continue
        match = row.fullmatch(line)
        if match is None:
            raise ValueError("malformed corner-profile row")
        target = tuple(map(int, match["target"]))
        profile = tuple(map(int, match["profile"].split(",")))
        if target in records:
            raise ValueError("duplicate corner target")
        records[target] = profile
    expected = set(itertools.product((0, 2), repeat=8))
    if set(records) != expected:
        raise ValueError("corner coverage is incomplete")
    return records


def write_profiles(path: Path, targets: dict[tuple[int, ...], tuple[int, ...]]) -> None:
    lines = [HEADER, "# TARGET <8 ternary digits> profile=<8 permutation indices>"]
    for target in itertools.product(range(3), repeat=8):
        lines.append(
            "TARGET " + "".join(map(str, target))
            + " profile=" + ",".join(map(str, targets[target]))
        )
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corners", type=Path, default=Path("corner_profiles.txt"))
    parser.add_argument("--output", type=Path, default=Path("generated_pair_profiles.txt"))
    parser.add_argument("--profiles-per-target", type=int, default=100)
    args = parser.parse_args()
    if args.profiles_per_target < 1:
        raise ValueError("profiles-per-target must be positive")

    permutations = tuple(itertools.permutations(range(8)))
    masks = order_masks()
    mask_index = {mask: index for index, mask in enumerate(masks)}
    missing_index = {pair: i for i, pair in enumerate(G8_MISSING)}

    transitions = []
    for order_index, order in enumerate(permutations):
        row = []
        for position in range(7):
            pair = tuple(sorted((order[position], order[position + 1])))
            coordinate = missing_index.get(pair)
            if coordinate is None:
                continue
            swapped = list(order)
            swapped[position], swapped[position + 1] = (
                swapped[position + 1], swapped[position]
            )
            replacement = mask_index[
                sum(
                    int(swapped.index(a) < swapped.index(b)) << edge
                    for edge, (a, b) in enumerate(PAIRS)
                )
            ]
            pair_edge = EDGE_INDEX[pair]
            delta = ((masks[replacement] >> pair_edge) & 1) - (
                (masks[order_index] >> pair_edge) & 1
            )
            row.append((replacement, coordinate, delta))
        transitions.append(tuple(row))

    corners = read_corners(args.corners)
    queue = deque()
    seen = set()
    retained = {}
    targets = {}
    # Match the canonical completion order: coordinate zero is the low bit.
    for bits in range(256):
        target = tuple(2 * ((bits >> coordinate) & 1) for coordinate in range(8))
        profile = corners[target]
        if len(profile) != 8 or len(set(profile)) != 8 or tuple(sorted(profile)) != profile:
            raise ValueError(f"corner {target} has a noncanonical profile")
        for arc in G8_ARCS:
            if sum(predicts_arc(masks[index], arc) for index in profile) != 5:
                raise ValueError(f"corner {target} fails a fixed arc")
        for digit, pair in zip(target, G8_MISSING):
            edge = EDGE_INDEX[pair]
            if sum((masks[index] >> edge) & 1 for index in profile) != 3 + digit:
                raise ValueError(f"corner {target} fails a missing pair")
        targets[target] = profile
        if profile not in seen:
            seen.add(profile)
            retained[target] = retained.get(target, 0) + 1
            queue.append((profile, target))

    processed = 0
    while queue and len(targets) < 3**8:
        profile, target = queue.popleft()
        processed += 1
        for slot, order_index in enumerate(profile):
            for replacement, coordinate, delta in transitions[order_index]:
                changed = list(target)
                changed[coordinate] += delta
                if changed[coordinate] not in (0, 1, 2):
                    continue
                changed_target = tuple(changed)
                updated = list(profile)
                updated[slot] = replacement
                updated_profile = tuple(sorted(updated))
                targets.setdefault(changed_target, updated_profile)
                if (
                    updated_profile not in seen
                    and retained.get(changed_target, 0) < args.profiles_per_target
                ):
                    seen.add(updated_profile)
                    retained[changed_target] = retained.get(changed_target, 0) + 1
                    queue.append((updated_profile, changed_target))

    if len(targets) != 3**8:
        raise RuntimeError(f"exchange search reached only {len(targets)} targets")
    write_profiles(args.output, targets)
    digest = sha256(args.output.read_bytes()).hexdigest()
    print(
        f"corners={len(corners)} targets={len(targets)} processed_states={processed} "
        f"retained_states={len(seen)} profiles_per_target={args.profiles_per_target}"
    )
    print(f"certificate_sha256={digest}")


if __name__ == "__main__":
    main()
