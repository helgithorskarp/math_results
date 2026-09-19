#!/usr/bin/env python3
"""Exact, solver-free verifier for all degree-two G8 mixture profiles."""

from __future__ import annotations

import collections
import itertools
import re
from hashlib import sha256
from pathlib import Path

PAIRS = tuple((a, b) for a in range(8) for b in range(a + 1, 8))
EDGE_INDEX = {pair: edge for edge, pair in enumerate(PAIRS)}
G8_ARCS = (
    (0, 1), (0, 2), (0, 3), (4, 0), (6, 0), (7, 0),
    (1, 3), (1, 4), (5, 1), (1, 6), (7, 1), (2, 3),
    (2, 4), (5, 2), (6, 2), (2, 7), (3, 5), (3, 6),
    (3, 7), (4, 5),
)
G8_MISSING = (
    (0, 5), (1, 2), (3, 4), (4, 6),
    (4, 7), (5, 6), (5, 7), (6, 7),
)
HEADER = "CERTIFICATE stable_transitivity_g8_pair_mixtures_v1 n=8 targets=6561"
ROW = re.compile(r"TARGET (?P<target>[012]{8}) profile=(?P<profile>[0-9,]+)")
EXPECTED_LAYERS = {0: 832, 1: 4192, 2: 9344, 3: 11584, 4: 9344, 5: 4192, 6: 832}


def order_masks() -> tuple[int, ...]:
    """Enumerate masks directly from all vertex permutations."""
    masks = []
    for order in itertools.permutations(range(8)):
        position = [0] * 8
        for rank, vertex in enumerate(order):
            position[vertex] = rank
        masks.append(
            sum(
                int(position[a] < position[b]) << edge
                for edge, (a, b) in enumerate(PAIRS)
            )
        )
    if len(masks) != 40320 or len(set(masks)) != 40320:
        raise AssertionError("total-order enumeration is incomplete")
    return tuple(masks)


def predicts_arc(mask: int, arc: tuple[int, int]) -> int:
    a, b = arc
    if a < b:
        return (mask >> EDGE_INDEX[(a, b)]) & 1
    return 1 - ((mask >> EDGE_INDEX[(b, a)]) & 1)


def read_profiles(path: Path) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines or lines[0] != HEADER:
        raise ValueError("wrong mixture-profile header")
    records = []
    for line in lines[1:]:
        if not line or line.startswith("#"):
            continue
        match = ROW.fullmatch(line)
        if match is None:
            raise ValueError("malformed mixture-profile row")
        records.append(
            (
                tuple(map(int, match["target"])),
                tuple(map(int, match["profile"].split(","))),
            )
        )
    return records


def verify(path: Path) -> str:
    profiles = read_profiles(path)
    expected_targets = list(itertools.product(range(3), repeat=8))
    if [target for target, _ in profiles] != expected_targets:
        raise ValueError("target coverage or lexicographic order is wrong")

    orders = order_masks()
    g8_hits = tuple(
        sum(predicts_arc(order, arc) for arc in G8_ARCS)
        for order in orders
    )
    if max(g8_hits) != 13:
        raise ValueError("the G8 maximum is not 13")
    layers = collections.Counter(13 - hits for hits in g8_hits)
    if layers != EXPECTED_LAYERS:
        raise ValueError("wrong exhaustive G8 defect distribution")

    arc_checks = 0
    total_profile_orders = 0
    for target, profile in profiles:
        if len(profile) != 8 or len(set(profile)) != 8:
            raise ValueError(f"target {target}: profile is not square-free of size eight")
        if tuple(sorted(profile)) != profile:
            raise ValueError(f"target {target}: profile is not in canonical order")
        if any(index < 0 or index >= len(orders) for index in profile):
            raise ValueError(f"target {target}: order index out of range")

        for arc in G8_ARCS:
            count = sum(predicts_arc(orders[index], arc) for index in profile)
            if count != 5:
                raise ValueError(f"target {target}: fixed arc {arc} has count {count}")
            arc_checks += 1
        for digit, pair in zip(target, G8_MISSING):
            edge = EDGE_INDEX[pair]
            count = sum((orders[index] >> edge) & 1 for index in profile)
            if count != 3 + digit:
                raise ValueError(
                    f"target {target}: missing pair {pair} has count {count}"
                )
            arc_checks += 1
        defect = sum(13 - g8_hits[index] for index in profile)
        if defect != 4:
            raise ValueError(f"target {target}: total G8 defect is {defect}")
        total_profile_orders += len(profile)

    rows = [
        "vertices=8 total_orders=40320",
        "g8_arcs=20 missing_pairs=8 maximum_g8_hits=13 tight_orders=832",
        "g8_defect_layers=0:832,1:4192,2:9344,3:11584,4:9344,5:4192,6:832",
        f"targets={len(profiles)} profile_orders={total_profile_orders} squarefree_profiles={len(profiles)}",
        f"arc_count_checks={arc_checks}",
        "target_box={0,1,2}^8",
        "theorem=m(W)=3_for_every_degree_two_extension_of_G8",
    ]
    canonical = "\n".join(rows)
    return canonical + "\naudit_sha256=" + sha256(canonical.encode("ascii")).hexdigest()


if __name__ == "__main__":
    print(verify(Path("pair_profiles.txt")))
