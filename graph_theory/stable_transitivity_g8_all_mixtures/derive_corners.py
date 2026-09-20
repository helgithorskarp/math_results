#!/usr/bin/env python3
"""Derive the six G8 box-corner files from the cited ray certificates."""

from __future__ import annotations

import argparse
import itertools
import re
from pathlib import Path

PAIRS = tuple((a, b) for a in range(8) for b in range(a + 1, 8))
EDGE_INDEX = {pair: index for index, pair in enumerate(PAIRS)}
G8_ARCS = (
    (0, 1), (0, 2), (0, 3), (4, 0), (6, 0), (7, 0),
    (1, 3), (1, 4), (5, 1), (1, 6), (7, 1), (2, 3),
    (2, 4), (5, 2), (6, 2), (2, 7), (3, 5), (3, 6),
    (3, 7), (4, 5),
)
MISSING_PAIRS = (
    (0, 5), (1, 2), (3, 4), (4, 6),
    (4, 7), (5, 6), (5, 7), (6, 7),
)


def order_masks(orders: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    masks = []
    for order in orders:
        position = [0] * 8
        for rank, vertex in enumerate(order):
            position[vertex] = rank
        masks.append(sum(
            int(position[a] < position[b]) << edge
            for edge, (a, b) in enumerate(PAIRS)
        ))
    return tuple(masks)


def predicts(mask: int, arc: tuple[int, int]) -> int:
    a, b = arc
    if a < b:
        return (mask >> EDGE_INDEX[(a, b)]) & 1
    return 1 - ((mask >> EDGE_INDEX[(b, a)]) & 1)


def parse_profile(text: str) -> tuple[int, ...]:
    expanded = []
    for term in text.split(","):
        order, multiplicity = term.split(":")
        expanded.extend([int(order)] * int(multiplicity))
    return tuple(sorted(expanded))


def read_degree_one_profiles(
        path: Path, order_index: dict[tuple[int, ...], int]) -> dict[int, tuple[int, ...]]:
    pattern = re.compile(
        r"CLASS (\d+) tournament=\d+ x1=([0-7,]+) x2=([0-7,]+) "
        r"y1=([0-7,]+) y2=([0-7,]+) y3=([0-7,]+)"
    )
    profiles = {}
    for line in path.read_text().splitlines():
        match = pattern.fullmatch(line)
        if match is None:
            continue
        listed = [tuple(map(int, term.split(","))) for term in match.groups()[1:]]
        # The order-eight certificate stores its arc convention opposite to
        # the G8 margin convention used here.  Complement the Y side before
        # applying the completion-to-representative maps.  The definition-
        # level checks in derive_degree (and again in verify_boxes.cpp)
        # validate the resulting margins without trusting this convention.
        profile = [listed[0], listed[1], *(order[::-1] for order in listed[2:])]
        profiles[int(match.group(1))] = tuple(sorted(order_index[p] for p in profile))
    if len(profiles) != 96:
        raise ValueError(f"expected 96 degree-one profiles, read {len(profiles)}")
    return profiles


def read_higher_profiles(source: Path, degree: int) -> dict[int, tuple[int, ...]]:
    filename = "m6_profiles.txt" if degree == 6 else "residue_profiles.txt"
    profiles = {}
    for line in (source / filename).read_text().splitlines():
        if not line.startswith("CLASS "):
            continue
        if degree < 6 and f" dilation={degree} " not in line:
            continue
        match = re.search(r"CLASS (\d+).* profile=(.+)$", line)
        if match is None:
            raise ValueError("malformed source profile")
        profiles[int(match.group(1))] = parse_profile(match.group(2))
    if len(profiles) != 96:
        raise ValueError(f"expected 96 degree-{degree} profiles, read {len(profiles)}")
    return profiles


def read_completion_maps(source: Path) -> list[tuple[int, int, tuple[int, ...]]]:
    pattern = re.compile(r"COMPLETION ([01]{8}) class=(\d+) completion_to_t=([0-7,]+)")
    maps = []
    for line in (source / "g8_maps.txt").read_text().splitlines():
        match = pattern.fullmatch(line)
        if match is not None:
            bits = int(match.group(1), 2)
            mapping = tuple(map(int, match.group(3).split(",")))
            maps.append((bits, int(match.group(2)), mapping))
    if len(maps) != 256:
        raise ValueError(f"expected 256 completion maps, read {len(maps)}")
    return maps


def derive_degree(
        source: Path,
        degree_one: Path,
        output: Path,
        degree: int,
        orders: tuple[tuple[int, ...], ...],
        masks: tuple[int, ...],
        order_index: dict[tuple[int, ...], int]) -> None:
    stabilizer = (7 * degree + 5) // 6
    profile_size = degree + 2 * stabilizer
    if degree == 1:
        source_profiles = read_degree_one_profiles(degree_one, order_index)
    else:
        source_profiles = read_higher_profiles(source, degree)

    corners = {}
    for bits, source_class, mapping in read_completion_maps(source):
        source_profile = source_profiles[source_class]
        profile = tuple(sorted(
            order_index[tuple(mapping[v] for v in orders[index])]
            for index in source_profile
        ))
        target = tuple(degree * ((bits >> coordinate) & 1) for coordinate in range(8))
        if len(profile) != profile_size:
            raise ValueError("wrong profile size after relabeling")
        for arc in G8_ARCS:
            count = sum(predicts(masks[index], arc) for index in profile)
            if count != degree + stabilizer:
                raise ValueError(f"profile fails fixed arc {arc}")
        for digit, pair in zip(target, MISSING_PAIRS):
            edge = EDGE_INDEX[pair]
            count = sum((masks[index] >> edge) & 1 for index in profile)
            if count != stabilizer + digit:
                raise ValueError(f"profile fails missing pair {pair}")
        if target in corners:
            raise ValueError("duplicate corner")
        corners[target] = profile
    if len(corners) != 256:
        raise ValueError("incomplete corner set")

    lines = [f"G8_CORNERS degree={degree} profile_size={profile_size}"]
    for target in sorted(corners):
        lines.append(
            "TARGET " + "".join(map(str, target))
            + " profile=" + ",".join(map(str, corners[target]))
        )
    output.write_text("\n".join(lines) + "\n")
    print(f"degree={degree} corners={len(corners)} output={output}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="stable_transitivity_mu8 source directory")
    parser.add_argument("degree_one_certificate", type=Path, help="cert_n8_m2.txt")
    parser.add_argument("output_directory", type=Path)
    args = parser.parse_args()

    orders = tuple(itertools.permutations(range(8)))
    masks = order_masks(orders)
    order_index = {order: index for index, order in enumerate(orders)}
    args.output_directory.mkdir(parents=True, exist_ok=True)
    for degree in range(1, 7):
        derive_degree(
            args.source,
            args.degree_one_certificate,
            args.output_directory / f"corners_d{degree}.txt",
            degree,
            orders,
            masks,
            order_index,
        )


if __name__ == "__main__":
    main()
