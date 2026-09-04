#!/usr/bin/env python3
"""Audit the local-extremal deficiency identity for a putative R(5,5;43) graph."""

from __future__ import annotations

import argparse
import hashlib
import io
import itertools
import json
import re
import tarfile
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 43
LOCAL_ORDERS = tuple(range(18, 25))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def graph6_order_and_edges(line: bytes) -> tuple[int, int]:
    data = line.strip()
    if data.startswith(b">>graph6<<"):
        data = data[len(b">>graph6<<") :]
    if not data or data[0] == 126:
        raise ValueError("only short graph6 order headers are expected")
    order = data[0] - 63
    bit_count = order * (order - 1) // 2
    expected_bytes = (bit_count + 5) // 6
    payload = data[1:]
    if len(payload) != expected_bytes:
        raise ValueError((order, len(payload), expected_bytes))
    values = [byte - 63 for byte in payload]
    if any(value < 0 or value > 63 for value in values):
        raise ValueError("invalid graph6 byte")
    padding = 6 * expected_bytes - bit_count
    if padding and values[-1] & ((1 << padding) - 1):
        raise ValueError("nonzero graph6 padding")
    return order, sum(value.bit_count() for value in values)


def load_extrema() -> dict[str, object]:
    document = json.loads((HERE / "extrema.json").read_text(encoding="utf-8"))
    expected = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}
    observed = {int(key): value for key, value in document["max_edges"].items()}
    if observed != expected:
        raise AssertionError((observed, expected))
    return document


def audit_extreme_archive(path: Path, document: dict[str, object]) -> None:
    source = document["sources"]["orders_18_through_23"]
    if sha256(path) != source["sha256"]:
        raise AssertionError("wrong r45extreme archive hash")
    maxima = {int(key): value for key, value in document["max_edges"].items()}
    pattern = re.compile(r"^r45extreme/r45(\d+)\.(\d+)\.g6$")
    with tarfile.open(path, "r:gz") as archive:
        members = {member.name: member for member in archive.getmembers() if member.isfile()}
        labelled_edges: dict[int, list[int]] = {order: [] for order in range(18, 24)}
        for name in members:
            match = pattern.fullmatch(name)
            if match and int(match.group(1)) in labelled_edges:
                labelled_edges[int(match.group(1))].append(int(match.group(2)))
        for order in range(18, 24):
            maximum = maxima[order]
            if max(labelled_edges[order]) != maximum:
                raise AssertionError((order, labelled_edges[order], maximum))
            member_name = f"r45extreme/r45{order}.{maximum}.g6"
            extracted = archive.extractfile(members[member_name])
            if extracted is None:
                raise AssertionError(member_name)
            lines = list(io.BytesIO(extracted.read()))
            if not lines:
                raise AssertionError(f"empty maximum catalog for order {order}")
            for line in lines:
                if graph6_order_and_edges(line) != (order, maximum):
                    raise AssertionError((member_name, line[:20]))


def audit_order24(path: Path, document: dict[str, object]) -> None:
    source = document["sources"]["order_24"]
    if sha256(path) != source["sha256"]:
        raise AssertionError("wrong order-24 catalog hash")
    histogram: Counter[int] = Counter()
    with path.open("rb") as stream:
        for line in stream:
            order, edges = graph6_order_and_edges(line)
            if order != 24:
                raise AssertionError(order)
            histogram[edges] += 1
    if sum(histogram.values()) != source["graph_count"]:
        raise AssertionError(sum(histogram.values()))
    if max(histogram) != document["max_edges"]["24"]:
        raise AssertionError(max(histogram))
    if histogram[max(histogram)] != source["maximum_edge_graph_count"]:
        raise AssertionError(histogram[max(histogram)])


