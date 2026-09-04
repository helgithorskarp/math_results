#!/usr/bin/env python3
"""Fetch and audit the external small-Ramsey catalog inputs used here."""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
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
R45_ARCHIVE_URL = BASE_URL + "r45extreme.tar.gz"
R45_MAXIMUM_EXPECTED = {
    14: (60, 1, "752aa8b1509075bc39cb1151936b250c681fbdf0a9fdda20d8d5bbb6e6356c62"),
    15: (66, 1, "128419e4c94b2b187d51b05ec25d00b86f396eeb82d112d8e0b9666f595fdc93"),
    16: (72, 5, "794848d5ad48e715a02ef96b375077838fea85ed64c8152d3b1a8f6e8024d889"),
    17: (79, 1, "5a572caf1a35b7a45753c754f11e83b65a716a8e21db20680d4b67a637c158b6"),
    18: (85, 74, "46abaee2572d06bba1e594554809d784be60f8f60b9b0d3345b8bf3dd800810a"),
}


def audit_r35() -> None:
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
        for encoded in lines:
            adjacency = decode_short_graph6(encoded)
            if len(adjacency) != order:
                raise AssertionError("wrong graph order")
            if contains_clique(adjacency, 3):
                raise AssertionError("catalog graph is not triangle-free")
            if contains_clique(complement_adjacency(adjacency), 5):
                raise AssertionError("catalog graph has an independent five-set")
            histogram[core_edge_count(adjacency)] += 1
        if dict(sorted(histogram.items())) != expected_histogram:
            raise AssertionError((order, histogram))


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
    audit_r35()
    audit_r45_extremal()
    print("PASS official R(3,5) catalog counts=105,12,1 minima=15,20,26")
    print("PASS official R(4,5) maxima at orders 14,...,18 are 60,66,72,79,85")
    print("PASS official extremal R(4,5;14,60) catalog is the pinned singleton")


if __name__ == "__main__":
    main()
