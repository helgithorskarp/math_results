#!/usr/bin/env python3
"""Definition-first verification of the complete circulant K_43 minimum."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from array import array
from collections import Counter
from pathlib import Path


ORDER = 43
DISTANCES = 21
STATE_COUNT = 1 << DISTANCES
FULL_MASK = STATE_COUNT - 1
EXOO_LENGTHS = (1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21)


def mask_from_lengths(lengths: list[int] | tuple[int, ...]) -> int:
    if len(set(lengths)) != len(lengths) or any(not 1 <= x <= DISTANCES for x in lengths):
        raise ValueError("malformed distance-class list")
    return sum(1 << (x - 1) for x in lengths)


def lengths_from_mask(mask: int) -> list[int]:
    return [x for x in range(1, DISTANCES + 1) if mask & (1 << (x - 1))]


def distance_mask(vertices: tuple[int, ...]) -> int:
    result = 0
    for x, y in itertools.combinations(vertices, 2):
        residue = (x - y) % ORDER
        length = min(residue, ORDER - residue)
        result |= 1 << (length - 1)
    return result


def canonical_translate(vertices: tuple[int, ...]) -> tuple[int, ...]:
    return min(tuple(sorted((x - origin) % ORDER for x in vertices)) for origin in vertices)


def canonical_five_set_orbits() -> Counter[int]:
    """Enumerate one actual five-set per translation orbit, without division."""
    result: Counter[int] = Counter()
    for rest in itertools.combinations(range(1, ORDER), 4):
        vertices = (0, *rest)
        if canonical_translate(vertices) == vertices:
            result[distance_mask(vertices)] += 1
    if sum(result.values()) != 22_386:
        raise AssertionError("expected exactly C(43,5)/43 translation orbits")
    return result


def multiplier_image(mask: int, multiplier: int) -> int:
    image = 0
    for length in lengths_from_mask(mask):
        residue = multiplier * length % ORDER
        image |= 1 << (min(residue, ORDER - residue) - 1)
    return image


def direct_low_objective_scan(frequencies: Counter[int]) -> set[int]:
    """Directly scan all colorings up to color swap, stopping only above one."""
    # High-multiplicity masks first make the exhaustive rejection scan fast.
    # This ordering cannot affect which assignments survive.
    items = sorted(
        frequencies.items(), key=lambda item: (-item[1], item[0].bit_count(), item[0])
    )
    survivors: set[int] = set()
    for red in range(1, STATE_COUNT, 2):  # distance 1 red fixes color swap
        objective = 0
        for mask, multiplicity in items:
            intersection = red & mask
            if intersection == 0 or intersection == mask:
                objective += multiplicity
                if objective > 1:
                    break
        if objective <= 1:
            if objective == 0:
                raise AssertionError("found a zero-clique circulant coloring")
            survivors.add(red)
            survivors.add(FULL_MASK ^ red)
    return survivors


def subset_zeta_histogram(frequencies: Counter[int]) -> Counter[int]:
    """Recompute the certificate's ancillary full objective histogram."""
    zeta = array("I", [0]) * STATE_COUNT
    for mask, multiplicity in frequencies.items():
        zeta[mask] = multiplicity
    for bit in range(DISTANCES):
        flag = 1 << bit
        for mask in range(STATE_COUNT):
            if mask & flag:
                zeta[mask] += zeta[mask ^ flag]
    return Counter(zeta[mask] + zeta[FULL_MASK ^ mask] for mask in range(STATE_COUNT))


def verify(path: Path) -> None:
    document = json.loads(path.read_text())
    expected_header = {
        "format": "circulant43-k5-classification-v1",
        "order": 43,
        "distance_class_count": 21,
        "coloring_count": 2_097_152,
        "five_set_count": 962_598,
        "five_set_translation_orbit_count": 22_386,
        "distinct_distance_masks": 10_437,
        "minimum_monochromatic_five_set_orbits": 1,
        "minimum_monochromatic_K5_count": 43,
        "minimizing_coloring_count": 42,
        "minimizing_red_length_count_histogram": {"10": 21, "11": 21},
        "effective_multiplier_color_swap_group_order": 42,
        "minimizing_symmetry_orbit_count": 1,
        "exoo_red_lengths": list(EXOO_LENGTHS),
        "canonical_from_exoo": {"multiplier": 20, "color_swapped": True},
        "exoo_red_orbits": 1,
        "exoo_blue_orbits": 0,
    }
    for key, value in expected_header.items():
        if document.get(key) != value:
            raise AssertionError(f"certificate header mismatch at {key}")

    frequencies = canonical_five_set_orbits()
    if len(frequencies) != document["distinct_distance_masks"]:
        raise AssertionError("distinct distance-mask count mismatch")
    if Counter(frequencies.values()) != Counter(
        {int(key): value for key, value in document["distance_mask_orbit_multiplicity_histogram"].items()}
    ):
        raise AssertionError("distance-mask multiplicity histogram mismatch")

    certified = document["minimizers"]
    certified_masks = [mask_from_lengths(entry["red_lengths"]) for entry in certified]
    if certified_masks != sorted(set(certified_masks)):
        raise AssertionError("minimizer list is not strictly bitmask-sorted")
    for entry, red in zip(certified, certified_masks, strict=True):
        red_orbits = sum(value for mask, value in frequencies.items() if mask & ~red == 0)
        blue_orbits = sum(value for mask, value in frequencies.items() if mask & red == 0)
        if (red_orbits, blue_orbits) != (entry["red_orbits"], entry["blue_orbits"]):
            raise AssertionError("direct minimizer clique recount mismatch")
        if red_orbits + blue_orbits != 1:
            raise AssertionError("listed minimizer does not have objective one orbit")

    direct_survivors = direct_low_objective_scan(frequencies)
    if direct_survivors != set(certified_masks):
        raise AssertionError("direct exhaustive minimum classification mismatch")

    exoo = mask_from_lengths(EXOO_LENGTHS)
    symmetry_orbit = {
        image
        for multiplier in range(1, DISTANCES + 1)
        for image in (multiplier_image(exoo, multiplier), FULL_MASK ^ multiplier_image(exoo, multiplier))
    }
    if symmetry_orbit != direct_survivors:
        raise AssertionError("the minimizing set is not the Exoo multiplier/color-swap orbit")
    canonical = min(direct_survivors)
    if lengths_from_mask(canonical) != document["canonical_minimizer_red_lengths"]:
        raise AssertionError("canonical minimizer mismatch")
    if FULL_MASK ^ multiplier_image(exoo, 20) != canonical:
        raise AssertionError("declared canonical map from Exoo is incorrect")

    objective_histogram = subset_zeta_histogram(frequencies)
    stored_histogram = Counter(
        {int(key): value for key, value in document["objective_orbit_histogram"].items()}
    )
    if objective_histogram != stored_histogram:
        raise AssertionError("full objective histogram mismatch")
    if sum(objective_histogram.values()) != STATE_COUNT:
        raise AssertionError("objective histogram does not cover every coloring")

    print("PASS independently verified complete circulant K_43 classification")
    print("colorings=2097152 five_set_orbits=22386 distance_masks=10437")
    print("minimum_orbits=1 minimum_K5=43 minimizers=42 symmetry_orbits=1")
    print(f"certificate_sha256={hashlib.sha256(path.read_bytes()).hexdigest()}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    arguments = parser.parse_args()
    verify(arguments.certificate)


if __name__ == "__main__":
    main()