def audit_identity(document: dict[str, object]) -> None:
    maxima = {int(key): value for key, value in document["max_edges"].items()}
    # Three times the number of monochromatic triangles can be apportioned
    # over vertices.  Since 3*C(43,3)/43=861, the contribution of a vertex
    # of red degree d to twice the total local deficiency is the expression
    # below.
    twice_deficiency = {
        degree: 2 * (maxima[degree] + maxima[42 - degree])
        - 2 * 861
        + 3 * degree * (42 - degree)
        for degree in LOCAL_ORDERS
    }
    expected = {18: 8, 19: 17, 20: 26, 21: 29, 22: 26, 23: 17, 24: 8}
    if twice_deficiency != expected:
        raise AssertionError((twice_deficiency, expected))

    # Dynamic programming over all 43-term degree lists verifies the sharp
    # arithmetic maximum subject only to the handshaking parity condition.
    possible = {(0, 0)}
    for _ in range(N):
        possible = {
            ((parity + degree) % 2, total + twice_deficiency[degree])
            for parity, total in possible
            for degree in LOCAL_ORDERS
        }
    maximum_twice = max(total for parity, total in possible if parity == 0)
    if maximum_twice != 1244:
        raise AssertionError(maximum_twice)
    maximum_deficiency = maximum_twice // 2
    if maximum_deficiency != 622:
        raise AssertionError(maximum_deficiency)

    local_sides = 2 * N
    baseline = 7 * local_sides
    exceptional_sides = maximum_deficiency - baseline
    if baseline != 602 or exceptional_sides != 20 or local_sides - exceptional_sides != 66:
        raise AssertionError((baseline, exceptional_sides))

    degree_weights = {
        degree: 29 - twice_deficiency[degree] for degree in LOCAL_ORDERS
    }
    if degree_weights != {18: 21, 19: 12, 20: 3, 21: 0, 22: 3, 23: 12, 24: 21}:
        raise AssertionError(degree_weights)
    # If all 86 local deficiencies are at least seven, then Delta>=602 and
    # 1247 - 2*Delta <= 43 is exactly this weighted degree concentration.
    if 29 * N - 2 * baseline != 43:
        raise AssertionError("wrong hard-case degree budget")
    # The weight is a multiple of three, and it is odd because 1247-2*Delta
    # is odd.  The apparent bound 43 therefore sharpens to 39.
    hard_weight_maximum = 39
    if hard_weight_maximum % 6 != 3 or hard_weight_maximum + 6 <= 43:
        raise AssertionError(hard_weight_maximum)
    if (1247 - hard_weight_maximum) // 2 != 604:
        raise AssertionError("wrong hard-case deficiency minimum")

    # Color complementation sends every degree d to 42-d.  Normalize to at
    # most 451 red edges, hence degree sum at most 902.  Enumerate the small
    # integer-profile superset forced by the weight bound (graphicality and
    # all deeper Ramsey constraints are deliberately not assumed here).
    noncentral_degrees = (18, 19, 20, 22, 23, 24)
    count_ranges = [range(43 // degree_weights[degree] + 1) for degree in noncentral_degrees]
    hard_profiles = []
    for noncentral_counts in itertools.product(*count_ranges):
        used = sum(noncentral_counts)
        if used > N:
            continue
        counts = dict(zip(noncentral_degrees, noncentral_counts, strict=True))
        counts[21] = N - used
        weight = sum(degree_weights[degree] * counts.get(degree, 0) for degree in LOCAL_ORDERS)
        degree_sum = sum(degree * counts.get(degree, 0) for degree in LOCAL_ORDERS)
        if weight <= hard_weight_maximum and degree_sum % 2 == 0 and degree_sum <= 902:
            hard_profiles.append((counts, weight, degree_sum))
    if len(hard_profiles) != 104:
        raise AssertionError(len(hard_profiles))
    weight_histogram = Counter(weight for _, weight, _ in hard_profiles)
    if weight_histogram != Counter({3: 1, 9: 2, 15: 5, 21: 9, 27: 17, 33: 27, 39: 43}):
        raise AssertionError(weight_histogram)
    if (min(item[2] for item in hard_profiles), max(item[2] for item in hard_profiles)) != (890, 902):
        raise AssertionError("wrong normalized degree-sum range")
    maximum_delta_profiles = [
        counts for counts, weight, _ in hard_profiles if (1247 - weight) // 2 == 622
    ]
    if maximum_delta_profiles != [{18: 0, 19: 0, 20: 1, 22: 0, 23: 0, 24: 0, 21: 42}]:
        raise AssertionError(maximum_delta_profiles)

    print("PASS exact R(4,5;k) maxima pinned for k=18,...,24")
    print(
        "PASS twice-deficiency coefficients="
        + ",".join(f"{degree}:{twice_deficiency[degree]}" for degree in LOCAL_ORDERS)
    )
    print("PASS total local deficiency <=622 over 86 color-neighborhoods")
    print("PASS either one deficiency <=6 or at least 66 deficiencies equal 7")
    print("PASS hard-case degree weight <=39 and deficiency >=604")
    print(f"PASS hard-case complement-normalized degree-count profiles={len(hard_profiles)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--extreme-archive", type=Path)
    parser.add_argument("--order24-catalog", type=Path)
    args = parser.parse_args()
    if (args.extreme_archive is None) != (args.order24_catalog is None):
        parser.error("supply both upstream catalog paths or neither")

    document = load_extrema()
    audit_identity(document)
    if args.extreme_archive is not None:
        audit_extreme_archive(args.extreme_archive, document)
        audit_order24(args.order24_catalog, document)
        print("PASS pinned upstream catalogs and graph6 extrema")


if __name__ == "__main__":
    main()
