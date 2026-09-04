#!/usr/bin/env python3
"""Definition-level audit of the C86 orbit transfer and tube arithmetic."""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 43
FULL_MASK = (1 << N) - 1
RED_LENGTHS = {1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21}
PRIMARY = frozenset(
    {0, 1, 2, 8, 9, 10, 11, 17, 18, 19, 25, 26, 27, 28, 34, 35, 36, 37}
)
ODD_REPRESENTATIVE = PRIMARY ^ {42}
FU_MALIK = frozenset(
    {1, 2, 3, 4, 10, 11, 12, 18, 19, 20, 21, 27, 28, 29, 30, 35, 36, 37, 38}
)
PINNED_OUTPUT_HASHES = [
    "a0addcbe7aaae06ac3d67aec330d191ce393ce4423993a642efabffc1d4a4233",
    "37c0a740ac7ee06a9fb20204ade77f323781a9528f4596aefe57f5b5315e6131",
]


def rotate_positions(positions: frozenset[int], shift: int) -> frozenset[int]:
    return frozenset((position + shift) % N for position in positions)


def rotate_word(word: int, shift: int) -> int:
    shift %= N
    if shift == 0:
        return word & FULL_MASK
    return ((word << shift) | (word >> (N - shift))) & FULL_MASK


def canonical_rotation(word: int) -> int:
    return min(rotate_word(word, shift) for shift in range(N))


