#!/usr/bin/env python3
"""Fetch and audit the external small-Ramsey catalog inputs used here."""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
from pathlib import Path
import tarfile
from urllib.request import urlopen

from verify_anchor_propagation import (
    EXTREMAL_R4514_G6,
    complement_adjacency,
    core_edge_count,
    decode_short_graph6,
)


BASE_URL = "https://users.cecs.anu.edu.au/~bdm/data/"
R35_EXPECTED = {
    9: (
        290,
        "3246c40dc444a248ae9199625abe16a984f630cf3d5f1ff1528e4409ff0c80cb",
        {
            7: 1, 8: 3, 9: 11, 10: 28, 11: 59, 12: 73,
            13: 62, 14: 33, 15: 14, 16: 4, 17: 2,
        },
    ),
    10: (
        313,
        "194d2f95511f562e44a4137b1b91633f182e2adb14e7ea6880fa1b052bcbb3bb",
        {
            10: 1, 11: 2, 12: 10, 13: 32, 14: 69, 15: 86,
            16: 65, 17: 32, 18: 12, 19: 3, 20: 1,
        },
    ),
    11: (
        105,
        "d5c52b2209e25080868adeef2dd52fa32835e5143208aceef129332c9184f16e",
        {15: 1, 16: 6, 17: 19, 18: 31, 19: 30, 20: 13, 21: 4, 22: 1},
    ),
    12: (
        12,
        "322e7a54e67f4201bd37998ab420afb3eee41b1dcd6b277b7f055bda152da95e",
        {20: 1, 21: 2, 22: 5, 23: 2, 24: 2},
    ),
    13: (
        1,
        "eb4d3f787f07ed14c0a82a83bee170ed096c24b6a7e971fded185ca1a760798f",
        {26: 1},
    ),
}


def contains_clique(adjacency, size: int) -> bool:
    return any(
        all(adjacency[first][second]
            for first, second in itertools.combinations(vertices, 2))
        for vertices in itertools.combinations(range(len(adjacency)), size)
    )


def independent_four_transversal_number(adjacency) -> int:
    """Return the minimum number of vertices hitting every independent 4-set."""
    order = len(adjacency)
    independent_fours = tuple(
        sum(1 << vertex for vertex in vertices)
        for vertices in itertools.combinations(range(order), 4)
        if not any(
            adjacency[first][second]
            for first, second in itertools.combinations(vertices, 2)
        )
    )
    for size in range(order + 1):
        for vertices in itertools.combinations(range(order), size):
            transversal = sum(1 << vertex for vertex in vertices)
            if all(transversal & independent for independent in independent_fours):
                return size
    raise AssertionError("finite set family has no transversal")
R45_ARCHIVE_URL = BASE_URL + "r45extreme.tar.gz"
R45_MAXIMUM_EXPECTED = {
    14: (60, 1, "752aa8b1509075bc39cb1151936b250c681fbdf0a9fdda20d8d5bbb6e6356c62"),
    15: (66, 1, "128419e4c94b2b187d51b05ec25d00b86f396eeb82d112d8e0b9666f595fdc93"),
    16: (72, 5, "794848d5ad48e715a02ef96b375077838fea85ed64c8152d3b1a8f6e8024d889"),
    17: (79, 1, "5a572caf1a35b7a45753c754f11e83b65a716a8e21db20680d4b67a637c158b6"),
    18: (85, 74, "46abaee2572d06bba1e594554809d784be60f8f60b9b0d3345b8bf3dd800810a"),
    19: (92, 210, "ed07d7e9cc6d56770a3f2814c540f8d34bb26f9fd702cf540d160306fd8e9d57"),
}


def audit_r35() -> dict[int, tuple[tuple[int, int], ...]]:
    catalog_records = {}
    for order, (expected_count, expected_digest, expected_histogram) in (
        R35_EXPECTED.items()
    ):
        with urlopen(BASE_URL + f"r35_{order}.g6", timeout=60) as response:
            raw = response.read()
        if hashlib.sha256(raw).hexdigest() != expected_digest:
            raise AssertionError(f"order-{order} R(3,5) catalog digest changed")
        lines = raw.decode("ascii").splitlines()
        if len(lines) != expected_count or len(lines) != len(set(lines)):
            raise AssertionError(f"order-{order} R(3,5) catalog count")
        histogram = Counter()
        records = []
        for encoded in lines:
            adjacency = decode_short_graph6(encoded)
            if len(adjacency) != order:
                raise AssertionError("wrong graph order")
            if contains_clique(adjacency, 3):
                raise AssertionError("catalog graph is not triangle-free")
            if contains_clique(complement_adjacency(adjacency), 5):
                raise AssertionError("catalog graph has an independent five-set")
            edge_count = core_edge_count(adjacency)
            histogram[edge_count] += 1
            records.append(
                (edge_count, independent_four_transversal_number(adjacency))
            )
        if dict(sorted(histogram.items())) != expected_histogram:
            raise AssertionError((order, histogram))
        catalog_records[order] = tuple(records)
    cover_spectra = {
        order: dict(sorted(Counter(cover for _, cover in records).items()))
        for order, records in catalog_records.items()
    }
    if cover_spectra != {
        9: {1: 26, 2: 263, 3: 1},
        10: {2: 197, 3: 116},
        11: {3: 105},
        12: {4: 12},
        13: {5: 1},
    }:
        raise AssertionError(cover_spectra)
    return catalog_records


