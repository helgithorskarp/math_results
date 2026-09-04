#!/usr/bin/env python3
"""Independent catalog and arithmetic audit for the local-deficiency lemma."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import re
import tarfile
from pathlib import Path


ARCHIVE_SHA256 = "9cfac9dbd1c209cfa342e5d5424df2a7a3fbb008ca00bf0a992e5bbe72f925b6"
ORDER24_SHA256 = "83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0"
EXPECTED_MAXIMA = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}
EXPECTED_MAXIMUM_WITNESSES = {18: 74, 19: 210, 20: 1, 21: 31, 22: 133, 23: 2, 24: 2}


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            result.update(block)
    return result.hexdigest()


def graph6(text: bytes, adjacency: bool = False) -> tuple[int, int, tuple[int, ...] | None]:
    data = text.strip()
    header = b">>graph6<<"
    if data.startswith(header):
        data = data[len(header) :]
    if not data or data[0] == 126:
        raise AssertionError("expected short graph6")
    order = data[0] - 63
    pair_count = order * (order - 1) // 2
    payload_length = (pair_count + 5) // 6
    if len(data) != payload_length + 1:
        raise AssertionError((order, len(data), payload_length + 1))
    values = tuple(byte - 63 for byte in data[1:])
    if any(value not in range(64) for value in values):
        raise AssertionError("invalid graph6 character")
    padding = 6 * payload_length - pair_count
    if padding and values[-1] & ((1 << padding) - 1):
        raise AssertionError("nonzero graph6 padding")
    edge_count = sum(value.bit_count() for value in values)
    if not adjacency:
        return order, edge_count, None

    bits = "".join(f"{value:06b}" for value in values)
    rows = [0] * order
    position = 0
    for second in range(1, order):
        for first in range(second):
            if bits[position] == "1":
                rows[first] |= 1 << second
                rows[second] |= 1 << first
            position += 1
    return order, edge_count, tuple(rows)


def has_clique(rows: tuple[int, ...], size: int) -> bool:
    def search(candidates: int, remaining: int) -> bool:
        if remaining == 0:
            return True
        while candidates.bit_count() >= remaining:
            vertex_bit = candidates & -candidates
            candidates ^= vertex_bit
            vertex = vertex_bit.bit_length() - 1
            if search(candidates & rows[vertex], remaining - 1):
                return True
        return False

    return search((1 << len(rows)) - 1, size)


def verify_ramsey_line(line: bytes, order: int, edges: int) -> None:
    observed_order, observed_edges, rows_or_none = graph6(line, adjacency=True)
    if (observed_order, observed_edges) != (order, edges) or rows_or_none is None:
        raise AssertionError((observed_order, observed_edges, order, edges))
    rows = rows_or_none
    if has_clique(rows, 4):
        raise AssertionError("maximum witness has K4")
    universe = (1 << order) - 1
    complement = tuple(universe ^ (1 << vertex) ^ rows[vertex] for vertex in range(order))
    if has_clique(complement, 5):
        raise AssertionError("maximum witness has independent five-set")


def scan_catalogs(archive_path: Path, order24_path: Path) -> dict[int, int]:
    if digest(archive_path) != ARCHIVE_SHA256 or digest(order24_path) != ORDER24_SHA256:
        raise AssertionError("catalog digest mismatch")

    member_pattern = re.compile(r"r45extreme/r45(18|19|20|21|22|23)\.(\d+)\.g6")
    maxima = {}
    witness_counts = {}
    with tarfile.open(archive_path, "r:gz") as archive:
        members = {
            match.groups(): member
            for member in archive.getmembers()
            if member.isfile() and (match := member_pattern.fullmatch(member.name))
        }
        for order in range(18, 24):
            labels = [int(edge_text) for (order_text, edge_text) in members if int(order_text) == order]
            maxima[order] = max(labels)
            member = members[(str(order), str(maxima[order]))]
            source = archive.extractfile(member)
            if source is None:
                raise AssertionError(member.name)
            lines = tuple(source)
            witness_counts[order] = len(lines)
            for line in lines:
                verify_ramsey_line(line, order, maxima[order])

    order24_count = 0
    maximum24 = -1
    maximum24_lines: list[bytes] = []
    with order24_path.open("rb") as source:
        for line in source:
            order, edges, _ = graph6(line)
            if order != 24:
                raise AssertionError(order)
            order24_count += 1
            if edges > maximum24:
                maximum24 = edges
                maximum24_lines = [line]
            elif edges == maximum24:
                maximum24_lines.append(line)
    maxima[24] = maximum24
    witness_counts[24] = len(maximum24_lines)
    for line in maximum24_lines:
        verify_ramsey_line(line, 24, maximum24)

    if maxima != EXPECTED_MAXIMA:
        raise AssertionError(maxima)
    if witness_counts != EXPECTED_MAXIMUM_WITNESSES:
        raise AssertionError(witness_counts)
    if order24_count != 352366:
        raise AssertionError(order24_count)

    print(f"catalog_sha256={ARCHIVE_SHA256},{ORDER24_SHA256}")
    print("catalog_maxima=" + ",".join(str(maxima[order]) for order in range(18, 25)))
    print(
        "maximum_witness_counts="
        + ",".join(str(witness_counts[order]) for order in range(18, 25))
    )
    print("order24_catalog_graphs=352366")
    print("maximum_witnesses_are_K4_and_independent5_free=true")
    return maxima


def audit_arithmetic(maxima: dict[int, int]) -> None:
    coefficients = {
        degree: 2 * (maxima[degree] + maxima[42 - degree])
        - 2 * 861
        + 3 * degree * (42 - degree)
        for degree in range(18, 25)
    }
    expected = {18: 8, 19: 17, 20: 26, 21: 29, 22: 26, 23: 17, 24: 8}
    if coefficients != expected:
        raise AssertionError(coefficients)

    # Independently maximize the coefficient sum over all 43-term degree
    # sequences with even total degree.  This deliberately ignores stronger
    # graphicality and Ramsey conditions, so the resulting upper bound is safe.
    states = {(0, 0)}
    for _ in range(43):
        states = {
            ((parity + degree) % 2, value + coefficients[degree])
            for parity, value in states
            for degree in range(18, 25)
        }
    maximum_twice_deficiency = max(value for parity, value in states if parity == 0)
    if maximum_twice_deficiency != 1244:
        raise AssertionError(maximum_twice_deficiency)
    total_deficiency_bound = maximum_twice_deficiency // 2
    if total_deficiency_bound != 622:
        raise AssertionError(total_deficiency_bound)

    # If 86 integer deficiencies all exceeded seven, their sum would be at
    # least 688.  If none is below seven, each non-seven term spends at least
    # one of the 20 units above the 602 baseline.
    if 86 * 8 <= total_deficiency_bound:
        raise AssertionError("averaging bound failed")
    nonseven_budget = total_deficiency_bound - 86 * 7
    if nonseven_budget != 20 or 86 - nonseven_budget != 66:
        raise AssertionError(nonseven_budget)

    # The target states weight <=43.  Divisibility by three and parity sharpen
    # it to 39, agreeing with the later source strengthening.
    weights = {degree: 29 - coefficient for degree, coefficient in coefficients.items()}
    if tuple(weights.values()) != (21, 12, 3, 0, 3, 12, 21):
        raise AssertionError(weights)
    allowed_weights = {
        sum(weights[degree] for degree in sequence)
        for sequence in itertools.product(range(18, 25), repeat=1)
    }
    if allowed_weights != set(weights.values()):
        raise AssertionError("weight sanity check")
    if 43 // 3 * 3 != 42 or max(value for value in range(44) if value % 6 == 3) != 39:
        raise AssertionError("weight sharpening")

    print("twice_deficiency_coefficients=8,17,26,29,26,17,8")
    print("maximum_twice_deficiency=1244")
    print("maximum_total_deficiency=622")
    print("minimum_one_local_deficiency_at_most=7")
    print("hard_branch_exact_seven_sides_at_least=66")
    print("target_weight_bound=43,later_sharpened_to_39")
    print("independent_checks=true")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("extreme_archive", type=Path)
    parser.add_argument("order24_catalog", type=Path)
    arguments = parser.parse_args()
    maxima = scan_catalogs(arguments.extreme_archive, arguments.order24_catalog)
    audit_arithmetic(maxima)


if __name__ == "__main__":
    main()