def transport_position(index: int) -> int:
    base = 42 if index % 2 == 0 else 37
    return (base + 17 * (index // 2)) % N


def cycle_states() -> list[frozenset[int]]:
    states = []
    active = set(PRIMARY)
    for index in range(2 * N):
        states.append(frozenset(active))
        active.symmetric_difference_update({transport_position(index)})
    if active != set(PRIMARY):
        raise AssertionError("transport did not close")
    return states


def edge_is_red(u: int, v: int, flipped_length_one: frozenset[int]) -> bool:
    distance = min((u - v) % N, (v - u) % N)
    red = distance in RED_LENGTHS
    if distance == 1:
        position = min(u, v) if abs(u - v) == 1 else 42
        if position in flipped_length_one:
            red = not red
    return red


def monochromatic_fives(
    flipped_length_one: frozenset[int],
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    red_fives: list[tuple[int, ...]] = []
    blue_fives: list[tuple[int, ...]] = []
    for vertices in itertools.combinations(range(N), 5):
        colors = [
            edge_is_red(u, v, flipped_length_one)
            for u, v in itertools.combinations(vertices, 2)
        ]
        if all(colors):
            red_fives.append(vertices)
        elif not any(colors):
            blue_fives.append(vertices)
    return red_fives, blue_fives


def load_radius_evidence() -> list[dict[str, object]]:
    document = json.loads((HERE / "base_radius6_evidence.json").read_text())
    if document["source_commit"] != "91e596cd4b6abf3675e82414749421455da8d6c8":
        raise AssertionError("wrong inherited source commit")
    if document["source_sha256"] != "e7ea42ffcef7c23b00336cbdb27f12203ee2e0ad93afd2a8d6093fe0071ce308":
        raise AssertionError("wrong inherited source hash")
    runs = document["runs"]
    for run, expected_hash in zip(runs, PINNED_OUTPUT_HASHES, strict=True):
        if run["radius"] != 6:
            raise AssertionError("wrong inherited radius")
        if run["improvement_found"] is not False or run["exact_minimum"] != 2:
            raise AssertionError("wrong inherited minimum")
        if run["target_monochromatic_k5_count"] != 1:
            raise AssertionError("wrong inherited search target")
        if run["output_sha256"] != expected_hash:
            raise AssertionError("wrong inherited output hash")
    return runs


def parse_expected_output() -> tuple[int, list[int], list[int], int]:
    fields = {}
    for line in (HERE / "EXPECTED_OUTPUT.txt").read_text().splitlines():
        key, value = line.split("=", 1)
        fields[key] = value
    records = int(fields["generated_records"])
    inner = [int(item) for item in fields["inner_exact_layers"].split(",")]
    ambient = [int(item) for item in fields["ambient_exact_layers"].split(",")]
    closed = int(fields["closed_radius6_volume"])
    return records, inner, ambient, closed


def independently_check_inner_prefix(expected: list[int], radius: int = 4) -> None:
    minimum_distance: dict[int, int] = {}
    center_words = [sum(1 << bit for bit in center) for center in (PRIMARY, ODD_REPRESENTATIVE)]
    for center in center_words:
        for distance in range(radius + 1):
            for error_positions in itertools.combinations(range(N), distance):
                error = sum(1 << bit for bit in error_positions)
                key = canonical_rotation(center ^ error)
                old = minimum_distance.get(key)
                if old is None or distance < old:
                    minimum_distance[key] = distance
    if 0 in minimum_distance or FULL_MASK in minimum_distance:
        raise AssertionError("unexpected fixed rotation orbit")
    layers = Counter(minimum_distance.values())
    observed = [N * layers[distance] for distance in range(radius + 1)]
    if observed != expected[: radius + 1]:
        raise AssertionError((observed, expected[: radius + 1]))


def main() -> None:
    states = cycle_states()
    if len(set(states)) != 86:
        raise AssertionError("C86 states are not distinct")
    if Counter(transport_position(index) for index in range(86)) != Counter(
        {position: 2 for position in range(N)}
    ):
        raise AssertionError("wrong transition multiplicities")

    for k in range(N):
        if states[2 * k] != rotate_positions(PRIMARY, 17 * k):
            raise AssertionError(("even orbit", k))
        if states[2 * k + 1] != rotate_positions(ODD_REPRESENTATIVE, 17 * k):
            raise AssertionError(("odd orbit", k))
    if len({rotate_positions(PRIMARY, shift) for shift in range(N)}) != N:
        raise AssertionError("primary rotation orbit is not free")
    if len({rotate_positions(ODD_REPRESENTATIVE, shift) for shift in range(N)}) != N:
        raise AssertionError("odd rotation orbit is not free")
    if states[71] != FU_MALIK or rotate_positions(ODD_REPRESENTATIVE, 36) != FU_MALIK:
        raise AssertionError("Fu-Malik orbit alignment failed")

    primary_red, primary_blue = monochromatic_fives(PRIMARY)
    odd_red, odd_blue = monochromatic_fives(ODD_REPRESENTATIVE)
    fm_red, fm_blue = monochromatic_fives(FU_MALIK)
    if (len(primary_red), len(primary_blue)) != (2, 0):
        raise AssertionError("primary representative is not objective two")
    if (len(odd_red), len(odd_blue)) != (0, 2):
        raise AssertionError("odd representative is not objective two")
    if (len(fm_red), len(fm_blue)) != (0, 2):
        raise AssertionError("Fu-Malik representative is not objective two")

    radius_documents = load_radius_evidence()
    if [frozenset(run["center_length_one_positions"]) for run in radius_documents] != [
        PRIMARY,
        FU_MALIK,
    ]:
        raise AssertionError("radius evidence has the wrong centers")

    records, inner, ambient, closed = parse_expected_output()
    if records != 2 * sum(math.comb(N, distance) for distance in range(7)):
        raise AssertionError("wrong generated-record count")
    independently_check_inner_prefix(inner)
    recomputed_ambient = [
        sum(math.comb(903 - N, outside) * inner[distance - outside]
            for outside in range(distance + 1))
        for distance in range(7)
    ]
    if recomputed_ambient != ambient or sum(ambient) != closed:
        raise AssertionError("ambient tube convolution mismatch")

    # Rotation is a coordinate permutation, hence it preserves both Hamming
    # distance and the red/blue monochromatic-five objective.  The two orbit
    # identities above therefore transfer the two imported radius-six minima
    # to all 86 centers.
    print("PASS C86 is exactly two free C43 rotation orbits")
    print("PASS direct K5 recounts: primary=2 odd=2 Fu-Malik=2")
    print("PASS pinned radius-six evidence covers one representative per orbit")
    print(f"PASS exact closed C86 radius-six tube volume={closed}")


if __name__ == "__main__":
    main()