def audit_residual_menu(
    catalog_records: dict[int, tuple[tuple[int, int], ...]]
) -> None:
    """Rebuild the menu directly from catalog records, not histograms."""
    r55_minimum_edges = {20: 50, 21: 56}
    partitions = {
        23: ((10, 13), (11, 12)),
        22: ((9, 13), (10, 12), (11, 11)),
    }
    case_specs = (
        (23, 219, "red"),
        (23, 219, "blue"),
        (23, 220, "red"),
        (23, 220, "blue"),
        (22, 220, "red"),
        (22, 220, "blue"),
    )
    expected_lines = [
        "# d M disconnected_color component_orders opposite_edges_D "
        "opposite_edges_outside candidate_unordered_type_pairs\n"
    ]
    for backbone_order, cross_total, disconnected_color in case_specs:
        outside_order = 43 - backbone_order
        outside_minimum = r55_minimum_edges[outside_order]
        outside_maximum = outside_order * (outside_order - 1) // 2 - outside_minimum
        global_totals = {"red": 231 + cross_total, "blue": 672 - cross_total}
        opposite_color = "blue" if disconnected_color == "red" else "red"
        for first_order, second_order in partitions[backbone_order]:
            if first_order == second_order:
                record_pairs = itertools.combinations_with_replacement(
                    catalog_records[first_order], 2
                )
            else:
                record_pairs = itertools.product(
                    catalog_records[first_order],
                    catalog_records[second_order],
                )
            counts = Counter()
            for (first_edges, first_cover), (second_edges, second_cover) in record_pairs:
                first_cross_edges = (
                    first_order * (first_order + 21 - backbone_order)
                    - 2 * first_edges
                )
                second_cross_edges = (
                    second_order * (second_order + 21 - backbone_order)
                    - 2 * second_edges
                )
                if (
                    first_cross_edges < outside_order * first_cover
                    or second_cross_edges < outside_order * second_cover
                ):
                    continue
                counts[
                    first_order * second_order + first_edges + second_edges
                ] += 1
            for opposite_edges, type_pairs in sorted(counts.items()):
                outside_edges = (
                    global_totals[opposite_color]
                    + opposite_edges
                    - 21 * backbone_order
                )
                if outside_minimum <= outside_edges <= outside_maximum:
                    expected_lines.append(
                        f"{backbone_order} {cross_total} {disconnected_color} "
                        f"{first_order}+{second_order} {opposite_edges} "
                        f"{outside_edges} {type_pairs}\n"
                    )
    actual = Path(__file__).with_name(
        "RESIDUAL_COMPONENT_MENUS.tsv"
    ).read_text(encoding="ascii")
    if actual != "".join(expected_lines):
        raise AssertionError("official catalog records do not reproduce residual menu")


def audit_r45_extremal() -> None:
    wanted = {
        f"r45extreme/r45{order}.{maximum}.g6": order
        for order, (maximum, _, _) in R45_MAXIMUM_EXPECTED.items()
    }
    members = {}
    with urlopen(R45_ARCHIVE_URL, timeout=120) as response:
        with tarfile.open(fileobj=response, mode="r|gz") as archive:
            for member in archive:
                if member.name in wanted:
                    extracted = archive.extractfile(member)
                    if extracted is None:
                        raise AssertionError("extremal catalog member is not a file")
                    members[wanted[member.name]] = extracted.read()
    if set(members) != set(R45_MAXIMUM_EXPECTED):
        raise AssertionError("an extremal R(4,5) catalog member is missing")
    for order, raw in members.items():
        maximum, expected_count, expected_digest = R45_MAXIMUM_EXPECTED[order]
        if hashlib.sha256(raw).hexdigest() != expected_digest:
            raise AssertionError(f"extremal order-{order} catalog digest changed")
        lines = raw.decode("ascii").splitlines()
        if len(lines) != expected_count or len(lines) != len(set(lines)):
            raise AssertionError(f"extremal order-{order} catalog count")
        for encoded in lines:
            adjacency = decode_short_graph6(encoded)
            if len(adjacency) != order or core_edge_count(adjacency) != maximum:
                raise AssertionError("wrong extremal graph parameters")
            if contains_clique(adjacency, 4):
                raise AssertionError("extremal graph contains K4")
            if contains_clique(complement_adjacency(adjacency), 5):
                raise AssertionError("extremal graph has an independent five-set")
    if members[14].decode("ascii").splitlines() != [EXTREMAL_R4514_G6]:
        raise AssertionError("extremal R(4,5;14) catalog is not the pinned singleton")


def main() -> None:
    catalog_records = audit_r35()
    audit_residual_menu(catalog_records)
    audit_r45_extremal()
    print("PASS official R(3,5) catalog counts=290,313,105,12,1 "
          "minima=7,10,15,20,26")
    print("PASS official R(4,5) maxima at orders 14,...,19 are "
          "60,66,72,79,85,92")
    print("PASS official extremal R(4,5;14,60) catalog is the pinned singleton")
    print("PASS official R(3,5) records and independent-4 covers reproduce menu")


if __name__ == "__main__":
    main()
