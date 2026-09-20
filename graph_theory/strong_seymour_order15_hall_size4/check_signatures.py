#!/usr/bin/env python3
"""Independent orbit-expansion check of the ten size-four signatures."""

from __future__ import annotations

import collections
import hashlib
import itertools
import json


REPRESENTATIVES = [
    "000000111111111111",
    "000010111111111111",
    "001000111111011011",
    "001000111111011101",
    "001000111111011111",
    "001000111111111011",
    "001000111111111111",
    "001001111111001111",
    "001001111111011111",
    "001001111111111111",
]
EXPECTED_ORBIT_SIZES = [24, 8, 72, 144, 72, 72, 24, 24, 24, 8]
EXPECTED_REPRESENTATIVE_SHA256 = (
    "f0e081ae71e96b13b914619781c5d0d82c42ab36efcee834325f2452a323fd05"
)
EXPECTED_SURVIVOR_SHA256 = (
    "ecf26ea337d8d00a8d0118bc3ca3350174bcdc819f1d1802cf52b0c387d539d5"
)
PAIRS = [(first, second) for first in range(4) for second in range(first + 1, 4)]


def unpack(pattern: str) -> tuple[list[list[bool]], list[list[bool]]]:
    assert len(pattern) == 18 and set(pattern) <= {"0", "1"}
    adjacency = [[False] * 4 for _ in range(4)]
    shift = 0
    for first, second in PAIRS:
        adjacency[first][second] = pattern[shift] == "1"
        adjacency[second][first] = not adjacency[first][second]
        shift += 1
    link = [[False] * 3 for _ in range(4)]
    for tail in range(4):
        for head in range(3):
            link[tail][head] = pattern[shift] == "1"
            shift += 1
    return adjacency, link


def pack(adjacency: list[list[bool]], link: list[list[bool]]) -> str:
    bits = [int(adjacency[first][second]) for first, second in PAIRS]
    bits.extend(int(link[tail][head]) for tail in range(4) for head in range(3))
    return "".join(str(bit) for bit in bits)


def relabel(pattern: str, s_perm: tuple[int, ...], r_perm: tuple[int, ...]) -> str:
    adjacency, link = unpack(pattern)
    relabeled_adjacency = [[False] * 4 for _ in range(4)]
    relabeled_link = [[False] * 3 for _ in range(4)]
    for first in range(4):
        for second in range(4):
            relabeled_adjacency[first][second] = adjacency[
                s_perm[first]
            ][s_perm[second]]
    for tail in range(4):
        for head in range(3):
            relabeled_link[tail][head] = link[s_perm[tail]][r_perm[head]]
    return pack(relabeled_adjacency, relabeled_link)


def forced_extra_count(
    adjacency: list[list[bool]], link: list[list[bool]], vertex: int
) -> int:
    extras: set[tuple[str, int]] = set()
    s_out = [other for other in range(4) if adjacency[vertex][other]]
    r_out = [head for head in range(3) if link[vertex][head]]
    if r_out:
        extras.add(("root", 0))
    for other in range(4):
        if adjacency[vertex][other]:
            continue
        for midpoint in s_out:
            if adjacency[midpoint][other]:
                extras.add(("S", other))
        for head in r_out:
            if not link[other][head]:
                extras.add(("S", other))
    for head in range(3):
        if link[vertex][head]:
            continue
        for midpoint in s_out:
            if link[midpoint][head]:
                extras.add(("R", head))
    return len(extras)


def classify(pattern: str) -> str:
    adjacency, link = unpack(pattern)
    if any(sum(link[tail][head] for tail in range(4)) < 2 for head in range(3)):
        return "infeasible"
    p = [sum(adjacency[vertex]) for vertex in range(4)]
    q = [sum(link[vertex]) for vertex in range(4)]
    if any(p[vertex] + q[vertex] < 3 for vertex in range(4)):
        return "infeasible"
    if any(
        p[vertex] + q[vertex] == 3
        and forced_extra_count(adjacency, link, vertex) >= 2
        for vertex in range(4)
    ):
        return "forced_ordinary"
    return "survivor"


def raw_patterns():
    for tournament_bits in range(1 << 6):
        adjacency = [[False] * 4 for _ in range(4)]
        for shift, (first, second) in enumerate(PAIRS):
            adjacency[first][second] = bool(tournament_bits & (1 << shift))
            adjacency[second][first] = not adjacency[first][second]
        for link_bits in range(1 << 12):
            link = [
                [bool(link_bits & (1 << (3 * tail + head))) for head in range(3)]
                for tail in range(4)
            ]
            yield pack(adjacency, link)


def digest(values: set[str] | list[str]) -> str:
    payload = "\n".join(sorted(values)) + "\n"
    return hashlib.sha256(payload.encode()).hexdigest()


def main() -> None:
    permutations_s = list(itertools.permutations(range(4)))
    permutations_r = list(itertools.permutations(range(3)))
    expanded: set[str] = set()
    measured_orbit_sizes = []
    for representative, expected_size in zip(
        REPRESENTATIVES, EXPECTED_ORBIT_SIZES, strict=True
    ):
        orbit = {
            relabel(representative, s_perm, r_perm)
            for s_perm in permutations_s
            for r_perm in permutations_r
        }
        assert len(orbit) == expected_size
        assert expanded.isdisjoint(orbit)
        measured_orbit_sizes.append(len(orbit))
        expanded.update(orbit)

    counts = collections.Counter()
    survivors: set[str] = set()
    for pattern in raw_patterns():
        category = classify(pattern)
        counts[category] += 1
        if category == "survivor":
            survivors.add(pattern)

    assert expanded == survivors
    assert counts == {
        "infeasible": 239776,
        "forced_ordinary": 21896,
        "survivor": 472,
    }
    representative_sha256 = digest(REPRESENTATIVES)
    survivor_sha256 = digest(survivors)
    assert representative_sha256 == EXPECTED_REPRESENTATIVE_SHA256
    assert survivor_sha256 == EXPECTED_SURVIVOR_SHA256
    report = {
        "counts": dict(sorted(counts.items())),
        "orbit_sizes": measured_orbit_sizes,
        "representative_sha256": representative_sha256,
        "status": "VERIFIED",
        "survivor_sha256": survivor_sha256,
    }
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
